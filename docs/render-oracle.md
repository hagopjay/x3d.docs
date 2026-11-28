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

## Step 4 (24 Nov): the three.js PhysicalMaterial, second pass

The step 2 fix curved only the environment light and failed under a direct light. Twelve one-light probes (base 0.5, metallic 0/1, roughness 1/0.5/0.2, intensity 1/2) showed X_ITE, x3d.wgpu, Blender and Castle agreeing within 5, with three.js alone off. The fit: X_ITE reads 255 x (0.5 x I / PI)^(1/2.2), so a PhysicalMaterial's light is not multiplied by PI and the whole result goes through a 1/2.2 power (Confirmed on the probes).

| three.js vs X_ITE | before | after |
|---|---|---|
| furnace 29 (AGREE/NEAR/FAR) | 19 / 9 / 1 | 20 / 9 / 0, held-out 29 of 29 |
| lit 12 | 8 / 1 / 3 | 8 / 2 / 2 |
| `lit_physical_direct` | 24.9 FAR | 4.9 NEAR |
| PhysicalMaterial fixture mad | 5.33 | 0.5 |

Lesson: a fit on one scene family is a hypothesis, not a fix; four engines agreeing is a specification. Open: rough metals (three.js 80 vs X_ITE 59, Suspected multiple scattering). Source: x3d.loom PR #180.

## Steps 5 to 8 (24 Nov): the engines caught up

The oracle's list of faults was worked down in the bridges and renderers we own, one cause at a time (source: x3d.loom README Results 9 to 13, PRs #180 to #188, x3d.wgpu #9).

| engine | fault found | cause | before then after, vs X_ITE 16.6.0 |
|---|---|---|---|
| three.js | PhysicalMaterial wrong under a light | X_ITE has no PI factor on PhysicalMaterial light and curves the whole output by 1/2.2 | furnace 29 FAR 1 to 0, `lit_physical_direct` 24.9 to 4.9 |
| three.js | ambient and attenuation | material ambientIntensity fixed at 0.2; only one attenuation term kept | `lit_emissive_ambient` 15.9 to 0.25, `lit_point_attenuation` 10.4 to 0.4 |
| Babylon | PBR black (metals under EnvironmentLight and PBR under a direct light were one bug) | PBR winding wrong on Babylon's own primitives | `lit_physical_direct` 59.5 to 1.5, furnace held-out outside 21 to 2 of 29 |
| Babylon | no fog, no PixelTexture, linear point falloff, UnlitMaterial white | the fog code started only for LocalFog; a texture type never read; the falloff law lives inline in the StandardMaterial shader; the material type was never named | `lit_fog_linear` 71.5 to 3.7, `lit_texture_pixel` 53 to 7.4, `lit_point_attenuation` 30.7 to 1.3, `exp2_a_unlit_default` 127 to 0 |
| x3d.wgpu | no Fog, no PixelTexture, rotated Box texture | missing nodes; an arbitrary axis pair per Box face | `lit_fog_linear` 70.5 to 0.7, `lit_texture_pixel` 82.8 to 0.5 |

End state (AGREE/NEAR/FAR against X_ITE): furnace 29 three.js 20/9/0, x3d.wgpu 10/19/0, Babylon 18/11/0; lit 12 three.js 10/2/0, x3d.wgpu 11/1/0, Babylon 8/4/0; in the majority vote none of the three is the outlier in any scene. Left for other lanes: the Blender importer ignores Background, headlight and EnvironmentLight; Castle's EnvironmentLight level; a Cycles world for the furnace scenes; rough metals (three.js and Babylon 80 to 83 against 59, cause unknown).
