import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error


spec = importlib.util.spec_from_file_location("mint_token", Path(__file__).parents[1] / "scripts/mint_token.py")
mint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mint)


class TokenSetupTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "token.json"

    def test_token_is_saved_privately_and_not_returned_to_the_terminal(self):
        with patch.object(mint.urllib.request, "build_opener") as factory:
            factory.return_value.open.return_value.__enter__.return_value = io.StringIO(
                json.dumps({"id": "token-id", "token": "adk_synthetic", "scope": "ADMIN"}))
            result = mint.mint("https://dev-api.agentdeck.eu", "test", 1, "console-jwt", self.output)
            self.assertEqual(result, self.output)
            self.assertEqual(self.output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(self.output.read_text())["token"], "adk_synthetic")
            request = factory.return_value.open.call_args.args[0]
            self.assertEqual(request.get_header("Authorization"), "Bearer console-jwt")
            self.assertEqual(json.loads(request.data)["scope"], "ADMIN")

    def test_custom_origins_and_existing_credentials_are_rejected_before_network_access(self):
        with patch.object(mint.urllib.request, "build_opener") as factory:
            with self.assertRaises(ValueError):
                mint.mint("https://unrelated.example", "test", 1, "console-jwt", self.output)
            self.output.write_text("preserve me")
            with self.assertRaises(ValueError):
                mint.mint("https://dev-api.agentdeck.eu", "test", 1, "console-jwt", self.output)
            factory.assert_not_called()
            self.assertEqual(self.output.read_text(), "preserve me")

    def test_http_errors_do_not_echo_tokens_or_server_bodies(self):
        error = urllib.error.HTTPError("https://dev-api.agentdeck.eu", 404, "missing", {},
                                       io.BytesIO(b"console-jwt adk_synthetic"))
        with patch.object(mint.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = error
            with self.assertRaisesRegex(ValueError, "not deployed") as caught:
                mint.mint("https://dev-api.agentdeck.eu", "test", 1, "console-jwt", self.output)
            self.assertNotIn("console-jwt", str(caught.exception))
            self.assertNotIn("adk_synthetic", str(caught.exception))

    def test_failed_storage_identifies_the_created_token_for_revocation_without_its_secret(self):
        with patch.object(mint.urllib.request, "build_opener") as factory, \
                patch.object(mint.Path, "mkdir", side_effect=PermissionError("denied")):
            factory.return_value.open.return_value.__enter__.return_value = io.StringIO(
                json.dumps({"id": "token-id", "token": "adk_synthetic"}))
            with self.assertRaisesRegex(ValueError, "revoke its ID token-id") as caught:
                mint.mint("https://dev-api.agentdeck.eu", "test", 1, "console-jwt", self.output)
            self.assertNotIn("adk_synthetic", str(caught.exception))

    def test_authorization_is_never_forwarded_on_redirect(self):
        self.assertIsNone(mint.NoRedirect().redirect_request(None, None, 302, "redirect", {}, "https://other.example"))


if __name__ == "__main__":
    unittest.main()
