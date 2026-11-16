"""Tests for claims_lib / check_claims. Standard library only:  python3 -I -B -m unittest discover -s docs/tools-shared -p 'test_claims.py'
Set X3D_CLAIMS_REPOS to a directory of repo checkouts to also run the mutation check on the committed ledgers."""
import copy
import json
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import claims_lib as CL  # noqa: E402


class Tokens(unittest.TestCase):
    def test_sign_and_decimal_stay_in_the_token(self):
        self.assertEqual(CL.tokens("x = -1.5, 0.25"), ["x", "-1.5", "0.25"])
        self.assertEqual(CL.tokens("range 3-5"), ["range", "3", "5"])
        self.assertEqual(CL.tokens("approved_with_remarks"), ["approved", "with", "remarks"])
        self.assertEqual(CL.tokens("1e-5 and 2.5E+3"), ["1e-5", "and", "2.5e+3"])

    def test_nfkc_and_minus(self):
        self.assertEqual(CL.tokens("Kärki"), CL.tokens("Kärki"))
        self.assertEqual(CL.tokens("−1.5"), ["-1.5"])


class Numbers(unittest.TestCase):
    def reads(self, t):
        return sorted({r for rs in CL.numbers_in(t) for r in rs})

    def test_readings(self):
        self.assertEqual(self.reads("3.000 kg"), [3.0, 3000.0])          # the article's 4.200 limit
        self.assertEqual(self.reads("1.234,50"), [1234.5])
        self.assertEqual(self.reads("1,234.50"), [1234.5])
        self.assertEqual(self.reads("0,5"), [0.5])
        self.assertEqual(self.reads("x -1.5"), [-1.5])
        self.assertEqual(self.reads("3-5"), [3.0, 5.0])

    def test_value_status(self):
        vs = CL.value_status
        self.assertEqual(vs(57468875, '"raw_bytes_total": 57468875'), "match")
        self.assertEqual(vs(57468875, "57,468,875 bytes"), "match")
        self.assertEqual(vs(4.2, "4.200 kg"), "match")                    # ambiguous reading accepted ...
        self.assertEqual(vs(4200, "4.200 kg"), "match")                   # ... both ways, as the article warns
        self.assertEqual(vs(42, "4.200 kg"), "mismatch")
        self.assertEqual(vs(5, "-5"), "mismatch")                         # a sign is part of the number
        self.assertEqual(vs(66.3, "0.6633", transform={"scale": 100, "round": 1}), "match")
        self.assertEqual(vs(66.3, "0.6633"), "mismatch")                   # no declared conversion, no match
        self.assertEqual(vs([0.5, 0.5, 1.0], 'rotation="0.5 0.5 1"'), "match")
        self.assertEqual(vs([0.5, 1.0, 0.5], 'rotation="0.5 0.5 1"'), "mismatch")
        self.assertEqual(vs("Viewpoint", "<Viewpoint DEF='cam'/>"), "match")
        self.assertEqual(vs(None, "x"), "unchecked")
        self.assertEqual(vs(True, "true"), "unchecked")


class Verdicts(unittest.TestCase):
    def test_matrix(self):
        V = CL.verdict_of
        P = CL.Policy()
        self.assertEqual(V("found", "match", 1, "q", P, 1), "verified")
        self.assertEqual(V("found", "match", 1, "q", P, 2), "check")       # a repeated quote needs a place
        self.assertEqual(V("not_found", "match", 1, "q", P, 0), "check")
        self.assertEqual(V("found", "mismatch", 1, "has 2", P, 1), "check")
        self.assertEqual(V("found", "mismatch", 1, "two", P, 1), "unchecked")
        self.assertEqual(V("found", "mismatch", "abc", "q", P, 1), "reworded")
        self.assertEqual(V("unresolved", "match", 1, "q", P, 0), "unchecked")
        self.assertEqual(V("unresolved", "mismatch", 7, "has 8", P, 0), "check")     # wrong inside its own quote, no source needed
        self.assertEqual(V("unresolved", "mismatch", "word", "other", P, 0), "unchecked")
        self.assertEqual(V("moved", "match", 1, "q", CL.Policy(strict_pins=True), 1), "check")


