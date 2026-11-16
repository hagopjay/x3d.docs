#!/usr/bin/env python3
"""Check the claim ledger of docs/learn: every ledger line must name a register row, and (when its source can be read) the quote must
be in the source and the value inside the quote. Prints a coverage figure per chapter. Standard library only; no network.

    python3 docs/tools-shared/check_claims.py                          # link checks only (ledger <-> chapter), offline
    python3 docs/tools-shared/check_claims.py --repos ../checkouts     # also FIND + COMPARE against checkouts named <repo>/ under DIR
    python3 docs/tools-shared/check_claims.py --fetch --strict-pins    # CI: read each pinned file from raw.githubusercontent.com (public repos)
    python3 docs/tools-shared/check_claims.py --private DIR            # owner only: re-find sealed private quotes by digest
    python3 docs/tools-shared/check_claims.py --repos DIR --json out.json --summary
Exit 1 on any error; 0 otherwise. Unresolved sources (no checkout, private, external) are warnings unless --require-resolved.
"""
import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import claims_lib as CL  # noqa: E402
import learn_lib as L  # noqa: E402

CLAIMS = L.LEARN / "claims"


_INDEX = {}


def row_index():
    """{row id: (chapter, row)} over every chapter's Numbers register and Heuristics table (built once)."""
    if not _INDEX:
        for ch in L.chapters():
            for r in ch.numbers + ch.heuristics:
                _INDEX[r[0]] = (ch, r)
    return _INDEX


def ledger_path(chapter):
    return CLAIMS / (chapter.path.stem + ".jsonl")


def check_chapter_claims(chapter, repos=None, require_resolved=False, strict_pins=False, fetch=False, cache=None, private=None):
    """-> (errors, warnings, report) for one chapter. No ledger file: no errors, report None."""
    p = ledger_path(chapter)
    if not p.exists():
        return [], [], None
    meta, entries, problems = CL.load_ledger(p)
    errs = [f"{p.name}: {x}" for x in problems]
    warns = []
    e2, w2 = CL.check_links(chapter, entries, row_index())
    errs += [f"{p.name}: {x}" for x in e2]
    warns += [f"{p.name}: {x}" for x in w2]
    for sev, label, ln, frag in L.leak_sweep(p.read_text(encoding="utf-8")):
        (errs if sev == "error" else warns).append(f"{p.name}: LEAK[{label}] line {ln}: {frag!r}")
    policy = CL.Policy(strict_pins=strict_pins)
    resolver = CL.Resolver(repos=repos, root=L.ROOT.parent, fetch=fetch, cache=cache, private=private)
    items = []
    for e in entries:
        if e.get("id") is None or not (e.get("quote") or e.get("quote_sha256")):
            continue
        it = CL.check_entry(e, resolver, policy)
        items.append(it)
        tag = f"{p.name}:{e['_line']} {it['field']}"
        if it["verdict"] == "check":
            hint = e.get("line")
            why = it["note"] or (f"quote not found in {it['document']}" if it["status"] == "not_found" else
                                 f"quote not at line {hint}; found at lines {it['lines']}" if it["status"] == "moved" and hint else
                                 f"quote found {it['occurrences']} times, at lines {it['lines']}; add a \"line\" hint" if it["occurrences"] > 1 else
                                 f"value {it['value']!r} not inside the quote")
            errs.append(f"{tag}: verdict check ({why})")
        elif it["verdict"] == "unchecked":
            (errs if require_resolved else warns).append(f"{tag}: unchecked ({it['note'] or 'value kind not comparable'})")
        elif it["verdict"] == "reworded":
            warns.append(f"{tag}: reworded (text value not inside the quote)")
    summ = collections.Counter(i["verdict"] for i in items)
    ver = {(i["field"], json.dumps(i["value"])) for i in items if i["verdict"] == "verified"}
    cov = CL.coverage(chapter, entries, ver)
    floor = meta.get("coverage_floor")
    if floor is not None and cov["coverage"] is not None and cov["coverage"] + 1e-9 < float(floor):
        errs.append(f"{p.name}: coverage {cov['coverage']:.3f} is below the committed floor {floor}")
    return errs, warns, {"chapter": chapter.name, "entries": len(entries), "verdicts": {v: summ.get(v, 0) for v in CL.VERDICTS},
                         "coverage": cov, "items": items}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", help="directory with one checkout per repo name (read-only git show is used)")
    ap.add_argument("--chapter", help="two-digit chapter number")
    ap.add_argument("--json", help="write the full report here")
    ap.add_argument("--receipt", help="write the compact, deterministic receipt that Appendix G is built from (commit it)")
    ap.add_argument("--date", help="date string recorded in the receipt (YYYY-MM-DD); omitted when not given")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--warn", action="store_true")
    ap.add_argument("--require-resolved", action="store_true")
    ap.add_argument("--strict-pins", action="store_true")
    ap.add_argument("--fetch", action="store_true", help="read pinned files of public repos from raw.githubusercontent.com when no checkout has them")
    ap.add_argument("--cache", help="directory that caches fetched files (CI cache)")
    ap.add_argument("--private", help="directory with private sources; only `private:<name>` entries are read from it")
    a = ap.parse_args()
    bad, reports = 0, []
    chs = [c for c in L.chapters() if not a.chapter or c.num == a.chapter]
    for c in chs:
        errs, warns, rep = check_chapter_claims(c, a.repos, a.require_resolved, a.strict_pins, a.fetch, a.cache, a.private)
        if rep:
            reports.append(rep)
            v, cv = rep["verdicts"], rep["coverage"]
            pct = f"{cv['coverage']:.1%}" if cv["coverage"] is not None else "n/a"
            print(f"{c.name:34s} entries {rep['entries']:3d}  verified {v['verified']:3d} check {v['check']:3d} reworded {v['reworded']:3d} "
                  f"unchecked {v['unchecked']:3d}  coverage {cv['values_with_quote']}/{cv['values']} values = {pct}; "
                  f"verified {cv['values_verified']}; rows {cv['rows_with_ledger']}/{cv['rows']}")
        elif a.summary:
            print(f"{c.name:34s} no ledger")
        for e in errs:
            print("   ERROR", e)
        if a.warn:
            for w in warns:
                print("   warn ", w)
        bad += len(errs)
    if reports:
        tv = sum(r["coverage"]["values"] for r in reports)
        tc = sum(r["coverage"]["values_with_quote"] for r in reports)
        print(f"\n{len(reports)} chapters with a ledger; coverage {tc}/{tv} register values; {bad} errors")
    else:
        print(f"\nno ledgers under {CLAIMS}; {bad} errors")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({"schema": CL.SCHEMA, "reports": reports}, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if a.receipt:
        rows = [{"id": i["field"], "chapter": r["chapter"][:2], "value": i["value"], "source": i["document"], "verdict": i["verdict"],
                 "line": i["line"], "pin": i["pin"]} for r in reports for i in r["items"]]
        cov = [{"chapter": r["chapter"][:2], **{k: v for k, v in r["coverage"].items() if k != "coverage" and k != "verified_coverage"}} for r in reports]
        rec = {"schema": CL.SCHEMA, "engine": "check_claims 0.1", "strict_pins": a.strict_pins, "entries": rows, "coverage": cov}
        if a.date:
            rec["date"] = a.date
        pathlib.Path(a.receipt).write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
