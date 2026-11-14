# x3d-blender-io: an AST masterclass and teardown

The add-on (`io_scene_x3d`, extension id `x3d_blender_io`) at
[hagopjay/x3d-blender-io](https://github.com/hagopjay/x3d-blender-io), measured on 2026-11-13 at `origin/main`
`e071a61` and compared against the fork's first commit `7f8c0fb` (2026-10-08, "Import April 2026 X3D 4.0 rewrite
of io_scene_x3d (extension 2.5.1 base)").

**How to read the labels in this document.**

* **Measured** means a script in `tools/` computed it from the source with Python's `ast`, from `git`, from the
  GitHub API (`gh`), or from the x3d_mcp validator. Every number in a table is measured unless the table says
  otherwise.
* **Inferred** means the number comes from a heuristic. These are marked *inferred* where they appear: X3D node
  and field use from string literals, call resolution, and pipeline roles assigned by hand to modules.
* **Claimed** means a PR description says it. Claims are quoted, and checked where the data allows.
* Nothing in the add-on was imported or executed. No Blender or X_ITE run of the add-on was made for this
  document.

The four scenes (X3D 4.0, validated with the user's x3d_mcp fork, rendered in X_ITE 16.7.0) are linked from
`index.html`:

| scene | what it shows |
|---|---|
| `scenes/callgraph-3d.x3d` | 554 functions as a 3D force layout, 697 static call edges, coloured by pipeline role |
| `scenes/coverage-sunburst.x3d` | the 267 concrete X3D 4.1 nodes by component, and which are written and read |
| `scenes/fork-timeline.x3d` | 42 snapshots of `origin/main`: lines, tests and X3D coverage per PR, and CI results |
| `scenes/code-city.x3d` | modules as districts and functions as buildings; height is complexity, colour is fork-era status |

---

## 1. The shape of the add-on

```
                         Blender scene (bpy)
             ┌──────────────────┴──────────────────┐
   EXPORT    │                                     │   IMPORT
             ▼                                     ▲
  export_x3d.export  (legacy fw() writer,     import_x3d.load_web3d (legacy VRML/X3D
  1,620 lines, 29 nested writers)┐               tree: vrmlNode/x3dNode parser, then
             │ X3D 4.0/4.1     │               geometry_importers{28}, appearance_*,
             ▼                 │ X3D 3.x        importLamp_*, importRoutesXML, HAnim,
  export_pipeline ─► extract ─►│ text           Geo*, Inline, splats)  ◄── .x3d .wrl .x3dv .x3dz
  (Blender → IR)     material  │                     │  Inline assets
             ▼        splat_*  ▼                     ▼
          ir.py  (IRScene, IRShape, IRMeshGeometry, IRPBRMaterial, IRLight, IRHumanoid, IRGaussianSplats …)
             ▼                                       ▲
       emit_x3d40 ─► validate ─► .x3d       parse_x3d40 ─► populate (Inline asset bridge),
                                            bridge_gltf (glTF/glb Inlines), splat_io
```

These things are measured.

* **Two pipelines in each direction.** Export has the legacy Blender exporter, which builds XML strings with
  `fw('%s<Shape' % ident)`, and the X3D 4.0 path, *Blender → `extract` → `ir` dataclasses → `emit_x3d40`*. The two
  are not separate: `export_x3d` calls into `extract` 13 times (the biggest cross-module edge in
  the call graph). It is both the 3.x writer and the dispatcher for the 4.0 path.
* **Import has one dominant module.** `import_x3d.py` is 7,264 of 16,530 source lines (44 %) and holds 245 of 557
  `def`s. The IR-based import (`parse_x3d40` → `populate`) is small (445 lines) and is used for Inline assets. It is
  not a second full importer.
* **The Blender surface is small.** There are three registered classes: `ImportX3D` (`import_scene.x3d`, 12
  options, including the fork's `color_space`, `light_units` and `gpu_instances`), `ExportX3D`
  (`export_scene.x3d`, 27 options, including `x3d_version` and `color_space`), and the `IO_FH_X3D` file handler
  for `.x3d;.wrl;.x3dv;.x3dz`. There is also an `AddonPreferences`. There are no Panels or custom Menus.
* **Imports are lazy.** 101 of the 206 import statements sit inside functions; `import_x3d` alone has 35. That is
  the usual Blender add-on idiom, which keeps registration cheap and avoids import cycles. It also means the
  module-level import graph understates the coupling. The call graph is the truer picture.

| module | role | lines base -> head | defs | CC sum | max CC (function) |
|---|---|---|---|---|---|
| `import_x3d` | import-classic | 4386 -> 7264 | 245 | 2045 | 79 (`importMesh_IndexedFaceSet`) |
| `export_x3d` | export-classic | 1918 -> 1985 | 46 | 371 | 94 (`export.writeIndexedFaceSet`) |
| `extract` | export-modern | 184 -> 1317 | 53 | 472 | 41 (`extract_scene`) |
| `translations` | ui | 1201 -> 1226 | 3 | 5 | 3 (`translate`) |
| `emit_x3d40` | export-modern | 260 -> 822 | 44 | 294 | 26 (`_animation_xml`) |
| `__init__` | ui | 621 -> 712 | 24 | 44 | 4 (`export_ui_include`) |
| `material` | export-modern | 573 -> 666 | 30 | 248 | 32 (`analyze_material`) |
| `ir` | ir | 118 -> 373 | 13 | 34 | 8 (`IRInstance.iter_shapes`) |
| `parse_x3d40` | import-modern | 258 -> 258 | 15 | 63 | 10 (`_decompose_matrix`) |
| `splat_io` | bridge | new -> 256 | 14 | 84 | 21 (`_rows_to_splats`) |
| `export_pipeline` | export-modern | 156 -> 250 | 7 | 56 | 25 (`save`) |
| `geospatial` | import-classic | new -> 216 | 8 | 32 | 11 (`parse_geo_system`) |
| `populate` | import-modern | 185 -> 187 | 10 | 45 | 9 (`_populate_viewpoints`) |
| `mfstring` | ir | 174 -> 174 | 8 | 29 | 13 (`decode`) |
| `splat_native` | bridge | new -> 171 | 10 | 51 | 14 (`extract_native_splats`) |
| `validate` | export-modern | 50 -> 165 | 7 | 51 | 23 (`_coerce_field`) |
| `matrix_safety` | import-classic | new -> 157 | 9 | 38 | 21 (`push_scale_to_children`) |
| `x3d_registry` | ir | 107 -> 107 | 1 | 1 | 1 (`get_node_spec`) |
| `prefs` | ui | 69 -> 69 | 2 | 5 | 4 (`X3D_Preferences.get_report_url`) |
| `viewpoint_fov` | bridge | new -> 50 | 4 | 13 | 5 (`blender_camera_angle`) |
| `bridge_gltf` | bridge | 49 -> 49 | 3 | 16 | 6 (`import_gltf`) |
| `material_node_search` | export-modern | 30 -> 30 | 0 | 0 | - |
| `emit_x3d33` | export-modern | 26 -> 26 | 1 | 2 | 2 (`export_ir_scene`) |

`export_x3d` is 1,985 lines but a single function, `export`, spans 1,620 of them. It defines 29 nested writer
closures (`writeIndexedFaceSet`, `writeFog`, `writeSpeaker` …) that share the outer function's state.

## 2. The taxonomy the AST reveals

### 2.1 X3D coverage (inferred from string literals, with evidence strength)

The analyser reads every string literal and f-string fragment and checks it against the X3D Unified Object Model
4.1 (`X3dUnifiedObjectModel-4.1.xml` in the x3d_mcp fork): 267 concrete nodes in 37 components. Each literal is
classified as follows.

* **write**: an emitted tag (`'<Sphere '`) or attribute (`radius="`) anywhere, or a node name in an export-role
  module.
* **read**: a node name in an import-role module used as a dispatch-table key, in a comparison
  (`spec == 'Switch'`), as an argument to `getChildBySpec` / `getFieldAs*`, or in a node-name constant.
* **strength**: 3 means an emitted tag or dispatch-table key; 2 means a comparison or getter argument; 1 means the
  name only appears in a collection, such as `SHADER_SPECS`. The sunburst draws strength-1 wedges translucent.

| | base `7f8c0fb` | head `e071a61` |
|---|---|---|
| X3D 4.1 nodes written by export | 39 | **54** |
| X3D 4.1 nodes read by import | 42 | **68** |
| written and read (round-trippable at node level) | 26 | **43** |
| components touched | 14 | **20 of 37** |

**A finding that changes the method: the importer animates by ROUTE field names, not by node type.**
`importRoutesXML` builds channels from `fromField`/`toField` (`value_changed → set_translation | set_rotation |
set_scale`, `fraction_changed → set_fraction`, `value_changed → set_point`). It then reads `key`/`keyValue`
(width 4 for rotation, 3 otherwise) from *whatever node* is routed. The literals `PositionInterpolator`,
`OrientationInterpolator` and `TimeSensor` therefore never appear in a type check. The analyser adds them as reads
from ROUTE fields, and that addition is *inferred*. The consequence:

* a `SplinePositionInterpolator` or `EaseInEaseOut` chain imports as linear keys, with no warning;
* a `ScalarInterpolator` routed to `set_scale` would be read with width 3.

The field-name routing is elegant duck typing. It is also an untested edge.

| component | nodes | written (base -> head) | read (base -> head) | nodes written | nodes read |
|---|---|---|---|---|---|
| Rendering | 16 | 5 -> 7 | 13 -> 13 | Color, ColorRGBA, Coordinate, IndexedLineSet, IndexedTriangleSet, Normal, PointSet | Color, ColorRGBA, Coordinate, IndexedLineSet, IndexedTriangleFanSet, IndexedTriangleSet, IndexedTriangleStripSet, LineSet, Normal, PointSet, TriangleFanSet, TriangleSet, TriangleStripSet |
| Geometry2D | 8 | 2 -> 2 | 0 -> 8 | Circle2D, Rectangle2D | Arc2D, ArcClose2D, Circle2D, Disk2D, Polyline2D, Polypoint2D, Rectangle2D, TriangleSet2D |
| Core | 8 | 1 -> 7 | 0 -> 1 | MetadataBoolean, MetadataDouble, MetadataFloat, MetadataInteger, MetadataSet, MetadataString, WorldInfo | MetadataSet |
| Geometry3D | 7 | 5 -> 5 | 7 -> 7 | Box, Cone, Cylinder, IndexedFaceSet, Sphere | Box, Cone, Cylinder, ElevationGrid, Extrusion, IndexedFaceSet, Sphere |
| Shape | 10 | 5 -> 5 | 3 -> 6 | Appearance, Material, PhysicalMaterial, Shape, UnlitMaterial | Appearance, Material, PhysicalMaterial, Shape, TwoSidedMaterial, UnlitMaterial |
| Shaders | 8 | 3 -> 3 | 0 -> 3 | ComposedShader, FloatVertexAttribute, ShaderPart | ComposedShader, PackagedShader, ProgramShader |
| Texturing | 11 | 5 -> 5 | 5 -> 5 | ImageTexture, MovieTexture, PixelTexture, TextureCoordinate, TextureTransform | ImageTexture, MovieTexture, PixelTexture, TextureCoordinate, TextureTransform |
| Geospatial | 11 | 0 -> 0 | 0 -> 3 | - | GeoElevationGrid, GeoOrigin, GeoViewpoint |
| Grouping | 4 | 3 -> 2 | 1 -> 2 | Group, Transform | Switch, Transform |
| Interpolation | 13 | 0 -> 3 | 2 -> 3 | CoordinateInterpolator, OrientationInterpolator, PositionInterpolator | CoordinateInterpolator, OrientationInterpolator, PositionInterpolator |
| Lighting | 4 | 3 -> 3 | 3 -> 3 | DirectionalLight, PointLight, SpotLight | DirectionalLight, PointLight, SpotLight |
| Navigation | 7 | 3 -> 3 | 2 -> 2 | Collision, NavigationInfo, Viewpoint | NavigationInfo, Viewpoint |
| CADGeometry | 6 | 0 -> 0 | 0 -> 2 | - | IndexedQuadSet, QuadSet |
| EnvironmentalEffects | 5 | 2 -> 2 | 0 -> 1 | Background, Fog | Background |
| HAnim | 7 | 0 -> 2 | 0 -> 2 | HAnimHumanoid, HAnimJoint | HAnimHumanoid, HAnimJoint |
| Sound | 21 | 2 -> 2 | 2 -> 2 | AudioClip, Sound | AudioClip, Sound |
| Text | 3 | 0 -> 0 | 2 -> 2 | - | FontStyle, Text |
| GaussianSplats | 1 | 0 -> 1 | 0 -> 1 | GaussianSplats | GaussianSplats |
| Networking | 4 | 0 -> 1 | 1 -> 1 | Inline | Inline |
| Time | 1 | 0 -> 1 | 1 -> 1 | TimeSensor | TimeSensor |

Components with no node touched (17 of 37): CubeMapTexturing (3), DIS (6), EnvironmentalSensor (3), EventUtilities (7), Followers (14), KeyDeviceSensor (2), Layering (3), Layout (5), NURBS (13), ParticleSystems (10), Picking (5), PointingDeviceSensor (4), RigidBodyPhysics (14), Scripting (1), TextureProjection (2), Texturing3D (7), VolumeRendering (13).

**The dispatch table.** `import_x3d.geometry_importers` maps 28 X3D geometry nodes to builder functions. It is the
most reliable evidence of real import support, and the place to add new geometry.

### 2.2 Round-trip asymmetry (measured at node level, a lower bound at field level)

* **Read but never written (25 nodes).** Arc2D, ArcClose2D, Disk2D, Polyline2D, Polypoint2D, TriangleSet2D,
  ElevationGrid, Extrusion, GeoElevationGrid, GeoOrigin, GeoViewpoint, IndexedQuadSet, QuadSet, all six
  triangle/fan/strip sets, LineSet, Switch, Text, FontStyle, TwoSidedMaterial, and the two shader nodes the
  importer only recognises. A round trip turns all of these into `IndexedFaceSet`/`IndexedTriangleSet` (mesh) or
  lines. That is by design for a DCC tool, but worth stating: a `Switch` comes back as visibility, and a `Text`
  comes back as a mesh (the exporter treats `FONT` as mesh-like).
* **Written but never read (11 nodes).** Collision, Fog, Group, WorldInfo, ShaderPart, FloatVertexAttribute, and
  five `Metadata*` value nodes (only `MetadataSet` is matched on import). Fog and Collision come from the legacy
  writer.
* **Field level** (lower bound on the read side; import fields are attributed by function name, such as
  `importLamp_SpotLight`, so fields read in shared helpers are missed). `Background` is written with 11 fields
  (the six skybox `*Url`s, `skyAngle`, `groundColor` …). The importer keeps the sky and ground gradients and
  `transparency` on the scene for re-export (`importBackground`, read by hand), but not the six `*Url` fields. Light
  `attenuation`, `ambientIntensity` and `global` are written but not read back. `ElevationGrid` and `Extrusion`
  are read field by field but never written. Details are in `data/field_roundtrip.json`.

### 2.3 Blender data handled (measured literals and attribute chains)

* Object types compared: `MESH` (27 sites), `ARMATURE` 11, `LIGHT` 10, `EMPTY` 10, `FONT` 8, `CURVE` 6, `SURFACE`
  6, `CAMERA` 6, `POINTCLOUD` 5 (Blender 5.3 splats), `META` 4, `IMAGE` 4, `SPEAKER` 2. The 4.0 path treats
  `{MESH, CURVE, SURFACE, FONT}` as mesh-like (`extract.MESH_LIKE_TYPES`).
* `bpy.data` collections touched: meshes (53), objects (37), materials (18), fonts (16), scenes, images, curves,
  actions, collections, sounds, textures, lights, speakers, cameras, armatures, pointclouds.
* Shader nodes the importer creates by type: OutputMaterial, VertexColor, Math, BsdfTransparent, MixShader, RGB,
  Mix, LightPath, Emission, Mapping, TexCoord, TexImage, Value, SeparateColor. The Principled BSDF is reached
  through Blender's `node_shader_utils` wrapper, which a literal scan does not see.
* Bulk data paths: 37 functions use `foreach_get`/`foreach_set`. PR #25 added the two on the export side
  (`extract._read_all`, `_crease_from_sharp_edges`). The importer had them from the start.

### 2.4 Pipeline stages (roles assigned by hand per module, so inferred)

`ui` (registration, prefs, translations) → **export**: `export-classic` (legacy writer), `export-modern`
(pipeline, extract, material, emit, validate) → `ir` (dataclasses, registry, MFString) → **import**:
`import-classic` (import_x3d, geospatial, matrix_safety), `import-modern` (parse_x3d40, populate) → `bridge`
(glTF, splats, viewpoint FOV). The colours in every scene use this order. They are the dataviz reference palette's
dark steps, checked with its validator: all checks pass, and the worst adjacent CVD ΔE is 8.4.

## 3. Complexity and structure

| function | CC | lines | nesting | fork era |
|---|---|---|---|---|
| `export_x3d:export.writeIndexedFaceSet` | 94 | 400 | 9 | unchanged |
| `import_x3d:importMesh_IndexedFaceSet` | 79 | 248 | 4 | modified (CC 77 -> 79) |
| `import_x3d:importMesh_Extrusion` | 65 | 208 | 4 | unchanged |
| `import_x3d:importRoutesXML` | 54 | 144 | 4 | added |
| `import_x3d:load_web3d` | 53 | 199 | 5 | modified (CC 29 -> 53) |
| `import_x3d:finalize_light_units` | 50 | 161 | 3 | added |
| `import_x3d:importShape` | 47 | 128 | 3 | modified (CC 9 -> 47) |
| `import_x3d:appearance_CreatePBRMaterial` | 46 | 127 | 3 | added |
| `import_x3d:unlit_colour_material` | 43 | 79 | 3 | added |
| `extract:extract_scene` | 41 | 285 | 3 | modified (CC 33 -> 41) |
| `import_x3d:_import_coordinate_morphs` | 40 | 68 | 5 | added |
| `import_x3d:vrmlNode.__parse` | 38 | 162 | 7 | unchanged |
| `import_x3d:_import_skin_shape` | 36 | 95 | 4 | added |
| `export_x3d:export.writeMaterialH3D` | 32 | 277 | 6 | unchanged |
| `import_x3d:vrmlNode.getFieldName` | 32 | 67 | 9 | unchanged |

These things are measured.

* **One god function, complexity hidden in closures.** `export_x3d.export` spans 1,620 lines, but its own
  cyclomatic complexity is only 8. The complexity lives in its 29 nested writer closures, which share the outer
  function's state and together sum to CC 310 (298 at base). The largest is `writeIndexedFaceSet` (CC 94, 400 lines,
  unchanged). The fork era touched 8 of the closures (`writeSpotLight` 3 → 7, `writePointLight` 3 → 6,
  `export_main` 17 → 21, `writeMaterial` 8 → 9 …) through PRs #28–#31 (colour space, light units).
  *Correction:* an earlier version of this document said `export` had CC 287. That came from an analyser bug that
  charged the closures' statements to the outer function; it is fixed and every number here is recomputed.
* **Complexity is accreting into dispatchers.** `importShape` went from CC 9 to 47, `load_web3d` from 29 to 53 and
  `extract_scene` from 33 to 41 (its 4 closures add another 61). Each fidelity PR added a branch in the place that
  already knew the context. New functions are not more complex than old ones: the median CC is 4 for both, the mean
  7.6 for added functions vs 6.9 for older ones. The risk is concentrated in those dispatchers.
* **45 functions have CC > 20 and 5 have CC > 50** (all five in the importer or in `writeIndexedFaceSet`).
* **The fork era's footprint:** 249 functions added, 51 modified and 257 unchanged since `7f8c0fb`, by AST body
  hash. The code city colours these. Most of the legacy importer's geometry builders (`importMesh_Extrusion`,
  the triangle sets, the parser classes `vrmlNode`/`x3dNode`) were never touched.
* **Cross-module calls (inferred static resolution):** `export_x3d → extract` 13, `__init__ → translations` 8,
  `import_x3d → geospatial` 7, `extract → matrix_safety` 4, `import_x3d → mfstring` 4, `import_x3d → splat_native` 3.
  `matrix_safety` (PR #37) is already called from both directions. Of 697 call edges, 72 cross a module boundary.
* **Candidates for dead code (static, needs a human).** 18 public top-level functions have no resolved caller,
  for example `emit_x3d33.export_ir_scene`, `material.get_diffuse_color`/`get_emissive_color`,
  `splat_io.write_antimatter_splat`, `x3d_registry.get_node_spec` and `import_x3d.load_with_profiler`. Some are
  reached dynamically or from tools and tests. Treat the list as a review queue, not a verdict.
* **The first fork commit removed a hidden-Switch geometry library.** At base, `emit_x3d40` wrote
  `<Switch DEF="GeometryLibrary" whichChoice="-1">` to hold DEF'd geometry. `d3ad977` replaced it with
  DEF-at-first-use / USE-after, which is why the timeline shows `W- Switch` on that step.

## 4. The fork era, PR by PR

38 PRs on hagopjay/x3d-blender-io, **all merged, none open** (checked with `gh pr list --state all`). The
hagsmac fork has no PRs of its own; PRs #23–#25 came from hagsmac branches. On top of those, 4 commits were pushed
straight to main on 2026-10-08. Each row compares the merge commit's AST with its first parent's.

| step | date | what and why | AST delta (lines; functions +new -gone ~changed) | X3D coverage delta | tests (+new = total) | CI on main |
|---|---|---|---|---|---|---|
| [`d3ad977`](https://github.com/hagopjay/x3d-blender-io/commit/d3ad977) | 10-08 | **Add X3D 4.0 export path with PBR materials, full mesh data and DEF/USE**.  | +712; +35 -7 ~18 | R+ PhysicalMaterial, UnlitMaterial; W- Switch | +8 = 20 | - |
| [`420cfc3`](https://github.com/hagopjay/x3d-blender-io/commit/420cfc3) | 10-08 | **Honour X3D_STRICT_VALIDATION in the round-trip test**.  | no add-on change | - | 20 | - |
| [`fd87df7`](https://github.com/hagopjay/x3d-blender-io/commit/fd87df7) | 10-08 | **Write hierarchy, lights, cameras, text and animation on the X3D 4.0 path**.  | +344; +14 -1 ~7 | W+ OrientationInterpolator, PositionInterpolator, TimeSensor | +6 = 26 | - |
| [#1](https://github.com/hagopjay/x3d-blender-io/pull/1) | 10-08 | **Add CI, AI review workflows, contribution templates and CONTRIBUTING**. No automation: add CI (unit 3.11/3.13, bpy wheel, Blender 4.5/5.1/5.2 headless), AI review, templates. | no add-on change | - | 26 | success |
| [#2](https://github.com/hagopjay/x3d-blender-io/pull/2) | 10-08 | **Milestone 3: animation import from XML ROUTEs and HAnim export**. X3D 4.0 animation came back static and armatures were skipped: ROUTE import, HAnim 2.0 export. | +498; +15 -0 ~12 | W+ HAnimHumanoid, HAnimJoint | +3 = 30 | cancelled |
| [#3](https://github.com/hagopjay/x3d-blender-io/pull/3) | 10-08 | **Bump the actions group with 4 updates**. Dependabot: actions group bump. | no add-on change | - | 30 | success |
| [#4](https://github.com/hagopjay/x3d-blender-io/pull/4) | 10-08 | **Milestone 4a: import HAnim humanoids into armatures with skin and joint animation**. HAnimHumanoid imported as a static mesh: build armature, skin weights, joint animation. | +306; +8 -0 ~2 | R+ HAnimHumanoid, HAnimJoint | +1 = 31 | cancelled |
| [#5](https://github.com/hagopjay/x3d-blender-io/pull/5) | 10-08 | **Milestone 4b: Inline asset bridge (X3D, glTF, splat files) and X3D 4.1 GaussianSplats**. X3D as the scene graph that references glTF parts and splats: Inline bridge + 4.1 GaussianSplats. | +680; +32 -0 ~11; new `splat_io` | W+ GaussianSplats, Inline, PointSet; R+ GaussianSplats | +15 = 46 | success |
| [#6](https://github.com/hagopjay/x3d-blender-io/pull/6) | 10-10 | **Declare Shape and Geometry2D components when needed in X3D headers**. profile=Immersive without component statements failed x3d_mcp's profile check. | +25; +1 -0 ~1 | - | +3 = 49 | success |
| [#7](https://github.com/hagopjay/x3d-blender-io/pull/7) | 10-11 | **README: X_ITE renders the 4.1 GaussianSplats node**. README: X_ITE does render the 4.1 GaussianSplats node. | no add-on change | - | 49 | success |
| [#8](https://github.com/hagopjay/x3d-blender-io/pull/8) | 10-11 | **Fit emissiveColor, Viewpoint fieldOfView and Background to X3D 4.0**. emissiveColor > 1 broke the XSD; 16:9 cameras opened 1.8x too wide; Background fit. | +93; +6 -0 ~8; new `viewpoint_fov` | - | +5 = 54 | success |
| [#9](https://github.com/hagopjay/x3d-blender-io/pull/9) | 10-11 | **Export lights with global="true" so they light the scene**. Suns exported with global=false lit nothing in X_ITE. | +10; +0 -0 ~7 | - | 54 | cancelled |
| [#10](https://github.com/hagopjay/x3d-blender-io/pull/10) | 10-11 | **Own extension id (x3d_blender_io 2.6.0) and Blender 5.3 native splat export**. Own extension id 2.6.0; Blender 5.3 PointCloud splats export natively. | +194; +11 -0 ~4; new `splat_native` | - | +6 = 60 | success |
| [#11](https://github.com/hagopjay/x3d-blender-io/pull/11) | 10-11 | **Add a research showcase page with live X3D demos**. Research showcase page with live X3D demos (docs only). | no add-on change | - | 60 | success |
| [#12](https://github.com/hagopjay/x3d-blender-io/pull/12) | 10-11 | **Make the splat round trip exact at any size**. Imports of >= ~18k splats silently produced nothing (expat deferral); exact float32 round trip. | +91; +5 -0 ~6 | - | +8 = 68 | success |
| [#13](https://github.com/hagopjay/x3d-blender-io/pull/13) | 10-12 | **docs(showcase): drop the p = 0.017 claim from the Evolved Light tile**. Showcase: drop an unsupported p = 0.017 claim. | no add-on change | - | 68 | success |
| [#14](https://github.com/hagopjay/x3d-blender-io/pull/14) | 10-15 | **Bump actions/upload-artifact from 6 to 7 in the actions group**. Dependabot: upload-artifact 6 -> 7. | no add-on change | - | 68 | cancelled |
| [#15](https://github.com/hagopjay/x3d-blender-io/pull/15) | 10-15 | **Bridge fixes: light strength round trip, importer texture cache, export-import-export tests**. Light strength round trip, importer texture cache, export-import-export tests. | +7; +0 -0 ~5 | - | +6 = 74 | success |
| [#16](https://github.com/hagopjay/x3d-blender-io/pull/16) | 10-16 | **X3D 4.0 round trip: keep light intensity and shadows, Viewpoint descriptions, head meta, Shape metadata and Background**. Earth-twin round trip lost light intensity/shadows, Viewpoint descriptions, head meta, metadata, Background; AO false positive. | +378; +16 -0 ~14 | W+ MetadataBoolean, MetadataDouble, MetadataFloat, MetadataInteger, MetadataSet, MetadataString; R+ Background, MetadataSet | +28 = 102 | success |
| [#17](https://github.com/hagopjay/x3d-blender-io/pull/17) | 10-16 | **Import: animate every object under a routed Transform; add Rectangle2D and Disk2D**. Two shapes under one routed Transform crashed (UnboundLocalError); Rectangle2D, Disk2D. | +48; +2 -0 ~1 | R+ Disk2D, Rectangle2D | +3 = 105 | success |
| [#18](https://github.com/hagopjay/x3d-blender-io/pull/18) | 10-16 | **Import: show only the child an X3D Switch chooses**. Switch showed every child at once. | +43; +2 -0 ~1 | R+ Switch | +6 = 111 | success |
| [#19](https://github.com/hagopjay/x3d-blender-io/pull/19) | 10-16 | **Import: an UnlitMaterial shows emissiveColor times emissiveTexture**. UnlitMaterial emissiveTexture ignored emissiveColor. | +26; +1 -0 ~1 | - | +4 = 115 | success |
| [#20](https://github.com/hagopjay/x3d-blender-io/pull/20) | 10-16 | **Import: a texture's alpha makes the surface transparent**. Texture alpha only honoured for PhysicalMaterial + BLEND/MASK. | +55; +2 -0 ~2 | - | +6 = 121 | success |
| [#21](https://github.com/hagopjay/x3d-blender-io/pull/21) | 10-17 | **Shroud round-trip fixes: ElevationGrid colours import, lines survive X3D 4.0 export**. Shroud round trips: ElevationGrid colours, lines lost on 4.0 export. | +58; +2 -0 ~3 | W+ IndexedLineSet | +7 = 128 | success |
| [#22](https://github.com/hagopjay/x3d-blender-io/pull/22) | 10-17 | **Morphs both ways: CoordinateInterpolator to shape keys on import, shape keys to CoordinateInterpolator on export**. CoordinateInterpolator ROUTEs ignored: morphs both ways (shape keys). | +246; +5 -0 ~7 | W+ CoordinateInterpolator; R+ CoordinateInterpolator | +11 = 139 | success |
| [#23](https://github.com/hagopjay/x3d-blender-io/pull/23) | 10-18 | **Fix phantom <Sphere> for mesh objects that evaluate to no faces**. Face-less meshes exported a phantom grey <Sphere radius=0.75>. | +4; +0 -0 ~3 | - | +2 = 141 | cancelled |
| [#24](https://github.com/hagopjay/x3d-blender-io/pull/24) | 10-18 | **Add 194-case export conformance suite and CI job**. 194-case export conformance suite + CI job + answer key + golden GLSL target. | no add-on change | - | +4 = 145 | success+suite |
| [#25](https://github.com/hagopjay/x3d-blender-io/pull/25) | 10-26 | **Export: read per-corner attributes in bulk (315 s to 0.67 s on a 66k-vertex mesh)**. Per-corner attribute reads were quadratic: 315 s -> 0.67 s on a 66k-vertex mesh. | +28; +2 -0 ~4 | - | +2 = 147 | success+suite |
| [#26](https://github.com/hagopjay/x3d-blender-io/pull/26) | 11-12 | **Import fidelity: smooth primitives, X3D's Blinn-Phong specular, unlit lines and points, quads and Geometry2D**. x3d.demo through Unreal/Babylon/Cycles vs X_ITE: smooth primitives, Blinn-Phong, quads, Geometry2D. | +288; +16 -0 ~8 | R+ Arc2D, ArcClose2D, Circle2D, IndexedQuadSet, Polyline2D, Polypoint2D, QuadSet, TriangleSet2D, TwoSidedMaterial | +35 = 182 | success+suite |
| [#27](https://github.com/hagopjay/x3d-blender-io/pull/27) | 11-12 | **X3D colours and lines as X_ITE draws them: line and point colours, a Colour Space option, unlit surfaces without a material**. Line/point colours, Colour Space option, unlit surfaces without a material, as X_ITE draws them. | +306; +11 -0 ~14 | R+ ComposedShader, PackagedShader, ProgramShader | +11 = 192 | success+suite |
| [#28](https://github.com/hagopjay/x3d-blender-io/pull/28) | 11-12 | **Light units (X3D lights in glTF viewers as X_ITE draws them), ColorRGBA clamp, fidelity rig**. Point/spot lights 1.75 W per unit drew 30 where X_ITE draws 74: light units; fidelity rig. | +236; +8 -0 ~12 | - | +15 = 207 | success+suite |
| [#29](https://github.com/hagopjay/x3d-blender-io/pull/29) | 11-12 | **Colour round trip: the export writes colours back the way the import read them**. sRGB import had no way back: export Colour Space option. | +119; +5 -0 ~11 | - | +7 = 214 | success+suite |
| [#30](https://github.com/hagopjay/x3d-blender-io/pull/30) | 11-12 | **sRGB by default; classic lights fitted to what X_ITE draws; light-unit review fixes**. As Is default drew classic colours too bright; classic lights fitted to X_ITE. | +400; +13 -1 ~18 | - | +18 = 230 | success+suite |
| [#31](https://github.com/hagopjay/x3d-blender-io/pull/31) | 11-12 | **Unlit glb colours and ColorRGBA alpha; light-fit and light-colour fixes from the #30 review**. Filled UnlitMaterial + Color drew white in Babylon; ColorRGBA alpha; light fit review fixes. | +272; +10 -1 ~18 | - | +22 = 252 | success+suite |
| [#32](https://github.com/hagopjay/x3d-blender-io/pull/32) | 11-13 | **Export: drop unreadable emission masks; rig: Khronos glTF Validator step**. Procedural emission masks read as 'on': drop unreadable masks; glTF Validator step. | +46; +1 -0 ~1 | - | +5 = 257 | success+suite |
| [#33](https://github.com/hagopjay/x3d-blender-io/pull/33) | 11-13 | **Rig: glTF Validator gate and manifest; glb animation time; DEF identity in glb extras**. glb animation time from 0, DEF identity into glb extras, Validator gate + manifest. | +33; +1 -0 ~7 | - | +18 = 275 | success+suite |
| [#34](https://github.com/hagopjay/x3d-blender-io/pull/34) | 11-13 | **Add Group instances import option for EXT_mesh_gpu_instancing**. Group instances option so the glTF exporter writes EXT_mesh_gpu_instancing. | +55; +2 -0 ~3 | - | +4 = 279 | success+suite |
| [#35](https://github.com/hagopjay/x3d-blender-io/pull/35) | 11-13 | **Import GeoElevationGrid and GeoViewpoint; fix the stars-view import crash**. stars-view.x3d (scale 1e-16) crashed: float64 inverses; GeoElevationGrid, GeoViewpoint. | +379; +14 -0 ~6; new `geospatial` | R+ GeoElevationGrid, GeoOrigin, GeoViewpoint | +42 = 321 | success+suite |
| [#36](https://github.com/hagopjay/x3d-blender-io/pull/36) | 11-13 | **docs: single-page brag/showcase site for GitHub Pages (/docs)**. Single-page brag/showcase site under /docs (docs only). | no add-on change | - | 321 | success+suite |
| [#37](https://github.com/hagopjay/x3d-blender-io/pull/37) | 11-13 | **Fix stars-view glb scale: keep extreme Inline scales out of Blender's float32 inverses**. Extreme Inline scales left glb 1e8 too small: push scale to children. | +185; +12 -0 ~11; new `matrix_safety` | - | +8 = 329 | success+suite |
| [#38](https://github.com/hagopjay/x3d-blender-io/pull/38) | 11-13 | **Brag page v2: named star view as POC #1, live Blender showpieces**. Brag page v2 (docs only). | no add-on change | - | 329 | success+suite |

**The phases** (the bands in `fork-timeline.x3d`):

1. **Oct 8: the 4.0 path and Milestones 3–4.** PBR, DEF/USE, lights, cameras, sampled animation, HAnim both
   ways, Inline asset bridge, X3D 4.1 GaussianSplats. The largest structural growth: `extract` grew from 184 to
   about 800 lines.
2. **Oct 10–12: conformance to the spec and to X_ITE.** Component statements, `emissiveColor` clamping, FOV,
   `global="true"` lights, its own extension id, Blender 5.3 native splats, exact float32 splat round trips. The
   last of these fixed a silent empty import of ≥ 18k splats caused by expat's deferral.
3. **Oct 15–17: round-trip fidelity found by real scenes.** The earth-twin campus, the Library of Polyxandria and
   the Shroud scenes exposed light-intensity and shadow loss, metadata, Switch, unlit/alpha and morph gaps, each
   fixed with a bpy test.
4. **Oct 18–26: proof and performance.** The phantom-Sphere fix (#23), the 194-case conformance suite with its CI
   job (#24), and bulk attribute reads (#25, claimed 315 s → 0.67 s). Then 17 quiet days.
5. **Nov 12: "as X_ITE draws it".** Import fidelity against Unreal, Babylon.js and Cycles; X_ITE's colour
   model; light units fitted to X_ITE (claimed: a PointLight of 1 drew 30 where X_ITE draws 74); sRGB as the
   default. The busiest day for the importer: `finalize_light_units` (CC 54) and `fit_classic_lights` arrived.
6. **Nov 13: the glb leg and extremes.** The Khronos glTF Validator gate, DEF identity in glb extras, GPU
   instancing, `GeoElevationGrid`/`GeoViewpoint` (new `geospatial`), float64 inverses for 1e-16 scales (new
   `matrix_safety`). Plus the docs site.

## 5. How it is tested

* **Unit and bpy tests (measured with AST):** from 12 test functions in 3 files at base to **329 in 36 files**.
  The `*_bpy` modules need Blender's `bpy` wheel; CI runs them in the "Round-trip tests with the bpy wheel" job.
* **The PRs' own test counts check out.** The counts PR authors quote in their descriptions match the AST count
  of `test_*` functions at each merge:

  | PR | 8 | 12 | 15 | 18 | 19 | 20 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 37 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | claimed | 54 | 68 | 74 | 111 | 115 | 121 | 147 | 182 | 192 | 207 | 214 | 230 | 252 | 257 | 274 | 278+10 skip | 320 | 328+10 skip |
  | AST `test_*` | 54 | 68 | 74 | 111 | 115 | 121 | 147 | 182 | 192 | 207 | 214 | 230 | 252 | 257 | 275 | 279 | 321 | 329 |

  From #33 on, the AST count is one higher. That fits one `test_*` function that is not collected, or is skipped,
  outside the "skipped" figure. This is inferred, not checked.
* **CI on `main` (measured, `gh run list`).** There were 38 pushes to main. 33 runs succeeded, 5 were cancelled
  when the next merge started a new run, and **0 failed**. The jobs are: unit tests on Python 3.11 and 3.13 (ruff
  syntax errors block the job; undefined names are advisory "until the legacy exporter is cleaned up"); bpy-wheel
  round trips on Python 3.11 (the Khronos glTF Validator was added for the glb gate in #33); Blender 4.5.14, 5.1.2
  and 5.2.2 headless (build and validate the extension zip, install it into a clean profile, run the tests inside
  Blender); and since #24, **the export conformance suite on Blender 5.1.2, green in all 14 runs since it was
  added**.
* **The conformance suite (`tests/suite`), parsed with AST:** 19 zones (Z00 document … Z18 stress). There are 133
  literal `case()` calls (CORE 97, FIDELITY 17, ROADMAP 19) and 10 loop-generated case sites. At run time this
  gives the documented 194 cases (the CI step name says 195). The most common checks are transforms (`xf`, 34),
  XPath (22), mesh (18), roadmap (16) and textures (14). The suite exports with the checked-out `source/`
  (`--repo`), validates the file and fails on any CORE failure. A separate browser check (`x3d_browser_check.py`,
  X_ITE) exists but is not in CI.
* **Not covered by CI (measured from the workflow and the PR text).** Since #28 the PR authors have tested
  locally on **bpy 5.3.0**, but the CI matrix tops out at **5.2.2**. Code paths that only exist in Blender 5.3
  (native PointCloud splats from #10, `POINTCLOUD` handling) are therefore only tested on the authors' machines.
  The fidelity rig (`tools/fidelity_rig`, Playwright + X_ITE + Babylon.js + glTF Validator) also runs outside CI.

## 6. Insights

1. **The add-on is two exporters and one importer wearing one operator.** The legacy writer (`fw()` strings) and
   the IR path coexist. The legacy function is also the router, which is why its closures still form the tallest cluster after
   the 4.0 work.
2. **The IR is real on export and thin on import.** Export goes through dataclasses (`IRScene` … `IRHumanoid`).
   Import builds Blender data straight from the parse tree, and the IR is used only for Inlines. Feature work on
   import therefore lands in `import_x3d.py`: it grew 4,386 → 7,264 lines, and 2,878 of the 6,165 lines the fork
   added are there.
3. **Fidelity is defined by X_ITE.** Colour space, light units, unlit handling and line colours (#26–#31) all
   calibrate to how X_ITE draws, then carry that through glb to Babylon.js. This is a deliberate reference-renderer
   choice. It is visible in the code as functions named after it (`_x_ite_spot_factor`, `fit_classic_lights`).
4. **The tests grew 27×.** Source lines grew 1.6× and test functions 27×. Almost every PR from #15 on adds bpy
   tests, and several (#21, #22, #28, #32, #35) say in their text that the new tests fail on the previous main.
5. **Reading wins over writing.** Import touches 68 nodes and export 54. The gold caps in the sunburst show where
   the fork era added reach: Geometry2D, CAD quads, Geo*, Switch, TwoSidedMaterial on the read side;
   interpolators, HAnim, metadata, `GaussianSplats` and `Inline` on the write side.
6. **17 of 37 components are untouched**, including RigidBodyPhysics, NURBS, Followers, ParticleSystems,
   VolumeRendering, Layering/Layout and the sensors. RigidBodyPhysics matters to your other work: the
   x3d-physx-bridge writes RigidBodyCollection scenes, and no RigidBodyPhysics node is read here, so the physics
   would not survive an import (inferred: not run).

## 7. Risks and recommendations

| risk (evidence) | recommendation |
|---|---|
| `export_x3d.export`: 1,620 lines, 29 closures sharing state (sum CC 310), still changing (#28–#31) | Extract the 3.x writer from the 4.0 dispatcher. Move the closures to a module with an explicit writer context object, one PR per zone, and let the conformance suite be the safety net. |
| `importShape` CC 9 → 47, `load_web3d` 29 → 53, `extract_scene` 33 → 41 | Give each fidelity concern (colour space, unlit, light units) its own resolver called once per shape. Add a CI complexity gate on these three (e.g. `radon cc` or this repo's `tools/astlib.py`). |
| ROUTE import is duck-typed by field name | Check the node type of the routed source. Warn for spline/ease interpolators and for a `ScalarInterpolator` routed to `set_scale`. Add bpy tests for both. |
| Blender 5.3 paths are tested only locally | Add 5.3 to the Blender matrix once its headless build is cacheable, or mark the 5.3-only tests clearly as skipped in CI. |
| The X_ITE browser check and the fidelity rig are outside CI | Run `x3d_browser_check.py` as a nightly job with the pinned full-Chromium recipe from the x3d.poc smoke fix (headless-shell crashes on X_ITE's wasm pages, see the sibling note `smoke-ci-findings.md`). |
| Round-trip asymmetry (25 read-only, 11 write-only nodes; Background skybox URLs not read) | Publish the asymmetry as a table in the README. Reading `Background` URLs and `Fog` back is cheap and closes visible gaps. |
| 18 statically uncalled public functions | Review them: delete them or wire them up. `emit_x3d33.export_ir_scene` and `splat_io.write_antimatter_splat` look like stubs. |
| Branch hygiene (measured): 38 merged remote branches still exist on origin and fork; `origin/claude/project-thread-r9gvzh` has 1 unmerged commit (a glTF Validator script and measured scenes). Local `feat/x3d-test-suite` and `feat/export-suite-and-phantom-fix` are superseded (the AO fix landed independently in #16 as `35c4e63`). The local checkout is on `feat/export-suite-conformance`, 38 commits behind `origin/main`. | Decide on r9gvzh and delete the merged branches. Neither was done here. |

## 8. Method and limits

* `tools/astlib.py` parses each module with `ast` and records classes (with Blender bases and `bl_*` and
  `*Property` options), every `def` including methods and nested functions, imports (and whether they are lazy),
  McCabe complexity (`if`/loops/`except`/comprehension `if`s/boolean operators/`match` cases), block nesting
  depth (an `elif` counts at the depth of its `if`; an earlier version of this document counted each `elif` one level
  deeper and quoted `load_web3d` at depth 11, the corrected value is 5), a position-free body hash, calls, X3D vocabulary and Blender vocabulary.
* **Call resolution is static and partial:** bare names (local, nested, sibling-nested, imported), `self.`/`cls.`
  methods, `module.func` and `Class.method`. Dynamic dispatch (`geometry_importers[spec](...)`, callbacks,
  `getattr`) is not drawn as edges. The dispatch table is reported separately.
* `tools/era.py` re-runs the analysis on every first-parent commit of `origin/main` with `git show` (no checkout).
  `tools/coverage.py` holds the read/write rules; `tools/scenes.py` builds the scenes.
* There are 557 `def` statements and 554 unique qualified names. `export.writeIndexedFaceSet.vertex_key` is
  defined in several branches. The call graph uses unique names, the code city every `def`.
* **graphify** was not found on this Mac: not on PATH, not in pip, pipx, uv, brew or global npm, not in
  `~/Projects`, the Claude plugin folders or shell history. Nothing was installed. This teardown uses Python's
  `ast` directly.
* Rendering was checked in the Claude app's built-in browser (Chromium, software WebGL). Cold loads took up to
  about 35 s per scene with no slow network request (CPU-bound, probably font decoding and Text tessellation). A
  warm reload of the timeline took 2.4 s. This was not measured on a real GPU.

### Reproduce

```bash
cd ~/Projects/x3d/work/x3d-blender-io-masterclass
python3 tools/run_head.py head && python3 tools/coverage.py head   # needs snap/head (git archive origin/main source tests tools)
python3 tools/era.py            # ~90 s, reads git objects only
python3 tools/scenes.py && python3 tools/pr_table.py && python3 tools/doc_tables.py && python3 tools/build_doc.py
~/Projects/x3d/x3d_mcp/.venv/bin/python ~/Projects/x3d/work/x3d-physx-bridge/tools/validate_one.py scenes/*.x3d
python3 -m http.server 8817 --bind 127.0.0.1   # then open http://localhost:8817/
```
