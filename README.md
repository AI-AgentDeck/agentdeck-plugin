# AgentDeck for Claude Code and Codex

Turn a business website, approved documents or a brief into an AgentDeck agent with configured
prompts, indexed knowledge and a tested preview. Setup reasoning runs in your Claude Code or Codex session;
AgentDeck's authenticated MCP tools handle crawling, validation and execution.

The plugin is thin. The workflow guidance — how to create, write prompts, test, update and go live —
is served by the AgentDeck server (`get_guide`), so every app connected to it gets the same rules.
The plugin adds the local bundle helper and files, an independent conversation judge and the
connection.

This is the **team preview on `dev`**. Production acceptance is not complete. The first release
will be promoted to `main` after live evaluation. One repository packages both runtimes with shared
skills and separate MCP configuration.

## Customer setup

Use an AgentDeck account and Python **3.11 or newer** for local bundle helpers.
Choose the runtime you use below. Claude Code and Codex both connect by signing in with your
AgentDeck account; no token is needed.

Customer connection is available only in environments where customer access has been enabled.
Production customer access is not enabled yet; use the dev console for this preview.

### Claude Code

Use Claude Code **2.1.310 or newer**.

1. Install the plugin (each command separately):

   ```text
   /plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
   /plugin install agentdeck@agentdeck
   ```

2. The plugin connects to dev by default. For another environment, run
   `/plugin configure agentdeck@agentdeck` and pick its URL.
3. Run `/mcp`, choose `agentdeck`, then **Authenticate**. Sign in to the AgentDeck console in the
   browser and choose **Allow**. Do this once per environment; Claude Code keeps the sign-in.

The sign-in lets the plugin create and manage agents inside your business workspace. Workspace and
daily usage limits apply. You can disconnect it again in the AgentDeck console.
Never paste tokens into normal chats or git.

In Claude Code use **either** this plugin **or** `claude mcp add` for AgentDeck — not both, or the
session has two AgentDeck servers.

### Codex CLI

Use Codex CLI **0.164.0 or newer**. The native package and launcher are tested with 0.164.0.
The IDE extension is not an installation target for this package.

Run these commands separately in your terminal:

```sh
codex plugin marketplace add AI-AgentDeck/agentdeck-plugin --ref dev
```

```sh
codex plugin add agentdeck@agentdeck
```

Sign in once, then start a new Codex session:

```sh
codex mcp login agentdeck
```

Your browser opens AgentDeck; sign in and choose **Allow**. This connects AgentDeck only — you log
into Codex with your usual Codex account, and nothing here creates an OpenAI API key. The packaged
connection uses dev.

To pick another environment, obtain the launcher from this repository:

```sh
git clone --branch dev https://github.com/AI-AgentDeck/agentdeck-plugin.git
```

Run the launcher from the directory where you want bundles and reports to be written. Replace
`/path/to` with the parent of your clone:

```sh
python3 /path/to/agentdeck-plugin/plugins/agentdeck/scripts/run_codex.py --environment dev --login
```

`--login` signs in to that environment before the session starts; leave it out once you are signed in.
The launcher supplies the matching MCP endpoint and version for that session only.

Start a new session after installation or an update. In Codex, use a bundled skill:

```text
$agentdeck:create-agent Create a preview for https://agentdeck.eu/ in dev.
```

The other skills are `$agentdeck:update-agent`, `$agentdeck:test-agent` and `$agentdeck:go-live`.
You can also describe the AgentDeck task normally. An independent judge requires a host that can
start a fresh agent; without one, acceptance remains INCOMPLETE with artifacts ready for review.

Scripts and automated runs that cannot open a browser use a personal token instead (AgentDeck
**Settings → Connect AI apps → Advanced**), with `--token-env NAME` or
`--token-file /private/token.json` — a JSON object with a `token` field, as written by the internal
mint helper. Append Codex options after `--`, such as `-- --cd /path/to/business-workspace`. The
launcher supports `dev`, `prod` and `local`; production customer access remains disabled until
separately released. Do not put a token directly in command arguments or paste it into a Codex
conversation. To update the cached package:

```sh
codex plugin marketplace upgrade agentdeck
codex plugin add agentdeck@agentdeck
```

Update the launcher checkout with `git pull --ff-only` and start a new session. Installation and
connection behavior follows the [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
and [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

## Use

Claude Code commands (run each separately):

```text
/agentdeck:create-agent https://agentdeck.eu/
/agentdeck:create-agent ./approved-business-faq.txt
/agentdeck:update-agent <agent-uuid> Correct cancellation terms using ./approved-policy.txt
/agentdeck:test-agent <agent-uuid> Check German and English prices, unknown facts and handoff
/agentdeck:go-live <agent-uuid> https://customer.example
```

Each skill calls `whoami` and then the server's guide for its job, and follows it. Business facts
stay in knowledge; prompts define behavior. On top of the guide's evaluation checklist, a read-only
judge reviews sources and conversations independently. Unresolved questions remain explicit instead
of becoming guesses. A server without `guideVersion` in `whoami` is too old for this plugin; the
skills say so and stop.

The portable configuration is saved to `./agentdeck/<slug>.json`. Private source ledgers, creation
keys and reports stay in `.agentdeck-work/<slug>/`. Keep these out of your own project's git history
too. A saved creation key makes uncertain retries idempotent. Schema and tool descriptions are read
from the backend at runtime. Updates replace a complete bundle, removing omitted sections.

## Current boundaries

- PREPARING becomes READY when initial knowledge/key setup is ready. READY is not a quality verdict.
- A READY agent answers wherever its snippet is placed, on any number of the customer's websites, and in
  the client hub's test chat. `go-live` checks acceptance and hands over the snippet and channel steps.
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

AgentDeck staff sign in the same way. For Codex or a headless evaluation, follow
[Internal setup: create an admin token](docs/internal-setup.md).

```sh
python3 scripts/check.py
python3 scripts/check_codex.py
python3 -m unittest discover -s tests -v
claude --plugin-dir ./plugins/agentdeck
```

`scripts/check_codex.py` uses a disposable Codex home and a synthetic local MCP server to check
installation, shared skill discovery, bearer/version headers and endpoint selection without model
calls. This is a packaging/connection smoke check, not live business acceptance.

A local `--plugin-dir` session has its own options and sign-in. Configure and authenticate inside it.

Run a scoped mocked evaluation (real Claude usage, substituted MCP tools):

```sh
claude plugin eval ./plugins/agentdeck --case signed-out --runs 1 --ablation none --trust-plugin --no-publish --max-cost-usd 2
```

See [the evaluation guide](evals/README.md) for full mock and five-industry live runs, tool grants,
reports and CI secrets. Mock success proves orchestration only; real acceptance needs a deployed
dev backend, an AgentDeck token (an evaluation cannot sign in through a browser) and actual
conversations.

## Releases

`dev` is the team branch; `main` is the release branch. Main pull requests come from dev, pass
validation, and increase the version after the first release. Live acceptance on dev is a manual
run (Actions → live-acceptance) when a release needs it. Keep Claude and Codex manifest versions
and MCP headers equal. Reports stay private. Branch protection requires the validation check.
Make `main` the repository's default branch when promoting the first stable release.

Backend: <https://github.com/AI-AgentDeck/agent-backend>. Privacy:
<https://agentdeck.eu/privacy/>. Sources can be processed by your selected runtime and AgentDeck's model providers
as part of the requested workflow. License: [MIT](LICENSE).
