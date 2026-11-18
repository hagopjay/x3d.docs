# 24. Math Lab: one model owner, two transports

> **Say it:** Keep one program that owns the model and let it travel (a local server, or the same files inside the page on WebAssembly); then never trust a float hash across the two, never trust a copied receipt across a dependency major version, and never trust a node count as proof that a scene can be seen. **[C]**

| field | value |
|---|---|
| chapter code | `MLB` |
| prerequisites | [01 The tether](01-the-tether.md) for the thesis; [03 Validator and gates](03-validator-and-gates.md) for what a validator pass does and does not say; [23 Traceability and lineage](23-traceability-lineage.md) for why an identity hash is a claim with a scope |
| after this you can | (1) draw the Math Lab pipeline (kernel, sample, native X3D 4.0 and Manim source text) and say which part owns the numbers; (2) explain why a static host needs no second implementation and what contract makes that true; (3) predict which kernels give a different float hash under Pyodide, and compare across runtimes with a stated tolerance; (4) write a receipt that names every dependency major version; (5) add a screenshot witness for an overlay and say what a node count cannot show; (6) draw the line between generating Manim source and executing it |
| sources read | `x3d.mathslab@24c9bbd` (`docs/PAGES.md`, `docs/FOLDBACK.md`, `VALIDATION.md`, `receipts/runtime-parity.json`, `receipts/browser-smoke-pages.json`, `receipts/browser-smoke-server.json`, `receipts/x3d-validation.json`, `receipts/math-mcp.json`, `receipts/release-checks.json`, `mathlab/mcp_server.py`, `tests/test_pages.py`, `web/app.js`); `x3d.loom` launch note `LEARNINGS-mathlab.md` (the five findings, as written on 2026-11-17 against `x3d.mathslab` at its launch commit `78c3aa4`) |
| instruments used | CPython 3.13.18 (Linux x86_64, glibc); Pyodide 0.27.7 = CPython 3.12.7 on WebAssembly; Chromium 153.0.8010.12 via Playwright 1.63.0, software GL; mcp 2.3.0 (and 1.29.0 in the older receipts); SciPy 1.17.0; Node 22.23.4; the X3D validator pin recorded in `receipts/x3d-validation.json` (`x3d_mcp` commit `b5c9956`, XSD 4.0, semantic vocabulary 4.1). Nothing was re-run for the five findings; the drills below re-read the recorded receipts with Python 3.13.18 |

Math Lab is a set of six lessons (linear maps, derivative, integral, Fourier series, Lorenz, gradient descent) in which one Python kernel per lesson produces numbers and everything the learner sees is generated from those numbers. It was first a local application and then put on a static host. Moving it taught five things that apply to any X3D project that wants to run on a page with no server behind it. This chapter states each with its number, its instrument and its grade, and it marks what was not tested.

---

## 1. The map

```text
   lesson parameters (JSON, 32 KiB cap, finite numbers only)
        |
        v
   decode_request  -- one gate, one 4 MiB response budget, both transports
        |
        v
   kernel  mathlab/*.py   pure standard library; the ONLY owner of the numbers
        |
        v
   sample  (floats + metrics)  ---- identity: sample_sha256  (same-runtime identity, section 4)
        |
        +--> X3D 4.0 adapter -> native scene (8 root nodes) -> X_ITE in the browser
        |                              \-> validated: XSD 4.0 + semantic checks (section 7)
        +--> Manim source text (a string; never imported, never run on the public page)

   transport A  server mode : loopback HTTP /api/*  -> local CPython 3.13.18
   transport B  Pages mode  : web/static-api.js -> Pyodide 0.27.7 (CPython 3.12.7) in page
   selector: /api/health answers "x3d.mathlab" on 127.0.0.1 or localhost, else Pyodide
```

| in scope | out of scope |
|---|---|
| the pipeline above; why the model owner stays single; the stdlib-only contract; the parity measurement between the two Pythons; the receipt that named one dependency major version; the overlay that hid a validated scene; the generate/execute split for Manim | the lessons' mathematics (the repository has its own independent checks in `receipts/independent-math.json`, not read here); hardware GPU timing; browsers other than Chromium; the Manim video itself (not rendered); whether Pages is live (that depends on a repository setting) |

