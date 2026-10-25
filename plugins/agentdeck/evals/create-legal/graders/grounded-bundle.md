---
type: llm
focus:
  source: file
  path: agentdeck/synthetic-legal.json
---
PASS if this is an id-free AgentDeck bundle for Synthetic Documents, with useful behavior prompts and FAQ knowledge grounded in these approved synthetic facts: The published document-review fee is 83 EUR. Official authority fees are separate and not published. No completion deadline or legal outcome is guaranteed. Facts such as prices and schedules belong in knowledge, not behavior prompts. The absence of a contact or deadline must not be replaced by an invented value. FAIL on an invented price, contact, date, availability or guarantee, an unrelated business, or embedded credentials/agent IDs.
