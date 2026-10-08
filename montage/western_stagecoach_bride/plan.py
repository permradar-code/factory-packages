# -*- coding: utf-8 -*-
"""Edit plan for film 2 "The Stagecoach Bride" (hand edit, 8 Oct 2026).

Order follows briefs/western_stagecoach_bride/shotlist.json (v4). Differences from the factory edit:
  * every narration block gets its own visuals (new silent b-roll B01..B46 from the fix1 batch + stills),
    so no dialogue clip ever plays under the narrator and nothing loops;
  * dialogue clips keep the WHOLE line (trim by the clip's own audio, not by a transcript);
  * C61/C102 replaced by C61R/C102R (Rose not in frame); C32 cut before the horses come loose.

Visual spec strings:
  "B01"            whole clip (b-roll from fix1 or a v1 clip)
  "C112@0-3.5"     part of a clip (seconds)
  "img:I01"        still image with slow push
  "frame:C52@0.3"  still made from a clip frame
Numbers after "|" are relative weights (default = clip length or 4.5 for stills).
"""

# (kind, id, extra)
# kind: clip  -> standalone clip with its own sound (dialogue or action); extra = "a-b" to force a range
#       title -> title card (text, seconds)
#       narr  -> narration block, extra = list of visuals
#       end   -> end screen (seconds)
PLAN = [
    # ---------- COLD OPEN: a line from the very first second (film 1 lost 40% in the first 30 s) ----------
    # Film 1 retention: 91% at 0:09 -> 64% at 0:34 -> 48% at 0:43 (slow, half-comic auction; the payoff came at 0:43).
    # So: three hard beats in 15 s, the narrator's hook over the walk, gunfire by ~0:30.
    ("clip", "C103", None),            # 0:00 "I wore it for you, Caleb. Like I promised."
    ("clip", "C104", None),            # "Keep walking, ma'am."
    ("clip", "C102R", "0-3"),          # the crowd laughs
    # the hook over the walk: first sentence of N01 ("...never seen the face of the man she had come a thousand miles to marry")
    ("narr", "N00", {"src": "N01", "from": 0.0, "to": 10.9, "vis": ["C60@0-6", "C112@1-7"]}),
    ("title", "T00", ("THREE DAYS EARLIER", 2.0)),
    # ---------- the robbery: in medias res, gunfire first ----------
    ("clip", "C31", None),
    ("clip", "C01", "0-4"),
    ("clip", "C28", None),
    ("clip", "C29", None),
    ("clip", "C02", "0-5"),
    ("clip", "C32", "0-2.3"),
    ("clip", "C03", None),
    ("clip", "C33", None),
    ("clip", "C04", None),
    ("clip", "C05", None),
    ("clip", "C34", None),
    ("clip", "C35", None),
    ("narr", "N01", {"from": 11.0, "vis": ["B01", "B02", "img:I01", "B03", "C60@1-5|4", "img:I02", "C06|5"]}),
    ("title", "T01", ("THE STAGECOACH BRIDE", 4.0)),
    ("clip", "C105", None),
    ("clip", "C106", None),
    ("clip", "C107", None),
    ("narr", "N02", ["C21", "B04"]),
    # ---------- act 1: Cedar Bluff ----------
    ("title", "T03", ("THAT MORNING · CEDAR BLUFF", 2.6)),
    ("clip", "C07", None),
    ("clip", "C08", None),
    ("clip", "C09", None),
    ("clip", "C10", None),
    ("clip", "C12", "0-3.5"),
    ("clip", "C11", None),
    ("clip", "C13", "0-3.5"),
    ("clip", "C14", None),
    ("clip", "C15", None),
    ("clip", "C36", None),
    ("clip", "C37", None),
    ("clip", "C38", None),
    ("narr", "N03", ["B05", "B06"]),
    ("clip", "C39", None),
    ("clip", "C40", None),
    ("clip", "C41", None),
    ("clip", "C42", None),
    ("clip", "C43", None),
    ("clip", "C44", None),
    ("clip", "C16", None),
    ("clip", "C17", None),
    ("narr", "N04", ["C18", "B07", "B08", "B09", "img:I04", "B10"]),
    ("clip", "C45", None),
    ("clip", "C46", None),
    ("clip", "C47", None),
    ("clip", "C48", None),
    ("clip", "C49", None),
    ("clip", "C108", None),
    ("narr", "N05", ["img:I05", "B11", "B12", "B13"]),
    ("clip", "C50", None),
    ("clip", "C51", None),
    ("narr", "N06", ["B14", "B15", "frame:C52@0.2|4"]),
    ("clip", "C52", None),
    ("clip", "C53", None),
    ("clip", "C54", None),
    ("clip", "C55", None),
    ("narr", "N07", ["B16", "B17"]),
    # ---------- the arrest, the walk, the jail ----------
    ("clip", "C56", None),
    ("clip", "C57", None),
    ("clip", "C58", None),
    ("clip", "C109", None),
    ("clip", "C59", None),
    ("narr", "N08", ["img:I06|4", "C112@0-4|4"]),
    ("clip", "C61R", None),            # Agatha mocks her during the walk (no "thief" in the first 30 s) ...
    ("clip", "C110", None),            # ... and Clara shuts her up: "One more word, Agatha..."
    ("clip", "C111", None),
    ("clip", "C112", "4-8"),
    ("clip", "C62", None),
    ("clip", "C63", None),
    ("clip", "C64", None),
    ("narr", "N09", ["B18", "B19", "B20", "frame:C65@0.3|5", "B21"]),
    ("clip", "C65", None),
    ("clip", "C66", None),
    ("narr", "N10", ["B22", "frame:C63@0.3|4"]),
    ("clip", "C67", None),
    ("clip", "C68", None),
    ("clip", "C69", None),
    ("clip", "C70", "0-4.6"),
    ("narr", "N11", ["B23", "B24", "B25", "img:I07", "B26"]),
    ("clip", "C71", None),
    ("clip", "C72", None),
    ("clip", "C73", None),
    ("clip", "C74", None),
    ("narr", "N12", ["B27", "B28"]),
    ("clip", "C75", None),
    ("clip", "C76", None),
    ("clip", "C77", None),
    ("clip", "C78", None),
    ("narr", "N13", ["img:I08", "B29", "B30", "B31", "B32"]),
    ("clip", "C79", None),
    ("clip", "C80", None),
    # ---------- Red Canyon ----------
    ("narr", "N14", ["img:I09", "B33", "B34", "B35"]),
    ("clip", "C81", None),
    ("clip", "C82", None),
    ("narr", "N15", ["B36", "B37"]),
    ("clip", "C84", None),
    ("clip", "C85", None),
    ("clip", "C86", None),
    # ---------- showdown on Main Street ----------
    ("narr", "N16", ["B38", "img:I10", "B39"]),
    ("clip", "C87", None),
    ("clip", "C88", None),
    ("clip", "C89", None),
    ("clip", "C90", None),
    ("clip", "C91", None),
    ("clip", "C92", None),
    ("clip", "C93", None),
    ("clip", "C94", None),
    # ---------- justice, proposals, finale ----------
    ("narr", "N17", ["img:I11", "B40", "B41", "frame:C95@0.3|4"]),
    ("clip", "C95", None),
    ("clip", "C96", None),
    ("clip", "C97", None),
    ("clip", "C98", None),
    ("narr", "N18", ["B42"]),
    ("clip", "C99", None),
    ("clip", "C100", None),
    ("narr", "N19", ["B43", "B44", "B45", "C101|5", "B46"]),
    ("end", "END", 12.0),   # short, bright end card for the YouTube end screen (no 20 s of murk)
]

