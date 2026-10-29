---
max_turns: 10
runs: 1
timeout_seconds: 120
allowed_tools: [Read, Glob, Grep, Skill]
tags: [mock, environment]
---
Create a new AgentDeck agent in DEV only for a synthetic club, using the existing connection. The server identity must match dev before any write. If it does not, stop and tell me what is wrong.
