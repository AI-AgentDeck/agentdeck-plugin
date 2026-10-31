#!/usr/bin/env python3
"""Copy the plugin for a headless live evaluation that authenticates with a token instead of signing in."""

import argparse
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/agentdeck"
ENDPOINTS = {"dev": "https://dev-api.agentdeck.eu/mcp", "prod": "https://api.agentdeck.eu/mcp",
             "local": "http://localhost:8080/mcp"}
# `claude plugin eval` gives each run a fresh config directory, so no sign-in carries over, and it
# passes only EVAL_* variables from the operator's shell into the run. The copy's header names the
# variable; the token itself is never written to disk.
TOKEN_VARIABLE = "EVAL_AGENTDECK_TOKEN"


def prepare(environment, destination):
    if environment not in ENDPOINTS:
        raise ValueError("select a known environment")
    destination = Path(destination).expanduser()
    if destination.exists() or destination.is_symlink():
        raise ValueError("destination already exists; choose a new directory")
    shutil.copytree(PLUGIN, destination, ignore=shutil.ignore_patterns("results", "__pycache__"))
    path = destination / ".mcp.json"
    config = json.loads(path.read_text())
    server = config["mcpServers"]["agentdeck"]
    server["url"] = ENDPOINTS[environment]
    server["headers"]["Authorization"] = "Bearer ${" + TOKEN_VARIABLE + "}"
    path.write_text(json.dumps(config, indent=2) + "\n")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=ENDPOINTS, default="dev")
    parser.add_argument("--output", required=True, help="new directory for the evaluation copy")
    args = parser.parse_args()
    try:
        copy = prepare(args.environment, args.output)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Evaluation copy for " + args.environment + " at " + str(copy) + "; export " + TOKEN_VARIABLE
          + " before running claude plugin eval on it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
