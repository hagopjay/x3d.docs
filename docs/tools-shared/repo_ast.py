"""Multi-language AST snapshot of a git tree, cached per blob sha (read-only: git ls-tree / cat-file, no checkout).

Python   -> astlib (Python ast)               JS/MJS/TS/TSX + inline <script> in HTML -> jsast.cjs (TypeScript parser)
X3D      -> XML element tree (expat iterparse): node-type counts, ROUTEs, DEF/USE, Scripts, protos, components
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import astlib  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
CACHE.mkdir(exist_ok=True)
VENDOR = re.compile(r"(node_modules/|/vendor/|/vendors/|x_ite|babylon|(^|/)three[./]|\.min\.(js|mjs)$|/dist/|(^|/)lib/|/assets/components/|"
                    r"/pkg/|/third_party/|/external/|draco|ammo|havok|rapier|physx-js|mujoco_wasm|\.bundle\.js$|-bundle\.js$|/libs?/)", re.I)
CODE_EXT = {"py": "py", "js": "js", "mjs": "js", "cjs": "js", "ts": "js", "tsx": "js", "html": "html", "htm": "html"}
X3D_EXT = {"x3d"}
MAX_X3D = 60_000_000


class Repo:
    def __init__(self, path):
        self.path = path
        self.p = subprocess.Popen(["git", "-C", path, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def git(self, *a):
        return subprocess.run(["git", "-C", self.path, *a], check=True, capture_output=True, text=True).stdout

    def blob(self, sha):
        self.p.stdin.write((sha + "\n").encode())
        self.p.stdin.flush()
        header = self.p.stdout.readline().split()
        size = int(header[2])
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return data

    def tree(self, ref):
        out = []
        for line in self.git("ls-tree", "-r", "-l", ref).splitlines():
            meta, path = line.split("\t", 1)
            _mode, typ, sha, size = meta.split()
            if typ == "blob":
                out.append((path, sha, int(size) if size != "-" else 0))
        return out


def classify(path):
    name = path.rsplit("/", 1)[-1]
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in X3D_EXT:
        return "x3d"
    if ext in CODE_EXT:
        return "vendor" if VENDOR.search(path) else CODE_EXT[ext]
    return None


# ---------------------------------------------------------------- X3D files

def x3d_summary(data: bytes):
    tags, routes, defs, uses, comps, meta = Counter(), 0, 0, 0, [], {}
    elements, depth, maxdepth = 0, 0, 0
    try:
        for ev, el in ET.iterparse(__import__("io").BytesIO(data), events=("start", "end")):
            if ev == "start":
                depth += 1
                maxdepth = max(maxdepth, depth)
                tag = el.tag.split("}")[-1]
                elements += 1
                if tag == "X3D":
                    meta = {"profile": el.get("profile"), "version": el.get("version")}
                elif tag == "component":
                    comps.append(f"{el.get('name')}:{el.get('level')}")
                elif tag == "ROUTE":
                    routes += 1
                elif tag == "ProtoInstance":
                    tags["ProtoInstance"] += 1
                if el.get("DEF"):
                    defs += 1
                if el.get("USE"):
                    uses += 1
                if tag in astlib.X3D_NODES:
                    tags[tag] += 1
            else:
                depth -= 1
                el.clear()
        err = None
    except ET.ParseError as e:
        err = str(e)[:120]
    return {"nodes": dict(tags), "routes": routes, "defs": defs, "uses": uses, "components": comps, "elements": elements,
            "depth": maxdepth, "parse_error": err, **meta}


# ---------------------------------------------------------------- code files

def _cache_get(kind, sha):
    p = CACHE / f"{kind}-{sha}.json"
    return json.loads(p.read_text()) if p.exists() else None


def _cache_put(kind, sha, obj):
    (CACHE / f"{kind}-{sha}.json").write_text(json.dumps(obj))


def py_summary(text):
    mod = astlib.analyze_module("m", text)
    fns = []
    for f in mod["functions"]:
        fns.append({"qualname": f["qualname"], "name": f["name"], "class": f["class"], "line": f["line"], "end": f["end"], "loc": f["loc"],
                    "cc": f["cc"], "depth": f["depth"], "hash": f["hash"], "calls": f["calls_raw"],
                    "x3d": [[t[1], t[2]] for t in f["x3d"] if t[0] == "node"]})
    imports = [{"spec": i["target"], "names": [[k, v] for v, k in i.get("alias", {}).items()] if "alias" in i else [], "lazy": i["lazy"]} for i in mod["imports"]]
    return {"loc": mod["loc"], "functions": fns, "imports": imports, "classes": [{"name": c["qualname"], "line": c["line"], "bases": c["bases"]} for c in mod["classes"]]}


def analyse_blobs(repo: Repo, items):
    """items: [(path, sha, kind)] -> {sha: result}; fills the cache."""
    res, js_batch = {}, {}
    for path, sha, kind in items:
        cached = _cache_get(kind, sha)
        if cached is not None:
            res[sha] = cached
            continue
        data = repo.blob(sha)
        if kind == "x3d":
            r = x3d_summary(data) if len(data) <= MAX_X3D else {"skipped": "too large", "nodes": {}}
            r["bytes"] = len(data)
            _cache_put(kind, sha, r)
            res[sha] = r
        elif kind == "py":
            try:
                r = py_summary(data.decode("utf-8", "replace"))
            except SyntaxError as e:
                r = {"error": str(e)[:200], "loc": 0, "functions": [], "imports": [], "classes": []}
            _cache_put(kind, sha, r)
            res[sha] = r
        else:
            js_batch[sha] = {"name": path, "text": data.decode("utf-8", "replace")}
    if js_batch:
        with tempfile.TemporaryDirectory() as td:
            inp, outp = pathlib.Path(td) / "in.json", pathlib.Path(td) / "out.json"
            inp.write_text(json.dumps(js_batch))
            subprocess.run(["node", str(ROOT / "tools" / "jsast.cjs"), str(inp), str(outp)], check=True)
            out = json.loads(outp.read_text())
        for sha, r in out.items():
            kind = "html" if js_batch[sha]["name"].lower().endswith((".html", ".htm")) else "js"
            _cache_put(kind, sha, r)
            res[sha] = r
    return res


def snapshot(repo: Repo, ref, role_fn):
    files = []
    for path, sha, size in repo.tree(ref):
        k = classify(path)
        if k and k != "vendor":
            files.append((path, sha, k))
    vendored = sum(1 for p, _, _ in repo.tree(ref) if classify(p) == "vendor")
    res = analyse_blobs(repo, files)
    code, scenes = {}, {}
    for path, sha, k in files:
        r = res[sha]
        if k == "x3d":
            scenes[path] = dict(r, sha=sha)
        elif not r.get("skipped") or r.get("loc"):
            code[path] = dict(json.loads(json.dumps(r)), sha=sha, lang=k, role=role_fn(path))  # deep copy: identical blobs share a cache entry
    resolve(code)
    return {"code": code, "scenes": scenes, "vendored_files": vendored}


# ---------------------------------------------------------------- call resolution across files (inferred)

def _rel(base, spec):
    if not spec.startswith("."):
        return None
    parts = base.split("/")[:-1]
    for seg in spec.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            parts = parts[:-1]
        else:
            parts.append(seg)
    return "/".join(parts)


def resolve(code):
    by_stem = {}
    for path in code:
        stem = re.sub(r"\.(js|mjs|cjs|ts|tsx|py)$", "", path)
        by_stem[stem] = path
        if stem.endswith("/index"):
            by_stem[stem[:-6]] = path
    py_mods = {path[:-3].replace("/", "."): path for path in code if path.endswith(".py")}
    for path, r in code.items():
        top = {f["name"]: f["qualname"] for f in r["functions"] if "." not in f["qualname"]}
        bind_fn, bind_ns = {}, {}
        for imp in r.get("imports", []):
            spec = imp["spec"]
            tgt = None
            if r["lang"] == "py":
                tail = spec.lstrip(".")
                cands = [m for m in py_mods if m.endswith(tail)] if tail else []
                tgt = py_mods[cands[0]] if len(cands) == 1 else None
            else:
                rel = _rel(path, spec)
                if rel is not None:
                    rel = re.sub(r"\.(js|mjs|cjs|ts|tsx)$", "", rel)
                    tgt = by_stem.get(rel)
            if not tgt:
                continue
            imp["resolved"] = tgt
            for orig, local in imp.get("names", []):
                if orig == "*":
                    bind_ns[local] = tgt
                else:
                    bind_fn[local] = (tgt, orig)
        for f in r["functions"]:
            out = set()
            cls = f.get("class")
            for c in f["calls"]:
                parts = c.split(".")
                t = None
                if len(parts) == 1:
                    n = parts[0]
                    if f["qualname"] + "." + n in {g["qualname"] for g in r["functions"]}:
                        t = (path, f["qualname"] + "." + n)
                    elif n in top:
                        t = (path, top[n])
                    elif n in bind_fn:
                        tp, orig = bind_fn[n]
                        q = next((g["qualname"] for g in code[tp]["functions"] if g["qualname"] == orig), None)
                        if q:
                            t = (tp, q)
                elif parts[0] in ("this", "self") and len(parts) == 2 and cls:
                    q = cls + "." + parts[1]
                    if any(g["qualname"] == q for g in r["functions"]):
                        t = (path, q)
                elif len(parts) == 2 and parts[0] in bind_ns:
                    tp = bind_ns[parts[0]]
                    if any(g["qualname"] == parts[1] for g in code[tp]["functions"]):
                        t = (tp, parts[1])
                if t and t != (path, f["qualname"]):
                    out.add(t[0] + "::" + t[1])
            f["resolved"] = sorted(out)


def digest(obj):
    return hashlib.sha1(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:10]
