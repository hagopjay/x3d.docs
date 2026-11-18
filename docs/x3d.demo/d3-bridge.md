# D3 to X3D Bridge (sixteen D3Blocks ideas in true 3D)

Demo folder `docs/demos/d3-bridge/v1/` in x3d.demo (PR #85; number from the bridge thread). Lesson table: x3d.loom `LEARNINGS-d3-bridge.md`. Reusable emitter: x3d.loom `kit/d3-x3d/`.

**What it shows.** D3 computes the layout, X3D carries the scene. Heatmap becomes a heat terrain, Chord a dome of arches, Treemap a terraced city, MovingBubbles a space-time cube, D3graph a d3-force-3d graph, Sankey a canyon with depth lanes, Scatter a 3D cloud with its three 2D projections on the walls, Timeseries a ridgeline wall, Elasticgraph a live force graph driven through the SAI, CirclePacking tiers of spheres, Violin solids of revolution, ImageSlider a flat-to-relief morph, RadialGraph the X3D 4.0 type hierarchy on a sphere, Tree a cone tree, Maps a globe above its Equal Earth projection, and Particles a word with real thickness. All data comes from the x3d.* repositories themselves.

| Check | Result | Instrument |
|---|---|---|
| Scenes valid | 16 of 16 | x3d_mcp `fa5dccf` `validate_xml`, XSD 4.0, lxml 6.1.3 |
| Scenes load | 16 of 16, 0 console errors | X_ITE 16.6.0, headless Chromium, SwiftShader (no GPU) |
| Live D3 to X3D | 129 force ticks in 8 s, Transform equals simulation position x scale | same run |
| Layout libraries | D3 7.9.0, d3-force-3d 3.0.6, d3-sankey 0.12.3, world-atlas 2.0.2 | `manifest.json` |

**Three things to remember.** Keep the flat D3 chart as one Viewpoint, so 3D only adds. Spend the third axis on what 2D hides: crossings, overplotting, time, breadth, a real third variable. Name Transforms and Coordinates (DEF) so a live D3 simulation can write them through the SAI each tick.

**Open.** No GPU, phone or headset run. Labels overlap in dense charts. Relief colours read darker than the photo under PBR.

## v2 (18 Nov 2026)

Folder `docs/demos/d3-bridge/v2/` (x3d.demo PR #91); lessons in x3d.loom `LEARNINGS-d3-bridge-v2.md`. There are five interactive flagships:
- the living graph, which grows demo by demo through time;
- the clickable chord dome, with flow beads;
- the sankey canyon, with pulses and a 5-stop tour;
- the project globe, with arcs from Blacksburg to the twin sites;
- the space-time cube, sliced by a moving ClipPlane slab.

Build-time label declutter runs on all 16 scenes.

| Check | Result | Instrument |
|---|---|---|
| Scenes valid | 16 of 16 | x3d_mcp `fa5dccf` `validate_xml`, XSD 4.0 |
| Scenes load | 16 of 16, 0 console errors | X_ITE 16.6.0, headless Chromium, SwiftShader |
| Living graph | 144/144 nodes, 757 edges at the last demo | page API |
| Chord isolate | 1 of 91 opaque, restore 91 of 91 | page API |
| Label overlaps at default view | type sphere 73 → 0, sankey 19 → 0 | build-time projection |

**Remember.** A ClipPlane animates with no script when it rides a Transform while the content counter-moves. **Open.** Relief colour is still desaturated under PBR, and there is no GPU run.

## v2.1 and v2.2: an honest receipt

- **v2.1** (`docs/demos/d3-bridge/v2.1/`) fixed three review findings. The validator now fails loudly (exit 1 on an error, exit 2 on an empty set). Every scene declares Rendering level 5 for ClipPlane. The page no longer throws without WebGL.
- **v2.2** (`docs/demos/d3-bridge/v2.2/`) cleans the scene files. A DEF is kept only when the file USEs it, a ROUTE names it, or the page reaches it by SAI. Names the page addresses are declared with `<EXPORT>`. A label's hidden LOD level is a `WorldInfo`, not an empty `Group`.
- **Result** (x3d_mcp `semantic_diagnostics`, fa5dccf): v2.1 had 64 warnings and 1,305 info notes, and v2.2 has 0 and 0. 16 of 16 scenes still load with 0 console errors (headless Chromium, SwiftShader, X_ITE 16.6.0).

**Remember.** A receipt that lumps the checker's grades together overstates the problem. Report errors, warnings and info separately. The reusable pass is in x3d.loom `kit/d3-x3d/hygiene.mjs`.
