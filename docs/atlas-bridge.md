# The Atlas bridge: an X3D world goes to World Labs Atlas and comes back (23 Nov 2026)

Demo: x3d.demo `docs/demos/atlas-bridge/v1/` (Demo 77). Code: `kit/` and `build/` there.
Fold-back: x3d.loom `LEARNINGS-atlas-bridge.md`, failure modes 229 to 235; the bridge node `x3d.threejs/bridge/src/nodes/GaussianSplats.js`.
Earlier, with no spend: [Marble's successor, Atlas, in X3D](marble-atlas.md) (Demo 76).

## The idea in plain words

Demo 76 showed where each Atlas output belongs in X3D, using made-up data. This one makes the real calls, in both directions.

**Out.** Build a room in X3D from plain boxes, cylinders and a sphere. For every `Viewpoint`, hand Atlas the camera and a depth map: how far the nearest surface is at each pixel. Atlas paints a picture that fits that depth. The room becomes a library or a granite chamber, and the walls stay where the X3D put them.

**Back.** From those pictures (and the X3D's own depth) Atlas builds Gaussian splats, then a mesh and simple collision boxes. All of it is written into one X3D 4.1 file and drawn by the X3D to three.js bridge:

| Atlas sends back | X3D node | Held against the X3D by |
|---|---|---|
| the cameras | `Viewpoint` | comparing with the Viewpoints sent: 0 m, 0 degrees, 36 of 36 |
| its own depth for the pictures | (measured, not stored) | the depth that was sent: within about 1 to 2% |
| splats (SPZ, 2,000,000) | `GaussianSplats` + a `MetadataString` naming the dense file | distance from each splat to the nearest X3D solid: median 37.8 mm |
| mesh (GLB) | `IndexedTriangleSet` + `ImageTexture` | same distance for its vertices: median 43 mm (King's Chamber) |
| collider boxes (GLB) | `Collision` with `Box` proxies | 99.5% of the X3D surface covered, 3.3% of open air wrongly blocked (reading room) |

## Three things X3D gives a generative model

1. **A camera it cannot move.** X3D and Atlas use the same camera axes, and the cameras come back unchanged.
2. **A shape it must respect.** Depth is the contract. The picture can be anything; the geometry is the scene graph's.
3. **Names.** "Repaint the globe" is a mask made from the pixels the nodes called `Globe…` cover. Outside it, 95 to 98% of pixels stay as they were.

## What went wrong on the way (and is now a test)

- The collision boxes in a real file are stored as matrices with their axes shuffled; read the simple way they are wrong.
- X3D never draws a `Collision` proxy, so the boxes looked missing until they got a Group of their own.
- The splat renderer drew everything too dark until it was told how the bridge handles colour (13.3 → 22.2 dB against the source picture).
- A prompt that said "red granite" in passing got yellow limestone. Lead with the material.
- Two paid runs overlapped and one overwrote the other's ledger lines. The ledger now merges and keeps a journal.

## Cost and rights

8,986 credits ($8.99) of a 10,000 cap, 16 paid calls: one refined splat is 5,000 of that. Every call is in the demo's `ledger.json`. The outputs were made on signup credits, so World Labs owns them and licenses personal, non-commercial use; they are shown with credit and a takedown notice. The numbers measure this bridge's round trip, not Atlas.

## Not done

No real GPU was used, so speed is unknown. X_ITE has not drawn the return worlds. The bridge's `Inline` does not read glTF yet, which is why the mesh is converted to X3D triangles.

## Version 2: Blender in the loop (24 Nov 2026)

Demo folder: x3d.demo `docs/demos/atlas-bridge/v2/`. One scene, a vaulted scriptorium, is modelled in Blender 5.3 and exported as X3D by the Blenderizer add-on. Blender then does five jobs. Every number has a receipt in the demo's `receipts/` folder.

| # | Blender's job | What it showed |
|---|---|---|
| 1 | Build the input | Blender cameras and the exported X3D Viewpoints agree to 0.0007 mm. Cycles depth and the X3D depth agree to a median of 0.09 mm. Atlas returned depth within 0.73% of what it was sent. |
| 2 | Clean the result | The 24 Atlas pictures are projected onto the exact Blender geometry and baked into one texture. The result is a valid X3D 4.0 file with straight shelves and a flat floor, 22.9 dB from the pictures it was painted from. |
| 3 | Match colour | One Blender compositor node (ASC CDL) was fitted between the two rings of pictures. It changed little, which is the finding: the v1 gap comes from the generated pictures disagreeing about content, not from exposure. |
| 4 | Judge | The Cycles object-index pass marks every object's outline. Atlas keeps 84.1% of them. |
| 5 | Test the colliders | Balls dropped in Blender's rigid-body engine rest a median 47.5 mm from where they rest in the X3D room; 61 of 323 land 100 mm or more too high. |

The main lesson: when the scene graph already has the geometry, bring home only the paint. The Atlas mesh sits a median 24 mm from the true surface and is wavy; the baked X3D uses the true surface.

What is not done: no refined splat of this scene, no repair of the Atlas mesh, and faces that no Atlas view saw keep their flat Blender colour (the receipt counts them). Book edges show ghosting where two views disagree.

Cost: 1,320 credits in 4 calls for this version. Rights are as in version 1: World Labs credit, personal non-commercial use, takedown notice.
