# MOIASTRO factory v2 — Phase 1.5: "never get stuck" (for Claude Code in the cloud)

Кратко по-русски: фабрика не должна застревать. Если Google отказал — сама идёт по цепочке обходов,
включая режим «ингредиентов» (как во Flow, который сработал там, где фабрика сдалась). Если всё равно
не вышло — клип помечается «нужен ручной», владелец получает уведомление и готовый пакет для Flow,
а остальная работа идёт дальше. Очередь: можно остановить задачу, переделки идут первыми, финальный
монтаж сам не запускается. Плюс доработки монтажа, найденные на фильме 3.

Lessons come from film 3 "The Barn in the Storm" (project `western_barn_storm_v1`, 9 Oct 2026).

---

## 0. Repositories and ground rules

- **Work repo:** `permradar-code/moiastro-engine`.
- **Base:** branch `feature/factory-v2-phase1` (PR #1). Create `feature/factory-v2-phase1-5` from it and open a
  **PR into `feature/factory-v2-phase1`**. Do not merge.
- **Reference repo (read-only):** `permradar-code/factory-packages`, branch `tools/montage`:
  - `montage/western_barn_storm/build.py`, `plan.py` — the film-3 hand edit (newer than the film-2 one you ported)
  - `montage/western_barn_storm/short_fire.py`, `montage/western_stagecoach_bride/shorts_vertical.py` — Shorts
  - `montage/western_barn_storm/thumbs_ai.py` — thumbnails with caption over key art
- **Never:** deploy, restart services, touch the VPS, read/print/commit secrets or `.env`, change provider keys,
  weaken tests, rewrite history, make real provider calls in tests.
- Same rules as Phase 1: opt-in where behaviour changes for old projects, atomic writes with project owner/mode,
  all existing tests pass, new tests on synthetic media.

## 1. What actually got stuck on film 3 (facts)

1. Five videos (C06, C07, B01, C67, H01) failed in every step of the Omni → Omni-light → Veo → Veo-light chain.
   Errors: "prominent individuals" (face similarity), "unspecified policy", "The input could not be submitted …
   Responsible AI practices" (the **start frame** itself was refused: a child together with a baby).
   The same shots were made in **Google Flow with "ingredients"** (Veo 3.1 Fast with reference images of the
   characters/location, **no start frame**) on the first try. One shot (C65, child + baby) is still FAILED.
2. `film_redo` / `montage_assets_repair` on a few assets got status QUEUED and waited behind the factory's own
   **automatic final render**. There is no cancel endpoint; the owner had to `systemctl restart` the Studio.
3. Manually made clips had to be copied with scp and marked READY with a Python one-liner as user `moiastro`,
   then `chown/chmod` by hand (Phase 1 upload endpoint fixes the clips; references are still not covered).
4. A main character's reference (R001/R002) came out ugly; its description could not be changed because the
   fingerprint is locked; the owner replaced `references/R00x/source.png` by hand.
5. Only 4 vertical 9:16 hooks per film — not enough for a good Short (we had to crop 16:9 clips).

## 2. Video: the "ingredients" fallback (main deliverable)

- Allow `reference_images` on `/generate/vertex/veo` in `app/provider_worker.py` (the provider
  `VertexReferenceMediaProvider.generate_veo` already supports it: ≤3 images, `referenceType: asset`, 8 s,
  no `source_image`/`last_frame`). Add `client.veo(..., reference_images=[...])` in `provider_client.py`.
- In `montage_assets_runner.py`, after the existing chain (and the Phase-1 policy variants) fails with a
  policy/safety error, add:
  5. **Veo 3.1 Fast, ingredients mode**: no start frame; up to 3 refs chosen deterministically
     (characters in the shot by importance, then location); prompt = the shot's image prompt (what is in the
     frame) + motion prompt + dialogue line with the usual dialogue direction; 8 s; `generate_audio` as for the
     normal clip. Store as the clip; the edit trims it (dialogue alignment runs as usual).
  6. **Veo 3.1 (standard), ingredients mode** — same request, other model.
- **Start-frame refusal shortcut:** if the error says the *input* was refused ("input could not be submitted",
  "input image", "prominent individuals" on an image-to-video call), do **not** retry other prompts with the same
  frame — jump straight to the ingredients steps.
- **Children / babies rule table** for prompt softening (both image and video): "a baby" → "a baby wrapped in a
  blanket, face hidden", "a child cries / is hurt / is grabbed" → "a child stands close to her mother", child +
  armed man in one frame → split or show the man from behind. Keep it a small data table with tests.
- Cost: refused requests are free, successful fallbacks cost the normal Veo price; cap total attempts per asset
  (`production.policy_retry_max`, default stays 3 for prompt variants; ingredients steps are +2 on top) and show
  the real spend per asset in the Studio.

