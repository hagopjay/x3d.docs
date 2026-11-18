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

## v2 (same day)
Folder `docs/demos/math-concept-graph/v2/`. Re-run against a full private crawl: 90 links (40 Confirmed, 39 Likely, 11 Suspected), 88 terms, 26 Confirmed gaps, every lesson linked to OntoMathPro (14 with a Confirmed link, up from 11), OEIS and arXiv added, v1 errata listed. Valid by x3d_mcp `fa5dccf`; browser 0 errors in headless Chromium, SwiftShader, X_ITE 16.6.0. Rule learned: search every language label before declaring a gap. The raw crawl is quarantined and not published; a leak check found 0 matches.

## v3 (same day)
Folder `docs/demos/math-concept-graph/v3/`. Adds Wikidata (CC0) Q-ids for all 18 lessons (15 exact, 3 close) and a Russian-label check: of 50 cited OntoMathPro terms with a Russian label, Wikidata agrees on 19, hits only on 7, has nothing on 24; 4 Russian-only terms still need a human reader. Valid by x3d_mcp `fa5dccf`; 0 console errors, headless Chromium, SwiftShader, X_ITE 16.6.0.
