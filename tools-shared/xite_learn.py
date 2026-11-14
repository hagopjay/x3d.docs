"""Learning heuristics for X_ITE 16.7.0, each computed from the AST, the field inventory and the user's own scene corpus.

H1 Keystone      read first what many modules lean on and that is short: reverse-PageRank / sqrt(lines)
H2 Leverage      abstract types ranked by concrete nodes unlocked per 100 lines of the abstract module
H3 Spec deltas   fields X_ITE adds, drops or types differently from X3DUOM 4.1: places where a renderer knows more than the spec
H4 Surprise      residual of log(lines) against log(fields): machinery hidden behind few fields (case studies) vs pure data (skim)
H5 Twins         nodes with the same bases and near-identical method sets: learn one, get the rest
H6 Temperament   share of event fields (inputOnly/outputOnly): data nodes, sensors, engines
H7 Locus         per component, lines in Components/<C> (the nodes) vs Browser/<C> (the machinery the nodes call)
H8 Your corpus   value of a node = how many of your own X3D files use it (x3d.loom + x3d.demo + x3d.onto, measured)
Curriculum       keystones -> highest-leverage abstracts -> concrete nodes by value x surprise / prerequisite cost
"""
import json
import math
import pathlib
import re
from collections import Counter, defaultdict

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
X = ROOT / "xite"
N = json.load(open(X / "data" / "nodes.json"))
H = json.load(open(X / "data" / "head.json"))
C = H["code"]
MODS = N["modules"]

# ---------------------------------------------------------------- corpus (H8)
corpus = Counter()
for repo in ("loom", "demo", "onto"):
    for r in json.load(open(ROOT / repo / "data" / "head.json"))["scenes"].values():
        for n in r["nodes"]:
            corpus[n] += 1

# ---------------------------------------------------------------- module graph, H1
paths = sorted(C)
idx = {p: i for i, p in enumerate(paths)}
n = len(paths)
A = np.zeros((n, n))
for p, r in C.items():
    for d in r.get("deps", []):
        if d in idx:
            A[idx[p], idx[d]] = 1.0
# PageRank on "depends on" edges: rank flows to what is depended upon
outdeg = A.sum(1, keepdims=True)
M = np.divide(A, outdeg, out=np.zeros_like(A), where=outdeg > 0)
pr = np.ones(n) / n
for _ in range(80):
    pr = 0.15 / n + 0.85 * (M.T @ pr + pr[outdeg[:, 0] == 0].sum() / n)
indeg = A.sum(0)
lines = np.array([max(C[p]["loc"], 5) for p in paths])
keystone = pr / np.sqrt(lines)
H1 = sorted(({"module": paths[i], "pagerank": float(pr[i]), "dependents": int(indeg[i]), "lines": int(lines[i]),
              "score": float(keystone[i] * 1e4)} for i in range(n)), key=lambda d: -d["score"])

# ---------------------------------------------------------------- inheritance (X_ITE's own tree)
by_name = {}
for rel, m in MODS.items():
    by_name.setdefault(m["name"], (rel, m))
children = defaultdict(set)
for name, (rel, m) in by_name.items():
    for b in m["bases"]:
        children[b].add(name)


def descendants(t, seen=None):
    seen = seen if seen is not None else set()
    for c in children.get(t, ()):
        if c not in seen:
            seen.add(c)
            descendants(c, seen)
    return seen


concrete = {nm for nm, (rel, m) in by_name.items() if m["concrete"]}
H2 = []
for name, (rel, m) in by_name.items():
    if m["concrete"]:
        continue
    d = descendants(name) & concrete
    if not d:
        continue
    H2.append({"type": name, "module": rel, "lines": m["lines"], "unlocks": len(d), "per100": round(100 * len(d) / max(m["lines"], 20), 2),
               "your_use": sum(corpus[x] for x in d)})
H2.sort(key=lambda d: -d["per100"])

