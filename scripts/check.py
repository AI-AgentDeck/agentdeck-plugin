#!/usr/bin/env python3
"""Check package consistency and invoke Claude Code's authoritative validators."""

import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/agentdeck"


def check():
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    mcp = json.loads((PLUGIN / ".mcp.json").read_text())["mcpServers"]["agentdeck"]
    versions = {marketplace["version"], marketplace["plugins"][0]["version"], manifest["version"],
                mcp["headers"]["X-Agentdeck-Plugin-Version"]}
    if len(versions) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("marketplace, plugin and MCP header must share a semantic version")
    if marketplace["name"] != "agentdeck" or manifest["name"] != "agentdeck":
        raise ValueError("installation namespace must remain agentdeck")
    if marketplace["plugins"][0]["source"] != "./plugins/agentdeck":
        raise ValueError("marketplace must install the package in this repository")
    if mcp["url"] != "${user_config.mcp_url}" or mcp["headers"]["Authorization"] != "Bearer ${user_config.token}":
        raise ValueError("MCP must use configured endpoint and token")
    if manifest["userConfig"]["token"].get("sensitive") is not True:
        raise ValueError("token option must use secure storage")
    if "default" in manifest["userConfig"]["token"]:
        raise ValueError("token option cannot have a default credential")
    if (ROOT / "AGENTS.md").read_bytes() != (ROOT / "CLAUDE.md").read_bytes():
        raise ValueError("AGENTS.md and CLAUDE.md differ")
    for name in ["create-agent", "update-agent", "test-agent", "go-live"]:
        if not (PLUGIN / "skills" / name / "SKILL.md").is_file():
            raise ValueError("required skill missing: " + name)
    for path in PLUGIN.rglob("*.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            if re.match(r"https?://|#", target):
                continue
            reference = (path.parent / target.split("#")[0]).resolve()
            if not reference.is_relative_to(PLUGIN) or not reference.exists():
                raise ValueError("missing or out-of-package reference in " + str(path.relative_to(ROOT)) + ": " + target)
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            compile(path.read_text(), str(path), "exec")
    for target in [ROOT, PLUGIN]:
        subprocess.run(["claude", "plugin", "validate", "--strict", str(target)], check=True)
    print("Package consistency and Claude validation passed.")


if __name__ == "__main__":
    try:
        check()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
