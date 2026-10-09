# -*- coding: utf-8 -*-
"""Edit plan for film 3 "The Barn in the Storm" (hand edit, 9 Oct 2026).

Order follows briefs/western_barn_storm/shotlist.json. Owner's review notes (9 Oct) applied:
  C04 cut before the coat drops to the ground; B04/B06 from 3 s (hands/reins wrong before);
  C40 cut before the close-up where Wade loses his hat; C82 without the first frames (two girls);
  C44 cropped above the burned-in subtitles; C46 short (oversized hand); C58 face close-up (half a body
  in the wide shot); C65 only her coming down with the baby (laid "through the bars" later);
  C76 from the ladder (the cradle was already uncovered at the start); C07 (Flow/Veo) darkened to night.
Flow clips (C06, C07, B01, C67, H01) live in FIX.

Visual specs as in film 2: "B04@3-6" part of a clip, "img:I01" still, "frame:C14@2" still from a clip,
"|5" weight in seconds.
"""

PLAN = [
    # ---------- COLD OPEN: the knock, the joke, the threat ----------
    ("clip", "C01", None),             # "May we sleep in your barn, mister? Just till the rain stops."
    ("clip", "C02", None),             # "No, ma'am."
    ("clip", "C04", "0-2.1"),          # "You'll sleep in the house."  (cut before the coat falls)
    ("clip", "C05", None),             # "Does he bite, Mama?"
    ("clip", "C06", None),             # "Only on Sundays."  (Flow)
    ("clip", "C07", "4.2-8"),          # "Five hundred dollars for the boy."  (Flow/Veo, line at the end)
    ("clip", "C08", None),             # "And the woman?"
    ("clip", "C09", None),             # "The woman doesn't matter."
    ("narr", "N01", ["B01", "frame:C01@2|5", "frame:C09@1.5|5"]),   # no C03: the girl's arm is twisted
    ("title", "T01", ("THE BARN IN THE STORM", 4.0)),
    # ---------- the road, the house ----------
    ("narr", "N02", ["img:I01", "img:I03", "img:I02", "img:I04"]),
    ("narr", "N03", ["img:I05", "img:I06", "frame:C10@1|5"]),
    ("clip", "C10", None),
    ("clip", "C11", None),
    ("clip", "C12", None),
    ("clip", "C13", None),
    ("clip", "C14", None),
    ("narr", "N04", ["img:I07|6", "frame:C14@2|5", "frame:C11@1|5"]),
    ("narr", "N05", ["img:I10", "frame:C35@2|5", "img:I08", "img:I09"]),
    # ---------- morning: breakfast, the cradle ----------
    ("clip", "B02", "0-5"),
    ("clip", "C15", None),
    ("clip", "C16", None),
    ("clip", "C17", None),
    ("clip", "C18", None),
    ("clip", "C19", None),
    ("narr", "N06", ["img:I11", "img:I12", "img:I13", "B03"]),
    ("clip", "C20", None),
    ("clip", "C21", None),
    ("clip", "C22", None),
    ("clip", "C23", None),
    ("clip", "C24", None),
    ("clip", "C25", None),
    ("narr", "N07", ["img:I14", "img:I15", "img:I16", "frame:C50@2|5"]),
    ("narr", "N08", ["img:I17", "img:I18", "frame:C17@4|5", "img:I19", "frame:C26@2|5"]),
    ("clip", "C26", None),
    ("clip", "C27", None),
    ("clip", "C28", None),
    ("clip", "C29", None),
    ("narr", "N09", ["B04@3-6", "img:I20", "img:I21", "frame:C27@1|4"]),
    # ---------- town: the boots ----------
    ("narr", "N10", ["B05", "frame:C30@0.5|5", "frame:C33@0.5|5"]),
    ("clip", "C30", None),
    ("clip", "C31", None),
    ("clip", "C32", None),
    ("clip", "C33", None),
    ("clip", "C34", None),
    ("clip", "C35", None),
    ("clip", "C36", None),
    ("clip", "C37", None),
    ("narr", "N11", ["B06@3-6", "img:I22", "frame:C36@1.5|6", "frame:C53@3|5", "frame:C49@1|6"]),
    # ---------- Leadville, the telegram ----------
    ("narr", "N12", ["img:I23", "img:I24"]),
    ("clip", "C38", None),
    ("clip", "C39", None),
    ("clip", "C40", "0-3.4"),
    ("clip", "C41", None),
    ("clip", "C42", None),
    ("clip", "C43", None),
    ("narr", "N13", ["img:I25", "frame:C39@4|5", "img:I26", "frame:C50@1|5"]),
    ("clip", "C44", None),
    ("clip", "C45", None),
    ("clip", "C46", "0.5-3.4"),
    ("clip", "C47", None),
    ("narr", "N14", ["frame:C47@3|5", "frame:C44@0.4|5"]),
    # ---------- the truth ----------
    ("clip", "C48", None),
    ("clip", "C49", None),
    ("clip", "C50", None),
    ("clip", "C51", None),
    ("clip", "C52", None),
    ("clip", "C53", None),
    ("clip", "B07", "1-6"),
    ("clip", "C54", None),
    ("clip", "C55", None),
    ("clip", "C56", None),
    ("narr", "N15", ["frame:C55@2|6", "frame:C56@1|6", "frame:C54@2|6"]),   # no I28: an extra woman in the frame
    ("narr", "N16", ["img:I29", "img:I30", "frame:C19@1|5", "img:I31", "frame:C63@1|5"]),
    ("clip", "C57", None),
    ("clip", "C58", None),
    # ---------- the storm comes back ----------
    ("narr", "N17", ["B08", "img:I27", "img:I32", "frame:C59@1|5", "frame:C62@1|5", "frame:C60@1|5"]),
    ("narr", "N18", ["img:I33", "img:I34", "img:I35", "frame:C57@3|5"]),
    ("clip", "C59", None),
    ("clip", "C60", None),
    ("clip", "C61", None),
    ("clip", "C62", None),
    ("clip", "C63", None),
    ("clip", "C64", None),
    ("clip", "C65", "0-2.8"),
    ("clip", "C66", None),
    ("clip", "C67", None),
    ("clip", "C68", None),
    ("clip", "C69", None),
    ("clip", "C70", None),
    ("clip", "C71", None),
    ("clip", "C72", None),
    ("clip", "C73", None),
    ("clip", "C74", None),
    ("clip", "C75", None),
    ("narr", "N19", ["img:I36", "img:I37", "img:I38"]),
    ("narr", "N20", ["frame:C37@1|5", "frame:C35@2|5", "img:I39", "frame:C31@3|5"]),
    ("narr", "N21", ["img:I40", "frame:C74@3|5", "img:I41"]),
    # ---------- morning: the cradle comes down ----------
    ("clip", "C76", "2-6"),
    ("clip", "C77", None),
    ("clip", "C78", None),
    ("clip", "C79", None),
    ("clip", "C80", None),
    ("clip", "C81", None),
    ("clip", "C82", "0.4-2.6"),
    ("clip", "C83", None),
    ("narr", "N22", ["B09", "img:I42", "frame:C77@3|5", "img:I43"]),
    ("narr", "N23", ["frame:C79@2|5", "img:I44", "img:I45", "frame:C83@3|5"]),
    ("end", "END", 12.0),
]

