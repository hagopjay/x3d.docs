# x3d.dance: two HAnim dancers that listen, groove and learn (28 Nov 2026)

Built by hagsMac in hagopjay/x3d.dance (public). Learnings are in x3d.loom `LEARNINGS-dance.md` (failure modes 516 to 518). Integration receipt: x3d.dance `docs/ECOSYSTEM.md`.

## What it is

| Part | What | Where |
|---|---|---|
| Bodies | Ada and Rex, HAnim 2.0 LOA-4 (146 joints), MakeHuman CC0 skin, X3D 4.0 and 4.1 | `hanim/`, `web/stage-*.x3d` |
| Ears | Audio in, tempo, phase, bar, syncopation, sections (spectral flux, autocorrelation) | `web/src/dsp.js` |
| Groove | Each dancer's own pocket and latency, coupled to the partner | `web/src/beatmind.js`, `dancer.js` |
| Memory | HAnimMotion export, genomes and ratings in MetadataSet, SHA-256 hash chain | `web/src/export.js` |
| Learning | 20 genes, evolution from your thumbs up and down; training under the Loom method | `web/src/evolve.js`, `tools/train.mjs`, `runs/` |
| Blender | X3D to the node editor and back, HAnimMotion to Action, Cycles renders | `blender/` |

## What the validators say (x3d_mcp `ca0e75c`, X_ITE 16.8.1, headless Chromium with SwiftShader)

| File | XSD | Semantic check | Own linter |
|---|---|---|---|
| `stage-4.0.x3d` (3.9 MB), `stage-4.1.x3d` (4.0 MB) | valid | 1 error (`PhysicalMaterial` outside Immersive), fixed by a Shape level 2 statement; 13 harmless weight-0 warnings remain | OK |
| `stage-4.0-mannequin.x3d` (0.46 MB) | valid | clean | not run |
| Synthetic house performance, 180 frames, 48 joints | valid | same cause as the stage | not run |

X_ITE draws the scene with or without the statement.

## Where to see it

The demo page is listed on the x3d.demo site once the demo number is assigned.

## Credit and takedown

MakeHuman assets are CC0 (MakeHuman team / Data Collection AB); X_ITE is MIT (create3000); HAnim joint values trace to ISO/IEC 19774-1:2019 as reproduced in x3d.py and coderextreme/x3dschema. No commercial music is committed. To have anything removed, open an issue on hagopjay/x3d.dance.
