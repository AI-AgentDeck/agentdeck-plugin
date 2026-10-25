---
type: llm
focus:
  source: file
  path: agentdeck/synthetic-dental.json
---
PASS if the id-free AgentDeck bundle is for the requested synthetic business, has useful behavior prompts and FAQ knowledge grounded in the complete approved operator brief below, and preserves its languages and action boundaries. Put changing business facts in knowledge. FAIL on an invented price, contact, date, availability or guarantee, an unrelated business, or embedded credentials/agent IDs. Missing contact details or response times must remain explicit gaps. The supplied source URL is approved provenance. This grader checks grounding; the reduced mock does not establish real backend schema validity.

Approved operator brief:

The approved complete source is this brief, associated with https://synthetic-dental.example/. An examination costs 37 EUR. Opening hours are Monday to Friday 09:00–17:00. Insurance coverage is not published. The job is to answer published questions and capture name and phone for a human follow-up. The supported visitor languages are English and German; default English; use a friendly concise tone. The follow-up contact and response time are unpublished, so acknowledge that gap rather than inventing a contact. Do not enable bookings or callbacks. Use a supported model from whoami.
