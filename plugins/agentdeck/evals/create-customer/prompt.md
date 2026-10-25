---
max_turns: 90
runs: 1
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit, Bash]
tags: [mock, creation, industry]
---
Create an AgentDeck preview in dev for Synthetic Customer Dental, using slug synthetic-customer. This is an explicitly SYNTHETIC orchestration evaluation. MCP is mocked; do not present its outputs as real-business acceptance. You may create and test the mock agent and save local run files. All necessary business decisions are supplied below; ask only if something is actually missing.

The approved complete source is this brief, associated with https://synthetic-customer.example/. An examination costs 37 EUR. Opening hours are Monday to Friday 09:00–17:00. Insurance coverage is not published. The job is to answer published questions and capture name and phone for a human follow-up. The supported visitor languages are English and German; default English; use a friendly concise tone. The follow-up contact and response time are unpublished, so acknowledge that gap rather than inventing a contact. Do not enable bookings or callbacks. Use a supported model from whoami.

Write prompts and FAQ knowledge, validate, save the creation key before creating, wait until ready, run about ten independent test conversations including both languages, unknown facts and scope/injection cases, and use a fresh chat-judge subagent. Save the final bundle at agentdeck/synthetic-customer.json and the report at .agentdeck-work/synthetic-customer/report.md. Finish with the returned preview link, version, verdicts and unresolved questions.
