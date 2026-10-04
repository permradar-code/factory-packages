# HANDOFF: western_widows_piano_v1 (rewritten 4 Oct 2026, end of session 2)

Talk to the user in Russian, briefly, no filler. Branch `pkg/western_widows_piano_v1` in `permradar-code/factory-packages`; local checkout `C:\Users\permr\fl_work\wwp` (keep it short: git fails with "Filename too long" in long paths). Source of truth for content: `briefs/western_widows_piano/shotlist.json` on branch `tools/montage` (commit **7d0f9ec**); process: `BRIEF.md` in the same folder (commit **bb32e99**). Always re-fetch both at the start:
`gh api -H "Accept: application/vnd.github.raw" "repos/permradar-code/factory-packages/contents/briefs/western_widows_piano/shotlist.json?ref=tools/montage" > _variants/brief/shotlist.json` (same for BRIEF.md).

## 0. Mode the user ordered
"Work to the END without stops and without questions. All STOP points are lifted." Decide yourself:
- bad result: max 2 regenerations per clip/image, then keep the best and write the problem into README "Notes for the montage";
- Flow "famous people" filter on a minor character (not Clara): make that character a NEW face from its `look`, redo all its refs, continue. Never dodge the filter with angles/distance;
- Gemini or Flow limit: wait and retry once an hour, do other work meanwhile;
- doubts: write into README "Questions" and go on.
Stop only if Flow credits < 150, or when the context is ~70% full: update this file, push, tell the user a new session is needed. At the very end: README with credits per clip, manifest `phase: done`, final push, ONE summary message to the user.
Push after every ~10 finished files; keep manifest and README current.

## 1. Approved decisions
- Faces: Clara = candidate **#2** of `docs/clara_candidates.jpg` (look 7d0f9ec: "very pretty, original fictional character", beauty mark under the left eye, copper-chestnut braided crown); Deke = v4 (long jaw, half-smile); Marshal = v2 (scar through the eyebrow); Mercer, Lily, Pike, Agatha, Sam = first approved versions. All in `visuals/refs/` (CHAR_*_front/_34/_full.png, 1376x768).
- Marshal: ALWAYS write "plain five-pointed silver star badge, no lettering, no engraving". Piano: no nameplate, no lettering. `build_queue.py` adds these automatically.
- Narrator: ElevenLabs "Bill" (`pqHfZKP75CvOlQylNhV4`); music M01..M13 approved, M14 skipped; M06 accepted. Kitchen ref with four chairs stays.
- Clip STOP 2 result: variant (a), dialogue is spoken inside the Flow clips (Mercer test: line audible, lips match).
- Tools (BRIEF bb32e99): scene stills I16..I69 in **Gemini** (2752x1536, for zoom moves), new chat every 7-8 images; clip first frames `Cxx_first` in **Flow images** (fast, no download/upload; upload the current refs into the Flow project once); video in Flow only. If Flow images give the usage limit again: first frames in Gemini (upload via the patch), try Flow again next day (limit is daily, resets in ~24 h; seen reset 3 Oct ~01:30 -> 4 Oct 10:30 OK).
- Flow pacing, strict: one request at a time, x1 (never x2-x4), wait until finished, pause 30-60 s, max ~30 per hour, log every image with time in `_variants/flow_log.tsv`. Videos one at a time too.

## 2. Exact status
- Phase 0, 1 (refs), 5 (narration N01..N10 + alignment), 6 (music M01..M13): DONE and pushed.
- Phase 3 images: **I01..I15 done** (visuals/images/I01..I15.png, 1280x720), I16..I69 pending.
- Phase 2/4 clips: **C13 done** (`visuals/video/C13.mp4`, 6 s, 10 credits, first frame `visuals/images/C13_first.png`, user accepted it). C11 and C34 must be (re)made with the final Clara; all other clips (49 in total, ids with a/b like C02a) pending. Shotlist now has 49 clips: 4 s x11, 6 s x28, 8 s x10; credits 7/10/12; one pass ~477 (core 445); optional C06, C21, C28 go last and only if > 150 credits remain.
- Flow credits: the balance is NOT shown in the UI. User reported 905 on 3 Oct. Spent **29** (7 Mercer test, 12 dropped C11 with the old Clara, 10 C13). **Left 876** (manifest `flow_credits_left`). Guard: stop below 150. Read the price in the settings chip before every video.
- ElevenLabs left 9720 of 23736 (music cost ~6.9 credits/s, narration ~0.22/char); nothing more is needed from it.
- manifest.json holds the 16 finished scenes (I01..I15, C13), `phase: images`.