# X_ITE tree vs X3DUOM tree
uom = N["uom"]
tree_diff = []
for name, (rel, m) in by_name.items():
    if name in uom:
        u = {uom[name]["base"], *uom[name].get("also", [])} - {None}
        x = set(m["bases"])
        if x and u and x != u:
            tree_diff.append({"node": name, "x_ite": sorted(x), "uom": sorted(u)})

# ---------------------------------------------------------------- H3 spec deltas
H3 = []
for name, r in N["report"].items():
    if "missing" not in r:
        continue
    for f in r["extra"]:
        H3.append({"node": name, "kind": "X_ITE adds", "field": f})
    for f in r["missing"]:
        H3.append({"node": name, "kind": "X_ITE lacks", "field": f})
    for f in r["type_diff"]:
        H3.append({"node": name, "kind": "type differs", "field": f})
    for f in r["access_diff"]:
        H3.append({"node": name, "kind": "access differs", "field": f})
extra_fields = Counter(d["field"] for d in H3 if d["kind"] == "X_ITE adds")

# ---------------------------------------------------------------- H4 surprise, H6 temperament
rows = []
for name in concrete:
    rel, m = by_name[name]
    nf = len(m["fields"])
    if nf == 0:
        continue
    acc = Counter(f["access"] for f in m["fields"])
    events = (acc["inputOnly"] + acc["outputOnly"]) / nf
    rows.append([name, rel, nf, m["lines"], events, acc["outputOnly"] / nf])
xs = np.log([r[2] for r in rows])
ys = np.log([r[3] for r in rows])
slope, icpt = np.polyfit(xs, ys, 1)
H4, H6 = [], []
for (name, rel, nf, ln, ev, outp), x, y in zip(rows, xs, ys):
    resid = float(y - (slope * x + icpt))
    temper = "sensor" if outp >= 0.3 else ("engine" if ev >= 0.35 else ("event-driven" if ev >= 0.2 else "data"))
    H4.append({"node": name, "fields": nf, "lines": ln, "surprise": round(resid, 2), "x_lines_vs_expected": round(math.exp(resid), 1)})
    H6.append({"node": name, "temperament": temper, "event_share": round(ev, 2)})
H4.sort(key=lambda d: -d["surprise"])

# ---------------------------------------------------------------- H5 twins
twins = []
names = sorted(concrete)
for i, a in enumerate(names):
    ma = set(by_name[a][1]["methods"])
    for b in names[i + 1:]:
        if by_name[a][1]["bases"] != by_name[b][1]["bases"]:
            continue
        mb = set(by_name[b][1]["methods"])
        if len(ma | mb) >= 4:
            j = len(ma & mb) / len(ma | mb)
            if j >= 0.8:
                twins.append([a, b, round(j, 2)])
# group twins into families
fam = {}
for a, b, j in twins:
    ra, rb = fam.get(a, a), fam.get(b, b)
    root = min(ra, rb)
    for k, v in list(fam.items()):
        if v in (ra, rb):
            fam[k] = root
    fam[a] = fam[b] = root
families = defaultdict(list)
for k, v in fam.items():
    families[v].append(k)
H5 = sorted((sorted(v) for v in families.values()), key=lambda v: -len(v))

# ---------------------------------------------------------------- H7 locus of behaviour
loc_nodes, loc_browser = Counter(), Counter()
for p, r in C.items():
    parts = p.split("/")
    if p.startswith("src/x_ite/Components/") and len(parts) > 4:
        loc_nodes[parts[3]] += r["loc"]
    if p.startswith("src/x_ite/Browser/") and len(parts) > 4:
        loc_browser[parts[3]] += r["loc"]
H7 = sorted(({"component": c, "node_lines": loc_nodes[c], "browser_lines": loc_browser[c],
              "browser_share": round(loc_browser[c] / max(1, loc_nodes[c] + loc_browser[c]), 2)}
             for c in set(loc_nodes) | set(loc_browser)), key=lambda d: -d["browser_share"])

