# Field notes: four Blender pipeline demos (Demos 58 to 61, 19 Nov 2026)

The Blender pipelines lane built four demos in one day on x3d-blender-io 8310e7b and Blender 5.3.0 (bpy pip wheel). Grades: **C** = Confirmed by a named tool in this work, **L** = Likely (strong evidence, one cause not isolated), **S** = Suspected. Rig for every browser number: Playwright headless Chromium 157.0.8103.78, SwiftShader, no GPU. Validator: x3d_mcp 39c6e94 (`validate_xml` XSD, `validate_semantic`).

| Demo | Folder in x3d.demo | Headline |
|---|---|---|
| 58 Baked Light Gallery | `docs/demos/blender-baked-light/v1/` | Cycles light baked per corner, drawn unlit: X_ITE 16.7.1 vs Cycles SSIM 0.960, X_ITE vs Babylon 7.54.0 SSIM 0.9992 |
| 59 Flywheel Forge | `docs/demos/blender-flywheel-forge/v1/` | an agent's bpy orrery through an 8-check gate: 4/8 → 8/8 over 8 generations, SSIM 0.933 |
| 60 One Asset, Every Engine | `docs/demos/blender-every-engine/v1/` | one .blend in X_ITE, X3DOM, Castle, three.js, Babylon, Blender re-import; two glTF flags take three.js from SSIM 0.81 to 0.966 |
| 61 The Walking Twin | `docs/demos/blender-walking-twin/v1/` | IFC4 building + 16-joint H-Anim 2.0 walker; click reads GlobalId and carbon through SAI; 24/24 GlobalIds found in the IFC |

## 1. Rules for the next agent

