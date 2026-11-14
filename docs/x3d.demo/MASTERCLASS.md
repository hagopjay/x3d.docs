# x3d.demo: an AST masterclass and teardown

[hagopjay/x3d.demo](https://github.com/hagopjay/x3d.demo), `main` d10b457, measured 2026-11-13 ("Demo repo for x3d-io.ai
work", GitHub Pages from `docs/`). Created 2026-11-07; 26 first-parent steps; 25 PRs, all merged. The local checkout's
`origin` is hagsmac/x3d.demo, which is 40 commits behind (last change 2026-11-07); this analysis uses hagopjay's `main`.

**Labels** as in the x3d.loom masterclass: measured (ASTs, XML walk, git, gh), inferred (call resolution, literal node
names, roles from demo folder names), claimed (PR text). Nothing executed or installed.

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | 97 files (28 more are exact copies), 3113 functions, 3100 in-file calls and only 5 cross-file calls |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the 111 X3D files (orange) and named in code (blue) |
| `scenes/fork-timeline.x3d` | 26 steps of `main` with code lines per role, X3D megabytes, new node types, Pages deploys |
| `scenes/code-city.x3d` | functions as buildings per demo folder; amber = the same body exists in 2+ files |

## 1. What the AST says the demo repo is

A **publishing shelf**. Every demo is a self-contained page: 3100 calls inside files, 5 across files. Each new
version is a new folder (`v1`, `v2` …) and the old one is never edited: across all 26 steps of history the AST sees
**0 functions changed**, only added. That makes the repo append-only by construction.

| role (hand-assigned from directory names) | code files | code lines | functions | X3D files | X3D MB |
|---|---|---|---|---|---|
| Babylon/WebGPU ports | 25 | 27,008 | 3,047 | 25 | 32.8 |
| X_ITE demos | 59 | 15,979 | 3,016 | 62 | 37.8 |
| collider events + heritage facade | 12 | 31,104 | 2,318 | 2 | 23.4 |
| physics (Ten Minute Physics, MuJoCo bridge) | 20 | 6,985 | 279 | 17 | 26.9 |
| STEM studies | 39 | 4,505 | 365 | 5 | 0.0 |
| doc shelf (index, versions) | 20 | 387 | 39 | 0 | 0.0 |

* **Code:** 85,968 lines in 175 files (html 59, js 61, py 55), 8,963 named function definitions, 409 vendored files excluded (X_ITE and Babylon builds).
  One page (`x3d-mujoco-bridge/v1/index.html`) inlines a minified bundle and is excluded from function counts.
* **Scenes:** 111 X3D files, 120.9 MB: X3D 4.0 100, X3D 4.1 11; profiles Immersive 91, Full 17, Interchange 3. 3,767 ROUTEs, 1 file with a Script, 6 files with a ProtoInstance.
  The largest are `hall.x3d` (13 MB), `facade.x3d` (11 MB, twice) and `pantheon.x3d` (6 MB).
* **Duplication:** 2784 of 4056 functions of 3+ lines (69 %) have a body that exists in another file, and 28 files
  are exact copies. **2,139 of 4056 function bodies (55 % of the function lines) are identical to functions in
  x3d.loom**: the HEP collider pages, the brain/torso pages, the heritage facade and the WebGPU ports are copies of the
  Loom's viewers. The demo repo is a downstream mirror of the Loom's pages.

### Hot spots (measured; one row per distinct body)

| function | CC | lines | nesting |
|---|---|---|---|
| `docs/demos/heritage-facade/v1/facade.html::frame` (same body in 2 files) | 154 | 266 | 5 |
| `docs/demos/collider-events/v1/dijet.html::frame` (same body in 10 files) | 144 | 239 | 5 |
| `docs/demos/tether-firehose/v4/index.html::drawWF` | 142 | 80 | 2 |
| `docs/demos/tether-firehose/v4/index.html::drawMatrix` | 123 | 60 | 3 |
| `docs/demos/gobbler-demiurge-webgpu/v1/src/hover.js::start.frame` (same body in 2 files) | 96 | 51 | 3 |
| `docs/demos/tether-firehose/v4/index.html::liveTether` | 93 | 40 | 3 |
| `docs/demos/gobbler-demiurge-webgpu/v1/src/hover.js::start` (same body in 2 files) | 87 | 340 | 1 |
| `docs/demos/tether-firehose/v4/index.html::patchRow` | 80 | 30 | 3 |
| `docs/demos/tether-firehose/v4/index.html::cardShow` | 76 | 18 | 3 |
| `docs/demos/tether-firehose/v4/index.html::drawScope` | 76 | 49 | 5 |
| `docs/demos/tether-firehose/v4/index.html::run` | 69 | 28 | 1 |
| `docs/demos/tether-firehose/v4/index.html::restore` | 67 | 15 | 4 |

The top entries are the Loom's WebGPU viewer `frame` loop, copied into each collider and facade page.

## 2. Taxonomy: X3D used by the demos

Node types used, by number of files: Shape (103), Appearance (103), Transform (101), Viewpoint (90), Coordinate (87), NavigationInfo (86), Background (82), TimeSensor (66), PhysicalMaterial (58), DirectionalLight (57), WorldInfo (51), Material (50), IndexedTriangleSet (40), Color (39), PositionInterpolator (38). Components touched: Rendering 11, Shape 7, Geometry3D 7, Navigation 6, Texturing 6, Interpolation 6, Geospatial 5, Core 4, Lighting 3, Grouping 3, Shaders 3, EventUtilities 3, EnvironmentalEffects 2, Text 2, HAnim 2, ParticleSystems 2, Geometry2D 2, NURBS 1, GaussianSplats 1, Time 1, Networking 1, PointingDeviceSensor 1, EnvironmentalSensor 1, Texturing3D 1, Scripting 1.

The code names 122 node types, more than the 82 the scenes use, because the embedded WebGPU reader (from the Loom bridge)
carries its own node table.

## 3. The history, step by step

| step | date | title | code delta | X3D delta |
|---|---|---|---|---|
| [#1](https://github.com/hagopjay/x3d.demo/pull/1) | 11-07 | Demo doc v1: three WebGPU demos, versioned | +15,553 lines; +1117 -0 ~0 fns | +1 X3D files (+11.7 MB); scenes start using 4 node types; code names 44 more |
| [#2](https://github.com/hagopjay/x3d.demo/pull/2) | 11-07 | Demo doc v2: fix "no adapter" on the demo pages | +15,594 lines; +1119 -0 ~0 fns | +1 X3D files (+11.7 MB) |
| [#3](https://github.com/hagopjay/x3d.demo/pull/3) | 11-07 | Demo doc v3: explain the Chrome WebGPU blocklist | +24 lines; +1 -0 ~0 fns | - |
| [#4](https://github.com/hagopjay/x3d.demo/pull/4) | 11-07 | Demo doc v4: meme wall | +20 lines; +1 -0 ~0 fns | - |
| [#5](https://github.com/hagopjay/x3d.demo/pull/5) | 11-07 | Demo doc v5: Neural Canvas (brain and torso CT) as demo 3 | +2,819 lines; +319 -0 ~0 fns | code names 12 more |
| [#6](https://github.com/hagopjay/x3d.demo/pull/6) | 11-07 | Demo doc v6: Manifold of emotion (demo 4) and a STEM shelf | +20 lines; +1 -0 ~0 fns | - |
| [#7](https://github.com/hagopjay/x3d.demo/pull/7) | 11-07 | Demo doc v7: STEM studies live, hosted manifold, X_ITE twins | +7,749 lines; +735 -0 ~0 fns | +6 X3D files (+2.1 MB); scenes start using 25 node types; code names 1 more |
| [#8](https://github.com/hagopjay/x3d.demo/pull/8) | 11-07 | Doc v8: KANSEI as the Babylon flagship, plus the X_ITE twin fix | +0 lines; +0 -0 ~0 fns | - |
| [#9](https://github.com/hagopjay/x3d.demo/pull/9) | 11-07 | Docs v8 and v9: KANSEI (demo 6), Loomsong (demo 7) and a GitHub shelf | +20 lines; +1 -0 ~0 fns | - |
| [#10](https://github.com/hagopjay/x3d.demo/pull/10) | 11-07 | Docs v9 and v10: Loomsong playable, Tether Firehose 4, GitHub shelf | +8,474 lines; +1336 -0 ~0 fns | +3 X3D files (+6.7 MB); scenes start using 8 node types; code names 53 more |
| [#11](https://github.com/hagopjay/x3d.demo/pull/11) | 11-07 | Neural Canvas (Babylon WebGPU) v2 as a new folder, v1 untouched | +2,984 lines; +350 -0 ~0 fns | - |
| [#12](https://github.com/hagopjay/x3d.demo/pull/12) | 11-07 | Docs v11 and v12: WebGPU manifold, Chirp and Electron Cloud (Demos 9 to 11) | +5,336 lines; +598 -0 ~0 fns | +1 X3D files (+2.0 MB); code names 6 more |
| [#13](https://github.com/hagopjay/x3d.demo/pull/13) | 11-08 | X3D demos: Blender X3D I/O showcase (12), MuJoCo bridge, Ontology constellation, Dynasty Loom, Confluence IFC, Gobbler | +8,466 lines; +695 -0 ~0 fns | +56 X3D files (+28.3 MB); scenes start using 35 node types; code names 2 more |
| [#14](https://github.com/hagopjay/x3d.demo/pull/14) | 11-08 | Docs v14, v15: Gobbler 3 on WebGPU (Demo 18), artifact card kept, STEM Pages link | +3,150 lines; +275 -0 ~0 fns | +1 X3D files (+0.2 MB); code names 4 more |
| [#15](https://github.com/hagopjay/x3d.demo/pull/15) | 11-08 | Doc v16: Demo 19, Material Odyssey on Babylon WebGPU | +3,374 lines; +316 -0 ~0 fns | +1 X3D files (+0.9 MB) |
| [#16](https://github.com/hagopjay/x3d.demo/pull/16) | 11-08 | Docs v17, v18: Gobbler Demiurge, Dynasty Loom, Library Hall on Babylon WebGPU (Demos 20 to 22) | +3,112 lines; +517 -0 ~0 fns | +21 X3D files (+27.7 MB); scenes start using 7 node types |
| `9db2b1d` | 11-08 | Revise introductory paragraph in index.html | +0 lines; +0 -0 ~0 fns | - |
| [#17](https://github.com/hagopjay/x3d.demo/pull/17) | 11-09 | Doc v19: Demo 23, Gobbler Gyroscope on Babylon WebGPU | +6,413 lines; +509 -0 ~0 fns | +1 X3D files (+1.9 MB) |
| [#18](https://github.com/hagopjay/x3d.demo/pull/18) | 11-13 | LUMEN Interference on X_ITE v1 (demo candidate, not yet linked from the index) | +167 lines; +24 -0 ~0 fns | +1 X3D files (+0.7 MB); scenes start using 1 node types |
| [#19](https://github.com/hagopjay/x3d.demo/pull/19) | 11-13 | Add Ten Minute Physics in X3D, batches 1 and 2 | +247 lines; +18 -0 ~0 fns | +3 X3D files (+0.6 MB) |
| [#20](https://github.com/hagopjay/x3d.demo/pull/20) | 11-13 | Add Ten Minute Physics in X3D, batch 2 (jelly, cloth, height-field water) | +285 lines; +19 -0 ~0 fns | +3 X3D files (+11.6 MB) |
| [#21](https://github.com/hagopjay/x3d.demo/pull/21) | 11-13 | Add Giza Osiris Shaft and Hall of Records X3D study (demo v1) | +286 lines; +18 -0 ~0 fns | +1 X3D files (+0.1 MB); scenes start using 1 node types |
| [#22](https://github.com/hagopjay/x3d.demo/pull/22) | 11-13 | Ten Minute Physics in X3D, batch 3: physics witness, MuJoCo cross-check, fixed billiards | +590 lines; +60 -0 ~0 fns | +2 X3D files (+0.5 MB) |
| [#23](https://github.com/hagopjay/x3d.demo/pull/23) | 11-13 | Ten Minute Physics in X3D, batch 4: spatial hashing, smoke tunnel, joints vs MuJoCo | +343 lines; +45 -0 ~0 fns | +3 X3D files (+6.1 MB); scenes start using 1 node types |
| [#24](https://github.com/hagopjay/x3d.demo/pull/24) | 11-13 | Ten Minute Physics in X3D, batch 5: FLIP water, rigid bodies, cloth self collision (+ review errata, field guide) | +521 lines; +71 -0 ~0 fns | +3 X3D files (+7.1 MB) |
| [#25](https://github.com/hagopjay/x3d.demo/pull/25) | 11-13 | Ten Minute Physics in X3D, batch 6: integrators, sweep and prune, Morton and BVH | +421 lines; +59 -0 ~0 fns | +3 X3D files (+1.0 MB) |

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
3. **The repo is heavy:** 120.9 MB of X3D plus 104 MB of HTML (inlined data). Pages serves it, but clones and CI will slow
   down. Consider Git LFS or release assets for scenes over 5 MB.
4. **A smoke test per page** would catch the "no adapter" and texture-fallback class of bug (PRs #2, Loom #20) before
   deploy; the x3d.poc Pages smoke recipe (full Chromium, not headless-shell) is reusable.

## 6. Method and limits

As in the x3d.loom masterclass (same tools, same cache). Inline scripts are analysed at their HTML line numbers. Roles are
assigned from folder names (`*-webgpu` and `brain-torso` → WebGPU; collider events and heritage facade → HEP; Ten Minute
Physics and the MuJoCo bridge → physics; `stem`; everything else under `docs/demos` → X_ITE demos; the rest → doc shelf).
Scenes validate with x3d_mcp (XSD valid, 0 errors, 0 warnings) and render in X_ITE 16.7.0 in the Claude browser pane.
