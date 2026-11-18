# Hypergraph proof of concept: field notes (18 Nov 2026)

Demo: `docs/demos/hypergraph/v1/` in x3d.demo. A hyperedge (a relation among 3 or more concepts) is drawn as a hub Transform, spokes (IndexedLineSet) and a translucent Sphere; concepts are 4D points with w = difficulty tier, rotated in the XW, YW and ZW planes and projected to 3D. Full findings table: x3d.loom `LEARNINGS-hypergraph.md`.

Numbers (computed from the authored data, rig: headless Chromium, SwiftShader, X_ITE 16.6.0, X3D 4.0 XSD via x3d_mcp fa5dccf): 40 concepts, 15 hyperedges, 73 incidences, 138 distinct pairs after clique expansion (1.89 per incidence), 13.3 frames/s on software GL.

Three traps worth knowing: `Switch whichChoice` shows one child only (wrap in a Group); the Interchange profile has no Text; assigning a JS array to an MFVec3f through the SAI breaks, use `new X3D.MFVec3f(...)`.

The data is illustrative, not the DSA Tutor database.

## v2: Chess ECO A to E overlay (18 Nov 2026)

`docs/demos/hypergraph/v2/` in x3d.demo adds 48 ECO openings (boxes, w = volume A to E), 8 engine concepts and 21 more hyperedges (16 chess, 5 bridges to DSA) to the same 4D space, with a DSA / Chess / Both switch. Counts (data.json): 96 concepts, 36 hyperedges, 233 incidences, 550 distinct pairs after clique expansion. Rig: headless Chromium, SwiftShader, X_ITE 16.6.0, XSD via x3d_mcp fa5dccf; 3.9 frames/s on software GL. ECO ranges: major families cross-checked against a public list, minors from memory (Likely). Groupings and bridges are authored judgement. Details: x3d.loom `LEARNINGS-hypergraph-eco.md`.

## v3: the full ECO table, drawn with Babylon.js (18 Nov 2026)

`docs/demos/hypergraph/v3/` in x3d.demo uses all 500 ECO codes (3,865 named lines) from the Lichess chess-openings table (CC0, commit 3ba6b20). 99 hyperedges: 5 volumes, 27 families, 5 first-move groups, 40 transposition meeting points, the DSA and engine sets and 5 bridges. Correction to an earlier expectation: the table has no duplicate end positions; transpositions come from replaying every line (python-chess 1.10): 831 events, 148 positions joining 2 or more codes. Render: Babylon.js 9.37 (1.4 MB bundle with deep imports), with an XSD-valid X3D file (x3d_mcp fa5dccf) and an X_ITE view of the same data. Rig: headless Chromium on software GL, so no frame rates are claimed. Findings: x3d.loom `LEARNINGS-hypergraph-v3.md`.