| the five findings | grade | section |
|---|---|---|
| one model owner survives a move to static hosting | [C] | 3 |
| a float hash is a same-runtime identity | [C] | 4 |
| a receipt is true for one dependency major version | [C] | 5 |
| a scene can pass every structural check and be partly hidden | [L] for the pixels, [C] for the code read | 6 |
| generate Manim source on the public host, execute it only locally | [L] | 7 |

Read next: deeper, [23 Traceability and lineage](23-traceability-lineage.md) for the same question (what exactly does an identity or a receipt bind) answered with a hash chain; wider, [21 Many hands on one scene](21-yjs-collaboration.md) for a second case where two runtimes must agree on one scene.

---

## 2. The architecture and who owns what

| stage | file or tool | what it owns | what it must not do |
|---|---|---|---|
| request gate | `decode_request` (32 KiB, strict JSON, finite numbers); 4 MiB response budget | refusing a bad request before a kernel sees it | differ between transports |
| kernel | `mathlab/*.py`, one per lesson | every number: samples, metrics, closed-form references | import anything outside the standard library (needed for transport B) |
| sample | the kernel's output plus `sample_sha256` | identity of one run in one runtime | stand as an identity across runtimes (section 4) |
| X3D adapter | native X3D 4.0 writer | geometry, DEF names, metadata that records the parameters and the sample identity | re-derive a number the kernel owns |
| Manim bridge | source-text generator | a Python program as a string, from the same sample | import or execute Manim on the public page (section 7) |
| renderer | X_ITE in the page | pixels | be the only evidence that a scene is correct |
| transport | loopback HTTP, or `web/static-api.js` calling Pyodide | moving the same request and response | hold model logic |

The rule behind the table is the one this base keeps meeting: a number should have one author. When the page needs the model, the cheapest way to give it a second author is to port the kernel to JavaScript, and the cost of that choice shows up later as drift. Math Lab avoided it by making the kernels portable instead of porting them. **[C]** (design read in `docs/PAGES.md`; the contract is tested, section 3.)

---

## 3. Why the model owner stays single: Pyodide as a static transport

Pages mode fetches the same `mathlab/*.py` files, writes them into the Pyodide file system and calls them behind the same request gate and the same 4 MiB budget. There is no second implementation of any lesson. `pyodide.js` is pinned by an SRI sha384 and loaded from a pinned version path. **[C]** (`x3d.mathslab@24c9bbd:docs/PAGES.md`, read.)

What makes this safe is a portability contract, not luck. `tests/test_pages.py` has four tests:

| test | what it fails on |
|---|---|
| `test_every_installed_module_exists` | the list of files copied into the browser names a file that is not there |
| `test_installed_modules_import_only_stdlib_and_each_other` | a kernel imports a third-party package (the kernels use no SciPy; the independent check in `receipts/independent-math.json` is separate) |
| `test_installed_set_covers_server_dependencies` | a module the server needs is missing from the browser set |
| `test_manim_is_never_installed_in_the_browser` | Manim, or the MCP wrapper `mcp_server`, would be shipped to the page |

The measurement, from the two recorded browser passes (same 6 lessons, same probe, Chromium 153.0.8010.12 via Playwright 1.63.0, software GL, Linux):

```text
                           server mode (CPython 3.13.18)     Pages mode (Pyodide 0.27.7)
 lessons rendered                 6 of 6                            6 of 6
 root nodes per scene             8                                 8
 console errors                   0                                 0
 first native scene               1.833 s                           5.159 s  (incl. ~10 MB)
 each lesson switch               1.950 - 2.196 s                   2.219 - 2.550 s
 parameter nudge changes model id yes (MODEL cea87d14.. -> 5c97982f..)   same two ids
 Manim download                   mathlab-gradient.py, 104,672 B, has a Scene class   same
```

