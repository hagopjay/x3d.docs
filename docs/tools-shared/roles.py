"""Repos, refs and hand-assigned roles (inferred from directory names; documented in each MASTERCLASS.md)."""

LOOM_ORDER = ["webgpu", "physics", "drift", "kit", "brain", "mol", "platformer", "runs"]
LOOM_LABEL = {"webgpu": "x3d.webgpu (Babylon/WebGPU bridge, reader, ports)", "physics": "x3d.physics (PhysX + MuJoCo bridges, TMP ports)",
              "drift": "x3d.drift (KANSEI racing game)", "kit": "kit (loomkit gates, examples) + docs",
              "brain": "x3d.brain (imaging demo)", "mol": "x3d.mol (proteins, AlphaFold keyframes)",
              "platformer": "x3d.platformer (NIB)", "runs": "runs (recorded evidence)"}


def loom_role(path):
    top = path.split("/")[0]
    return {"x3d.webgpu": "webgpu", "x3d.physics": "physics", "x3d.drift": "drift", "x3d.brain": "brain", "x3d.mol": "mol",
            "x3d.platformer": "platformer", "runs": "runs"}.get(top, "kit")


DEMO_ORDER = ["webgpu", "xite", "hep", "physics", "stem", "shelf"]
DEMO_LABEL = {"webgpu": "Babylon/WebGPU ports", "xite": "X_ITE demos", "hep": "collider events + heritage facade",
              "physics": "physics (Ten Minute Physics, MuJoCo bridge)", "stem": "STEM studies", "shelf": "doc shelf (index, versions)"}


def demo_role(path):
    parts = path.split("/")
    if len(parts) < 3 or parts[0] != "docs" or parts[1] != "demos":
        return "shelf"
    d = parts[2]
    if "webgpu" in d or d in ("brain-torso",):
        return "webgpu"
    if d in ("collider-events", "heritage-facade"):
        return "hep"
    if d in ("ten-minute-physics", "x3d-mujoco-bridge"):
        return "physics"
    if d == "stem":
        return "stem"
    return "xite"


CFG = {
    "loom": {"path": "/Users/handshake/Projects/x3d/work/x3d.loom-physics", "ref": "origin/main", "repo": "hagopjay/x3d.loom",
             "role": loom_role, "order": LOOM_ORDER, "label": LOOM_LABEL},
    "demo": {"path": "/Users/handshake/Projects/x3d/work/x3d.demo", "ref": "upstream/main", "repo": "hagopjay/x3d.demo",
             "role": demo_role, "order": DEMO_ORDER, "label": DEMO_LABEL},
}


ONTO_ORDER = ["dynasty", "xdomain", "gobbler", "loom", "v2", "explorer", "sim", "docs"]
ONTO_LABEL = {"dynasty": "dynasty-loom (genealogy hypersphere)", "xdomain": "xdomain (fuzz, lawful metric, URDF/glTF, eval)",
              "gobbler": "Gobbler demiurge + v4", "loom": "Loom gates (loom, loom-feedback, tools, evidence)",
              "v2": "v2 Sun-Earth-Moon village", "explorer": "v1 explorer, harness, demo, data",
              "sim": "sim ontologies + proposal", "docs": "docs and root"}


def onto_role(path):
    top = path.split("/")[0]
    return {"dynasty-loom": "dynasty", "xdomain": "xdomain", "gobbler-demiurge": "gobbler", "gobbler-v4": "gobbler",
            "loom": "loom", "loom-feedback": "loom", "tools": "loom", "evidence": "loom", "v2": "v2", "assets": "v2",
            "harness": "explorer", "demo": "explorer", "data": "explorer", "out": "explorer", "scenes": "explorer",
            "explorer.html": "explorer", "constellation.html": "explorer", "sim": "sim", "proposal": "sim"}.get(top, "docs")


CFG["onto"] = {"path": "/Users/handshake/Projects/x3d/x3d.onto", "ref": "upstream/claude/project-thread-3mgt8g", "repo": "hagopjay/x3d.onto",
               "role": onto_role, "order": ONTO_ORDER, "label": ONTO_LABEL}


XITE_ORDER = ["nodes", "browser", "core", "rendering", "parser", "math", "api"]
XITE_LABEL = {"nodes": "Components: one module per X3D node type", "browser": "Browser: per-component machinery (contexts, renderers)",
              "core": "core: Fields, Base, Execution, Prototype, Routing, Configuration, IO", "rendering": "Rendering + GLSL shader sources",
              "parser": "Parser: XML, VRML, JSON, glTF, OBJ, STL, PLY, SVG ...", "math": "standard/: math, geometry, utility",
              "api": "API, registration, bundles"}
CFG["xite"] = {"path": None, "ref": "16.7.0", "repo": "create3000/x_ite", "order": XITE_ORDER, "label": XITE_LABEL,
               "role": lambda p: __import__("xite_ast").role(p)}
