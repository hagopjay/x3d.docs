# 26. Lenses on a chess board: a claim is not a picture

> **Say it:** An overlay is a claim, so give each one a named question, an exact quantity and an instrument; test it against a library that shares no code with it, not against a twin; keep the geometric, the legal, the engine and the estimated apart; paint after the last `await` behind a revision and an epoch; hold the thing you analyze still; and say what a software-GL browser run cannot show. **[C]**

| field | value |
|---|---|
| chapter code | `LNS` |
| prerequisites | [02 Loom laws](02-loom-laws.md) for witness and gate; [03 Validator and gates](03-validator-and-gates.md) for the pinned XSD and semantic pass; [06 X_ITE, the oracle](06-xite-the-oracle.md) for what a browser run can and cannot say; [25 Accretion](25-accretion-gated-growth.md) for the habit of a parity test and a tamper table |
| after this you can | (1) write the question, quantity and instrument for an overlay before drawing it; (2) tell an independent oracle from a twin and say what each catches; (3) keep attack count, legal move, engine line and static exchange apart on one square; (4) write an async SAI paint that cannot commit onto a newer position; (5) say why a live game makes an analysis stale and what an honest fix costs; (6) make an overlay that does not steal picks, and read a picked square from a PROTO field; (7) split a claim between a Node run and a native-browser run |
| sources read | `x3d.chess@9eb14e9` (branch `claude/project-thread-2j8j26`, pull request 7 on `hagopjay/x3d.chess`): `docs/LENSES.md`, `docs/RESULTS.md` (section "Lens overlays"), `docs/INTEGRATION-ATLAS.md`, `docs/CHESS-REVIEW.md`, `evidence/lens-smoke.json`, the module headers and code of `viewer/js/{terrain,concepts,inspector,branches,skyline,lenses,wasm-transport,scene,main}.js`, `tools/{terrain,concepts,inspector,branches,skyline}-test.mjs`, `tools/transport-tests.mjs`, `tools/lens-smoke.mjs`, `tools/concepts_gen.py`, `tools/inspector_expect.py`, `tools/gen_grid.py` |
| instruments used | `x3d.chess@9eb14e9`; Node v22.23.5; `python-chess 1.11.2` as the oracle; the pinned `x3d_mcp` validator vendored in `x3d.chess` (XSD 4.0, semantic vocabulary 4.1) as the repository's own tests call it; vendored Stockfish WASM run as a UCI process under Node; for the browser rows: `Chromium 153.0.8010.12, SwiftShader` (software GL) with Playwright 1.63.0, read from the recorded receipt and not re-run here; no GPU; X_ITE as vendored in the repository |

A chess viewer is a small place to learn a large lesson. Five optional overlays sit on top of a grid of live games: a terrain of attack pressure, a lens for named concepts, a square inspector, engine lines drawn as arcs, and a skyline of every board's score. Each one is easy to draw and easy to draw wrongly, because a coloured column looks the same whether it counts attackers, legal moves or an engine's opinion. This chapter reads the change that added them, re-runs the checks that can be re-run here, and records what an adversarial review found. It teaches the method; it does not advertise the viewer.

---

## 1. The map

```text
   FEN of one board (the only input every lens shares)
        |
        +--> terrain    attack-count balance      height = abs(balance), colour = sign
        +--> concepts   13 rules, one per view    flags on squares, SEE is an estimate
        +--> inspector  relations of ONE square   attackers, defenders, legal, pins, x-rays
        +--> branches   engine MultiPV 3, d10     arcs; each PV replayed legally first
        +--> skyline    last score per board      column per board, 60-ply ribbon
                |
   per lens: create once -> await -> [revision + epoch check] -> paint synchronously
                |
   proof tiers (strongest first)
      python-chess oracle under Node
      hand-derived known answers
      pinned XSD and semantic validator
      native Chromium smoke (SwiftShader): no GPU, no frame-rate claim
```

| in scope | out of scope |
|---|---|
| the five lenses' questions, quantities and instruments; the oracle design and its numbers; the eight defects the adversarial review found; the async paint pattern; the hold-to-analyze finding; picking; native versus Node evidence | chess strength; engine tuning; the server transport (it has no analysis endpoint, per `docs/LENSES.md`); frame rate or any GPU measurement; the earlier chess chapters of the viewer (rule studies, export) except where a lens reuses them |

| Loom term ([02](02-loom-laws.md)) | here | note |
|---|---|---|
| witness | an independent library (python-chess), a real engine, the pinned validator, a native run | each is a different instrument; none is a proof of the others |
| gate | the aggregate test plus the native smoke in CI, per the commit message of the earlier integration | the CI wiring was read, not run here |
| receipt | `evidence/lens-smoke.json`, schema `x3dchess.browser-smoke/1` | its own `scope` line says a blocked browser is not a pass |

Read next: deeper, [06 X_ITE, the oracle](06-xite-the-oracle.md) for what a rendered browser run can say; wider, [25 Accretion](25-accretion-gated-growth.md) for a second case of a parity test plus a tamper table.

---

## 2. A claim is not a picture: question, quantity, instrument

Before a lens draws anything it must say three things: the **question** a person would ask, the **exact quantity** on screen, and the **instrument** that produced it. `docs/LENSES.md` carries one row per lens with an "honest label" cell; this table is the same information cut into those three, plus the thing the lens is not.

| lens | question | exact quantity | instrument | it is not |
|---|---|---|---|---|
| terrain, count mode | where is attack pressure concentrated | abs(white attackers minus black attackers) on the square, capped at 6 | geometric attackers from chess.js, via `controlGrid()` in `analysis.js`; pins still count | legal mobility, an exchange value, an engine score |
| terrain, material mode | same, weighted | abs(sum of white attacker values minus sum of black), P1 N3 B3 R5 Q9, K0, capped at 12 | same geometry, a value table | static exchange evaluation |
| concepts (13) | which structural or tactical fact is true here | one rule per picture, for example hanging piece, isolated pawn, outpost | the repository's own board model; chess.js only validates the FEN and counts legal moves for the side to move | a verdict; none looks ahead |
| concepts, SEE | what does a capture sequence on this square estimate | a swap-list gain on one square | iterative swap list over a private occupancy array | "wins": it ignores pins, checks, promotion and en passant |
| inspector | what touches this square, and which relations are legal | attackers and defenders (geometric), legal destinations (chess.js), absolute pins, x-ray batteries | chess.js attackers and verbose legal moves | mobility; an engine view |
| engine lines | what does the engine prefer here | up to three principal variations, MultiPV 3, depth 10 in the app, scores from White's side | the vendored Stockfish WASM, each PV replayed legally in chess.js before drawing | a move tree, a proof that an alternative loses |
| skyline | how are all boards doing at once | height `clamp(cp/100, -6, 6) x 0.4` of the last accepted score record; typed mate; hollow for a bound; grey slab for no score | the producer's score record, per `docs/PROTOCOL.md` | a win probability |