| # | Rule | Grade | Evidence |
|---|---|---|---|
| 1 | **Valid is not visible.** Gate on a frame, not only on validators. Forge gen 0 passed XSD, semantic, size and a clean X_ITE load and drew a black frame (mean 0.014). In Demo 60 every file passed its validator and 4 of 8 default legs drew over half the frame pure white. | C | Forge gate.json gen 0; Demo 60 scores.json |
| 2 | **Gate the gate.** Two of the Forge's defects were in the gate: a grey Cycles world the browser never draws (new Worlds get a grey Background node), and a wall-clock motion check that read 0.41 and 0.54 on two runs. Use a black world for references and drive interpolators through SAI (`set_fraction`) for motion. | C | Forge gen 1 and gen 2 reruns |
| 3 | **Blender lights reach X3D capped.** Lights made in Blender export at intensity ≤ 1 with no attenuation. Set `x3d_attenuation` = 0 0 1 and `x3d_energy_per_intensity` (4π for a point lamp, 1 for a sun). `x3d_intensity` only marks a value as meant; it does not set it. | C | Forge gen 3 (SSIM 0.871 → 0.954), gen 7 first try (3.0 exported unchanged) |
| 4 | **`use_animation` is off by default** in the X3D export: a keyframed scene exports frozen and still passes every validator. | C | Forge gen 0 → 1 |
| 5 | **A lamp inside an emitter mesh:** the exporter keeps `use_shadow`, so `PointLight shadows="true"` inside the Sun sphere shadows the whole scene in X_ITE. In glTF and USD the flag is lost and the re-imported lamp casts shadows again. Keep lamps out of emitters. | C | Forge gen 1; Demo 60 USD re-import SSIM 0.880 → 0.990 with only `use_shadow=False` restored |
| 6 | **X_ITE 16.7.1 ignores a light's `ambientIntensity` under PhysicalMaterial** (frames byte-identical), and metallic 1.0 with no environment map reads black. Use metallic ≈ 0.7 or ship an environment. | C | Forge gen 6 (dead end, kept), gen 2 |
| 7 | **glTF light units:** Blender's glTF exporter defaults to physical units (sun 3.0 → 2,049 lux, 400 W lamp → 21,741 cd); three.js r170, Babylon 7.54.0 and Castle 5.3.0 white out. `export_import_convert_lighting_mode="COMPAT"` fixes it, and the importer needs the same flag. | C | Demo 60: SSIM 0.81 → 0.966 / 0.965 / 0.936; re-import 0.553 → 0.880 |
| 8 | **glTF animations:** the default ACTIONS mode writes one glTF animation per object; Blender's own importer plays only the first and parks the rest in muted NLA tracks. `export_animation_mode="ACTIVE_ACTIONS"` writes one animation with every channel. | C | Demo 60: 4 animations → 1 with 4 channels, re-import motion 0.79 → 8.61 /255 |
| 9 | **X3DOM 1.8.3 whites out PhysicalMaterial** scenes; the same file with Material instead drops from 53% to 4.5% white. | C | Demo 60 single-variable test |
| 10 | **Castle clears to 26/255 grey** without a Background (X3D's default is black), and an Inline wrapper around a file loses that file's Viewpoint in castle-model-viewer 5.3.0. Write an explicit Background. | C | Demo 60 raw frames; wrapper test |
| 11 | **Exposure for a baked room:** the bake recipe's 70th-percentile rule blew out a slot-lit room; the 99.5th percentile mapped to 2.6 worked. Outward faces gather outside light unless faces are oriented into the room; per-corner noise needs 384 spp plus facing-aware smoothing. | C | Demo 58 bake-stats.json |
| 12 | **H-Anim names:** the add-on's name table uses the H-Anim 1.x names `ankle` and `wrist`; x3d_mcp's semantic check wants the 2.0 names `talocrural` and `radiocarpal`. Per-bone `x3d_hanim_joint` overrides work (with a misleading "not an H-Anim 2.0 joint name" diagnostic). | C | Demo 61: 4 warnings → 0 |
| 13 | **Metadata placement:** `x3d_metadata` lands on the Shape, not the Transform, and elements that share a Blender material share one Appearance through DEF/USE. To highlight one element in the browser, give it its own material copy through SAI. | C | Demo 61 page |
| 14 | **ifcopenshell's `unit.assign_unit()` defaults to millimetres:** extrusions in metres came out 3.2 mm tall. Assign SI metres explicitly. Model steel members as `IfcIShapeProfileDef`, not boxes (a solid box made the ridge beam 5.5 t; the IPE 300 is 472 kg). | C | Demo 61 elements.json |
| 15 | **Leak sweeps of .blend files** must decompress zstd with `read_across_frames=True`; `grep -I` skips binaries silently. | C | re-sweep of all 12 demo .blend files, clean |

## 2. What this does not prove

* No real GPU, no phone, no Unreal, Unity or Godot leg. Software-GL frame rates are not quoted.
* Demo 61 carbon factors are illustrative, not from a certified EPD or checked against a database.
* Demo 60 X3DOM cause is isolated to PhysicalMaterial vs Material only; which part of X3DOM's PBR path saturates is not traced (S).

## 3. Candidate add-on fixes (not made yet)

1. Add the H-Anim 2.0 joint names (`talocrural`, `radiocarpal`, …) to `hanim_names.STANDARD_JOINTS` and map `foot`/`hand` to them.
2. Normalise the camera rotation axis (exported with length 1.000046 in Demo 58).
3. Document in the export panel that `x3d_intensity` is a marker and `x3d_energy_per_intensity` sets the value.

## Links

* Baked Light Gallery: https://hagopjay.github.io/x3d.demo/demos/blender-baked-light/v1/
* Flywheel Forge: https://hagopjay.github.io/x3d.demo/demos/blender-flywheel-forge/v1/
* One Asset, Every Engine: https://hagopjay.github.io/x3d.demo/demos/blender-every-engine/v1/
* The Walking Twin: https://hagopjay.github.io/x3d.demo/demos/blender-walking-twin/v1/
* Add-on: https://github.com/hagopjay/x3d-blender-io
* Loom copy of these notes: `LEARNINGS-blender-four-demos.md` in x3d.loom

## Demos 63 and 64: the Giza H-Anim pair (19 Nov 2026)

* **Giza Crawl** (Demo 63). An H-Anim explorer walks, stoops, crawls and climbs through the Great Pyramid, the Subterranean Chamber and the Osiris Shaft, then into an imagined Hall of Records, in 28 graded chapters. https://hagopjay.github.io/x3d.demo/demos/blender-giza-crawl/v1/
* **Giza Fall** (Demo 64). A Bullet ragdoll is shoved off the summit. It is baked to H-Anim joints, followed by a tracking camera, and each of its 197 impacts plays a sound. https://hagopjay.github.io/x3d.demo/demos/blender-giza-fall/v1/

What the next build should know (C = Confirmed, L = Likely). Validator: x3d_mcp 39c6e94. Rig: headless Chromium 157 with SwiftShader and X_ITE 16.7.1.

1. **Moving a figure.** x3d-blender-io 8310e7b drops an armature object's own keyframes (C). Parent the armature to an animated Empty, and keep long travel off `humanoid_root`, or X_ITE loses the skinned mesh (L).
2. **Jumping in time.** The X_ITE SAI browser has no `currentTime`; use `Date.now()/1000` (C). To jump, disable the TimeSensor, wait, re-enable it and set `startTime` (C).
3. **Checking the rig.** Check a rig's sign conventions with a rendered side view. In headless bpy that means Cycles, because Workbench needs a GPU (C).
4. **Background.** A generated scene gets no X3D Background from the add-on. Insert the sky in the generator (C).
5. **Impact sounds.** Mass × |Δv − gΔt| per body per frame is enough to drive impact sounds with no physics callbacks (C).

Loom copy: `LEARNINGS-blender-giza-demos.md` in x3d.loom.

## Demo 65: Great Pyramid Numbers (19 Nov 2026)

* **Live:** https://hagopjay.github.io/x3d.demo/demos/blender-giza-numbers/v1/ . The page tests π, τ, φ and the 29.9792458° latitude against Dash 2015, Petrie, Cole and AERA, digit by digit, with error bars. The graded receipt (`claims.json`, 27 claims) drives both the page and the Blender scene.
* **Method:** for every match, show the digits that agree next to the digits the survey can support. Count the latitude lines that cross a building (about 20,800 at 1e-7° here) before calling a location precise.
* **X3D:** x3d_mcp's semantic check rejects a MetadataSet name with a space (C). Transform `visible` through SAI toggles overlay groups in X_ITE 16.7.1 (C).

Loom copy: `LEARNINGS-giza-numbers.md` in x3d.loom.

## Demo 65 v2 and v3: Pyramid Observatory and The Reveal (19 Nov 2026)

- **v2** is the owner's outside review build, kept as delivered: 16 findings, analytic instruments, and a start-up that waits for X_ITE.
- **v3** adds:
  - **The Reveal:** five acts, each shown first in a Wonder lens, then in a Test lens with literal digit colouring and a grade stamp.
  - **Coincidence Engine:** 254 numbers per pyramid checked against 16 constants. At 4 digits, chance predicts 0.70 matches per pyramid. Results: Khufu 1, Khafre 2, Menkaure 3, Red 0, Louvre 1.
  - **Eclipse sky:** a panel of the eclipse sky.
  - **Blender round-trip witness:** a census of what the scene keeps and what it loses.
- **Round trip, Confirmed:**
  - Geometry, cameras, lights and textures survive.
  - Switches, Groups, WorldInfo and TextureTransform are lost.
  - Text comes back as meshes.
  - DEF names come back with an `OB_` prefix.
  - The returned file is XSD valid with 0/0 (x3d_mcp 39c6e94).
- **Importer warning fix:** the false "indexed up to … padding" warnings are fixed in x3d-blender-io #69.
- Full rules are in x3d.loom `LEARNINGS-giza-numbers-v3.md`.

## Demo 65 v4: the Sacred Geometry Atlas (19 Nov 2026)

- **Live:** https://hagopjay.github.io/x3d.demo/demos/blender-giza-numbers/v4/ . A Cycles-baked plateau in two lights (golden hour, moonlit night) under 52,602 HYG stars drawn as X3D 4.1 Gaussian splats with 3,547 labels, plus 63 sacred-geometry claims, each graded twice and each with a 3D proof.
- **Two grades per claim:** the number (Confirmed 30, Likely 22, Suspected 5, False 5, Untested 1) and the design (Designed 11, Possible 15, Coincidence 29, Unknown 8).
- **Sky in its own layer, Confirmed (X_ITE 16.7.1):**
  - Layer 0 holds the stars in light-years; layer 1 holds the scene in metres. The page copies the scene camera's orientation to the sky camera each frame.
  - A GaussianSplats node under a Transform scale of 300 or more crashed the page; scale 30 and 1 work.
  - Every GaussianSplats node needs `bboxCenter` and `bboxSize` (Loom trap `splat-bbox`).
  - A viewpoint made through the SAI is not used until `set_bind = true`.
- **Bake, Confirmed:**
  - Ground as a 4096² lightmap on an `ElevationGrid`; pyramids as one baked colour per face.
  - Welding the add-on's export and sharing `Coordinate` between day and night took two 5.4 MB files to one 2.33 MB file.
  - `UnlitMaterial` needs `<component name='Shape' level='1'/>` under Immersive and Interchange: XSD-valid, semantic error without it (x3d_mcp 39c6e94).
  - A camera facing due south is a half turn: take the axis from the quaternion, not from the matrix's antisymmetric part.
- **Sky findings:** the four shafts fit their stars in four different years (2492, 2357, 2359, 2383 BC); Thuban was 1.34° from the pole in 2560 BC; Herschel's passage star fits 2185 BC, not the building date; Kochab stood over Mizar in 2465 BC (Spence gave 2467 BC).
- **Gates:** XSD valid (4.0 and 4.1), 0 semantic errors and warnings, Loom traps and page traps 0, unit tests 8 of 8, rig console clean at 1366 px and 390 px. Not checked: a real GPU, a real phone, Firefox, Safari.
- **Credit:** HYG Database v4.1 by David Nash, CC BY-SA 4.0.
- Full rules are in x3d.loom `LEARNINGS-giza-atlas-v4.md`.
