Task 06 — owner controls for the advisor: MCP tools + Studio block. Model: Sonnet 5.5 (high) is enough (Opus also fine).
Repo permradar-code/moiastro-engine. Branch cc/advisor-controls-06 stacked on cc/advisor-runner-05 (PR #8). Draft PR.
Review of PR #8 (owner's Claude): accepted; 363 tests pass locally (runner, fallbacks, policy, export, advisor, worker).

The owner drives the factory through MCP (via his Claude chat) and reviews in Studio. Add:

1. MCP tools (same pattern as app/mcp_montage_assets_tools_v2.py, registered in mcp_server.py; Russian-friendly short output):
   - film_recovery_policy(project_id, changes_json="") -> read / set montage/recovery/policy.json (validated; e.g.
     {"enabled": true, "regen_budget_usd_per_film": 6}); shows effective caps and ledger totals (calls, tokens, text $, regen $).
   - film_recovery_cards(project_id, status="") -> per asset: shot, class, what was tried, status
     (OPEN/AWAITING_OWNER/SKIPPED_WITH_OPTIONS/EXHAUSTED/final_blocked), ranked options with factory-priced cost, diagnosis,
     and for a retell the proposed prompt + what changes on screen.
   - film_recovery_decide(project_id, asset_id, decision, option_rank=0) where decision in
     apply_option | approve_retell | approve_skip | rerequest | keep_skipped. Respects caps; refuses with a clear reason.
     After a decision that re-queues work, say that a factory run (film_resume / the existing run tool) is needed — or
     trigger it the same way the existing tools do, if that is the established pattern.
   - Include these in the MCP tool list docs (docs/edit_v2.md or a new docs/recovery_advisor.md, 1 page, RU summary on top).
2. Studio: on the existing asset card (NEEDS_MANUAL / SKIPPED by recovery_advisor) a «Совет режиссёра» block — diagnosis,
   ranked options with cost, buttons Применить / Одобрить пересказ / Пропустить / Спросить заново, calling new Studio endpoints
   that wrap the same functions. Keep it small; reuse montage.js patterns. The old «Восстановление» tab stays until task 08.
3. Export message: film_export / the review page show the D5 blocked list in Russian ("Финальная выгрузка заблокирована:
   сцены C13, C18 с репликами пропущены в черновике — одобрите пропуск или загрузите свой клип").

Tests: MCP tools with a temp project (policy read/write/validation, cards listing, each decision path, caps refusal);
Studio endpoints (happy path + refusal); no network. Run them + test_advisor_runner.py, test_recovery_advisor.py,
test_studio.py, test_montage_operator_ui.py, test_mcp_video_tools.py. Report results.

Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/.
Deploy later = restart moiastro-studio + moiastro-mcp (+ provider-worker for task 04).
At the end of the PR description add a short DEPLOY section: the exact git commands to bring the whole stack
(#4..#9) onto backup/server-state-20261015 on the VPS as user moiastro, the services to restart, and a read-only smoke check
(GET /check/openai/advisor via the worker, film_recovery_policy on a test project).
