---
name: go-live
description: Check an AgentDeck preview's acceptance evidence and prepare its domain, widget and channel publishing handover.
argument-hint: "<agent UUID> <approved domain>"
---

Configured MCP endpoint: `${user_config.mcp_url}`. Publishing request: $ARGUMENTS.
Read [connection](../../references/connection.md) and [publishing](../../references/publishing.md).

Call `whoami`, `get_agent` and `get_agent_status` for the requested agent. Verify the environment,
scope, approved customer domain and current version. Read the acceptance report and match its
version and sources to the agent; unresolved blockers or incomplete tests stop the handover.

Inspect the tools the server actually exposes. The current contract has no supported MCP tool
that adds customer domains or transitions an agent from TEST to LIVE. When those operations are
absent, report `BLOCKED: publishing operation unavailable` and produce a precise admin handover:
agent UUID, environment, reviewed version, approved domain, widget snippet if previously returned,
requested channels and acceptance evidence. Refer the operator to supported platform controls or
a backend change. Do not invent a publish endpoint, edit the database, bypass origin checks or
treat Lifecycle.ACTIVE as AgentStage.LIVE.

If a future server exposes publishing, read its schema and requirements, show what will become
public and apply only the user's explicit publishing authorization for this agent, domain and
environment. Verify the resulting LIVE state and perform a separately authorized public smoke test.
Channel setup is separate: credentials and accounts belong in the console's connection flows.
Never use real notifications, CRM writes, bookings or phone calls as an incidental test.
