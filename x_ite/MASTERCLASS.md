# X_ITE 16.7.0: an AST masterclass, and heuristics for learning it

[create3000/x_ite](https://github.com/create3000/x_ite) is the X3D browser every fidelity decision in your repos calibrates
against ("as X_ITE draws it"). This teardown reads **version 16.7.0 exactly as installed** in
`x3d-physx-bridge/node_modules/x_ite`. Nothing was downloaded: the unminified bundles keep webpack's `;// ./src/...` module
markers, so `tools/xite_split.py` rebuilt the source tree (752 modules from 24 bundles; npm
dependencies such as opentype.js and the Ammo.js physics build are split out as vendored). No commit history, by your choice.

**Labels.** *Measured*: the TypeScript parser over every module, regular expressions over X_ITE's own fixed conventions
(`getStaticProperties`, `X3DFieldDefinition`, `setPrototypeOf`, `.call (this)` mixins), the X3D Unified Object Model 4.1,
and your scene corpus. *Inferred*: the heuristics' weights and thresholds, which are choices, stated with each one.

| scene | what it shows |
|---|---|
| `scenes/learning-map.x3d` | **X_ITE's own class tree** (394 node classes) with the 32-step curriculum as a gold path; colour = temperament, size = use in your files |
| `scenes/conformance-sunburst.x3d` | every X3D 4.1 node: X_ITE's module size and its field-by-field agreement with the spec; outer ring = your usage |
| `scenes/callgraph-3d.x3d` | 641 modules by force layout, 5745 functions, 4,796 references between modules |
| `scenes/code-city.x3d` | functions as buildings in 94 directories; amber = the same body in 2+ modules |

## 1. Anatomy in numbers (measured)

* **98,369 lines of X_ITE's own JavaScript** in 730 modules: node classes 47,535, browser machinery
  16,230, rendering and GLSL 3,582, core (fields, execution, routing, prototypes) 10,650,
  parsers 12,188, math 6,474, API and registration 1,710. 5,940 named functions, 5,001 of
  them methods attached with X_ITE's `Object.assign(Object.setPrototypeOf(X.prototype, Base.prototype), {...})` idiom.
* **One module per node type.** 292 concrete node modules: **266 of the 267** X3D 4.1 nodes,
  plus 26 X_ITE-only types (glTF material extensions such as `SheenMaterialExtension`, the Annotation
  component, `InstancedShape`, `BlendMode`, `DepthMode`, `SpecularGlossinessMaterial` …). The one 4.1 node without a module
  is `ProtoInstance`, which X_ITE implements in its execution layer (`X3DPrototypeInstance`).
* **Field conformance** against X3DUOM 4.1: **194 nodes match field for field** (name, type, access), 43
  add fields, 29 differ, 1 has no module.
* **Most complex functions:** `SVGParser.dAttribute` 82 (SVGParser); `PLYAParser.parseVertices` 81 (PLYAParser); `X3DNode.toXMLStream` 62 (X3DNode); `X3DNode.getMetaData` 59 (X3DNode); `X3DNode.setMetaData` 56 (X3DNode); `X3DNode.toJSONStream` 52 (X3DNode).

## 2. Learning heuristics

Each heuristic turns a measurement into a decision about *what to read next*. They are built for X_ITE but work on any
large codebase that mirrors a specification.

### H1. Keystones: read what everything leans on, if it is short

*Measure:* PageRank over "module A uses module B" edges (rank flows to what is depended upon), divided by √lines.
*Why it teaches:* a module that hundreds of others reference defines the vocabulary they are all written in. If it is also
short, reading it is the cheapest way to make every other file legible.

| module | modules depending on it | lines | score |
|---|---|---|---|
| [Namespace](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Namespace.js) | 721 | 19 | 637.8 |
| [Fields](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Fields.js) | 346 | 19 | 63.0 |
| [FieldDefinitionArray](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/FieldDefinitionArray.js) | 299 | 19 | 46.0 |
| [SFNodeCache](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Fields/SFNodeCache.js) | 11 | 30 | 24.0 |
| [X3DFieldDefinition](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DFieldDefinition.js) | 299 | 94 | 20.7 |
| [IterableWeakSet](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/IterableWeakSet.js) | 2 | 5 | 18.5 |
| [Algorithm](https://github.com/create3000/x_ite/blob/16.7.0/src/standard/Math/Algorithm.js) | 80 | 145 | 14.6 |
| [X3DCast](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DCast.js) | 91 | 21 | 13.5 |
| [X3DConstants](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DConstants.js) | 189 | 100 | 13.2 |
| [X3DNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DNode.js) | 377 | 1235 | 10.0 |
| [Components](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components.js) | 23 | 31 | 10.0 |
| [X3DChildObject](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DChildObject.js) | 6 | 106 | 8.6 |

`Namespace` (721 dependents, 19 lines) is X_ITE's registry: every module registers its export there, so knowing it explains
the bundle's wiring. `Fields` and `X3DFieldDefinition` are the type system every node declares itself in. `X3DNode`
(1,235 lines) is the one long keystone: the base class of everything.

### H2. Leverage: learn the abstract type that unlocks the most nodes per line

*Measure:* for each abstract type in X_ITE's own class tree, the concrete nodes that inherit from it, per 100 lines of the
abstract module. *Why:* abstract types are where shared behaviour lives; a 19-line base that 30 nodes extend is 30 lessons for
the price of one.

| abstract type | concrete nodes unlocked | lines | per 100 lines | uses in your files |
|---|---|---|---|---|
| [X3DAppearanceChildNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Shape/X3DAppearanceChildNode.js) | 30 | 19 | 150.0 | 601 |
| [X3DSensorNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DSensorNode.js) | 24 | 20 | 120.0 | 239 |
| [X3DSoundNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Sound/X3DSoundNode.js) | 22 | 20 | 110.0 | 79 |
| [X3DChildNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DChildNode.js) | 149 | 160 | 93.12 | 2877 |
| [X3DGeometricPropertyNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Rendering/X3DGeometricPropertyNode.js) | 17 | 19 | 85.0 | 487 |
| [X3DComposableVolumeRenderStyleNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/VolumeRendering/X3DComposableVolumeRenderStyleNode.js) | 9 | 23 | 39.13 | 3 |
| [X3DTextureNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Texturing/X3DTextureNode.js) | 12 | 34 | 35.29 | 128 |
| [X3DBoundedObject](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Grouping/X3DBoundedObject.js) | 43 | 127 | 33.86 | 1266 |
| [X3DNetworkSensorNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Networking/X3DNetworkSensorNode.js) | 6 | 20 | 30.0 | 11 |
| [X3DMetadataObject](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DMetadataObject.js) | 6 | 23 | 26.09 | 121 |
| [X3DTextureCoordinateNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Texturing/X3DTextureCoordinateNode.js) | 5 | 20 | 25.0 | 61 |
| [X3DMaterialExtensionNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/X_ITE/X3DMaterialExtensionNode.js) | 13 | 57 | 22.81 | 0 |

**X_ITE's tree is not the spec's tree.** In 36 nodes the bases differ from X3DUOM's. X_ITE adds
implementation layers the spec does not have (`X3DLineGeometryNode`, `X3DPointGeometryNode`, `X3DArrayChaserObject`,
`X3DGeospatialObject`, `X3DSingleTextureNode`), and sometimes skips a spec mixin. These differences show where a renderer
needs a shared code path that the spec never names:

| node | X_ITE bases | X3DUOM bases |
|---|---|---|
| CADPart | X3DProductStructureChildNode, X3DTransformNode | X3DGroupingNode, X3DProductStructureChildNode |
| X3DEnvironmentTextureNode | X3DSingleTextureNode | X3DTextureNode |
| CoordinateChaser | X3DArrayChaserObject, X3DChaserNode | X3DChaserNode |
| CoordinateDamper | X3DArrayFollowerObject, X3DDamperNode | X3DDamperNode |
| TexCoordChaser2D | X3DArrayChaserObject, X3DChaserNode | X3DChaserNode |
| TexCoordDamper2D | X3DArrayFollowerObject, X3DDamperNode | X3DDamperNode |
| GaussianSplats | X3DGaussianSplatsNode | X3DBoundedObject, X3DChildNode |
| Arc2D | X3DLineGeometryNode | X3DGeometryNode |
| Circle2D | X3DLineGeometryNode | X3DGeometryNode |
| Disk2D | X3DGeometryNode, X3DLineGeometryNode | X3DGeometryNode |
| Polyline2D | X3DLineGeometryNode | X3DGeometryNode |
| Polypoint2D | X3DPointGeometryNode | X3DGeometryNode |
| GeoCoordinate | X3DCoordinateNode, X3DGeospatialObject | X3DCoordinateNode |
| GeoElevationGrid | X3DGeometryNode, X3DGeospatialObject | X3DGeometryNode |
| GeoLOD | X3DBoundedObject, X3DChildNode, X3DGeospatialObject | X3DBoundedObject, X3DChildNode |
| GeoLocation | X3DGeospatialObject, X3DTransformMatrix3DNode | X3DGroupingNode |
| GeoPositionInterpolator | X3DGeospatialObject, X3DInterpolatorNode | X3DInterpolatorNode |
| GeoProximitySensor | X3DEnvironmentalSensorNode, X3DGeospatialObject | X3DEnvironmentalSensorNode |
| GeoTouchSensor | X3DGeospatialObject, X3DTouchSensorNode | X3DTouchSensorNode |
| GeoTransform | X3DGeospatialObject, X3DTransformMatrix3DNode | X3DGroupingNode |

### H3. Spec deltas: where the renderer knows more than the spec

*Measure:* field-by-field difference between each node's `fieldDefinitions` and X3DUOM 4.1. *Why:* an added field is a
lesson the spec does not teach (what a real renderer needed); a missing or retyped field is a place to be careful when you
write scenes. The most common additions: `shadowBias` (6), `shadowColor` (6), `shadowMapSize` (6), `tangent` (5), `pointerEvents` (4), `loop` (3), `update` (2), `visibilityStart` (2).

| node | delta | fields |
|---|---|---|
| Analyser | X_ITE adds | byteFrequencyData, byteTimeDomainData, floatFrequencyData, floatTimeDomainData |
| Appearance | X_ITE adds | blendMode, depthMode |
| BooleanTrigger | X_ITE adds | triggerFalse |
| BoundedPhysicsModel | X_ITE adds | damping |
| BufferAudioSource | X_ITE adds | bufferLength |
| CADFace | X_ITE adds | rebuild |
| ComposedCubeMapTexture | X_ITE adds | update |
| ComposedTexture3D | X_ITE adds | update |
| Convolver | X_ITE adds | numberOfChannels |
| DirectionalLight | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| ElevationGrid | X_ITE adds | tangent |
| EnvironmentLight | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| FillProperties | X_ITE adds | transparent |
| Fog | X_ITE adds | visibilityStart |
| FontStyle | X_ITE adds | style |
| GeoElevationGrid | X_ITE adds | tangent |
| GeoViewpoint | X_ITE adds | headlight, navType |
| HAnimHumanoid | X_ITE adds | displacementWeightsTexture, displacementsTexture, displacers, jointName, jointTextures |
| HAnimJoint | X_ITE adds | displacementWeights, displacements, maxAngle, minAngle |
| HAnimSegment | X_ITE adds | displacementWeightsTexture, displacementsTexture |
| HAnimSite | X_ITE adds | coord, displacers, meshVertexIndex, purpose |
| ImageTexture | X_ITE adds | colorSpaceConversion |
| IndexedLineSet | X_ITE adds | tangent |
| Layer | X_ITE adds | pointerEvents |
| LayerSet | X_ITE adds | activeLayerNode |
| LayoutLayer | X_ITE adds | pointerEvents |
| LineSet | X_ITE adds | tangent |
| LocalFog | X_ITE adds | visibilityStart |
| MicrophoneSource | X_ITE adds | loop |
| MultiTexture | X_ITE adds | renderedTextures |
| NavigationInfo | X_ITE adds | availableViewers, transitionActive, transitionStart, viewer |
| OrthoViewpoint | X_ITE adds | fieldOfViewOffset |
| OscillatorSource | X_ITE adds | loop |
| ParticleSystem | X_ITE adds | pointerEvents, scale, scaleKey |
| PhysicalMaterial | X_ITE adds | extensions |
| PixelTexture | X_ITE adds | loadState |
| PointLight | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| PointSet | X_ITE adds | tangent |
| RenderedTexture | X_ITE adds | children, enabled, loadState |
| RigidBody | X_ITE adds | collection, otherGeometry, transform |
| ScreenFontStyle | X_ITE adds | style |
| Shape | X_ITE adds | pointerEvents |
| Sound | X_ITE adds | children, traversed |
| SpatialSound | X_ITE adds | traversed |
| SpotLight | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| SquadOrientationInterpolator | X_ITE adds | closed |
| StreamAudioSource | X_ITE adds | loop |
| TextureProjector | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| TextureProjectorParallel | X_ITE adds | shadowBias, shadowColor, shadowMapSize |
| TimeSensor | X_ITE adds | cycleComplete, cycleCompleteTime, cycleCount, range |
| BufferAudioSource | X_ITE lacks | bufferlength, length |
| ComposedShader | X_ITE lacks | field |
| ListenerPointSource | X_ITE lacks | elapsedTime, gain, isActive, isPaused, pauseTime, resumeTime, startTime, stopTime |
| PackagedShader | X_ITE lacks | field |
| Script | X_ITE lacks | field, sourceCode |
| ShaderPart | X_ITE lacks | sourceCode |
| ShaderProgram | X_ITE lacks | field, sourceCode |
| StreamAudioSource | X_ITE lacks | channelCountMode, channelInterpretation |
| X3DPrototypeInstance | X_ITE lacks | metadata |
| Analyser | access differs | channelCount, frequencyBinCount |
| AudioDestination | access differs | channelCount, maxChannelCount |
| BiquadFilter | access differs | channelCount |
| BufferAudioSource | access differs | bufferDuration, channelCount |
| ChannelMerger | access differs | channelCount |
| ChannelSelector | access differs | channelCount |
| ChannelSplitter | access differs | channelCount |
| Convolver | access differs | channelCount |
| Delay | access differs | channelCount |
| DynamicsCompressor | access differs | channelCount |
| Gain | access differs | channelCount |
| InlineGeometry | access differs | smooth |
| RenderedTexture | access differs | height |
| StreamAudioDestination | access differs | channelCount |
| WaveShaper | access differs | channelCount |
| BufferAudioSource | type differs | loopEnd, loopStart |
| FloatVertexAttribute | type differs | name |
| HAnimPose | type differs | set_fraction |
| Matrix3VertexAttribute | type differs | name |
| Matrix4VertexAttribute | type differs | name |
| MovieTexture | type differs | hasSound |
| OrthoViewpoint | type differs | fieldOfView |
| ParticleSystem | type differs | particleLifetime |

Reading this table: shadow maps need `shadowBias`, `shadowColor`, `shadowMapSize` on every light; GPU skinning adds
displacement *textures* to H-Anim; `Script`, `ComposedShader`, `PackagedShader` and `ShaderProgram` "lack" `field` because
their fields are user-declared at run time; most Sound "access differs" rows are `channelCount`, which X_ITE reports rather
than accepts.

### H4. Surprise: machinery hidden behind few fields

*Measure:* fit log(lines) against log(fields) across all nodes (slope 0.421), then take each node's residual.
*Why:* a node's fields are its contract; its lines are its cost. Big positive residuals are nodes whose behaviour is far
richer than their interface: the best case studies. Big negative residuals are thin data holders whose logic lives in a
base class or in `Browser/`: skim them.

| case studies (more lines than fields predict) | fields | lines | vs expected |
|---|---|---|---|
| StaticGroup | 6 | 830 | 8.0x |
| ParticleSystem | 25 | 1129 | 5.9x |
| Layout | 7 | 531 | 4.8x |
| Extrusion | 15 | 665 | 4.3x |
| Script | 8 | 455 | 3.9x |
| HAnimHumanoid | 37 | 745 | 3.3x |
| GeneratedCubeMapTexture | 5 | 286 | 3.0x |
| Appearance | 14 | 435 | 2.9x |
| ImageCubeMapTexture | 7 | 305 | 2.7x |
| OrthoViewpoint | 16 | 417 | 2.6x |
| CollidableShape | 9 | 318 | 2.6x |
| HAnimSegment | 17 | 418 | 2.6x |

| skim (inherit almost everything) | fields | lines | vs expected |
|---|---|---|---|
| Contact | 17 | 59 | 0.4x |
| CADLayer | 9 | 44 | 0.4x |
| AcousticProperties | 7 | 39 | 0.4x |
| CADPart | 14 | 51 | 0.3x |
| Group | 8 | 40 | 0.3x |
| Gain | 16 | 52 | 0.3x |
| Transform | 13 | 45 | 0.3x |
| NurbsPatchSurface | 15 | 47 | 0.3x |

### H5. Twins: learn one, get the rest

*Measure:* concrete nodes with identical base classes and method-name sets at least 80 % alike (Jaccard).
*Why:* when the AST says two nodes are built the same way, the second one costs nothing.

* IndexedQuadSet, IndexedTriangleFanSet, IndexedTriangleSet, IndexedTriangleStripSet, TriangleFanSet, TriangleStripSet
* CartoonVolumeStyle, EdgeEnhancementVolumeStyle, ShadedVolumeStyle, SilhouetteEnhancementVolumeStyle, ToneMappedVolumeStyle
* FloatVertexAttribute, Matrix3VertexAttribute, Matrix4VertexAttribute
* SplinePositionInterpolator, SplinePositionInterpolator2D, SplineScalarInterpolator
* TextureCoordinate, TextureCoordinate3D, TextureCoordinate4D
* Color, ColorRGBA
* IsoSurfaceVolumeData, VolumeData
* PointLight, SpotLight
* QuadSet, TriangleSet

### H6. Temperament: data, event-driven, engine, sensor

*Measure:* the share of a node's fields that are events (inputOnly, outputOnly) and outputs. *Why:* you read a data node for
its fields, an engine for its update loop, a sensor for when it fires. Knowing which kind you are looking at tells you where
in the module to start. Counts: data 192, event-driven 43, engine 30, sensor
25. Most event-heavy engines (event share ≥ 35 %, not output-dominated): IntegerSequencer, BooleanSequencer, Contour2D, PositionChaser2D, IntegerTrigger, TexCoordChaser2D, PositionChaser, ScalarChaser.

### H7. Locus: where a component's behaviour actually lives

*Measure:* lines in `Components/<C>` (the node classes) against `Browser/<C>` (the per-component machinery the nodes call).
*Why:* for some components the node classes are the behaviour; for others they are thin handles over a browser subsystem,
and reading the nodes alone teaches little.

| component | node lines | browser lines | in browser |
|---|---|---|---|
| WebXR | 0 | 513 | 100 % |
| GaussianSplats | 132 | 623 | 83 % |
| Text | 430 | 933 | 68 % |
| Texturing3D | 934 | 1,282 | 58 % |
| Navigation | 1,738 | 2,239 | 56 % |
| Core | 2,575 | 2,416 | 48 % |
| PointingDeviceSensor | 708 | 566 | 44 % |
| Geometry2D | 604 | 351 | 37 % |
| Geometry3D | 1,423 | 728 | 34 % |
| Layout | 720 | 364 | 34 % |
| Interpolation | 843 | 286 | 25 % |
| Texturing | 1,915 | 580 | 23 % |
| Networking | 921 | 255 | 22 % |
| Rendering | 3,363 | 880 | 21 % |
| NURBS | 1,638 | 321 | 16 % |
| Picking | 1,228 | 227 | 16 % |
| Shaders | 1,730 | 303 | 15 % |
| Lighting | 1,082 | 192 | 15 % |
| Time | 411 | 66 | 14 % |
| KeyDeviceSensor | 446 | 74 | 14 % |
| Followers | 974 | 139 | 12 % |
| Scripting | 378 | 48 | 11 % |
| Geospatial | 1,557 | 172 | 10 % |
| Sound | 2,731 | 273 | 9 % |
| VolumeRendering | 2,049 | 203 | 9 % |
| X_ITE | 1,831 | 152 | 8 % |
| Shape | 2,223 | 176 | 7 % |
| Grouping | 1,398 | 89 | 6 % |
| CubeMapTexturing | 726 | 41 | 5 % |
| EnvironmentalEffects | 892 | 23 | 3 % |
| Layering | 682 | 20 | 3 % |
| ParticleSystems | 2,312 | 75 | 3 % |
| RigidBodyPhysics | 2,579 | 17 | 1 % |
| DIS | 494 | 0 | 0 % |
| HAnim | 1,773 | 0 | 0 % |
| EventUtilities | 357 | 0 | 0 % |
| TextureProjection | 502 | 0 | 0 % |
| Annotation | 242 | 0 | 0 % |
| EnvironmentalSensor | 510 | 0 | 0 % |
| CADGeometry | 484 | 0 | 0 % |

GaussianSplats (83 %), Text (68 %), Texturing3D and Navigation keep their logic in `Browser/`; HAnim, RigidBodyPhysics, DIS
and CAD keep it in the nodes. WebXR has no nodes at all.

### H8. Your corpus: weight everything by what you actually write

*Measure:* how many of your own X3D files (x3d.loom, x3d.demo, x3d.onto) use each node. Top: Appearance 311, Shape 309, Viewpoint 271, Transform 269, NavigationInfo 240, Coordinate 208, Background 202, Material 196, WorldInfo 163, DirectionalLight 141, Group 138, PhysicalMaterial 131.
*Why:* the same renderer is a different textbook for different readers. Weighting by your corpus puts `Appearance`,
`Coordinate` and `NavigationInfo` early, and lets `HAnimHumanoid` wait until you need it.

## 3. The curriculum (32 steps, generated)

Tracks: **keystone** (H1, at least 20 dependents), **abstract** (H2), **quick win** (your usage per line to read, including
prerequisites not yet learned), **deep dive** (nodes you use with surprise above 0.5, H4). The learning map draws this path.

| step | track | read | why |
|---|---|---|---|
| 1 | keystone | [Namespace](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Namespace.js) | keystone: 721 modules depend on it, 19 lines |
| 2 | keystone | [Fields](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Fields.js) | keystone: 346 modules depend on it, 19 lines |
| 3 | keystone | [FieldDefinitionArray](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/FieldDefinitionArray.js) | keystone: 299 modules depend on it, 19 lines |
| 4 | keystone | [X3DFieldDefinition](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DFieldDefinition.js) | keystone: 299 modules depend on it, 94 lines |
| 5 | keystone | [Algorithm](https://github.com/create3000/x_ite/blob/16.7.0/src/standard/Math/Algorithm.js) | keystone: 80 modules depend on it, 145 lines |
| 6 | keystone | [X3DCast](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DCast.js) | keystone: 91 modules depend on it, 21 lines |
| 7 | keystone | [X3DConstants](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Base/X3DConstants.js) | keystone: 189 modules depend on it, 100 lines |
| 8 | keystone | [X3DNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DNode.js) | keystone: 377 modules depend on it, 1235 lines |
| 9 | abstract | [X3DAppearanceChildNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Shape/X3DAppearanceChildNode.js) | abstract X3DAppearanceChildNode: unlocks 30 concrete nodes in 19 lines; your files use them 601 times |
| 10 | abstract | [X3DSensorNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DSensorNode.js) | abstract X3DSensorNode: unlocks 24 concrete nodes in 20 lines; your files use them 239 times |
| 11 | abstract | [X3DSoundNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Sound/X3DSoundNode.js) | abstract X3DSoundNode: unlocks 22 concrete nodes in 20 lines; your files use them 79 times |
| 12 | abstract | [X3DChildNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/X3DChildNode.js) | abstract X3DChildNode: unlocks 149 concrete nodes in 160 lines; your files use them 2877 times |
| 13 | abstract | [X3DGeometricPropertyNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Rendering/X3DGeometricPropertyNode.js) | abstract X3DGeometricPropertyNode: unlocks 17 concrete nodes in 19 lines; your files use them 487 times |
| 14 | abstract | [X3DComposableVolumeRenderStyleNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/VolumeRendering/X3DComposableVolumeRenderStyleNode.js) | abstract X3DComposableVolumeRenderStyleNode: unlocks 9 concrete nodes in 23 lines; your files use them 3 times |
| 15 | abstract | [X3DTextureNode](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Texturing/X3DTextureNode.js) | abstract X3DTextureNode: unlocks 12 concrete nodes in 34 lines; your files use them 128 times |
| 16 | abstract | [X3DBoundedObject](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Grouping/X3DBoundedObject.js) | abstract X3DBoundedObject: unlocks 43 concrete nodes in 127 lines; your files use them 1266 times |
| 17 | quick win | [WorldInfo](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/WorldInfo.js) | WorldInfo: in 163 of your X3D files, 76 lines to read (with X3DInfoNode) |
| 18 | quick win | [MetadataString](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/MetadataString.js) | MetadataString: in 54 of your X3D files, 81 lines to read (with X3DMetadataObject) |
| 19 | quick win | [Normal](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Rendering/Normal.js) | Normal: in 66 of your X3D files, 107 lines to read (with X3DNormalNode) |
| 20 | quick win | [Coordinate](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Rendering/Coordinate.js) | Coordinate: in 208 of your X3D files, 187 lines to read (with X3DCoordinateNode) |
| 21 | quick win | [Color](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Rendering/Color.js) | Color: in 63 of your X3D files, 121 lines to read (with X3DColorNode) |
| 22 | quick win | [MetadataDouble](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Core/MetadataDouble.js) | MetadataDouble: in 23 of your X3D files, 81 lines to read (with X3DMetadataObject) |
| 23 | quick win | [FloatVertexAttribute](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Shaders/FloatVertexAttribute.js) | FloatVertexAttribute: in 42 of your X3D files, 125 lines to read (with X3DVertexAttributeNode) |
| 24 | quick win | [PositionInterpolator](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Interpolation/PositionInterpolator.js) | PositionInterpolator: in 50 of your X3D files, 147 lines to read (with X3DInterpolatorNode) |
| 25 | deep dive | [ParticleSystem](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/ParticleSystems/ParticleSystem.js) | ParticleSystem: 5.9x the lines its 25 fields predict; in 36 of your X3D files |
| 26 | deep dive | [Appearance](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Shape/Appearance.js) | Appearance: 2.9x the lines its 14 fields predict; in 311 of your X3D files |
| 27 | deep dive | [Extrusion](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Geometry3D/Extrusion.js) | Extrusion: 4.3x the lines its 15 fields predict; in 32 of your X3D files |
| 28 | deep dive | [StaticGroup](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Grouping/StaticGroup.js) | StaticGroup: 8.0x the lines its 6 fields predict; in 6 of your X3D files |
| 29 | deep dive | [IndexedFaceSet](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Geometry3D/IndexedFaceSet.js) | IndexedFaceSet: 2.0x the lines its 22 fields predict; in 117 of your X3D files |
| 30 | deep dive | [NavigationInfo](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/Navigation/NavigationInfo.js) | NavigationInfo: 1.8x the lines its 16 fields predict; in 240 of your X3D files |
| 31 | deep dive | [CollidableShape](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/RigidBodyPhysics/CollidableShape.js) | CollidableShape: 2.6x the lines its 9 fields predict; in 30 of your X3D files |
| 32 | deep dive | [HAnimHumanoid](https://github.com/create3000/x_ite/blob/16.7.0/src/x_ite/Components/HAnim/HAnimHumanoid.js) | HAnimHumanoid: 3.3x the lines its 37 fields predict; in 12 of your X3D files |

## 4. Insights

1. **X_ITE is a near-literal transcription of the spec.** 194 of 267 nodes declare exactly the spec's fields, and every
   node module starts with the same `getStaticProperties(name, component, level, containerField, version)` call. That
   regularity is why this teardown could check conformance with a few regular expressions, and why the field tables are a
   reliable reference when the spec text is ambiguous.
2. **The extensions tell you where rendering reality presses on the spec**: shadows, GPU skinning, glTF PBR extensions,
   pointer events on layers. They are also where your exports may draw differently in other browsers.
3. **Two places to read for every component:** `Components/` for the contract and `Browser/` for the machinery (H7).
   A hypothesis tested and rejected: that your Loom bridge's unfinished nodes (gap, todo, blocked in `NODES.json`) cluster
   in components whose X_ITE logic lives in `Browser/`. Measured on the 260 tracked nodes, the opposite holds: 36 % are
   unfinished in browser-heavy components (share ≥ 40 %) against 54 % elsewhere (correlation −0.23). The bridge has done
   the machinery-heavy components; what is left is the long tail of node-local behaviour (Sound, HAnim, CAD, DIS, Followers).

## 5. Method and limits

* Source rebuilt from the npm bundles; module boundaries are webpack's. 24 fragments parse with recoverable errors where a
  bundle wrapper cuts a statement. GLSL shader sources are counted as modules (they are JS strings).
* Module references are resolved by webpack's export names (`Lighting_X3DLightNode`) and the component bundles' external
  accessors (`external_X_ITE_X3D_X3DNode_default()`); method-to-method dispatch through `this` is not followed.
* Field defaults are compared numerically with a 0.1 % tolerance (X_ITE writes 0.785398 where X3DUOM writes 0.7854); defaults
  built with `new …` are not compared.
* The heuristics' thresholds (≥ 20 dependents, Jaccard ≥ 0.8, surprise > 0.5, temperament cut-offs) are choices; change them in
  `tools/xite_learn.py` and the curriculum regenerates.
* All four scenes validate with x3d_mcp (XSD 4.0, 0 errors, 0 warnings) and render in X_ITE 16.7.0 itself in the Claude browser pane.