Why the split matters is visible on one square. Take the position `k7/8/8/r4pPK/8/8/8/8 w - f6 0 1`, the repository's own example in `docs/CHESS-REVIEW.md`. White's pawn on g5 can capture the pawn on f5 en passant onto f6, but the white king on h5 and the black rook on a5 stand on one rank, so removing both pawns would expose the king. Four instruments, one square (f6), four different answers:

| instrument | question put to f6 | answer | where it comes from |
|---|---|---|---|
| attack count (terrain) | white attackers minus black attackers | +1: g5 attacks f6, nothing black does | `controlGrid`, inspector `control.balance`, python-chess `attackers` (1 white, 0 black) |
| geometric relation (inspector) | does g5 attack f6 | yes, pseudo-legal | python-chess `pseudo_legal_moves` contains `g5f6` |
| legal move (inspector) | may g5 play to f6 | no: `attackLegalToPlay` is `false`, and f6 is in no legal destination list | chess.js and python-chess both list exactly four legal moves, none to f6: `g5g6 h5g6 h5h4 h5h6` (drill D-LNS-5) |
| engine line | what would the engine play | not asked; and a PV through g5f6 would be rejected by the legal replay | `verifyLine` in `branches.js` |

The terrain would paint f6 as white-ahead and the inspector would dim the g5 ray, and both are correct, because they answer different questions. A lens that merged them would be wrong whichever it chose. [C] `x3d.chess@9eb14e9`, Node v22.23.5, python-chess 1.11.2 (drill D-LNS-5).

```text
   same square, increasing commitment                  what can be wrong
   ---------------------------------------------------------------------------------
   attack count    "who points at it"                  ignores pins, turn, check
   legal move      "who may go there now"              exact for the side to move only
   static exchange "what a swap sequence nets"         ignores pins, checks, promotion
   engine PV       "what a search at depth d chose"    depth, hash, bound; one run
   skyline score   "last score a producer reported"    needs a bound and an identity
```

Three details of that ladder are code, not prose.

* `attackLegalToPlay` is three-valued: `true`, `false` or `null`. It is `null` when there is no move to ask about: the target holds the enemy king (that is a check, not a move), an own piece (a defender), or an empty square that a pawn only controls diagonally. For the colour not on move it means "if that colour were to move", with the en passant right dropped (header of `inspector.js`). [C]
* A score keeps four things apart: `engine_cp`, `engine_mate`, `unavailable`, and a bound (`exact`, `lowerbound`, `upperbound`, `null`). A missing score is a grey slab, never a zero. [C] `branches.js`, `skyline.js` headers.
* A result is bound to the FEN it searched. A result for any other FEN is dropped (`acceptResult`). [C]

---

## 3. An independent oracle versus parity with your own twin

A **twin** is a second implementation written by the same hand from the same idea. Agreement between module and twin shows that the two were typed the same way; it cannot show that either is right. An **oracle** shares no code and, ideally, no algorithm with the module. This repository's tests are explicit about it: the header of `tools/concepts_gen.py` says it computes everything with python-chess and "a recursive, board-copying SEE", where the JavaScript uses "an iterative swap-list over a private occupancy array", and that "none of it shares code or an algorithm with the JavaScript module".

| expectation source | what it catches | what it cannot | used for |
|---|---|---|---|
| twin (same author, same algorithm) | typing slips, refactor drift | a shared misreading of the rule | not relied on here |
| hand-derived answer (a comment gives the reasoning) | a misreading you can state | cases nobody thought of | classic positions, geometry coordinates, skyline curve |
| independent library (python-chess) | any disagreement over thousands of generated cases | python-chess's own bugs; rules the library does not define (a "backward pawn") | attack counts, legal sets, SEE |
| real engine (vendored Stockfish WASM under Node) | a parser that fails on real output; a PV that is not legal | engine strength; Worker start-up in a browser | `branches.js` |
| pinned XSD and semantic validator | invalid X3D | whether it looks right | every generated document |
| negative control (a mutated fixture) | an oracle that always says yes | nothing by itself | all of the above |

The numbers, each re-run on 2026-11-18 with Node v22.23.5 and python-chess 1.11.2 (`pip install chess`, `CHESS_TEST_PYTHON=python3`):

| lens | command | result | oracle |
|---|---|---|---|
| terrain | `node tools/terrain-test.mjs` | 609 checks, both modes, XSD and semantic pass | python-chess attack counts, plus hand-derived grids |
| concepts | `CHESS_TEST_PYTHON=python3 node tools/concepts-test.mjs` | 50,112 checks over 327 positions (300 random from seed 20261117 plus 27 classic, per `concepts_gen.py` and the test) | python-chess `attackers_mask`, `attacks_mask`, `legal_moves`, a board-copying SEE |
| inspector | `CHESS_TEST_PYTHON=python3 node tools/inspector-test.mjs` | 35 tests; 100 seeded positions x 64 squares; the expectation file is regenerated and compared byte for byte | python-chess legal moves, attackers and pins |
| branches | `node tools/branches-test.mjs` | 9 test groups, including real Stockfish WASM at MultiPV 3, depth 8 | python-chess checks that every PV move is legal and that the first move of a mate line mates |
| skyline | `node tools/skyline-test.mjs` | 3,360 checks, 1 to 64 boards, 7 documents validated | hand-derived curve, ribbon geometry, the pinned validator |
| transport | `node tools/transport-tests.mjs` | 17 tests, 17 pass, 0 fail | scripted workers |

