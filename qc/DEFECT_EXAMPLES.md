# Defect examples for the future frame inspector (task 09)
Each line: film · shot · what the script wants · what the generator produced · category. Collected by hand; the
inspector's checklist/prompt is built from these. Add new cases after every film review.

## Film 5 «Marry Me by Sunday» — first frames, 16 Oct 2026 (opening test, 31 frames, 10 redone by hand)
- C02 · plain street · readable "GENERAL STORE" sign · TEXT_IN_FRAME
- C12 · street, Eli at the trough · readable "CEDAR BLUFF" sign · TEXT_IN_FRAME
- C09 · Judge Voss alone with a cigar · an unrelated young man next to him · EXTRA_PERSON
- C13 · Nora's small farm wagon with the mare · wagon standing without a horse · VEHICLE_WITHOUT_HORSE
- C26 · Nora's small farm wagon · a covered settler wagon + an extra man · WRONG_PROP · EXTRA_PERSON
- C21 · Asa jerks his wrist free · looked like a friendly handshake · WRONG_ACTION
- B02 · Lucy on the wagon peeking at the rider · Lucy sitting on Eli's horse · WRONG_POSITION
- B03 · wagon fording the creek, Nora driving · woman in brown on the seat, then nobody on the seat · WRONG_PERSON · VEHICLE_WITHOUT_DRIVER
- B04 · wagon + rider on the hill · a woman in plaid and a bonnet instead of Nora · WRONG_PERSON · WRONG_OUTFIT
- C18 · Eli looks at Nora and the kids (not in refs) · an invented woman in a bonnet and invented kids, 3 times ·
  UNREFERENCED_PEOPLE_INVENTED (prevent at storyboard: anyone mentioned must be in refs, else "only Eli in frame")
- minor, accepted: C01 Nora standing instead of on the seat · C04 Asa holds a black saddle horse instead of Nora's mare ·
  C06 Sam in a jacket instead of suspenders · C11 blurred stranger where Nora should be

## Film 4 «The Widow's Rifle» — owner's timecode review of the final cut (Oct 2026)
- cut-off end of a spoken line (C36 inside the clip) · DIALOGUE_CUT
- a repeated action inside one clip (C39) · REPEATED_TAKE
- faces drifting between shots, a "double" of a character · IDENTITY_DRIFT · DUPLICATE_CHARACTER
- 8–18 s stills under the narrator · LONG_STILL (fixed in task 07: max 4 s)

## Film 5 — sample videos, 16 Oct 2026
- C01 (6 s, first shot of the film) · ONE shot: close on the gloved hand on the bridle, tilt up to Asa · the video model made
  THREE shots inside one clip (cuts at ~1.2 s and ~2 s): wide horse+wagon → Asa walking with his head out of frame → medium
  shot of Asa talking on the OTHER side of the horse; Nora jumps from standing to seated; readable sign "…AR CHRON…" ·
  CUTS_INSIDE_CLIP · CONTINUITY_JUMP · TEXT_IN_FRAME. Detectable for free: ffmpeg scene detection (select=gt(scene,0.2))
  on every clip → any cut inside a clip = defect. Prevention: add "one continuous shot, no cuts" to every motion prompt.
- C22 · line said 100 % correctly, but word timings rejected → `dialogue alignment missing` (factory bug: word end vs
  duration check, see task 08) · FALSE_ALIGNMENT_FAILURE
