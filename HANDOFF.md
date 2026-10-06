# HANDOFF: western_stagecoach_bride_v1 (6 Oct 2026, session 2) — shotlist v3

Talk to the user in Russian, briefly. Branch `pkg/western_stagecoach_bride_v1` in `permradar-code/factory-packages`; local worktree `C:\Users\permr\fl_work\wsb` (main checkout `C:\Users\permr\fl_work\wwp` stays on the film-1 branch). **Source of truth is shotlist v3** (tools/montage commit 316323b, 6 Oct; 101 clips, 11 stills, 22 narration blocks, ~18 min). Re-read with `git show origin/tools/montage:briefs/western_stagecoach_bride/shotlist.json` (and BRIEF.md); local copies in `_variants/brief/` (gitignored). The old v2 (60 stills) is obsolete.

## Status
- Phase 0, 1 (refs 38 files, approved at STOP 1): done.
- Phase 2 (v3 stills): **I01–I11 done** (visuals/images/I01..I11.png, ChatGPT, 1672x941).
- v2 stills reused as first frames: I02→`C12_first.png` (ok), I03→`C11_first.png` (ok, grey travel dress), I04→`C13_first.png` (redone 6 Oct in Flow: hands folding the dress into a carpetbag).
- Phase 3 now: **only cold open C01–C04 (first + last), then STOP 2.** STOP 2 answered 6 Oct: approved I01-I11, C01, C02, C03_first, C04_last; C04_first, C03_last, C13_first were redone (waiting for the user's look). C01_last and C02_last are NOT used: video for those clips is first-frame only. C02_last, C03_last, C04_first/last came from Flow because ChatGPT's file-attachment limit was reached until 15:09 6 Oct.
- Flow route that works (new project 25886d44..., refs already uploaded by name): fresh tab, click the prompt bar once to wake the page, click '+' (457,538), TYPE the file name (search is focused), Enter; repeat per ref; type prompt; send at (896,540); ~30 s; open tile, download icon (1144,30) -> '1K' (1188,70). A last frame can be made by EDITING the first-frame tile (type the change in the edit bar, send at (806,535)). Tabs freeze often: use a fresh tab, never close old ones. Last frames are made with the first frame attached (`tools/build_frame.py C01:last` builds the package, first frame = `01_FIRST_FRAME.jpg`).
- The other ~110 frames are NOT to be made here: the user plans to generate them via API on the server. Do not start them.
- Phases 4 (narration), 5 (music), video: not started. Flow credits spent: 0.

## Decisions
- All stills in ChatGPT (user: "where it works better"). Flow project 25886d44-... is empty apart from a few uploads; do not use it.
- Rose face = ChatGPT variant 1; Buck scar side and Rose's faint brow scar accepted.

## ChatGPT workflow (tested, ~1.5-3 min per image; two tabs in parallel work)
1. `python tools/build_stage.py I05` (stills) or `python tools/build_frame.py C02:first C02:last` (frames) -> `_variants/stage/<ID>/` with `00_prompt_<ID>.txt` and numbered 1024px refs (`_variants/up/`, rebuild from `visuals/refs` with PIL thumbnail 1024 if missing).
2. New chat in the tab (`navigate https://chatgpt.com/`, new chat every 2-3 images). `find "Прикрепить файлы"` -> ref, `file_upload` the files (max 10 incl. the txt). Then click the composer and type "New separate image. Generate ONE image exactly as described in the attached file 00_prompt_<ID>.txt, using the attached reference images as described there. Output a single wide 16:9 landscape image." **The first typing after a page load is swallowed: look at a screenshot and repeat the click+type if the text is missing.** Enter to send. (A leftover draft may appear: ctrl+a before typing.)
3. Wait until the image is finished (no "%", "Редактировать" button visible), click the image to open the viewer, **verify with a screenshot that the viewer is open**, click download at (1164,26), Escape. `tools/grab.ps1 -Dest visuals\images\<ID>.png` (polls the newest file in Downloads).
4. Check faces vs refs, no text, correct outfit; max 3 regenerations.

## What burned us
- (1164,26) outside the viewer is "Поделиться" and creates a PUBLIC link (once; deleted in "Общие ссылки").
- Never close Chrome tabs (the extension loses the tab group); open new ones via `tabs_context_mcp {createIfEmpty:true}`. Extension disconnects sometimes: retry once, then stop and tell the user.
- A local web server cannot be reached from https pages; pass files via `file_upload`.
- ChatGPT limit: 10 files per message.
- Flow tabs freeze; Gemini not tried.
