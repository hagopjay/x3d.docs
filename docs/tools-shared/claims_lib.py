"""Claim ledger for docs/learn: FIND + COMPARE (and LOCATE as line numbers) over quotes, no model, standard library only.

A chapter's Numbers register says WHAT a base claims; the ledger (docs/learn/claims/<chapter>.jsonl) says WHERE it was read:
one line per value, {id, value, quote, source, grade}. The checker answers three questions in code:
  FIND     is the quote in the cited source, as an unbroken run of lowercase words (punctuation and spacing ignored)?
  COMPARE  is the value inside the quote (numbers as numbers, text by words)?
  LOCATE   line and character span of the quote in the source, so a reader can open it.
Verdicts: verified / check / reworded / unchecked. Coverage = share of register values that came with a ledger entry.
Contract and schema: docs/learn/AUTHORING.md section 7 (claim ledger).

Provenance of the method: adapted from the GAIK toolkit's source_tracing component (MIT). The verdict logic (verdict_of), the Policy
field names and defaults, and the verdict vocabulary follow it. New here: the tokenizer (a number keeps its sign, decimal point and
exponent), the number readings, multi-value lists, declared transforms, the ledger file and its link rules, pinned-source resolution
(git or raw fetch), digest-only private entries, and line location in text.

    GAIK source_tracing, MIT License. Copyright (c) 2026 GAIK - GenAI for knowledge mgt
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
    (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify,
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import dataclasses
import hashlib
import json
import pathlib
import re
import subprocess
import time
import unicodedata
import urllib.error
import urllib.request

SCHEMA = "claims/0.1"
SOURCE_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_.\-]*)@([0-9a-f]{7,40}):(\S.*)$")
VERDICTS = ("verified", "check", "reworded", "unchecked")
KINDS = ("repo", "self", "external", "private")
OWNER = "hagopjay"                                   # GitHub owner of every cited repo unless OWNERS says otherwise
OWNERS = {"castle-engine": "castle-engine"}          # repos cited as repo@sha that live under another owner
# Repos a public ledger may cite as repo@sha:path (raw fetch must work without a token). Anything else is cited as private:<name>.
PUBLIC_REPOS = frozenset({"x3d.ml", "x3d.docs", "x3d.loom", "x3d_mcp", "x3d-blender-io", "x3d.lab", "x3d.castle", "x3d.music",
                          "x3d.mashtots", "x3d.demo", "x3d.xray", "castle-engine", "x3d.accrete", "x3d.chess"})
MAX_FETCH_BYTES = 8_000_000
KIND_GRADE_CAP = {"private": "S", "external": "L"}   # a private note is a lead, an external page is read-not-run (AUTHORING section 5)
RANK = {"C": 3, "L": 2, "S": 1}


# ---- tokens ---------------------------------------------------------------------------------------------------------
# A number keeps its sign, decimal point and exponent ("-1.5" is not "1 5"); a sign counts only when it does not follow a word
# character, so "3-5" is two numbers. Everything else is a run of letters and digits; underscore and punctuation separate.
_NUMTOK = r"(?:(?<![\w.)\]])[+\-])?\d+(?:[.,]\d+)*(?:[eE][+\-]?\d+)?"
TOKEN_RE = re.compile(_NUMTOK + r"|[^\W_]+", re.UNICODE)


def _norm(text):
    return unicodedata.normalize("NFKC", text).replace("−", "-").replace("–", "-").lower()


def tokens(text):
    return [m.group() for m in TOKEN_RE.finditer(_norm(text))]


def token_spans(text):
    """[(token, start, end)] with offsets into the NFKC-normalised text (length-preserving for ASCII sources)."""
    t = _norm(text)
    return [(m.group(), m.start(), m.end()) for m in TOKEN_RE.finditer(t)], t


def find_runs(hay, needle):
    """Start indices of every occurrence of the token run `needle` in `hay` (overlaps counted)."""
    n = len(needle)
    if not n:
        return []
    first = needle[0]
    return [i for i in range(len(hay) - n + 1) if hay[i] == first and hay[i:i + n] == needle]


# ---- numbers ----------------------------------------------------------------------------------------------------------
_RUN_RE = re.compile(r"(?<![\w.])([+\-])?(\d(?:[\d.,'’]*\d)?(?:[eE][+\-]?\d+)?)", re.UNICODE)
_GROUPED = re.compile(r"[1-9]\d{0,2}(?:(?:\.\d{3})+|(?:,\d{3})+)")


def readings_of(run):
    """Every way a digit run can be read: 3.000 is 3.0 and 3000; 1.234,50 is 1234.5; 1,234.50 is 1234.5."""
    raw = run.replace("'", "").replace("’", "")
    out = set()
    if re.fullmatch(r"\d+(?:\.\d+)?[eE][+\-]?\d+", raw):
        out.add(raw)
    else:
        seps = {c for c in raw if c in ",."}
        if not seps:
            out.add(raw)
        elif len(seps) == 1:
            s = next(iter(seps))
            if raw.count(s) > 1 or _GROUPED.fullmatch(raw):
                out.add(raw.replace(s, ""))
            if raw.count(s) == 1:
                out.add(raw.replace(",", "."))
        else:
            dec = raw[max(raw.rfind(","), raw.rfind("."))]
            grp = "," if dec == "." else "."
            out.add(raw.replace(grp, "").replace(dec, "."))
    res = []
    for c in out:
        try:
            res.append(float(c))
        except ValueError:
            pass
    return res


def numbers_in(text):
    """[(set_of_signed_readings, primary_reading)] for each number run in the text, in order."""
    out = []
    for m in _RUN_RE.finditer(_norm(text)):
        sign = -1.0 if m.group(1) == "-" else 1.0
        rs = sorted(sign * r for r in readings_of(m.group(2)))
        if rs:
            out.append(rs)
    return out


def _close(a, b, tol):
    return abs(a - b) <= max(tol, 1e-9 * abs(b))


def as_number(v):
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v.strip()):
        return float(v)
    return None


# ---- policy and COMPARE ---------------------------------------------------------------------------------------------
@dataclasses.dataclass
class Policy:
    number_tolerance: float = 1e-6        # absolute, on top of a 1e-9 relative band
    reworded_is_problem: bool = False     # a text value not in the quote: check instead of reworded
    ambiguous_quote_is_check: bool = True # quote found more than once: check (docs claims need one place)
    min_quote_words: int = 1
    max_quote_words: int = 40             # a quote is evidence, not a copy of the source (licence and size)
    strict_pins: bool = False             # a source found at HEAD instead of its pinned sha: check


def apply_transform(q, tr):
    """Declared conversion from the quote's number to the claimed value: {"scale": 100, "round": 1}. Not a guess: it is written down."""
    if not tr:
        return q
    x = q * float(tr.get("scale", 1)) + float(tr.get("offset", 0))
    return round(x, int(tr["round"])) if "round" in tr else x


