# MOIASTRO factory v2 — Phase 1 task (for Claude Code in the cloud)

Кратко по-русски: фабрика должна сама монтировать фильм так же, как я смонтировал «The Stagecoach Bride» вручную; клипы и фильм смотрятся и скачиваются прямо в вебке; любой клип можно заменить своим файлом или пропустить; отказы Google обходятся автоматически. Работа — в отдельной ветке и Pull Request. Никакого деплоя.

---

## 0. Repositories and ground rules

- **Work repo:** `permradar-code/moiastro-engine` (the factory: FastAPI Studio API, durable asset runner, MCP server, `web/studio`).
- **Reference repo (read-only):** `permradar-code/factory-packages`, branch `tools/montage`. It holds the hand-edit pipeline that produced a good film:
  - `montage/western_stagecoach_bride/build.py` — EDL → video segments → audio mix → SRT (the logic to port)
  - `montage/western_stagecoach_bride/plan.py` — the edit plan format (clips, narration blocks with their own visuals, titles, end card, music cues, subscribe badges)
  - `montage/western_stagecoach_bride/qc.py` — QC (black / freeze / silence / loudness / contact sheets)
  - `montage/western_stagecoach_bride/shorts.py`, `thumbs.py` — Shorts and thumbnails (Phase 2, read only for now)
  - `briefs/western_stagecoach_bride/fix1/build_fix1.py` — how b-roll per narration block is specified (`"for": "N04"`)
  - `briefs/western_stagecoach_bride/shorts1/build_shorts1.py` — vertical 9:16 clips as `hooks`
- **Branch:** `feature/factory-v2-phase1` from the default branch. Open a **Pull Request**; do not merge.
- **Never:** deploy, restart services, touch the VPS, read/print/commit secrets or `.env`, change provider keys, weaken existing tests, rewrite git history.
- **Keep existing behaviour working.** New behaviour is opt-in per project: `production.edit.engine = "v2"` in the shotlist (default stays the old engine). Existing projects must render exactly as before.
- **Tests:** the whole existing test suite must pass. Add tests for everything new. Use synthetic media generated with ffmpeg `lavfi` (color/testsrc + sine) — no real provider calls, no network.
- **File writes:** always atomic (temp file + rename) and with the same owner/mode as the project directory (lesson learned: a JSON state file rewritten by root with mode 0600 made the Studio API return empty data). Add a helper and use it everywhere new code writes into `projects/<id>/`.

## 1. Edit engine v2 (the main deliverable)

Port `build.py` into the factory as a reusable module (e.g. `app/production/edit_v2/`), driven by the project's shotlist/state instead of hard-coded paths.

**Edit plan.** Build an EDL from the shotlist timeline in order:
- `clip` with dialogue → plays **with its own audio**. Trim: whisper word timings from `dialogue_alignment:<id>` when the transcript covers ≥80% of the expected line (fuzzy match), cut = first word − 0.0 s … last word + 0.25 s, min 2.4 s; otherwise energy-based speech span (band-pass 150–4000 Hz, threshold max−22 dB): start = 0 if speech starts < 1.0 s else speech_start − 0.45 s; end = speech_end + 0.85 s.
- `clip` without dialogue (action) → whole clip or `edit.range: "a-b"`.
- `narration` block → its **own visuals only**: a list from `visuals` on the narration row (ids of b-roll clips, `img:<id>` stills, `frame:<clip>@<sec>` stills, `<clip>@a-b` ranges, optional `|weight`). If `visuals` is missing, auto-collect clips/images whose `for` equals the narration id, in timeline order.
  - **A dialogue clip must never be used under narration.** Validate and fail the plan with a clear message if it happens.
  - Block length = 0.5 s lead + voice + 0.9 s tail. Allocation: videos keep natural speed; stills absorb a shortfall first (max 7 s each); then videos slow down up to 1.25×; only then hold the last frame. Crossfade 0.45 s between visuals inside a block.
  - Stills get a slow Ken Burns move (alternate push-in / lateral drift).
- `title` cards (Rye font from branding), `end` card (bright frame of a chosen clip + series name, default 12 s).
- No clip is used twice unless the plan says so explicitly.

**Audio mix** (numpy, as in `build.py`): speech normalised to −20 dB active RMS; ambient of action clips −23 dB; b-roll ambience under narration −34 dB; music cues from `music_cues.json` anchored to event ids with 2 s crossfades; ducking −15 dB under speech, −7 dB under clips (attack 0.15 s, release 0.6 s); final `loudnorm` I=−14 LUFS, TP=−1.5 (two-pass, linear) plus an oversampled true-peak limiter so the AAC file measures ≤ −1.0 dBTP.

**Overlays:** animated subscribe badge (`subscribe_overlay_source` from branding) at `production.edit.badge_at: [[event_id, seconds], …]`.

**Subtitles:** narration from ElevenLabs character alignment, grouped into readable cues; dialogue cues from the clip's speech span and its line text (support `production.edit.line_overrides: {clip_id: "new line"}` for clips replaced by hand).

