#!/usr/bin/env python3
"""Check shared package consistency and invoke Claude Code’s authoritative validators."""

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
    codex_manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    codex_marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    codex_mcp = json.loads((PLUGIN / ".codex.mcp.json").read_text())["mcpServers"]["agentdeck"]
    versions = {codex_manifest["version"], codex_mcp["http_headers"]["X-Agentdeck-Plugin-Version"],
                marketplace["version"], marketplace["plugins"][0]["version"], manifest["version"],
                mcp["headers"]["X-Agentdeck-Plugin-Version"]}
    if len(versions) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("marketplace, plugin and MCP header must share a semantic version")
    if marketplace["name"] != "agentdeck" or manifest["name"] != "agentdeck":
        raise ValueError("installation namespace must remain agentdeck")
    if marketplace["plugins"][0]["source"] != "./plugins/agentdeck":
        raise ValueError("marketplace must install the package in this repository")
    if mcp["url"] != "${user_config.mcp_url}":
        raise ValueError("MCP must use the configured endpoint")
    if any(name.lower() == "authorization" for name in mcp["headers"]) or set(manifest["userConfig"]) != {"mcp_url"}:
        raise ValueError("Claude Code connects by signing in: a static Authorization header or token option disables it")
    if (ROOT / "AGENTS.md").read_bytes() != (ROOT / "CLAUDE.md").read_bytes():
        raise ValueError("AGENTS.md and CLAUDE.md differ")
    if codex_marketplace["name"] != "agentdeck" or codex_manifest["name"] != "agentdeck":
        raise ValueError("Codex namespace must remain agentdeck")
    if codex_marketplace["plugins"][0]["source"] != {"source": "local", "path": "./plugins/agentdeck"}:
        raise ValueError("Codex marketplace must use the shared package")
    if codex_manifest["skills"] != "./skills/" or codex_manifest["mcpServers"] != "./.codex.mcp.json":
        raise ValueError("Codex must load shared skills and its native MCP configuration")
    if codex_mcp["url"] != "https://dev-api.agentdeck.eu/mcp" or codex_mcp["bearer_token_env_var"] != "AGENTDECK_TOKEN":
        raise ValueError("Codex preview must use dev and an environment-supplied token")
    if "Authorization" in codex_mcp["http_headers"] or "headers" in codex_mcp:
        raise ValueError("Codex credentials must not be embedded or use Claude's header format")
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
    print("Shared package consistency and Claude validation passed; run scripts/check_codex.py for native Codex smoke checks.")


if __name__ == "__main__":
    try:
        check()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
