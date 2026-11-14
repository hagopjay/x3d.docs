# x3d.onto: an AST masterclass and teardown

[hagopjay/x3d.onto](https://github.com/hagopjay/x3d.onto) (private; default branch `claude/project-thread-3mgt8g`, head 554c647),
measured 2026-11-13. hagsmac/x3d.onto is a fork with the same head (0 ahead, 0 behind). The repo starts on 2026-10-27
("extracted from the Mac working tree") and its last change is 2026-11-04: 67 commits, 37 first-parent steps,
17 PRs, all merged (#6 and #7 into `dynasty-loom/*` branches, the rest into the default branch; #15 was merged despite its
"[Do not merge yet]" title). No CI: the repo has no Actions runs. 6 remote branches are not merged (`dspy-agent`,
`project-thread-bfwscy`, `dynasty-loom/v2` and `v3`, `loom/gemini-api`, `loom/lawful-gemini`).

**Labels** as in the x3d.loom masterclass. The ontology lens adds rdflib 7.6.0 (from the x3d_mcp venv, already installed):
every `.ttl` file parsed, classes, properties, `rdfs:subClassOf` and OWL restrictions counted.

| scene | what it shows |
|---|---|
| `scenes/ontology-hierarchy.x3d` | **the X3D Ontology 4.1 class tree** in 3D: 364 classes, levels by depth; gold = new in 4.1, blue ring = narrowed by the proposal, orange halo = named by the sim vocabularies, size = use in the repo's scenes |
| `scenes/callgraph-3d.x3d` | 186 files, 1724 functions, 1581 in-file and 26 cross-file calls |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the 253 X3D files (orange) and named in code (blue) |
| `scenes/fork-timeline.x3d` | 37 steps from 2026-10-27 to 2026-11-04 |
| `scenes/code-city.x3d` | functions as buildings per directory; amber = body in 2+ files |

## 1. What the AST says x3d.onto is

**An ontology repo whose code is mostly worlds.** Only **7 of 175 Python files** touch the ontology (import rdflib, run
SPARQL or name a `.ttl`): `harness/build.py` (6 SPARQL queries), `harness/build_sim.py`, `harness/proposal_sketch.py`,
`harness/test_harness41.py`, `harness/xslt_diagnosis.py`, `demo/audit_numbers.py`, `demo/build_tour.py`. The ontology itself
lives in data: two copies of the official X3D Ontology (4.0 and 4.1, 1.1 MB each), one proposal, and 8 small "sim"
vocabularies. Everything else is scenes built *from* the ontology's knowledge: the Dynasty Loom genealogy hypersphere
(half of all code), the Gobbler demiurge village, the v2 Sun-Earth-Moon village of 364 classes, and the cross-domain tools.

| role (hand-assigned from directory names) | code files | code lines | functions | X3D files | X3D MB |
|---|---|---|---|---|---|
| dynasty-loom (genealogy hypersphere) | 61 | 17,534 | 1,476 | 9 | 5.2 |
| xdomain (fuzz, lawful metric, URDF/glTF, eval) | 37 | 3,737 | 298 | 224 | 0.0 |
| Gobbler demiurge + v4 | 47 | 6,909 | 620 | 10 | 4.2 |
| Loom gates (loom, loom-feedback, tools, evidence) | 54 | 2,523 | 267 | 8 | 0.3 |
| v2 Sun-Earth-Moon village | 18 | 2,194 | 363 | 0 | 0.0 |
| v1 explorer, harness, demo, data | 22 | 1,664 | 159 | 2 | 0.5 |
| sim ontologies + proposal | 0 | 0 | 0 | 0 | 0.0 |
| docs and root | 7 | 457 | 49 | 0 | 0.0 |

* **Code:** 35,018 lines in 246 files (html 9, py 175, js 62), 3,169 named function definitions; 156 over complexity 20, 38 over 50.
* **Scenes:** 253 X3D files, 10.1 MB; X3D 4.1 226, X3D 4.0 27; profiles Full 204, Immersive 32, Interchange 8, Interactive 4, CADInterchange 3, MedicalInterchange 2. 224 of them are the `xdomain` differential
  validator fuzzer's corpus (small X3D 4.1 Full-profile files). 25 files use protos, 3 a Script, 147 ROUTEs in all.
* **Little copying:** 137 of 1,734 functions of 3+ lines have a body in another file (8 %), far less than the Loom (31 %) or
  the demo shelf (69 %).
* **Tests:** 101 Python `test_*` functions and 9 JS `test(`/`it(` calls, no CI to run them.

### Hot spots (measured; one row per distinct body)

| function | CC | lines | nesting |
|---|---|---|---|
| `dynasty-loom/gates/datagates.py::check` | 165 | 201 | 4 |
| `dynasty-loom/ingest/ingest.py::main` | 162 | 247 | 5 |
| `dynasty-loom/tapestry/build_loom_scene.py::gen_stops` | 145 | 171 | 3 |
| `dynasty-loom/ingest/build.py::Builder.person` | 130 | 147 | 4 |
| `dynasty-loom/ingest/loomview.py::compute` | 126 | 144 | 3 |
| `dynasty-loom/gates/run_gates.py::main` | 119 | 142 | 4 |
| `xdomain/lawful/metric.py::score` | 119 | 126 | 4 |
| `dynasty-loom/x3d/build_genealogy_x3d.py::build` | 115 | 234 | 3 |
| `xdomain/urdf/urdf_check.py::check` | 113 | 122 | 5 |
| `dynasty-loom/tapestry/build_loom_scene.py::plan` | 111 | 143 | 4 |
| `xdomain/lawful/offline.py::summarise_live` | 108 | 63 | 4 |
| `dynasty-loom/tapestry/tools/write_receipt.py::main` | 104 | 118 | 2 |

Every top function is in `dynasty-loom` or `xdomain/lawful`: data gates (`datagates.check` 165), ingest (`ingest.main` 162),
scene generation (`gen_stops` 145) and the lawful metric (`metric.score` 119). These are long single-pass builders; they
read top to bottom, but each is a candidate for splitting by stage.

## 2. The ontology lens (measured with rdflib)

| file | triples | OWL classes | object props | datatype props | subClassOf |
|---|---|---|---|---|---|
| `data/X3dOntology4.0.ttl` | 17,736 | 355 | 326 | 712 | 440 |
| `data/X3dOntology4.1.ttl` | 18,121 | 364 | 337 | 727 | 454 |
| `proposal/X3dOntology4.1.narrowing-sketch.ttl` | 2,088 | 56 | 0 | 0 | 0 |
| `sim/agency.ttl` | 97 | 0 | 0 | 0 | 0 |
| `sim/geons.ttl` | 119 | 0 | 0 | 0 | 0 |
| `sim/heritage.ttl` | 105 | 0 | 0 | 0 | 0 |
| `sim/parts_contact.ttl` | 131 | 0 | 0 | 0 | 0 |
| `sim/perspective.ttl` | 137 | 0 | 0 | 0 | 0 |
| `sim/prepositions.ttl` | 134 | 0 | 0 | 0 | 0 |
| `sim/scale.ttl` | 121 | 0 | 0 | 0 | 0 |
| `sim/verification.ttl` | 64 | 0 | 0 | 0 | 0 |

* **4.0 → 4.1:** 355 → 364 classes, **+9, none removed**: EnvironmentLight, FontLibrary, GaussianSplats, HAnimPose, InlineGeometry, RenderedTexture, Tangent, X3DTangentNode, X3DUrlOutputObject.
* **The narrowing proposal** (`proposal/X3dOntology4.1.narrowing-sketch.ttl`, 2,088 triples, none of them in 4.1) adds
  **310 `owl:allValuesFrom` restrictions on 143 classes**. It narrows what a node field may hold, mostly
  `hasChildren` (42), `hasColor`, `hasTexCoord`, `hasCoord` (15 each), `hasNormal` (14), `hasAttrib` (13), `hasFogCoord`
  (13). In the official ontology these SFNode/MFNode properties accept any X3D node; the proposal encodes the spec's
  acceptable node types, which is what x3d_mcp's `where_can_place` and containerField checks need. HAnimHumanoid gets the
  most (12), then the geometry sets (7 each).
* **The sim vocabularies** (`sim/*.ttl`: agency, geons, heritage, parts_contact, perspective, prepositions, scale,
  verification; 64–137 triples each) define no OWL classes. They are graded statements in a private namespace
  (`example.invalid/sim/spatial-cognition#`) with `x3dNode` / `x3dField` / `onNode` links into X3D 4.1: perspective → Viewpoint,
  NavigationInfo, OrthoViewpoint; scale → GeoCoordinate, GeoLOD, LOD, `unit`; parts_contact → SingleAxisHingeJoint, Cone;
  prepositions → Transform. 35 X3D terms are named this way (orange halos in the hierarchy scene).

## 3. Taxonomy: X3D used by the scenes

Node types used, by number of files: Appearance (42), Shape (41), NavigationInfo (31), Transform (31), Group (30), Coordinate (27), ProtoInstance (25), Background (24), CADFace (23), PhysicalMaterial (21), Viewpoint (19), ParticleSystem (19), GeoLOD (17), IndexedLineSet (15), IndexedFaceSet (15). Components touched: Rendering 11, Sound 9, Shape 8, Texturing 7, Geospatial 7, NURBS 7, Navigation 6, Interpolation 6, HAnim 6, ParticleSystems 5, Picking 5, VolumeRendering 5, EnvironmentalEffects 4, Grouping 4, Geometry3D 4, Core 4, Networking 4, DIS 4, CADGeometry 4, Layout 4, RigidBodyPhysics 4, Lighting 3, Text 3, Shaders 3, Texturing3D 3, Layering 3, EventUtilities 2, CubeMapTexturing 2, Geometry2D 2, PointingDeviceSensor 1, Time 1, EnvironmentalSensor 1, GaussianSplats 1, Scripting 1, Followers 1.

The code names all 267 node types only because `explorer.html` embeds the complete node table (284 names); without it,
the most is 43 (`dynasty-loom/x3d/build_genealogy_x3d.py`).

## 4. The history, step by step

| step | date | title | code delta | X3D delta |
|---|---|---|---|---|
| `9d5fd9b` | 10-27 | Add Gobbler v4 vision spec from owner's answers | +0 lines; +0 -0 ~0 fns | - |
| `ec56def` | 10-27 | PLAN: drop a private artifact link | +0 lines; +0 -0 ~0 fns | - |
| `268c94d` | 10-27 | Gobbler v4: hover and UI-corner spec, mock on the owner's stills, placement function with tests, pick benchmarks | +457 lines; +43 -0 ~0 fns | - |
| `9faf90e` | 10-28 | Gobbler v4 step 1: live hover, none/minimal UI and corner cards on the Gobbler 3 Deep scene | +1,836 lines; +170 -0 ~0 fns | - |
| `be53dca` | 10-28 | Gobbler v4: fixes from the first review pass, phone-touch and bad-parameter suites | +53 lines; +5 -0 ~14 fns | - |
| `9195527` | 10-28 | Gobbler v4: tuning panel (key T), second review pass fixes, frames and docs | +64 lines; +9 -1 ~16 fns | - |
| `9aa9cb8` | 10-28 | Gobbler v4: published copy carries the scene as .xml | +7 lines; +0 -0 ~2 fns | - |
| `91e13e9` | 10-28 | Gobbler demiurge step 2: bird-first page (honest staged loader, gzip delivery, Face view, four controls) | +840 lines; +73 -0 ~0 fns | - |
| `3f2c16e` | 10-28 | Gobbler demiurge: validator helper takes the fork checkout from X3D_MCP | -1 lines; +0 -0 ~0 fns | - |
| `c8dfcbb` | 10-28 | Gobbler demiurge: T = tour and Shift+T = tuning (plan key rule), step-3 notes from the planning review, honest fps row | +7 lines; +0 -0 ~1 fns | - |
| `85b88ed` | 10-28 | Gobbler demiurge: key table on the page names T = tour and Shift+T = tuning | +0 lines; +0 -0 ~0 fns | - |
| `598a941` | 10-28 | Gobbler demiurge step 5: feathers modelled in Blender, golden-hour light baked, exported through the blenderizer; fan unfurls on approach | +378 lines; +27 -0 ~3 fns | +3 X3D files (+0.2 MB); scenes start using 3 node types |
| `860e73a` | 10-28 | Gobbler demiurge steps 6 and 7: spline tour over the shot list with seeded drift, preening wave, weaving shuttles, flight bows; the heart beats a replay of 30 real validator runs | +128 lines; +11 -0 ~6 fns | - |
| `e8e19bf` | 10-28 | Gobbler demiurge: tour route round the underside, thinner heart ping, fan frame, README for steps 5 to 7, unused mid vane dropped | +1 lines; +0 -0 ~2 fns | - |
| `114420e` | 10-28 | Gobbler demiurge: page text names the heartbeat, the Blender feathers and the seed parameter | +0 lines; +0 -0 ~0 fns | - |
| `a986523` | 10-28 | Gobbler demiurge step 8: the shell tenders are H-Anim humanoids modelled in Blender, three gaits, walking the ribcage | +251 lines; +14 -0 ~4 fns | +1 X3D files (+0.0 MB); scenes start using 2 node types |
| `0f6be62` | 10-28 | Gobbler demiurge step 3 and 11: Earth, Moon and the village from Blender, ladder stops 4 to 7, the picture-judge test | +856 lines; +86 -1 ~19 fns | +2 X3D files (+1.4 MB) |
| `874c45b` | 10-29 | Gobbler demiurge: lighting, materials and shaders pass on the world (baked village light, atmosphere, fountain, clothed villagers, earthshine) | +437 lines; +35 -2 ~34 fns | +3 X3D files (+2.2 MB) |
| `593dbcd` | 10-29 | Gobbler demiurge step 10: sound on M (a bed for the cosmos, a bed for the village, the Sun's heartbeat) | +230 lines; +29 -0 ~2 fns | - |
| `bb56a8d` | 10-29 | Gobbler demiurge: a published copy can carry the beds as .mp4 (same container), sound.js is ASCII only | +1 lines; +0 -0 ~3 fns | - |
| `4fd3cdd` | 10-29 | Gobbler demiurge: README no longer lists music as open (it is built, unlistened on a real device) | +0 lines; +0 -0 ~0 fns | - |
| `92bcaa6` | 10-29 | Gobbler demiurge: correct numbers and wording found by a fact-check of the tech breakdown | +0 lines; +0 -0 ~0 fns | - |
| [#1](https://github.com/hagopjay/x3d.onto/pull/1) | 10-29 | Loom thesis loop: gate lints, lawful metric + DSPy, differential validator fuzzer | +3,066 lines; +209 -0 ~0 fns | +224 X3D files (+0.0 MB); scenes start using 102 node types |
| [#2](https://github.com/hagopjay/x3d.onto/pull/2) | 10-29 | Gobbler demiurge: Mashtots ring, a khachkar in the plaza, and the Armenian knot | +1,115 lines; +76 -0 ~9 fns | +1 X3D files (+0.4 MB) |
| [#3](https://github.com/hagopjay/x3d.onto/pull/3) | 10-30 | Loom gate: flag raw shader CDATA, and record the genealogy loom's findings | +49 lines; +2 -0 ~2 fns | +4 X3D files (+0.0 MB); scenes start using 2 node types |
| [#4](https://github.com/hagopjay/x3d.onto/pull/4) | 10-31 | Loom gate: leave an int compared inside a float builtin alone | +6 lines; +0 -0 ~2 fns | - |
| [#5](https://github.com/hagopjay/x3d.onto/pull/5) | 10-31 | dynasty-loom: Dynasty Loom v3 under version control, exactly as published | +14,448 lines; +1062 -0 ~0 fns | +9 X3D files (+5.1 MB); scenes start using 5 node types |
| [#8](https://github.com/hagopjay/x3d.onto/pull/8) | 11-01 | Dynasty Loom v2 + v5 into the default branch (follow-up to #6 and #7) | +3,086 lines; +357 -2 ~53 fns | - |
| [#9](https://github.com/hagopjay/x3d.onto/pull/9) | 11-01 | Loom gate: color-emissive-white, a white emissive washes out per-face colours (FACTS Q, from x3d-ray) | +79 lines; +4 -0 ~1 fns | +2 X3D files (+0.0 MB); scenes start using 1 node types |
| [#10](https://github.com/hagopjay/x3d.onto/pull/10) | 11-04 | Loom v1: consolidated definition, sources, learnings and loomkit | +1,235 lines; +48 -0 ~0 fns | - |
| [#11](https://github.com/hagopjay/x3d.onto/pull/11) | 11-04 | Fold back: Gear Loom mechanism gates (tools/gear_loom) | +156 lines; +17 -0 ~0 fns | - |
| [#12](https://github.com/hagopjay/x3d.onto/pull/12) | 11-04 | Fold back: Break-the-Loom mutant/control detectors (tools/break_loom) | +255 lines; +38 -0 ~0 fns | - |
| [#13](https://github.com/hagopjay/x3d.onto/pull/13) | 11-04 | Fold back: Data City source-to-scene truth gates (tools/loom_data_city) | +268 lines; +13 -0 ~0 fns | +1 X3D files (+0.1 MB); scenes start using 2 node types |
| [#14](https://github.com/hagopjay/x3d.onto/pull/14) | 11-04 | Fold back: Loomsong IV fidelity predicates (tools/loom_fidelity_v4) | +92 lines; +9 -0 ~0 fns | - |
| [#15](https://github.com/hagopjay/x3d.onto/pull/15) | 11-04 | [Do not merge yet] Fold back: IFC bridge contracts and world-triangle witness (tools/loom_ifc_bridge_v1) | +145 lines; +17 -0 ~0 fns | +1 X3D files (+0.2 MB) |
| [#16](https://github.com/hagopjay/x3d.onto/pull/16) | 11-04 | Fold back: Gobbler Cabinet residency, profiler and radiance contracts (loom-feedback/gobbler-cabinet) | +197 lines; +65 -0 ~0 fns | - |
| [#17](https://github.com/hagopjay/x3d.onto/pull/17) | 11-04 | Fold back: Linked Observatory arrival, join and scope contracts (loom-feedback/linked-observatory) | +125 lines; +43 -0 ~0 fns | - |

**Phases.** Oct 27–28: the extraction and Gobbler v4. Oct 30–31: the Loom thesis loop (gate lints, lawful metric with DSPy,
differential validator fuzzer), Gobbler demiurge, and Dynasty Loom v2, v3 and v5 under version control. Nov 1: gates
(color-emissive-white). Nov 4: **Loom v1** consolidated and seven fold-back PRs (#11–#17) that move gates from other
projects (gear loom, break-the-loom, data city, Loomsong fidelity, IFC bridge, Gobbler cabinet, linked observatory) into
the method. The next day the method moved to its own repo, x3d.loom (created 2026-11-05), and x3d.onto stopped changing.

## 5. Insights, risks, recommendations

1. **x3d.onto is the Loom's birthplace.** Its last week is the Loom v1 consolidation; x3d.loom starts the day after. The
   gates, laws and fold-back pattern began here. Worth stating in both READMEs so the lineage is not lost.
2. **The proposal is the most reusable artefact.** 310 restrictions that turn "any node" into the spec's acceptable types
   are exactly what a validator or a generator needs. Recommendation: test it against x3d_mcp's X3DUOM-based placement
   table (they should agree node by node) and, if they do, offer it upstream to Web3D with that agreement as evidence.
3. **Two copies of a 1.1 MB official ontology** are vendored without a source pin. Record the upstream URL and date, or
   fetch them in the harness, so a refresh is a diff and not a mystery.
4. **101 tests, no CI.** A single pytest workflow would protect the harness and the gates; the repo is small enough.
5. **The sim vocabularies** use a placeholder namespace (`example.invalid`). Give them a real one before anything links to
   them.

## 6. Method and limits

As in the x3d.loom masterclass, plus `tools/onto_lens.py` (rdflib over every `.ttl`, Python `ast` for SPARQL strings and
`.ttl` paths). `v2/tour.js` inlines a minified bundle and is excluded from function counts. Restriction counts are taken
from `rdfs:subClassOf` blank nodes in the proposal. The hierarchy scene draws the 412 `rdfs:subClassOf` edges between
classes that are themselves declared `owl:Class` (454 in the file; the rest point at classes declared elsewhere).
