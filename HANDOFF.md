# HANDOFF: western_widows_piano_v1 (written 2026-10-03, end of session 1)

Talk to the user in Russian, briefly. Branch: `pkg/western_widows_piano_v1` in `permradar-code/factory-packages`. Source of truth for content: `briefs/western_widows_piano/shotlist.json` on branch `tools/montage`; process: `BRIEF.md` in the same folder (re-read it: it was updated during the session, see section 4).

## 0. Session 2 status (newest; overrides sections 2 and 5 where they differ)
- Re-fetched brief from `tools/montage` (commit `4a477fb`): shotlist has the NEW Clara look ("28-year-old ... beautiful, slender, soft youthful features ... gray-green eyes with a quiet weariness ... proud dignified expression ..."). Local copy of the fresh brief: `wwp\_variantsrief\` (gitignored). Use `look` from there, no manifest note needed (user said so).
- STOP 1 answer: Mercer, Lily, Pike, Agatha, Sam approved (do not touch). Clara, Deke, Marshal: redo. Clara: 4 front variants as two x2 requests with a pause, show the user, only then the other angles. Deke: skinny, 35, sharp face, thin mustache; Marshal: 50, gray walrus mustache; both must NOT resemble famous actors. Then show a sheet and wait for "ок".
- UPDATE (user, later in session 2): limit looks DAILY. All images x1 (no x2). Log exact time of EVERY image and the moment the limit hits in `_variants/flow_log.tsv` to compute the daily quota. Probe Flow every 2 hours with ONE x1 image. Plan B Gemini (gemini.google.com in user's Chrome) is BLOCKED by region ('не поддерживается в вашей стране'); do not try to bypass. Piano nameplate: leave until there is limit headroom. Music: STOP 4 passed (M02 ok). M01, M03-M13 generated sequentially (`tools/music_run.py`), M14 skipped by the user. No regeneration (--force --seed) without the user. M06 Shenandoah not yet verified by ear. ElevenLabs counter 14016/23736 (left 9720); the counter lags by one cue. Credit cost: ~6.88 per second of music, ~0.22 per narration character.
- 09:30 (VPN off): Flow image x1 still returned the usage limit; a 4 s video (Mercer, 7 credits) WORKED: video quota is separate from the image limit. mp4 has an AAC audio track. Credits: 905 -> 898. Gemini web (gemini.google.com, Pro account of the user) now opens: image mode via "+" -> "Создание изображений", aspect 16:9 menu, upload via the cc_file_input patch (find "all file inputs", try ref of the first file input, file_upload), output 2752x1536 jpg, no visible watermark. The first Gemini request returned an empty answer; a short follow-up in the same chat produced the image. Tests in `_variants/tests/`.
- SESSION 2, LATER (newest): decision by the user: ALL images are made in GEMINI (gemini.google.com in the user's Chrome, Pro account), one at a time with pauses, logged in `_variants/flow_log.tsv`. Video only in Flow. Clip start frames: make in Gemini, upload into Flow via the upload patch, then Frames-to-video.
  * Shotlist was updated again (commit 7c7b740): ONE speaker per clip (shot/reverse shot), 49 clips (4 s x11, 6 s x28, 8 s x10; credits 7/10/12; ~477 credits for one take, 445 core). Fresh copy in `_variants/brief/shotlist.json`; RE-FETCH before clips (`gh api -H "Accept: application/vnd.github.raw" repos/permradar-code/factory-packages/contents/briefs/western_widows_piano/shotlist.json?ref=tools/montage`). Credits now ~898, guard 150 -> usable ~748 (one take + ~270 of retakes).
  * Clara look updated again (commit 09daddf): "strikingly beautiful like the lead actress of a modern western drama ... no freckles" (take `look` from the fresh shotlist).
  * Gemini UI recipe (viewport 1366x585): new chat -> "+" (533,292) -> "Создание изображений" (642,467) -> aspect pill (825,505) -> 16:9 (566,458) -> click prompt (700,397) -> type -> Enter. Clicks right after a page load are often swallowed: take a screenshot after each step; do not click tiles of the gallery (it attaches a style). Mode and 16:9 persist inside a chat: chat `https://gemini.google.com/app/3fc37b8806ccfe4e` is already in image mode 16:9, just type a new prompt there (add "a clearly different man/woman than in the previous images" to get different faces). After ~35 s: scroll down 10x3, scroll up 1, hover (826,200), download icon is at ~(1150,37..78) (top right of the latest image). Then `powershell -File tools/grab_gem.ps1 -Name X` (saves newest Gemini download as real PNG into `_variants/gemini/`, refuses duplicates). Output 2752x1536 (16:9), no visible watermark. Reference images upload: use the cc_file_input patch (tools/flow_upload_patch.js) + find "all file inputs" + file_upload on the first ref.
  * Done in Gemini (15 images, no limit hit up to 10:00): CLARA_front_v1..v4, DEKE_front_v1..v4, MARSHAL_front_v1..v4 in `_variants/gemini/` (+ *_sheet.jpg contact sheets, sent to the user). NEXT: wait for the user's choice of faces; then Clara 3/4 + full body from the chosen front (WITH the chosen front as reference), same for Deke/Marshal; then PIANO (no nameplate), HORSE, 8 locations. Chosen faces go to `visuals/refs/CHAR_*_front.png` (resize to 1376x768 like the others is optional; Gemini originals are 2752x1536).
