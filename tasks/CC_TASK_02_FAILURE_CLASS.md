# Claude Code task 02 — one shared failure classifier (`failure_class.py`), no callers changed

Repo `permradar-code/moiastro-engine`. Base: `backup/server-state-20261015`. New branch `cc/failure-class-02`
(you may branch from `cc/recovery-audit-01` so the audit doc is there). Draft PR into `backup/server-state-20261015`.
Suggested model: Sonnet 5.5 (high) is enough — small, pure module.

Follow `docs/RECOVERY_AUDIT_2026-10.md` §3.4, §4.2 (row `failure_class.py`), §5 case #3, §6 task 02. Review of the audit
by the owner's Claude: accepted as written; additions below.

## Deliver
1. `app/production/failure_class.py` — pure, stdlib only, no I/O:
   - `classify(source) -> FailureInfo` where `source` is a `ProviderError`, a `ProviderWorkerClientError`, any exception,
     or a stored asset record (`dict` from `assets_state.json`: `status/error_kind/error/attempts/metadata`).
   - `FailureInfo` (frozen dataclass, `to_dict()`): `cls` ∈ `policy_refusal | capacity | transient | auth | invalid_request |
     missing_dependency | output_defect | qc_failure | unknown`; `confirmed_policy_refusal: bool` (**structured signals only**:
     `safety_reason`, `finish_reason`, Google status / RAI fields, `kind == "safety"` from `provider_errors`);
     `suspected_policy_refusal: bool` (text match only); `retryable: bool`; `provider_kind`, `http_status`, `safety_reason`
     (may be None); `message` sanitised with the existing `provider_errors.sanitize_message` (≤240 chars, no URLs/tokens/paths).
   - One phrase table = the **union** of the five existing lists (§3.4), each phrase tagged with where it came from, so a later
     task can switch callers without losing any wording. A text match sets `suspected_policy_refusal`, never `confirmed`.
   - "no inline video" / empty Veo output → `output_defect`; quota/429/RESOURCE_EXHAUSTED → `capacity`; timeouts/5xx/connection →
     `transient`; 401/403/credentials → `auth`; 400 on duration/size/format → `invalid_request`; missing image/reference/audio →
     `missing_dependency`.
2. `tests/test_failure_class.py` — offline, stdlib + pytest only (must collect without `httpx`; if importing
   `provider_errors` pulls `httpx`, keep the classifier free of that import and copy only `sanitize_message` logic or import it lazily):
   - a table of ≥30 sample inputs (exceptions and stored records, incl. the wordings from §3.2 row 1: "prominent individual",
     "usage guidelines", "support code", "sensitive words", "Responsible AI practices", "filtered output", "no inline video",
     429, 503, timeout, 401, "duration must be", missing reference) → expected class/flags;
   - one parametrised test built from `tests/recovery_director_cases_13.json` (synthetic failures per case, documented as synthetic);
   - a test that prints/asserts the **divergence table**: for each sample, what each of the 5 old classifiers says today vs the new one
     (call the old functions only if they import without `httpx`; otherwise mark "not importable here" — do not install packages);
   - a secrets test: a message containing `sk-test…`, an `AIza…` key, a bearer token, a URL and `/opt/...` path comes out clean.
3. Append to the audit doc §3.4 a short "task 02 result" paragraph with the divergence table.

## Rules
- **Do not change any caller** (`provider_errors.py`, `montage_assets_runner.py`, `policy_retry.py`, `recovery_shadow/*`) in this PR.
- No network, no paid APIs, no secrets, no package installs. Do not touch systemd, OAuth, MCP auth, `web/studio/reviews/`.
- Run only the new tests plus `tests/test_google_policy_refusals.py` / `tests/test_policy_retry.py` if they collect.
- Keep the module < ~200 lines; clear names; short docstring at the top explaining confirmed vs suspected.

