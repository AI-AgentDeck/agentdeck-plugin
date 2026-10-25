# AgentDeck plugin

This repository packages Claude Code skills and an MCP connection. The backend owns tool schemas,
authorization, configuration validation and execution. Read its live `get_spec` and tools/list;
never copy its production schema into the plugin or guess an unavailable operation.

The marketplace and plugin are both named `agentdeck`. The repository is `agentdeck-plugin`.
Keep the marketplace version, plugin version and MCP version header equal. `dev` is the team
branch; `main` is the release branch. A main pull request needs passing live acceptance on dev.

Use `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v` for offline checks.
`claude plugin validate --strict` is authoritative for Claude packaging. Model evaluations cost
real usage; scope runs and keep reports local. Fixtures test orchestration, not real agent quality.
Never mark a live gate passed from a mock run, a skipped case or an unjudged transcript.

Business facts and customer prompts are not public test fixtures. Use public source URLs for live
acceptance and synthetic facts for mock cases. Tokens, bundles, run state and transcripts stay out
of git. Public references describe patterns rather than copying private tenants' content.

Write self-explanatory code and few comments. Add tests for data integrity, credentials handling,
retry behavior and release gates. Keep this file byte-identical to CLAUDE.md when changing either.
