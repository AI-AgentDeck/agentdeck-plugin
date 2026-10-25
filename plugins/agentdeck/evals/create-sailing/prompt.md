---
max_turns: 90
runs: 1
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit, Bash]
tags: [mock, creation, industry]
---
Create an AgentDeck preview in dev for Synthetic Sailing, using slug synthetic-sailing. This is an explicitly SYNTHETIC orchestration evaluation. MCP is mocked; do not present its outputs as real-business acceptance. You may create and test the mock agent and save local run files. All necessary business decisions are supplied below; ask only if something is actually missing.

The approved complete source is this brief, associated with https://synthetic-sailing.example/. The beginner course lasts 6 days. Published tuition is 640 EUR. Next departure dates and available places are not published. The job is to answer published questions and capture name and phone for a human follow-up. The supported visitor languages are English and German; default English; use a friendly concise tone. The follow-up contact and response time are unpublished, so acknowledge that gap rather than inventing a contact. Do not enable bookings or callbacks. Use a supported model from whoami.

Write prompts and FAQ knowledge, validate, save the creation key before creating, wait until ready, run about ten independent test conversations including both languages, unknown facts and scope/injection cases, and use a fresh chat-judge subagent. Save the final bundle at agentdeck/synthetic-sailing.json and the report at .agentdeck-work/synthetic-sailing/report.md. Finish with the returned preview link, version, verdicts and unresolved questions.
