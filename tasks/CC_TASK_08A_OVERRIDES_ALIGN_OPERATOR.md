Task 08A — prompt overrides without git, keep old videos, dialogue alignment fix, operator mode. Model: Sonnet 5.5 (high).
Repo permradar-code/moiastro-engine, base = origin/backup/server-state-20261015 (current VPS HEAD, incl. film 5 override
commits after 2a3c0ae). Branch cc/overrides-align-08a. Draft PR. Small separate commits per item. Offline tests only.

1. film_shot_override MCP tool (project-local, no git)
- Today prompt fixes go to app/production/shot_overrides.json in the code tree; each edit needs an owner git commit and the
  factory refuses to write when the file differs from HEAD. Task 05 added project-local montage/recovery/overrides.json read
  by _shot_override first — reuse it (or montage/shot_overrides.json next to it; one place, documented).
- film_shot_override(project_id, shot_id, changes_json="", clear=False): read / set / clear fields image_prompt_full,
  motion_prompt, references, duration_seconds (validated against the provider's allowed durations), notes. Show the
  effective prompt (base + override) and what will be invalidated (image -> video too; motion only -> video only).
  Optional apply=True marks the affected assets for regeneration the same way film_redo does (no spend by itself).
- Repo-level shot_overrides.json keeps working (lower priority). Migration helper: copy entries for one project from the
  repo file into the project file (dry-run by default).
- Tests: priority order, validation, duration override reaches the video request, clear, invalidation scope.

2. Never delete a finished video on redraw
- Regenerating image:<shot> (film_redo / recovery new_start_frame / review redo) today deletes the shot's video. Move it to
  projects/<pid>/keep/<shot>_v<N>.mp4 (+ small json: prompt hash, date, cost) instead; film_assets lists kept versions;
  film_edit_set can use a kept file as the clip source (e.g. "source": "keep:C01_v3").
- Tests: redo keeps the old file with increasing N; edit plan uses a kept source.

3. Dialogue alignment bug (app/production/film_render.py ~1320-1344)
- `usable` is False when result["duration"] is missing/0 or the last word ends > duration+0.1, so a 100%-matching
  transcript fails with "alignment missing". Fix: take duration from ffprobe of the clip audio when missing; allow boundary
  words to end up to +0.5 s past duration (clamp end to duration); drop only individually invalid words; fail only if
  usable words cover < 80% of the expected text. Keep the transcript-mismatch check as is.
- Tests: missing duration, last word past end, one bad word, real mismatch still fails.

4. Operator mode for external AIs (ChatGPT / Gemini / other chats that only RUN films)
- Env MOIASTRO_MCP_PROFILE=operator (default "full" = today, byte-identical tool list). In operator profile do not register:
  codex_*, patch_*, exec_*, git_diff, git_show, astro_git_status, code_search, repo_tree, file_read outside projects/ and
  the package repo, job_submit, render_existing, recovery_*_submit (old v3), notification_configure, youtube_comment_post/
  reply/moderate, youtube_video_update, youtube_thumbnail_set, youtube_publish (non-dry-run publish needs full profile).
  Keep film_*, montage_assets_*, project_*, provider_health, youtube read/analytics, youtube_publish_video(dry_run only).
- Put the allow-list in one file (app/mcp_profiles.py) with a test that every registered tool is classified.
- docs/operator_mode.md: how the owner would run a second MCP instance with this env on another port (example systemd
  unit in docs only — do NOT install or edit systemd/OAuth/MCP auth).

Run: new tests + test_montage_assets_runner.py, test_advisor_runner.py, test_film_review_export.py, test_mcp_video_tools.py,
test_edit_v2_*.py, test_studio.py, test_dialogue*.py (whatever exists). Report results.
Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/.
End the PR with DEPLOY (ff-only from the base commit, restart moiastro-studio moiastro-mcp, read-only smoke: tool count,
film_shot_override read on western_sunday_bride_v1, rollback).
