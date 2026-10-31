#!/usr/bin/env python3
"""Start a Codex session connected to a chosen AgentDeck environment.

By default Codex signs in through the browser (`codex mcp login agentdeck`, run once per environment with
--login). Scripts and automated runs that cannot open a browser pass a personal token instead, from a private
file or an environment variable, never as an argument.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


ENDPOINTS = {"dev": "https://dev-api.agentdeck.eu/mcp", "prod": "https://api.agentdeck.eu/mcp",
             "local": "http://localhost:8080/mcp"}
PLUGIN = Path(__file__).resolve().parents[1]


def server_config(environment, with_token):
    version = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())["version"]
    token = ',bearer_token_env_var="AGENTDECK_TOKEN"' if with_token else ""
    return 'mcp_servers.agentdeck={url=' + json.dumps(ENDPOINTS[environment]) + token + \
        ',http_headers={"X-Agentdeck-Plugin-Version"=' + json.dumps(version) + '}}'


def launch(environment, token=None, arguments=(), login=False):
    if environment not in ENDPOINTS:
        raise ValueError("select a known environment")
    if token is not None and (not isinstance(token, str) or not token.startswith("adk_")
                              or any(c.isspace() for c in token)):
        raise ValueError("a token must be a valid adk_ token")
    config = server_config(environment, token is not None)
    environment_values = {**os.environ, "AGENTDECK_MCP_URL": ENDPOINTS[environment]}
    if token is not None:
        environment_values["AGENTDECK_TOKEN"] = token
    elif login:
        signed_in = subprocess.call(["codex", "-c", config, "mcp", "login", "agentdeck"], env=environment_values)
        if signed_in:
            return signed_in
    return subprocess.call(["codex", "-c", config, *arguments], env=environment_values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=ENDPOINTS, default="dev")
    parser.add_argument("--login", action="store_true", help="sign in through the browser before starting")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--token-file", type=Path, help="scripts: private JSON object containing a token field")
    source.add_argument("--token-env", help="scripts: name of an environment variable containing the adk_ token")
    parser.add_argument("codex_args", nargs=argparse.REMAINDER, help="Codex arguments after --")
    args = parser.parse_args()
    try:
        token = None
        if args.token_file:
            value = json.loads(args.token_file.expanduser().read_text())
            if not isinstance(value, dict):
                raise ValueError("token file must contain a JSON object")
            token = value.get("token", "")
        elif args.token_env:
            token = os.environ.get(args.token_env, "")
        arguments = args.codex_args[1:] if args.codex_args[:1] == ["--"] else args.codex_args
        if token is None:
            print("Starting Codex with AgentDeck in " + args.environment + ". If it is not signed in yet, run this"
                  " again with --login.")
        else:
            print("Starting Codex with AgentDeck in " + args.environment + ". The token is not saved.")
        return launch(args.environment, token, arguments, login=args.login)
    except (OSError, ValueError):
        print("Could not start AgentDeck: check the environment, token source and Codex installation.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