# ---------------------------------------------------------------- curriculum
def chain(name, seen=None):
    seen = seen if seen is not None else set()
    for b in by_name.get(name, (None, {"bases": []}))[1]["bases"]:
        if b not in seen and b in by_name:
            seen.add(b)
            chain(b, seen)
    return seen


steps, learned = [], set()
for k in [k for k in H1 if k["dependents"] >= 20][:8]:
    steps.append({"step": len(steps) + 1, "read": k["module"], "why": f"keystone: {k['dependents']} modules depend on it, {k['lines']} lines"})
    learned.add(pathlib.Path(k["module"]).stem)
for t in H2[:8]:
    steps.append({"step": len(steps) + 1, "read": t["module"], "why": f"abstract {t['type']}: unlocks {t['unlocks']} concrete nodes in {t['lines']} lines; your files use them {t['your_use']} times"})
    learned.add(t["type"])
surprise = {d["node"]: d["surprise"] for d in H4}
cands = []
for name in concrete:
    v = corpus.get(name, 0)
    if not v:
        continue
    pre = chain(name) - learned
    cost = by_name[name][1]["lines"] + sum(by_name[b][1]["lines"] for b in pre)
    cands.append((name, v, cost, sorted(pre), surprise.get(name, 0)))
# quick wins: most of your usage per line read
quick = sorted(cands, key=lambda c: -math.log1p(c[1]) / math.sqrt(max(c[2], 30)))[:8]
for name, v, cost, pre, sp in quick:
    steps.append({"step": len(steps) + 1, "track": "quick win", "read": by_name[name][0],
                  "why": f"{name}: in {v} of your X3D files, {cost} lines to read" + (f" (with {', '.join(pre)})" if pre else "")})
# deep dives: nodes you use whose implementation is far bigger than their fields suggest
taken = {q[0] for q in quick}
deep = sorted((c for c in cands if c[4] > 0.5 and c[0] not in taken), key=lambda c: -math.log1p(c[1]) * c[4])[:8]
for name, v, cost, pre, sp in deep:
    steps.append({"step": len(steps) + 1, "track": "deep dive", "read": by_name[name][0],
                  "why": f"{name}: {math.exp(sp):.1f}x the lines its {len(by_name[name][1]['fields'])} fields predict; in {v} of your X3D files"})
for s_ in steps:
    s_.setdefault("track", "keystone" if s_["why"].startswith("keystone") else "abstract")

out = {"H1_keystones": H1[:25], "H2_leverage": H2[:25], "tree_diff": tree_diff, "H3_spec_deltas": H3, "H3_extra_fields": extra_fields.most_common(),
       "H4_surprise": H4, "H4_fit": {"slope": round(float(slope), 3), "intercept": round(float(icpt), 3)}, "H5_twins": H5[:20],
       "H6_temperament": H6, "H7_locus": H7, "H8_corpus_top": corpus.most_common(40), "curriculum": steps,
       "corpus_nodes": len(corpus), "corpus_files": None}
(X / "data" / "learn.json").write_text(json.dumps(out, indent=1))
print("H1", [(pathlib.Path(d["module"]).stem, d["dependents"], d["lines"]) for d in H1[:10]])
print("H2", [(d["type"], d["unlocks"], d["lines"], d["per100"]) for d in H2[:10]])
print("tree diffs", len(tree_diff), tree_diff[:6])
print("H3 adds", extra_fields.most_common(10))
print("H4 top", [(d["node"], d["fields"], d["lines"], d["x_lines_vs_expected"]) for d in H4[:10]])
print("H4 bottom", [(d["node"], d["fields"], d["lines"], d["x_lines_vs_expected"]) for d in H4[-8:]], "fit", out["H4_fit"])
print("H5", H5[:8])
print("H6", Counter(d["temperament"] for d in H6))
print("H7", [(d["component"], d["node_lines"], d["browser_lines"], d["browser_share"]) for d in H7[:8]], "...", [(d["component"], d["browser_share"]) for d in H7[-5:]])
print("curriculum", [(s["step"], pathlib.Path(s["read"]).stem) for s in steps])