| fact | value | grade | instrument |
|---|---|---|---|
| lessons rendered from Pyodide | 6 of 6, 0 console errors | [C] | `receipts/browser-smoke-pages.json`, Chromium 153.0.8010.12, Playwright 1.63.0, software GL |
| first native scene, Pages vs server | 5.159 s vs 1.833 s | [C] | `receipts/browser-smoke-pages.json`, `receipts/browser-smoke-server.json` |
| lesson switch, Pages vs server | 2.219 to 2.550 s vs 1.950 to 2.196 s, each including a 1.5 s settle wait in the probe | [C] | same |
| first scene, as quoted in the launch note | 4.6 to 5.0 s | [L] | the launch note; the retained receipt holds 5.159 s, a different run, so the receipt is the number to quote |
| runtime download | about 10 MB, needs the network on first load | [L] | `docs/PAGES.md`, a stated size, not measured separately |

Two honest remarks. The timings include a network download over the sandbox proxy and a software renderer, so they bound the cost of the transport and say nothing about a user's machine. And the Pages numbers are not a claim that Pyodide is fast: the first scene took 2.8 times the server's time, and no profile separates the runtime download from the rest.

---

## 4. A float hash is a same-runtime identity

Both transports run the same source files at default parameters. The source hashes match everywhere. The samples do not always match, and the pattern is clean:

| lesson | floats compared | differing | max absolute difference | `sample_sha256` equal | numeric functions used |
|---|---:|---:|---:|---|---|
| linear | 990 | 18 | 2.220e-16 | no | `sin`, `cos`, `exp` |
| derivative | 759 | 5 | 4.441e-16 | no | `sin`, `cos`, `exp` |
| integral | 1,206 | 0 | 0 | yes | +, *, sqrt |
| fourier | 2,314 | 20 | 3.331e-16 | no | `sin`, `cos`, `exp` |
| lorenz | 6,073 | 0 | 0 | yes | +, *, sqrt |
| gradient | 5,041 | 0 | 0 | yes | +, *, sqrt |
| **total** | **16,383** | **43** | **4.441e-16** | 3 of 6 | |

Instrument: `x3d.mathslab@24c9bbd:receipts/runtime-parity.json`; native CPython 3.13.18 on glibc against Pyodide 0.27.7 (CPython 3.12.7 on WebAssembly) in Chromium via Playwright 1.63.0; the floats were walked recursively over the whole sample. **[C]**

Reading it:

* The three identical lessons together hold 12,320 floats, all equal bit for bit. The three that differ differ in 43 of 4,063 floats (18 + 5 + 20 of 990 + 759 + 2,314), each by at most 4.441e-16.
* `math.ulp(1.0)` is 2.220e-16 and `math.ulp(2.0)` is 4.441e-16 (run, drill D-MLB-3), so the largest difference is one or two units in the last place depending on the magnitude of the value. The receipt says "about one ulp"; that is the right order and the receipt does not record the magnitudes. **[C]** for the ulp values, **[L]** for "one or two".
* The split follows the functions used. Addition, multiplication and square root are correctly rounded by IEEE 754, so two runtimes agree. `sin`, `cos` and `exp` are not required to be correctly rounded and each runtime's math library may round a last bit differently. That is the explanation the receipt gives, and the three-and-three split fits it; it was not tested by swapping the math library, so it is **[L]**.
* The consequence is about identity, not accuracy. An identity hash over floats binds the data to the runtime that produced it. Two correct runtimes can disagree on the hash and be equally right.

```text
   what to compare            same runtime               across runtimes
   ---------------------------------------------------------------------------------
   source files               sha256 of the bytes        sha256 of the bytes   (matched: 6 of 6)
   samples                    sample_sha256 (replay)     floats within a stated tolerance
   X3D text                   byte hash                  byte hash, if floats print alike
```

The tolerance has to be stated and has to be chosen on purpose: the one in the drill (1e-12 absolute) accepts the recorded differences with room to spare and rejects a 1e-9 perturbation. That tolerance is a teaching choice, not a Math Lab setting. **[S]** as a recommendation for a real project.

---

## 5. A receipt is true for one dependency major version

The first delivered validation named `mcp` 1.29.0 and recorded 89 passing tests plus a passing stdio probe. The first fresh run under `mcp` 2.3.0 failed 4 of those 89:

| change in `mcp` 2.x | effect | fix |
|---|---|---|
| `mcp.server.fastmcp` renamed (`MCPServer` in `mcp.server.mcpserver`) | the server module no longer imported | a try/except import of either name in `mathlab/mcp_server.py` |
| tool annotation attributes became snake_case (`readOnlyHint` became `read_only_hint`) | tests that read the old spelling failed | tests and the probe read both spellings |

