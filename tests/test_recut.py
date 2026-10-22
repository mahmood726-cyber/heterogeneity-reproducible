"""Filesystem contract tests only; no simulated numerical validation results."""
import contextlib
import hashlib
import importlib.util
import io
import shutil
import uuid
import unittest
from pathlib import Path
from unittest.mock import patch

ARCHIVE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("recut", ARCHIVE / "scripts/recut.py")
recut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recut)


class RecutContracts(unittest.TestCase):
    def setUp(self):
        # Inherit workspace ACLs; mkdtemp's 0700 mode excludes some Windows sandbox identities.
        self.root = ARCHIVE.parent / ("_recut_test_" + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(self.cleanup_workspace)
        (self.root / "fixture.txt").write_bytes(b"test fixture\n")
        self.hashes = {"fixture.txt": hashlib.sha256(b"test fixture\n").hexdigest()}

    def cleanup_workspace(self):
        target = self.root.resolve()
        if target.parent != ARCHIVE.parent.resolve() or not target.name.startswith("_recut_test_"):
            raise ValueError("Refusing cleanup outside the test workspace")
        shutil.rmtree(target)

    def test_original_bytes_pass(self):
        self.assertEqual(recut.verify_hashes(self.hashes, self.root), 1)

    def test_tampering_fails(self):
        (self.root / "fixture.txt").write_bytes(b"changed fixture\n")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            recut.verify_hashes(self.hashes, self.root)

    def test_missing_file_fails(self):
        with self.assertRaisesRegex(ValueError, "missing file"):
            recut.verify_hashes({"missing.txt": self.hashes["fixture.txt"]}, self.root)

    def test_empty_manifest_fails(self):
        with self.assertRaisesRegex(ValueError, "Empty"):
            recut.verify_hashes({}, self.root)

    def test_path_escape_fails(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            recut.verify_hashes({"../fixture.txt": self.hashes["fixture.txt"]}, self.root)

    def test_generated_and_preserved_outputs_excluded(self):
        for folder in ("results", "outputs", "full.prev-1", "node_modules", "tmp", "temp",
                       ".tmp", ".pytest_cache", "_recut_test_fixture", "scratch.tmp"):
            p = self.root / folder
            p.mkdir()
            (p / "fixture.txt").write_bytes(b"ignored test fixture")
        self.assertEqual(recut.inventory(self.root), self.hashes)

    def test_preserve_keeps_previous_runs_and_uses_next_number(self):
        for area in ("results", "outputs"):
            p = self.root / area
            (p / "full").mkdir(parents=True)
            (p / "full" / "new.txt").write_bytes(b"new test fixture")
            (p / "full.prev-1").mkdir()
            (p / "full.prev-1" / "old.txt").write_bytes(b"old test fixture")
        with patch.object(recut, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            recut.preserve("full")
        for area in ("results", "outputs"):
            p = self.root / area
            self.assertFalse((p / "full").exists())
            self.assertEqual((p / "full.prev-1/old.txt").read_bytes(), b"old test fixture")
            self.assertEqual((p / "full.prev-2/new.txt").read_bytes(), b"new test fixture")


if __name__ == "__main__":
    unittest.main()
