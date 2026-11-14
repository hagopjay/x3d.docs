"""MASTERCLASS.md + index.html for loom and demo, and a top-level index.html. Numbers come from data/*.json."""
import html
import json
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import astlib  # noqa: E402
from roles import CFG  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAL = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
e = html.escape


def load(n):
    d = ROOT / n / "data"
    return {k: json.load(open(d / f"{k}.json")) for k in ("head", "era", "scene_stats", "prs", "runs")}


def pr_rows(n, era):
    rows = []
    for s in era[1:]:
        d = s["delta"]
        tag = f"[#{s['pr']}]({s['pr_url']})" if s["pr"] else f"`{s['sha']}`"
        x = []
        if d["scenes_new"]:
            x.append(f"+{len(d['scenes_new'])} X3D files ({d['scene_mb']:+} MB)")
        if d["used_new"]:
            x.append(f"scenes start using {len(d['used_new'])} node types")
        if d["known_new"]:
            x.append(f"code names {len(d['known_new'])} more")
        rows.append(f"| {tag} | {s['date'][5:10]} | {(s['pr_title'] or s['subject']).replace('|', '/')} | {d['loc']:+,} lines; +{d['added']} -{d['removed']} ~{d['changed']} fns | {'; '.join(x) or '-'} |")
    return "| step | date | title | code delta | X3D delta |\n|---|---|---|---|---|\n" + "\n".join(rows)


def hotspots(head):
    fs = [(p, f) for p, r in head["code"].items() for f in r["functions"] if f["qualname"] != "<module>"]
    out = ["| function | CC | lines | nesting |", "|---|---|---|---|"]
    seen = set()
    for p, f in sorted(fs, key=lambda t: -t[1]["cc"]):
        if f["hash"] in seen:
            continue
        seen.add(f["hash"])
        copies = sum(1 for q, g in fs if g["hash"] == f["hash"])
        out.append(f"| `{p}::{f['qualname']}`" + (f" (same body in {copies} files)" if copies > 1 else "") + f" | {f['cc']} | {f.get('loc')} | {f['depth']} |")
        if len(out) >= 14:
            break
    return "\n".join(out)


def roles_table(n, head):
    cfg = CFG[n]
    C, S = head["code"], head["scenes"]
    out = ["| role (hand-assigned from directory names) | code files | code lines | functions | X3D files | X3D MB |", "|---|---|---|---|---|---|"]
    for r in cfg["order"]:
        cf = [p for p in C if cfg["role"](p) == r]
        sf = [p for p in S if cfg["role"](p) == r]
        out.append(f"| {cfg['label'][r]} | {len(cf)} | {sum(C[p]['loc'] for p in cf):,} | {sum(len(C[p]['functions']) for p in cf):,} | {len(sf)} | {sum(S[p].get('bytes', 0) for p in sf) / 2 ** 20:.1f} |")
    return "\n".join(out)


def node_table(head):
    used = Counter(nn for r in head["scenes"].values() for nn in r["nodes"])
    comp = Counter()
    for nn, k in used.items():
        if nn in astlib.X3D_NODES:
            comp[astlib.X3D_NODES[nn]["component"]] += 1
    tops = ", ".join(f"{nn} ({k})" for nn, k in used.most_common(15))
    return f"Node types used, by number of files: {tops}. Components touched: " + ", ".join(f"{c} {k}" for c, k in comp.most_common()) + "."