def value_status(value, quote, policy=Policy(), transform=None):
    """'match' | 'mismatch' | 'unchecked'. Numbers by reading, lists of numbers in order, text by an unbroken run of words."""
    if value is None or isinstance(value, (bool, dict)):
        return "unchecked"
    if isinstance(value, list) and value and all(as_number(x) is not None for x in value):
        seq = numbers_in(quote)
        want = [as_number(x) for x in value]
        for i in range(len(seq) - len(want) + 1):
            if all(any(_close(apply_transform(r, transform), w, policy.number_tolerance) for r in seq[i + j]) for j, w in enumerate(want)):
                return "match"
        if len(want) > 1 and len(seq) == 1:  # one number broadcast to every component (a cube's size "2" for "2 2 2")
            if all(any(_close(r, w, policy.number_tolerance) for r in seq[0]) for w in want[:1]) and len(set(want)) == 1:
                return "match"
        return "mismatch"
    num = as_number(value)
    if num is not None:
        for rs in numbers_in(quote):
            if any(_close(apply_transform(r, transform), num, policy.number_tolerance) for r in rs):
                return "match"
        return "mismatch"
    text = str(value)
    wanted = tokens(text)
    if not wanted:
        return "unchecked"
    return "match" if find_runs(tokens(quote), wanted) else "mismatch"


def verdict_of(status, vstate, value, quote, policy=Policy(), occurrences=1):
    if status == "unresolved":
        # the source cannot be read here, but a number that is not inside its own quote is wrong without reading anything
        return "check" if vstate == "mismatch" and (as_number(value) is not None or isinstance(value, list)) else "unchecked"
    if status not in ("found", "moved") or len(tokens(quote)) < policy.min_quote_words:
        return "check"
    if policy.strict_pins and status == "moved":
        return "check"
    if vstate == "match":
        return "check" if (policy.ambiguous_quote_is_check and occurrences > 1) else "verified"
    if vstate == "mismatch":
        exact = as_number(value) is not None or isinstance(value, list)
        if not exact:
            return "check" if policy.reworded_is_problem else "reworded"
        return "check" if re.search(r"\d", quote) else "unchecked"
    return "unchecked"


