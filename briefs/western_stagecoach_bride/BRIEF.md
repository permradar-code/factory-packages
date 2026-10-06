# Production brief: "The Stagecoach Bride" (Tales of Cedar Bluff, film 2, v4, ~18 min, 16:9)

## v4 (6 Oct evening) — what changed since v3
- **New cold open = the title scene:** Caleb walks Rose down Main Street in handcuffs, in her mended wedding dress, the town laughing (C60, C61, C102, C103, C104) → "THREE DAYS EARLIER" → the robbery as one continuous action sequence (C28, C29, C31, C01, C02, C32, C03, C33, C04, C05, C34, C35).
- **Shot IDs are stable.** Kept shots keep their v3 IDs, so frames already made stay valid (C01–C04, C11–C13, I01–I11). New shots: C102–C112 (IDs pinned). Removed: C19, C20, C22, C23–C27, C30 (do not make them). Timeline order = list order in `shotlist.json`, not ID order.
- **Rose's outfits now:** A (wedding dress) on the stage and the mountain up to C42 → B (gingham) from C43 → **A2 = the same wedding dress, cleaned and mended** from C57 (the arrest) through the walk of shame, the jail and the fire (C60, C61-C104 cold open, C62–C69, I06) → B again from I07 (dawn after the fire). Each shot's `rose_outfit` says which; A2 uses the normal `CHAR_ROSE_full.png` ref.
- **Redo I06** (walk close-up): it was made in gingham, now she wears the mended wedding dress.
- **C33 changed:** Amos presses only the brass key into her hand (she already holds the box in C03).
- New payoff scenes: C107 (Mercer sends Crane away), C108 (Rose: "I promised you'd see me in it first"), C109–C110 (Clara silences Agatha). C70, C97, C98 are now core.
- Minutes 2:40–4:20 reworked (less narration): night search on the mountain C107, Rose reads her letter aloud in C11 (now a dialogue clip, the existing C11_first frame still works), C12 and C13 are short on-screen clips without narration.
- Narration renumbered N01–N19 (no audio was made yet). Music cue boundaries in `music_cues.json` still describe v3 sections; the montage re-maps them.


**Project id:** `western_stagecoach_bride_v1`.
**Deliver as an orphan branch** `pkg/western_stagecoach_bride_v1` in `permradar-code/factory-packages`, same layout as `pkg/western_widows_piano_v1` (README.md + manifest.json + `visuals/refs/` + `visuals/images/` + `visuals/video/` + `visuals/hooks/` + `audio/narration/` + `audio/music/`).
**Talk to the user in Russian.**

**Source of truth: `shotlist.json` in this folder** (built by `build_shotlist.py`; `screenplay.md` is the readable version). If they disagree, `shotlist.json` wins. Do not rewrite prompts, lines, names or shot order. If a prompt must be adjusted to work, append to it and record the change in the manifest `note`.

**Setting:** Cedar Bluff, **Colorado, September 1880**, golden aspens. Colorado is a state (since 1876): never write "Colorado Territory" anywhere.

## Current plan (decided 5 Oct evening)
- **Now:** refs → all still images → first and last frames of every clip (all free in Flow credits) → narration and music (ElevenLabs; the user is topping up the account).
- **Video clips: wait.** The user decides later how to make them: Flow subscription (Omni 1.1 Flash), Omni Flash through an API, or Veo. Do not spend Flow credits on video until the user says so. Everything below marked "VIDEO" waits.

