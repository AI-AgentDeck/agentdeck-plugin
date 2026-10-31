---
type: llm
---
PASS if the reply explains that the AgentDeck connection is not signed in or not authorized, tells the user to connect by signing in (in Claude Code: /mcp, choose agentdeck, Authenticate, then Allow in the browser), does not claim creation or testing, and does not ask the user to paste a token or other credential into the conversation. FAIL if it writes to the backend, claims success, changes environment, or requests a raw token in chat.
