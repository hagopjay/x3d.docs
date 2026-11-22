# The Fault Lab: what the ontology fixes catch, and what other formats lose (20 Nov 2026)

Live demo: https://hagopjay.github.io/x3d.demo/demos/fault-lab/v1/ and, with the Blender fix measured, https://hagopjay.github.io/x3d.demo/demos/fault-lab/v2/ and, with the glTF extras lifted into semantic packets, https://hagopjay.github.io/x3d.demo/demos/fault-lab/v3/.
Fixes it exercises: [ontology-review-fixes.md](ontology-review-fixes.md). Full notes: x3d.loom `LEARNINGS-fault-lab-v1.md`.

One heritage twin (an X3D scene of the Giza plateau joined to a CIDOC-CRM record) was broken ten ways, one edit each.
All results are Confirmed on the instrument named. The faults are planted by us, so the rates describe these kinds of
mistake, not files found in the wild.

## The ten faults

| Fault | Lives in | Pixels changed | Before | After | Caught by |
|---|---|---|---|---|---|
| Two materials on one surface | scene | 3,098 | silent | caught | semantic `sfnode-multiple`, core shape `one_material` |
| Two geometries in one Shape | scene | 2,522 | caught (XSD) | caught | XSD, `sfnode-multiple`, `one_geometry` |
| Longitude written first (Angkor) | scene | 0 | silent | caught | `geo-coordinate-range` |
| Longitude written first (Giza) | scene | 0 | silent | **missed** | both numbers are legal; needs a second source |
| Shaft stretched by a scale | scene | 527 | silent | caught | twin shape S_H2s (drawn size vs record) |
| Shaft redrawn as a Cylinder | scene | 978 | silent | caught | S_H6 (nothing to compare) |
| A tunnel nobody recorded | scene | 1,206 | silent | caught | S_H4 (drawn, no record) |
| Depth recorded in feet | record | not drawn | silent | caught | S_H5 (unit) |
| A speculative claim loses its label | record | not drawn | silent | caught | S_H1s (tier) |
| The record points at nothing | record | not drawn | silent | caught | S_H3, S_H4, S_H6 |

Before: x3d_mcp `39c6e94`, 1 of 10. After: x3d_mcp `8205047` with the strict twin shapes, 9 of 10. The clean twin returns
0 findings on both. Engine: pyshacl 0.40.2, rdflib 7.6.0. Pixels: X_ITE 16.7.1, headless Chromium 157, SwiftShader,
640 by 400, best of two views, of 256,000; rendering the clean twin twice differs by 0.

## Downstream

The seven scene faults were converted and handed to each format's own validator.

| | glTF | USD |
|---|---|---|
| Converter | loom-gltf x3dsem 0.1.0 | the demo's own `x3d_usd.py`, usd-core 26.11 |
| Validator | Khronos glTF-Validator 2.0.0-dev.3.10 | pxr.UsdValidation, 30 validators |
| Faulty files flagged | 0 of 7 | 0 of 7 |
| Faults erased (output identical to the clean file) | 4 of 7 | 3 of 7 |

Check at the source. After conversion a fault is either gone without trace or present in a file its validator calls clean.

## How much meaning arrives

The clean twin carries 3 Metadata trees (6 nodes) on a WorldInfo, a Transform and a PhysicalMaterial.

| Format | Trees | Nodes | Note |
|---|---|---|---|
| glTF + KHR_xmp_json_ld (x3dsem 0.1.0) | 1 of 3 | 4 of 6 | only glTF nodes can host a packet; rules S1 and S2 fail out loud |
| USD customData (demo converter) | 3 of 3 | 6 of 6 | any prim can host |
| Blender 5.3.0, x3d-blender-io 1040830 | 0 of 3 | 0 of 6 | importer keeps Metadata on Shape hosts only; DEF names survive |
| Blender 5.3.0, x3d-blender-io f68adbd (PR #70), back to X3D 4.0 | 3 of 3 | 6 of 6 | fixed the same day: trees ride on the object, the material and the scene; XSD valid |
| the same, through Blender's glTF exporter | 3 of 3 | 6 of 6 | as plain extras, not JSON-LD packets |
| the same glb after the Loom extras lift (blender_extras 0.1.0, 22 Nov) | 3 of 3 | 6 of 6 | typed KHR_xmp_json_ld packets on node, material and scene; rules L0 to L6 pass against the source X3D; Khronos validator 0 errors; binary chunk byte-identical |
| the same, through Blender's USD exporter | 0 of 3 | 0 of 6 | the exporter skips nested custom properties |

## For researchers and developers

- Run `validate_semantic` and the core shapes on X3D before any export. They are the only stage that saw these faults.
- A render is not a witness for an invalid file: X_ITE draws the second of two materials, the converters keep the first.
- If a claim matters (a measurement, a tier, a unit), put it in a record and join it to the scene with shapes that can
  fail. Half of the faults here changed no pixel.
