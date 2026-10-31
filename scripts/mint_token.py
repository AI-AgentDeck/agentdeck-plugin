#!/usr/bin/env python3
"""Create an environment-scoped AgentDeck token using an admin's console access token."""

import argparse
import getpass
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


APIS = {"https://dev-api.agentdeck.eu": "dev", "https://api.agentdeck.eu": "prod",
        "http://localhost:8080": "local"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        return None


def mint(api, name, days, access_token, output):
    if api not in APIS:
        raise ValueError("choose a documented AgentDeck API origin; redirects and custom origins are not accepted")
    if not name.strip() or not 1 <= days <= 365:
        raise ValueError("provide a token name and an expiry from 1 to 365 days")
    output = Path(output).expanduser()
    if output.exists() or output.is_symlink():
        raise ValueError("output already exists; choose a new filename to preserve the current credential")
    access_token = access_token.strip().strip("\"'")
    if not access_token or any(c in access_token for c in "\r\n"):
        raise ValueError("a console access token is required")
    body = json.dumps({"name": name, "scope": "ADMIN", "expiresInDays": days}).encode()
    request = urllib.request.Request(api + "/api/admin/api-tokens", data=body, method="POST",
                                     headers={"Authorization": "Bearer " + access_token,
                                              "Content-Type": "application/json"})
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        hints = {401: "console access token is invalid or expired", 403: "sign in as an enabled admin",
                 404: "API tokens are disabled or the backend feature is not deployed",
                 429: "request limit reached; wait before trying again", 503: "authentication service is unavailable"}
        raise ValueError("token creation failed (HTTP " + str(error.code) + "): "
                         + hints.get(error.code, "the server refused the request")) from None
    if not isinstance(result, dict) or not isinstance(result.get("token"), str) or not result["token"].startswith("adk_"):
        raise ValueError("server returned no usable AgentDeck token")
    try:
        output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except OSError:
        raise ValueError("token was created but could not be saved; revoke its ID "
                         + str(result.get("id", "in the admin token list")) + " before retrying") from None
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", choices=APIS, default="https://dev-api.agentdeck.eu")
    parser.add_argument("--name", default="claude-code")
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--output", help="private JSON file; default ~/.config/agentdeck/tokens/<environment>.json")
    args = parser.parse_args()
    output = args.output or str(Path.home() / ".config/agentdeck/tokens" / (APIS[args.api] + ".json"))
    try:
        saved = mint(args.api, args.name, args.days, getpass.getpass("Console access token (hidden): "), output)
    except (ValueError, OSError, urllib.error.URLError, EOFError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Token saved privately to " + str(saved) + ". Use it with run_codex.py --token-file or as EVAL_AGENTDECK_TOKEN for a headless evaluation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
