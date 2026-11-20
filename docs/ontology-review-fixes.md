# Fixes from the ontology engineering review (20 Nov 2026)

A second engineering review of the ontology work ranked 25 findings. This page says what was built for each, where, and what it measured. Full notes with the limits: x3d.loom `LEARNINGS-ontology-review-fixes.md`.

Instruments: x3d_mcp fork (PR #28 merged as `bbd773f`, PR #29), XSD 4.1 and X3DUOM 4.1 as bundled there, rdflib 7.6.0, pyshacl 0.40.2, Python 3.13.18; x3d.loom PR #146 (merged as `556faf1`) and PR #147; a container with no GPU. Grades: Confirmed means measured there.

| # | Finding | What was built | Measured | Where |
|---|---|---|---|---|
| F1 | An SFNode field could hold two nodes and no check said so | `sfnode-multiple` in `validate_semantic`; SHACL set `x3d-cardinality` generated from the X3DUOM (481 node and field pairs) | 12 of 12 planted faults caught, 0 of 6 legal controls flagged, 7 of 2,211 corpus files flagged (all hand-made probes) | x3d_mcp #28 |
| F2 | The heritage twin's shapes passed 8 of 8 extra planted faults | hand-written `shapes-strict.ttl` beside the generated shapes; "cannot measure" is a violation | 8 of 8 named, clean twin 0, shipped faults 2 of 2 | x3d_mcp #28 |
| F3 | Receipts held only survivors (123 of 123 witness entries pass) | `loom.rejection/1`: every required witness judged, each refusal with class, reason and place | kit self-test 151 controls in both modes | x3d.loom #146 |
| F4 | 14 render fails with `reason: null` | a `failure` block per warn or fail: floor missed, image region, class, rule link | 19 records, 11 explained by an existing rule, 8 unexplained | x3d.loom #146 |
| F5 | A query could build 1 GiB in 3.3 s inside the deadline | address-space cap on the forked SPARQL worker | the same query stopped in 0.82 s | x3d_mcp #29 |
| F6 | `LIMIT` without `ORDER BY` returned different rows per process | answer carries `stable: false` and a warning | 3 hash seeds: flagged on each | x3d_mcp #29 |
| F7 | `ORDER BY` in a subquery switched off the stabilising sort | only the outermost modifiers are read | 3 hash seeds: one row order | x3d_mcp #29 |
| F8 | Four grade predicates, three scales | loom-core: one claim shape, `grade` C/L/S and `verdict` supported/refuted/untested | 369 claims from 5 demo dialects, 369 conform | x3d.loom #146 |
| F9 | 0 of 144 claims hashed, 29 ids not IRIs | sha256 per claim, every id repair listed | 369 of 369 hashed, 19 repairs on claims | x3d.loom #146 |
| F15 | `where_can_place` had no XSD verdict | each row carries `xsd` A, R or I; `verified_only` filter | 4,879 accepted, 740 rejected, 890 inconclusive of 6,509 rows | x3d_mcp #29 |
| F18 | glTF semantic spec said Metadata travels on any host | spec lists the hosts that travel; probe fixture and test | 3 of 5 trees dropped on the probe, S1 and S2 fail as they should | x3d.loom #147 |
| F20 | 78 of 116 witness runs named no tool version | every witness record carries the kit's content hash and commit | new runs only; old receipts are not rewritten | x3d.loom #147 |
| F22 | wgpu receipt wrote `receipt`, its doc says `schema` | the receipt writes both | not compiled locally; CI builds it | x3d.wgpu #8 |
| F23 | A geodetic latitude of 137 passed every check | `geo-coordinate-range` in `validate_semantic` | 5 of 5 planted, 0 flagged in 2,214 corpus files | x3d_mcp #29 |
| F25 | The x3d_mcp teardown is dated (48 tools then, 59 now) | a dated-page banner on the teardown | checked 2026-11-20 at `bbd773f` | this repository |

## Closed without a build

| # | Finding | Decision |
|---|---|---|
| F16 | Ontology IRIs change with every release | no new code: x3d_mcp already writes shapes against 4.1 only; stable IRIs are the publisher's call |
| F17 | No Turtle to X3D converter | do not build: XML stays the master, RDF a derived view |
| F19 | Blender round-trip audit skips Metadata | deferred: graded Likely from a code read; Blender was not available to verify a fix |
| F21 | Render-and-score ran on 2 of 25 artifact receipts | deferred: large; port the glTF harness to X3D subjects |

## Waiting

F10 to F14 and F24 are changes to x3d.onto, which was not reachable for writing when this was built.

## What the failure records already showed

Grouping the 19 render failures by engine, class and rule gave two groups of three with no rule: three.js and Babylon.js both render brighter than the Khronos reference on the same three subjects (measurement Confirmed, cause Suspected). That is the first output of the "receipt to rule" loop, produced without a model.
