# HANDOFF: western_stagecoach_bride_v1 (5 Oct 2026, end of session 1)

Talk to the user in Russian, briefly. Branch `pkg/western_stagecoach_bride_v1` in `permradar-code/factory-packages`; local worktree `C:\Users\permr\fl_work\wsb` (main checkout `C:\Users\permr\fl_work\wwp` stays on the film-1 branch). Source of truth: `briefs/western_stagecoach_bride/shotlist.json` + `BRIEF.md` on `tools/montage` (re-read with `git show origin/tools/montage:<path>`; local copies in `_variants/brief/`, gitignored).

## Status
- Phase 0 done. Phase 1 (23 new refs + 15 reused) done and APPROVED by the user at STOP 1 (all images of refs in ChatGPT, 1672x941).
- Phase 2 (stills): done I02, I03, I04 (+ I01, I45 reused). Pending: 55 images, order in `_variants/order.json` (timeline order, not ID order). Next: I05.
- Phases 3-5 not started. VIDEO waits for the user's decision (no Flow credits for video).
- Flow credits spent: 0.

## User decisions
- Rose face = ChatGPT variant 1. "Where it works better, do it there": ChatGPT for faces/refs, Flow/Gemini only if faster.
- Buck's scar on the wrong cheek and Rose's faint brow scar were accepted.

## What works (ChatGPT, tested)
1. `python tools/build_stage.py I05 ...` makes `_variants/stage/<ID>/`: `00_prompt_<ID>.txt` (scene + numbered ref list) and numbered 1024px jpg refs from `_variants/up/` (rebuild `up/` from `visuals/refs` with PIL, thumbnail 1024).
2. In a ChatGPT chat: upload those files (file_upload to the "Прикрепить файлы" input found by `find`, or to your own `<input type=file multiple>` and paste them into `.ProseMirror` via a ClipboardEvent), type "New separate image. Generate ONE image exactly as described in the attached file 00_prompt_<ID>.txt, using the attached reference images as described there. Output a single wide 16:9 landscape image.", Enter.
3. Wait ~90-100 s (slower in long chats: new chat every 3-4 images; a fresh chat is ~70-90 s). Look at the screenshot: image must be finished (no "%").
4. Click the image (668,245) to open the viewer, click download (1164,26), Escape. `tools/grab.ps1 -Dest visuals\images\<ID>.png` converts the newest file in Downloads (it polls up to 90 s).
5. ChatGPT limit: 10 files per message. Shots with 10-11 refs (I31, I44, ...) need a merged ref sheet for minor characters.

## What burned us
- NEVER click (1164,26) unless the image viewer is open: on the chat page that spot is the "Поделиться" button and creates a PUBLIC link (happened once; I deleted it in "Общие ссылки", the user's old links were untouched).
- After `navigate` the first typing/clicking is swallowed: do the typing in a second call.
- Closing a Chrome tab makes the extension lose the whole tab group; the other tabs become uncontrollable. Do not close tabs; open new ones via `tabs_context_mcp {createIfEmpty:true}`.
- The extension disconnects now and then ("not connected"): retry once, then stop and tell the user.
- Flow (new project 25886d44-bf88-49ae-b9ca-00ac2dc0467f): tabs freeze; attaching refs through the "+" picker mis-clicks into tiles and opens editors. Uploaded 33 refs there already (jpg names like CHAR_ROSE_front.jpg). Not faster than ChatGPT in practice. Gemini not tried.
- Local servers cannot be fetched from https pages (blocked); pass data through `file_upload` instead.

## Open ChatGPT chats (user can see them in history)
"Generate Image" (I02-I05 chat; I05 was stuck at 99%) and "ChatGPT" (I05 files pasted, not sent). Check the history before regenerating I05.
