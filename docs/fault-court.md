# Fault Court: X3D, glTF and USD judged on the same mistakes (26 Nov 2026)

The kit, pre-registration and results are in x3d.loom `fault-court/`. The results page is Demo 82 (`fault-court/v1` on the demo site). Failure modes 318 to 322 come from this test.

## The test

- **One scene, three formats.** A textured cube, a box, a camera, an animation, a unit and a metadata value. Three independent writers produced it natively as X3D 4.0, glTF 2.0 and USD. No file was converted from another.
- **The mistakes.** 60 planted mistakes in six format-neutral families, plus 10 legal-but-unusual decoys.
- **The checkers.** Each format was judged only by its own official checkers:
  - X3D: x3d_mcp XSD plus semantic checks.
  - glTF: the Khronos glTF-Validator.
  - USD: usd-core with its 30 registered validators.
- **Pre-registered.** The design and thresholds were committed before any faulty file was checked.

## Result

| | X3D | glTF | USD |
|---|---|---|---|
| Mistakes the format can state (of 60) | **53** | 48 | 44 |
| Caught by its own checkers | 39 | **46** | 5 |
| Held-out half, plus Loom rules | 17 → 20 of 25 | 23 → 23 of 24 | 1 → 10 of 20 |
| False alarms | 0 | 0 | 0 |

## What this means for "X3D is the format an AI can be held accountable to"

- **X3D is the richest language.** It can state the most mistakes, including event wiring, units, typed metadata and humanoid joints.
- **X3D's validator is not the strongest judge.** glTF's validator caught 12 mistakes that X3D's missed. X3D's caught none that glTF's missed.
  - X3D's misses are data mistakes that sit between values or in files: per-vertex counts, missing textures, a hierarchy cycle, declared bounds.
  - A schema checks each value on its own, so it cannot see them.
- **The Loom closed part of the gap, measurably.** Rules learned from half the mistakes caught mistakes they had never seen, with no false alarms. That is one turn of the flywheel. The next turn is to move the rules into the validator itself.

**The claim we could make after turn 1:** X3D can say the most, and with the Loom it can check more each turn. Its validator did not yet check as much as glTF's. Turn 2, below, closed that.

## Turn 2 (26 Nov 2026): the rules moved into the validator

The next turn was taken. Every issue code the Khronos glTF-Validator can raise (170) was mapped to X3D, and each one X3D can state got a failing and a passing scene.

| | Before (x3d_mcp `4d433af`) | After (`f0bde28`) |
|---|---|---|
| glTF-Validator codes X3D can state, reported by X3D's checks | 40 of 88 | **88 of the 170 Khronos codes** (the 88 the project judged X3D can state; the project classified the rest) |
| Fault Court, X3D caught | 39 of 53 | **52 of 53**, a fix confirmation by a rule writer who had seen the faults (held-out figure: Loom arm, 17 to 20 of 25) |
| On the 43 mistakes glTF can also state | X3D 29, glTF 41 | X3D 42, glTF 41 |
| Decoys flagged | 0 of 10 | 1 of 10 |

How to read it:

- **88, not 170.** 46 codes guard glTF's byte layout and 21 guard structures X3D has no way to write. Those are properties of the format, not a score. 12 codes are glTF material features X3D 4.0 cannot express, and 3 wait for the Tangent node of X3D 4.1.
- **The Fault Court rerun is a fix confirmation.** The checks were written with all 60 mistakes in view. The one still missed is not a mistake in X3D. A new held-out number needs a new sealed list from another author.
- **The flagged decoy** has key times in seconds, which is legal in glTF and stalls an animation in X3D. It is counted as a false alarm because the list was fixed before the run.
- **Real files.** The new checks were run over 1,496 X3D scenes before shipping. Three checks raised false alarms and were fixed; the survey also found two real defects in existing demos.

**The claim we can make now:** on the mistakes both can state, X3D's validator reports what glTF's does, and a few things it does not (zero scale, declared boxes through transforms, event wiring). Each turn is recorded in the Loom's `flywheel/LEDGER.md`, and anyone can rerun it with one command.

