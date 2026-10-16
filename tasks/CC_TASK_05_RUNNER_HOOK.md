Task 05 — wire the advisor into the factory runner (opt-in per project). Model: Opus 5.5.
Repo permradar-code/moiastro-engine. Branch cc/advisor-runner-05 stacked on cc/advisor-worker-04 (PR #7). Draft PR.
Review of PR #7 (owner's Claude): accepted; 271 tests pass locally in a venv with the repo requirements.

Goal: one failed shot never stops a film. With montage/recovery/policy.json {"enabled": true} the runner calls
recovery_advisor.run_pass (worker_transport / worker_critic) for terminal assets and EXECUTES the directive through its
normal paths; without policy.json (or enabled:false) behaviour is byte-identical to today (audit §4.2 row 5, §5 #11-12).

Deliver
1. Runner hook (montage_assets_runner.py), after the video stage, before source_blockers: run_pass -> for each applied
   directive re-enter the idempotent runner (max_rounds cap). Executors:
   - retry_same: re-queue the asset with the same request (attempts +1);
   - ingredients_mode: the existing ingredients_fast path (no start frame, reference images);
   - new_start_frame: regenerate image:<shot> (same image prompt), then the video;
   - switch_provider: per-shot provider override (Veo, allowed durations 4/6/8);
   - rewrite_prompt: project-local montage/recovery/overrides.json read by _shot_override BEFORE the repo-level
     shot_overrides.json (only after owner approval when it is a policy retell, D2);
   - still_under_narration: skip the video, add img:<shot> to the narration row visuals via the existing
     edit_overrides mechanism (film_edit_set rows.<id>.visuals); merge_with_neighbour / drop_shot / exhausted -> skip
     via asset_ops.skip_asset(skipped_by="recovery_advisor") with metadata.recovery merged (never replaced).
   Spend: every regeneration goes through the normal spend accounting and the advisor ledger; caps from policy.json.
2. D5 enforcement: film_export (and the final QC verdict) refuse while recovery_advisor.final_export_blocked() is non-empty,
   with a clear Russian+English message listing the shots; approve_skip() clears it. Draft render is allowed.
3. Telegram: one montage_notify event per needs_owner / awaiting-approval card (short, Russian), no spam on re-runs.
4. Bug fix found in task 04 (separate commit, applies to ALL projects): the runner's _is_video_safety_block misses six
   refusal wordings (incl. the real B06 text without HTTP status), so the Omni -> Veo ladder never starts. Make it use
   failure_class.classify (policy_refusal confirmed OR suspected -> treat as a safety block). Same for the
   provider_errors kind used by _attempt, so such failures are not 'permanent' after one try. Keep every existing test green;
   add tests for the six wordings.

Tests (offline, venv with repo requirements)
- audit §5 #11 and #12: FakeClient run, one shot fails permanently, ten succeed -> with advisor on: retry/ingredients
  executed through _attempt, then exhaustion -> run reaches AWAITING_RENDER / montage_ready (not PREPARED_WITH_GAPS), edit
  plan builds without the clip, QC lists it; dialogue shot -> draft OK, export refused until approve_skip;
  advisor off -> all existing runner tests unchanged, transport never called.
- a rewrite_prompt override is picked up by _shot_override on the next attempt; still_under_narration adds the still.
- crash between reserve and answer -> no second paid call after restart.
- Run: new tests + test_montage_assets_runner.py, test_fallbacks.py, test_policy_retry.py, test_edit_v2_*.py,
  test_film_review_export.py, test_recovery_advisor.py, test_advisor_worker.py, test_failure_class.py. Report results.

Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/. Studio UI and MCP tools are
task 06 (keep this PR to the runner, export, QC, notify). Deploy later = restart moiastro-studio + moiastro-provider-worker.
