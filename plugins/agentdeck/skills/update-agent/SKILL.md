---
name: update-agent
description: Inspect and revise an existing AgentDeck agent's prompts, settings or knowledge, preserve unrelated configuration and test the change.
---

Use the user’s request as the agent to change (a name or an ID) and the requested change. The AgentDeck server's guide says how
to update safely; this skill adds the local files and the independent judge. Read
[connection](../../references/connection.md) and [the runtime guide](../../references/runtime.md).

1. Call `whoami` and check it as the connection guide says. A missing `guideVersion` means the
   server is older than this plugin: tell the user the AgentDeck server needs updating and stop.
2. Read the guide in one call, `get_guide(topics=["update", "impact", "overview",
   "prompt-design", "evaluation", "server-rules"])`, and follow the update topic. Do not fill a missing
   topic from memory — report it.
3. Find the agent with `list_agents` (`query` with the agent or business name); if several match,
   let the user pick. Never guess, and never act outside the connection's scope.
4. Change it with `update_agent` as the guide says: a `patch` of only the keys that change, with the
   `version` and `fingerprint` from `get_agent`. On `stale_version`, read `get_agent` again and
   rebuild the change; never resend the old one.
5. Test the change as the guide says, then — in addition to its checklist — send the sources,
   expectations and complete transcripts to the plugin's independent judge (see the runtime guide).
6. Export again and save the portable bundle with the bundled
   `scripts/bundle.py save --input <export.json> --slug <slug>`. The input is the bundle object, not
   its response envelope. Use `--replace` only for a local bundle the user asked to update. Write
   the report to `.agentdeck-work/<slug>/report.md`.
