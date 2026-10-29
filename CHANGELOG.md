# Changelog

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
