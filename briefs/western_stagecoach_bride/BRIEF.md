# Google Flow brief: "The Stagecoach Bride" (Tales of Cedar Bluff, film 2, ~25 min, 16:9)

**Project id:** `western_stagecoach_bride_v1`.
**Deliver as an orphan branch** `pkg/western_stagecoach_bride_v1` in `permradar-code/factory-packages`, same layout as `pkg/western_widows_piano_v1` (README.md + manifest.json + `visuals/refs/` + `visuals/images/` + `visuals/video/` + `visuals/hooks/` + `audio/narration/` + `audio/music/`).
**Generate ONLY:** new refs, images, clips, hook clips, narration and new music cues. Montage, captions and packaging are done by the montage chat.
**Report Flow credits** per clip and in total in README.md and manifest.json.
**Talk to the user in Russian.**

**Source of truth: `shotlist.json` in this folder** (built by `build_shotlist.py`; `screenplay.md` is the readable version in Russian/English). If they disagree, `shotlist.json` wins. Do not rewrite prompts, lines, names or shot order. If a prompt must be adjusted to work, append to it and record the change in the manifest `note`.

**Setting:** Cedar Bluff, **Colorado, September 1880**, golden aspens. Colorado is a state (since 1876): never write "Colorado Territory" anywhere.

## What is new in this film (read first)
1. **Structure.** Cold open C01–C04 is the stagecoach attack, cut before the outcome; then "TEN DAYS EARLIER". Action clips are marked `"action_shot": true`: their video prompts demand that the motion is already happening in the first frame. Make their first frames mid-action too (`start_frame_full_prompt` says so).
2. **Reuse from film 1, do not regenerate:**
   - Character refs for Clara, Lily, Mercer, Agatha, Marshal Hart; refs for the horse, main street, ranch, kitchen, barn, parlor: `pkg/western_widows_piano_v1/visuals/refs/`. The `ref_files` field of every shot already points there. They are also uploaded in the Flow project `7a937194-22cf-4e10-a8ea-406b0d82a514`; you can work in the same project.
   - Images `I01` and `I45`: copy from the film 1 package (`reuse_from` field) into `visuals/images/` under the new names. Do not generate them.
   - Music cues with `reuse_from` in `music_cues.json` (M02, M04, M05, M11, M14): copy the files from `pkg/western_widows_piano_v1/audio/music/` into `audio/music/` under the new IDs before running the music script.
   - Narrator: the same voice **Bill** (`pqHfZKP75CvOlQylNhV4`), same settings as film 1.
3. **Rose has two outfits.** Outfit A (ivory lace wedding dress, short veil pinned back) in every Rose shot up to and including **I20**. Outfit B (faded green gingham dress, low bun) from **I22** on (I22 shows the green dress folded on a chair; Rose is still in a nightgown under a blanket there). Make two full-body refs: `CHAR_ROSE_full.png` (A) and `CHAR_ROSE_full_B.png` (B); for shots after I20 attach `_full_B` instead of `_full`.
4. **Image IDs are not in timeline order** (I46–I60 were added later). Always follow the order of `timeline`, not the numbers.
5. **Retention version (v2).** The story is written so every block ends on a hook. Keep the order exactly; the montage depends on it. Key setups and payoffs: the watcher at the station (I48) → the roan's broken horseshoe (I53, N07c night fight in the barn, I29, C25) → the handwriting proof (I56).
6. **Violence rule:** gunfights and fire, but no blood close-ups, no gore. When Caleb is hit (C23) he clutches his shoulder; no blood spray.

## Credits (Flow balance about 397 on 5 Oct)
| Group | Clips | One take |
|---|---|---|
| Core clips (`"priority": "core"`) | 26 | 244 credits |
| Optional clips | 10 | 100 credits |
| Hook clips for Shorts (`hooks`, 9:16) | 3 | 21 credits |

- **Stop line: 150 credits.** Check the balance before every video. If the next generation would take it under 150, stop and report what is done and what remains.
- Core clips first, in timeline order, **except the cold open C01–C04, which you make first of all** (it decides how good the film is).
- **Regenerations:** at most 1 per clip, at most 2 for C01–C04 and C31. If a clip still fails, keep the best take and describe the problem in the note; the montage can cover it with an image.
- Optional clips and hooks only after all core clips, and only if credits stay above 150 (the user may add credits or switch some clips to Veo via Vertex; ask before spending on optional work).

