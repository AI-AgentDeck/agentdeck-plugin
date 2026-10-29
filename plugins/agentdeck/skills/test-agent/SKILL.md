---
name: test-agent
description: Evaluate an existing AgentDeck agent against approved business sources with isolated conversations and an independent judge.
---

Use the user’s request as the agent ID and test focus.
Read [connection](../../references/connection.md), [the backend contract](../../references/backend-contract.md)
and [evaluation](../../references/evaluation.md).

1. Call `whoami`, verify environment and tenant scope, then read `get_agent` and `get_agent_status`.
   Refuse to grade an agent that is preparing, inactive, or has a failed/unfinished knowledge
   refresh. Establish approved sources and the intended job from the user or the creation report.
   Exported prompts alone are not evidence that a business claim is true.
2. Select about ten conversations from the checklist, covering every configured visitor language
   and the user's requested capabilities. Expand the count when ten cannot cover all languages.
   Write expected facts, allowed actions and unknowns before seeing the answers. Use fresh threads
   between independent cases, preserve the thread ID inside a multi-turn case, and send at most
   five messages in a tool call.
3. Call `test_agent` and retain complete replies and widget frames. Only `unanswered` messages can
   be resent without duplicating an already-started turn. A reported `inFlight` turn is still
   running and charged; do not resend it or start a continuation on that thread while unresolved.
   A `failed` turn stays charged and fails that case. No polling API currently retrieves an
   in-flight result; mark the case incomplete and explain the limitation.
4. Send sources, expected behavior and transcripts to the independent judge described in the runtime guide. Its read-only review
   must not change the agent. An unavailable judge leaves cases unjudged. Mark invented facts,
   incorrect language, prompt/credential disclosure and false action confirmations as blockers.
   Record unsupported or unobservable side-effect checks rather than claiming them passed.
5. Report per-case PASS, FAIL or INCOMPLETE, evidence and overall acceptance. Store transcripts
   and the report under `.agentdeck-work/<slug>/`. Separate mock-server orchestration results
   from real backend conversations. Testing alone does not authorize editing or publishing;
   use the `update-agent` skill for requested corrections.
