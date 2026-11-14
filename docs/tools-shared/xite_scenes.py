"""X_ITE-specific scenes: spec-conformance sunburst and the learning map (inheritance tree + curriculum path)."""
import json
import math
import pathlib
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import astlib  # noqa: E402
import x3dkit as K  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
X = ROOT / "xite"
N = json.load(open(X / "data" / "nodes.json"))
L = json.load(open(X / "data" / "learn.json"))
GH = "https://github.com/create3000/x_ite/blob/16.7.0/"
REP = N["report"]
corpus = dict(L["H8_corpus_top"])
corpus_all = Counter()
for repo in ("loom", "demo", "onto"):
    for r in json.load(open(ROOT / repo / "data" / "head.json"))["scenes"].values():
        for nn in r["nodes"]:
            corpus_all[nn] += 1
CONF_C = {"exact": "#0ca30c", "extends": "#3987e5", "differs": "#ec835a", "missing": "#d03b3b"}
TEMP_C = {"data": "#3987e5", "event-driven": "#199e70", "engine": "#d95926", "sensor": "#c98500"}


def header(title, desc):
    metas = "\n".join(f'    <meta name="{K.esc(k)}" content="{K.esc(v)}"/>' for k, v in
                      [("title", title), ("description", desc), ("creator", "Claude Code (Opus 5.5), X_ITE masterclass"),
                       ("generator", "tools/xite_scenes.py (static analysis of the X_ITE 16.7.0 npm bundle; nothing executed)"),
                       ("reference", "https://github.com/create3000/x_ite/tree/16.7.0"), ("created", "2026-11-13")])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">
<X3D profile="Immersive" version="4.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.0.xsd">
  <head>
{metas}
  </head>
  <Scene>