## Format and tools (decided on film 1)
- 16:9, 720p, 24 fps; Omni 1.1 Flash for video. Hooks: **9:16** (Flow offers 9:16 for Omni 1.1 Flash; first frames 9:16 too).
- Still images `I..` → **Gemini app** (2752×1536), new chat every 7–8 images. Clip first frames `C.._first` → **Flow images**. Video → Flow only.
- **Pacing, strict:** one request at a time, x1, wait until it finishes, pause 30–60 s, at most ~30 images per hour, log every request with time. If the limit message appears: stop image work, switch to narration/music/downloads, retry after 1 hour with one x1 request.
- Flow tab freezes: fresh tab per step, never open a tile while it renders; switch modes via the `flow-prompt-box-settings` localStorage key (see `pkg/western_widows_piano_v1/HANDOFF.md`). Set LANDSCAPE before opening settings, then pick 9:16 inside the Video popup.
- One speaker per clip (already split in the shotlist). Every video prompt says who speaks and that everyone else keeps quiet.
- Celebrity filter: faces must be original. If it triggers, change the face, never work around the filter.

---

## Phase 0: setup
1. Create the orphan branch `pkg/western_stagecoach_bride_v1` with stub README.md and manifest.json (schema as in film 1, `project_id` = `western_stagecoach_bride_v1`).
2. Local working folder mirroring the branch layout; copy the reused images and music (see above). Push after every phase.

## Phase 1: new refs (images, free)
New entries without `reuse_refs`: CHAR_ROSE (front, three-quarter, full A, full B), CHAR_CALEB, CHAR_CRANE, CHAR_BUCK, CHAR_AMOS (front, three-quarter, full), PROP_STAGE, PROP_BOX, LOC_PASS, LOC_JAIL, LOC_CANYON, LOC_CRANE, LOC_STATION (one image each).
Faces: 3–4 front variants, pick the best, then the other angles with the chosen front as reference.
**STOP 1.** Push, show the user Rose (front + both outfits), Caleb and Crane, wait for "ок".

## Phase 2: voice test (3 clips)
C09 (Rose), C05 (Caleb), C15 (Crane): first frame + video. Check: audio present, line word-for-word, lip sync, face matches refs. Record in README.
**STOP 2.** User decides: continue, or adjust voices/faces.

## Phase 3: cold open
C01–C04 (action). First frames already in motion. Up to 2 regenerations each.
**STOP 3.** Push and show the user the four clips; this sets the bar for the rest.

## Phase 4: images (free)
All `type: image` steps except the reused ones: prompt = `full_prompt`, references = `ref_files`. 2 variants, keep the best. Reject: wrong faces, broken hands, any text, modern objects, wrong Rose outfit.

## Phase 5: core clips
All remaining `priority: core` clips in timeline order: first frame (`start_frame_full_prompt`, refs from `ref_files`, up to 4 tries), then Frames-to-video with `video_prompt`, `duration_s`. Reject a take if the face morphs, the wrong person speaks, a line is changed or extended, extra fingers, text on screen.

## Phase 6: narration (ElevenLabs, no Flow credits)
Script `tts_elevenlabs.py`, key only from the environment variable `ELEVENLABS_API_KEY` (never print it, never write it to files or git).
1. `python tts_elevenlabs.py --check`: report characters left vs needed (**~16,800 characters** for one pass of N00–N21; the user is topping up the account).
2. `python tts_elevenlabs.py --voice pqHfZKP75CvOlQylNhV4` for all blocks (existing ones are skipped). No voice test needed: same voice as film 1.
3. Push `audio/narration/*.mp3` and `*.alignment.json`.

## Phase 7: music (ElevenLabs Music)
First copy the 5 reused cues (see above). Then `python music_elevenlabs.py --check`, `python music_elevenlabs.py --only M01` (test), **STOP 4** for the user to approve the action sound, then `python music_elevenlabs.py` for the rest. Push `audio/music/*.mp3` + `music_log.json`.

## Phase 8 (only with spare credits): optional clips, then hooks
Optional clips in timeline order while the balance stays above 150. Then the 3 hooks from `hooks` in `shotlist.json` (9:16, files in `visuals/hooks/`). Ask the user before starting this phase.

## manifest.json / README.md
Same schema and rules as film 1 (`briefs/western_widows_piano/BRIEF.md`, sections "manifest.json" and "README.md"). Scenes in timeline order; skipped shots stay with `"type": "skipped"` and a reason. Add `"hooks"` and `"music"` sections. README: credits per clip, regenerations and why, notes for the montage, questions.

## Do not
- Change lines, names, plot or shot order.
- Put text, titles, logos or watermarks into frames; no company names on the stagecoach.
- Make captions or the montage.
- Push `_variants/` or any secret.
- Continue past a STOP without the user's answer.
