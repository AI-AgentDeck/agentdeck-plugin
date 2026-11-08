# AgentDeck

Build, test and update the AI agent that answers your customers, from your website, in Claude Code or
Codex. AgentDeck reads the site, builds an agent that answers only from your own material, test-chats it
and hands you a preview link and the snippet for your site.

**Claude Code** — install, then sign in with `/mcp` → **agentdeck** → **Authenticate** → **Allow**:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin
/plugin install agentdeck@agentdeck
/agentdeck:create-agent https://your-business.com
```

**Codex CLI** — install, sign in, then use `$agentdeck:create-agent` in a new session:

```sh
codex plugin marketplace add AI-AgentDeck/agentdeck-plugin
codex plugin add agentdeck@agentdeck
codex mcp login agentdeck
```

The other commands are `test-agent`, `update-agent` and `go-live`. No token is needed: you sign in with
your AgentDeck account.

In the Claude desktop app: **Add marketplace** → `AI-AgentDeck/agentdeck-plugin` → **Sync** → install
**AgentDeck**.

## What it sends and stores

- It talks only to AgentDeck's server (`https://api.agentdeck.eu/mcp` unless you choose another AgentDeck
  environment in the plugin's settings), after you sign in. It sends what you give it: your website's
  address, documents you add and the agent's settings and test messages.
- It saves each agent's setup in your project, in `agentdeck/<agent>.json`, and its working notes and
  test evidence in `.agentdeck-work/<agent>/`.
- It keeps no password or token in files: signing in is handled by Claude Code or Codex.

Full guide, Claude and ChatGPT connectors and troubleshooting:
[repository README](https://github.com/AI-AgentDeck/agentdeck-plugin#readme).
[Website](https://agentdeck.eu) · [Client hub](https://client-hub.agentdeck.eu) ·
[Privacy](https://client-hub.agentdeck.eu/privacy-policy) · MIT license.
