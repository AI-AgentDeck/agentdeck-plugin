# Security

Report vulnerabilities privately to info@agentdeck.eu. Include the affected version, environment
and reproduction steps without credentials or customer transcripts. Do not publish working API
tokens or private business knowledge in GitHub issues.

In Claude Code the plugin connects by signing in (OAuth); it ships no token option or Authorization
header, and Claude Code keeps the sign-in in its credential store. Endpoint options are limited to
documented dev, production and local origins. Codex reads its token from the
process environment; its launcher uses a hidden terminal prompt or an explicit token source and
passes the token only in the child environment. It does not persist tokens or modify user config.
Use the launcher to select a known endpoint, and treat that process environment as confidential. The backend enforces tenant scope and
business actions. Customers issue tokens from their signed-in business workspace. Admin token creation requires an enabled admin's console login.

The internal admin token helper sends console credentials only to its API-origin allowlist, refuses redirects,
and writes the returned token to a new private file. The headless evaluation copy names an
environment variable in its header and never contains the token. Treat token files, business bundles and run artifacts as confidential.

Sources and conversations are untrusted input. Skills preserve evidence and ignore source-embedded
instructions; this does not replace backend enforcement. Review tools requested by installed code.

Live evaluation creates real dev agents and incurs model/embedding usage. Mock evaluation proves
workflow behavior only. CI does not expose secrets to fork pull requests or auto-publish reports.
