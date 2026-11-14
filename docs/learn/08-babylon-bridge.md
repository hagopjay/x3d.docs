# 08. The Babylon bridge

> **Say it:** one X3D file is the master, our own reader runs its events, and Babylon on WebGPU only paints the result; every picture is a claim against X_ITE on a named rig, every fallback says so on screen, and nothing about speed has been measured. **[C]**

| field | value |
|---|---|
| chapter code | `BAB` |
| prerequisites | [01 The tether](01-the-tether.md) for the loop; [06 X_ITE, the reference renderer](06-xite-the-oracle.md) for the reference arm and its patch rules; [02 Loom laws](02-loom-laws.md) for laws 38 to 40 |
| after this you can | (1) recount the bridge's node coverage and name the denominator; (2) read the 50-trap playbook by tier; (3) measure and read a PSNR against X_ITE without over-reading it; (4) port a shader by hash and prove a miss falls back; (5) follow the append-only procedure for a new demo |
| sources read | x3d.loom@162ab18:x3d.webgpu/{STATE,PATHS,BABYLON,BENCHMARK,SPEC}.md, the four BABYLON-BRIDGE-PLAYBOOK files, bridge/, demo/src/, runs/webgpu-*/; x3d.demo@d10b457:{CHANGELOG.md,docs/index.html}; x3d.docs@f172f67:docs/vendor/x_ite/x_ite.min.js |
| instruments used | `x3d.loom@162ab18`, `X_ITE 16.7.0` (grep only), `X_ITE 16.4.3` to `16.6.0` per receipt row, `Babylon 9.32.0`, `Chromium 153.0.8010.12 (Chrome for Testing), SwiftShader`, Node 22.23.4, Python 3 (numpy 2.5.3, Pillow 12.3.0, lxml), `xmllint`, `x3d_mcp fork b4efcd3` and `X3DUOM 4.0` through the bridge driver; software GL only |

Rig for every **[C]** below that this chapter re-ran (2026-11-14): read-only checkouts, scratch copies for anything that writes, Node 22.23.4, Python with `-I`, no network, no GPU. A number read from a recorded run is named by receipt path and graded **[L]** unless a drill re-derived it.

## 1. The map

```text
  scene.x3d   the master: validated first (chapters 01, 03), never edited to please a renderer
      |
      +------------------------+---------------------------------+
      v                        v                                 v
  X3D validator          X_ITE 16.x (WebGL2)            OUR READER = the brain
  XSD + semantic rules   reference body                 reader.js  parse, DEF/USE, ROUTE
  (chapter 03)           draws pixels A                 kit.js + nodes/*.js  event nodes
                              |                         sai.js  X3D.getBrowser() shim
                              |                                |  node tree + events
                              |                                v
                              |                   BABYLON 9.32.0 = the body (WebGPU)
                              |                   body.js  body-cam.js  body-br.js
                              |                   wgsl.js  FNV-1a(GLSL) -> hand WGSL
                              |                                |
                              |                                v
                              +-------> compare <----------- pixels B
                                           |
                                           v
                                 RECEIPT.md (rig, versions) + GAPS.md (each gap graded)
```

Sections: 2 why a second renderer; 3 architecture; 4 node coverage recounted; 5 the 50-trap playbook; 6 the parity method; 7 the ports; 8 laws 39 and 40 in code; 9 shader porting; 10 the adapter trap; 11 a 16-step port procedure; 12 why there is no speed claim.

**In scope:** the bridge as built in `x3d.loom@162ab18:x3d.webgpu/`, its tracker and playbook, and how to measure it. **Out of scope:** X_ITE internals ([06](06-xite-the-oracle.md), [the X_ITE masterclass](../x_ite/MASTERCLASS.md)); the Loom's AST teardown ([the loom masterclass](../x3d.loom/MASTERCLASS.md)); Castle on its own renderer ([09](09-castle-engine.md)); glTF export as a route ([11](11-gltf-usd-khronos.md)); physics ([13](13-physics.md)). **No speed claim appears here.** No receipt in the repository holds a timing from a real GPU for any Babylon or WebGPU body (section 12).

**Read next:** deeper, [06 X_ITE, the reference renderer](06-xite-the-oracle.md) for the arm every number here is measured against; wider, [07 x3d.xray](07-xray.md) for a second consumer of the same "scene as the master, viewer as a witness" idea.

## 2. Why: a second renderer, and why the file stays the master

| fact | value | grade | instrument | source |
|---|---|---|---|---|
| X_ITE draws through WebGL2 only | 0 hits for "webgpu", 0 for "navigator.gpu", 1 `getContext("webgl2"` in `x_ite.min.js` 16.7.0 (sha256 prefix b7df063e8cb1) | C | grep over the vendored bundle, `X_ITE 16.7.0` | x3d.docs@f172f67:docs/vendor/x_ite/x_ite.min.js (re-run: `grep -o -i webgpu` on the file, counted) |
| X3D cannot name a WebGPU shader | 4.1 draft lists Cg, GLSL, HLSL; VERTEX and FRAGMENT parts only; `WGSL` and `COMPUTE` need a standards proposal (gate G5) | L | read in README.md and SPEC.md | x3d.loom@162ab18:x3d.webgpu/README.md |
| scored options A to G | F (hybrid: X_ITE stays truth, showpieces on a runtime plus WebGPU body) 30 of 35; all others 19 to 25 | L | the scorecard is a judgement; every effort figure is [S] | x3d.loom@162ab18:x3d.webgpu/PATHS.md |
| why not export to glTF and use any engine | glTF drops ROUTEs, Script and shader nodes; the validator checks the source while the viewer would see a derived file (only option B fails the tether test outright) | L | PATHS.md section 2, BABYLON.md section 2.2 | x3d.loom@162ab18:x3d.webgpu/PATHS.md |

The design that follows is F on a Babylon body (path G): X_ITE stays the oracle and the validator's target, and the bridge renders showpieces, each gated by a measured comparison against X_ITE. This is [Loom law 38](02-loom-laws.md), one master, many renderers: a renderer that disagrees is a finding about the reader or the body, never a reason to edit the scene.

