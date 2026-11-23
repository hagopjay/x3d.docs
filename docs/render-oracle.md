# The render oracle: do six engines draw the same X3D scene?

**The idea.** Draw the same scene in several engines with one fixed camera, subtract the pictures, and list where they disagree. A disagreement is evidence that one engine departs from the standard. The tool is checked first by planting defects it must catch.

**Step 1 (23 Nov 2026), 29 conformance scenes, three engines** (X_ITE 16.6.0, the three.js bridge on three r187, x3d.wgpu 0.5.1; 128x128, Chromium 157.0.8103.78 / SwiftShader, software only):

| pair | AGREE | NEAR | FAR |
|---|--:|--:|--:|
| X_ITE vs x3d.wgpu | 10 | 19 | 0 |
| X_ITE vs three.js bridge | 2 | 6 | 21 |
| three.js bridge vs x3d.wgpu | 8 | 0 | 21 |

* The five largest gaps are one cause (Likely): the three.js bridge draws nothing for `EnvironmentLight`, so sphere pixels are 0 where X_ITE and wgpu give 137 to 255.
* An older X_ITE 16.7.1 record, used as a held-out judge, agrees: X_ITE and wgpu 29/29 in tolerance, three.js 8/29.
* Planted defects (brightness, shifts, radius, sphere to box) were caught in every observable case; a 10% gain error and a flipped sphere were **not**, because these scenes are uniform spheres. The 29 scenes make only 10 distinct pictures, so step 2 needs richer scenes.

Code, pictures and the full matrix: `hagopjay/x3d.loom` `x3d.render-oracle/` and `LEARNINGS-render-oracle.md`. Grades: the numbers are Confirmed (measured); the cause is Likely.

## Step 2 (same day): the fix, then six engines

His order was to fix the three.js bridge first. It now draws `EnvironmentLight` and curves the indirect light the way X_ITE does, which took X_ITE vs three.js from 21 FAR scenes to 1. Then Babylon, Blender and Castle were added on the same 29 scenes and the same 128x128 rig:

| engine vs X_ITE | AGREE | NEAR | FAR | held-out rows in tolerance |
|---|--:|--:|--:|--:|
| x3d.wgpu | 10 | 19 | 0 | 29 / 29 |
| three.js bridge | 19 | 9 | 1 | 28 / 29 |
| Castle | 2 | 7 | 20 | 11 / 29 |
| Blender importer + Cycles | 6 | 9 | 14 | 9 / 29 |
| Babylon bridge | 2 | 13 | 14 | 8 / 29 |

* Blender's importer ignores `Background` and `EnvironmentLight` (Likely); Babylon draws metals black under an `EnvironmentLight` (cause Suspected); Castle draws the environment at the wrong level (255 expected, 147 drawn).
* Five of six engines read 186 to 188 on a headlit PhysicalMaterial; three.js reads 128. Majority vote points at the odd one.
* Castle's numbers come from today's snapshot (sha256 `dce6a4cd...`), not the build pinned earlier, because the snapshot URL is moving.
* All software rendering; the scenes are furnace probes, so lit, coloured, asymmetric scenes are the next step.

## Step 3: twelve lit scenes, a second judge, a vote

The furnace scenes could only test one behaviour, so twelve lit, coloured, asymmetric scenes were added (directional, spot and point light, specular, emissive and ambient, transparency, a texture, a metal under one light, fog, nested transforms, a default headlight). Six engines, same rig.

| engine vs X_ITE (12 scenes) | AGREE | NEAR | FAR |
|---|--:|--:|--:|
| x3d.wgpu | 9 | 1 | 2 |
| three.js bridge | 8 | 1 | 3 |
| Babylon bridge | 6 | 2 | 4 |
| Castle | 1 | 7 | 4 |
| Blender importer | 0 | 3 | 9 |

* **Controls:** 24 of 24 planted scene mutants (light flipped, colour changed, shininess changed, taller cone) were caught across all six engines.
* **New gaps:** x3d.wgpu draws no PixelTexture colours and no linear fog (Babylon and Blender draw no fog either); Babylon draws a PhysicalMaterial under a DirectionalLight black; three.js lights it wrongly (hot sphere, dark box); the Blender importer draws no default headlight and no sky.
* **No external record exists for these scenes**, so the earlier held-out check is gone. A majority vote and FLIP (a second image metric, agreeing 0.92 on rank with the first) are consistency checks only; where every pair disagrees (fog, texture) the vote names no outlier.
