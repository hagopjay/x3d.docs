# x3d.loom: an AST masterclass and teardown

[hagopjay/x3d.loom](https://github.com/hagopjay/x3d.loom), `origin/main` 162ab18, measured 2026-11-13. The repo was created on
2026-11-05 ("The X3D Loom v1.0, public snapshot"), so there is no fork era: its whole history is the era. In 8 days the
first-parent line of `main` took 45 steps; 44 of the 45 PRs merged into `main` (#36 went to `bridge-review` and #42 to a
working branch). The hagsmac copy has its own 4 PRs (2 merged into hagsmac/main, 1 closed, 1 open: the Babylon visual-lane WIP).

**Labels.** *Measured*: Python `ast`, the TypeScript compiler's parser (JS, MJS, TS, TSX and inline `<script>` in HTML),
an XML element walk of every `.x3d` file, `git` and `gh`. *Inferred*: call resolution (static, by name and import binding),
X3D node names found as string literals in code, and the roles, which are assigned by top-level directory. *Claimed*: the
bridge's own tracker `x3d.webgpu/bridge/NODES.json` and PR text. Nothing was executed and nothing was installed (the
TypeScript parser is the copy already installed for x3d-physx-bridge).

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | 383 files laid out by a force model, 3419 functions of 3+ lines around them, 1012 cross-file and 2610 in-file calls |
| `scenes/coverage-sunburst.x3d` | the 267 X3D 4.1 nodes: used in the repo's 219 X3D files (orange) and the bridge tracker's status per node |
| `scenes/fork-timeline.x3d` | 45 steps of `main`: code lines per role, X3D megabytes, new node types in scenes and code, CI |
| `scenes/code-city.x3d` | functions as buildings per directory; aqua = body in one file, amber = same body in 2+ files |

## 1. What the AST says the Loom is

The Loom is not one program. It is **eight sub-projects that do not call each other**: in the call graph each role is an
island: all 1,174 statically resolved cross-file calls stay inside their own sub-project (physics 484, drift 459,
kit 139, platformer 91, mol 1). Static resolution finds no calls between `x3d.webgpu` files: whatever wires them
(globals, dynamic registration, page-level script order) is outside what this method follows. They share a *method* (laws, failure modes,
loomkit gates, receipts, documented in the root Markdown files) rather than a library.

| role (hand-assigned from directory names) | code files | code lines | functions | X3D files | X3D MB |
|---|---|---|---|---|---|
| x3d.webgpu (Babylon/WebGPU bridge, reader, ports) | 201 | 36,301 | 3,132 | 120 | 3.0 |
| x3d.physics (PhysX + MuJoCo bridges, TMP ports) | 209 | 18,684 | 1,468 | 33 | 1.2 |
| x3d.drift (KANSEI racing game) | 37 | 12,261 | 724 | 14 | 10.5 |
| kit (loomkit gates, examples) + docs | 61 | 11,405 | 548 | 0 | 0.0 |
| x3d.brain (imaging demo) | 14 | 8,063 | 628 | 2 | 5.2 |
| x3d.mol (proteins, AlphaFold keyframes) | 25 | 4,986 | 361 | 0 | 0.0 |
| x3d.platformer (NIB) | 19 | 3,382 | 235 | 4 | 0.4 |
| runs (recorded evidence) | 46 | 1,620 | 199 | 46 | 21.4 |

* **Code:** 96,702 lines in 612 files (py 133, js 454, html 25). 6,916 named function definitions, 241 with cyclomatic complexity
  over 20 and 34 over 50.
* **Scenes:** 219 X3D files, 41.7 MB: X3D 4.0 202, X3D 4.1 17; profiles Immersive 152, Interchange 62, Interactive 4, Full 1. 1,694 ROUTEs, but only 2 files with a `Script` node and 1
  file with a `ProtoInstance`: behaviour lives in the JavaScript around the scenes, not inside them.
