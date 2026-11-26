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

**The claim we can make:** X3D can say the most, and with the Loom it can check more each turn. Its validator does not yet check as much as glTF's.
