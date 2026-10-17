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
- C12 (no dialogue) · Eli waters his horse at the trough · he POURS water from a bucket into the trough at waist height with
  a visible stream and gurgling — reads as if he urinates into the trough; + a cut at 5.04 s to a new close shot ·
  AMBIGUOUS_ACTION (embarrassing) · CUTS_INSIDE_CLIP. Prevention: "the horse drinks from an already full trough; nobody
  pours water, no stream, no bucket in hand". Check every "waters / pours / washes" action for how it looks.
- C18 · close-up of Eli · an invented woman in a bonnet stands right next to him for the whole clip, invented kids and a man
  in a cap on the wagon behind → crop would need ~2x upscale (720p) → regenerate with "only Eli in frame" ·
  UNREFERENCED_PEOPLE_INVENTED
- Owner-found, not caught by the AI checker: C01 cuts, C12 pouring. The inspector must also ask "how does this action
  look to a viewer?", not only "are the right people present?".
- C12 v2 (after the global "one continuous shot, no cuts" rule) · static wide shot · the model made a DISSOLVE/MORPH
  transition at ~1.5–2.5 s into a second angle (over Nora's shoulder) and Eli LOST HIS HAT in the second angle ·
  TRANSITION_MORPH · PROP_CONTINUITY. ffmpeg scene detection (gt(scene,0.15)) did NOT catch it (soft transition) →
  the inspector needs a better test: compare frames 0.5 s apart over the whole clip (histogram/SSIM drop) and a
  vision check "same people, same clothes/hats at start and end". Prevention: describe ONE simple camera move, avoid
  prompts that imply two viewpoints ("the crowd laughs, Nora sees the stranger"), use 4 s instead of 6 s for silent
  cutaways, and state "keeps his hat on".

## Film 5 opening test — summary (17 Oct 2026)
Spent ≈ $27.8 (plan $22.5 + video redos ≈ $4.3 + frame redraws ≈ $1.0). 31 clips, draft 2:02.
Video redos (6): C01 ×2 (cuts + sign text, then posed first frame), C12 (dissolve + hat lost), C18 (extra person),
C08 (judge swallowed the key line), C02 (horse head growing from Asa's back — "holds the mare's bridle", no mare ref),
C21 (Asa lost his bowler, other face). ~15 first-frame redraws: wrong street background, sign text, ambiguous pouring,
extra people, wagon without driver, missing Sam, wrong clothes.
Free fixes (13): trims C03 (2 foreign frames at start), C05 (sign at end), C12, C19, C23 (whip pan), C27 (Sam's hat
vanishes); crops C01, C04, C11 (woman in beige in the foreground), C17 (wagon without horse), C25 (unknown black hat in
the foreground); C13 dropped (wagon without horse + empty trough); subtitle fix C02.
Kept: C04 black horse instead of the mare, C09 judge's hat appears, C20 Nora off-screen, C21 looks into the camera
(gaze was set by the first frame; the motion prompt can't turn it).
Lessons: lines ≤ ~12 words per 8 s; gaze in the first-frame prompt; every horse/wagon gets a ref; name anyone seen from
behind in the foreground; the video model invents cuts when motion text and first frame disagree.
