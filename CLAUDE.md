# AgentDeck plugin

This repository packages shared skills for Claude Code and Codex, with runtime-specific MCP connections. The backend owns tool schemas,
authorization, configuration validation and execution. Read its live `get_spec` and tools/list;
never copy its production schema into the plugin or guess an unavailable operation. The backend
also serves the shared workflow guidance (`get_guide`); skills keep only what is specific to a
runtime — the connection, local files, `bundle.py` and the independent judge. Claude Code connects
by signing in, so the shipped `.mcp.json` carries no Authorization header.

The marketplace and plugin are both named `agentdeck`. The repository is `agentdeck-plugin`.
Keep all runtime manifest versions and MCP version headers equal. `dev` is the team
branch; `main` is the release branch. A main pull request needs a passing `validate`; live
acceptance on dev is a manual run.

Use `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v` for offline checks.
`claude plugin validate --strict` is authoritative for Claude packaging.
Run `python3 scripts/check_codex.py` to install into an isolated Codex home and verify skill
discovery and authenticated MCP handshake against a local synthetic server, without model calls. Model evaluations cost
real usage; scope runs and keep reports local. Fixtures test orchestration, not real agent quality.
Never mark a live gate passed from a mock run, a skipped case or an unjudged transcript.

Business facts and customer prompts are not public test fixtures. Use public source URLs for live
acceptance and synthetic facts for mock cases. Tokens, bundles, run state and transcripts stay out
of git. Public references describe patterns rather than copying private tenants' content.

Write self-explanatory code and few comments. Add tests for data integrity, credentials handling,
retry behavior and release gates. Keep this file byte-identical to CLAUDE.md when changing either.
