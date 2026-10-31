---
name: go-live
description: Check an AgentDeck agent's acceptance evidence and hand over its widget snippet and channel steps.
---

Use the user’s request as the agent ID and the websites it should appear on. The AgentDeck server's
guide says what a handover contains; this skill adds where the local evidence is. Read
[connection](../../references/connection.md).

1. Call `whoami` and check it as the connection guide says. A missing `guideVersion` means the
   server is older than this plugin: tell the user the AgentDeck server needs updating and stop.
2. Call `get_guide(topic="go-live")` and follow it, with `get_guide(topic="overview")` and
   `get_guide(topic="server-rules")` when it refers to them. Do not fill a missing topic from
   memory — report it.
3. The acceptance evidence is the report under `.agentdeck-work/<slug>/report.md` and the portable
   bundle under `./agentdeck/`. A missing or mismatched report is a gap to name, not a pass.
4. Place a snippet on a public site, connect a channel or run a real-channel smoke test only with
   the user's explicit authorization for that agent, environment and site.
