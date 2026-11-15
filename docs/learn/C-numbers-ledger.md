# Appendix C. Numbers ledger

Merged from the *Numbers register* of every chapter by `tools-shared/build_learn.py`. Edit the chapter, not this file.

<!-- BEGIN GENERATED -->
**433 numbers** from 16 chapters. Grades: [C] 389 · [L] 40 · [S] 4. Every row names its instrument; a row without one fails `check_learn.py`.

| ID | Ch | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|---|
| N-TH-1 | [01](01-the-tether.md) | non-background pixel fraction, `visible.x3d` | 0.1752 | [C] | `X_ITE 16.7.0`, Chromium 153, SwiftShader, 320 x 240 | section 5 (run 2026-11-14) |
| N-TH-2 | [01](01-the-tether.md) | non-background pixel fraction, `blank.x3d` (valid, faces away) | 0.0000 | [C] | `X_ITE 16.7.0`, Chromium 153, SwiftShader, 320 x 240 | section 5 (run 2026-11-14) |
| N-TH-3 | [01](01-the-tether.md) | scenes valid at the fork gate, of the two | 2 of 2 | [C] | `x3d_mcp fork b4efcd3` | section 5 (run 2026-11-14) |
| N-TH-4 | [01](01-the-tether.md) | hint loop alone, repaired cases | 521 of 540 (96.5%) | [C] | `x3d_mcp fork b4efcd3`, seed 20261029 | `x3d_mcp@b4efcd3:evaluation/exact_fix_eval.py` (run 2026-11-14) |
| N-TH-5 | [01](01-the-tether.md) | `repair_x3d` alone, repaired cases, at `b4efcd3` | 76 of 540 (14.1%) | [C] | `x3d_mcp fork b4efcd3`, seed 20261029 | `x3d_mcp@b4efcd3:evaluation/exact_fix_eval.py` |
| N-TH-6 | [01](01-the-tether.md) | `repair_x3d` alone, repaired cases, at `535fdac` | 81 of 540 (15.0%) | [C] | `x3d_mcp fork 535fdac`, seed 20261029 | `x3d_mcp@535fdac:evaluation/exact_fix_eval.py` (run 2026-11-14) |
| N-TH-7 | [01](01-the-tether.md) | hint loop gives the seed back exactly, at `b4efcd3` | 268 of 540 (49.6%); 15 valid only by deleting an element | [C] | `x3d_mcp fork b4efcd3` | `x3d_mcp@b4efcd3:evaluation/exact_fix_eval.py` |
| N-TH-8 | [01](01-the-tether.md) | injected route faults caught, gate vs XSD alone | 13 of 13 vs 0 of 13 | [C] | `x3d_mcp fork b4efcd3`, 24 seeds | section 6 (run 2026-11-14) |
| N-TH-9 | [01](01-the-tether.md) | injected displaced part caught | 0 of 14 | [C] | `x3d_mcp fork b4efcd3`, 24 seeds | section 6 (run 2026-11-14) |
| N-TH-10 | [01](01-the-tether.md) | unchanged seeds flagged by the gate | 0 of 24 | [C] | `x3d_mcp fork b4efcd3` | section 6 (run 2026-11-14) |
| N-TH-11 | [01](01-the-tether.md) | seeds, mutation sites, errors at `535fdac` and at `b4efcd3` | 25, 15,651, 570 and 24, 10,294, 577 | [C] | `x3d_mcp fork 535fdac` and `b4efcd3` | section 7 (run 2026-11-14) |
| N-TH-12 | [01](01-the-tether.md) | fix operations used in the 540-case run at `b4efcd3` | `set_attribute` 290, `move` 127, `rename_element` 58, `remove_attribute` 29, `rename_attribute` 29, `remove_element` 15, `wrap` 10 | [C] | `x3d_mcp fork b4efcd3` | `x3d_mcp@b4efcd3:evaluation/exact_fix_eval.py` |
| N-TH-13 | [01](01-the-tether.md) | hints for one broken ROUTE in the worked example | 2 hints for 1 error; 1 fix applied, valid True | [C] | `x3d_mcp fork b4efcd3` | section 5 step 4 (run 2026-11-14) |
| N-TH-14 | [01](01-the-tether.md) | model repair with hints vs plain errors, first round | 507 vs 489 of 540; 31 gained, 13 lost; p 0.0096 | [L] | a hosted model, as reported | `x3d.loom@162ab18:LOOM-v1.md` section 7.1 |
| N-TH-15 | [01](01-the-tether.md) | valid scenes that drew nothing; blank among valid | 203 of 1,058; 17 of 91 | [L] | as reported, not re-checked | `x3d.loom@162ab18:LOOM-v1.md` section 7.2, failure mode 91 |
| N-TH-16 | [01](01-the-tether.md) | planted ROUTE-first faults caught before and after PR #15 | 0 to 200 of 200 | [L] | libxml2 2.14.6, fork 56809ca to the PR #15 change | `x3d_mcp@b4efcd3:docs/ROUTE-COLOUR-HANIM-CHECKS.md` |
| N-TH-17 | [01](01-the-tether.md) | scenes in the fork's XSD-verdict corpus run | 2,857 (1,593 invalid, 1,264 valid), verdict unchanged | [L] | libxml2 2.14.6, as reported | `x3d_mcp@b4efcd3:docs/ROUTE-COLOUR-HANIM-CHECKS.md` |
| N-TH-18 | [01](01-the-tether.md) | lawful metric AUC on recorded scenes | 0.997 on 383 | [L] | x3d.onto, as reported | `x3d.loom@162ab18:LOOM-v1.md` section 7.2 |
| N-TH-19 | [01](01-the-tether.md) | chain forgery after a scene edit verifies | 1 of 1 | [C] | chain sketch, Python 3.13.18 | section 9 (run 2026-11-14) |
| N-TH-20 | [01](01-the-tether.md) | doha seed gate errors at `535fdac` and `b4efcd3` | 1 and 2 semantic errors | [C] | `x3d_mcp fork 535fdac` and `b4efcd3` | section 7 (run 2026-11-14) |
| N-TH-21 | [01](01-the-tether.md) | tether score of X3D | 5 of 5 | [L] | reasoned from the [C] rows above | section 3 |
| N-LAW-1 | [02](02-loom-laws.md) | laws in `LOOM-v1.md` section 3, ids contiguous | 44 | [C] | python parse of the table, `x3d.loom@162ab18` | `x3d.loom@162ab18:LOOM-v1.md` |
| N-LAW-2 | [02](02-loom-laws.md) | failure modes in section 8, ids contiguous | 160 | [C] | python parse of the table, `x3d.loom@162ab18` | `x3d.loom@162ab18:LOOM-v1.md` |
| N-LAW-3 | [02](02-loom-laws.md) | witness rows in section 6.1 | 13 | [C] | python parse, `x3d.loom@162ab18` | `x3d.loom@162ab18:LOOM-v1.md` |
| N-LAW-4 | [02](02-loom-laws.md) | profile files and profile rows in section 6.2 | 20 files, 11 rows | [C] | count, `x3d.loom@162ab18` | `x3d.loom@162ab18:kit/profiles/` |
| N-LAW-5 | [02](02-loom-laws.md) | laws and failure modes at the first public snapshot | 35 and 92 | [C] | `git show 0244784:LOOM-v1.md`, python parse | `x3d.loom@0244784:LOOM-v1.md` |
| N-LAW-6 | [02](02-loom-laws.md) | laws and failure modes added by commit `babba96` (PR #41) | law 44; failure modes 148 to 160 (13) | [C] | `git show --stat babba96` | `x3d.loom@babba96:LOOM-v1.md` |
| N-LAW-7 | [02](02-loom-laws.md) | negative controls caught, each mode | 82 (normal and `-O`) | [C] | loomkit `test_gates.py`, Python 3.13.18 | `x3d.loom@162ab18:kit/tests/test_gates.py` |
| N-LAW-8 | [02](02-loom-laws.md) | trap rules, page-trap rules, page forms, two-sided | 15, 8, 10 | [C] | loomkit self-test | `x3d.loom@162ab18:kit/loomkit/traps.py`, `pagetraps.py` |
| N-LAW-9 | [02](02-loom-laws.md) | physics diagnostic codes and tests | 18 codes; 30 physics tests | [C] | `physics.py` docstring; `last-run.json` | `x3d.loom@162ab18:kit/loomkit/physics.py` |
| N-LAW-10 | [02](02-loom-laws.md) | physics witness on the two real records | cap 3 pass; cap 0 `PHYS_WAIVERS_OVER_CAP` | [C] | loomkit physics, `x3d.physics/runs` | `x3d.loom@162ab18:x3d.physics/runs/` |
| N-LAW-11 | [02](02-loom-laws.md) | mutation controls on the real record | 14 of 14 caught | [C] | `physx_controls.py` | `x3d.loom@162ab18:x3d.physics/tools/physx_controls.py` |
| N-LAW-12 | [02](02-loom-laws.md) | steps recorded and replay hosts, Chromium and Firefox records | 1918 and 969 steps; 5 replays each, 0 mismatches | [C] | loomkit physics, one machine | `x3d.loom@162ab18:x3d.physics/runs/` |
| N-LAW-13 | [02](02-loom-laws.md) | profiles with a `traps` entry pinning 11 and 15 rules | 15 pin 11; 2 pin 15; the kit has 15 | [C] | python over `kit/profiles/*.json` | `x3d.loom@162ab18:kit/profiles/` |
| N-LAW-14 | [02](02-loom-laws.md) | failure modes that record a recurrence | 7 (55, 58, 72, 73, 94, 107, 128) | [C] | regex over section 8, 2 false hits removed | `x3d.loom@162ab18:LOOM-v1.md` |
| N-LAW-15 | [02](02-loom-laws.md) | failure-mode classes in this chapter, ids covered once | 11 classes, 160 ids | [C] | D-LAW-7 script | this chapter, section 3 |
| N-LAW-16 | [02](02-loom-laws.md) | disagreement rows in `SOURCES.md` section 2 | 16 (README says 14) | [C] | count | `x3d.loom@162ab18:SOURCES.md` |
| N-LAW-17 | [02](02-loom-laws.md) | rules R1 to R33 in `LEARNINGS-from-patches.md` section 6 | 33 (README says 25) | [C] | count | `x3d.loom@162ab18:LEARNINGS-from-patches.md` |
| N-LAW-18 | [02](02-loom-laws.md) | physics playbook witness patterns | 19 (README says ten) | [C] | count | `x3d.loom@162ab18:PHYSICS-PLAYBOOK.md` |
| N-LAW-19 | [02](02-loom-laws.md) | leak sweep of the public snapshot | status pass, 67 replacements, residue empty | [L] | as recorded, not re-run | `x3d.loom@162ab18:SWEEP-REPORT.json` |
| N-LAW-20 | [02](02-loom-laws.md) | laws whose check column starts `code:` and `process:` | 27 and 17 | [L] | D-LAW-2 script (judgement of the column) | this chapter, section 2 |
| N-VAL-1 | [03](03-validator-and-gates.md) | distinct rule ids in `semantic.py` | 51 | C | `x3d_mcp fork b4efcd3`, Python `ast` | x3d_mcp@b4efcd3:src/validation/semantic.py |
| N-VAL-2 | [03](03-validator-and-gates.md) | same, at the fork base | 19 ids, 10 check functions, 24 report sites | C | `x3d_mcp upstream 74da0ec`, Python `ast` | x3d_mcp@74da0ec:src/validation/semantic.py |
| N-VAL-3 | [03](03-validator-and-gates.md) | rule ids across semantic, splat arrays, splat inspector | 72 (51 + 2 + 19) | C | `x3d_mcp fork b4efcd3`, Python `ast` | x3d_mcp@b4efcd3:src/validation/{semantic,splat_arrays}.py, src/transfer/inspect_splats.py |
| N-VAL-4 | [03](03-validator-and-gates.md) | hint rule ids and edit operations | 19 and 10 | C | `x3d_mcp fork b4efcd3`, regex and `ast` | x3d_mcp@b4efcd3:src/validation/hints.py |
| N-VAL-5 | [03](03-validator-and-gates.md) | full test suite | 1,367 passed, 27 skipped, 1,394 collected, 104 s | C | pytest 9.2.0, Python 3.13.18, no Chromium | x3d_mcp@b4efcd3:tests/ |
| N-VAL-6 | [03](03-validator-and-gates.md) | concrete nodes in X3DUOM 4.0 and 4.1 | 260 and 267; 7 only in 4.1 | C | `X3DUOM 4.1` (4fc10e8e15c0), `X3DUOM 4.0` (7e426a238656) | x3d_mcp@b4efcd3:src/validation/schemas/X3dUnifiedObjectModel-4.{0,1}.xml |
| N-VAL-7 | [03](03-validator-and-gates.md) | XSD cold compile | 1,456 ms (4.0), 1,547 ms (4.1) | C | `x3d_mcp fork b4efcd3`, libxml2 2.14.6, 4 vCPU 2.30 GHz | scratch timing run, 2026-11-14 |
| N-VAL-8 | [03](03-validator-and-gates.md) | warm repeat-call median, 12-line scene | 0.022 ms XSD, 0.314 ms semantic, 0.371 ms gate | C | `x3d_mcp fork b4efcd3`, 300 runs each | scratch timing run, 2026-11-14 |
| N-VAL-9 | [03](03-validator-and-gates.md) | faulty scenes passing the XSD, and carrying a semantic error | 8 of 15, and 6 of those 8 | C | `x3d_mcp fork b4efcd3` | 15 scratch scenes, section 4 |
| N-VAL-10 | [03](03-validator-and-gates.md) | hint loop on the 13 invalid scenes | 10 end valid, 2 of them by deleting a node, 3 not fixed | C | `x3d_mcp fork b4efcd3` `exact_fix_hints(apply=true)` | scratch run, 2026-11-14 |
| N-VAL-11 | [03](03-validator-and-gates.md) | exact-fix evaluation re-run | 540 cases, 577 errors; 14.1% before, 96.7% after, 49.6% seed-exact, 2.8% by removal | C | `x3d_mcp fork b4efcd3`, seed 20261029 | x3d_mcp@b4efcd3:evaluation/exact_fix_eval.py |
| N-VAL-12 | [03](03-validator-and-gates.md) | exact-fix numbers in the docs | 96.9% after, 15.0% before, 47.6% seed-exact (570 errors) | L | stated in the repo, not re-derived at its commit | x3d_mcp@b4efcd3:docs/EXACT-FIX-HINTS.md |
| N-VAL-13 | [03](03-validator-and-gates.md) | oversize verdict | 11,700,036-byte start tag, `checked: false`, 1,763 ms | C | `x3d_mcp fork b4efcd3`, `X3D XSD 4.1` | scratch probe, 2026-11-14 |
| N-VAL-14 | [03](03-validator-and-gates.md) | loomkit controls | 82 negative controls, 15 trap rules, 8 page-trap rules, 10 page forms, both `-O` modes, 3.8 s | C | loomkit `162ab18` | x3d.loom@162ab18:kit/tests/test_gates.py |
| N-VAL-15 | [03](03-validator-and-gates.md) | loomkit sub-commands | 17 | C | loomkit `162ab18`, read | x3d.loom@162ab18:kit/loomkit/cli.py |
| N-VAL-16 | [03](03-validator-and-gates.md) | recorded grammar witnesses per validator pin | fa0b389: 15; 327c5c4: 4; 13121b6: 1; none: 4 (24 total) | C | loomkit `162ab18` evidence records | x3d.loom@162ab18:runs/*/evidence/grammar.json |
| N-VAL-17 | [03](03-validator-and-gates.md) | blender-io catalogue | 195 cases: 148 CORE, 21 FIDELITY, 26 ROADMAP | C | `x3d-blender-io@ab99988` catalogue | x3d-blender-io@ab99988:docs/test-suite/x3d_case_catalog.md |
| N-VAL-18 | [03](03-validator-and-gates.md) | blender-io recorded CORE scoreboard | 143 pass 4 fail, then 147 / 147 (194-case scene) | C | recorded reports parsed; Blender 5.2.2 and 5.1.0, add-on v2.6.1 | x3d-blender-io@ab99988:docs/test-suite/reports/ |
| N-VAL-19 | [03](03-validator-and-gates.md) | blender-io "148/148" | not recorded | S | not run (no Blender here) | x3d-blender-io@ab99988:docs/test-suite/SUITE_COMMENTARY.md |
| N-VAL-20 | [03](03-validator-and-gates.md) | new rule scratch patch | tests 148 to 151 passed; false positives 2 to 1 of 14 scenes | C | scratch copy of `x3d_mcp fork b4efcd3` | scratch patch, section 10 |
| N-VAL-21 | [03](03-validator-and-gates.md) | masterclass rule count at `13121b6` | 62 (definition not recoverable) | L | stated in the teardown; not reproduced | x3d.docs@f172f67:docs/x3d_mcp/MASTERCLASS.md |
| N-MCP-1 | [04](04-mcp-for-agents.md) | tools, prompts, resources registered | 53, 5, 2 (FastMCP lists 1 resource and 1 template) | C | `x3d_mcp fork b4efcd3`, Python `ast`, `mcp` 1.30.0 | x3d_mcp@b4efcd3:src/tools/*.py |
| N-MCP-2 | [04](04-mcp-for-agents.md) | tools by transport | stdio 53; HTTP with token 53; HTTP without token 47 | C | `x3d_mcp fork b4efcd3`, `list_tools()` | x3d_mcp@b4efcd3:src/server.py |
| N-MCP-3 | [04](04-mcp-for-agents.md) | tools and prompts at the fork base | 34 and 4 | C | `x3d_mcp upstream 74da0ec`, `list_tools()` | x3d_mcp@74da0ec:src/server.py |
| N-MCP-4 | [04](04-mcp-for-agents.md) | `tools/list` size, compact JSON | 28,075 B (base); 64,426 B (stdio); 56,205 B (HTTP no token) | C | `x3d_mcp upstream 74da0ec`, `x3d_mcp fork b4efcd3` | scratch run, 2026-11-14 (method in D-MCP-2) |
| N-MCP-5 | [04](04-mcp-for-agents.md) | growth of `tools/list` over the base | +36,351 B (+129.5 %) | C | arithmetic on N-MCP-4 | section 2 |
| N-MCP-6 | [04](04-mcp-for-agents.md) | server instructions length | 2,212 (base); 3,353 (HTTP no token); 4,692 (stdio) characters | C | `x3d_mcp upstream 74da0ec`, `x3d_mcp fork b4efcd3` | x3d_mcp@b4efcd3:src/server.py |
| N-MCP-7 | [04](04-mcp-for-agents.md) | tool functions that are `async def` | 26 of 53 | C | `x3d_mcp fork b4efcd3`, `inspect.iscoroutinefunction` | section 8 harness, 2026-11-14 |
| N-MCP-8 | [04](04-mcp-for-agents.md) | bytes crossing the tool boundary, 10 edits, 40,000-node scene (6,505,087 B) | 176,462,418 inline; 10,849 by `blob_id` | C | `x3d_mcp fork b4efcd3`, in-process | scratch run, 2026-11-14 (method in D-MCP-3) |
| N-MCP-9 | [04](04-mcp-for-agents.md) | same, 4,000-node scene (642,887 B) | 17,494,418 inline; 10,756 by `blob_id` | C | `x3d_mcp fork b4efcd3`, in-process | D-MCP-3, 2026-11-14 |
| N-MCP-10 | [04](04-mcp-for-agents.md) | `blob_put` stored size of the 40,000-node scene | 100,091 B (zstd) for 6,505,087 B | C | `x3d_mcp fork b4efcd3`, zstandard 0.25.0 | scratch run, 2026-11-14 (method in D-MCP-3) |
| N-MCP-11 | [04](04-mcp-for-agents.md) | SDK request-body cap | 4 MiB (4,194,304 B), `413 Request body too large` | C | `mcp` 1.30.0 `server/transport_security.py` (read) | installed package source |
| N-MCP-12 | [04](04-mcp-for-agents.md) | splat run, 200,000 splats (11,200,362 B) | `splat_inspect` 3,310 B in 0.17 s; `splat_chunk` 4 chunks of 6.5 to 6.6 MB in 4.87 s, 5 of 5 files valid | C | `x3d_mcp fork b4efcd3`, numpy 2.5.4 | scratch run, seed 20261114 |
| N-MCP-13 | [04](04-mcp-for-agents.md) | oversize start tag | 11,700,036 B, `checked: false`, 1,763 ms | C | `x3d_mcp fork b4efcd3`, libxml2 2.14.6 | scratch probe, 2026-11-14 |
| N-MCP-14 | [04](04-mcp-for-agents.md) | SPARQL guard defaults | 20,000 chars; 20 s; 20,000 rows | C | `x3d_mcp fork b4efcd3` (read; refusals exercised at 1 s and 5 rows) | x3d_mcp@b4efcd3:src/x3d_utils/ontology_guard.py |
| N-MCP-15 | [04](04-mcp-for-agents.md) | test suite | 1,367 passed, 27 skipped, 1,394 collected, 104 s | C | pytest 9.2.0, Python 3.13.18, no Chromium | x3d_mcp@b4efcd3:tests/ |
| N-MCP-16 | [04](04-mcp-for-agents.md) | one 645 B scene, answer sizes | `validate_x3d` 62 B valid, 285 B one error; `exact_fix_hints` 1,325 B; `blob_put` 331 B; summary 539 B | C | `x3d_mcp fork b4efcd3` | section 7 table |
| N-MCP-17 | [04](04-mcp-for-agents.md) | first `validate_x3d` call per schema version | 1,443 to 1,645 ms over two runs (4.1 and 4.0); later calls under 1 ms | C | `x3d_mcp fork b4efcd3`, libxml2 2.14.6 | section 8 byte table |
| N-MCP-18 | [04](04-mcp-for-agents.md) | ledger probes on two records | edit caught, first-record drop caught, fresh forged chain verifies | C | `x3d_mcp fork b4efcd3` | D-MCP-6 |
| N-MCP-19 | [04](04-mcp-for-agents.md) | stdio `path=` reach | 2 `validate_x3d` reads, 1 of 2 `blob_put` reads; 27 allowed extensions | C | `x3d_mcp fork b4efcd3` | D-MCP-5 |
| N-MCP-20 | [04](04-mcp-for-agents.md) | tools in the masterclass snapshot | 48 (and 34 at the base) | L | stated in the teardown at `13121b6`, not re-run | x3d.docs@f172f67:docs/x3d_mcp/MASTERCLASS.md |
| N-MCP-21 | [04](04-mcp-for-agents.md) | repo-stated zstd ratio on a real 10.9 MB scene | 25 to 1 | L | stated in the repo, not re-run | x3d_mcp@b4efcd3:docs/transfer-layer.md |
| N-MCP-22 | [04](04-mcp-for-agents.md) | PR claims: false positives 96 to 22 (264 scenes); blind set 62.6 % to 100 % | as stated | L | PR descriptions via the masterclass; not re-derived | x3d.docs@f172f67:docs/x3d_mcp/MASTERCLASS.md |
| N-SEM-1 | [05](05-semantic-layer.md) | tools, prompts at b4efcd3 | 53 tools, 5 prompts, 1 resource, 1 template; 51 tools without numpy | C | `x3d_mcp fork b4efcd3`, in-memory `list_tools` | x3d_mcp@b4efcd3:src/server.py |
| N-SEM-2 | [05](05-semantic-layer.md) | tools, prompts at the PR base | 48 tools, 4 prompts | C | `x3d_mcp fork 13121b6` | x3d_mcp@13121b6:src/server.py |
| N-SEM-3 | [05](05-semantic-layer.md) | converter vs Saxon goldens | graph-isomorphic 10 of 10; text-identical 0 of 10 | C | `x3d_mcp fork b4efcd3`, rdflib 7.6.0 | x3d_mcp@b4efcd3:tests/fixtures/scene_rdf/ |
| N-SEM-4 | [05](05-semantic-layer.md) | ontology 4.1 as bundled | 18,108 triples, 364 classes, 337 object and 727 datatype properties, sha256 057f1ba083a6 | C | rdflib 7.6.0 | x3d_mcp@b4efcd3:src/validation/schemas/X3dOntology4.1.ttl |
| N-SEM-5 | [05](05-semantic-layer.md) | domain pooling, 4.1 (4.0) | 901 (877) properties with a domain, 294 (296) with several, max 355 (347), `DEF` 337 (329) | C | rdflib 7.6.0 | same files |
| N-SEM-6 | [05](05-semantic-layer.md) | axioms that could reject a node | 0 `owl:disjointWith`, 0 `owl:Restriction`, both releases | C | rdflib 7.6.0 | same files |
| N-SEM-7 | [05](05-semantic-layer.md) | containerField defaults | 235 of 252 (3.3), 261 of 278 (4.0), 268 of 285 (4.1) elements | C | converter tables sha256 1a5f3229a7ee | x3d_mcp@b4efcd3:src/validation/schemas/X3dToTurtle-tables.json |
| N-SEM-8 | [05](05-semantic-layer.md) | positional IRI churn | 42 to 43 individuals; 34 kept, 8 renamed; 5 of 5 DEF-named kept | C | `x3d_mcp fork b4efcd3` | one NavigationInfo inserted into HelloWorld |
| N-SEM-9 | [05](05-semantic-layer.md) | Box: map vs gate vs XSD | map 12 parents (10 concrete); gate 10; both 9; XSD on gate pairs A 5, R 3, I 2 | C | `x3d_mcp fork b4efcd3`, `X3DUOM 4.1`, `X3D XSD 4.1` | `ontology_vs_gate("Box")` |
| N-SEM-10 | [05](05-semantic-layer.md) | ImageTexture: map vs gate vs XSD | map 85 rows, 62 parents (55 concrete); gate 36 pairs, 14 parents; both 12; XSD gate A 31, R 1, I 4; map-only R 42, I 2 | C | same | `ontology_vs_gate("ImageTexture")` |
| N-SEM-11 | [05](05-semantic-layer.md) | `subclass` inference | HelloWorld +81 triples, types 3 / 3 / 8, 688 ms; LabScene41 +72, 3 / 4 / 6, 46 ms | C | `x3d_mcp fork b4efcd3` `rdf_infer` | scratch run, 2026-11-14 |
| N-SEM-12 | [05](05-semantic-layer.md) | RDFS and OWL-RL closure | RDFS +17,985 (HelloWorld, 4.9 s), +18,620 (LabScene41); OWL-RL +32,510 and +33,394, about 15 s | C | owlrl 7.6.2 | same |
| N-SEM-13 | [05](05-semantic-layer.md) | DEF effect on type count (RDFS) | DEF'd Transform 343, DEF-less Group 51, Scene 46; Box plus Transform node under OWL-RL: 14 types, 0 `owl:Nothing` | C | owlrl 7.6.2 | same |
| N-SEM-14 | [05](05-semantic-layer.md) | `x3d-core` shapes | 9 node shapes, 11 property shapes, 12 check ids, 5 `sh:agentInstruction`; slice 1,734 triples | C | rdflib, pyshacl 0.40.2 | x3d_mcp@b4efcd3:src/validation/schemas/shapes/x3d-core.shacl.ttl |
| N-SEM-15 | [05](05-semantic-layer.md) | shapes on fixtures, no inference | 7 clean: 0 V, 3 W (S4); Faulted 4 V + 2 W; BoxChild 1 V; LabScene41Faulted 3 V | C | pyshacl 0.40.2 | x3d_mcp@b4efcd3:tests/fixtures/scene_rdf/ |
| N-SEM-16 | [05](05-semantic-layer.md) | false alarm with `inference="rdfs"` | clean HelloWorld 2,185 results (2,180 V, 5 W), 17.3 s; faulted 2,236; 2 of 6 faults gone | C | pyshacl 0.40.2, owlrl 7.6.2 | D-SEM-6 |
| N-SEM-17 | [05](05-semantic-layer.md) | contact shape on ShelfCase | Lamp floating 0.85, Book sunk -0.2; XSD valid, `validate_semantic` 0 errors, `x3d-core` 0 results; LabScene41 Orb floating 1.00 | C | `x3d_mcp fork b4efcd3`, pyshacl 0.40.2 | section 7 |
| N-SEM-18 | [05](05-semantic-layer.md) | arity shapes on 3 colours | naive minCount flags 2 (white wrongly); SPARQL arity 1; `sh:minListLength` 0 | C | pyshacl 0.40.2 | D-SEM-7 |
| N-SEM-19 | [05](05-semantic-layer.md) | legality query by release | 6 rows (4.0), 1 row (4.1) on HelloWorldFaulted | C | `x3d_mcp fork b4efcd3` | D-SEM-4 |
| N-SEM-20 | [05](05-semantic-layer.md) | duplicate rows, joined graph | 4 plain, 1 with DISTINCT or without the ontology | C | rdflib 7.6.0 | D-SEM-8 |
| N-SEM-21 | [05](05-semantic-layer.md) | tool caps | 300,000 triples; 120,000 inline characters; 20,000 query characters; 20 s; 20,000 rows; 500 per page; 8 graphs; 256,000 shape characters; 120 XSD documents | C | read, not run | x3d_mcp@b4efcd3:src/x3d_utils/{semantic_web,ontology_guard}.py |
| N-SEM-22 | [05](05-semantic-layer.md) | session fault matrix | colour seen by 3 of 4 layers, USE-before-DEF 1, ROUTE 2, floating and sunk 1 | C | `x3d_mcp fork b4efcd3` | section 9 |
| N-SEM-23 | [05](05-semantic-layer.md) | claim ledger tamper test | 3 records verify; one changed character fails at index 0 | C | `x3d_mcp fork b4efcd3` | `claim_append`, `claims_verify` |
| N-SEM-24 | [05](05-semantic-layer.md) | the lab page | not yet published; no ontology-lab page at the pinned commit | C | `x3d.demo@d10b457` directory read | x3d.demo@d10b457:docs/demos/ |
| N-XIT-1 | [06](06-xite-the-oracle.md) | X3DUOM 4.1 concrete nodes | 267 | C | `X3DUOM 4.1` (sha256 4fc10e8e15c0), ElementTree | x3d_mcp@b4efcd3:src/validation/schemas/X3dUnifiedObjectModel-4.1.xml |
| N-XIT-2 | [06](06-xite-the-oracle.md) | nodes X_ITE can `createNode` | 266 of 267 (`ProtoInstance` fails); same on 5 patches | C | `X_ITE 16.7.0` (and 16.4.3, 16.5.1, 16.6.1, 16.7.1), Chromium 153, SwiftShader | scratch run, 2026-11-14 (D-XIT-1) |
| N-XIT-3 | [06](06-xite-the-oracle.md) | registered node names | 294 at 16.7.0; 295 at 16.7.1; 266 in X3DUOM 4.1, 28 not | C | regex over unminified `dist/` | npm tarball `x_ite@16.7.0` (D-XIT-1) |
| N-XIT-4 | [06](06-xite-the-oracle.md) | supported components | 39 on 5 patches | C | `X_ITE 16.7.0`, `browser.supportedComponents` | scratch run, 2026-11-14 |
| N-XIT-5 | [06](06-xite-the-oracle.md) | webpack modules, own sources | 752 in 24 bundles, 730 own (16.4.3 to 16.7.0); 762 and 732 at 16.7.1 | C | marker scan, `X_ITE 16.7.0` | npm tarballs (D-XIT-7) |
| N-XIT-6 | [06](06-xite-the-oracle.md) | `x_ite.min.js` size | 1,306,961 B raw; 280,795 B at `gzip -9`; sha256 prefix b7df063e8cb1; byte-identical to the vendored copy | C | `wc`, `gzip -9`, `sha256sum` | x3d.docs@f172f67:docs/vendor/x_ite/x_ite.min.js |
| N-XIT-7 | [06](06-xite-the-oracle.md) | WebGL2 only | 1 `getContext ("webgl2")` line; 0 hits for webgpu | C | grep, `X_ITE 16.7.0` | npm tarball `x_ite@16.7.0` |
| N-XIT-9 | [06](06-xite-the-oracle.md) | release cadence, 16.x | 23 releases, 2026-07-27 to 2026-11-08, median gap 5.7 d, 68 in 365 d | C | npm 10.9.9 `npm view x_ite time` | npm registry, read 2026-11-14 |
| N-XIT-10 | [06](06-xite-the-oracle.md) | npm versions and maintainers | 306 versions; 1 maintainer; latest 16.7.1 | C | npm 10.9.9 | npm registry, read 2026-11-14 |
| N-XIT-11 | [06](06-xite-the-oracle.md) | draw test, visible box | 0.1752 on 5 patches | C | `X_ITE 16.4.3` to `16.7.1`, Chromium 153, SwiftShader, 320 x 240 | scratch run (D-XIT-2) |
| N-XIT-12 | [06](06-xite-the-oracle.md) | draw test, blank and off-camera | 0.0000 on 5 patches; first two frames 1.0000 | C | same | scratch run (D-XIT-2) |
| N-XIT-14 | [06](06-xite-the-oracle.md) | picking with a pickable faint shape | 0 events; 1 event after `pointerEvents = false` | C | `X_ITE 16.4.3`, `16.5.1`, `16.7.0` | scratch run (D-XIT-4) |
| N-XIT-15 | [06](06-xite-the-oracle.md) | hosted-page policy trap | canvas 0 x 0 CSS, 1 x 1 buffer; 0.1752 with the fix | C | `X_ITE 16.5.1`, `16.7.0`, emulated policy | scratch run (D-XIT-3) |
| N-XIT-16 | [06](06-xite-the-oracle.md) | callback freeze | B events per 500 ms: 28 to 31 guarded, 0 throwing | C | `X_ITE 16.5.1`, `16.7.0`, `16.7.1` | scratch run (D-XIT-6) |
| N-XIT-17 | [06](06-xite-the-oracle.md) | vendored patches in `x3d.demo` | 20 files: 1 x 16.4.3, 13 x 16.5.1, 5 x 16.6.0, 1 x 16.7.0; 29 pages | C | shell over banners | x3d.demo@d10b457:docs/demos (D-XIT-8) |
| N-XIT-18 | [06](06-xite-the-oracle.md) | renderer vs validator, seven scenes | all draw 0.1752; 5 invalid or inconsistent; 3 dropped something silently | C | `X_ITE 16.7.0`; `x3d_mcp fork b4efcd3` | scratch run (D-XIT-5) |
| N-XIT-19 | [06](06-xite-the-oracle.md) | browser option defaults | `ColorSpace LINEAR_WHEN_PHYSICAL_MATERIAL`, `ToneMapping NONE`, `DisplayColorSpace SRGB`, `Exposure 1`, `Multisampling 4`, `OrderIndependentTransparency false`, `MaximumFrameRate 80` | C | `X_ITE 16.4.3` to `16.7.1`, `getBrowserOption` | scratch run, 2026-11-14 |
| N-XIT-21 | [06](06-xite-the-oracle.md) | version diff 16.4.3 to 16.7.1 | 2 renames, +10 modules and +1 node at 16.7.1; defaults unchanged | C | marker and name scan | npm tarballs (section 8) |
| N-XIT-22 | [06](06-xite-the-oracle.md) | locus shares (H7) | `WebXR` 100%, `GaussianSplats` 83%, `Text` 68%, `RigidBodyPhysics` 1%, `HAnim` 0% | C | marker scan, `X_ITE 16.7.0` | npm tarball (D-XIT-7) |
| N-XIT-23 | [06](06-xite-the-oracle.md) | teardown anatomy | 98,369 lines, 730 modules, 5,940 functions; 194 / 43 / 29 / 1 field conformance | L | read, not re-run | x3d.docs@f172f67:docs/x_ite/MASTERCLASS.md |
| N-XIT-24 | [06](06-xite-the-oracle.md) | curriculum | 32 steps in 4 tracks of 8 | C | read in the exact file | x3d.docs@f172f67:docs/x_ite/MASTERCLASS.md |
| N-XRY-1 | [07](07-xray.md) | declared looks | 12 (6 contrasts, 6 drifts); manifest sha256 prefix a5fce6ec4bade0c8 | C | `x3d.xray@8fa6845` | x3d.xray@8fa6845:x3dray/looks.py |
| N-XRY-2 | [07](07-xray.md) | thresholds | Cliff floor 147/1000, TV floor 1/10, alpha 1/20, q survive 1/10, q Confirmed 1/20, MIN_SIDE 20, M 199..999, WORK_CAP 10,000,000 | C | read in code | x3d.xray@8fa6845:x3dray/looks.py |
| N-XRY-3 | [07](07-xray.md) | noise calibration | 4 of 150 pure-noise histories earn a Confirmed (2.67%) | C | `examples/eda_1_signal_and_noise.py --calibrate`, seeds 1000 to 1149 | x3d.xray@8fa6845:examples/ |
| N-XRY-4 | [07](07-xray.md) | planted signal | 2 C looks (effect 647/1000 and 380/1000, q 0.0060) | C | same, seed 7 | same |
| N-XRY-5 | [07](07-xray.md) | price of looking | q 0.0130 at m = 13; 0.0510 at m = 51; 0.0120 at m = 12 | C | `stats.bh_q` | x3d.xray@8fa6845:x3dray/stats.py |
| N-XRY-6 | [07](07-xray.md) | SplitMix64 seed 0 first word | 16294208416658607535 (0xE220A8397B1DCDAF) | C | `stats.SplitMix64` | x3d.xray@8fa6845:x3dray/stats.py |
| N-XRY-7 | [07](07-xray.md) | largest passing permutation count at M = 999 | 49 | C | arithmetic on `ALPHA` | x3d.xray@8fa6845:x3dray/looks.py |
| N-XRY-8 | [07](07-xray.md) | test suite | 857 ran, 810 passed, 3 failed, 24 errored, 20 skipped, 295.5 s | C | `unittest discover`, Git 2.43.0, Python 3.13.18 | x3d.xray@8fa6845:tests/ |
| N-XRY-9 | [07](07-xray.md) | JS twin and inference tests | 37 and 16 tests pass | C | `test_eda_infer`, `test_eda_js_parity`, Node 22.23.4 | x3d.xray@8fa6845:tests/ |
| N-XRY-10 | [07](07-xray.md) | gallery suite | 43 pass; 42 pass with a shared sign mistake | C | scratch copy, Python 3.13.18 | x3d.xray@8fa6845:tests/test_gallery.py |
| N-XRY-11 | [07](07-xray.md) | tool set | 11 shared, 1 MCP-only, 4 page-only | C | `python3 -m x3dray tools` | x3d.xray@8fa6845:x3dray/web/tools.js |
| N-XRY-12 | [07](07-xray.md) | repository size | 12,844 Python lines in `x3dray/`, 4,842 JavaScript lines in the web folders, 44 test files, 875 `def test_` lines | C | `wc -l`, grep | x3d.xray@8fa6845 |
| N-XRY-13 | [07](07-xray.md) | synthetic scene | `xray.x3d` 125,302 B, 98 labels, 12 buildings, 16 commits; XSD 4.0 valid | C | `x3d_mcp fork b4efcd3`, lxml 6.1.3 | experiments/smoke_synthetic_pipeline.py run |
| N-XRY-14 | [07](07-xray.md) | semantic findings on that scene | 0 errors, 7 warnings, 145 info | C | `x3d_mcp fork b4efcd3` | same |
| N-XRY-15 | [07](07-xray.md) | `MetadataString` tagged | 90 of 90; stripped: 90 `containerfield-unknown`, XSD errors 0 | C | `x3d_mcp fork b4efcd3` | same (D-XRY-5) |
| N-XRY-16 | [07](07-xray.md) | smoke pipeline | `ok` true, `release_ready` false; 3 gates pass, 4 skipped; page 37 files, 6,295,152 B | C | `x3d.xray@8fa6845` | smoke JSON, 2026-11-14 |
| N-XRY-17 | [07](07-xray.md) | thin repo: history | 10 commits, 1 day, ai 9 and you 1, 363 files | C | `x3d.xray@8fa6845` on `x3d.castle@d70e00c` | D-XRY-4 |
| N-XRY-18 | [07](07-xray.md) | thin repo: tree | 12,218,378 B, 78,637 text lines; top 64 files 79.2% of lines | C | same | same |
| N-XRY-19 | [07](07-xray.md) | thin repo: churn | 274 of 283 text files churn equals size; 349 of 363 files in one commit | C | same | same |
| N-XRY-20 | [07](07-xray.md) | thin repo: EDA | 12 looks, 0 evaluated; lattice 1 concept over 15 files | C | same | same |
| N-XRY-21 | [07](07-xray.md) | pass 1 benchmark | 121 nodes: 10.14 s to 0.63 s (16.08x), outputs hash-equal | L | read, not re-run | x3d.xray@8fa6845:docs/development-pass-1.html |
| N-XRY-22 | [07](07-xray.md) | pass tests | 178, 312 and 442 Python tests at passes 1, 2, 3 | L | read, not re-run | x3d.xray@8fa6845:docs/development-pass-{1,2,3}.html |
| N-XRY-23 | [07](07-xray.md) | pass 3 layout repair | 7,936 overlapping glyph pairs to 0 at 1,000 entities | L | read, not re-run | x3d.xray@8fa6845:docs/development-pass-3.html |
| N-XRY-24 | [07](07-xray.md) | limits of the calibration | 4 of 150 is for these seeds and this generator | C | `examples/eda_1_signal_and_noise.py` | x3d.xray@8fa6845:examples/ |
| N-BAB-1 | [08](08-babylon-bridge.md) | concrete nodes in the bridge tracker | 260 | C | `X3DUOM 4.0` via `NODES.json` | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-2 | [08](08-babylon-bridge.md) | tracker headline "reader knows" | 186 of 260 (71.5%): base 75, gap 70, bridged 41; claimed 8, blocked 1, todo 65 | C | `driver.py status`, `x3d.loom@162ab18` | x3d.loom@162ab18:x3d.webgpu/bridge/tools/driver.py (D-BAB-1) |
| N-BAB-3 | [08](08-babylon-bridge.md) | page-bundle census, 8 Nov tree | 68 of 260 (72 defs) | C | `census.js` on `git archive 60824ce` | x3d.loom@60824ce:x3d.webgpu/demo/src (D-BAB-2) |
| N-BAB-4 | [08](08-babylon-bridge.md) | page-bundle census, today | 75 of 260 (79 defs); 83 (87) with the hall extension | C | `census.js`, 162ab18 | x3d.loom@162ab18:x3d.webgpu/bridge/tools/census.js |
| N-BAB-5 | [08](08-babylon-bridge.md) | bridged without a logged gap | 41 of 260 (15.8%) | C | `driver.py status` | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-6 | [08](08-babylon-bridge.md) | batch headlines 20 to 26 | 175, 175, 179, 184, 184, 181, 186 | L | read in `BATCH-NN.md` | x3d.loom@162ab18:x3d.webgpu/bridge/BATCH-20.md to BATCH-26.md |
| N-BAB-7 | [08](08-babylon-bridge.md) | slots filled by batches 21 to 26 | 30: 17 bridged, 13 gap; PRs #43 to #45 | C | `NODES.json`, merge log | x3d.loom@162ab18:x3d.webgpu/bridge/NODES.json |
| N-BAB-8 | [08](08-babylon-bridge.md) | visual compare rows, batches 21 to 26 | 42 rows; PSNR 11.73 to 40.03, median 35.92 | C | parsed from the reports; X_ITE 16.6.0, 320 x 240, SwiftShader | x3d.loom@162ab18:x3d.webgpu/bridge/BATCH-21.md to BATCH-26.md |
| N-BAB-9 | [08](08-babylon-bridge.md) | X_ITE 16.7.0 WebGPU strings | 0 "webgpu", 0 `navigator.gpu`, 1 `getContext("webgl2"` | C | grep, `x_ite.min.js` sha256 prefix b7df063e8cb1 | x3d.docs@f172f67:docs/vendor/x_ite/x_ite.min.js (grep, section 2) |
| N-BAB-10 | [08](08-babylon-bridge.md) | merged traps | 50: first seen v1 13, v2 19, v3 13, v4 5; tiers A 14, B 20, C 11, W 5 | C (count), S (ranking) | script over the section 5 table | this chapter, section 5 |
| N-BAB-11 | [08](08-babylon-bridge.md) | distinct hash-keyed shader programs | 26 (Collider 5, brain 4, manifold 7, Gobbler 3 6, Demiurge 4); 22 on 8 Nov; 6 more keyed by DEF in Dynasty | C | grep of `'[0-9a-f]{8}-[0-9a-f]{8}'` | x3d.loom@162ab18:x3d.webgpu/demo/src |
| N-BAB-12 | [08](08-babylon-bridge.md) | facade PSNR by window | 39.30 dB whole; 41.90 dB bottom 40 rows cropped; MAE 0.84 and 0.79 | C | numpy, Pillow, 960 x 540, X_ITE 16.4.3 reference | x3d.loom@162ab18:runs/webgpu-quick-wins-20261107/ (D-BAB-4) |
| N-BAB-13 | [08](08-babylon-bridge.md) | Pantheon splats; Manifold | 50.17 and 51.01 dB; 49.34 and 48.47 dB | L | `X_ITE 16.4.3` (960 x 540); `X_ITE 16.5.1` (640 x 360); SwiftShader | x3d.loom@162ab18:runs/webgpu-{pantheon-splats,manifold}-2026110*/RECEIPT.md |
| N-BAB-14 | [08](08-babylon-bridge.md) | brain, Babylon 9.32.0 | 33.03 all; 35.11 glass to 21.53 labels; torso 30.26 | L | `X_ITE 16.6.0`, 640 x 360, SwiftShader | x3d.loom@162ab18:runs/webgpu-brain-20261107/RECEIPT.md |
| N-BAB-15 | [08](08-babylon-bridge.md) | KANSEI, masked | 24.36 to 32.46 over 6 views; sim hash equal in 6 of 6 | L | `X_ITE 16.5.1`, 640 x 360, SwiftShader | x3d.loom@162ab18:runs/webgpu-drift-20261107/RECEIPT.md |
| N-BAB-16 | [08](08-babylon-bridge.md) | Material Odyssey | 25.5 to 30.7 as authored (6 film times); 18.4 to 28.2 look on | L | `X_ITE 16.4.3`, 1280 x 536, SwiftShader | x3d.loom@162ab18:runs/webgpu-odyssey-20261108/RECEIPT.md |
| N-BAB-17 | [08](08-babylon-bridge.md) | Chirp; Cloud; Gobbler 3; Demiurge; Dynasty; Hall | 24.87 to 25.36; 19.24 to 19.40 (21.01 to 24.96 masked); 14.60 to 19.66; 7.18 to 13.26; 29.0 to 37.8; 17.5 to 25.3 dB | L | `X_ITE 16.5.1`, SwiftShader | x3d.loom@162ab18:runs/webgpu-{chirp,cloud,gobbler,demiurge,dynasty,hall}-*/ |
| N-BAB-18 | [08](08-babylon-bridge.md) | corpus name census | 111 files: 86 base-only, 22 need gap or todo or claimed, 1 unknown | C | lxml, `NODES.json` | x3d.demo@d10b457:docs/demos (D-BAB-5) |
| N-BAB-19 | [08](08-babylon-bridge.md) | real-GPU timing receipts for any bridge body | 0; `bench/receipts/` holds 1 file (the G1 adapter probe) | C | `ls` | x3d.loom@162ab18:x3d.webgpu/bench/receipts/ |
| N-BAB-27 | [08](08-babylon-bridge.md) | X_ITE volume slice count | 400 at MEDIUM (200 LOW, 600 HIGH); spacing \|dimensions\| / 399 | C | X_ITE 16.6.0, `VolumeRenderingComponent` read | x_ite 16.6.0 npm package, `VolumeRenderingComponent.js` (read) |
| N-BAB-28 | [08](08-babylon-bridge.md) | batch 43 fixture assertions | 151 over 10 nodes (19, 30, 14, 8, 18, 11, 10, 11, 11, 19) | C | x3d.loom batch 43 receipts; X_ITE 16.6.0, Chromium 153, SwiftShader | x3d.loom `receipts/` (batch 43) |
| N-BAB-29 | [08](08-babylon-bridge.md) | faint-alpha stack, bridge against X_ITE | 10 against 24 plain stack; 14 against 28 Edge; 40 against 78 Boundary | C | x3d.loom batch 43 fixtures; X_ITE 16.6.0 | `VolumeData`, `EdgeEnhancementVolumeStyle`, `BoundaryEnhancementVolumeStyle` fixtures |
| N-BAB-20 | [08](08-babylon-bridge.md) | batch 44 nodes bridged; steps passed, ours and X_ITE | 10 nodes; NurbsCurve 32 and 32, NurbsCurve2D 36 and 36, ContourPolyline2D 14 and 14, Contour2D 22 and 22, NurbsPositionInterpolator 55 and 52, NurbsOrientationInterpolator 51 and 48, NurbsSurfaceInterpolator 52 and 51, NurbsPatchSurface 35 and 35, NurbsSet 47 and 46, NurbsSwungSurface 18 and 18 | C | `driver.py batch -n 10 --close`, X_ITE 16.6.0, Chromium 153.0.8010.12, SwiftShader | x3d.loom@4887a98:x3d.webgpu/bridge/BATCH-44.md |
| N-BAB-21 | [08](08-babylon-bridge.md) | weighted quarter circle radius | 1.00 to 2.2e-16 here; up to 1.24 in X_ITE 16.6.0 | C | Node (D-BAB-6); X_ITE 16.6.0 SwiftShader | x3d.loom@4887a98:x3d.webgpu/bridge/fixtures/NurbsCurve.test.json |
| N-BAB-22 | [08](08-babylon-bridge.md) | weighted midpoint of the quarter circle | (0.7071, 0.7071, 0) here; (0.75, 0.75, 0) in X_ITE 16.6.0 | C | Node (D-BAB-6); X_ITE SAI | x3d.loom@4887a98:x3d.webgpu/bridge/fixtures/NurbsPositionInterpolator.test.json |
| N-BAB-23 | [08](08-babylon-bridge.md) | patch normal difference to X_ITE | largest component 0.21 (12 x 12 cells), 0.28 (8 x 8); spec bound 0.3 | C | X_ITE 16.6.0 private getNormals, SwiftShader | x3d.loom@4887a98:x3d.webgpu/bridge/fixtures/NurbsPatchSurface.test.json |
| N-BAB-24 | [08](08-babylon-bridge.md) | swung surface frame difference | 1.2e-7 on an even spine; up to 0.017 on a 2.2-unit vase; spec bound 0.02 | C | X_ITE 16.6.0 private getVertices, SwiftShader | x3d.loom@4887a98:x3d.webgpu/bridge/fixtures/NurbsSwungSurface.test.json |
| N-BAB-25 | [08](08-babylon-bridge.md) | NURBS visual compare rows, batch 44 | 6 rows; iou 0.85 to 0.99; mad 1.64 to 3.74; PSNR 23.38 to 37.12 dB (320 x 240) | C | X_ITE 16.6.0, SwiftShader, parsed from the report | x3d.loom@4887a98:x3d.webgpu/bridge/BATCH-44.md |
| N-BAB-26 | [08](08-babylon-bridge.md) | solid FALSE back face gap | 9312 of 19012 pixels drawn in a two-quad IndexedFaceSet fixture | C | Babylon 9.32.0 body vs X_ITE 16.6.0, SwiftShader | x3d.loom@4887a98:x3d.webgpu/bridge/fixtures/NurbsPatchSurface.test.json |
| N-BAB-30 | [08](08-babylon-bridge.md) | three.js bridge status of the 260 nodes | drawn 15, reader-checked 29, reader 50, todo 119, upstream 47 | C | `driver.py status` | x3d.loom@108a282:x3d.threejs/bridge/NODES.json |
| N-BAB-31 | [08](08-babylon-bridge.md) | lines: reader, sai, kit, 150 node files; Babylon body files; three.js body | 388, 319, 648, 5882; 518 + 234 + 919 = 1671; 284 | C | `wc -l` | x3d.loom@108a282:x3d.webgpu/ and x3d.threejs/bridge/src/body-three.js |
| N-BAB-32 | [08](08-babylon-bridge.md) | node hooks left to port | 15 geometry (15 plain data), 61 build (43 call only Body), 61 changed; 19 files name the engine | L | regex over `src/nodes/*.js` | x3d.loom@108a282:x3d.webgpu/bridge/src/nodes |
| N-BAB-33 | [08](08-babylon-bridge.md) | three.js visual rows | 16 pictures; IoU 0.90 to 1.00; PSNR 32.38 to 70.12 dB over 11, median 42.95; 5 identical (2 empty) | C | X_ITE 16.6.0, three.js r187, Chromium 153.0.8010.12, SwiftShader, 320 x 240 | x3d.loom@108a282:x3d.threejs/bridge/receipts/ |
| N-BAB-34 | [08](08-babylon-bridge.md) | first Viewpoint bound at load, IoU before and after | 0.34 to 0.64 on 10 of 10; 0.99 to 1.00 on 9 of 10, Material 0.90 | C | same rig, two runs of the 10 fixtures | x3d.loom@108a282:x3d.threejs/bridge/fixtures/ |
| N-BAB-35 | [08](08-babylon-bridge.md) | Phong exponent factor 4 | Sphere 28.22 to 36.98 dB; Box 63.84 to 70.12 dB | C | same rig | x3d.loom@108a282:x3d.threejs/bridge/src/body-three.js |
| N-BAB-36 | [08](08-babylon-bridge.md) | event fixtures through the three.js bundle | 30 run; 29 pass in ours and X_ITE; ColorDamper differs by a documented X_ITE hue-seam defect | C | X_ITE 16.6.0, Chromium 153.0.8010.12 | x3d.loom@108a282:x3d.threejs/bridge/receipts/ |
| N-BAB-37 | [08](08-babylon-bridge.md) | three.js bridge status, batch 1 | drawn 23, reader-checked 29, reader 49, todo 122, upstream 37 | C | `driver.py status` | x3d.loom@95eda37:x3d.threejs/bridge/NODES.json |
| N-BAB-38 | [08](08-babylon-bridge.md) | batch 1 lighting rows against X_ITE | SpotLight 63.14 and 63.13 dB; PointLight 36.61, 36.30, 51.15; attenuation 59.17 | C | X_ITE 16.6.0, three.js r187, SwiftShader, 320 x 240 | x3d.loom@95eda37:x3d.threejs/bridge/receipts/ |
| N-BAB-39 | [08](08-babylon-bridge.md) | Fog rows | 52.00, 53.41, 46.55 dB; IoU 0.99 | C | same rig | x3d.loom@95eda37:x3d.threejs/bridge/receipts/Fog.json |
| N-BAB-40 | [08](08-babylon-bridge.md) | texture rows | ImageTexture 99 dB (identical); PixelTexture 45.66; TextureTransform 50.12 and 50.21; textured primitives 39.58 | C | same rig | x3d.loom@95eda37:x3d.threejs/bridge/receipts/ |
| N-BAB-41 | [08](08-babylon-bridge.md) | TextureTransform order and sign, 4 variants in the Transform order and 4 in the column order | 50.12 (-C S R C T, rotation +, translation +); 21.34, 25.72, 21.39 for the other signs; 21.30 for T C R S -C | C | same rig, one run | x3d.loom@95eda37:x3d.threejs/bridge/src/body-three.js |
| N-BAB-42 | [08](08-babylon-bridge.md) | all compared pictures of the two batches | 30 pictures; IoU 0.90 to 1.00; PSNR 32.38 to 70.12 dB over 24, median 50.13; 6 identical | C | same rig | x3d.loom@95eda37:x3d.threejs/bridge/receipts/ |
| N-BAB-43 | [08](08-babylon-bridge.md) | three.js bridge status, batch 2 | drawn 53, reader-checked 29, reader 46, todo 95, upstream 37 | C | `driver.py status` | x3d.loom@38530ab:x3d.threejs/bridge/NODES.json |
| N-BAB-44 | [08](08-babylon-bridge.md) | all compared pictures after batch 2 | 61 pictures; IoU 0.90 to 1.00; PSNR 25.32 to 80.17 dB over 47 that differ, median 50.24; 14 at 99 dB (12 identical, 2 empty frames) | C | X_ITE 16.6.0, Chromium 153.0.8010.12, SwiftShader, three.js r187 | x3d.loom@38530ab:x3d.threejs/bridge/receipts/*.json |
| N-BAB-45 | [08](08-babylon-bridge.md) | pictures new in batch 2 | 31 pictures over 27 fixtures; 8 pixel-identical; IoU 0.91 to 1.00 | C | same rig | same receipts |
| N-BAB-46 | [08](08-babylon-bridge.md) | ElevationGrid triangulation | diagonal (a, c, d) (a, d, b): 99 dB; the other diagonal: mad 2.70, 29.13 dB | C | same rig, same fixture twice | x3d.loom@38530ab:x3d.threejs/bridge/src/nodes/Geometry.js |
| N-BAB-47 | [08](08-babylon-bridge.md) | Extrusion before and after BR.ifsExtras (first fixture) | IoU 0.98 to 0.99; mad 0.41 to 0.16; PSNR 39.98 to 38.65 dB; star fixture after: 0.99, 0.20, 37.51 dB | C | same rig | x3d.loom@38530ab:x3d.threejs/bridge/receipts/Extrusion.json |
| N-BAB-48 | [08](08-babylon-bridge.md) | lines of the three.js body | body-three.js 461 (was 284 for 12 core nodes), nodes/Geometry.js 115 | C | `wc -l` | x3d.loom@38530ab:x3d.threejs/bridge/src |
| N-BAB-49 | [08](08-babylon-bridge.md) | float32 resolution at geocentric radius 6.4e6 m | about 0.5 m | C | float32 spacing at 6.4e6 | x3d.loom@bfeba57:x3d.webgpu/bridge/src/nodes/GeoCoordinate.js |
| N-BAB-50 | [08](08-babylon-bridge.md) | great-circle midpoint, latitude 0 to 60, WGS84 | latitude 30.0832518, height -2663.0003 m | C | Python, X_ITE 16.6.0 | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/GeoPositionInterpolator.test.json (D-BAB-12) |
| N-BAB-51 | [08](08-babylon-bridge.md) | GeoTransform rotation 90 degrees about local up, geoCenter 111.32 m east | box 10 m east of the centre drawn 10 m north of it | C | both engines | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/GeoTransform.test.json |
| N-BAB-52 | [08](08-babylon-bridge.md) | GeoViewpoint speed, height 500 m, speedFactor 3 | 153 | C | `BR.geo.speedOf`; X_ITE formula (height + 10) / 10 x factor | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/GeoViewpoint.test.json |
| N-BAB-53 | [08](08-babylon-bridge.md) | Shaded, 16 cubed Gaussian ball, directional light, unrotated, red along a row (ours, X_ITE) | 6/42/80/115/139/154/162 and 0/39/75/108/135/159/159 | C | SwiftShader, 320 x 240 | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/_volume-smooth-lit.test.json |
| N-BAB-54 | [08](08-babylon-bridge.md) | same ball turned 0.9 rad about Z, Shaded, five probes (ours, X_ITE) | lit side 156 and 36 (ours, X_ITE) at the same probe | C | SwiftShader | rig runs of 2026-11-15, not in a fixture |
| N-BAB-55 | [08](08-babylon-bridge.md) | plain Gaussian ball, core 243, centre pixel | 18 (bridge), 23 (X_ITE) | C | SwiftShader | rig run of 2026-11-15 |
| N-BAB-56 | [08](08-babylon-bridge.md) | block of 204 filling half the width, 16 voxels, centre pixel | 70 in both engines; 204 at 8 voxels (nearest) and 97 at 32 voxels | C | SwiftShader | D-BAB-13 |
| N-BAB-57 | [08](08-babylon-bridge.md) | ProjectionVolumeStyle AVERAGE of a uniform grey 204 volume | 38 | C | both engines | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/ProjectionVolumeStyle.test.json |
| N-BAB-58 | [08](08-babylon-bridge.md) | BlendedVolumeStyle defaults, voxels 204 and 102 | 153 (ALPHA0: 215, ONE_MINUS_ALPHA0: 91) | C | both engines | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures/BlendedVolumeStyle.test.json |
| N-BAB-59 | [08](08-babylon-bridge.md) | batch 45 fixture steps passed (ours / X_ITE) | Geo 305 and 300; Blended 63 and 53, Composed 17 and 17, Projection 32 and 32 | C | `run-tests.js` | x3d.loom@bfeba57:x3d.webgpu/bridge/fixtures |
| N-BAB-70 | [08](08-babylon-bridge.md) | three.js bridge status, batch 3 | drawn 65, reader-checked 29, reader 45, todo 93, upstream 28 | C | `driver.py status` | x3d.loom@72a4bca:x3d.threejs/bridge/NODES.json |
| N-BAB-71 | [08](08-babylon-bridge.md) | all compared pictures after batch 3 | 86 pictures; IoU 0.90 to 1.00; PSNR 25.32 to 80.17 dB over 62 that differ, median 50.23; 24 at 99 dB (identical or empty frames) | C | `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 | x3d.loom@72a4bca:x3d.threejs/bridge/receipts/*.json |
| N-BAB-72 | [08](08-babylon-bridge.md) | pictures new in batch 3 | 25 pictures over 13 fixtures; 10 pixel-identical; the other 15 at 35.03 to 67.60 dB, median 48.04; IoU 0.98 to 1.00 | C | same rig | same receipts |
| N-BAB-73 | [08](08-babylon-bridge.md) | TextureProperties fixture, FASTEST read as nearest against measured smooth | 28.23 dB (mad 1.27) against 67.60 dB (mad 0.01) | C | same rig | fixtures/TextureProperties.x3d, receipts/TextureProperties.json |
| N-BAB-74 | [08](08-babylon-bridge.md) | a 4 x 4 texture on a box, smooth against hard texels | 18.80 dB against 64.50 dB | C | same rig | TextureProperties fixture, first version |
| N-BAB-75 | [08](08-babylon-bridge.md) | LineProperties, thin lines against screen-space quads | IoU 0.63 (689 against 1051 foreground pixels) against 0.98 and 47.71 dB (1069) | C | same rig | receipts/LineProperties.json |
| N-BAB-76 | [08](08-babylon-bridge.md) | MultiTexture ADD placements | frame 28.15 (canvas sum), 27.84 (after the light), 35.03 dB (before the light, unclipped); ADD cube mean red 181.1, 226.2, 214.1 against 214.9 | C | same rig | receipts/MultiTexture.json |
| N-BAB-77 | [08](08-babylon-bridge.md) | Background level view, ground stopping at the last groundAngle against held to the horizon | mad 36.07 (9.75 dB) against 0.28 (53.61 dB) | C | same rig | receipts/Background.json |
| N-BAB-78 | [08](08-babylon-bridge.md) | TwoSidedMaterial on an open cylinder, caps always drawn against honoured | 22.41 dB against 39.57 dB | C | same rig | receipts/TwoSidedMaterial.json |
| N-BAB-79 | [08](08-babylon-bridge.md) | LocalFog and FogCoordinate | 60.30 dB and 99 dB after two field events; FogCoordinate 43.55 dB twice | C | same rig | receipts/LocalFog.json, receipts/FogCoordinate.json |
| N-BAB-60 | [08](08-babylon-bridge.md) | GeoLOD, centre 50 m up, parent scale 1.9 and 2.1 | level 1 and level 0 | C | both engines | x3d.loom@c80cecd:x3d.webgpu/bridge/fixtures/GeoLOD.test.json |
| N-BAB-61 | [08](08-babylon-bridge.md) | hitGeoCoord longitude under a GeoLocation 3.3 m east of the origin | 8.4e-7 degrees (true: 3.0e-5) | C | X_ITE 16.6.0 and bridge | x3d.loom@c80cecd:x3d.webgpu/bridge/fixtures/GeoTouchSensor.test.json |
| N-BAB-62 | [08](08-babylon-bridge.md) | batch 46 fixture steps passed, ours and X_ITE alike | GeoLOD 92, GeoTouchSensor 51, GeoProximitySensor 64, GeoMetadata 30, EspduTransform 146, ReceiverPdu 69, SignalPdu 70, TransmitterPdu 82, DISEntityManager 30, DISEntityTypeMapping 43 | C | `run-tests.js` | x3d.loom@c80cecd:x3d.webgpu/bridge/fixtures |
| N-BAB-63 | [08](08-babylon-bridge.md) | batch 47 fixture steps passed, ours and X_ITE alike | CollisionSensor 36, CollisionSpace 34, Contact 30 | C | `run-tests.js` | x3d.loom@80388ce:x3d.webgpu/bridge/fixtures |
| N-BAB-64 | [08](08-babylon-bridge.md) | unit cube resting on a fixed ground, contacts kept | Bullet 2 of the 4 lower corners; bridge 4 | C | X_ITE 16.6.0, SwiftShader rig | x3d.loom@80388ce:x3d.webgpu/bridge/fixtures/CollisionSensor.test.json |
| N-BAB-65 | [08](08-babylon-bridge.md) | resting distance of a ball on the ground | X_ITE 3e-8; bridge up to 5 mm (slop) | C | both engines | WHY-physics-sensing-batch.md section 5 |
| N-BAB-66 | [08](08-babylon-bridge.md) | full regression after the shim fix and batch 47 | 142 picture fixtures and 45 event fixtures pass, in chunks of 8 | C | our engine, SwiftShader | x3d.loom@80388ce |
| N-BAB-80 | [08](08-babylon-bridge.md) | three.js bridge status, batch 5 | drawn 98, reader-checked 32, reader 41, todo 66, upstream 23 | C | `driver.py status` | x3d.loom@1192dd4:x3d.threejs/bridge/NODES.json |
| N-BAB-81 | [08](08-babylon-bridge.md) | all compared pictures after batch 5 | 116 pictures; IoU 0.65 to 1.00; PSNR 19.21 to 99 dB, median 53.67; 25 at 99 dB | C | `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 | x3d.loom@1192dd4:x3d.threejs/bridge/receipts/* |
| N-BAB-82 | [08](08-babylon-bridge.md) | cube-map pictures | ImageCubeMapTexture 31.45 and 31.98 dB; ComposedCubeMapTexture 29.12; GeneratedCubeMapTexture 34.03 (IoU 0.94 and 0.98) | C | same rig | receipts/*CubeMapTexture.json |
| N-BAB-83 | [08](08-babylon-bridge.md) | ComposedShader pictures | 40.47 and 39.75 dB, IoU 1.00; with the `#version` line left in IoU 0 (mad 21.87 and 18.17) | C | same rig | receipts/ComposedShader.json, D-BAB-72 |
| N-BAB-84 | [08](08-babylon-bridge.md) | Text against X_ITE's glyph renderer | IoU 0.65, 19.21 dB (the boxes match to the pixel) | C | same rig | receipts/Text.json |
| N-BAB-85 | [08](08-babylon-bridge.md) | CAD nodes, four fixtures of one scene | IoU 0.99; 54.88, 51.22, 51.21 and 53.67 dB | C | same rig | receipts/CAD*.json |
| N-BAB-86 | [08](08-babylon-bridge.md) | Geo fixture steps passed, ours and X_ITE alike | GeoViewpoint 98 and 96, GeoLOD 92, GeoElevationGrid 64, GeoProximitySensor 64, GeoTouchSensor 51, GeoTransform 34, GeoLocation 22 and 19, GeoOrigin 22, GeoCoordinate 16 | C | same rig | receipts/Geo*.json |
| N-BAB-87 | [08](08-babylon-bridge.md) | review of batch 4 | 171 agents, 83 raw findings, 69 survived two skeptics (10 high, 36 medium, 23 low); by lens 16 regression, 15 pointer, 15 input, 12 cube and shader, 11 Inline and Text | C | workflow run 2026-11-15 | x3d.loom pull request #70 |
| N-BAB-88 | [08](08-babylon-bridge.md) | GeoViewpoint frame, right basis against swapped | IoU 1.00 and 64.48 dB against IoU 0 and 18.49 dB (the batch-46 fixture: 98 of 98 either way) | C | same rig | receipts/GeoViewpointFrame.json |
| N-BAB-89 | [08](08-babylon-bridge.md) | GeoLocation with the matrix transposed (D-BAB-73) | 9 of 22 steps fail; the position reads 0 0 0 where 6378137 0 0 is expected | C | same rig | receipts/GeoLocation.json |
| N-BAB-95 | [08](08-babylon-bridge.md) | Layer, LayerSet, Layout, LayoutGroup, LayoutLayer, ScreenGroup, ScreenFontStyle, Viewport against X_ITE | 8 of 8 pass; 12 pictures IoU 1.00 at 99 dB (Layout 3, LayoutLayer 2, ScreenGroup 3, Viewport 4) | C | Chromium 153.0.8010.12 SwiftShader, X_ITE 16.6.0, three.js r187 | receipts/Layout.json |
| N-BAB-96 | [08](08-babylon-bridge.md) | LayerSet with the Background left on every pass (D-BAB-75) | 4 of 86 steps fail; red world box missing | C | same rig | receipts/LayerSet.json |
| N-BAB-97 | [08](08-babylon-bridge.md) | LayerHeadlight, headlight shot | IoU 0.90, 16.66 dB: the lit boxes differ in extent, the pixel probes agree | C | same rig | receipts/LayerHeadlight.json |
| N-BAB-98 | [08](08-babylon-bridge.md) | ViewportMany, ten tiles | IoU 0.98, 26.27 dB, 12 of 12 steps | C | same rig | receipts/ViewportMany.json |
| N-BAB-90 | [08](08-babylon-bridge.md) | Disk2D, Rectangle2D, Extrusion silhouette overlap with X_ITE | 0.98, 0.97, 0.93 | C | SwiftShader, 320 x 240 | x3d.loom@cd71796:x3d.webgpu/bridge/receipts |
| N-BAB-91 | [08](08-babylon-bridge.md) | PointProperties default pointSizeMin, scale, max | 1, 1, 1 in the standard and X_ITE; hall default was 0 | C | X_ITE 16.6.0 | PointProperties.test.json |
| N-BAB-92 | [08](08-babylon-bridge.md) | NurbsTextureCoordinate uv step with centre weight 3, 8 cells | 0.125 in X_ITE (regular); rational form would give 0.114 | C | X_ITE 16.6.0 | NurbsTextureCoordinate.test.json |
| N-BAB-93 | [08](08-babylon-bridge.md) | NurbsSweptSurface triangles, octagon along a bend and triangle along an arc | 160 and 36, equal in both engines | C | both engines | NurbsSweptSurface.test.json |
| N-BAB-94 | [08](08-babylon-bridge.md) | NurbsTrimmedSurface untrimmed 8 x 8 patch triangles | 128 in both engines | C | both engines | NurbsTrimmedSurface.test.json |
| N-CAS-1 | [09](09-castle-engine.md) | registered model formats; of them with `OnSave` | 21; 7 | C | `formats.py`, 2026-11-14 | `castle-engine@48ce617:src/` |
| N-CAS-2 | [09](09-castle-engine.md) | parse-only groups; registrations in them (one abstract) | 11; 99 | C | `xite_names.py` | `castle-engine@48ce617:src/scene/x3d/castleinternalnodesunsupported.pas` |
| N-CAS-3 | [09](09-castle-engine.md) | parse-only names with a same-named non-abstract class in X_ITE | 97 of 99 | C | `xite_names.py`, `x_ite@16.7.1` npm dist | `x_ite@16.7.1:dist/x_ite.js`, `dist/assets/components/` |
| N-CAS-4 | [09](09-castle-engine.md) | non-abstract classes found in X_ITE by `getStaticProperties` | 292 | C | `xite_names.py` | `x_ite@16.7.1:dist/` |
| N-CAS-5 | [09](09-castle-engine.md) | names and `RegisterNodeClasses` calls in the whole tree | 333; 43 | C | inline Python | `castle-engine@48ce617:src/` |
| N-CAS-6 | [09](09-castle-engine.md) | change classes in `TX3DChange`; spec files; generated helper files | 43; 42; 409 | C | inline Python, `ls` | `castle-engine@48ce617:src/scene/x3d/castlefields_misctypes.inc`, `tools/internal/x3d-nodes-to-pascal/` |
| N-CAS-7 | [09](09-castle-engine.md) | mean FLIP, core 11: X_ITE, Babylon add-on glb, Babylon Castle glb, Castle native, Castle all | 0.0457, 0.0485, 0.0491, 0.1149, 0.1146 | C | `core11.py`; FLIP 1.7, Cycles 256 spp, 512 px | `x3d.castle@d70e00c:results/quality/public/results.json` |
| N-CAS-8 | [09](09-castle-engine.md) | mean FLIP, all 15, same five legs | 0.0748, 0.0516, 0.0658, 0.1321, 0.1289 | C | `core11.py` | same |
| N-CAS-9 | [09](09-castle-engine.md) | core scenes where Castle native beats X_ITE; means on the other 7 core scenes | 4 of 11; 0.0406 against 0.0386 | C | `core11.py`, inline Python | same |
| N-CAS-10 | [09](09-castle-engine.md) | share of the all-15 Castle-minus-X_ITE gap in `materials-world` plus `lights-after` | 0.770 | C | inline Python | same |
| N-CAS-11 | [09](09-castle-engine.md) | `p1` Castle FLIP before and after attenuation `0 0 1`; X_ITE | 0.0546, 0.0059; 0.0053 | C | receipt read | `docs/quality-leg.md` section 3 |
| N-CAS-12 | [09](09-castle-engine.md) | `p4` Castle FLIP before and after; X_ITE; share of the gap closed | 0.0446, 0.0237; 0.0085; 58% | C | receipt read, arithmetic | same |
| N-CAS-13 | [09](09-castle-engine.md) | mean FLIP change of the best single Castle switch (SSAA 4x) | -0.0027 | C | inline Python, 15 scenes | `results.json` |
| N-CAS-14 | [09](09-castle-engine.md) | stock writer glbs failing the validator; errors | 24 of 70; 14,379 | C | `Khronos glTF-Validator 2.0.0-dev.3.10`, receipt | `results/scout-70/stock-writer-gltf-validate.json` |
| N-CAS-15 | [09](09-castle-engine.md) | exporter glbs with 0 errors and 0 warnings; INFO notes | 70 of 70; 77 | C | same validator, receipt | `results/phase3/gate70-default/gltf-validate.json` |
| N-CAS-16 | [09](09-castle-engine.md) | exporter census: lights, cameras, textures, vertex colours, lines, points, animation | 41/43, 55/55, 11/17, 26/27, 14/17, 10/11, 0/21 | C | `census_compare.py` receipt | `results/phase3/gate70-default/census.json` |
| N-CAS-17 | [09](09-castle-engine.md) | rig, 21 scenes, phase 3 `self`: mean; median | 7.80; 3.40 | C | X_ITE 16.7.1 vs Babylon 9.32.0, Chromium 153.0.8010.12, SwiftShader, 512 px | `results/phase3/rig-gate-summary.json` |
| N-CAS-18 | [09](09-castle-engine.md) | same rig, phase 2 binary `self`: mean; median | 7.53; 1.05 | C | same | same |
| N-CAS-19 | [09](09-castle-engine.md) | phase 2 receipt means: exporter `rigcam`, add-on glb, stock glb | 7.80, 9.22, 17.62 | C | same rig | `results/rig-exporter/results.json` |
| N-CAS-20 | [09](09-castle-engine.md) | share of the 21-scene sum carried by the four largest scenes | 71% | C | inline Python | `rig-gate-summary.json` |
| N-CAS-21 | [09](09-castle-engine.md) | fixtures passing: phase 3 binary; phase 2 binary | 18 of 18; 4 of 18 | C | `phase3_check.py` receipts | `results/phase3/fixtures.json`, `fixtures-baseline.json` |
| N-CAS-22 | [09](09-castle-engine.md) | gap rows: total; Confirmed; Likely | 20; 19; 1 | C | row count | `docs/castle-gaps.md` |
| N-CAS-23 | [09](09-castle-engine.md) | docker workflow runs, both success | 2 (8 min 32 s; 2 min 50 s) | C | `gh run view`, 2026-11-14 | `hagopjay/x3d.castle` Actions |
| N-CAS-24 | [09](09-castle-engine.md) | `#version` ComposedShader snippet through the validator | valid, 0 errors, 1 INFO | C | `x3d_mcp fork b4efcd3` | drill D-CAS-6 |
| N-CAS-25 | [09](09-castle-engine.md) | mutated glb, inner cone above outer | E=1 W=0 I=1 | C | `Khronos glTF-Validator 2.0.0-dev.3.10` | drill D-CAS-5 |
| N-CAS-26 | [09](09-castle-engine.md) | physical light factor at 3 m, attenuation `1 0 0` against `0 0 1` | 1 against 0.111 (9x) | C | arithmetic on `add_light.glsl` | `castle-engine@48ce617:src/scene/glsl/source/lighting_model_physical/add_light.glsl:123-128` |
| N-CAS-27 | [09](09-castle-engine.md) | specular cap 0.25 against 0.5, rig mean; median | 7.45 against 7.80; 0.58 against 3.40 | C | rig, 3 repeats, Babylon 9.32 only; receipt re-read | `results/phase3/rig-specular-cap025-summary.json` |
| N-CAS-28 | [09](09-castle-engine.md) | field-guide claims checked; split | 279 = 127 + 133 + 13 + 6 | S | carried from a private note | not linkable |
| N-BLE-1 | [10](10-blender-pipeline.md) | `test_*` functions (AST) | 336 in 35 files (274 in 30 bpy files) | **[C]** | Python 3.13.18 `ast` | x3d-blender-io@ab99988:tests/ |
| N-BLE-2 | [10](10-blender-pipeline.md) | tests run without `bpy` | 62, OK | **[C]** | unittest runner | x3d-blender-io@ab99988:.github/scripts/run_tests_in_blender.py |
| N-BLE-3 | [10](10-blender-pipeline.md) | tests run with `bpy` | 335 ran, OK, 10 skipped (glb validator absent) | **[C]** | `bpy 5.3.0` | same |
| N-BLE-4 | [10](10-blender-pipeline.md) | glb-validator tests with the validator present | 10 of 10 pass | **[C]** | `gltf-validator 2.0.0-dev.3.10`, `bpy 5.3.0` | x3d-blender-io@ab99988:tests/test_glb_validator_bpy.py |
| N-BLE-5 | [10](10-blender-pipeline.md) | conformance cases | 195 = 148 CORE + 21 FIDELITY + 26 ROADMAP | **[C]** | `tests/suite/x3d_test_suite.py` on `bpy 5.3.0` | x3d-blender-io@ab99988:tests/suite/README.md |
| N-BLE-6 | [10](10-blender-pipeline.md) | CORE pass, ROADMAP, FIDELITY | 148/148; 21 MISSING + 5 NEW; 19 WARN + 2 PASS | **[C]** | `validate_x3d_export.py`, `bpy 5.3.0` | same |
| N-BLE-7 | [10](10-blender-pipeline.md) | suite exports valid | main 7,010,591 B (4.0), crease 4,911,800 B (4.0), x41 4,617,408 B (4.1), 0 errors | **[C]** | `x3d_mcp fork b4efcd3` | same |
| N-BLE-8 | [10](10-blender-pipeline.md) | concrete nodes in X3DUOM 4.1 | 267 | **[C]** | XML count of `ConcreteNode` | x3d_mcp@b4efcd3:src/validation/schemas/X3dUnifiedObjectModel-4.1.xml |
| N-BLE-9 | [10](10-blender-pipeline.md) | nodes written / read, teardown | 54 / 68 (base 39 / 42), both 43 | **[L]** | teardown method, not reproduced | x3d.docs@f172f67:docs/x3d-blender-io/MASTERCLASS.md |
| N-BLE-10 | [10](10-blender-pipeline.md) | nodes written / read, naive literal scan | 46 / 65, both 38 | **[C]** | rule in section 3 | x3d-blender-io@ab99988:source/ |
| N-BLE-11 | [10](10-blender-pipeline.md) | probe centre patch, X_ITE units (X_ITE / Babylon.js) | 74/74, 204/203, 204/203, 57/56, 78/78 | **[C]** | `X_ITE 16.7.1`, `Babylon.js 9.32.0`, Chrome 153 SwiftShader | x3d-blender-io@ab99988:tools/fidelity_rig/probes.json |
| N-BLE-12 | [10](10-blender-pipeline.md) | probe centre patch, BLENDER units (Babylon.js) | 30, 27, 120, 30, 78 | **[C]** | same | same |
| N-BLE-13 | [10](10-blender-pipeline.md) | p2 `geometry_delta` | 47.07 (centre 204 against 203) | **[C]** | same | same |
| N-BLE-14 | [10](10-blender-pipeline.md) | glb validator on the five probe glbs | 0 errors, 0 warnings, 3 infos each | **[C]** | `Khronos glTF-Validator 2.0.0-dev.3.10` | x3d-blender-io@ab99988:tools/fidelity_rig/validate_glb.mjs |
| N-BLE-15 | [10](10-blender-pipeline.md) | PLY bytes per splat, SH 0 to 3 | 68, 104, 164, 248 | **[C]** | `splat_io.write_ply`, 1,000 splats | x3d-blender-io@ab99988:source/splat_io.py |
| N-BLE-16 | [10](10-blender-pipeline.md) | toy bake: raw max, exposure, final max, bytes | 1.9151, 0.7569, 0.9696, 9,356 B (280 corners) | **[C]** | `bpy 5.3.0` Cycles CPU 16 spp, `x3d_mcp fork b4efcd3` | (scratch script; reproduced by D-BLE-9) |
| N-BLE-17 | [10](10-blender-pipeline.md) | add-on version strings | manifest 2.6.4; `bl_info` 2.6.1; generator meta v2.6.1 | **[C]** | `grep`, export header | x3d-blender-io@ab99988:source/blender_manifest.toml, source/__init__.py |
| N-BLE-18 | [10](10-blender-pipeline.md) | legacy exporter header | `<X3D version="3.0">` for the option labelled "X3D 3.3" | **[C]** | run of an X3D33 export | x3d-blender-io@ab99988:source/export_x3d.py:342 |
| N-BLE-19 | [10](10-blender-pipeline.md) | native splat type values | `['POINTS', 'GAUSSIAN_SPLAT']`; `wm.ply_export` of a splat: 0 vertices, 156 B | **[C]** | `bpy 5.3.0` | probe (D-BLE-7) |
| N-BLE-20 | [10](10-blender-pipeline.md) | npm and PyPI latest on 2026-11-14 | bpy 5.3.0; x3d 4.0.65.8; x_ite 16.7.1; babylonjs 9.36.0 (rig pins 9.32.0) | **[C]** | `pip index versions`, `npm view` | registries |
| N-BLE-21 | [10](10-blender-pipeline.md) | source size | 16,753 lines in `source/*.py`; `import_x3d.py` 7,340; `export_x3d.py` 1,985 | **[C]** | `wc -l` | x3d-blender-io@ab99988:source/ |
| N-BLE-22 | [10](10-blender-pipeline.md) | demo scenes, Blender units to X_ITE units, `geometry_delta` | 40.5 to 25.3 (ontology constellation), 37.3 to 13.7 (materials shelf) | **[L]** | rig on nine scenes, README | x3d-blender-io@ab99988:README.md |
| N-BLE-23 | [10](10-blender-pipeline.md) | baked village file growth | 26 KB to 330 KB gzipped | **[S]** | carried from the bake-stage skill text | skill text, receipt not public |
| N-BLE-24 | [10](10-blender-pipeline.md) | bridges first graded Confirmed that verified lower | 12 of 13 | **[S]** | verifier pass in a private note | carried, not re-checked |
| N-GLT-1 | [11](11-gltf-usd-khronos.md) | validator verdict on a 48-byte glb with no scene | 0 errors, 0 warnings, 0 tris | [C] | `Khronos glTF-Validator 2.0.0-dev.3.10` | scratch run 2026-11-14 (snippet in Section 5.3) |
| N-GLT-2 | [11](11-gltf-usd-khronos.md) | required unknown extension: validator infos / exit code | 1 info, exit 0 | [C] | `Khronos glTF-Validator 2.0.0-dev.3.10` | scratch run 2026-11-14 |
| N-GLT-3 | [11](11-gltf-usd-khronos.md) | ratified extensions in the registry | 27 (24 KHR, 3 EXT) | [C] | Khronos registry sha256 prefix `32868b162d85` | `KhronosGroup/glTF:extensions/README.md`, fetched 2026-11-14 |
| N-GLT-4 | [11](11-gltf-usd-khronos.md) | exhibition flat glb nodes / bytes / tris | 1,721 / 491,832 / 2,064 | [C] | `Khronos glTF-Validator 2.0.0-dev.3.10` plus JSON parse | carried project glb, run 2026-11-14; matches `x3d-blender-io@ab99988:release_notes.md` |
| N-GLT-5 | [11](11-gltf-usd-khronos.md) | exhibition instanced glb nodes / bytes | 10 / 125,224 | [C] | same | same |
| N-GLT-6 | [11](11-gltf-usd-khronos.md) | cathedral flat glb nodes / bytes / tris | 1,224 / 1,097,864 / 27,544 | [C] | same | same |
| N-GLT-7 | [11](11-gltf-usd-khronos.md) | cathedral instanced glb nodes / bytes | 16 / 864,228 | [C] | same | same |
| N-GLT-8 | [11](11-gltf-usd-khronos.md) | cathedral animated glb bytes / animations / channel path | 4,741,136 / 1 / `weights` | [C] | JSON parse 2026-11-14 | carried project glb |
| N-GLT-9 | [11](11-gltf-usd-khronos.md) | repo scenes exporting a glb, all with 0 errors and 0 warnings | 33 of 34 | [L] | `bpy 5.3.0`, `Khronos glTF-Validator 2.0.0-dev.3.10`, carried | `x3d-blender-io@ab99988:tools/fidelity_rig/README.md` |
| N-GLT-10 | [11](11-gltf-usd-khronos.md) | of those 33, empty glbs / points-only glbs | 5 / 2 | [L] | same | `x3d-blender-io@ab99988:release_notes.md` |
| N-GLT-11 | [11](11-gltf-usd-khronos.md) | first animation sample, default versus `frame_start = 0` | 0.041667 s versus 0.0 s | [L] | `bpy 5.3.0` | `x3d-blender-io@ab99988:tools/fidelity_rig/README.md` |
| N-GLT-12 | [11](11-gltf-usd-khronos.md) | `export_apply` True versus False: byte-identical glbs | 34 of 34 scenes | [L] | `bpy 5.3.0` | same |
| N-GLT-13 | [11](11-gltf-usd-khronos.md) | extreme scale: exporter result for Inline scale 1.057e-16 | about 1e8 too small (scale near 1e8 instead of 9.46e15) | [L] | `bpy 5.3.0` | `x3d-blender-io@ab99988:release_notes.md` |
| N-GLT-14 | [11](11-gltf-usd-khronos.md) | `emissiveColor 0.5` as drawn: X_ITE / as-is glb / sRGB glb | 128 / 186 / 127 | [L] | `X_ITE 16.7.1`, `Babylon.js 9.32.0`, Chromium 153, SwiftShader | `x3d-blender-io@ab99988:release_notes.md` |
| N-GLT-15 | [11](11-gltf-usd-khronos.md) | instanced versus flat render in Babylon.js 9.32.0 | 0 of 262,144 pixels differ | [L] | Chromium 153, SwiftShader (carried) | `x3d-blender-io@ab99988:release_notes.md` |
| N-GLT-16 | [11](11-gltf-usd-khronos.md) | ROUTE elements in the animated X3D / in its glb | 2 / 0 | [C] | `grep -c '<ROUTE'` and JSON parse, 2026-11-14 | carried project files |
| N-UNR-1 | [12](12-unreal-tier1.md) | determinant of the axis swap P | -1 | [C] | Python 3, 2026-11-14 | derivation in Section 4.1 |
| N-UNR-2 | [12](12-unreal-tier1.md) | determinant of the alternative `(x, z, -y)` | +1 | [C] | Python 3, 2026-11-14 | Section 4.1 |
| N-UNR-3 | [12](12-unreal-tier1.md) | UE `(120, 340, 90)` cm to X3D | `(1.2, 0.9, 3.4)` m | [C] | converter formula, 2026-11-14 | Section 4.1 |
| N-UNR-4 | [12](12-unreal-tier1.md) | yaw 90 degrees to X3D rotation | `0 -1 0 1.5708` | [C] | converter functions, 2026-11-14 | Section 4.2 |
| N-UNR-5 | [12](12-unreal-tier1.md) | horizontal 58 degrees at 16:9 to `fieldOfView` | 0.6045 rad (34.63 degrees) | [C] | Python 3, 2026-11-14 | Section 4.4 |
| N-UNR-6 | [12](12-unreal-tier1.md) | float32 spacing at 100,000 and 1,000,000 | 0.0078 and 0.0625 | [C] | numpy, 2026-11-14 | Section 4.5 |
| N-UNR-7 | [12](12-unreal-tier1.md) | exhibition output `<Transform>` count | 1,719 | [C] | `grep -o '<Transform '`, 2026-11-14 | converter output (private file) |
| N-UNR-8 | [12](12-unreal-tier1.md) | aurora static output `<Transform>` / USE | 1,216 / 1,208 | [C] | grep, 2026-11-14 | converter output; re-run byte-identical |
| N-UNR-9 | [12](12-unreal-tier1.md) | exhibition glb nodes: flat / instanced | 1,721 / 10 | [C] | JSON parse, `Khronos glTF-Validator 2.0.0-dev.3.10`, 2026-11-14 | `x3d-blender-io@ab99988:release_notes.md` agrees |
| N-UNR-10 | [12](12-unreal-tier1.md) | exhibition glb bytes: flat / instanced | 491,832 / 125,224 | [C] | file size, 2026-11-14 | same |
| N-UNR-11 | [12](12-unreal-tier1.md) | aurora glb nodes: flat / instanced | 1,224 / 16 | [C] | JSON parse, 2026-11-14 | same |
| N-UNR-12 | [12](12-unreal-tier1.md) | aurora glb bytes: flat / instanced | 1,097,864 / 864,228 | [C] | file size, 2026-11-14 | same |
| N-UNR-13 | [12](12-unreal-tier1.md) | triangles: exhibition / aurora static | 2,064 / 27,544 | [C] | `Khronos glTF-Validator 2.0.0-dev.3.10`, 2026-11-14 | carried project glbs |
| N-UNR-14 | [12](12-unreal-tier1.md) | validator verdict on all four static and instanced glbs | 0 errors, 0 warnings | [C] | same | same |
| N-UNR-15 | [12](12-unreal-tier1.md) | instanced render versus flat render in Babylon.js 9.32.0 | 0 of 262,144 pixels differ | [L] | Chromium 153, SwiftShader (carried) | `x3d-blender-io@ab99988:release_notes.md` |
| N-UNR-16 | [12](12-unreal-tier1.md) | probe p1 / p2 centre patch: X_ITE | 74 / 204 | [L] | `X_ITE 16.7.1`, Chromium 153, SwiftShader (carried) | `x3d-blender-io@ab99988:tools/fidelity_rig/README.md` |
| N-UNR-17 | [12](12-unreal-tier1.md) | PSNR of offset-3 pair / noise sigma 5 pair | 38.63 dB / 34.31 dB | [C] | numpy, 2026-11-14 | Section 7.2 |
| N-UNR-18 | [12](12-unreal-tier1.md) | Unreal 5.8 frames rendered in this base | 0 | [C] | none | this chapter |
| N-UNR-19 | [12](12-unreal-tier1.md) | light calibration constant K | 1.01736 (assumed 1.2) | [C] | UE 5.8.4 on RTX PRO 6000 Blackwell SE, driver 580.82.07, 2026-11-14 | notebook 07 step 8 (recorded run, not in a repo) |
| N-UNR-20 | [12](12-unreal-tier1.md) | stilllife vs X_ITE 16.7.0: match / IoU / SSIM | 1.000 / 0.997 / 0.8195 | [C] | same, X_ITE on ANGLE Vulkan, Chromium 159 | notebook 07 step 10 |
| N-UNR-21 | [12](12-unreal-tier1.md) | stilllife luma ratio Unreal / X_ITE and Unreal / Cycles | 0.715 / 0.601 | [C] | same | notebook 07 step 10 |
| N-UNR-22 | [12](12-unreal-tier1.md) | cold start (first shader compile) / warm start | 312.7 s / 15.3 s | [C] | same, 44 shader workers | notebook 07 step 6 |
| N-UNR-23 | [12](12-unreal-tier1.md) | 1080p Lumen still, stilllife / peak VRAM | 10 s / 7.5 GB | [C] | same | notebook 07 step 9 |
| N-UNR-24 | [12](12-unreal-tier1.md) | instances dropped by Interchange from the instanced glb | 1,711 | [C] | same | Interchange log |
| N-UNR-25 | [12](12-unreal-tier1.md) | odyssey White Room: clipped pixels at the calibrated EV / picked offset | 86 % / -14 EV | [C] | same | exposure bracket |
| N-UNR-26 | [12](12-unreal-tier1.md) | Khronos controls: picked offset | +2 EV | [C] | same | exposure bracket |
| N-UNR-27 | [12](12-unreal-tier1.md) | scorecard of the first leg | 40 PASS, 3 WARN, 0 FAIL, 1 SKIP | [C] | same | notebook 07 step 11 |
| N-UNR-28 | [12](12-unreal-tier1.md) | E1 PBR grid vs Cycles, FLIP frame / object | 0.289 / 0.427 | [C] | flip-evaluator LDR, G4 stills, 2026-11-15 | Section 11.2 |
| N-UNR-29 | [12](12-unreal-tier1.md) | E2 Cornell box vs X_ITE, FLIP frame / object | 0.321 / 0.489 | [C] | same | Section 11.2 |
| N-UNR-30 | [12](12-unreal-tier1.md) | E2 Cornell box vs Cycles, FLIP frame / object | 0.285 / 0.433 | [C] | same | Section 11.2 |
| N-UNR-31 | [12](12-unreal-tier1.md) | E3 light ladder vs X_ITE, FLIP frame / object | 0.092 / 0.735 | [C] | same | Section 11.2 |
| N-UNR-32 | [12](12-unreal-tier1.md) | E3 light ladder vs Cycles, FLIP frame / object | 0.091 / 0.724 | [C] | same | Section 11.2 |
| N-UNR-33 | [12](12-unreal-tier1.md) | E3 object share of the frame | 11.7 % | [C] | same | Section 11.2 |
| N-UNR-34 | [12](12-unreal-tier1.md) | FP32 FMA throughput from Python on Vulkan, 60 s | 98.1 TFLOPS (best 98.2) | [C] | wgpu-py 0.33.0 Vulkan, RTX PRO 6000 Blackwell SE, driver 580.82.07, 2026-11-15 | Section 11.5 |
| N-UNR-35 | [12](12-unreal-tier1.md) | power and SM clock peak during it | 541 W, 2,430 MHz | [C] | nvidia-smi, 0.5 s samples, 2026-11-15 | Section 11.5 |
| N-UNR-36 | [12](12-unreal-tier1.md) | Mandelbulb 4K, 4 rays per pixel, render only | 94.0 fps (3.12 G rays/s) | [C] | wgpu-py 0.33.0 Vulkan, RTX PRO 6000 Blackwell SE, 2026-11-15 | Section 11.5 |
| N-UNR-37 | [12](12-unreal-tier1.md) | tier-1 bounds: IoU / repeat / spread margin | 0.95 / 0.02 / 0.05 | [C] | `x3d.lab` PR #32, `tier1_proof_cells.py` | Section 11.4 |
| N-UNR-38 | [12](12-unreal-tier1.md) | Mandelbulb 8K at 64 rays per pixel | 0.67 s | [C] | same | Section 11.5 |
| N-UNR-39 | [12](12-unreal-tier1.md) | all-pairs N-body, 262,144 bodies: interaction rate | 1.48 x 10^12 /s (29.7 TFLOPS at 20 flops each) | [C] | same | Section 11.5 |
| N-UNR-40 | [12](12-unreal-tier1.md) | tier-1 proof run verdicts (PASS / FAIL / SKIP) | 2 / 3 / 1 | [C] | UE 5.8.4 Vulkan SM6+RT, X_ITE 16.7.0 ANGLE Vulkan, Cycles 5.2.3, flip-evaluator LDR object pixels, RTX PRO 6000 Blackwell SE, 2026-11-15 | Section 11.7 |
| N-UNR-41 | [12](12-unreal-tier1.md) | outline IoU vs X_ITE, range over scored views | 0.980-1.000 | [C] | same | Section 11.7 |
| N-UNR-42 | [12](12-unreal-tier1.md) | repeat render object FLIP, every view | 0.000 | [C] | same | Section 11.7 |
| N-UNR-43 | [12](12-unreal-tier1.md) | E1 PBR grid: UE-X / UE-C / X-C object FLIP | 0.221 / 0.260 / 0.298 | [C] | same | Section 11.7 |
| N-UNR-44 | [12](12-unreal-tier1.md) | E2 Cornell box: UE-X / UE-C / X-C object FLIP | 0.516 / 0.419 / 0.458 | [C] | same | Section 11.7 |
| N-UNR-45 | [12](12-unreal-tier1.md) | E3 light ladder: UE-X / UE-C / X-C object FLIP | 0.735 / 0.724 / 0.677 | [C] | same | Section 11.7 |
| N-UNR-46 | [12](12-unreal-tier1.md) | odyssey DroneCam: UE-X / UE-C / X-C object FLIP | 0.667 / 0.699 / 0.527 | [C] | same | Section 11.7 |
| N-UNR-47 | [12](12-unreal-tier1.md) | peak VRAM across the proof run's stills | 12.2 GB | [C] | same | Section 11.7 |
| N-PHY-1 | [13](13-physics.md) | Explicit Euler pendulum energy growth, h = 0.01, 100 s | +10.89 (final dE/E0) | [C] | numpy 2.5.3 | D-PHY-1 |
| N-PHY-2 | [13](13-physics.md) | Symplectic Euler pendulum, same run | +0.0002 final, 0.0150 max | [C] | numpy 2.5.3 | D-PHY-1 |
| N-PHY-3 | [13](13-physics.md) | Discrete free fall against continuum gap, 1 s at 1/240 | -0.020437 m (`g h t/2` = 0.020438) | [C] | numpy 2.5.3 | D-PHY-2 |
| N-PHY-4 | [13](13-physics.md) | PhysX 5.12 free fall error against discrete solution | 1.5e-6 m (limit 1e-4) | [L] | read, not run: `x3d.loom@162ab18:x3d.physics/physx-bridge/evidence/p1-analytic.json` | same file |
| N-PHY-5 | [13](13-physics.md) | Bead pre-projection violation, 1 to 100 substeps | 7.31e-3, 3.19e-4, 2.03e-5, 8.16e-7 | [C] | numpy 2.5.3 | D-PHY-3 |
| N-PHY-6 | [13](13-physics.md) | Kinetic energy, fixed, buggy and no collisions | 0.500000 each | [C] | numpy 2.5.3 | D-PHY-4 |
| N-PHY-7 | [13](13-physics.md) | Order of symplectic Euler, T = 1 and T = 2 pi | 1.00 and 2.00 | [C] | numpy 2.5.3 | D-PHY-5 |
| N-PHY-8 | [13](13-physics.md) | Wave grid max amplitude at c dt/dx 0.7071 and 0.72, 400 steps | 4.65e-3 and 1.18e59 | [C] | numpy 2.5.3 | D-PHY-6 |
| N-PHY-9 | [13](13-physics.md) | Variable-step pendulum, two seeds, jitter 0.5 | final angle 0.1592 and 0.4356 | [C] | numpy 2.5.3 | D-PHY-7 |
| N-PHY-10 | [13](13-physics.md) | Physics witness on the 2 PhysX records | pass | [C] | `x3d.loom@162ab18` `kit/loom physics` | D-PHY-8 |
| N-PHY-11 | [13](13-physics.md) | Negative controls on the real records | 14 of 14 caught | [C] | `x3d.loom@162ab18` `physx_controls.py` | D-PHY-8 |
| N-PHY-12 | [13](13-physics.md) | Kit self-test controls | 82, normal and `-O` | [C] | `x3d.loom@162ab18` `kit/tests/test_gates.py` | D-PHY-8 |
| N-PHY-13 | [13](13-physics.md) | `PHYS_*` codes in the witness | 18 listed in the docstring | [C] | `x3d.loom@162ab18:kit/loomkit/physics.py` | section 3.5 |
| N-PHY-14 | [13](13-physics.md) | MuJoCo importer threat checks | 16 defended and 3 gaps (19) | [C] | read via python json count, `x3d.loom@162ab18` | D-PHY-9 |
| N-PHY-15 | [13](13-physics.md) | Ten Minute Physics scenes built | 17 in 6 batches | [C] | `ls`, `x3d.demo@d10b457` | D-PHY-10 |
| N-PHY-16 | [13](13-physics.md) | RigidBody or Script elements in those scenes | 0 files | [C] | `grep -lE`, `x3d.demo@d10b457` | D-PHY-10 |
| N-PHY-17 | [13](13-physics.md) | Replay of the Chromium run: steps and differing hashes | 1918 steps, 0 differing, 4 hosts | [L] | read, `x3d.loom@162ab18:x3d.physics/runs/physx-grand-cascade-chromium.physics.json` | PLAYBOOK pattern 3 |
| N-PHY-18 | [13](13-physics.md) | CCD tunnelling, 5 m/s marble, 5 mm wall | 0 of 40 on, 10 of 40 off | [L] | read, `physx-bridge/tests/analytic.test.ts` evidence | PLAYBOOK pattern 7 |
| N-PHY-19 | [13](13-physics.md) | Independent review of v1 to v4 | 125 claims, 55 findings, 25 survived, 0 false alarms | [L] | read, `ten-minute-physics/ERRATA-v1-v4.md` | law 44 row |
| N-PHY-20 | [13](13-physics.md) | Default contact friction in X_ITE (two bodies at 0.5, multiplied) | 0.25 | [C] | x3d.loom PR #56, X_ITE 16.6.0, Chromium 153, SwiftShader | section 9.3 |
| N-PHY-21 | [13](13-physics.md) | Box thrown at 4 m/s, slide distance in X_ITE and in the bridge | 3.06 to 3.27 m and 1.63 m | [C] | same rig | section 9.3 |
| N-PHY-22 | [13](13-physics.md) | Ball at 4 m/s against a fixed wall, bounce 1, minBounceSpeed 0, speed after | 3.2 to 4 m/s in X_ITE; 3.99 in the bridge | [C] | same rig | section 9.3 |
| N-PHY-23 | [13](13-physics.md) | Body rest height with a sphere offset 1 m below the origin | 0.5 m in X_ITE, 1.5 m in the bridge | [C] | same rig | section 9.3 |
| N-PHY-24 | [13](13-physics.md) | Files using RigidBodyCollection, RigidBody, CollidableShape | 31, 31, 27 | [L] | `grep -rl` by the batch author over the Loom repos, not re-run here | section 9 |
| N-PHY-25 | [13](13-physics.md) | Hinge limits plus and minus 0.5 rad, final ball position, bridge | x 1.755, y 4.034, angle -0.50 | [C] | batch 42 `SingleAxisHingeJoint` probe; X_ITE 16.6.0, Chromium 153, SwiftShader | section 9.5 |
| N-PHY-26 | [13](13-physics.md) | Same swing in X_ITE, unsigned angle | 3.45 (limits ignored) | [C] | same rig | section 9.5 |
| N-PHY-27 | [13](13-physics.md) | Motor torque 1 N m on 1 kg, 0.3 m sphere, angular acceleration | 25.1 rad/s per second measured; 27.8 theory | [C] | same rig, wall-clock wait | section 9.5 |
| N-PHY-28 | [13](13-physics.md) | DoubleAxisHingeJoint motor 1 rad/s for 1.5 s, hinge1Angle band in the test | 1.1 to 1.9 rad | [C] | same rig | section 9.5 |
| N-MET-1 | [14](14-methods.md) | chapters 01 to 13 | 13 | C | `check_learn.py` at this commit | `x3d.docs@f172f67:docs/learn/` |
| N-MET-2 | [14](14-methods.md) | heuristics before chapter 14 | 161 | C | `build_learn.py` at this commit | `docs/learn/D-heuristics-ledger.md` |
| N-MET-3 | [14](14-methods.md) | drills before chapter 14 | 97 | C | `build_learn.py` at this commit | `docs/learn/E-drills.md` |
| N-MET-4 | [14](14-methods.md) | drills with a recorded run | 89 | C | `build_learn.py` at this commit | `docs/learn/E-drills.md` |
| N-MET-5 | [14](14-methods.md) | numbers registered | 277 | C | `build_learn.py` at this commit | `docs/learn/C-numbers-ledger.md` |
| N-MET-6 | [14](14-methods.md) | numbers graded C | 235 | C | `learn_lib.py` count | `docs/learn/C-numbers-ledger.md` |
| N-MET-7 | [14](14-methods.md) | numbers graded L | 38 | C | `learn_lib.py` count | `docs/learn/C-numbers-ledger.md` |
| N-MET-8 | [14](14-methods.md) | numbers graded S | 4 | C | `learn_lib.py` count | `docs/learn/C-numbers-ledger.md` |
| N-MET-9 | [14](14-methods.md) | heuristics graded C | 124 | C | `learn_lib.py` count | `docs/learn/D-heuristics-ledger.md` |
| N-MET-10 | [14](14-methods.md) | heuristics graded L | 30 | C | `learn_lib.py` count | `docs/learn/D-heuristics-ledger.md` |
| N-MET-11 | [14](14-methods.md) | heuristics graded S | 7 | C | `learn_lib.py` count | `docs/learn/D-heuristics-ledger.md` |
| N-MET-12 | [14](14-methods.md) | methods in this chapter | 7 | C | read | this file |
| N-YJS-1 | [15](15-yjs-collaboration.md) | unit and fuzz tests passing | 22 of 22 | [C] | Node v22.23.4, Yjs 13.6.33 | `x3d.loom@0689f1a:x3d.yjs/test` |
| N-YJS-2 | [15](15-yjs-collaboration.md) | fuzz seeds converged | 200 of 200 | [C] | same, 3 peers x 300 ops | `x3d.yjs/receipts/bench.md` |
| N-YJS-3 | [15](15-yjs-collaboration.md) | different pixels after add, move, remove | 0 of 145,116 each | [C] | X_ITE 16.6.0, Chromium 153, SwiftShader | `x3d.yjs/receipts/e2e-xite.json` |
| N-YJS-4 | [15](15-yjs-collaboration.md) | different pixels, offline control | 16,633 | [C] | same | same |
| N-YJS-5 | [15](15-yjs-collaboration.md) | apply latency, median, X_ITE | 0.30 ms | [C] | same, in-process link | same |
| N-YJS-6 | [15](15-yjs-collaboration.md) | apply latency, median, three.js bridge | 0.20 ms | [C] | three r187, SwiftShader | `x3d.yjs/receipts/e2e-threejs-bridge.json` |
| N-YJS-7 | [15](15-yjs-collaboration.md) | incremental vs fresh picture, bridge | 0 of 153,600 pixels | [C] | same | same |
| N-YJS-8 | [15](15-yjs-collaboration.md) | bytes per field update | 44 to 47 | [C] | Node v22.23.4, Yjs 13.6.33 | `x3d.yjs/receipts/bench.md` |
| N-YJS-9 | [15](15-yjs-collaboration.md) | state size per node | 155 to 168 bytes | [C] | same | same |
| N-YJS-10 | [15](15-yjs-collaboration.md) | local setField at 50,000 nodes with observer | 147,518 per second | [C] | Intel Xeon 2.10 GHz x4 | same |
| N-YJS-11 | [15](15-yjs-collaboration.md) | structural add+remove pairs at 500 / 5,000 / 50,000 nodes | 280 / 24 / 2 per second | [C] | same | same |
| N-YJS-12 | [15](15-yjs-collaboration.md) | loadXML at 50,000 nodes | 535.5 ms | [C] | same | same |
| N-YJS-13 | [15](15-yjs-collaboration.md) | remote apply at 500 nodes | 149,687 per second | [C] | same | same |
| N-YJS-14 | [15](15-yjs-collaboration.md) | orphan nodes over 200 fuzz seeds | 5,127 | [C] | same | same |
| N-YJS-15 | [15](15-yjs-collaboration.md) | reported conflicts over 200 seeds: def-clash, sfnode-slot, duplicate | 206, 31, 15 | [C] | same | same |
| N-PTR-1 | [18](18-three-pathtracer.md) | e2 Cornell, path tracer 6 bounces vs X_ITE, object FLIP | 0.265 | [C] | Chromium 153 SwiftShader; X_ITE 16.6.0; 96 spp | `x3d.loom@5f59349:x3d.threejs/pathtracer/results/results.json` |
| N-PTR-2 | [18](18-three-pathtracer.md) | e2 Cornell, path tracer 1 bounce vs X_ITE | 0.142 | [C] | same | same |
| N-PTR-3 | [18](18-three-pathtracer.md) | e2 Cornell, path tracer vs Cycles | 0.380 | [C] | same; bpy 5.3.0 CPU 256 spp OIDN | same |
| N-PTR-4 | [18](18-three-pathtracer.md) | e2 Cornell, Cycles vs X_ITE (spread) | 0.468 | [C] | same | same |
| N-PTR-5 | [18](18-three-pathtracer.md) | e1 PBR grid, path tracer vs Cycles | 0.743 | [C] | same | same |
| N-PTR-6 | [18](18-three-pathtracer.md) | e1 pass bound (X-C + 0.05) | 0.349 | [C] | same | same |
| N-PTR-7 | [18](18-three-pathtracer.md) | e3 light ladder, path tracer vs Cycles; bound | 0.751; 0.755 | [C] | same | same |
| N-PTR-8 | [18](18-three-pathtracer.md) | e2 bridge raster vs X_ITE | 0.595 | [C] | same | same |
| N-PTR-9 | [18](18-three-pathtracer.md) | Noise floor: two 96 spp Cornell runs against each other | 0.055 | [C] | same | `results/runs/` notes; README |
| N-PTR-10 | [18](18-three-pathtracer.md) | Cycles vertical angle drawn at 4:3 from the add-on's horizontal 1.2695 rad | 1.0092 rad (asked 0.7854) | [C] | numpy 2.5.4 (D-PTR-1) | `cycles_job.py` docstring |
| N-PTR-11 | [18](18-three-pathtracer.md) | First (wrong) e1 spread X-C and bound before the camera match | 0.594; 0.644 | [C] | same rig, unmatched Cycles | commit history of `x3d.loom` PR #76 |
| N-PTR-12 | [18](18-three-pathtracer.md) | Path-tracer time per 96-sample scene on SwiftShader | 59 to 111 s trace, 100 to 190 s with shader build | [C] | Chromium 153 SwiftShader | `results/runs/f6/*.json` |
| N-PTR-13 | [18](18-three-pathtracer.md) | Object share of e3 light ladder | 16.4 percent of pixels | [C] | same | `results/results.json` |
| N-PTR-14 | [18](18-three-pathtracer.md) | e3 frame FLIP with a lit sky sphere vs without | 0.93 vs 0.09 | [C] | same | first and final run files |
| N-PTR-15 | [18](18-three-pathtracer.md) | Demo 25 headless check: samples reached; X_ITE root nodes | 181; 12 | [C] | Chromium 153 SwiftShader | `x3d.demo` PR 29 description |
<!-- END GENERATED -->