# ---- sources --------------------------------------------------------------------------------------------------------
def kind_of(src):
    if SOURCE_RE.match(src or ""):
        return "repo"
    for k in ("self", "external", "private"):
        if (src or "").startswith(k + ":"):
            return k
    return None


def _safe_path(path):
    """A published path inside a repo: no parent steps, no query, no fragment, no scheme, no absolute path."""
    return bool(path) and not path.startswith("/") and ".." not in path.split("/") and not re.search(r"[?#%\\\s]", path)


def quote_digest(quote):
    """sha256 of the token run of a quote: what a private ledger line publishes instead of the quote itself."""
    return hashlib.sha256(" ".join(tokens(quote)).encode("utf-8")).hexdigest()


class Resolver:
    """Turns a source string into text.
    repos:   directory holding one checkout per repo name (read-only `git show`, then the working-tree file as a 'moved' fallback).
    fetch:   when no checkout answers, GET https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path> (public repos only, stdlib,
             size capped, cached under `cache`). A pinned sha is then always available, so 'moved' cannot happen.
    private: directory with private sources, for `private:<name>` (read here, never published).
    self:    a path under this repo's root. external never resolves."""

    def __init__(self, repos=None, root=None, fetch=False, cache=None, private=None, timeout=20):
        self.repos = pathlib.Path(repos) if repos else None
        self.root = pathlib.Path(root) if root else None
        self.fetch = fetch
        self.cache_dir = pathlib.Path(cache) if cache else None
        self.private = pathlib.Path(private) if private else None
        self.timeout = timeout
        self.cache = {}
        self.fetched = 0

    def get(self, src):
        """-> (text or None, status) with status in pinned / moved / a reason string."""
        if src in self.cache:
            return self.cache[src]
        r = self._get(src)
        self.cache[src] = r
        return r

    def _fetch(self, repo, sha, path):
        if not _safe_path(path):
            return None, f"unsafe path {path!r}"
        owner = OWNERS.get(repo, OWNER)
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{path}"
        key = hashlib.sha256(url.encode()).hexdigest()
        if self.cache_dir:
            f = self.cache_dir / key
            if f.is_file():
                return f.read_text(encoding="utf-8", errors="replace"), "pinned"
        err = "no attempt"
        for attempt in range(3):           # a flaky network must not turn a verified claim into a failed build
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "x3d-docs-claims/0.1"}), timeout=self.timeout) as r:
                    data = r.read(MAX_FETCH_BYTES + 1)
                break
            except urllib.error.HTTPError as ex:
                if ex.code == 404:      # definitive: that path does not exist at that sha in a public repo
                    return None, f"missing: {repo}@{sha}:{path} does not exist (HTTP 404)"
                err = f"HTTP {ex.code}"
            except (urllib.error.URLError, OSError) as ex:
                err = type(ex).__name__
            time.sleep(1.5 * (attempt + 1))
        else:
            return None, f"fetch failed for {repo}@{sha}:{path} ({err})"
        if len(data) > MAX_FETCH_BYTES:
            return None, f"{path} larger than {MAX_FETCH_BYTES} bytes"
        self.fetched += 1
        text = data.decode("utf-8", "replace")
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            (self.cache_dir / key).write_text(text, encoding="utf-8")
        return text, "pinned"

    def _get(self, src):
        k = kind_of(src)
        if k == "repo":
            repo, sha, path = SOURCE_RE.match(src).groups()
            d = self.repos / repo if self.repos else None
            if d is not None and d.is_dir():
                try:
                    out = subprocess.run(["git", "-C", str(d), "show", f"{sha}:{path}"], capture_output=True, timeout=30)
                    if out.returncode == 0:
                        return out.stdout.decode("utf-8", "replace"), "pinned"
                except (OSError, subprocess.SubprocessError):
                    pass
            if self.fetch:
                got = self._fetch(repo, sha, path)
                if got[0] is not None:
                    return got
                if d is None or not d.is_dir():
                    return got
            if d is None or not d.is_dir():
                return None, "no checkout of " + repo
            f = d / path
            if f.is_file():
                return f.read_text(encoding="utf-8", errors="replace"), "moved"
            return None, f"{path} not in {repo}"
        if k == "self":
            if not self.root:
                return None, "no root"
            f = (self.root / src[5:]).resolve()
            if self.root.resolve() in f.parents and f.is_file():
                return f.read_text(encoding="utf-8", errors="replace"), "pinned"
            return None, "self path not found"
        if k == "private" and self.private:
            f = (self.private / src[8:]).resolve()
            if self.private.resolve() in f.parents and f.is_file():
                return f.read_text(encoding="utf-8", errors="replace"), "pinned"
            return None, "private source not found under --private"
        return None, "source kind cannot be checked in public: " + (k or "unknown")