class Entries(unittest.TestCase):
    def setUp(self):
        self.d = pathlib.Path(tempfile.mkdtemp())
        (self.d / "docs").mkdir()
        (self.d / "docs" / "src.txt").write_text("alpha 12 ms\nbeta 12 ms\ngamma 99\n", encoding="utf-8")
        self.r = CL.Resolver(root=self.d)

    def e(self, **kw):
        base = {"id": "N-TST-1", "value": 99, "quote": "gamma 99", "source": "self:docs/src.txt"}
        base.update(kw)
        return CL.check_entry(base, self.r)

    def test_verified_and_located(self):
        it = self.e()
        self.assertEqual((it["verdict"], it["line"], it["occurrences"]), ("verified", 3, 1))

    def test_value_not_in_quote(self):
        self.assertEqual(self.e(value=98)["verdict"], "check")

    def test_quote_not_in_source(self):
        self.assertEqual(self.e(quote="gamma 100", value=100)["verdict"], "check")

    def test_repeated_quote_needs_a_line_hint(self):
        self.assertEqual(self.e(quote="12 ms", value=12)["verdict"], "check")
        self.assertEqual(self.e(quote="12 ms", value=12, line=2)["verdict"], "verified")
        self.assertEqual(self.e(quote="12 ms", value=12, line=3)["verdict"], "check")   # hint names a line without the quote

    def test_external_and_private_never_resolve_in_public(self):
        self.assertEqual(self.e(source="external:vendor page")["verdict"], "unchecked")
        self.assertEqual(self.e(source="private:lab notebook")["verdict"], "unchecked")

    def test_long_quote_is_refused(self):
        self.assertEqual(self.e(quote=" ".join(["w"] * 60), value="w")["verdict"], "check")

    def test_a_404_at_a_pin_is_a_broken_citation_not_an_unreadable_one(self):
        class Gone:
            def get(self, src):
                return None, "missing: x3d.loom@abc1234:a.json does not exist (HTTP 404)"
        class Offline:
            def get(self, src):
                return None, "fetch failed for x3d.loom@abc1234:a.json (URLError)"
        e = {"id": "N-TST-1", "value": 1, "quote": "n 1", "source": "x3d.loom@abc1234:a.json"}
        self.assertEqual(CL.check_entry(e, Gone())["verdict"], "check")
        self.assertEqual(CL.check_entry(e, Offline())["verdict"], "unchecked")       # a flaky network never fails a build by itself


class Suggest(unittest.TestCase):
    class Stub:
        def __init__(self, text):
            self.text = text

        def get(self, src):
            return self.text, "pinned"

    class Ch:
        code = "TST"
        numbers = [["N-TST-1", "q", "1,234 ms; 7", "[C]", "x", "`tools@abc1234:data/x.txt`"],
                   ["N-TST-2", "q", "55", "[L]", "x", "a directory `tools@abc1234:data/`"]]
        heuristics = []

    def test_suggests_only_nontrivial_numbers_of_a_cited_file_and_the_draft_verifies(self):
        import claims_suggest as CS
        stub = self.Stub("alpha\nthe run took 1,234 ms in total and 7 more\nbeta\n")
        out = CS.suggest(self.Ch, stub)
        self.assertEqual([(e["id"], e["value"]) for e in out], [("N-TST-1", 1234)])     # 7 is trivial; row 2 cites a directory
        self.assertEqual(out[0]["grade"], "C")
        self.assertIn("1,234 ms", out[0]["quote"])
        self.assertNotIn("line", out[0])
        self.assertEqual(CL.check_entry(out[0], stub)["verdict"], "verified")

    def test_a_repeated_quote_gets_a_line_hint_and_a_note(self):
        import claims_suggest as CS
        stub = self.Stub("took 1,234 ms\nelse\ntook 1,234 ms\n")
        out = CS.suggest(self.Ch, stub)
        self.assertIn("ambiguous", out[0]["note"])
        self.assertEqual(out[0]["line"], 1)
        self.assertEqual(CL.check_entry(out[0], stub)["verdict"], "verified")


