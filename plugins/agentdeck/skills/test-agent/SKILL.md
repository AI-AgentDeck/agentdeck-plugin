---
name: test-agent
description: Evaluate an existing AgentDeck agent against approved business sources with isolated conversations and an independent judge.
---

Use the user’s request as the agent ID and test focus. The AgentDeck server's guide says how to
test; this skill adds the local files and the independent judge. Read
[connection](../../references/connection.md) and [the runtime guide](../../references/runtime.md).

1. Call `whoami` and check it as the connection guide says. A missing `guideVersion` means the
   server is older than this plugin: tell the user the AgentDeck server needs updating and stop.
2. Call `get_guide(topic="test")` and follow it, with `get_guide(topic="evaluation")` for the
   checklist and, when it refers to them, `get_guide(topic="overview")` and
   `get_guide(topic="server-rules")`. Do not fill a missing topic from memory — report it.
3. In addition to the guide's checklist, send the sources, expected behavior and complete
   transcripts to the plugin's independent judge (see the runtime guide). Its review is read-only.
   An unavailable judge leaves cases INCOMPLETE; a case passes only when both pass it.
4. Store transcripts and the report under `.agentdeck-work/<slug>/`. Separate mock-server
   orchestration results from real backend conversations. Testing alone does not authorize
   editing or publishing; use the `update-agent` skill for requested corrections.
