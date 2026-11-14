"""X3D 4.0 scenes for x3d.loom / x3d.demo: call graph, X3D node sunburst, history timeline, clone city.

usage: python3 tools/scenes.py loom|demo
Large repos: significant functions (CC >= 8) are spheres/buildings with hover tooltips; the long tail is merged into one
PointSet / IndexedFaceSet per colour so the scene stays light. Functions under 3 lines are omitted.
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
import x3dkit as K  # noqa: E402
from roles import CFG  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = sys.argv[1]
cfg = CFG[NAME]
D = ROOT / NAME / "data"
OUT = ROOT / NAME / "scenes"
OUT.mkdir(exist_ok=True)
HEAD = json.load(open(D / "head.json"))
ERA = json.load(open(D / "era.json")) if (D / "era.json").exists() else []
CODE, SCENES = HEAD["code"], HEAD["scenes"]
SHA = (subprocess.run(["git", "-C", cfg["path"], "rev-parse", cfg["ref"]], capture_output=True, text=True).stdout.strip()
       if cfg["path"] else cfg["ref"])
GH = f"https://github.com/{cfg['repo']}/blob/{SHA}/"
PAL = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]  # validated, dark, fixed order
ORDER, LABEL = cfg["order"], cfg["label"]
RC = {r: PAL[i] for i, r in enumerate(ORDER)}
TITLE = {"loom": "x3d.loom", "demo": "x3d.demo", "onto": "x3d.onto", "xite": "X_ITE 16.7.0"}[NAME]
LANE_MB, LANE_USED, LANE_KNOWN = "#8a8a85", "#c3c2b7", "#f0efec"  # lanes are neutral so they never read as a role colour
SIG = 8  # CC threshold for an individual, hoverable mark


def header(title, desc):
    metas = "\n".join(f'    <meta name="{K.esc(k)}" content="{K.esc(v)}"/>' for k, v in
                      [("title", title), ("description", desc), ("creator", f"Claude Code (Opus 5.5), {TITLE} masterclass"),
                       ("generator", "tools/scenes.py (static analysis: Python ast + TypeScript parser + XML tree; nothing executed)"),
                       ("reference", f"https://github.com/{cfg['repo']}/tree/{SHA}"), ("created", "2026-11-13")])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.0//EN" "https://www.web3d.org/specifications/x3d-4.0.dtd">
<X3D profile="Immersive" version="4.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.0.xsd">
  <head>
{metas}
  </head>
  <Scene>
"""


def fns(path):
    return [f for f in CODE[path]["functions"] if f["qualname"] != "<module>" and f.get("loc", 0) >= 3]


# body-hash multiplicity across files (clone detection)
HASH_FILES = defaultdict(set)
for p in CODE:
    for f in fns(p):
        HASH_FILES[f["hash"]].add(p)


def shared(f):
    return len(HASH_FILES[f["hash"]]) > 1


# exact file clones: identical multiset of function bodies
SIGS = defaultdict(list)
for p in sorted(CODE):
    hs = tuple(sorted(f["hash"] for f in fns(p)))
    if hs:
        SIGS[hs].append(p)
GROUPS = sorted(SIGS.values(), key=lambda v: v[0])
REP = {v[0]: v for v in GROUPS}  # representative path -> all copies


def merged_points(points_by_colour, name):
    out = []
    for colr, pts in points_by_colour.items():
        if not pts:
            continue
        out.append(f'    <Shape DEF="{name}_{colr[1:]}"><Appearance><Material emissiveColor="{K.rgb(colr)}" diffuseColor="0 0 0"/></Appearance>'
                   f'<PointSet><Coordinate point="{", ".join(K.f3(p) for p in pts)}"/></PointSet></Shape>\n')
    return "".join(out)


# ---------------------------------------------------------------- 1. call graph (file layout + function spirals)

