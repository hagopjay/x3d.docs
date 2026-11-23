# A scale ladder in X3D: one room per power of ten (23 Nov 2026)

How to carry a reader from metres to nanometres in the browser without losing depth precision or losing track of
what is measured. Worked out on a private eleven-room atlas; the notes and grades are in x3d.loom
`LEARNINGS-scale-ladder-atlas.md`.

Instruments: Blender 5.3.0 `bpy` wheel, x3d-blender-io 2.7.2 at `903c1e5`, x3d_mcp fork validator at `4d433af`,
X_ITE 16.7.0 in headless Chromium with SwiftShader. Grades: Confirmed (a named tool ran), Likely, Suspected.

## The pattern

1. **Build every rung near 1 m.** Give each rung its own Blender collection and its own X3D file. Store the real
   window size and the magnification as data beside the file. Confirmed: eleven rooms from 4.37 m to 3.2 nm all draw
   with ordinary near and far planes.
2. **Put the next rung's window in the scene.** A thin gold frame the size of the next room's field of view shows the
   ratio and gives a camera somewhere to fly.
3. **Export one collection per file with a receipt.** `bpy.ops.export_scene.x3d(use_selection=True,
   use_receipt=True, x3d_version='X3D40')`. Read the receipt before looking at a frame.
4. **Set light strength in the generator.** A light made in Blender leaves capped at intensity 1, and X_ITE divides a
   PhysicalMaterial's diffuse light by π. Put `x3d_intensity` and `x3d_energy_per_intensity` on each light so the
   export writes the value you mean. Area lights leave as directional lights: a flat surface lit only at a raking
   angle needs a second light from above.
5. **Gate, then look.** Validate every file, then load each one in X_ITE and take a still at every Viewpoint. On
   software GL allow four minutes per still.
6. **Label the register in the data.** Each room says whether it is built from evidence or made as art, and each
   claim carries its grade and its source row. The page reads the same list the generator reads.

## Numbers from the first build

| Measure | Value | Grade |
|---|---|---|
| Rooms exported and valid X3D 4.0 | 11 of 11, 0 errors | Confirmed |
| Objects dropped by the exporter | 0 | Confirmed |
| Lights approximated (area to directional) | 23 | Confirmed |
| Light intensities clamped to 1 | 23 | Confirmed |
| Rooms that drew near black before the light patch | 11 of 11 | Confirmed |
| Largest room on the page | 8.1 MB (635 fibres as tubes) | Confirmed |
| Frame rate | not measured (no GPU) | n/a |
