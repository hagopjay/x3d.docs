#!/usr/bin/env python3
"""Build docs/learn: merged ledgers (appendices A, C, D, E, F), the chapter table in 00-start-here.md, and HTML for every .md.

    pip install markdown-it-py mdit-py-plugins
    python3 docs/tools-shared/build_learn.py            # ledgers + HTML
    python3 docs/tools-shared/build_learn.py --no-html  # ledgers only

Ledgers are regenerated between <!-- BEGIN GENERATED --> and <!-- END GENERATED --> markers; hand-written text outside the markers is kept.
Nothing here executes chapter content; it only parses the strict tables defined in docs/learn/AUTHORING.md.
"""
import argparse
import collections
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import learn_lib as L  # noqa: E402

LEARN = L.LEARN
SITE = "X3D Elucidation"
BEGIN, END = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"

APPENDICES = {
    "A-validator-register.md": "Appendix A. Instrument and validator register",
    "B-glossary.md": "Appendix B. Glossary",
    "C-numbers-ledger.md": "Appendix C. Numbers ledger",
    "D-heuristics-ledger.md": "Appendix D. Heuristics ledger",
    "E-drills.md": "Appendix E. Drill index",
    "F-source-map.md": "Appendix F. Source map",
}
EXTRA = {"AUTHORING.md": "Authoring contract", "CHANGELOG.md": "Changelog"}


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(cell(str(x)) for x in r) + " |")
    return "\n".join(out)


def put_block(path, title, head_text, generated):
    block = f"{BEGIN}\n{generated}\n{END}"
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if BEGIN in t and END in t:
            t = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: block, t, flags=re.S)
        else:
            t = t.rstrip() + "\n\n" + block + "\n"
    else:
        t = f"# {title}\n\n{head_text}\n\n{block}\n"
    path.write_text(t, encoding="utf-8")


def counts_by_grade(rows, idx):
    c = collections.Counter(L.grade_of(r[idx]) or "?" for r in rows)
    return f"[C] {c['C']} · [L] {c['L']} · [S] {c['S']}" + (f" · unparsed {c['?']}" if c["?"] else "")


