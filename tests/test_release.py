from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_release.py"
MANIFEST = Path("plugins/agentdeck/.claude-plugin/plugin.json")


class ReleaseGateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.name", "Synthetic Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.root / "README.md").write_text("Synthetic release fixture\n")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "bootstrap")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def version(self, value):
        path = self.root / MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"version": value}))

    def check(self, base="main"):
        return subprocess.run([sys.executable, str(SCRIPT), "--base", base], cwd=self.root,
                              capture_output=True, text=True)

    def test_first_release_is_allowed_against_a_real_bootstrap_branch(self):
        self.version("0.1.0")
        self.assertEqual(self.check().returncode, 0)

    def test_an_unavailable_base_does_not_masquerade_as_a_first_release(self):
        self.version("0.1.0")
        self.assertNotEqual(self.check("missing-branch").returncode, 0)

    def test_repeated_or_older_versions_block_promotion(self):
        self.version("0.2.0")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "release")
        for value in ["0.2.0", "0.1.9"]:
            with self.subTest(version=value):
                self.version(value)
                self.assertNotEqual(self.check().returncode, 0)

    def test_a_numeric_version_increase_allows_promotion(self):
        self.version("0.9.0")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "release")
        self.version("0.10.0")
        self.assertEqual(self.check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