# ---- the check of one entry -----------------------------------------------------------------------------------------
def seal(value, quote, source, **extra):
    """Ledger line for a PRIVATE source: the quote is not published, only its digest and length. The value must be inside the quote now,
    because nobody can re-check that part later in public."""
    if value_status(value, quote) != "match":
        raise ValueError("value is not inside the quote; refusing to seal")
    n = len(tokens(quote))
    return dict({"value": value, "source": source, "quote_sha256": quote_digest(quote), "quote_words": n, "grade": "S"}, **extra)


def _check_private(e, resolver, item):
    """FIND by digest: slide a window of quote_words tokens over the private source and compare sha256. COMPARE cannot run without the
    quote, so the verdict never rises above 'unchecked' here; what the hit proves is that the source still holds the sealed words."""
    n = int(e.get("quote_words") or 0)
    text, how = resolver.get(item["document"])
    if text is None or n < 1:
        item.update(status="unresolved", value_status="unchecked", verdict="unchecked", note=how if text is None else "quote_words missing")
        return item
    toks = tokens(text)
    want = e["quote_sha256"]
    hits = [i for i in range(len(toks) - n + 1) if hashlib.sha256(" ".join(toks[i:i + n]).encode("utf-8")).hexdigest() == want]
    item.update(status="found" if hits else "not_found", occurrences=len(hits), value_status="unchecked", pin=how,
                verdict="unchecked" if hits else "check",
                note="private: sealed words found by digest; value not comparable in public" if hits else "private: sealed words not found by digest")
    return item


def check_entry(e, resolver, policy=Policy()):
    """-> item dict (GAIK-shaped field names plus ours)."""
    quote = e.get("quote") or ""
    src = e.get("source") or ""
    value = e.get("value")
    item = {"field": e.get("id"), "value": value, "quote": quote, "document": src, "status": None, "value_status": None,
            "verdict": None, "occurrences": 0, "line": None, "lines": [], "span": None, "pin": None, "note": ""}
    if not quote and kind_of(src) == "private" and e.get("quote_sha256"):
        return _check_private(e, resolver, item)
    if len(tokens(quote)) > policy.max_quote_words:
        item.update(status="not_found", value_status="unchecked", verdict="check", note=f"quote longer than {policy.max_quote_words} words")
        return item
    text, how = resolver.get(src)
    if text is None and how.startswith("missing:"):
        item.update(status="not_found", value_status="unchecked", verdict="check", note=how)
        return item
    if text is None:
        item.update(status="unresolved", value_status=value_status(value, quote, policy, e.get("transform")), note=how)
        item["verdict"] = verdict_of("unresolved", item["value_status"], value, quote, policy)
        return item
    spans, norm = token_spans(text)
    hay = [t for t, _, _ in spans]
    needle = tokens(quote)
    hits = find_runs(hay, needle)
    item["occurrences"] = len(hits)
    item["lines"] = [norm.count("\n", 0, spans[h][1]) + 1 for h in hits]
    at = e.get("line")
    status = "not_found"
    if hits:
        status = "found"
        pick = hits[0]
        if at is not None:
            lines = [norm.count("\n", 0, spans[h][1]) + 1 for h in hits]
            near = [h for h, ln in zip(hits, lines) if ln == at]
            if near:
                pick, hits = near[0], near[:1]
                item["occurrences"] = 1
            else:
                status = "moved"
        item["line"] = norm.count("\n", 0, spans[pick][1]) + 1
        item["span"] = [spans[pick][1], spans[pick + len(needle) - 1][2]]
    if how == "moved" and status == "found":
        status = "moved"
        item["note"] = "pinned sha not available; read from the checkout's current file"
    item["status"] = status
    item["pin"] = how
    item["value_status"] = value_status(value, quote, policy, e.get("transform")) if hits else "unchecked"
    item["verdict"] = verdict_of(status, item["value_status"], value, quote, policy, item["occurrences"])
    return item


