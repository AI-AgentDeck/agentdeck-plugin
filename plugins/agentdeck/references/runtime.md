# Runtime integration

The four skills share their business workflow, which the AgentDeck server serves through
`get_guide`. Use the instructions below for the host running this session. Never execute another
runtime's setup commands or treat an unexpanded placeholder as input.

## Claude Code

Install `agentdeck@agentdeck` from the AgentDeck marketplace. The plugin's server connects by
signing in (`/mcp` → `agentdeck` → Authenticate); its environment is the plugin option
`${user_config.mcp_url}`, set with `/plugin configure agentdeck@agentdeck`. Tools use
`mcp__plugin_agentdeck_agentdeck__*`, or `mcp__agentdeck__*` when the user added the server with
`claude mcp add` instead of the plugin's own.

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

## The independent judge

The server's evaluation topic defines the checklist every test case is held to. The plugin adds an
independent judge on top of it: a fresh read-only agent that sees only the
[judge contract](chat-judge.md), business goal, approved evidence, expectations and complete
transcripts. Do not give it the authoring conversation or the desired verdict, write tools or
business mutations. In Claude Code it is `agentdeck:chat-judge`; the Claude agent definition is not
a registered Codex agent, so in Codex start a fresh read-only agent when the host supports it. If a
fresh judge cannot be started, leave cases INCOMPLETE and provide the saved artifacts for a
separate review; a second pass by the same author is not independent acceptance.
