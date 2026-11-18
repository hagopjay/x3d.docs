# Accountability review, 18 Nov 2026: what was verified and what changed

An outside frontier model reviewed the x3d.* framework against the tether, "X3D is the 3D format an AI can be held
accountable to", and ranked ten defects. Its verdict: X3D is a credible contract; this framework did not yet enforce
it consistently (failed checks that return success, evidence admission, unmeasured foldback benefit). Every defect
was re-checked before any fix. Grades are ours (C Confirmed, L Likely, S Suspected).

Pins: x3d.loom 7b620c2, x3d.demo 66953a4, x3d_mcp fa5dccf (lxml 6.1.3, libxml2 2.14.6), x3d-blender-io 044bea3,
headless Chromium 157.0.8103.78 via Playwright 1.63.0.

| # | Defect | Our grade | Fix (where) | Proof after the fix |
|---:|---|:-:|---|---|
| 1 | Loom `traps` prints fail, exits 0 | C | exit follows records: fail 1, error 2 (x3d.loom `kit/loomkit/cli.py`) | reviewer's bad-colour probe exits 1; record written first |
| 2 | Blender checker accepts `<Banana>`; compressed exports unchecked; semantic errors only logged | C (source) | blenderizer thread, x3d-blender-io PR #46 | that thread: unknown elements error, gzip validated, semantic errors fail |
| 3 | Declared `pass/C` satisfies a measured witness | C | typed origins executed / declared / reviewed; `record` refuses C (x3d.loom) | 6 new negative controls |
| 4 | Profile wants 11 trap rules, tool emits 15 | C, wider: 15 of 20 profiles stale, 24 requirements, at loom ba8ea1a (first count said 17; corrected after the second review) | profiles bind rule ids (`rules_include`); kit CI workflow | every shipped profile accepts a fresh witness |
| 5 | D3 `validate.py` exits 0 on invalid or empty input; hard-coded commit | C | shared `tools/assurance/validate_scenes.py` (x3d.demo) | Banana exit 1, empty exit 2; commit derived |
| 6 | Heritage shows C for an S interpretation; Background cardinality error | C | `heritage-geo/v3`: grades from 7 atomic parts, weakest part wins | `check_grades.py` pass; XSD + semantic 2/2 clean |
| 7 | 3D Tiles converter loses nested URI base; silently drops ADD, extra contents, frames | C | `tools/tiles3d` v2 resolves per tileset and refuses losses unless `--allow-lossy` | 16 controls; 177/177 files identical to v1 on the shipped tileset |
| 8 | 4.0 XSD rejects the normative `transferFunction` | C (bundled and live web3d.org copy) | fixture pack in x3d_mcp; upstream report **held** | XSD and semantic verdicts pinned separately |
| 9 | WebGL failure leaves blank panels or an endless boot screen | C (Giza v6, D3 v1 and v2) | `docs/lib/gfx-guard.js`, `giza-osiris-hall/v6.1`; D3 handed to its thread | WebGL off: reason, still, fallbacks, 33-row ledger |
| 10 | Foldback tests an empty repo with the author's own smoke | C (source) | `foldback --target --base --consumer`, `x3d-static/v2` | regressing patch caught; unknown base is an error |

**New findings while verifying.** D3 v2 `scenes/spacetime.x3d` uses ClipPlane (Rendering 5) outside the Immersive
profile with no component line (x3d_mcp semantic error; sent to the D3 thread). A kit test pinned the exit-0 bug as
correct behaviour. A same-second `.pyc` masked a regressing patch in the new foldback mode until the clone was cleaned
between runs.

**Still open (honest).** Unsigned records can be hand-edited; the review's held-out learning experiment (fixed model,
equal budget, with and without Loom knowledge) is not run; real-GPU timing is unverified; "X3D is uniquely
accountable" stays unsupported as an exclusive claim. The stronger, defensible claim is declarative interaction plus
domain components plus inspectable scene structure, with checks that now fail when they should.

