# Publishing is a separate operation

Preview creation does not publish a business agent. A preview can be reviewed from the widget's
standalone host while customer domains and external channels remain disconnected. The current
MCP tools can inspect readiness and configuration but cannot add domains or set AgentStage.LIVE.

Prepare a handover with:

- Agent UUID, environment, reviewed version and portable bundle path.
- Preview URL and the server-returned widget snippet when available.
- Approved domain and any path/language requirements supplied by the user.
- Acceptance report and unresolved business or integration questions.
- Channels requested and the connections still needed in supported console flows.
- Explicit publishing blocker if the server lacks a supported activation operation.

Do not replace a missing publishing API with SQL, a guessed HTTP route, lifecycle activation or
relaxed origin checks. A future publishing operation must be discovered from the actual server
and requires the user's authorization for that agent, environment and domain. Keep real-channel
smoke tests separate from isolated previews and disclose any real calls or notifications before
performing them. Plans, payment and customer self-service belong to later product phases.