After a change of about four lines, 93 of 93 tests pass and the stdio probe passes 6 of 6, now recorded as `mcp_sdk: 2.3.0`. **[C]** Instrument: `python -m unittest discover` under CPython 3.13.18 with mcp 2.3.0; records `x3d.mathslab@24c9bbd:receipts/release-checks.json` ("Ran 93 tests"), `receipts/math-mcp.json`, and `docs/FOLDBACK.md` (the lesson). The older figures (89 passed, SDK 1.29.0) are in `VALIDATION.md` at the same commit and are still true of that environment.

```text
   receipt A (old):  tests = 89 pass    mcp = 1.29.0    <- true, and invisible to anyone on 2.x
   fresh run (new):  tests = 89, 4 fail mcp = 2.3.0     <- the witness
   receipt B (new):  tests = 93 pass    mcp = 2.3.0     probe 6 of 6
```

The point is not that `mcp` broke compatibility; a major version is allowed to. The point is that the old receipt was a true statement about an environment it did not name, so nobody could see it had expired. A receipt that records every dependency's major version fails loudly when the environment changes, and a fresh-environment run is a witness that a copied receipt can never be.

---

## 6. The overlay hid a validated scene

The page draws the 3D canvas full size and puts an equation card over its lower part. All structural checks were green: eight root nodes, a valid X3D document, a passing validator run. At 1440 by 900 pixels the Lorenz, gradient and integral scenes were partly behind the card, by about 100 pixels at the bottom. **[L]** for the size: the before and after screenshots were taken with Playwright 1.63.0 and recorded in the launch note, and are not retained in the repository; `docs/FOLDBACK.md` records the lesson in words.

The fix has two parts, both visible in the code: size the canvas to the region the card leaves free, and zoom the authored viewpoint after the world loads (`viewpoint.fieldOfView *= 0.75` in `web/app.js`). The comment in the code says the change is view-only: the X3D document, its bounds and its identity are untouched. **[C]** (code read, `x3d.mathslab@24c9bbd:web/app.js`; not re-run.)

| check | passes while the scene is hidden | what it is a witness for |
|---|---|---|
| node count (8 root nodes) | yes | the adapter produced the expected structure |
| XSD 4.0 plus semantic checks, 6 worlds, 2 negative twins caught | yes | the file is valid and two named defects are caught |
| identity hash matches the export | yes | the bytes are the ones the kernel produced |
| screenshot at a stated size, compared before and after | **no** | what a person sees at that size |

The validation receipt is explicit about its reach: it names the tool pin (`x3d_mcp` commit `b5c9956`, XSD 4.0, semantic vocabulary 4.1, direct function calls, no network and no model), it caught an invalid numeric radius at the XSD stage and a missing ROUTE source at the semantic stage, and it says per-file checks "do not establish Math Lab mapping fidelity, physical validity, visible rendering or GPU performance". **[C]** (`receipts/x3d-validation.json`, read.) Visibility belongs to a rendering witness. Chapter 06 covers the renderer as an oracle; this finding is the reason a page with an overlay needs one that looks at pixels.

---

## 7. Generate versus execute: the Manim boundary

Manim renders a video by running Python. A public static host should not offer that. The Pages build therefore does two things and refuses a third:

| action | on the public page | where it happens |
|---|---|---|
| generate Manim source text from the shared sample | yes | in the page, same generator as the server (download `mathlab-gradient.py`, 104,672 bytes, contains a `Scene` class) |
| import Manim | never | `test_manim_is_never_installed_in_the_browser` |
| execute the source, render a video | no | local only: needs a local Manim install and a local server |

There is no code-execution endpoint on a static host because there is no server; the in-browser Python can evaluate only the six enumerated lessons. **[L]** The boundary is designed and tested at the module-list level (the browser module list excludes the MCP wrapper and Manim); it was not attacked, for example by trying to make the page evaluate a string. The video path itself was not run in this measurement (section 9). The rule it teaches is general: split generation from execution, and let only generation ship to a public host.

```text
   shared sample --> generate source text --> [ public page: show / download ]
                                        \
                                         `--> execute: local only, trusted scene, own limits
