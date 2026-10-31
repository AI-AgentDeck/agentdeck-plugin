<p align="center">
  <a href="https://agentdeck.eu"><img src="docs/assets/agentdeck-icon.svg" width="88" height="88" alt="AgentDeck"></a>
</p>

<h1 align="center">AgentDeck for Claude Code and Codex</h1>

<p align="center">
  Build, test and update the AI agent that answers your customers — from your website, in a chat with your AI app.
</p>

<p align="center">
  <a href="https://agentdeck.eu">Website</a> ·
  <a href="https://client-hub.agentdeck.eu">Client hub</a> ·
  <a href="https://agentdeck.eu/connect/">Connect guide</a> ·
  <a href="https://client-hub.agentdeck.eu/privacy-policy">Privacy</a> ·
  <a href="LICENSE">MIT license</a>
</p>

---

Tell your AI app about your business and give it your website. AgentDeck reads the site, asks a few
questions — what the agent should achieve, which languages your customers write in, when a person should
take over — and builds an agent that answers only from your own material. It then test-chats the agent,
checks the answers against your website and hands you a preview link and a one-line snippet for your site.

> **Preview.** The plugin and the addresses below connect to the dev environment (`dev-api.agentdeck.eu`,
> client hub `dev-client-hub.agentdeck.eu`). Production customer access is not switched on yet.

## Pick your app

