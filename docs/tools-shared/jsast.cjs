// JS/TS/MJS/TSX and inline <script> AST extractor using the TypeScript compiler API (parse only, nothing executed).
// usage: node jsast.cjs IN.json OUT.json      IN = {key: {name, text}}   OUT = {key: result}
// The TypeScript package is the one already installed for x3d-physx-bridge (5.9.3); nothing was installed for this.
const ts = require("/Users/handshake/Projects/x3d/work/x3d-physx-bridge/node_modules/typescript");
const fs = require("fs");
const crypto = require("crypto");
const [, , inPath, outPath] = process.argv;
const vocab = JSON.parse(fs.readFileSync(__dirname + "/../cache/x3dvocab.json", "utf8"));
const NODES = new Set(vocab.nodes);
const TAG_RE = /<\s*([A-Z][A-Za-z0-9]*)/g;
const K = ts.SyntaxKind;
const DECISION = new Set([K.IfStatement, K.ConditionalExpression, K.ForStatement, K.ForInStatement, K.ForOfStatement,
  K.WhileStatement, K.DoStatement, K.CatchClause, K.CaseClause]);
const BOOL_OPS = new Set([K.AmpersandAmpersandToken, K.BarBarToken, K.QuestionQuestionToken]);

function kindOf(name) {
  if (/\.tsx$/i.test(name)) return ts.ScriptKind.TSX;
  if (/\.ts$/i.test(name)) return ts.ScriptKind.TS;
  return ts.ScriptKind.JS;
}

function inlineScripts(html) {
  // inline classic and module scripts (no src=), placed at their HTML line numbers
  const out = [];
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1];
    if (/\bsrc\s*=/.test(attrs)) continue;
    const t = attrs.match(/type\s*=\s*["']([^"']+)["']/i);
    if (t && !/^(module|text\/javascript|application\/javascript)$/i.test(t[1])) continue; // json, shaders, importmaps
    const startLine = html.slice(0, m.index + m[0].indexOf(">") + 1).split("\n").length - 1;
    out.push({ startLine, code: m[2] });
  }
  return out;
}

