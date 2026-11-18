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
