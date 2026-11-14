"""AST teardown of the io_scene_x3d add-on (x3d-blender-io fork).

analyze_tree(files: dict[relpath -> source text]) -> dict  (JSON-serialisable)

Everything here is static: it reads Python source with `ast` and never imports the add-on.
X3D node/field/component names come from the X3D Unified Object Model 4.1 (x3d_mcp fork copy).
"""
from __future__ import annotations

import ast
import hashlib
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

UOM_PATH = "/Users/handshake/Projects/x3d/x3d_mcp/src/validation/schemas/X3dUnifiedObjectModel-4.1.xml"
UOM40_PATH = "/Users/handshake/Projects/x3d/x3d_mcp/src/validation/schemas/X3dUnifiedObjectModel-4.0.xml"

# ---------------------------------------------------------------- X3D vocabulary

def load_uom(path=UOM_PATH):
    root = ET.parse(path).getroot()
    nodes = {}
    for n in root.find("ConcreteNodes"):
        idef = n.find("InterfaceDefinition")
        ci = idef.find("componentInfo")
        inh = idef.find("Inheritance")
        fields = {f.get("name"): f.get("type") for f in idef.findall("field")}
        nodes[n.get("name")] = {
            "component": ci.get("name") if ci is not None else "?",
            "level": int(ci.get("level")) if ci is not None else 0,
            "base": inh.get("baseType") if inh is not None else None,
            "fields": fields,
        }
    statements = {}
    for s in root.find("Statements"):
        idef = s.find("InterfaceDefinition")
        fields = {f.get("name"): f.get("type") for f in idef.findall("field")} if idef is not None else {}
        statements[s.get("name")] = {"component": "Statements", "level": 0, "base": None, "fields": fields}
    return nodes, statements


X3D_NODES, X3D_STATEMENTS = load_uom()
X3D_NODES_40, _ = load_uom(UOM40_PATH)
X3D_ALL = {**X3D_STATEMENTS, **X3D_NODES}
# field names that are too generic to mean anything on their own
GENERIC_FIELDS = {"metadata", "IS", "DEF", "USE", "class", "id", "style", "name", "value", "type", "description",
                  "children", "url", "enabled", "title", "content", "on", "load", "level", "size", "version",
                  "profile", "info", "key", "values", "color", "point", "index", "length", "string", "family",
                  "scale", "center", "position", "radius", "height", "top", "bottom", "side", "solid", "ccw",
                  "translation", "rotation", "direction", "location", "intensity", "visible", "transparency",
                  "image", "repeatS", "repeatT", "texture", "geometry", "appearance", "material", "loop", "speed",
                  "pitch", "source", "fromNode", "toNode", "fromField", "toField", "address", "orientation"}
ALL_FIELD_NAMES = set()
for _n in X3D_ALL.values():
    ALL_FIELD_NAMES.update(_n["fields"])
ALL_FIELD_NAMES -= {"IS", "DEF", "USE", "class", "id", "style", "metadata", "containerField"}

RE_TAG = re.compile(r"<\s*([A-Za-z][A-Za-z0-9]*)")
RE_ATTR = re.compile(r"\b([A-Za-z][A-Za-z0-9]*)\s*=\s*[\"'{%]")

# ---------------------------------------------------------------- Blender vocabulary

BLENDER_OBJECT_TYPES = {"MESH", "CURVE", "SURFACE", "META", "FONT", "ARMATURE", "LATTICE", "EMPTY", "GPENCIL",
                        "CAMERA", "LIGHT", "SPEAKER", "LIGHT_PROBE", "VOLUME", "POINTCLOUD", "CURVES",
                        "GREASEPENCIL", "IMAGE"}
BLENDER_LIGHT_TYPES = {"POINT", "SUN", "SPOT", "AREA"}
BLENDER_KINDS = {"Operator": "Operator", "Panel": "Panel", "Menu": "Menu", "AddonPreferences": "AddonPreferences",
                 "PropertyGroup": "PropertyGroup", "FileHandler": "FileHandler", "UIList": "UIList",
                 "ImportHelper": "ImportHelper", "ExportHelper": "ExportHelper", "Gizmo": "Gizmo",
                 "GizmoGroup": "GizmoGroup", "Header": "Header"}

