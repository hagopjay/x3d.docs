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

| | Before (x3d_mcp `4d433af`) | After (`0b941c9`) |
|---|---|---|
| glTF-Validator codes X3D can state, reported by X3D's checks | 40 of 88 | **88 of 88** |
| Fault Court, X3D caught | 39 of 53 | **52 of 53** |
| On the 43 mistakes glTF can also state | X3D 29, glTF 41 | X3D 42, glTF 41 |
| Decoys flagged | 0 of 10 | 1 of 10 |

How to read it:

- **88, not 170.** 46 codes guard glTF's byte layout and 21 guard structures X3D has no way to write. Those are properties of the format, not a score. 12 codes are glTF material features X3D 4.0 cannot express, and 3 wait for the Tangent node of X3D 4.1.
- **The Fault Court rerun is a fix confirmation.** The checks were written with all 60 mistakes in view. The one still missed is not a mistake in X3D. A new held-out number needs a new sealed list from another author.
- **The flagged decoy** has key times in seconds, which is legal in glTF and stalls an animation in X3D. It is counted as a false alarm because the list was fixed before the run.
- **Real files.** The new checks were run over 1,496 X3D scenes before shipping. Three checks raised false alarms and were fixed; the survey also found two real defects in existing demos.

**The claim we can make now:** on the mistakes both can state, X3D's validator reports what glTF's does, and a few things it does not (zero scale, declared boxes through transforms, event wiring). Each turn is recorded in the Loom's `flywheel/LEDGER.md`, and anyone can rerun it with one command.

Table of all 170 codes: x3d_mcp `docs/GLTF-VALIDATOR-PARITY.md`. Method and learnings: x3d.loom `LEARNINGS-flywheel-turn-2.md` (failure modes 323 to 328).