Full lesson table: x3d.loom `LEARNINGS-accountability-review.md`.

## Second review (18 Nov 2026, evening)

A second pass by the same external reviewer found that "all ten closed" overstated the published workflow. Each item
below was reproduced on the shipped code before it was fixed, and each fix has a control that fails on the old code.

| # | Finding | Grade | Reproduced (instrument) | Fix | Where |
|---|---|---|---|---|---|
| 1 | Target fold-back hashed the patch file, then re-read it after the baseline run (hash A, apply B) | C | swapped file: original hash recorded, outcome `regressed` (loomkit `test_gates.py`) | patch frozen once into a private read-only copy; only that copy is hashed and applied | x3d.loom `kit/loomkit/foldback.py` |
| 1b | A patch that edits its own test reads as `held` | C | patch breaks `lib.py` and rewrites `check.py`: `held` | `scorer changed` outcome; profile `x3d-static/v3` requires `scorer_unchanged` | x3d.loom |
| 4 | 3D Tiles content placed at the bounding-volume centre | C | 9.996 m on the reviewer's off-centre sphere (`test_tiles3d.py` against v2 as shipped) | content at the tile frame origin: 0.0000 m; ECEF-baked content refused | x3d.demo `tools/tiles3d` v2.1 |
| 6 | Loom README taught the empty-repo fold-back and profile v1 | C | README lines 48, 60, 63 | target-bound example; v3 for publishing; v1 marked legacy | x3d.loom README |
| 7 | Giza VI.1 no-graphics ledger: 132 undefined cells | C | 33 rows, 132 undefined, 0 of 23 links (`check_giza_ledger.cjs`, Playwright 1.63.0) | Giza v6.2 renders named fields as text; 0 mismatches | x3d.demo `giza-osiris-hall/v6.2` |
| 8 | Malformed XML killed the validator before its receipt | C | `XMLSyntaxError`, no receipt | per-file errors recorded, semantic `not_run`, receipt always written, exit 1 | x3d.demo `tools/assurance/validate_scenes.py` |
| 10 | Guard's slow note appended only its STYLE element | C | no alert after timeout (`check_gfx_guard.cjs`) | `gfx-guard-v2.js`; also drops `javascript:` links (new finding, v1 let one through) | x3d.demo `docs/lib` |
| — | Profile `origins` as a string matched by substring | C | `"declared" in "undeclared"` | `load_profile` requires a list of known origins | x3d.loom |

Items 2, 3 and 5 (Blender export overwrite, importer intent loss, field-aware validation) are in x3d-blender-io #48.
The import path now records what it drops; it does not yet rebuild interaction, so a round trip still loses
behaviour, now on the record.

Lesson: a hash binds evidence only when the hashed bytes are the bytes used, and a check that counts rows is not a
check of what the rows say.

## Third review (18 Nov 2026, late)

The third pass confirmed the round-2 repairs on their own cases, then found failures on ordinary inputs:
"unchanged", "atomic" and "lossless" were claimed about sets nobody had written down. Each item was reproduced
with the reviewer's own probe scripts before the fix and re-run after.