TITLE_ID = "T01"
END_BG = ("B09", 3.0)

# per-clip filters: "pre" on the source frame (crop), "post" after scaling + grade (colour)
CLIP_VF = {
    "C07": {"post": "eq=brightness=-0.13:saturation=0.75:gamma=0.85,colorbalance=bs=0.10:bm=0.05:rs=-0.05"},
    "C44": {"pre": "crop=iw*0.81:ih*0.81:iw*0.095:0"},          # burned-in subtitle at the bottom
    "C58": {"pre": "crop=iw*0.42:ih*0.42:iw*0.48:ih*0.40"},         # face close-up only
}

# music: (cue, anchor event, offset s). "S2:Mxx" = series score from film 2.
MUSIC = [
    ("M01", "C01", 0.0),        # storm and dread
    ("S2:M02", "T01", 0.0),     # series theme under the title
    ("S2:M07", "N02", 0.0),     # the long walk in the rain
    ("M03", "N03", 0.0),        # inside the quiet house
    ("S2:M03", "N05", 0.0),     # Cedar Bluff talk, the morning
    ("M02", "N06", 0.0),        # Anna and the cradle (lullaby)
    ("M03", "C20", 0.0),        # the porch at night
    ("S2:M09", "N07", 0.0),     # Henry
    ("S2:M11", "N08", 0.0),     # the house comes alive, the fence, the cow
    ("S2:M03", "N10", 0.0),     # into town
    ("M04", "C33", 0.0),        # Wade stands up for her - payoff
    ("M03", "N11", 0.0),        # the ride home
    ("S2:M05", "N12", 0.0),     # Vance, the telegram
    ("S2:M06", "C44", 0.0),     # Pike asks around
    ("S2:M09", "C48", 0.0),     # her story
    ("M01", "B07", 0.0),        # she tries to leave in the storm
    ("S2:M07", "N16", 0.0),     # Texas, the badge in the trunk
    ("M02", "C57", 0.0),        # Molly's prayer
    ("M01", "N17", 0.0),        # the riders come
    ("S2:M13", "C59", 0.0),     # the gate
    ("S2:M10", "C66", 0.0),     # gunfire
    ("S2:M14", "C73", 0.0),     # the letter, justice
    ("M03", "N21", 0.0),        # after the storm
    ("M02", "C76", 0.0),        # the cradle comes down
    ("M04", "C80", 0.0),        # "Stay anyway", the wedding
    ("S2:M02", "N23", 0.0),     # epilogue + end screen
]

# animated SUBSCRIBE badge: first right after the cold open (~0:35), then a few more
BADGE_AT = [("N01", 4.0), ("N05", 2.0), ("N10", 2.0), ("N16", 2.0), ("N21", 2.0)]

LINE_FIX = {}
