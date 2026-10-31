# Changelog

## 0.5.0

- Claude Code connects by signing in instead of a pasted token. The `token` option and the static
  Authorization header are gone. After upgrading, run `/mcp` → `agentdeck` → **Authenticate** once
  and choose **Allow** in the browser.
- The workflow guidance (create, prompt design, industry patterns, test, evaluation, update, go-live
  and the server's rules) is now served by the AgentDeck server through `get_guide`, so every app
  connected to it gets the same rules. The skills call `whoami` and the guide, and keep only what is
  specific to Claude Code and Codex: the connection, `bundle.py`, local files and the independent
  judge, which is used in addition to the guide's checklist. A server without `guideVersion` is
  reported as needing an update.
- Removed `references/prompt-design.md`, `industry-patterns.md`, `evaluation.md`,
  `backend-contract.md` and `publishing.md`, and `scripts/configure_plugin.py`.
- Live acceptance runs on a copy made by `scripts/prepare_eval_plugin.py`, whose header reads
  `EVAL_AGENTDECK_TOKEN`; an evaluation cannot sign in through a browser.
- Codex connects by signing in too: run `codex mcp login agentdeck` once (or the launcher with
  `--login`). The packaged connection no longer reads `AGENTDECK_TOKEN`; the launcher's
  `--token-file` and `--token-env` remain for scripts, and its hidden token prompt is gone.

## 0.4.2

- The environment setting no longer carries an `options` list, which Claude Code 2.1.251 refuses at
  install (`userConfig.mcp_url: Unrecognized key: "options"`). Its description names the three URLs.

## 0.4.1

- Repository rules: `main` takes pull requests from `dev` only (`main only from dev` check).

## 0.4.0 — unreleased

- Agents are PREPARING, then READY; the TEST and LIVE stages are gone. A READY agent answers wherever
  its snippet is placed, and `go-live` hands over the snippet and channel steps instead of blocking.
- Live acceptance is a manual workflow; release pull requests require only `validate`.

## 0.2.0 — unreleased

- Customer workspace creation using backend capabilities and tenant-scoped tokens.
- Customer connection instructions and workspace-bound local creation keys.

## 0.1.0 — unreleased

- Claude Code marketplace and create, update, test and go-live skills.
- Independent conversation judge and source-grounded acceptance checklist.
- Portable bundle persistence with stable local idempotency keys.
- Admin token creation and secure plugin configuration helpers.
- Mock workflow evaluations and a separate five-industry live acceptance gate.
- Explicit handling of publishing, per-upload readiness and console-edit concurrency gaps.