TEXT = {
"onto": '# x3d.onto: an AST masterclass and teardown\n\n[hagopjay/x3d.onto](https://github.com/hagopjay/x3d.onto) (private; default branch `claude/project-thread-3mgt8g`, head {sha}),\nmeasured 2026-11-13. hagsmac/x3d.onto is a fork with the same head (0 ahead, 0 behind). The repo starts on 2026-10-27\n("extracted from the Mac working tree") and its last change is 2026-11-04: {commits} commits, {steps} first-parent steps,\n17 PRs, all merged (#6 and #7 into `dynasty-loom/*` branches, the rest into the default branch; #15 was merged despite its\n"[Do not merge yet]" title). No CI: the repo has no Actions runs. 6 remote branches are not merged (`dspy-agent`,\n`project-thread-bfwscy`, `dynasty-loom/v2` and `v3`, `loom/gemini-api`, `loom/lawful-gemini`).\n\n**Labels** as in the x3d.loom masterclass. The ontology lens adds rdflib 7.6.0 (from the x3d_mcp venv, already installed):\nevery `.ttl` file parsed, classes, properties, `rdfs:subClassOf` and OWL restrictions counted.\n\n| scene | what it shows |\n|---|---|\n| `scenes/ontology-hierarchy.x3d` | **the X3D Ontology 4.1 class tree** in 3D: 364 classes, levels by depth; gold = new in 4.1, blue ring = narrowed by the proposal, orange halo = named by the sim vocabularies, size = use in the repo\'s scenes |\n| `scenes/callgraph-3d.x3d` | {cg_files} files, {cg_fns} functions, {cg_in} in-file and {cg_cross} cross-file calls |\n| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the {nscenes} X3D files (orange) and named in code (blue) |\n| `scenes/fork-timeline.x3d` | {steps} steps from 2026-10-27 to 2026-11-04 |\n| `scenes/code-city.x3d` | functions as buildings per directory; amber = body in 2+ files |\n\n## 1. What the AST says x3d.onto is\n\n**An ontology repo whose code is mostly worlds.** Only **7 of 175 Python files** touch the ontology (import rdflib, run\nSPARQL or name a `.ttl`): `harness/build.py` (6 SPARQL queries), `harness/build_sim.py`, `harness/proposal_sketch.py`,\n`harness/test_harness41.py`, `harness/xslt_diagnosis.py`, `demo/audit_numbers.py`, `demo/build_tour.py`. The ontology itself\nlives in data: two copies of the official X3D Ontology (4.0 and 4.1, 1.1 MB each), one proposal, and 8 small "sim"\nvocabularies. Everything else is scenes built *from* the ontology\'s knowledge: the Dynasty Loom genealogy hypersphere\n(half of all code), the Gobbler demiurge village, the v2 Sun-Earth-Moon village of 364 classes, and the cross-domain tools.\n\n{roles}\n\n* **Code:** {loc:,} lines in {files} files ({langs}), 3,169 named function definitions; {cc20} over complexity 20, {cc50} over 50.\n* **Scenes:** {nscenes} X3D files, {mb} MB; {versions}; profiles {profiles}. 224 of them are the `xdomain` differential\n  validator fuzzer\'s corpus (small X3D 4.1 Full-profile files). 25 files use protos, 3 a Script, 147 ROUTEs in all.\n* **Little copying:** 137 of 1,734 functions of 3+ lines have a body in another file (8 %), far less than the Loom (31 %) or\n  the demo shelf (69 %).\n* **Tests:** 101 Python `test_*` functions and 9 JS `test(`/`it(` calls, no CI to run them.\n\n### Hot spots (measured; one row per distinct body)\n\n{hotspots}\n\nEvery top function is in `dynasty-loom` or `xdomain/lawful`: data gates (`datagates.check` 165), ingest (`ingest.main` 162),\nscene generation (`gen_stops` 145) and the lawful metric (`metric.score` 119). These are long single-pass builders; they\nread top to bottom, but each is a candidate for splitting by stage.\n\n## 2. The ontology lens (measured with rdflib)\n\n| file | triples | OWL classes | object props | datatype props | subClassOf |\n|---|---|---|---|---|---|\n{ttl_table}\n\n* **4.0 → 4.1:** 355 → 364 classes, **+9, none removed**: {added}.\n* **The narrowing proposal** (`proposal/X3dOntology4.1.narrowing-sketch.ttl`, 2,088 triples, none of them in 4.1) adds\n  **310 `owl:allValuesFrom` restrictions on 143 classes**. It narrows what a node field may hold, mostly\n  `hasChildren` (42), `hasColor`, `hasTexCoord`, `hasCoord` (15 each), `hasNormal` (14), `hasAttrib` (13), `hasFogCoord`\n  (13). In the official ontology these SFNode/MFNode properties accept any X3D node; the proposal encodes the spec\'s\n  acceptable node types, which is what x3d_mcp\'s `where_can_place` and containerField checks need. HAnimHumanoid gets the\n  most (12), then the geometry sets (7 each).\n* **The sim vocabularies** (`sim/*.ttl`: agency, geons, heritage, parts_contact, perspective, prepositions, scale,\n  verification; 64–137 triples each) define no OWL classes. They are graded statements in a private namespace\n  (`example.invalid/sim/spatial-cognition#`) with `x3dNode` / `x3dField` / `onNode` links into X3D 4.1: perspective → Viewpoint,\n  NavigationInfo, OrthoViewpoint; scale → GeoCoordinate, GeoLOD, LOD, `unit`; parts_contact → SingleAxisHingeJoint, Cone;\n  prepositions → Transform. 35 X3D terms are named this way (orange halos in the hierarchy scene).\n\n## 3. Taxonomy: X3D used by the scenes\n\n{nodes}\n\nThe code names all 267 node types only because `explorer.html` embeds the complete node table (284 names); without it,\nthe most is 43 (`dynasty-loom/x3d/build_genealogy_x3d.py`).\n\n## 4. The history, step by step\n\n{prtable}\n\n**Phases.** Oct 27–28: the extraction and Gobbler v4. Oct 30–31: the Loom thesis loop (gate lints, lawful metric with DSPy,\ndifferential validator fuzzer), Gobbler demiurge, and Dynasty Loom v2, v3 and v5 under version control. Nov 1: gates\n(color-emissive-white). Nov 4: **Loom v1** consolidated and seven fold-back PRs (#11–#17) that move gates from other\nprojects (gear loom, break-the-loom, data city, Loomsong fidelity, IFC bridge, Gobbler cabinet, linked observatory) into\nthe method. The next day the method moved to its own repo, x3d.loom (created 2026-11-05), and x3d.onto stopped changing.\n\n## 5. Insights, risks, recommendations\n\n1. **x3d.onto is the Loom\'s birthplace.** Its last week is the Loom v1 consolidation; x3d.loom starts the day after. The\n   gates, laws and fold-back pattern began here. Worth stating in both READMEs so the lineage is not lost.\n2. **The proposal is the most reusable artefact.** 310 restrictions that turn "any node" into the spec\'s acceptable types\n   are exactly what a validator or a generator needs. Recommendation: test it against x3d_mcp\'s X3DUOM-based placement\n   table (they should agree node by node) and, if they do, offer it upstream to Web3D with that agreement as evidence.\n3. **Two copies of a 1.1 MB official ontology** are vendored without a source pin. Record the upstream URL and date, or\n   fetch them in the harness, so a refresh is a diff and not a mystery.\n4. **101 tests, no CI.** A single pytest workflow would protect the harness and the gates; the repo is small enough.\n5. **The sim vocabularies** use a placeholder namespace (`example.invalid`). Give them a real one before anything links to\n   them.\n\n## 6. Method and limits\n\nAs in the x3d.loom masterclass, plus `tools/onto_lens.py` (rdflib over every `.ttl`, Python `ast` for SPARQL strings and\n`.ttl` paths). `v2/tour.js` inlines a minified bundle and is excluded from function counts. Restriction counts are taken\nfrom `rdfs:subClassOf` blank nodes in the proposal. The hierarchy scene draws the 412 `rdfs:subClassOf` edges between\nclasses that are themselves declared `owl:Class` (454 in the file; the rest point at classes declared elsewhere).\n',
"loom": """# x3d.loom: an AST masterclass and teardown

[hagopjay/x3d.loom](https://github.com/hagopjay/x3d.loom), `origin/main` {sha}, measured 2026-11-13. The repo was created on
2026-11-05 ("The X3D Loom v1.0, public snapshot"), so there is no fork era: its whole history is the era. In 8 days the
first-parent line of `main` took {steps} steps; 44 of the 45 PRs merged into `main` (#36 went to `bridge-review` and #42 to a
working branch). The hagsmac copy has its own 4 PRs (2 merged into hagsmac/main, 1 closed, 1 open: the Babylon visual-lane WIP).

**Labels.** *Measured*: Python `ast`, the TypeScript compiler's parser (JS, MJS, TS, TSX and inline `<script>` in HTML),
an XML element walk of every `.x3d` file, `git` and `gh`. *Inferred*: call resolution (static, by name and import binding),
X3D node names found as string literals in code, and the roles, which are assigned by top-level directory. *Claimed*: the
bridge's own tracker `x3d.webgpu/bridge/NODES.json` and PR text. Nothing was executed and nothing was installed (the
TypeScript parser is the copy already installed for x3d-physx-bridge).

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | {cg_files} files laid out by a force model, {cg_fns} functions of 3+ lines around them, {cg_cross} cross-file and {cg_in} in-file calls |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the repo's {nscenes} X3D files (orange) and the bridge tracker's status per node |
| `scenes/fork-timeline.x3d` | {steps} steps of `main`: code lines per role, X3D megabytes, new node types in scenes and code, CI |
| `scenes/code-city.x3d` | functions as buildings per directory; aqua = body in one file, amber = same body in 2+ files |

## 1. What the AST says the Loom is

The Loom is not one program. It is **eight sub-projects that do not call each other**: in the call graph each role is an
island: all 1,174 statically resolved cross-file calls stay inside their own sub-project (physics 484, drift 459,
kit 139, platformer 91, mol 1). Static resolution finds no calls between `x3d.webgpu` files: whatever wires them
(globals, dynamic registration, page-level script order) is outside what this method follows. They share a *method* (laws, failure modes,
loomkit gates, receipts, documented in the root Markdown files) rather than a library.

{roles}

* **Code:** {loc:,} lines in {files} files ({langs}). 6,916 named function definitions, {cc20} with cyclomatic complexity
  over 20 and {cc50} over 50.
* **Scenes:** {nscenes} X3D files, {mb} MB: {versions}; profiles {profiles}. 1,694 ROUTEs, but only 2 files with a `Script` node and 1
  file with a `ProtoInstance`: behaviour lives in the JavaScript around the scenes, not inside them.
* **Duplication:** of 3,814 functions of 3+ lines, {shared} have a body that also exists in another file. 25 files are exact
  copies of another (same multiset of function bodies). The biggest family is the WebGPU viewer: `viewer.tpl.html`,
  `-v2`, `-v2-1`, `-v3`, `-v3-1`, `collider.html`, `collider-v2.html` and `first-light*.html` each carry their own `frame`
  function (CC 127 to 154). Versioning by copying a page is the Loom's habit; it keeps old demos frozen, at the price of
  fixes that must be applied N times (PR #20's SAI texture-fallback fix is the kind of change this multiplies).

### Hot spots (measured; one row per distinct body)

{hotspots}

`x3d.drift/engine/car.js::stepCar` (CC 185) and `ai.js::driftDrive` (CC 132) are the most complex functions in either repo:
a vehicle model and a driving AI in single functions. They are the first candidates for splitting, with the drift game's
own tests as the net.

## 2. Taxonomy: X3D through three lenses

{nodes}

**The bridge tracker against the AST.** `x3d.webgpu/bridge/NODES.json` tracks 260 X3D 4.0 nodes for the Babylon/WebGPU
reader. Its statuses: base 75, bridged 41, claimed 8, gap 70, todo 65, blocked 1. Cross-checked against the code:

| tracker status | nodes | named as a literal in code | used in a scene in the repo |
|---|---|---|---|
{tracker}

Every node the tracker calls base, bridged, claimed, gap or blocked is named in the code, so the tracker and the code agree
(measured). Only 17 of the 65 "todo" nodes appear in code. The 70 "gap" nodes all have a test scene: a gap is a node that is
read and tested but not yet drawn the way X_ITE draws it, which is what the Babylon "visual lane" PRs (#43 to #45) burn
down with picture comparisons against X_ITE. In the sunburst, the outer ring is this tracker and the white dots mark code
naming.

## 3. The history, step by step

{prtable}

**Phases.** Nov 5–6: public snapshots and five sub-projects in a day (zinc fingers, platformer, collider, brain, drift).
Nov 7–8: x3d.webgpu, a Babylon/WebGPU bridge, nine ports of existing X3D demos and the node-by-node reader (batches 1 to 20,
"reader 175 of 260"). Nov 9: the bridge gets validation that can fail, a fidelity preflight and the first CI. Nov 12–13:
x3d.mol (proteins, AlphaFold 3 keyframes), physics under the Loom (PhysX and MuJoCo bridges, laws 41–44, failure modes
124–160) and the Babylon visual lane.

## 4. Tests and CI

* CI exists only for the bridge: `.github/workflows/bridge.yml` (from #35). Runs: 13 in all; on `main` 2 succeeded and 2
  were cancelled. The rest of the Loom (drift, physics bridges, mol, brain, kit) has no CI.
* Tests found by AST: 62 JS `test(`/`it(` calls and no Python `test_*` functions. The Loom's real checks are its **gates
  and receipts** (`kit/loomkit`, `receipts/*.json`, `runs/`), which are evidence files rather than unit tests; this
  analysis does not count them as tests.

## 5. Insights, risks, recommendations

1. **A method repo, not a code library.** No shared runtime between sub-projects. Good for isolation; it means a fix in
   one viewer does not reach the copies. Recommendation: extract the WebGPU viewer's `frame` loop and the SAI shim into one
   module that the pages import, and keep frozen versions as tags rather than copied files.
2. **The tracker is honest and checkable.** The AST agrees with NODES.json on every claimed or bridged node. Worth
   publishing as a generated table, with this cross-check as a CI step, so the claim "N of 260" can never drift from the code.
3. **Complexity lives in games and render loops** (`stepCar` 185, `frame` 127–154, `driftDrive` 132). Split by phase
   (input, integrate, collide, render) before the next feature.
4. **CI covers one of eight sub-projects.** Add the existing drift and physics tests to a workflow; they already run headless.
5. **Behaviour outside the scenes.** 1,694 ROUTEs but 2 Scripts: the X3D files stay portable, and the JS does the work.
   That is a deliberate Loom rule; the risk is that X_ITE-only users get a static scene.

## 6. Method and limits

Same method as the x3d-blender-io and x3d_mcp masterclasses, extended: `tools/jsast.cjs` (TypeScript parser) for JS/TS
and inline scripts, `tools/repo_ast.py` (blob-sha cache, `git cat-file`, no checkout), `tools/era.py` (every first-parent
commit). Vendored files are excluded by path ({vendored} files: X_ITE, Babylon, minified bundles). Anonymous callbacks are
charged to their enclosing function. Six `.tpl.html` templates contain placeholders and parse with recoverable errors.
Clone detection hashes each function's whitespace-normalised source text. Scenes validate with x3d_mcp (XSD 4.0 valid,
0 errors, 0 warnings) and were rendered in the Claude browser pane (X_ITE 16.7.0, software WebGL); the call graph and the
city take 30 to 50 s to load there.
""",
"demo": """# x3d.demo: an AST masterclass and teardown

[hagopjay/x3d.demo](https://github.com/hagopjay/x3d.demo), `main` {sha}, measured 2026-11-13 ("Demo repo for x3d-io.ai
work", GitHub Pages from `docs/`). Created 2026-11-07; {steps} first-parent steps; 25 PRs, all merged. The local checkout's
`origin` is hagsmac/x3d.demo, which is 40 commits behind (last change 2026-11-07); this analysis uses hagopjay's `main`.

**Labels** as in the x3d.loom masterclass: measured (ASTs, XML walk, git, gh), inferred (call resolution, literal node
names, roles from demo folder names), claimed (PR text). Nothing executed or installed.

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | {cg_files} files ({cg_dup} more are exact copies), {cg_fns} functions, {cg_in} in-file calls and only {cg_cross} cross-file calls |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the {nscenes} X3D files (orange) and named in code (blue) |
| `scenes/fork-timeline.x3d` | {steps} steps of `main` with code lines per role, X3D megabytes, new node types, Pages deploys |
| `scenes/code-city.x3d` | functions as buildings per demo folder; amber = the same body exists in 2+ files |

## 1. What the AST says the demo repo is

A **publishing shelf**. Every demo is a self-contained page: {cg_in} calls inside files, {cg_cross} across files. Each new
version is a new folder (`v1`, `v2` …) and the old one is never edited: across all {steps} steps of history the AST sees
**0 functions changed**, only added. That makes the repo append-only by construction.

{roles}

* **Code:** {loc:,} lines in {files} files ({langs}), 8,963 named function definitions, {vendored} vendored files excluded (X_ITE and Babylon builds).
  One page (`x3d-mujoco-bridge/v1/index.html`) inlines a minified bundle and is excluded from function counts.
* **Scenes:** {nscenes} X3D files, {mb} MB: {versions}; profiles {profiles}. 3,767 ROUTEs, 1 file with a Script, 6 files with a ProtoInstance.
  The largest are `hall.x3d` (13 MB), `facade.x3d` (11 MB, twice) and `pantheon.x3d` (6 MB).
* **Duplication:** {shared} of {fn3} functions of 3+ lines (69 %) have a body that exists in another file, and 28 files
  are exact copies. **{xr_hit:,} of {fn3} function bodies ({xr_pct} % of the function lines) are identical to functions in
  x3d.loom**: the HEP collider pages, the brain/torso pages, the heritage facade and the WebGPU ports are copies of the
  Loom's viewers. The demo repo is a downstream mirror of the Loom's pages.

### Hot spots (measured; one row per distinct body)

{hotspots}

The top entries are the Loom's WebGPU viewer `frame` loop, copied into each collider and facade page.

## 2. Taxonomy: X3D used by the demos

{nodes}

The code names 122 node types, more than the 82 the scenes use, because the embedded WebGPU reader (from the Loom bridge)
carries its own node table.

## 3. The history, step by step

{prtable}

**Phases.** Nov 7: the demo doc v1 to v12, WebGPU demos (Neural Canvas, KANSEI, manifold, chirp, electron cloud). Nov 8:
the X3D demo shelf (Blender X3D I/O showcase, MuJoCo bridge, ontology constellation, Dynasty Loom, Confluence IFC, Gobbler)
and the Babylon ports. Nov 9: Gobbler Gyroscope. Nov 13: LUMEN interference, Giza Osiris Hall, and Ten Minute Physics in
X3D (six batches).

## 4. Tests and deploys

* No test workflow. The only Actions runs are GitHub Pages deploys: 26 on `main`, 25 succeeded and 1 failed.
* 18 Python test functions found by AST, all in `gobbler-worlds-within/v1/tests` (radiance, semantic, server). The pages are verified by hand and by the PRs'
  screenshots, according to the PR text.

## 5. Insights, risks, recommendations

1. **Copies drift.** With 53 % of function bodies copied from the Loom, a fix in the Loom's viewer does not reach the
   published demos. Recommendation: record each demo's source commit in the Loom (a `SOURCE` line per folder) and add a
   check that reports which demo pages lag their Loom source, using the body-hash comparison from this teardown.
2. **Append-only is a feature here.** Frozen versions make every doc link stable. Keep it, but point the index at the
   newest version and mark old ones as archived.
3. **The repo is heavy:** {mb} MB of X3D plus 104 MB of HTML (inlined data). Pages serves it, but clones and CI will slow
   down. Consider Git LFS or release assets for scenes over 5 MB.
4. **A smoke test per page** would catch the "no adapter" and texture-fallback class of bug (PRs #2, Loom #20) before
   deploy; the x3d.poc Pages smoke recipe (full Chromium, not headless-shell) is reusable.

## 6. Method and limits

As in the x3d.loom masterclass (same tools, same cache). Inline scripts are analysed at their HTML line numbers. Roles are
assigned from folder names (`*-webgpu` and `brain-torso` → WebGPU; collider events and heritage facade → HEP; Ten Minute
Physics and the MuJoCo bridge → physics; `stem`; everything else under `docs/demos` → X_ITE demos; the rest → doc shelf).
Scenes validate with x3d_mcp (XSD valid, 0 errors, 0 warnings) and render in X_ITE 16.7.0 in the Claude browser pane.
""",
}


