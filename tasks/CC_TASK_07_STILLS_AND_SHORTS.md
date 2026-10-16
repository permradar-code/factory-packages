Task 07 — stills cadence under the narrator + Shorts fixes. Model: Sonnet 5.5 (high) is enough.
Repo permradar-code/moiastro-engine, base backup/server-state-20261015 (HEAD a948a34, = VPS). Branch cc/stills-shorts-07. Draft PR.
Small, separate commits per item. Offline tests only; venv with the repo requirements is fine.

A. Stills under the narrator (owner rule: a new picture about every 3 s, never long holds; film 4 had 8–18 s holds)
1. edit_v2/config.py: still_max_seconds 7.0 -> 4.0, still_qc_max_seconds 7.5 -> 4.5 (both stay tunable per film).
2. edit_v2/plan.py allocate(): when stills hit still_max and there is no video to slow down, today the last branch
   scales every visual up (`lens * need / sum(lens)`) -> stills longer than still_max. Instead fill the gap by CYCLING the
   block's stills (repeat them in order; each repeat gets a different Ken Burns move — reuse the existing even/odd move
   logic or add a direction offset) so no single still exceeds still_max; record a plan warning
   "N04: 3 stills for 21 s — repeated; add ~4 stills". Videos keep current behaviour.
3. Storyboard check in film_package_prepare (or the montage contract validation it calls): for each narration row,
   needed_stills = ceil((est narration seconds − seconds covered by its video b-roll) / 3); if the row has fewer, add a
   warning to the prepare result (not an error) listing the row, has/needs. This is the hook a future auto-storyboarder
   will use.
Tests: allocate never yields a still > still_max when there is no video; cycling order/moves; QC flags a 5 s still;
prepare warns on a thin block; existing edit_v2 tests updated only where the 7.0/7.5 defaults are asserted.

B. Shorts: subtitle line leaking from a cut-out gap (real case: film 4 Short with pieces [0,8.67] and [14.92, …]; the cue
13.23–14.92 lay in the gap but showed from 0 s to 8.7 s of the Short)
- story_short.render caption mapping: `f2s` uses ±0.05 s tolerance, and when only ONE end of a cue maps, the other end
  is set to 0.0 / total. Fix: if only one end maps, clamp the missing end to the boundary of the SAME piece that contains
  the mapped end (piece start for a missing start, piece end for a missing end), then apply the existing < 0.3 s drop.
  With an opener, never place film captions inside the opener seconds.
- Test: the real case above (no caption in 0–8.7 s; with opener the same), plus a cue that truly spans a cut.

C. Shorts: download link + no MCP timeout
- Studio route GET /api/montage/{project_id}/shorts (list: name, duration, size, mtime) and
  GET /api/montage/{project_id}/shorts/{name}.mp4 (name validated like film_story_short names); film_download_links adds
  a "shorts" list; film_story_short returns "download_url".
- film_story_short takes 6–7 min and the MCP client times out at ~230 s (the render still finishes). Make it queue the
  render as a background job and return at once {"ok", "job": name, "status": "RUNNING"}; add film_story_short_status
  (project_id, name) -> RUNNING / DONE (+ result dict incl. download_url) / FAILED (+ sanitised error). Reuse an existing
  job/worker pattern in the codebase; keep the synchronous path available for tests.
- Tests for the routes, name validation (no traversal), and the job status transitions (fake render).

Run: new tests + tests/test_story_short.py, tests/test_story_short_opener.py, tests/test_edit_v2_*.py,
tests/test_film_review_export.py, tests/test_mcp_video_tools.py, tests/test_studio.py. Report results.
Rules: no network/paid APIs/secrets; don't touch OAuth, MCP auth, systemd, web/studio/reviews/.
Deploy = restart moiastro-studio + moiastro-mcp. End the PR with the same DEPLOY section style as PR #9 (ff-only from
a948a34, restart, read-only smoke check, rollback).
