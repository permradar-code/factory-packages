# Google Flow brief: "The Widow's Piano" (western drama, long-form ~16 min, 16:9)

**Project id:** `western_widows_piano_v1`.
**Deliver as an orphan branch** `pkg/western_widows_piano_v1` in `permradar-code/factory-packages`, in the same format as `pkg/nitm_f106_flow_v1` (README.md + manifest.json + `visuals/images/` + `visuals/video/`), plus `visuals/refs/` and `audio/narration/`.
**Generate ONLY the visuals and the narrator voice.** Montage, music, captions and character-voice decisions are done by the montage chat.
**Report Flow credits spent** (per clip and total) in README.md and manifest.json.
Talk to the user in Russian.

**Source of truth: `shotlist.json` in this folder.** It has every character, prop and location (with exact looks and voices) and the full timeline with ready prompts. `screenplay.md` is the readable version. If they disagree, `shotlist.json` wins. Do not rewrite prompts or dialogue lines. If a prompt has to be adjusted to work, append to it and record the change in the manifest `note`.

## Format
- 16:9, 720p, 24 fps. Video model: **Omni 1.1 Flash** (same as the F-106 and Corinth packages). Images: **Nano Banana Pro**, 16:9.
- Clip length is in each clip's `duration_s` (8 or 10 s). Images are free; video costs credits.
- Era lock for EVERY prompt (already inside the prompts): 1879 Colorado Territory, period clothing, no text, no logos, no watermark, no modern objects.

---

## Phase 0: setup
1. Create the orphan branch `pkg/western_widows_piano_v1` with a stub README.md and manifest.json (schema below).
2. Local working folder, e.g. `~/Videos/western_widows_piano/`, mirroring the branch layout:
```
visuals/refs/     CHAR_CLARA_front.png, CHAR_CLARA_34.png, CHAR_CLARA_full.png, PROP_PIANO.png, LOC_RANCH.png ...
visuals/images/   I01.png ... I69.png, and clip frames C01_first.png (C01_last.png only if a clip has an end frame)
visuals/video/    C01.mp4 ... C38.mp4
audio/narration/  N01.mp3 + N01.alignment.json ...
_variants/        rejected versions (NOT pushed)
```
3. File names strictly by the IDs in `shotlist.json`. Push after every phase (commit per phase, not one giant commit).

## Phase 1: references (images, free)
For every entry in `characters`, `props` and `locations` (including `CHAR_SAM`, used in flashbacks):
- **Characters:** front portrait, three-quarter, full body. Prompt = `look` + `style`, plain background, even light. Make 3–4 front variants, pick the best, then generate the other two angles **with the chosen front image as the reference** so the face matches.
- **Props and locations:** one image each.

**STOP 1.** Push, then show the user Clara, Mercer, Lily and Pike and wait for "ок". These faces carry the whole film and cannot be changed later.

## Phase 2: voice and face test (3 clips)
Make first frames and clips **C11, C13, C34** (Clara speaks in all three), using the Phase 4 procedure. Record in README.md:
- Does the downloaded mp4 have an audio track at all? (The F-106 clips had none.)
- If yes: does Clara sound like the same woman in all three? Are the lines word-for-word and lip-synced?
- Does her face, hair and dress match the references?

**STOP 2.** The user and the montage chat decide:
- **(a)** voice and face hold: continue as written;
- **(b)** no audio, or the voice drifts: clips are made with the characters speaking silently (lips moving), and the montage chat dubs the lines separately.
Do not generate other clips before the decision.

## Phase 3: images I01–I69 (free)
For each timeline step with `"type": "image"`:
- prompt = `full_prompt` as is;
- image references = files from `visuals/refs/` for every ID in `refs` (for a character: `_front` and `_full`);
- 2 variants, keep the best.

Reject: faces that don't match the references; broken hands; any text or lettering; non-period clothing or objects. Steps with `"flashback": true` must look desaturated. If 4 tries fail, keep the best, mark it in the manifest note and move on.

