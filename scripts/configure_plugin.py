#!/usr/bin/env python3
"""Configure the installed Claude plugin without putting an API token in command arguments."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


ENDPOINTS = {"dev": "https://dev-api.agentdeck.eu/mcp", "prod": "https://api.agentdeck.eu/mcp",
             "local": "http://localhost:8080/mcp"}


def configure(environment, token):
    if environment not in ENDPOINTS or not isinstance(token, str) or not token.startswith("adk_") or any(c.isspace() for c in token):
        raise ValueError("select a known environment and a valid adk_ token")
    values = json.dumps({"mcp_url": ENDPOINTS[environment], "token": token})
    result = subprocess.run(["claude", "plugin", "configure", "agentdeck@agentdeck", "--values-stdin"],
                            input=values, text=True, capture_output=True)
    if result.returncode:
        raise ValueError("Claude could not configure agentdeck@agentdeck; install it first and use Claude Code 2.1.310 or newer")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=ENDPOINTS, default="dev")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--token-file", type=Path, help="private JSON file written by mint_token.py")
    source.add_argument("--token-env", help="name of an environment variable containing the adk_ token")
    args = parser.parse_args()
    try:
        if args.token_file:
            stored = json.loads(args.token_file.expanduser().read_text())
            if not isinstance(stored, dict):
                raise ValueError("token file must be the JSON object saved by mint_token.py")
            token = stored.get("token", "")
        else:
            token = os.environ.get(args.token_env, "")
        configure(args.environment, token)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Configured AgentDeck for " + args.environment + "; restart Claude Code before using it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
