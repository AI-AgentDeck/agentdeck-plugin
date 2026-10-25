---
name: create-agent
description: Create an AgentDeck business agent from a website, local documents or a business brief, then validate and test its preview.
argument-hint: "<website URL | local document | business brief>"
---

Create a business-specific agent with configured prompts and searchable knowledge. Finish with a
tested preview, a portable bundle and any unresolved business questions. Configured MCP endpoint:
`${user_config.mcp_url}`. Use this request as the business input: $ARGUMENTS.

Read [connection and authorization](../../references/connection.md) first. Use the plugin's
`agentdeck` MCP server (`mcp__plugin_agentdeck_agentdeck__*`).

1. Call `whoami`. Verify the selected environment, ADMIN scope for creation, compatibility and caps.
   An authentication failure ends the run with setup instructions; do not ask for a token in chat.
   Read `get_spec` and the available tool schemas. They define the actual bundle and operation inputs.
2. For a website, start `crawl` and poll its returned ID as described in
   [the backend contract](../../references/backend-contract.md). Review the pages and obtain full
   text for facts that the returned excerpts do not establish. For text or files, read only the
   supplied material. Keep a source ledger under `.agentdeck-work/<slug>/`.
3. Establish the job: answers, lead capture and any supported actions; visitor languages; handoff
   contact and channel; tone; and non-negotiable boundaries. Infer these only when supported by the
   request or sources. Ask one batch of at most five remaining questions. If an answer is unavailable,
   record the gap and configure the agent to acknowledge it instead of filling it in.
4. Follow [prompt design](../../references/prompt-design.md) and the relevant
   [industry pattern](../../references/industry-patterns.md). Put changing business facts in the
   knowledge base. Write system and enabled-feature prompts, profiles, widget texts and lead fields
   against `get_spec`. Use supported model and language IDs from `whoami`. Choose only actions whose
   actual tool and environment configuration exist. A request for booking or callbacks does not
   establish that a calendar or phone connection is available.
5. Call `validate_agent`, fix every error at its returned path and disclose warnings. Show the
   business goal, sources, languages, actions and environment that will be created. An existing
   instruction to create in this environment authorizes creation; clarify unresolved scope before
   writing. Save the candidate locally and run the bundled `scripts/bundle.py prepare` helper with
   a descriptive slug and `--environment dev|prod|local`. It records a stable idempotency key before the first create attempt.
6. Send the validated bundle as one JSON string to `create_agent`, using that recorded key. Retry
   an uncertain create only with exactly the same bundle and key. Save returned IDs and links in
   the private run state, separate from the portable bundle. The present create tool does not
   accept a crawl ID or file bytes: discovered URLs go into the bundle; uploads require the new
   agent ID. Follow the backend contract for file ingestion and indexing verification.
7. Poll `get_agent_status` until `TEST`, `crawled=true`, no failed or unfinished refresh, and the key
   is ready where reported. Follow the bounded polling rules. `TEST` is infrastructure readiness,
   not a quality verdict. Run [the acceptance checklist](../../references/evaluation.md) on fresh
   test threads, invoke `agentdeck:chat-judge` with the source evidence and transcripts, and make
   at most two correction rounds through `get_agent` → validate → `update_agent`. Wait for each
   refresh and retest affected cases. Account for `inFlight` and `failed` results exactly as the
   backend contract describes. Never count an unanswered or unjudged case as passing.
8. Read back `get_agent`, preserve its export warnings, and use `scripts/bundle.py save` to write
   the final id-free configuration to `./agentdeck/<slug>.json` (`--replace` for the candidate prepared by this same run). Report the agent ID, environment,
   version, preview link, widget snippet when returned, test verdicts with evidence and remaining
   gaps. Write the report to `.agentdeck-work/<slug>/report.md`. Distinguish ready for review from
   blocked or failed acceptance. Publishing is handled by `/agentdeck:go-live`.

The helper is `${CLAUDE_PLUGIN_ROOT}/scripts/bundle.py`; run `--help` for its arguments. It performs
local persistence checks; `validate_agent` remains the configuration validator. When local file
tools are unavailable, report the missing bundle artifact rather than claiming it was saved.
