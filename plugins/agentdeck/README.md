# AgentDeck

Create business agents from approved websites, documents or briefs in Claude Code. The plugin
uses AgentDeck's MCP tools to validate configuration, build knowledge and run isolated test chats.
It returns a preview, portable bundle and evidence report, and offers update/test/publishing-handover skills.

Install the team preview:

```text
/plugin marketplace add AI-AgentDeck/agentdeck-plugin#dev
/plugin install agentdeck@agentdeck
```

Customers obtain a business-scoped token from AgentDeck Settings → Connect Claude Code when
customer access is enabled. Select the matching environment and enter that token in the masked
option. Restart Claude Code. Create with `/agentdeck:create-agent <website-or-brief>`.
Production acceptance and a supported publishing operation are required before going live.

Customer setup, internal admin setup, validation and known limits are in the
[repository README](https://github.com/AI-AgentDeck/agentdeck-plugin/tree/dev#readme).
Privacy: <https://agentdeck.eu/privacy/>. License: MIT.
