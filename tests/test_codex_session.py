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
    def test_signs_in_by_default_with_no_token_anywhere(self):
        with patch.object(session.subprocess, "call", return_value=17) as call:
            self.assertEqual(session.launch("dev", None, ["--cd", "/tmp/work"]), 17)
        call.assert_called_once()
        args = call.call_args.args[0]
        env = call.call_args.kwargs["env"]
        self.assertNotIn("bearer_token_env_var", args[2])
        self.assertIn('"X-Agentdeck-Plugin-Version"=', args[2])
        self.assertEqual(env["AGENTDECK_MCP_URL"], session.ENDPOINTS["dev"])
        self.assertEqual(args[-2:], ["--cd", "/tmp/work"])

    def test_login_runs_codex_mcp_login_first_and_stops_when_it_fails(self):
        with patch.object(session.subprocess, "call", side_effect=[0, 5]) as call:
            self.assertEqual(session.launch("prod", None, login=True), 5)
        login, start = [c.args[0] for c in call.call_args_list]
        self.assertEqual(login[-3:], ["mcp", "login", "agentdeck"])
        self.assertIn(json.dumps(session.ENDPOINTS["prod"]), login[2])
        self.assertEqual(start[:3], login[:3])

        with patch.object(session.subprocess, "call", return_value=1) as call:
            self.assertEqual(session.launch("dev", None, login=True), 1)
        call.assert_called_once()

    def test_a_script_token_is_only_in_the_child_environment(self):
        before = dict(os.environ)
        with patch.object(session.subprocess, "call", return_value=0) as call:
            session.launch("dev", "adk_synthetic", login=True)
        call.assert_called_once()
        args = call.call_args.args[0]
        self.assertNotIn("adk_synthetic", " ".join(args))
        self.assertEqual(call.call_args.kwargs["env"]["AGENTDECK_TOKEN"], "adk_synthetic")
        self.assertIn('bearer_token_env_var="AGENTDECK_TOKEN"', args[2])
        self.assertEqual(dict(os.environ), before)

    def test_environment_selection_uses_only_known_origins(self):
        with patch.object(session.subprocess, "call", return_value=0) as call:
            for name, endpoint in session.ENDPOINTS.items():
                session.launch(name)
                self.assertIn(json.dumps(endpoint), call.call_args.args[0][2])
            call.reset_mock()
            for environment, token in [("https://other.example", None), ("dev", "console-jwt"),
                                       ("dev", "adk_secret\n"), ("dev", "")]:
                with self.assertRaises(ValueError):
                    session.launch(environment, token)
            call.assert_not_called()

    def test_argument_passthrough_without_a_token(self):
        with patch.object(session.sys, "argv", ["run_codex.py", "--environment", "local", "--login", "--",
                                                "--cd", "/tmp"]), \
                patch.object(session, "launch", return_value=0) as launch:
            self.assertEqual(session.main(), 0)
            launch.assert_called_once_with("local", None, ["--cd", "/tmp"], login=True)

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