## Owner decisions (for task 03+, record them in the audit doc §7.2 in this PR)
- D1: leave `policy_retry` / Stagecoach safe prompts / C47 swap untouched until task 07; then decide.
- D2: policy-refusal retells need the owner's approval (first release).
- D3: `gpt-5.6-luna` list price ≈ $0.20 / Mtok input, $1.20 / Mtok output (public price lists, 15 Oct 2026; owner to confirm on
  OpenAI's pricing page). Text budget per film: $2 default.
- D4: first opt-in = a new small test project (a 2–3 minute Cedar Bluff mini-film), not film 4.
- D5: an exhausted **dialogue** shot is auto-skipped **for the draft render only** (the film must keep going), marked loudly in QC
  and in the Studio/Telegram `needs_owner` list; **final export stays blocked** until the owner decides (approve skip / upload /
  option). Non-dialogue shots: auto-skip with options, export allowed.
- D6: remove the 13 `recovery_*` MCP tools in task 08 (tentative — the owner confirms he no longer drives the factory from ChatGPT).

## Real data from the VPS (owner ran the §7.1 commands, 16 Oct) — use it in this PR
- Live Recovery unit = **v3** (`recovery_server_v3`, `RECOVERY_SEMANTIC_ENABLED=1`, session limit 3, `RECOVERY_VEO_ENABLED=1`,
  `RECOVERY_VEO_BUDGET_USD=10`). `veo_trials_reserved.json = {"reserved_usd": 8.0}`; `/var/lib/moiastro-recovery` = 312 MB.
- Key files: provider-worker and recovery load `providers.env`; studio loads `montage.env` + `telegram.env`; mcp only `telegram.env`.
  → confirms: the advisor's OpenAI call must go through the Provider Worker.
- Film 4 ran with `film.edit.engine = v2`, `policy_retry_max = 3`, `video_provider = google_vertex_omni`
  (`gemini-omni-1.1-flash-preview`); `montage/policy_log.json` exists (8.6 KB). So §3.2 step 3 did apply (the variant chain ran).
- No asset is FAILED/NEEDS_MANUAL any more (they were regenerated or skipped by hand), so the original error texts of the 13 cases
  are gone from `assets_state.json`. What survives (from `film_assets`, `policy_variants`) — **use these exact strings as real samples**:
  1. `"The input could not be submitted. This input contains content that violates Google's Responsible AI practices. If you think this was an error, send feedback."`
     — shot B06, an innocent wide shot ("the whole town at the rope line, wind snapping the bunting"); runner took the
     `input_refused: straight to ingredients` shortcut and **`ingredients_fast` (no start frame, reference images) succeeded**.
  2. `"Request blocked for an unspecified policy reason. Please modify your input and retry."`
     — shot C78 (Hannah pours gold coins on a bank counter, one line of dialogue): original, soften_action, camera_change and
     face_clause (new start frame) **all refused**; `ingredients_fast` (no start frame) **succeeded**.
     — shot H06 (a man walks in and speaks to the bank manager): original refused, `soften_action` succeeded.
  3. Ten shots (B01, C13, C15, C18, C37, C60, C73, B07, H02, H05) show `READY, attempts=2`, no `policy_variants`, no manual upload:
     refused on the first factory attempt, then **succeeded on a later plain re-run** (Resume / redo).
- Classifier consequences for this PR:
  - samples 1 and 2 → `cls = policy_refusal`. Add a field `refusal_scope ∈ {"input", "unspecified", "output", None}`
    ("input could not be submitted" → `input`); keep `confirmed_policy_refusal` for structured signals only and set
    `suspected_policy_refusal = True` for these texts.
  - record in the doc (for task 03): on this provider a refusal is often **not stable** — innocent scenes are refused, a plain
    re-run or ingredients mode (dropping the start frame) usually passes. The advisor ranking must therefore try, before any
    rewrite of the story: (a) one plain `retry_same`, (b) `ingredients_mode` (no start frame, reference images only),
    (c) `new_start_frame` (regenerate the first frame image), and only then an honest retell / still / drop.
    Add `retry_same`, `ingredients_mode`, `new_start_frame` to the planned action enum in §4.5 of the audit doc.