"""


def conformance(name):
    r = REP.get(name)
    if not r or "missing" not in r:
        return "missing"
    if r["missing"] or r["type_diff"] or r["access_diff"]:
        return "differs"
    return "extends" if r["extra"] else "exact"


def scene_conformance():
    nodes = astlib.X3D_NODES
    comp = defaultdict(list)
    for n, info in nodes.items():
        comp[info["component"]].append(n)
    lines = {m["name"]: m["lines"] for m in N["modules"].values()}
    total = len(nodes)
    gap = 0.004
    comps = sorted(comp, key=lambda c: (-len(comp[c]), c))
    out = [header("X_ITE 16.7.0: spec conformance sunburst",
                  "Inner ring: the 37 components of X3D 4.1. Middle ring: X_ITE's module for each node, height ~ log(lines), colour = field-by-field "
                  "comparison with X3DUOM 4.1 (green exact, blue X_ITE adds fields, salmon fields missing or typed differently, red no module). "
                  "Outer ring (violet): how many of your own X3D files (x3d.loom, x3d.demo, x3d.onto) use the node. Hover for the differences.")]
    out.append(K.background())
    out.append(K.viewpoint("Top view, tilted", (0, 30, 24), (0, 0, 0), def_="VP_TOP"))
    out.append(K.viewpoint("Straight down", (0, 46, 0.01), (0, 0, 0)))
    mat = K.Mat()
    cnt = Counter()
    a = 0.0
    for c in comps:
        ns = sorted(comp[c])
        span = len(ns) / total * 2 * math.pi
        a0, a1 = a + gap, a + span - gap
        cc = Counter(conformance(n) for n in ns)
        pts, faces = K.wedge(5.2, 7.4, a0, a1, 0.3)
        out.append(f'    <Anchor description="{K.esc(f"{c}: {len(ns)} nodes; " + ", ".join(f"{k} {v}" for k, v in cc.items()))}">'
                   + K.ifs(pts, faces, mat("Comp", "#6b6b66", emissive=0.5)).strip() + "</Anchor>\n")
        mid = (a0 + a1) / 2
        flip = math.pi / 2 < (mid % (2 * math.pi)) < 3 * math.pi / 2
        out.append(K.flat_label(f"{c} {len(ns)}", ((7.25 if flip else 5.35) * math.cos(mid), 0.62, -(7.25 if flip else 5.35) * math.sin(mid)),
                                mid + (math.pi if flip else 0), size=0.3, justify="BEGIN" if flip else "END"))
        for i, n in enumerate(ns):
            b0 = a + span * i / len(ns) + gap / 2
            b1 = a + span * (i + 1) / len(ns) - gap / 2
            st = conformance(n)
            cnt[st] += 1
            ln = lines.get(n, 0)
            h = 0.3 + 0.55 * math.log2(1 + ln / 20) if ln else 0.15
            r = REP.get(n, {})
            parts = []
            for key, lab in (("extra", "adds"), ("missing", "lacks"), ("type_diff", "type differs"), ("access_diff", "access differs")):
                if r.get(key):
                    parts.append(f"{lab}: {', '.join(r[key])}")
            desc = f"{n} ({c}): {st}; {ln} lines in {r.get('module', 'no module')}" + ("; " + "; ".join(parts) if parts else "")
            pts, faces = K.wedge(7.8, 10.2, b0, b1, h, steps=1)
            out.append(f'    <Anchor description="{K.esc(desc)}">' + K.ifs(pts, faces, mat("St_" + st, CONF_C[st])).strip() + "</Anchor>\n")
            u = corpus_all.get(n, 0)
            if u:
                hh = 0.25 + 0.45 * math.log2(1 + u)
                pts, faces = K.wedge(10.6, 13.0, b0, b1, hh, steps=1)
                out.append(f'    <Anchor description="{K.esc(f"{n}: used in {u} of your X3D files")}">' + K.ifs(pts, faces, mat("Use", "#9085e9")).strip() + "</Anchor>\n")
            else:
                pts, faces = K.wedge(10.6, 13.0, b0, b1, 0.05, steps=1)
                out.append(K.ifs(pts, faces, mat("Off", K.NEUTRAL, emissive=0.6)))
            if st != "exact" or u >= 30:
                m = (b0 + b1) / 2
                fl = math.pi / 2 < (m % (2 * math.pi)) < 3 * math.pi / 2
                out.append(K.flat_label(n, (13.3 * math.cos(m), 0.05, -13.3 * math.sin(m)), m + (math.pi if fl else 0), size=0.3,
                                        justify="END" if fl else "BEGIN"))
        a += span
    xo = N["coverage"]["x_ite_only"]
    out.append(K.label(["X_ITE 16.7.0 vs X3D 4.1", f"{len(N['coverage']['implemented'])} of 267 nodes have a module",
                        f"exact {cnt['exact']} · extends {cnt['extends']} · differs {cnt['differs']} · none {cnt['missing']}",
                        f"+{len(xo)} X_ITE-only node types"], (0, 1.6, 0), size=0.55))
    out.append(K.label(["X_ITE-only: " + ", ".join(xo[:9]), ", ".join(xo[9:18]), ", ".join(xo[18:])], (0, 0.3, 16.2), size=0.4, color=K.TEXT2, billboard=False))
    out.append(K.FOOTER)
    (X / "scenes" / "conformance-sunburst.x3d").write_text("".join(out))
    return dict(cnt)


def scene_learning_map():
    mods = {m["name"]: (rel, m) for rel, m in N["modules"].items()}
    temper = {d["node"]: d["temperament"] for d in L["H6_temperament"]}
    names = sorted(mods)
    parents = {n: [b for b in mods[n][1]["bases"] if b in mods] for n in names}
    memo = {}

    def depth(n, seen=()):
        if n in memo:
            return memo[n]
        ps = [p for p in parents[n] if p not in seen]
        memo[n] = 0 if not ps else 1 + max(depth(p, seen + (n,)) for p in ps)
        return memo[n]
    idx = {n: i for i, n in enumerate(names)}
    E = np.array([(idx[n], idx[p]) for n in names for p in parents[n]])
    rng = np.random.default_rng(5)
    P = rng.normal(0, 8, (len(names), 3))
    for n in names:
        P[idx[n], 1] = -3.2 * depth(n)
    k, temp = 2.0, 4.0
    for _ in range(450):
        Dv = P[:, None, :] - P[None, :, :]
        dist = np.linalg.norm(Dv, axis=2) + 1e-2
        disp = ((k * k / dist ** 2)[:, :, None] * Dv).sum(1)
        d = P[E[:, 0]] - P[E[:, 1]]
        dl = np.linalg.norm(d, axis=1, keepdims=True) + 1e-3
        att = d * (dl / k)
        np.add.at(disp, E[:, 0], -att)
        np.add.at(disp, E[:, 1], att)
        disp[:, 1] = 0
        disp[:, [0, 2]] -= 0.06 * P[:, [0, 2]] * np.linalg.norm(P[:, [0, 2]], axis=1, keepdims=True) / 6
        ln = np.linalg.norm(disp, axis=1, keepdims=True) + 1e-9
        P += disp / ln * np.minimum(ln, temp)
        temp = max(0.05, temp * 0.99)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    span = float(np.max(hi - lo))
    steps = L["curriculum"]
    out = [header("X_ITE 16.7.0: a learning map",
                  "X_ITE's own class tree (bases from setPrototypeOf and .call(this) mixins), abstract types on top. Concrete nodes are coloured by "
                  "temperament (blue data, aqua event-driven, orange engine, amber sensor) and sized by how many of your own X3D files use them; "
                  "grey = abstract. The gold path is the 32-step curriculum: 8 keystone modules (the plinths above the tree), then abstract types, "
                  "quick wins and deep dives. Hover any sphere or plinth for the reason it is on the path.")]
    out.append(K.background())
    out.append(K.viewpoint("Whole map", c + np.array([0, span * 0.45, span * 1.15]), c + np.array([0, 2, 0]), def_="VP_ALL"))
    out.append(K.viewpoint("Keystones: read these first", np.array([c[0], hi[1] + 12, c[2] + 46]), np.array([c[0], hi[1] + 5, c[2]])))
    mat, geo = K.Mat(), K.Geo()
    pts, ii = [], []
    for n in names:
        for p in parents[n]:
            pts += [P[idx[n]], P[idx[p]]]
            ii += [len(pts) - 2, len(pts) - 1, -1]
    out.append(f'    <Shape DEF="Inherits"><Appearance><Material emissiveColor="0.42 0.42 0.40" diffuseColor="0 0 0" transparency="0.5"/></Appearance>'
               f'<IndexedLineSet coordIndex="{" ".join(map(str, ii))}"><Coordinate point="{", ".join(K.f3(p) for p in pts)}"/></IndexedLineSet></Shape>\n')
    step_of = {}
    for s in steps:
        step_of[pathlib.Path(s["read"]).stem] = s
    for n in names:
        rel, m = mods[n]
        p = P[idx[n]]
        u = corpus_all.get(n, 0)
        concrete = m["concrete"]
        r = (0.22 + 0.2 * math.log1p(u)) if concrete else 0.3
        colr = TEMP_C.get(temper.get(n), "#3987e5") if concrete else "#6b6b66"
        s = step_of.get(pathlib.Path(rel).stem)
        desc = (f"{n}: {'concrete' if concrete else 'abstract'}, {m['lines']} lines, bases {', '.join(m['bases']) or '-'}"
                + (f", {temper.get(n)}" if concrete else "") + (f", used in {u} of your X3D files" if u else "")
                + (f"  |  STEP {s['step']} ({s['track']}): {s['why']}" if s else ""))
        out.append(f'    <Anchor description="{K.esc(desc)}" url="{K.mf(GH + rel)}" parameter="{K.mf("target=_blank")}"><Transform translation="{K.f3(p)}" scale="{r:.3f} {r:.3f} {r:.3f}">'
                   f'<Shape><Appearance>{mat("N_" + colr[1:], colr, emissive=0.5)}</Appearance>{geo("Ball", "<Sphere radius=\"1\" />")}</Shape></Transform></Anchor>\n')
        if s or u >= 60 or (not concrete and depth(n) <= 1):
            out.append(K.label((f"{s['step']}. " if s else "") + n, (p[0], p[1] + r + 0.45, p[2]), size=0.5 if s else 0.4, color=K.TEXT if s else K.TEXT2))
    # keystone plinths above the tree
    keys = [s for s in steps if s["track"] == "keystone"]
    kpos = {}
    for j, s in enumerate(keys):
        x = c[0] + (j - (len(keys) - 1) / 2) * 7.0
        y = hi[1] + 6
        kpos[s["step"]] = np.array([x, y, c[2]])
        out.append(f'    <Anchor description="{K.esc("STEP " + str(s["step"]) + ": " + s["read"] + "  |  " + s["why"])}" url="{K.mf(GH + s["read"])}" parameter="{K.mf("target=_blank")}">'
                   f'<Transform translation="{x:.2f} {y:.2f} {c[2]:.2f}" scale="2.6 0.5 1.4"><Shape><Appearance>{mat("Plinth", "#c98500", emissive=0.6)}</Appearance>{geo("Box", "<Box size=\"1 1 1\" />")}</Shape></Transform></Anchor>\n')
        out.append(K.label([f"{s['step']}. {pathlib.Path(s['read']).stem}"], (x, y + 0.9, c[2]), size=0.55))
    # the path
    path = []
    for s in steps:
        if s["step"] in kpos:
            path.append(kpos[s["step"]])
        else:
            stem = pathlib.Path(s["read"]).stem
            if stem in idx:
                path.append(P[idx[stem]])
    if len(path) > 1:
        out.append(f'    <Shape DEF="CurriculumPath"><Appearance><Material emissiveColor="{K.rgb("#c98500")}" diffuseColor="0 0 0"/>'
                   f'<LineProperties linewidthScaleFactor="3"/></Appearance><LineSet vertexCount="{len(path)}"><Coordinate point="{", ".join(K.f3(p) for p in path)}"/></LineSet></Shape>\n')
    lx, ly = lo[0] - 3, hi[1] + 3
    for j, (txt, colr) in enumerate((("data node", TEMP_C["data"]), ("event-driven node", TEMP_C["event-driven"]), ("engine node", TEMP_C["engine"]),
                                     ("sensor node", TEMP_C["sensor"]), ("abstract type", "#6b6b66"), ("curriculum path / keystone", "#c98500"))):
        out.append(f'    <Transform translation="{lx:.2f} {ly - j * 1.2:.2f} {c[2]:.2f}" scale="0.4 0.4 0.4"><Shape><Appearance><Material diffuseColor="{K.rgb(colr, 0.75)}" emissiveColor="{K.rgb(colr, 0.45)}"/></Appearance><Sphere USE="Ball"/></Shape></Transform>\n')
        out.append(K.label(txt, (lx + 0.8, ly - j * 1.2, c[2]), size=0.6, justify="BEGIN"))
    out.append(K.label(["X_ITE 16.7.0 · learning map", f"{len(names)} node classes · curriculum of {len(steps)} steps weighted by your own scenes"],
                       (c[0], hi[1] + 11, c[2]), size=1.5))
    out.append(K.FOOTER)
    (X / "scenes" / "learning-map.x3d").write_text("".join(out))
    return {"classes": len(names), "max_depth": max(memo.values()), "path_points": len(path)}


if __name__ == "__main__":
    st = {"conformance": scene_conformance(), "learning_map": scene_learning_map()}
    print(st)
    json.dump(st, open(X / "data" / "xite_scene_stats.json", "w"), indent=1)
