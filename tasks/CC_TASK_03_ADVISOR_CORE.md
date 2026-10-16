# Claude Code task 03 — Recovery Advisor, pure core (not wired into the factory yet)

Repo `permradar-code/moiastro-engine`. New branch `cc/advisor-core-03`, stacked on `cc/failure-class-02` (PR #5).
Draft PR into `backup/server-state-20261015`. Suggested model: **Opus 5.5** (this is the core of the design).

## Review of PR #5 (owner's Claude)
Accepted. 133 tests pass locally. Two gaps, because the owner's paste of task 02 was cut off — fix them in this PR:
1. Add the second REAL Google sample to `tests/test_failure_class.py`:
   `"Request blocked for an unspecified policy reason. Please modify your input and retry."` (shots C78 and H06 of film 4)
   → `policy_refusal`, suspected, scope `unspecified` (the classifier already does this; just pin it with a test).
2. Record in the audit doc (§3.2 / §4.3) the evidence that was cut off:
   - C78 (Hannah pours gold coins on a bank counter, has dialogue): original, soften_action, camera_change and face_clause
     (new start frame) were ALL refused; `ingredients_fast` (no start frame, reference images only) succeeded.
   - H06 (a man walks in and speaks to the bank manager): original refused, soften_action succeeded.
   - B06 (innocent wide fair shot): "input could not be submitted" → ingredients shortcut succeeded.
   - Ten shots (B01, C13, C15, C18, C37, C60, C73, B07, H02, H05) are READY with `attempts=2`, no `policy_variants`, no manual
     upload: most likely refused once, then passed on a later plain re-run (Resume/redo). Confirm from the code what
     `attempts=2` without variants means and say so in the doc.
   - Conclusion: on this provider many refusals are **not stable** (innocent scenes refused; a plain re-run or dropping the
     start frame passes). Cheap mechanical steps must come **before** any story change.

## Deliver (pure; nothing in the factory imports it yet)
`app/production/recovery_advisor.py` (+ `app/production/recovery_advisor_schemas.py` if it keeps files < ~400 lines each),
following audit §4.2–4.7 and §4.9, with these changes:

1. **Action enum** (card `allowed_actions`, recommendation `options[].action`), in fixed preference order:
   `retry_same < ingredients_mode < new_start_frame < switch_provider < rewrite_prompt < still_under_narration <
   merge_with_neighbour < drop_shot < needs_owner`.
   - `retry_same` = the same request once more; `ingredients_mode` = no start frame, reference images only;
     `new_start_frame` = regenerate the first-frame image from the same image prompt.
   - `allowed_actions` excludes what was already tried for this asset (read the asset's `policy_variants` / policy log and
     the advisor rounds), e.g. no `ingredients_mode` if `ingredients_fast` already ran and failed.
2. **Deterministic pre-steps, no model call**: for `suspected` (not confirmed) policy refusals, `output_defect` and `unknown`,
   `run_pass` first proposes `retry_same` (once per asset) and then `ingredients_mode` (if not yet tried) **without calling
   OpenAI**. Only when these are exhausted does it build a card for the model. Confirmed policy refusals skip `retry_same`
   but may still use `ingredients_mode` / `new_start_frame` before the model. These steps are not story changes and may
   auto-apply within the caps (D2 applies only to model-proposed retells).
3. **No-evasion gate** exactly as audit §4.5 rule 5 (honesty flags + lexical lint + critic for confirmed-refusal retells).
   Note: the factory's own `policy_retry` texts (D1) must NOT be reused by the advisor.
4. **D5**: for a dialogue shot, exhaustion → `SKIPPED` for the **draft** render with `metadata.recovery.final_blocked = true`
   and `needs_owner`; a helper `final_export_blocked(project) -> list[asset_id]` that task 05/06 will use in export/QC.
   Non-dialogue shots: `SKIPPED_WITH_OPTIONS`, export allowed.
5. **Transport** is an injected callable (`advise(card) -> dict`), so this PR needs no network and no Provider Worker change
   (that is task 04). Ship a `FakeAdvisorTransport` in tests.
6. **Storage / ledger / idempotency** exactly as audit §4.6–4.7 (`montage/recovery/…`, RESERVED → ANSWERED/INTERRUPTED/FAILED,
   atomic 0600 writes, no automatic re-request of an INTERRUPTED round). Caps from `policy.json`, default `enabled: false`;
   `text_budget_usd_per_film` default 2.0 with prices input $0.20 / output $1.20 per Mtok (D3), counted from returned usage.
7. `PROMPT_VERSION = "advisor-1"`; put the draft prompt from audit §4.9 in the module, updated for the new actions and the
   rule "try mechanical steps first; a story change is the last resort before still/merge/drop".
8. Confirm the card field names against `montage_assets_contract.py` / `montage_input.json` shape before freezing the schema
   (audit §4.4 note); include the narration block text around the shot and the shot's timeline role.

## Tests (offline; run only these + `tests/test_failure_class.py`)
`tests/test_recovery_advisor.py`: audit §5 cases #1, #2, #4–#10, plus:
- pre-steps: a suspected refusal → first pass proposes `retry_same` with **0** transport calls; second failure →
  `ingredients_mode`, 0 calls; third → card + 1 transport call;
- `allowed_actions` excludes already-tried variants (use a C78-like record whose policy_variants list original/soften/camera/
  face_clause refused and ingredients_fast not yet tried → next = `ingredients_mode`);
- D5: dialogue shot exhausted → draft skip + `final_blocked`, `final_export_blocked()` lists it; non-dialogue → export allowed;
- fixtures: the 13 film-4 cases (synthetic, documented) + a small synthetic non-western project `tests/fixtures/recovery_lighthouse_v1/`
  (6 shots, one 9:16, one dialogue shot, one run with `language: "ru"`, ids not starting with C/B).

## Rules
- Not imported by any production module; no change to runner, provider_worker, policy_retry, Studio, MCP.
- No network, no paid APIs, no secrets, no package installs (if `httpx` is missing, keep the module free of it).
- Update the audit doc §6 (task list) if the plan changes; keep the Russian summary at the top current (2–3 lines added).
