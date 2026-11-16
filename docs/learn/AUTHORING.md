# AUTHORING: how this knowledge base is written, checked and grown

This file is the contract for every chapter under `docs/learn/`. A chapter that breaks it fails `tools-shared/check_learn.py`.
It is also the *method*: the way a claim enters this base is the same way a claim enters an X3D pipeline we trust.

**Thesis the whole base serves:** *X3D is the 3D format an AI can be held accountable to.* Machine-readable rules (XSD, DTD,
X3DUOM, ontology) let software name exactly what is wrong; a second renderer shows what is visible; a ledger travels with the file.
Everything here either teaches that machinery, measures it, or marks where it stops.

**Audience:** people who already believe in X3D and want to learn the framework deeply: the laws, the traps, the instruments, the
numbers and the honest limits. No marketing. Assume the reader will re-run what you wrote.

---

## 1. Grades (every claim carries one)

| grade | token | meaning | what is required |
|---|---|---|---|
| Confirmed | **[C]** | we measured it, or read it in the exact code or file | the *instrument* is named (validator commit, renderer version, hardware, tool version) |
| Likely | **[L]** | read in a source we trust, or reasoned from [C] facts | the *source* is named; say what would confirm it |
| Suspected | **[S]** | a guess, a design expectation, or a number from a source we did not re-check | say it is a guess; never use it as a premise for a [C] |

Rules: never upgrade a grade in a later chapter without a re-measurement; a number copied from another document is [L] at best until you
re-derive it; "x leads the field" style claims are not gradable and are not written.

## 2. Name the instrument behind every number

A number without an instrument is a rumour. Canonical instrument strings (use these spellings; Appendix A registers them):

| instrument | how to write it | what it checks |
|---|---|---|
| X3D MCP validator, our fork | `x3d_mcp fork <sha7>` e.g. `x3d_mcp fork b4efcd3` | XSD plus semantic rules, exact-fix hints |
| X3D MCP validator, upstream | `x3d_mcp upstream 74da0ec` | upstream baseline |
| X3D Unified Object Model / XSD | `X3DUOM 4.1`, `X3D XSD 4.0` (with sha256 prefix when you used a file) | vocabulary, field types |
| Reference renderer | `X_ITE <version>` plus the rig: `Chromium <ver>, SwiftShader` or the named GPU | what a browser draws |
| glTF validator | `Khronos glTF-Validator <ver>` | glb structure only, not looks |
| Blender | `bpy <ver>` | the add-on's test suite and rig |
| Repo state | `<repo>@<sha7>` | which checkout was read or run |
| Hardware | the exact GPU and driver, or `software GL` | any timing |

If you did not run it, say `read, not run`. If a number comes from a recorded run in a repo, cite the receipt path.

## 3. Chapter template (strict; the linter checks the headings)

```
# NN. Title                                   (NN = two digits; file is NN-slug.md)

> **Say it:** one sentence a reader can repeat. **[grade]**

| field | value |
|---|---|
| chapter code | `XXX` (the id prefix used below) |
| prerequisites | chapter numbers or "none" |
| after this you can | 3 to 5 concrete abilities |
| sources read | repo@sha:path list (short) |
| instruments used | the strings from section 2 |

## 1. The map
   One ASCII diagram (fenced ```text, at most 96 columns) and one table that orients the reader. Say what is in scope and what is not.

## 2..N. Core sections
   Dense tables, ranked lists, worked examples with real snippets (X3D XML, commands, field names). Every numeric row names its instrument.
   Prefer a table to a paragraph. Prefer a worked example to an explanation. Quote file paths and commands exactly so they can be re-run.

## Heuristics
   | ID | Rule (imperative, at most 30 words) | Grade | Evidence | Instrument |
   IDs are `H-<CODE>-<n>`. A rule is something a practitioner can apply at a decision point and be wrong about; not a fact.

## Drills
   ### D-<CODE>-<n> Title
   - **Level:** L1 (look it up) | L2 (run a tool and compare) | L3 (break it, fix it, extend it)
   - **Task:** what to do
   - **Verify:** the exact command, file or tool that checks the answer
   - **Answer:** the answer key, with numbers
   - **Checked:** `<date> <instrument>` if you ran it, or `not run`
   At least five drills; at least two must be L2 or L3; at least two must have `Checked` run, not "not run".

