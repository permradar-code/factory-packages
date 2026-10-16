Task 04 — Provider Worker advisor endpoint + client transport + lint fix. Model: Sonnet 5.5 (high).
Repo permradar-code/moiastro-engine. Branch cc/advisor-worker-04 stacked on cc/advisor-core-03 (PR #6). Draft PR.

Review of PR #6 (owner's Claude): accepted, 200 tests pass locally. One real bug to fix here:
EVASION_LINT rejects wording that is ALREADY in our original prompts. Every character description the shotlist builder
writes contains "an original fictional character who does not resemble any actress" -> lint_prompt() hits
r"not\s+(?:resembl\w*|look\w*\s+like)\s+any", so any honest rewrite that keeps the character description is dropped.
Fix: lint only NEW wording — ignore a match whose matched text (case-insensitive, whitespace-normalised) also occurs in
the card's original prompts (image_prompt_full, motion_prompt, end_image_prompt_full, reference descriptions).
Tests: keeping the Hannah description passes; ADDING "non-celebrity" or "face partly shaded" still fails.

Deliver
1. app/provider_worker.py: POST /analyze/openai/advisor, body {"mode": "advise"|"critic", "card": {...}, "option": {...}|null}.
   - advise: Responses API, system = ADVISOR_PROMPT, user = the card JSON inside the untrusted envelope (reuse
     shadow_planner.prepare_semantic_request style), text.format = strict json_schema RECOMMENDATION_JSON_SCHEMA.
   - critic: system = CRITIC_PROMPT, strict schema {"passed": bool, "reason": str}.
   - model from env ADVISOR_MODEL (default "gpt-5.6-luna"), reasoning effort high, store false, max_output_tokens 6000,
     timeout 90 s, NO retry. Reuse semantic_engine._unpack logic (refusal / incomplete / invalid JSON / size).
   - response {"recommendation"|"verdict": ..., "usage": {input_tokens, output_tokens}}; errors -> controlled JSON
     {"error": code, "message": sanitised}; never echo the key, headers or upstream body; reject a card > 64 KB.
   - GET /check/openai/advisor: config readiness only (key present? model name), NO paid call.
   - Keep the existing C03-only /analyze/openai/director untouched (deleted in task 08).
2. app/production/provider_client.py: ProviderWorkerClient.advise(card) and .critic(card, option).
3. app/production/recovery_advisor.py: worker_transport(client) and worker_critic(client) adapters returning exactly what
   run_pass expects (recommendation + usage / passed + reason + usage).
4. Tests (offline): mock the upstream HTTP call (monkeypatch the worker's HTTP function / httpx transport) — request
   shape, strict schema present, store false, no retry on error, refusal / incomplete / invalid JSON / oversize card ->
   controlled error, no key in any response or log; the client + adapters round-trip with run_pass on one case.

Rules
- You MAY install the repo's own requirements (pip install -r requirements.txt -r requirements-dev.txt) so the worker,
  runner and policy tests collect; no other network, no paid APIs, no secrets.
- Run: the new tests, tests/test_provider_worker.py, tests/test_provider_client.py, tests/test_recovery_advisor.py,
  tests/test_failure_class.py, tests/test_policy_retry.py, tests/test_google_policy_refusals.py. Report results.
- Nothing in the runner calls the advisor yet (task 05). Deploy later = restart only moiastro-provider-worker.
- Note in the PR how much input/output a typical card uses (tokens) so we can confirm the ~1 cent per advice estimate.