def build_ledgers(chs):
    nums = [(c, r) for c in chs for r in c.numbers if len(r) >= 6]
    heur = [(c, r) for c in chs for r in c.heuristics if len(r) >= 5]
    drl = [(c, d) for c in chs for d in c.drills]

    # C numbers
    rows = [[r[0], f"[{c.num}]({c.name})", r[1], r[2], r[3], r[4], r[5]] for c, r in nums]
    gen = (f"**{len(nums)} numbers** from {len(chs)} chapters. Grades: {counts_by_grade([r for _, r in nums], 3)}. "
           "Every row names its instrument; a row without one fails `check_learn.py`.\n\n"
           + table(["ID", "Ch", "Quantity", "Value", "Grade", "Instrument", "Source"], rows))
    put_block(LEARN / "C-numbers-ledger.md", APPENDICES["C-numbers-ledger.md"],
              "Merged from the *Numbers register* of every chapter by `tools-shared/build_learn.py`. Edit the chapter, not this file.", gen)

    # D heuristics
    rows = [[r[0], f"[{c.num}]({c.name})", r[1], r[2], r[3], r[4]] for c, r in heur]
    gen = (f"**{len(heur)} heuristics.** Grades: {counts_by_grade([r for _, r in heur], 2)}. Retired rules are struck through in their chapter, never deleted.\n\n"
           + table(["ID", "Ch", "Rule", "Grade", "Evidence", "Instrument"], rows))
    put_block(LEARN / "D-heuristics-ledger.md", APPENDICES["D-heuristics-ledger.md"],
              "Merged from the *Heuristics* table of every chapter. Edit the chapter, not this file.", gen)

    # E drills
    rows = []
    for c, d in drl:
        title = re.sub(r"^D-[A-Z]+-\d+\s*", "", d["head"])
        chk = d.get("checked", "").strip().split("\n")[0]
        lvl = re.search(r"L[123]", d.get("level", ""))
        rows.append([d["id"], f"[{c.num}]({c.name})", lvl.group(0) if lvl else "?", title, chk])
    ran = sum(1 for r in rows if not re.match(r"\W*not run", r[4], re.I))
    gen = (f"**{len(rows)} drills**, {ran} with a recorded run (`Checked`), {len(rows) - ran} not yet run. Levels: "
           + ", ".join(f"{k} {v}" for k, v in sorted(collections.Counter(r[2] for r in rows).items())) + ".\n\n"
           + table(["ID", "Ch", "Level", "Drill", "Checked"], rows))
    put_block(LEARN / "E-drills.md", APPENDICES["E-drills.md"],
              "Every drill has a task, a verify command and an answer key. Run the ones marked *not run* and send the result as a PR to the chapter.", gen)

    # F source map
    refs = collections.defaultdict(lambda: collections.defaultdict(set))
    for c in chs:
        for m in re.finditer(r"([A-Za-z0-9_][A-Za-z0-9_.\-]*)@([0-9a-f]{7,12})\b", c.text):
            refs[m.group(1)][m.group(2)].add(c.num)
    rows = []
    for repo in sorted(refs):
        for sha in sorted(refs[repo]):
            rows.append([f"`{repo}`", f"`{sha}`", ", ".join(sorted(refs[repo][sha]))])
    gen = f"{len(rows)} (repo, commit) pairs cited. A number holds only at the commit named beside it.\n\n" + table(["Repo", "Commit", "Chapters"], rows)
    put_block(LEARN / "F-source-map.md", APPENDICES["F-source-map.md"],
              "Every `repo@sha` cited anywhere in the chapters, with the chapters that cite it.", gen)

    # A instruments
    inst = collections.defaultdict(lambda: [0, set(), collections.Counter()])
    for c, r in nums:
        k = re.sub(r"\s+", " ", L.strip_md(r[4]))
        inst[k][0] += 1
        inst[k][1].add(c.num)
        inst[k][2][L.grade_of(r[3]) or "?"] += 1
    rows = [[f"`{k}`", v[0], ", ".join(sorted(v[1])), " ".join(f"{g}:{n}" for g, n in sorted(v[2].items()))]
            for k, v in sorted(inst.items(), key=lambda kv: (-kv[1][0], kv[0]))]
    gen = f"{len(rows)} distinct instrument strings across the numbers registers.\n\n" + table(["Instrument as written", "Numbers", "Chapters", "Grades"], rows)
    put_block(LEARN / "A-validator-register.md", APPENDICES["A-validator-register.md"],
              "Which validator, renderer, rig or checkout stands behind each number. The hand-written part describes the pins; the table below is generated.", gen)


def build_chapter_table(chs):
    rows = []
    for c in chs:
        say = c.say if len(c.say) < 220 else c.say[:217].rstrip() + "..."
        rows.append([f"[{c.num}]({c.name})", c.title_plain, say, len(c.heuristics), len(c.drills), len(c.numbers), f"{c.bytes // 1024} KB"])
    tbl = table(["Ch", "Title", "Say it", "Rules", "Drills", "Numbers", "Size"], rows)
    p = LEARN / "00-start-here.md"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    b, e = "<!-- BEGIN CHAPTER-TABLE -->", "<!-- END CHAPTER-TABLE -->"
    if b in t and e in t:
        t = re.sub(re.escape(b) + r".*?" + re.escape(e), lambda m: f"{b}\n{tbl}\n{e}", t, flags=re.S)
        p.write_text(t, encoding="utf-8")