Four design choices in those tests are worth copying.

1. **The oracle is pinned and the expectation is checked in.** `inspector_expect.py` uses a fixed seed and its output is committed as `tools/inspector-expect.json`; the test regenerates it and fails if the bytes differ. A changed python-chess or a changed seed cannot slide past quietly. [C] `tools/inspector-test.mjs` (the assertion "committed expectation file is not what the fixed-seed generator produces").
2. **Coverage is counted, not hoped for.** The inspector test tallies what its 6,400 square comparisons actually contained: en passant moves 21, castles 21, promotions 92, checks 20, pinned pieces 12, geometric attacks that are illegal 698, and attacks that have no move to ask about 4,080, and asserts floors (for example at least 10 en passant, at least 100 illegal attackers). A random test that never meets a pin proves nothing about pins. [C] run of 2026-11-18.
3. **Metamorphic checks add cases the generator did not write.** The concepts test mirrors files and flips colours on 1,507 positions and requires the same answers under the symmetry. [C] same run.
4. **Negative controls.** The concepts test mutates 19 fixtures and requires each to be detected; the terrain test corrupts a grid and requires disagreement with python-chess; the branches test corrupts one PV and requires exactly one rejection and two surviving lines. A green test that cannot go red is decoration. [C]

One disagreement between sources, recorded as the contract asks. `docs/LENSES.md` and `docs/RESULTS.md` say the real-engine check ran "on three FENs"; the test itself says `4 FENs x multipv 3 depth 8` and defines four cases (a black queen-up and a white queen-down position, and a white and a black back-rank mate in one). The code supports four; the prose is the loser and is graded [S]. The documents also say depth 8 for the native run in one row and depth 10 in another: the query `depth=8` sets the game arena, while the "Engine lines" button asks for `{multipv:3, depth:10}` (`viewer/js/main.js`), and the receipt's labels read `d10`. Both are true; they are two different searches. [C]

---

## 4. Eight defects the adversarial review found, and what each teaches

`docs/LENSES.md` states that "adversarial review per module fixed real defects, each with a regression test", and lists eight. The tree at `9eb14e9` holds the fixed code and the regression tests, not the code before the fix, so what each defect did before is read from the test comments and the list ([L]); that the test now exists and passes is run ([C]).

| # | defect (as listed) | regression test | what it teaches |
|---|---|---|---|
| 1 | `groupFlat` could loop forever on `k=0` | `tools/terrain-test.mjs` "6b": `groupFlat([1,2,3],0)` must throw "positive integer"; also non-integer `k`, ragged length, non-array input | a loop whose step is a parameter needs the parameter validated; the test names the bad inputs one by one |
| 2 | a UCI `wdl` field made a lowerbound read as exact | `tools/branches-test.mjs` line 35: "Stockfish prints wdl BEFORE the bound; the bound used to be dropped" | a parser must accept optional tokens in any order the producer can emit; read real output, not the grammar you remember |
| 3 | arc apexes sat off the drawn path | `tools/branches-test.mjs` lines 137 to 140: every apex lies on the x/z midpoint of consecutive squares | state a geometric invariant and test it on every vertex, not on one example |
| 4 | a duplicate rank was labelled but never drawn | `viewer/js/branches.js` line 209 (`seenRanks`), test at line 134 | a label and a drawing must come from one list; otherwise a number appears with nothing under it |
| 5 | defender rays were dimmed as if illegal | `tools/inspector-test.mjs` lines 407 to 415 | "not applicable" is not "no": the answer is three-valued, and `null` must not render as `false` |
| 6 | small negative scores were drawn above the baseline and rounded to "0.0" | `tools/skyline-test.mjs` line 187 and `viewer/js/skyline.js` line 203 | sign survives rounding and clamping; test -4 centipawns, not only -250 |
| 7 | a reported 0 cp vanished on the ribbon | `tools/skyline-test.mjs` lines 188 to 192: an isolated exact zero is a hairline tick, not a gap | a value of zero and a missing value are different things; the sentinel must not collide with a measurement |
| 8 | concept flags spilled onto neighbouring squares | `tools/concepts-test.mjs` lines 290 to 300: every pole and vertex inside its own square (abs(dx), abs(dz) under 0.5) and on the board | an annotation must be contained by the thing it annotates; the old pennant spilled 0.16 off the h-file |

Defects 2 and 5 are the same family as the `PhysicalMaterial` disagreement in [chapter 25](25-accretion-gated-growth.md): a component that is right under its own vocabulary and wrong under its neighbour's. Defects 6 and 7 are two ends of one problem, the neighbourhood of zero. Defect 4 is a count that was kept in two places.

### 4.1 Two defects reproduced by deleting the guard

A regression test is only worth the failure it would have caught. Two of the eight can be re-created in a scratch copy by deleting the line that fixes them; the repository is not touched.

```bash
# from a checkout of x3d.chess at 9eb14e9
T=$(mktemp -d); mkdir -p "$T/viewer/js"; ln -s "$PWD/viewer/vendor" "$T/viewer/vendor"
cp viewer/js/branches.js viewer/js/terrain.js viewer/js/analysis.js "$T/viewer/js/"

# defect 2: drop the wdl branch -> the bound is lost
sed -i '/t\[i\] === "wdl"/d' "$T/viewer/js/branches.js"
node --input-type=module -e "import('$T/viewer/js/branches.js').then(m=>console.log(m.parseInfoLine('info depth 9 score cp 7 wdl 400 500 100 lowerbound nodes 5 pv e2e4').bound))"
# defect 1: drop the k guard -> k=0 never terminates (here it exhausts a 200 MB heap)
sed -i '/k must be a positive integer/d' "$T/viewer/js/terrain.js"
node --max-old-space-size=200 --input-type=module -e "import('$T/viewer/js/terrain.js').then(m=>console.log(m.groupFlat([1,2,3],0).length))"; echo exit=$?
```

On the unmodified tree the first prints `lowerbound`; on the mutated copy it prints `exact`. The second throws `RangeError: groupFlat: k must be a positive integer` on the real tree; on the mutated copy it aborts with `FATAL ERROR: Reached heap limit` (exit 134), because `a.length % 0` is `NaN`, which is falsy, so the length check does not catch it and the loop `i += 0` pushes an empty slice forever. A spinning loop and an out-of-memory abort are the same defect seen at different heap sizes. [C] `x3d.chess@9eb14e9`, Node v22.23.5, 2026-11-18.