# ---------------------------------------------------------------- module roles (pipeline stage, hand-assigned)

def mcp_role(mod):
    """x3d_mcp: role by package (hand-assigned, documented)."""
    top = mod.split(".")[0]
    return {"server": "server", "tools": "mcp-tools", "validation": "validation", "x3d_utils": "x3d-utils",
            "transfer": "transfer", "playground": "playground", "dataset": "dataset-eval",
            "evaluation": "dataset-eval"}.get(top, "other")


ROLE_FN = mcp_role

MODULE_ROLE = {
    "__init__": ("ui", "Registration: operators, file handler, menus"),
    "prefs": ("ui", "Add-on preferences"),
    "translations": ("ui", "UI translation tables"),
    "export_x3d": ("export-classic", "Legacy X3D 3.x writer (fw() string emission) + 4.0 dispatch"),
    "export_pipeline": ("export-modern", "X3D 4.0 export orchestration: extract -> IR -> emit"),
    "extract": ("export-modern", "Blender scene -> IR (mesh, material, light, animation, HAnim)"),
    "emit_x3d40": ("export-modern", "IR -> X3D 4.0 XML text"),
    "emit_x3d33": ("export-modern", "X3D 3.3 header shim"),
    "material": ("export-modern", "Shader-node graph analysis -> PBR / Phong parameters"),
    "material_node_search": ("export-modern", "Shader node search helpers"),
    "validate": ("export-modern", "Post-export XML validation"),
    "ir": ("ir", "Intermediate representation (dataclasses) shared by both directions"),
    "x3d_registry": ("ir", "X3D component/profile registry for headers"),
    "mfstring": ("ir", "MFString quoting/parsing"),
    "import_x3d": ("import-classic", "Legacy VRML/X3D parser + Blender builder (geometry, shading, lights, animation, HAnim, Inline)"),
    "parse_x3d40": ("import-modern", "X3D 4.0 XML -> IR (Inline asset collection)"),
    "populate": ("import-modern", "IR -> Blender scene (Inline asset bridge)"),
    "bridge_gltf": ("bridge", "glTF/glb Inline import via Blender's glTF add-on"),
    "splat_io": ("bridge", "Gaussian-splat PLY/.splat read/write"),
    "splat_native": ("bridge", "Blender 5.3 native splat export"),
    "geospatial": ("import-classic", "Geo coordinate systems (GD/UTM/GC) for Geo* nodes"),
    "matrix_safety": ("import-classic", "float64 inverses for extreme-scale matrices"),
    "viewpoint_fov": ("bridge", "Viewpoint fieldOfView <-> Blender camera"),
}

READ_CALL_HINTS = ("getField", "getChild", "getChildren", "get", "find", "findall", "iter", "attrib",
                   "findSpec", "getSpec", "_attribute", "_attr", "_float", "_parse")

# ---------------------------------------------------------------- helpers

def dotted(node):
    """Best-effort dotted name for an expression (Name / Attribute chains / calls)."""
    parts = []
    while True:
        if isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        elif isinstance(node, ast.Name):
            parts.append(node.id)
            break
        elif isinstance(node, ast.Call):
            parts.append("()")
            node = node.func
        elif isinstance(node, ast.Subscript):
            parts.append("[]")
            node = node.value
        else:
            parts.append("?")
            break
    return ".".join(reversed(parts))


def set_parents(tree):
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child._parent = parent


DECISION_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp, ast.Assert,
                  ast.comprehension, ast.match_case)


