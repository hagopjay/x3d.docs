"""X_ITE node inventory from the rebuilt source (regex over module text; the patterns are X_ITE's own conventions) and a
field-by-field comparison with the X3D Unified Object Model 4.1."""
import json
import pathlib
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent / "xite"
SRC = ROOT / "src"
UOM = "/Users/handshake/Projects/x3d/x3d_mcp/src/validation/schemas/X3dUnifiedObjectModel-4.1.xml"

STATIC = re.compile(r'getStaticProperties \("(\w+)",\s*"(\w+)",\s*(\d+),\s*"(\w*)",\s*"([\d.]+)"(?:,\s*"([^"]*)")?\)')
FIELD = re.compile(r'\.(inputOutput|initializeOnly|inputOnly|outputOnly),\s*"(\w+)",\s*new [\w ()]*?\.\s*([SM]F\w+) \(([^)]*)\)')
PROTO = re.compile(r'Object \.setPrototypeOf \((\w+) \.prototype,\s*\(?(\w+?)(?:\(\)\))?\s*\.prototype\)')
CALLBASE = re.compile(r'^\s*\(?(\w+?)(?:\(\)\)?)?\s*\.call \(this', re.M)
NSADD = re.compile(r'x_ite_Namespace \.add \("(\w+)"')
METHOD = re.compile(r'^   (\w+) \(([^)]*)\)\s*$', re.M)  # X_ITE style: 3-space indented method in an Object.assign literal


def load_uom():
    root = ET.parse(UOM).getroot()
    nodes = {}
    for sect in ("ConcreteNodes", "AbstractNodeTypes"):
        for n in root.find(sect):
            idef = n.find("InterfaceDefinition")
            inh = idef.find("Inheritance")
            add = [a.get("baseType") for a in idef.findall("AdditionalInheritance")]
            ci = idef.find("componentInfo")
            fields = {f.get("name"): {"type": f.get("type"), "access": f.get("accessType"), "default": f.get("default")}
                      for f in idef.findall("field")}
            nodes[n.get("name")] = {"abstract": sect == "AbstractNodeTypes", "base": inh.get("baseType") if inh is not None else None,
                                    "also": add, "component": ci.get("name") if ci is not None else None,
                                    "level": int(ci.get("level")) if ci is not None else None, "fields": fields}
    return nodes


def base_name(tok):
    tok = re.sub(r"^external_X_ITE_X3D_", "", tok)
    tok = re.sub(r"_default$", "", tok)
    return tok.split("_")[-1]


def norm_default(xtype, raw):
    raw = raw.strip()
    if not raw or raw.startswith("new") or "(" in raw:
        return None
    return " ".join(re.sub(r"\s+", " ", raw.replace(",", " ")).split())


