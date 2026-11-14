# Appendix B. Glossary

Two parts: the X3D framework and the tools around it, then the vocabulary of the method (the Loom). Chapter pointers say where the term does work.
Definitions are working definitions for this base; the standard's own text wins wherever they differ.

## Part 1. X3D and its neighbours

| term | working definition | where |
|---|---|---|
| **X3D** | the ISO/IEC 19775 family: a scene graph, an event model and several encodings for interactive 3D. This base targets 4.0 and notes 4.1 additions | [01](01-the-tether.md) |
| **encodings** | XML (`.x3d`), ClassicVRML (`.x3dv`), JSON (`.x3dj`), compressed binary (`.x3db`); the validator in this base reads the XML encoding | [03](03-validator-and-gates.md) |
| **profile** | a named bundle of components and levels a file declares it needs (Core, Interchange, Interactive, Immersive, Full, CADInterchange, MPEG-4). "Valid" is relative to the declared profile | [03](03-validator-and-gates.md) |
| **component, level** | a group of related nodes (Core, Grouping, Shape, Lighting, Texturing, ...) and the support level inside it | [03](03-validator-and-gates.md), [06](06-xite-the-oracle.md) |
| **node, field** | a typed object in the scene graph and one of its typed slots. Field types are single (`SFFloat`) or multiple (`MFVec3f`) | [03](03-validator-and-gates.md) |
| **access type** | `initializeOnly`, `inputOnly`, `outputOnly`, `inputOutput`: which fields may be set at load, received, emitted or both. A ROUTE must respect them | [03](03-validator-and-gates.md) |
| **DEF / USE** | name a node once, reuse it by reference. USE-before-DEF and name clashes are classic scene faults | [03](03-validator-and-gates.md), [05](05-semantic-layer.md) |
| **ROUTE** | a typed connection from one node's output field to another's input field; the dataflow of an X3D scene. Behaviour lives here, which is why glTF export loses it | [11](11-gltf-usd-khronos.md) |
| **event cascade** | the ordered propagation of events triggered by one input within one timestamp | [02](02-loom-laws.md), [09](09-castle-engine.md) |
| **TimeSensor, interpolators** | the clock and the keyframe nodes that turn time into field values; the standard animation chain | [06](06-xite-the-oracle.md), [13](13-physics.md) |
| **Script node** | embeds code that reads and writes fields; the part of a scene a validator can only partly judge | [02](02-loom-laws.md) |
| **PROTO / EXTERNPROTO / IS** | user-defined node types, in-file or external, with interface fields wired to inner fields by `IS` | [03](03-validator-and-gates.md) |
| **Inline** | pulls another scene (or glTF) into this one by URL; a path and privacy trap when exported | [10](10-blender-pipeline.md), [11](11-gltf-usd-khronos.md) |
| **SAI** | the Scene Access Interface: the API through which page code reads and writes a running scene (`X3D.getBrowser()` in X_ITE) | [06](06-xite-the-oracle.md) |
| **X3DUOM** | the X3D Unified Object Model: an XML description of every node, field and type, from which schemas and tools are generated | [03](03-validator-and-gates.md), [05](05-semantic-layer.md) |
| **XSD / DTD** | the schema and the legacy document type definition for the XML encoding. They define grammar; they do not say a scene looks right | [03](03-validator-and-gates.md) |
| **X3D Ontology** | an OWL ontology of the X3D vocabulary (class tree, field types, restrictions) used for the graph view in chapter 05 | [05](05-semantic-layer.md) |
| **containerField** | an attribute saying which field of the parent a child node fills; a wrong or missing value is a frequent, silent fault | [03](03-validator-and-gates.md), [07](07-xray.md) |
| **Viewpoint, NavigationInfo** | the camera and the navigation settings; the first Viewpoint decides what a still render shows, so a render check depends on it | [06](06-xite-the-oracle.md) |
| **Material family** | `Material` (classic), `PhysicalMaterial` and `UnlitMaterial` (4.0), `TwoSidedMaterial`; the choice sets how lights and colour spaces behave per renderer | [10](10-blender-pipeline.md) |
| **ComposedShader** | a node carrying GLSL; a renderer on another API (WebGPU) must port each program by hand, keyed by a hash of its source | [08](08-babylon-bridge.md) |
| **HAnim** | the Humanoid Animation component: joints, segments, sites, skin | [10](10-blender-pipeline.md) |
| **RigidBodyPhysics** | the component that describes bodies, joints and collision spaces; an engine such as PhysX or MuJoCo can run it | [13](13-physics.md) |
| **Gaussian splats** | the X3D 4.1 splat node family for point-based radiance scenes; carried in glTF by a Khronos extension | [10](10-blender-pipeline.md), [11](11-gltf-usd-khronos.md) |
| **X_ITE** | the browser X3D engine used here as the reference renderer (WebGL2 only) | [06](06-xite-the-oracle.md) |
| **Castle Game Engine** | a native Pascal engine built on X3D; examined as a host and as a source of seam knowledge | [09](09-castle-engine.md) |
| **Babylon.js** | a browser 3D engine with a WebGPU path; the body in the Babylon bridge, with our own reader as the brain | [08](08-babylon-bridge.md) |
| **WebGL2 / WebGPU / WGSL** | the two browser graphics APIs and the shading language of the second | [08](08-babylon-bridge.md) |
| **glTF / glb** | Khronos's runtime asset format and its single-file binary form; extensions are named `KHR_*` or `EXT_*` | [11](11-gltf-usd-khronos.md) |
| **glTF-Validator** | the Khronos tool that checks glb structure; it does not judge looks | [11](11-gltf-usd-khronos.md) |
| **USD / USDZ** | Pixar's scene description format and its zipped form; a second carrier beside glTF | [11](11-gltf-usd-khronos.md) |
| **Blender, bpy** | the DCC tool that is the studio of this base, and its Python module that runs headless | [10](10-blender-pipeline.md) |
| **Lumen, Nanite, HISM** | Unreal Engine's global illumination, virtualised geometry and hierarchical instanced meshes | [12](12-unreal-tier1.md) |
| **SwiftShader** | Chromium's software GPU. It proves a browser path runs; it proves nothing about GPU speed | [08](08-babylon-bridge.md), [06](06-xite-the-oracle.md) |
| **PSNR, FLIP** | an image-difference score in dB (higher is closer) and a perceptual difference metric (lower is closer); both are correctness yardsticks, not beauty scores | [08](08-babylon-bridge.md), [09](09-castle-engine.md) |
| **MCP** | the Model Context Protocol: how a model calls tools such as the x3d_mcp validator | [04](04-mcp-for-agents.md) |
| **RDF / OWL / SPARQL / SHACL** | graph data, ontology language, graph query language and shape constraints | [05](05-semantic-layer.md) |
| **BH q, permutation null** | the false-discovery-rate correction and the shuffled-data baseline used by the EDA stage of x3d.xray | [07](07-xray.md) |

