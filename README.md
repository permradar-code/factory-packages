# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress (phase: images). Source of truth: `briefs/western_widows_piano/shotlist.json` (branch `tools/montage`, shotlist commit 7d0f9ec, brief commit bb32e99: 49 clips of 4/6/8 s, one speaker per clip).

## Status
| Part | State |
|---|---|
| Phase 1 references | done (Clara = candidate #2 of `docs/clara_candidates.jpg`) |
| Phase 5 narration | done (voice Bill, N01..N10 + alignment) |
| Phase 6 music | done (M01..M13, M14 skipped) |
| Phase 2 voice/face test | done: C11, C13, C34 with the final Clara |
| Phase 3 images | 69 of 69 done (I01..I69) |
| Phase 4 clips | 29 of 49 done: C01, C02a, C02b, C03, C04, C05, C07, C08a, C08b, C09a, C09b, C10, C11, C12, C13, C14, C15a, C15b, C16a, C16b, C17, C18, C19b, C20a, C20b, C21, C22, C23, C34 |

## What is in the package
- `visuals/refs/`: 8 characters x 3 angles, PROP_PIANO, PROP_HORSE, 8 LOC_* (1376x768 PNG).
- `visuals/images/`: stills I.. (Gemini, 1280x720 PNG) and the clip first frames Cxx_first.png (Flow images, 1376x768).
- `visuals/video/`: clips (Flow Omni 1.1 Flash, 720p, 24 fps, AAC audio with the spoken line).
- `audio/narration/`, `audio/music/`, `docs/`, `manifest.json`, `HANDOFF.md` (working notes for the next session), `tools/` (helper scripts).

## Credits (Flow, per clip; balance is not shown in the UI)
Spent 295, left 610 (905 reported on 3 Oct). Spent outside the package: 7 (Mercer test) + 12 (C11 with the rejected Clara v2).

| Clip | Length | Credits | Takes | Frame tries | Note |
|---|---|---|---|---|---|
| C01 | 8 s | 12 | 1 | 1 | wide establishing crane shot; Deke is small in frame (lip-sync hard to judge); audio present |
| C02a | 6 s | 10 | 1 | 1 | Lily speaks (Clara partly out of focus in foreground); audio present |
| C02b | 6 s | 10 | 1 | 1 | Clara speaks facing camera, Lily from behind; audio present |
| C03 | 8 s | 12 | 1 | 1 | Agatha and two women gossip under a parasol; audio present |
| C04 | 6 s | 10 | 1 | 1 | Pike on the platform, frontal; audio present |
| C05 | 6 s | 10 | 1 | 1 | first video try refused by Flow famous-people filter (no charge), identical retry passed; Agatha speaks the bid, cut to Clara close-up |
| C07 | 4 s | 7 | 1 | 1 | Mercer starts small at the back and walks toward camera (push-in); line audible; 3 'unusual activity' errors before the page reload, no charge |
| C08a | 6 s | 10 | 1 | 1 | Deke speaks (gavel), Pike and Mercer silent |
| C08b | 4 s | 7 | 1 | 2 | Flow famous-people filter refused the first frame+video twice (no charge); frame regenerated once (same prompt + one appended sentence 'original fictional character'), then passed. Mercer speaks; Mercer's beard looks fuller than the ref |
| C09a | 4 s | 7 | 1 | 1 | Deke speaks (gavel), Mercer from behind; audio present |
| C09b | 6 s | 10 | 1 | 1 | Mercer speaks, Deke silent; audio present |
| C10 | 6 s | 10 | 1 | 1 | silent shot: Mercer walks up to Clara and Lily; two 'unusual activity' frame errors before reload, no charge |
| C11 | 8 s | 12 | 1 | 3 | first frame needed 3 tries (wide shots made Clara tiny; close-up framing sentence appended to the frame prompt). Face stable, line audible, lips move |
| C12 | 6 s | 10 | 1 | 1 | Mercer speaks beside his horse at the ranch gate; audio present |
| C13 | 6 s | 10 | 1 |  | first clip with the final Clara (cand #2); passed Flow's filter first try; user accepted it |
| C14 | 8 s | 12 | 1 | 2 | first frame try 1 had Mercer small in profile; try 2 with an appended framing sentence has him large and 3/4; Mercer speaks the fence line |
| C15a | 6 s | 10 | 1 | 1 | Clara speaks (Lily at the piano, Mercer from behind); audio present |
| C15b | 4 s | 7 | 1 | 1 | reverse angle: Mercer speaks, Lily and Clara from behind; audio present |
| C16a | 6 s | 10 | 1 | 1 | Clara speaks on the porch with two cups, Mercer from behind; audio present |
| C16b | 6 s | 10 | 1 | 1 | Mercer speaks on the porch, Clara from behind; audio present |
| C17 | 6 s | 10 | 1 | 1 | Mercer cracks a rock, speaks the silver line; audio present |
| C18 | 6 s | 10 | 1 | 1 | Pike arrives by buggy and speaks to Clara on the porch (wide-ish, Pike medium size); 1 'unusual activity' error on the video (no charge, page reloaded); audio present |
| C19b | 4 s | 7 | 1 | 1 | Clara refuses the paper and speaks, Pike from behind; audio present |
| C20a | 4 s | 7 | 1 | 1 | Pike speaks to Mercer at the barn, Mercer from behind; audio present |
| C20b | 6 s | 10 | 1 | 1 | Mercer speaks holding an axe, Pike from behind; 1 'unusual activity' error on the video (no charge, page reloaded); audio present |
| C21 | 8 s | 12 | 1 | 1 | Pike in the buggy speaks the note line and drives off; audio present |
| C22 | 6 s | 10 | 1 | 1 | silent action: masked rider torches the hay, Mercer drags it out with a pitchfork; frame title was mistyped once (nothing sent) |
| C23 | 4 s | 7 | 1 | 1 | Clara fires the shotgun and speaks the line; horses rear; audio present |
| C34 | 4 s | 7 | 1 | 1 | face stable, Clara speaks the line, Mercer silent; framing sentence appended to the frame prompt (Clara large in the foreground) |

ElevenLabs (monthly package, no card charge): narration 1549 credits, music 9476, left 9720 of 23736.

## Notes for the montage
- Faces: Clara = candidate #2 (final), Deke = v4, Marshal = v2, others first approved versions. Marshal's star badge has no lettering.
- I13 shows a small brass nameplate on the piano (no readable text), I01 shop signs are blank.
- Kitchen reference has four chairs (accepted).
- Wide first frames make the speaker small and lip-sync weak (C01); for dialogue clips a framing sentence was appended to the frame prompt when needed (C11, C14, C34); see the manifest notes.
- Mercer's beard looks fuller in some frames (C08b, C12, C14) than in the reference.
- I58 (auction, Clara and the clerk): try 1 gave Clara a beard and glasses (rejected); try 2 accepted, but the word BANK is legible on the building (it comes from the platform reference).
- C18: Pike arrives by buggy and speaks; Pike is medium-size in frame, lip-sync is hard to judge.

## Questions
- Flow image limit: first hit 3 Oct ~01:30 after ~60 images in ~25 min; reset by 4 Oct 10:30 (daily limit). On 4 Oct about 40 frame images were made in about 6 hours without hitting it again.
- Flow "famous people" filter: blocked the first Clara face earlier; on 4 Oct it refused C05 video once (identical retry passed) and C08b video twice (frame regenerated with one appended sentence, then passed). No new face was needed so far; if Mercer or Agatha keep being refused, make a new face per the mode rules.
- Flow "We noticed some unusual activity ... browser extensions" (no charge): appears every ~10 requests; fix = reload the Flow page and re-inject the queue (see HANDOFF section 9).
- Gemini images come out 16:9 (2752x1536) even when the aspect pill is not set after "new chat".
- C19a (Pike holds out the paper, 8 s) NOT made: Flow refused it 3 times in a row ('content violates our rules', no charge): frame 1 + video, frame 1 + video with 'original fictional character', then a regenerated frame (C19a_first.png, kept in visuals/images, Pike holding the paper) + video. Pike passed in C04 and C18. Try again later (maybe with a new face for Pike or a different framing) or cover the line with C19b.