## Honest limits
   What this chapter does NOT show, what was read and not run, where sources disagree, which numbers are stale. A bullet list with grades.

## Numbers register
   | ID | Quantity | Value | Grade | Instrument | Source |
   IDs are `N-<CODE>-<n>`. One row per number a reader might quote (at least 12). The Source column is `repo@sha:path` or a recorded-run path.
   The registers of all chapters are merged into Appendix C by `tools-shared/build_learn.py`.

## Sources and provenance
   Repos, commits, dates read. Mention private-source gaps without linking them (see section 5).
```

Depth ladder: put a "Read next" line at the end of the map section pointing to one chapter that goes deeper and one that goes wider.

## 4. Style

* Density beats length. Chapters run 20 to 60 KB; a table row should carry a fact, a number and an instrument.
* Diagrams are fenced `text` blocks (box-drawing or plain ASCII, at most 96 columns, no tabs) so they render on GitHub and on the Pages site.
  Every chapter has at least two. Prefer: pipelines, ladders, matrices, annotated node trees.
* Code and X3D are fenced with a language tag (`xml`, `bash`, `python`, `json`). Every snippet must be copyable.
* Say what you did not check. A short honest limit is worth more than a long hedge.
* One voice: plain sentences, no exclamation marks, no marketing words, no emoji. Ranked lists over adjectives.
* Do not write "leads", "best", "first ever", "revolutionary". Write the measurement.
* Name the patch AND the rig with every render claim (X_ITE version plus Chromium/SwiftShader or the GPU).
* When two sources disagree, record both, say which one the code supports, and grade the loser [S].
* Cross-link chapters with relative links (`[the tether](01-the-tether.md)`); link to code with `repo@sha:path` text, plus a GitHub URL only
  for PUBLIC repos.

## 5. Public-repo hygiene (this repo is PUBLIC; the linter and the leak sweep enforce this)

Never write, in any file: links to private documents or artifacts, cloud project ids or bucket names, API keys or key fragments, email
addresses, local machine paths (a person's home or drive paths; cite `repo@sha:path` instead), account aliases, spend or credit figures,
session or thread ids, or anything about unpublished plates, unpublished lab material or unpublished data of any project whose owner has not
published it. Do not quote the owner's chat words; write the *rule* instead. `tools-shared/check_learn.py` carries the exact patterns.

Findings held for an upstream report (to the Web3D Consortium, X_ITE, Castle or others) and not yet sent are NOT published here unless the same
finding already stands in a file of a PUBLIC repository (then cite that file). When unsure, leave it out and list it in your hand-off note.

Private memory notes and private artifacts are *leads*, not sources: re-derive every figure from a public file, a repo checkout, a recorded
run, or run the tool again. If you cannot, grade it [S] and say "carried from a private note, not re-checked".

## 6. How the base grows (the augmentation loop)

1. **Observe**: a new measurement, a failure, a PR or a drill that went wrong.
2. **Write the rule**: add a row to the owning chapter's Heuristics table with the next free ID and a grade no higher than the evidence.
3. **Name the instrument** and add the number to that chapter's Numbers register.
4. **Add or fix a drill** that would have caught it; run it; fill `Checked`.
5. **Rebuild**: `python3 docs/tools-shared/build_learn.py` regenerates the ledgers (Appendix C numbers, D heuristics, E drills) and the HTML;
   `python3 docs/tools-shared/check_learn.py` lints structure, grades and leaks.
6. **Log it** in `docs/learn/CHANGELOG.md` (date, chapter, what changed, which instrument). Retire a heuristic by striking it, never by deleting its ID.
7. **Demote on contradiction**: a later measurement that disagrees with a [C] row downgrades the row and records both numbers.

New demos or measurements land as new versions; an earlier measurement is never overwritten, it is superseded by a dated row.

## 7. Claim ledger (optional per chapter; from chapter 23 on, a chapter ships with one)

A Numbers register says *what* a chapter claims. A ledger says *where it was read*: one JSON line per value with the quote that holds it.
`tools-shared/check_claims.py` then does in code what a reviewer would do by hand, with no model and no network unless you ask for it:

| step | question | how |
|---|---|---|
| FIND | is the quote in the cited source, pinned at the sha? | token run match: lowercase words, punctuation and spacing ignored, a number keeps its sign and decimal point |
| COMPARE | is the value inside the quote? | numbers as numbers (4.200 may be 4.2 or 4200; 1.234,5 and 1,234.5 both read 1234.5), lists in order, text by words |
| LOCATE | where is it? | line and character span; Appendix G links the line at the pinned sha |

File: `docs/learn/claims/<chapter file stem>.jsonl` (for example `22-typed-judgments-jev.jsonl`). One JSON object per line; blank lines and lines
starting with `#` are skipped; an optional first object `{"_meta": {...}}` carries `schema` (`claims/0.1`), `coverage_floor` and a note.
A chapter without a ledger file is unchanged: nothing below applies to it.