def scene_callgraph():
    reps = list(REP)
    idx = {p: i for i, p in enumerate(reps)}
    rep_of = {p: v[0] for v in GROUPS for p in v}
    roles = sorted({cfg["role"](p) for p in reps}, key=ORDER.index)
    nF = len(reps)
    hub = {r: nF + i for i, r in enumerate(roles)}
    edges = Counter()
    fcalls = []
    for p in reps:
        for f in CODE[p]["functions"]:
            for t in f["resolved"]:
                tp, tq = t.split("::", 1)
                tp = rep_of.get(tp)
                if tp is None:
                    continue
                if tp != p:
                    edges[(idx[p], idx[tp])] += 1
                    fcalls.append((p, f["qualname"], tp, tq))
        edges[(idx[p], hub[cfg["role"](p)])] += 2
        d = p.rsplit("/", 1)[0]
        for q in reps:  # same-directory affinity (cheap: only neighbours in sort order)
            pass
    # same directory neighbours
    bydir = defaultdict(list)
    for p in reps:
        bydir[p.rsplit("/", 1)[0]].append(idx[p])
    for members in bydir.values():
        for a, b in zip(members, members[1:]):
            edges[(a, b)] += 1
    sizes = np.array([math.sqrt(sum(CODE[p]["loc"] for p in reps if cfg["role"](p) == r) + 400) for r in roles])
    ang = (np.cumsum(sizes) - sizes / 2) / sizes.sum() * 2 * math.pi
    R = 12 + 1.2 * math.sqrt(nF)
    hubp = np.stack([R * np.cos(ang), np.zeros_like(ang), -R * np.sin(ang)], 1)
    rng = np.random.default_rng(3)
    P = np.zeros((nF + len(roles), 3))
    for p in reps:
        P[idx[p]] = hubp[roles.index(cfg["role"](p))] + rng.normal(0, 4, 3)
    P[nF:] = hubp
    E = np.array(list(edges))
    W = np.array([min(4.0, 0.5 + math.log1p(w)) for w in edges.values()])
    mass = np.array([1 + math.sqrt(len(fns(p))) / 3 for p in reps] + [1] * len(roles))
    k, temp = 4.0, 6.0
    for _ in range(500):
        Dv = P[:, None, :] - P[None, :, :]
        dist = np.linalg.norm(Dv, axis=2) + 1e-2
        rep = ((k * k * mass[None, :] * mass[:, None]) / dist ** 2)[:, :, None] * Dv
        disp = rep.sum(1)
        d = P[E[:, 0]] - P[E[:, 1]]
        dl = np.linalg.norm(d, axis=1, keepdims=True) + 1e-3
        att = d * (dl / k) * W[:, None]
        np.add.at(disp, E[:, 0], -att)
        np.add.at(disp, E[:, 1], att)
        disp[:, 1] *= 0.5
        ln = np.linalg.norm(disp, axis=1, keepdims=True) + 1e-9
        P[:nF] += (disp / ln * np.minimum(ln, temp))[:nF]
        temp = max(0.05, temp * 0.99)
    # functions on a Fibonacci sphere around their file
    fpos = {}
    for p in reps:
        fl = sorted(fns(p), key=lambda f: -f["cc"])
        n = len(fl)
        rad = 0.5 + 0.18 * math.sqrt(n)
        for i, f in enumerate(fl):
            y = 1 - 2 * (i + 0.5) / max(n, 1)
            rr = math.sqrt(max(0, 1 - y * y))
            th = i * 2.399963
            fpos[(p, f["qualname"])] = P[idx[p]] + rad * np.array([rr * math.cos(th), y, rr * math.sin(th)])
    lo, hi = P[:nF].min(0), P[:nF].max(0)
    c = (lo + hi) / 2
    span = float(np.max(hi - lo))
    nfun = sum(len(fns(p)) for p in reps)
    nsig = sum(1 for p in reps for f in fns(p) if f["cc"] >= SIG)
    dup_files = sum(len(v) - 1 for v in GROUPS)
    out = [header(f"{TITLE}: call graph as a 3D force layout",
                  f"Files are laid out by a force model (calls between files, same directory, pinned role hubs); each file's functions sit "
                  f"on a small sphere around it. {nsig} functions with CC >= {SIG} are spheres with tooltips; the other functions of 3+ lines are points. "
                  f"Coloured lines: {len(fcalls)} calls between files; grey lines: calls inside a file (static, inferred). {dup_files} exact file copies are drawn once (label xN). origin/main {SHA[:7]}.")]
    out.append(K.background())
    out.append(K.viewpoint("Overview", c + np.array([0, span * 0.8, span * 1.1]), c + np.array([0, 0, span * 0.06]), def_="VP_ALL"))
    for r in roles:
        sel = [idx[p] for p in reps if cfg["role"](p) == r]
        q = P[sel].mean(0)
        out.append(K.viewpoint(LABEL[r], q + np.array([0, 18, 26]), q))
    mat, geo = K.Mat(), K.Geo()
    # cross-file call lines
    pts, ii, cols = [], [], []
    for p, q1, tp, tq in fcalls:
        a, b = fpos.get((p, q1)), fpos.get((tp, tq))
        if a is None:
            a = P[idx[p]]
        if b is None:
            b = P[idx[tp]]
        pts += [a, b]
        ii += [len(pts) - 2, len(pts) - 1, -1]
        cols += [K.rgb(RC[cfg["role"](p)], 0.9), K.rgb(RC[cfg["role"](tp)], 0.9)]
    if pts:
        out.append(f'    <Shape DEF="CrossFileCalls"><Appearance><Material emissiveColor="1 1 1" diffuseColor="0 0 0" transparency="0.3"/></Appearance>'
                   f'<IndexedLineSet colorPerVertex="true" coordIndex="{" ".join(map(str, ii))}"><Color color="{", ".join(cols)}"/>'
                   f'<Coordinate point="{", ".join(K.f3(p) for p in pts)}"/></IndexedLineSet></Shape>\n')
    # calls inside a file, dim grey (anonymous callbacks are charged to their enclosing function)
    pts, ii = [], []
    for p in reps:
        for f in CODE[p]["functions"]:
            a = fpos.get((p, f["qualname"]))
            for t in f["resolved"]:
                tp, tq = t.split("::", 1)
                b = fpos.get((p, tq)) if tp == p else None
                if a is not None and b is not None:
                    pts += [a, b]
                    ii += [len(pts) - 2, len(pts) - 1, -1]
    if pts:
        out.append(f'    <Shape DEF="InFileCalls"><Appearance><Material emissiveColor="0.42 0.42 0.40" diffuseColor="0 0 0" transparency="0.55"/></Appearance>'
                   f'<IndexedLineSet coordIndex="{" ".join(map(str, ii))}"><Coordinate point="{", ".join(K.f3(p) for p in pts)}"/></IndexedLineSet></Shape>\n')
    infile = len(pts) // 2
    small = defaultdict(list)
    for p in reps:
        role = cfg["role"](p)
        for f in fns(p):
            pos = fpos[(p, f["qualname"])]
            if f["cc"] >= SIG:
                r = 0.12 + 0.07 * math.sqrt(f["cc"])
                copies = f" · body in {len(HASH_FILES[f['hash']])} files" if shared(f) else ""
                desc = f"{p}::{f['qualname']}  |  CC {f['cc']}, {f.get('loc', 0)} lines, line {f['line']}, {len(f['resolved'])} resolved calls{copies}"
                out.append(f'    <Anchor description="{K.esc(desc)}" url="{K.mf(GH + p + "#L" + str(f["line"]))}" parameter="{K.mf("target=_blank")}">'
                           f'<Transform translation="{K.f3(pos)}" scale="{r:.3f} {r:.3f} {r:.3f}"><Shape><Appearance>{mat("M_" + role, RC[role])}</Appearance>'
                           f'{geo("Ball", "<Sphere radius=\"1\" />")}</Shape></Transform></Anchor>\n')
            else:
                small[RC[role]].append(pos)
    out.append(merged_points(small, "SmallFunctions"))
    # labels for big file groups
    for p in sorted(reps, key=lambda p: -CODE[p]["loc"])[:24]:
        copies = len(REP[p])
        lab = p.split("/")[-1] + (f"  x{copies}" if copies > 1 else "")
        out.append(K.label([lab, f"{CODE[p]['loc']:,} lines · {len(fns(p))} fns"], P[idx[p]] + np.array([0, 2.4, 0]), size=0.9, color=K.TEXT2))
    for r in roles:
        sel = [idx[p] for p in reps if cfg["role"](p) == r]
        q = P[sel].mean(0)
        out.append(K.label(LABEL[r], (q[0], P[sel][:, 1].max() + 5, q[2]), size=1.8))
    out.append(K.label([f"{TITLE} · call graph", f"{len(reps)} files ({dup_files} more are exact copies) · {nfun} functions of 3+ lines · {len(fcalls)} cross-file calls · origin/main {SHA[:7]}"],
                       (c[0], hi[1] + 12, lo[2] - 8), size=2.6))
    out.append(K.FOOTER)
    (OUT / "callgraph-3d.x3d").write_text("".join(out))
    return {"files": len(reps), "dup_files": dup_files, "functions": nfun, "spheres": nsig, "cross_file_calls": len(fcalls), "in_file_calls": infile}


