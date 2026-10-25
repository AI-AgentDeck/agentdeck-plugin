import contextlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("bundle", Path(__file__).parents[1] / "plugins/agentdeck/scripts/bundle.py")
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class BundlePersistenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cwd = contextlib.chdir(self.root)
        self.cwd.__enter__()
        self.addCleanup(self.cwd.__exit__, None, None, None)
        self.source = self.root / "candidate.json"
        self.document = {"schema": "agentdeck/agent-bundle@1", "display-name": "Synthetic club",
                         "agent": {"prompts": {"system-prompt": "Answer from approved knowledge."}}}
        self.source.write_text(json.dumps(self.document))

    def test_retries_preserve_the_creation_key_across_process_state(self):
        first = bundle.persist("prepare", self.source, "synthetic-club", "dev")
        second = bundle.persist("prepare", self.source, "synthetic-club", "dev")
        self.assertEqual(first["idempotencyKey"], second["idempotencyKey"])
        state = json.loads(Path(first["statePath"]).read_text())
        self.assertEqual(state["createBundleHash"], first["sha256"])
        self.assertEqual(json.loads(Path(first["bundlePath"]).read_text()), self.document)
        self.assertEqual(Path(first["statePath"]).stat().st_mode & 0o777, 0o600)

    def test_retrying_another_environment_is_refused(self):
        bundle.persist("prepare", self.source, "club", "dev")
        with self.assertRaisesRegex(ValueError, "another bundle or environment"):
            bundle.persist("prepare", self.source, "club", "prod")

    def test_a_changed_candidate_cannot_reuse_an_uncertain_create(self):
        first = bundle.persist("prepare", self.source, "club", "dev")
        self.document["display-name"] = "Changed"
        self.source.write_text(json.dumps(self.document))
        with self.assertRaises(ValueError):
            bundle.persist("prepare", self.source, "club", "dev")
        self.assertEqual(json.loads(Path(first["bundlePath"]).read_text())["display-name"], "Synthetic club")

    def test_response_envelopes_and_environment_credentials_are_refused(self):
        self.source.write_text(json.dumps({"bundle": self.document, "agentId": "server-id"}))
        with self.assertRaises(ValueError):
            bundle.persist("save", self.source, "club")
        self.document["agent"]["api-key"] = "synthetic-secret"
        self.source.write_text(json.dumps(self.document))
        with self.assertRaisesRegex(ValueError, "environment-owned field"):
            bundle.persist("save", self.source, "club")
        self.assertFalse(Path("agentdeck/club.json").exists())

    def test_replacing_an_artifact_is_explicit(self):
        bundle.persist("save", self.source, "club")
        self.document["display-name"] = "Changed"
        self.source.write_text(json.dumps(self.document))
        with self.assertRaises(ValueError):
            bundle.persist("save", self.source, "club")
        result = bundle.persist("save", self.source, "club", replace=True)
        self.assertEqual(json.loads(Path(result["bundlePath"]).read_text())["display-name"], "Changed")

    def test_path_traversal_and_symlinks_are_refused(self):
        with self.assertRaises(ValueError):
            bundle.persist("save", self.source, "../outside")
        Path("agentdeck").symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            bundle.persist("save", self.source, "club")

    def test_duplicate_keys_and_oversized_payloads_are_refused(self):
        self.source.write_text('{"schema":"a","schema":"b"}')
        with self.assertRaisesRegex(ValueError, "duplicate"):
            bundle.read_bundle(self.source)
        self.source.write_bytes(b"x" * (bundle.MAX_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "512 KiB"):
            bundle.read_bundle(self.source)


if __name__ == "__main__":
    unittest.main()
