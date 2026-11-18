# Gobbler.flyte field notes (18 Nov 2026)

Gobbler.flyte (x3d.gobbler `flyte/`, PR #1) is a 24/7 agent loop that grows an X3D world only through validated steps. These notes cover what an X3D learner can take from it. Grades: Confirmed (a named tool ran), Likely, Suspected.

## The loop

| Organ | Does | X3D instrument |
|---|---|---|
| Scout | reads 12 feeds; sets namesakes aside | web3d.org RSS, HN, arXiv, release feeds |
| Weaver | proposes a loom action + an X3D fragment | Haiku 5.5 (only with a typed allowance) or the x3d.accrete procedural generator |
| Witness | referees the fragment | x3d.accrete gate 2.0.0 @ 93063bf, x3d_mcp b5c9956, x3d.loom traps.py @ 4cf5c7a |
| Keeper | appends to a hash-chained world | x3d.accrete `WorldStore.append` |

## Lessons

| Lesson | Grade | Where it shows |
|---|---|---|
| "X3D" is three things online: the ISO format, AMD Ryzen X3D chips, and a video-recognition network (X3D-M and similar). In the 18 Nov snapshot, 6 of 12 HN title hits and 11 of 15 arXiv hits were not the format. | Confirmed | `flyte/fixtures/feeds/`, `relevance.py` |
| A gate and a validator can disagree. `PhysicalMaterial` passes the accrete gate, then the pinned x3d_mcp semantic pass refuses it under the Immersive profile. Validate with the same instrument that guards the commit. | Confirmed | `tests/test_flyte.py::Referee`; [chapter 3](../learn/03-validator-and-gates.md) |
| Error codes make good feedback. Each refusal code (GATE_CONTAINMENT, GATE_NODE_FORBIDDEN, MCP_SEMANTIC_PROFILE_COMPONENT) went back to the generator; the simulated day admitted 35 of 35 turns after 26 refusals. | Confirmed (scripted model) | `runs/sim-2026-11-18/summary.json` |
| A human in the loop needs a clock. A reversible question takes the preferred pick after 4 h; an irreversible step (a send outside the repos) never does, and needs the word "send". | Confirmed | `hitl.py`, `Answers` tests |
| Web text is untrusted input. Titles reach the model quoted and linted by x3d.loom's `untrusted.py`. | Confirmed | `VendoredLoom` tests |

## Drill

1. Why does a watcher for X3D news need a namesake filter before it ranks? *Answer: on the live snapshot, most "x3d" hits outside web3d.org were chips or the video net.*
2. Which instrument should Witness run before Keeper commits? *Answer: the same validator that the commit path runs (here x3d_mcp b5c9956 inside x3d.accrete), not only the gate.*

## After the second review (18 Nov, x3d.gobbler PR #2)

| Lesson | Grade | Where it shows |
|---|---|---|
| One grade hides many questions. Each turn now carries facets (structure, source, target, admission, human, render, reuse), and the loop's grade stops at Likely. | Confirmed | `flyte/runs/sim-2026-11-18-r2/summary.json` |
| A single-file X_ITE page must also inline its stylesheet's `url(assets/...)` images and its fonts, or it asks the page origin for them. Re-pin the stylesheet's SRI to the bytes actually served. | Confirmed (Chromium 157, 2 real 404s fixed) | `gobbler-flyte/build_standalone.py` |
| The Intervention Lab teaches three rules by experiment: a digest you issue yourself adds no witness, a guard must reject known failures, and a retry is not a return. | Confirmed (native run, 12 of 12 rules) | `evidence-lab/`, `tools/lab_browser_check.cjs` |

Drill 3. Why does re-running the same consumption three times leave the reuse count at 1? *Answer: reuse counts distinct (guard, target, input digest) tuples; a retry repeats one tuple.*
