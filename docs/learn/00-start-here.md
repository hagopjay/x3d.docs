# X3D Elucidation: the deep-learning base for an AI-accountable 3D format

> **Thesis:** *X3D is the 3D format an AI can be held accountable to.* Its rules are machine-readable, so software can say exactly what is wrong; a second renderer shows what is visible; a ledger travels with the file. This base teaches that machinery, measures it, and marks where it stops. **[L]** (the claim is argued across chapters 01 to 05; only the measured parts are [C])

This is the learning base for people who already believe in X3D and want the framework in depth: the laws, the traps, the instruments, the numbers and the honest limits. It sits beside six AST teardowns of the code bases that produced the numbers ([x3d-blender-io](../x3d-blender-io/MASTERCLASS.md), [x3d_mcp](../x3d_mcp/MASTERCLASS.md), [x3d.loom](../x3d.loom/MASTERCLASS.md), [x3d.onto](../x3d.onto/MASTERCLASS.md), [x3d.demo](../x3d.demo/MASTERCLASS.md), [X_ITE 16.7.0](../x_ite/MASTERCLASS.md)); the teardowns say what the code *is*, these chapters say what it *teaches*.

## How to read a claim here

| mark | meaning | what stands behind it |
|---|---|---|
| **[C]** | Confirmed | measured, or read in the exact file; the *instrument* is named beside the number |
| **[L]** | Likely | read in a source we trust or reasoned from [C] facts; the source is named |
| **[S]** | Suspected | a guess or a design expectation; never a premise for a [C] |

**The instrument rule.** A number without its validator, renderer version or rig is a rumour. Every number in the *Numbers register* of every chapter
names its instrument, for example `x3d_mcp fork b4efcd3`, `X_ITE 16.7.0 on Chromium 153 / SwiftShader`, `bpy 5.3.0`. The register of all instruments
is [Appendix A](A-validator-register.md); every number is in [Appendix C](C-numbers-ledger.md). A result holds only at the pin it names: re-run it at a new pin and
add a dated row, never overwrite the old one.

## The system in one picture

```text
 author (model, Blender, hand)
        |
        v
 +------------------+  exact codes, exact fixes  +----------------------------+
 | validator ladder |<-------- repair loop ----->| scene.x3d (text, hashable) |
 | XSD > rules >    |                            |   THE MASTER               |
 | route/colour/... |                            +-------------+--------------+
 +--------+---------+                                          |
          |                     every body reads the same file |
          v          +------------+------------+--------------+----+------------+
    gate verdict     |            |            |              |    |            |
    (pin, receipt)   v            v            v              v    v            v
                  X_ITE        Babylon       Castle         Blender          glb / USD
                  WebGL2       WebGPU        native         add-on           --> Unreal
                  the oracle   body          host           (blenderizer)
                     |            |            |              |                 |
                     +------------+-- parity: dB, FLIP, counts, node census ----+
                                  |
                          ledger travels with the file
              (who wrote it, which pin passed it, what was drawn)
```

## Reading paths

| path | for | read in this order | you can then |
|---|---|---|---|
| **A. Agent builder** | wiring a model to X3D tools | [01](01-the-tether.md), [03](03-validator-and-gates.md), [04](04-mcp-for-agents.md), [05](05-semantic-layer.md), [02](02-loom-laws.md) | build a write, validate, repair loop and say what it does not catch |
| **B. Engine and renderer builder** | hosting or drawing X3D | [06](06-xite-the-oracle.md), [08](08-babylon-bridge.md), [09](09-castle-engine.md), [12](12-unreal-tier1.md), [02](02-loom-laws.md) | port a scene to a second renderer and log the gaps honestly |
| **C. Artist and pipeline owner** | Blender, glTF, USD, Unreal | [10](10-blender-pipeline.md), [11](11-gltf-usd-khronos.md), [12](12-unreal-tier1.md), [03](03-validator-and-gates.md) | export a scene that survives the trip and prove it |
| **D. Science and simulation** | sci-vis, physics | [13](13-physics.md), [10](10-blender-pipeline.md), [07](07-xray.md), [06](06-xite-the-oracle.md) | build a validated scientific scene with a conservation check |
| **E. Skeptic's tour** | deciding whether to trust any of this | [02](02-loom-laws.md) (failure modes), [Appendix C](C-numbers-ledger.md) sorted by grade, every *Honest limits* section | find the weakest claim in the base; send a PR |
| **F. Methods** | how to learn and extend this | [14](14-methods.md), [AUTHORING](AUTHORING.md), [Appendix E](E-drills.md) | run the drills, add a heuristic with its falsifier |

