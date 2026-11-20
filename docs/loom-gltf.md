# The Loom for glTF 2.0

The x3d.loom method (gate, render in N engines, score against a reference, receipt) now runs on glTF 2.0 too. Code and full spec: hagopjay/x3d.loom `formats/gltf/` (`SPEC.md`). Learnings: x3d.loom `LEARNINGS-loom-gltf.md`.

| Stage | glTF tool |
|---|---|
| Corpus | Khronos glTF-Sample-Assets, 7 assets pinned by commit + sha256 |
| Gate | Khronos glTF-Validator 2.0.0-dev.3.10 |
| Harness | one camera + one 2.5 lux KHR_lights_punctual sun, no IBL, no tone map, clear #20242c |
| Reference | Khronos glTF Sample Renderer 1.1.0, Blender Cycles 5.3.0 as a second witness |
| Engines | three r187, Babylon 9.32.0, X_ITE 16.7.1 (via X3D Inline); x3d.wgpu listed, not run yet |
| Score | PSNR, SSIM, silhouette IoU after matching the display encode; candidates also scored against each other |
| Semantic | X3D Metadata, IFC, CIDOC-CRM, PROV-O → KHR_xmp_json_ld → X3D, rules S0-S7 |
| Receipt | `loom.render-receipt/1`, same `gpu` and `api_validation` blocks as x3d.wgpu |

First run (Chromium 157 on SwiftShader, no GPU): 28 scored runs, 17 pass, 5 warn, 6 fail; X_ITE closest to the Khronos reference. The Walking Twin's 24 IFC ids and the Giza twin's 9 CIDOC-CRM references round-trip with no loss.

Where "correct" is pinned: glTF defines only its BRDF (Appendix B). Lights, ambient, view and display encode are pinned by the Loom's harness and named in every receipt. X3D stays the reference format because its ISO text defines the whole picture.
