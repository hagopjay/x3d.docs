# Heritage + geospatial Loom (Giza provenance twin, Burruss placement)

Demo folder `docs/demos/heritage-geo/v1/` in x3d.demo (PR #61, candidate Demo 46). Full lesson table: x3d.loom `LEARNINGS-heritage-geo.md`.

**What it shows.** Four Giza monuments placed with X3D `GeoLocation`; every statement about them is a CIDOC-CRM E13 Attribute Assignment carried as a `MetadataSet`, graded Confirmed, Likely or Suspected, and also exported as JSON-LD. A second tab places the Drillfield and Burruss Hall (reused Google Solar API data, academic non-commercial PoC only).

| Check | Result | Instrument |
|---|---|---|
| Giza and Burruss scenes valid | 0 errors | x3d_mcp `fa5dccf` `validate_xml`, XSD 4.0 |
| Both tabs render, no page errors | yes | headless Chromium, software GL, X_ITE 16.6.0; not timed |
| Open-data rows | 11, graded | live calls from a build container, 18 Nov 2026 |

**Three things to remember.** `metadata` must come first inside a Transform or GeoLocation in the 4.0 XSD. GD is lat, lon; WKT and GeoJSON are lon, lat. GeoLocation needs no extra rotation for Y-up content.

**Open.** USGS EPQS says 627.175 m at the Burruss point; the Drillfield reference is 617 m. No Egyptian DEM, no IFC placement, no GeoSPARQL endpoint yet.
