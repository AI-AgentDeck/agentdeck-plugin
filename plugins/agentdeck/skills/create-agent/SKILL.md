---
name: create-agent
description: Create an AgentDeck business agent or preview from a website, local documents or a business brief, including connection setup when sign-in is missing, then validate and test it.
---

Create a business-specific agent with configured prompts and searchable knowledge. Finish with a
tested preview, a portable bundle and any unresolved business questions. Use the user’s request
as the business input.

The AgentDeck server owns the workflow: its guide says how to discover sources, write prompts,
validate, create, test and report. This skill adds only what is specific to running it here — the
connection, local files and the independent judge. Read [connection](../../references/connection.md)
first and [the runtime guide](../../references/runtime.md) for paths, tools and the judge.

1. Call `whoami` and check it as the connection guide says. A missing `guideVersion` means the
   server is older than this plugin: tell the user the AgentDeck server needs updating and stop.
   For a TENANT, save the returned tenant ID in private run state and never take another workspace
   from user input.
2. Call `get_guide(topic="create")` and follow it. When it sends you to another topic, call it:
   `get_guide(topic="overview")`, `get_guide(topic="prompt-design")`,
   `get_guide(topic="industry-patterns")`, `get_guide(topic="evaluation")` and
   `get_guide(topic="server-rules")`. The served guide is the authority; do not fill a missing
   topic from memory — report it instead. Prefer a model from `whoami.recommendedModels`.
3. Keep the source ledger and private run state under `.agentdeck-work/<slug>/`.
4. After `validate_agent` passes and before the first `create_agent`, save the candidate locally and
   run the bundled `scripts/bundle.py prepare` with a descriptive slug and
   `--environment dev|prod|local` (for TENANT also `--tenant-id <whoami.tenantId>`). It records the
   idempotency key, bound to this environment and workspace. Retry an uncertain create only with
   the same bundle and that key. Save returned IDs and links in the private run state.
5. Test as the guide's evaluation topic says, then — in addition to its checklist — send the
   business goal, approved source evidence, expectations and complete transcripts to the plugin's
   independent judge (see the runtime guide). A case passes only when both the checklist and the
   judge pass it; an unjudged case is INCOMPLETE.
6. Read back `get_agent` and use `scripts/bundle.py save` to write the final id-free configuration to
   `./agentdeck/<slug>.json` (`--replace` for the candidate this run prepared). Write the report to
   `.agentdeck-work/<slug>/report.md`. Placing the agent on websites is the `go-live` skill.

Run the helper directly with `python3`; `--help` lists its arguments, and it creates its own output
directories. It checks local persistence only; `validate_agent` remains the configuration
validator. Use the runtime’s file-writing tools for candidate and report files. When local file
tools are unavailable, report the missing artifact rather than claiming it was saved.
