# Internal setup: create an admin token

This guide is for AgentDeck staff and developers. In Claude Code, staff connect the plugin the same
way customers do — `/mcp` → `agentdeck` → **Authenticate**, signed in as an admin — and need no
token. A token is still needed for Codex, which connects with one, and for a headless live
evaluation, which cannot sign in through a browser. For customer onboarding, use
[Customer setup](../README.md#customer-setup).

## Requirements

Clone this repository, use Python 3.11 or newer, and sign in as an enabled admin in the target
environment's console. The backend token endpoint must be deployed and enabled. Admin token
management is currently through the API.

For dev, sign in at <https://dev-client-hub.agentdeck.eu>. Locate the current console access token
in browser DevTools:

```javascript
Object.entries(localStorage).find(([key]) => key.endsWith('.accessToken'))?.[1]
```

This is a short-lived console access token. If absent, obtain the signed-in session's access token;
do not substitute its ID token. Keep it out of chats and shell history.

## Issue the admin token

From the cloned repository:

```sh
python3 scripts/mint_token.py --api https://dev-api.agentdeck.eu --name codex
```

Paste the console access token into the hidden terminal prompt. The helper requests an ADMIN token
through `POST /api/admin/api-tokens` and saves it to `~/.config/agentdeck/tokens/dev.json` with mode
0600. It prints the filename, not the secret. The default expiry is 90 days; use `--days` to choose
1–365 days. A 404 means token support is disabled or the feature has not been deployed; a 401 means
the console access token is invalid or expired.

## Use it

- **Codex:** `python3 plugins/agentdeck/scripts/run_codex.py --environment dev --token-file ~/.config/agentdeck/tokens/dev.json`.
- **Headless live evaluation:** `python3 scripts/prepare_eval_plugin.py --environment dev --output <new dir>`
  copies the plugin with an MCP header that reads `EVAL_AGENTDECK_TOKEN`; see
  [the evaluation guide](../evals/README.md). The token is never written into the copy.

Use separate credentials for each environment. The helpers also support the production and local
API origins; consult `--help` before selecting a different environment. Production access requires
its release gate and backend features to be enabled.

## Revoke or replace a token

Use the admin API with your console session: `GET /api/admin/api-tokens` lists your active tokens,
and `DELETE /api/admin/api-tokens/{id}` revokes one. The mint helper refuses to overwrite an existing
credential file; choose a new `--output` filename when issuing a replacement. Revoke a token that
is no longer needed.

See [SECURITY.md](../SECURITY.md) for credential handling and vulnerability reports.

## ChatGPT plugin directory package

`chatgpt/` holds what OpenAI's plugin submission portal takes: `plugin.json` (listing, review test cases),
`mcp.json` (the production server, sign-in by dynamic client registration, no headers) and the icons. Build the
ZIP with `python3 scripts/build_chatgpt_package.py --demo-url <recording URL>` (or `--draft` for the portal's
automated checks) and upload `dist/agentdeck-chatgpt.zip`. `tests/test_chatgpt_package.py` holds the portal's
limits. The full submission walk-through is `docs/directory/SUBMISSION.md` in agent-backend.
