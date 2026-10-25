# AgentDeck for Claude Code

Turn a business website, approved documents or a brief into an AgentDeck agent with configured
prompts, indexed knowledge and a tested preview. Setup reasoning runs in your Claude Code session;
AgentDeck's authenticated MCP tools handle crawling, validation and execution.

This is the **team preview on `dev`**. Production acceptance is not complete. The first release
will be promoted to `main` after live evaluation. This package currently targets Claude Code.

## Install

Use Claude Code **2.1.310 or newer**, Python **3.11 or newer** for the local helpers, and an AgentDeck
admin token from the environment you intend to use. New-agent creation is admin-only today.

In Claude Code:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
```

Select an MCP endpoint (dev by default) and enter the token in its masked option. Restart Claude
Code after installation or configuration changes. Never paste tokens into normal chats or git.

After the first release on main, a stable installation will also be available with:

```text
/plugin install agentdeck --marketplace AI-AgentDeck/agentdeck-plugin
```

## Create an adk token

The token endpoint must be deployed and enabled first. The console has no token-management page
yet. Clone this repository, sign in as an admin at the matching console (dev:
<https://dev-client-hub.agentdeck.eu>), then locate the current access token in browser DevTools:

```javascript
Object.entries(localStorage).find(([key]) => key.endsWith('.accessToken'))?.[1]
```

This is a short-lived console access token. If absent, obtain the signed-in session's access
token; do not substitute its ID token. In a terminal, from this repository:

```sh
python3 scripts/mint_token.py --api https://dev-api.agentdeck.eu --name claude-code
```

Paste the console token into the hidden terminal prompt. The helper calls
`POST /api/admin/api-tokens` and saves the new token to `~/.config/agentdeck/tokens/dev.json` with
mode 0600. It prints the filename, not the secret. A 404 means token support is disabled or the
backend feature has not been deployed; a 401 means the access token is invalid or expired.

After installation, configure the plugin without putting the token in shell history:

```sh
python3 scripts/configure_plugin.py --environment dev --token-file ~/.config/agentdeck/tokens/dev.json
```

Tokens expire and can be revoked through the admin API. Use separate credentials per environment.
See [SECURITY.md](SECURITY.md) for handling and vulnerability reports.

## Use

```text
/agentdeck:create-agent https://agentdeck.eu/
/agentdeck:create-agent ./approved-business-faq.txt
/agentdeck:update-agent <agent-uuid> Correct cancellation terms using ./approved-policy.txt
/agentdeck:test-agent <agent-uuid> Check German and English prices, unknown facts and handoff
/agentdeck:go-live <agent-uuid> https://customer.example
```

Creation follows eight stages: identify caller, discover sources, ask missing questions, write the
bundle, validate, create and index, test and refine, then hand over. Business facts stay in knowledge;
prompts define behavior. A read-only judge reviews sources and conversations independently. At most
two correction rounds run; unresolved questions remain explicit instead of becoming guesses.

The portable configuration is saved to `./agentdeck/<slug>.json`. Private source ledgers, creation
keys and reports stay in `.agentdeck-work/<slug>/`. Keep these out of your own project's git history
too. A saved creation key makes uncertain retries idempotent. Schema and tool descriptions are read
from the backend at runtime. Updates replace a complete bundle, removing omitted sections.

## Current boundaries

- PREPARING becomes TEST when initial knowledge/key setup is ready. TEST is not a quality verdict.
- Today's MCP tools cannot add domains or set TEST → LIVE. `go-live` produces a blocked admin handover.
- Discovery returns short excerpts. Material facts need full approved sources. Creation re-fetches
  configured URLs; it does not accept a discovery crawl ID.
- Files upload after creation. Their individual indexing state is not reliably exposed by
  `get_agent_status`; verify it in Knowledge or with source-specific fresh-thread checks.
- Export omits some file-only settings, uploaded binaries, credentials and channel connections.
  Preserve warnings and original upload files when promoting to another environment.
- Bundle versions do not capture concurrent console edits. Read-back comparison narrows the race
  but cannot provide atomic protection against one.
- `inFlight` test turns keep running and stay charged; do not resend them. Only `unanswered` messages
  were never started and are refunded. The current tools cannot retrieve a late result.

## Develop and validate

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests -v
claude --plugin-dir ./plugins/agentdeck
```

A local `--plugin-dir` session has its own identity/options. The configuration helper targets the
marketplace-installed `agentdeck@agentdeck` package. Configure local options inside that session.

Run a scoped mocked evaluation (real Claude usage, substituted MCP tools):

```sh
claude plugin eval ./plugins/agentdeck --case missing-token --runs 1 --ablation none --trust-plugin --no-publish --max-cost-usd 2
```

See [the evaluation guide](evals/README.md) for full mock and five-industry live runs, tool grants,
reports and CI secrets. Mock success proves orchestration only; real acceptance needs a deployed
dev backend, an AgentDeck token and actual conversations.

## Releases

`dev` is the team branch; `main` is the release branch. Main pull requests come from dev, pass
validation and live acceptance on dev, and increase the version after the first release. Keep
marketplace version, plugin version and MCP header equal. Reports stay private. Configure branch
protection to require the validation and live-acceptance checks; CI alone cannot prevent bypass.

Backend: <https://github.com/AI-AgentDeck/agent-backend>. Privacy:
<https://agentdeck.eu/privacy/>. Sources can be processed by Claude and AgentDeck's model providers
as part of the requested workflow. License: [MIT](LICENSE).