* **Duplication:** of 3,814 functions of 3+ lines, 1168 have a body that also exists in another file. 25 files are exact
  copies of another (same multiset of function bodies). The biggest family is the WebGPU viewer: `viewer.tpl.html`,
  `-v2`, `-v2-1`, `-v3`, `-v3-1`, `collider.html`, `collider-v2.html` and `first-light*.html` each carry their own `frame`
  function (CC 127 to 154). Versioning by copying a page is the Loom's habit; it keeps old demos frozen, at the price of
  fixes that must be applied N times (PR #20's SAI texture-fallback fix is the kind of change this multiplies).

### Hot spots (measured; one row per distinct body)

| function | CC | lines | nesting |
|---|---|---|---|
| `x3d.drift/engine/car.js::stepCar` | 185 | 331 | 5 |
| `x3d.webgpu/demo/src/viewer-v3-1.tpl.html::frame` (same body in 2 files) | 154 | 266 | 5 |
| `x3d.webgpu/demo/collider-v2.html::frame` (same body in 3 files) | 144 | 239 | 5 |
| `x3d.drift/engine/ai.js::driftDrive` | 132 | 186 | 4 |
| `x3d.webgpu/demo/collider.html::frame` (same body in 3 files) | 127 | 221 | 5 |
| `x3d.mol/src/witness.py::check` | 106 | 163 | 6 |
| `kit/loomkit/hepevent.py::load_spec` | 83 | 92 | 3 |
| `x3d.webgpu/demo/first-light.html::frame` | 83 | 163 | 5 |
| `kit/examples/zinc_site_scene.py::build` | 79 | 113 | 5 |
| `x3d.drift/build/kcars.py::build_car` | 77 | 360 | 4 |
| `x3d.brain/tools/build_brain_scene.py::main` | 72 | 277 | 5 |
| `x3d.drift/engine/ai.js::driveAI` | 72 | 123 | 5 |

`x3d.drift/engine/car.js::stepCar` (CC 185) and `ai.js::driftDrive` (CC 132) are the most complex functions in either repo:
a vehicle model and a driving AI in single functions. They are the first candidates for splitting, with the drift game's
own tests as the net.

## 2. Taxonomy: X3D through three lenses

Node types used, by number of files: Appearance (166), Shape (165), Viewpoint (162), Material (138), Transform (137), NavigationInfo (123), WorldInfo (101), Background (96), Coordinate (94), DirectionalLight (79), Box (77), Group (76), IndexedFaceSet (69), Sphere (61), Cylinder (53). Components touched: Sound 21, Rendering 14, Followers 14, RigidBodyPhysics 13, Interpolation 11, Shape 9, Texturing 9, Core 8, Shaders 8, ParticleSystems 8, Geometry3D 7, Texturing3D 7, Geometry2D 6, CADGeometry 6, Navigation 5, EnvironmentalEffects 5, Layout 5, Grouping 4, Lighting 4, PointingDeviceSensor 4, EventUtilities 4, CubeMapTexturing 3, Networking 3, Layering 3, Text 2, KeyDeviceSensor 2, EnvironmentalSensor 2, Time 1, Scripting 1, GaussianSplats 1.

**The bridge tracker against the AST.** `x3d.webgpu/bridge/NODES.json` tracks 260 X3D 4.0 nodes for the Babylon/WebGPU
reader. Its statuses: base 75, bridged 41, claimed 8, gap 70, todo 65, blocked 1. Cross-checked against the code:

| tracker status | nodes | named as a literal in code | used in a scene in the repo |
|---|---|---|---|
| base | 75 | 75 | 63 |
| bridged | 41 | 41 | 41 |
| claimed | 8 | 8 | 1 |
| gap | 70 | 70 | 70 |
| todo | 65 | 17 | 12 |
| blocked | 1 | 1 | 1 |

Every node the tracker calls base, bridged, claimed, gap or blocked is named in the code, so the tracker and the code agree
(measured). Only 17 of the 65 "todo" nodes appear in code. The 70 "gap" nodes all have a test scene: a gap is a node that is
read and tested but not yet drawn the way X_ITE draws it, which is what the Babylon "visual lane" PRs (#43 to #45) burn
down with picture comparisons against X_ITE. In the sunburst, the outer ring is this tracker and the white dots mark code
naming.

## 3. The history, step by step

| step | date | title | code delta | X3D delta |
|---|---|---|---|---|
| `849fc7e` | 11-05 | The X3D Loom v1.0, public snapshot 2: the Mashtots2 fold-in | +159 lines; +9 -0 ~6 fns | - |
| `58b0d40` | 11-05 | The X3D Loom v1.0, public snapshot 3: Mashtots slide show guard applied | +0 lines; +0 -0 ~0 fns | - |
| [#1](https://github.com/hagopjay/x3d.loom/pull/1) | 11-06 | Zinc fingers under the Loom: metal-site witness, controls and study plan | +472 lines; +23 -0 ~1 fns | - |
| [#3](https://github.com/hagopjay/x3d.loom/pull/3) | 11-06 | x3d.platformer (NIB): a physics platformer made of X3D, and a play witness for the Loom | +3,654 lines; +238 -0 ~5 fns | +4 X3D files (+0.4 MB); scenes start using 30 node types; code names 32 more |
| [#4](https://github.com/hagopjay/x3d.loom/pull/4) | 11-06 | The Loom Collider: a collider-event demo in X3D, a plausibility witness and first light | +6,680 lines; +343 -0 ~3 fns | +18 X3D files (+20.7 MB); scenes start using 14 node types; code names 36 more |
| [#5](https://github.com/hagopjay/x3d.loom/pull/5) | 11-06 | x3d.brain: high-fidelity brain imaging demo under the Loom | +8,063 lines; +603 -0 ~0 fns | +2 X3D files (+5.1 MB); scenes start using 11 node types; code names 6 more |
| [#6](https://github.com/hagopjay/x3d.loom/pull/6) | 11-06 | x3d.drift (KANSEI): a drift-racing game made of X3D, and the x3d-drift Loom profile | +12,261 lines; +705 -0 ~0 fns | +14 X3D files (+10.6 MB); scenes start using 5 node types; code names 7 more |
| [#2](https://github.com/hagopjay/x3d.loom/pull/2) | 11-06 | Zinc fingers P1: fourteen deposited structures, a site census and fourteen site scenes | +2,333 lines; +84 -0 ~10 fns | +28 X3D files (+0.7 MB) |
| [#7](https://github.com/hagopjay/x3d.loom/pull/7) | 11-06 | x3d.webgpu: a specification scaffold for X3D on WebGPU (docs plus a probe page) | +56 lines; +2 -0 ~0 fns | - |
| [#8](https://github.com/hagopjay/x3d.loom/pull/8) | 11-07 | x3d.webgpu: First Light and the Collider, X3D scenes run and drawn with WebGPU | +8,662 lines; +647 -0 ~0 fns | +2 X3D files (+2.1 MB); scenes start using 7 node types; code names 4 more |
| [#9](https://github.com/hagopjay/x3d.loom/pull/9) | 11-07 | Loom: fold back two rebuilds by another model (laws 38-40, five rules) | +132 lines; +6 -0 ~2 fns | - |
| [#10](https://github.com/hagopjay/x3d.loom/pull/10) | 11-07 | x3d.webgpu: Collider v2, an outside rebuild reviewed and folded in | +5,212 lines; +374 -0 ~0 fns | - |
| [#11](https://github.com/hagopjay/x3d.loom/pull/11) | 11-07 | x3d.webgpu: GaussianSplats on the WebGPU bridge (Pantheon port) | +2,864 lines; +195 -0 ~0 fns | +1 X3D files (+0.7 MB); scenes start using 1 node types |
| [#12](https://github.com/hagopjay/x3d.loom/pull/12) | 11-07 | x3d.webgpu: five HEP event pages and a splat facade (quick wins) | +141 lines; +6 -0 ~0 fns | - |
| [#13](https://github.com/hagopjay/x3d.loom/pull/13) | 11-07 | x3d.webgpu: Neural Canvas (Brain Loom) on Babylon WebGPU through our X3D reader | +1,720 lines; +189 -0 ~0 fns | - |
| [#14](https://github.com/hagopjay/x3d.loom/pull/14) | 11-07 | x3d.webgpu: viewer adapter fallback (v2-1, v3-1 templates) | +5,317 lines; +377 -0 ~0 fns | - |
| [#15](https://github.com/hagopjay/x3d.loom/pull/15) | 11-07 | x3d.webgpu: Babylon/WebGPU bridge playbook v1 | +0 lines; +0 -0 ~0 fns | - |
| [#16](https://github.com/hagopjay/x3d.loom/pull/16) | 11-07 | x3d.webgpu: Manifold of Emotion WebGPU port, plan and scaffold | +235 lines; +15 -0 ~0 fns | code names 1 more |
| [#17](https://github.com/hagopjay/x3d.loom/pull/17) | 11-07 | x3d.webgpu: KANSEI drift on Babylon WebGPU (port 3), with an opt-in Timing button | +825 lines; +101 -0 ~7 fns | - |
| [#18](https://github.com/hagopjay/x3d.loom/pull/18) | 11-07 | Neural Canvas v2: brain parity re-run after the normals fix, shared adapter retry and Timing button | +87 lines; +35 -22 ~4 fns | - |
| [#19](https://github.com/hagopjay/x3d.loom/pull/19) | 11-07 | x3d.webgpu: Manifold of Emotion on Babylon WebGPU (port 4), opt-in Timing button | +868 lines; +76 -4 ~11 fns | - |
| [#20](https://github.com/hagopjay/x3d.loom/pull/20) | 11-07 | SAI shim: probe texture fallback urls once (KANSEI made about 2,350 failed requests on Pages) | +19 lines; +3 -0 ~1 fns | - |
| [#22](https://github.com/hagopjay/x3d.loom/pull/22) | 11-07 | Gobbler 3 knowledge-graph page on Babylon 9.32.0 WebGPU (port 2) | +1,434 lines; +71 -0 ~0 fns | code names 5 more |
| [#21](https://github.com/hagopjay/x3d.loom/pull/21) | 11-07 | x3d.webgpu: Chirp and Electron Cloud on Babylon WebGPU (ports 4 and 5), switchable cinematic looks, parity gaps logged | +636 lines; +64 -0 ~11 fns | code names 1 more |
| [#23](https://github.com/hagopjay/x3d.loom/pull/23) | 11-08 | Material Odyssey on Babylon (port #6) and bridge playbook v2 | +530 lines; +51 -0 ~0 fns | - |
| [#24](https://github.com/hagopjay/x3d.loom/pull/24) | 11-08 | Gobbler demiurge on Babylon (port #7) | +677 lines; +45 -0 ~0 fns | code names 5 more |
| [#25](https://github.com/hagopjay/x3d.loom/pull/25) | 11-08 | x3d.webgpu: Dynasty Loom hypersphere on Babylon (port #8) | +866 lines; +43 -0 ~0 fns | - |
| [#26](https://github.com/hagopjay/x3d.loom/pull/26) | 11-08 | x3d.webgpu/bridge: node tracker, driver and kit; batches 1 to 12 (60 nodes), reader 135 of 260 | +2,532 lines; +293 -0 ~0 fns | +57 X3D files (+0.0 MB); scenes start using 54 node types; code names 50 more |
| [#27](https://github.com/hagopjay/x3d.loom/pull/27) | 11-08 | Library hall on Babylon WebGPU (port #9, +8 node types) | +751 lines; +75 -0 ~0 fns | code names 4 more |
| [#28](https://github.com/hagopjay/x3d.loom/pull/28) | 11-08 | x3d.webgpu/bridge: batches 12 and 13 (10 nodes), reader 140 of 260 | +736 lines; +68 -0 ~4 fns | +11 X3D files (+0.1 MB); scenes start using 11 node types; code names 9 more |
| [#29](https://github.com/hagopjay/x3d.loom/pull/29) | 11-08 | x3d.webgpu/bridge: batch 14, Sound graph (5 nodes), reader 145 of 260 | +274 lines; +24 -2 ~4 fns | +5 X3D files (+0.0 MB); scenes start using 5 node types; code names 5 more |
| [#30](https://github.com/hagopjay/x3d.loom/pull/30) | 11-08 | x3d.webgpu/bridge: batch 15, Sound graph (5 nodes), reader 150 of 260 | +189 lines; +10 -0 ~3 fns | +5 X3D files (+0.0 MB); scenes start using 5 node types; code names 5 more |
| [#31](https://github.com/hagopjay/x3d.loom/pull/31) | 11-08 | x3d.webgpu/bridge: batch 16, Sound sources and spatial (5 nodes), reader 155 of 260 | +249 lines; +30 -0 ~1 fns | +5 X3D files (+0.0 MB); scenes start using 5 node types; code names 5 more |
| [#32](https://github.com/hagopjay/x3d.loom/pull/32) | 11-08 | Bridge batches 17 to 19: sound streams, Layering, Layout, shader holders (170/260) | +524 lines; +48 -0 ~2 fns | +15 X3D files (+0.0 MB); scenes start using 15 node types; code names 14 more |
| [#33](https://github.com/hagopjay/x3d.loom/pull/33) | 11-08 | Bridge batch 20: ShaderProgram, cube maps, 3D textures (175/260) | +266 lines; +31 -0 ~6 fns | +5 X3D files (+0.0 MB); scenes start using 6 node types; code names 5 more |
| [#34](https://github.com/hagopjay/x3d.loom/pull/34) | 11-08 | Bridge: shot op and three demo scenes | +2 lines; +1 -0 ~1 fns | +3 X3D files (+0.0 MB) |
| [#35](https://github.com/hagopjay/x3d.loom/pull/35) | 11-09 | Bridge: validation that can fail, fidelity preflight, scene lifecycle, first CI | +574 lines; +45 -7 ~28 fns | - |
| [#37](https://github.com/hagopjay/x3d.loom/pull/37) | 11-12 | x3d.mol: proteins as validated X3D, a Babylon.js viewer and a Blender stage | +3,599 lines; +262 -0 ~0 fns | - |
| [#38](https://github.com/hagopjay/x3d.loom/pull/38) | 11-13 | Physics under the Loom: the physics witness, two profiles, laws 41-43, failure modes 124-147, and x3d.physics | +18,155 lines; +1147 -0 ~2 fns | +33 X3D files (+1.2 MB); scenes start using 9 node types; code names 8 more |
| [#39](https://github.com/hagopjay/x3d.loom/pull/39) | 11-13 | x3d.mol: AlphaFold 3 diffusion illustration as validated X3D keyframes, with a live player | +1,387 lines; +91 -0 ~12 fns | - |
| [#40](https://github.com/hagopjay/x3d.loom/pull/40) | 11-13 | docs: what Marble splats teach (frame wrapper, header drift, clip and renormalise) | +0 lines; +0 -0 ~0 fns | - |
| [#41](https://github.com/hagopjay/x3d.loom/pull/41) | 11-13 | Fold back the Ten Minute Physics ports: law 44, failure modes 148-160, playbook patterns 11-19 | +842 lines; +123 -0 ~0 fns | - |
| [#43](https://github.com/hagopjay/x3d.loom/pull/43) | 11-13 | Babylon bridge, visual lane: gap burn-down with X_ITE picture compare (batches 21 on) | +1,042 lines; +108 -0 ~15 fns | code names 8 more |
| [#44](https://github.com/hagopjay/x3d.loom/pull/44) | 11-13 | Babylon bridge, visual lane part 2: batches 22 to 23 and on (Texturing3D, particles, CAD) | +1 lines; +1 -0 ~4 fns | +9 X3D files (+0.1 MB); scenes start using 12 node types |
| [#45](https://github.com/hagopjay/x3d.loom/pull/45) | 11-13 | Babylon bridge, visual lane part 3: batches 24 to 26 (Texturing, 2D geometry, CAD) | +0 lines; +0 -0 ~0 fns | +2 X3D files (+0.0 MB) |

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
commit). Vendored files are excluded by path (5 files: X_ITE, Babylon, minified bundles). Anonymous callbacks are
charged to their enclosing function. Six `.tpl.html` templates contain placeholders and parse with recoverable errors.
Clone detection hashes each function's whitespace-normalised source text. Scenes validate with x3d_mcp (XSD 4.0 valid,
0 errors, 0 warnings) and were rendered in the Claude browser pane (X_ITE 16.7.0, software WebGL); the call graph and the
city take 30 to 50 s to load there.
