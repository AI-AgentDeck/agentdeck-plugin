import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("configure_plugin", Path(__file__).parents[1] / "scripts/configure_plugin.py")
configure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(configure)


class ConfigurePluginTest(unittest.TestCase):
    def test_secret_is_sent_on_stdin_and_not_in_process_arguments(self):
        with patch.object(configure.subprocess, "run") as run:
            run.return_value.returncode = 0
            configure.configure("dev", "adk_synthetic")
            self.assertNotIn("adk_synthetic", " ".join(run.call_args.args[0]))
            self.assertEqual(json.loads(run.call_args.kwargs["input"])["token"], "adk_synthetic")
            self.assertEqual(json.loads(run.call_args.kwargs["input"])["mcp_url"], "https://dev-api.agentdeck.eu/mcp")

    def test_untrusted_origins_and_non_adk_credentials_never_reach_claude(self):
        with patch.object(configure.subprocess, "run") as run:
            for environment, token in [("https://other.example", "adk_synthetic"), ("dev", "console-jwt")]:
                with self.assertRaises(ValueError):
                    configure.configure(environment, token)
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
