"""Rebuild X_ITE's src/ tree from the unminified webpack bundles shipped in the npm package (no download).
Each ';// ./src/<path>' marker starts a module; the text up to the next marker is that module (as concatenated by webpack)."""
import json, pathlib, re, sys
DIST = pathlib.Path("/Users/handshake/Projects/x3d/work/x3d-physx-bridge/node_modules/x_ite/dist")
OUT = pathlib.Path(__file__).resolve().parent.parent / "xite"
MARK = re.compile(r"^;// \./((?:src|node_modules)/[^\s]+)\s*$")
bundles = [DIST / "x_ite.js"] + sorted(p for p in (DIST / "assets" / "components").glob("*.js") if not p.name.endswith(".min.js"))
mods, where = {}, {}
for b in bundles:
    cur, buf = None, []
    def flush():
        if cur:
            mods.setdefault(cur, "".join(buf)); where.setdefault(cur, b.name)
    for line in open(b, encoding="utf-8"):
        m = MARK.match(line)
        if m:
            flush(); cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    flush()
src = OUT / "src"
for path, text in mods.items():
    p = src / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
version = json.load(open(DIST.parent / "package.json"))["version"]
(OUT / "data" / "modules.json").write_text(json.dumps({"version": version, "bundles": [b.name for b in bundles], "where": where,
                                                      "lines": {k: v.count("\n") for k, v in mods.items()}}, indent=1))
print("X_ITE", version, "bundles", len(bundles), "modules", len(mods), "lines", sum(v.count("\n") for v in mods.values()))