**Outputs:** `render/long.mp4` (1920×1080, 24 fps, H.264 CRF 18, AAC 192k), `subtitles/long.srt`, `qc/long_preview_480p.mp4`, `render/edl_timed.json`.

**QC (port `qc.py`)** into `final_qc:long`: duration, black > 0.4 s (title cards allowed), freeze > 2.5 s (title cards allowed), silence > 1.5 s, loudness, plus two new checks: (a) no dialogue clip inside a narration block, (b) no still held > 7.5 s. Contact sheets: first 60 s every 2 s, whole film every 10 s.

**Performance:** render segments in parallel (configurable jobs), cache segments by content hash so re-renders after a single replaced clip only rebuild that segment.

## 2. Studio web: watch, download, replace, skip

- **Player:** final film, preview and each clip/image playable in the browser (extend `web/studio/montage.js` + existing asset endpoints, HTTP range requests for video).
- **Downloads:** buttons for final MP4, SRT, thumbnails, and **"all clips (ZIP)"** streamed on the fly (no temp copy of the whole set on disk).
- **Upload your own file** per asset card: `POST /api/montage/{project}/assets/{asset_id}/upload` (multipart, size limit configurable, default 500 MB).
  - Validate with ffprobe: video → H.264/HEVC + AAC (or no audio for b-roll), aspect matches the shot (16:9 or 9:16, ±2%), duration ≥ 0.8 × target; image → PNG/JPEG, aspect matches.
  - Store atomically at the asset path with correct owner/mode; set `status=READY`, `metadata.source="manual_upload"`, original filename and sha256.
  - Invalidate only dependants (its `dialogue_alignment`, `final_*`), exactly like `film_redo` does, and resume missing work.
  - Optional field "new line text" → stored in `line_overrides` and used for alignment and subtitles.
- **Skip:** `POST …/assets/{asset_id}/skip` → new status `SKIPPED`. Skipped assets do not block finalize, export or montage; the edit engine drops them (and warns in QC). "Unskip" restores PENDING.
- **Partial export:** `film_export` and the GitHub package export accept projects where every required asset is READY or SKIPPED.

## 3. Automatic way around Google refusals

When a provider fails with a policy-type error (texts like "prominent individuals", "Responsible AI practices", "unspecified policy reason", "safety"), do not repeat the same request. Generate up to **3 variants**, stop at the first success, log each variant and reason in the asset state:
1. **Soften action wording:** remove/replace phrases with a weapon pointed at a person ("presses a derringer to her side" → "stands close beside her, one hand inside his coat"), "kneels clutching his hurt wrist" → "stands disarmed", etc. Keep a small rule table + a generic fallback sentence.
2. **Camera change:** "seen from behind / over the shoulder / face partly shaded by a hat brim", keep the line.
3. **Face-similarity refusals:** regenerate the start frame with an extra "plain, unremarkable, clearly non-celebrity features" clause and a new seed; for a referenced main character keep the references.

Refused requests cost nothing, but the total number of attempts per asset is capped (`production.policy_retry_max`, default 3). Each variant must keep the shot's aspect ratio, characters and dialogue.

## 4. MCP tools (app/mcp_server.py and the montage tools module)

Add: `film_asset_skip(project_id, asset_id)`, `film_asset_unskip(...)`, `film_edit_render(project_id, engine="v2")` (queues the v2 render), `film_download_links(project_id)` (returns Studio URLs for final/preview/srt/zip). Uploading stays in the web UI (binary). Update tool docstrings.

## 5. Acceptance checklist (put the results in the PR description)

- [ ] All old tests pass; new tests for: plan building (narration never contains a dialogue clip), allocation rules, trim logic (whisper vs energy fallback), audio levels within ±1 dB of targets on synthetic input, SRT timing, upload validation (good/bad aspect, too short), skip → export allowed, policy-retry variant generation, atomic write keeps owner/mode.
- [ ] A synthetic end-to-end test: 6 dialogue clips, 3 action clips, 3 narration blocks with b-roll + stills, 2 music cues → `long.mp4` renders, QC passes, duration matches the EDL ±0.1 s, A/V offset 0.
- [ ] `docs/edit_v2.md` documents the shotlist fields (`visuals`, `for`, `badge_at`, `line_overrides`, `edit.engine`, `policy_retry_max`) with a short example.
- [ ] PR description: what changed, how to enable per project, migration notes, how to roll back (feature flag off), and a short Russian summary for the owner.

## 6. Phase 2 (do NOT start; only list open questions in the PR)

YouTube upload through the API with schedule, chapters, tags, DE/ES/NL localizations, `containsSyntheticMedia`, playlist, captions and thumbnail; automatic vertical Shorts (full-screen 9:16, big 2–4-word captions) and thumbnail packs from `shorts.py` / `thumbs.py`; script → shotlist with coverage/budget/policy pre-check; daily analytics digest; Cedar Bluff character library; spend dashboard.
