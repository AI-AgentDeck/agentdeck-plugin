import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "codex_session", Path(__file__).parents[1] / "plugins/agentdeck/scripts/run_codex.py")
session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(session)


class CodexSessionTest(unittest.TestCase):
    def test_token_is_only_in_child_environment_and_config_is_session_scoped(self):
        before = dict(os.environ)
        with patch.object(session.subprocess, "call", return_value=17) as call:
            self.assertEqual(session.launch("dev", "adk_synthetic", ["--cd", "/tmp/work"]), 17)
        args = call.call_args.args[0]
        env = call.call_args.kwargs["env"]
        self.assertNotIn("adk_synthetic", " ".join(args))
        self.assertEqual(env["AGENTDECK_TOKEN"], "adk_synthetic")
        self.assertEqual(env["AGENTDECK_MCP_URL"], session.ENDPOINTS["dev"])
        self.assertEqual(args[-2:], ["--cd", "/tmp/work"])
        self.assertIn('bearer_token_env_var="AGENTDECK_TOKEN"', args[2])
        self.assertIn('"X-Agentdeck-Plugin-Version"=', args[2])
        self.assertEqual(dict(os.environ), before)

    def test_environment_selection_uses_only_known_origins(self):
        with patch.object(session.subprocess, "call", return_value=0) as call:
            for name, endpoint in session.ENDPOINTS.items():
                session.launch(name, "adk_synthetic")
                self.assertIn(json.dumps(endpoint), call.call_args.args[0][2])
            call.reset_mock()
            for environment, token in [("https://other.example", "adk_synthetic"), ("dev", "console-jwt"),
                                       ("dev", "adk_secret\n"), ("dev", None)]:
                with self.assertRaises(ValueError):
                    session.launch(environment, token)
            call.assert_not_called()

    def test_no_terminal_requires_explicit_token_source(self):
        with patch.object(session.sys, "argv", ["run_codex.py"]), \
                patch.object(session.sys.stdin, "isatty", return_value=False), \
                patch.object(session.getpass, "getpass") as prompt, \
                patch.object(session, "launch") as launch:
            self.assertEqual(session.main(), 1)
            prompt.assert_not_called()
            launch.assert_not_called()

    def test_hidden_prompt_and_argument_passthrough(self):
        with patch.object(session.sys, "argv", ["run_codex.py", "--environment", "local", "--", "--cd", "/tmp"]), \
                patch.object(session.sys.stdin, "isatty", return_value=True), \
                patch.object(session.getpass, "getpass", return_value="adk_synthetic"), \
                patch.object(session, "launch", return_value=0) as launch:
            self.assertEqual(session.main(), 0)
            launch.assert_called_once_with("local", "adk_synthetic", ["--cd", "/tmp"])

    def test_invalid_token_file_does_not_echo_its_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private.json"
            path.write_text('{"token": "adk_secret_that_must_not_be_logged"')
            with patch.object(session.sys, "argv", ["run_codex.py", "--token-file", str(path)]), \
                    patch("sys.stderr") as stderr, patch.object(session, "launch") as launch:
                self.assertEqual(session.main(), 1)
                self.assertNotIn("adk_secret", str(stderr.write.call_args_list))
                launch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