```

---

## 8. Using it

| step | command or place | what comes back |
|---|---|---|
| list the portability tests | `python3 -I -m unittest tests.test_pages -v` from the repository root | four tests, each a contract in section 3 |
| read the parity receipt | `python3 -I -c "import json;print(json.load(open('receipts/runtime-parity.json'))['finding'])"` | the one-sentence finding |
| find which lessons disagree | read `lessons.<name>.bit_identical` in the same file | false for linear, derivative and fourier |
| compare the two transports | read `receipts/browser-smoke-pages.json` and `receipts/browser-smoke-server.json`, field `lessons[].model` | equal model ids for integral, lorenz, gradient; different for the other three |
| one pass over every lesson | `tools/browser_smoke.js` in `x3d.mathslab` | a JSON receipt with a parameter nudge, a download check and console errors, against either transport |
| the transport selector | `web/app.js`, `/api/health` probe | the loopback server answers `x3d.mathlab`; any other host uses Pyodide |

---

## 9. What was not tested, ranked by how likely it is to matter

1. **Hardware GPU.** Every render and timing is Chromium 153 on software GL. Frame time and GPU memory are unmeasured.
2. **Other browsers and devices.** Firefox, Safari and a phone were not run. Pyodide and WebGL differences are the likely places for a gap.
3. **Parity away from default parameters.** The 16,383 floats are at default parameters only. A different parameter reaches different inputs to `sin`, `cos` and `exp`; the size of the difference there is unmeasured, and the tolerance in section 4 is a guess for it.
4. **Manim video.** Only source generation ran. No video was rendered, so nothing here shows that the generated source renders as the X3D scene looks.
5. **A deployed Pages site.** The files and the design were read and the page was served from a local static server for the receipts. Pages goes live only when the repository owner enables it (Settings, Pages, main, root).
6. **The math itself.** This chapter does not re-check the lessons' mathematics.

---

## Heuristics

| ID | Rule | Grade | Evidence | Instrument |
|---|---|---|---|---|
| H-MLB-1 | Run the model owner's own code in the page instead of porting it; write "standard library only" as a contract and test it. | C | 6 of 6 lessons rendered from Pyodide behind the same gate; 4 portability tests | `x3d.mathslab@24c9bbd:receipts/browser-smoke-pages.json`, `tests/test_pages.py` |
| H-MLB-2 | Never compare numeric data across runtimes by hash; compare floats with a tolerance you state, and keep the hash for same-runtime replay. | C | 3 of 6 lessons hash differently across CPython 3.13.18 and Pyodide 0.27.7; 43 of 16,383 floats differ by at most 4.441e-16 | `receipts/runtime-parity.json`, Playwright 1.63.0 |
| H-MLB-3 | Expect `sin`, `cos`, `exp` to be the first functions to differ across runtimes; +, *, sqrt are correctly rounded and agree. | L | the three lessons that differ use the first set, the three that agree use the second; the math library was not swapped to confirm | same |
| H-MLB-4 | Write every dependency's major version into the receipt, and treat a fresh-environment run as the witness. | C | 4 of 89 tests failed under mcp 2.3.0; the receipts named 1.29.0; 93 of 93 pass after the shim | `python -m unittest discover`, CPython 3.13.18, mcp 2.3.0 |
| H-MLB-5 | Add a screenshot witness for any overlay, at a stated window size; do not read a node count or a validator pass as visibility. | L | a validated scene was partly behind a card at 1440x900; node counts and X3D validation were green | launch note, Playwright 1.63.0; fix read in `web/app.js` |
| H-MLB-6 | Change the view, not the document, when you reframe for an overlay: keep the X3D bytes and the identity unchanged. | C | `fieldOfView *= 0.75` applied after load; the code says the document, bounds and identity are untouched | `x3d.mathslab@24c9bbd:web/app.js`, read |
| H-MLB-7 | Split generate from execute; ship only generation to a public static host and keep a test that the execution library is never installed there. | L | Manim source is generated in the page; `test_manim_is_never_installed_in_the_browser` | `tests/test_pages.py`; not attacked |
| H-MLB-8 | Put the transport behind one selector and one response shape, so the controller code is the same for both. | C | `/api/health` probe picks loopback or Pyodide; the two smoke receipts have identical `lessons[]` fields | `web/app.js`, both smoke receipts |
| H-MLB-9 | Quote a timing from a recorded receipt, not from a note, and name the transport, the browser and the renderer. | C | the note says 4.6 to 5.0 s for the first scene; the retained receipt says 5.159 s | `receipts/browser-smoke-pages.json` |

---

## Drills

Each drill needs a checkout of `x3d.mathslab` at `24c9bbd` (or later) and `python3 -I`. They read recorded receipts; none renders anything.

### D-MLB-1 Which lessons are bit-identical
- **Level:** L1
- **Task:** From the parity receipt, list the lessons whose samples are bit-identical across CPython and Pyodide, and the number of floats they hold together.
- **Verify:** `python3 -I -c "import json;p=json.load(open('receipts/runtime-parity.json'))['lessons'];print([k for k,v in p.items() if v['bit_identical']],sum(v['floats'] for v in p.values() if v['bit_identical']))"`
- **Answer:** `['integral', 'lorenz', 'gradient']` and 12320.
- **Checked:** 2026-11-17 `x3d.mathslab@24c9bbd` receipt, Python 3.13.18

### D-MLB-2 Totals and the worst difference
- **Level:** L2
- **Task:** Over all six lessons, how many floats were compared, how many differ, and what is the largest absolute difference? Which lessons carry all the differences?
- **Verify:** `python3 -I -c "import json;p=json.load(open('receipts/runtime-parity.json'))['lessons'];print(sum(v['floats'] for v in p.values()),sum(v['differing_floats'] for v in p.values()),max(v['max_abs_diff'] for v in p.values()))"`
- **Answer:** 16383 floats, 43 differ (18 linear, 5 derivative, 20 fourier), maximum 4.441e-16.
- **Checked:** 2026-11-17 `x3d.mathslab@24c9bbd` receipt, Python 3.13.18

### D-MLB-3 What one ulp is, and what a tolerance has to accept
- **Level:** L2
- **Task:** Print `math.ulp` at 1.0, 2.0 and 4.0. Then take 200 values `sin(i/10)`, move one of them by one unit in the last place with `math.nextafter`, and compare the two lists three ways: by a hash of `repr`, by an absolute tolerance of 1e-12, and again after adding 1e-9 to one value.
- **Verify:** `python3 -I -c "import math,hashlib;xs=[math.sin(i/10) for i in range(1,201)];ys=list(xs);ys[7]=math.nextafter(ys[7],2.0);h=lambda v:hashlib.sha256(repr(v).encode()).hexdigest();print(math.ulp(1.0),math.ulp(2.0),math.ulp(4.0),h(xs)==h(ys),all(abs(a-b)<=1e-12 for a,b in zip(xs,ys)));zs=list(xs);zs[7]+=1e-9;print(all(abs(a-b)<=1e-12 for a,b in zip(xs,zs)))"`
- **Answer:** `2.220446049250313e-16 4.440892098500626e-16 8.881784197001252e-16`, then `False True` (hash differs, tolerance accepts one ulp), then `False` (tolerance rejects a 1e-9 shift). The recorded maximum, 4.441e-16, is 2 ulp at 1.0 or 1 ulp for values in [2, 4).
- **Checked:** 2026-11-17 Python 3.13.18, standard library only

### D-MLB-4 Same model, two transports
- **Level:** L2
- **Task:** Compare `lessons[].model` between the Pages and the server smoke receipts. For how many lessons is the model identity equal, and which are they? Does that agree with D-MLB-1? Then read `first_native_scene_s` in both.
- **Verify:** `python3 -I -c "import json;a=json.load(open('receipts/browser-smoke-pages.json'));b=json.load(open('receipts/browser-smoke-server.json'));print([x['model']==y['model'] for x,y in zip(a['lessons'],b['lessons'])],a['first_native_scene_s'],b['first_native_scene_s'])"`
- **Answer:** `[False, False, True, False, True, True]`, 5.159 and 1.833. Equal for lessons 3, 5 and 6 (integral, lorenz, gradient), the same three as D-MLB-1: the model id in the page is the sample hash, so it inherits the runtime scope.
- **Checked:** 2026-11-17 `x3d.mathslab@24c9bbd` receipts, Python 3.13.18

### D-MLB-5 The portability contract
- **Level:** L1
- **Task:** Name the four tests in `tests/test_pages.py` and say which one stops Manim reaching the page.
- **Verify:** `grep -n "def test_" tests/test_pages.py`
- **Answer:** `test_every_installed_module_exists`, `test_installed_modules_import_only_stdlib_and_each_other`, `test_installed_set_covers_server_dependencies`, `test_manim_is_never_installed_in_the_browser` (the last one).
- **Checked:** 2026-11-17 `x3d.mathslab@24c9bbd`, `grep`

### D-MLB-6 Receipt versus fresh run
- **Level:** L3
- **Task:** (a) Find where the older validation names the `mcp` version and test count, and where the newer receipt records the SDK. (b) Find the line that lets the server import under both 1.x and 2.x. (c) Write the receipt row that would have made the 2.x failure visible on day one, and say what a reader on 2.3.0 should have done on reading the old receipt.
- **Verify:** `grep -n "1.29.0\|89 passed" VALIDATION.md`; `grep -n "mcp_sdk" receipts/math-mcp.json`; `sed -n 15,19p mathlab/mcp_server.py`
- **Answer:** (a) `VALIDATION.md` names SDK 1.29.0 and 89 tests; `receipts/math-mcp.json` has `"mcp_sdk": "2.3.0"`. (b) the `try: from mcp.server.fastmcp import FastMCP` / `except ModuleNotFoundError: from mcp.server.mcpserver import MCPServer as FastMCP` pair. (c) a row such as `mcp 1.29.0 (major 1)` beside the test count; a reader on 2.3.0 should treat the receipt as not applying and re-run, which finds 4 failures out of 89.
- **Checked:** not run (read only; the 4-of-89 failure itself was not reproduced here)

---

## Honest limits

* **[C]** Nothing was re-run for the five findings. The numbers are read from receipts in `x3d.mathslab@24c9bbd` and from the launch note; the drills re-read the receipts and compute small facts (ulp values, totals) with Python 3.13.18.
* **[C]** All renders and timings are Chromium 153.0.8010.12 via Playwright 1.63.0 on software GL, one machine, single runs. No hardware GPU, no Firefox, Safari or phone.
* **[C]** Parity was measured at default parameters only. A different parameter point may give larger differences; this is unmeasured.
* **[L]** The explanation of the parity split (correctly rounded operations agree, transcendental functions may not) fits the pattern and is the receipt's own reading; the math library was not swapped to test it.
* **[L]** The overlay's size (about 100 px) and the effect of the fix come from before and after screenshots recorded in the launch note; the screenshots are not retained in the repository. The code that applies the fix was read.
* **[L]** The generate/execute boundary was checked by a module-list test, not attacked. Manim video was not rendered.
* **[C]** Two sources disagree slightly: the launch note gives 4.6 to 5.0 s for the first scene and 2.1 to 2.5 s per switch; the retained receipts give 5.159 s and 2.219 to 2.550 s. This chapter uses the receipts; the note's figures are graded [L].
* **[C]** The launch note cites the launch commit `78c3aa4`; the receipts were read at `24c9bbd`, a later commit of the same repository.
* **[S]** The 1e-12 tolerance is a teaching value for a stdlib kernel of this size, not a recommendation measured on other data.
* **[C]** The X3D validation reaches XSD 4.0 and a semantic subset on six default worlds; it is unsigned and is not a formal acceptance receipt. The X3D validator pin is `x3d_mcp` commit `b5c9956`, which is not one of the two validator strings in Appendix A (`x3d_mcp fork b4efcd3`, `x3d_mcp upstream 74da0ec`).

---

## Numbers register

| ID | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|
| N-MLB-1 | floats compared across CPython 3.13.18 and Pyodide 0.27.7, six lessons | 16,383 | [C] | default parameters, Playwright 1.63.0 Chromium | `x3d.mathslab@24c9bbd:receipts/runtime-parity.json` |
| N-MLB-2 | floats that differ, total (linear 18, derivative 5, fourier 20) | 43 | [C] | same | same |
| N-MLB-3 | floats in the three bit-identical lessons (integral, lorenz, gradient) | 12,320 | [C] | same | same |
| N-MLB-4 | largest absolute float difference | 4.441e-16 | [C] | same | same |
| N-MLB-5 | lessons whose `sample_sha256` is equal across runtimes | 3 of 6 | [C] | same | same |
| N-MLB-6 | `math.ulp` at 1.0; at 2.0 | 2.220446049250313e-16; 4.440892098500626e-16 | [C] | `math.ulp`, Python 3.13.18 | drill D-MLB-3, run |
| N-MLB-7 | lessons rendered from Pyodide; console errors | 6 of 6; 0 | [C] | Chromium 153.0.8010.12, Playwright 1.63.0, software GL | `x3d.mathslab@24c9bbd:receipts/browser-smoke-pages.json` |
| N-MLB-8 | first native scene, Pages; server | 5.159 s; 1.833 s | [C] | same, both receipts | `receipts/browser-smoke-pages.json`, `receipts/browser-smoke-server.json` |
| N-MLB-9 | lesson switch, Pages; server (each includes a 1.5 s settle wait) | 2.219 to 2.550 s; 1.950 to 2.196 s | [C] | same | same |
| N-MLB-10 | first native scene, as written in the launch note | 4.6 to 5.0 s | [L] | the launch note; superseded by N-MLB-8 | `x3d.loom` `LEARNINGS-mathlab.md` |
| N-MLB-11 | Pyodide runtime download, first load | about 10 MB | [L] | stated in `docs/PAGES.md`, not separately measured | `x3d.mathslab@24c9bbd:docs/PAGES.md` |
| N-MLB-12 | tests failed under mcp 2.3.0 out of the old suite | 4 of 89 | [C] | `python -m unittest discover`, CPython 3.13.18, mcp 2.3.0 | `x3d.mathslab@24c9bbd:docs/FOLDBACK.md` |
| N-MLB-13 | tests passing after the shim; stdio probe checks | 93 of 93; 6 of 6 | [C] | same | `x3d.mathslab@24c9bbd:receipts/release-checks.json`, `receipts/math-mcp.json` |
| N-MLB-14 | mcp version in the older receipt; in the newer receipt | 1.29.0; 2.3.0 | [C] | read | `x3d.mathslab@24c9bbd:VALIDATION.md`, `receipts/math-mcp.json` |
| N-MLB-15 | request cap; response budget | 32 KiB; 4 MiB | [C] | read, not run here | `x3d.mathslab@24c9bbd:docs/PAGES.md` |
| N-MLB-16 | root nodes per scene | 8 | [C] | Chromium 153.0.8010.12, Playwright 1.63.0 | `x3d.mathslab@24c9bbd:receipts/browser-smoke-pages.json` |
| N-MLB-17 | generated Manim source, gradient lesson | 104,672 bytes | [C] | same | same |
| N-MLB-18 | X3D validation: worlds passed; negative twins caught | 6; 2 | [C] | `x3d_mcp` commit `b5c9956`, XSD 4.0, semantic vocabulary 4.1, direct calls | `x3d.mathslab@24c9bbd:receipts/x3d-validation.json` |
| N-MLB-19 | overlay: canvas hidden by the equation card at 1440x900 | about 100 px | [L] | before and after screenshots, Playwright 1.63.0, in the launch note, not retained | `x3d.loom` `LEARNINGS-mathlab.md` |
| N-MLB-20 | field-of-view scale applied after load | 0.75 | [C] | read | `x3d.mathslab@24c9bbd:web/app.js` |

---

## Sources and provenance

Read on 2026-11-17: the public repository `x3d.mathslab` (https://github.com/hagopjay/x3d.mathslab) at `24c9bbd`, files listed in the header; the launch note `LEARNINGS-mathlab.md` of `x3d.loom` (five findings, written against the repository's launch commit `78c3aa4`). Nothing was re-run for the findings. Python 3.13.18 was used only to read the recorded receipts and to compute the ulp values in drill D-MLB-3. The X3D validator is the pin recorded in the receipt, not one of Appendix A's two named validators. Gaps: the before and after screenshots of section 6 are held outside the public repository and are therefore graded [L]; the Manim video path and any hardware GPU run do not exist yet.