class Links(unittest.TestCase):
    class Ch:
        code = "TST"
        numbers = [["N-TST-1", "q", "1,234 ms; 5 of 9", "[C]", "x", "y"]]
        heuristics = [["H-TST-1", "Keep 7 bars", "C", "seen 3 times", "x"], ["H-TST-2", "Keep 7 bars", "L", "seen 3 times", "x"]]

    def test_link_errors(self):
        good = {"id": "N-TST-1", "value": 1234, "quote": "q", "source": "self:a", "grade": "C", "_line": 2}
        self.assertEqual(CL.check_links(self.Ch, [good])[0], [])
        bad_id = dict(good, id="N-TST-9")
        bad_grade = dict(good, grade="L")
        bad_val = dict(good, value=1235)
        bad_src = dict(good, source="Medium article")
        for e in (bad_id, bad_grade, bad_val, bad_src):
            self.assertTrue(CL.check_links(self.Ch, [e])[0], e)
        self.assertEqual(CL.check_links(self.Ch, [dict(good, id="H-TST-1", value=7, grade="C")])[0], [])
        self.assertEqual(CL.check_links(self.Ch, [dict(good, id="Q-TST-1", value=7)])[0], [])

    def test_a_prose_claim_must_stand_in_the_chapter_text(self):
        class Prose(self.Ch):
            text = "The gate took 0.371 ms and 12 scenes failed."
        q = {"id": "Q-TST-1", "value": 0.371, "quote": "q", "source": "self:a", "_line": 2}
        self.assertEqual(CL.check_links(Prose, [q])[0], [])
        self.assertTrue(CL.check_links(Prose, [dict(q, value=0.372)])[0])

    def test_a_bare_number_is_not_a_quote(self):
        e = {"id": "N-TST-1", "value": 1234, "quote": "1,234", "source": "self:a", "_line": 2}
        self.assertTrue(any("numbers only" in x for x in CL.check_links(self.Ch, [e])[0]))
        self.assertEqual(CL.check_links(self.Ch, [dict(e, quote="took 1,234 ms")])[0], [])

    def test_a_private_repo_is_never_cited_as_repo_at_sha(self):
        e = {"id": "N-TST-1", "value": 1234, "quote": "q", "source": "x3d_ai@abc1234:notes/a.md", "_line": 2}
        self.assertTrue(any("public list" in x for x in CL.check_links(self.Ch, [e])[0]))
        self.assertEqual(CL.check_links(self.Ch, [dict(e, source="x3d.loom@abc1234:a.md")])[0], [])

    def test_carry_edge_never_raises_the_grade(self):
        origin = type("O", (), {"code": "ORG"})
        idx = {"N-ORG-1": (origin, ["N-ORG-1", "q", "0.371 ms", "[L]", "x", "y"]), "N-ORG-2": (origin, ["N-ORG-2", "q", "0.371 ms", "[C]", "x", "y"])}
        e = {"id": "N-TST-1", "value": 1234, "quote": "q", "source": "self:a", "_line": 2}
        self.assertEqual(CL.check_links(self.Ch, [dict(e, **{"from": "N-ORG-2"})], idx)[0][0].split(": ", 1)[1][:6], "value ")   # 1234 not in origin
        e = {"id": "H-TST-1", "value": 7, "quote": "q", "source": "self:a", "_line": 2}
        idx = {"N-ORG-1": (origin, ["N-ORG-1", "q", "7 ms", "[L]", "x", "y"])}
        ok = CL.check_links(self.Ch, [dict(e, id="H-TST-2", grade="L", **{"from": "N-ORG-1"})], idx)[0]
        up = CL.check_links(self.Ch, [dict(e, id="H-TST-1", grade="C", **{"from": "N-ORG-1"})], idx)[0]
        self.assertEqual(ok, [])
        self.assertTrue(any("never rises" in x for x in up), up)
        self.assertTrue(CL.check_links(self.Ch, [dict(e, grade="C", **{"from": "N-NOPE-1"})], idx)[0])

    def test_coverage_counts_register_numbers(self):
        cov = CL.coverage(self.Ch, [{"id": "N-TST-1", "value": 1234}])
        self.assertEqual((cov["values"], cov["values_with_quote"]), (3, 1))


