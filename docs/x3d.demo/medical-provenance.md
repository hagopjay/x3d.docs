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

## v2 (x3d.demo, folder `medical-provenance/v2/`)

| Finding | Grade | Instrument |
|---|---|---|
| FMA is-a ancestors for 120 shapes; 108 non-generic classes; class filter selects e.g. all 24 ribs | C | EBI OLS4 hierarchicalAncestors |
| Page reads each MetadataSet back from the running scene and compares with the claim file: 111 of 111 agree; one edited grade caught (110 of 111) | C | headless Chromium, X_ITE 16.6.0; self-consistency, not a signature |
| 1033 claims (C 671, L 284, S 78); both scenes valid, 0 errors | C | x3d_mcp `fa5dccf` `validate_xml` |

Next: sign or hash the claim file into the scene, HAnimHumanoid on the 37 mapped bones, BodyParts3D meshes, VolumeData from open DICOM.

## v3 (`medical-provenance/v3/`): claims hashed into the scene

Per-shape SHA-256 of the canonical claim list in each MetadataSet, plus one root (`b3a6e1ac3b237154...`) in the scene head. The page recomputes all of them with WebCrypto from `claims.json`: 111 of 111 match, a changed claim text is caught (110 of 111, root differs). `verify.py` repeats it offline for both scenes (torso 111/111, brain 10/10). Both scenes valid, 0 errors (x3d_mcp `fa5dccf`). Headless Chromium, software GL, X_ITE 16.6.0. A hash is not a signature: hold the root outside the folder and add a keyed signature when the owner sets a key policy.

## v4 (`medical-provenance/v4/`): a jointed H-Anim skeleton

A real `HAnimHumanoid` built from the CT bones: 35 joints, 35 segments (34 bones plus a pelvis), FMA id and claim digest on each segment, posable in the page. Valid, 0 errors (x3d_mcp `fa5dccf`); all 35 joint and 35 segment names in the XSD enumerations; forward-kinematics error 0.000000 m. Joint centres are estimated from the meshes (grade S). Ribs, sternum and cartilage have no H-Anim segment and are drawn outside it. CT scene (+X patient-right, +Z posterior) needs a 180 degree turn about Y for H-Anim. Headless Chromium, software GL, X_ITE 16.6.0; other H-Anim players not tested.

## v5 (`medical-provenance/v5/`): open BodyParts3D meshes vs the CT surfaces

100 of 110 torso shapes with an FMA class are paired by FMA id with the open BodyParts3D mesh (998 element files), fitted into the CT frame (scale 0.9397, rotation 10.6 degrees, similarity fit, 67 structures) and compared by mean surface distance: 27 close (under 15 mm), 56 partial, 17 far; spine median 10.8 mm. The 17 far ones are posture and extent differences, not bad meshes. Both scenes valid, 0 errors (x3d_mcp `fa5dccf`); headless Chromium, software GL, X_ITE 16.6.0. **Licence flag:** BodyParts3D headers say CC BY-SA 2.1 Japan, the current page says CC BY 4.0; the derived mesh file is shipped under the stricter reading with a notice, for the owner to confirm. Next: an articulated fit with the v4 joints.

## v6 (`medical-provenance/v6/`): an open DICOM CT as X3D VolumeData

One TCIA Pancreas-CT series (185 slices, CC BY 3.0 read from the archive API, pixel-data SHA-256 recorded) resampled to a 128 x 92 x 128 volume (2.8 x 2.0 x 2.8 mm voxels, about 536 KB gzip) and shown as `VolumeData` and `SegmentedVolumeData` (ImageTexture3D NRRD). One MetadataSet on the Transform carries series UID, DOI, licence, processing and file hashes; the page decodes the same arrays for an axial slice scrubber and verifies them with WebCrypto. Both scenes valid, 0 errors (x3d_mcp `fa5dccf`); page 0 console errors, no overflow at 1280 and 390 px (headless Chromium, software GL). Ten claims: 5 C, 2 L, 3 S.

Honest limits: the segment ids are HU bands, not organs, and their FMA terms are judgements (grade S); not registered to the v3 torso or BodyParts3D; the transfer-function texture cannot pass the XSD, so colour-by-density is not used; GPU browsers not tested; the segmented scene draws slowly in software GL. Lessons MP-23 to MP-27 in x3d.loom `LEARNINGS-medical-provenance.md`. Data notice: `NOTICE-TCIA.md`.

## v7 (`medical-provenance/v7/`): an open pancreas label as an FMA-linked segment

The v6 CT series plus the NIH pancreas label of the same series (TCIA, 1 MB zip) as segment 5 of a `SegmentedVolumeData`, carrying FMA:7198 Pancreas, the label zip hash, the annotator statement and the axis fix in its MetadataSet. The label's header cannot be trusted for alignment, so all 8 axis flips were tested against the CT: only the slice flip lands on uniform soft tissue (105 +/- 20 HU, next best 41). 87.1 mL over 84 slices at full resolution, 88.6 mL on the shipped grid. Scene valid, 0 errors (x3d_mcp `fa5dccf`); page 0 console errors, no overflow at 1280 and 390 px (headless Chromium, software GL). Nine claims: 4 C, 3 L, 2 S.

Limits: one patient, one annotator; label licence not stated apart from the collection (CC BY 3.0, flagged); not registered to the v3 torso or BodyParts3D; GPU browsers not tested. Lessons MP-28 to MP-30 in x3d.loom.