# music: (cue, anchor event id, offset seconds). Each cue plays until the next one starts (2 s crossfade).
MUSIC = [
    ("M09", "C103", 0.0),    # cold open: the tender, sad theme (comes back at the arrest)
    ("M01", "T00", 0.0),     # the robbery chase starts on the card
    ("M07", "N01", 0.0),     # alone on the mountain
    ("M02", "T01", 0.0),     # series theme under the title
    ("M05", "C105", 0.0),    # Crane and Buck
    ("M03", "T03", 0.0),     # Cedar Bluff, the letters
    ("M06", "C36", 0.0),     # the stage was hit, the search
    ("M04", "C39", 0.0),     # rescue, the ranch
    ("M08", "C45", 0.0),     # the box, Crane's visit, the barn
    ("M09", "N07", 0.0),     # the dress, the arrest, the jail
    ("M10", "C67", 0.0),     # the fire
    ("M11", "N11", 0.0),     # dawn, the horseshoe, the letters
    ("M12", "N14", 0.0),     # Red Canyon
    ("M13", "N16", 0.0),     # showdown
    ("M14", "N17", 0.0),     # justice and the proposals
]

# the animated SUBSCRIBE badge (bell rings): event id + seconds into the event; never on N09 (the address).
# First one at ~0:28 - average viewer leaves around 0:30 (owner's request, 8 Oct).
BADGE_AT = [("N00", 6.0), ("N02", 1.5), ("N09", 9.0), ("N11", 2.0), ("N16", 1.5)]   # N09: on the narrator's address
BADGE_AT = [b for b in BADGE_AT if b[1] is not None]