## Phase 4: clips C01–C38 (credits)
For each step with `"type": "clip"`, in order:
1. **First frame** (image, free): prompt `start_frame_full_prompt`, references from `refs`. Characters in their starting positions, mouths closed. Regenerate freely until it is right: the whole clip depends on it. Save as `visuals/images/Cxx_first.png`.
2. **Video:** Frames-to-video from the first frame, Omni 1.1 Flash, `duration_s`, 16:9. Prompt = `video_prompt` as is (action, camera, exact lines, voice description).
3. **Reject the take if:** the face morphs or becomes another person; someone walks through doors or objects; the wrong character speaks; a line is changed, cut or extended; extra hands or fingers; text on screen.
4. **Max 2 regenerations per clip.** After 3 bad takes keep the best one and describe the problem in the manifest note.

**Credit guard:** check the balance before every video generation. If fewer than **150** credits are left, stop and report what is done and what remains. Clips with `"priority": "optional"` (C06, C21, C28) go **last**, only if more than 150 credits remain after all core clips; otherwise skip them (the montage covers them with images).

## Phase 5: narrator voice (ElevenLabs, no Flow credits)
Can run in parallel with Phase 3. Script `tts_elevenlabs.py` in this folder; the key comes from the environment variable `ELEVENLABS_API_KEY` (never write it to files or git).
1. `python tts_elevenlabs.py --check`: report characters left vs needed (~7,000 per pass).
2. `python tts_elevenlabs.py --voices`: show the user the list. Wanted: a warm, older American male storyteller.
3. Test: `python tts_elevenlabs.py --voice <ID> --only N01`. **STOP 3:** the user listens to `audio/narration/N01.mp3` and approves the voice.
4. Then `python tts_elevenlabs.py --voice <ID>` for all blocks (existing ones are skipped).
5. Push `audio/narration/*.mp3` and `*.alignment.json`. The alignment files carry word timings for the montage: keep them.

---

## manifest.json (schema `moiastro.montage.package.v2`, adapted)
```json
{
  "schema": "moiastro.montage.package.v2",
  "project_id": "western_widows_piano_v1",
  "title": "They Auctioned the Widow's Piano for Her Husband's Debt — Then a Silent Stranger Raised One Hand",
  "language": "en",
  "aspect_ratio": "16:9",
  "fps": 24,
  "source": "Google Flow (Omni 1.1 Flash 720p clips; Nano Banana Pro images); narration ElevenLabs",
  "flow_credits_spent": 0,
  "flow_credits_left": 0,
  "phase": "refs | test | images | clips | narration | done",
  "narration": {"voice_id": null, "files": ["audio/narration/N01.mp3"]},
  "refs": {"CHAR_CLARA": ["visuals/refs/CHAR_CLARA_front.png", "visuals/refs/CHAR_CLARA_34.png", "visuals/refs/CHAR_CLARA_full.png"]},
  "scenes": [
    {"shot_id": "I07", "type": "image", "image": "visuals/images/I07.png", "note": ""},
    {"shot_id": "C12", "type": "video", "video": "visuals/video/C12.mp4", "duration": 8,
     "first_frame": "visuals/images/C12_first.png", "has_audio": true, "dialogue_ok": true,
     "takes": 2, "credits": 0, "note": "Mercer turns his head at 7 s"}
  ]
}
```
Scenes go in timeline order. Skipped shots stay in the list with `"type": "skipped"` and a reason.

## README.md (same spirit as the F-106 package)
- What is in the package, models and settings used.
- Credits spent, per clip, including regenerations.
- Regenerated / rejected items and why.
- **Notes for the montage:** anything the editor must know ("C08: Deke finishes his line at 8.5 s"; "C22: fire only appears from 3 s"; "I37: the silver came out golden").
- **Questions:** anything you could not decide yourself.

## Do not
- Change lines, names, plot or shot order.
- Put text, titles, logos or watermarks into frames.
- Make music, captions or the montage.
- Push `_variants/` or any secret.
- Continue past a STOP without the user's answer.
