"""Whole-history AST timeline for x3d.loom or x3d.demo: every first-parent commit of main, PR attribution, per-step deltas."""
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import astlib  # noqa: E402
import repo_ast as ra  # noqa: E402
from roles import CFG  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEST_CALLS = {"test", "it", "describe"}


def tests_in(r):
    if r["lang"] == "py":
        return [f["qualname"] for f in r["functions"] if f["name"].startswith("test")]
    n = sum(1 for f in r["functions"] for c in f["calls"] if c in ("test", "it", "test.each", "it.each"))
    return [f"<js test {i}>" for i in range(n)]


def summarise(s, role_fn):
    C, S = s["code"], s["scenes"]
    funcs = {p + "::" + f["qualname"]: [f["hash"], f["cc"], f.get("loc", 0)] for p, r in C.items() for f in r["functions"] if f["qualname"] != "<module>"}
    bodies = Counter(v[0] for v in funcs.values() if v[2] >= 3)
    used = Counter()
    for r in S.values():
        for n in r["nodes"]:
            used[n] += 1
    known = set()
    for r in C.values():
        for f in r["functions"]:
            for n, ctx in f["x3d"]:
                if n in astlib.X3D_NODES:
                    known.add(n)
    roles = Counter()
    for p, r in C.items():
        roles[role_fn(p)] += r["loc"]
    scene_roles = Counter(role_fn(p) for p in S)
    return {
        "funcs": funcs, "used": dict(used), "known": sorted(known), "roles": dict(roles), "scene_roles": dict(scene_roles),
        "tests": {p: tests_in(r) for p, r in C.items() if tests_in(r)},
        "scenes": {p: [r.get("sha"), r.get("bytes", 0)] for p, r in S.items()},
        "stats": {"loc": sum(r["loc"] for r in C.values()), "funcs": len(funcs), "files": len(C),
                  "distinct_bodies": len(bodies), "cloned_bodies": sum(1 for v in bodies.values() if v > 1),
                  "cc": sum(v[1] for v in funcs.values()), "edges": sum(len(f["resolved"]) for r in C.values() for f in r["functions"]),
                  "scenes": len(S), "scene_mb": round(sum(r.get("bytes", 0) for r in S.values()) / 2 ** 20, 1),
                  "node_types_used": len([n for n in used if n in astlib.X3D_NODES]), "node_types_known": len(known),
                  "routes": sum(r.get("routes", 0) for r in S.values()),
                  "tests": sum(len(v) for v in [tests_in(r) for r in C.values()])},
    }


def delta(a, b):
    fa, fb = a["funcs"], b["funcs"]
    return {
        "added": len(set(fb) - set(fa)), "removed": len(set(fa) - set(fb)),
        "changed": sum(1 for k in set(fa) & set(fb) if fa[k][0] != fb[k][0]),
        "loc": b["stats"]["loc"] - a["stats"]["loc"],
        "role_loc": {r: b["roles"].get(r, 0) - a["roles"].get(r, 0) for r in set(a["roles"]) | set(b["roles"]) if b["roles"].get(r, 0) != a["roles"].get(r, 0)},
        "scenes_new": sorted(set(b["scenes"]) - set(a["scenes"])),
        "scenes_changed": sorted(p for p in set(a["scenes"]) & set(b["scenes"]) if a["scenes"][p][0] != b["scenes"][p][0]),
        "scene_mb": round(b["stats"]["scene_mb"] - a["stats"]["scene_mb"], 1),
        "used_new": sorted(set(b["used"]) - set(a["used"])), "known_new": sorted(set(b["known"]) - set(a["known"])),
        "tests": b["stats"]["tests"] - a["stats"]["tests"],
    }


def main(name):
    cfg = CFG[name]
    repo = ra.Repo(cfg["path"])
    prs = json.load(open(ROOT / name / "data" / "prs.json"))
    by_merge = {p["mergeCommit"]["oid"]: p for p in prs if p.get("mergeCommit")}
    shas = repo.git("rev-list", "--first-parent", "--reverse", cfg["ref"]).split()
    steps, prev = [], None
    for sha in shas:
        full, date, author, subj, parents = repo.git("log", "-1", "--format=%H%x1f%ad%x1f%an%x1f%s%x1f%P", "--date=iso-strict", sha).rstrip("\n").split("\x1f")
        s = summarise(ra.snapshot(repo, sha, cfg["role"]), cfg["role"])
        pr = by_merge.get(full)
        m = re.search(r"Merge pull request #(\d+)", subj)
        if not pr and m:
            pr = next((p for p in prs if p["number"] == int(m.group(1))), None)
        e = {"sha": full[:7], "date": date, "author": author, "subject": subj, "pr": pr["number"] if pr else None,
             "pr_title": pr["title"] if pr else None, "pr_url": pr["url"] if pr else None, "stats": s["stats"],
             "roles": s["roles"], "scene_roles": s["scene_roles"]}
        if prev:
            e["delta"] = delta(prev, s)
        steps.append(e)
        prev = s
        print(name, e["sha"], e["pr"], e["stats"]["loc"], e["stats"]["funcs"], e["stats"]["scenes"], file=sys.stderr)
    json.dump(steps, open(ROOT / name / "data" / "era.json", "w"), indent=1)
    json.dump({k: v for k, v in prev.items()}, open(ROOT / name / "data" / "head_summary.json", "w"))


if __name__ == "__main__":
    for n in sys.argv[1:]:
        main(n)
