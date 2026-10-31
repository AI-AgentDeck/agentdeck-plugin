# Establish the caller and environment

Read [the runtime guide](runtime.md) for tool names, paths and the judge.

## Which server

Use the one AgentDeck MCP server this session has: in Claude Code the plugin's `agentdeck` server
(tools `mcp__plugin_agentdeck_agentdeck__*`) or one the user added with `claude mcp add`
(`mcp__agentdeck__*`); in Codex the `agentdeck` server. If two AgentDeck servers are connected, stop
and ask the user to keep one — two connections can point at different environments.

Never ask the user to paste a credential into the conversation, print stored options or credential
environment variables, or put a token in a bundle, report, URL or source ledger.

## Check `whoami`

Call `whoami` before anything else.

- `guideVersion` missing: the server predates the guide this plugin relies on. Tell the user the
  AgentDeck server needs updating and stop; do not work from remembered guidance.
- `environment` must match the endpoint: dev-api → dev, api.agentdeck.eu → prod, localhost → local.
  A mismatch or a missing value ends the run before any write. Say which endpoint differed and let
  the user correct the setting; do not switch endpoints or retry another environment yourself.
  Production creation or publishing needs an instruction that explicitly targets production; a
  configured production URL alone is not that instruction.
- Scope: ADMIN creates new businesses. TENANT creates and manages agents only in its own workspace,
  and only when `capabilities.createAgent` is true; otherwise creation stops with that reason.
- `plugin_outdated`, `plugin_version_missing` or `plugin_version_unreadable`: follow the returned
  update instructions and stop before writes. A missing header can also mean a proxy strips it.
- Record the caps. A 429 or `cap_reached` ends costly work; show the reset instead of looping.

Then follow the server's guide (`get_guide`), its `get_spec` and the tool schemas. The server is
the authority for keys, models, enabled tools and validation; describe a capability gap when a
required tool is absent.

## Not connected or not signed in

In Claude Code the plugin connects by signing in; there is no token to configure. When tools are
missing, a call answers 401, or `/mcp` shows the server as needing authentication, tell the user:

1. Run `/mcp`, choose `agentdeck`, then **Authenticate**.
2. In the browser, sign in to the AgentDeck console of that environment and choose **Allow**.
3. Return to Claude Code; the tools appear without a restart.

The environment is the plugin option `/plugin configure agentdeck@agentdeck` (dev by default).

In Codex, the connection uses a workspace token from AgentDeck Settings, supplied through the
repository's launcher (see the runtime guide). Never ask a customer for an admin login or a
console session token.

A 404 can mean the backend feature is disabled or not deployed. A 503 is an operational failure,
not a reason to sign in again.