| # | Finding | Grade | Fix | Where |
|---|---|---|---|---|
| 1, 3, 4, 5 | Splat sidecar aliasing; failed export changes a referenced GLB; strict import changes sensors (disabled, fan-out, offset box); same-position tour stops collapse | C | content-digest sidecar names; staged publish with rollback; exact-edge and field accounting; pose-matched stops | x3d-blender-io #49 |
| 2 | `scorer_unchanged` was a path-name guess: edited `expected.json`, or `check.py` under `sh -c`, earned true | C | `--scorer` declares the oracle closure (hashed at base); undeclared = unknown, refused by x3d-static/v3; a declared scorer edit is re-scored with the base scorer | x3d.loom |
| 6 | Converter wrote `mesh&a.glb` raw (bad XML) and dropped `?query` (HTTP 200 became 403) | C | URI components kept; XML and MFString escaping; output parsed before success | x3d.demo tools/tiles3d v2.2 |
| 7 | Antimeridian region: GeoLOD centre at lon 0, 12,756,294 m off | C | east < west unwrapped before the midpoint | same |
| 8 | One page-wide ready flag: second pane lost its failure panel | C | splat v3 page (x3d.demo #103); shared `gfx-guard-v3.js` `pane()` API | x3d.demo |
| 9 | Receipt written, then manifest collided: partial successor | C | manifest versioned with its receipt; both staged and renamed together | x3d.loom |
| 10 | Failed optional witness written into `not_run`, against the shipped schema | C | manifest v2 with a `failed` list, validated before writing; profile bytes hashed | x3d.loom |
| — | Space/Unicode git paths crashed foldback; mode-000 scene lost the validator receipt; polar origin crashed the converter; encoded local paths refused; stale conversion report | C | git's own path parser; per-file read boundary; pole branch; decode for filesystem only; report every run | x3d.loom, x3d.demo |

Lesson: "unchanged" can only be claimed about a declared set, and "atomic" about every file a publication touches.
Anything undeclared is unknown, and unknown must not pass.

## Fourth review (18 Nov 2026, night)

The fourth pass confirmed the round-3 repairs and asked for automatic promotion to be blocked until identity and
numerical checks were repaired. Every item was reproduced on main with the reviewer's probes (Python 3.13.18, Node
22, linkedom 0.18.12; no browser or GPU), fixed, and kept as a control: x3d.loom `review4_controls`, 20 new, 135
caught in all, plain and `-O`; x3d.demo tiles3d suite 33 of 33.

| # | Finding | Grade | Fix | Where |
|---|---|---|---|---|
| 1 | Profile read twice: the attested hash was not of the evaluated bytes | C | one read, parsed and hashed | x3d.loom #128 |
| 2, 3 | Symlinked scorer and renamed scorer data escaped the base hash | C | tree inventory against the globs, symlink text and resolved hash, before and after the patch | same |
| 4 | Optional pass from another candidate shown as pass | C | `stale` status | same |
| 5, 6 | Comparator typo read as `at least`; empty controls passed | C | closed rule set; `PHYS_NO_CONTROLS` | same |
| 7, 9 | Runs keyed by basename; waiver cap per run, profile says total | C | relative-path keys, distinct ids, total cap | same |
| 8 | Signature + IEND passed as a decodable PNG | C | stdlib bounded decoder | same |
| 10 | Forced receipt inside evidence inventoried itself | C | refused (`RECEIPT_INSIDE_EVIDENCE`) | same |
| — | NaN limit, arbitrary `--prev`, forced-pair rollback, stdlib schema fallback, glob language per Python version, absent coverage key, cached-bytecode replay | C | strict JSON; predecessor must verify; originals copied aside and restored; typed profile parse; one glob language; key required; replay in a fresh clone | same |
| — | Committed-limit metric identity (a limit matched by value, not by metric) | L | documented as open | same |
| — | Blender timers, hover and anisotropic proximity | C | blenderizer lane | x3d-blender-io #50 |
| G1 | Parent scale left out of geometricError (range 814.8 m, expected 1629.6 m) | C | largest axis scale applied | x3d.demo #106, tiles3d v2.3 |
| G2 | `viewerRequestVolume` dropped silently | C | refused; recorded under `--allow-lossy` | same |
| — | Splat page: idle pane counted, so the slow note appeared; viewer library had no deadline | C | started panes only; shared loader with deadline and Retry | blender-splat v4 |

Lesson: every set Loom vouches for (the profile, the scorer, the runs, the visible witnesses) must be read once, keyed
by full identity, and closed. An open set or a second read is where a wrong pass gets in. Real-GPU timing remains
open, and the Web3D report remains unsent.
