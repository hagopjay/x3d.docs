#!/usr/bin/env python3
"""Lint docs/learn: chapter template, grades, ids, drills, numbers, links, and the public-repo leak sweep.

    python3 docs/tools-shared/check_learn.py            # exit 1 on any error
    python3 docs/tools-shared/check_learn.py --warn     # also print warnings
    python3 docs/tools-shared/check_learn.py --summary  # one line per chapter
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import learn_lib as L  # noqa: E402
import check_claims as CC  # noqa: E402  (claim ledger: links, value-in-quote, leak sweep; offline)

MIN = {"heuristics": 8, "drills": 5, "numbers": 12, "diagrams": 2, "tables": 4}


def check_chapter(c):
    errs, warns = [], []
    t = c.text
    if not re.match(r"^# " + c.num + r"\. ", t):
        errs.append("first line must be '# NN. Title' with the file's own NN")
    if not c.say:
        errs.append("missing '> **Say it:** ...' line")
    elif not re.search(r"\[[CLS]\]", c.say):
        warns.append("Say-it line has no grade token")
    if not c.code:
        errs.append("meta table has no 'chapter code' row")
    for label, rx in L.REQUIRED_HEADINGS:
        if not re.search(rx, t, re.M):
            errs.append(f"missing heading: {label}")
    if len(c.heuristics) < MIN["heuristics"]:
        errs.append(f"heuristics {len(c.heuristics)} < {MIN['heuristics']}")
    if len(c.drills) < MIN["drills"]:
        errs.append(f"drills {len(c.drills)} < {MIN['drills']}")
    if len(c.numbers) < MIN["numbers"]:
        errs.append(f"numbers {len(c.numbers)} < {MIN['numbers']}")
    if c.diagrams < MIN["diagrams"]:
        errs.append(f"ASCII diagrams (```text) {c.diagrams} < {MIN['diagrams']}")
    if c.tables < MIN["tables"]:
        warns.append(f"tables {c.tables} < {MIN['tables']}")
    if not (15_000 <= c.bytes <= 75_000):
        warns.append(f"size {c.bytes} bytes outside 15-75 KB")
    for row in c.heuristics:
        if len(row) < 5:
            errs.append(f"heuristic row has {len(row)} cells (want 5): {row[0]}")
            continue
        if not row[0].startswith(f"H-{c.code}-"):
            errs.append(f"{row[0]}: id prefix must be H-{c.code}-")
        if L.grade_of(row[2]) not in L.GRADES:
            errs.append(f"{row[0]}: grade cell must be C, L or S (got {row[2]!r})")
        if not row[4].strip():
            errs.append(f"{row[0]}: empty Instrument cell")
        if len(row[1].split()) > 45:
            warns.append(f"{row[0]}: rule longer than 45 words")
    for row in c.numbers:
        if len(row) < 6:
            errs.append(f"number row has {len(row)} cells (want 6): {row[0]}")
            continue
        if not row[0].startswith(f"N-{c.code}-"):
            errs.append(f"{row[0]}: id prefix must be N-{c.code}-")
        if L.grade_of(row[3]) not in L.GRADES:
            errs.append(f"{row[0]}: grade cell must be C, L or S (got {row[3]!r})")
        if not row[4].strip() or row[4].strip() in ("-", "n/a"):
            errs.append(f"{row[0]}: empty Instrument cell")
        if not row[5].strip():
            errs.append(f"{row[0]}: empty Source cell")
    ran = 0
    for d in c.drills:
        for k in ("level", "task", "verify", "answer", "checked"):
            if not d.get(k):
                errs.append(f"{d['id']}: missing '{k.title()}:' line")
        if d.get("level") and not re.search(r"\bL[123]\b", d["level"]):
            errs.append(f"{d['id']}: level must be L1, L2 or L3")
        if d.get("checked") and not re.match(r"\W*not run", d["checked"], re.I):
            ran += 1
        if not d["id"].startswith(f"D-{c.code}-"):
            errs.append(f"{d['id']}: id prefix must be D-{c.code}-")
    if c.drills and ran < 2:
        errs.append(f"only {ran} drills have a real 'Checked' line (need >= 2)")
    lvl = [re.search(r"\bL([123])\b", d.get("level", "")) for d in c.drills]
    if c.drills and sum(1 for m in lvl if m and m.group(1) in "23") < 2:
        errs.append("need >= 2 drills at L2 or L3")
    inside, widest = False, 0
    for ln in t.splitlines():
        if re.match(r"^```text\s*$", ln):
            inside = True
            continue
        if inside and ln.startswith("```"):
            inside = False
            continue
        if inside:
            widest = max(widest, len(ln))
    if widest > 100:
        warns.append(f"ASCII diagram {widest} columns wide (> 100)")
    # bare grade tokens in prose are fine; ungraded numeric tables are linted via the registers
    for sev, label, ln, frag in L.leak_sweep(t):
        (errs if sev == "error" else warns).append(f"LEAK[{label}] line {ln}: {frag!r}")
    # links
    for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", t):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:)", href):
            continue
        tgt = (c.path.parent / href).resolve()
        if not tgt.exists():
            errs.append(f"broken relative link: {href}")
    ce, cw, _ = CC.check_chapter_claims(c)          # no ledger file: nothing happens
    errs += ce
    warns += [w for w in cw if ": unchecked (" not in w]
    return errs, warns


def check_other(path):
    errs, warns = [], []
    t = path.read_text(encoding="utf-8")
    for sev, label, ln, frag in L.leak_sweep(t):
        (errs if sev == "error" else warns).append(f"LEAK[{label}] line {ln}: {frag!r}")
    for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", t):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:)", href):
            continue
        if not (path.parent / href).resolve().exists():
            warns.append(f"broken relative link: {href}")
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--warn", action="store_true")
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    bad = 0
    ids = {}
    chs = L.chapters()
    for c in chs:
        errs, warns = check_chapter(c)
        for row in c.heuristics + c.numbers:
            ids.setdefault(row[0], []).append(c.name)
        if a.summary or errs or (a.warn and warns):
            print(f"{c.name:34s} {c.bytes // 1024:3d} KB  H{len(c.heuristics):3d} D{len(c.drills):2d} N{len(c.numbers):3d}"
                  f" diag{c.diagrams:2d} tbl{c.tables:3d}  errors {len(errs)} warnings {len(warns)}")
        for e in errs:
            print("   ERROR", e)
        if a.warn:
            for w in warns:
                print("   warn ", w)
        bad += len(errs)
    for k, v in ids.items():
        if len(v) > 1:
            print("ERROR duplicate id", k, v)
            bad += 1
    # two threads can claim the same chapter number or code in parallel (PR #24 renumbered a duplicate 15): fail on either
    for label, key in (("chapter number", lambda c: c.num), ("chapter code", lambda c: c.code)):
        seen = {}
        for c in chs:
            seen.setdefault(key(c), []).append(c.name)
        for k, v in seen.items():
            if len(v) > 1:
                print(f"ERROR duplicate {label} {k}: {v}")
                bad += 1
    others = [p for p in L.LEARN.glob("*.md") if not L.CHAPTER_RE.match(p.name)]
    for p in others:
        errs, warns = check_other(p)
        for e in errs:
            print(f"ERROR {p.name}: {e}")
        if a.warn:
            for w in warns:
                print(f"warn  {p.name}: {w}")
        bad += len(errs)
    print(f"\n{len(chs)} chapters, {len(others)} other md files, {bad} errors")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
