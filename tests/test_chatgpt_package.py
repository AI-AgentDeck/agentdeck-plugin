import json
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_chatgpt_package  # noqa: E402

PLUGIN = json.loads((ROOT / "chatgpt" / "plugin.json").read_text(encoding="utf-8"))
MCP = json.loads((ROOT / "chatgpt" / "mcp.json").read_text(encoding="utf-8"))
OPENAI = PLUGIN["extensions"]["com.openai"]
INTERFACE = OPENAI["interface"]


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    return struct.unpack(">II", header[16:24])


class ChatGptPackageTest(unittest.TestCase):
    """The limits OpenAI's portal enforces, checked before upload."""

    def test_listing_fields_fit_the_portal(self):
        self.assertLessEqual(len(INTERFACE["displayName"]), 30)
        self.assertLessEqual(len(INTERFACE["shortDescription"]), 30)
        self.assertLessEqual(len(INTERFACE["longDescription"]), 4000)
        self.assertLessEqual(len(INTERFACE["developerName"]), 80)
        self.assertRegex(PLUGIN["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        prompts = INTERFACE["defaultPrompt"]
        self.assertLessEqual(len(prompts), 3)
        self.assertEqual(len(prompts), len(set(prompts)))
        self.assertTrue(all(len(prompt) <= 128 for prompt in prompts))
        self.assertTrue(all(len(item) <= 120 for item in INTERFACE["capabilities"]))

    def test_every_listing_link_is_https(self):
        for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
            self.assertTrue(INTERFACE[key].startswith("https://"), key)

    def test_the_server_signs_in_and_carries_no_headers(self):
        server = MCP["mcpServers"]["agentdeck"]
        self.assertEqual(server["url"], "https://api.agentdeck.eu/mcp")
        self.assertNotIn("headers", server)
        self.assertEqual(server["extensions"]["com.openai"]["auth"]["client"]["mode"], "dcr")

    def test_review_has_five_positive_and_three_negative_cases(self):
        cases = OPENAI["review"]["test_cases"]
        self.assertEqual(len(cases["positive"]), 5)
        self.assertEqual(len(cases["negative"]), 3)
        for case in cases["positive"]:
            self.assertTrue(all(case[key] for key in ("description", "prompt", "tools_triggered", "expected_behavior")))

    def test_icons_are_square_and_bundled(self):
        for key in ("logo", "composerIcon"):
            path = ROOT / "chatgpt" / INTERFACE[key].removeprefix("./")
            width, height = png_size(path)
            self.assertEqual(width, height, key)
            self.assertGreaterEqual(width, 48, key)

    def test_the_zip_carries_the_demo_url_and_every_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = build_chatgpt_package.build(Path(tmp) / "p.zip", "https://example.com/demo", draft=False)
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
                plugin = json.loads(archive.read("plugin.json"))
        self.assertTrue({"plugin.json", "mcp.json", "assets/logo.png", "assets/composer-icon.png"} <= names)
        self.assertEqual(plugin["extensions"]["com.openai"]["review"]["demo_recording_url"], "https://example.com/demo")

    def test_no_secret_or_token_is_packaged(self):
        text = (ROOT / "chatgpt" / "mcp.json").read_text() + (ROOT / "chatgpt" / "plugin.json").read_text()
        for marker in ("adk_", "clientSecret", "Authorization", "Bearer"):
            self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