## 3. NEXT STEPS in order
1. **C11 and C34 again** with the final Clara (shotlist 7d0f9ec prompts: `start_frame_full_prompt` for the frame, `video_prompt` for the clip). C11: 8 s (12 cr), C34: 4 s (7 cr). Compare Clara's voice across C11, C13, C34 (the user will judge by ear; just deliver the three files and record has_audio).
2. Phase 3: images I16..I69 in Gemini (pipeline in section 4). Review a contact sheet every ~10 images (`tools/sheet.sh`).
3. Phase 4: all clips in timeline order, core first, optional last. First frames in Flow images (section 5), video one at a time. Credits per clip into manifest scenes and README table.
4. Push every ~10 files; at the end README + manifest `phase: done` + one message.
The user earlier said "images first, then clips"; the new brief/decision keeps the order but allows interleaving; do C11/C34 first as he asked.

## 4. Gemini pipeline (stills; also fallback for first frames)
Tab: always a tab opened by `tabs_create_mcp` (NOT the first tab). Viewport is 1366x641 or 1366x585 and changes between tabs: never trust hard-coded coordinates, get them from JS (`FIND`).
**Never use JS `.click()` on the Gemini download button**: after 1-2 programmatic downloads Chrome silently blocks all later downloads in that tab (the page still says "Изображение скачано", no file). If it happens: open a NEW tab, never JS-click downloads again. Downloads by real clicks (computer tool) work indefinitely.
**Setup of a chat** (every 7-8 images, or when generation gets slow):
1. `navigate https://gemini.google.com/app` (or click "Новый чат" in the sidebar; the SPA keeps the JS state), wait 6 s.
2. Paste `tools/gemini_helpers.js` with `javascript_tool` (once per page load).
3. Image mode + ratio with REAL clicks: click the "+" ("Загрузка и инструменты"; get xy with `FIND(/Загрузка и инструменты/)`), then the menu item "Создание изображений" (menu is open only if the click registered), then the pill "Соотношение сторон" and the option "16:9". **The first click after a page load or a new chat is often swallowed**: take a small screenshot (scale 0.4) after the "+" click; if no menu, click again. The same for the aspect pill. Verify with JS: button aria-labels "Отменить выбор: Изображения" and "Соотношение сторон, 16:9" exist.
4. Attach input: click "+", then "Загрузить файлы" (intercepted by the patch, no native dialog), then in JS tag the LAST `input[type=file]` that is not `#PQ` with `aria-label="GEMINI_ATTACH_INPUT"`, and `find "file input labeled GEMINI_ATTACH_INPUT"` -> ref. Gemini reuses this one input for the whole session: later `file_upload` straight to that ref attaches files (no menu clicks).
5. Prompt queue: `python tools/build_queue.py` (reads `_variants/brief/shotlist.json`, writes `_variants/up/<ID>_<n>.jpg` = refs scaled to 1024 px, `_variants/queue_images.json`, `_variants/queue_frames.json`; prompts get a prefix naming the attached refs in order). Upload `_variants/queue_images.json` into the `#PQ` input (`find "file input labeled PROMPT_QUEUE_INPUT"` + `file_upload`), then `await LOADQ()` -> "loaded 69". (queue_frames.json has the clip first-frame prompts + video prompts + durations.)
**One image = one message** with a `browser_batch` (file_upload works inside the batch) + a Bash call:
```
browser_batch: [ hover(cx,cy of PREVIOUS image), left_click(x,y of PREVIOUS image = download icon),
  file_upload(paths=[_variants/up/<ID>_1.jpg ...], ref=<GEMINI_ATTACH_INPUT ref>),
  javascript START('<ID>'),  wait 10 s x3-4,  screenshot scale 0.1 (cheap; forces rendering),  javascript "await WAIT(40000)" ]
Bash: tools/gem_save.sh <PREVID> visuals/images/<PREVID>.png      # waits for the new download, dedupes by hash, makes 1280x720 PNG, keeps the 2752x1536 original in _variants/gemini2
```
WAIT returns {x,y,cx,cy,n,id} when the image is ready (x,y = download icon, cx,cy = hover point; they were 1151,71 / 827,239 in a fresh chat) or {pending} (poll again with another batch) or {err:'timeout'}.
Facts: `javascript_tool` dies after 45 s per call; generation takes 45-80 s in a fresh chat but 3-9 min after ~10 images in one chat; a background/hidden tab may not render: the tiny screenshot fixes it; `.ql-editor` takes text via `execCommand('insertText')`; Gemini sometimes answers a "two images" request with one image; faces converge if the same description is re-sent in one chat, use "Retry" (menu "Повторить") or a new chat for variety.
Gemini download name `Gemini_Generated_Image_*.jfif` (really JPEG); `tools/grab_gem.ps1` converts to PNG.

