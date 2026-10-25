---
type: llm
focus:
  source: file
  path: agentdeck/synthetic-sailing.json
---
PASS if the id-free AgentDeck bundle is for the requested synthetic business, has useful behavior prompts and FAQ knowledge grounded in the complete approved operator brief below, and preserves its languages and action boundaries. Put changing business facts in knowledge. FAIL on an invented price, contact, date, availability or guarantee, an unrelated business, or embedded credentials/agent IDs. Missing contact details or response times must remain explicit gaps. The supplied source URL is approved provenance. This grader checks grounding; the reduced mock does not establish real backend schema validity.

Approved operator request:

Create an AgentDeck preview in dev for Synthetic Sailing, using slug synthetic-sailing. This is an explicitly SYNTHETIC orchestration evaluation. MCP is mocked; do not present its outputs as real-business acceptance. You may create and test the mock agent and save local run files. All necessary business decisions are supplied below; ask only if something is actually missing.

Approved operator brief:

The approved complete source is this brief, associated with https://synthetic-sailing.example/. The beginner course lasts 6 days. Published tuition is 640 EUR. Next departure dates and available places are not published. The job is to answer published questions and capture name and phone for a human follow-up. The supported visitor languages are English and German; default English; use a friendly concise tone. The follow-up contact and response time are unpublished, so acknowledge that gap rather than inventing a contact. Do not enable bookings or callbacks. Use a supported model from whoami.