## 3. Images and references

- Check that the montage image path really falls back from Gemini to OpenAI (`image_router.py` has a secondary)
  for `image:*` and `reference:*` on policy errors, and apply the children rule table before switching.
- **Reference upload in the web UI** (like Phase-1 clip upload): replace `references/<Rxxx>/source.png`, validate
  PNG/JPEG + aspect, atomic, owner/mode, `metadata.source="manual_upload"`, sha256. Do **not** reset budget
  approval / fingerprint. List images and videos that used this reference and offer "Redo these" (checkboxes),
  never redo them automatically.
- **Edit a reference description and regenerate** without touching the budget fingerprint (store the override in
  `montage/edit_overrides.json` like Phase 1 does for line text).

## 4. Never block: NEEDS_MANUAL + notifications

- When every step fails, set the asset to new status **`NEEDS_MANUAL`** (not FAILED). It does not stop the other
  assets; finalize/export treat it like `SKIPPED` once the owner presses Skip, or like READY once a file is uploaded.
- On the asset card: **"Flow pack"** download (ZIP streamed on the fly): `prompt.txt` (image prompt + motion +
  dialogue line, ready to paste into Flow), the 3 ingredient images, the start frame, target aspect and duration.
- **Telegram/email notification** (`app/notifications.py` already exists) when: an asset goes NEEDS_MANUAL,
  a review gate waits for approval, a job stalls, the film is ready. One message per event, short, Russian.

## 5. Queue: stop, priority, no surprise renders

- **Cancel:** `POST /api/montage/{p}/jobs/current/cancel` + button "Остановить" + MCP `film_job_cancel`.
  Cooperative flag checked between assets; running ffmpeg/whisper subprocesses are terminated; assets in progress
  go back to PENDING. Provider calls already sent are allowed to finish but their result is kept, not wasted.
- **Priority:** redo / repair / upload-follow-up work runs **next**, before the rest of a long run, not after it.
- **No automatic final render.** Final montage starts only from the button "Собрать фильм" (or MCP
  `film_edit_render`) after "Approve All Videos". Optional per-project flag `production.edit.auto_render: true`.
- **Watchdog:** a job without heartbeat for 10 min is marked STALLED, its worker restarted, work resumed; notify.
- A permanent policy failure is never re-queued by "Resume" (only by Redo with a changed prompt or by upload).

## 6. Edit engine v2: port the film-3 improvements

Compare `montage/western_barn_storm/build.py` + `plan.py` with what you ported in Phase 1 and add:
- Whisper cut: start = first word **− 0.35 s**, end = last word **+ 0.4 s** (−0.0/+0.25 clipped the first
  syllable); truncate repeated words to the expected word count; if the transcript has fewer words than
  expected − 1, use the energy span instead (PARTIAL).
- Global colour grade `production.edit.grade` (film 3: `eq=contrast=1.05:saturation=1.15:gamma=1.13:brightness=0.03`)
  applied to clips and stills.
- Per-clip filters `edit.vf: {"pre": "crop=…", "post": "eq=…"}` (crop away burned-in text, face close-up,
  day→night).
- Series music library: cues like `S2:M07` reuse a music file from another project of the same series.
- `frame:<clip>@<sec>|<weight>` stills inside narration blocks, `<clip>@a-b` ranges (check they match).
- End-screen background from a chosen clip (`END_BG`) and the title card id.

## 7. More vertical hooks (small)

- Shotlist/package template: **8 vertical 9:16 hooks** per film instead of 4, chosen from the strongest dialogue
  beats (threat, humiliation, reveal, kiss/proposal, joke), each 6–8 s with one line. Only the template and the
  validation; the owner approves the budget as usual.
- (Phase 2, do not start: automatic Shorts builder and thumbnail packs — list questions in the PR.)

## 8. Acceptance (put results in the PR description)

- [ ] All old tests + Phase 1 tests pass.
- [ ] Tests: ingredients fallback is reached after the chain fails; start-frame refusal skips straight to it;
      quota/timeout errors never trigger variants; attempt cap respected; children rule table.
- [ ] Tests: NEEDS_MANUAL does not block other assets; Flow pack ZIP contents; notification calls (mocked).
- [ ] Tests: cancel stops a synthetic long job within 5 s and leaves no half-written files; redo jumps the queue;
      no final render without the button/flag; watchdog marks a stalled job.
- [ ] Tests: reference upload keeps fingerprint and budget approval; dependants listed, not regenerated.
- [ ] Tests: whisper −0.35/+0.4, repeated-word truncation, PARTIAL fallback, grade + per-clip vf in the segment
      command, `S2:` music resolution.
- [ ] `docs/edit_v2.md` and a new `docs/fallbacks.md` updated; PR description with a short Russian summary,
      how to enable, rollback, and the exact deploy steps (which services to restart).