## 5. Flow pipeline (video; first frames as Flow images)
Project: `https://flow.google.com/project/7a937194-22cf-4e10-a8ea-406b0d82a514` (tab id from `tabs_context_mcp`; if first click after load is swallowed, click again). User is logged in (PRO).
- Settings chip at the bottom of the prompt bar (~(812,595) at 1366x641). Tabs "Изображение"/"Видео". Image: Nano Banana Pro, 16:9, **x1**, cost 0. Video: sub-tab "Кадры" (first/last frame slots "Первый"/"Последний"; keep the last slot empty), 16:9, model Omni 1.1 Flash, **720p**, duration buttons 4/6/8 (positions ~(684,493)/(739,493)/(796,493)), x1; the cost line "Стоимость генерации в бонусах: N" must read 7/10/12. After a reload the duration and the tab can reset: zoom on the chip region (650,440)-(922,615) and READ the cost before sending.
- Upload local files into Flow without freezing the tab: `javascript_tool` patch (same as tools/flow_upload_patch.js: replace `HTMLInputElement.prototype.click` so a file input is appended to the page), click the first-frame slot or "+", click "Загрузить" in the picker, `find "all input type=file elements"` -> ref, `file_upload` (max 10 MB per call; use the 1024 px copies in `_variants/up` or 1280x720 PNGs), wait 8-10 s, search the picker by file name, press Enter. Upload ALL current refs once into the project (CHAR_*_front/_34/_full, PROP_*, LOC_*) and attach them to Flow image prompts by name via "+" + search + Enter.
- Image first frame: prompt = `start_frame_full_prompt` (+ the ref prefix) with the refs attached; result at the top of the grid (newest first, ~20-40 s). Check: faces match, mouths closed, the speaker large and frontal (small/far faces lip-sync badly). Max 4 tries per first frame. In the picker, generated images get auto titles ("Woman posing for portrait"): rename is not possible, find them by grid position or use the "Frames" slot from the tile ("Добавить в запрос").
- Video: pick the first frame in the "Первый" slot, type `video_prompt` AS IS, send, wait 60-120 s (a clip is "done" when the tile shows a play icon and a title), open the tile (click), download icon top-right (~(1083,29)) -> "720p исходный размер" (~(1102,108)); then `powershell -File C:\Users\permr\fl_work\grab2.ps1 -Name Cxx -Sub visuals\video -Ext mp4`. Check with ffprobe (audio stream), `volumedetect`/`silencedetect`, and a contact sheet of frames (`ffmpeg -vf fps=1,scale=480:-1,tile=3x2`). Reject: face morphs, wrong person speaks, line changed, extra fingers, text on screen. Max 2 regenerations per clip.
- Errors: "Бонусы за эту генерацию не списаны" = nothing was charged (usage limit, filter, overload). A rejected tile has a retry arrow. Remove nothing else.
- Credits ledger: after every clip write credits in `manifest.json` scene (`credits`, `takes`) and README table; update `flow_credits_spent/left`.