---

## 5. Async SAI: create once, paint synchronously after the last await

Every overlay is an X3D fragment. `browser.createX3DFromString` is asynchronous, so the paint has a gap in the middle in which the board can move, reset or be disposed. `lenses.js` fixes the shape of every lens in one sentence: "created once, painted synchronously after its last `await`, and guarded by a per-lens revision plus the board's epoch".

```text
   request (FEN, square, result)
       |  rev = ++this.rev.<lens>          <- bumped BEFORE any await
       |  epoch = view.epoch               <- captured BEFORE any await
       |  compute geometry (pure, sync)
       v
   await this._mount(name, xml)            <- the ONLY await; single-flight, created once
       |
       |  if (!s || !alive(epoch) || rev !== this.rev.<lens>
       |      || view.lastFen !== fenSearched) return false
       v
   write SAI fields (no await from here to the end)      <- nothing can interleave
```

| piece | what it does | where | grade |
|---|---|---|---|
| single-flight mount | `mounts` is a map name to promise; a second request waits on the same promise; a failure deletes the entry so a retry can recreate it | `BoardLens._mount` | [C] read |
| revision | a per-lens counter; a newer request wins | `rev.terrain`, `rev.concepts`, `rev.insp`, `rev.branches`, `rev.ribbon` | [C] read |
| epoch | the board's generation; reset or dispose bumps it | `view.epoch`, `_alive(epoch)` | [C] read |
| FEN check | branches also require `view.lastFen === result.fenSearched` after the await | `showBranches` | [C] read |
| pending set | `_track` keeps unfinished paints so a test or a dispose can wait for them | `BoardLens._track` | [C] read |
| inspector | `selectSquare` bumps the revision before the await; `acceptInspection` is the check after it | `inspector.js`, `_paintInspection` | [C] read |

The rule that matters is the position of the check: **after** the last `await`, never before it. A check placed before the await guards nothing, because the world can change during the await. The documentation of `concepts.js` says it in a line comment ("the ONLY await: the staleness check must come after it"), and the same file notes that a hand-made empty report is refused rather than silently drawn.

What is tested and what is not. The pure parts have strong tests: `inspectionStaleReason`, `skylineUpdate` (it rejects an older generation and a non-increasing sequence number, and a rejected update never advances the guards), `acceptResult`. The controller `BoardLens` itself, where the awaits live, is imported by no Node test (a search of `tools/*.mjs` for `lenses.js` finds no match); it is exercised only by the native smoke, which presses each lens and does not race one. So the pattern is read and is working in one browser run; it has no adversarial race test. [C] for the search, [S] that the pattern holds under a real race.

---

## 6. Hold the game to analyze

A live arena moves every board within a second or so. An engine search takes longer than that. The first native run is reported to have lost the lines: each search finished against a FEN that was no longer on the board, so the stale-result guard did the right thing and dropped it, and nothing was drawn. `docs/LENSES.md` records the reason in one sentence ("Without a hold, a live game moves within a second and every result would be stale"); the first-run observation itself is carried from the hand-off for this chapter and no receipt in the repository records the failed run, so it is [L], and the sentence in `LENSES.md` is [C] as a statement of the design.

The options, and what each costs:

| fix | cost | verdict |
|---|---|---|
| loosen the guard and draw lines on whatever FEN is now on the board | the arcs describe a position the board is no longer in; the stale guard exists to forbid exactly this | wrong |
| draw lines on a frozen copy of the position beside the live board | a second board, more scene, more code; not built | a fair option, [S] |
| **hold the focused game before its next move is applied, analyze, release** | the observed game stops while held, so the lens changes what it observes | chosen |

The mechanism is small. `WasmTransport.holdGame(id)` installs a promise on the game and returns the held FEN; the game loop awaits it before applying its next move; `releaseGame(id)` resolves it. The transport test is honest about the one gap: "at most the in-flight move may land after the hold". So `main.js` waits for the board to catch up (up to 40 polls of 100 ms, 4 s) and if the board still differs from the held FEN it releases and refuses ("The board had not caught up with its game; try again") instead of drawing. The button label says what happened ("g0 paused so the position stays still") and pressing the button again clears the lines and resumes. The transport test `holdGame freezes a game at its current FEN until released, then play resumes` passes (17 of 17 in `transport-tests.mjs`), and the native receipt step `engine-lines` shows three labels on a held game, `#1 d10 cp -74 (White POV) Nd7`, `#2 d10 cp -71 ... h5`, `#3 d10 cp -70 ... Bd7`; the smoke script asserts that the game is held while the lines show and released after the second press. [C] for the test and the script text, [L] for the receipt run (read, not re-run).

The lesson generalises: when an analysis must describe a state, make the state stop, say so on screen, and keep the guard strict. Relaxing the guard to make the picture appear would have turned a missing overlay into a wrong one.

---

## 7. Picking: effect shapes must not catch the pointer

Every board is a PROTO with a TouchSensor inside it. An overlay drawn above the board is a new surface; if it can be hit, it takes the click that was meant for the board. Two rules keep picking working.

1. **Every overlay and effect shape is created with `pointerEvents='false'`.** It is in the generated XML of the concepts (`concepts.js` lines 417 and 418), the branches (`branches.js` line 237), the effects (`fx.js` lines 8 and 16) and the terrain (its header: one Shape with `pointerEvents=false, visible=false`). [C] read.
2. **The board PROTO exposes the hit point.** `tools/gen_grid.py` adds `<field accessType='outputOnly' type='SFVec3f' name='hitPoint'/>` to the PROTO and routes the sensor's `hitPoint_changed` into it with an `IS`/`connect`. The scene registers a field callback on that field, keeps the last point per board, and, on `touchTime`, converts it with `squareAt` ("TouchSensor hit point is board-local: files along +x, rank 1 at +z") and calls the inspector. A PROTO hides its inner nodes; without an outputOnly field the scene cannot read what the sensor saw. [C] read.