| You use | Install anything? | Go to |
|---|---|---|
| **Claude** on the web, desktop or phone | No — add AgentDeck as a connector | [Claude](#claude-web-desktop-phone) |
| **ChatGPT** (Plus, Pro, Business) | No — add AgentDeck as a connector | [ChatGPT](#chatgpt) |
| **Claude Code** | The plugin (recommended) | [Claude Code](#claude-code) |
| **The Claude desktop app** with the plugin | Add this repository as a marketplace | [Claude desktop app](#claude-desktop-app) |
| **Codex CLI** | The plugin | [Codex](#codex-cli) |

**The plugin installs from this repository's name alone:** wherever an app asks for a marketplace, enter
[`AI-AgentDeck/agentdeck-plugin`](https://github.com/AI-AgentDeck/agentdeck-plugin) and install **AgentDeck**.

Every app connects by **signing in with your AgentDeck account** and choosing **Allow**. You never copy an
API key or a token. No account yet? [Create one in the client hub](https://client-hub.agentdeck.eu/sign-up).

The plugin adds what a connector cannot: ready-made commands, local copies of every agent, and an
independent second check of each test conversation. The rules for building a good agent are served by
AgentDeck itself, so every app follows the same ones.

## Claude Code

Needs Claude Code **2.1.310 or newer** and Python **3.11 or newer**.

**1. Install** — in Claude Code, one command at a time:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin
```

```text
/plugin install agentdeck@agentdeck
```

**2. Sign in** — type `/mcp`, choose **agentdeck**, then **Authenticate**. Your browser opens AgentDeck: sign
in and choose **Allow**. Once per environment; Claude Code remembers it.

**3. Create your first agent:**

```text
/agentdeck:create-agent https://your-business.com
```

| Command | What it does | Example |
|---|---|---|
| `/agentdeck:create-agent` | Builds an agent from a website, a document or a short brief | `/agentdeck:create-agent https://your-business.com` |
| `/agentdeck:test-agent` | Test-chats the agent and reports what it gets wrong | `/agentdeck:test-agent <agent id> check prices in German and English` |
| `/agentdeck:update-agent` | Changes what the agent says or knows, then tests again | `/agentdeck:update-agent <agent id> new cancellation terms from ./policy.txt` |
| `/agentdeck:go-live` | Checks the agent is ready and gives you the snippet for your site | `/agentdeck:go-live <agent id> https://your-business.com` |

You can also just ask, for example *"Create an AgentDeck agent for my website"*. The agent id is in the
result of `create-agent` and in the client hub.

Use **either** the plugin **or** `claude mcp add` for AgentDeck in Claude Code, not both — otherwise the
session has two AgentDeck servers.

## Claude desktop app

1. Open the app's plugins and choose **Add marketplace**.
2. Enter `AI-AgentDeck/agentdeck-plugin` and click **Sync**.
3. Install **AgentDeck** from the list, then sign in to AgentDeck and choose **Allow** when it asks.

Use the same commands as in Claude Code, for example `/agentdeck:create-agent https://your-business.com`.
If you only chat in the app and do not need saved files, the [connector](#claude-web-desktop-phone) is
simpler still.

## Codex CLI

Needs Codex CLI **0.164.0 or newer** and Python **3.11 or newer**. The IDE extension is not supported.

**1. Install** — in your terminal, one command at a time:

```sh
codex plugin marketplace add AI-AgentDeck/agentdeck-plugin
```

```sh
codex plugin add agentdeck@agentdeck
```

**2. Sign in:**

```sh
codex mcp login agentdeck
```

Your browser opens AgentDeck: sign in and choose **Allow**. This connects AgentDeck only; you keep signing in
to Codex with your usual account.

**3. Create your first agent** — in a new Codex session:

```text
$agentdeck:create-agent https://your-business.com
```

The other commands are `$agentdeck:test-agent`, `$agentdeck:update-agent` and `$agentdeck:go-live`, as in
the Claude Code table above.

<details>
<summary>Another environment, or a script</summary>

The packaged connection uses dev. To choose dev, prod or local for one session, use the launcher from a clone
of this repository, run from the folder where your agent files should be written:

```sh
git clone https://github.com/AI-AgentDeck/agentdeck-plugin.git
```

```sh
python3 /path/to/agentdeck-plugin/plugins/agentdeck/scripts/run_codex.py --environment dev --login
```

`--login` signs in to that environment first; leave it out once you are signed in. Codex options go after
`--`, for example `-- --cd /path/to/workspace`.

A script that cannot open a browser uses a personal token instead (client hub → **Settings → Connect AI apps
→ Advanced**), passed with `--token-env NAME` or `--token-file /private/token.json` (a JSON object with a
`token` field). Never put a token in a command line or a chat.

</details>

## Claude (web, desktop, phone)

No install. Add it once on the web or in the desktop app.

1. Copy the AgentDeck address:

   ```text
   https://dev-api.agentdeck.eu/mcp
   ```

2. Open [Claude's connector window](https://claude.ai/new?modal=add-custom-connector#customize/connectors).
3. Name it **AgentDeck**, paste the address and click **Add**. Leave the other options as they are.
4. Sign in to AgentDeck in the window that opens and click **Allow**.

Then, in a new chat: *"Create an AgentDeck agent for https://your-business.com"*.

## ChatGPT

No install. Needs ChatGPT Plus, Pro or Business.

1. Open [ChatGPT settings → Connectors](https://chatgpt.com/#settings/Connectors), open **Advanced settings**
   and turn on **Developer mode**.
2. Copy the AgentDeck address: `https://dev-api.agentdeck.eu/mcp`
3. Click **Create**, name it **AgentDeck**, paste the address and choose **OAuth** as the authentication.
4. Sign in to AgentDeck in the window that opens and click **Allow**.

Then, in a new chat with AgentDeck turned on: *"Create an AgentDeck agent for https://your-business.com"*.

## Claude Code without the plugin

If you only want the AgentDeck tools, without the commands:

```sh
claude mcp add --transport http agentdeck https://dev-api.agentdeck.eu/mcp
```

Then type `/mcp` in Claude Code, choose **agentdeck** → **Authenticate**, and click **Allow** in the browser.

## After you connect

- **See and manage your agents** in the [client hub](https://client-hub.agentdeck.eu): conversations, leads,
  the website chat's look, Instagram, WhatsApp, Messenger and Telegram.
- **Disconnect an app** under **Settings → Connect AI apps** in the client hub.
- **Your files** (plugin only): each agent's configuration is saved to `./agentdeck/<name>.json`, and the
  sources, test conversations and report to `.agentdeck-work/<name>/`. Keep both out of public git.
- **Limits**: each workspace has a number of agents and daily crawls and test chats. The client hub's
  **Connect AI apps** page shows them.

## Update the plugin

Claude Code:

```text
/plugin marketplace update agentdeck
```

Codex:

```sh
codex plugin marketplace upgrade agentdeck
```

```sh
codex plugin add agentdeck@agentdeck
```

Start a new session afterwards. If AgentDeck answers `plugin_outdated`, it is time to update.

## Troubleshooting

| You see | Do this |
|---|---|
| "needs authentication" or a sign-in error | Claude Code: `/mcp` → **agentdeck** → **Authenticate**. Codex: `codex mcp login agentdeck`. |
| Two AgentDeck servers in Claude Code | Remove the one added with `claude mcp add` (`claude mcp remove agentdeck`) and keep the plugin. |
| `plugin_outdated` | [Update the plugin](#update-the-plugin) and start a new session. |
| `cap_reached` | A daily limit was reached; the message says when it resets (00:00 UTC). |
| The agent is still "preparing" | It is still reading your website. Wait a minute and ask again. |

Questions: <info@agentdeck.eu>.

## Developers

<details>
<summary>How it is built, current limits, validation and releases</summary>

The plugin is thin. The workflow guidance — how to create, write prompts, test, update and go live — is
served by the AgentDeck server (`get_guide`), so every connected app gets the same rules. The plugin adds the
local bundle helper and files, an independent conversation judge and the connection. One repository packages
both runtimes with shared skills and separate MCP configuration. Each skill calls `whoami` and then the
server's guide for its job; a server without `guideVersion` in `whoami` is too old for this plugin, and the
skills say so and stop. A saved creation key makes uncertain retries idempotent. Updates replace a complete
bundle, removing omitted sections. For another Claude Code environment run
`/plugin configure agentdeck@agentdeck` and sign in again.

### Current boundaries

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

### Develop and validate

Customers install from `main`, the default branch. To try unreleased changes, install from `dev`:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
```

AgentDeck staff sign in the same way. For a headless evaluation, follow
[Internal setup: create an admin token](docs/internal-setup.md).

```sh
python3 scripts/check.py
python3 scripts/check_codex.py
python3 -m unittest discover -s tests -v
claude --plugin-dir ./plugins/agentdeck
```

`scripts/check_codex.py` uses a disposable Codex home and a synthetic local MCP server to check
installation, shared skill discovery, the version header and endpoint selection without model
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

### Releases

`dev` is the team branch; `main` is the release branch. Main pull requests come from dev, pass
validation, and increase the version after the first release. Live acceptance on dev is a manual
run (Actions → live-acceptance) when a release needs it. Keep Claude and Codex manifest versions
and MCP headers equal. Reports stay private. Branch protection requires the validation check.
Make `main` the repository's default branch when promoting the first stable release.

Backend: <https://github.com/AI-AgentDeck/agent-backend>. Sources you give the plugin can be processed by
your AI app and AgentDeck's model providers as part of the requested workflow.

</details>
