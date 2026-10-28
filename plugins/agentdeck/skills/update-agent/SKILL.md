---
name: update-agent
description: Inspect and revise an existing AgentDeck agent's prompts, settings or knowledge, preserve unrelated configuration and test the change.
---

Use the user’s request as the agent ID and requested change.
Read [connection](../../references/connection.md) and [the backend contract](../../references/backend-contract.md).

1. Call `whoami`, verify environment and scope, then `get_spec` and `get_agent` for the supplied
   UUID. If the user has only a business name, ask for the UUID or the private creation report;
   do not guess another tenant's agent. Read status and export warnings too.
2. Start from the returned complete bundle and version. Identify the requested sections and
   preserve every unrelated section. A whole-bundle write removes omitted sections. Keep domain,
   credential and channel configuration outside the bundle. Review export warnings before writing
   because some file-only settings cannot be represented in an export.
3. Use [prompt design](../../references/prompt-design.md) for behavioral edits. For knowledge
   corrections, establish the authoritative source and replace contradicted text rather than
   adding a second conflicting answer. Removing a source deletes its indexed web/FAQ content on
   refresh; uploads have a separate lifecycle and no delete tool is currently exposed here.
4. Call `validate_agent` with the agent ID and proposed complete bundle. Explain the section diff,
   source removals, warnings and the intended behavior. Apply within the user's authorized scope.
   The version protects against other bundle writes; console edits do not advance that version.
   Read back immediately before applying, compare with the snapshot used for the proposal, and
   stop to reconcile any intervening edit. This comparison narrows the race; it is not an atomic
   guarantee against a console write during application.
5. Call `update_agent` with the returned version as `expectedVersion`. On `stale_version`, read
   again, rebuild the requested change and revalidate; do not blindly overwrite the newer bundle.
   An uncertain response calls for reading status and configuration before deciding to retry.
6. Wait for any refresh to finish. Use the [acceptance checklist](../../references/evaluation.md)
   on new test threads for changed behavior and a representative unchanged behavior. Use the
   independent judge and at most two correction rounds. Stop on operational failures or exhausted
   caps instead of looping.
7. Export again and save the portable bundle using
   the bundled `scripts/bundle.py save --input <export.json> --slug <slug>` (see the runtime guide).
   The input is the bundle object, not its response envelope. Use `--replace` only for a local
   bundle the user asked to update. Report the applied version, differences, test outcomes,
   unresolved warnings and preview link if known. Never say a live agent has been sandboxed merely
   because these particular test conversations are isolated.
