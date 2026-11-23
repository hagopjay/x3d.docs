# The render oracle: do six engines draw the same X3D scene? (step 1, three engines)

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