## Part 2. The method (the Loom and the tether)

| term | working definition | where |
|---|---|---|
| **the tether** | the property that an AI's output can be checked by an exact oracle, repaired from its reports, checked again by a second renderer, and carries its own history. "X3D is the 3D format an AI can be held accountable to" | [01](01-the-tether.md) |
| **tether score** | one point each for an unreliable writer, an exact oracle, valid-differs-from-works, history that must travel with the artifact, and someone answerable later | [01](01-the-tether.md) |
| **oracle** | a checker whose verdict can be reproduced from the same input: the validator for grammar, X_ITE for a render | [03](03-validator-and-gates.md), [06](06-xite-the-oracle.md) |
| **pin** | the exact commit or version a number was measured at. A number is quoted with its pin or not at all | [A](A-validator-register.md) |
| **exact-fix hint** | a validator message that names a concrete edit (move, wrap, rename, set), not just an error | [03](03-validator-and-gates.md) |
| **repair loop** | write, validate, send the report back, rewrite, validate again, until clean or a cap | [01](01-the-tether.md) |
| **valid is not visible** | a file can pass grammar and draw nothing; grammar starts the inspection and never ends it | [01](01-the-tether.md), [02](02-loom-laws.md) |
| **valid is not placed** | a file can pass the schema with parts floating or sunk; a placement check finds them | [05](05-semantic-layer.md) |
| **grade [C]/[L]/[S]** | Confirmed (measured, instrument named), Likely (read or reasoned), Suspected (a guess) | [AUTHORING](AUTHORING.md) |
| **law, failure mode, playbook pattern** | numbered rules, numbered mistakes already paid for once, and numbered procedures of the Loom | [02](02-loom-laws.md) |
| **Loom** | the method that makes one artifact right: a generator, independent witnesses and a receipt | [02](02-loom-laws.md) |
| **generator** | code that emits the artifact; the only place a fix may go | [02](02-loom-laws.md) |
| **witness / gate / receipt** | an independent checker that observes; a predicate that decides whether work may proceed; the record binding candidate, witnesses and outputs | [03](03-validator-and-gates.md) |
| **candidate** | the exact set of files under test, identified by a hash of its inventory | [03](03-validator-and-gates.md) |
| **negative control** | a deliberately wrong input that a gate must reject for the intended reason; a control that passes means a broken gate | [02](02-loom-laws.md) |
| **fold-back** | what a project learned, returned to the shared method as an additions-only patch with its counterexamples | [02](02-loom-laws.md) |
| **parity** | agreement between two renderers on the same file, expressed as numbers (dB, counts), never as "looks the same" | [08](08-babylon-bridge.md) |
| **master / body / brain** | the X3D file is the master; the renderer's drawing code is a body; our reader that runs the scene graph and events is the brain | [08](08-babylon-bridge.md) |
| **look** | a presentation layer (bloom, tone curve, grain) that may add to a scene but never assert; it has an "as authored" switch | [08](08-babylon-bridge.md) |
| **round trip** | export then re-import, to measure what a pipeline loses; a re-export can be valid even when the source was not, so score fidelity, not validity | [10](10-blender-pipeline.md) |
| **bake** | compute light once (for example Cycles vertex colours) and store it in the file so it travels | [10](10-blender-pipeline.md) |
| **tier-1 framework** | in this base: a host that drives the same file, passes the same gate and reports parity numbers like X_ITE does | [12](12-unreal-tier1.md) |
| **teardown** | an AST-based analysis of a code base with measured numbers; the six on this site | [00](00-start-here.md) |