function analyse(name, text) {
  let code = text;
  const isHtml = /\.html?$/i.test(name);
  if (isHtml) {
    const parts = inlineScripts(text);
    if (!parts.length) return { skipped: "no inline script", loc: 0, functions: [], imports: [], classes: [] };
    const lines = [];
    for (const p of parts) { while (lines.length < p.startLine) lines.push(""); lines.push(...p.code.split("\n")); }
    code = lines.join("\n");
  }
  const nonEmpty = code.split("\n").filter(l => l.trim());
  const avg = nonEmpty.length ? nonEmpty.reduce((a, l) => a + l.length, 0) / nonEmpty.length : 0;
  if (code.length > 40000000)
    return { skipped: `too large (${code.length} chars)`, loc: nonEmpty.length, functions: [], imports: [], classes: [] };
  const sf = ts.createSourceFile(name, code, ts.ScriptTarget.Latest, true, isHtml ? ts.ScriptKind.JS : kindOf(name));
  const line = n => sf.getLineAndCharacterOfPosition(n.getStart(sf)).line + 1;
  const endLine = n => sf.getLineAndCharacterOfPosition(n.getEnd()).line + 1;
  const functions = [], imports = [], classes = [];
  const isFn = n => ts.isFunctionDeclaration(n) || ts.isMethodDeclaration(n) || ts.isArrowFunction(n) || ts.isFunctionExpression(n)
    || ts.isConstructorDeclaration(n) || ts.isGetAccessorDeclaration(n) || ts.isSetAccessorDeclaration(n);

  function protoOwner(n) {
    // X_ITE style: Object.assign (Object.setPrototypeOf (X.prototype, B.prototype), { method () {} }) -> "X"
    let o = n.parent;
    if (ts.isPropertyAssignment(o)) o = o.parent;
    if (!o || !ts.isObjectLiteralExpression(o) || !o.parent || !ts.isCallExpression(o.parent)) return null;
    const first = o.parent.arguments[0];
    if (!first || first === o) return null;
    const m = first.getText(sf).match(/(\w+)\s*\.prototype/) || first.getText(sf).match(/^(\w+)$/);
    return m ? m[1] : null;
  }
  function fnName(n) {
    const own = (ts.isMethodDeclaration(n) || (n.parent && ts.isPropertyAssignment(n.parent))) ? protoOwner(n) : null;
    if (own) { const b = n.name ? n.name.text : (n.parent.name ? n.parent.name.text : null); if (b) return own + "." + b; }
    if (n.name && (ts.isIdentifier(n.name) || ts.isStringLiteral(n.name) || ts.isPrivateIdentifier(n.name))) return n.name.text;
    if (ts.isConstructorDeclaration(n)) return "constructor";
    const p = n.parent;
    if (p && ts.isVariableDeclaration(p) && ts.isIdentifier(p.name)) return p.name.text;
    if (p && ts.isPropertyAssignment(p) && p.name && (ts.isIdentifier(p.name) || ts.isStringLiteral(p.name))) return p.name.text;
    if (p && ts.isPropertyDeclaration(p) && p.name && ts.isIdentifier(p.name)) return p.name.text;
    if (p && ts.isBinaryExpression(p) && p.operatorToken.kind === K.EqualsToken) return p.left.getText(sf).replace(/\s+/g, "").slice(0, 60);
    return null; // anonymous callback: folded into the enclosing function
  }
  function calleeName(e) {
    if (ts.isIdentifier(e)) return e.text;
    if (ts.isPropertyAccessExpression(e)) return (calleeName(e.expression) || "?") + "." + e.name.text;
    if (ts.isElementAccessExpression(e)) return (calleeName(e.expression) || "?") + ".[]";
    if (e.kind === K.ThisKeyword) return "this";
    if (ts.isCallExpression(e)) return (calleeName(e.expression) || "?") + "()";
    return null;
  }
  function literalCtx(n) {
    const p = n.parent;
    if (!p) return "other";
    if (ts.isCaseClause(p)) return "case";
    if (ts.isBinaryExpression(p) && [K.EqualsEqualsEqualsToken, K.EqualsEqualsToken, K.ExclamationEqualsEqualsToken].includes(p.operatorToken.kind)) return "compare";
    if (ts.isPropertyAssignment(p) && p.name === n) return "key";
    if (ts.isCallExpression(p)) return "call:" + (calleeName(p.expression) || "?").split(".").pop();
    if (ts.isArrayLiteralExpression(p)) return "collection";
    return "other";
  }
  function note(n, t) {
    if (DECISION.has(n.kind)) t.cc++;
    else if (ts.isBinaryExpression(n) && BOOL_OPS.has(n.operatorToken.kind)) t.cc++;
    if (ts.isCallExpression(n) || ts.isNewExpression(n)) { const c = calleeName(n.expression); if (c) t.calls.push(c); }
    if (ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n)) {
      if (NODES.has(n.text)) t.x3d.push([n.text, literalCtx(n)]);
      else if (n.text.includes("<")) for (const m of n.text.matchAll(TAG_RE)) if (NODES.has(m[1])) t.x3d.push([m[1], "emit-tag"]);
    }
    if (ts.isTemplateHead(n) || ts.isTemplateMiddle(n) || ts.isTemplateTail(n))
      for (const m of n.text.matchAll(TAG_RE)) if (NODES.has(m[1])) t.x3d.push([m[1], "emit-tag"]);
    if ((ts.isPropertyAssignment(n) || ts.isMethodDeclaration(n)) && n.name && ts.isIdentifier(n.name) && /^[A-Z]/.test(n.name.text) && NODES.has(n.name.text))
      t.x3d.push([n.name.text, "key"]);
  }

  function visitFn(fn, prefix, cls, owner) {
    const name = fnName(fn);
    const qual = name ? prefix + name : null;
    const rec = qual ? { qualname: qual, name, class: cls, line: line(fn), end: endLine(fn), cc: 1, depth: 0, calls: [], x3d: [] } : null;
    const target = rec || owner; // anonymous callbacks are charged to whoever encloses them
    function walk(n, depth) {
      if (n !== fn && isFn(n)) { visitFn(n, qual ? qual + "." : prefix, cls, target); return; }
      if (n !== fn && ts.isClassLike(n)) { visitClass(n, qual ? qual + "." : prefix); return; }
      if (n !== fn) note(n, target);
      const nest = ts.isIfStatement(n) || ts.isForStatement(n) || ts.isForOfStatement(n) || ts.isForInStatement(n)
        || ts.isWhileStatement(n) || ts.isDoStatement(n) || ts.isSwitchStatement(n) || ts.isTryStatement(n);
      const elif = ts.isIfStatement(n) && n.parent && ts.isIfStatement(n.parent) && n.parent.elseStatement === n;
      const d = nest && !elif ? depth + 1 : depth;
      if (rec && d > rec.depth) rec.depth = d;
      ts.forEachChild(n, c => walk(c, d));
    }
    walk(fn, 0);
    if (rec) {
      rec.loc = rec.end - rec.line + 1;
      rec.hash = crypto.createHash("sha1").update(fn.getText(sf).replace(/\s+/g, " ")).digest("hex").slice(0, 12);
      functions.push(rec);
    }
  }
  function visitClass(c, prefix) {
    const cname = c.name ? c.name.text : (c.parent && ts.isVariableDeclaration(c.parent) && ts.isIdentifier(c.parent.name) ? c.parent.name.text : "<class>");
    const bases = (c.heritageClauses || []).flatMap(h => h.types.map(t => t.expression.getText(sf)));
    classes.push({ name: prefix + cname, line: line(c), bases });
    for (const m of c.members) {
      if (isFn(m)) visitFn(m, prefix + cname + ".", prefix + cname, null);
      else if (ts.isPropertyDeclaration(m) && m.initializer && isFn(m.initializer)) visitFn(m.initializer, prefix + cname + ".", prefix + cname, null);
    }
  }
  // module top level: "<module>" collects top-level calls and literals
  const top = { qualname: "<module>", name: "<module>", class: null, line: 1, end: 1, cc: 1, depth: 0, calls: [], x3d: [] };
  function walkTop(n) {
    if (ts.isImportDeclaration(n) && ts.isStringLiteral(n.moduleSpecifier)) {
      const names = [];
      const ic = n.importClause;
      if (ic && ic.name) names.push(["default", ic.name.text]);
      if (ic && ic.namedBindings) {
        if (ts.isNamespaceImport(ic.namedBindings)) names.push(["*", ic.namedBindings.name.text]);
        else for (const e of ic.namedBindings.elements) names.push([(e.propertyName || e.name).text, e.name.text]);
      }
      imports.push({ spec: n.moduleSpecifier.text, names, lazy: false });
      return;
    }
    if (ts.isCallExpression(n) && n.expression.kind === K.ImportKeyword && n.arguments[0] && ts.isStringLiteral(n.arguments[0]))
      imports.push({ spec: n.arguments[0].text, names: [], lazy: true });
    if (isFn(n)) { visitFn(n, "", null, top); return; }
    if (ts.isClassLike(n)) { visitClass(n, ""); return; }
    note(n, top);
    ts.forEachChild(n, walkTop);
  }
  ts.forEachChild(sf, walkTop);
  top.loc = 0; top.hash = "module";
  if (top.calls.length || top.x3d.length) functions.push(top);
  // a bundle inlined into a page (Babylon, X_ITE ...) shows up as many one- or two-letter function names
  const named = functions.filter(f => f.name !== "<module>");
  const short = named.filter(f => f.name.length <= 2).length;
  if (named.length >= 40 && short / named.length > 0.35)
    return { skipped: `minified bundle inlined (${short} of ${named.length} functions have 1-2 letter names)`, loc: nonEmpty.length, functions: [], imports, classes: [] };
  const longLines = code.split("\n").filter(l => l.length > 2000).length;
  return { loc: nonEmpty.length, functions, imports, classes, parse_errors: (sf.parseDiagnostics || []).length, data_lines: longLines };
}

const input = JSON.parse(fs.readFileSync(inPath, "utf8"));
const out = {};
for (const [key, { name, text }] of Object.entries(input)) {
  try { out[key] = analyse(name, text); }
  catch (e) { out[key] = { error: String(e).slice(0, 200), loc: 0, functions: [], imports: [], classes: [] }; }
}
fs.writeFileSync(outPath, JSON.stringify(out));
