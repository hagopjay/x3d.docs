# x3d.gobbler field notes (17 Nov 2026)

Repo: https://github.com/hagopjay/x3d.gobbler (commit 4a24d4b). A 12-feather X3D observatory bound to the Atlas (2,181 entities, 7,222 edges, pinned `x3d.loom@ba30153` + `x3d.docs@ff0565e`). Rig for every number below: Python 3.13.18, rdflib 7.6.0, x3d_mcp `fa5dccf`, Chromium 153.0.8010.12 on SwiftShader (behaviour, not speed).

## Why this repo matters to x3d.docs
The Atlas witness imports `docs/tools-shared/learn_lib.py` and `claims_lib.py` from **this** repo at a pinned sha. Result of the replay: with `x3d.docs@ff0565e` present, the six Atlas output files rebuild byte-identical and the 17-check witness plus two scene checks pass (19/19). Those two helper files are therefore load-bearing for another repo: renaming or moving them breaks the Atlas. Keep their paths stable or bump the pin deliberately.

## Reproduce
```bash
git clone https://github.com/hagopjay/x3d.gobbler && cd x3d.gobbler
python3 tools/fetch_pins.py          # shallow-fetches x3d.docs at flywheel-review/atlas/src/DOCS.sha
make replay PY=python               # needs rdflib; X3D_MCP_DIR=<x3d_mcp checkout> for the XSD/semantic scene check
```

## Four traps this turned up (details and evidence: x3d.gobbler/CHANGES.md)
| Trap | Fix |
|---|---|
| A single-file X_ITE page cannot lazy-load `assets/components/*`, `assets/lib/*.wasm` or `x_ite.css`; the page hides the canvas until the stylesheet loads, so it dies with a generic "could not open" message | embed components as blob URLs, the wasm as a data URL, the CSS byte-exact (SRI), and shim `getProviderURL` / `getLibraryURL` |
| `rotation 0 0 0 3.142` from a look-at helper: near a half turn the antisymmetric part vanishes | read the axis from the symmetric part; x3d_mcp's `rotation-zero-axis` rule catches it |
| Absolute home-directory paths in witness scripts | `X3D_MCP_DIR` / `X3D_DOCS` env with a sibling-checkout fallback |
| Absolutely positioned side panels with no bottom bound overlap the control bar below ~900 px height | bottom-anchor and scroll; test with a real click, not a DOM query |
