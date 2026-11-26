# X3D answers the USD rulebooks (26 Nov 2026)

The Fault Court's turn 2 matched X3D's validator to the Khronos glTF-Validator. Turn 3 does the same for USD, the format NVIDIA's Omniverse and Isaac Sim judge assets in. The question: **of every mistake USD's checkers catch, which can an X3D file make, and does X3D's validator catch those?**

- **Kit and tests:** x3d_mcp `tests/usd_parity.py`. The table it generates is `docs/USD-VALIDATION-PARITY.md`.
- **Ledger and learnings:** x3d.loom `flywheel/LEDGER.md` (turn 3) and `LEARNINGS-flywheel-turn-3.md`.
- **Failure modes:** 364 to 373.

## The rulebooks

| Rulebook | Who | Rules |
|---|---|---|
| OpenUSD validators (usd-core 26.11) | Pixar, the USD library itself | 30 |
| Omniverse Asset Validator 1.18.0 | NVIDIA, the checker inside Omniverse | 40 |
| SimReady Foundation (23 Nov 2026) | NVIDIA, the requirements Isaac Sim validates robot and prop assets against | 270 |

## The answer

| What X3D does with the mistake | Rules |
|---|---|
| **X3D can state it, and its validator reports it** (each with a scene it must flag and a scene it must pass) | **66 of 66** |
| X3D's standard makes the mistake impossible (one root, +Y up, metres, seconds, normals computed when absent) | 32 |
| SimReady fixes it differently (Z up); the exporter converts, and Blender's USD export already writes Z up | 1 |
| USD machinery X3D does not have (layers, variants, API schemas, subsets, packages) | 50 |
| A USD or Omniverse feature X3D 4.0 lacks (MDL and MaterialX materials, texture colour space, articulations, lidar, render products) | 38 |
| One simulator's runtime schema (PhysX, Newton, MuJoCo, Isaac Sim) | 44 |
| A pipeline or profile convention (names, folders, thumbnails, required metadata, label vocabularies) | 92 |
| Needs a person or a render (tessellation density, pivot placement) | 17 |
| **Total** | **340** |

## How to read it

- **The 66 is the score.** Where an X3D file can be wrong in a way USD's checkers would catch, X3D's validator now catches it too:
  - meshes that are not manifold;
  - faces with no area;
  - normals turned against the winding;
  - unused and duplicated points;
  - coordinates too far out for 32-bit floats;
  - two shapes in the same place;
  - rigid bodies with impossible inertia;
  - a body simulated twice;
  - joint loops;
  - colliders overlapping at rest;
  - textures too large for RTX.

  18 checks were added for this.
- **The 32 are the opposite of a gap.** USD needs rules to make authors declare the up axis, the units and the root. X3D's standard fixes all three, so an X3D file cannot get them wrong.
- **The 92 policy rows are the opening.** They are SimReady's pipeline conventions. An *X3D SimReady profile*, written as metadata conventions and checked by the same validator, would let an X3D scene be judged "SimReady before export". It does not exist yet.
- **The 38 feature rows count against X3D as a language.** Today you cannot write MDL materials, texture colour space or a robot articulation in X3D 4.0.

## Real files first

The new checks were run on 1,548 real X3D scenes from these repositories before they shipped. That run found false alarms the test scenes never showed, and each one was fixed:
- **A Python identity trick** reported a shared collision shape in 9 files that had none.
- **Rules taken from a simulator's profile** flagged legal X3D: a trebuchet's latch, a jelly made of a loop of joints, a pendulum bob with no collider. They became information, naming the simulators that care.
- **A fixed 1 mm precision rule** flagged 40 km terrains; precision is now judged relative to the object's size.
- **Children of LOD and Switch**, which are alternatives, were counted as overlapping shapes.
- **Boxes drawn around tilted dominoes** overlapped when the dominoes did not.

The x3d_mcp test suite went from 1,847 to 1,894 passing tests, with none broken.

**The claim we can make now:** for every mistake an X3D file can make that OpenUSD, the Omniverse Asset Validator or SimReady would catch in USD, X3D's validator reports it, before the file ever reaches Blender or USD. Each turn is a row in the Loom's ledger, rerunnable with one command.

## After Blender: the first end-to-end run (26 Nov)
84 of the parity scenes were imported into Blender 5.3.0, exported to USD, and judged by usd-core 26.11 and the Omniverse Asset Validator 1.18.0 (Python 3.12.3). 70 rules ran; 27 are ones X3D can state.

| Pairs of scene and rule | Count | Meaning |
|---|---|---|
| both quiet | 1,748 | |
| both report a fault | 8 | the X3D check predicted the USD failure |
| X3D only | 17 | Blender's importer repaired the fault, so USD never sees it |
| export-made | 1 | the scene was clean, USD complains anyway |
| to review | 2 | |

Read: for the 17, the X3D validator is the only place the fault shows, which is the case for checking before export. The first 30 USD validators (usd-core) reported nothing on any export, so they say nothing either way. Not covered yet: real files and the SimReady requirement pages. Source: x3d_mcp #33, `docs/USD-BLENDER-JOIN.md`.

Turn 4 (the rulebooks executed after a Blender export, and Newton): [usd-run2-newton.md](usd-run2-newton.md).