# ------------------------------------------------------------------ HTML
CSS = """
:root{--bg:#1a1a19;--panel:#232321;--line:#383835;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#8a8a85;--link:#86b6ef;--code:#262624}
@media (prefers-color-scheme:light){:root:not([data-theme=dark]){--bg:#faf9f6;--panel:#f1efe9;--line:#d8d5cb;--ink:#1c1c1a;--ink2:#46463f;--ink3:#77766d;--link:#1f5fb5;--code:#ebe8df}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
a{color:var(--link)}.wrap{display:grid;grid-template-columns:1fr;max-width:1320px;margin:0 auto}
@media(min-width:1000px){.wrap{grid-template-columns:260px minmax(0,1fr)}}
.side{padding:1.2rem 1rem;font-size:.86rem;border-right:1px solid var(--line)}
@media(min-width:1000px){.side{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto}}
.side b.t{display:block;font-size:1rem;margin-bottom:.3rem}.side a{display:block;color:var(--ink2);text-decoration:none;padding:.18rem 0}
.side a:hover,.side a.cur{color:var(--ink)}.side a.cur{font-weight:600}.side h4{margin:1rem 0 .3rem;color:var(--ink3);font:600 .72rem/1 system-ui;letter-spacing:.08em;text-transform:uppercase}
main{padding:1.6rem 1.25rem 5rem;min-width:0;max-width:1000px}
h1{font-size:1.9rem;line-height:1.2;margin:.2rem 0 1rem}h2{font-size:1.4rem;border-bottom:1px solid var(--line);padding-bottom:.3rem;margin-top:2.4rem}h3{font-size:1.1rem;margin-top:1.8rem}
code{background:var(--code);padding:.08rem .3rem;border-radius:3px;font-size:.9em}
pre{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:.8rem 1rem;overflow:auto;line-height:1.35;font-size:.82rem}pre code{background:none;padding:0;font-size:inherit}
table{border-collapse:collapse;display:block;overflow:auto;margin:1rem 0;font-size:.88rem;max-width:100%}th,td{border:1px solid var(--line);padding:.32rem .55rem;vertical-align:top;text-align:left}th{background:var(--panel);position:sticky;top:0}
blockquote{margin:1rem 0;padding:.4rem 1rem;border-left:3px solid #d95926;background:var(--panel)}blockquote p{margin:.3rem 0}
.g{font:700 .68rem/1.5 ui-monospace,Consolas,monospace;display:inline-block;min-width:1.5em;text-align:center;padding:0 .3em;border-radius:3px;vertical-align:.08em}
.g.C{background:var(--ink);color:var(--bg);border:1px solid var(--ink)}.g.L{border:1px solid var(--ink)}.g.S{border:1px dashed var(--ink3);color:var(--ink2)}
.nav{color:var(--ink3);font-size:.88rem;display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:.5rem}.pn{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line)}
details.toc{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:.4rem .9rem;margin:1rem 0;font-size:.88rem}details.toc summary{cursor:pointer;color:var(--ink2)}details.toc a{display:block;text-decoration:none;padding:.08rem 0}details.toc a.l3{padding-left:1rem;color:var(--ink2)}
.foot{margin-top:3rem;color:var(--ink3);font-size:.82rem}
"""

CHIP_RE = re.compile(r"(?<![\w\[`])\[([CLS])\](?![\w(\]])")


