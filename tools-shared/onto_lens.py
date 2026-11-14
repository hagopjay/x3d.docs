"""Ontology lens for x3d.onto: Turtle files (rdflib, from the x3d_mcp venv) and the code that queries them (Python ast).
Run with ~/Projects/x3d/x3d_mcp/.venv/bin/python. Reads git objects only.
"""
import ast
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter, defaultdict

import rdflib
from rdflib.namespace import OWL, RDF, RDFS

REPO = "/Users/handshake/Projects/x3d/x3d.onto"
REF = "upstream/claude/project-thread-3mgt8g"
OUT = pathlib.Path(__file__).resolve().parent.parent / "onto" / "data" / "onto_lens.json"


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], check=True, capture_output=True).stdout


def local(u):
    s = str(u)
    return re.split(r"[#/]", s)[-1] or s


names = git("ls-tree", "-r", "--name-only", REF).decode().split("\n")
ttl = [n for n in names if n.endswith(".ttl")]
graphs, res = {}, {"files": {}}
for n in ttl:
    g = rdflib.Graph()
    g.parse(data=git("show", f"{REF}:{n}").decode("utf-8"), format="turtle")
    graphs[n] = g
    classes = set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, RDFS.Class))
    oprops = set(g.subjects(RDF.type, OWL.ObjectProperty))
    dprops = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    indiv = set(g.subjects(RDF.type, OWL.NamedIndividual))
    sub = [(local(a), local(b)) for a, b in g.subject_objects(RDFS.subClassOf) if isinstance(b, rdflib.URIRef)]
    preds = Counter(local(p) for p in g.predicates())
    ns = sorted({str(u).rsplit("#", 1)[0] + "#" if "#" in str(u) else str(u).rsplit("/", 1)[0] + "/" for t in g for u in t if isinstance(u, rdflib.URIRef)})
    res["files"][n] = {"triples": len(g), "classes": sorted(local(c) for c in classes), "object_props": len(oprops), "datatype_props": len(dprops),
                       "individuals": sorted(local(i) for i in indiv), "subclass": sub, "predicates": preds.most_common(15), "namespaces": ns[:20]}
    print(n, len(g), "classes", len(classes), "obj", len(oprops), "dt", len(dprops), "indiv", len(indiv), "sub", len(sub), file=sys.stderr)

# 4.0 -> 4.1 and 4.1 -> narrowing proposal
def cls(n):
    return set(res["files"][n]["classes"])
c40, c41 = cls("data/X3dOntology4.0.ttl"), cls("data/X3dOntology4.1.ttl")
res["diff_40_41"] = {"added": sorted(c41 - c40), "removed": sorted(c40 - c41), "n40": len(c40), "n41": len(c41)}
prop = "proposal/X3dOntology4.1.narrowing-sketch.ttl"
gp, g41 = graphs[prop], graphs["data/X3dOntology4.1.ttl"]
new_triples = [t for t in gp if t not in g41]
res["proposal"] = {"triples": len(gp), "not_in_4.1": len(new_triples),
                   "predicates_of_new": Counter(local(p) for _, p, _ in new_triples).most_common(12),
                   "subjects_of_new": Counter(local(s) for s, _, _ in new_triples).most_common(15)}

res["proposal"]["restrictions_per_class"] = Counter(local(s) for s, o in gp.subject_objects(RDFS.subClassOf) if isinstance(o, rdflib.BNode))
res["proposal"]["restricted_props"] = Counter(local(o) for o in gp.objects(None, OWL.onProperty)).most_common(15)

# sim ontologies: what X3D terms they point at
x3d_terms = c41 | {local(p) for p in g41.subjects(RDF.type, OWL.ObjectProperty)} | {local(p) for p in g41.subjects(RDF.type, OWL.DatatypeProperty)}
res["sim_links"] = {}
for n in ttl:
    if n.startswith("sim/"):
        g = graphs[n]
        refs = Counter()
        for t in g:
            for u in t:
                if isinstance(u, rdflib.URIRef) and "x3d" in str(u).lower() and local(u) in x3d_terms:
                    refs[local(u)] += 1
        res["sim_links"][n] = refs.most_common(30)

# code that touches ontologies: Python files importing rdflib, SPARQL text in literals, .ttl paths named
code = defaultdict(lambda: {"rdflib": False, "sparql": 0, "ttl": set(), "x3d_terms": 0})
for n in names:
    if not n.endswith(".py"):
        continue
    try:
        tree = ast.parse(git("show", f"{REF}:{n}").decode("utf-8", "replace"))
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            if any(m and m.startswith("rdflib") for m in mods):
                code[n]["rdflib"] = True
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if re.search(r"\b(SELECT|CONSTRUCT|ASK)\b[\s\S]*\bWHERE\b", v):
                code[n]["sparql"] += 1
            for m in re.findall(r"[\w./-]+\.ttl\b", v):
                code[n]["ttl"].add(m)
res["code"] = {k: dict(v, ttl=sorted(v["ttl"])) for k, v in code.items() if v["rdflib"] or v["sparql"] or v["ttl"]}
OUT.write_text(json.dumps(res, indent=1, default=list))
print(json.dumps({"diff": {k: (v if not isinstance(v, list) else v[:12]) for k, v in res["diff_40_41"].items()}, "proposal": res["proposal"],
                  "sim_links": {k: v[:8] for k, v in res["sim_links"].items()},
                  "code": {k: v for k, v in list(res["code"].items())[:30]}}, indent=1, default=list)[:5000])
