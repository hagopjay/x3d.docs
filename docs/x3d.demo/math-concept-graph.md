# Math Lab concept graph (OntoMathPro, OpenMath, MathML, PhySH)

Demo folder `docs/demos/math-concept-graph/v1/` in x3d.demo. Lessons table: x3d.loom `LEARNINGS-math-ontology.md`.

**What it shows.** The 18 Math Lab lessons linked to ontology terms, 69 graded claims (33 Confirmed, 29 Likely, 7 Suspected) plus 27 Confirmed gaps, as an X3D scene with a `MetadataSet` per claim and as JSON-LD.

| Check | Result | Instrument |
|---|---|---|
| Scene valid | 0 errors | x3d_mcp `fa5dccf` `validate_xml`, XSD 4.0 |
| Semantic check | 0 errors after adding containerField="metadata" | x3d_mcp `fa5dccf` |
| Cited terms live | 67 of 67 | scout.py, 18 Nov 2026 |
| Page loads, toggles work, no console errors | yes | headless Chromium, software GL, X_ITE 16.6.0; not timed |

**Three things to remember.** OntoMathPro has no RDF endpoint (HTML listing only, 737 of 3450 labels Russian-only). OpenMath has no probability or statistics CD beyond s_dist1. PhySH is CC0 with a JSON API but is too coarse for classical lessons.
