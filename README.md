# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress. Source of truth: `briefs/western_widows_piano/shotlist.json` (branch `tools/montage`, shotlist commit 7d0f9ec, brief commit bb32e99: 49 clips of 4/6/8 s, one speaker per clip).

## Status (4 Oct 2026)
| Part | State |
|---|---|
| Phase 1 references | done, user-approved (Clara = candidate #2 of `docs/clara_candidates.jpg`) |
| Phase 5 narration | done (voice Bill, N01..N10 + alignment) |
| Phase 6 music | done (M01..M13, M14 skipped) |
| Phase 2 voice/face test | C13 done and accepted; C11 and C34 to be redone with the new Clara |
| Phase 3 images I01..I69 | I01..I15 done, I16..I69 pending |
| Phase 4 clips C01..C49 | C13 done, the rest pending |

## What is in the package
- `visuals/refs/`: 8 characters x 3 angles (CHAR_*_front / _34 / _full.png), PROP_PIANO (no nameplate), PROP_HORSE, 8 LOC_*. All 1376x768 PNG.
- `visuals/images/`: I01..I15 (1280x720 PNG, made in Gemini), C13_first.png.
- `visuals/video/`: C13.mp4 (1280x720, 24 fps, AAC audio).
- `audio/narration/`: N01..N10 (N07a, N07b) mp3 + alignment.json, voice "Bill" (ElevenLabs pqHfZKP75CvOlQylNhV4), about 9 min.
- `audio/music/`: M01..M13 mp3 + music_log.json (M14 skipped by decision). M06 accepted by the user.
- `docs/clara_candidates.jpg`: the 8 candidate fronts for Clara (#2 chosen).
- `manifest.json`, `HANDOFF.md` (full working notes for the next session), `tools/` (helper scripts).

## Tools and settings
- Stills I.. : Gemini app (image mode, 16:9, 2752x1536 originals, no visible watermark), scaled to 1280x720 here.
- Clip first frames: Flow images (Nano Banana Pro) per the latest brief; Gemini as the fallback. Video: Flow, Omni 1.1 Flash 720p, 24 fps (4/6/8 s = 7/10/12 credits).
- Narration and music: ElevenLabs.

## Credits
Flow credits (balance not shown in the UI; 905 reported by the user on 3 Oct): spent 29, left 876.

| Item | Credits | Note |
|---|---|---|
| Mercer test clip (4 s) | 7 | not in the package |
| C11 (8 s) with the rejected Clara v2 | 12 | clip dropped, to be redone |
| C13 (6 s) | 10 | kept |
| Total | 29 | one full pass of all clips is about 477 |

ElevenLabs (monthly package, no card charge): narration 1549 credits, music 9476 (M02 275; per-cue split is an estimate, see `audio/music/music_log.json`), left 9720 of 23736.

## Notes for the montage
- Faces: Clara = candidate #2 (final), Deke = v4, Marshal = v2, others are the first approved versions. Marshal's star badge has no lettering.
- I13 shows a small brass nameplate on the piano (no readable text), I01 shop signs are blank/illegible.
- Kitchen reference has four chairs instead of three (accepted by the user).
- C13: Clara speaks in the first second; the voice should be compared with C11 and C34 once those are redone.
- Rejected variants are not pushed: Clara/Deke/Marshal candidate fronts, the first LOC_STREET (legible shop signs), the first piano (brass plate with lettering), Clara v2 files and the C11 clip made with her.

## Questions
- Flow image limit: first hit 3 Oct ~01:30 after ~60 images in ~25 min; still active at 09:30 the same day; on 4 Oct 10:30 a single x1 image worked, so it is a daily limit.
- Flow's "famous people" filter blocked the first Clara face (Gemini "like an actress" wording) on C13 x3 and C34 x1 (no charge). Rule from the user: make a new face, no workarounds with angles. Watch for it on every new face.
- Gemini slows down badly in long chats (5-9 min per image after ~10 images): new chat every 7-8 images.
