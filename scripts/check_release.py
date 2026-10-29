#!/usr/bin/env python3
"""Require a version increase before promoting an existing plugin to main."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    args = parser.parse_args()
    path = "plugins/agentdeck/.claude-plugin/plugin.json"
    old = subprocess.run(["git", "show", args.base + ":" + path], capture_output=True, text=True)
    if old.returncode:
        exists = subprocess.run(["git", "rev-parse", "--verify", args.base], capture_output=True).returncode == 0
        if not exists:
            print("Release base is unavailable; fetch it before checking.", file=sys.stderr)
            return 1
        print("First plugin release: no prior package on main.")
        return 0
    current = json.loads(Path(path).read_text())["version"]
    previous = json.loads(old.stdout)["version"]
    if tuple(map(int, current.split("."))) <= tuple(map(int, previous.split("."))):
        print("Release version must increase from " + previous, file=sys.stderr)
        return 1
    print("Release version: " + previous + " -> " + current)
    return 0


if __name__ == "__main__":
    sys.exit(main())
