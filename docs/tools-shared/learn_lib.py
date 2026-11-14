"""Shared parsing for the docs/learn knowledge base: chapters, heuristics, drills, numbers, instruments.

Stdlib only. Used by build_learn.py (ledgers + HTML) and check_learn.py (lint + leak sweep).
Format contract: docs/learn/AUTHORING.md section 3.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEARN = ROOT / "learn"
CHAPTER_RE = re.compile(r"^(?!00-)(\d\d)-[a-z0-9_\-]+\.md$")  # 00-start-here.md is the hub, not a chapter
GRADES = ("C", "L", "S")

REQUIRED_HEADINGS = [
    ("## 1. The map", r"^## 1\. The map\s*$"),
    ("## Heuristics", r"^## Heuristics\s*$"),
    ("## Drills", r"^## Drills\s*$"),
    ("## Honest limits", r"^## Honest limits\s*$"),
    ("## Numbers register", r"^## Numbers register\s*$"),
    ("## Sources and provenance", r"^## Sources and provenance\s*$"),
]


def split_row(line):
    """Split one markdown table row on unescaped pipes."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def section(text, heading_re):
    """Body of the '## ' section whose heading matches heading_re (up to the next '## ' heading)."""
    m = re.search(heading_re, text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(r"^## ", rest, re.M)
    return rest[: n.start()] if n else rest


def strip_md(s):
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return s.strip()


def grade_of(cell):
    m = re.search(r"\[?\b([CLS])\b\]?", strip_md(cell))
    return m.group(1) if m else None


class Chapter:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.name = self.path.name
        self.text = self.path.read_text(encoding="utf-8")
        self.num = self.name[:2]
        m = re.search(r"^# (.+)$", self.text, re.M)
        self.title = m.group(1).strip() if m else self.name
        self.title_plain = re.sub(r"^\d+\.\s*", "", self.title)
        self.code = None
        self.meta = {}
        for line in self.text.splitlines()[:40]:
            if line.startswith("|") and "---" not in line:
                cells = split_row(line)
                if len(cells) >= 2 and cells[0].lower() not in ("field",):
                    self.meta[cells[0].lower()] = cells[1]
        c = self.meta.get("chapter code", "")
        m = re.search(r"([A-Z]{2,4})", c)
        self.code = m.group(1) if m else None
        m = re.search(r"^>\s*\*\*Say it:\*\*\s*(.+)$", self.text, re.M)
        self.say = m.group(1).strip() if m else ""
        self.heuristics = self._rows(r"^## Heuristics\s*$", r"H-[A-Z]{2,4}-\d+")
        self.numbers = self._rows(r"^## Numbers register\s*$", r"N-[A-Z]{2,4}-\d+")
        self.drills = self._drills()
        self.fences = re.findall(r"^```(\w*)\s*$", self.text, re.M)
        self.diagrams = len(re.findall(r"^```text\s*$", self.text, re.M))
        self.tables = len(re.findall(r"^\|[\s:|-]{3,}\|\s*$", self.text, re.M))
        self.bytes = len(self.text.encode("utf-8"))

    def _rows(self, heading_re, id_re):
        body = section(self.text, heading_re)
        rows = []
        for line in body.splitlines():
            if re.match(r"^\|\s*" + id_re + r"\s*\|", line):
                rows.append(split_row(line))
        return rows

    def _drills(self):
        body = section(self.text, r"^## Drills\s*$")
        out = []
        parts = re.split(r"^### (?=D-)", body, flags=re.M)
        for p in parts[1:]:
            head, _, rest = p.partition("\n")
            d = {"head": head.strip(), "id": head.split()[0] if head.split() else ""}
            for key in ("Level", "Task", "Verify", "Answer", "Checked"):
                m = re.search(r"^[-*]\s*\*\*" + key + r":?\*\*:?\s*(.+?)(?=^[-*]\s*\*\*|\Z)", rest, re.M | re.S)
                d[key.lower()] = m.group(1).strip() if m else ""
            out.append(d)
        return out


def chapters():
    out = []
    for p in sorted(LEARN.iterdir()):
        if CHAPTER_RE.match(p.name):
            out.append(Chapter(p))
    return out


# ---- leak sweep (docs/learn is PUBLIC) -------------------------------------------------------
LEAK_PATTERNS = [
    # (name, regex, severity)
    ("private-link", r"claude\.ai/", "error"),
    ("session-id", r"\b(cmsg_|cse_|session_01)[A-Za-z0-9]+", "error"),
    ("api-key-aiza", r"AIza[0-9A-Za-z_\-]{20,}", "error"),
    ("api-key-sk", r"\bsk-[A-Za-z0-9_\-]{20,}", "error"),
    ("api-key-gh", r"\b(ghp_|gho_|ghs_|github_pat_)[A-Za-z0-9_]{16,}", "error"),
    ("api-key-hf", r"\bhf_[A-Za-z0-9]{20,}", "error"),
    ("api-key-aws", r"\bAKIA[0-9A-Z]{16}\b", "error"),
    ("private-key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "error"),
    ("email", r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+\.[A-Za-z]{2,}", "error"),
    ("windows-path", r"[A-Za-z]:\\\\?(Users|Windows)", "error"),
    ("local-path", r"(/home/user/|/mnt/project-files|/tmp/claude|/root/\.claude)", "error"),
    ("gcp-id", r"(polyx-planet|gs://|\.iam\.gserviceaccount|projects/[a-z0-9\-]+/locations)", "error"),
    ("owner-alias", r"\b(hagsmac|Jason|zenodelic)\b", "error"),
    ("shroud", r"\bShroud\b", "error"),
    ("unpublished-lab", r"\b(SLJM|Michel lab|Michel's lab|Sarah Lucie)\b", "warn"),
    ("held-or-unsent", r"\b(HELD|unsent|not yet sent|until .{0,20}says? .?send)\b", "warn"),
    ("spend", r"(\$\s?\d+(\.\d+)?\s?(k|M)?\b.{0,30}(spend|credit|billing|cap)|spending cap|out of credit)", "warn"),
    ("marble-key", r"\bMarble\b.{0,40}\b(key|API)\b", "warn"),
    ("chat-quote", r"\b(his words|owner's words|HagopJay (said|wrote|asked))\b", "warn"),
]


def leak_sweep(text, name=""):
    hits = []
    for label, rx, sev in LEAK_PATTERNS:
        for m in re.finditer(rx, text, re.I if label in ("owner-alias",) else 0):
            ln = text.count("\n", 0, m.start()) + 1
            hits.append((sev, label, ln, m.group(0)[:60]))
    return hits