## The chapters

<!-- BEGIN CHAPTER-TABLE -->
| Ch | Title | Say it | Rules | Drills | Numbers | Size |
|---|---|---|---|---|---|---|
| [01](01-the-tether.md) | The tether | X3D can be held to account because a program can name exactly what is wrong with a file, a second program can show what the file draws, and the record of both checks can travel inside the file; this holds for structur... | 14 | 7 | 21 | 45 KB |
| [02](02-loom-laws.md) | The Loom laws | the Loom is 44 numbered laws and 160 numbered failure modes, each paid for by a recorded failure; this chapter indexes them by number so you can find the law that forbids a mistake, the incident that created it, and t... | 14 | 8 | 20 | 52 KB |
| [03](03-validator-and-gates.md) | The validator and the gates | A validator is a ladder, not a verdict: every rung names what it checked, the rungs below the renderer cannot see "looks right", and a verdict without a commit and a schema version is a rumour. **[C]** | 12 | 7 | 21 | 53 KB |
| [04](04-mcp-for-agents.md) | x3d_mcp as the agent interface | x3d_mcp gives a model 53 callable tools whose answers are small, structured and checkable, tells it the canonical path on connect, and keeps big documents and hostile queries out of its context with guards that live i... | 12 | 7 | 22 | 53 KB |
| [05](05-semantic-layer.md) | The semantic layer: RDF, OWL, SPARQL, SHACL on X3D | An X3D scene can be turned into a graph of facts, questioned with SPARQL, held to SHACL shapes and (carefully) reasoned over, but the ontology only proposes, the shapes dispose and the validators gate; every result na... | 11 | 8 | 24 | 53 KB |
| [06](06-xite-the-oracle.md) | X_ITE, the reference renderer | X_ITE is the second program that tells you what a scene draws and what its events do, and it is a good oracle only when you name its patch, its browser and its options, drive it with guarded code, and remember that it... | 12 | 8 | 21 | 54 KB |
| [07](07-xray.md) | x3d.xray, the X-ray method | x3d.xray turns the git history of a family of repositories into one X3D scene whose every number is computed by code, graded by checks declared before the data is read, and re-derived by a second reader; on a reposito... | 12 | 8 | 24 | 46 KB |
| [08](08-babylon-bridge.md) | The Babylon bridge | one X3D file is the master, our own reader runs its events, and Babylon on WebGPU only paints the result; every picture is a claim against X_ITE on a named rig, every fallback says so on screen, and nothing about spee... | 36 | 13 | 59 | 104 KB |
| [09](09-castle-engine.md) | Castle Game Engine as an X3D host | Castle is a native Pascal engine whose internal model is the X3D node graph, which makes it the best-mapped host we examined for seam knowledge and traps; nothing measured here shows it leading on node coverage, confo... | 15 | 8 | 28 | 53 KB |
| [10](10-blender-pipeline.md) | Blender as the studio: x3d-blender-io and the sci-vis knowledge base | Blender is where a scene is modelled, lit and baked, and the add-on is the door it leaves through; every exit can be gated by a validator and a second renderer, a re-export is valid even when the source was not, so wh... | 13 | 9 | 24 | 53 KB |
| [11](11-gltf-usd-khronos.md) | glTF, USD and Khronos: what survives and what the gate proves | an X3D scene that goes through Blender to a glb keeps its geometry, materials, lights, cameras and fixed animation, loses its behaviour (ROUTEs, Scripts, PROTOs, sensors) and its authoring identity unless you pay to c... | 11 | 6 | 16 | 41 KB |
| [12](12-unreal-tier1.md) | Unreal as a tier-1 X3D framework | Unreal is a plausible tier-1 endpoint for *rendering* an X3D scene through a glb, it cannot run X3D behaviour without a plugin that does not exist, and today every Unreal claim in this base is read, not run: no Unreal... | 15 | 8 | 27 | 49 KB |
| [13](13-physics.md) | Physics in X3D: RigidBodyPhysics, PhysX, MuJoCo and the Ten Minute Physics ports | A valid X3D physics scene says nothing about whether the simulation is stable, deterministic or right; the physics analogue of the validator is a run record whose hashes replay, whose references are exact, and whose c... | 23 | 11 | 28 | 66 KB |
| [14](14-methods.md) | Methods: how to learn, test and extend this base | You learn X3D here by predicting a result, running the tool, comparing, grading the gap and recording a rule with a falsifier; a heuristic you cannot falsify is not in the ledger. **[L]** | 8 | 5 | 12 | 10 KB |
<!-- END CHAPTER-TABLE -->

