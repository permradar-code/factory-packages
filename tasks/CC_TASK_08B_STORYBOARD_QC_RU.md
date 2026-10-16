Task 08B — storyboard checker rules, clip cut/dissolve check, Russian shot descriptions in Studio, retire old Recovery v3.
Model: Sonnet 5.5 (high). Repo permradar-code/moiastro-engine, base = the 08A branch after merge (or origin
backup/server-state-20261015 if 08A is not merged yet — then keep files apart to avoid conflicts). Branch cc/storyboard-qc-08b.
Draft PR, small commits, offline tests only. Background: owner's film 5 opening had many defects caused by prompts, list in
factory-packages qc/DEFECT_EXAMPLES.md (owner pastes it if needed).

1. storyboard_check.py — more rules (warnings in film_package_prepare; each with shot id + Russian one-line hint)
- Person names/roles mentioned in image or motion prompt but missing from the shot's references -> "дорисует чужого".
- Quoted text or sign/newspaper/letter wording ("GENERAL STORE", any "..." inside prompts, 'sign reads') -> text on screen.
- wagon/buggy/cart/carriage without horse + driver named in the same prompt.
- close-up / medium close without a background phrase (street, interior, etc.).
- risky verbs: pour, wash, pee, lying, embrace, undress, blood, gun pointed at woman/child -> ask for exact visual wording.
- dialogue clips: camera words tilt / pan up / reveal / cut to / then / another angle -> only static or slow push-in.
- more than one speaking character in one clip; motion prompt with two viewpoints ("then", "cut to", "we see", "reverse").
- first clip of the film is a static portrait (no action verb) -> "первый кадр должен быть экшеном".
- clothing: a character described with different outfits in adjacent shots (simple keyword diff) -> continuity warning.
- Return a summary count by type; prepare prints the top 15. Tests for each rule (positive + negative).

2. film_clip_check(project_id, shot_ids="") — free, ffmpeg only
- Per clip: hard cuts (scene score > 0.2) AND soft dissolves: frame difference every 0.5 s (mean abs diff of downscaled
  grey frames) with a sustained-change window, plus first-vs-last frame similarity; report timestamps and a verdict
  OK / CUT@t / DISSOLVE@t..t / CHECK. Optional contact sheet path (frames every 0.5 s) for the owner's chat review.
- Runs automatically after the video stage as a warning in film_status / review page (not blocking).
- Tests with synthetic clips made by ffmpeg in the test (hard cut, crossfade, static) — no external files.

3. review_ru: short Russian description per shot in Studio
- Owner can't read the browser-translated prompts. Add an optional "review_ru" field per shot in the shotlist/contract
  (written by the storyboarder; 1-2 short sentences: who, where, what happens, line if any). Studio review cards show it
  above the English prompt; if missing, show nothing new (no machine translation, no network).
- film_package_prepare warns when review_ru is missing for > 20% of shots. Tests for contract validation + Studio render.

4. Retire the old Recovery v3 service paths (moiastro-recovery)
- Remove the old «Восстановление» Studio tab and recovery_*_submit / recovery_veo_* MCP tools from registration (keep
  modules importable; keep recovery_health read-only). Release its reserved Veo budget record if one is stored in the repo
  data model (report what you find; don't delete data files). Docs: what the owner must do on the VPS to stop/disable the
  service (commands in the PR only; do NOT edit systemd).

Run: new tests + test_storyboard_check*.py, test_film_package*.py, test_studio.py, test_montage_operator_ui.py,
test_mcp_video_tools.py, test_advisor_runner.py. Report results.
Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/.
End the PR with DEPLOY (ff-only, restart moiastro-studio moiastro-mcp, smoke: film_clip_check on western_sunday_bride_v1
C01 and C12 must report the known cut/dissolve, rollback).
