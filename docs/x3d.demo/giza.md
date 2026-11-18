# Giza VI · The Five Witnesses (five editions, one night, one ledger)

Demo folder `docs/demos/giza-osiris-hall/v6/` in x3d.demo (PR 83). It ships beside the unchanged packs `v4/` (Hawara Witness Atlas v4.1), `v4-horizon/` (Giza IV Horizon Engine) and `v5/` (Giza V Earth's Tesla Coil). v1 to v3 are untouched. Full lesson table: x3d.loom `LEARNINGS-giza-vi.md` (G6-1 to G6-15).

**What it shows.** A 216 s guided film in five acts and 16 shots, which you can pause and walk around in:

| Act | Name | What it covers | Mark |
|---|---|---|---|
| I | Stone | the measured plateau | Confirmed |
| II | Below | the Osiris Shaft, Hawara 81.6 km south, Herodotus's twelve courts under VISOR | Likely |
| III | Horizon | Giza IV's king in the King's Chamber | Authored |
| IV | Coil | Giza V's sky plate and arcs, paid for by its live energy ledger | Authored |
| V | Return | real HYG stars precessed from 10,500 BCE to 2000 CE, then the equinox dawn | Likely |

It is drawn by Babylon.js 8.56.2. Every caption line and each of the 33 ledger rows carries a mark: Confirmed, Likely, Suspected or Authored. Authored marks invention; it is not a truth grade.

| Check | Result | Instrument |
|---|---|---|
| X3D twin `giza-vi.x3d` | 4.0 Immersive, XSD valid, 0 semantic errors, 0 warnings; 40 meshes, 67,726 vertices, 111,850 triangles | x3d_mcp `fa5dccf` |
| Twin in X_ITE | ready in 2.96 s, 16 Viewpoints, 0 page errors | X_ITE 16.6.0, headless Chromium 157, SwiftShader (no GPU) |
| Page | ready in 1.1 to 1.4 s, 0 page errors, 16 shots reviewed | Babylon.js 8.56.2, same browser |
| Tests | VI 11/11, Hawara 17/17, IV 38/38 + 8, V 58/58 | Node 22.23.5, Python 3.13 |
| Pack numbers | Giza to Hawara is 81.6 km straight line (the pack says "roughly 90 km"); the 12.5 GJ bank drains in 20.66 s with supply off | haversine on Wikipedia coordinates; V's `tesla.mjs` |

**Three things to remember.**
1. One pure geometry module feeds both renderers. The showpiece can use every Babylon trick while the accountable file stays validated X3D, with a grade on every Shape and the inventions hidden in a `Switch`.
2. In Babylon's right-handed mode, faces stay clockwise-front, and `ComputeNormals` with the RH flag points them inward. The exporter swaps indices so the X3D file is `ccw='true'`.
3. `CascadedShadowGenerator` drew nothing in this scene, while a plain PCF `ShadowGenerator` worked at once.

**Open.**
- No real-GPU timing yet.
- The IV and V scenes keep their 3 and 7 `MetadataString` containerField semantic errors, as authored.
- Act III's ghosted-pyramid shot reads dim on SwiftShader.
- A demo card number is pending from the demo lane.
