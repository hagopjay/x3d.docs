# The self-coding loop: X3D behaviour written by search (26 Nov 2026)

The kit, pre-registration and results are in x3d.loom `selfcode/`. Failure modes 329 to 339 come from this test. It is built on the behaviour graph of x3d-blender-io (see the behaviour graph page): a typed node catalogue, a graph in plain Python, and a simulator checked against X_ITE.

## The test

- **The task.** A static stage with four objects. A hidden reference behaviour is poked by a script (hover, press, drag, release, leave). The synthesiser sees only what the watched fields did every 0.05 s.
- **The method.** Search over sensors, timers, event utilities, followers and ROUTEs, typed by the X3DUOM catalogue. Interpolator tables are fitted, not searched. One simulator run is the unit of cost. No language model, no person.
- **The judges.** The simulator on a stimulus the search never saw; the x3d_mcp kernel (X3D 4.0 XSD and semantic checks, `f0bde28`) on every written file; X_ITE in a browser on a sample.
- **Registered first.** Five hypotheses were committed (`ec934f1`) before any test seed was run.

## Results

| Hypothesis | Result | Grade |
|---|---|---|
| It codes itself: at least 80% of unseen in-vocabulary tasks solved and correct on an unseen stimulus | 87 of 90 (95% interval 91 to 99%) | C |
| The kernel accepts every file it writes | 267 of 267 with 0 schema and 0 semantic errors | C |
| A longer lesson is at least as good as a short one | 87 against 86 | C |
| Memory halves the search on the next batch | 4,109 to 1,018 simulator runs, Wilcoxon p = 2.9e-12, no loss of correctness | C |
| Controls outside the vocabulary are missed | 1 of 18 solved and correct | C |

Browser replay (exploratory): 15 of 18 sampled solutions match their reference in X_ITE 16.8.1 at the strict threshold, 2 more are within the court's own replay noise, and 1 is a real disagreement between simulator and browser; 3 of 3 mismatched controls were told apart.

On the node editor's own test worlds it rebuilt the door, and from the counter's behaviour alone it wrote a ripple carry (Bit 1 toggles when Bit 0 falls). It missed the snake.

## The stack on one file

`selfcode/stack/` holds one scene with four layers, each with its own judge: a glTF 2.0 door (Khronos glTF-Validator, 0 errors), an X3D 4.0 scene that Inlines it and whose behaviour was written by the search (kernel, 0 errors), the scene as RDF in X3D Ontology terms answering "what does a press on a TouchSensor end up changing?" with one SPARQL query, and a receipt naming every file by hash and every judge by version.

## Outside its own test: the wild set

The 87 of 90 above is on tasks written by the same hand as the search. `selfcode/wild/` runs the same search on real scenes: every `.x3d` file in the project's repositories that has a ROUTE, no Script, and only nodes the simulator runs. 656 qualify. The split is by file hash, the method was tuned on 60 development scenes, the predictions were committed (`31461d5`), and then 100 unread scenes were run.

| | Result |
|---|---|
| Left out, each for a counted reason | 47 of 100 |
| Rebuilt from one demonstration and right on unseen input | 39 of 53 (74%, 95% interval 60 to 84%) |
| Written scenes that add a kernel error | 0 of 39 |
| Originals of 1-3 behaviour nodes | 31 of 32 |
| Originals of 4-10 nodes | 4 of 8 |
| Originals of 11 or more nodes | 2 of 11 |
| Median cost of a rebuilt scene | 4 simulator runs |

Judges: simulator `x3d-blender-io@3e3c1e8`, kernel `x3d_mcp@f0bde28`. These are the simulator's verdicts; a browser sample follows.

Read it with three cautions. It is a test of animation: 50 of the 53 tasks had nothing to poke. Size is the wall: generated scenes with 75 to 400 animated fields are out of reach. And the scenes are a family from this project's own generators and model runs, so they succeed and fail in groups. Two of the six registered predictions failed (large scenes did a little better than predicted, and memory saved a third of the runs where none was predicted) and are reported as failed.

The development split paid for itself. A graph writer that printed six decimals turned a key of 3.14159265 into 3.141593, past pi, and every turntable ran backwards. A lesson of two turns taught the search a recording that broke when watched longer. And one bug in the marking code had filed 21 solved scenes under "cannot be read".

### The wild set in a browser

A sample of the rebuilt scenes (the first 12 by hash) was replayed against the originals in X_ITE 16.8.1. Expectations were written before each run, and both runs failed them, which is the useful part.

- **Run 1** used the pair judge as shipped: 9 same, 2 differs, 1 unclear, and all 3 planted controls came out "same". The judge was blind. In X_ITE a looping TimeSensor takes its phase from the wall clock, so two replays a few seconds apart are at different points of the loop, and a file disagreed with itself on every sample. It also compared rotations number by number, and X_ITE spells one rotation more than one way.
- **Run 2** started the original and the written scene at the same moment in two browsers and compared rotations as rotations: 9 same, 0 differs, 2 unclear, 1 tool error; controls 1 of 3. A file now agrees with itself.
- **Afterwards**: the tool error was a stream that is not a number, and that pair is the same; the controls differ only in the first half of the loop, and all 3 differ on every sample when the watch is put there.

- **Run 3** sent all 39 rebuilt scenes through the fixed judge (x3d-blender-io 2.7.8), each watched for a whole loop: 25 same, 1 differs, 9 unclear, 4 tool errors, and all 3 planted errors caught. The expectation was 30 same and none different, so this failed as well.

Of 39 rebuilt scenes, 25 were seen to behave the same in X_ITE. One differs by 0.000004 rad: a model-written "spin" whose keys of 0 and 6.28319 move the cube five millionths of a radian, which the search matched with the wrong clock inside the simulator's tolerance. Thirteen could not be judged, most of them short fast scenes on a loaded machine.

## Learning from a recording

`selfcode/lesson.py` reads an `x3d.activity/1` recording from the Blender node editor's recorder and shows the search only the pointer calls and what landed on the stage. Nodes, ROUTEs and inner events are withheld. From one press of a button it rebuilt the door (60 runs, the original's three nodes); from three presses it rebuilt the two-bit counter with its ripple carry (664 runs). Both agree with the original on a stimulus that was not recorded. Two worlds: a first result, not a rate.

## What to take from it

- A scene language with typed fields and an executable meaning can be written by search, not only checked. 3 of the 108 test tasks could be stated in glTF 2.0 core, which has keyframes and no events.
- Search the wiring, solve the numbers. Remembered shapes transfer because they hold no times or values.
- One demonstration can leave look-alike programs standing. Design the lesson to separate them and judge on an unseen stimulus.
- A table with a key per sample is a recording, not a rule.
- A search finds the holes in its judge. One solution is equivalent to its reference in the simulator and different in X_ITE; a sample of every batch should go to a second engine.
- The registered tasks are synthetic and by the same author as the method. The wild set is the first check on files nobody wrote for it; a sealed task list by someone else is still the next step.
