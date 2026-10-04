"""Rebuilds README.md from manifest.json (status, credits per clip, notes, questions). usage: python tools/build_readme.py"""
import json, os
W = r"C:\Users\permr\fl_work\wwp"
m = json.load(open(os.path.join(W, "manifest.json"), encoding="utf-8"))
sl = json.load(open(os.path.join(W, "_variants", "brief", "shotlist.json"), encoding="utf-8-sig"))
clips = [s for s in m["scenes"] if s["type"] == "video"]
imgs = [s for s in m["scenes"] if s["type"] == "image"]
n_clips = sum(1 for x in sl["timeline"] if x.get("type") == "clip")
n_imgs = sum(1 for x in sl["timeline"] if x.get("type") == "image")
order = {x["id"]: i for i, x in enumerate(sl["timeline"])}
clips.sort(key=lambda s: order.get(s["shot_id"], 999))
rows = "\n".join(f"| {c['shot_id']} | {c.get('duration') or ''} s | {c['credits']} | {c.get('takes',1)} | {c.get('frame_tries','')} | {c.get('note','')} |" for c in clips)
spent = m["flow_credits_spent"]; left = m["flow_credits_left"]
t = f"""# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress (phase: {m['phase']}). Source of truth: `briefs/western_widows_piano/shotlist.json` (branch `tools/montage`, shotlist commit 7d0f9ec, brief commit bb32e99: 49 clips of 4/6/8 s, one speaker per clip).

## Status
| Part | State |
|---|---|
| Phase 1 references | done (Clara = candidate #2 of `docs/clara_candidates.jpg`) |
| Phase 5 narration | done (voice Bill, N01..N10 + alignment) |
| Phase 6 music | done (M01..M13, M14 skipped) |
| Phase 2 voice/face test | done: C11, C13, C34 with the final Clara |
| Phase 3 images | {len(imgs)} of {n_imgs} done (I01..I{max(int(s['shot_id'][1:]) for s in imgs)}) |
| Phase 4 clips | {len(clips)} of {n_clips} done: {', '.join(c['shot_id'] for c in clips)} |

## What is in the package
- `visuals/refs/`: 8 characters x 3 angles, PROP_PIANO, PROP_HORSE, 8 LOC_* (1376x768 PNG).
- `visuals/images/`: stills I.. (Gemini, 1280x720 PNG) and the clip first frames Cxx_first.png (Flow images, 1376x768).
- `visuals/video/`: clips (Flow Omni 1.1 Flash, 720p, 24 fps, AAC audio with the spoken line).
- `audio/narration/`, `audio/music/`, `docs/`, `manifest.json`, `HANDOFF.md` (working notes for the next session), `tools/` (helper scripts).

## Credits (Flow, per clip; balance is not shown in the UI)
Spent {spent}, left {left} (905 reported on 3 Oct). Spent outside the package: 7 (Mercer test) + 12 (C11 with the rejected Clara v2).

| Clip | Length | Credits | Takes | Frame tries | Note |
|---|---|---|---|---|---|
{rows}

ElevenLabs (monthly package, no card charge): narration 1549 credits, music 9476, left 9720 of 23736.

## Notes for the montage
- Faces: Clara = candidate #2 (final), Deke = v4, Marshal = v2, others first approved versions. Marshal's star badge has no lettering.
- I13 shows a small brass nameplate on the piano (no readable text), I01 shop signs are blank.
- Kitchen reference has four chairs (accepted).
- Wide first frames make the speaker small and lip-sync weak (C01); for dialogue clips a framing sentence was appended to the frame prompt when needed (C11, C14, C34); see the manifest notes.
- Mercer's beard looks fuller in some frames (C08b, C12, C14) than in the reference.

## Questions
- Flow image limit: first hit 3 Oct ~01:30 after ~60 images in ~25 min; reset by 4 Oct 10:30 (daily limit). On 4 Oct about 40 frame images were made in about 6 hours without hitting it again.
- Flow "famous people" filter: blocked the first Clara face earlier; on 4 Oct it refused C05 video once (identical retry passed) and C08b video twice (frame regenerated with one appended sentence, then passed). No new face was needed so far; if Mercer or Agatha keep being refused, make a new face per the mode rules.
- Flow "We noticed some unusual activity ... browser extensions" (no charge): appears every ~10 requests; fix = reload the Flow page and re-inject the queue (see HANDOFF section 9).
- Gemini images come out 16:9 (2752x1536) even when the aspect pill is not set after "new chat".
"""
open(os.path.join(W, "README.md"), "w", encoding="utf-8").write(t)
print("readme ok", len(clips), len(imgs))
