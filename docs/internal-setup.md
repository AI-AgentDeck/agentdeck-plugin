# Internal setup: create an admin token

This guide is for AgentDeck staff and developers who need admin access to create agents for
businesses, debug the platform or run team acceptance tests. For customer onboarding, use
[Customer setup](../README.md#customer-setup): Settings → Connect Claude Code issues a token
restricted to the signed-in customer's business workspace.

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

## Issue and configure the admin token

From the cloned repository:

```sh
python3 scripts/mint_token.py --api https://dev-api.agentdeck.eu --name claude-code
```

Paste the console access token into the hidden terminal prompt. The helper requests an ADMIN token
through `POST /api/admin/api-tokens` and saves it to `~/.config/agentdeck/tokens/dev.json` with mode
0600. It prints the filename, not the secret. The default expiry is 90 days; use `--days` to choose
1–365 days. A 404 means token support is disabled or the feature has not been deployed; a 401 means
the console access token is invalid or expired.

After installing the plugin, configure it without putting the token in command arguments:

```sh
python3 scripts/configure_plugin.py --environment dev --token-file ~/.config/agentdeck/tokens/dev.json
```

Restart Claude Code. Use separate credentials for each environment. The helpers also support the
production and local API origins; consult `--help` before selecting a different environment.
Production access requires its release gate and backend features to be enabled.

## Revoke or replace a token

Use the admin API with your console session: `GET /api/admin/api-tokens` lists your active tokens,
and `DELETE /api/admin/api-tokens/{id}` revokes one. The mint helper refuses to overwrite an existing
credential file; choose a new `--output` filename when issuing a replacement. Revoke a token that
is no longer needed.

See [SECURITY.md](../SECURITY.md) for credential handling and vulnerability reports.
