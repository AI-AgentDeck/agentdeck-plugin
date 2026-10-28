#!/usr/bin/env python3
"""Start a Codex session with an AgentDeck token supplied outside chat and process arguments."""

import argparse
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys


ENDPOINTS = {"dev": "https://dev-api.agentdeck.eu/mcp", "prod": "https://api.agentdeck.eu/mcp",
             "local": "http://localhost:8080/mcp"}
PLUGIN = Path(__file__).resolve().parents[1]


def launch(environment, token, arguments=()):
    if environment not in ENDPOINTS or not isinstance(token, str) or not token.startswith("adk_") or any(c.isspace() for c in token):
        raise ValueError("select a known environment and a valid adk_ token")
    version = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())["version"]
    config = 'mcp_servers.agentdeck={url=' + json.dumps(ENDPOINTS[environment]) + \
             ',bearer_token_env_var="AGENTDECK_TOKEN",http_headers={"X-Agentdeck-Plugin-Version"=' + \
             json.dumps(version) + '}}'
    environment_values = {**os.environ, "AGENTDECK_TOKEN": token, "AGENTDECK_MCP_URL": ENDPOINTS[environment]}
    return subprocess.call(["codex", "-c", config, *arguments], env=environment_values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=ENDPOINTS, default="dev")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--token-file", type=Path, help="private JSON object containing a token field")
    source.add_argument("--token-env", help="name of an environment variable containing the adk_ token")
    parser.add_argument("codex_args", nargs=argparse.REMAINDER, help="Codex arguments after --")
    args = parser.parse_args()
    try:
        if args.token_file:
            value = json.loads(args.token_file.expanduser().read_text())
            if not isinstance(value, dict):
                raise ValueError("token file must contain a JSON object")
            token = value.get("token", "")
        elif args.token_env:
            token = os.environ.get(args.token_env, "")
        elif sys.stdin.isatty():
            token = getpass.getpass("AgentDeck workspace token (hidden): ")
        else:
            raise ValueError("run from a terminal for the hidden prompt, or use --token-file or --token-env")
        arguments = args.codex_args[1:] if args.codex_args[:1] == ["--"] else args.codex_args
        print("Starting Codex with AgentDeck in " + args.environment + ". The token is not saved.")
        return launch(args.environment, token, arguments)
    except (OSError, ValueError):
        print("Could not start AgentDeck: check the environment, token source and Codex installation.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