The ordering assumption is real: the handler reads the stored hit point when `touchTime` fires, so it assumes `hitPoint_changed` arrived first. The native receipt step `inspector-click` (a real mouse click at 45% by 55% of the canvas) reports board 0 selected and square `d4` inspected, which is one observation that the order holds in that browser, not a statement about the order in the standard. [L]

`pointerEvents` is an X_ITE picking extension, not an X3D 4.0 field. The portable export removes it and says so: `export.js` strips the attribute and reports a loss `Shape.pointerEvents ... X_ITE picking extension omitted from portable X3D`. So the picking rule belongs to the live viewer only, and the exported file must not be expected to behave the same way in another browser. [C] read.

---

## 8. Native browser evidence versus Node evidence

Two tiers of evidence, and a sentence for what each cannot say.

| tier | what it ran | it can say | it cannot say |
|---|---|---|---|
| Node, pure logic | module functions on FENs; python-chess oracle; the pinned validator on generated documents | the numbers are right for the rule; the XML is valid; PVs are legal | that anything was drawn, picked, or readable |
| Node, real engine | vendored Stockfish WASM as a UCI child process (`NodeUciWorker`) | the parser and the legal replay survive real output | that a Worker starts in a browser (`docs/INTEGRATION-ATLAS.md`: "WASM Worker initialization must run in the browser; Node UCI execution cannot close that part") |
| native browser, software GL | `tools/lens-smoke.mjs` in Chromium 153.0.8010.12 with SwiftShader, Playwright 1.63.0, 8 boards, `?engine=wasm&boards=8&depth=8&pool=2` | each lens mounts and toggles; 13 concepts cycled; inspector by key (`f4`) and by real click (`d4`); 3 engine labels with the game held; 8 skyline columns including a typed mate `+M1`; 192 pieces, 0 misplaced, 0 console errors | frame rate, GPU precision, depth-sorting of translucent columns on real hardware, label legibility, pixel parity, behaviour with 20 boards |

The receipt is `evidence/lens-smoke.json`, schema `x3dchess.browser-smoke/1`, status `pass`, `errors: []`, started 2026-11-18T03:03:18Z. Its own scope line is the discipline in one sentence: "Native X_ITE UI/geometry check when executed. A blocked browser is not a pass." The smoke asserts through the page's own state (`need(...)` on DOM text, node counts and the held flag), not through pixels; a screenshot is saved but never compared.

`docs/LENSES.md` closes with the honest part: terrain and concepts repaint on every move of every board when on; with 20 boards on software GL that costs frames; "measure on real hardware before relying on it". The terrain and the heat overlay also share a plane, so only one should be shown at a time. Neither of those is something SwiftShader can settle. [C] read; the receipt rows [L] (read, not re-run here).

---

## 9. What is missing, ranked

| rank | gap | why it matters | grade |
|---|---|---|---|
| 1 | no race test for `BoardLens` | the async guards are the claim of section 5 and only a happy-path browser run touches them | [C] absent |
| 2 | no GPU run | translucent columns, label size and frame cost are unmeasured | [C] absent |
| 3 | the first-run lost-lines finding has no receipt | a finding that drove a design change should be recorded as a run | [L] |
| 4 | depth and FEN count differ between prose and test | small, but a reader quoting "three FENs" quotes the loser | [C] |
| 5 | the server transport has no analysis endpoint | engine lines work only with `engine=wasm` | [C] read |
| 6 | the eight defects have no before-fix tree to re-run | section 4.1 reproduces two by deleting a guard; six are read from comments | [C] |

## 10. When the library lacks the rule: Chess960 castling [C]

chess.js 1.4 cannot castle in Chess960 and, worse, emits a wrong `O-O` for a king on b1 with rooks on a1 and f1. The port keeps chess.js for every ordinary move and adds only what is missing, then lets an independent oracle say whether that is enough.

* **Hide the unsupported rule from the library.** Load every position with castling `-`, so chess.js can never emit a wrong castle, and keep the real rights (one rook file per side per colour) in a wrapper. `fen()` stays chess.js-readable for every overlay; a second `fen960()` carries Shredder letters for Stockfish and python-chess.
* **Reuse the library's own turn passing.** A castle is two `remove` and two `put` calls plus chess.js's null move, so the move number, half-move clock and history stay right with no private bookkeeping.
* **Check the final position, not just the path.** Moving the castling rook can open a line onto the king (king c1, rook b1, enemy rook a1). A path-only rule accepts it; the wrapper tries the castle on a scratch board and asks `isAttacked`.
* **Compare to the oracle at every ply.** python-chess `chess960=True` played castling-biased games (260 games, 25,465 plies, 235 castles, all four kinds); the wrapper's legal-move set, SAN, FEN and seven terminal flags matched at every ply. A spot-check list could not have found the shielded-rook case or the castle-only stalemate that chess.js would call a stalemate by mistake.
* **Keep encodings separate.** The engine speaks king-takes-own-rook (`e1h1`); the board highlights king to destination. Events carry both (`uci`, `engine_uci`), and engine lines are verified against the Shredder FEN so a castling line is drawn instead of dropped.

Instrument: `x3d.chess` `tools/chess960-test.mjs` with python-chess 1.11.2, Node 22, vendored Stockfish 19 lite WASM under Node and in Chromium 153 (SwiftShader). Not measured: hardware GPU, frame rate, and the lenses' analysis of castling rights, which read the compat FEN.

---

## Heuristics

