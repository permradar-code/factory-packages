Task 09 — film_export under ProtectHome, captions cut off, clip-check calibration, vehicle rule noise. Model: Sonnet 5.5 (high).
Repo permradar-code/moiastro-engine, base = origin/backup/server-state-20261015 (after 08B merge). Branch cc/export-captions-09.
Draft PR, small separate commits, offline tests only.

1. film_export push fails: "cannot read /home/moiastro/.ssh/known_hosts"
- moiastro-studio.service has ProtectHome=true (long-standing), so the process sees neither ~/.ssh/known_hosts nor the key.
  film_render.py (~l.380) and montage_assets_sources.py (~l.200) already use a temp UserKnownHostsFile for clones;
  film_export.py `_run` does not.
- Fix: one shared helper (e.g. app/production/git_ssh.py) used by all three: temp known_hosts with
  StrictHostKeyChecking=accept-new, and IdentityFile from env MOIASTRO_GIT_SSH_KEY (default: none -> current behaviour).
  film_export clone+push uses it. Clear Russian error when the key is not readable ("ключ GitHub недоступен службе — см.
  docs/git_ssh.md").
- docs/git_ssh.md: what the OWNER does on the VPS (do NOT edit systemd in the repo): either a systemd drop-in with
  `BindReadOnlyPaths=/home/moiastro/.ssh` or copy a deploy key to /opt/moiastro-engine/secrets/ (0600, owner moiastro, in
  .gitignore) + `Environment=MOIASTRO_GIT_SSH_KEY=...`; then restart moiastro-studio and moiastro-mcp. Exact commands.
- Tests: helper builds the right GIT_SSH_COMMAND; export uses it (fake git); unreadable key -> clear error.

2. Captions: in the film 5 opening draft one dialogue caption sits so low that half the letters are cut off.
- Find why: likely captions are burned BEFORE a clip's crop/zoom (film_edit_set "vf" crop on C04/C11/C17/C25) or the
  bottom margin ignores the crop. Captions must be drawn AFTER all per-clip crops, inside the 16:9 safe area (bottom margin
  >= 7% of height). Also report why only one caption appears in the 2-minute draft (expected: either all lines or none,
  per the film's caption setting) — fix if it's a bug, explain if intended.
- Tests: caption y-position after a crop stays inside the frame; caption pipeline order.

3. film_clip_check calibration (first real run on western_sunday_bride_v1)
- Caught correctly: C03 CUT@0.5 (2 foreign frames at the start), C19 DISSOLVE@0..2 (odd jump). C09 CUT@0.1 unknown.
- Missed: C23 (fast smeared camera move wide -> close-up), C27 (Sam's hat disappears, boy changes), C05 (pan reveals sign
  text). Their numbers: median_step 0.123 / 0.162 / 0.161, max_step 0.192 / 0.214 / 0.229, first_last_diff 0.221 / 0.200 /
  0.294. All clean clips had median_step <= 0.086.
- Add verdict CHECK when median_step > 0.11 or first_last_diff > 0.25 (constants, documented), reason text in Russian
  ("быстрое движение камеры / сильная смена картинки — посмотрите глазами"). Ignore cuts in the first 0.15 s (encoder
  start) unless the scene score is very high. Tests with the numbers above.

4. storyboard_check vehicle_no_horse is noisy (45/153 on film 5): require a horse in the same prompt; require a named
   driver only when the vehicle moves (drive/ride/roll/arrive/leave). Update tests.

Run: new tests + test_film_review_export.py, test_clip_check.py, test_storyboard_check_rules.py, test_edit_v2_*.py,
test_mcp_video_tools.py. Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/.
End the PR with DEPLOY (ff-only, restart moiastro-studio moiastro-mcp, owner's one-time key step from docs/git_ssh.md,
smoke: film_clip_check western_sunday_bride_v1 shows CHECK for C05/C23/C27; film_export dry run; rollback).
