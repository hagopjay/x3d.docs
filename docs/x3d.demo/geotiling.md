# Geotiling (Burruss Hall to Earth, GeoLOD quadtree, 3D Tiles bridge)

Demo folder `docs/demos/geotiling/v1/` in x3d.demo (candidate Demo 47). Full lesson table: x3d.loom `LEARNINGS-geotiling.md`.

**What it shows.** The data of the earlier "Drillfield to the Stars" zoom rebuilt as a real tile pyramid: 132 `GeoElevationGrid` tiles (z7 to z15) nested by `GeoLOD`, a globe, `GeoLocation` beacons, six `GeoViewpoint`s, a 90 s zoom-out tour by `GeoPositionInterpolator`, the Drillfield 0.25 m DSM behind a 2.5 km `GeoLOD`, the same pyramid as a 3D Tiles 1.1 tileset with GLB content, and a converter that turns a tileset back into X3D `GeoLOD`. Satellite imagery is Google data, academic non-commercial PoC only; `--open-textures` rebuilds without it.

| Check | Result | Instrument |
|---|---|---|
| X3D files valid | 266 native + 177 converted, 0 invalid | x3d_mcp `fa5dccf` `validate_xml`, XSD 4.0 |
| Streaming | z7 to z14 around Blacksburg in about 25 s at 4.5 km; 0.5 fps with the Drillfield in view | X_ITE 16.6.0, headless Chromium, SwiftShader (no GPU) |
| Converter | native and converted trees fetch the same tiles per level | same run |

**Three things to remember.** Nest GeoLOD by file (`rootUrl`, `child1..4Url`): inline `rootNode` children need a `GeoOrigin` in the bundled XSD. 3D Tiles child transforms are parent-relative. GD heights are ellipsoidal, so add the geoid offset (-32.6 m at Blacksburg) to ASL heights, cameras included.

**Open.** No skirts (hairline cracks). No GPU timing. No Google photoreal GLB bodies exist to test the converter on. The "$50 of Google fees" is not visible in any log opened.