Babylon is the default body because, among the engines surveyed, it alone has a path from GLSL to WGSL [L]. The bridge never used that path: `grep -rli 'glslang\|twgsl'` over `demo/src`, `bridge/src` and `runs/webgpu-*` returns 0 files [C, 2026-11-14]; it hand-ports shaders (section 9). Gate G2 (do the Collider's GLSL programs compile through glslang plus twgsl and match X_ITE?) is listed in `x3d.webgpu/README.md` and has no receipt: `bench/receipts/` holds one file, the G1 adapter probe [C, `ls`].

## 3. Architecture: the reader is the brain, Babylon is the body

The reader holds time, ROUTEs, sensors and the SAI; Babylon objects are disposable views of the node tree; a page written for X_ITE keeps calling `X3D.getBrowser()` and a shim answers.

```text
  page app.js (unchanged)           one frame
        |  X3D.getBrowser()...
        v
  +----------+  fields   +--------------------------+  changed(node, field)  +-------------+
  | sai.js   | --------> | reader.js  node tree     | ---------------------> | body.js     |
  | shim     | <-------- | emit / drain events      | <--------------------- | Babylon     |
  +----------+ callbacks | DEF/USE = shared objects |  picks, camera, time   | meshes,     |
                         | ROUTEs, TimeSensor       |                        | materials,  |
  kit.js: BR.node(name, spec), one file per node     |                        | lights,     |
  (field table from X3DUOM; receive/tick/build)      |                        | cameras     |
                         +--------------------------+                        +-------------+
                  ComposedShader GLSL -> whitespace collapse -> FNV-1a -> wgsl.js table
                  hit: hand-ported WGSL.  miss: Material fallback + notice on screen
```

Files, with `wc -c` sizes [C] (`x3d.loom@162ab18:x3d.webgpu/`): `demo/src/brain/reader.js` 30,896 B (parse, typed fields, DEF/USE, ROUTE cascade, TimeSensor, interpolators); `body.js` 33,752 (node tree to Babylon: groups, shapes, lights, PBR, lines, text, clip planes); `body-cam.js` 13,540 (viewpoints, orbit, picking, frame loop); `sai.js` 21,911 (`getNamedNode`, `createNode`, `addRoute`, `replaceWorld`, callbacks); `wgsl.js` 12,111 (hash-keyed ports); `shared/adapter.js` 1,097 and `shared/timing.js` 11,928 (section 10, section 12); `bridge/src/kit.js` 31,928 (`BR.node(name, spec)`: field table, `receive`, `tick`, `init`, `build`, `geometry`, `changed`); `bridge/src/body-br.js` 55,254 (the Babylon side of the kit; nodes without a `build` stay silent); `bridge/src/fidelity.js` 6,439 (preflight report); `bridge/src/nodes/*.js` 115 files, one per node.

A kit node is small: `BooleanToggle` is one `BR.node` call with a field table and one `receive`; its test spec is `set`, `event`, `expect` steps run in our reader and in X_ITE through the SAI both speak. On a scratch copy, `node --test tools/*.test.js` passed 33 of 33 and `python3 tools/driver.py check BooleanToggle --no-xite` printed `PASS BooleanToggle xsd:ok ours:pass 9/9 xite:skipped` [C, 2026-11-14]; `--no-xite` is exploratory and cannot close a batch.

What exists is not what the spec describes: `SPEC.md` and `BABYLON.md` describe a TypeScript runtime generated from X3DUOM 4.1 and registered as a Babylon `SceneLoader` plugin, with a Script sandbox and a load receipt; what runs is plain JavaScript (the demo README says "working demos, not the runtime the spec describes"). The spec's M1 parity rule (mean absolute difference at most 4/255, luma within 0.01 against X_ITE 16.7.0) has been applied to no port [C: every receipt uses PSNR, MAD or silhouette overlap].

## 4. Node coverage, recounted at x3d.loom@162ab18

The primer v2 of 8 November said **68 of 260** X3D 4.0 node types. The tracker at `162ab18` says **186 of 260**: `python3 tools/driver.py status` prints `reader knows 186/260 | base 75 blocked 1 bridged 41 claimed 8 gap 70 todo 65`. Both are right about different things, and the difference is the lesson.

Census commands: D-BAB-1 (`node tools/census.js ../demo/src`, today) and D-BAB-2 (the same on `git archive 60824ce`); all re-run 2026-11-14.

| denominator | count | share of 260 | what it measures | grade | instrument |
|---|---|---|---|---|---|
| concrete nodes in the tracker | 260 | 100% | `X3dUnifiedObjectModel-4.0.xml`; includes `ProtoInstance` syntax | C | `X3DUOM 4.0` via `NODES.json` meta |
| page-bundle census, 8 Nov (60824ce) | 68 (72 defs) | 26.2% | types with a field table in at least one Babylon page | C | `census.js`, re-run on `git archive 60824ce` |
| same census, today | 75 (79 defs) | 28.8% | adds Inline, LOD, ProximitySensor, four HAnim names from the Demiurge and Dynasty parts | C | `census.js`, 162ab18 |
| same census plus the hall extension | 83 (87 defs) | 31.9% | adds the 8 nodes marked `claimed` | C | `census.js` with `hall/reader-ext-hl.js` |
| tracker headline "reader knows" | 186 | 71.5% | `base` 75 + kit modules 111 (41 `bridged`, 70 `gap`) | C | `driver.py status` |
| bridged without a logged gap | 41 | 15.8% | fixture validates against the 4.0 XSD, test passes in our reader and X_ITE | C | `driver.py status` |
| still `todo` | 65 | 25.0% | NURBS 13, VolumeRendering 13, RigidBodyPhysics 13 (+1 blocked), Geospatial 11, DIS 6, Picking 5, HAnim 2, TextureProjection 2 | C | `NODES.json` |

The delta since the primer, like for like [C]:

| step | change | cause |
|---|---|---|
| 68 to 75 on the page-bundle census | +7 | Demiurge (Inline, LOD, ProximitySensor, four HAnim types) and Dynasty added reader parts |
| 75 to 186 on the tracker headline | +111 | kit modules written batch by batch: 41 `bridged`, 70 `gap` |
| 68 to 186, the naive subtraction | +118 | mixes two definitions; the tracker did not exist at 60824ce (first commit `db725e8`, 8 Nov, after the primer's tree) |
| 175 (batch 20, 9 Nov) to 186 (batch 26, 13 Nov) | +11 net | batches 21 to 26 filled 30 tracker slots (17 `bridged`, 13 `gap`), so 19 of them added no name; the batch-21 commit message says five `gap` nodes moved to `bridged` [C, `git show e6c3f9a`] |

Batches 21 to 26 arrived through PRs #43 (batch 21), #44 (22, 23) and #45 (24, 25, 26) on 13 Nov. The headline printed in each `BATCH-NN.md` is a snapshot of a mutable tracker and is not monotonic:

| batch | nodes | bridged / gap | headline after | PSNR range, dB (320 x 240) |
|---|---|---|---|---|
| 21 | five fan, strip and quad sets | 5 / 0 | 175 | 32.71 to 34.91 (5 rows) |
| 22 | StaticGroup, Texturing3D coordinate nodes | 3 / 2 | 179 | 33.85 to 36.63 (6 rows) |
| 23 | CADAssembly, CADFace; three particle emitters and models | 2 / 3 | 184 | 11.73 to 38.03 (11 rows) |
| 24 | FillProperties, TwoSidedMaterial, TextureCoordinateGenerator, two 3D textures | 0 / 5 | 184 | 16.62 to 32.13 (5 rows) |
| 25 | four 2D geometries; LineSet | 4 / 1 | 181 | 26.35 to 35.86 (5 rows) |
| 26 | CADLayer, CADPart, Polyline2D; CoordinateDouble, Polypoint2D | 3 / 2 | 186 | 28.35 to 40.03 (10 rows) |

The dip at batch 25 (184 to 181) is consistent with `driver.py reopen`, which returns worked-on nodes to `wip` before they are re-checked [L, docstring read; the batch-25 reopen list was not traced]. All 42 visual rows together: PSNR 11.73 to 40.03, median 35.92 [C, parsed from `BATCH-21..26.md`]. Read those with section 6: a node can PASS with 11.73 dB.

What is missing (`NODES.json`) [C]: NURBS 13 and VolumeRendering 13 are all `todo`; RigidBodyPhysics has 13 `todo` and 1 `blocked`; Geospatial 11, DIS 6 and Picking 5 are `todo`; Sound has 19 of 21 nodes at `gap` (the Analyser note says nothing is wired into the analyser yet; not checked for the other 18); Shaders 5 of 8 and Layout 5 of 5 are `gap`.

**Three claims hide behind one count.** "Reader knows" means a field table exists; it does not mean the node passes a fixture or that the picture is right. The repository's own assessment of the tracker at `6b3cb76` says recognising, passing a field test and drawing correctly "are different achievements", that the canonical test bundle registered 180 names at the 175 headline, and that the tracker is "not a rendering conformance percentage" [L, read, not re-run]. `bridged` is the strongest word in the tracker and still means one fixture in two engines at 320 x 240.

A name-level census of the 111 parseable demo scenes (86 base-only, 22 needing a `gap`, `todo` or `claimed` node, 1 with unknown names) is drill D-BAB-5; "base" is the union of six reader parts, not what any one page loads.

## 5. The playbook, merged: 50 traps, ranked

The playbook is four files in `x3d.loom@162ab18:x3d.webgpu/`, each a new file that leaves the earlier ones unchanged: `BABYLON-BRIDGE-PLAYBOOK.md` v1 (7 Nov, 11,796 B: laws, ports #1 to #3, adapter pitfall, publishing), `-v2.md` (8 Nov, 9,044 B: a trap table by area from ports #3 to #9 and the Odyssey port), `-v3.md` (7,005 B: Demiurge and Dynasty) and `-v4.md` (1,304 B: the Hall, eight lines) [C, `wc -c`]. Merged and de-duplicated here: **50 traps (T01 to T44 in the table, T45 to T50 beside it); 13 first appear in v1, 19 in v2, 13 in v3, 5 in v4** [C, counted from the table below by script].

Ranking rubric (ours, **[S]**: no incidence data exists): tier **A** is silent on the default path or hit by two or more ports (the picture is plausible, wrong and unlogged); **B** is silent but scene-specific; **C** is loud (an error, a blank page) or tooling; **W** is a WGSL porting rule. Inside a tier: ports hit, then how silent. When a port "looks wrong", read tier A first: the playbook's advice is to find the symptom before touching lighting, because most of the cost was convention, not physics. The "check" column is a grep I ran at `162ab18` over `demo/src/` (a file present means the fix exists in some page, not in every body); "read" means no check was made.

| ID | tier | from; port | symptom and cause | fix | check |
|---|---|---|---|---|---|
| T01 | A | v1, v2; Brain, Odyssey | PBR looks cool and inside-out; X3D counter-clockwise is the front face | `sideOrientation = CounterClockWise`; `null` on MeshBuilder primitives, which the flag turns inside out | grep: 3 files |
| T02 | A | v1, v2; Brain | PhysicalMaterial colours are already linear: converting again made cortex too dark | assign `baseColor` to `albedoColor` as authored; v1 and v2 say "convert authored sRGB" (conflict C1) | `body.js` line 303 |
| T03 | A | v2; Odyssey | scene too bright, 8-light cap hit: 59 of 60 lights have `global=false`, Babylon lights everything | `includedOnlyMeshes` = meshes under the light's parent group, applied after the world builds and on change; a shape sees at most 6 | grep: odyssey-ext.js |
| T04 | A | v2; Odyssey | a USE is a placement: state keyed by node id is overwritten by the second placement (74 lights for 62 placements) | state per Babylon object; the shared body still keys `rec` by id (assessment P1, open at 6b3cb76) | assessment; not re-checked |
| T05 | A | v2; Odyssey | corridor floods pink: Babylon adds an emissive texture to the emissive colour, X3D multiplies | texture in `diffuseTexture`, colour in `emissiveColor` | read |
| T06 | A | v2, bridge README; Manifold | `events.emit` queued ROUTEs but never ran `addFieldCallback`: nothing animates; two wrappers fire callbacks twice | run callbacks from one emit hook (`R.hooks.cb`) | README findings |
| T07 | A | v2; Manifold | first frames washed out: final image processing converts linear to gamma, display-referred shaders already did | `imageProcessing.fromLinearSpace = false` | grep: body-manifold.js |
| T08 | A | v1, v2, v3; Brain, Dynasty | glow sprites draw over glass: `alphaIndex` defaults to MAX_VALUE | explicit `alphaIndex` on every non-glass mesh; blended shapes in document order | grep: 7 files |
| T09 | A | v4; Hall | a textured unlit shape ignores its PNG alpha (glows, shafts, halos drawn opaque) | `hasAlpha`, alpha from diffuse, sorted blend, depth write off; JPEGs stay opaque | grep: 4 files |
| T10 | A | v3; Dynasty | additive glow layers draw black glass: `BlendMode` (ONE, ONE) ignored | (ONE, ONE) to `ALPHA_ONEONE`, (SRC_ALPHA, ONE) to `ALPHA_ADD`, else default plus a note; re-apply on assignment | grep: 2 files |
| T11 | A | v3; Demiurge | a looping `TimeSensor` with `startTime 0` runs from 1970: `elapsedTime` 1.8e9, a shader loses every digit | start it when the world activates; X_ITE counts from activation | read |
| T12 | A | v2, v4; Odyssey, Hall | seeking a TimeSensor twice at one timestamp lands once; a paused film stays frozen | `events.begin(ts + 1e-6)`; disable, wait two frames, set start, resume and pause times, enable; clear pause on disable | grep: odyssey (2 files) |
| T13 | A | v3; Demiurge | near plane 0.3 cuts the Earth and village out (1 m is 0.0004 units) | honour `nearDistance` and `farDistance`; re-apply when they change | grep: body-dm.js |
| T14 | A | v3; Demiurge, Dynasty | X_ITE's logarithmic depth has no Babylon counterpart; shaders that wrote `gl_FragDepth` mis-sort | `engine.useReverseDepthBuffer = true` (`?rz=0` off); write plain projected depth `c.z / c.w` | grep: 4 boot files |
| T15 | B | v1, v2 | billboards face the wrong way in a right-handed scene | orient each frame in the body (+Z at the eye) | `body.js` 78 to 95 |
| T16 | B | v1, v2 | unlit text and lines draw black | `emissiveColor`; a line set with no `Color` uses the Material's | grep: 6 files |
| T17 | B | v1 | a clip plane clips the whole scene | `material.clipPlane`, not `scene.clipPlane` | grep: body-cam.js |
| T18 | B | v1 | torso failed to load: `Matrix.FromQuaternion` on a Transform with `center` or `scaleOrientation` | `toRotationMatrix`; shear is dropped (assessment P1) | grep: body.js |
| T19 | B | v1 | viewpoint inside a rotated Transform; zoom divides by zero at the rotation centre | apply the parent rotation; clamp distance | read |
| T20 | B | v2 | coplanar textured glow panel and floor z-fight | `zOffset 4`, `zOffsetUnits 8` on the panel | grep: 2 files |
| T21 | B | v2 | metals dark and speckled; packed maps wrong | `enableSpecularAntiAliasing`, an environment floor; roughness G, metallic B, data textures `gammaSpace=false`, `invertNormalY=true` | grep: 3 files |
| T22 | B | v2 | cube map with `noMipmap = true` raises WebGPU mip errors | `noMipmap = false` | read |
| T23 | B | v2 | a mesh whose first `setVerticesData` call is a custom attribute drops it | set the position first | read |
| T24 | B | v2 | blended glow sorts differently from X_ITE | feed `bboxCenter` to `mesh.setBoundingInfo` | grep: body-gob.js |
| T25 | B | v2 | `geometryData` and `babylonGeometry` shared one cache key: the second rebuild drew 0 vertices | suffix the key with the colour variant; dispose both | read |
| T26 | B | v2 | `Background` sky gradient drawn sRGB-encoded by Babylon, almost black by headless X_ITE | logged as a gap, not tuned | GAPS.md |
| T27 | B | v3 | two views on two engines: the shim holds one browser and one body | second custom element `x3d-babylon` chosen when an adapter answers; the other view stays on X_ITE | grep: boot-dl.js |
| T28 | B | v3 | bare `Appearance` with no Material and a per-face `Color` drew black on black | route through an unlit vertex-colour program, opaque | read |
| T29 | B | v3 | `Inline`, `ProximitySensor`, `IMPORT`/`EXPORT` have no Babylon counterpart | fetch and adopt on `load`; box-test the eye in the sensor frame; answer `getImportedNode` from `getNamedNode` | grep: 3 files |
| T30 | B | v3 | `alphaMode AUTO` and a proxy sphere paint glow over an opaque core | AUTO is opaque for programs that write alpha 1; write `fragDepth`, depth write off on the blended material | grep: wgsl-dl.js |
| T31 | B | v3 | a page that probes the engine (`getComponent`, `createNode("BlendMode")`) picks its path from your shim's answer | list the probes; test both answers and every look | read |
| T32 | B | v3 | a textured UnlitMaterial at full opacity: 14 portrait plates showed at once | carry the material, `opacity = 1 - transparency`, re-apply on change | read |
| T33 | B | v4 | `Extrusion`, `Disk2D`, `Rectangle2D` have no Babylon node | convert to IndexedFaceSet at parse time; update buffers in place for animation | hall/reader-ext-hl.js |
| T34 | C | v1 | `BlendMode` and `DepthMode` are X_ITE-only; the 4.0 XSD rejects them, and `ParticleSystem` with physics | say so in the validation line; 4 names sit outside the 4.0 list | NODES.json meta |
| T35 | C | v2 | loading Babylon replaces `window.X3D`; the X_ITE engine stops | restore it after the bundle loads; engines switch both ways | grep: 6 files |
| T36 | C | v2, v3 | WGSL compile errors arrive as console warnings; a `*/` inside a block comment of a concatenated bundle ends it | the harness listens to warnings; `node --check` the bundle (only build-hall.py does) | grep: 1 of 13 |
| T37 | C | v2 | first frame shows half-built pipelines; a slowed rAF ages time-driven code | `scene.whenReadyAsync()`; pass `maxDt` | grep: 3 files |
| T38 | C | v4 | more than 16 vertex outputs: each shadow-mapped light costs two | count shadow lights per mesh before choosing cascades | read |
| T39 | C | v4, v2 | brightness gap blamed on the light unit: `lightScale 0.75` moved luma 4 percent | measure the unit first; glTF punctual units kept a hall within 1 grey level | Hall RECEIPT |
| T40 | W | v1, v2, v4 | no `gl_PointSize`, no wide lines | camera-facing quads with a `corner` attribute (`corner * (s / viewport.zw) * w`); ribbons for lines | grep: wgsl-point.js |
| T41 | W | v2, v3 | `pow(x, 2.)` of a negative; `smoothstep(a, b, x)` with a > b; `select(false, true, c)` order | `x * x`; write the clamp formula; re-derive every `select()` | read |
| T42 | W | v3 | no `inverse()`, no matrix/scalar divide, no implicit int-float mix, no `uniform float u[32]` | cofactor `inv3`; `f32(i)`; eight `vec4f` `u0..u7` and `uAt(i)` | read |
| T43 | W | v3 | window y runs down: `cross(dFdx, dFdy)` flips, dither mirrors; derivatives must precede `discard` | `cross(dpdy, dpdx)`; accept the mirrored pattern; compute `fwidth` first | Demiurge G8 |
| T44 | W | v3 | look constants differ per theme, code does not: hash keys need one port per theme | key by ComposedShader DEF; read `const` lines from the scene's GLSL | `DL_BY_DEF` |

Six more traps live in other sections and keep their numbers here:

| ID | tier | from | trap and where it lives |
|---|---|---|---|
| T45 | B | v2 | 263k-number MF arrays through the SAI: non-copying `fieldView`, typed `MFVec4f` and `MFFloat` parse (Manifold) |
| T46 | C | v1 | no adapter on some Windows laptops: section 10 |
| T47 | C | v1 | edited GLSL falls back to no shader (X3D 31.2.2): section 9 |
| T48 | C | v1 | the tone-map choice changes the picture: section 8 |
| T49 | C | v4 | `loadURL` takes an MFString; fixed page chrome over a canvas needs a `ResizeObserver` (Hall) |
| T50 | C | v2, v3 | a hidden canvas keeps rendering (skip when `getClientRects().length === 0`); a headless click on an auto-hidden control needs a mouse move first |

Carried, in no playbook version [L unless marked]: Babylon mixes fog after tone mapping, X_ITE in linear, so pass a display-space fog colour [S]; `VertexData.ComputeNormals` assumes left-handed, so pass `{ useRightHandedSystem: true }` (grep: 7 files); PCF shadows drew nothing and `usePoissonSampling` did (`drift/drift-ext.js` line 319); GL depth bias is twice too strong in WebGPU (`z -= (k / 2) * w`); a flat varying comes from the first vertex in WebGPU, the last in GL (Gobbler 3 gap G7).

## 6. The parity method: PSNR against X_ITE on a software GPU

The measurement is a witness, not a score: same file, two renderers, a number that says where to look.

1. Same scene file (record its sha256), Viewpoint, canvas size and Switch settings, in X_ITE (name the patch: 16.4.3, 16.5.1 or 16.6.0 appear in the receipts) and in the bridge page (`Babylon 9.32.0`), "As authored" only.
2. Headless Chromium 153 on SwiftShader cannot present a WebGPU swap chain (every pipeline reports "Instance dropped"). `stub-swapchain.py` replaces `canvas.getContext('webgpu')` with an object whose `getCurrentTexture()` returns an offscreen texture; the page reads it back (`__demo.capture`, `__snap`).
3. Slow `requestAnimationFrame` (600 ms splat viewers, 1.2 s brain) or frames pile up and the read-back waits over ten minutes.
4. Pin time: seek both renderers (Odyssey), use the page's freeze, or compare the scene hash instead of pixels for scenes that grow (`scenes.sha256` for the HEP events).
5. PSNR on 8-bit RGB, `10 * log10(255^2 / MSE)`, with the mean absolute difference; state whole frame, crop or mask. Layers that differ by construction (tracts, slice planes, labels) score low: say so, do not tune to the metric.
6. Write `RECEIPT.md` (rig, versions, scripts) and `GAPS.md` (each line graded). The bridge's visual rig adds bounds to a test spec (`iou` silhouette overlap, `mad`, `fg` mean colour of drawn pixels, `cover`, `bbox`, `count`); a shot where neither engine drew anything fails unless `empty` is true.

A worked number (D-BAB-4, re-run): the two committed facade frames, 960 x 540, X_ITE 16.4.3 against our own-runtime page.

| window | PSNR | MAE of 255 |
|---|---|---|
| whole frame | 39.30 dB | 0.84 |
| bottom 40 rows cropped (the receipt's caption crop) | 41.90 dB | 0.79 |

The receipt's 41.9 dB and 0.79 are re-derived; the same frames differ by 2.6 dB between the whole frame and one crop. A PSNR without its window is not comparable with another PSNR.

```text
  dB   what the rows are                                   rows (reference X_ITE patch)
  50 +  shaders ported term for term, no lens or bloom     Pantheon splats 50.17, 51.01 (16.4.3)
  49 +                                                      Manifold 49.34, 48.47 (16.5.1)
  42 +  one generated view                                  facade 41.90, re-derived (16.4.3)
  35 +  lit meshes, glass, layers                           brain 33.03 all; 35.11 glass to
     |                                                      30.26 torso (16.6.0)
  30 +  "same picture, small shading differences"           Dynasty 29.0 to 37.8 (16.5.1)
  25 +  "same scene, detail differs"                        KANSEI 24.36 to 32.46; Chirp 24.87
     |                                                      to 25.36; Odyssey 25.5 to 30.7
  21 +  thin things: ribbons, labels, slice planes          brain tracts 22.51, labels 21.53
  17 +  method: clocks, pose, background                    Hall 17.5 to 25.3; Gobbler 3 14.60
     |                                                      to 19.66; Cloud 19.24 whole frame
   7 +  "means little" in the receipt's own words           Demiurge 7.18 to 13.26 (16.5.1)
```

Rows are read from `runs/webgpu-*/RECEIPT.md` and `GAPS.md` at `x3d.loom@162ab18` **[L]**; rig in each: Chromium 153.0.8010.12, SwiftShader, stubbed swap chain (Odyssey names "headless Chromium" without a version). The tiers are ours; the receipts say only that 30 dB or more is "the same picture with small shading and edge differences" and 24 to 29 dB the same scene differing in detail.

**What the ladder cannot say:**

| it cannot say | evidence | grade |
|---|---|---|
| that a bright number is a faithful picture | `Polypoint2D`: iou 1, 40.03 dB, drawn pixels' mean colour [202, 162, 41] in ours and [64, 51, 13] in X_ITE: a few small squares on black move PSNR little (`BATCH-26.md`, X_ITE 16.6.0, 320 x 240) | C (read) |
| that a low number is a wrong picture | `ExplosionEmitter`: iou 0.05, 11.73 dB, verdict PASS: particle age differs on a CPU raster, so extent is compared with a wide bound (`BATCH-23.md`) | C (read) |
| that the window is the same | Cloud 19.24 dB whole frame, 21.01 with background excluded; facade 39.30 against 41.90 | C |
| that the clocks agree | Gobbler 3 captured the engines at different instants; its gap G4 says PSNR "is not a parity figure"; Demiurge G4: 7 to 13 dB "means little"; Dynasty night Crown 18.8 and Wide 22.1 "probably pose drift" [S]. Odyssey and KANSEI pin time (seek; sim hash equal in 6 of 6 views); the Hall's receipt says its film clock agrees; for the other receipts the clock is not stated | C (read) |
| that it holds on a real GPU or within a tolerance | all rows are SwiftShader; the spec's profiles (`parity/look` 4/255 and luma 0.01; SSIM 0.95 and PSNR 30 for the benchmark) are proposals and calibration (X_ITE against itself on two GPUs, TBD-13) is not done | C |

## 7. The ports and what each taught

| # | port, PR (merge) | headline parity (reference, size) | what it taught |
|---|---|---|---|
| 1 | Pantheon splats, #11 (7 Nov), own runtime | 50.17, 51.01 dB (16.4.3, 960 x 540) | the stub swap chain; GPU bitonic sort; X_ITE's splat shader ported line by line |
| 2 | HEP events and facade, #12 (7 Nov) | facade 41.9 dB (16.4.3); events by scene hash | event scenes grow: compare hashes; 140,000 splats pad to 262,144 (171 dispatches) |
| 3 | Neural Canvas, #13 (7 Nov) | 33.03 all; 21.53 to 35.11 per layer (16.6.0, 640 x 360) | winding, `alphaIndex`, billboards, clip planes, 4 shader keys |
| 4 | adapter retry, #14 (7 Nov) | none | harmless, not the cure for the blocklist (section 10) |
| 5 | KANSEI, #17 (7 Nov) | 24.36 to 32.46 masked (16.5.1, 640 x 360) | fog order, right-handed normals, shadows; keep the simulation out of the renderer |
| 6 | Manifold, #19 (7 Nov) | 49.34, 48.47 (16.5.1, 640 x 360) | emit callbacks, `fromLinearSpace`, attribute order, big arrays; 7 keys |
| 7 | Chirp and Cloud, #21 (7 Nov) | 24.87 to 25.36; 19.24 to 19.40 whole, 21.01 to 24.96 masked (16.5.1, 1100 x 700) | unlit HDR vertex colour, the geometry cache key, `Background` sky; re-run earlier pages after editing shared files |
| 8 | Gobbler 3, #22 (7 Nov) | 14.60 to 19.66 (16.5.1, 640 x 360) | depth bias, flat varyings, point quads; clocks not locked; 6 keys |
| 9 | Material Odyssey, #23 (8 Nov) | 25.5 to 30.7 as authored; 18.4 to 28.2 look on (16.4.3, 1280 x 536) | light scope, USE audit, emissive texture, seeking; no new node type needed |
| 10 | Gobbler Demiurge, #24 (8 Nov) | 7.18 to 13.26 (16.5.1, 960 x 540) | `startTime 0`, pause, near and far, reversed depth; 4 keys |
| 11 | Dynasty Loom, #25; Library Hall, #27 (8 Nov) | 29.0 to 37.8; 17.5 to 25.3 (16.5.1) | two engines on one page, `BlendMode`, `IMPORT`/`EXPORT`; the Hall has no shader ("the first all-standard-node page", v4) |

[L] for every parity cell (read in the named receipts, not re-run except the facade).

## 8. A look may add, never assert; a fallback must say so

Both rules are [Loom laws](02-loom-laws.md) (39 and 40), kept on this track as code habits.

| rule | mechanism and evidence | grade |
|---|---|---|
| a look decorates and can be switched off | Odyssey: switch `OD.on`, Look button (key L), `?look=0`; Chirp and Cloud: a pill and `?look=0`. Recipe: generated cube environment, `DefaultRenderingPipeline` (MSAA 4, bloom, grain, vignette, neutral tone map), camera dust, up to three spot shadow generators. Odyssey look off 25.5 to 30.7 dB, on 18.4 to 28.2 dB (16.4.3): the look adds reflections, bloom, shadows, grain and dust by design and is "not a target" | L (playbook v2 section 2, receipt) |
| a default can assert | Collider: Neutral tone map at exposure 1.65 turned towers pink-white (13.9% near-white crown pixels against 1.2% for per-channel exp at 1.35), found by counting pixels on a purpose-built region, not by PSNR | L (playbook v1 4.2) |
| a miss, a gap or a software adapter must show | a hash miss draws the Material; 6 of 13 builders refuse an unported shader; `scene.getFidelityReport()` keeps recognition, known gaps and unverified fidelity apart ("no report is a conformance certificate", `bridge/README.md`); `adapter.js` and `timing.js` name the adapter and label SwiftShader, WARP and llvmpipe "these numbers do not count" | C (read, grep) |
| unknown nodes should not vanish silently | the reader tallies unknown tags; on screen only in the manifold and Gobbler 3 pages, a console line elsewhere (2 of 7 pages at 8 Nov) | S (primer, carried) |

## 9. Shader porting: hash-keyed GLSL to hand-written WGSL

```text
  <ComposedShader DEF=..>  ShaderPart VERTEX url="data:..,GLSL"   ShaderPart FRAGMENT url=..
        |  decode the data URL (base64 or percent), keep the text after the first comma
        v
  collapse each run of whitespace to one space, trim:     s.replace(/\s+/g, ' ').trim()
        v
  FNV-1a, 32-bit:  h = 0x811c9dc5;  per UTF-16 unit  h ^= c;  h = imul(h, 0x01000193) >>> 0
        v
  key = hex8(vertex) + '-' + hex8(fragment)          e.g.  1bc84a9f-b6fcc411  (collision flash)
        v
  table lookup:  hit  -> hand-ported WGSL with its uniform names
                 miss -> Material fallback and a notice on screen (law 40); never a guess
```

Worked example, the five Collider programs (D-BAB-3: an independent Python port of the same hash over `demo/collider.x3d`, equal to the `key:` fields in `collider-v2.html`) **[C]**:

| DEF | role | key (vertex-fragment) |
|---|---|---|
| `trkShader2` | tracks | `da010848-2732de59` |
| `twrShader2` | calorimeter towers | `e899d3ba-71ea799c` |
| `shellShader2` | detector shells | `2318d20e-451c1b62` |
| `flashShader2` | collision flash | `1bc84a9f-b6fcc411` |
| `hazeShader2` | backdrop haze | `07e052cf-7ecaed2f` |

Extra spaces inside the flash fragment leave the key unchanged; changing one constant (`12.0` to `12.5`) moves only the fragment half, to `1bc84a9f-bd1839be`, and the program misses. That is the feature: the page cannot claim to render code it did not run.

Counts at `162ab18` [C, grep `'[0-9a-f]{8}-[0-9a-f]{8}'` over 9 files of `demo/src`]: 26 distinct hash keys (Collider 5, brain 4, manifold 7, Gobbler 3 6, Demiurge 4); the primer's 22 on 8 Nov is 5 + 4 + 7 + 6, before Demiurge. Dynasty keys 6 programs (`sky`, `ring`, `seedcore`, `seedglow`, `fiber`, `shell`) by ComposedShader DEF, because its two looks differ only in `const` look constants read out of the scene's own GLSL (`dynasty/wgsl-dl.js`, `DL_BY_DEF`). The Hall's builder refuses any ComposedShader.

The WGSL rules that cost time are T40 to T44 in section 5. Review rule from the Gobbler port: one author writes the WGSL term for term and a second re-derives every constant, operator and `select()` argument order; that review found one real defect [L, carried]. WGSL compile errors surface as console warnings, so a harness must listen to them (T36).

## 10. The adapter and blocklist trap

| observation | detail | source | grade |
|---|---|---|---|
| symptom | "requestAdapter() returned no adapter" or "WebGPU not available" on one Windows laptop (Intel gen-9 integrated GPU, UHD 620 class, Chrome 156); plain and `high-performance` requests both null | playbook v1 section 4.1 | L (read; no Windows here) |
| cause | `chrome://gpu` Dawn Info lists the adapter only on the D3D11 backend, blocklisted ("D3D11 backend not fully implemented", crbug.com/41479539); the only other adapter, the CPU Basic Render Driver, is blocklisted too | same; `x3d.demo@d10b457:docs/index.html` repeats it | L |
| a wrong theory | "the viewer asked only for `high-performance`": `shared/adapter.js` now retries plain, caller options, low-power, fallback adapter and records the winner in `window.__adapterVia`; harmless, not the cure | playbook v1; `adapter.js` | C (read) |
| the fix that worked | `chrome://flags/#enable-unsafe-webgpu` set to Enabled, relaunch. The demo page warns it "switches off Chrome's safety check for WebGPU on that GPU, so use it for these demos only". A Mac with a normal Metal adapter was fine; Edge is another route | playbook v1; `docs/index.html` | L |
| a source conflict | `STATE.md` 4.2 records a probe on this hardware (7 Nov) that got a hardware adapter without the flag and says Chromium's default blocklist patterns hold only Qualcomm and `*:*:PowerVR*25.1*`; the playbook says the same hardware later returned null and the browser state had differed. Cause unknown | `STATE.md`, playbook v1 | L; neither re-run |

A page must show the tip when `requestAdapter()` is null, and which adapter and request answered (law 40). Diagnose in order: a probe page over http or `file://`, never `about:blank` where `navigator.gpu` is absent (`bench/webgpu-probe.html`); `chrome://gpu`, Dawn Info, "Blocklisted"; the flag, knowing what it disables; another browser or machine. In this sandbox the only adapter is SwiftShader's fallback, with `--enable-unsafe-webgpu` [L, `STATE.md` section 5].

## 11. Porting a new demo: sixteen steps, append-only

`x3d.demo` keeps every version: `docs/versions/vN/index.html` is a frozen snapshot, `docs/index.html` the newest copy, demos live at `docs/demos/<name>/vN/`; "nothing is overwritten; a change makes a new version" (`x3d.demo@d10b457:CHANGELOG.md`). Of the 13 `build*.py`, 5 enforce a new output folder in code (`grep -l -i "refusing to overwrite\|never overwrite\|must be new" build*.py`: demiurge, dynasty, hall, manifold, odyssey), 6 refuse an unported shader (`grep -l "no WGSL port\|carries a ComposedShader" build*.py`) and 1 runs `node --check` on the bundle (hall) [C].

| # | step |
|---|---|
| 1 | validate the scene, record its sha256; the file is the master (law 38) |
| 2 | census its node names against `NODES.json`; list every non-`base` node and every ComposedShader |
| 3 | copy the carrier: `reader.js`, `body.js`, `body-cam.js`, `sai.js`, `wgsl.js`, `boot.js`, `adapter.js`, `timing.js`; add `kit.js`, `nodes/*.js`, `body-br.js` only if the scene needs kit nodes (builders omit the kit by default) |
| 4 | pin Babylon to one exact version from a CDN with a subresource-integrity hash (9.32.0 so far) |
| 5 | hash every shader, write the ports, make the builder refuse an unported one |
| 6 | run the demo's own `app.js` unchanged against the SAI shim; a patch is a finding |
| 7 | match X_ITE as authored first; add looks after, switchable, with `?look=0` |
| 8 | read `global` on every light and scope the non-global ones; audit USE for state keyed by node id; check the light unit before blaming it (T03, T04, T39) |
| 9 | put fallbacks on screen: shader miss, unknown nodes, adapter name, the flag tip |
| 10 | build into a **new** folder; `node --check` the bundle |
| 11 | measure: stub swap chain, slowed rAF, pinned time, As authored, window named, per layer |
| 12 | write `runs/<name>-<date>/RECEIPT.md` (rig, versions, scripts) and `GAPS.md` (each line graded); list audio, Timing and a real-GPU pass as open |
| 13 | leak sweep on the served bytes: model and vendor names, cloud ids, cost figures, private links, unpublished material, keys, embedded metadata |
| 14 | publish to `docs/demos/<name>/v1/` (vN+1 for a revision), add `docs/versions/vN`, copy it to `docs/index.html`, add a CHANGELOG line and a `SOURCES.md` row with byte hashes |
| 15 | say on the page what it is: renderer and version, "correctness evidence, no timings", the flag tip |
| 16 | if you edited a shared file, re-run the earlier pages' smoke tests; open a PR; verify the live URL after Pages builds |

## 12. No speed claim exists, and what one would take

- No receipt holds a WebGPU or Babylon timing from a real GPU: `bench/receipts/` has one file, the G1 adapter probe; the timing test I read (`runs/webgpu-drift-20261107`) feeds synthetic timestamps to the panel [C, `ls`, receipt read].
- The Timing panel is opt-in: 2 s warm-up, 20 s window, p50, p95, p99, adapter and canvas recorded, software adapters labelled; 7 of 13 builders include it [C, `shared/timing.js`, grep].
- The decision rule (`BENCHMARK.md` section 9, **[L]**): Go only if parity holds (SSIM 0.95, PSNR 30), p95 is at most 0.70 of arm A in all 3 runs, at most 0.85 of the engine's own WebGL2 arm, with no 10% regression; otherwise No-go or Inconclusive. Gate G0 (consent to use a named real GPU for metrics) is open.
- The only real-GPU number in the sources is an X_ITE frame rate on one machine, vsync-capped: a ceiling check, not a comparison ([06](06-xite-the-oracle.md), `STATE.md`) [L, carried].

A timing claim needs a named GPU and driver, vsync off, three runs and their spread, the same scene on the X_ITE arm and on the engine's WebGL2 arm, and a receipt that fits `bench/receipt.schema.json`. Until then this chapter says nothing about "faster", "lighter" or "smoother", and neither should a page.
## Heuristics

| ID | Rule (imperative, at most 30 words) | Grade | Evidence | Instrument |
|---|---|---|---|---|
| H-BAB-1 | Give every node count its denominator and definition: page-bundle census, tracker headline or bridged-without-gap. Never subtract across definitions. | C | 68, 75, 186 and 41 all describe one codebase (N-BAB-2 to N-BAB-5) | `census.js`, `driver.py status`, `x3d.loom@162ab18` |
| H-BAB-2 | Treat `bridged` as one fixture passing in two engines at 320 x 240, and read the node's gap note before quoting it. | C | 70 of the 111 kit modules are `gap`; the assessment separates recognised, passing and correct | `NODES.json`, `ASSESSMENT-2026-11-08.md` |
| H-BAB-3 | Write the PSNR window (whole frame, crop or mask) beside every dB figure. | C | same two frames: 39.30 dB whole, 41.90 cropped | numpy PSNR, 960 x 540 (D-BAB-4) |
| H-BAB-4 | Do not accept or reject a node on dB; use the bounds written in its test spec and look at the picture. | C | 11.73 dB with verdict PASS; 40.03 dB with a drawn colour 3 to 4 times dimmer | `BATCH-23.md`, `BATCH-26.md`, X_ITE 16.6.0 |
| H-BAB-5 | Pin time in both renderers before comparing an animated scene, or label the figure "not a parity figure". | L | Gobbler 3 and Demiurge receipts say so; Odyssey and KANSEI pin | `runs/webgpu-*/GAPS.md`, SwiftShader |
| H-BAB-6 | Key a shader port by FNV-1a of the whitespace-collapsed GLSL; on a miss draw the Material and say so; make the builder refuse an unported shader. | C | whitespace edit keeps the key, one constant changes the fragment half; 6 of 13 builders refuse | Python port of the page hash (D-BAB-3) |
| H-BAB-7 | When a port looks wrong, check tier A of the trap table before touching light: winding, colour space, light scope, USE identity, emissive texture. | L | the playbooks' own advice; the tier order is our judgement [S] | playbooks v1 to v4 |
| H-BAB-8 | On every public WebGPU page show the adapter, which request answered and, when null, the flag tip with its safety cost. | L | one gen-9 laptop got no adapter until the flag was set | playbook v1; `docs/index.html` |
| H-BAB-9 | Make no speed claim without a named real GPU, driver, three runs and a receipt that fits the schema. | C | 0 timing receipts for any bridge body; 1 file in `bench/receipts/` | `ls`, `BENCHMARK.md` section 9 |
| H-BAB-10 | Where a playbook line and the code disagree, the code wins; record both and correct the playbook by a new version. | C | v1 and v2 say "convert authored sRGB"; `body.js` line 303 assigns the colour as authored | `brain/body.js` read |

## Drills

### D-BAB-1 Recount the bridge's coverage
- **Level:** L2
- **Task:** From `x3d.loom@162ab18:x3d.webgpu/bridge`, print the tracker totals, then count node names in the six reader parts and say how many of them are in the 260.
- **Verify:** `python3 tools/driver.py status`; `node tools/census.js ../demo/src > c.json`; then `python3 -I -c "import json;c=set(json.load(open('c.json'))['defs']);n=json.load(open('NODES.json'))['nodes'];print(len(c),len([x for x in c if x in n]))"`
- **Answer:** `reader knows 186/260 | base 75 blocked 1 bridged 41 claimed 8 gap 70 todo 65`; census prints `79 75` (4 defs outside the 4.0 list: `BlendMode`, `DepthMode`, `EnvironmentLight`, `GaussianSplats`). 186 = 75 + 41 + 70.
- **Checked:** 2026-11-14 `x3d.loom@162ab18`, Node 22.23.4, Python 3

### D-BAB-2 Re-derive the primer's 68
- **Level:** L2
- **Task:** Reproduce the primer's "68 of 260" from the tree it cites, then list what the same census gains by today.
- **Verify:** `git archive 60824ce x3d.webgpu/demo/src | tar -x -C OLD`; `node tools/census.js OLD/x3d.webgpu/demo/src`; repeat on the current tree and diff the `defs`.
- **Answer:** 72 defs, 68 in the 4.0 list, against 79 and 75 today. Added: `HAnimHumanoid`, `HAnimJoint`, `HAnimSegment`, `HAnimSite`, `Inline`, `LOD`, `ProximitySensor`; none removed. The tracker did not exist at 60824ce, so 68 to 186 is not like for like.
- **Checked:** 2026-11-14 `x3d.loom@162ab18` and `60824ce`, Node 22.23.4

### D-BAB-3 Break a shader key, then predict which half moves
- **Level:** L3
- **Task:** Compute the keys of the five ComposedShaders in `x3d.webgpu/demo/collider.x3d` with an independent implementation and compare them with the `key:` fields in `collider-v2.html`. Then (a) add runs of spaces inside `flashShader2`'s fragment and (b) change `u_phase * 12.0` to `u_phase * 12.5`; predict both keys first.
- **Verify:**
```python
import re, sys, urllib.parse
from lxml import etree
def fnv(s):
    h = 0x811c9dc5
    for c in s: h = ((h ^ ord(c)) * 0x01000193) & 0xffffffff
    return '%08x' % h
n = lambda s: re.sub(r'\s+', ' ', s).strip()
def src(u):
    b = re.match(r'\s*"?(data:[^"]*)"?\s*$', u, re.S).group(1).split(',', 1)[1]
    return urllib.parse.unquote(b) if re.search(r'%[0-9a-fA-F]{2}', b) else b
for cs in etree.parse(sys.argv[1]).iter('ComposedShader'):
    if cs.get('DEF'):                        # USE copies carry no parts
        p = {x.get('type').upper(): src(x.get('url')) for x in cs.iter('ShaderPart')}
        print(cs.get('DEF'), fnv(n(p['VERTEX'])) + '-' + fnv(n(p['FRAGMENT'])))
```
- **Answer:** the five keys equal the table in section 9. (a) leaves `1bc84a9f-b6fcc411` unchanged; (b) gives `1bc84a9f-bd1839be`: only the fragment half moves and the page would miss the port and fall back.
- **Checked:** 2026-11-14 `x3d.loom@162ab18`, Python 3 with lxml, scratch copies of the scene

### D-BAB-4 Move a PSNR by changing its window
- **Level:** L2
- **Task:** Compute PSNR and mean absolute error between the two committed facade frames, whole and with the bottom 40 rows cropped, and say which the receipt used.
- **Verify:** `runs/webgpu-quick-wins-20261107/frame-facade-webgpu.png` and `frame-facade-xite16.4.3.png` (960 x 540); `psnr = 10*np.log10(255**2 / ((a-b)**2).mean())` on RGB floats, over `[:540]` and `[:500]`.
- **Answer:** whole frame 39.30 dB (MAE 0.84); bottom 40 rows cropped 41.90 dB (MAE 0.79), the receipt's 41.9 and 0.79. A 2.6 dB spread from the window alone.
- **Checked:** 2026-11-14 numpy 2.5.3, Pillow 12.3.0, `x3d.loom@162ab18`

### D-BAB-5 Census a corpus before you promise a port
- **Level:** L3
- **Task:** For every `.x3d` under `x3d.demo@d10b457:docs/demos`, list node names, classify each by `NODES.json` status and report how many scenes need only `base` names. Then say why "base" is not a promise that a given page can load the scene.
- **Verify:** parse each file with lxml, skip `X3D head Scene ROUTE field meta component unit IS connect fieldValue Proto* IMPORT EXPORT`, treat `BlendMode DepthMode EnvironmentLight GaussianSplats` as extension names, look the rest up in `NODES.json`.
- **Answer:** 111 files parse (the two `facade.x3d` do not); 86 use only `base` or extension names, 22 use at least one `gap`, `todo` or `claimed` node (CoordinateInterpolator 9, LineSet 8, PointProperties 6, Geo nodes 2 each), 1 uses unknown names. "Base" is the union of six reader parts: a page loads only its own bundle, and each page's census must be run on its own `PARTS` list (the hall extension alone adds 8).
- **Checked:** 2026-11-14 lxml, `x3d.demo@d10b457`, `x3d.loom@162ab18`

## Honest limits

- **Software GL only, Chromium only [C].** Every pixel number is SwiftShader in Chrome for Testing 153.0.8010.12; no real GPU, Firefox or Safari. Babylon 9.32.0 is a snapshot; 9.33.0 to 9.35.0 (per the primer) were not run [L].
- **Per-port dB figures are read, not re-run [L].** Re-run here: the facade frames, the census counts, the hash keys, the greps, the 33 tests. The 42 visual rows of batches 21 to 26 were parsed from the batch reports, not regenerated (that needs X_ITE 16.6.0 and a browser).
- **Sources disagree.** C1: playbooks v1 and v2 say to convert authored sRGB; `brain/body.js` line 303 assigns the colour as authored; the code is the evidence and no later playbook version corrects the sentence. C2: "42 of 260" (playbook v1), 62, 68 and 186 count different readers; the primer explains 42 as 44 table entries minus 2 X_ITE-only names [L, carried]. C3: the blocklist, `STATE.md` against the playbook (section 10). C4: the primer's "55 traps" is its own symptom table; the 50 here merge the four playbook files; they are not the same list. C5: the primer's 22 hash keys against 26 today. C6: batch headlines are non-monotonic (184, 184, 181, 186); the dip's cause is inferred [L].
- **Open defects were read at `6b3cb76`, not re-checked at `162ab18` [L]:** shared-node occurrence bookkeeping, dropped shear, IndexedFaceSet normals, ignored `head/unit`, ColorRGBA alpha. They bound what "bridged" means.
- **Behaviour was never compared [L].** No event traces, pointer tapes or audio pass; fixtures compare ROUTE chains in two engines, not whole pages. The noise floor of X_ITE against itself (TBD-13) is unmeasured, so no dB threshold here is a standard.
- **Carried, not re-checked [S]:** law-40 coverage by page, the Gobbler review defect, all effort figures in `PATHS.md` and `BABYLON.md` (person-weeks are guesses), the 1,396 `gl.*` call sites. Private run logs, device owners' details and unpublished material are left out on purpose.

## Numbers register

| ID | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|
| N-BAB-1 | concrete nodes in the bridge tracker | 260 | C | `X3DUOM 4.0` via `NODES.json` | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-2 | tracker headline "reader knows" | 186 of 260 (71.5%): base 75, gap 70, bridged 41; claimed 8, blocked 1, todo 65 | C | `driver.py status`, `x3d.loom@162ab18` | x3d.loom@162ab18:x3d.webgpu/bridge/tools/driver.py (D-BAB-1) |
| N-BAB-3 | page-bundle census, 8 Nov tree | 68 of 260 (72 defs) | C | `census.js` on `git archive 60824ce` | x3d.loom@60824ce:x3d.webgpu/demo/src (D-BAB-2) |
| N-BAB-4 | page-bundle census, today | 75 of 260 (79 defs); 83 (87) with the hall extension | C | `census.js`, 162ab18 | x3d.loom@162ab18:x3d.webgpu/bridge/tools/census.js |
| N-BAB-5 | bridged without a logged gap | 41 of 260 (15.8%) | C | `driver.py status` | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-6 | batch headlines 20 to 26 | 175, 175, 179, 184, 184, 181, 186 | L | read in `BATCH-NN.md` | x3d.loom@162ab18:x3d.webgpu/bridge/BATCH-20.md to BATCH-26.md |
| N-BAB-7 | slots filled by batches 21 to 26 | 30: 17 bridged, 13 gap; PRs #43 to #45 | C | `NODES.json`, merge log | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-8 | visual compare rows, batches 21 to 26 | 42 rows; PSNR 11.73 to 40.03, median 35.92 | C | parsed from the reports; X_ITE 16.6.0, 320 x 240, SwiftShader | x3d.loom@162ab18:x3d.webgpu/bridge/BATCH-21.md to BATCH-26.md |
| N-BAB-9 | X_ITE 16.7.0 WebGPU strings | 0 "webgpu", 0 `navigator.gpu`, 1 `getContext("webgl2"` | C | grep, `x_ite.min.js` sha256 prefix b7df063e8cb1 | x3d.docs@f172f67:docs/vendor/x_ite/x_ite.min.js (grep, section 2) |
| N-BAB-10 | merged traps | 50: first seen v1 13, v2 19, v3 13, v4 5; tiers A 14, B 20, C 11, W 5 | C (count), S (ranking) | script over the section 5 table | this chapter, section 5 |
| N-BAB-11 | distinct hash-keyed shader programs | 26 (Collider 5, brain 4, manifold 7, Gobbler 3 6, Demiurge 4); 22 on 8 Nov; 6 more keyed by DEF in Dynasty | C | grep of `'[0-9a-f]{8}-[0-9a-f]{8}'` | x3d.loom@162ab18:x3d.webgpu/demo/src |
| N-BAB-12 | facade PSNR by window | 39.30 dB whole; 41.90 dB bottom 40 rows cropped; MAE 0.84 and 0.79 | C | numpy, Pillow, 960 x 540, X_ITE 16.4.3 reference | x3d.loom@162ab18:runs/webgpu-quick-wins-20261107/ (D-BAB-4) |
| N-BAB-13 | Pantheon splats; Manifold | 50.17 and 51.01 dB; 49.34 and 48.47 dB | L | `X_ITE 16.4.3` (960 x 540); `X_ITE 16.5.1` (640 x 360); SwiftShader | x3d.loom@162ab18:runs/webgpu-{pantheon-splats,manifold}-2026110*/RECEIPT.md |
| N-BAB-14 | brain, Babylon 9.32.0 | 33.03 all; 35.11 glass to 21.53 labels; torso 30.26 | L | `X_ITE 16.6.0`, 640 x 360, SwiftShader | x3d.loom@162ab18:runs/webgpu-brain-20261107/RECEIPT.md |
| N-BAB-15 | KANSEI, masked | 24.36 to 32.46 over 6 views; sim hash equal in 6 of 6 | L | `X_ITE 16.5.1`, 640 x 360, SwiftShader | x3d.loom@162ab18:runs/webgpu-drift-20261107/RECEIPT.md |
| N-BAB-16 | Material Odyssey | 25.5 to 30.7 as authored (6 film times); 18.4 to 28.2 look on | L | `X_ITE 16.4.3`, 1280 x 536, SwiftShader | x3d.loom@162ab18:runs/webgpu-odyssey-20261108/RECEIPT.md |
| N-BAB-17 | Chirp; Cloud; Gobbler 3; Demiurge; Dynasty; Hall | 24.87 to 25.36; 19.24 to 19.40 (21.01 to 24.96 masked); 14.60 to 19.66; 7.18 to 13.26; 29.0 to 37.8; 17.5 to 25.3 dB | L | `X_ITE 16.5.1`, SwiftShader | x3d.loom@162ab18:runs/webgpu-{chirp,cloud,gobbler,demiurge,dynasty,hall}-*/ |
| N-BAB-18 | corpus name census | 111 files: 86 base-only, 22 need gap or todo or claimed, 1 unknown | C | lxml, `NODES.json` | x3d.demo@d10b457:docs/demos (D-BAB-5) |
| N-BAB-19 | real-GPU timing receipts for any bridge body | 0; `bench/receipts/` holds 1 file (the G1 adapter probe) | C | `ls` | x3d.loom@162ab18:x3d.webgpu/bench/receipts/ |

## Sources and provenance

- `x3d.loom@162ab18` (read 2026-11-14): `x3d.webgpu/{README,STATE,PATHS,BABYLON,BENCHMARK,SPEC}.md`, the four playbook files, `bridge/` (tracker, assessment, batches 01 to 26, tools, src, fixtures, receipts), `demo/src/`, `runs/webgpu-*/`. Re-run: census, driver status, tests, hash keys, greps. `x3d.loom@60824ce` extracted with `git archive` (D-BAB-2).
- `x3d.demo@d10b457`: `CHANGELOG.md` (append-only rule), `docs/index.html` (blocklist text), `docs/demos/SOURCES.md`, every `.x3d` for D-BAB-5. `x3d.docs@f172f67`: `docs/vendor/x_ite/x_ite.min.js` (grep, section 2); chapters [06](06-xite-the-oracle.md) and [02](02-loom-laws.md); [the Loom masterclass](../x3d.loom/MASTERCLASS.md) for the AST view of the same repository, not duplicated here.
- Private-source gap: a private primer of 8 November and private notes on each port were pointers only. Figures here were re-derived from the repository or read from a named receipt; the rest are graded [S] or [L] and labelled carried. No private document, link, identifier or chat wording is reproduced.
- Siblings: [01](01-the-tether.md), [03](03-validator-and-gates.md), [04](04-mcp-for-agents.md), [07](07-xray.md), [09](09-castle-engine.md), [11](11-gltf-usd-khronos.md), [13](13-physics.md).
