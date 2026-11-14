import sys, json, time, collections
sys.path.insert(0, 'tools'); import repo_ast as ra
cfg = {"loom": ("/Users/handshake/Projects/x3d/work/x3d.loom-physics", "origin/main"), "demo": ("/Users/handshake/Projects/x3d/work/x3d.demo", "upstream/main")}
for name in sys.argv[1:]:
    t = time.time(); repo = ra.Repo(cfg[name][0])
    s = ra.snapshot(repo, cfg[name][1], lambda p: p.split('/')[0])
    C = s["code"]
    print(name, "code files", len(C), "loc", sum(r["loc"] for r in C.values()), "fns", sum(len(r["functions"]) for r in C.values()),
          "edges", sum(len(f["resolved"]) for r in C.values() for f in r["functions"]), "scenes", len(s["scenes"]), "vendored", s["vendored_files"], f"{time.time()-t:.0f}s")
    print(" langs", collections.Counter(r["lang"] for r in C.values()), "skipped", sum(1 for r in C.values() if r.get("skipped")), "errors", [p for p,r in C.items() if r.get("error")][:5])
    print(" parse_errors", sum(1 for r in C.values() if r.get("parse_errors")), [p for p,r in C.items() if r.get("parse_errors")][:6])
    print(" big", sorted(((r["loc"], p) for p, r in C.items()), reverse=True)[:12])
    print(" x3d parse errors", [p for p, r in s["scenes"].items() if r.get("parse_error")][:8])
    json.dump(s, open(f"{name}/data/head.json", "w"))
