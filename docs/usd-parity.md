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
| **X3D can state it, and its validator reports it** (each with a scene it must flag and a scene it must pass) | **66 of the 340 rules** (the 66 the project judged X3D can state; the project classified the other 274) |
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

Turn 4b, the rules on a new stack (x3d.downey, 20 scenes: one true defect, seven false alarms fixed): [downey-rules-test.md](downey-rules-test.md).

## The SimReady profile: 66 becomes 66 plus 20 (27 Nov 2026)

The table above files 92 SimReady rules as "a pipeline or profile convention". Twenty of them needed only one thing: a place in an X3D file to write the fact. The X3D SimReady profile (draft 2) gives each a place, x3d_mcp checks it, and NVIDIA's own validator confirms the check on the converted file.

- **Checks:** x3d_mcp `src/validation/simready_checks.py` (PR 40). **Crossing and receipts:** x3d.nVidia `q12/profile_crossing.py`, `docs/SIMREADY-X3D-PROFILE.md` (PR 4).
- **Failure modes:** 497 to 504 (x3d.loom `LEARNINGS-simready-profile.md`).

| | Rules | Source |
|---|---|---|
| Stated by plain X3D and checked | 66 of 340 | unchanged |
| Open in plain X3D, closed by the opt-in profile, checked | 20 | new ledger status `profile` |
| **Stated and checked in all** | **86 of 340** | always quoted as 66 plus 20 |
| Still a pipeline or profile convention | 71 | mate, connection, gripper, packaging and AIF equipment profiles |
| Profile rules confirmed both ways by NVIDIA's validator | 19 of 20 | usd-validation-nvidia 1.23.0, SimReady tiers c3bd1d8, usd-core 26.11, Python 3.12.3 |
| Profile rules with no executable NVIDIA rule | 1 (VG.021, triangulated meshes) | X3D-only |

### Where an X3D file writes each fact

| Fact SimReady asks for | In the X3D file | SimReady rules |
|---|---|---|
| Author, licence, category, Wikidata Q-code | `<meta name="creator">`, `<meta name="license">`, `<meta name="simready:category">`, `<meta name="simready:qcode">` | SR.003, SR.004 |
| Thumbnail | `<meta name="Image" content="picture.png"/>` | SR.002 |
| Metres | no `<unit category="length">`, or a factor of 1 | UN.007 |
| Meshes, triangulated | `IndexedFaceSet` or `IndexedTriangleSet`, not `Box` or `Sphere` | VG.MESH.001, VG.021 |
| At least one moving body, or two | `<meta name="simready:features" content="rigid_bodies multibody"/>` and `RigidBody` nodes | RB.001, RB.MB.001 |
| Every shape and material labelled | a `MetadataSet name="semantics:labels"` holding one `MetadataString` per taxonomy | SL.001, SL.003, SL.QCODE.001, SL.MAT.001 |
| Labels from a closed vocabulary | the `MetadataString` is named `coco`, `cityscapes`, `ade20k`, `pascal_voc`, `sunrgbd`, `imagenet_1k`, `affordance` or `affordance_state` | COCO.001, CITY.001, ADE.001, VOC.001, SUN.001, IN1K.001, AFF.001, AFF.002 |

### How to read it

