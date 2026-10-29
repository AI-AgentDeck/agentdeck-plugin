---
name: create-agent
description: Create an AgentDeck business agent or preview from a website, local documents or a business brief, including connection setup when authentication is missing, then validate and test it.
---

Create a business-specific agent with configured prompts and searchable knowledge. Finish with a
tested preview, a portable bundle and any unresolved business questions. Use the user’s request
as the business input.

Read [connection and authorization](../../references/connection.md) first. Use the plugin's `agentdeck` MCP server and follow
[the runtime guide](../../references/runtime.md) for paths, tools and the independent judge.

1. Call `whoami`. Verify the selected environment, scope, compatibility and caps. ADMIN creates a
   new business; TENANT creates inside its existing workspace when `capabilities.createAgent=true`.
   For a tenant, save its returned tenant ID in private run state and never take another workspace
   from user input. A missing or false customer capability ends creation with setup/update instructions.
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
   a descriptive slug and `--environment dev|prod|local`. For TENANT also pass `--tenant-id <whoami.tenantId>`.
   It records a stable idempotency key before the first create attempt, bound to this environment and workspace.
6. Send the validated bundle as one JSON string to `create_agent`, using that recorded key. Retry
   an uncertain create only with exactly the same bundle and key. Save returned IDs and links in
   the private run state, separate from the portable bundle. For TENANT, verify the result's tenant
   matches `whoami`; stop and report a mismatch. The present create tool does not
   accept a crawl ID or file bytes: discovered URLs go into the bundle; uploads require the new
   agent ID. Follow the backend contract for file ingestion and indexing verification.
7. Poll `get_agent_status` until `READY`, `crawled=true`, no failed or unfinished refresh, and the key
   is ready where reported. Follow the bounded polling rules. `READY` is infrastructure readiness,
   not a quality verdict. Run [the acceptance checklist](../../references/evaluation.md) on fresh
   test threads, invoke the independent judge using the runtime guide with the source evidence and transcripts, and make
   at most two correction rounds through `get_agent` → validate → `update_agent`. Wait for each
   refresh and retest affected cases. Account for `inFlight` and `failed` results exactly as the
   backend contract describes. Never count an unanswered or unjudged case as passing.
8. Read back `get_agent`, preserve its export warnings, and use `scripts/bundle.py save` to write
   the final id-free configuration to `./agentdeck/<slug>.json` (`--replace` for the candidate prepared by this same run). Report the agent ID, environment,
   version, preview link, widget snippet when returned, test verdicts with evidence and remaining
   gaps. Write the report to `.agentdeck-work/<slug>/report.md`. Distinguish ready for review from
   blocked or failed acceptance. Placing it on websites is handled by the `go-live` skill.

The helper is the bundled `scripts/bundle.py` (resolve its path using the runtime guide); run `--help` for its arguments. It performs
local persistence checks; `validate_agent` remains the configuration validator. When local file
tools are unavailable, report the missing bundle artifact rather than claiming it was saved.
Use the runtime’s file-writing tools for candidate and report files. Run the helper directly with `python3`; it creates
its output directories, so no shell `mkdir`, `cat` or command chain is needed.
