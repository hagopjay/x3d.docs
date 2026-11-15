# Appendix E. Drill index

Every drill has a task, a verify command and an answer key. Run the ones marked *not run* and send the result as a PR to the chapter.

<!-- BEGIN GENERATED -->
**145 drills**, 132 with a recorded run (`Checked`), 13 not yet run. Levels: L1 25, L2 77, L3 43.

| ID | Ch | Level | Drill | Checked |
|---|---|---|---|---|
| D-TH-1 | [01](01-the-tether.md) | L1 | Score five pipelines | not run |
| D-TH-2 | [01](01-the-tether.md) | L2 | Valid but blank | 2026-11-14, `x3d_mcp fork b4efcd3`; `X_ITE 16.7.0`, `Chromium 153 (Chrome for Testing 153.0.8010.12), SwiftShader`, 320 x 240 |
| D-TH-3 | [01](01-the-tether.md) | L2 | Read the hints, then break the loop | 2026-11-14, `x3d_mcp fork b4efcd3`, lxml 6.1.3, libxml2 2.14.6 |
| D-TH-4 | [01](01-the-tether.md) | L3 | Move the pin | 2026-11-14, `x3d_mcp fork 535fdac`, `ffbc20f`, `327c5c4`, `b4efcd3`; Python 3.13.18, lxml 6.1.3 |
| D-TH-5 | [01](01-the-tether.md) | L3 | Make the profile refuse a blank frame | 2026-11-14, `x3d.loom@162ab18` loomkit; `x3d_mcp fork b4efcd3`; `X_ITE 16.7.0`, `Chromium 153 ... SwiftShader` |
| D-TH-6 | [01](01-the-tether.md) | L3 | Forge the ledger | 2026-11-14, `chain.py` as printed in section 9, Python 3.13.18; the stamped scene also passed `x3d_mcp fork b4efcd3` (`valid True`) |
| D-TH-7 | [01](01-the-tether.md) | L2 | Detection against injected faults | 2026-11-14, `x3d_mcp fork b4efcd3`, lxml 6.1.3, libxml2 2.14.6 |
| D-LAW-1 | [02](02-loom-laws.md) | L1 | Which law and which failures came with PR #41 | 2026-11-14, `git` on `x3d.loom@162ab18` |
| D-LAW-2 | [02](02-loom-laws.md) | L2 | Re-derive the counts | 2026-11-14, `x3d.loom@162ab18`, Python 3.13.18 (the second line is run against this file as published) |
| D-LAW-3 | [02](02-loom-laws.md) | L2 | Run the kit's self-test | 2026-11-14, `x3d.loom@162ab18` loomkit, Python 3.13.18, normal and `-O` |
| D-LAW-4 | [02](02-loom-laws.md) | L3 | Weaken a gate and watch the suite fail | 2026-11-14, `x3d.loom@162ab18` loomkit in a scratch copy, Python 3.13.18 |
| D-LAW-5 | [02](02-loom-laws.md) | L2 | Let the physics witness judge the real records | 2026-11-14, `x3d.loom@162ab18` loomkit physics witness on `x3d.physics/runs`, Python 3.13.18 |
| D-LAW-6 | [02](02-loom-laws.md) | L3 | Find the profile that cannot accept a new run | 2026-11-14, `x3d.loom@162ab18` loomkit, `kit/profiles/x3d-static.json`, Python 3.13.18 |
| D-LAW-7 | [02](02-loom-laws.md) | L1 | Classify, then verify the catalogue | 2026-11-14, the K-table of this chapter, Python 3.13.18 (the script only; the classification is a judgement) |
| D-LAW-8 | [02](02-loom-laws.md) | L1 | Apply the checklist to a described project | not run |
| D-VAL-1 | [03](03-validator-and-gates.md) | L2 | Count the rules two ways | 2026-11-14 `x3d_mcp fork b4efcd3` and `x3d_mcp upstream 74da0ec`, Python `ast`. |
| D-VAL-2 | [03](03-validator-and-gates.md) | L2 | Walk a scene up the ladder | 2026-11-14 `x3d_mcp fork b4efcd3`, `X3D XSD 4.0` (0509fa5bd601); base column from `x3d_mcp upstream 74da0ec`. |
| D-VAL-3 | [03](03-validator-and-gates.md) | L2 | Same bytes, two schemas | 2026-11-14 `x3d_mcp fork b4efcd3`, `X3D XSD 4.0`, `X3D XSD 4.1`. |
| D-VAL-4 | [03](03-validator-and-gates.md) | L3 | Add a rule, then break it | 2026-11-14 scratch copy of `x3d_mcp@b4efcd3`, pytest 9.2.0. |
| D-VAL-5 | [03](03-validator-and-gates.md) | L3 | A gate that rejects, accepts and goes stale | 2026-11-14 loomkit `162ab18`, `x3d_mcp fork b4efcd3`. |
| D-VAL-6 | [03](03-validator-and-gates.md) | L1 | The conformance suite, without Blender | 2026-11-14 `x3d-blender-io@ab99988`, Python 3.13.18. |
| D-VAL-7 | [03](03-validator-and-gates.md) | L2 | What "not checkable" looks like | 2026-11-14 `x3d_mcp fork b4efcd3`, libxml2 2.14.6. |
| D-MCP-1 | [04](04-mcp-for-agents.md) | L2 | Count the surface three ways | 2026-11-14 `x3d_mcp fork b4efcd3`, `mcp` 1.30.0, Python `ast`. |
| D-MCP-2 | [04](04-mcp-for-agents.md) | L2 | Price a session before it starts | 2026-11-14 `x3d_mcp fork b4efcd3` and `x3d_mcp upstream 74da0ec`, `mcp` 1.30.0. |
| D-MCP-3 | [04](04-mcp-for-agents.md) | L2 | Edit a big scene twice, once by value and once by name | 2026-11-14 `x3d_mcp fork b4efcd3`, in-process calls, 4 vCPU Intel Xeon 2.30 GHz. |
| D-MCP-4 | [04](04-mcp-for-agents.md) | L3 | Trip each SPARQL guard | 2026-11-14 `x3d_mcp fork b4efcd3`, rdflib 7.6.0. |
| D-MCP-5 | [04](04-mcp-for-agents.md) | L2 | What does `path=` reach | 2026-11-14 `x3d_mcp fork b4efcd3`. |
| D-MCP-6 | [04](04-mcp-for-agents.md) | L3 | Forge a ledger | 2026-11-14 `x3d_mcp fork b4efcd3`. |
| D-MCP-7 | [04](04-mcp-for-agents.md) | L3 | Do it through a real client | not run (no MCP client or socket was used in this chapter). |
| D-SEM-1 | [05](05-semantic-layer.md) | L1 | Count the tool surface | 2026-11-14 `x3d_mcp fork b4efcd3` and `x3d_mcp fork 13121b6`, Python 3.13.18, in-memory `list_tools`. |
| D-SEM-2 | [05](05-semantic-layer.md) | L1 | Count the ontology | 2026-11-14 rdflib 7.6.0, `X3dOntology4.1.ttl` as bundled at `x3d_mcp fork b4efcd3`. |
| D-SEM-3 | [05](05-semantic-layer.md) | L2 | Strip the DOCTYPE | 2026-11-14 `x3d_mcp fork b4efcd3` converter, ontology 4.1 (an emulation, not a Saxon run). |
| D-SEM-4 | [05](05-semantic-layer.md) | L2 | One query, two ontologies | 2026-11-14 `x3d_mcp fork b4efcd3`, rdflib 7.6.0. |
| D-SEM-5 | [05](05-semantic-layer.md) | L3 | A part that floats | 2026-11-14 `x3d_mcp fork b4efcd3`, pyshacl 0.40.2. |
| D-SEM-6 | [05](05-semantic-layer.md) | L3 | Break it with reasoning | 2026-11-14 `x3d_mcp fork b4efcd3`, pyshacl 0.40.2, owlrl 7.6.2, 35.6 s. |
| D-SEM-7 | [05](05-semantic-layer.md) | L2 | Set semantics and a silent ignore | 2026-11-14 pyshacl 0.40.2, rdflib 7.6.0. |
| D-SEM-8 | [05](05-semantic-layer.md) | L2 | What RDF forgets | 2026-11-14 `x3d_mcp fork b4efcd3`, rdflib 7.6.0, pyshacl 0.40.2. |
| D-XIT-1 | [06](06-xite-the-oracle.md) | L2 | Count the coverage three ways | 2026-11-14 `X_ITE 16.7.0` (static scan) and `X_ITE 16.4.3`, `16.5.1`, `16.6.1`, `16.7.0`, `16.7.1` (`createNode`), `X3DUOM 4.1`, Chromium 153, SwiftShader |
| D-XIT-2 | [06](06-xite-the-oracle.md) | L2 | Catch the sampler that lies | 2026-11-14 `X_ITE 16.4.3`, `16.5.1`, `16.6.1`, `16.7.0`, `16.7.1`, Chromium 153, SwiftShader, 320 x 240 |
| D-XIT-3 | [06](06-xite-the-oracle.md) | L3 | Reproduce the hosted-page black draw and fix it | 2026-11-14 `X_ITE 16.5.1`, `16.7.0`, Chromium 153, SwiftShader, emulated policy above (the real host's policy was not available) |
| D-XIT-4 | [06](06-xite-the-oracle.md) | L2 | Break picking with a faint shape, then fix it | 2026-11-14 `X_ITE 16.4.3`, `16.5.1`, `16.7.0`; `x3d_mcp fork b4efcd3`; Chromium 153, SwiftShader |
| D-XIT-5 | [06](06-xite-the-oracle.md) | L2 | Five scenes the renderer accepts and the validator does not | 2026-11-14 `X_ITE 16.7.0`, `x3d_mcp fork b4efcd3`, `X3D XSD 4.0` and `4.1`, lxml 6.1.3, Chromium 153, SwiftShader |
| D-XIT-6 | [06](06-xite-the-oracle.md) | L3 | Freeze a route with one exception | 2026-11-14 `X_ITE 16.5.1`, `16.7.0`, `16.7.1`, Chromium 153, SwiftShader |
| D-XIT-7 | [06](06-xite-the-oracle.md) | L2 | Re-derive H7, the locus of behaviour | 2026-11-14 marker scan of `x_ite@16.7.0`, `16.6.1`, `16.7.1` (module counts 752, 752, 762), Python 3.13.18 |
| D-XIT-8 | [06](06-xite-the-oracle.md) | L1 | Count the patches a repository ships | 2026-11-14 `x3d.demo@d10b457`, shell |
| D-XRY-1 | [07](07-xray.md) | L2 | Recompute the noise calibration | 2026-11-14 `x3d.xray@8fa6845`, Python 3.13.18 |
| D-XRY-2 | [07](07-xray.md) | L1 | The price of looking, by hand and by code | 2026-11-14 `x3d.xray@8fa6845`, Python 3.13.18 |
| D-XRY-3 | [07](07-xray.md) | L2 | Pin the generator and the add-one limit | 2026-11-14 `x3d.xray@8fa6845`, Python 3.13.18 |
| D-XRY-4 | [07](07-xray.md) | L2 | Run the method on a thin public repository | 2026-11-14 `x3d.xray@8fa6845`, `x3d.castle@d70e00c`, Git 2.43.0 |
| D-XRY-5 | [07](07-xray.md) | L3 | Reproduce the containerField defect and see which rung catches it | 2026-11-14 `x3d_mcp fork b4efcd3`, `X3D XSD 4.0`, lxml 6.1.3, `x3d.xray@8fa6845` |
| D-XRY-6 | [07](07-xray.md) | L3 | Make the producer and the reader agree on a bug | 2026-11-14 `x3d.xray@8fa6845` (scratch copy), Python 3.13.18 |
| D-XRY-7 | [07](07-xray.md) | L2 | Run the synthetic pipeline and read the gate verdicts | 2026-11-14 `x3d.xray@8fa6845`, `X_ITE 16.7.0` dist, Python 3.13.18 |
| D-XRY-8 | [07](07-xray.md) | L1 | Classify five looks by the grade function | not run (read at `x3d.xray@8fa6845:x3dray/looks.py` lines 309 to 349) |
| D-BAB-1 | [08](08-babylon-bridge.md) | L2 | Recount the bridge's coverage | 2026-11-14 `x3d.loom@162ab18`, Node 22.23.4, Python 3 |
| D-BAB-2 | [08](08-babylon-bridge.md) | L2 | Re-derive the primer's 68 | 2026-11-14 `x3d.loom@162ab18` and `60824ce`, Node 22.23.4 |
| D-BAB-3 | [08](08-babylon-bridge.md) | L3 | Break a shader key, then predict which half moves | 2026-11-14 `x3d.loom@162ab18`, Python 3 with lxml, scratch copies of the scene |
| D-BAB-4 | [08](08-babylon-bridge.md) | L2 | Move a PSNR by changing its window | 2026-11-14 numpy 2.5.3, Pillow 12.3.0, `x3d.loom@162ab18` |
| D-BAB-5 | [08](08-babylon-bridge.md) | L3 | Census a corpus before you promise a port | 2026-11-14 lxml, `x3d.demo@d10b457`, `x3d.loom@162ab18` |
| D-BAB-9 | [08](08-babylon-bridge.md) | L1 | Opacity of a stack of slices | 2026-11-14 python3 -I |
| D-BAB-6 | [08](08-babylon-bridge.md) | L2 | Check the weights: radius 1.00, not 1.24 | 2026-11-14 Node, `x3d.loom@4887a98` |
| D-BAB-7 | [08](08-babylon-bridge.md) | L2 | Re-run one NURBS node against X_ITE | 2026-11-14 `x3d.loom@4887a98`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, Babylon 9.32.0 |
| D-BAB-8 | [08](08-babylon-bridge.md) | L3 | Predict a set's triangle counts | 2026-11-14 `x3d.loom@4887a98`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, Babylon 9.32.0 |
| D-BAB-10 | [08](08-babylon-bridge.md) | L2 | Break the first-Viewpoint rule and read the picture | 2026-11-14 `x3d.loom@108a282`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-11 | [08](08-babylon-bridge.md) | L2 | Swap the ElevationGrid diagonal and predict the number | 2026-11-14 `x3d.loom@38530ab`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-12 | [08](08-babylon-bridge.md) | L2 | Midpoint of latitude 0 to latitude 60 | 2026-11-15 python3 -I |
| D-BAB-13 | [08](08-babylon-bridge.md) | L3 | Why a block of 204 draws 70 | 2026-11-15 python3 -I (70.35); the rig gives 70 in both engines |
| D-BAB-70 | [08](08-babylon-bridge.md) | L2 | Make FASTEST mean nearest and predict which box moves | 2026-11-15 `x3d.loom@72a4bca`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-71 | [08](08-babylon-bridge.md) | L3 | Stop the ground at its last groundAngle | 2026-11-15 `x3d.loom@72a4bca`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-72 | [08](08-babylon-bridge.md) | L2 | Leave the `#version` line in a ComposedShader | 2026-11-15 `x3d.loom@1192dd4`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-73 | [08](08-babylon-bridge.md) | L3 | Transpose the matrix of a GeoLocation | 2026-11-15 `x3d.loom@1192dd4`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-74 | [08](08-babylon-bridge.md) | L2 | How much of a patch does a ring keep | 2026-11-15 python3 -I (0.4487) |
| D-BAB-75 | [08](08-babylon-bridge.md) | L2 | Keep the Background on every pass | 2026-11-15 `x3d.loom@c9b7695`, `X_ITE 16.6.0`, Chromium 153.0.8010.12 SwiftShader, three.js r187 |
| D-BAB-76 | [08](08-babylon-bridge.md) | L2 | What the skin of one vertex becomes | 2026-11-15 python3 -I ((0.5, 0.5, 0.0)) |
| D-BAB-77 | [08](08-babylon-bridge.md) | L1 | How many heights make 125,000 triangles | 2026-11-15 python3 -I (251) |
| D-CAS-1 | [09](09-castle-engine.md) | L2 | Count the parse-only nodes and name the denominator | 2026-11-14 `castle-engine@48ce617`, Python 3.13.18 |
| D-CAS-2 | [09](09-castle-engine.md) | L2 | Count loaders and savers without trusting a number | 2026-11-14 `castle-engine@48ce617`, Python 3.13.18 |
| D-CAS-3 | [09](09-castle-engine.md) | L2 | Re-derive the headline FLIP and what it hides | 2026-11-14 `x3d.castle@d70e00c` receipt, Python 3.13.18 |
| D-CAS-4 | [09](09-castle-engine.md) | L2 | Validate two exporter glbs | 2026-11-14 `Khronos glTF-Validator 2.0.0-dev.3.10`, Node 22.23.4 |
| D-CAS-5 | [09](09-castle-engine.md) | L3 | Break the spot-cone rule | 2026-11-14 `Khronos glTF-Validator 2.0.0-dev.3.10`, Python 3.13.18 |
| D-CAS-6 | [09](09-castle-engine.md) | L3 | A valid scene the validator cannot warn about | 2026-11-14 `x3d_mcp fork b4efcd3` (validator half only) |
| D-CAS-7 | [09](09-castle-engine.md) | L3 | Design the TimeSensor origin fixture | not run |
| D-CAS-8 | [09](09-castle-engine.md) | L1 | Attenuation at 3 m and at 0.5 m | 2026-11-14 Python 3.13.18 (arithmetic on the formula read at `castle-engine@48ce617`) |
| D-BLE-1 | [10](10-blender-pipeline.md) | L2 | Which version does an exported file claim? | 2026-11-14 `bpy 5.3.0`, `x3d-blender-io@ab99988`. |
| D-BLE-2 | [10](10-blender-pipeline.md) | L3 | Reproduce the colour trap | 2026-11-14 `x3d_mcp fork b4efcd3`, `bpy 5.3.0`. |
| D-BLE-3 | [10](10-blender-pipeline.md) | L2 | Count the tests two ways | 2026-11-14 `bpy 5.3.0`, `gltf-validator 2.0.0-dev.3.10`. |
| D-BLE-4 | [10](10-blender-pipeline.md) | L3 | A matching centre, a failing scene | 2026-11-14 `X_ITE 16.7.1`, `Babylon.js 9.32.0`, Chrome for Testing 153.0.8010.12 SwiftShader, `bpy 5.3.0`. |
| D-BLE-5 | [10](10-blender-pipeline.md) | L2 | Is a re-export evidence of a good importer? | 2026-11-14 `x3d_mcp fork b4efcd3`, `bpy 5.3.0`. |
| D-BLE-6 | [10](10-blender-pipeline.md) | L2 | Splat bytes, from the writer | 2026-11-14 `x3d-blender-io@ab99988`, Python 3.13.18. |
| D-BLE-7 | [10](10-blender-pipeline.md) | L3 | Can Blender 5.3 export a splat? | 2026-11-14 `bpy 5.3.0` (PLY export and operator list ran; the 4.1 export is covered by the test pass, not re-run here). |
| D-BLE-8 | [10](10-blender-pipeline.md) | L1 | Grade a Survey claim | not run |
| D-BLE-9 | [10](10-blender-pipeline.md) | L3 | A toy bake, gated | 2026-11-14 `bpy 5.3.0`, `x3d_mcp fork b4efcd3`. |
| D-GLT-1 | [11](11-gltf-usd-khronos.md) | L2 | Build a glb that passes and is empty | 2026-11-14 `Khronos glTF-Validator 2.0.0-dev.3.10` (the empty glb only; the one-node variant was not run). |
| D-GLT-2 | [11](11-gltf-usd-khronos.md) | L2 | Make a required extension pass | 2026-11-14 `Khronos glTF-Validator 2.0.0-dev.3.10`. |
| D-GLT-3 | [11](11-gltf-usd-khronos.md) | L1 | Count the ratified extensions | 2026-11-14 registry file sha256 prefix `32868b162d85` (counted by line range 12 to 38; the awk form above was not run verbatim). |
| D-GLT-4 | [11](11-gltf-usd-khronos.md) | L2 | Instancing leaves the triangle count alone | 2026-11-14 `Khronos glTF-Validator 2.0.0-dev.3.10` on carried project files (a reader without the files can use `tests/test_import_gpu_instances_bpy.py` in the repo instead). |
| D-GLT-5 | [11](11-gltf-usd-khronos.md) | L3 | Find the loss in a glb | 2026-11-14 Python `json` on the carried glb (the failing-run extension was not written). |
| D-GLT-6 | [11](11-gltf-usd-khronos.md) | L3 | Find the animation start fault without Blender | not run (no animated glb with the fault was produced here). |
| D-UNR-1 | [12](12-unreal-tier1.md) | L2 | Derive and check the axis swap | 2026-11-14 Python 3 (the converters' own `ue_rot`, `mm`, `axis_angle`). |
| D-UNR-2 | [12](12-unreal-tier1.md) | L1 | Convert a field of view | 2026-11-14 Python 3. |
| D-UNR-3 | [12](12-unreal-tier1.md) | L2 | Catch the winding flip | 2026-11-14 Python 3 with numpy. |
| D-UNR-4 | [12](12-unreal-tier1.md) | L1 | Instancing arithmetic | 2026-11-14 grep on `x3d-blender-io@ab99988` and Python 3. |
| D-UNR-5 | [12](12-unreal-tier1.md) | L3 | Break a PSNR comparison | 2026-11-14 numpy for all three numbers (offset 38.63 dB, noise 34.31 dB, square 22.71 dB). |
| D-UNR-6 | [12](12-unreal-tier1.md) | L3 | Write the pass and fail line for a gate | not run (no Unreal here). |
| D-UNR-7 | [12](12-unreal-tier1.md) | L2 | Pick an exposure from a bracket | 2026-11-15 pytest 9 on the PR #29 branch (11 new tests pass). |
| D-UNR-8 | [12](12-unreal-tier1.md) | L2 | Count what Interchange kept | 2026-11-15 UE 5.8.4 Interchange on RTX PRO 6000 (one run). |
| D-PHY-1 | [13](13-physics.md) | L2 | Symplectic against explicit Euler on a pendulum | `2026-11-14 python3 -I numpy 2.5.3`: explicit 10.8933 and 11.0130, symplectic 0.0002 and 0.0150. |
| D-PHY-2 | [13](13-physics.md) | L2 | The exact reference for a stepped scheme | `2026-11-14 python3 -I numpy 2.5.3`: sim 5.074562500, discrete 5.074562500, continuum 5.095000000, gap -0.020437. |
| D-PHY-3 | [13](13-physics.md) | L2 | XPBD bead on a wire: substeps against residual and energy | `2026-11-14 python3 -I numpy 2.5.3`: 7.31e-03, 3.19e-04, 2.03e-05, 8.16e-07; dE -8.7945, -4.3632, -1.4550, -0.3125. |
| D-PHY-4 | [13](13-physics.md) | L3 | A check that cannot fail: the wrong twin | `2026-11-14 python3 -I numpy 2.5.3`: KE 0.500000 three times; v at t = 1.0 s fixed [0,0] and [1,0]; buggy [1,0] and [0,0]; none [1,0] and [0,0]. The oblique extension was not run. |
| D-PHY-5 | [13](13-physics.md) | L2 | Order of a method depends on where you measure | `2026-11-14 python3 -I numpy 2.5.3`: T=1 explicit 1.00, symplectic 1.00; T=2pi explicit 1.06, symplectic 2.00. |
| D-PHY-6 | [13](13-physics.md) | L3 | The CFL limit is a stability limit, not "outrunning a cell" | `2026-11-14 python3 -I numpy 2.5.3`: 0.6 -> 2.69e-03; 0.70 -> 3.42e-03; 0.7071 -> 4.65e-03; 0.72 -> 1.18e+59; 0.80 -> 4.40e+170. Bisection not run. |
| D-PHY-7 | [13](13-physics.md) | L2 | Fixed against variable step | `2026-11-14 python3 -I numpy 2.5.3`: jitter 0 dE/E0 0.0002 theta 0.007586 twice; jitter 0.5 dE/E0 -0.0117, theta 0.159239 and 0.435642. |
| D-PHY-8 | [13](13-physics.md) | L2 | Re-judge the PhysX run records and attack them | `2026-11-14 x3d.loom@162ab18 kit/loom physics`: status pass; `physx_controls.py`: "14 controls on the real record, 14 caught with the intended code"; `test_gates.py`: 82 controls, optimized False and True. This verifies the records replay in the **recorded** hosts (it reads the hashes; it does not run PhysX again). |
| D-PHY-9 | [13](13-physics.md) | L1 | Count the MuJoCo threat checks yourself | `2026-11-14 x3d.loom@162ab18`: Counter({('defended','pass'): 16, ('gap','pass'): 3}). |
| D-PHY-10 | [13](13-physics.md) | L1 | The ports are baked, not simulated by X3D | `2026-11-14 x3d.demo@d10b457 grep`: 17; 0; 200. |
| D-PHY-11 | [13](13-physics.md) | L2 | Find the four X_ITE contact rules in the source | 2026-11-14 `grep` over X_ITE 16.7.0 (read, behaviour not run) |
| D-MET-1 | [14](14-methods.md) | L1 | Count the base | 2026-11-14 `build_learn.py` at this commit. |
| D-MET-2 | [14](14-methods.md) | L2 | Grade mix | 2026-11-14 `learn_lib.py` count, Python 3.13. |
| D-MET-3 | [14](14-methods.md) | L3 | Break the linter | 2026-11-14 `check_learn.py` at this commit. |
| D-MET-4 | [14](14-methods.md) | L2 | Pin audit | not run. |
| D-MET-5 | [14](14-methods.md) | L3 | Teach-back | not run. |
| D-ANM-1 | [15](15-animation-timelines.md) | L2 | Red to blue at half time | `2026-11-15 X_ITE 16.6.0, Chromium 153.0.8010.12 SwiftShader`: [0.9999999999999991, 0, 1] |
| D-ANM-2 | [15](15-animation-timelines.md) | L2 | What a tolerance buys | `2026-11-15 gsap 3.15.1, Node 22.23.4` |
| D-ANM-3 | [15](15-animation-timelines.md) | L1 | Which Theatre package may be in a shipped page | `2026-11-15 npm registry, 0.7.2` |
| D-ANM-4 | [15](15-animation-timelines.md) | L2 | Run the whole rig | `2026-11-15 X_ITE 16.6.0, three.js r187, Chromium 153.0.8010.12 SwiftShader` |
| D-ANM-5 | [15](15-animation-timelines.md) | L3 | Break the HSV rule | not run again after the first run that found it; the 0.059 figure is from that run. |
| D-ANM-6 | [15](15-animation-timelines.md) | L2 | Euler convention | `2026-11-15 Node 22.23.4` |
| D-ANM-7 | [15](15-animation-timelines.md) | L2 | Count the keys of the orrery | `2026-11-15 X_ITE 16.6.0, three.js r187, Chromium 153.0.8010.12 SwiftShader` |
| D-YJS-1 | [15](15-yjs-collaboration.md) | L1 | Run the suite | 2026-11-15 Node v22.23.4, Yjs 13.6.33, pycrdt 0.14.13 |
| D-YJS-2 | [15](15-yjs-collaboration.md) | L3 | Break the export | 2026-11-15 Node v22.23.4, Yjs 13.6.33 |
| D-YJS-3 | [15](15-yjs-collaboration.md) | L2 | Two browsers | 2026-11-15 Chromium 153.0.8010.12 SwiftShader, X_ITE 16.6.0 |
| D-YJS-4 | [15](15-yjs-collaboration.md) | L2 | Price a structural edit | 2026-11-15 Node v22.23.4, Intel Xeon 2.10 GHz x4 |
| D-YJS-5 | [15](15-yjs-collaboration.md) | L1 | Predict the winner | 2026-11-15 `x3d.loom@a9640eb` tests |
| D-ZOD-1 | [16](16-typed-x3d-zod.md) | L1 | Run the suite | 2026-11-15 Node v22.23.4, zod 4.6.7, ajv 8.20.0 |
| D-ZOD-2 | [16](16-typed-x3d-zod.md) | L2 | Regenerate and compare | 2026-11-15 Node v22.23.4, schema sha1 `c6765a4` |
| D-ZOD-3 | [16](16-typed-x3d-zod.md) | L3 | Put the tuple bug back | 2026-11-15 Node v22.23.4, zod 4.6.7, ajv 8.20.0 |
| D-ZOD-4 | [16](16-typed-x3d-zod.md) | L2 | The upstream file has the NavigationInfo bug | 2026-11-15 ajv 8.20.0, zod 4.6.7, schema sha1 `c6765a4` |
| D-ZOD-5 | [16](16-typed-x3d-zod.md) | L2 | Size a vocabulary | 2026-11-15 Node v22.23.4 and Python 3.13, schema sha1 `c6765a4` |
| D-ZOD-6 | [16](16-typed-x3d-zod.md) | L3 | Find the stack limit | 2026-11-15 Node v22.23.4, zod 4.6.7 |
| D-PTR-1 | [18](18-three-pathtracer.md) | L1 | The vertical angle that Cycles drew | `2026-11-15 python3 -I numpy 2.5.4` |
| D-PTR-2 | [18](18-three-pathtracer.md) | L2 | Apply the bound | `2026-11-15 python3 -I` |
| D-PTR-3 | [18](18-three-pathtracer.md) | L2 | Re-score a strip | `2026-11-15 python3 -I flip-evaluator 1.7` |
| D-PTR-4 | [18](18-three-pathtracer.md) | L2 | Find what overwrites X_ITE | `2026-11-15 grep, headless Chromium 153` |
| D-PTR-5 | [18](18-three-pathtracer.md) | L3 | Break a light conversion | `not run` |
| D-PTR-6 | [18](18-three-pathtracer.md) | L3 | Isolate the e1 gap | `not run` |
<!-- END GENERATED -->