| ID | Rule | Grade | Evidence | Instrument |
|---|---|---|---|---|
| H-LNS-1 | Before drawing an overlay, write its question, its exact quantity and its instrument; if one of the three is missing, the overlay is a picture, not a claim. | C | the lens table of `docs/LENSES.md` has an honest-label cell per lens; the legends are asserted in tests | `x3d.chess@9eb14e9:docs/LENSES.md` |
| H-LNS-2 | Keep attack count, legal move, static exchange and engine line apart on one square; never merge two into one colour. | C | at f6: balance +1, attacker g5 pseudo-legal, move g5f6 illegal | inspector, python-chess 1.11.2, drill D-LNS-5 |
| H-LNS-3 | Return `null`, not `false`, when the question does not apply; render `null` neutrally. | C | defender and pawn-diagonal cases are `null` (defect 5); 4,080 such attackers in the 100-position run | `tools/inspector-test.mjs`, run 2026-11-18 |
| H-LNS-4 | Test against a library that shares no code or algorithm with the module; agreement with a twin is parity, not correctness. | C | a board-copying SEE against an iterative swap list; 50,112 checks, 0 disagreements | `tools/concepts-test.mjs`, python-chess 1.11.2 |
| H-LNS-5 | Commit the oracle's expectation file and regenerate it in the test; fail on a byte difference. | C | inspector expectation file, fixed seed | `tools/inspector-test.mjs` |
| H-LNS-6 | Count what a random test actually met and assert floors; a test that never meets a pin says nothing about pins. | C | 21 en passant, 21 castles, 92 promotions, 12 pinned, 698 illegal attackers | `tools/inspector-test.mjs` coverage block |
| H-LNS-7 | Give every oracle a negative control: a mutated fixture it must reject. | C | 19 mutated concept fixtures detected; corrupted PV gives exactly 1 rejection | `tools/concepts-test.mjs`, `tools/branches-test.mjs` |
| H-LNS-8 | Parse a producer's output by reading real output, and accept optional tokens in any order it can emit. | C | `wdl` before `lowerbound` turned a bound into `exact` when the branch was deleted | scratch mutation, section 4.1 |
| H-LNS-9 | Validate any loop-step parameter; a falsy length check does not catch a zero step. | C | `[1,2,3].length % 0` is NaN; the guard removed gives a heap abort, exit 134 | scratch mutation, Node v22.23.5 |
| H-LNS-10 | Treat the neighbourhood of zero as its own test case: -4 cp, 0 cp and a missing score must look different. | C | labels `+0.0`, `-0.0`, `0.0`; cap below baseline for -4 cp; zero is a hairline tick | `tools/skyline-test.mjs` line 187, run |
| H-LNS-11 | Put the staleness check after the last `await`, and bump the revision before the first. | C | `showBranches`, `_paintInspection`, header of `concepts.js` | `x3d.chess@9eb14e9:viewer/js/lenses.js`, read |
| H-LNS-12 | When an analysis must describe a state, hold the state, say so on screen, and keep the guard strict. | L | held game test passes; the lost-lines first run is carried from a hand-off, not a receipt | `tools/transport-tests.mjs`, 17 of 17 |
| H-LNS-13 | Create every overlay shape with `pointerEvents='false'`, and expose the picked point through an outputOnly PROTO field. | C | all overlay generators carry it; `hitPoint` in the board PROTO | `viewer/js/*.js`, `tools/gen_grid.py`, read |
| H-LNS-14 | Say in the receipt what a blocked or software-GL run cannot show; never read a pass as a frame-rate or pixel claim. | C | receipt `scope` line; `docs/LENSES.md` limits | `evidence/lens-smoke.json`, Chromium 153.0.8010.12 SwiftShader |
| H-LNS-15 | When prose and test disagree on a number, quote the test and grade the prose [S]. | C | "three FENs" in two documents, four in the test | `tools/branches-test.mjs` line 298 |

---

## Drills

Each drill runs from a checkout of `x3d.chess` at `9eb14e9` with Node 22 or newer. Drills that use the oracle need `pip install chess` (python-chess 1.11.2) and `CHESS_TEST_PYTHON=python3`. The checkout is read-only for every drill; mutations go to a `mktemp -d` copy.

### D-LNS-1 Count the lenses and the concepts
- **Level:** L1
- **Task:** How many concept identifiers does `concepts.js` export, and which one is the static exchange estimate?
- **Verify:** `node --input-type=module -e "import('./viewer/js/concepts.js').then(m=>console.log(m.CONCEPT_IDS.length, m.CONCEPT_IDS.join(' ')))"`
- **Answer:** 13: `hanging see isolated doubled passed backward connected outpost openFiles halfOpenFiles rookFile kingZone bishopPair`. The static exchange estimate is `see`.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5

### D-LNS-2 Re-run the oracles
- **Level:** L2
- **Task:** Run the terrain, concepts and skyline tests and record each tool's own count line. Then run the concepts test without `CHESS_TEST_PYTHON` and say what happens.
- **Verify:** `node tools/terrain-test.mjs`, `CHESS_TEST_PYTHON=python3 node tools/concepts-test.mjs`, `node tools/skyline-test.mjs`; then `node tools/concepts-test.mjs` unset.
- **Answer:** terrain `"checks":609`; concepts `"checks":50112,"positions":327`; skyline `"checks":3360,"validated_documents":7`. Without the variable the concepts test prints `FAIL: CHESS_TEST_PYTHON is not set; the independent oracle cannot be run` and does not pass: the oracle is required, not optional.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5, python-chess 1.11.2

### D-LNS-3 Delete the wdl branch
- **Level:** L3
- **Task:** Reproduce defect 2: in a scratch copy of `branches.js`, delete the `wdl` branch of `parseInfoLine`, parse `info depth 9 score cp 7 wdl 400 500 100 lowerbound nodes 5 pv e2e4`, and compare the `bound` with the real module. Then say which existing test would turn red and why.
- **Verify:** the first script of section 4.1.
- **Answer:** real module `lowerbound`, mutated copy `exact`. `tools/branches-test.mjs` line 36 feeds three orderings of `wdl` and the bound (`lowerbound` after `wdl`, `upperbound` before `wdl`, and no bound, expecting `exact`) and asserts each; the first would read `exact` and fail. The fix matters because an engine search that stops at a bound is not an exact score.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5, scratch copy

### D-LNS-4 Delete the k guard
- **Level:** L3
- **Task:** Reproduce defect 1: call `groupFlat([1,2,3],0)` on the real module and on a copy with the guard line deleted, under `--max-old-space-size=200`. Explain why the length check does not catch it.
- **Verify:** the second script of section 4.1.
- **Answer:** real module throws `RangeError: groupFlat: k must be a positive integer`; the mutated copy aborts with `Reached heap limit` and exit 134. `3 % 0` is `NaN`, which is falsy, so the line `if (a.length % k)` never fires and `i += 0` pushes empty slices without end.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5, scratch copy