- FACES CHOSEN by the user: Clara v2, Deke v4, Marshal v2; refs CHAR_{CLARA,DEKE,MARSHAL}_{front,34,full}.png replaced in visuals/refs (old ones in _variants/old_refs, gitignored). RULE: in ALL prompts/frames for Marshal write "plain five-pointed silver star badge, no lettering, no engraving". Gemini ref upload recipe: install patch, +, Upload files, JS-tag the LAST input[type=file] (aria-label), `find` it, file_upload on that ref; always screenshot after the download click (it sometimes opens the image viewer: close with the back arrow at (46,32)). Image chat in use: gemini.google.com/app/7a43c2beaf6f3879 (image mode, 16:9). NEXT: PIANO without nameplate, HORSE, 8 LOC_* in Gemini, then Phase 2 clip tests with the fresh shotlist.
- Strict Flow pacing from the user: ONE request at a time, max x2 (refs x1), never x3/x4, 30-60 s pause, <=30 images/hour, log in `_variants/flow_log.tsv` (time, images, request, result), start frames max 4 tries. On "лимит": stop, log time/count, do audio/music/download/manifest, retry a single x1 an hour later.
- Credits: user says 905 left at start of session 2. Stop below 150. Track in manifest `flow_credits_spent/left`.
- Flow limit: 08:50 on 3 Oct a single x2 request (Clara front) failed with the usage limit again (7h20m after the first). Downloading existing images still works under the limit. See README "Questions".
- PROP_PIANO downloaded to `visuals/refs/PROP_PIANO.png` (the parlor variant; brass plate reads "J. & C. FISCHER, NEW YORK" - text in frame, may remake). The other variant (field background) stays in Flow.
- Phase 5: voices listed. Candidates (American, male): Bill `pqHfZKP75CvOlQylNhV4` (old, wise), Brian `nPczCjzI2devNBz1zQrb`, Roger `CwhRBWXzGAHq8TQ4Fs17`, Chris `iP95p4xoKVk53GoZ742B` (also Eric `cjVigY5qzO86Huf0OWal`, Callum `N2lVS1w4EtoT3dr4eOWO`). Free previews in `_variants/voice_previews/`. STOP 3 PASSED: Bill approved. Full narration N01..N10 done and pushed (audio/narration, manifest.narration filled). ElevenLabs characters left: 19339 of 23736. Next: phase 6 (music), test M02 -> STOP 4.
- Claude in Chrome works; project tab opened with tabs_context_mcp(createIfEmpty). Prompt box ~(680,558), send arrow ~(902,595) in the 1366x641 viewport.