# ---------------------------------------------------------------- 2. X3D node sunburst: used by scenes vs named by code (+ loom tracker)

TRACK = {}
if NAME == "loom":
    raw = subprocess.run(["git", "-C", cfg["path"], "show", f"{cfg['ref']}:x3d.webgpu/bridge/NODES.json"], capture_output=True, text=True).stdout
    TRACK = {k: v.get("status") for k, v in json.loads(raw)["nodes"].items()}
TRACK_C = {"base": "#0ca30c", "bridged": "#0ca30c", "claimed": "#3987e5", "gap": "#ec835a", "todo": "#6b6b66", "blocked": "#d03b3b"}


def scene_sunburst():
    used = Counter()
    for r in SCENES.values():
        for n in r["nodes"]:
            used[n] += 1
    known = defaultdict(set)
    for p, r in CODE.items():
        for f in r["functions"]:
            for n, ctx in f["x3d"]:
                if n in astlib.X3D_NODES:
                    known[n].add(p)
    nodes = astlib.X3D_NODES
    comp = defaultdict(list)
    for n, info in nodes.items():
        comp[info["component"]].append(n)
    cov = lambda n: used[n] + len(known[n])  # noqa: E731
    comps = sorted(comp, key=lambda c: (-sum(1 for n in comp[c] if cov(n)), -len(comp[c]), c))
    total = len(nodes)
    gap = 0.004
    outer = "bridge tracker status (NODES.json)" if TRACK else "named in code"
    out = [header(f"{TITLE}: X3D 4.1 node sunburst",
                  f"Inner ring: X3D 4.1 components. Middle ring (orange): node types used in the repo's {len(SCENES)} X3D files (height ~ log2(1 + files)). "
                  + ("Outer ring: the WebGPU bridge's own tracker status per node (green base/bridged, blue claimed, salmon gap, grey todo, red blocked); "
                     "a white dot marks nodes the code names as a string literal (TypeScript/Python AST)." if TRACK else
                     "Outer ring (blue): node types named as string literals in the code (height ~ log2(1 + files)).") + " Hover for details.")]
    out.append(K.background())
    out.append(K.viewpoint("Top view, tilted", (0, 30, 24), (0, 0, 0), def_="VP_TOP"))
    out.append(K.viewpoint("Straight down", (0, 46, 0.01), (0, 0, 0)))
    mat = K.Mat()
    a = 0.0
    for c in comps:
        ns = sorted(comp[c], key=lambda n: (-cov(n), n))
        span = len(ns) / total * 2 * math.pi
        a0, a1 = a + gap, a + span - gap
        cn = sum(1 for n in ns if cov(n))
        pts, faces = K.wedge(5.2, 7.4, a0, a1, 0.25 + 0.04 * cn)
        out.append(f'    <Anchor description="{K.esc(f"Component {c}: {sum(1 for n in ns if used[n])} of {len(ns)} used in scenes")}">'
                   + K.ifs(pts, faces, mat("C_on" if cn else "C_off", "#6b6b66" if cn else "#2c2c2a", emissive=0.5)).strip() + "</Anchor>\n")
        mid = (a0 + a1) / 2
        if cn:
            flip = math.pi / 2 < (mid % (2 * math.pi)) < 3 * math.pi / 2
            r = 7.25 if flip else 5.35
            out.append(K.flat_label(f"{c} {sum(1 for n in ns if used[n])}/{len(ns)}", (r * math.cos(mid), 0.6, -r * math.sin(mid)),
                                    mid + (math.pi if flip else 0), size=0.3, justify="BEGIN" if flip else "END"))
        for i, n in enumerate(ns):
            b0 = a + span * i / len(ns) + gap / 2
            b1 = a + span * (i + 1) / len(ns) - gap / 2
            # middle: scene usage
            if used[n]:
                h = 0.3 + 0.9 * math.log2(1 + used[n])
                ex = sorted(p for p, r in SCENES.items() if n in r["nodes"])[:4]
                pts, faces = K.wedge(7.8, 10.2, b0, b1, h, steps=1)
                out.append(f'    <Anchor description="{K.esc(f"{n} ({c}) used in {used[n]} X3D files, e.g. " + ", ".join(ex))}">'
                           + K.ifs(pts, faces, mat("Used", K.WRITE_C)).strip() + "</Anchor>\n")
            else:
                pts, faces = K.wedge(7.8, 10.2, b0, b1, 0.06, steps=1)
                out.append(K.ifs(pts, faces, mat("Off", K.NEUTRAL, emissive=0.6)))
            # outer: tracker status (loom) or code naming (demo)
            if TRACK:
                st = TRACK.get(n)
                if st:
                    h = 0.6 if st in ("base", "bridged") else 0.4 if st == "claimed" else 0.25
                    pts, faces = K.wedge(10.6, 13.0, b0, b1, h, steps=1)
                    k = len(known[n])
                    out.append(f'    <Anchor description="{K.esc(f"{n}: tracker says {st}; named in {k} code files; used in {used[n]} scenes")}">'
                               + K.ifs(pts, faces, mat("T_" + st, TRACK_C[st])).strip() + "</Anchor>\n")
                    if k:
                        m = (b0 + b1) / 2
                        out.append(f'    <Transform translation="{11.8 * math.cos(m):.3f} {h + 0.12:.3f} {-11.8 * math.sin(m):.3f}" scale="0.09 0.09 0.09">'
                                   f'<Shape><Appearance>{mat("Dot", "#f0efec", emissive=0.9)}</Appearance><Sphere USE="DotBall"/></Shape></Transform>\n'
                                   if "DotBall" in mat.seen else
                                   f'    <Transform translation="{11.8 * math.cos(m):.3f} {h + 0.12:.3f} {-11.8 * math.sin(m):.3f}" scale="0.09 0.09 0.09">'
                                   f'<Shape><Appearance>{mat("Dot", "#f0efec", emissive=0.9)}</Appearance><Sphere DEF="DotBall" radius="1"/></Shape></Transform>\n')
                        mat.seen.add("DotBall")
                else:
                    pts, faces = K.wedge(10.6, 13.0, b0, b1, 0.06, steps=1)
                    out.append(K.ifs(pts, faces, mat("Off", K.NEUTRAL, emissive=0.6)))
            else:
                k = len(known[n])
                if k:
                    h = 0.3 + 0.9 * math.log2(1 + k)
                    pts, faces = K.wedge(10.6, 13.0, b0, b1, h, steps=1)
                    out.append(f'    <Anchor description="{K.esc(f"{n} named in {k} code files, e.g. " + ", ".join(sorted(known[n])[:4]))}">'
                               + K.ifs(pts, faces, mat("Known", K.READ_C)).strip() + "</Anchor>\n")
                else:
                    pts, faces = K.wedge(10.6, 13.0, b0, b1, 0.06, steps=1)
                    out.append(K.ifs(pts, faces, mat("Off", K.NEUTRAL, emissive=0.6)))
            if cov(n) or (TRACK.get(n) in ("base", "bridged", "claimed")):
                m = (b0 + b1) / 2
                flip = math.pi / 2 < (m % (2 * math.pi)) < 3 * math.pi / 2
                out.append(K.flat_label(n, (13.3 * math.cos(m), 0.05, -13.3 * math.sin(m)), m + (math.pi if flip else 0), size=0.3,
                                        justify="END" if flip else "BEGIN"))
        a += span
    nu = sum(1 for n in nodes if used[n])
    nk = sum(1 for n in nodes if known[n])
    lines = ["X3D 4.1", f"{total} concrete nodes", f"used in scenes: {nu}", f"named in code: {nk}"]
    if TRACK:
        st = Counter(TRACK.values())
        lines.append(f"tracker: {st['base'] + st['bridged']} base/bridged, {st['claimed']} claimed")
    out.append(K.label(lines, (0, 1.6, 0), size=0.6))
    out.append(K.FOOTER)
    (OUT / "coverage-sunburst.x3d").write_text("".join(out))
    agree = {}
    if TRACK:
        for st in ("base", "bridged", "claimed", "gap", "todo", "blocked"):
            ns = [n for n, s in TRACK.items() if s == st]
            agree[st] = {"n": len(ns), "named_in_code": sum(1 for n in ns if known[n]), "used_in_scenes": sum(1 for n in ns if used[n])}
    return {"used": nu, "known": nk, "tracker": agree, "used_top": used.most_common(25)}


