# Runtime integration

The four skills share their business workflow. Use the instructions for the host running this
session. Never execute another runtime's setup commands or treat an unexpanded placeholder as input.

## Claude Code

Install `agentdeck@agentdeck` from the AgentDeck marketplace. Configure its environment and sensitive
token option with `/plugin configure agentdeck@agentdeck`, then restart. The configured URL is
`${user_config.mcp_url}`. Tools use `mcp__plugin_agentdeck_agentdeck__*`.

Resolve helpers from `${CLAUDE_PLUGIN_ROOT}/scripts/`. Use Read/Write/Edit for local evidence,
bundles and reports. Invoke the packaged `agentdeck:chat-judge` agent for independent evaluation.
Claude appends the invocation arguments to skills automatically.

## Codex CLI

Install the Codex marketplace and plugin using the repository README. The packaged MCP connection
uses the dev endpoint, reads the bearer token from `AGENTDECK_TOKEN`, and supplies the plugin-version
header. The session launcher selects dev, prod or local explicitly and sets a session-only MCP
configuration. Its `AGENTDECK_MCP_URL` is nonsecret; it identifies the expected environment. If that
variable is absent, the packaged connection expects dev. Do not read or print `AGENTDECK_TOKEN`.

Start the launcher from a terminal, never as a model tool call requiring an interactive secret.
For missing authentication, ask the operator to run the launcher with their workspace token using
its hidden prompt, token-file or token-env option. Do not run Claude's configuration command.

Codex exposes the skills as `$agentdeck:create-agent`, `$agentdeck:update-agent`,
`$agentdeck:test-agent` and `$agentdeck:go-live`. Their input is the user's surrounding request.
Discover the actual tools for the `agentdeck` server; do not assume Claude's tool prefix.

Resolve helper paths from the installed SKILL.md location: the plugin root is two directories above
its containing skill directory. For example, `<plugin-root>/skills/create-agent/SKILL.md` uses
`<plugin-root>/scripts/bundle.py`. Use absolute paths for helpers, while keeping generated artifacts
in the user's working directory. Use the available file-editing tools rather than Claude tool names.

For independent judging, start a fresh read-only agent when the host supports it. Supply only the
[judge contract](chat-judge.md), business goal, approved evidence, expectations and transcripts.
Do not give it the authoring conversation or desired verdict. Do not give it write tools or invoke
business mutations. The Claude agent definition is not a registered Codex agent. If a fresh judge
cannot be started, leave cases INCOMPLETE and provide the saved artifacts for a separate review;
a second pass by the same author is not independent acceptance.
