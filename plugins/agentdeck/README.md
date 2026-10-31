<img src="../../docs/assets/agentdeck-icon.svg" width="56" height="56" alt="AgentDeck">

# AgentDeck

Build, test and update the AI agent that answers your customers, from your website, in Claude Code or
Codex. AgentDeck reads the site, builds an agent that answers only from your own material, test-chats it
and hands you a preview link and the snippet for your site.

**Claude Code** — install, then sign in with `/mcp` → **agentdeck** → **Authenticate** → **Allow**:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
/agentdeck:create-agent https://your-business.com
```

**Codex CLI** — install, sign in, then use `$agentdeck:create-agent` in a new session:

```sh
codex plugin marketplace add AI-AgentDeck/agentdeck-plugin --ref dev
codex plugin add agentdeck@agentdeck
codex mcp login agentdeck
```

The other commands are `test-agent`, `update-agent` and `go-live`. No token is needed: you sign in with
your AgentDeck account. This preview connects to the dev environment.

Full guide, Claude and ChatGPT connectors and troubleshooting:
[repository README](https://github.com/AI-AgentDeck/agentdeck-plugin/tree/dev#readme).
[Website](https://agentdeck.eu) · [Client hub](https://client-hub.agentdeck.eu) ·
[Privacy](https://client-hub.agentdeck.eu/privacy-policy) · MIT license.