# ---------------------------------------------------------------- 3. timeline (index x)

def scene_timeline():
    runs = json.load(open(D / "runs.json"))
    ci = {}
    for r in runs:
        if r["headBranch"] == "main":
            ci.setdefault(r["headSha"][:7], r["conclusion"])
    steps = ERA[1:]
    dx = 1.3
    xs = [i * dx for i in range(len(steps))]
    xc = xs[-1] / 2
    out = [header(f"{TITLE}: history as a 3D timeline",
                  f"One column per first-parent commit of main ({len(steps)} steps, {ERA[1]['date'][:10]} to {ERA[-1]['date'][:10]}). Front lane: code lines added per role "
                  "(1 unit = 1,500 lines). Middle lane: X3D megabytes added (mid grey, 1 unit = 5 MB). Back lane: new X3D node types used in scenes (light grey) "
                  "and new node types named in code (white), 0.15 unit each. Dots: CI or Pages deploy on main. Hover a column, click for the PR.")]
    out.append(K.background())
    out.append(K.viewpoint("Front, elevated", (xc, max(30, 0.55 * xs[-1]), max(44, 0.75 * xs[-1])), (xc, 0, -5), def_="VP_FRONT"))
    out.append(K.viewpoint("Oblique from the left", (-14, 18, 26), (xc * 0.7, 2, -6)))
    mat, geo = K.Mat(), K.Geo()
    box = lambda: geo("Unit", '<Box size="1 1 1" />')  # noqa: E731
    W = 0.9
    for i, e in enumerate(steps):
        x = xs[i]
        d = e["delta"]
        parts, up, down = [], 0.0, 0.0
        for role in ORDER:
            v = d["role_loc"].get(role, 0)
            if not v:
                continue
            h = abs(v) / 1500
            y = up + h / 2 if v > 0 else -(down + h / 2)
            if v > 0:
                up += h + 0.02
            else:
                down += h + 0.02
            parts.append(f'<Transform translation="{x:.3f} {y:.3f} 0" scale="{W} {max(h, 0.02):.3f} {W}"><Shape><Appearance>{mat("T_" + role, RC[role])}</Appearance>{box()}</Shape></Transform>')
        tag = f"#{e['pr']}" if e["pr"] else e["sha"]
        desc = (f"{tag} {e['date'][:10]}: {e['pr_title'] or e['subject']}  |  lines {d['loc']:+d}, functions +{d['added']} -{d['removed']} ~{d['changed']}, "
                f"X3D files +{len(d['scenes_new'])} ({d['scene_mb']:+} MB), new node types in scenes {len(d['used_new'])}, in code {len(d['known_new'])}")
        url = e["pr_url"] or f"https://github.com/{cfg['repo']}/commit/{e['sha']}"
        body = "".join(parts) or f'<Transform translation="{x:.3f} 0.02 0" scale="{W} 0.04 {W}"><Shape><Appearance>{mat("NoChange", "#4a4a46")}</Appearance>{box()}</Shape></Transform>'
        out.append(f'    <Anchor description="{K.esc(desc)}" url="{K.mf(url)}" parameter="{K.mf("target=_blank")}"><Group>{body}</Group></Anchor>\n')
        if d["scene_mb"] > 0:
            h = d["scene_mb"] / 5
            out.append(f'    <Transform translation="{x:.3f} {h / 2:.3f} -5" scale="{W} {h:.3f} {W}"><Shape><Appearance>{mat("MB", LANE_MB)}</Appearance>{box()}</Shape></Transform>\n')
        for key, colr, dz in (("used_new", LANE_USED, -10.2), ("known_new", LANE_KNOWN, -10.8)):
            n = len(d[key])
            if n:
                out.append(f'    <Anchor description="{K.esc(tag + (" scenes start using: " if key == "used_new" else " code starts naming: ") + ", ".join(d[key]))}">'
                           f'<Transform translation="{x:.3f} {n * 0.075:.3f} {dz}" scale="{W / 2:.2f} {n * 0.15:.3f} 0.5"><Shape><Appearance>{mat("N_" + key, colr)}</Appearance>{box()}</Shape></Transform></Anchor>\n')
        c = ci.get(e["sha"])
        if c:
            out.append(f'    <Anchor description="{K.esc("main run for " + e["sha"] + ": " + c)}"><Transform translation="{x:.3f} 0.22 0.9" scale="0.22 0.22 0.22"><Shape><Appearance>'
                       f'{mat("CI_" + c, K.GOOD if c == "success" else ("#d03b3b" if c == "failure" else K.CANCEL))}</Appearance>{geo("Dot", "<Sphere radius=\"1\" />")}</Shape></Transform></Anchor>\n')
        out.append(K.flat_label(tag, (x, 0.05, 1.7), 0.0, size=0.34 if e["pr"] else 0.26, color=K.TEXT2, justify="MIDDLE"))
        if i == 0 or e["date"][:10] != steps[i - 1]["date"][:10]:
            out.append(K.flat_label(e["date"][5:10], (x, 0.05, 2.6), 0.0, size=0.45, color=K.TEXT, justify="BEGIN"))
    out.append(f'    <Transform translation="{xc:.2f} -0.08 -4.6" scale="{xs[-1] + 4:.2f} 0.06 15"><Shape><Appearance>{mat("Band", "#262624", emissive=0.9, diffuse=0.4)}</Appearance>{box()}</Shape></Transform>\n')
    for z, t in ((0, "code lines per role (1 = 1,500)"), (-5, "X3D MB added (1 = 5 MB)"), (-10.5, "new node types: scenes / code")):
        out.append(K.label(t, (-1.2, 0.4, z), size=0.4, justify="END", billboard=False))
    f0, f1 = ERA[0]["stats"], ERA[-1]["stats"]
    out.append(K.label([f"{TITLE}: {ERA[0]['date'][:10]} -> {ERA[-1]['date'][:10]}, {len(steps) + 1} commits on main's first-parent line",
                        f"code {f0['loc']:,} -> {f1['loc']:,} lines · functions {f0['funcs']} -> {f1['funcs']} · X3D files {f0['scenes']} -> {f1['scenes']} ({f1['scene_mb']} MB) · "
                        f"node types in scenes {f1['node_types_used']}, named in code {f1['node_types_known']}"], (xc, 11, -14), size=0.85))
    items = [(LABEL[r], RC[r]) for r in ORDER] + [("X3D MB added", LANE_MB), ("node types newly used", LANE_USED), ("node types newly named in code", LANE_KNOWN),
                                                 ("main run: success", K.GOOD), ("cancelled", K.CANCEL)]
    for j, (txt, colr) in enumerate(items):
        lx = (j % 5) * (xs[-1] / 5) + 0.3
        lz = 3.6 + (j // 5) * 1.0
        out.append(f'    <Transform translation="{lx:.2f} 0.2 {lz:.2f}" scale="0.45 0.45 0.45"><Shape><Appearance><Material diffuseColor="{K.rgb(colr, 0.75)}" emissiveColor="{K.rgb(colr, 0.45)}"/></Appearance>{box()}</Shape></Transform>\n')
        out.append(K.flat_label(txt, (lx + 0.5, 0.05, lz), 0.0, size=0.36, color=K.TEXT2))
    out.append(K.FOOTER)
    (OUT / "fork-timeline.x3d").write_text("".join(out))
    return {"steps": len(steps)}


# ---------------------------------------------------------------- 4. clone city

def box_faces(cx, cz, s, h):
    x0, x1, z0, z1 = cx - s / 2, cx + s / 2, cz - s / 2, cz + s / 2
    v = [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1), (x0, h, z0), (x1, h, z0), (x1, h, z1), (x0, h, z1)]
    f = [[4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return v, f


def scene_city():
    depth = {"demo": 3, "xite": 4}.get(NAME, 2)
    district = defaultdict(list)
    for p in sorted(CODE):
        for f in fns(p):
            district["/".join(p.split("/")[:depth]) if p.count("/") >= depth else p.rsplit("/", 1)[0] or p].append((p, f))
    dists = []
    for dname, items in district.items():
        cells = [((p, f), max(0.22, 0.13 * math.sqrt(f.get("loc", 3))), max(0.22, 0.13 * math.sqrt(f.get("loc", 3)))) for p, f in items]
        area = sum(w * d for _, w, d in cells)
        pos, (w, d) = K.shelf_pack([(i, cw, cd) for i, (_, cw, cd) in enumerate(cells)], max(math.sqrt(area) * 1.2, max(cw for _, cw, _ in cells)), 0.1)
        role = Counter(cfg["role"](p) for p, _ in items).most_common(1)[0][0]
        dists.append((dname, role, cells, pos, w + 1.2, d + 1.2))
    dists.sort(key=lambda t: (ORDER.index(t[1]), -t[4] * t[5]))
    total = sum(t[4] * t[5] for t in dists)
    dpos, (CW, CD) = K.shelf_pack([(t[0], t[4], t[5]) for t in dists], math.sqrt(total) * 1.5, 1.6)
    cx, cz = CW / 2, CD / 2
    COL = {"unique": "#199e70", "shared": "#c98500"}
    out = [header(f"{TITLE}: clone city",
                  f"Districts = directories (plate tint = role), buildings = functions of 3+ lines in source order: footprint ~ sqrt(lines), height = CC x 0.1. "
                  f"Aqua: the body exists in one file only. Amber: the same body (whitespace-normalised AST text hash) is in two or more files. "
                  f"Functions with CC >= {SIG} carry tooltips; the rest are merged geometry.")]
    out.append(K.background())
    out.append(K.viewpoint("City overview", (cx, CW * 0.9, cz + CD * 1.2), (cx, 3, cz + 1), def_="VP_CITY"))
    mat, geo = K.Mat(), K.Geo()
    box = lambda: geo("B", '<Box size="1 1 1" />')  # noqa: E731
    merged = {k: ([], []) for k in COL}
    counts = Counter()
    towers = []
    for dname, role, cells, pos, w, d in dists:
        ox, oz = dpos[dname]
        out.append(f'    <Transform translation="{ox + w / 2:.3f} -0.06 {oz + d / 2:.3f}" scale="{w:.3f} 0.12 {d:.3f}"><Shape><Appearance>'
                   f'{mat("Plate_" + role, RC[role], emissive=0.18, diffuse=0.3)}</Appearance>{box()}</Shape></Transform>\n')
        loc = sum(f.get("loc", 0) for (_, f), _, _ in cells)
        if len(cells) > 25:
            out.append(K.flat_label(f"{dname}  ({len(cells)} fns)", (ox + 0.2, 0.02, oz + d + 0.5), 0.0, size=0.6 if len(cells) > 200 else 0.42))
        for i, ((p, f), s, _) in enumerate(cells):
            px, pz = pos[i]
            h = max(0.08, f["cc"] * 0.1)
            st = "shared" if shared(f) else "unique"
            counts[st] += 1
            x, z = ox + 0.6 + px + s / 2, oz + 0.6 + pz + s / 2
            if f["cc"] >= SIG:
                desc = f"{p}::{f['qualname']}  |  CC {f['cc']}, {f.get('loc', 0)} lines, line {f['line']}  |  " + (
                    f"same body in {len(HASH_FILES[f['hash']])} files" if st == "shared" else "unique body")
                out.append(f'    <Anchor description="{K.esc(desc)}" url="{K.mf(GH + p + "#L" + str(f["line"]))}" parameter="{K.mf("target=_blank")}">'
                           f'<Transform translation="{x:.3f} {h / 2:.3f} {z:.3f}" scale="{s * 0.92:.3f} {h:.3f} {s * 0.92:.3f}"><Shape><Appearance>'
                           f'{mat("S_" + st, COL[st])}</Appearance>{box()}</Shape></Transform></Anchor>\n')
                towers.append((f["cc"], p, f["qualname"], x, h, z))
            else:
                v, fc = box_faces(x, z, s * 0.92, h)
                V, F = merged[st]
                base = len(V)
                V.extend(v)
                F.extend([[base + j for j in q] for q in fc])
    for st, (V, F) in merged.items():
        if V:
            out.append(K.ifs(V, F, mat("S_" + st, COL[st]), def_=f"Merged_{st}"))
    for cc, p, q, x, h, z in sorted(towers, reverse=True)[:10]:
        out.append(K.label(f"{q} (CC {cc})", (x, h + 0.8, z), size=0.6))
    lz = CD + 2.8
    for j, st in enumerate(("unique", "shared")):
        lx = j * CW / 2.2
        out.append(f'    <Transform translation="{lx:.2f} 0.3 {lz:.2f}" scale="0.7 0.7 0.7"><Shape><Appearance>{mat("S_" + st, COL[st])}</Appearance>{box()}</Shape></Transform>\n')
        out.append(K.flat_label(f"{'body in one file' if st == 'unique' else 'body copied in 2+ files'} ({counts[st]} functions)", (lx + 0.8, 0.05, lz), 0.0, size=0.8))
    out.append(K.label([f"{TITLE} · clone city", f"{sum(counts.values())} functions of 3+ lines in {len(dists)} directories · origin/main {SHA[:7]}"],
                       (cx * 0.45, CW * 0.38, -8), size=2.2))
    out.append(K.FOOTER)
    (OUT / "code-city.x3d").write_text("".join(out))
    return dict(counts, districts=len(dists))


# ---------------------------------------------------------------- 5. (onto only) X3D Ontology 4.1 class hierarchy

def scene_ontology():
    L = json.load(open(D / "onto_lens.json"))
    f41 = L["files"]["data/X3dOntology4.1.ttl"]
    classes = sorted(set(f41["classes"]))
    sub = [(a, b) for a, b in f41["subclass"] if a in classes and b in classes]
    parents = defaultdict(list)
    for a, b in sub:
        parents[a].append(b)
    added = set(L["diff_40_41"]["added"])
    restr = L["proposal"]["restrictions_per_class"]
    simref = Counter()
    for refs in L["sim_links"].values():
        for nme, k in refs:
            simref[nme] += k
    used = Counter(nn for r in SCENES.values() for nn in r["nodes"])
    # depth = longest path to a root
    memo = {}
    def depth(c, seen=()):
        if c in memo:
            return memo[c]
        ps = [p for p in parents.get(c, []) if p not in seen]
        memo[c] = 0 if not ps else 1 + max(depth(p, seen + (c,)) for p in ps)
        return memo[c]
    idx = {c: i for i, c in enumerate(classes)}
    n = len(classes)
    rng = np.random.default_rng(11)
    P = rng.normal(0, 8, (n, 3))
    for c in classes:  # abstract levels stacked by depth (y), concrete nodes at the bottom
        P[idx[c], 1] = -3.0 * depth(c)
    E = np.array([(idx[a], idx[b]) for a, b in sub])
    k, temp = 2.2, 4.0
    for _ in range(400):
        Dv = P[:, None, :] - P[None, :, :]
        dist = np.linalg.norm(Dv, axis=2) + 1e-2
        disp = ((k * k / dist ** 2)[:, :, None] * Dv).sum(1)
        d = P[E[:, 0]] - P[E[:, 1]]
        dl = np.linalg.norm(d, axis=1, keepdims=True) + 1e-3
        att = d * (dl / k)
        np.add.at(disp, E[:, 0], -att)
        np.add.at(disp, E[:, 1], att)
        disp[:, 1] = 0  # keep the depth levels
        disp[:, [0, 2]] -= 0.06 * P[:, [0, 2]] * np.linalg.norm(P[:, [0, 2]], axis=1, keepdims=True) / 6  # gravity toward the axis
        ln = np.linalg.norm(disp, axis=1, keepdims=True) + 1e-9
        P += disp / ln * np.minimum(ln, temp)
        temp = max(0.05, temp * 0.99)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    span = float(np.max(hi - lo))
    out = [header("x3d.onto: the X3D Ontology 4.1 class hierarchy",
                  f"{n} OWL classes of X3dOntology4.1.ttl and {len(sub)} rdfs:subClassOf edges, levels by depth (abstract types on top). "
                  "Sphere size ~ log(1 + X3D files in the repo that use the node). Gold: class new in 4.1 (not in 4.0). "
                  "Blue ring: classes the proposal X3dOntology4.1.narrowing-sketch.ttl narrows (owl:allValuesFrom restrictions; ring size ~ count). "
                  "Orange halo: named by the sim spatial-cognition vocabularies. Hover for details.")]
    out.append(K.background())
    out.append(K.viewpoint("Whole hierarchy", c + np.array([0, span * 0.35, span * 1.1]), c, def_="VP_ALL"))
    out.append(K.viewpoint("Top: abstract types", np.array([c[0], hi[1] + 14, c[2] + span * 0.6]), np.array([c[0], hi[1] - 4, c[2]])))
    mat, geo = K.Mat(), K.Geo()
    pts, ii = [], []
    for a, b in sub:
        pts += [P[idx[a]], P[idx[b]]]
        ii += [len(pts) - 2, len(pts) - 1, -1]
    out.append(f'    <Shape DEF="SubClassOf"><Appearance><Material emissiveColor="0.45 0.45 0.43" diffuseColor="0 0 0" transparency="0.45"/></Appearance>'
               f'<IndexedLineSet coordIndex="{" ".join(map(str, ii))}"><Coordinate point="{", ".join(K.f3(p) for p in pts)}"/></IndexedLineSet></Shape>\n')
    for cl in classes:
        p = P[idx[cl]]
        u = used.get(cl, 0)
        r = 0.25 + 0.22 * math.log1p(u)
        abstract = cl.startswith("X3D")
        colr = "#c98500" if cl in added else ("#6b6b66" if abstract else "#f0efec")
        desc = (f"{cl}  |  depth {depth(cl)}, parents {', '.join(parents.get(cl, [])) or '-'}  |  used in {u} X3D files of the repo"
                + (" | NEW in 4.1" if cl in added else "") + (f" | proposal narrows {restr[cl]} properties" if cl in restr else "")
                + (f" | named {simref[cl]}x by sim vocabularies" if cl in simref else ""))
        out.append(f'    <Anchor description="{K.esc(desc)}"><Transform translation="{K.f3(p)}">'
                   f'<Transform scale="{r:.3f} {r:.3f} {r:.3f}"><Shape><Appearance>{mat("C_" + colr[1:], colr, emissive=0.5)}</Appearance>{geo("Ball", "<Sphere radius=\"1\" />")}</Shape></Transform>'
                   + (f'<Transform rotation="1 0 0 1.5708" scale="{r + 0.15 + 0.06 * restr[cl]:.3f} 0.04 {r + 0.15 + 0.06 * restr[cl]:.3f}"><Shape><Appearance>{mat("Ring", "#3987e5", emissive=0.7)}</Appearance>{geo("Disc", "<Cylinder radius=\"1\" height=\"1\" top=\"false\" bottom=\"false\" />")}</Shape></Transform>' if cl in restr else "")
                   + (f'<Transform scale="{r + 0.35:.3f} {r + 0.35:.3f} {r + 0.35:.3f}"><Shape><Appearance>{mat("Halo", "#d95926", transparency=0.7)}</Appearance>{geo("Ball", "<Sphere radius=\"1\" />")}</Shape></Transform>' if cl in simref else "")
                   + "</Transform></Anchor>\n")
        if u >= 20 or cl in added or depth(cl) <= 1 or restr.get(cl, 0) >= 6:
            out.append(K.label(cl, (p[0], p[1] + r + 0.5, p[2]), size=0.5, color=K.TEXT2))
    lx, ly = lo[0] - 2, hi[1] + 2
    for j, (txt, colr) in enumerate((("class new in 4.1", "#c98500"), ("abstract type (X3D...)", "#6b6b66"), ("concrete node", "#f0efec"),
                                     ("narrowed by the proposal (ring)", "#3987e5"), ("named by sim vocabularies (halo)", "#d95926"))):
        out.append(f'    <Transform translation="{lx:.2f} {ly - j * 1.2:.2f} {c[2]:.2f}" scale="0.4 0.4 0.4"><Shape><Appearance><Material diffuseColor="{K.rgb(colr, 0.75)}" emissiveColor="{K.rgb(colr, 0.45)}"/></Appearance><Sphere USE="Ball"/></Shape></Transform>\n')
        out.append(K.label(txt, (lx + 0.8, ly - j * 1.2, c[2]), size=0.6, justify="BEGIN"))
    out.append(K.label(["X3D Ontology 4.1 · class hierarchy", f"{n} classes · {len(sub)} subClassOf · 4.0 -> 4.1: +{len(added)} · proposal narrows {len(restr)} classes with {sum(restr.values())} restrictions"],
                       (c[0], hi[1] + 6, c[2]), size=1.4))
    out.append(K.FOOTER)
    (OUT / "ontology-hierarchy.x3d").write_text("".join(out))
    return {"classes": n, "subclass": len(sub), "max_depth": max(memo.values()), "added": len(added), "restricted": len(restr), "sim_named": len(simref)}


if __name__ == "__main__":
    if NAME == "xite":
        st = {"callgraph": scene_callgraph(), "city": scene_city()}
        json.dump(st, open(D / "scene_stats.json", "w"), indent=1, default=str)
        print(json.dumps(st, default=str))
        raise SystemExit
    st = {"callgraph": scene_callgraph(), "sunburst": scene_sunburst(), "timeline": scene_timeline(), "city": scene_city()}
    if NAME == "onto":
        st["ontology"] = scene_ontology()
    json.dump(st, open(D / "scene_stats.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in st.items()}, default=str)[:1800])
