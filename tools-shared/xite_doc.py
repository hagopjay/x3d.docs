"""MASTERCLASS.md and index.html for X_ITE 16.7.0, built from xite/data/*.json."""
import html
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
X = ROOT / "xite"
N = json.load(open(X / "data" / "nodes.json"))
L = json.load(open(X / "data" / "learn.json"))
H = json.load(open(X / "data" / "head.json"))
SS = json.load(open(X / "data" / "scene_stats.json"))
XS = json.load(open(X / "data" / "xite_scene_stats.json"))
MOD = json.load(open(X / "data" / "modules.json"))
C = H["code"]
GH = "https://github.com/create3000/x_ite/blob/16.7.0/"


def stem(p):
    return pathlib.Path(p).stem


roles = Counter()
for p, r in C.items():
    roles[r["role"]] += r["loc"]
fs = [f for r in C.values() for f in r["functions"] if f["qualname"] != "<module>"]
top_cc = sorted(((f["cc"], p, f["qualname"], f.get("loc")) for p, r in C.items() for f in r["functions"] if f["qualname"] != "<module>"), reverse=True)[:10]
cov = N["coverage"]
conf = XS["conformance"]

t_h1 = "\n".join(f"| [{stem(d['module'])}]({GH}{d['module']}) | {d['dependents']} | {d['lines']} | {d['score']:.1f} |" for d in L["H1_keystones"][:12])
t_h2 = "\n".join(f"| [{d['type']}]({GH}{d['module']}) | {d['unlocks']} | {d['lines']} | {d['per100']} | {d['your_use']} |" for d in L["H2_leverage"][:12])
adds = Counter(d["field"] for d in L["H3_spec_deltas"] if d["kind"] == "X_ITE adds")
by_node = {}
for d in L["H3_spec_deltas"]:
    by_node.setdefault((d["node"], d["kind"]), []).append(d["field"])
t_h3 = "\n".join(f"| {n} | {k} | {', '.join(v)} |" for (n, k), v in sorted(by_node.items(), key=lambda kv: (kv[0][1], kv[0][0])))
t_h4a = "\n".join(f"| {d['node']} | {d['fields']} | {d['lines']} | {d['x_lines_vs_expected']}x |" for d in L["H4_surprise"][:12])
t_h4b = "\n".join(f"| {d['node']} | {d['fields']} | {d['lines']} | {d['x_lines_vs_expected']}x |" for d in L["H4_surprise"][-8:])
t_h5 = "\n".join(f"* {', '.join(v)}" for v in L["H5_twins"][:12])
temp = Counter(d["temperament"] for d in L["H6_temperament"])
temp_ex = {}
for d in sorted(L["H6_temperament"], key=lambda d: -d["event_share"]):
    temp_ex.setdefault(d["temperament"], []).append(d["node"])
t_h7 = "\n".join(f"| {d['component']} | {d['node_lines']:,} | {d['browser_lines']:,} | {round(100 * d['browser_share'])} % |" for d in L["H7_locus"])
t_cur = "\n".join(f"| {s['step']} | {s['track']} | [{stem(s['read'])}]({GH}{s['read']}) | {s['why']} |" for s in L["curriculum"])
t_tree = "\n".join(f"| {d['node']} | {', '.join(d['x_ite'])} | {', '.join(d['uom'])} |" for d in L["tree_diff"][:20])

