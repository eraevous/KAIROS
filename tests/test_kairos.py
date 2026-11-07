"""Self-test for kairos.py: the records-store ownership marker and shell path quoting. Standard library only.

    python3 -m unittest discover -s tests

Nothing here touches the network or the real home folder: HOME/USERPROFILE point at a temporary folder
before kairos.py is imported, and the one call that would run relay-kit is replaced by a fake."""
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
KAIROS = HERE.parent / "kairos.py"


def load_kairos(home: pathlib.Path):
    """Import kairos.py fresh with its HOME-derived constants pointing at `home`."""
    saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
    os.environ["HOME"] = os.environ["USERPROFILE"] = str(home)
    try:
        spec = importlib.util.spec_from_file_location("kairos_under_test", KAIROS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    assert mod.ROOT == home / "Kairos", mod.ROOT
    return mod


class MarkerLogic(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = pathlib.Path(self.tmp.name)
        self.k = load_kairos(self.home)
        self.dec = self.k.RECORDS / "governance" / "decisions.jsonl"
        self.dec.parent.mkdir(parents=True)
        self.calls = []
        # Replace the subprocess runner: record the command, pretend the ledger tool printed the new id.
        self.k.run = lambda cmd, **kw: (self.calls.append(cmd), (0, "DEC-001\n"))[1]

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_ledger_without_marker_is_not_seeded(self):
        self.dec.write_text("", encoding="utf-8")
        r = self.k.step_seed("tester")
        self.assertTrue(r.ok)
        self.assertIn("pre-existing", r.detail)
        self.assertEqual(self.calls, [])
        c = self.k.check_records()
        self.assertTrue(c.ok)
        self.assertIn("pre-existing, left untouched", c.detail)

    def test_marker_and_empty_ledger_seeds_once(self):
        self.dec.write_text("", encoding="utf-8")
        self.k.MARKER.write_text(json.dumps({"created": "2026-11-07T15:00:00Z", "owner": "tester"}), encoding="utf-8")
        c = self.k.check_records()
        self.assertFalse(c.ok, "init ran but the seed did not: check must ask for a resume")
        self.assertIn("created by the Dev Kit on 2026-11-07", c.detail)
        r = self.k.step_seed("tester")
        self.assertTrue(r.ok)
        self.assertEqual(len(self.calls), 1)
        self.assertIn("append", self.calls[0])
        self.assertIn("--offline", self.calls[0])
        row = json.loads(self.calls[0][-1])
        self.assertIn("tester's Kairos records store", row["decision"])
        # The fake did not write the line; a real run would, so simulate it and confirm no second append.
        self.dec.write_text(json.dumps({"id": "DEC-001", "decision": "x"}) + "\n", encoding="utf-8")
        self.calls.clear()
        r2 = self.k.step_seed("tester")
        self.assertTrue(r2.ok)
        self.assertEqual(self.calls, [])
        self.assertIn("created by the Dev Kit on 2026-11-07", self.k.check_records().detail)

    def test_existing_store_without_marker_reports_pre_existing(self):
        self.dec.write_text(json.dumps({"id": "DEC-009", "decision": "someone else's"}) + "\n", encoding="utf-8")
        r = self.k.step_records("tester")
        self.assertTrue(r.ok)
        self.assertIn("not ours", r.detail)
        self.assertFalse(self.k.MARKER.exists())
        c = self.k.check_records()
        self.assertTrue(c.ok)
        self.assertIn("pre-existing, left untouched", c.detail)

    def test_step_records_writes_marker_after_init(self):
        self.dec.parent.rmdir()   # an empty records folder: init may run
        self.k.run = lambda cmd, **kw: (self.calls.append(cmd), (0, "Created\n"))[1]
        r = self.k.step_records("tester")
        self.assertTrue(r.ok)
        self.assertIn("init", self.calls[0])
        m = json.loads(self.k.MARKER.read_text(encoding="utf-8"))
        self.assertEqual(m["owner"], "tester")
        self.assertRegex(m["created"], r"^\d{4}-\d{2}-\d{2}T")


class ShellPaths(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = pathlib.Path(self.tmp.name)
        self.k = load_kairos(self.home)

    def tearDown(self):
        self.tmp.cleanup()

    def test_posix_quoting_is_absolute_and_safe(self):
        self.k.IS_WINDOWS = False
        p = self.home / "Kairos" / "repos" / "my Fathom"
        q = self.k.shell_path(p)
        self.assertTrue(q.startswith("'") and q.endswith("'"), q)
        self.assertIn(str(self.home), q)
        self.assertNotIn("~", q)

    def test_windows_quoting_uses_double_quotes(self):
        self.k.IS_WINDOWS = True
        q = self.k.shell_path(self.home / "Kairos" / "repos" / "Fathom")
        self.assertTrue(q.startswith('"') and q.endswith('"'), q)
        self.assertNotIn("~", q)

    def test_fix_lines_and_next_never_print_tilde_paths(self):
        out = []
        self.k.say = lambda msg="": out.append(msg)
        self.k.cmd_next(None)
        text = "\n".join(out)
        self.assertIn(str(self.home), text)
        for ln in text.splitlines():
            if "--out" in ln or "pip install" in ln or "delete" in ln:
                self.assertNotIn("~/", ln, ln)
        for fix in (self.k.check_cockpit().fix, self.k.check_module("Telosmith").fix):
            self.assertNotIn("~", fix, fix)
            self.assertIn(str(self.home), fix)


if __name__ == "__main__":
    unittest.main()
