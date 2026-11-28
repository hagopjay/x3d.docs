# Do the Babylon and three.js bridges really map all 260 X3D nodes?

**The question (28 Nov 2026).** The two engine bridges list almost every X3D 4.0 node as done. This audit asks which are *codified* (mapping code plus a test that checks the picture or the value), which are only *carried* (parsed or ignored), and which are missing, in both directions, with the file or test behind every cell.

Rig for every pixel number: 128x128, scene's own Viewpoint, no tone mapping; Chromium 157 to 158 on SwiftShader; X_ITE 16.6.0 as reference; three r187 bridge; Babylon 9.32.0; x3d-view (wgpu) on lavapipe. Judge: object-pixel MAE, AGREE <= 2, NEAR <= 8, FAR > 8. Grades: C measured, L read, S suspected.

| finding | grade |
|---|---|
| Neither bridge writes X3D back: **0 of 260** in the engine-to-X3D direction. Blender writes 100 of 260 (x3d-blender-io #117, Blender 5.3.0) | C |
| Receipt grades, Babylon / three.js: codified 144 / 155, shallow (under 5 checks) 9 / 57, part held 40 / 20, no node test 67 / 24, missing 0 / 4 | C for the recorded numbers, "held" is a keyword match, S |
| three.js: 41 of 55 codified nodes agree with X_ITE on a scene their receipt author did not write | C |
| Babylon: 21 of 57 codified agree, 23 near; 17 of 42 untested nodes far | C |
| 31 nodes ran 2 checks on three.js and up to 93 on Babylon from the same fixture | C |
| Babylon draws Arc2D, Circle2D, Polyline2D, Polypoint2D far from X_ITE (MAE 93 to 123) though receipts pass | C numbers, cause S |
| Babylon ImageTexture, an untested node: MAE 91 of 255 on a 4x4 image, fixed to IoU 0.95 (x3d.loom #258); the same image on a Box is still upside down | C |
| wgpu counts what its loader drops: 98 nodes were dropped silently until the silent-drop fix (x3d.wgpu #10) | C, wgpu thread |

**How it was built.** One minimal scene per node, `x3d.render-oracle/scenes-260/` (255 of 260 valid against x3d-4.0.xsd, 5 blocked by what look like schema defects, held), built from the Blender node board's parent chains so every engine shares one row key. The first batch was half blank in X_ITE and scored AGREE for two blank pictures; the rewrite dropped X_ITE blanks from 77+ to 1 of 122 visible. Two rig faults moved results more than any mapping: scene files the scenes named did not exist, and X_ITE's own "Loading done" toast was drawn into the Babylon runner's reference picture.

**Next.** The Babylon Box texture flip, line and point drawing in Babylon, 3D and cube textures and MultiTexture, the engine-to-X3D exporters, the 14 deferred scenes. Code and data: `hagopjay/x3d.loom` `x3d.render-oracle/`, `LEARNINGS-bridge-audit-260.md`, failure modes 559 to 567 in `LOOM-v1.md`.