## 1. Where things are

### Local (user's Windows PC, user `permr`)
| What | Path |
|---|---|
| Working folder = checkout of THIS branch | `C:\Users\permr\fl_work\wwp` |
| Refs (24 PNG, committed) | `C:\Users\permr\fl_work\wwp\visuals\refs\` |
| Empty dirs for later phases | `...\wwp\visuals\images`, `...\wwp\visuals\video`, `...\wwp\audio\narration`, `...\wwp\_variants` (gitignored) |
| Brief as first downloaded (old) | `C:\Users\permr\fl_work\wwp_brief\` |
| Brief as updated (has music phase) | `C:\Users\permr\fl_work\wwp_brief_new\` (BRIEF.md, shotlist.json, music_cues.md/json, music_elevenlabs.py, tts_elevenlabs.py, narration/) |
| Narration source texts + TTS script (gitignored, needed to run TTS) | `...\wwp\narration\N*.txt`, `...\wwp\tts_elevenlabs.py` |
| Helper scripts (also copied into this branch under `tools/`) | `C:\Users\permr\fl_work\grabn.ps1`, `grab2.ps1`, `upd_wwp.py` (+ `wwp_show.py`, `wwp_init.py`; all copied into `tools/` of this branch, paths inside are hard-coded to C:\Users\permr\fl_work) |
| Browser downloads land in | `C:\Users\permr\Downloads` |
| Tools needed on PATH | git, gh (logged in as `permradar-code`), ffmpeg/ffprobe (`C:\ffmpeg\bin`), python |

Short paths matter: git on Windows fails with "Filename too long" when the repo sits in the long app scratch folder, so keep working in `C:\Users\permr\fl_work\`.

### "flow_automation_tool"
There is NO such tool in my environment. I never used one. Generation is done by driving the Google Flow web UI in the user's own Chrome through the **Claude in Chrome** extension (tools `mcp__claude-in-chrome__*`: tabs_context_mcp, navigate, computer (click/type/key/screenshot/zoom/scroll), find, read_page, get_page_text, file_upload, javascript_tool, browser_batch). The user is logged in to Google Flow (plan PRO). If the extension is "not connected": install https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn and sign in to the side panel with the same account as the app. If a different tool is meant, ask the user.

### Flow project for this film
`https://flow.google.com/project/7a937194-22cf-4e10-a8ea-406b0d82a514` (created 3 Oct 2026, 01:03 local). Contains all rejected variants (they are NOT in git) and the uploaded `CHAR_*_front.png` files.

### How I run a generation in Flow (what works)
1. `tabs_context_mcp(createIfEmpty)`, `navigate` to the project URL. Viewport changes between sessions (1366x641 or 1366x585); always take a screenshot before clicking by coordinates. In the 585-high viewport: prompt box text area ~(640,503), send arrow ~(901,539), "+" (attach) ~(465,538), settings chip (model/ratio/count) ~(815,538).
2. Settings chip -> tabs "Изображение" / "Видео". Image: pick aspect (16:9 first button), model dropdown, count x1..x4. Video: sub-tabs "Кадры" (first/last frame) or "Ингредиенты", aspect, model "Omni 1.1 Flash", 720p, duration 4/6/8/10 s, x1..x4. The chip text shows the current state, cost shows as "Стоимость генерации в бонусах: N".
3. **A NEW PROJECT RESETS THE MODEL TO "Nano Banana 2". Switch it to "Nano Banana Pro" every time** (the brief requires Pro).
4. Attach references: click "+", type part of the file/title name, press **Enter** (adds the highlighted result; fewer clicks than the "Добавить в запрос" button). Wait ~2 s after opening the picker before typing, or the text is lost. The picker search matches asset titles; uploaded files keep their file name (e.g. `CHAR_CLARA_front`), generated ones get auto titles ("Woman posing for portrait").
5. Type the prompt in the text area, click the send arrow. Result appears at the top of the project (newest first), ~20-40 s for images, ~60-120 s for 4-6 s clips.
6. Frames-to-video: in "Кадры" mode click the first-frame slot (and the last-frame slot if the shot has an end frame), search the image title, Enter. Keep the last slot empty if the clip has no end frame.
7. `get_page_text` returns the whole page as text (prompts, statuses, errors, titles) and is the cheapest way to see what succeeded.
8. Failed ("Ошибка") tiles can be removed with the trash icon on the tile (no confirm); the circular arrow retries.

