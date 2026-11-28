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

## Blind court 4 (28 Nov 2026): the target was 30 and the score was 23

One turn later, the same protocol. Court 3's 15 misses were turned into 13 checks, 7 more were written from the editor's own list of what goes wrong, and the 20 were frozen by pushed commit (x3d_mcp `c185673`) before two new blind authors' set was opened. The target told to the project owner beforehand was 30 of 40.

| Measure | Old kernel `ca0e75c` | New kernel `c185673` |
|---|---|---|
| All 40 unseen faults caught | 19 | 23 (+4, none lost) |
| Behaviour (20) | 12 | 13 |
| Structure (20) | 7 | 10 |
| Caught by the XSD alone | 3 | 3 |
| The 19 faults that repeat a court 3 fault | 16 | 18 |
| **The 21 faults that are new mistakes** | **3** | **5** |
| Warnings or errors on the 50 legal files | 0 | 0 |
| The set the checks were written from (court 3, editor's reading) | 25 of 40 | 38 of 40 |

Instruments: x3d_mcp `validate_xml` (X3D 4.0 XSD) and `semantic_diagnostics`, Python 3.13.18, lxml 6.1.3. A fresh second reader, not told which kernel said what, and the kernel editor agree on all 40 faults; the reader judged all 40 real. The authors' witness is X_ITE 16.8.0 in headless Chromium 158 on SwiftShader, all 40 pairs run, not repeated by us.

**How to read it.**

- The target failed by seven. Four of five written expectations held: at least +3, and three limits on false alarms.
- The headline hides two different numbers. The second reader marked 19 of the 40 faults as the same mistake court 3 had planted. The kernel names 18 of those 19 and 5 of the other 21: 95% on mistakes it has met, 24% on mistakes it has not.
- The 13 checks written from court 3's misses gained two faults, and both were court 3's mistakes planted again (a Script function whose name matches no field, a ProtoInstance field the prototype does not declare). On new mistakes they gained nothing. A check written from a miss is a regression test.
- The only gains on new mistakes came from the 7 checks written from no test set: a ball with transparency 1, and a first Viewpoint looking away from the scene.
- Of the 14 faults that break the standard the kernel names 13. Of the 26 that are legal and wrong only against what the scene was meant to do, it names 10 (the second reader's count).
- The legal files are clean. Court 3's 18 complaints came mostly from a kit with no X_ITE component files; with the whole distribution in the kit there are none.

**The 17 misses split in two.** Nine could be stated from the file alone and are the next rule candidates: a PlaneSensor's `trackPoint_changed` driving a position, browser key codes compared with `actionKeyPress`, a moving target routed to a damper's `set_value`, `isActive` routed to `set_bind`, a `USE` with attributes of its own, one face wound the other way on a closed mesh, per-face colours with `colorPerVertex` left TRUE, an Inline url that names no file, and a MetadataSet entry with `containerField='metadata'`. Eight cannot be told from a correct file at all: a `cycleInterval` of 500, a door that turns about its middle, a texture scale of 0.25 meant as four repeats. Pattern rules do not reach those. A scene would have to carry its own expectations for a checker to hold it to them.

**What the next court changes.** Each author gets the one-line list of every mistake already planted, with the instruction not to plant any again. The headline is the score on new mistakes, with repeats beside it. The target is set on new mistakes only: 5 of 21 is the number to beat.

**Limits.** Authors, second reader and rule writer are agents of one model family, which is why half the set repeats the last one; a stranger's set would likely score lower. The repeat marking is one reader's judgement. Forty faults; +4 is within what a different author would move (sign test p = 0.125). One scoring script was edited after the seal was opened, to leave a helper file out of the reader's packet; the results page lists it.

Plan, set, every verdict and the scoring script: x3d.loom `flywheel/court-4/` (`PREREG.md`, `RESULTS.md`). The checks: x3d_mcp PR 42. Failure modes 519 to 525.

## Blind court 5 (plan of 28 Nov 2026): closing the gap without tricks

There is no court 5 score. This is the plan it will be run under, written and tested on a dummy set before any author is briefed.

**The gap has three parts.** Court 4's kernel named 18 of the 19 faults that repeated court 3 and 5 of the 21 that were new. Rules written from the last court's misses gained only repeats. And 8 of the 17 misses were legal files that are wrong only against what the author meant.

**Five changes, ranked.**

1. **New mistakes only in the headline.** Authors are handed the 120 mistakes already planted in courts 2, 2b, 3 and 4, one line each, and may repeat none. Repeats are still marked by the second reader and scored beside the headline.
2. **Rules from the standard, not from the last set.** A grid built from the X3D 4.0 object model lists 6,434 places where one of 15 classes of mistake can occur across the 260 nodes (a value outside its stated range, a ROUTE into a field that takes no events, an index past the end of its array, and so on). A cell is closed by a wrong file and its corrected twin on which the kernel speaks and stays silent. Every new check is labelled `grid` or `misses`, and the score says which label earned each gain. A count of cells is coverage of this grid, not of X3D.
3. **Stated intent as its own arm.** A scene may say what it is for in `meta` lines a machine can test, for example `after 1.6s: Door.rotation[3] > 1.4`. A headless play test in X_ITE sends the stimuli and checks each line. The kernel never sees the intent and the two scores are never added.
4. **A catch proven by machine.** A diagnostic counts only if the check that names the mistake fires more often on the fault than on its corrected twin. Rescoring court 4 this way changes nothing (still 19 to 23, and 3 to 5 on new mistakes), so the rule costs no comparability.
5. **A set by a stranger.** Every court so far was written by agents of one model family. A slot is reserved for a set from outside; it is empty until the project owner chooses a source.

**No promised number.** Court 3's target was missed by one and court 4's by seven. Court 5 registers a direction test (the new kernel proves more new mistakes than the old one and loses none, with the exact sign test printed), the like-for-like figure from court 4 (5 of 21), and a forecast labelled as a guess.

**Twelve tricks it may not use**, among them: rescoring after the seal is opened, dropping a fault from the denominator, counting a note that fires whatever the mistake was, a check keyed to a file name or an author's habit, an intent line that states the answer, and calling a seen set held-out.

**State.** Sixty faults are planned (three authors: behaviour, structure and data, look). The list of earlier mistakes, the grid, the intent stripper, the play test, the scorer and the briefs exist and ran end to end on a dummy set of four faults (kernels x3d_mcp `ebe969b` and `2943b78`, X_ITE 16.8.0, headless Chromium). The grid is unprobed and the kernel turn has not started.

Plan and scaffold: x3d.loom `flywheel/court-5/` (`PLAN.md`, `PREREG-DRAFT.md`, `intent/INTENT.md`). Failure modes 568 and 569.
