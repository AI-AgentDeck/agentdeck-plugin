---
name: update-agent
description: Inspect and revise an existing AgentDeck agent's prompts, settings or knowledge, preserve unrelated configuration and test the change.
---

Use the user’s request as the agent ID and requested change. The AgentDeck server's guide says how
to update safely; this skill adds the local files and the independent judge. Read
[connection](../../references/connection.md) and [the runtime guide](../../references/runtime.md).

1. Call `whoami` and check it as the connection guide says. A missing `guideVersion` means the
   server is older than this plugin: tell the user the AgentDeck server needs updating and stop.
2. Call `get_guide(topic="update")` and follow it. When it refers to them, call
   `get_guide(topic="overview")`, `get_guide(topic="prompt-design")`,
   `get_guide(topic="evaluation")` and `get_guide(topic="server-rules")`. Do not fill a missing
   topic from memory — report it.
3. If the user has only a business name, ask for the agent UUID or the private creation report
   under `.agentdeck-work/`; never guess another tenant's agent.
4. Test the change as the guide says, then — in addition to its checklist — send the sources,
   expectations and complete transcripts to the plugin's independent judge (see the runtime guide).
5. Export again and save the portable bundle with the bundled
   `scripts/bundle.py save --input <export.json> --slug <slug>`. The input is the bundle object, not
   its response envelope. Use `--replace` only for a local bundle the user asked to update. Write
   the report to `.agentdeck-work/<slug>/report.md`.