### D-LNS-5 One square, four answers
- **Level:** L2
- **Task:** For `k7/8/8/r4pPK/8/8/8/8 w - f6 0 1` list the legal moves, then ask the inspector about f6 and python-chess about `g5f6`. Report the control balance, the attacker's `attackLegalToPlay` and whether `g5f6` is pseudo-legal and legal.
- **Verify:** `node --input-type=module -e "import('./viewer/vendor/chess.js').then(async({Chess})=>{const fen='k7/8/8/r4pPK/8/8/8/8 w - f6 0 1';console.log(new Chess(fen).moves({verbose:true}).map(m=>m.from+m.to).sort().join(' '));const I=await import('./viewer/js/inspector.js');const i=I.inspect(fen,'f6');console.log(i.control.balance,i.attackedBy.w.map(a=>a.square+':'+a.attackLegalToPlay).join(),i.legal.destinations.length)})"` and `python3 -c "import chess;b=chess.Board('k7/8/8/r4pPK/8/8/8/8 w - f6 0 1');m=chess.Move.from_uci('g5f6');print(sorted(x.uci() for x in b.legal_moves), m in b.pseudo_legal_moves, m in b.legal_moves)"`
- **Answer:** legal moves `g5g6 h5g6 h5h4 h5h6`. Control balance 1; attacker `g5:false`; zero destinations on f6; `g5f6` is pseudo-legal (True) and not legal (False), because removing both pawns opens the a5 to h5 rank onto the king.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, chess.js as vendored, python-chess 1.11.2

### D-LNS-6 The neighbourhood of zero
- **Level:** L2
- **Task:** Feed the skyline five scores, +5, -5, +4, -4 and 0 centipawns, and write the label and whether the cap sits above or below the baseline for each.
- **Verify:** the `eq([5,-5,4,-4,0,-250,249]...)` line of `tools/skyline-test.mjs`; or build a state with `skylineLayout`, `skylineState`, `skylineUpdate` and read `skylinePoints(...).labels`.
- **Answer:** labels `+0.1`, `-0.1`, `+0.0`, `-0.0`, `0.0`. With the baseline at y 4, the cap vertex is 4.04 for +5, +4 and 0 (the minimum thickness), and 3.96 for -5 and -4 (below). A small negative score keeps its downward sign instead of being drawn up and called zero.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5

### D-LNS-7 Count what the random test met
- **Level:** L2
- **Task:** Run the inspector test and report the coverage tally of its 100 x 64 comparisons. Which counter is named for one case but counts two?
- **Verify:** `CHESS_TEST_PYTHON=python3 node tools/inspector-test.mjs`
- **Answer:** `{"ep":21,"castle":21,"promotion":92,"check":20,"pinned":12,"illegalAttack":698,"kingTarget":4080}`; 35 tests pass. `kingTarget` increments whenever `attackLegalToPlay` is `null`, which includes defenders and pawn diagonals as well as king targets, so its name undersells it. The floors asserted are for example at least 10 en passant and at least 100 illegal attackers.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Node v22.23.5, python-chess 1.11.2

### D-LNS-8 Read the native receipt
- **Level:** L1
- **Task:** From `evidence/lens-smoke.json`, give the browser version, the number of boards and pieces, the count of misplaced pieces, the labels of the three engine lines, and the skyline label that is a typed mate.
- **Verify:** `python3 -c "import json;d=json.load(open('evidence/lens-smoke.json'));print(d['browser_version'],d['scene']['boards'],d['scene']['pieces'],d['scene']['misplaced'],[s for s in d['steps'] if s['name']=='engine-lines'][0]['labels'],[s for s in d['steps'] if s['name']=='skyline'][0]['labels'])"`
- **Answer:** `153.0.8010.12`, 8 boards, 192 pieces, 0 misplaced; labels `#1 d10 cp -74 (White POV) Nd7`, `#2 d10 cp -71 (White POV) h5`, `#3 d10 cp -70 (White POV) Bd7`; the typed mate is `+M1`.
- **Checked:** 2026-11-18 `x3d.chess@9eb14e9`, Python 3

---

## Honest limits

* **[C]** The five Node test gates were re-run on 2026-11-18 and pass with the counts quoted. The 17 transport tests pass.
* **[L]** The native browser run (`evidence/lens-smoke.json`: Chromium 153.0.8010.12, SwiftShader, Playwright 1.63.0) is read from its receipt, not re-run here; the numbers are the receipt's.
* **[L]** The statement that the first native run dropped every MultiPV result because the live game moved is carried from a hand-off note; no receipt of the failed run is in the repository. The design reason in `docs/LENSES.md` is [C] as text.
* **[L]** What each of the eight defects did before its fix is read from the regression-test comments and the list in `docs/LENSES.md`; the pre-fix tree is not in the checkout. Only defects 1 and 2 were re-created, by deleting a guard in a scratch copy.
* **[C]** No Node test imports `lenses.js`; the async guards of section 5 have no adversarial race test, only a happy-path browser run. That they hold under a real race is [S].
* **[C]** python-chess is an oracle for attack counts, legal moves and SEE; it cannot be one for "backward pawn", "outpost" or "king-zone weight", which are the repository's own definitions. The concepts test checks the rule as written, not that the rule is good chess; `docs/LENSES.md` says the definitions are "counting rules, not strategic verdicts".
* **[C]** A software-GL browser run says nothing about frame rate, GPU precision, translucent sorting, label legibility or 20-board cost; the repository says so itself.
* **[C]** `docs/LENSES.md` and `docs/RESULTS.md` say "three FENs" for the real-engine test; the test has four. Documents and test also use depth 8 (arena and test) and depth 10 (the button). The tests and code are quoted; the prose is [S].
* **[S]** That a frozen copy of the position beside the live board would be a better fix than holding the game is an expectation, not a measurement.
* **[C]** Timings were not measured and none is claimed. The CI wiring (aggregate test and native smoke) is read from the commit message, not run.

---

## Numbers register