Table of all 170 codes: x3d_mcp `docs/GLTF-VALIDATOR-PARITY.md`. Method and learnings: x3d.loom `LEARNINGS-flywheel-turn-2.md` (failure modes 323 to 328).

## Turn 3 (26 Nov 2026): the USD rulebooks

The same method against USD: all 340 rules of OpenUSD's validators, NVIDIA's Omniverse Asset Validator and the SimReady Foundation. The project judged that X3D can state 66 of them (66 of 340; the project classified the rest), and its validator now reports those 66; 32 more cannot be broken in X3D at all. See [usd-parity.md](usd-parity.md).

## The rules on a new stack (26 Nov 2026)

The glTF and USD checks run on x3d.downey's 20 scenes before and after they landed: 0 new errors, one true defect every earlier witness had passed, seven false alarms fixed. See [downey-rules-test.md](downey-rules-test.md).

## Blind court 3 (27 Nov 2026): the first score with the test sealed first

Courts 2 and 2b gave the kernel its only blind score, 24 of 40, and checks were then written from their misses. Scoring those checks on the same two sets (37 of 40) only confirms the fix. Court 3 was built to measure the turn properly:

1. Two fresh authors, forbidden to read any repository, each wrote 20 faults, a corrected twin for every fault, and 5 legal decoys, and returned only a hash.
2. The kernel was frozen by pushed commit with its 11 new checks (x3d_mcp `d647a10`).
3. The scoring rule and four expectations were pushed.
4. Only then was the set opened, and the old and the new kernel were each run on it once.

| Measure | Old kernel `ebe969b` | New kernel `d647a10` |
|---|---|---|
| All 40 unseen faults caught | 19 | 25 (+6, none lost) |
| Behaviour (20) | 8 | 11 |
| Structure (20) | 11 | 14 |
| Caught by the XSD alone | 5 | 5 |
| Warnings or errors on the 50 legal files | 18 | 18, none from the new checks, none judged wrong |
| The sets the checks were written from (courts 2 and 2b) | 24 of 40 | 37 of 40 |

Instruments: x3d_mcp `validate_xml` (X3D 4.0 XSD) and `semantic_diagnostics`; two readers decided separately whether a finding names the planted mistake and agree on all 40 faults. The authors' witness is X_ITE 16.8.0 (34 of 40 pairs run in the browser, 6 reasoned).

**How to read it.**

- The paired change, 19 to 25 on one unseen set, is the measure of the turn. The checks written from the last test did carry to a new one.
- The same kernel flags 92% of the faults it was written from and 62% of unseen ones. That gap is the over-fitting, and it is printed every turn from now on.
- The old kernel scored 24 of 40 on the last unseen set and 19 of 40 on this one with the same code, so scores on different sets cannot be compared.
- One of the four expectations failed: 26 of 40 was expected and 25 arrived.
- The 15 misses are mostly legal files that play wrong (a clock meant to repeat with loop false, swapped drag limits, a Script handler whose name matches no field, Viewpoint order, a LOD range as long as its children, `ccw` false on outward faces). They are the next candidates, and they are now seen.

**The eleven checks** (x3d_mcp PR 39): a pointing sensor with nothing to sense or switched off for good; a clock that can never start; an interpolator, sequencer or trigger with nothing in or nothing out; a Switch index past its children; plain ROUTEs in a circle; an environment sensor of size 0 0 0; a Script with no code; a looping spin that does not close; an angle that reads as degrees; an Extrusion with fewer than two points; a light with direction 0 0 0. On 2,396 tracked project scenes the wiring checks raise 44 warnings on real scenes: 30 true, all in model-written scenes, and 14 where a web page drives the scene from outside the file, which a file check cannot see.

**Limits.** One browser engine as witness; authors, second reader and rule writer are agents of the same family; forty faults; two small leaks from the authors' reports, disclosed before opening (dropping the affected pair gives 18 to 24 of 38).

Plan, set, every verdict and the scoring script: x3d.loom `flywheel/court-3/` (`PREREG.md`, `RESULTS.md`). Failure modes 476 to 483.
