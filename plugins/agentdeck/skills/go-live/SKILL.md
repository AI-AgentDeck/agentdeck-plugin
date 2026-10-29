---
name: go-live
description: Check an AgentDeck agent's acceptance evidence and hand over its widget snippet and channel steps.
---

Use the user’s request as the agent ID and the websites it should appear on.
Read [connection](../../references/connection.md) and [publishing](../../references/publishing.md).

Call `whoami`, `get_agent` and `get_agent_status` for the requested agent. Verify the environment,
scope, `stage=READY` and current version. Read the acceptance report and match its version and
sources to the agent; unresolved blockers or incomplete tests stop the handover.

A READY agent needs no activation: it answers wherever its snippet is placed. The snippet is the
`widgetSnippet` a `create_agent` or `update_agent` result returned (in the creation report), or the
one the client hub shows under the agent's Integrations; never assemble one from a guessed key. If a
site refuses the widget, the environment checks declared domains and an operator must add it. Hand
over the snippet, the websites it goes on, requested channels with the client hub flows that connect them,
and the acceptance evidence. Do not invent a publish endpoint or edit the database. Place a snippet
on a public site only with the user's explicit authorization, and keep any public smoke test
separately authorized.
Channel setup is separate: credentials and accounts belong in the console's connection flows.
Never use real notifications, CRM writes, bookings or phone calls as an incidental test.