| field | required | meaning |
|---|---|---|
| `id` | yes | an existing row of the chapter (`N-<CODE>-n`, `H-<CODE>-n`) or `Q-<CODE>-n` for a claim in prose that has no row (its number must occur in the chapter text) |
| `value` | yes | a number, a list of numbers (an SFVec3f or colour), a string, or null |
| `quote` | yes, except private | at most 40 words copied from the source; it must occur as an unbroken run of words |
| `source` | yes | `repo@sha:path` (a repo on the public list in `claims_lib.PUBLIC_REPOS`), `self:docs/learn/NN-slug.md`, `external:<label>` or `private:<name>` |
| `grade` | no | `C`, `L` or `S`; if present it must equal the register's grade for `id` |
| `line` | no | a hint, required when the quote occurs more than once in the source (a repeated quote with no hint is `check`) |
| `in` | no | which register cell holds the value: `value` (default), `quantity`, `instrument` or `source` |
| `transform` | no | a declared conversion from the quote's number to the value, `{"scale": 100, "round": 1}`; without it a converted number is `check` |
| `from` | no | a carry edge: the row this number was taken from; the value must be in that row and the grade may not rise |
| `quote_sha256`, `quote_words` | private only | digest of the quote's token run and its length; the quote itself is never written (`claims_lib.seal`) |

Verdicts, as in the source-tracing component of the GAIK toolkit that `claims_lib.py` is adapted from (MIT; its notice is kept in that file): **verified** (quote found once, value inside it),
**check** (quote not found, found in more than one place, found at another line than the hint, longer than 40 words, or the value is not inside it),
**reworded** (a text value that is not inside its quote), **unchecked** (the source cannot be read here: external, private, or no checkout).
A `check` is a lint error. An `unchecked` is a warning offline and an error under `--require-resolved`.

Rules that keep the ledger honest:

1. **Grade caps follow the source.** `private:` is never above [S] (a private note is a lead); `external:` is never above [L] (read, not run); only `repo@sha:path` and `self:` can carry [C], and only when the verdict is verified.
2. **A carried number never rises.** `from` names the origin row; the origin must contain the value; the carrier's grade is at most the origin's.
3. **Coverage is a figure, not a goal in itself.** It is the share of numbers in Value cells that have a ledger line with that number: `values_with_quote / values`. A `coverage_floor` in `_meta` fails the lint when coverage drops below it; lowering it shows in the diff. Derived numbers (a ratio, a recompute) stay uncovered unless the receipt that holds them is quoted.
4. **`verified` does not say the quote is the right place.** It says the value is in the words and the words are in the file at that sha. A quote that appears twice needs a `line`. Quotes that name no key (a bare `499`) are weak: quote the key too.
5. **Public hygiene.** Ledgers are served with the site. They go through the same leak sweep as chapters. A private source publishes a digest, never words; `check_claims.py --private DIR` lets its owner re-find the words by digest, and COMPARE cannot be re-run in public.
6. **Pins.** In CI use `--fetch --strict-pins`: every `repo@sha:path` is read at its sha from the public repository, so a pin that was rewritten or never existed is `check`, not silently read at HEAD.

Commands:

```bash
python3 docs/tools-shared/check_learn.py --warn --summary            # offline: ledger <-> register links, value in quote, leak sweep
python3 docs/tools-shared/check_claims.py --fetch --strict-pins --summary --receipt docs/learn/claims/receipt.json
python3 docs/tools-shared/build_learn.py                             # Appendix G from the receipt
python3 -I -B -m unittest discover -s docs/tools-shared -p 'test_claims.py'
```

What this cannot do (same limits as the method it adapts): it cannot tell that a quote is the wrong place when the value is there; it reads
text only (a number in a figure, a PDF scan or a binary has no ledger line); it does not judge a derived figure; and `4.200` stays ambiguous.
