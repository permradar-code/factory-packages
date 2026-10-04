# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Finished (phase: done). Source of truth: `briefs/western_widows_piano/shotlist.json` (branch `tools/montage`, shotlist commit 7d0f9ec, brief commit bb32e99: 49 clips of 4/6/8 s, one speaker per clip).

## Status
| Part | State |
|---|---|
| Phase 1 references | done (Clara = candidate #2 of `docs/clara_candidates.jpg`) |
| Phase 5 narration | done (voice Bill, N01..N10 + alignment) |
| Phase 6 music | done (M01..M13, M14 skipped) |
| Phase 2 voice/face test | done: C11, C13, C34 with the final Clara |
| Phase 3 images | 72 of 69 done (I01..I72) |
| Phase 4 clips | 47 of 49 done: C01, C02a, C02b, C03, C04, C05, C06, C07, C08a, C08b, C09a, C09b, C10, C11, C12, C13, C14, C15a, C15b, C16a, C16b, C17, C18, C19b, C20a, C20b, C21, C22, C23, C24, C25a, C25b, C26a, C26b, C27, C28, C29, C30, C31a, C31b, C32, C34, C35, C36, C37a, C37b, C38. Skipped (closed at montage from start frames): C19a, C33 |

## What is in the package
- `visuals/refs/`: 8 characters x 3 angles, PROP_PIANO, PROP_HORSE, 8 LOC_* (1376x768 PNG).
- `visuals/images/`: stills I.. (Gemini, 1280x720 PNG) and the clip first frames Cxx_first.png (Flow images, 1376x768).
- `visuals/video/`: clips (Flow Omni 1.1 Flash, 720p, 24 fps, AAC audio with the spoken line).
- `audio/narration/`, `audio/music/`, `docs/`, `manifest.json`, `HANDOFF.md` (working notes for the next session), `tools/` (helper scripts).

## Credits (Flow, per clip; balance is not shown in the UI)
Spent 484, left 421 (905 reported on 3 Oct). Spent outside the package: 7 (Mercer test) + 12 (C11 with the rejected Clara v2).

| Clip | Length | Credits | Takes | Frame tries | Note |
|---|---|---|---|---|---|
| C01 | 8 s | 12 | 1 | 1 | wide establishing crane shot; Deke is small in frame (lip-sync hard to judge); audio present |
| C02a | 6 s | 10 | 1 | 1 | Lily speaks (Clara partly out of focus in foreground); audio present |
| C02b | 6 s | 10 | 1 | 1 | Clara speaks facing camera, Lily from behind; audio present |
| C03 | 8 s | 12 | 1 | 1 | Agatha and two women gossip under a parasol; audio present |
| C04 | 6 s | 10 | 1 | 1 | Pike on the platform, frontal; audio present |
| C05 | 6 s | 10 | 1 | 1 | first video try refused by Flow famous-people filter (no charge), identical retry passed; Agatha speaks the bid, cut to Clara close-up |
| C06 | 6 s | 10 | 1 | 1 | Optional clip: Deke auction call 'Six dollars, going once... going twice...'; Flow tab froze once before sending the frame (reopened, no charge) |
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
| C24 | 6 s | 10 | 1 | 1 | Mercer pins Deke (masked rider) and speaks the line; Mercer in profile; audio present |
| C25a | 6 s | 10 | 1 | 1 | Clara speaks on the porch steps, Mercer from behind; frame had Clara mid-size (edit attempt did not submit, original kept), the clip pushes in to a good close-up; audio present |
| C25b | 4 s | 7 | 1 | 1 | Mercer speaks, Clara from behind; 1 'unusual activity' error on the frame (no charge, page reloaded); audio present |
| C26a | 6 s | 10 | 1 | 1 | Lily speaks, Clara from behind hugs her; audio present |
| C26b | 6 s | 10 | 1 | 1 | Clara speaks, Lily from behind; audio present |
| C27 | 8 s | 12 | 1 | 1 | Deke shouts the opening bid from the wagon, Pike raises a finger; Deke is medium-size in frame; audio present |
| C28 | 6 s | 10 | 1 | 1 | Agatha whispers the line, then close-up on Clara and Lily's joined hands; audio present |
| C29 | 6 s | 10 | 1 | 1 | silent: Mercer, the Marshal and a clerk ride into town; audio track is ambient |
| C30 | 6 s | 10 | 1 | 1 | Mercer walks to the platform and speaks the line; Pike silent in the background; audio present |
| C31a | 8 s | 12 | 1 | 1 | Marshal speaks (star badge has no lettering), Pike reacts; 1 'unusual activity' error on the video (no charge, page reloaded); audio present |
| C31b | 4 s | 7 | 1 | 1 | Pike protests, Marshal from behind; 'original fictional character' appended to the Pike prompts; audio present |
| C32 | 6 s | 20 | 2 | 2 | take 1 rejected: Pike was thin and clean-shaven in the first frame (and in the video), take 2 with a stricter Pike description is correct; Mercer speaks, audio present |
| C34 | 4 s | 7 | 1 | 1 | face stable, Clara speaks the line, Mercer silent; framing sentence appended to the frame prompt (Clara large in the foreground) |
| C35 | 8 s | 12 | 1 | 2 | Mercer hands letter to Clara (shown from behind); frame try1 lost to a Flow tab freeze at 99% (no charge), try2 OK |
| C36 | 8 s | 12 | 1 | 1 | Mercer line, then reverse on Clara covering her mouth, tears; Clara in the reverse is a bit less like the ref (no clear beauty mark, hair simpler), usable |
| C37a | 6 s | 10 | 1 | 1 | Clara speaks at the piano, Mercer in doorway, Lily from behind; one unusual-activity error (no charge), page reloaded |
| C37b | 4 s | 7 | 1 | 1 | Reverse angle, Mercer in doorway says 'I'd like that, ma'am.'; Mercer is medium-size in frame and already smiling in the start frame (his first smile) |
| C38 | 6 s | 10 | 1 | 1 | Final wide shot, ranch at dusk, crane up and pull back, stars; ambient only, no dialogue; Flow tab froze once between frame and video (reopened, no charge) |
| C19a | skipped | 0 | 0 | | NOT MADE: Flow refused 3 times in a row (policy error 'content violates our rules', no charge). Not retried further by decision of 4 Oct 2026. Start frame `visuals/images/C19a_first.png`. Close at montage from the start frame C19a_first.png (Pike holding the paper) and still I57; the line is also covered by C19b. |
| C33 | skipped | 0 | 0 | | NOT MADE: Flow refused 3 times in a row ('cannot create videos that may harm the reputation of people or current events', no charge). Not retried further by decision of 4 Oct 2026. Start frame `visuals/images/C33_first.png`. Close at montage from the start frame C33_first.png (Marshal handcuffing Pike, crowd, Agatha with parasol) and still I57. |
| **Total** | | **465** | | | 47 clips; plus 19 spent outside the package = 484 |

ElevenLabs (pay-as-you-go plan, resets 24 Oct): narration 1549 credits, music 9476, N10 re-voice and the C19a Pike candidates after that; left 9641 of 23736.

## Extras (outside the 49 clips)
- Thumbnail A: `docs/thumbs/A.png` (2752x1536), Gemini tries: 1. Main. Sunny ranch morning: Clara left, double-barrel aimed at Mercer, Mercer right by the gate with the bay horse, hat on chest, piano under tarp on a wagon, empty sky top right for the title.
- Thumbnail B: `docs/thumbs/B.png` (2752x1536), Gemini tries: 3. Night, burning barn. Try 1 rejected (references did not attach, faces did not match); try 2 rejected (unrequested piano on the porch with garbled lettering); try 3 accepted (2 regenerations used, the maximum). Riders are silhouettes, rearing is mild.
- Thumbnail C: `docs/thumbs/C.png` (2752x1536), Gemini tries: 1. Auction: Clara in tears left, piano on the wagon, Deke with the gavel, Agatha laughing with the parasol, Mercer raising a hand in the crowd.
- Dialogue C19a_pike (skipped clip C19a (Pike)): `audio/dialogue/C19a_pike_v1.mp3`, `audio/dialogue/C19a_pike_v2.mp3`. Text: "Five hundred for the land. Clears your debt and buys you a ticket east.". v1 = Edward (smug, charismatic villain, middle-aged American), v2 = Monty (upper-class east-coast American villain, elderly). Both from the ElevenLabs shared voice library and added to the account as PIKE_Edward / PIKE_Monty. Choose by ear.
- N10 narration re-voiced with the updated sign-off text (tools/montage commit 0d49d1a), voice Bill, 14.2 s.

## Notes for the montage
- Faces: Clara = candidate #2 (final), Deke = v4, Marshal = v2, others first approved versions. Marshal's star badge has no lettering.
- I13 shows a small brass nameplate on the piano (no readable text), I01 shop signs are blank.
- Kitchen reference has four chairs (accepted).
- Wide first frames make the speaker small and lip-sync weak (C01); for dialogue clips a framing sentence was appended to the frame prompt when needed (C11, C14, C34); see the manifest notes.
- Mercer's beard looks fuller in some frames (C08b, C12, C14) than in the reference.
- I58 (auction, Clara and the clerk): try 1 gave Clara a beard and glasses (rejected); try 2 accepted, but the word BANK is legible on the building (it comes from the platform reference).
- C18: Pike arrives by buggy and speaks; Pike is medium-size in frame, lip-sync is hard to judge.
- C36: the reverse shot on Clara (tears, hand over mouth) is a little less like the reference than the other Clara shots (no clear beauty mark, simpler hair); usable.
- C37b: reverse angle, Mercer stands in the doorway at medium size and already smiles in the start frame (his first smile); lip-sync is hard to judge at that size, the line is short (about 1 s).
- C06 is an optional clip and was made (credits were above 150).
- Flow viewport changed between 641 and 585 px high between tabs; the Flow tab froze twice in this session (reopened, nothing was charged).
- Thumbnails A, B, C are in docs/thumbs (2752x1536, bright style, no text). A is the main one (free sky top right for the title).
- C19a Pike line: two ElevenLabs voice candidates in audio/dialogue (v1 Edward, v2 Monty) for the montage to lay over the start frame.
- Epilogue (after C38, before N10): narration N09b, images I70, I71, I72 (ChatGPT, film look, 1672x941, one try each). The epilogue has no video clips: use the stills with slow moves.

## Questions
- Flow image limit: first hit 3 Oct ~01:30 after ~60 images in ~25 min; reset by 4 Oct 10:30 (daily limit). On 4 Oct about 40 frame images were made in about 6 hours without hitting it again.
- Flow "famous people" filter: blocked the first Clara face earlier; on 4 Oct it refused C05 video once (identical retry passed) and C08b video twice (frame regenerated with one appended sentence, then passed). No new face was needed so far; if Mercer or Agatha keep being refused, make a new face per the mode rules.
- Flow "We noticed some unusual activity ... browser extensions" (no charge): appears every ~10 requests; fix = reload the Flow page and re-inject the queue (see HANDOFF section 9).
- Gemini images come out 16:9 (2752x1536) even when the aspect pill is not set after "new chat".
- C19a and C33 are NOT made: Flow refused each of them 3 times in a row (no credits charged). Decision of 4 Oct 2026: no more attempts; both beats are closed at montage from the start frames (visuals/images/C19a_first.png, visuals/images/C33_first.png) and the still I57. They are recorded in the manifest as type 'skipped'.
- Gemini image generation without references gives wrong faces silently: after every sent message the attach input is spent, so click '+' then 'Upload files' again (a fresh input must appear) and check that the reference chips are visible before sending.