doc = f"""# X_ITE 16.7.0: an AST masterclass, and heuristics for learning it

[create3000/x_ite](https://github.com/create3000/x_ite) is the X3D browser every fidelity decision in your repos calibrates
against ("as X_ITE draws it"). This teardown reads **version 16.7.0 exactly as installed** in
`x3d-physx-bridge/node_modules/x_ite`. Nothing was downloaded: the unminified bundles keep webpack's `;// ./src/...` module
markers, so `tools/xite_split.py` rebuilt the source tree ({len(MOD['lines'])} modules from {len(MOD['bundles'])} bundles; npm
dependencies such as opentype.js and the Ammo.js physics build are split out as vendored). No commit history, by your choice.

**Labels.** *Measured*: the TypeScript parser over every module, regular expressions over X_ITE's own fixed conventions
(`getStaticProperties`, `X3DFieldDefinition`, `setPrototypeOf`, `.call (this)` mixins), the X3D Unified Object Model 4.1,
and your scene corpus. *Inferred*: the heuristics' weights and thresholds, which are choices, stated with each one.

| scene | what it shows |
|---|---|
| `scenes/learning-map.x3d` | **X_ITE's own class tree** ({XS['learning_map']['classes']} node classes) with the 32-step curriculum as a gold path; colour = temperament, size = use in your files |
| `scenes/conformance-sunburst.x3d` | every X3D 4.1 node: X_ITE's module size and its field-by-field agreement with the spec; outer ring = your usage |
| `scenes/callgraph-3d.x3d` | {SS['callgraph']['files']} modules by force layout, {SS['callgraph']['functions']} functions, {SS['callgraph']['cross_file_calls']:,} references between modules |
| `scenes/code-city.x3d` | functions as buildings in {SS['city']['districts']} directories; amber = the same body in 2+ modules |

## 1. Anatomy in numbers (measured)

* **{sum(roles.values()):,} lines of X_ITE's own JavaScript** in {len(C)} modules: node classes {roles['nodes']:,}, browser machinery
  {roles['browser']:,}, rendering and GLSL {roles['rendering']:,}, core (fields, execution, routing, prototypes) {roles['core']:,},
  parsers {roles['parser']:,}, math {roles['math']:,}, API and registration {roles['api']:,}. {len(fs):,} named functions, 5,001 of
  them methods attached with X_ITE's `Object.assign(Object.setPrototypeOf(X.prototype, Base.prototype), {{...}})` idiom.
* **One module per node type.** {cov['x_ite_concrete']} concrete node modules: **{len(cov['implemented'])} of the 267** X3D 4.1 nodes,
  plus {len(cov['x_ite_only'])} X_ITE-only types (glTF material extensions such as `SheenMaterialExtension`, the Annotation
  component, `InstancedShape`, `BlendMode`, `DepthMode`, `SpecularGlossinessMaterial` …). The one 4.1 node without a module
  is `ProtoInstance`, which X_ITE implements in its execution layer (`X3DPrototypeInstance`).
* **Field conformance** against X3DUOM 4.1: **{conf['exact']} nodes match field for field** (name, type, access), {conf['extends']}
  add fields, {conf['differs']} differ, {conf['missing']} has no module.
* **Most complex functions:** """ + "; ".join(f"`{q}` {cc} ({stem(p)})" for cc, p, q, ln in top_cc[:6]) + f""".

## 2. Learning heuristics

Each heuristic turns a measurement into a decision about *what to read next*. They are built for X_ITE but work on any
large codebase that mirrors a specification.

### H1. Keystones: read what everything leans on, if it is short

*Measure:* PageRank over "module A uses module B" edges (rank flows to what is depended upon), divided by √lines.
*Why it teaches:* a module that hundreds of others reference defines the vocabulary they are all written in. If it is also
short, reading it is the cheapest way to make every other file legible.

| module | modules depending on it | lines | score |
|---|---|---|---|
{t_h1}

`Namespace` (721 dependents, 19 lines) is X_ITE's registry: every module registers its export there, so knowing it explains
the bundle's wiring. `Fields` and `X3DFieldDefinition` are the type system every node declares itself in. `X3DNode`
(1,235 lines) is the one long keystone: the base class of everything.

### H2. Leverage: learn the abstract type that unlocks the most nodes per line

*Measure:* for each abstract type in X_ITE's own class tree, the concrete nodes that inherit from it, per 100 lines of the
abstract module. *Why:* abstract types are where shared behaviour lives; a 19-line base that 30 nodes extend is 30 lessons for
the price of one.

| abstract type | concrete nodes unlocked | lines | per 100 lines | uses in your files |
|---|---|---|---|---|
{t_h2}

**X_ITE's tree is not the spec's tree.** In {len(L['tree_diff'])} nodes the bases differ from X3DUOM's. X_ITE adds
implementation layers the spec does not have (`X3DLineGeometryNode`, `X3DPointGeometryNode`, `X3DArrayChaserObject`,
`X3DGeospatialObject`, `X3DSingleTextureNode`), and sometimes skips a spec mixin. These differences show where a renderer
needs a shared code path that the spec never names:

| node | X_ITE bases | X3DUOM bases |
|---|---|---|
{t_tree}

### H3. Spec deltas: where the renderer knows more than the spec

*Measure:* field-by-field difference between each node's `fieldDefinitions` and X3DUOM 4.1. *Why:* an added field is a
lesson the spec does not teach (what a real renderer needed); a missing or retyped field is a place to be careful when you
write scenes. The most common additions: """ + ", ".join(f"`{f}` ({n})" for f, n in adds.most_common(8)) + f""".

| node | delta | fields |
|---|---|---|
{t_h3}

Reading this table: shadow maps need `shadowBias`, `shadowColor`, `shadowMapSize` on every light; GPU skinning adds
displacement *textures* to H-Anim; `Script`, `ComposedShader`, `PackagedShader` and `ShaderProgram` "lack" `field` because
their fields are user-declared at run time; most Sound "access differs" rows are `channelCount`, which X_ITE reports rather
than accepts.

### H4. Surprise: machinery hidden behind few fields

*Measure:* fit log(lines) against log(fields) across all nodes (slope {L['H4_fit']['slope']}), then take each node's residual.
*Why:* a node's fields are its contract; its lines are its cost. Big positive residuals are nodes whose behaviour is far
richer than their interface: the best case studies. Big negative residuals are thin data holders whose logic lives in a
base class or in `Browser/`: skim them.

| case studies (more lines than fields predict) | fields | lines | vs expected |
|---|---|---|---|
{t_h4a}

| skim (inherit almost everything) | fields | lines | vs expected |
|---|---|---|---|
{t_h4b}

### H5. Twins: learn one, get the rest

*Measure:* concrete nodes with identical base classes and method-name sets at least 80 % alike (Jaccard).
*Why:* when the AST says two nodes are built the same way, the second one costs nothing.

{t_h5}

### H6. Temperament: data, event-driven, engine, sensor

*Measure:* the share of a node's fields that are events (inputOnly, outputOnly) and outputs. *Why:* you read a data node for
its fields, an engine for its update loop, a sensor for when it fires. Knowing which kind you are looking at tells you where
in the module to start. Counts: data {temp['data']}, event-driven {temp['event-driven']}, engine {temp['engine']}, sensor
{temp['sensor']}. Most event-heavy engines (event share ≥ 35 %, not output-dominated): {', '.join(temp_ex.get('engine', [])[:8])}.

### H7. Locus: where a component's behaviour actually lives

*Measure:* lines in `Components/<C>` (the node classes) against `Browser/<C>` (the per-component machinery the nodes call).
*Why:* for some components the node classes are the behaviour; for others they are thin handles over a browser subsystem,
and reading the nodes alone teaches little.

| component | node lines | browser lines | in browser |
|---|---|---|---|
{t_h7}

GaussianSplats (83 %), Text (68 %), Texturing3D and Navigation keep their logic in `Browser/`; HAnim, RigidBodyPhysics, DIS
and CAD keep it in the nodes. WebXR has no nodes at all.

### H8. Your corpus: weight everything by what you actually write

*Measure:* how many of your own X3D files (x3d.loom, x3d.demo, x3d.onto) use each node. Top: """ + ", ".join(f"{n} {k}" for n, k in L["H8_corpus_top"][:12]) + f""".
*Why:* the same renderer is a different textbook for different readers. Weighting by your corpus puts `Appearance`,
`Coordinate` and `NavigationInfo` early, and lets `HAnimHumanoid` wait until you need it.

## 3. The curriculum (32 steps, generated)

Tracks: **keystone** (H1, at least 20 dependents), **abstract** (H2), **quick win** (your usage per line to read, including
prerequisites not yet learned), **deep dive** (nodes you use with surprise above 0.5, H4). The learning map draws this path.

| step | track | read | why |
|---|---|---|---|
{t_cur}

## 4. Insights

1. **X_ITE is a near-literal transcription of the spec.** 194 of 267 nodes declare exactly the spec's fields, and every
   node module starts with the same `getStaticProperties(name, component, level, containerField, version)` call. That
   regularity is why this teardown could check conformance with a few regular expressions, and why the field tables are a
   reliable reference when the spec text is ambiguous.
2. **The extensions tell you where rendering reality presses on the spec**: shadows, GPU skinning, glTF PBR extensions,
   pointer events on layers. They are also where your exports may draw differently in other browsers.
3. **Two places to read for every component:** `Components/` for the contract and `Browser/` for the machinery (H7).
   A hypothesis tested and rejected: that your Loom bridge's unfinished nodes (gap, todo, blocked in `NODES.json`) cluster
   in components whose X_ITE logic lives in `Browser/`. Measured on the 260 tracked nodes, the opposite holds: 36 % are
   unfinished in browser-heavy components (share ≥ 40 %) against 54 % elsewhere (correlation −0.23). The bridge has done
   the machinery-heavy components; what is left is the long tail of node-local behaviour (Sound, HAnim, CAD, DIS, Followers).

## 5. Method and limits

* Source rebuilt from the npm bundles; module boundaries are webpack's. 24 fragments parse with recoverable errors where a
  bundle wrapper cuts a statement. GLSL shader sources are counted as modules (they are JS strings).
* Module references are resolved by webpack's export names (`Lighting_X3DLightNode`) and the component bundles' external
  accessors (`external_X_ITE_X3D_X3DNode_default()`); method-to-method dispatch through `this` is not followed.
* Field defaults are compared numerically with a 0.1 % tolerance (X_ITE writes 0.785398 where X3DUOM writes 0.7854); defaults
  built with `new …` are not compared.
* The heuristics' thresholds (≥ 20 dependents, Jaccard ≥ 0.8, surprise > 0.5, temperament cut-offs) are choices; change them in
  `tools/xite_learn.py` and the curriculum regenerates.
* All four scenes validate with x3d_mcp (XSD 4.0, 0 errors, 0 warnings) and render in X_ITE 16.7.0 itself in the Claude browser pane.
"""
(X / "MASTERCLASS.md").write_text(doc)
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>X_ITE 16.7.0 · AST masterclass</title>
<style>body{{margin:0;background:#1a1a19;color:#f0efec;font:15px/1.5 system-ui,sans-serif}}main{{max-width:1100px;margin:0 auto;padding:2rem 1.25rem}}
a{{color:#86b6ef}}.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:1rem}}.card{{background:#232321;border:1px solid #383835;border-radius:8px;padding:1rem}}
.card p{{color:#c3c2b7}}.btn{{background:#262624;border:1px solid #4a4a46;color:#f0efec;padding:.35rem .7rem;border-radius:5px;text-decoration:none;margin-right:.4rem}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:.7rem}}.tile{{background:#232321;border:1px solid #383835;border-radius:8px;padding:.7rem}}
.k{{color:#c3c2b7;font-size:.8rem;text-transform:uppercase}}.v{{font-size:1.2rem;font-weight:600}}.note{{color:#8a8a85;font-size:.85rem}}</style></head><body><main>
<p class=note><a href="../index.html">← all masterclasses</a> · local · X_ITE 16.7.0 as installed in x3d-physx-bridge · nothing downloaded or published</p>
<h1>X_ITE 16.7.0: AST masterclass and learning heuristics</h1>
<p>Write-up with eight learning heuristics and a 32-step curriculum weighted by your own scenes: <a href="MASTERCLASS.md">MASTERCLASS.md</a>.</p>
<div class=tiles>{''.join(f"<div class=tile><div class=k>{html.escape(k)}</div><div class=v>{html.escape(v)}</div></div>" for k, v in [
    ("own code", f"{sum(roles.values()):,} lines"), ("modules", str(len(C))), ("X3D 4.1 nodes with a module", f"{len(cov['implemented'])} / 267"),
    ("exact field match", f"{conf['exact']} nodes"), ("X_ITE-only node types", str(len(cov['x_ite_only']))), ("curriculum", "32 steps")])}</div>
<h2>Scenes</h2><p class=note>All validate with x3d_mcp (XSD 4.0; 0 errors, 0 warnings). Hover for details; click to open the module on GitHub (tag 16.7.0).</p><div class=cards>
{''.join(f"<div class=card><h3>{t}</h3><p>{d}</p><a class=btn href='view.html?scene={s}'>Open in viewer</a><a class=btn href='scenes/{s}.x3d'>{s}.x3d</a></div>" for s, t, d in [
    ("learning-map", "Learning map", "X_ITE's own class tree, abstract types on top; concrete nodes coloured by temperament (blue data, aqua event-driven, orange engine, amber sensor), sized by use in your files. Gold path = the curriculum, starting on the keystone plinths."),
    ("conformance-sunburst", "Spec conformance", "Per X3D 4.1 node: X_ITE module size and field agreement (green exact, blue extends, salmon differs, red none). Violet outer ring: your usage."),
    ("callgraph-3d", "Module graph", "Modules by force layout with their functions around them; coloured lines are references between modules."),
    ("code-city", "Code city", "Functions as buildings per directory; amber bodies appear in two or more modules.")])}</div></main></body></html>"""
(X / "index.html").write_text(page)
print("MASTERCLASS.md", len(doc.splitlines()), "lines")
