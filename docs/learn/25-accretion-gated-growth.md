# 25. Accretion: an append-only X3D world grown one gated patch at a time

> **Say it:** Grow a world by letting a deterministic planner pick the slot, any generator propose a fragment, a whitelist gate plus a pinned XSD and semantic validator admit it, and a hash-chained ledger record it; then say out loud that the chain proves self-consistency, not authorship, and that the gate is only as good as the agreement between its vocabulary and the validator's. **[C]**

| field | value |
|---|---|
| chapter code | `ACC` |
| prerequisites | [01 The tether](01-the-tether.md) for the thesis; [02 Loom laws](02-loom-laws.md) for witness, gate and receipt; [03 Validator and gates](03-validator-and-gates.md) for the XSD and semantic stages; [23 Traceability](23-traceability-lineage.md) for hash chains and what they cannot show |
| after this you can | (1) split a growing scene into planner, generator, gate and ledger and say which of them may be a model; (2) read an admission record and say what it re-checks on replay and what it does not; (3) find a vocabulary disagreement between a gate and the validator behind it with one full-pipeline test per admitted node type; (4) say where a numeric floor belongs and why Python `\d` is the wrong lexer; (5) port a verifier to a browser and prove parity with a tamper table; (6) put a Host-header guard on a loopback server |
| sources read | `x3d.accrete@93063bf` (`README.md`, `docs/GATE-CONTRACT.md`, `docs/REVIEW-2026-11-17.md`, `docs/PAGES.md`, `accretion/gate.py`, `accretion/world.py`, `web/verify-archive.js`, `tests/test_static_export.py`, `tools/build_demo.py`, `tools/pages_smoke.js`, `reports/store-scaling.json`); `x3d.accrete@52ba996` (the tree as supplied, for the before side of each fix); `x3d_mcp@b5c9956` as vendored in `x3d.accrete` (read through its adapter, not edited) |
| instruments used | Python 3.13.18, lxml 6.1.3 (libxml2 2.14.6), jsonschema 4.26.0, Node 22.23.4, 4 vCPU Linux container, no GPU; `X3D XSD 4.0` and the upstream semantic pass (4.1 UOM tables) as vendored from `x3d_mcp@b5c9956`; `X_ITE 16.6.0` bundled in the viewer; `Chromium 153.0.8010.12` (Playwright, software GL, SwiftShader); `x3d.accrete@93063bf` for every run; no model API was called |

Accretion is a small system with a large idea: a shared 3D world nobody owns end to end, grown by many small additions, each one accepted by code and recorded where it cannot be edited quietly. This chapter reads the public reference implementation (`x3d.accrete`), re-runs what it can, and records what an independent review of 17 November 2026 found. The original design ran its generator as Claude Haiku inside a claude.ai artifact; that source was never supplied and this implementation keeps the model OFF. Everything below is about the part that does not need a model: the gate and the ledger.

---

## 1. The map

```text
   ledger prefix (hash of last entry, count n)
        |
        v
   PLANNER      seed = sha256(previous_hash + ":" + n)   cell, level, mode, biome   [no model]
        |  plan
        v
   GENERATOR    proposes a fragment for that slot        authored procedural (OFF: model)
        |  raw X3D fragment, at most 12 KiB
        v
   GATE         (1) fragment gate   24 node types + ROUTE, caps, typed fields, fit wrapper
        |       (2) pinned XSD 4.0   on the exact wrapped scene bytes
        |       (3) pinned semantic  x3d_mcp@b5c9956, 4.1 UOM tables
        |  all three pass, or nothing is written
        v
   LEDGER       SQLite, BEGIN IMMEDIATE, head/tail compare-and-swap
                entry = plan + candidate hashes + admission record + pipeline identity
                hash  = sha256(accretion-c14n/1 of the entry), chained by prev_hash
        |
        v
   VERIFY       replay placement, recompute hashes, bind witnesses; never re-run the gate
```

| in scope | out of scope |
|---|---|
| the four roles and the contract between them; the gate's vocabulary and caps; the chain, its checkpoint and its limits; the 17 November review and the fixes; the static viewer and its browser verifier | model-written fragments (not run; the original used Haiku and its source was not supplied); rendered acceptance (`render` is `not_run`); signatures; multi-writer deployment; GPU or cloud cost |

| Loom term ([02](02-loom-laws.md)) | here | note |
|---|---|---|
| card, kickoff | the plan: a pure function of the ledger prefix | fixed before any candidate exists |
| weave | the generator | replaceable; the gate does not ask who wrote the bytes |
| witness | `fragment`, `xsd`, `semantic` (and `render`, not required, `not_run`) | listed per entry by `witness_rows` in `accretion/world.py` |
| gate | the policy: all three required witnesses must pass | the policy is stored in every entry and compared on replay |
| receipt | the ledger entry, schema `accretion.local-admission/v1` | explicitly not a `loom.receipt/1` |

The Loom mapping is the repository's own and is graded [L]: it follows `x3d.loom@7a7d657` as read there, and nothing here confirms that a Loom profile would accept an Accretion entry.

Read next: deeper, [23 Traceability](23-traceability-lineage.md) for the same hash-chain limits applied to a scene's provenance; wider, [03 Validator and gates](03-validator-and-gates.md) for what the XSD and semantic stages do and miss.

---

## 2. Four roles, one rule: only the gate decides

| role | what it owns | what it must not do | where | model allowed? |
|---|---|---|---|---|
| planner | cell, level, mode (generate or augment), biome, seed | read a clock or a random source | `plan_next` in `accretion/world.py` | no |
| generator | the local geometry inside its slot | choose its own slot, nest global nodes | `accretion/generator.py` (six families: orrery, coral, ziggurat, beacon, mycelium, gyroscope) | yes, here OFF |
| gate | the verdict | trust the generator | `accretion/gate.py`, `accretion/mcp_adapter.py` | no |
| ledger | order, hashes, the atomic commit | admit anything the gate did not pass | `WorldStore.append` | no |

