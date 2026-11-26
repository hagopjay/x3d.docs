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

## What to take from it

- A scene language with typed fields and an executable meaning can be written by search, not only checked. 3 of the 108 test tasks could be stated in glTF 2.0 core, which has keyframes and no events.
- Search the wiring, solve the numbers. Remembered shapes transfer because they hold no times or values.
- One demonstration can leave look-alike programs standing. Design the lesson to separate them and judge on an unseen stimulus.
- A table with a key per sample is a recording, not a rule.
- A search finds the holes in its judge. One solution is equivalent to its reference in the simulator and different in X_ITE; a sample of every batch should go to a second engine.
- The tasks are synthetic and by the same author as the method. A sealed task list by someone else is the next step.
