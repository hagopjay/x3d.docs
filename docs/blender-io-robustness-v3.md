# Blender I/O for X3D 4.0: robustness plan v3, in one page (22 Nov 2026)

The add-on's goal is unchanged from v2: mission-critical does not mean nothing is lost, it means **no loss is silent**.
v3 keeps v2's twelve weeks and four gates and changes what the gates measure. Full notes and the probe scripts:
x3d.loom `LEARNINGS-blender-io-robustness-v3.md` and `runs/blender-io-perturb-20261122/`.

Instruments for every measured number here: x3d-blender-io main at `47ed742` (manifest 2.6.5), Blender 5.3.0 `bpy` wheel,
Python 3.13.18, x3d.py 4.0.65.8, Linux x86_64, no GPU. Grades: Confirmed (a named tool ran or the file was read at the
named commit), Likely (read or reasoned), Suspected.

## Three measurements that changed the plan

| Measurement | Result | Grade |
|---|---|---|
| Change one Blender property, export X3D 4.0, compare | 363 scalar properties changed; 39 change the file, 324 leave it byte-identical; none of the 324 has a declared class | Confirmed |
| Build a UV sphere in four processes, export | 4 different files; from one saved .blend, 4 identical files. The writer is deterministic; the sphere operator is not | Confirmed for this scene |
| Rank the first-trip budget by element | ROUTE is the largest group in the main profile: 62 of 221 differences | Confirmed |

| Datablock | Properties changed | File changed | File identical |
|---|---|---|---|
| Principled BSDF inputs | 34 | 5 | 29 |
| Object | 83 | 8 | 75 |
| Mesh (scalar settings) | 23 | 0 | 23 |
| Material settings | 35 | 3 | 32 |
| Camera | 55 | 8 | 47 |
| World | 15 | 0 | 15 |
| Lights (point, sun, spot, area) | 118 | 15 | 103 |
| All | 363 | 39 | 324 |

Most of the 324 are editor flags, and some are masked by the starting state. The list still holds real losses: light
`energy` changes nothing from the 10 W default on any light type (a Blender-made light is capped at intensity 1).

## The contract: seven properties

| # | Property | Gate |
|---|---|---|
| 1 | Declared mapping: every Blender property and every X3D field has a row (exact, approximate, carried, dropped, not applicable) | perturbation sweep both ways; field-level parity check |
| 2 | Loss receipt: every export and import says what it dropped, approximated or carried | receipt totals equal the sweep's findings on the 195-case suite |
| 3 | Fixed point: a second round trip changes nothing | `tools/io_sync/fixed_point.py` (in CI) |
| 4 | Bounded first trip: first-trip loss never grows | `first_trip_budget.json` (in CI: 221, 65, 98) |
| 5 | Transactional and reproducible: a failed export leaves the old file; a frozen scene gives one file | rollback tests; two-process test on frozen fixtures |
| 6 | Identity survives (new): DEF names, ROUTE endpoints, Metadata, units, provenance | identity invariants in the round-trip gate |
| 7 | Hostile input is safe (new): no crash, hang, memory blow-up, stray network call or code execution | fuzzing, hostile corpus, resource-limit tests |

One rule for every judge: a gate is trusted only after it has caught a planted fault of the kind it claims to catch.

## The five judges

| Layer | Today | v3 adds |
|---|---|---|
| Structure | XSD, x3d.py strict | Web3D Schematron, disagreements kept as fixtures |
| Meaning | x3d_mcp by hand | x3d_mcp pinned by commit, in CI |
| Round trip | fixed point, first-trip budget | counts, bounding box, material values, DEF/USE and ROUTE graphs; six metamorphic relations |
| Appearance | X_ITE 16.7.1 against Babylon.js 9.32.0 on 9 scenes | same renderer with two exporters (the add-on's X3D and Blender's own glb, both drawn in X_ITE); EEVEE after a calibration run; x3d.wgpu as a browserless witness; Cycles as a witness only |
| Behaviour | preset tests | X_ITE event log before and after a round trip |

## Four gates

