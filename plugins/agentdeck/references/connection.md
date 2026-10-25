# Establish the caller and environment

The installed MCP server is `agentdeck`. Claude Code exposes its tools with the prefix
`mcp__plugin_agentdeck_agentdeck__`. The connection supplies the token and plugin-version header;
never ask the user to paste credentials into a conversation, use Bash to print stored options,
or put a token in a bundle, report, URL or source ledger.

Call `whoami` before other operations. Match its `environment` with the endpoint shown in the
invoked skill: dev-api → dev, api.agentdeck.eu → prod, localhost → local. An unexpected or missing
environment ends the run before writes. Explain which endpoint/profile differed and let the
operator correct installation settings. Do not automatically switch endpoints or retry another
environment with the same credential. Production creation or publishing needs an instruction
that explicitly targets production; a configured production URL alone is not that instruction.

Record the returned scope, supported models/languages, plugin compatibility and remaining caps.
New-agent creation currently requires ADMIN; a tenant token can only act on its own existing
agents. Read operations succeeding does not grant creation rights. On `plugin_outdated`,
`plugin_version_missing` or `plugin_version_unreadable`, follow the returned update instructions
and stop before writes. A missing or unreadable header can also mean a proxy is stripping it.

For 401 or no connection, explain how to issue an environment-specific `adk_` token using the
repository's token helper, then configure `agentdeck@agentdeck` in Claude Code. A 404 can mean
the backend feature is disabled or this branch has not been deployed. A 503 is an operational
failure, not proof that the token should be replaced. A 429 or `cap_reached` ends costly work;
show the reset/remaining allowance instead of creating another token or looping.

After identity checks, read `get_spec` and the actual MCP tool input schemas. The backend is the
authority for keys, defaults, models, enabled tools and validation. Do not maintain a copied
schema or silently substitute a requested model. Describe a capability gap when a required
tool is absent. Reuse the current session's authorization for its stated goal and environment;
ask only for missing business facts or unresolved action scope.