def own_nodes(fn):
    """Walk a function body without descending into nested defs/classes (lambdas are kept)."""
    stack = list(fn.body) + list(fn.args.defaults) + list(fn.args.kw_defaults or [])
    stack = [s for s in stack if s is not None and not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    while stack:
        n = stack.pop()
        yield n
        for c in ast.iter_child_nodes(n):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            stack.append(c)


def complexity(fn):
    cc = 1
    for n in own_nodes(fn):
        if isinstance(n, DECISION_NODES):
            cc += 1
            if isinstance(n, ast.comprehension):
                cc += len(n.ifs)
        elif isinstance(n, ast.BoolOp):
            cc += len(n.values) - 1
    return cc


def max_depth(fn):
    best = 0

    def rec(stmts, d):
        nonlocal best
        for s in stmts:
            if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            blocks = []
            if isinstance(s, ast.If) and len(s.orelse) == 1 and isinstance(s.orelse[0], ast.If):
                best = max(best, d + 1)          # elif chain: the elif is not one level deeper
                rec(s.body, d + 1)
                rec(s.orelse, d)
                continue
            if isinstance(s, (ast.If, ast.For, ast.AsyncFor, ast.While)):
                blocks = [s.body, s.orelse]
            elif isinstance(s, (ast.With, ast.AsyncWith)):
                blocks = [s.body]
            elif isinstance(s, ast.Try) or (hasattr(ast, "TryStar") and isinstance(s, ast.TryStar)):
                blocks = [s.body, s.orelse, s.finalbody] + [h.body for h in s.handlers]
            elif isinstance(s, ast.Match):
                blocks = [c.body for c in s.cases]
            if blocks:
                best = max(best, d + 1)
                for b in blocks:
                    rec(b, d + 1)

    rec(fn.body, 0)
    return best


def body_hash(fn):
    """Hash of the function's AST without positions: equal hash == unchanged logic."""
    dumped = ast.dump(fn, annotate_fields=False, include_attributes=False)
    return hashlib.sha1(dumped.encode()).hexdigest()[:12]


def string_pieces(node):
    """(text, is_fstring_part) for str constants and f-string literal parts."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.JoinedStr):
        return [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
    return []


def literal_context(node):
    """Classify how an exact string literal is used."""
    p = getattr(node, "_parent", None)
    hops = 0
    while p is not None and hops < 4:
        if isinstance(p, ast.Compare):
            return "compare"
        if isinstance(p, ast.Dict):
            return "dict-key" if node in p.keys or any(_contains(k, node) for k in p.keys if k) else "dict-value"
        if isinstance(p, ast.Call):
            callee = dotted(p.func).split(".")[-1]
            if callee in ("frozenset", "set", "tuple", "list"):
                return "collection"
            return "call:" + callee
        if isinstance(p, ast.Subscript):
            return "subscript"
        if isinstance(p, (ast.Set, ast.Tuple, ast.List)):
            node, p, hops = p, getattr(p, "_parent", None), hops + 1
            continue
        if isinstance(p, (ast.Assign, ast.AnnAssign, ast.Return)):
            return "assign"
        break
    return "other"


def _contains(tree, target):
    return any(n is target for n in ast.walk(tree))


# ---------------------------------------------------------------- per-module analysis

def analyze_module(modname, text, role_map=MODULE_ROLE):
    tree = ast.parse(text)
    set_parents(tree)
    role = ROLE_FN(modname) if ROLE_FN else role_map.get(modname, ("other", ""))[0]
    mod = {
        "module": modname,
        "role": role,
        "role_desc": "",
        "loc": len(text.splitlines()),
        "doc": (ast.get_docstring(tree) or "").strip().split("\n")[0][:160],
        "imports": [],          # {target, names, lazy, relative}
        "classes": [],
        "functions": [],        # flat, including methods and nested
        "dispatch_tables": [],  # dicts keyed by X3D node name -> function
        "constants": [],        # module-level node-name sets (e.g. SMOOTH_PRIMITIVES)
    }

    # imports (top-level vs lazy)
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            lazy = not isinstance(getattr(n, "_parent", None), ast.Module)
            if isinstance(n, ast.Import):
                for a in n.names:
                    mod["imports"].append({"target": a.name, "names": [a.asname or a.name], "lazy": lazy, "relative": False})
            else:
                target = ("." * n.level) + (n.module or "")
                mod["imports"].append({"target": target, "names": [a.name for a in n.names],
                                       "alias": {a.asname or a.name: a.name for a in n.names},
                                       "lazy": lazy, "relative": n.level > 0})

    # module-level dispatch tables / node-name constants
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            name = st.targets[0].id
            v = st.value
            if isinstance(v, ast.Dict):
                pairs = []
                for k, val in zip(v.keys, v.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str) and k.value in X3D_ALL:
                        pairs.append([k.value, dotted(val)])
                if pairs:
                    mod["dispatch_tables"].append({"name": name, "line": st.lineno, "pairs": pairs})
            strs = [c.value for c in ast.walk(v) if isinstance(c, ast.Constant) and isinstance(c.value, str)]
            nodes_in = [s for s in strs if s in X3D_ALL]
            btypes = [x for x in strs if x in BLENDER_OBJECT_TYPES]
            if btypes and len(btypes) >= 2:
                mod.setdefault("blender_constants", []).append({"name": name, "line": st.lineno, "types": btypes})
            if nodes_in and not isinstance(v, ast.Dict) and len(nodes_in) >= 2:
                mod["constants"].append({"name": name, "line": st.lineno, "nodes": nodes_in})

    def visit_class(cls, prefix):
        bases = [dotted(b) for b in cls.bases]
        kinds = sorted({BLENDER_KINDS[b.split(".")[-1]] for b in bases if b.split(".")[-1] in BLENDER_KINDS})
        attrs, props = {}, []
        for st in cls.body:
            if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
                if st.targets[0].id.startswith("bl_") and isinstance(st.value, ast.Constant):
                    attrs[st.targets[0].id] = st.value.value
                elif st.targets[0].id.startswith("bl_") and isinstance(st.value, (ast.Set, ast.Tuple)):
                    attrs[st.targets[0].id] = [e.value for e in st.value.elts if isinstance(e, ast.Constant)]
            if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name) and isinstance(st.annotation, ast.Call):
                ptype = dotted(st.annotation.func).split(".")[-1]
                if ptype.endswith("Property"):
                    kw = {k.arg: (k.value.value if isinstance(k.value, ast.Constant) else dotted(k.value)) for k in st.annotation.keywords}
                    props.append({"name": st.target.id, "type": ptype, "label": kw.get("name"), "default": kw.get("default")
                                  if isinstance(kw.get("default"), (str, int, float, bool, type(None))) else str(kw.get("default"))})
        decos = [dotted(d.func if isinstance(d, ast.Call) else d) for d in cls.decorator_list]
        qual = prefix + cls.name
        mod["classes"].append({"name": cls.name, "qualname": qual, "line": cls.lineno, "end": cls.end_lineno,
                               "bases": bases, "blender_kind": kinds, "bl": attrs, "props": props,
                               "decorators": decos, "dataclass": any("dataclass" in d for d in decos),
                               "methods": [b.name for b in cls.body if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))],
                               "doc": (ast.get_docstring(cls) or "").split("\n")[0][:160]})
        for st in cls.body:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit_func(st, qual + ".", cls_name=qual)
            elif isinstance(st, ast.ClassDef):
                visit_class(st, qual + ".")

    def visit_func(fn, prefix, cls_name=None, parent_fn=None):
        qual = prefix + fn.name
        calls, x3d_tokens, blender, diags = [], [], Counter(), []
        bulk = Counter()
        for n in own_nodes(fn):
            if isinstance(n, ast.Call):
                d = dotted(n.func)
                calls.append(d)
                if d.split(".")[-1] == "Diagnostic":
                    vals = [a.value if isinstance(a, ast.Constant) else None for a in n.args[:2]]
                    kw = {k.arg: (k.value.value if isinstance(k.value, ast.Constant) else None) for k in n.keywords}
                    level = vals[0] if vals and vals[0] else kw.get("level")
                    check = vals[1] if len(vals) > 1 and vals[1] else kw.get("check")
                    for k in n.keywords:
                        if k.arg == "check" and isinstance(k.value, ast.JoinedStr):
                            check = "".join(v.value if isinstance(v, ast.Constant) else "*" for v in k.value.values)
                        if k.arg == "level" and isinstance(k.value, ast.IfExp):
                            level = "/".join(str(x.value) for x in (k.value.body, k.value.orelse) if isinstance(x, ast.Constant))
                    diags.append([level, check, n.lineno])
                if d.split(".")[-1] != "Diagnostic" and len(n.args) >= 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in n.args[:2]) \
                        and n.args[0].value in ("error", "warning", "info") and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", n.args[1].value):
                    diags.append([n.args[0].value, n.args[1].value, n.lineno])  # helper reporter: report("error", "physics-mass", ...)
                elif d.split(".")[-1] in ("err", "add", "report", "warn") and any(
                        isinstance(a, ast.Constant) and isinstance(a.value, str) and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", a.value) for a in n.args):
                    ck = next(a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", a.value))
                    lv = next((a.value for a in n.args if isinstance(a, ast.Constant) and a.value in ("error", "warning", "info")), "(helper)")
                    diags.append([lv, ck, n.lineno])
                _parts = d.split(".")
                if _parts[-1] in X3D_ALL and _parts[-1][:1].isupper() and (len(_parts) == 1 or _parts[0] in ("x3d", "x3d_mod", "x3dpy")):
                    x3d_tokens.append(("node", _parts[-1], "emit-x3dpy", n.lineno))  # x3d.py object construction
                if d.split(".")[-1] == "SubElement" and len(n.args) >= 2 and isinstance(n.args[1], ast.Constant) \
                        and isinstance(n.args[1].value, str) and n.args[1].value in X3D_ALL:
                    x3d_tokens.append(("node", n.args[1].value, "emit-tag", n.lineno))
                last = d.split(".")[-1]
                if last in ("foreach_get", "foreach_set"):
                    bulk[last] += 1
                if last == "new" and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                    if n.args[0].value.startswith(("ShaderNode", "NodeSocket", "GeometryNode", "CompositorNode")):
                        blender["node:" + n.args[0].value] += 1
                for k in n.keywords:
                    if k.arg == "type" and isinstance(k.value, ast.Constant) and isinstance(k.value.value, str):
                        if k.value.value.startswith(("ShaderNode", "GeometryNode")):
                            blender["node:" + k.value.value] += 1
                if d.startswith("bpy.ops."):
                    blender["op:" + ".".join(d.split(".")[2:4])] += 1
            if isinstance(n, ast.Attribute):
                d = dotted(n)
                if d.startswith("bpy.data.") and len(d.split(".")) >= 3:
                    blender["data:" + d.split(".")[2]] += 1
                elif d.startswith("bpy.types.") and len(d.split(".")) >= 3:
                    blender["type:" + d.split(".")[2]] += 1
            if isinstance(n, ast.Compare):
                sides = [n.left] + list(n.comparators)
                attr_side = [s for s in sides if isinstance(s, ast.Attribute) and s.attr in ("type", "bl_idname", "rotation_mode", "blend_method", "interpolation")]
                if attr_side:
                    for s in sides:
                        for c in ast.walk(s):
                            if isinstance(c, ast.Constant) and isinstance(c.value, str) and c.value.isupper():
                                kind = attr_side[0].attr
                                if c.value in BLENDER_OBJECT_TYPES and kind == "type":
                                    blender["obj:" + c.value] += 1
                                elif c.value in BLENDER_LIGHT_TYPES and kind == "type":
                                    blender["light:" + c.value] += 1
                                else:
                                    blender["enum:" + kind + "=" + c.value] += 1
            # X3D vocabulary
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                s = n.value
                if isinstance(getattr(n, "_parent", None), ast.JoinedStr):
                    ctx = "fstring"
                else:
                    ctx = None
                for tag in RE_TAG.findall(s):
                    if tag in X3D_ALL:
                        x3d_tokens.append(("node", tag, "emit-tag", n.lineno))
                for attr in RE_ATTR.findall(s):
                    if attr in ALL_FIELD_NAMES:
                        x3d_tokens.append(("field", attr, "emit-attr", n.lineno))
                if ctx is None:
                    lc = literal_context(n)
                    if s in BLENDER_OBJECT_TYPES and lc in ("compare", "collection"):
                        blender["obj:" + s] += 1
                    if s in X3D_ALL:
                        x3d_tokens.append(("node", s, lc, n.lineno))
                    elif s in ALL_FIELD_NAMES:
                        x3d_tokens.append(("field", s, lc, n.lineno))
        cc = complexity(fn)
        rec = {
            "qualname": qual, "name": fn.name, "class": cls_name, "parent_fn": parent_fn,
            "line": fn.lineno, "end": fn.end_lineno, "loc": fn.end_lineno - fn.lineno + 1,
            "args": len(fn.args.args) + len(fn.args.kwonlyargs) + len(fn.args.posonlyargs),
            "cc": cc, "depth": max_depth(fn), "hash": body_hash(fn),
            "returns": sum(1 for n in own_nodes(fn) if isinstance(n, ast.Return)),
            "doc": (ast.get_docstring(fn) or "").split("\n")[0][:160],
            "calls_raw": calls, "x3d": x3d_tokens, "diags": diags, "blender": dict(blender), "bulk": dict(bulk),
            "decorators": [dotted(d.func if isinstance(d, ast.Call) else d) for d in fn.decorator_list],
        }
        mod["functions"].append(rec)
        # nested defs
        for st in ast.walk(fn):
            if st is fn:
                continue
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and _direct_parent_def(st) is fn:
                visit_func(st, qual + ".", cls_name=cls_name, parent_fn=qual)
            elif isinstance(st, ast.ClassDef) and _direct_parent_def(st) is fn:
                visit_class(st, qual + ".")

    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visit_func(st, "")
        elif isinstance(st, ast.ClassDef):
            visit_class(st, "")
    return mod


def _direct_parent_def(node):
    p = getattr(node, "_parent", None)
    while p is not None and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
        p = getattr(p, "_parent", None)
    return p


# ---------------------------------------------------------------- whole-package analysis

def analyze_tree(files):
    """files: {modname: text} for the add-on package (source/*.py)."""
    mods = {}
    errors = {}
    for name, text in files.items():
        try:
            mods[name] = analyze_module(name, text)
        except SyntaxError as e:
            errors[name] = str(e)
    resolve_calls(mods)
    return {"modules": mods, "errors": errors}


def resolve_calls(mods):
    """Resolve calls_raw to package-internal function ids 'module:qualname'. Heuristic, documented in the report."""
    defs = {}          # module -> {qualname}
    top = {}           # module -> {toplevel name -> qualname}
    classes = {}       # module -> {class qualname -> [methods]}
    for m, d in mods.items():
        defs[m] = {f["qualname"] for f in d["functions"]}
        top[m] = {f["name"]: f["qualname"] for f in d["functions"] if f["class"] is None and f["parent_fn"] is None}
        for c in d["classes"]:
            top[m].setdefault(c["name"], c["qualname"])
        classes[m] = {c["qualname"]: c for c in d["classes"]}
    for m, d in mods.items():
        # name -> (module, name) from relative imports
        imported_names, imported_mods = {}, {}
        for imp in d["imports"]:
            if imp.get("relative"):
                tmod = imp["target"].lstrip(".")
                if tmod:
                    for local, orig in imp.get("alias", {}).items():
                        imported_names[local] = (tmod, orig)
                else:  # from . import x
                    for local, orig in imp.get("alias", {}).items():
                        imported_mods[local] = orig
        for f in d["functions"]:
            resolved, external = [], Counter()
            nested = {g["name"]: g["qualname"] for g in d["functions"] if g["parent_fn"] == f["qualname"]}
            sibling_nested = {}
            if f["parent_fn"]:
                sibling_nested = {g["name"]: g["qualname"] for g in d["functions"] if g["parent_fn"] == f["parent_fn"]}
            for c in f["calls_raw"]:
                parts = c.split(".")
                target = None
                if len(parts) == 1:
                    n = parts[0]
                    if n in nested:
                        target = (m, nested[n])
                    elif n in sibling_nested:
                        target = (m, sibling_nested[n])
                    elif n in top[m]:
                        target = (m, top[m][n])
                    elif n in imported_names:
                        tm, tn = imported_names[n]
                        if tm in top and tn in top[tm]:
                            target = (tm, top[tm][tn])
                    if target and target[1] in classes.get(target[0], {}):
                        init = target[1] + ".__init__"
                        target = (target[0], init) if init in defs[target[0]] else None
                elif parts[0] in ("self", "cls") and len(parts) == 2 and f["class"]:
                    cand = f["class"] + "." + parts[1]
                    if cand in defs[m]:
                        target = (m, cand)
                    else:  # look in package base classes
                        for b in classes[m].get(f["class"], {}).get("bases", []):
                            if b in top[m] and top[m][b] + "." + parts[1] in defs[m]:
                                target = (m, top[m][b] + "." + parts[1])
                elif len(parts) == 2 and parts[0] in imported_mods:
                    tm = imported_mods[parts[0]]
                    if tm in top and parts[1] in top[tm]:
                        target = (tm, top[tm][parts[1]])
                elif len(parts) == 2 and parts[0] in top[m]:  # Class.staticmethod
                    cand = top[m][parts[0]] + "." + parts[1]
                    if cand in defs[m]:
                        target = (m, cand)
                if target:
                    resolved.append(target[0] + ":" + target[1])
                else:
                    root = parts[0]
                    if root in ("bpy", "mathutils", "bmesh", "numpy", "np", "math", "os", "re", "xml", "ET",
                                "struct", "json", "gzip", "zipfile", "urllib", "addon_utils", "bpy_extras", "logging"):
                        external[".".join(parts[:3])] += 1
                    else:
                        external["<method>." + parts[-1]] += 1
            f["calls"] = sorted(set(resolved))
            f["calls_count"] = Counter(resolved)
            f["external"] = dict(external)
    return mods


# ---------------------------------------------------------------- test analysis

def analyze_tests(files):
    """files: {relpath: text} for tests/*.py. Returns test inventory and which add-on modules each test file imports."""
    out = {}
    for path, text in files.items():
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        tests = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test")]
        targets = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module:
                tail = n.module.split(".")[-1]
                if tail in MODULE_ROLE:
                    targets.add(tail)
                for a in n.names:
                    if a.name in MODULE_ROLE:
                        targets.add(a.name)
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name.split(".")[-1] in MODULE_ROLE:
                        targets.add(a.name.split(".")[-1])
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                m = re.match(r"(?:source|io_scene_x3d|x3d_blender_io)[./]([a-z_0-9]+)", n.value)
                if m and m.group(1) in MODULE_ROLE:
                    targets.add(m.group(1))
        out[path] = {"tests": tests, "n": len(tests), "targets": sorted(targets), "loc": len(text.splitlines()),
                     "bpy": "bpy" in text}
    return out


# ---------------------------------------------------------------- generalised resolver (dotted module names, absolute imports)

def _abs_target(cur_mod, imp):
    """Absolute dotted module for an import record from module cur_mod."""
    t = imp["target"]
    if not imp.get("relative"):
        return t
    level = len(t) - len(t.lstrip("."))
    pkg = cur_mod.split(".")[:-1]
    if level > 1:
        pkg = pkg[: len(pkg) - (level - 1)]
    rest = t.lstrip(".")
    return ".".join([p for p in pkg + ([rest] if rest else []) if p])


def resolve_calls(mods):  # noqa: F811  (replaces the add-on-specific resolver above)
    defs, top, classes = {}, {}, {}
    for m, d in mods.items():
        defs[m] = {f["qualname"] for f in d["functions"]}
        top[m] = {f["name"]: f["qualname"] for f in d["functions"] if f["class"] is None and f["parent_fn"] is None}
        for c in d["classes"]:
            top[m].setdefault(c["name"], c["qualname"])
        classes[m] = {c["qualname"]: c for c in d["classes"]}

    def find_mod(name):
        if name in mods:
            return name
        for cand in (name.split(".", 1)[1] if "." in name else None,):  # e.g. src.validation.semantic
            if cand and cand in mods:
                return cand
        return None

    for m, d in mods.items():
        names, modalias = {}, {}
        for imp in d["imports"]:
            if "alias" in imp:  # from X import a as b
                base = _abs_target(m, imp)
                for local, orig in imp["alias"].items():
                    sub = find_mod((base + "." + orig) if base else orig)
                    if sub:
                        modalias[local] = sub
                    else:
                        bm = find_mod(base)
                        if bm:
                            names[local] = (bm, orig)
            else:  # import a.b [as c]
                tm = find_mod(imp["target"])
                if tm:
                    modalias[imp["names"][0]] = tm
        for f in d["functions"]:
            resolved, external = [], Counter()
            nested = {g["name"]: g["qualname"] for g in d["functions"] if g["parent_fn"] == f["qualname"]}
            sib = {g["name"]: g["qualname"] for g in d["functions"] if f["parent_fn"] and g["parent_fn"] == f["parent_fn"]}
            for c in f["calls_raw"]:
                parts = c.split(".")
                target = None
                if len(parts) == 1:
                    n = parts[0]
                    if n in nested:
                        target = (m, nested[n])
                    elif n in sib:
                        target = (m, sib[n])
                    elif n in top[m]:
                        target = (m, top[m][n])
                    elif n in names and names[n][1] in top.get(names[n][0], {}):
                        target = (names[n][0], top[names[n][0]][names[n][1]])
                    if target and target[1] in classes.get(target[0], {}):
                        init = target[1] + ".__init__"
                        target = (target[0], init) if init in defs[target[0]] else None
                elif parts[0] in ("self", "cls") and len(parts) == 2 and f["class"]:
                    cand = f["class"] + "." + parts[1]
                    if cand in defs[m]:
                        target = (m, cand)
                elif parts[0] in modalias and len(parts) == 2:
                    tm = modalias[parts[0]]
                    if parts[1] in top[tm]:
                        target = (tm, top[tm][parts[1]])
                elif len(parts) == 2 and parts[0] in top[m]:
                    cand = top[m][parts[0]] + "." + parts[1]
                    if cand in defs[m]:
                        target = (m, cand)
                if target:
                    resolved.append(target[0] + ":" + target[1])
                else:
                    external[".".join(parts[:2])] += 1
            f["calls"] = sorted(set(resolved))
            f["calls_count"] = Counter(resolved)
            f["external"] = dict(external)
    return mods


def module_files(root, pkgs=("src", "playground", "dataset", "evaluation")):
    """{dotted module name: text}. src/ is a sys.path root (imports say 'validation.semantic'); other dirs are packages."""
    import pathlib
    out = {}
    root = pathlib.Path(root)
    for pkg in pkgs:
        base = root / pkg
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.py")):
            rel = p.relative_to(root / "src" if pkg == "src" else root).with_suffix("")
            parts = list(rel.parts)
            if parts[-1] == "__init__":
                parts = parts[:-1] or ["__init__"]
                if pkg == "src" and parts == ["__init__"]:
                    parts = ["src_init"]
            out[".".join(parts)] = p.read_text(encoding="utf-8")
    return out


def analyze_tests_mcp(files, modnames):
    out = {}
    for path, text in files.items():
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        tests = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test")]
        targets = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module:
                mod = n.module[4:] if n.module.startswith("src.") else n.module
                if mod in modnames:
                    targets.add(mod)
                for a in n.names:
                    if f"{mod}.{a.name}" in modnames:
                        targets.add(f"{mod}.{a.name}")
            if isinstance(n, ast.Import):
                for a in n.names:
                    mod = a.name[4:] if a.name.startswith("src.") else a.name
                    if mod in modnames:
                        targets.add(mod)
        out[path] = {"tests": tests, "n": len(tests), "targets": sorted(targets), "loc": len(text.splitlines())}
    return out
