---
type: llm
focus:
  source: file
  path: .agentdeck-work/synthetic-customer/create.json
---
PASS only if the persisted creation state contains environment dev, tenantId 00000000-0000-4000-8000-000000000222, a nonempty idempotencyKey, and a createBundleHash. FAIL if the workspace is missing, belongs to another customer, or a credential is embedded.
