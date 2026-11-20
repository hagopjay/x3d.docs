# x3d_mcp: an AST masterclass and teardown of the fork

The user's fork [hagopjay/x3d_mcp](https://github.com/hagopjay/x3d_mcp) of
[Web3DConsortium/x3d_mcp](https://github.com/Web3DConsortium/x3d_mcp), measured on 2026-11-13 at `origin/main`
`13121b6` (2026-11-03). It is compared against the fork base `74da0ec`, which is upstream `main` of 2026-08-05 and
the commit the fork's own work starts from (the first fork PR merged on 2026-10-11).

> **Dated page.** Every number below describes `13121b6`. Checked on 2026-11-20: the fork's `main` is at `bbd773f` and holds 59 `@mcp.tool` decorators (`grep -rn "@mcp.tool" src`), against the 48 tools counted here. Read the counts as history, not as the current state.

**Labels.** *Measured* numbers come from Python's `ast` over the source, `git`, `gh` and the x3d_mcp validator
itself. *Inferred* marks a heuristic: X3D node knowledge read from string literals, static call resolution, and
roles assigned by hand per package. *Claimed* marks a PR description. Nothing in the server was imported or
executed for this document. The method and tools are the same as the x3d-blender-io masterclass, with an
analyser extended for FastMCP registrations and validator rules.

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | 911 functions as a 3D force layout, coloured by package role, with 1,187 static call edges |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: which the tools build by name, and which a validator rule names |
| `scenes/fork-timeline.x3d` | main's first-parent history and the integration branch as two lanes, with arcs where PRs landed |
| `scenes/code-city.x3d` | modules as districts and functions as buildings; height is complexity, colour is fork-era status |

---

## 1. The shape of the server

```
  MCP client ──stdio / streamable HTTP──►  server.py (FastMCP, 189 lines)
                                              │ register(mcp) × 12 tool modules
       ┌──────────────────────────────────────┼───────────────────────────────────────┐
  tools/ (3,802 lines)                     validation/ (4,294)                   transfer/ (3,733, new)
  48 @mcp.tool, 4 @mcp.prompt,             XSD (x3d-4.0/4.1.xsd, libxml2),       blob store + HTTP upload/download,
  2 @mcp.resource                          semantic.py: 23 _check_* rules,       capped reads, jobs queue,
  workflow · granular · convert ·          hints.py (exact-fix), repair.py,      splat PLY/SPZ/X3D readers,
  query · validate_tool · render ·         profile.py, defuse.py, autofix,       inspect + chunk
  scene_ops · animate · semantics ·        splat_arrays, oversize
  claims · splats · transfer                     │
       │                                         ▼
  x3d_utils/ (1,964): SceneManager over x3d.py, X3DUOM, ontology (rdflib/SPARQL + guard), placement, claims,
                      gen_schema, json2xml
  playground/ (2,969, new): Accountability Playground web app (auth, store, loop, judge, mutate, report)
  dataset/ + evaluation/ (2,339): scene generators, augmentation, exact-fix evaluation, Gemini hint loop
```

These things are measured.

* **Three new subsystems.** The fork grew the package from 5,733 to 19,290 lines (3.4×) and from 214 to 911
  `def`s. Most of the growth is in three subsystems that did not exist at base: the **transfer layer** (#12,
  documents by id instead of pasted, because of the 4 MiB HTTP body limit), the **Accountability Playground**
  (#6, a private web app where a model writes a scene and the validator judges it), and **exact-fix hints** (#14,
  structured repairs for every validator error).
* **The validator is the core.** `validation/` is the largest role (4,294 lines). `semantic.py` grew from 715 to
  1,616 lines, and the new `hints.py` is 1,127 lines.
* **The MCP surface grew by 14 tools and 2 resources**, from 34 tools to 48. The 4 prompts are unchanged.
  Registration is uniform: every tool module exposes `register(mcp)`, and the decorated functions are closures
  inside it.
* **Imports:** 77 of the 550 import statements are lazy (inside functions). Because `src/` is put on `sys.path`,
  imports are absolute (`from validation.semantic import …`). The analyser resolves them that way.

| module | role | lines base -> head | defs | CC sum | max CC (function) |
|---|---|---|---|---|---|
| `validation.semantic` | validation | 715 -> 1616 | 52 | 530 | 57 (`_check_rigid_body_physics`) |
| `transfer.blobs` | transfer | new -> 1218 | 77 | 328 | 23 (`BlobConfig.from_env`) |
| `validation.hints` | validation | new -> 1127 | 47 | 500 | 68 (`_attribute_hint`) |
| `playground.app` | playground | new -> 681 | 49 | 193 | 17 (`run`) |
| `tools.render` | mcp-tools | 435 -> 550 | 23 | 70 | 11 (`_element_to_x3dom_html`) |
| `tools.animate` | mcp-tools | 519 -> 519 | 14 | 59 | 19 (`_animate`) |
| `validation.validate` | validation | 117 -> 472 | 23 | 110 | 16 (`_validate_xml`) |
| `dataset.generators.numeric_sequences` | dataset-eval | 454 -> 454 | 10 | 69 | 21 (`generate_interpolator`) |
| `evaluation.exact_fix_eval` | dataset-eval | new -> 446 | 18 | 218 | 78 (`sites`) |
| `tools.convert` | mcp-tools | 174 -> 437 | 12 | 132 | 38 (`_coerce_value`) |
| `tools.scene_ops` | mcp-tools | 326 -> 432 | 18 | 84 | 14 (`_move_node`) |
| `playground.store` | playground | new -> 406 | 60 | 129 | 11 (`JournalStore.load`) |
| `transfer.inspect_splats` | transfer | new -> 379 | 13 | 120 | 40 (`cloud_from_x3d`) |
| `playground.loop` | playground | new -> 344 | 11 | 79 | 27 (`run_loop.main`) |
| `dataset.augment` | dataset-eval | 317 -> 317 | 12 | 46 | 12 (`augment_instruction`) |
| `tools.validate_tool` | mcp-tools | 105 -> 316 | 8 | 43 | 11 (`register.validate_x3d`) |
| `transfer.spz` | transfer | new -> 315 | 18 | 73 | 18 (`unpack`) |
| `x3d_utils.gen_schema` | x3d-utils | new -> 312 | 13 | 121 | 40 (`build_generation_schema`) |
| `tools.splats` | mcp-tools | new -> 301 | 14 | 72 | 14 (`_chunk_job`) |
| `transfer.chunk` | transfer | new -> 301 | 12 | 94 | 30 (`build_envelope`) |
| `x3d_utils.scene` | x3d-utils | 264 -> 296 | 20 | 64 | 7 (`SceneManager.set_field`) |
| `x3d_utils.json2xml` | x3d-utils | new -> 290 | 13 | 97 | 30 (`_Writer.node`) |
| `x3d_utils.x3duom` | x3d-utils | 264 -> 270 | 12 | 55 | 11 (`X3DUOM.get_abstract_types`) |
| `evaluation.hint_loop_gemini` | dataset-eval | new -> 256 | 12 | 68 | 30 (`main`) |
| `playground.report` | playground | new -> 252 | 9 | 78 | 27 (`full_report`) |
| `tools.transfer` | mcp-tools | new -> 248 | 11 | 63 | 16 (`register.blob_put`) |
| `validation.oversize` | validation | new -> 246 | 13 | 66 | 24 (`oversize_result`) |
| `transfer.capped` | transfer | new -> 240 | 11 | 66 | 21 (`Capped.feed`) |
| `x3d_utils.ontology` | x3d-utils | 132 -> 238 | 14 | 48 | 9 (`X3DOntology.extension_status`) |
| `tools.workflow` | mcp-tools | 231 -> 231 | 5 | 58 | 33 (`register.compose_scene`) |

84 modules in all; the table shows the 30 largest. Lines by role: validation 4,294, mcp-tools 3,802, transfer 3,733, playground 2,969, dataset-eval 2,339, x3d-utils 1,964, server 189.

## 2. The taxonomy the AST reveals

### 2.1 The MCP surface (measured from decorators)

| module | MCP tools (new in the fork era: PR) |
|---|---|
| `tools.granular` | add_child, add_route, create_node, def_node, get_scene, remove_node, reset_scene, set_field, use_node |
| `tools.validate_tool` | autofix_x3d, **exact_fix_hints** (#14), **repair_x3d** (#6), validate_current_scene, validate_semantic, validate_x3d |
| `tools.semantics` | describe_ontology_term, node_parents, query_ontology, **query_ontology_page** (#13), **where_can_place** (#13) |
| `tools.query` | describe_node, list_components, list_nodes, list_profiles |
| `tools.render` | render_current_scene, render_image, x3dom_page, x3dom_starter |
| `tools.transfer` | **blob_delete** (#12), **blob_info** (#12), **blob_put** (#12), **blob_read** (#12) |
| `tools.animate` | add_x3d_route, animate_x3d_node, x3d_animation_info |
| `tools.claims` | **claim_append** (#13), **claims_page** (#13), **claims_verify** (#13) |
| `tools.scene_ops` | modify_x3d_node, move_x3d_node, remove_x3d_node |
| `tools.workflow` | compose_scene, create_geometry, create_scene |
| `tools.convert` | convert_x3d, **x3d_generation_schema** (#12) |
| `tools.splats` | **splat_chunk** (#12), **splat_inspect** (#12) |

Prompts: animate_scene, audit_scene, build_scene, convert_to_x3dom (unchanged). Resources (new, #13): ontology_turtle, placement_resource. HTTP routes on the server: _pulse, _root plus the transfer layer's upload/download routes registered in `transfer.routes` when blobs are enabled.

### 2.2 Validator rules (measured from `Diagnostic(level, check, …)` calls and reporter helpers)

At base the semantic validator had **19** named rules; at head it has **62** across 90 report sites (50 error-level
sites, 20 warning, 10 info, 1 warning-or-info, and 9 helper-reported sites whose level is a parameter). The rules run as 23 `_check_*`
functions in `semantic._ALL_CHECKS`. The splat inspector (`transfer.inspect_splats`) and `validation.splat_arrays`
report 10 rules each. The PR number is the first fork PR whose merge adds the rule. Rules from #1–#4 and #7–#8
landed on main inside #6 and #15.

| family | rules (new in fork era: PR; level) |
|---|---|
| splat | `sh-degree-dropped` (#12) info; `spherical-harmonics` (#12) info; `splat-array-length` (#2) error; `splat-array-syntax` (#12) error; `splat-no-color` (#2) warning; `splat-opacity-space` (#2) error; `splat-quaternion-norm` (#2) error/warning; `splat-quaternion-order` (#3) warning; `splat-scale-space` (#2) error; `splat-sh-partial` (#2) warning; `splat-values-unchecked` (#12) warning |
| route | `route-before-def` (#15) error; `route-invalid-from-field` error; `route-invalid-to-field` error; `route-missing-from-node` error; `route-missing-to-node` error; `route-never-fires` (#2) warning; `route-out-of-scope` (#15) error; `route-type-mismatch` error; `route-wrong-access-type` error |
| splat (inspect) | `all-invisible` (#12) error; `chunk-before-x3d` (#12) info; `coordinate-frame` (#12) info; `non-finite` (#12) error; `opacity-range` (#12) error; `scale-range` (#12) error; `zero-quaternion` (#12) error |
| physics | `physics-joint-body` (#11) error/warning; `physics-joint-cross-collection` (#11) error; `physics-mass` (#11) error; `physics-non-finite` (#11) error; `physics-not-in-collection` (#11) warning; `physics-zero-axis` (#11) error |
| counts and indices | `array-count-extra` (#8) (helper); `array-count` (#8) (helper); `index-out-of-range` (#7) error; `lod-range-order` (#8) (helper); `tuple-count` (#2) error |
| spec values | `colour-out-of-range` (#15) error; `cycle-interval-zero` (#7) (helper); `enum-invalid` (#7) (helper); `rotation-zero-axis` (#7) (helper); `value-out-of-range` (#7) (helper) |
| def/use | `duplicate-def` error; `unused-def` info; `use-before-def` error; `use-undefined-def` error |
| containerfield | `containerfield-not-node` error; `containerfield-type-mismatch` error; `containerfield-unknown` error |
| shape | `shape-no-appearance` info; `shape-no-geometry` warning |
| structure | `empty-group` warning; `no-viewpoint` info |
| interpolators | `interpolator-key-length` error; `interpolator-key-order` (#7) error |
| naming | `hanim-*-name` (#15) warning/warning/info; `naming-convention` error/warning |
| profile | `profile-component-fix` (#6) info; `profile-component` (#6) error |
| size limits | `start-tag-over-limit` (#12) info |
| protos | `proto-undeclared` (#7) error |

The **rule families track the user's other work**: splats (Gaussian-splat export from x3d-blender-io and the
star views), physics (#11, from the x3d-physx-bridge stress test, findings X-05…X-13), and counts/indices/spec
values (#7, #8, built from mutation sweeps on the X3D example archives).

### 2.3 X3D node knowledge (inferred from string literals)

XSD validation and the X3DUOM-driven checks (containerField, ROUTE field types, placement) cover **every** X3D
node generically. The sunburst therefore shows **node-specific** knowledge:

* a node a validator rule names (outer ring), and
* a node a generator builds by name (middle ring): an x3d.py constructor (`Transform(...)`), an
  `etree.SubElement(scene, "TimeSensor")`, or an emitted `<Tag`.

The granular tools can create any node through `getattr(x3d_mod, node_type)`. "Built by name" is therefore about
templates, not limits.

| | base `74da0ec` | head `13121b6` |
|---|---|---|
| X3D 4.1 nodes named in a validator rule | 52 | **80** |
| X3D 4.1 nodes built by name (tools, dataset, playground) | 21 | **30** |

| component | nodes | built by name (base -> head) | named by validator (base -> head) | validator names |
|---|---|---|---|---|
| Interpolation | 13 | 5 -> 5 | 12 -> 12 | ColorInterpolator, CoordinateInterpolator, CoordinateInterpolator2D, NormalInterpolator, OrientationInterpolator, PositionInterpolator, PositionInterpolator2D, ScalarInterpolator, SplinePositionInterpolator, SplinePositionInterpolator2D, SplineScalarInterpolator, SquadOrientationInterpolator |
| Rendering | 16 | 2 -> 2 | 5 -> 11 | Color, ColorRGBA, Coordinate, CoordinateDouble, IndexedLineSet, IndexedTriangleFanSet, IndexedTriangleSet, IndexedTriangleStripSet, LineSet, PointSet, TriangleSet |
| Geometry3D | 7 | 4 -> 5 | 7 -> 7 | Box, Cone, Cylinder, ElevationGrid, Extrusion, IndexedFaceSet, Sphere |
| Navigation | 7 | 1 -> 3 | 4 -> 5 | Billboard, Collision, LOD, NavigationInfo, Viewpoint |
| Shape | 10 | 3 -> 5 | 2 -> 2 | Appearance, Shape |
| CADGeometry | 6 | 0 -> 0 | 3 -> 4 | CADAssembly, CADLayer, CADPart, IndexedQuadSet |
| DIS | 6 | 0 -> 0 | 4 -> 4 | EspduTransform, ReceiverPdu, SignalPdu, TransmitterPdu |
| EnvironmentalEffects | 5 | 1 -> 1 | 0 -> 4 | Background, Fog, LocalFog, TextureBackground |
| Grouping | 4 | 1 -> 2 | 4 -> 4 | Group, StaticGroup, Switch, Transform |
| HAnim | 7 | 0 -> 0 | 3 -> 4 | HAnimHumanoid, HAnimJoint, HAnimSegment, HAnimSite |
| EventUtilities | 7 | 0 -> 0 | 0 -> 3 | BooleanToggle, IntegerTrigger, TimeTrigger |
| Geospatial | 11 | 0 -> 0 | 2 -> 3 | GeoLOD, GeoOrigin, GeoPositionInterpolator |
| Layout | 5 | 0 -> 0 | 2 -> 3 | LayoutGroup, ScreenFontStyle, ScreenGroup |
| Lighting | 4 | 2 -> 3 | 0 -> 0 | - |
| Shaders | 8 | 0 -> 0 | 0 -> 3 | ComposedShader, PackagedShader, ShaderProgram |
| RigidBodyPhysics | 14 | 0 -> 0 | 0 -> 2 | RigidBody, RigidBodyCollection |
| Text | 3 | 0 -> 0 | 1 -> 2 | FontStyle, Text |
| Texturing | 11 | 1 -> 1 | 0 -> 1 | TextureProperties |
| Core | 8 | 0 -> 1 | 0 -> 1 | ProtoInstance |
| GaussianSplats | 1 | 0 -> 0 | 0 -> 1 | GaussianSplats |
| Layering | 3 | 0 -> 0 | 1 -> 1 | Viewport |
| Networking | 4 | 0 -> 0 | 1 -> 1 | Anchor |
| PointingDeviceSensor | 4 | 0 -> 1 | 0 -> 0 | - |
| Scripting | 1 | 0 -> 0 | 1 -> 1 | Script |
| Time | 1 | 1 -> 1 | 0 -> 1 | TimeSensor |

Components no rule or generator names: CubeMapTexturing (3), EnvironmentalSensor (3), Followers (14), Geometry2D (8), KeyDeviceSensor (2), NURBS (13), ParticleSystems (10), Picking (5), Sound (21), TextureProjection (2), Texturing3D (7), VolumeRendering (13).

### 2.4 Package roles (assigned by hand per package, so inferred)

`validation` → `mcp-tools` → `x3d-utils` → `transfer` → `server` → `playground` → `dataset-eval`. This order fixes
the colours in every scene. They are the dataviz reference palette's dark steps, checked with its validator: all
checks pass.

## 3. Complexity and coupling

| function | CC | lines | nesting | fork era |
|---|---|---|---|---|
| `evaluation.exact_fix_eval:sites` | 78 | 91 | 4 | added |
| `validation.hints:_attribute_hint` | 68 | 98 | 4 | added |
| `validation.hints:_placement_hint` | 63 | 146 | 3 | added |
| `validation.semantic:_check_rigid_body_physics` | 57 | 101 | 5 | added |
| `transfer.inspect_splats:cloud_from_x3d` | 40 | 75 | 4 | added |
| `x3d_utils.gen_schema:build_generation_schema` | 40 | 62 | 2 | added |
| `evaluation.exact_fix_eval:build_corpus` | 40 | 70 | 4 | added |
| `transfer.inspect_splats:_inspect` | 39 | 132 | 2 | added |
| `tools.convert:_coerce_value` | 38 | 56 | 1 | modified (CC 31 -> 38) |
| `validation.semantic:_check_gaussian_splats` | 38 | 84 | 4 | added |
| `validation.splat_arrays:check_splat_arrays` | 37 | 94 | 3 | added |
| `validation.hints:apply_fix` | 35 | 98 | 4 | added |
| `tools.workflow:register.compose_scene` | 33 | 110 | 4 | unchanged |
| `validation.hints:_required_hint` | 33 | 47 | 3 | added |
| `validation.hints:_route_hints` | 33 | 58 | 4 | added |

These things are measured.

* **No god function.** 39 functions have CC > 20 and 4 have CC > 50. All four were added in the fork era:
  `exact_fix_eval.sites` 78 (an evaluation script), `hints._attribute_hint` 68, `hints._placement_hint` 63 and
  `semantic._check_rigid_body_physics` 57.
* **The fork era rewrote most of the code.** 697 functions were added, 52 modified and 162 left unchanged since
  `74da0ec`, by AST body hash. In the code city, most buildings are new.
* **Coupling** (cross-role call edges, inferred static resolution): `mcp-tools → transfer` 87 is by far the
  largest. Since #12, every tool reads its input and writes its output through the transfer layer
  (`transfer.outputs`, `transfer.tooling`): `tools.validate_tool → transfer.outputs` 21 and
  `→ transfer.tooling` 14. Next come `mcp-tools → x3d-utils` 27, `dataset-eval → validation` 16 and
  `validation → x3d-utils` 14. `validation.hints → validation.semantic` (15) is the exact-fix layer reading the
  rules.
* **The playground reuses the validator in process** but stays apart from the server. `playground.report` imports
  `validation.semantic`, `validation.validate` and `validation.repair`, and `playground.mutate` imports
  `validation.profile`: 5 call edges, and no call into `tools/` or `server`. In the call graph it is a separate
  green continent joined by a single thread.
* **Modules over 80 lines that no test file imports:** `server`, `tools.query` (4 MCP tools; possibly exercised
  through the server in other tests, not checked) and the `evaluation/` scripts.

## 4. The fork era, PR by PR

There are 16 PRs on hagopjay/x3d_mcp: **15 merged and 1 closed** (#10, a duplicate CI proposal; #9 merged
instead). The hagsmac fork has no PRs of its own; #11 came from `hagsmac:fix/physics-findings`. PRs #1–#4 and #7–#8
were merged into `integration/validator-fixes` and reached `main` inside #6 and #15, so the timeline draws them as
a second lane with arcs. Besides the PRs, `main` has an upstream sync (`d61d4de`, bringing in `ff0c0c9`, solar
system examples, no source change) and one direct commit (`13121b6`, the notebook `x3d_duo.ipynb`, 2,088 lines).
Each row compares that PR's own merge commit with its first parent.

| PR | date | into | what and why | AST delta (lines; functions +new -gone ~changed) | tools / rules added | tests (+functions) | CI on main |
|---|---|---|---|---|---|---|---|
| [#1](https://github.com/hagopjay/x3d_mcp/pull/1) | 10-11 | integration | **Accept ROUTEs into a shader's declared fields**. ROUTEs into a ComposedShader's declared `<field>` were flagged `route-invalid-to-field`; X_ITE runs them. | +7; +0 -0 ~2 | - | +2 | (integration) |
| [#2](https://github.com/hagopjay/x3d_mcp/pull/2) | 10-11 | integration | **Check MF tuple counts, GaussianSplats data and routes that never fire**. Files passing XSD and semantic checks were still wrong: 5-number `Coordinate point`, raw ln(scale)/logit(opacity) splats, routes that never fire. | +165; +5 -0 ~1 | 8 rules | +14 | (integration) |
| [#3](https://github.com/hagopjay/x3d_mcp/pull/3) | 10-12 | integration | **Warn when splat orientations look written w x y z**. Splats written w x y z (3DGS PLY order) render smeared in X_ITE (SSIM 0.888): warn. | +13; +0 -0 ~1 | 1 rules | +3 | (integration) |
| [#4](https://github.com/hagopjay/x3d_mcp/pull/4) | 10-12 | integration | **Fix three semantic-check false positives (ProtoInstance, Metadata ancestry, ROUTE proto lookup)**. Three false positives (ProtoInstance children, Metadata ancestry, ROUTE on ProtoInstance): 96 -> 22 error files on 264 example scenes. | +23; +0 -0 ~6 | - | +8 | (integration) |
| [#5](https://github.com/hagopjay/x3d_mcp/pull/5) | 10-13 | main | **Integrate 3D_perspective_skill: 720p default, blank-frame detection, optional extension ontologies**. Integrate npolys/3D_perspective_skill: 720p default renders, blank-frame detection, optional extension ontologies. | +203; +9 -0 ~13 | - | +14 | - |
| [#6](https://github.com/hagopjay/x3d_mcp/pull/6) | 10-15 | main | **Accountability Playground: write, validate, repair, render, judge** (includes #1-#4). Accountability Playground: a private web app where a model writes a scene, the validator judges, repair and render follow. Carries #1-#4. | +3781; +240 -0 ~19 | tools: repair_x3d; 11 rules | +118 | - |
| [#7](https://github.com/hagopjay/x3d_mcp/pull/7) | 10-16 | integration | **Check spec values the XSD lets through: protos, rotations, sizes, enums, indices, key order**. Spec values the XSD lets through: undeclared protos, zero-axis rotations, negative sizes, bad enums, indices, key order (mutation sweep caught 0% of five kinds). | +174; +6 -0 ~0 | 7 rules | +13 | (integration) |
| [#8](https://github.com/hagopjay/x3d_mcp/pull/8) | 10-16 | integration | **Add count and index checks for six fresh blind spots**. Count and index rules: blind mutation set caught 62.6% -> 100%, no new alarms. | +114; +4 -0 ~0 | 3 rules | +8 | (integration) |
| [#9](https://github.com/hagopjay/x3d_mcp/pull/9) | 10-17 | main | **ci: run the test suite on every push and pull request**. No automated checks: pytest on 3.12/3.13 per push and PR, plus a non-blocking Chromium render smoke. | no source change | - | - | success |
| [#11](https://github.com/hagopjay/x3d_mcp/pull/11) | 10-18 | main | **Fix physics findings: DEF ordering, convert_x3d, set_field booleans, physics semantic checks**. Physics stress test findings X-05/06/08/09/10/13: DEF ordering, convert_x3d containerField, SFBool, RigidBodyPhysics checks. | +286; +10 -0 ~11 | 6 rules | +26 | success |
| [#12](https://github.com/hagopjay/x3d_mcp/pull/12) | 10-26 | main | **Transfer layer: blob store, splat inspect/chunk, JSON input for convert_x3d**. 4 MiB HTTP body limit: documents by id (blob store), splat inspect/chunk on the server, JSON input for convert_x3d. | +5958; +296 -0 ~21 | tools: blob_delete, blob_info, blob_put, blob_read, splat_chunk, splat_inspect, x3d_generation_schema; 12 rules | +525 | success |
| [#13](https://github.com/hagopjay/x3d_mcp/pull/13) | 10-26 | main | **Ontology tools: SPARQL guard and deadline, paged query, placement table, claim ledger**. Ontology tools: SPARQL guard (no SERVICE/FROM), deadline, row cap, paged query, placement table, claim ledger. | +637; +34 -0 ~5 | tools: ontology_turtle, placement_resource, claim_append, claims_page, claims_verify, query_ontology_page, where_can_place | +25 | success |
| [#14](https://github.com/hagopjay/x3d_mcp/pull/14) | 10-29 | main | **Exact-fix hints: turn validator errors into structured repairs**. Exact-fix hints: every XSD/semantic error gets a structured, applicable repair (loom thesis loop A4/D17). | +1925; +82 -0 ~2 | tools: exact_fix_hints | +12 | success |
| [#15](https://github.com/hagopjay/x3d_mcp/pull/15) | 10-30 | main | **Merge integration fixes; add ROUTE order, colour range and H-Anim name checks** (includes #7, #8). Merge the integration branch (#7, #8) and add ROUTE order, colour range and H-Anim name checks; report libxml2 give-ups. | +767; +26 -0 ~6 | 14 rules | +43 | success |
| [#16](https://github.com/hagopjay/x3d_mcp/pull/16) | 11-01 | main | **Make the https XSI namespace repair test independent of the x3d.py version**. Test assumed x3d.py writes https XSI namespace; 4.0.65.8 writes http. | no source change | - | - | success |

**The phases:**

1. **Oct 11–12: closing validator blind spots (integration lane).** Shader-field ROUTEs, MF tuple counts,
   splat data, routes that never fire, the w x y z quaternion order, and three false positives. On 264 example
   scenes the error-level files fell from 96 to 22 (claimed).
2. **Oct 13–16: people can watch.** The perspective skill (720p renders, blank-frame detection) and the
   Accountability Playground. With the integration lane it carried, its merge added 3,781 lines and 240
   functions, the largest product addition.
3. **Oct 16–18: spec values and physics.** Mutation-sweep-driven count/index/value checks (claimed: a blind defect
   set went from 62.6 % to 100 % caught) and the physics findings from the PhysX bridge. CI arrives (#9).
4. **Oct 25–26: the transfer layer.** Blobs, splat inspect/chunk, JSON input: +5,958 lines, 296 functions, 23 new
   modules, and +525 test functions in one PR. Then ontology tools with a SPARQL guard.
5. **Oct 29–Nov 1: the repair loop.** Exact-fix hints (#14), the integration merge with ROUTE-order, colour and
   H-Anim checks (#15), and a test made robust to x3d.py's namespace change (#16).

## 5. How it is tested

* **Test functions (AST):** from 284 in 20 files to **1,047 in 51 files**. PRs quote pytest's *passed* count,
  which counts each parametrised case. That count is close to the AST count early on and drifts as
  parametrisation grows:

  | PR | 2 | 4 | 5 | 6 | 11 | 12 | 13 | 14 | 15 |
  |---|---|---|---|---|---|---|---|---|---|
  | claimed pytest passed | 342 | 358 | 296 | 442 | 476 (+7 skip) | 1,180 (+26) | 1,209 | 1,242 (+26) | 1,316 (+21) |
  | AST `test_*` functions at merge | 342 | 353 | 298 | 416 | 442 | 967 | 992 | 1,004 | 1,047 |

  The gap is consistent with `@pytest.mark.parametrize`. This is inferred: the parametrisation was not counted.
* **CI (measured, `gh run list`):** the `tests` workflow arrived with #9 on 2026-10-17. It runs pytest on
  Python 3.12 and 3.13 (installing `.[dev,playground]` plus httpx and pillow), and a **non-blocking** headless
  Chromium render smoke test. All **8 runs on `main` succeeded**. Across all branches there were 18 runs: 15
  succeeded, 2 were cancelled and 1 failed (`fix/physics-findings` at `fa0b389`, before #11 merged).
* **Before #9 there was no CI.** PRs #1–#8 were tested locally; their descriptions quote local pytest runs.
* **Evaluations outside CI:** `evaluation/exact_fix_eval.py` and `hint_loop_gemini.py` measure the hint loop. #14
  states its own limits: valid is not the same as intended, fewer than half of the repairs restore the original
  scene, and the mutation classes and the hint rules were written by the same author.

## 6. Insights

1. **The fork turned a generator into a judge.** At base, x3d_mcp was mostly tools that build scenes. The fork
   era's weight is in judging them (62 rules, exact-fix hints, repair) and in moving big documents (the transfer
   layer). Validation is now the largest role, and every tool's input and output passes through the transfer layer.
2. **Rules come from real failures.** Every rule family maps to an incident with a measured before and after: X_ITE
   rendering splats smeared (#3), physics stress-test findings (#11), mutation sweeps (#7, #8), 96 → 22 false
   positives (#4). That is the "accountability" theme made concrete.
3. **The integration branch worked as a staging lane.** Six validator PRs were reviewed small and landed in two
   merges. The cost: two merges carry 6 PRs' worth of rules each, and `semantic.py` clashed with the hints in #15.
4. **The playground is a client of the validator, not of the server.** It imports `validation.*` directly. That is
   simple and fast, but the playground does not exercise the MCP tool surface it showcases.
5. **Upstream has not moved since the fork.** `upstream/main` has 0 commits that are not in the fork. The fork is
   106 commits ahead. Three PRs offered upstream (#33, #34 "Integration/validator fixes", #35 ontology) were
   closed without merging.

## 7. Risks and recommendations

| risk (evidence) | recommendation |
|---|---|
| The render smoke job is non-blocking; the playground and render paths can break silently | Make the smoke job blocking on `main` with the pinned full-Chromium recipe (`smoke-ci-findings.md`: X_ITE's wasm pages crash headless-shell). |
| `hints.py` (1,127 lines, 2 functions with CC > 60) is tested by its own author's mutation classes (#14's stated limit) | Add an independent defect corpus (for example x3d-blender-io's 194-case suite output and real user scenes) and report hint success on it separately. |
| `server` and `tools.query` have no test file importing them | Add an in-process FastMCP round trip that lists tools and calls each one with a minimal valid input (`test_inprocess_signatures.py` is a start). |
| Two branches carry unmerged work: `origin/claude/ontology-lentz-polys-3j5h8z` (`use-type-mismatch` check, 1 commit) and `origin/loom/exact-fix-gemini` (2 commits of Gemini hint-loop runs). The local `bridge/agents-slice` (worktree `x3d_mcp-agents-slice`) has 1 unpushed commit (MuJoCo bridge tools). | Decide on each. The `use-type-mismatch` rule looks like a candidate for the next validator PR. |
| The local checkout sits on `fix/physics-findings` (merged as #11); local `main` is 72 commits behind `origin/main` | Fast-forward local `main`. Not done here. |
| The rule PR attribution passes through merges (#6 carries #1–#4) | Keep `docs/` change notes per rule (as #15 did with `ROUTE-COLOUR-HANIM-CHECKS.md`) so blame survives the staging lane. |
| Upstream divergence (106 ahead, 3 upstream PRs closed) | If upstream contribution still matters, split out the false-positive fixes (#4) and the physics checks (#11) as small upstream PRs. They have the least fork-specific coupling. |

## 8. Method and limits

* This uses the same analyser as the x3d-blender-io masterclass (`tools/astlib.py`), extended for dotted
  absolute imports, FastMCP decorators (`@mcp.tool/prompt/resource/custom_route`), validator report calls
  (`Diagnostic(level, check)` and reporter helpers like `report("error", "physics-mass", …)`), and x3d.py
  constructors and `etree.SubElement` as node generation.
* **Two analyser bugs were found and fixed while making this document.** (1) Nested `def`s directly in a function
  body were charged to the outer function. (2) Each `elif` counted one nesting level deeper. Both masterclasses were
  recomputed. The x3d-blender-io document carries a correction note: `export_x3d.export` has its own CC 8, not
  287. Its 29 closures sum to 310.
* Call resolution is static. FastMCP's dispatch to tool closures and any `getattr` construction are not drawn.
  The graph has 1,187 distinct edges between functions (1,201 resolved targets including recursion).
* `tools/era.py` analyses every first-parent commit since `74da0ec` and each PR's own merge commit with
  `git show`, with no checkout.
* All scenes validate with this very repo's validator (XSD 4.0 valid; semantic 0 errors, 0 warnings). They were
  rendered in the Claude app's browser pane (X_ITE 16.7.0, software WebGL). They were not checked on a real GPU.

### Reproduce

```bash
cd ~/Projects/x3d/work/x3d-mcp-masterclass
python3 tools/run_snap.py base && python3 tools/run_snap.py head      # snap/* = git archive 74da0ec / origin/main
python3 tools/coverage.py head && python3 tools/mcp_taxonomy.py && python3 tools/era.py
python3 tools/scenes.py && python3 tools/doc_tables.py && python3 tools/build_doc.py && python3 tools/build_index.py
python3 -m http.server 8818 --bind 127.0.0.1
```
