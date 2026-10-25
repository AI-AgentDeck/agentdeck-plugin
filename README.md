# AgentDeck for Claude Code

Turn a business website, approved documents or a brief into an AgentDeck agent with configured
prompts, indexed knowledge and a tested preview. Setup reasoning runs in your Claude Code session;
AgentDeck's authenticated MCP tools handle crawling, validation and execution.

This is the **team preview on `dev`**. Production acceptance is not complete. The first release
will be promoted to `main` after live evaluation. This package currently targets Claude Code.

## Customer setup

Use Claude Code **2.1.310 or newer** and an AgentDeck account. Python **3.11 or newer** is
required for the plugin's local bundle helpers.

Customer connection is available only in environments where customer access has been enabled.
Production customer access is not enabled yet. Once available:

1. Sign in to AgentDeck and open **Settings → Connect Claude Code**.
2. Create a named token for your business workspace.
3. Follow the plugin installation commands shown on that page.
4. Inside Claude Code, open the configuration dialog:

   ```text
   /plugin configure agentdeck@agentdeck
   ```

5. Select the matching environment and paste your token into its masked field. Restart Claude Code.

Your token lets the plugin create and manage agents inside your business workspace. Workspace and
daily usage limits apply across its tokens. You can revoke a token from the same connection page.
Never paste tokens into normal chats or git.

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

The team preview is installed from `dev`:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
```

For AgentDeck staff and developers who need admin access, follow
[Internal setup: create an admin token](docs/internal-setup.md). That guide covers the admin API,
the hidden-prompt mint helper and secure configuration for team testing.

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
Make `main` the repository's default branch when promoting the first stable release.

Backend: <https://github.com/AI-AgentDeck/agent-backend>. Privacy:
<https://agentdeck.eu/privacy/>. Sources can be processed by Claude and AgentDeck's model providers
as part of the requested workflow. License: [MIT](LICENSE).