def chips(htm):
    parts = re.split(r"(<pre.*?</pre>|<code>.*?</code>)", htm, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = CHIP_RE.sub(lambda m: f'<span class="g {m.group(1)}" title="{ {"C":"Confirmed","L":"Likely","S":"Suspected"}[m.group(1)] }">{m.group(1)}</span>', parts[i])
    return "".join(parts)


def rewrite_links(htm, here):
    def fix(m):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", href):
            return m.group(0)
        base, _, frag = href.partition("#")
        if base.endswith(".md"):
            tgt = (here.parent / base).resolve()
            name = tgt.name
            if tgt.parent == LEARN.resolve() and name == "00-start-here.md":
                base = base[: -len(name)] + "index.html"
            else:
                base = base[:-3] + ".html"
        return f'href="{base}{"#" + frag if frag else ""}"'
    return re.sub(r'href="([^"]+)"', fix, htm)


def render_all(chs):
    from markdown_it import MarkdownIt
    from mdit_py_plugins.anchors import anchors_plugin

    md = MarkdownIt("commonmark", {"html": True}).enable("table").use(anchors_plugin, min_level=2, max_level=3, permalink=False)
    order = [(c.name, f"{c.num}. {c.title_plain}") for c in chs]
    files = sorted(LEARN.glob("*.md"))
    nav_ch = [(n, t) for n, t in order]
    apps = [(n, t) for n, t in APPENDICES.items() if (LEARN / n).exists()]
    ext = [(n, t) for n, t in EXTRA.items() if (LEARN / n).exists()]
    seq = [n for n, _ in nav_ch] + [n for n, _ in apps]
    for p in files:
        src = p.read_text(encoding="utf-8")
        body = md.render(src)
        m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else p.stem
        heads = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body, re.S)
        toc = ""
        if len(heads) > 4:
            items = "".join(f'<a class="l{lv}" href="#{i}">{html.escape(html.unescape(re.sub("<[^>]+>", "", t)))}</a>' for lv, i, t in heads)
            toc = f'<details class="toc"><summary>On this page ({len(heads)} sections)</summary>{items}</details>'
            body = body.replace("</h1>", "</h1>\n" + toc, 1)
        body = chips(rewrite_links(body, p))
        is_hub = p.name == "00-start-here.md"
        out = LEARN / ("index.html" if is_hub else p.with_suffix(".html").name)

        def navlink(n, t):
            href = "index.html" if n == "00-start-here.md" else n[:-3] + ".html"
            cur = ' class="cur"' if n == p.name else ""
            return f'<a{cur} href="{href}">{html.escape(t)}</a>'
        side = (f'<b class="t">{SITE}</b><a href="../index.html">&larr; all teardowns</a>'
                + navlink("00-start-here.md", "Start here" if (LEARN / "00-start-here.md").exists() else "")
                + "<h4>Chapters</h4>" + "".join(navlink(n, t) for n, t in nav_ch if n != "00-start-here.md")
                + "<h4>Appendices</h4>" + "".join(navlink(n, t) for n, t in apps)
                + "<h4>About</h4>" + "".join(navlink(n, t) for n, t in ext))
        pn = ""
        if p.name in seq:
            i = seq.index(p.name)
            prv = f'<a href="{seq[i - 1][:-3]}.html">&larr; {html.escape(seq[i - 1][:-3])}</a>' if i > 0 else "<span></span>"
            nxt = f'<a href="{seq[i + 1][:-3]}.html">{html.escape(seq[i + 1][:-3])} &rarr;</a>' if i + 1 < len(seq) else "<span></span>"
            pn = f'<div class="pn">{prv}{nxt}</div>'
        navbar = f'<div class="nav"><a href="index.html">{SITE}</a><a href="{p.name}">Markdown source</a><a href="https://github.com/hagopjay/x3d.docs/blob/gh-pages/docs/learn/{p.name}">GitHub</a></div>'
        page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>{html.escape(title)} · {SITE}</title><style>{CSS}</style></head><body><div class="wrap"><nav class="side">{side}</nav>'
                f'<main>{navbar}{body}{pn}<p class="foot">Grades: <span class="g C">C</span> confirmed (measured, instrument named) · <span class="g L">L</span> likely · '
                f'<span class="g S">S</span> suspected. Every number names its validator, renderer or rig. Rebuilt by <code>docs/tools-shared/build_learn.py</code>.</p></main></div></body></html>')
        out.write_text(page, encoding="utf-8")
    return len(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args()
    chs = L.chapters()
    build_ledgers(chs)
    build_chapter_table(chs)
    print(f"{len(chs)} chapters; heuristics {sum(len(c.heuristics) for c in chs)}, drills {sum(len(c.drills) for c in chs)}, "
          f"numbers {sum(len(c.numbers) for c in chs)}, bytes {sum(c.bytes for c in chs)}")
    if not a.no_html:
        n = render_all(chs)
        print(f"rendered {n} pages to {LEARN}")


if __name__ == "__main__":
    main()
