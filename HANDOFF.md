# HANDOFF: Shorts factory + montage (as of 2026-10-02, 14:40 MSK)

This document carries over the context of a previous long chat. It is everything a new chat needs to continue the work.
Everything below is in English except where quoted; talk to the user **in Russian**, briefly, without filler.

---

## 1. Who we work with and the rules

- The user runs several YouTube channels: aviation **Not In The Manual**, **Strange But Real** (SBR, shorts), **Мой Астролог** (astrology), and others.
- **Budget:** the user may auto-approve factory jobs up to **$3 per video**. Anything above that needs a question. **Right now money is tight**: ask before every new generation.
- **Hard prohibitions:**
  - Do not touch the astrology pipeline.
  - Do NOT restart the MCP/OAuth control plane (service `mcp`). Restarting `moiastro-studio` is allowed.
  - Do not merge `feature/montage-assets-v3` into `main` without an explicit "ок" from the user (still not given).
  - Never print or commit secrets from `/etc/moiastro-secrets`.
  - Factory code changes only with the user's approval.
- **Lessons for Shorts (from the stats):**
  - The first frame must already have motion plus a visual paradox, understandable in 1 second without sound. Text on the first frame must be visible from frame 0.
  - The first spoken words are the hook. No dates or intros.
  - One clear "impossible action" beats a "beautiful unusual place". SBR: the FLIP ship flipping upright got 77k; places got 1.2–2k; Elbląg with a girl intro got 264 with 76% swiping away.
  - No presenter girl.
  - The story must show the full cause-and-effect cycle on screen. For the bridge: it sinks → a ship passes over it → it rises.
  - **Before generating real objects, look at real photos.** Mistakes so far: C-130 drawn with a T-tail; the Corinth bridge drawn along the canal and among cliffs.
- **Stats:** C-130 / SR-71 aviation Shorts had 54–59% "continued watching" (target ≥70%). The SR-71 long video: AVD 3:51 of 9:38 (good), but few impressions so far.

## 2. Infrastructure

- **Factory** = VPS `/opt/moiastro-engine`, MCP connector **moi_astrolog**.
  - Services: studio :8788 (runs the montage_assets jobs), provider worker :8770, mcp.
  - The server's git is on `main` 49b617e, but the montage files in the working tree are copied from the branch **`feature/montage-assets-v3` (HEAD 36beaa1)** on GitHub `permradar-code/moiastro-engine`.
- **Server commands** go through `codex_run`:
  - not root, use `sudo -n`;
  - `rm -rf` is forbidden, use `find D -depth -delete`;
  - limit 180 s.
- **Tests** go through `exec_submit` with argv strictly `["python","-m","pytest","-q", <files>]` and `expected_head` 49b617e…; read results with `exec_status`.
- **Deploying code:** commit to the feature branch → codex: `git fetch origin feature/montage-assets-v3` + `git show FETCH_HEAD:<path> > <path>` for each file → tests → `sudo -n systemctl restart moiastro-studio`.
- **Two pre-existing test failures**, not ours: `test_studio_exposes_montage_prepare_route` and `test_fuzzy_whisper_spelling_can_still_match`.

### montage_assets mode (generates raw assets only)

1. `montage_assets_prepare(job_json)` → cost estimate + fingerprint.
2. `montage_assets_approve(project_id, fingerprint)` → generation: references → TTS → music → Whisper word timings → Gemini images → Veo.
3. `montage_assets_status`; `montage_assets_repair(project_id, [asset_ids])` resets FAILED assets.
4. **Exporting the package to GitHub is manual** (auto-export is not wired): codex_run
   `.venv/bin/python -m app.production.montage_assets_github <project_id>`
   → orphan branch `pkg/<project_id>` in `permradar-code/factory-packages`.
5. **Fetch it locally:**
   `git fetch --depth 1 origin pkg/X && git --work-tree=DIR checkout FETCH_HEAD -- . && git reset -q`.

**Input fields** (see `docs/montage_assets_input.md` in the repo):
- `aspect_ratio` 9:16 or 16:9;
- `voice` {voice: onyx/cedar, speed, instructions};
- `music` {prompt, model lyria-3-pro-preview, duration_s}. Lyria ignores the duration, trim it in montage;
- reference `prompt_raw: true`;
- **reference `files: {"<view>": "<source>"}`**: a real photo as the reference, costs $0;
- shot `end_image_prompt_full`: last frame for Veo;
- **shot `image_file` / `end_image_file`**: your own exact keyframes; Veo animates between them.

**Sources:**
- `https://…`;
- `stage:<path>`: a file in `/opt/moiastro-engine/projects/_sources/<path>`. Put it there via codex: clone the branch `ref/...` of the factory-packages repo, `cp`, then `chown moiastro:moiastro`;
- `git:<branch>:<path>`: does not work under the studio user (no SSH key), use `stage:`.

**Approximate prices:**
- Gemini image $0.04;
- Veo fast 720p $0.08/s (generates 4/6/8 s);
- OpenAI reference ~$0.18;
- TTS/Whisper: cents;
- Lyria ~$0.06.

**Known issues:**
- TTS (gpt-4o-mini-tts) **drops the final sentence** on long scripts: happened twice on C-130. Put the last line on an end card, or fix it in the factory.
- Whisper splits `C-130` into `C`/`130` and garbles names. Fix `words.json` by hand (example: `patch_c130_words.py`).
- Veo often ignores direction (the bridge went UP instead of down). The cure is your own end frame via `end_image_file`.

## 3. Montage (on the agent side, no CapCut)

All scripts are in the branch **`tools/montage`** of `permradar-code/factory-packages`.

