# Claude Code task 01 — Recovery Director audit + advisor design (no production changes)

Repository: `permradar-code/moiastro-engine`. Base branch: `backup/server-state-20261015` (HEAD `b96e9d6` or later —
this branch IS the live VPS code). Work in a new branch `cc/recovery-audit-01`, open a PR into
`backup/server-state-20261015`. Do not merge.

## Context
MOIASTRO is an AI film factory (Old West films for the YouTube channel Tales of Cedar Bluff): script → shotlist →
reference images → images → videos (Google Vertex Omni / Veo via `app/provider_worker.py`) → dialogue alignment →
narrator → music → edit engine v2 (`app/production/edit_v2/`) → QC → Shorts / thumbnails → YouTube upload.
Asset generation and retries: `app/production/montage_assets_runner.py`, `policy_retry.py`, `provider_errors.py`,
`asset_ops.py`, `generator.py`.

On 11–12 Oct ChatGPT/Codex added a "Recovery Director" (`app/recovery_shadow/*`, `app/production/scene_director.py`,
`scene_edit_recipe.py`, `app/mcp_recovery_tools.py`, `app/montage_recovery_preview_api.py`, `ops/moiastro-recovery*.service`,
`ops/install_recovery_*.sh`, ~60 `tests/test_recovery_*`). Its own design note (summary): failure collector →
diagnostic classifier (POLICY_REJECTION / CAPACITY / TRANSIENT_NETWORK / INVALID_REQUEST / MISSING_DEPENDENCY /
QUALITY_FAILURE / UNKNOWN) → story contract (GPT, `semantic_engine.py`) → strategy generator → cost/feasibility →
independent critic → policy gate → executor (not built) → media QC (not built). It admitted: the endpoint is C03-only,
`scene_director.py` splits actions by `;` (wrong), no executor integration.
What went wrong in practice: Recovery generated and assembled film 4 **outside** the factory (its own ffmpeg glue of 151
files), so the factory's edit engine never ran.

## The owner's target design (what Recovery must become)
Recovery = an **advisor only**. The factory owns every generation, retry and edit.
1. A factory asset fails (policy refusal, provider error, later: a QC failure such as a cut line, a face/identity drift,
   a repeated take). The factory writes a *failure card*: project, shot id, the scene's script excerpt + neighbours,
   image/motion prompt, references, error class + safe diagnostics, attempts so far, format/duration.
2. The advisor (OpenAI Responses API, existing key; model and prompts as in `semantic_engine.py`) reads the card
   **in the sense of the script** and returns a strict-JSON recommendation, ranked:
   `rewrite_prompt` (new image/motion prompt that keeps every story event and line) · `switch_provider` (Veo) ·
   `still_under_narration` · `merge_with_neighbour` · `drop_shot` · `needs_owner`, each with a reason and
   cost estimate. Never prompts that hide content from a safety filter; a confirmed policy refusal may only be retold
   honestly in another way, otherwise `needs_owner`.
3. The factory validates the recommendation (schema, per-shot attempt cap, per-film budget cap) and re-runs the asset
   through its normal path; if attempts are exhausted the asset is marked SKIPPED-with-options for the owner and the
   rest of the film continues (one failed shot must never block the edit).

## Task 01 (this PR): audit + design, **no behaviour change**
Deliver `docs/RECOVERY_AUDIT_2026-10.md` containing:
1. **Inventory** of every Recovery file: purpose, entry points (HTTP servers v1/v2/v3, MCP tools, Studio routes), which
   call OpenAI or Google (paid), which write to project files, which are C03/western-specific, which are dead/duplicate.
   Table: file → keep / reuse in advisor / delete later, with reason.
2. **All model prompts** used by Recovery (`_EXTRACTION_POLICY`, `_CRITIC_POLICY`, scene_director prompts, any others),
   quoted, with a short critique: what is good, what is missing for the advisor role (e.g. the script context, the
   channel's no-evasion rule, ranking of options).
3. **Today's failure path in the factory**: how a refused/failed asset flows through `montage_assets_runner.py`,
   `policy_retry.py` (soften_action / camera_change / face_clause variants), `provider_errors.py`, and why film 4 ended
   with `error_kind=permanent, attempts=1` and a blocked final render (`source_blockers`, `PREPARED_WITH_GAPS`).
4. **Advisor design**: module layout (proposal: `app/production/recovery_advisor.py` + one hook in the runner),
   failure-card JSON schema, recommendation JSON schema, where cards/recommendations are stored in the project
   (e.g. `montage/recovery/<asset>.json`), caps and budget, idempotency (no double paid calls on reconnect),
   how the owner sees `needs_owner` cases (MCP tool + Studio), what happens to the old Recovery services/routes.
5. **Test plan**: offline tests with mocked OpenAI responses, using `tests/recovery_director_cases_13.json`
   (the 13 real film-4 failures) + one synthetic non-western project; the factory must keep rendering when one shot
   stays failed.
6. **Step list** for task 02+ (small, reversible patches, each with tests), and anything the owner must do on the VPS.

## Rules
- Read code; you may run the existing test suite (`python -m pytest -q`), but **no network calls, no paid APIs, no secrets**
  (never print or commit keys/tokens; `.env` and credentials are not in the repo — do not look for them).
- Do not modify production code in this PR — only add the doc (and, if useful, a read-only script under `tools/` that
  prints the inventory). Do not touch `web/studio/reviews/`, OAuth, MCP auth or systemd units.
- Write the doc in English, concise, tables where possible; add a 10-line Russian summary at the top for the owner.
- If something cannot be determined from the repo (e.g. which services are actually running on the VPS), say so and
  list the exact read-only command the owner should run.
