# The USD rulebooks after a Blender export, and Newton as a second physics check (26 Nov 2026)

Turn 3 stated what X3D can say about the USD rulebooks. Turn 4 runs them: real X3D files go through **Blender 5.3.0 to USD** and are judged by all three rulebooks, then physics scenes are checked against a second engine.

- **Code and receipts:** x3d.nVidia `q12/` and `newton/` (PR #3), x3d_mcp `mesh-coincident` world pass (PR #34), x3d.loom ledger turn 4 and failure modes 393 to 406 (PR #221).
- **Instruments:** Blender 5.3.0 (`bpy`), x3d-blender-io 2.7.6, usd-core 26.11, Omniverse Asset Validator 1.18.0 (Python 3.12), usd-validation-nvidia 1.23.0 with the SimReady tiers at c3bd1d8, Newton 1.8.0 (Warp 1.19.0, CPU), MuJoCo 4.0.1.

## Q12 run 2: 141 real files, 359 fired pairs (Confirmed, executed)

| Corpus | Fired | Both | X3D only | USD only |
|---|---|---|---|---|
| Real files (141) | 359 | 140 | 117 | 102 |
| Fixtures (84) | 67 | 17 | 32 | 18 |

| USD-only pairs | Cause | Status |
|---|---|---|
| 38 | PointSet/LineSet exported as 0-face `UsdGeom.Mesh` | export-made |
| 32 | non-manifold vertices (`fall.x3d`: 0 in X3D, 668 after export) | likely export-made |
| 18 | identical shapes in one world place under different Transforms | **x3d_mcp gap, fixed** (scatter.x3d: 495 spheres in 69 groups) |
| 6 / 6 / 2 | zero-length PointSet normals / unused points / extents | export-made or likely |

SimReady **is** executable (165 of 270 pinned requirements have a rule); the first pass had called it unrunnable without looking for the packages (FM 393). Blender's Z-up export passes SimReady's up-axis rule on all 225 exports and the Y-up ones fail on all 225. Blender keeps no X3D physics, so RB.001 fails everywhere; the direct writer `x3d2usdphysics` writes UsdPhysics itself.

## Writer runtime variants: what flipped (Confirmed, 21 PhysX-bridge scenes)

SimReady's isolation matrix forbids engine schemas in the neutral stage, so `--runtimes physx,newton,mujoco` writes each engine's schemas into `runnables/physics/<engine>.usda` behind a variant set.

| Requirement | Neutral writer | Own runtime composition |
|---|---|---|
| RV.001, RV.004, RV.007 | 21 | 0 |
| DJ.002, DJ.004 (PhysX) | 8, 8 | 0, 0 |
| NEWTON.DJ.001, NEWTON.COL.001 | 8, 3 | 0, 0 |
| MUJOCO.COL.001, MUJOCO.DJ.001 | 21, 8 | 0, 0 |
| BA.001 / NEWTON.BA.001 | 8 / 21 | 2 / 15 |
| MUJOCO.COL.002, MUJOCO.DJ.002 | 0, 0 | 3, 8 (new conflicts) |

Nine codes flip; the earlier estimate of 14 was Suspected. **Newton does not use the roots**: with them, `add_usd` still leaves a joint to a static Xform outside every articulation, and the simulations are bit-identical with and without them (FM 406).

## Newton against PhysX's nine exact references (Confirmed, CPU)

| Engine | Passed | Misses |
|---|---|---|
| PhysX | 9/9 | none |
| Newton XPBD | 6/9 | pendulum period 14.5% slow at one 1/240 s step (0.17% at 10 substeps), sliding block creep |
| Newton MuJoCo | 6/9 | one weak bounce (effective e 0.14 against 0.6, Likely), creep, a fast ball through a thin wall |

A 134-domino spiral replays with 0 mismatches on CPython 3.12 and 3.13 for both solvers. Wave speed under a tip: MuJoCo 1.23 to 1.31 sqrt(gH), inside PhysX's range; XPBD 1.54 to 2.31, above real dominoes (Likely).

## Defects found
- **Newton 1.8.0 importer (drafts, not sent):** no filter pair from `FilteredPairsAPI` or a `collisionEnabled=false` joint when one side is static; a joint to a static Xform joins no articulation. Scripts in x3d.nVidia `newton/repros/`.
- **x3d-blender-io (filed):** RigidBody `position` ignored ([#99](https://github.com/hagopjay/x3d-blender-io/issues/99)); a USE'd body imported twice ([#100](https://github.com/hagopjay/x3d-blender-io/issues/100)).

## Not shown
No GPU run; one machine class for the writer measurements; the Foundry's own corpus (an optional third run); SimReady rule review by a person.