## 6. Things that burned us (do not repeat)
- **Flow "famous people" filter** ("Этот запрос может нарушать наши правила в отношении генерации изображений известных людей"): triggered on the Clara v2 face made with the words "strikingly beautiful like the lead actress of a modern western drama". Refusals can come after the render starts; no credits charged. Fix = new face, new look text WITHOUT celebrity/actress wording ("original fictional character"). C11 (profile) passed with the bad face only because the face was small: do not use angles as a bypass. The user's order for testing candidate faces: run a C13-type first frame through Flow video; a refusal is free.
- **Flow image usage limit**: after ~60 images/25 min, plus x4 requests; resets after ~a day. Overload message when many requests are sent at once.
- **Gemini slows down** in a chat with >10 images (3-9 min each) -> new chat every 7-8 images.
- **Chrome blocks automatic downloads** after JS-triggered ones (section 4).
- Gemini web was "not supported in your country" while the user had a VPN; works with VPN off.
- Gemini "two images" requests give one image; same description in one chat gives near-identical faces.
- Claude in Chrome: the first click after a page load/new chat is swallowed; `computer scroll` max 10 ticks; screenshots right after a click can lag (wait 1-2 s); `javascript_tool` hides outputs containing URLs with query strings.
- Gemini viewport size differs per tab (641 vs 585 high); the image viewer opens if a click lands on a picture (leave with the back arrow or reload).
- Text appears on signs, plates and papers unless prompts say blank/no lettering (queue builder adds "All signs, papers and books show no readable writing").
- File sizes: ref uploads <= 10 MB per call; Gemini originals are 2752x1536 ~3 MB; package PNGs are 1280x720 (~1.7 MB), so push in batches of ~10 files.

## 7. Local files and tools
| What | Where |
|---|---|
| Repo checkout | `C:\Users\permr\fl_work\wwp` |
| Refs / images / video | `visuals\refs`, `visuals\images`, `visuals\video` |
| Narration / music | `audio\narration`, `audio\music` (+ music_log.json, tools/music_run.py) |
| Local only (gitignored) | `_variants\` : `brief\` fresh shotlist+BRIEF, `up\` scaled refs, `queue_*.json`, `gemini\`, `gemini2\` Gemini originals, `old_refs`, `old_refs_v2` (rejected Clara v2 files), `flow_log.tsv` (every image with time), `clara_cand`, `tests` |
| Scripts in git (`tools/`) | `build_queue.py`, `gemini_helpers.js`, `gem_save.sh`, `grab_gem.ps1`, `sheet.sh`, `flow_upload_patch.js`, `recv.py` (unused: Gemini CSP blocks localhost), `music_run.py`, older `grab*.ps1`, `upd_wwp.py` |
| Outside the repo | `C:\Users\permr\fl_work\grab2.ps1` (saves the newest download as png/mp4), `grabn.ps1`; Downloads folder `C:\Users\permr\Downloads` |
| Needed on PATH | git, gh (logged in as permradar-code), ffmpeg/ffprobe, python, powershell |
`_variants/` is not pushed. If it is missing (new machine), rebuild: re-fetch shotlist, `python tools/build_queue.py`.
ElevenLabs key: Windows user env var `ELEVENLABS_API_KEY`; never print or store it.

## 8. User preferences
Russian, short, no filler. One video at a time (never x2/x3). Report Flow credits per clip. Never touch secrets. Deliver through the orphan branch (commit per phase/batch). Do not push `_variants/` or secrets. Send images/videos the user must judge with SendUserFile.
