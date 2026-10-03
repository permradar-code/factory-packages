# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress. Source of truth: briefs/western_widows_piano/shotlist.json (branch tools/montage, latest seen commit 7c7b740: one speaker per clip, 49 clips of 4/6/8 s).

## Status
Phase 1 (references) done, waiting for the user's OK on the sheet. Phases 5 (narration) and 6 (music) done. Next: Phase 2 (clip tests), then images and clips.

## What is in the package
- `visuals/refs/`: 8 characters x 3 angles (CHAR_*_front / _34 / _full.png), PROP_PIANO, PROP_HORSE, 8 LOC_* (all 1376x768 PNG).
  - Clara, Deke, Marshal have new faces (user's choice: Clara v2, Deke v4, Marshal v2). Mercer, Lily, Pike, Agatha, Sam are the approved first versions.
  - PROP_PIANO has no nameplate. Marshal's star badge is plain (no lettering), see manifest notes.
- `audio/narration/`: N01..N10 (N07a, N07b) mp3 + alignment.json, voice "Bill" (ElevenLabs pqHfZKP75CvOlQylNhV4), about 9 min.
- `audio/music/`: M01..M13 mp3 + music_log.json (M14 skipped by decision). M02 approved by ear; M06 accepted by the user.
- `manifest.json`, `tools/` (helper scripts).

## Tools and settings
- Images: Gemini (image mode, 16:9, 2752x1536 originals, no visible watermark), scaled to 1376x768 for refs. Reason: Flow's image limit (apparently daily) was hit in session 1 and was still active in session 2.
- Video: Google Flow, Omni 1.1 Flash 720p, 24 fps (4/6/8 s = 7/10/12 credits). Narration and music: ElevenLabs.

## Credits
- Flow: 7 credits spent (one 4 s test clip: Mercer says "Two hundred."; the mp4 HAS an AAC audio track, 48 kHz stereo). Balance about 898 of 905 reported by the user.
- ElevenLabs (monthly package, no card charge): narration 1549 credits, music 9476 credits (M02 275; per-cue split is an estimate, see music_log.json `_usage`). Left 9720 of 23736.

## Notes for the montage
- Test clip (not a numbered clip, not in the package): speech-like audio at 0-0.7 s, 1.3-1.9 s and about 3 s; Mercer's eyes are closed in the first second. Lip-sync and the line itself are for the user to judge by ear.
- Rejected variants are not pushed: Clara/Deke/Marshal front variants v1-v4 each, the first LOC_STREET (legible shop signs), the first piano (brass plate with lettering).
- LOC_KITCHEN shows four chairs instead of three; LOC_PARLOR/LOC_BARN contain the piano/horse in generic form (not generated from the PROP refs).

## Questions
- Flow image limit data: first hit at about 01:30 on 3 Oct after ~60 images in ~25 min; still active at 08:50 and at 09:30 (VPN off) with a single x2 / x1 request. Video generation worked at 09:35. Gemini web works since the VPN was turned off: 15+ images in an hour without a limit.
- The user decides how to proceed with Phase 2 (C11, C13, C34 tests) after the OK on the references sheet.
