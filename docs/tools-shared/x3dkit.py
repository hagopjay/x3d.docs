"""Shared X3D scene kit (copied from the x3d-blender-io masterclass, constants adapted to x3d_mcp).

scenes/callgraph-3d.x3d     module + call graph, 3D force layout (functions as spheres)
scenes/coverage-sunburst.x3d X3D 4.1 node coverage: components -> nodes, written ring and read ring
scenes/fork-timeline.x3d    42 snapshots of origin/main: LOC, tests and X3D coverage per PR
scenes/code-city.x3d        modules as districts, functions as buildings (height = cyclomatic complexity)
"""
import json
import math
import pathlib
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import astlib  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "scenes"
OUT.mkdir(exist_ok=True)
HEAD_SHA = subprocess.run(["git", "-C", "/Users/handshake/Projects/x3d/x3d_mcp", "rev-parse", "origin/main"],
                          capture_output=True, text=True).stdout.strip()
GH = f"https://github.com/hagopjay/x3d_mcp/blob/{HEAD_SHA}/"

# dataviz reference palette, dark steps, fixed order (validated: scripts/validate_palette.js --mode dark, all pass)
ROLE_ORDER = ["validation", "mcp-tools", "x3d-utils", "transfer", "server", "playground", "dataset-eval"]
ROLE_COLOR = dict(zip(ROLE_ORDER, ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9"]))
ROLE_LABEL = {"validation": "validation (XSD, semantic rules, hints, repair)", "mcp-tools": "MCP tools and prompts",
              "x3d-utils": "x3d_utils (scene builder, X3DUOM, ontology)", "transfer": "transfer layer (blobs, splats, jobs)",
              "server": "FastMCP server", "playground": "Accountability Playground (web app)",
              "dataset-eval": "dataset generators + evaluation"}
NEUTRAL = "#383835"
TEXT = "#f0efec"
TEXT2 = "#c3c2b7"
WRITE_C, READ_C, GAIN_C = "#d95926", "#3987e5", "#c98500"
GOOD, CANCEL = "#0ca30c", "#8a8a85"


def rgb(h, k=1.0):
    h = h.lstrip("#")
    return " ".join(f"{min(1.0, int(h[i:i + 2], 16) / 255 * k):.3f}" for i in (0, 2, 4))


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            .replace("'", "&apos;"))


def mf(*items):
    """MFString attribute value (goes inside a double-quoted XML attribute)."""
    return " ".join("&quot;" + esc(str(i).replace('"', "").replace("\\", "/")) + "&quot;" for i in items)


def f3(v):
    return " ".join(f"{x:.3f}" for x in v)


def header(title, desc, extra_meta=()):
    metas = "\n".join(f'    <meta name="{esc(k)}" content="{esc(v)}"/>' for k, v in
                      [("title", title), ("description", desc), ("creator", "Claude Code (Opus 5.5), x3d_mcp masterclass"),
                       ("generator", "tools/scenes.py (static Python ast analysis, no add-on code executed)"),
                       ("reference", f"https://github.com/hagopjay/x3d_mcp/tree/{HEAD_SHA}"),
                       ("created", "2026-11-13"), *extra_meta])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">
<X3D profile="Immersive" version="4.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.0.xsd">
  <head>
{metas}
  </head>
  <Scene>
"""


FOOTER = "  </Scene>\n</X3D>\n"


def look_at(pos, target):
    """Viewpoint orientation (axis angle) looking from pos to target with +Y up."""
    pos, target = np.array(pos, float), np.array(target, float)
    f = target - pos
    f /= np.linalg.norm(f)
    up = np.array([0, 1.0, 0])
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    m = np.array([r, u, -f]).T  # columns: camera x, y, z in world
    angle = math.acos(max(-1.0, min(1.0, (np.trace(m) - 1) / 2)))
    if abs(angle) < 1e-6:
        return "0 0 1 0"
    axis = np.array([m[2, 1] - m[1, 2], m[0, 2] - m[2, 0], m[1, 0] - m[0, 1]])
    n = np.linalg.norm(axis)
    if n < 1e-9:  # 180 degrees
        axis = np.sqrt(np.maximum(np.diag(m) + 1, 0) / 2)
        n = np.linalg.norm(axis)
    axis /= n
    return f"{axis[0]:.4f} {axis[1]:.4f} {axis[2]:.4f} {angle:.4f}"


def viewpoint(desc, pos, target, fov=0.785, def_=None):
    d = f' DEF="{def_}"' if def_ else ""
    return (f'    <Viewpoint{d} description="{esc(desc)}" position="{f3(pos)}" orientation="{look_at(pos, target)}" '
            f'centerOfRotation="{f3(target)}" fieldOfView="{fov}"/>\n')


def label(text_lines, pos, size=0.5, color=TEXT, justify="MIDDLE", billboard=True, family="SANS", style="PLAIN"):
    lines = text_lines if isinstance(text_lines, (list, tuple)) else [text_lines]
    shape = (f'<Shape><Appearance><Material diffuseColor="0 0 0" emissiveColor="{rgb(color)}"/></Appearance>'
             f'<Text string="{mf(*lines)}"><FontStyle family="{mf(family)}" style="{style}" justify="{mf(justify, "MIDDLE")}" '
             f'size="{size}"/></Text></Shape>')
    if billboard:
        return f'    <Transform translation="{f3(pos)}"><Billboard axisOfRotation="0 0 0">{shape}</Billboard></Transform>\n'
    return f'    <Transform translation="{f3(pos)}">{shape}</Transform>\n'


def flat_label(text, pos, yaw, size=0.3, color=TEXT, justify="BEGIN"):
    """Text lying on the XZ plane, baseline along direction yaw (radians, CCW seen from above)."""
    return (f'    <Transform translation="{f3(pos)}" rotation="0 1 0 {yaw:.4f}"><Transform rotation="1 0 0 -1.5708">'
            f'<Shape><Appearance><Material diffuseColor="0 0 0" emissiveColor="{rgb(color)}"/></Appearance>'
            f'<Text string="{mf(text)}"><FontStyle family="{mf("SANS")}" justify="{mf(justify, "MIDDLE")}" size="{size}"/></Text>'
            f'</Shape></Transform></Transform>\n')


def materials(defs):
    """defs: {DEF: (hex, transparency)} -> DEF'd Material nodes inside an invisible holder Switch."""
    return ""  # materials are DEF'd at first use instead (see Mat)


class Mat:
    """DEF a Material the first time, USE it afterwards (DEF always precedes USE in document order)."""

    def __init__(self):
        self.seen = set()

    def __call__(self, name, hexc, transparency=0.0, emissive=0.45, diffuse=0.75):
        if name in self.seen:
            return f'<Material USE="{name}"/>'
        self.seen.add(name)
        t = f' transparency="{transparency}"' if transparency else ""
        return (f'<Material DEF="{name}" diffuseColor="{rgb(hexc, diffuse)}" emissiveColor="{rgb(hexc, emissive)}" '
                f'specularColor="0.15 0.15 0.15" shininess="0.3"{t}/>')


class Geo:
    def __init__(self):
        self.seen = set()

    def __call__(self, name, xml):
        if name in self.seen:
            tag = xml.split()[0].lstrip("<")
            return f"<{tag} USE=\"{name}\"/>"
        self.seen.add(name)
        return xml.replace("<", f"<", 1).replace(" ", f' DEF="{name}" ', 1)


def background():
    return ('    <Background skyColor="0.067 0.067 0.063 0.10 0.10 0.095" skyAngle="1.5708" '
            'groundColor="0.067 0.067 0.063" />\n'
            '    <NavigationInfo type=\'"EXAMINE" "ANY"\' headlight="true" speed="4"/>\n')


def load(name):
    return json.load(open(DATA / name))




def wedge(r0, r1, a0, a1, h, steps=None):
    """Extruded annular sector as IndexedFaceSet points + faces (angles in radians, CCW from +X seen from above)."""
    steps = steps or max(1, int((a1 - a0) / 0.05) + 1)
    ang = np.linspace(a0, a1, steps + 1)
    pts = []
    for y in (0.0, h):
        for r in (r0, r1):
            for a in ang:
                pts.append((r * math.cos(a), y, -r * math.sin(a)))
    n = steps + 1
    B0, B1, T0, T1 = 0, n, 2 * n, 3 * n  # bottom inner, bottom outer, top inner, top outer
    faces = []
    for i in range(steps):
        faces.append([T0 + i, T1 + i, T1 + i + 1, T0 + i + 1])        # top
        faces.append([B1 + i, B1 + i + 1, T1 + i + 1, T1 + i])        # outer side
        faces.append([B0 + i + 1, B0 + i, T0 + i, T0 + i + 1])        # inner side
    faces.append([B0, B1, T1, T0])
    faces.append([B1 + steps, B0 + steps, T0 + steps, T1 + steps])
    return pts, faces


def ifs(pts, faces, app, def_=None):
    d = f' DEF="{def_}"' if def_ else ""
    idx = " ".join(" ".join(map(str, f)) + " -1" for f in faces)
    return (f'    <Shape{d}><Appearance>{app}</Appearance><IndexedFaceSet solid="false" creaseAngle="0.5" coordIndex="{idx}">'
            f'<Coordinate point="{", ".join(f3(p) for p in pts)}"/></IndexedFaceSet></Shape>\n')

STATUS_COLOR = {"added": "#199e70", "modified": "#c98500", "unchanged": "#6b6b66"}


def shelf_pack(items, max_w, gap):
    """items: list of (key, w, d) -> {key: (x, z)} top-left corners, total (w, d)."""
    x = z = row_d = 0.0
    pos, W = {}, 0.0
    for key, w, d in items:
        if x > 0 and x + w > max_w:
            x = 0.0
            z += row_d + gap
            row_d = 0.0
        pos[key] = (x, z)
        x += w + gap
        W = max(W, x - gap)
        row_d = max(row_d, d)
    return pos, (W, z + row_d)