- **The profile is opt-in.** A file is judged only when its head carries a `simready:` meta element. A plain X3D file in centimetres, built of Spheres, with no licence is still valid X3D and is never reported. That is why the 20 are counted apart: they are not mistakes in X3D.
- **"Confirmed both ways" fills four cells.** For each rule, the X3D check reports the failing scene and SimReady fails its USD; the X3D check passes the passing scene and SimReady passes its USD. The USD is written by `x3d2usdphysics` with nothing repaired.
- **The crossing found a real defect in our own writer.** It wrote `metersPerUnit = 1` for every scene, so a centimetre X3D file became a metre USD stage and passed UN.007. It now carries the unit as declared.
- **Three rules were left out on purpose.** SR.001 and NP.006 ask for fields the writer authors itself, so no X3D file can fail them. NP.001 fails the prim names `World` and `Looks` on a passing scene (7 failures, measured), so no writer following the usual USD layout can meet it.
- **One pair per rule is a small sample.** The next test is both validators over real files that opt in.
- **Third-party lists.** The eight label vocabularies (1,314 names, no images) come from NVIDIA/simready-foundation c3bd1d8 (Apache-2.0) and the public datasets it names: [ADE20K](https://ade20k.csail.mit.edu/), [Cityscapes](https://www.cityscapes-dataset.com/), [COCO](https://cocodataset.org/), [ImageNet](https://www.image-net.org/), [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/), [SUN RGB-D](https://rgbd.cs.princeton.edu/). A rights holder who wants a list removed can open an issue on x3d_mcp and it is taken out at once.


## Real assets: 0 of 27 as authored, 13 of 27 after the opt-in upgrade (28 Nov 2026)

The test the section above asked for. 27 real X3D physics scenes, the marble-machine scenes of x3d.loom `x3d.physics/physx-bridge/scenes`, were written to USD and judged by NVIDIA's validator against NVIDIA's own **Robotics-Prop 5.0.0** profile, first untouched and then after an opt-in upgrade.

| Measure | Count |
|---|---|
| Pass as authored | 0 of 27 |
| Pass after the upgrade | 13 of 27 (13 of the 18 with a body that can move) |
| Pass with no warning either | 6 |
| Upgraded copies valid against the X3D 4.0 XSD | 27 of 27 |
| x3d_mcp's profile checks agree with the validator on the untouched files | 157 of 162 scene-by-rule cells |

Instruments: usd-validation-nvidia 1.23.0, usd-core 26.11, SimReady tiers from NVIDIA/simready-foundation c3bd1d8, Python 3.12. Robotics-Prop 5.0.0 requires 47 requirements, 38 of them with a rule that can be run; the other 9 are not counted as passed. Pass is NVIDIA's own package-sample rule: no ERROR or FAILURE on a required requirement.

**How to read it.**

- As authored, only six required rules fail: provenance, thumbnail, the two label rules, no mesh, and no moving body. No physics rule fails. The bodies, colliders, masses and joints in the X3D files already satisfy the profile.
- The gap is facts. The upgrade adds a creator, a licence, a category, a Wikidata code, a thumbnail and one material word per look. It writes a copy, changes no shape and no number, and writes nothing for a fact it was not handed.
- The 14 that do not pass each have a stated reason: 9 have nothing that moves, 2 are test fixtures with no honest class code, and 3 draw with looks the facts file cannot name.
- The X3D check predicts NVIDIA's verdict on real files in 157 of 162 cells. Four of the five misses have one cause: the writer exports only what takes part in physics, so a shape that is only drawn is judged by one side and never seen by the other.

**What the real files taught.** Rewriting each Box as a mesh inside the X3D made ten dominoes vanish from view in X_ITE 16.8.0 within 2.5 seconds, so the X3D keeps its Boxes and the USD writer emits the exact twelve-triangle mesh. Spheres and cylinders stay as they are, because a faceted marble does not roll like a marble, and the validator's warning about them is left standing.

**Limits.** One corpus from one generator. No engine was run: a pass says the asset is well formed, not that it simulates well. Every fact graded likely or suggested in the sidecar (the creator name, 21 material words, the class chosen per scene) is waiting for the owner's review.

**Attribution.** Scenes: [hagopjay/x3d.loom, x3d.physics/physx-bridge](https://github.com/hagopjay/x3d.loom/tree/main/x3d.physics/physx-bridge), Apache-2.0. Class codes: [Wikidata](https://www.wikidata.org/) (CC0) through [QLever](https://qlever.dev/). Profile and rules: [NVIDIA/simready-foundation](https://github.com/NVIDIA/simready-foundation) c3bd1d8. If anything here is yours and should not be, open an issue on the repository and it will be taken down promptly.

Harness, facts, copies and receipt: x3d.nVidia `q12/real-assets/` and `q12/receipts/real-assets-20261128.json` (PR 5). Failure modes 538 to 543.
