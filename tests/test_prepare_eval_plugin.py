import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("prepare_eval_plugin", Path(__file__).parents[1] / "scripts/prepare_eval_plugin.py")
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class PrepareEvalPluginTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "agentdeck"

    def test_the_copy_reads_its_token_from_an_eval_variable_and_never_holds_one(self):
        prepare.prepare("dev", self.destination)
        server = json.loads((self.destination / ".mcp.json").read_text())["mcpServers"]["agentdeck"]
        self.assertEqual(server["url"], "https://dev-api.agentdeck.eu/mcp")
        self.assertEqual(server["headers"]["Authorization"], "Bearer ${EVAL_AGENTDECK_TOKEN}")
        self.assertTrue(prepare.TOKEN_VARIABLE.startswith("EVAL_"))
        self.assertNotIn("adk_", (self.destination / ".mcp.json").read_text())
        self.assertTrue((self.destination / "evals-live").is_dir())

    def test_the_shipped_plugin_keeps_signing_in(self):
        prepare.prepare("dev", self.destination)
        shipped = json.loads((prepare.PLUGIN / ".mcp.json").read_text())["mcpServers"]["agentdeck"]
        self.assertNotIn("Authorization", shipped["headers"])
        copied = json.loads((self.destination / ".mcp.json").read_text())["mcpServers"]["agentdeck"]
        self.assertEqual(copied["headers"]["X-Agentdeck-Plugin-Version"],
                         shipped["headers"]["X-Agentdeck-Plugin-Version"])

    def test_unknown_environments_and_existing_destinations_are_refused(self):
        with self.assertRaises(ValueError):
            prepare.prepare("https://other.example", self.destination)
        self.assertFalse(self.destination.exists())
        self.destination.mkdir()
        with self.assertRaises(ValueError):
            prepare.prepare("dev", self.destination)


if __name__ == "__main__":
    unittest.main()