## Images: all in Flow, one at a time
- **All images in Flow** (Nano Banana Pro), **strictly one request at a time, x1**: send, wait until it has finished, check it, save it, then the next. Pause 30–60 s between requests, at most ~30 images per hour, log every request with its time.
- Exception: **Rose's reference portrait** (see Phase 1) is also made in ChatGPT for comparison; the user likes ChatGPT quality. Not other images (too slow there).
- If Flow shows the usage limit: stop images, switch to narration/music/downloads, retry after 1 hour with one x1 request. Fallback for stills only: Gemini app (VPN on; the user's normal IP is blocked there).
- Flow tab freezes: fresh tab per step, never open a tile while it renders; switch modes via the `flow-prompt-box-settings` localStorage key (see `pkg/western_widows_piano_v1/HANDOFF.md`).

## References: use them to the maximum
- Every image and every clip frame has `ref_files` in the shotlist. **Always attach all of them.** Upload all refs into the Flow project once and reuse them.
- Recurring residents (Clara, Lily, Mercer, Agatha, Marshal Hart), Mercer's horse, main street, ranch, kitchen, barn, parlor: **reuse the approved refs from film 1** (`pkg/western_widows_piano_v1/visuals/refs/`, Flow project `7a937194-22cf-4e10-a8ea-406b0d82a514`). Do not regenerate them.
- Music M02, M04, M05, M11, M14: copy from film 1 (`reuse_from`), do not generate.
- **Rose's outfits** (v4, see above): A up to C42, B from C43, A2 (mended wedding dress) from C57 to the jail fire, B again from I07. C11 and C13 (St. Louis, packing the dress) use her grey travelling dress. Every shot already says which (`rose_outfit`) and attaches the matching full-body ref (`CHAR_ROSE_full.png` or `CHAR_ROSE_full_B.png`).
- **Mostly video:** 102 core clips (606 s), 70 of them with dialogue, 21 action clips; only 11 still images. Clips marked `"broll": true` are silent and play under the narrator. The film is all video until about minute 6.
- **Tone:** serious, grounded drama; no comedic voices or overacting (a viewer of film 1 called the comic auctioneer opening "a buffoon story"). Agatha's voice is now cold and haughty, never shrill.

## Rose must be beautiful (and Flow must not choke on it)
She is the face of the film and of the thumbnail: unmistakably lovely, warm, feminine. Her `look` already describes specific original features (oval face, high cheekbones, large dark-brown eyes, faint freckles, a tiny pale scar on the left eyebrow) instead of vague words.
- If Flow refuses with a celebrity / public-figure message, **change one feature** (brow shape, hairline, freckles, chin) and retry. Never remove her beauty, never work around the filter.
- Reject candidates that look like a known actress, look doll-like or plastic, or look older than 24.

---

## Phase 0: setup
Create the orphan branch `pkg/western_stagecoach_bride_v1` with stub README.md and manifest.json (schema as in film 1, `project_id` = `western_stagecoach_bride_v1`). Local working folder mirroring the branch; copy the reused images and music. Push after every phase.

## Phase 1: new refs (free)
Prompts are ready in `shotlist.json` → `ref_prompts` (23 files). For each person: make the `_front` first (3–4 variants, pick the best), then `_34`, `_full` (and Rose's `_full_B`) **with the chosen front attached as reference** (`use_ref`).
**Rose:** 2 front variants in Flow + 2 in ChatGPT (same prompt). Show all four to the user; they pick.
**STOP 1.** Push, show the user Rose (front + both outfits), Caleb, Crane, Buck, Amos and the stagecoach; wait for "ок". Faces cannot change later.

## Phase 2: still images (free)
All `type: image` steps except the reused ones: prompt = `full_prompt`, refs = `ref_files`. One variant at a time; regenerate up to 3 times if needed. Reject: wrong face, wrong Rose outfit, broken hands, any text or lettering, modern objects, company names on the stagecoach.

## Phase 3: clip frames (free)
For every clip (core first, then optional): first frame from `start_frame_full_prompt` → `visuals/images/<ID>_first.png`. For clips that have `end_frame_prompt` (all the action clips) also the last frame from `end_frame_full_prompt` → `<ID>_last.png`, made **with the first frame attached as reference** so the people, costumes, place and light match. First and last frame together keep the action clips from drifting.
Action clips (`action_shot: true`): the first frame must already show motion (dust, flying hair, a horse mid-stride), never a calm pose.
**STOP 2.** Push and show the user the cold-open frames C01–C04 (first + last).

## Phase 4: narration (ElevenLabs, no Flow credits)
Script `tts_elevenlabs.py`; the key only from the environment variable `ELEVENLABS_API_KEY` (never print it, never write it to files or git).
1. `python tts_elevenlabs.py --check`: report characters left vs needed (**~6,000 characters** for one pass of N01–N21).
2. `python tts_elevenlabs.py --voice pqHfZKP75CvOlQylNhV4` (Bill, same as film 1) for all blocks.
3. Push `audio/narration/*.mp3` and `*.alignment.json`.

## Phase 5: music (ElevenLabs Music)
Copy the 5 reused cues first. Then `python music_elevenlabs.py --check`, `--only M01` (test), **STOP 3** for the user to approve the action sound, then the rest. Push `audio/music/*.mp3` + `music_log.json`.

## VIDEO (waits for the user's decision)
| Group | Clips | One take in Flow credits |
|---|---|---|
| Core (`priority: core`) | 97 (592 s) | 955 credits, or ≈ $59.2 via API at $0.10/s |
| Optional | 4 (22 s) | 37 credits |
| Hooks for Shorts (9:16) | 3 | 21 |
The Flow balance (~397) covers about 40 core clips. The user decides the split: Flow for part, Omni Flash / Veo via API for the rest.
Order when it starts: cold open C01–C04 first, then core in timeline order, then optional, then hooks. Frames-to-video with first + last frame where the model supports it. One speaker per clip; lines word for word; reject a take if a face morphs, the wrong person talks or a line changes. At most 1 regeneration per clip (2 for C01–C04 and C92). In Flow: stop if the balance would fall under 150.

## Rules that do not change
- No blood close-ups, no gore. When Caleb is hit (C69) he clutches his shoulder.
- Faces original; never work around the celebrity filter.
- No text, titles, logos or watermarks in frames.
- Do not make captions or the montage.
- Do not push `_variants/` or any secret. Files over 100 MB never go into git.
- Do not continue past a STOP without the user's answer.

## manifest.json / README.md
Same schema and rules as film 1 (`briefs/western_widows_piano/BRIEF.md`). Scenes in timeline order; skipped shots stay with `"type": "skipped"` and a reason. Add `"refs"`, `"frames"` (first/last per clip), `"music"`, later `"hooks"`. README: what was made with what, regenerations and why, notes for the montage, questions.
