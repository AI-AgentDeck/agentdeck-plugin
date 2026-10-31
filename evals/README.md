# Plugin evaluations

The package contains two separate native `claude plugin eval` suites. Model calls in both use
your Claude account or API credentials. Only the live suite also creates real dev agents and
uses AgentDeck's embedding/chat budget. Cost estimates from Claude do not include backend calls.

## Mock orchestration

`plugins/agentdeck/evals/` substitutes the MCP server. Its cases cover authentication, environment
selection, preparing blockers, the publishing handover and complete creation flows for five synthetic industries.
The mock server is deliberately reduced; it does not implement real schema validation or real
agent reasoning. Its conversations cannot establish factual quality of a deployed business agent.

```sh
claude plugin eval ./plugins/agentdeck --runs 1 --ablation none --trust-plugin --no-publish --max-cost-usd 10 --allow-tools Write Edit "Bash(python3 *)"
```

The read-only cases need no extra grants. Creation cases use Write/Edit, the bundled Python helper
and a read-only judge subagent. Start with `--case create-dental` while iterating. Each case has
explicit wall-clock and turn limits; the cost ceiling stops additional runs, with a small possible
overrun from a run already in flight. Default multi-run and baseline evaluation can be used later
to assess reliability and the skill's contribution.

Do not use `--mocks off` for this suite. Keep reports local; generated reports and transcripts are
gitignored. If the engine is disabled server-side, document that the behavioral suite was not run;
schema validation is not a substitute.

## Live acceptance on dev

`plugins/agentdeck/evals-live/` uses real MCP tools. Sites are
public references from existing industry examples: Dental Angels, AR KFZ, Padelclub Plattling,
Norinohi and Schmidt & Schmidt document services. The legal case is document services rather than
a law firm. No unpublished customer prompt or knowledge file is copied into the plugin.

Each evaluation run gets a fresh Claude config directory, so a browser sign-in does not carry
over, and only `EVAL_*` variables from your shell reach it. So the live suite runs on a copy of the
plugin whose MCP header reads `EVAL_AGENTDECK_TOKEN`. First deploy the backend MCP branch and issue
an environment-specific admin token ([internal setup](../docs/internal-setup.md)). Then:

```sh
python3 scripts/prepare_eval_plugin.py --environment dev --output /tmp/agentdeck-eval
read -rs EVAL_AGENTDECK_TOKEN && export EVAL_AGENTDECK_TOKEN   # paste the adk_ token; it is not echoed
claude plugin eval /tmp/agentdeck-eval --eval-dir evals-live --mocks off --runs 1 --ablation none --trust-plugin --no-publish --max-cost-usd 20 --allow-tools Write Edit "Bash(python3 *)" "WebFetch(domain:dentalangels.hu)" "WebFetch(domain:ar-kfz-technik.e-m-ritter.chatgpt.site)" "WebFetch(domain:padelclub-plattling.de)" "WebFetch(domain:www.padelclub-plattling.de)" "WebFetch(domain:norinohi.com)" "WebFetch(domain:www.norinohi.com)" "WebFetch(domain:schmidt-export.com)" "WebFetch(domain:www.schmidt-export.com)" "mcp__plugin_agentdeck_agentdeck__*"
```

Use `--case dental` for the first live smoke test. Ten or more independent chats per agent are
required; each language, grounding, unknown facts and action boundaries are judged. Correctly
stopping on a missing sign-in or failed crawl still fails live acceptance: it did not prove a working
agent. Do not retry the whole suite blindly: it creates up to five new tenants per run and consumes
daily create limits. Reuse the private creation state/IDs when resuming an interrupted case.

Upload files are additional promotion artifacts; bundle-only equality does not cover uploaded
binaries or environment connections. Review a second-environment import separately before claiming
cross-environment equivalence. Go-live is a handover of the snippet and channel steps; there is no activation operation.

## CI and release gate

Offline validation and helper tests run without credentials, and `validate` is the check main
requires. Live acceptance against dev is started by hand from dev (Actions → live-acceptance). It
needs an `ANTHROPIC_API_KEY` and an `AGENTDECK_EVAL_TOKEN` in the protected GitHub environment
`dev-evaluations`; until those exist it stops at its first step without running anything. It
prepares the token-reading copy above and passes the secret as `EVAL_AGENTDECK_TOKEN`.

The workflow refuses missing secrets instead of treating a skipped evaluation as success. It does
not publish reports or automatically merge a release. CI reports remain on its ephemeral runner;
repeat locally for private retained reports. Do not upload traces as artifacts of this public repo:
they can contain business facts, created IDs and transcripts. The initial package remains on dev until the real
gate has passed.