### Uploading local files into Flow without freezing the tab
Clicking Flow's "Загрузить" opens a native Windows file dialog, which the browser extension cannot see; the tab then freezes. Workaround that works:
1. `javascript_tool`: monkey-patch `HTMLInputElement.prototype.click` so a `type=file` input is appended to the page (id `cc_file_input`) instead of opening the dialog, and make `window.showOpenFilePicker` throw AbortError. (Code: 	ools/flow_upload_patch.js in this branch; the patch is lost on page reload.)
2. Click "+" (picker), click "Загрузить" (the click is intercepted), then `find` "cc_file_input file input" -> ref.
3. `file_upload(paths=[...], ref=...)`: **max 10 MB per call**, several files allowed (4 PNGs of ~2 MB each worked).
4. Wait ~8 s for upload processing.

### How I download files and name them
In the image/video "edit view" (click a tile) the download icon is top-right (~(1144,30) for images, ~(1083,30) for videos). Image menu: "1K исходный размер" (first item, ~(1157,66)) is free; "2K повышенное разрешение" is an upscale (not used). Video menu: "270p GIF", "720p исходный размер" (~(1102,106)), "1080p повышенное разрешение" (not used). Files arrive in Downloads as `<title>_<timestamp>.jpg` (images are **JPEG even if you name them .png**; convert) and `.mp4` for clips.
- `grabn.ps1 -Names A,B,C [-Sub visuals\refs]`: takes the N newest image files in Downloads, sorts them by time, converts each to a real PNG with ffmpeg and saves them as `<name>.png` in `C:\Users\permr\fl_work\wwp\<Sub>` (default `visuals\refs`). The order of the Names must match the order I downloaded in. It prints source file name (the title) and size so you can verify the mapping.
- `grab2.ps1 -Name X [-Sub visuals\images] [-Ext png|mp4]`: same for ONE newest download (checks it is < 3 min old).
- `upd_wwp.py`: rebuilds `manifest.json` `refs` from `visuals/refs/*.png` and rewrites README.md (edit its README text before reuse); `wwp_init.py` created the stub manifest/README; `wwp_show.py` prints characters/props/locations from shotlist.json.
- **Arrow-key trick:** in the edit view `ArrowRight`/`ArrowLeft` moves to the next/previous asset of the WHOLE project in the grid order (newest first), not the filtered list. With x2 generations each prompt occupies 2 consecutive slots, so `ArrowRight` x2 moves to the next prompt's first variant. Use `key ... repeat: N`. Then click download. Several downloads can be done in one `browser_batch`, then `grabn.ps1` names them in order.
- The project search box (top) filters by prompt text; `Ctrl+A` there selects all tiles (do not use it).