- **`assemble_short.py <pkg> <out.mp4> --config cfg.json`**:
  - scenes come from manifest.json (`index, shot_id, start, image|video`);
  - Ken Burns for images, trim/slow-mo/push for video;
  - ASS captions in the Inter Display Black font, 3 words per line, the current word in yellow; caption width is measured and long lines are split;
  - labels styles: `Label` (top plate), `Stat` (big yellow number), `End` (centred card, `\n` for line breaks); a label with start=0 is visible on the very first frame;
  - sfx `whoosh`/`splash`;
  - music ducked under the voice, loudnorm −14 LUFS.
- **`combine_pkgs.py`** merges a base package with a fix pass (C-130 v1+v2).
- **Configs:** `configs/`. **Factory inputs:** `inputs/`.
- **The chat only accepts files up to ~30 MB.** Compress with two-pass ~2 Mbps:
  `ffmpeg -i in.mp4 -c:v libx264 -b:v 2050k -pass 1 … && … -pass 2 … -c:a copy`.
- **Vertical frame from a 16:9 clip:** blurred background plus the clip scaled to 900 px height and cropped to 1080, placed at y=230. Captions then sit below the subject.

## 4. Videos: status

### Not In The Manual (aviation, English)
- **C-130 lands on USS Forrestal (1963)**: done, `No_Hook_C130_Carrier_Landing_v2.mp4`, 1:34. The opening is cut to start straight on the paradox ("A four-engine cargo plane is lining up to land on an aircraft carrier"), first frame is a top-down view. **Planned to publish tonight at 20:00 MSK.**
  - Title: "The Plane That Landed on an Aircraft Carrier… Without a Hook".
  - Tags, description and pinned comment were given to the user.
  - Related video: the long SR-71.
  - Cost ~$4.8.
- **F-106 "Cornfield Bomber" (1970)**: script and 20-shot plan **ready, NOT launched** (`inputs/input_f106_v1.json`).
  - Hook: "This pilot just ejected. His jet didn't."
  - Finale: Foust flew this same jet again 9 years later, "He finally got back in it".
  - Budget options: A $2.75 / B $2.27 / **D $1.59 (one clip, on the hook only)** / C $1.07.
  - Waiting for money and the user's choice.
  - Facts: Wikipedia "Cornfield Bomber", f-106deltadart.com.
- **Next topics:** F-15 with one wing (1983), Pardo's Push, Gimli Glider.
- **Competitor WWIDO Infinite Learning** (MiG-21 short, 1.35M views): precision comes from a 3D model (DCS/Blender) plus CAD animation and HUD graphics, not from AI. Idea for the future: 3D aircraft models rendered in Blender on the server as keyframes.

### Strange But Real (shorts 10–15 s)
- **Corinth Canal sinking bridge**: v3 delivered (`This_Bridge_Sinks_On_Purpose_v3.mp4`). The user will publish it but is unhappy: it is unclear, there is no ship passing over, and the rise looks like a float.
  - **v4 idea:**
    - a ship-passing shot made with our own keyframes: start = `hook_end` (deck gone, yacht waiting); end = a composite with the yacht moved past the abutments;
    - the rise = the sinking clip played in reverse.
  - Cost ~$0.4. **Waiting for money.**
  - Materials:
    - photo: branch `ref/corinth` (`bridge_clean.png`, CC BY-SA, Aspasia Covaios — credit it in the description);
    - packages: `pkg/sbr_corinth_bridge_v2`, `pkg/sbr_corinth_hook_v3`;
    - staged files on the server: `_sources/corinth/{bridge.png,hook_end.png}`.
- **Other ideas** (one machine doing an impossible action): a ship launched sideways; a ship beached at full speed for scrapping (Alang); the Magdeburg water bridge; the Falkirk Wheel.

## 5. NEXT STEP: automate via Google Flow (user's subscription)

- The user has **Google AI Pro**, ~1050 Flow credits. Images are free there, video costs credits (Veo 3.1 / Omni Flash; 4/6/8/10 s; Frames mode = first + last frame; 360p drafts at half price).
- **Goal:** move the expensive part (images and video) to Flow. Keep the cheap part in the factory: TTS, Whisper timings, Lyria.
- **Option A (recommended, start with this):** a chat in the Claude desktop app **linked to the user's computer**. The agent drives Flow in the user's own browser (Claude in Chrome or the built-in pane):
  - uploads keyframes;
  - selects Frames mode;
  - writes the prompt and generates;
  - downloads to a folder;
  - picks up the files via the device bridge and edits.
- **Option B:** community MCP servers that drive a browser, e.g. github.com/luongvietan/google-flow-mcp, vietlh1505/google-flow-browser-mcp, daniazar/google-flow-mcp, hitjcl/google-flow-mcp.
  - They are 0-star forks and some hide the webdriver flag.
  - **Before installing, read the whole code** (risk of cookie theft from a logged-in Google session).
  - Run only on the user's PC, never on the VPS.
- **Risk:** automation violates Google's terms, so a block on the account is possible, and that account holds YouTube and Gmail. Generate one at a time, no batches. If possible, use a separate account: check whether Pro can be shared through a family group.

## 6. Other open items

- Merging `feature/montage-assets-v3` into main: waiting for "ок".
- SBR OAuth was never completed (needs the user's browser login); the token file `youtube_strange_but_real_token.json` does not exist. Public stats can be read through `/etc/moiastro-secrets/youtube_token.json` (Data API).
- NexLev weekly limit resets on Oct 4.
- Leftover project `sbr_v3_smoke` is in AWAITING_APPROVAL; do not approve it.
