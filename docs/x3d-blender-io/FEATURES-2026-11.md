# x3d-blender-io: interaction, instancing, HAnim names, splats and capture (18 Nov 2026)

Everything below is in x3d-blender-io PR #46 (branch `claude/project-thread-eqjqvi`). Tested on the `bpy` 5.2.4 wheel (headless), CPython 3.11. Browser checks: X_ITE 16.7.1, headless Chromium, SwiftShader (no frame-rate claims). Grades: Confirmed = a named tool ran, Suspected = not verified.

| Feature | How you author it in Blender | What comes out | Demo | Grade |
|---|---|---|---|---|
| **ROUTE interaction** | Custom properties `x3d_trigger` (touch or proximity), `x3d_action`, `x3d_target`, `x3d_radius`; panel *Object > X3D Interaction* | TouchSensor / ProximitySensor, TimeSensor, interpolators and ROUTEs in pure X3D, no Script | x3d.demo `blender-route/v1` | Confirmed (picking and door verified in X_ITE; proximity during a live tour Suspected) |
| **Camera tour** | `x3d_tour_order`, `x3d_tour_dwell`, `x3d_tour_travel`, `x3d_tour_loop`, `x3d_tour_autostart` | Viewpoint animation timeline | same demo | Confirmed |
| **Collection instances** | Linked duplicates and collection instances | `Group DEF` once, `USE` per instance | x3d.demo `blender-instancing/v1` (sizes in `receipts/sizes.json`) | Confirmed |
| **HAnim joint names** | Armature property `x3d_hanim_names = "standard"` (opt-in) | HAnimJoint names mapped to the standard set | none | Confirmed (opt-in because default renaming broke conformance Z14) |
| **Splat glb** | Object property `x3d_splat_glb` | KHR_gaussian_splatting `.glb` plus an `Inline` | none yet | Confirmed (7 tests; renders in X_ITE with prefixed SH names) |
| **Splat training views** | `python tools/splat_capture.py <out> --views 48` | Fibonacci-sphere renders, `transforms_train/test.json`, `points3d.ply` | none | Confirmed (smoke run, 5 tests); no trainer has consumed them (Suspected) |

## Traps worth knowing

1. A play-once `TimeSensor` with `startTime=0` fires at load; the exporter writes `startTime="1e+30"`.
2. X_ITE picking needs `x_ite.css` loaded.
3. `matrix_world` is stale for objects outside a view layer; the extractor uses `matrix_basis` and `matrix_parent_inverse`.
4. Splat spherical-harmonic attributes must carry the `KHR_gaussian_splatting:` prefix.

## Acceptance gates

`x3d.loom` PR #123 adds profile `x3d-blender-fidelity/v1`: zero vertex loss, mean delta-E 2000 below 2.0, SSIM above 0.95. No comparator exists yet, so nothing can be accepted under it until one is built.
