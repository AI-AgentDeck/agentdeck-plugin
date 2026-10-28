# AgentDeck

Create business agents from approved websites, documents or briefs in Claude Code or Codex. The plugin
uses AgentDeck's MCP tools to validate configuration, build knowledge and run isolated test chats.
It returns a preview, portable bundle and evidence report, and offers update/test/publishing-handover skills.

Install the Claude Code team preview (each command separately):

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
```

Customers obtain a business-scoped token from AgentDeck Settings → Connect Claude Code when
customer access is enabled. Select the matching environment and enter that token in the masked
option. Restart Claude Code. Create with `/agentdeck:create-agent <website-or-brief>`.
For Codex CLI 0.164.0 or newer, add the native marketplace and package in your terminal:

```sh
codex plugin marketplace add AI-AgentDeck/agentdeck-plugin --ref dev
codex plugin add agentdeck@agentdeck
```

Use the repository README's hidden-prompt launcher to select the environment and supply your
workspace token without saving it in configuration or command arguments. In a new Codex session,
use `$agentdeck:create-agent Create a preview for <website> in dev.` Shared workflows preserve
the same workspace limits, validation, knowledge and test-isolation rules.

Production acceptance comes before placing an agent on a customer's website; a READY agent needs no other activation.

Customer setup, internal admin setup, validation and known limits are in the
[repository README](https://github.com/AI-AgentDeck/agentdeck-plugin/tree/dev#readme).
Privacy: <https://agentdeck.eu/privacy/>. License: MIT.
