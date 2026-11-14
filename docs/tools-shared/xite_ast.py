"""AST of the rebuilt X_ITE 16.7.0 source (TypeScript parser via jsast.cjs) and a module dependency graph.

Inside the webpack bundle each module's default export is a const named <Dir>_<File> (e.g. Lighting_X3DLightNode) and the
component bundles reach the core through external_X_ITE_X3D_<Name>_default(). A call whose first segment is such a name is a
reference to that module. Writes xite/data/head.json in the same shape as repo_ast.snapshot (code + scenes)."""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "xite" / "src"
EXPORT = re.compile(r"harmony default export \*/ const (\w+) =")


def role(path):
    p = path
    if p.startswith(("src/lib/", "node_modules/")):
        return "vendor"
    if p.startswith("src/x_ite/Components/") and not p.endswith("Component.js"):
        return "nodes"
    if p.startswith("src/x_ite/Browser/"):
        return "browser"
    if p.startswith("src/x_ite/Parser/"):
        return "parser"
    if p.startswith(("src/x_ite/Rendering/", "src/assets/shaders/")):
        return "rendering"
    if p.startswith("src/standard/"):
        return "math"
    if p.startswith(("src/x_ite/Fields", "src/x_ite/Base/", "src/x_ite/Execution/", "src/x_ite/Prototype/", "src/x_ite/Routing/",
                     "src/x_ite/Configuration/", "src/x_ite/InputOutput/")):
        return "core"
    return "api"


def main():
    files = {str(p.relative_to(SRC)): p.read_text() for p in sorted(SRC.rglob("*.js")) if p.is_file()}
    code_files = {k: v for k, v in files.items() if role(k) != "vendor"}
    with tempfile.TemporaryDirectory() as td:
        inp, outp = pathlib.Path(td) / "in.json", pathlib.Path(td) / "out.json"
        inp.write_text(json.dumps({k: {"name": k, "text": v} for k, v in code_files.items()}))
        subprocess.run(["node", str(ROOT / "tools" / "jsast.cjs"), str(inp), str(outp)], check=True)
        res = json.loads(outp.read_text())
    sym = {}
    for path, text in code_files.items():
        for s in EXPORT.findall(text):
            sym[s] = path
    by_stem = {}
    for path in code_files:
        by_stem.setdefault(pathlib.Path(path).stem, path)
    edges = 0
    for path, r in res.items():
        r.update(lang="js", role=role(path), sha=None)
        deps = set()
        for f in r["functions"]:
            out = set()
            for c in f["calls"]:
                head = c.split(".")[0].split("(")[0]
                tgt = sym.get(head)
                if not tgt:
                    m = re.match(r"external_X_ITE_X3D_(\w+)_default", head)
                    if m:
                        tgt = by_stem.get(m.group(1))
                if tgt and tgt != path:
                    out.add(tgt + "::<module>")
                    deps.add(tgt)
            f["resolved"] = sorted(out)
            edges += len(out)
        r["deps"] = sorted(deps)
    head = {"code": res, "scenes": {}, "vendored_files": sum(1 for k in files if role(k) == "vendor")}
    (ROOT / "xite" / "data" / "head.json").write_text(json.dumps(head))
    fs = [f for r in res.values() for f in r["functions"] if f["qualname"] != "<module>"]
    print("modules", len(res), "loc", sum(r["loc"] for r in res.values()), "functions", len(fs), "module-level deps", sum(len(r["deps"]) for r in res.values()),
          "fn->module edges", edges, "exports mapped", len(sym), "parse errors", sum(1 for r in res.values() if r.get("parse_errors")),
          "skipped", [(k, r["skipped"]) for k, r in res.items() if r.get("skipped")][:4])
    named = [f for f in fs if "." in f["qualname"]]
    print("prototype-qualified methods", len(named), "e.g.", [f["qualname"] for f in named[:6]])


if __name__ == "__main__":
    main()
