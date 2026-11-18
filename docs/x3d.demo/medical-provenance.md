# Medical provenance atlas (FMA, SNOMED CT ids, H-Anim on the torso)

Demo folder `docs/demos/medical-provenance/v1/` in x3d.demo. Educational proof of concept, not medical advice. Lesson table: x3d.loom `LEARNINGS-medical-provenance.md`.

**What it shows.** The existing CT torso and template brain, with each organ Shape carrying a `MetadataSet` of FMA class, Uberon, Wikidata, SNOMED CT id, MeSH, H-Anim segment, BodyParts3D id and a C/L/S grade. 913 claims also export as JSON-LD.

| Check | Result | Instrument |
|---|---|---|
| Structures with an FMA class | 120 of 121 | FMA 5.1.0 via EBI OLS4, 117 of 117 labels resolved |
| SNOMED CT ids / H-Anim names / open meshes | 78 / 37 / 112 | Uberon SCTID xref; x3d_mcp XSD 4.1 (146 names); BodyParts3D lists |
| Claims by grade | C 551, L 284, S 78 | `claims.json` |
| Scenes valid | torso and brain, 0 errors | x3d_mcp `fa5dccf` `validate_xml` |
| Page | 0 console errors, no overflow at 1280 and 390 px | headless Chromium, software GL, X_ITE 16.6.0 |

**Remember.** An FMA label hit proves the class exists, not that the mesh is that structure. Left/right bones lose their SNOMED ids in the chain. H-Anim has no ribs or organs. BodyParts3D's two licence texts disagree. Not done: VolumeData, DICOM, HAnimHumanoid, BodyParts3D meshes.