### ElevenLabs key
The key is set as a Windows **user-level environment variable `ELEVENLABS_API_KEY`** on the user's PC (so new shells and sessions inherit it). Scripts read `os.environ["ELEVENLABS_API_KEY"]`. Never print it, never write it to a file, git or a message. If it is missing in a new session: ask the user to set it (`setx ELEVENLABS_API_KEY ...` or `$env:ELEVENLABS_API_KEY=...` in the same shell) and do not ask them to paste it into chat if avoidable.
Run from the folder that has `narration\` and the script: `cd C:\Users\permr\fl_work\wwp; python tts_elevenlabs.py --check`.

## 2. What is done

- **Phase 0:** orphan branch created, stub README/manifest pushed (commit `d8cf433`).
- **Phase 1, characters, DONE** (commit `bc95955`, 27 files): 8 characters x 3 angles = `visuals/refs/CHAR_{CLARA,LILY,MERCER,PIKE,DEKE,AGATHA,MARSHAL,SAM}_{front,34,full}.png` (1376x768). Front = best of 4 variants; 34 and full were made with the chosen front as reference (2 variants each, first one kept). The user was shown Clara, Mercer, Lily, Pike (and the other four) as contact sheets and **has not yet answered "ок"** (STOP 1 pending).
- **PROP_PIANO:** generated in Flow (2 variants titled "Old upright parlor piano") but NOT downloaded and NOT in git. Find it: project search "piano" or `get_page_text` and scroll; it is the oldest of the "props" batch, just above the first error tiles. Download the better one as `visuals/refs/PROP_PIANO.png`.
- **PROP_HORSE and LOC_STREET, LOC_PLATFORM, LOC_RANCH: failed**, and LOC_PARLOR, LOC_KITCHEN, LOC_BARN, LOC_RIDGE, LOC_BANK were never submitted. The submitted four returned: **"Вы достигли лимита на использование. Повторите попытку позже. Бонусы за эту генерацию контента не списаны."** (no credits charged). It happened about 25 minutes (~01:30 local on 3 Oct) after I had generated ~60 images in the project, 8 of them x4 and ~20 x2. I do not know the reset time; try again after at least 1 hour, ideally the next day. Retry with x1/x2, at most 2-3 prompts at a time.
- Credits spent in this project: **0** (images are free). Video credits have not been touched.

## 3. ElevenLabs (as of 3 Oct 2026)
`python tts_elevenlabs.py --check` -> plan payg, used 2 991 / 23 736, **left 20 745 characters**; the whole narration needs ~7 044 (one pass); N01 alone = 2 260. Resets 2026-10-24T14:11. Not run yet: `--voices`, `--only N01` test (STOP 3), full run. New phase 6 (music) uses the same account; narration has priority for characters.

## 4. What I learned about Flow / the brief that is not in BRIEF.md
- **BRIEF.md was updated during the session:** new **Phase 6, music** (ElevenLabs Music, no Flow credits): `music_cues.md/json` (14 cues, M01a..M13 instrumental, M14 optional end-credit country song with female vocal), `music_elevenlabs.py` (`--check`, `--only M02` test -> **STOP 4**, then all, `--force --seed n` to redo once; M06 must be "Shenandoah" on solo piano or just note it in README), output `audio/music/*.mp3` + `music_log.json`, manifest gets `"music": {"files": [...], "log": "audio/music/music_log.json"}`. Run music only AFTER narration is complete. The "Do not" list now says: no captions/montage, no music beyond the cue sheet. shotlist.json and tts_elevenlabs.py were unchanged (hash-checked). Always re-fetch the brief at the start: `gh api repos/permradar-code/factory-packages/contents/briefs/western_widows_piano -X GET -f ref=tools/montage`.
- **Clip prices (Omni 1.1 Flash, 720p, x1):** 4 s = 7 credits, 6 s = 10, 8 s = 12 (seen in the settings chip). 10 s was not looked at (the brief's clips are 8 or 10 s: check the number in the chip before the first one). 360p is half price (not used). Images 0. 1080p/2K downloads are "upscale" options; I only used the original size.
- **The balance is not shown anywhere I found.** The brief's credit guard ("stop below 150 left") needs a balance: look in the avatar/PRO menu, or ask the user for the number. Earlier packages used 21 (Corinth) and 114 (F-106) credits of ~1050.
- **Generation limits and glitches:**
  - Too many parallel requests -> tiles fail with "Инструмент Flow перегружен. Повторите попытку позже. Бонусы за эту генерацию не списаны." (8 submissions of x4 at once). Keep at most 3-4 pending, wait ~3-4 s between submissions.
  - Usage limit after many images, see section 2.
  - A tile sometimes ends with "Не удалось сгенерировать изображение" (one of the variants), also not charged.
  - In the settings menu the duration can reset (it showed 8 s after a reload): always zoom the chip/menu and read the cost before pressing send for a video.
  - After a reload the "Кадры/Ингредиенты" tab may flip to "Ингредиенты": re-select "Кадры".
  - The prompt box grows upward when references are attached; the send arrow and "+" stay at the bottom.
  - The very first click on a button after a page load is sometimes swallowed: verify with a screenshot.
  - `javascript_tool` is blocked when it would return URLs with query strings/cookies, so image URLs cannot be harvested; download through the UI.
  - Back arrow (top-left, ~(32,30)) returns from the edit view to the project view and keeps the search text; the scroll position resets to the top.
  - Window/viewport size can change mid-session, which shifts every coordinate.
- **Downloaded clips:** F-106 package (separate branch) showed clips have no audio track; whether Omni 1.1 Flash returns audio for speaking characters is exactly what Phase 2 (C11, C13, C34) must find out. Check with `ffprobe -show_streams`.
- **Style notes that worked:** prefix "Front-facing head-and-shoulders portrait, ... plain neutral grey-beige background, even soft light" + `look` + style; for angles "Three-quarter view ... The SAME woman as in the reference image, identical face, hair and clothing: <look>". For aircraft earlier: always repeat a "lock" text; here faces are the lock.
- **User preferences:** Russian, short, no filler; one video generation at a time (not x2/x3); ask before spending beyond what the brief authorises; never touch secrets; deliver by orphan branch; report credits per clip in README/manifest.

## 5. Next steps, in order
1. Wait for the user's answer on STOP 1 (faces of Clara, Mercer, Lily, Pike; contact sheets were sent as images in chat; regenerate any face the user rejects: front first, then the two angles from it).
2. When Flow's limit has reset: finish Phase 1: download PROP_PIANO; generate PROP_HORSE and the 8 LOC_* (look + style from shotlist.json, one image each, x2 to choose); download into `visuals/refs/` as `PROP_PIANO.png`, `PROP_HORSE.png`, `LOC_STREET.png`, ...; run `python tools/upd_wwp.py` (edit its README text first) to refresh manifest `refs`; commit "phase 1: props and locations"; push.
3. Phase 5 in parallel (no Flow credits): `python tts_elevenlabs.py --voices` -> show the user the list (want warm, older American male storyteller); test `--voice <ID> --only N01`; **STOP 3** (user listens to `audio/narration/N01.mp3`); then full run; push mp3 + alignment.json; set `manifest.narration.voice_id`.
4. Phase 2 (after STOP 1 OK): first frames + clips C11, C13, C34 (Clara speaks). Record in README: audio track present? same voice in all three? lines word-for-word and lip-synced? face/hair/dress match? **STOP 2**: user and montage chat choose (a) continue as written or (b) silent clips to be dubbed. Do not generate other clips before that.
5. Phase 3: images I01-I69 (free, 2 variants, refs from `refs`). Phase 4: clips C01-C38 with credit guard (stop below 150 credits; optional C06, C21, C28 last), max 2 regenerations per clip, one video at a time.
6. Phase 6 music after narration is complete (STOP 4 after the M02 test).
7. Final: README (credits per clip + total, rejected items, notes for montage, questions), manifest (`flow_credits_spent`, `flow_credits_left`, scenes in timeline order, `phase: done`), push after every phase. Do not push `_variants/`, narration source txt or secrets.
