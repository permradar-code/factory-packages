# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress. Source of truth: briefs/western_widows_piano/shotlist.json (branch tools/montage).

## Status: Phase 1 (references), waiting for STOP 1
- Characters: 8 of 8 done, 3 angles each (front, 3/4, full body) in visuals/refs/ (CHAR_*_front/_34/_full.png, 1376x768).
  The 3/4 and full-body images were made with the chosen front image as the face reference.
- STOP 1 answer (3 Oct): Mercer, Lily, Pike, Agatha, Sam approved. Clara, Deke and Marshal are being redone (new faces; Clara 28-30, beautiful,
  soft features, tiredness only in the eyes; Deke and Marshal must not resemble known actors). The current files for these three are the OLD versions.
- Props and locations: PROP_PIANO downloaded (note: the brass plate on it reads "J. & C. FISCHER, NEW YORK"; a text-free variant may be remade).
  PROP_HORSE and LOC_* (8) are pending because Flow returned "usage limit reached" (no credits were charged).
- Narration (phase 5 done): voice "Bill" (pqHfZKP75CvOlQylNhV4), approved at STOP 3. 11 blocks N01..N10 (N07a/N07b), about 9 min total, mp3 + alignment.json in audio/narration/. ElevenLabs characters left: 19339 of 23736.
- Flow credits spent so far: 0 (all images are free). Flow project: 7a937194-22cf-4e10-a8ea-406b0d82a514.

## Notes
- Model: Nano Banana Pro, 16:9. Prompt = look + style from shotlist.json plus a plain-background / even-light instruction.
- Rejected variants (not pushed) stay in the Flow project.
- Clara reads a little older than 28 (tired look); the face is consistent across the three angles. (Being replaced.)

## Questions
- Flow usage limit, data point 1: first limit at ~01:30 on 3 Oct after ~60 images in ~25 min. At 08:50 (about 7 h 20 min later) a single x2 image request
  still returned "Вы достигли лимита на использование" (no credits charged). So the limit is NOT a plain 1-hour one; probably daily or a longer rolling window.
  Next probe: one x1 request about an hour after 08:50, then again later; results go into this section.