| ID | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|
| N-LNS-1 | opt-in overlays in the change | 5 | [C] | read | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-2 | concepts in the concept lens | 13 | [C] | `CONCEPT_IDS.length`, Node v22.23.5 | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-3 | terrain checks, both modes, vs python-chess | 609 | [C] | `node tools/terrain-test.mjs`, python-chess 1.11.2 | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-4 | concepts checks; positions | 50,112; 327 | [C] | `CHESS_TEST_PYTHON=python3 node tools/concepts-test.mjs`, python-chess 1.11.2 | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-5 | concepts positions: random; classic; generator seed | 300; 27; 20261117 | [C] | `tools/concepts_gen.py` constants, 327 minus 300 | `x3d.chess@9eb14e9:tools/concepts_gen.py` |
| N-LNS-6 | inspector tests; random positions x squares | 35; 100 x 64 | [C] | `node tools/inspector-test.mjs`, python-chess 1.11.2 | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-7 | inspector run coverage: en passant; castle; promotion; check; pinned | 21; 21; 92; 20; 12 | [C] | same run, coverage block | `x3d.chess@9eb14e9:tools/inspector-test.mjs` |
| N-LNS-8 | inspector run: illegal geometric attackers; attackers with no move to ask about | 698; 4,080 | [C] | same run | `x3d.chess@9eb14e9:tools/inspector-test.mjs` |
| N-LNS-9 | branches: test groups; engine setting | 9; MultiPV 3, depth 8 | [C] | `node tools/branches-test.mjs`, vendored Stockfish under Node | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-10 | branches real-engine cases: in the prose; in the test | 3; 4 | [C] | prose loses; the test file defines four cases | `x3d.chess@9eb14e9:tools/branches-test.mjs` |
| N-LNS-11 | skyline checks; board range; documents validated | 3,360; 1 to 64; 7 | [C] | `node tools/skyline-test.mjs` | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-12 | transport tests run; passed | 17; 17 | [C] | `node tools/transport-tests.mjs`, Node v22.23.5 | `x3d.chess@9eb14e9:tools/transport-tests.mjs` |
| N-LNS-13 | mutated concept fixtures detected | 19 | [C] | concepts test, negative controls | `x3d.chess@9eb14e9:tools/concepts-test.mjs` |
| N-LNS-14 | colour-flip and file-mirror symmetry positions | 1,507 | [C] | concepts test output line | `x3d.chess@9eb14e9:tools/concepts-test.mjs` |
| N-LNS-15 | terrain caps: count mode; material mode | 6; 12 | [C] | read | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-16 | skyline height: pawns clamp; units per pawn | 6; 0.4 | [C] | read | `x3d.chess@9eb14e9:docs/LENSES.md` |
| N-LNS-17 | skyline hairline thickness for cp = 0 | 0.04 | [C] | read; test `near(capY(z,0)-baseRingY(z,0),SKY.MIN_H)` | `x3d.chess@9eb14e9:viewer/js/skyline.js` |
| N-LNS-18 | skyline labels for +5, -5, +4, -4, 0 cp | +0.1; -0.1; +0.0; -0.0; 0.0 | [C] | skyline test line 187 and a direct call, Node v22.23.5 | `x3d.chess@9eb14e9:tools/skyline-test.mjs` |
| N-LNS-19 | pennant spill before the fix (units off the h-file) | 0.16 | [L] | test comment; pre-fix tree not in the checkout | `x3d.chess@9eb14e9:tools/concepts-test.mjs` |
| N-LNS-20 | engine lines from the app button: MultiPV; depth | 3; 10 | [C] | read | `x3d.chess@9eb14e9:viewer/js/main.js` |
| N-LNS-21 | hold wait: polls; interval (ms); total (s) | 40; 100; 4 | [C] | read; total derived by multiplication | `x3d.chess@9eb14e9:viewer/js/main.js` |
| N-LNS-22 | ribbon window (plies); controller history cap | 60; 240 | [C] | read | `x3d.chess@9eb14e9:viewer/js/skyline.js` |
| N-LNS-23 | f6 position: control balance; legal moves; legal destinations on f6 | +1; 4; 0 | [C] | inspector, chess.js, python-chess 1.11.2 | `x3d.chess@9eb14e9:docs/CHESS-REVIEW.md` |
| N-LNS-24 | scratch mutation: k guard deleted, heap 200 MB: exit code | 134 | [C] | Node v22.23.5, `--max-old-space-size=200` | `x3d.chess@9eb14e9:viewer/js/terrain.js` |
| N-LNS-25 | scratch mutation: wdl branch deleted: bound read | exact | [C] | Node v22.23.5 | `x3d.chess@9eb14e9:viewer/js/branches.js` |
| N-LNS-26 | native run: boards; pieces; misplaced; console errors | 8; 192; 0; 0 | [L] | `evidence/lens-smoke.json`, Chromium 153.0.8010.12, SwiftShader, not re-run | `x3d.chess@9eb14e9:evidence/lens-smoke.json` |
| N-LNS-27 | native run: engine-line scores (cp, White POV) at depth 10 | -74; -71; -70 | [L] | same receipt | `x3d.chess@9eb14e9:evidence/lens-smoke.json` |
| N-LNS-28 | native run: concepts cycled; skyline columns | 13; 8 | [L] | same receipt | `x3d.chess@9eb14e9:evidence/lens-smoke.json` |
| N-LNS-29 | native run rig: Chromium; Playwright | 153.0.8010.12; 1.63.0 | [L] | same receipt | `x3d.chess@9eb14e9:evidence/lens-smoke.json` |
| N-LNS-30 | lens defects found by adversarial review, each with a regression test | 8 | [C] | list read; tests run | `x3d.chess@9eb14e9:docs/LENSES.md` |

---

## Sources and provenance

Read and run on 2026-11-18: `x3d.chess` at `9eb14e9`, the head of branch `claude/project-thread-2j8j26` (pull request 7 on `hagopjay/x3d.chess`, public), a merge of the lenses commit `d432fe8` with the main line. The Node gates were run from a checkout of that commit with Node v22.23.5 and python-chess 1.11.2; the scratch mutations of section 4.1 were made on copies and the checkout was left clean. The browser rows come from `evidence/lens-smoke.json` at the same commit and were not re-run in this session. Two things in this chapter were carried and not re-derived: the report that the first native run lost its engine lines, and the CI wiring described in the commit message. No private repository, private document or unpublished material was used.