| Gate | Weeks | Exit, in numbers |
|---|---|---|
| 1 Contract | 1 to 3 | 0 undeclared Blender properties and X3D fields; 0 of 49 nodes unmeasured (13 today); 0 undeclared ROUTE or DEF changes (58 today); receipt agrees on 195 of 195 cases; Schematron in CI |
| 2 Oracles | 4 to 6 | 5 of 5 judges catch a planted fault; thresholds written from a calibration run, then 20 scenes gated against Blender; render waivers below 27 of 43; round-trip gate on both Blender LTS lines |
| 3 Robustness | 7 to 10 | importer split into parser, node-to-IR and builder; 90% branch coverage on pure-Python layers; mutation kill rate 80%; 0 crashes and 0 hangs under fuzzing; no performance ratio above 1.2 |
| 4 Hub | 11 to 12 | DEF and Metadata survive X3D to Blender to glb and back, and through USD with a flatten codec (Blender's USD exporter returns 0 of 6 Metadata nodes today), one receipt per hop; an Unreal hand-off pack |

## What changed from v2, and why

1. **Find loss by perturbation, not by scanning reads.** A silent loss is a property the code never reads.
2. **Identity moved from Gate 4 to Gate 1.** It is the largest measured first-trip loss.
3. **Calibrate before gating appearance.** The delta-E 2.0 and SSIM 0.95 thresholds were never measured; Cycles casts shadows raster engines do not.
4. **Freeze fixtures; do not sort in the writer.** The nondeterminism is Blender's sphere operator.
5. **Every judge must catch a planted fault.** Five of the Fault Lab's ten faults change no pixel.
6. **The mapping table covers the whole standard** and feeds the coverage board's Blender column.
7. **The receipt lives beside the file**, with one content-derived hash line inside it.
8. **Hub order is glTF, USD, Unreal.** Unity and the behaviour node editor are optional and unscheduled.

## Built: Gates 1 and 2 (22 Nov 2026)

x3d-blender-io PR #72 builds the contract and the oracles; the add-on's own write-up is `docs/ORACLES.md` there, and the
run record is x3d.loom `runs/blender-io-gates12-20261122/` (lessons: `LEARNINGS-blender-io-gates-1-2.md`). Every judge
fails a planted fault in CI. Measured with bpy 5.3.0 and the Blender binaries 4.5.14 LTS, 5.1.2 and 5.2.2 LTS.

| Gate 1 piece | Result | Grade |
|---|---|---|
| Mapping table, Blender half | 262 rows + 3 patterns; 0 undeclared properties on all four versions | Confirmed |
| Mapping table, X3D half | 268 nodes, 3,363 fields (x3d.py 4.0.65.8); the export writes 30 nodes, 133 fields | Confirmed |
| Loss receipt v1 | a head line in every X3D 4.0 file, optional sidecar; probe scene 1 dropped, 4 approximated, 4 clamped | Confirmed |
| Web3D Schematron | 4 of 4 planted faults caught; 9 listed disagreements, 0 unexplained errors; one upstream rule bug (HAnimJoint USE) | Confirmed |

| Gate 2 judge | Result | Grade |
|---|---|---|
| Perturbation sweep, 3 starting states | 54 carried properties (one state found 39); 0 silent losses, 0 stale rows, 0 receipt disagreements on four versions | Confirmed |
| Golden files, 12 frozen scenes | byte-equal on all four versions | Confirmed |
| Six metamorphic relations | pass; the camera X3D binds follows the outliner, not the active camera (1 of 12 scenes, budgeted) | Confirmed |
| Round-trip invariants | faces, world bbox, lights, viewpoints and textures hold; materials, ROUTEs and collection instancing break (budgeted) | Confirmed |
| X_ITE on the add-on's X3D vs X_ITE on Blender's glb | 5 of 12 scenes pixel-identical; the rest differ for named exporter reasons | Confirmed |

Fixed on the way: Blender 4.5.14's import/export round trip did not converge (a non-unit normal on a degenerate face);
it now does on all three binaries. Decisions: X3D 4.0 is the default export from 2.7.0; the receipt line is always on
and the sidecar stays opt-in; A12 (linked collection instances on import) is queued as importer work; the nightly
workflow runs the slow judges on every Blender line.

## Fortified: 2.7.1 (22 Nov 2026)

x3d-blender-io PR #73 fixes three of the losses the judges found. None was a blocker; each was cheap and showed up in a
judge's numbers.

| Fix | Judge that found it | Before | After | Grade |
|---|---|---|---|---|
| The file opens on the active camera (`extract.bind_first` writes the subtree holding `scene.camera` first) | metamorphic R3 | 1 of 12 scenes moved the binding | 0 of 12 | Confirmed |
| An ORTHO camera becomes an `OrthoViewpoint` (extents from `ortho_scale` at the render aspect; Navigation level 3), and the importer reads it back | sweep, first-trip budget | written as a perspective Viewpoint; fieldOfView changed on the first round trip | carried; the budget group shrinks 1 to 0 in all 3 profiles | Confirmed |
| Light temperature folds into the colour (`color x temperature_color`, as Blender's glTF exporter does) | sweep | dropped, listed on the receipt | approximated, carried | Confirmed |

The sweep now counts 63 carried properties on bpy 5.3.0 (54 before) and passes on 4.5.14, 5.1.2, 5.2.2 and 5.3.0. The
fix showed a second Web3D Schematron rule bug. The `Viewpoint | OrthoViewpoint` rule (.sch line 2495) puts its
`count(preceding::OrthoViewpoint) > 0` clause outside the parentheses, so every Viewpoint after the first OrthoViewpoint
is reported as needing Navigation level 3 even when the file declares it. A two-node file gives 1 error with the
OrthoViewpoint first and 0 with it second. It is listed as a disagreement (7 per suite file) and has not been sent to
Web3D.

## Chaos round: 2.7.2 (22 Nov 2026)

x3d-blender-io PR #75 adds differential chaos testing (`tools/chaos/differential.py`, `docs/CHAOS.md` there). Each
one-edit mutant of the 12 frozen scenes goes to six judges: the add-on's validator, x3d.py, the Web3D XSD, the
Web3D Schematron, the importer and the re-export.

| Run | Crashing mutants | Grade |
|---|---|---|
| 2.7.1, rng 7 | 68 of 960, 5 signatures | Confirmed |
| after the first five fixes, rng 7 and 11 | 7 of 1,920, 3 more signatures | Confirmed |
| 2.7.2, rng 7, 11 and 23 (bpy 5.3.0) | 0 of 2,880 | Confirmed |
| 2.7.2 on Blender 4.5.14 and 5.2.2 | 0 of 960 each | Confirmed |

Eight crashes were fixed:
- a bool spelt `1` ended the import;
- one huge coordIndex padded the point list (`2147483647` raised MemoryError), and the same padding hit colours and
  texture coordinates;
- a malformed scale raised;
- fieldOfView INF raised;
- a NaN scale broke the re-export;
- X_ITE's radius -1 imported but failed the export's own check;
- the validator recursed on deep scenes.

Three of these lines are also in Blender's own X3D importer (Likely: read, not run). The validator is now strict
about SFBool spelling and vector widths, which x3d.py 4.0.65.8 does not check. CI runs 240 mutants on every PR, with
a planted fault, and the nightly runs 960 per Blender line.