# ---- ledger files and the chapter link ------------------------------------------------------------------------------
def load_ledger(path):
    """-> (meta dict, [entries], [problems]). One JSON object per line; a line starting with '#' or empty is skipped;
    the first object may be {"_meta": {...}}."""
    meta, entries, problems = {}, [], []
    for n, line in enumerate(pathlib.Path(path).read_text(encoding="utf-8").splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            o = json.loads(s)
        except json.JSONDecodeError as ex:
            problems.append(f"line {n}: not JSON ({ex.msg})")
            continue
        if not isinstance(o, dict):
            problems.append(f"line {n}: not an object")
        elif "_meta" in o:
            meta = o["_meta"]
        else:
            o["_line"] = n
            entries.append(o)
    return meta, entries, problems


_NUM_IN_CELL = re.compile(r"(?<![\w.#/@\-])\d[\d,]*(?:\.\d+)?(?![\d@])")


def cell_numbers(cell):
    """American-notation numbers in a register cell (thousands comma, decimal point); inline code is skipped."""
    s = re.sub(r"`[^`]*`", " ", cell)
    return [float(m.group().replace(",", "")) for m in _NUM_IN_CELL.finditer(s)]



def check_links(chapter, entries, index=None):
    """Ledger entry <-> chapter register. index: {row id: (chapter, row)} over the whole base, for carry edges ("from")."""
    errs, warns = [], []
    nrows = {r[0]: r for r in chapter.numbers if len(r) >= 6}
    hrows = {r[0]: r for r in chapter.heuristics if len(r) >= 5}
    seen = set()
    for e in entries:
        ln = e.get("_line")
        sk = kind_of(e.get("source") or "")
        for k in ("id", "source") + (() if sk == "private" else ("quote",)):
            if not e.get(k):
                errs.append(f"ledger line {ln}: missing '{k}'")
        if e.get("quote") and not any(not re.fullmatch(r"[+\-]?[\d.,e+\-]+", t) for t in tokens(e["quote"])):
            errs.append(f"ledger line {ln}: a quote of numbers only proves nothing about where it was read; quote the key or label beside the number")
        if sk == "private":
            if e.get("quote"):
                errs.append(f"ledger line {ln}: a private source never publishes its quote; use quote_sha256 and quote_words (claims_lib.seal)")
            if not re.fullmatch(r"[0-9a-f]{64}", e.get("quote_sha256") or "") or not isinstance(e.get("quote_words"), int) or e["quote_words"] < 1:
                errs.append(f"ledger line {ln}: a private source needs quote_sha256 (64 hex) and quote_words (>= 1)")
        if "value" not in e:
            errs.append(f"ledger line {ln}: missing 'value'")
        i = e.get("id", "")
        if i not in nrows and i not in hrows and not i.startswith(f"Q-{chapter.code}-"):
            errs.append(f"ledger line {ln}: id {i!r} is not a row of this chapter (want N-/H-{chapter.code}-n or Q-{chapter.code}-n)")
            continue
        if sk == "repo" and SOURCE_RE.match(e["source"]).group(1) not in PUBLIC_REPOS:
            errs.append(f"ledger line {ln}: repo {SOURCE_RE.match(e['source']).group(1)!r} is not on the public list (claims_lib.PUBLIC_REPOS); cite a private repo as private:<name>")
        if e.get("source") and kind_of(e["source"]) is None:
            errs.append(f"ledger line {ln}: source {e['source']!r} must be repo@sha:path, self:path, external:label or private:label")
        key = (i, json.dumps(e.get("value")), e.get("quote"))
        if key in seen:
            warns.append(f"ledger line {ln}: duplicate entry for {i}")
        seen.add(key)
        reg = nrows.get(i) or hrows.get(i)
        if reg is not None and e.get("grade"):
            from_reg = re.search(r"\b([CLS])\b", re.sub(r"[\[\]*`]", "", reg[3] if i in nrows else reg[2]))
            if from_reg and from_reg.group(1) != e["grade"]:
                errs.append(f"ledger line {ln}: grade {e['grade']} differs from the register's {from_reg.group(1)} for {i}")
        if i.startswith("Q-") and as_number(e.get("value")) is not None and getattr(chapter, "text", None) is not None:
            want = as_number(e["value"])                     # a prose claim: its number must stand somewhere in the chapter text
            if not any(_close(c, want, 1e-9) for c in cell_numbers(chapter.text)):
                errs.append(f"ledger line {ln}: value {e['value']} does not occur in the text of the chapter ({i})")
        cellix = {"quantity": 1, "value": 2, "instrument": 4, "source": 5}.get(e.get("in", "value"), 2)
        reg_cells = nrows[i][cellix] if i in nrows else (hrows[i][1] + " " + hrows[i][3]) if i in hrows else None
        if reg_cells is not None and as_number(e.get("value")) is not None:
            want = as_number(e["value"])
            if not any(_close(c, want, 1e-9) for c in cell_numbers(reg_cells)):
                errs.append(f"ledger line {ln}: value {e['value']} is not in the {e.get('in', 'value').title() if i in nrows else 'Rule or Evidence'} cell of {i} ({reg_cells[:60]!r})")
        if e.get("from") is not None:                      # a carried number: the origin row must hold it, and the grade may not rise
            org = (index or {}).get(e["from"])
            if org is None:
                errs.append(f"ledger line {ln}: 'from' {e['from']!r} is not a row of any chapter")
            else:
                och, orow = org
                cells = " ".join(orow[1:])
                if as_number(e.get("value")) is not None and not any(_close(c, as_number(e["value"]), 1e-9) for c in cell_numbers(cells)):
                    errs.append(f"ledger line {ln}: value {e['value']} is not in the origin row {e['from']}")
                og = re.search(r"\b([CLS])\b", re.sub(r"[\[\]*`]", "", orow[3] if e["from"].startswith("N-") else orow[2]))
                mine = e.get("grade") or (re.search(r"\b([CLS])\b", re.sub(r"[\[\]*`]", "", reg[3] if i in nrows else reg[2])) if reg else None)
                mine = mine.group(1) if hasattr(mine, "group") else mine
                if og and mine and RANK[mine] > RANK[og.group(1)]:
                    errs.append(f"ledger line {ln}: {i} is [{mine}] but its origin {e['from']} is [{og.group(1)}]; a carried number never rises in grade")
        cap = KIND_GRADE_CAP.get(sk)
        if cap and reg is not None:
            rg = re.search(r"\b([CLS])\b", re.sub(r"[\[\]*`]", "", reg[3] if i in nrows else reg[2]))
            top = max([x for x in (rg.group(1) if rg else None, e.get("grade")) if x], key=lambda x: RANK[x], default=None)
            if top and RANK[top] > RANK[cap]:
                errs.append(f"ledger line {ln}: grade {top} is above the cap [{cap}] for a {sk} source ({i})")
    return errs, warns


def coverage(chapter, entries, verified=None):
    """Register rows and register numbers that carry a ledger entry. The numbers denominator is the count of numbers in Value cells.
    verified: optional set of (id, value) pairs whose verdict is 'verified', for the stricter figure."""
    ids = {e.get("id") for e in entries}
    rows = [r for r in chapter.numbers if len(r) >= 6]
    cov_rows = sum(1 for r in rows if r[0] in ids)
    total_vals = covered_vals = verified_vals = 0
    for r in rows:
        nums = cell_numbers(r[2])
        mine = [as_number(e.get("value")) for e in entries if e.get("id") == r[0] and e.get("in", "value") == "value"]
        mine = [m for m in mine if m is not None]
        ver = [as_number(e.get("value")) for e in entries if e.get("id") == r[0] and e.get("in", "value") == "value"
               and verified is not None and (r[0], json.dumps(e.get("value"))) in verified]
        ver = [m for m in ver if m is not None]
        total_vals += len(nums)
        covered_vals += sum(1 for n in nums if any(_close(n, m, 1e-9) for m in mine))
        verified_vals += sum(1 for n in nums if any(_close(n, m, 1e-9) for m in ver))
    return {"rows": len(rows), "rows_with_ledger": cov_rows, "values": total_vals, "values_with_quote": covered_vals,
            "values_verified": verified_vals, "coverage": (covered_vals / total_vals) if total_vals else None,
            "verified_coverage": (verified_vals / total_vals) if total_vals else None}