def main():
    uom = load_uom()
    mods = {}
    for p in sorted((SRC / "src" / "x_ite" / "Components").rglob("*.js")):
        text = p.read_text()
        rel = str(p.relative_to(SRC))
        m = STATIC.search(text)
        ns = NSADD.search(text)
        name = (m.group(1) if m else (ns.group(1) if ns else p.stem))
        protos = PROTO.findall(text)
        bases = []
        for own, base in protos:
            if own == p.stem or own == name:
                bases.append(base_name(base))
        for tok in CALLBASE.findall(text):
            b = base_name(tok)
            if b not in bases and (b.startswith("X3D") or b in uom):
                bases.append(b)
        fields = [{"access": a, "name": n, "type": t, "default": norm_default(t, d)} for a, n, t, d in FIELD.findall(text)]
        methods = sorted(set(METHOD.findall(text) and [x[0] for x in METHOD.findall(text)]))
        mods[rel] = {"name": name, "component": m.group(2) if m else p.parent.name, "level": int(m.group(3)) if m else None,
                     "container": m.group(4) if m else None, "since": m.group(5) if m else None,
                     "concrete": bool(m), "bases": bases, "fields": fields, "methods": methods,
                     "lines": text.count("\n")}
    # compare concrete nodes with X3DUOM
    ACC = {"inputOutput": "inputOutput", "initializeOnly": "initializeOnly", "inputOnly": "inputOnly", "outputOnly": "outputOnly"}
    report = {}
    for rel, m in mods.items():
        if not m["concrete"]:
            continue
        u = uom.get(m["name"])
        if not u:
            report[m["name"]] = {"status": "not in X3D 4.1 UOM", "module": rel}
            continue
        xf = {f["name"]: f for f in m["fields"]}
        uf = {k: v for k, v in u["fields"].items() if k not in ("IS", "DEF", "USE", "class", "id", "style", "containerField")}
        missing = sorted(set(uf) - set(xf))
        extra = sorted(set(xf) - set(uf))
        typ = sorted(k for k in set(xf) & set(uf) if xf[k]["type"] != uf[k]["type"])
        acc = sorted(k for k in set(xf) & set(uf) if ACC.get(xf[k]["access"]) != uf[k]["access"])
        dflt = []
        for k in set(xf) & set(uf):
            a, b = xf[k]["default"], uf[k]["default"]
            if b is None or a is None or uf[k]["type"] in ("SFNode", "MFNode", "SFString", "MFString"):
                continue
            try:
                av = [float(x) for x in a.split()]
                bv = [float(x) for x in b.replace(",", " ").split()]
                if len(av) == len(bv) and any(abs(x - y) > 1e-3 * max(1.0, abs(y)) for x, y in zip(av, bv)):
                    dflt.append([k, a, b])
            except ValueError:
                if a.lower() != b.lower() and not (a in ("true", "false") or b in ("true", "false")):
                    dflt.append([k, a, b])
        report[m["name"]] = {"module": rel, "component": m["component"], "uom_component": u["component"], "level": m["level"], "uom_level": u["level"],
                             "x_ite_fields": len(xf), "uom_fields": len(uf), "missing": missing, "extra": extra,
                             "type_diff": typ, "access_diff": acc, "default_diff": sorted(dflt)}
    concrete = {m["name"] for m in mods.values() if m["concrete"]}
    uom_concrete = {k for k, v in uom.items() if not v["abstract"]}
    out = {"modules": mods, "report": report, "uom": {k: {kk: vv for kk, vv in v.items() if kk != "fields"} | {"nfields": len(v["fields"])} for k, v in uom.items()},
           "coverage": {"x_ite_concrete": len(concrete), "uom_concrete": len(uom_concrete),
                        "implemented": sorted(concrete & uom_concrete), "not_implemented": sorted(uom_concrete - concrete),
                        "x_ite_only": sorted(concrete - uom_concrete)}}
    (ROOT / "data" / "nodes.json").write_text(json.dumps(out, indent=1))
    c = out["coverage"]
    print("X_ITE concrete node modules", c["x_ite_concrete"], "| UOM 4.1 concrete", c["uom_concrete"], "| implemented", len(c["implemented"]),
          "| not implemented", c["not_implemented"], "| X_ITE-only", c["x_ite_only"])
    R = [r for r in report.values() if "missing" in r]
    print("nodes with missing fields", sum(1 for r in R if r["missing"]), "extra", sum(1 for r in R if r["extra"]),
          "type diffs", sum(len(r["type_diff"]) for r in R), "access diffs", sum(len(r["access_diff"]) for r in R),
          "default diffs", sum(len(r["default_diff"]) for r in R))
    ex = Counter(f for r in R for f in r["extra"])
    mi = Counter(f for r in R for f in r["missing"])
    print("most common extra fields", ex.most_common(15))
    print("most common missing fields", mi.most_common(15))
    print("default diffs sample", [(n, r["default_diff"]) for n, r in report.items() if r.get("default_diff")][:12])
    print("access diffs", [(n, r["access_diff"]) for n, r in report.items() if r.get("access_diff")][:12])
    print("type diffs", [(n, r["type_diff"]) for n, r in report.items() if r.get("type_diff")][:12])


if __name__ == "__main__":
    main()
