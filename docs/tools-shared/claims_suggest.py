#!/usr/bin/env python3
"""Draft ledger lines for a chapter from the files its register already cites. A person reviews every line before it is committed.

    python3 docs/tools-shared/claims_suggest.py --chapter 03 [--repos DIR] [--cache DIR] > draft.jsonl

For each Numbers-register row whose Source cell names `repo@sha:path` (a file, not a directory or a glob), read that file at the sha, find each
non-trivial number of the Value cell (at least 100, or with a decimal part) as a number, and print a ledger line whose quote is the words of
that line around the number (at most 12 words, copied verbatim). Numbers already in the chapter's ledger are skipped. A number that occurs
more than once in the file gets a `line` hint and a `"note": "ambiguous: ..."`. This is a lexical finder, not a judge: it proves the number is
in the file, not that the row means that place.
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check_claims as CC  # noqa: E402
import claims_lib as CL  # noqa: E402
import learn_lib as L  # noqa: E402

CITE = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_.\-]*)@([0-9a-f]{7,12}):([^\s`,;)\]]+)")


def nontrivial(x):
    return abs(x) >= 100 or x != int(x)


def suggest(chapter, resolver, have=()):
    out = []
    for r in chapter.numbers:
        if len(r) < 6:
            continue
        cites = [(a, b, re.sub(r":\d+(-\d+)?$", "", c.rstrip(".,"))) for a, b, c in CITE.findall(r[5])]
        cites = [c for c in cites if re.search(r"\.[A-Za-z0-9]+$", c[2]) and not re.search(r"[*{}]", c[2])]
        grade = L.grade_of(r[3])
        for a, b, c in cites[:1]:                         # the first cited file; more than one file needs a human choice
            src = f"{a}@{b}:{c}"
            text, _ = resolver.get(src)
            if text is None or len(CL._norm(text)) != len(text):
                continue
            spans, norm = CL.token_spans(text)
            for n in CL.cell_numbers(r[2]):
                if not nontrivial(n) or (r[0], n) in have:
                    continue
                hits = [i for i, (t, _, _) in enumerate(spans) if any(CL._close(x, n, 1e-9) for rs in CL.numbers_in(t) for x in rs)]
                if not hits:
                    continue
                i = hits[0]
                lo, hi = max(0, i - 5), min(len(spans), i + 6)
                ls = norm.rfind("\n", 0, spans[i][1]) + 1
                le = norm.find("\n", spans[i][1])
                le = len(norm) if le < 0 else le
                lo = max(lo, next(k for k, (_, s0, _) in enumerate(spans) if s0 >= ls))
                hi = min(hi, 1 + max(k for k, (_, s0, _) in enumerate(spans) if s0 < le))
                first = next(k for k, (_, s0, _) in enumerate(spans) if s0 >= ls)
                numeric = re.compile(r"[+\-]?[\d.,e+\-]+")
                while lo > first and all(numeric.fullmatch(spans[k][0]) for k in range(lo, hi)):      # a bare number is no quote: take the label before it
                    lo -= 1
                quote = text[spans[lo][1]:spans[hi - 1][2]]
                ln = norm.count("\n", 0, spans[i][1]) + 1
                e = {"id": r[0], "value": int(n) if n == int(n) else n, "quote": quote, "source": src, "grade": grade}
                same = len(CL.find_runs([t for t, _, _ in spans], CL.tokens(quote)))
                if same > 1:
                    e["line"] = ln
                    e["note"] = f"ambiguous: the quote occurs {same} times in the file; the line hint picks one, check it is the row's place"
                out.append(e)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", required=True)
    ap.add_argument("--repos")
    ap.add_argument("--cache")
    a = ap.parse_args()
    ch = next(c for c in L.chapters() if c.num == a.chapter)
    have = set()
    p = CC.ledger_path(ch)
    if p.exists():
        _, ents, _ = CL.load_ledger(p)
        have = {(e["id"], CL.as_number(e.get("value"))) for e in ents if CL.as_number(e.get("value")) is not None}
    res = CL.Resolver(repos=a.repos, fetch=True, cache=a.cache)
    for e in suggest(ch, res, have):
        print(json.dumps(e, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