## What every chapter contains

| part | why it is there |
|---|---|
| **Say it** | one sentence you can repeat and be held to, with a grade |
| **The map** | an ASCII diagram and a scoping table: what is in, what is out |
| **Core sections** | dense tables and worked examples with exact commands and field names |
| **Heuristics** | `H-<code>-<n>` rules a practitioner can apply at a decision point and be wrong about; merged into [Appendix D](D-heuristics-ledger.md) |
| **Drills** | `D-<code>-<n>` tasks with a verify command and an answer key; each says whether it was *run*; indexed in [Appendix E](E-drills.md) |
| **Honest limits** | what was read and not run, where sources disagree, what is stale |
| **Numbers register** | `N-<code>-<n>` rows: quantity, value, grade, instrument, source; merged into [Appendix C](C-numbers-ledger.md) |
| **Sources and provenance** | `repo@sha:path`, so every claim can be re-derived |

## The code bases this base was read against

| repo | state read | role |
|---|---|---|
| [x3d_mcp](https://github.com/hagopjay/x3d_mcp) (validator fork) | `x3d_mcp@b4efcd3` | the exact oracle: XSD plus semantic rules, exact-fix hints, 53 tools |
| [x3d-blender-io](https://github.com/hagopjay/x3d-blender-io) | `x3d-blender-io@ab99988` | Blender add-on, fidelity rig, glb gate |
| [x3d.loom](https://github.com/hagopjay/x3d.loom) | `x3d.loom@162ab18` | the method: laws, failure modes, playbooks, bridges, physics |
| [x3d.demo](https://github.com/hagopjay/x3d.demo) | `x3d.demo@d10b457` | append-only demo shelf |
| [x3d.castle](https://github.com/hagopjay/x3d.castle) | `x3d.castle@d70e00c` | Castle engine scout, exporter, quality leg |
| [x3d.xray](https://github.com/hagopjay/x3d.xray) | `x3d.xray@8fa6845` | EDA, gallery and code-city over X3D code bases |
| [x3d.onto](https://github.com/hagopjay/x3d.onto) | see [its teardown](../x3d.onto/MASTERCLASS.md) | the X3D Ontology in 3D |

## Run it yourself, for free

```bash
git clone https://github.com/hagopjay/x3d.docs && cd x3d.docs
pip install markdown-it-py mdit-py-plugins
python3 docs/tools-shared/check_learn.py --warn --summary   # lint: template, grades, ids, drills, leak sweep
python3 docs/tools-shared/build_learn.py                    # ledgers (Appendices A, C, D, E, F) + HTML
python3 -m http.server -d docs 8000                         # open http://localhost:8000/learn/
```

Everything uses free tools. No chapter requires a GPU, a paid API or an Unreal install; where a claim does (chapter 12), it says *read, not run* and gives the test that would promote it.

## Grow it

This base is meant to be curated continuously. The loop is in [AUTHORING](AUTHORING.md) section 6: observe, write the rule with the lowest grade the evidence allows,
name the instrument, add a drill that would have caught it, rebuild, log it in the [changelog](CHANGELOG.md). A later measurement that contradicts a [C] row demotes it and records both numbers.