class Private(unittest.TestCase):
    """A private source never publishes its quote: only a digest and a length, graded [S]."""

    def setUp(self):
        self.d = pathlib.Path(tempfile.mkdtemp())
        (self.d / "note.txt").write_text("The lab measured 12.5 ms on the third run and 99 on the fourth.\n", encoding="utf-8")

    class Ch:
        code = "TST"
        numbers = [["N-TST-1", "q", "12.5 ms", "[S]", "x", "y"], ["N-TST-2", "q", "7", "[C]", "x", "y"]]
        heuristics = []

    def test_seal_refuses_a_value_outside_its_quote(self):
        with self.assertRaises(ValueError):
            CL.seal(13, "measured 12.5 ms", "private:note.txt")

    def test_digest_find_without_the_quote(self):
        line = CL.seal(12.5, "measured 12.5 ms on the third run", "private:note.txt", id="N-TST-1")
        self.assertNotIn("quote", line)
        it = CL.check_entry(line, CL.Resolver(private=self.d))
        self.assertEqual((it["status"], it["verdict"], it["occurrences"]), ("found", "unchecked", 1))     # never 'verified' in public
        gone = dict(line, quote_sha256=CL.quote_digest("measured 12.6 ms on the third run"))
        self.assertEqual(CL.check_entry(gone, CL.Resolver(private=self.d))["verdict"], "check")        # sealed words no longer there
        self.assertEqual(CL.check_entry(line, CL.Resolver())["verdict"], "unchecked")                  # public CI cannot look

    def test_link_rules(self):
        ok = dict(CL.seal(12.5, "measured 12.5 ms", "private:note.txt", id="N-TST-1"), _line=2)
        self.assertEqual(CL.check_links(self.Ch, [ok])[0], [])
        self.assertTrue(CL.check_links(self.Ch, [dict(ok, quote="measured 12.5 ms")])[0])              # clear quote of a private source
        self.assertTrue(CL.check_links(self.Ch, [dict(ok, quote_sha256="abc")])[0])
        self.assertTrue(CL.check_links(self.Ch, [dict(ok, id="N-TST-2", value=7)])[0])                  # [C] row on a private source: above the cap
        ext = {"id": "N-TST-2", "value": 7, "quote": "seven 7", "source": "external:vendor page", "_line": 3}
        self.assertTrue(any("cap" in x for x in CL.check_links(self.Ch, [ext])[0]))                    # [C] row on an external source


class Fetch(unittest.TestCase):
    def test_unsafe_paths_never_reach_the_network(self):
        r = CL.Resolver(fetch=True)
        for bad in ("../x", "/etc/passwd", "a/../b", "a?b", "a#b", "a b", "a%2e"):
            self.assertIsNone(r._fetch("x3d.docs", "abc1234", bad)[0], bad)

    @unittest.skipUnless(os.environ.get("X3D_CLAIMS_NET"), "needs network")
    def test_pinned_fetch(self):
        r = CL.Resolver(fetch=True)
        t, how = r.get("x3d.loom@7a7d657:x3d.s1/receipts/corpus-2026-11-16.json")
        self.assertEqual(how, "pinned")
        self.assertIn('"scenes": 499', t)
        self.assertIsNone(CL.Resolver(fetch=True).get("x3d.loom@7a7d657:no/such/file.json")[0])


@unittest.skipUnless(os.environ.get("X3D_CLAIMS_REPOS"), "needs checkouts")
class Mutation(unittest.TestCase):
    """Every planted fault in a committed ledger entry must stop it from being 'verified'."""

    def test_planted_faults(self):
        learn = pathlib.Path(__file__).resolve().parent.parent / "learn" / "claims"
        res = CL.Resolver(repos=os.environ["X3D_CLAIMS_REPOS"], root=pathlib.Path(__file__).resolve().parent.parent.parent)
        n = caught = 0
        for f in sorted(learn.glob("*.jsonl")):
            _, entries, _ = CL.load_ledger(f)
            for e in entries:
                if CL.kind_of(e["source"]) not in ("repo", "self"):
                    continue
                self.assertEqual(CL.check_entry(e, res)["verdict"], "verified", e["id"])
                muts = []
                if isinstance(e["value"], (int, float)):
                    muts.append(dict(e, value=e["value"] + 1))
                    muts.append(dict(e, value=e["value"] * 10 + 7))
                q = e["quote"]
                digs = [i for i, ch in enumerate(q) if ch.isdigit()]
                if digs:
                    i = digs[-1]
                    muts.append(dict(e, quote=q[:i] + str((int(q[i]) + 1) % 10) + q[i + 1:]))   # a different digit in the quote
                muts.append(dict(e, source=e["source"].replace(".json", ".jsn").replace(".md", ".mdx")))
                for m in muts:
                    n += 1
                    if CL.check_entry(m, res)["verdict"] != "verified":
                        caught += 1
        self.assertEqual(caught, n, f"{caught} of {n} planted faults caught")
        print(f"\nmutation check: {caught} of {n} planted faults caught", file=sys.stderr)


if __name__ == "__main__":
    unittest.main()