def build(n):
    cfg = CFG[n]
    X = load(n)
    head, era, st = X["head"], X["era"], X["scene_stats"]
    C, S = head["code"], head["scenes"]
    fs = [f for r in C.values() for f in r["functions"] if f["qualname"] != "<module>"]
    vals = {
        "sha": era[-1]["sha"], "steps": len(era) - 1, "files": len(C), "loc": sum(r["loc"] for r in C.values()),
        "langs": ", ".join(f"{k} {v}" for k, v in Counter(r["lang"] for r in C.values()).items()),
        "cc20": sum(f["cc"] > 20 for f in fs), "cc50": sum(f["cc"] > 50 for f in fs),
        "nscenes": len(S), "mb": f"{sum(r.get('bytes', 0) for r in S.values()) / 2 ** 20:.1f}",
        "versions": ", ".join(f"X3D {k} {v}" for k, v in Counter(r.get("version") for r in S.values()).most_common()),
        "profiles": ", ".join(f"{k} {v}" for k, v in Counter(r.get("profile") for r in S.values()).most_common()),
        "shared": st["city"]["shared"], "fn3": st["city"]["shared"] + st["city"]["unique"],
        "cg_files": st["callgraph"]["files"], "cg_dup": st["callgraph"]["dup_files"], "cg_fns": st["callgraph"]["functions"],
        "cg_cross": st["callgraph"]["cross_file_calls"], "cg_in": st["callgraph"]["in_file_calls"], "vendored": head["vendored_files"],
        "roles": roles_table(n, head), "hotspots": hotspots(head), "nodes": node_table(head), "prtable": pr_rows(n, era),
    }
    if n == "loom":
        t = st["sunburst"]["tracker"]
        vals["tracker"] = "\n".join(f"| {k} | {v['n']} | {v['named_in_code']} | {v['used_in_scenes']} |" for k, v in t.items())
    elif n == "onto":
        L = json.load(open(ROOT / "onto" / "data" / "onto_lens.json"))
        vals["ttl_table"] = "\n".join(f"| `{k}` | {v['triples']:,} | {len(v['classes'])} | {v['object_props']} | {v['datatype_props']} | {len(v['subclass'])} |" for k, v in L["files"].items())
        vals["added"] = ", ".join(L["diff_40_41"]["added"])
        vals["commits"] = 67
    else:
        xr = json.load(open(ROOT / "demo" / "data" / "cross_repo.json"))
        vals["xr_hit"], vals["xr_pct"] = xr["hit"], round(100 * xr["hitlines"] / xr["lines"])
    doc = TEXT[n].format(**vals)
    (ROOT / n / "MASTERCLASS.md").write_text(doc)
    # index page
    first, last = era[0]["stats"], era[-1]["stats"]
    tiles = [("code lines", f"{first['loc']:,} → {last['loc']:,}"), ("functions", f"{first['funcs']:,} → {last['funcs']:,}"),
             ("X3D files", f"{first['scenes']} → {last['scenes']} ({last['scene_mb']} MB)"),
             ("node types in scenes / in code", f"{last['node_types_used']} / {last['node_types_known']}"),
             ("bodies shared by 2+ files", f"{st['city']['shared']:,} of {vals['fn3']:,}"), ("main steps", str(len(era) - 1))]
    legend = "".join(f"<span><i class=sw style='background:{PAL[i]}'></i>{e(cfg['label'][r])}</span>" for i, r in enumerate(cfg["order"]))
    cards = [("callgraph-3d", "Call graph", "Files by force layout, functions around them; spheres = CC ≥ 8 (hover), points = the rest. Coloured lines cross files, grey lines stay inside one."),
             ("coverage-sunburst", "X3D node sunburst", "Orange: node types used in the repo's X3D files. Outer ring: " + ("the bridge tracker's status (green base/bridged, blue claimed, salmon gap, grey todo, red blocked); white dot = named in code." if n == "loom" else "node types named in code (blue).")),
             ("fork-timeline", "History timeline", "One column per first-parent commit: code lines per role, X3D MB (grey), new node types (light grey, white), CI/Pages dots."),
             ("code-city", "Clone city", "Functions as buildings per directory. Aqua: body in one file. Amber: the same body is in two or more files.")] + ([("ontology-hierarchy", "X3D Ontology 4.1 hierarchy", "364 OWL classes by depth; gold = new in 4.1, blue ring = narrowed by the proposal, orange halo = named by the sim vocabularies; size = use in the repo's scenes.")] if n == "onto" else [])
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE[n]} · AST masterclass</title><style>
:root{{--s:#1a1a19;--s2:#232321;--b:#383835;--t:#f0efec;--t2:#c3c2b7;--t3:#8a8a85}} body{{margin:0;background:var(--s);color:var(--t);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:2rem 1.25rem 4rem}} a{{color:#86b6ef}} h2{{border-bottom:1px solid var(--b);padding-bottom:.4rem;margin-top:2.4rem}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(175px,1fr));gap:.75rem}} .tile{{background:var(--s2);border:1px solid var(--b);border-radius:8px;padding:.8rem}}
.k{{color:var(--t2);font-size:.8rem;text-transform:uppercase}} .v{{font-size:1.25rem;font-weight:600}} .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:1rem}}
.card{{background:var(--s2);border:1px solid var(--b);border-radius:8px;padding:1rem}} .card p{{color:var(--t2)}} .legend{{display:flex;flex-wrap:wrap;gap:.3rem .9rem;font-size:.8rem;color:var(--t2)}}
.sw{{display:inline-block;width:.8rem;height:.8rem;border-radius:2px;margin-right:.35rem;vertical-align:-1px}} .btn{{background:#262624;border:1px solid #4a4a46;color:var(--t);padding:.35rem .7rem;border-radius:5px;text-decoration:none;margin-right:.4rem}}
.note{{color:var(--t3);font-size:.85rem}}</style></head><body><main>
<p class=note><a href="../index.html">← all masterclasses</a> · local, generated 2026-11-13 from {cfg['repo']} main {era[-1]['sha']} · nothing published</p>
<h1>{TITLE[n]}: AST teardown</h1><p>Python <code>ast</code>, the TypeScript parser and an XML walk over every commit of <code>main</code>. Write-up: <a href="MASTERCLASS.md">MASTERCLASS.md</a>.</p>
<div class=tiles>{''.join(f"<div class=tile><div class=k>{e(k)}</div><div class=v>{e(v)}</div></div>" for k, v in tiles)}</div>
<h2>Four X3D 4.0 scenes</h2><p class=note>All validate with x3d_mcp (XSD 4.0 valid; 0 errors, 0 warnings). Big scenes take 30–50 s to load in software WebGL.</p>
<div class=legend>{legend}</div><br><div class=cards>{''.join(f"<div class=card><h3>{e(t)}</h3><p>{e(d)}</p><a class=btn href='view.html?scene={s}'>Open in viewer</a><a class=btn href='scenes/{s}.x3d'>{s}.x3d</a></div>" for s, t, d in cards)}</div>
</main></body></html>"""
    (ROOT / n / "index.html").write_text(page)
    print(n, "MASTERCLASS.md", len(doc.splitlines()), "lines")


TITLE = {"loom": "x3d.loom", "demo": "x3d.demo", "onto": "x3d.onto"}
if __name__ == "__main__":
    for n in ("loom", "demo", "onto"):
        build(n)
    top = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>x3d.loom, x3d.onto, x3d.demo masterclasses</title>
<style>body{margin:0;background:#1a1a19;color:#f0efec;font:16px/1.6 system-ui,sans-serif}main{max-width:820px;margin:3rem auto;padding:0 1.25rem}a{color:#86b6ef}</style></head>
<body><main><h1>AST masterclasses</h1><ul>
<li><a href="loom/index.html">x3d.loom</a>: eight sub-projects, the WebGPU bridge tracker cross-checked against the code</li>
<li><a href="xite/index.html">X_ITE 16.7.0</a>: the renderer itself; spec conformance, and eight learning heuristics with a curriculum weighted by your scenes</li>
<li><a href="onto/index.html">x3d.onto</a>: the Loom's birthplace; the X3D Ontology 4.1 tree, a 310-restriction narrowing proposal</li>
<li><a href="demo/index.html">x3d.demo</a>: the publishing shelf; 53 % of its function bodies are copies of Loom code</li>
<li>Earlier: x3d-blender-io (<code>../x3d-blender-io-masterclass</code>, port 8817) and x3d_mcp (<code>../x3d-mcp-masterclass</code>, port 8818)</li>
</ul></main></body></html>"""
    (ROOT / "index.html").write_text(top)