The planner is a pure function of the ledger prefix. `plan_next` takes the placements so far and the previous hash, and derives `seed = sha(previous_hash + ':' + n)`; the new entry is an augmentation of one of the last 32 touched cells with probability 42% (by the seed), otherwise the next cell of a square spiral. Because the seed includes the previous entry's hash, a reader can replay the whole plan from the archive alone. [C] `x3d.accrete@93063bf`, Python 3.13.18: calling `plan_next([], genesis)` twice gives equal plans (seed prefix `0165924b1d5d`, cell `[0, 0]`, word `vessel`).

The same design has a cost that the README states and a run shows. The previous hash contains `created_utc`, so a second history built by the same code has the same first plan and different ones after it. [C] `python3 tools/build_demo.py --count 96`, run twice: entry 1 has the same seed in both, 1 of 96 seeds match, 1 of 96 raw fragments match, and the tail hashes differ on every build (four builds, four tails). That is not a defect: a plan is reproducible from a recorded prefix, not from the code. It is why a published checkpoint, not "rebuild and compare", is the anchor ([section 5](#5-what-the-chain-proves-and-what-it-cannot)).

The generator here is authored procedural code: `build_demo` reports `"model_calls": 0`. The original design had a model propose each fragment. That is a different system and it is graded as read, not run:

| claim in the original design notes | grade | why |
|---|---|---|
| a model (Claude Haiku) proposes fragments inside a claude.ai artifact | [S] | design note read; the private source was never supplied; nothing here calls a model |
| 38 tests in the original gate | [S] | the repository says it "does not reproduce its claimed 38-test result"; its own suite is 99 tests |
| a 31-node vocabulary | [S] | the contract says "24 node types plus ROUTE", not 31 |
| per-call prices and a 1.2M-entry capacity | [S] | read in the notes, never run; this implementation measured 100 entries and refuses to project 1,000 as a result |

The repository's own caution is the right one: "historical model/pricing/capacity claims in the source notes are not treated as verified behavior of this implementation."

---

## 3. The gate: three instruments in a fixed order

```text
   raw fragment (UTF-8, at most 12 KiB)
        |
   XML preflight   no DOCTYPE, ENTITY, CDATA, comment, PI, namespace; five standard entities only
        |
   vocabulary      FIELDS: 24 node types + ROUTE; every field listed, anything else fails
        |
   typing + caps   finite typed numbers, ranges, keys 2..32, 80 nodes, 160 expanded shapes
        |
   fit             conservative sphere bound r <= 120 m, else refused; wrapper scales into 3 m
        |  canonical_x3d  (the admitted, fitted fragment, not the author's text)
        v
   wrap_scene      <X3D profile="Immersive" version="4.0"><Scene> ... </Scene></X3D>
        |
   XSD 4.0         pinned x3d_mcp b5c9956 validate_xml on the exact bytes that are stored
        |
   semantic        pinned x3d_mcp b5c9956 semantic pass; "pass" means no level == error
```

The gate's contract is in `docs/GATE-CONTRACT.md`. The numbers a reader will quote:

| bound | value | grade and instrument |
|---|---|---|
| node types in the vocabulary | 24, plus ROUTE | [C] `len(FIELDS)` is 25 with `ROUTE` present |
| raw source | 12 KiB | [C] contract table |
| canonical fitted output | 24 KiB | [C] contract table |
| source nodes | 80 | [C] |
| nesting depth | 16 (source depth only) | [C]; chains through USE are deeper (review G5, open) |
| expanded geometry instances | 160 | [C] |
| ROUTEs; interpolators | 12; 8 | [C] |
| coordinate points; indices | 1024; 4096 | [C] |
| reject radius; slot | 120 m; 3 m | [C] |
| float32 floor for sizes and scales | 1.1754944e-38 | [C] after the 17 November fix |

The fit is a bound, not a measurement. The contract says so: `bounds` are "origin-centred sphere envelopes enclosed by axis-aligned cubes", often loose, and the complexity score "is neither beauty nor scene readability nor measured rendering cost". Nothing in the gate says the fragment is visible, watertight or free of flashing (review G6: a 64 Hz light flash passes).

A worked pass and a worked refusal. Run from a checkout:

```bash
python3 -I -c "
import sys; sys.path.insert(0, '.')
from accretion.gate import gate_fragment
ok = gate_fragment('<Shape><Appearance><Material diffuseColor=\"0.2 0.6 0.9\"/></Appearance><Sphere radius=\"0.5\"/></Shape>', prefix='P1')
bad = gate_fragment('<Script url=\"https://example.org/a.js\"/>', prefix='P1')
print(ok['status'], [e['code'] for e in bad['errors']])"
```

The first returns `pass` with a canonical fragment whose DEF, USE and ROUTE names carry the prefix `P1`; the second returns `fail` with named `GATE_*` diagnostics and no renderable output. A failed attempt is stored as an attempt row and does not advance the world. [C] `x3d.accrete@93063bf`.

Mutation evidence. The review ran 30,000 mutation-fuzz runs (`nan`, `inf`, `1e999`, `1e-400`, empty, Unicode, truncation) on two rich fragments and reported zero uncaught exceptions and no wrong-admit of a forbidden node; that script is not in the repository, so it is [L] here. A smaller independent run of the same idea (drill D-ACC-8) gives, [C] with seed 20261117: 5,000 mutations of attribute values of the 24 example fragments, 402 passed, 4,598 failed, 0 uncaught exceptions, 0 passes holding a tag outside the vocabulary.

---

## 4. The ledger: one transaction, one chain

An entry is a single JSON document in `accretion-c14n/1` (sorted keys, shortest-float text, integral floats collapsed, `NaN` and duplicate keys refused). Its hash is the SHA-256 of that canonical form, and it carries the previous hash, so the entries form a chain from a fixed genesis `sha256("accretion-observatory-v1:genesis:accretion-c14n/1")`.

| part of an entry | content | bound by |
|---|---|---|
| `plan` | the planner's output | replayed by `verify_archive` |
| `candidate` | `raw_sha256`, `canonical_sha256`, `scene_sha256` | recomputed from the stored bytes |
| `admission` | policy, its digest, the fragment record, the `mcp` record (xsd, semantic, instrument identity), `render: not_run` | compared to `POLICY`; witness rows rebuilt |
| `pipeline` | the hashes of the code files that produced the verdict | digest recomputed |
| `prev_hash`, `hash`, `created_utc` | the chain | recomputed |

`WorldStore.append` takes a head and tail snapshot, plans, generates, gates, then opens `BEGIN IMMEDIATE`, re-reads the latest row, and refuses with `Conflict` if the head or tail moved. The entry and its attempt row commit together. [L] The review ran 6 threads against the same expected head: exactly 1 won and 5 conflicted, with 6 attempt rows recorded (1 committed, 5 conflicts); the verifier stayed valid. Read, not re-run.

`verify_archive` rechecks, per entry and in order: genesis, sequence, `prev_hash`, payload digest, placement replay, candidate byte digests, the exact `wrap_scene` identity, witness rows, the policy digest, the `pass` statuses and their bindings to the candidate, and the pipeline digest; then the declared checkpoint, and an external one if the caller holds it. It does not rerun the gate, the XSD or the semantic pass, and the result's own `scope` string says so.

---

## 5. What the chain proves and what it cannot

Self-consistency is checkable by anyone; authorship is not.

| edit to a stored archive | caught without an external checkpoint | caught with one |
|---|---|---|
| any field of the entry (the review reports 208 scalar mutations of one payload, all rejected [L]) | yes | yes |
| swap or duplicate entries | yes | yes |
| truncate the tail and fix the declared checkpoint | **no** | yes |
| rewrite the last entry, recompute its hash and the declared checkpoint | **no** | yes |

[C] Both "no" cells were run (drill D-ACC-5): a last entry with an edited title and a recomputed hash returns `valid: true` with no external checkpoint, and `TRUSTED_CHECKPOINT_MISMATCH` against the shipped checkpoint (`examples/checkpoint.json`, hash prefix `307fab65`, head 24). A truncated archive is valid without one and invalid with one. The README states the limit: hash continuity "does not establish authorship or stop an attacker replacing the entire database and its checkpoint". The same limit measured on a scene's own chain is in [23](23-traceability-lineage.md): 0 of 160 consistent forgeries caught.

Two things the review added, both open in the repository:

* The hash is malleable across `1` and `1.0` in fields outside the canonical forms (finding L2), and fields outside the entry hash are unauthenticated.
* A forged entry whose admission block is fabricated but self-consistent verifies (finding L1). The verifier checks that the record says `pass` and binds to the bytes, not that a gate ever ran. Only an independent re-run (the gate and both validators, on the stored bytes) could close that, and it is not built.

Pre-registered and recorded evidence are different things here, and the code keeps them apart:

| kind | example | why it matters |
|---|---|---|
| pre-registered | the policy and its digest in every entry; the caps; the benchmark's 90 s stop rule; the seven tamper cases named in `docs/PAGES.md` | fixed before the run; a later edit shows as a mismatch |
| recorded | the xsd and semantic results, the instrument identity, the pipeline file hashes | what happened once; `verify` checks bindings and never re-observes it |
| not recorded | a render | `render.status` is `not_run`; a visible preview is not a candidate-bound render witness |

---

## 6. The review: 45 findings, and what held

Method, from the review file: 6 reviewer lanes (gate, ledger, http, adapter, web, claims), 45 findings, each re-checked by 2 verifiers (one reproducing, one trying to refute), 80 agents in all, on the tree as supplied (`52ba996`). Two findings were refuted by the verifiers (WEB-4, WEB-6). Fixes landed in `93063bf` with regression tests in `tests/test_review_fixes.py`.

| finding | what was wrong | before (`52ba996`) | after (`93063bf`) | grade |
|---|---|---|---|---|
| G1 | values below float32 pass the gate and the pinned validators | `Box size="1e-320 1 1"` and `Transform scale="1e-40 1 1"`: gate, XSD, semantic all `pass` | `GATE_FIELD_POSITIVE`, `GATE_ZERO_SCALE` | [C] |
| G4 | numeric lexer accepts Unicode digits and spaces | `size="٢ ٢ ٢"` (Arabic-Indic) and two numbers joined by U+00A0 all pass | `GATE_FIELD_NUMBER`, `GATE_FIELD_LENGTH` | [C] |
| G3 | SpotLight `beamWidth` default wrong | a valid light with `cutOffAngle="0.7"` refused (`GATE_SPOT_CONE`) | default 0.589049 per the 4.0 UOM; the same fragment passes | [C] |
| H2 | no Host-header check | `GET /api/world` with `Host: evil.example:<port>` returns 200 | returns 403 | [C] |
| H6 | HEAD not routed | `HEAD /api/status` returns 404 | 200 | [C] |
| H1, H3, H4, H5 | no socket timeout, no frame-ancestors or directory listing off, deep JSON crashes a handler, key file mode | read in the review | marked fixed; `test_review_fixes.py` covers H1 and H3 (timeout, headers, no listing) but not H4 or H5 | [L] |
| F1 | `PhysicalMaterial` in the vocabulary, never admissible | gate passes, XSD passes, semantic fails | unchanged: documented, not fixed | [C] |
| L1 | verify passes a fabricated-admission forgery and a truncated archive | as in section 5 | open | [C] |
| L3 | append cost dominated by full-payload JSON re-parses | see section 8 | open | [C] with a correction |
| G2, G5, G6, G7 | uncapped triangle workload, USE depth, strobing, fit margin 1e-12 | read in the review | open | [L] |

The review also lists what it could not break: forbidden tags and fields rejected in any case; the XML preflight failed closed on DOCTYPE, ENTITY, CDATA, comments, PIs and namespaces; USE and ROUTE graphs refused every malformed case tried; path traversal blocked; a cross-origin POST needs both the bearer key and an allowed `Origin`; no XSS from ledger text; 1,200 generated candidates over 40 seeds (every family at every tier) all passed the full pipeline (`x3d.accrete@93063bf:docs/REVIEW-2026-11-17.md`, graded [L]: read, not re-run).

### 6.1 The vocabulary-disagreement trap (F1)

The gate lists `PhysicalMaterial` as admissible, with its own typed fields. The pinned semantic pass, run on the wrapped scene under `profile="Immersive"`, reports a `profile-component` error for it: the node belongs to Shape level 2, which the Immersive wrapper does not declare, and browsers that enforce the header refuse to load it.

```bash
python3 -I -c "
import sys; sys.path.insert(0, '.')
from accretion.gate import gate_fragment
from accretion import mcp_adapter, world
g = gate_fragment('<Shape><Appearance><PhysicalMaterial baseColor=\"1 0 0\"/></Appearance><Box/></Shape>', prefix='P1')
v = mcp_adapter.validate_scene(world.wrap_scene(g['canonical_x3d']))
print(g['status'], v['xsd']['status'], v['semantic']['status'], [f['check'] for f in v['semantic']['findings'] if f['level'] == 'error'])"
```

Output: `pass pass fail ['profile-component']`. [C] on `93063bf` and on `52ba996`. Nothing in the unit tests of either side catches this, because the gate tests assert the gate and the adapter tests assert the adapter. Only a test that sends every admitted node type through the whole pipeline would; the generator never emits `PhysicalMaterial`, so the 1,200-candidate sweep could not either. The contract now documents the mismatch and leaves the decision open (declare `<component name="Shape" level="2"/>` in the wrapper, or drop the node).

The general lesson is older than this repository: when a gate has its own vocabulary and defers to a second validator, two lists exist, and the product of the two lists is the real admission set. [03](03-validator-and-gates.md) says the same of the XSD against the semantic pass.

### 6.2 The float32 floor (G1)

A value like `1e-320` is a finite double and a lexically valid `SFFloat`, so the gate's finite check passed it and the pinned XSD did too (the review reports that the pinned XSD caught only `Sphere radius`, through `minExclusive` [L]). The 4.0 field type is single precision: below `1.1754944e-38` a value is denormal or zero when a renderer reads it. A positive size that reaches the renderer as 0 is a collapsed box; a scale that reaches it as 0 is a singular matrix. The fix puts the floor in the gate (`FLOAT32_MIN_NORMAL`), which is the only place that knows the narrowest consumer. [C]

### 6.3 The lexer (G4)

Python's `\d` and `str.split()` match Unicode digits and Unicode whitespace. The gate's regex used both, so `٢` read as a digit and U+00A0 as a separator, while the strict lexical form of an `SFFloat` has neither. The fix is an ASCII-only lexer (`[0-9]`, an explicit space set). The rule generalizes to any gate that parses numbers before a stricter stage: if the two parsers differ, the weaker one admits what the stronger one never intended. [C]

### 6.4 A loopback server needs a Host check (H2)

The server bound to `127.0.0.1` and checked `Origin` on POST. A page on another origin can still read a loopback GET after DNS rebinding, because the browser sends `Host: attacker.example` and the server answered anyway; the whole ledger was readable. A Host allow-list (loopback names with the server's port) closes it. [C] Drill D-ACC-6 reproduces 200 against 403 on the two trees.

---

## 7. The static viewer: port with a parity test, not a rewrite

`web/index.html` runs in two modes from one UI. Live mode reads `/api/*` from the local server and can grow the world with the author capability. Static mode (any other host, or `?static=1`) installs a `fetch` shim, `web/static-mode.js`, that answers the same endpoints from `web/static-world/` and refuses every POST. `/api/verify` is recomputed in the browser by `web/verify-archive.js`.

| property | value | grade and instrument |
|---|---|---|
| tests as supplied | 85 | [C] `python3 -I -m unittest discover -s tests -p 'test_*.py'` on `52ba996`, 3.1 s |
| tests with the static viewer and review fixes | 99 | [C] same command on `93063bf`, 4.5 s; +7 `test_review_fixes.py`, +7 `test_static_export.py` |
| 96-entry world built by the real gate and validators | 3.84, 4.01, 4.40, 4.02 s over four runs | [C] `python3 tools/build_demo.py --count 96`, 4 vCPU |
| in-browser verification of the committed 96-entry payload | 96 of 96, `valid: true`, 0 console errors, 0 HTTP errors | [C] `node tools/pages_smoke.js`, Chromium 153.0.8010.12, software GL, served under a `/x3d.accrete/` sub-path |
| static payload | 197 files, 4,280,343 bytes | [C] `find web/static-world -type f` |
| browser verifier re-runs the gate, XSD or semantic pass | no | [C] stated in the file header and in the returned `scope` |

Why a port. The Python verifier is the specification; a second implementation in another language is a second chance to drift. The browser port reimplements Web Crypto SHA-256, the `accretion-c14n/1` number formatting (a port of Python's `repr(float)`, including the switch to exponent form below `1e-4` and from `1e16`), and the placement replay. The control is `tests/test_static_export.py`, class `BrowserVerifierParity`: for a valid archive and seven tampered ones (a title edit, a one-byte edit of canonical bytes, a plan cell edit, a truncation, a reorder, a forged checkpoint hash, a changed genesis) the Python and Node verdicts must have the same `valid`, `checked` and error text, compared as a whole; a second test compares the float formatter with `repr` on eight values. Tests pass on both sides: 8 of 8 archive cases agree. [C]

What parity does not give: the browser verifier checks the same things as Python and no more. It does not re-run any validator, and its `published_checkpoint` comes from the same origin as the data ("the published checkpoint in `manifest.json` comes from the same origin and is not independent", `docs/PAGES.md`). Hosting adds no trust; the reader must compare the checkpoint with one obtained some other way.

Pages is not live. [C] On 17 November 2026 `https://hagopjay.github.io/x3d.accrete/` answered 404. `docs/PAGES.md` names the missing step: the repository owner sets Settings, Pages, Source "Deploy from a branch", branch `main`, folder `/ (root)`. Until then the static mode is exercised only by `tools/pages_smoke.js` against a local server that emulates the sub-path.

---

## 8. Cost, and a claim that needs its scope

The README says the next useful optimization is to replace "repeated full-payload rescans". The review confirmed that append cost at about 100 entries is dominated by repeated full-payload JSON parsing. A profile of the whole 96-append build gives a more precise picture:

| item | value | instrument |
|---|---|---|
| 96 appends, profiled wall time | 5.151 s (4.643 s inside `append`) | [C] `python3 -m cProfile -s cumtime tools/build_demo.py --count 96`, Python 3.13.18 |
| `validate_scene` (XSD and semantic, pinned) | 2.970 s, of which 96 `_get_schema` calls 1.394 s | same |
| `strict_json` | 19,008 calls, 1.073 s cumulative | same |
| `_placements` (replays the plan from stored payloads) | 289 calls, 0.814 s | same |
| `gate_fragment` | 0.218 s for 96 calls | same |

So: of the append's own time outside the pinned validators (4.643 minus 2.970 is 1.673 s), the JSON re-parsing is the largest item, which supports the README claim. Of the whole append, the largest single item is that the XSD schema is parsed again on every call (1.394 s). Both are fixable and neither fix is built: a transactionally maintained planning index would remove most of the JSON work, and caching the compiled schema would remove most of the other. The profile inflates absolute times; the shares are what to read. The README's own measured run (100 entries: 4.333 s cumulative append, 28.118 ms replay verification, JSON 1,819,603 bytes, X3D 266,921 bytes, on 3.12.14) is [L] here: read, not re-run. Its projection to 1,000 entries (154.386 s) is an estimate that the benchmark itself refused to turn into a result because it exceeds a 90 s stop rule written in advance; the review adds that sizes and hashes in the report do not reproduce on a fresh run (finding C1, they depend on timestamps), and only timings reproduce within about 5%.

---

## 9. What is missing, ranked

1. **An independent re-run on audit**: re-execute the gate and both validators on the stored bytes, so a fabricated admission cannot verify (L1).
2. **A full-pipeline test per admitted node type** (F1): one assertion that every name in `FIELDS` has at least one fragment that passes all three stages, or is removed from the vocabulary.
3. **An external anchor**: a signed or published checkpoint outside the origin that serves the archive. Section 5 shows what the lack costs.
4. **Plan-index columns and a cached schema** (L3, L4): cut append and startup verification, then measure again before quoting any capacity.
5. **A render witness bound to the candidate**: `render` stays `not_run` until a pinned renderer, a camera and a pixel floor exist (see [06](06-xite-the-oracle.md) and [02](02-loom-laws.md) law 2).
6. **A model generator, measured**: the original design's central claim. It needs model calls and has not been run.

---

## Heuristics

| ID | Rule | Grade | Evidence | Instrument |
|---|---|---|---|---|
| H-ACC-1 | Split growth into planner, generator, gate and ledger; let only the generator be a model, and make the other three replayable from the ledger. | C | `plan_next` is a pure function of prefix and hash; `verify_archive` replays it; `model_calls` is 0 | `x3d.accrete@93063bf` `accretion/world.py`, Python 3.13.18 |
| H-ACC-2 | Seed the planner from the previous hash, never from a clock or a random source. | C | same genesis gives equal plans; 1 of 96 seeds equal across two builds because the hash holds a timestamp | `tools/build_demo.py --count 96`, twice |
| H-ACC-3 | Whitelist fields as well as nodes, and fuzz the lexer: forbidden things must fail in any case and spelling. | C | 5,000 mutations: 0 exceptions, 0 passes with a tag outside the vocabulary; the review reports 30,000 (read, not run) | `x3d.accrete@93063bf` gate, seed 20261117 |
| H-ACC-4 | When a gate defers to a second validator, send every admitted node type through both before shipping the vocabulary. | C | `PhysicalMaterial`: gate pass, XSD pass, semantic `profile-component` error | `x3d.accrete@93063bf`, `x3d_mcp@b5c9956` |
| H-ACC-5 | Put a numeric floor at the narrowest type any consumer uses; a finite double is not a valid `SFFloat`. | C | `Box size` `1e-320` and `scale` `1e-40` passed gate, XSD and semantic on `52ba996`; refused on `93063bf` | same, `FLOAT32_MIN_NORMAL` |
| H-ACC-6 | Lex numbers with an explicit ASCII set; never `\d` or bare `split()` on untrusted text. | C | Arabic-Indic digits and U+00A0 separators were admitted on `52ba996` | `x3d.accrete@52ba996` and `93063bf` gate |
| H-ACC-7 | Check a comparison default against the standard's tables, not memory: a wrong default is a false reject. | C | SpotLight `beamWidth` default was pi/4; the 4.0 table says 0.589049; `cutOffAngle="0.7"` was refused | same, `X3D XSD 4.0` and UOM |
| H-ACC-8 | Guard a loopback server with a Host allow-list as well as an Origin check. | C | `Host: evil.example` read the ledger (200) on `52ba996`, 403 on `93063bf` | `serve.py`, curl, both trees |
| H-ACC-9 | Say that verify proves self-consistency; hold a checkpoint from outside the origin before calling a ledger tamper-evident. | C | forged last entry and truncated archive both `valid: true` without a checkpoint, both rejected with one | `verify_archive`, drill D-ACC-5 |
| H-ACC-10 | Port a verifier only with a parity test over a valid input and a tamper table, comparing verdict and error text. | C | 8 of 8 archive cases agree between Python and Node; float formatting agrees with `repr` on 8 values | `tests/test_static_export.py`, Node 22.23.4 |
| H-ACC-11 | State which of a benchmark's outputs reproduce: timings within a spread, never hashes or sizes that include timestamps. | C | four builds, four tail hashes; build wall time 3.84 to 4.40 s | `build_demo.py`, 4 vCPU |
| H-ACC-12 | Profile the whole path before a "dominated by X" claim is written; the biggest item may sit outside the claim's scope. | C | JSON re-parse 1.073 s is the largest part of the store's own time; the schema parse 1.394 s is larger over the whole append | cProfile, Python 3.13.18 |
| H-ACC-13 | Write the stop rule before the run and report a projection as an estimate, not a result. | L | the benchmark refused a 1,000-entry run projected at 154.386 s against a 90 s stop rule | `x3d.accrete@93063bf` `README.md`, read, not run |

---

## Drills

Each drill needs a checkout of `x3d.accrete` at `93063bf`, Python 3.12 or newer with `lxml` and `jsonschema` (the repository's `requirements.txt`), and for the second tree `git worktree add ../accrete-as-supplied 52ba996`. Run Python as `python3 -I`; the snippets add the checkout to `sys.path` themselves.

### D-ACC-1 Count the vocabulary
- **Level:** L1
- **Task:** How many keys does `FIELDS` hold, is `ROUTE` one of them, and how many node types is that?
- **Verify:** `python3 -I -c "import sys;sys.path.insert(0,'.');from accretion.gate import FIELDS;print(len(FIELDS),'ROUTE' in FIELDS)"`
- **Answer:** 25 keys, `ROUTE` present, so 24 node types plus ROUTE (the contract's number, not the original design's 31).
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Python 3.13.18

### D-ACC-2 Before and after the review
- **Level:** L2
- **Task:** Run the whole suite on both trees and say how many tests each runs and how the 14 new ones split between files.
- **Verify:** `python3 -I -m unittest discover -s tests -p 'test_*.py'` in each tree; `grep -c "    def test_" tests/test_*.py`.
- **Answer:** 85 on `52ba996`, 99 on `93063bf`. The new ones are 7 in `test_review_fixes.py` and 7 in `test_static_export.py`; the old files keep gate 28, generator 13, adapter 15, http 9, world 20.
- **Checked:** 2026-11-17 `x3d.accrete@52ba996` and `@93063bf`, Python 3.13.18, lxml 6.1.3

### D-ACC-3 The float32 floor and the lexer
- **Level:** L2
- **Task:** Gate the four fragments below on both trees and record `status` and the first error code. Then run the first through the XSD and semantic stages on the old tree.
- **Verify:** `python3 -I -c "import sys;sys.path.insert(0,'.');from accretion.gate import gate_fragment as g;[print(f[:44],g(f,prefix='P1')['status']) for f in ['<Shape><Box size=\"1e-320 1 1\"/></Shape>','<Transform scale=\"1e-40 1 1\"><Shape><Box/></Shape></Transform>','<Shape><Box size=\"٢ ٢ ٢\"/></Shape>','<Shape><Box size=\"2 2 2\"/></Shape>']]"`
- **Answer:** old tree: `pass` for all four (and the first also passes XSD and semantic through `mcp_adapter.validate_scene(world.wrap_scene(...))`). New tree: `fail` with `GATE_FIELD_POSITIVE`, `GATE_ZERO_SCALE`, `GATE_FIELD_NUMBER`, `GATE_FIELD_LENGTH` in that order.
- **Checked:** 2026-11-17 `x3d.accrete@52ba996` and `@93063bf`, pinned `x3d_mcp@b5c9956`, lxml 6.1.3

### D-ACC-4 The vocabulary trap
- **Level:** L2
- **Task:** Run the `PhysicalMaterial` snippet of section 6.1. Which stage refuses, with which check, and does the generator's sweep of six families at five tiers contain the node?
- **Verify:** the snippet in section 6.1; `grep -n PhysicalMaterial accretion/generator.py`.
- **Answer:** gate `pass`, XSD `pass`, semantic `fail` with `profile-component`; the generator never emits it (no match), which is why no sweep found it.
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, `x3d_mcp@b5c9956`, Python 3.13.18

### D-ACC-5 Forge the last entry
- **Level:** L3
- **Task:** Load `examples/world.json`, edit the last entry's title, recompute its hash with `accretion.world.sha(payload)`, set the archive's declared checkpoint to it, and call `verify_archive` twice: bare, and with the shipped checkpoint (`examples/checkpoint.json`). Then pop the last entry, fix the declared checkpoint, and repeat. What does each call return?
- **Verify:**
```python
import sys, copy; sys.path.insert(0, '.')
from accretion.codec import strict_json
from accretion.world import verify_archive, sha
a = strict_json(open('examples/world.json', encoding='utf-8').read()); held = dict(a['checkpoint'])
f = copy.deepcopy(a); last = f['entries'][-1]; last['payload']['title'] = 'FORGED'
last['hash'] = sha(last['payload']); f['checkpoint'] = {**f['checkpoint'], 'hash': last['hash']}
print(verify_archive(f)['valid'], verify_archive(f, held)['valid'])
t = copy.deepcopy(a); t['entries'].pop(); t['checkpoint'] = {'head': len(t['entries']), 'hash': t['entries'][-1]['hash']}
print(verify_archive(t)['valid'], verify_archive(t, held)['valid'])
```
- **Answer:** `True False` then `True False`. The first result of each pair is the limit (valid without an anchor); the second names the code `TRUSTED_CHECKPOINT_MISMATCH`.
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Python 3.13.18

### D-ACC-6 The rebinding guard
- **Level:** L3
- **Task:** Start the server from each tree on its own port with an empty world, then request `/api/world` with `Host: evil.example:<port>`, and `HEAD /api/status` normally. Record the four status codes.
- **Verify:** `python3 serve.py --demo-count 0 --data <fresh dir> --port <port> &` then `curl -s -o /dev/null -w '%{http_code}\n' -H 'Host: evil.example:<port>' http://127.0.0.1:<port>/api/world` and `curl -s -I -o /dev/null -w '%{http_code}\n' http://127.0.0.1:<port>/api/status`.
- **Answer:** `52ba996`: 200 for the foreign Host, 404 for HEAD. `93063bf`: 403 and 200. Stop both servers afterwards.
- **Checked:** 2026-11-17 `x3d.accrete@52ba996` and `@93063bf`, Python 3.13.18, curl

### D-ACC-7 Same code, different history
- **Level:** L2
- **Task:** Build 96 entries twice (`python3 tools/build_demo.py --count 96 --output <dir>`), and compare entry 1 and entry 2 plans, the number of identical seeds, the number of identical raw fragments, and the two tail hashes. Then time one build.
- **Verify:** load both `world.json` files and compare `entries[i]['payload']['plan']['seed']`, `raw_x3d` and the last `hash`; `python3 -I tools/verify_export.py <dir>/world.json` for each.
- **Answer:** entry 1: equal seed and cell. Entry 2 onward: different. 1 of 96 seeds and 1 of 96 raw fragments equal; tail hashes differ; both archives verify `valid: true`, `checked: 96`. One build takes about 4 s (3.84 to 4.40 s over four runs).
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Python 3.13.18, 4 vCPU

### D-ACC-8 Fuzz the gate
- **Level:** L3
- **Task:** Take the 24 raw fragments of `examples/world.json`. For 5,000 iterations pick one at random, pick one attribute value, and replace it with one of `nan`, `inf`, `-inf`, `1e999`, `1e-400`, empty, `٣`, `1<NBSP>2`, `-0`, `0`, `1e-39`, `99999999`, `abc`, a space, `1,5`, `0x10`, `1_0` (or, one time in five, truncate it). Count exceptions, passes, fails, and passes whose canonical output holds a tag outside `FIELDS`. Then extend: add a mutation that renames a tag to a lower-case spelling.
- **Verify:** a loop calling `gate_fragment(mutated, prefix='P1')` inside `try`, with `random.Random(20261117)`; parse `canonical_x3d` inside a wrapper element and compare tag sets.
- **Answer:** 5,000 runs: 402 pass, 4,598 fail, 0 uncaught exceptions, 0 passes with a tag outside the vocabulary. The review's 30,000-run figure with the same result is [L]; the lower-case rename should fail with a named `GATE_NODE_FORBIDDEN`-family code, not pass.
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Python 3.13.18 (the rename extension: not run)

### D-ACC-9 Profile an append
- **Level:** L2
- **Task:** Profile the 96-entry build and rank the top three costs inside `append`. Say which one the README's "repeated full-payload rescans" refers to and which one it does not.
- **Verify:** `python3 -m cProfile -s cumtime tools/build_demo.py --count 96 --output <dir>`, read `append`, `validate_scene`, `_get_schema`, `strict_json`, `_placements`.
- **Answer:** `validate_scene` 2.970 s (of which `_get_schema` 1.394 s), then `strict_json` 1.073 s (19,008 calls) and `_placements` 0.814 s. The README refers to the second and third; the first is the validator's own schema parse, which the claim does not mention.
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Python 3.13.18, lxml 6.1.3

### D-ACC-10 Browser parity
- **Level:** L2
- **Task:** Run the parity class alone, then the Pages smoke test, and say how many archive cases the first compares and what the second reports for entries checked and console errors.
- **Verify:** `python3 -I -m unittest discover -s tests -p 'test_static_export.py' -k Parity -v`; `node tools/pages_smoke.js shot.png` (needs Playwright with Chromium).
- **Answer:** the parity class passes 2 tests, the first over 8 archives (1 valid, 7 tampered); the smoke test prints `"checked": 96`, `"valid": true`, `"errors": []`, and `verifyJson.engine` `browser-js`.
- **Checked:** 2026-11-17 `x3d.accrete@93063bf`, Node 22.23.4, Chromium 153.0.8010.12 (Playwright, software GL)

---

## Honest limits

* **[C]** No model was called. The original Haiku-in-an-artifact design is [S] throughout: its 38 tests, prices and 1.2M capacity were read in the design notes, never run, and its source was never supplied.
* **[C]** The reference gate admits 24 node types. That is a subset chosen for safety, not a statement about X3D coverage.
* **[C]** The gate's bounds are conservative envelopes, not measured extents. No render, visibility, topology or flashing check exists. `render` is `not_run` in every entry.
* **[C]** `verify_archive`, in Python and in the browser, proves the stored record is self-consistent and replays the plan. It does not prove that a gate ran, who wrote the entry, or that the checkpoint is the one anyone else holds.
* **[C]** The browser verifier does not re-run the gate, the XSD or the semantic validators. Pages is not live; the static mode was run only through `tools/pages_smoke.js` against a local server.
* **[C]** `PhysicalMaterial` cannot be admitted and the repository leaves it so. Other findings (G2, G5, G6, G7, L1 to L5, F2 to F7, most WEB items) are open at `93063bf`.
* **[L]** The 30,000-run mutation fuzz, the 1,200-candidate sweep, the 6-thread contention probe, the 19 of 19 vendored-file blob match and the upstream drift (10 commits ahead of the pin, none in `src/validation`) are read from the review file, not re-run. The review's scripts are not in the repository.
* **[L]** The README's 100-entry benchmark (4.333 s, 28.118 ms, 1,819,603 and 266,921 bytes) is read from the repository and was not re-run; only timings of that kind reproduce, and then within about 5%.
* **[L]** The profile shares in section 8 come from one cProfile run, which inflates absolute times. The conclusion about the schema parse is about ranking, not milliseconds.
* **[L]** The Loom mapping is the repository's reading of `x3d.loom@7a7d657`. This chapter did not run a Loom profile against an Accretion entry.
* **[S]** The suggestion that caching the compiled schema and adding plan-index columns would remove most of the two largest costs is an expectation from the profile, not a measurement.
* **[C]** Timings are single runs on one shared container with 4 vCPUs; the third digit moves between runs. Hashes and sizes of a freshly built world are single-run values.

---

## Numbers register

| ID | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|
| N-ACC-1 | unit tests: as supplied; with static viewer and review fixes | 85; 99 | [C] | `python3 -I -m unittest discover -s tests -p 'test_*.py'`, Python 3.13.18, lxml 6.1.3 | `x3d.accrete@93063bf:tests/test_review_fixes.py` |
| N-ACC-2 | tests per file at `93063bf`: gate; generator; adapter; http; world; review fixes; static export | 28; 13; 15; 9; 20; 7; 7 | [C] | `grep -c "    def test_" tests/test_*.py` | `x3d.accrete@93063bf:tests/test_static_export.py` |
| N-ACC-3 | node types in the gate vocabulary, plus ROUTE | 24 | [C] | `len(FIELDS)` is 25, Python 3.13.18 | `x3d.accrete@93063bf:docs/GATE-CONTRACT.md` |
| N-ACC-4 | raw fragment cap; canonical cap (KiB) | 12; 24 | [C] | contract table, matches `accretion/gate.py` constants per the review | `x3d.accrete@93063bf:docs/GATE-CONTRACT.md` |
| N-ACC-5 | source nodes; nesting depth; expanded geometry instances | 80; 16; 160 | [C] | same | same |
| N-ACC-6 | float32 floor for sizes and scales | 1.1754944e-38 | [C] | `FLOAT32_MIN_NORMAL` in the gate | `x3d.accrete@93063bf:docs/GATE-CONTRACT.md` |
| N-ACC-7 | review: lanes; findings; verifiers per finding; agents | 6; 45; 2; 80 | [L] | review method as written, not repeated | `x3d.accrete@93063bf:docs/REVIEW-2026-11-17.md` |
| N-ACC-8 | review mutation-fuzz runs, uncaught exceptions | 30,000; 0 | [L] | review file, script not in the repository | same |
| N-ACC-9 | own mutation run: runs; pass; fail; exceptions; passes with a foreign tag | 5,000; 402; 4,598; 0; 0 | [C] | drill D-ACC-8, seed 20261117, Python 3.13.18 | `x3d.accrete@93063bf:accretion/gate.py` |
| N-ACC-10 | box size 1e-320 and scale 1e-40: gate, XSD, semantic verdicts as supplied; after the fix | pass, pass, pass; fail | [C] | drill D-ACC-3, `x3d_mcp@b5c9956`, lxml 6.1.3 | `x3d.accrete@52ba996:accretion/gate.py` |
| N-ACC-11 | `PhysicalMaterial` verdicts: gate; XSD; semantic | pass; pass; fail (`profile-component`) | [C] | drill D-ACC-4, `x3d_mcp@b5c9956` | `x3d.accrete@93063bf:docs/GATE-CONTRACT.md` |
| N-ACC-12 | foreign Host header on `/api/world`: as supplied; after the fix (HTTP status) | 200; 403 | [C] | drill D-ACC-6, curl | `x3d.accrete@93063bf:tests/test_review_fixes.py` |
| N-ACC-13 | `HEAD /api/status`: as supplied; after the fix (HTTP status) | 404; 200 | [C] | same | same |
| N-ACC-14 | forged last entry verifies without a checkpoint; with the shipped one | true; false | [C] | drill D-ACC-5 | `x3d.accrete@93063bf:accretion/world.py` |
| N-ACC-15 | shipped checkpoint head; hash prefix | 24; 307fab65 | [C] | `examples/checkpoint.json` | `x3d.accrete@93063bf:examples/checkpoint.json` |
| N-ACC-16 | 96-entry build wall time, four runs (s) | 3.84; 4.01; 4.40; 4.02 | [C] | `python3 tools/build_demo.py --count 96`, 4 vCPU | `x3d.accrete@93063bf:tools/build_demo.py` |
| N-ACC-17 | two builds of 96: identical seeds; identical raw fragments; distinct tail hashes over four builds | 1 of 96; 1 of 96; 4 of 4 | [C] | drill D-ACC-7 | same |
| N-ACC-18 | browser verification of the committed payload: entries checked; console errors | 96 of 96; 0 | [C] | `node tools/pages_smoke.js`, Chromium 153.0.8010.12, software GL | `x3d.accrete@93063bf:tools/pages_smoke.js` |
| N-ACC-19 | static payload: files; bytes | 197; 4,280,343 | [C] | `find web/static-world -type f` | `x3d.accrete@93063bf:web/static-world/manifest.json` |
| N-ACC-20 | parity cases: archives compared; of which tampered; float formatter values | 8; 7; 8 | [C] | `BrowserVerifierParity`, Node 22.23.4 | `x3d.accrete@93063bf:tests/test_static_export.py` |
| N-ACC-21 | profile of 96 appends: total; `validate_scene`; `_get_schema`; `strict_json` calls; `strict_json` time (s) | 5.151; 2.970; 1.394; 19,008; 1.073 | [C] | `python3 -m cProfile -s cumtime tools/build_demo.py --count 96` | `x3d.accrete@93063bf:accretion/world.py` |
| N-ACC-22 | README benchmark at 100 entries: append total (s); verify (ms); JSON bytes; X3D bytes | 4.333; 28.118; 1,819,603; 266,921 | [L] | `reports/store-scaling.json` as quoted in the README, not re-run | `x3d.accrete@93063bf:README.md` |
| N-ACC-23 | projected 1,000-entry run; stop rule (s) | 154.386; 90 | [L] | estimate only, not run | same |
| N-ACC-24 | loaded records; detail budgets; entry cap | 512; 24, 48, 96; 10,000 | [C] | README text, matches `serve.py` constants per the review | same |
| N-ACC-25 | review sweep: candidates; seeds; failures | 1200; 40; 0 | [L] | review file, not re-run | `x3d.accrete@93063bf:docs/REVIEW-2026-11-17.md` |
| N-ACC-26 | vendored files matching upstream blobs; upstream commits ahead of the pin | 19 of 19; 10 | [L] | review file, not re-run | same |

---

## Sources and provenance

Read and run on 2026-11-17: `x3d.accrete` at `93063bf` (public, https://github.com/hagopjay/x3d.accrete) and at `52ba996` for the as-supplied side; the vendored `x3d_mcp` at `b5c9956` through the repository's adapter; the bundled X_ITE 16.6.0 viewer through `tools/pages_smoke.js`. The repository states that its source is "a new reference implementation from the two supplied design notes" and that the private source archive of the original application was not supplied; nothing here is derived from that archive, and the original design's figures are graded [S] above. The review file `docs/REVIEW-2026-11-17.md` is a repository document; its findings are cited with its own ids and, where this chapter re-ran a finding, the run is named in a drill. The claim ledger for this chapter is `claims/25-accretion-gated-growth.jsonl`: each number above that is literal in a public file has a line with the words it was read from, pinned at the commit shown. Run results (test counts, timings, fuzz counts, verdicts of drills) have no source file to quote and stay uncovered; a reader re-checks them with the drill commands.
