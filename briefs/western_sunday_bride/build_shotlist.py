# -*- coding: utf-8 -*-
"""Source of truth for "Marry Me by Sunday" (Tales of Cedar Bluff, film 5). Screenplay: script.md (v2 FINAL, 16 Oct 2026).
Generates shotlist.json + music_cues.json (whole film) and shotlist_opening.json + music_cues_opening.json
(factory test: refs + the opening, same ids and file names, so the full film later reuses everything made for the test).
Setting: Cedar Bluff, Colorado (a state since 1876 - never "Territory"), late October 1881: Main Street, the white church,
the courtroom in the town hall, the Whitlock farm on Bitter Creek. Bright golden-aspen autumn; first snow from Sunday noon.
Rules (films 1-4 + owner decisions 16 Oct):
  * one speaker per clip; the line starts in the first second; lines > 24 words are split (script asserts it);
  * first minutes (cold open + scene 1 + supper) = all video, narration N01 runs over silent video b-roll;
  * after that every narration block gets a NEW STILL EVERY ~3 s (Ken Burns), never a long hold (script asserts it);
  * no weapons anywhere near Sam or Lucy; Eli carries NO gun at all; Asa's men never draw (Google refuses + series tone);
  * Nora wears ONE dress for the whole film (+ cream shawl at night/cold, + lace collar and aspen leaves at the wedding);
  * Eli: thick dark graying mustache, NO beard, silver-concho saddle always visible on the tall bay (the hint);
  * Will's chair = the same high-backed dark wood chair in scenes 2, 9 and N07, a three-legged stool beside it;
  * the ring is dark IRON (gold only on the table at the very end);
  * wagons and buggies only with horses harnessed in front; no legible text anywhere (letter = paper with a seal);
  * snow only from the church exit (scene 6) onward;
  * 8 native vertical hooks (production.hooks.count = 8), one line each.
Ref names are chosen NOT to collide with files of pkg/western_stagecoach_bride_v1 (used as package_branch for the test):
that branch already has LOC_BARN, LOC_KITCHEN, LOC_RANCH, PROP_HORSE, CHAR_AMOS... which would be silently reused.
"""
import copy, json, math, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado, late October 1881, "
         "bright natural autumn sunlight, golden-yellow aspens, 35mm film grain, warm vivid colors, shallow depth of field, "
         "period-accurate clothing and props. No text, no letters, no captions, no logos, no watermark, no modern objects.")
NIGHT = " Night: moonlight and warm oil-lamp light, faces clearly lit and readable."
SNOW = " Light first snow: soft snowflakes falling in sunshine, a thin dusting of white on the ground and on yellow aspen leaves."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, Colorado 1881, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
              "Warm, grounded drama with quiet dry humor: natural, restrained acting and natural voices, no slapstick, no exaggerated performances. "
              "Characters only speak the exact lines given, in English, with lips in sync. No subtitles, no text on screen, no music.")
ACTION = (" Fast, dynamic action from the very first frame: the movement is already happening when the shot starts, "
          "no slow build-up. Realistic weight and physics: real hooves, real splashing water, real dust.")
PREV = "pkg/western_stagecoach_bride_v1/visuals/refs"   # approved refs from films 1-2 (Clara, Mercer, Marshal, Main Street)
P = "sb"                                                 # file prefix of this film

CHARACTERS = {
 "CHAR_NORA": {"name": "Nora Whitlock", "role": "widow, 33, proud, dry humor",
   "look": "33-year-old American frontier woman, an original fictional character who does not resemble any actress, chestnut-brown hair in a braid pinned up around her head, light freckles, green eyes, a strong calm face, ALWAYS the same faded dark-green wool dress with small cream buttons down the front",
   "voice": "even, low American woman's voice, early thirties, a dry edge, rarely laughs"},
 "CHAR_SAM": {"name": "Sam Whitlock", "role": "her son, 9, 'the man of the house'",
   "look": "9-year-old boy, an original fictional character, dark hair, a serious frowning face, his late father's dark felt hat far too big for him, brown suspenders over a faded shirt, patched trousers, scuffed boots",
   "voice": "clear, serious, suspicious American boy's voice, nine years old"},
 "CHAR_LUCY": {"name": "Lucy Whitlock", "role": "her daughter, 6, loud and direct",
   "look": "6-year-old girl, an original fictional character, strawberry-blond curls, a gap in her front teeth, a faded blue gingham dress with a white pinafore, always holding a rag doll with a blue ribbon",
   "voice": "loud, bright, very direct American little girl's voice, six years old"},
 "CHAR_ELI": {"name": "Eli Kane", "role": "a quiet drifter, 46, secretly the owner of the Two Rivers Cattle Company",
   "look": "46-year-old American man, an original fictional character (not a celebrity lookalike), tall and broad-shouldered, a weathered sun-browned face, a thick dark mustache going gray, NO beard, calm gray eyes with fine lines, a worn brown canvas jacket with a sheepskin collar, a dusty black wide-brimmed hat, no gun belt, no firearms",
   "voice": "quiet, slow, dry American baritone, mid-forties, a faint smile in it"},
 "CHAR_ASA": {"name": "Asa Whitlock", "role": "the dead husband's brother, 42, grain merchant and church deacon, drowning in debt",
   "look": "42-year-old American man, an original fictional character, a neat light-brown pointed goatee, pale eyes, a tidy brown three-piece suit, a brown bowler hat, a gold watch chain across the vest, soft clean hands",
   "voice": "loud, smooth, falsely caring American man's voice, a sticky politeness"},
 "CHAR_VOSS": {"name": "Judge Harlan Voss", "role": "county judge, 68, gruff but honest",
   "look": "68-year-old American man, an original fictional character, a full white beard, bushy white eyebrows, a black frock coat, a string tie, a cigar",
   "voice": "gruff, gravelly old American man's voice, plain-spoken"},
 "CHAR_TATE": {"name": "Reverend Amos Tate", "role": "circuit preacher, 60, comes through once a month",
   "look": "60-year-old American man, an original fictional character, thin, clean-shaven, short gray hair, kind deep-set eyes, a worn black frock coat with a white clerical band, a black Bible held against his chest",
   "voice": "warm, humorous, slightly hoarse old preacher's voice"},
 "CHAR_DUNBAR": {"name": "Hank Dunbar", "role": "Two Rivers trail boss, 35 (courtroom only)",
   "look": "35-year-old American cowhand, an original fictional character, a sunburned face, a short sandy beard, dusty leather chaps over his trousers, a red neckerchief, a battered tan hat held in his hand, no gun belt",
   "voice": "loud, plain, dusty American cowhand's voice"},
 "CHAR_HOBBS": {"name": "Mr. Hobbs", "role": "storekeeper, 50",
   "look": "50-year-old balding storekeeper, an original fictional character, round spectacles, sleeve garters, a striped shirt and a checked vest",
   "voice": "nasal, fussy American voice"},
 # ---- recurring residents (refs exist on pkg/western_stagecoach_bride_v1) ----
 "CHAR_CLARA": {"name": "Clara Mercer", "role": "the widow of film 1, now married to John Mercer", "reuse_refs": True,
   "look": "26-year-old American frontier woman, very pretty, slender, gray-green eyes, warm chestnut hair with copper highlights in a soft braided crown, a dark-green Sunday dress, small oval silver locket",
   "voice": "warm, low, steady American woman's voice, late twenties"},
 "CHAR_MERCER": {"name": "John Mercer", "role": "Union veteran, Clara's husband (no lines)", "reuse_refs": True,
   "look": "40-year-old man, tall and lean, weathered tanned face, short dark-brown beard with gray at the chin, calm gray-blue eyes, long dark-brown canvas duster coat, black flat-brimmed hat",
   "voice": "deep, quiet, unhurried American baritone"},
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50 (courtroom, no lines)", "reuse_refs": True,
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
}
PROPS = {
 "PROP_WAGON_W": {"name": "Nora's wagon",
   "look": "a small weathered gray farm wagon with a plank seat, pulled by one old brown mare harnessed in front with worn leather harness"},
 "PROP_SADDLE": {"name": "Eli's horse and saddle",
   "look": "a tall dark-bay horse with a black mane wearing a fine dark-leather stock saddle decorated with round silver conchos, an expensive saddle that does not match the rider's worn clothes"},
 "PROP_CHAIR": {"name": "Will's chair",
   "look": "a sturdy high-backed chair of dark oiled wood with a woven rawhide seat, standing at the head of a rough plank table, a small three-legged wooden stool beside it"},
 "PROP_IRON_RING": {"name": "The iron ring",
   "look": "a simple dark iron ring bent from a square horseshoe nail, rough hammered surface, lying on a weathered wooden surface"},
}
LOCATIONS = {
 "LOC_STREET": {"name": "Cedar Bluff main street", "reuse_refs": True,
   "look": "small frontier town main street, dirt road, wooden false-front buildings, boardwalks, hitching rails, a wooden water trough, horses and wagons, mountains beyond; signs have no legible text"},
 "LOC_WHITLOCK": {"name": "Whitlock farm",
   "look": "a homestead on a creek in a mountain valley: a weathered log house with a wide front porch, a log barn, a pole-rail corral, a clear creek under tall cottonwoods, a wide hay meadow with round haystacks, golden-yellow aspens on the hills, blue mountains beyond"},
 "LOC_WHITLOCK_IN": {"name": "Whitlock kitchen",
   "look": "a plain log-house kitchen: a rough plank table with a high-backed dark wood chair at its head and a three-legged stool beside it, an oil lamp, a cast-iron stove with a coffee pot, a dish shelf with only two plates left, calico curtains, a doorway to a small children's room"},
 "LOC_WHITLOCK_BARN": {"name": "Whitlock barn",
   "look": "inside a log barn: a milk cow in a stall, a wooden milk bucket, hay, and in the corner a small blacksmith forge with bellows, an anvil on a stump and a tin can of horseshoe nails, light through the open doors"},
 "LOC_CHURCH_IN": {"name": "Cedar Bluff church",
   "look": "inside a small white frontier church: plain wooden pews on both sides of a center aisle, a simple wooden pulpit, tall clear windows with sunlight, white plank walls, a small cross on the wall"},
 "LOC_COURTROOM": {"name": "Courtroom in the town hall",
   "look": "a small frontier courtroom in a town hall: wooden benches full of townsfolk, a raised judge's desk with a gavel, a United States flag with 38 stars on a pole, a black iron stove, tall windows with winter sunlight, a double door at the back"},
}

SHOTS, HOOKS = [], []
_N = {"C": 0, "B": 0, "I": 0, "N": 0}
PART = {"v": "A"}            # A = test opening (cold open + payoff + N01), B = supper, C = porch + N02, F = rest of the film


def _next(k):
    _N[k] += 1
    return f"{k}{_N[k]:02d}"


def _dur(lines):
    w = sum(len(l.split()) for _, l in lines)
    return 6 if not lines else 4 if w <= 5 else 6 if w <= 13 else 8


def clip(action, refs, line=None, camera="", night=False, action_shot=False, dur=None, snow=False):
    lines = [line] if line else []
    SHOTS.append({"id": _next("C"), "type": "clip", "duration_s": dur or _dur(lines), "action": action, "camera": camera,
                  "dialogue": [{"speaker": a, "line": b} for a, b in lines], "refs": refs, "priority": "core",
                  "night": night, "snow": snow, "action_shot": action_shot, "broll": False, "start_frame_prompt": action,
                  "part": PART["v"]})
    return SHOTS[-1]["id"]


def broll(action, refs, camera="", night=False, dur=6, snow=False, action_shot=False):
    """silent clip under the narrator of the block that follows (field 'for')."""
    SHOTS.append({"id": _next("B"), "type": "clip", "duration_s": dur, "action": action, "camera": camera, "dialogue": [],
                  "refs": refs, "priority": "core", "night": night, "snow": snow, "action_shot": action_shot, "broll": True,
                  "start_frame_prompt": action, "for": None, "part": PART["v"]})
    return SHOTS[-1]["id"]


def img(prompt, refs, night=False, snow=False, motion="slow push in"):
    SHOTS.append({"id": _next("I"), "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "night": night,
                  "snow": snow, "for": None, "part": PART["v"]})


def narr(text):
    nid = _next("N")
    for s in reversed(SHOTS):                 # b-roll and stills written just before a narration block belong to it
        if s["type"] == "narration":
            break
        if s.get("for", 1) is None:
            s["for"] = nid
    SHOTS.append({"id": nid, "type": "narration", "text": " ".join(text.split()), "part": PART["v"]})
    return nid


def card(id_, text, seconds, big=False, subtitle=None):
    row = {"id": id_, "type": "title_card", "text": text, "duration_s": seconds, "part": PART["v"]}
    if big:
        row["big"] = True
    if subtitle:
        row["subtitle"] = subtitle
    SHOTS.append(row)


def hook(id_, beat, first_frame, video, refs, line, night=False, snow=False):
    HOOKS.append({"id": id_, "beat": beat, "duration_s": 8, "refs": refs, "first_frame": first_frame, "video": video,
                  "night": night, "snow": snow, "dialogue": [{"speaker": line[0], "line": line[1]}]})


N, S, LU, E, A, V = "CHAR_NORA", "CHAR_SAM", "CHAR_LUCY", "CHAR_ELI", "CHAR_ASA", "CHAR_VOSS"
TA, D, HO, CL, ME, MA = "CHAR_TATE", "CHAR_DUNBAR", "CHAR_HOBBS", "CHAR_CLARA", "CHAR_MERCER", "CHAR_MARSHAL"
ST, FARM, KIT, BARN, CH, CT = "LOC_STREET", "LOC_WHITLOCK", "LOC_WHITLOCK_IN", "LOC_WHITLOCK_BARN", "LOC_CHURCH_IN", "LOC_COURTROOM"
WAG, SAD, CHAIR, RING = "PROP_WAGON_W", "PROP_SADDLE", "PROP_CHAIR", "PROP_IRON_RING"
MARK = {}

# ============== COLD OPEN (0:00-1:00): Main Street, Friday morning. Dialogue only, no narrator, no title ==============
MARK["open"] = clip("Sunny frontier main street: close on a man's gloved hand in a brown suit sleeve grabbing the bridle of an old brown mare harnessed to a small gray farm wagon, the wagon jerking to a stop; Asa Whitlock in a bowler hat steps into frame holding the bridle.",
     [A, N, WAG, ST], (A, "Not so fast, Nora. Judge Voss hears my petition Monday morning."), camera="close on the gloved hand on the bridle, tilt up to Asa", action_shot=True)
clip("Asa Whitlock holds the mare's bridle and turns to the boardwalk in front of a general store, where townsfolk and ladies in Sunday hats watch; Nora sits on the wagon seat in her dark-green dress, a little girl with a rag doll beside her, a boy in an oversized hat in the wagon bed.",
     [A, N, LU, S, WAG, ST], (A, "A widow alone can't keep a homestead and raise two children. The whole town knows it."), camera="medium wide, the watching boardwalk behind Asa")
clip("Nora Whitlock on the wagon seat, reins in her hands, answers evenly, chin up.",
     [N, WAG, ST], (N, "I've kept it eleven months, Asa. Without your help."), camera="close-up, low angle from the street")
clip("Asa Whitlock smiles toward the people on the boardwalk, playing to them, one hand still on the bridle.",
     [A, ST], (A, "Eleven months of selling your wedding china. One plate at a time."), camera="medium close-up, the boardwalk crowd soft behind him")
clip("On the store boardwalk, ladies in Sunday hats laugh behind their fans; cut to Nora on the wagon seat, her face turning to stone.",
     [N, ST], camera="pan from the laughing ladies to Nora's still face", dur=4)
clip("The boy in his father's oversized hat jumps down from the wagon bed onto the dusty street, fists clenched, glaring up at his uncle.",
     [S, A, WAG, ST], (S, "You leave my ma alone!"), camera="low angle on the boy", action_shot=True)
clip("Asa Whitlock pats the boy's hat condescendingly and turns toward the steps of the town hall across the street.",
     [A, S, ST], (A, "You see, Judge? There's a boy who needs a man's hand."), camera="medium shot, following Asa's turn")
clip("Judge Harlan Voss stands on the wooden steps of the town hall, white beard, black frock coat, a cigar in his fingers, looking down at the wagon.",
     [V, ST], (V, "Mrs. Whitlock, I'll be plain. Show me a man on that place by Monday, and I'll throw his petition out."), camera="medium shot from street level")
clip("Judge Voss takes the cigar from his mouth and speaks heavily.",
     [V, ST], (V, "If not, those children go to their uncle."), camera="close-up")
clip("Nora Whitlock on the wagon seat, stunned but steady.",
     [N, WAG, ST], (N, "Monday? The preacher only comes through on Sunday."), camera="close-up")
clip("Asa Whitlock, sugary, tips his bowler hat to her.",
     [A, ST], (A, "Then I suppose you have until Sunday, sister."), camera="close-up")
MARK["trough"] = clip("The boardwalk crowd roars with laughter; Nora lifts her eyes past them: across the street at the wooden water trough a dusty tall stranger with a thick graying mustache waters a tall dark-bay horse with a silver-studded saddle. He is the only one not looking at the scene.",
     [N, E, SAD, ST], camera="over Nora's shoulder, rack focus to the stranger at the trough", dur=6)
clip("Nora climbs down from the wagon seat and walks straight across the dusty street toward the trough; heads on the boardwalk turn to follow her.",
     [N, ST], camera="tracking shot from behind Nora, the stranger ahead", dur=6)
clip("Nora stops in front of the stranger at the water trough and looks him in the face.",
     [N, E, SAD, ST], (N, "Mister. Are you married?"), camera="medium two-shot across the trough")
clip("Eli Kane slowly lifts his head from the horse, water dripping from the bucket in his hand.",
     [E, SAD, ST], (E, "No, ma'am."), camera="close-up")
clip("Nora, not blinking.",
     [N, ST], (N, "Would you like to be? By Sunday?"), camera="close-up")
clip("Dead silence on the street. On the wagon seat the little girl's mouth falls open, clutching her rag doll.",
     [LU, WAG, ST], camera="close-up on the little girl", dur=4)
MARK["supper_q"] = clip("Eli Kane looks past Nora at the two children on the wagon, at the uncle with the bridle, then back at her, and asks one question.",
     [E, ST], (E, "...What's for supper?"), camera="close-up, slow push in")
card("T01", "MARRY ME BY SUNDAY", 4.0, big=True, subtitle="A Tale of Cedar Bluff")

# ============== SCENE 1 (1:04-2:00): first payoff, then the road to the farm ==============
MARK["grab"] = clip("Main street: Asa Whitlock rushes up and grabs Nora by the elbow.",
     [A, N, ST], (A, "Have you lost your mind? He's a saddle tramp!"), camera="medium shot", action_shot=True)
clip("Eli Kane calmly takes Asa's wrist in his big hand. He does not squeeze. He just holds it.",
     [E, A, ST], (E, "I'd take my hand off the lady, friend."), camera="close on the hand on the wrist, then up to Eli's calm face")
clip("Asa Whitlock jerks his hand free, red-faced.",
     [A, ST], (A, "And who are you to tell me-"), camera="close-up", dur=4)
MARK["ask_sunday"] = clip("Eli Kane, quiet, not moving.",
     [E, ST], (E, "Nobody yet. Ask me again on Sunday."), camera="close-up")
clip("On the store boardwalk the ladies stop laughing and lower their fans; on the wagon seat the little girl giggles into her rag doll.",
     [LU, WAG, ST], camera="pan from the boardwalk to the giggling girl", dur=4)
clip("Nora steps close to Eli and speaks quietly, only for him.",
     [N, E, ST], (N, "Eleven dollars and a hen. That's what I can pay."), camera="close two-shot")
clip("Eli Kane, the corner of his mustache lifting.",
     [E, ST], (E, "Keep the hen. Is it far?"), camera="close-up")
clip("Nora answers, already turning back to her wagon.",
     [N, ST], (N, "Three miles up Bitter Creek."), camera="medium close-up")
MARK["saddle"] = clip("Eli swings up onto the tall dark-bay horse; close on the fine dark-leather saddle with round silver conchos; the boy in the wagon bed stares at it.",
     [E, S, SAD, ST], camera="close on the silver conchos, rack focus to the staring boy", dur=4)
broll("Golden autumn road along a creek: the small gray farm wagon with the old brown mare rolls between yellow aspens, a tall rider on a dark-bay horse beside it.",
      [N, E, WAG, SAD, FARM], camera="wide tracking shot from the side")
broll("The rider on the dark-bay horse with the silver-studded saddle rides beside the wagon; the little girl on the wagon seat peeks at him from behind her doll.",
      [E, LU, SAD, WAG], camera="medium tracking shot")
broll("A clear mountain creek running under tall cottonwoods with golden leaves drifting down onto the water, hooves and wagon wheels splashing through the ford.",
      [FARM, WAG], camera="low angle at the ford")
broll("The wagon and the rider come over a rise: below them a log homestead with a porch, a barn, a corral and a wide hay meadow with round haystacks, golden aspens on the hills.",
      [FARM, WAG, SAD], camera="wide crane-like shot from behind")
MARK["N01"] = narr("""Will Whitlock had died in February, of a fever that took three men in the valley that winter.
He left his wife a hundred and sixty acres on Bitter Creek, two children, eleven dollars, and the best hay meadow in the county.
His brother Asa had been very helpful ever since. Too helpful.""")

# ============== SCENE 2a (2:00-3:30): supper interrogation (humor, the chair) - optional part B of the test ==============
PART["v"] = "B"
MARK["chair"] = clip("Log kitchen at sunset, a supper of beans and cornbread on the plank table: Eli reaches for the high-backed dark wood chair at the head of the table; the boy snaps at him.",
     [S, E, CHAIR, KIT], (S, "That's Pa's chair."), camera="medium shot, the chair in the foreground")
clip("Silence. Nora freezes by the stove with a pot in her hands.",
     [N, KIT], camera="close-up on Nora", dur=4)
clip("Eli Kane calmly lets go of the chair and pulls the little three-legged stool to the table instead.",
     [E, CHAIR, KIT], (E, "Then I'll take the stool."), camera="medium shot")
clip("The boy watches him with deep suspicion across the table; the little girl stares at the stranger without blinking, her rag doll on her lap.",
     [S, LU, KIT], camera="two-shot of the children", dur=4)
clip("The little girl, chin on the table, studies the big stranger on the stool.",
     [LU, KIT], (LU, "Do you snore?"), camera="close-up")
clip("Eli Kane, folding his big hands, completely serious.",
     [E, KIT], (E, "Only when I'm asleep."), camera="close-up")
clip("The little girl leans to her mother and whispers loudly behind her hand.",
     [LU, N, KIT], (LU, "Pa snored like a bear."), camera="medium close-up")
clip("The boy crosses his arms, his father's hat still on his head at the table.",
     [S, KIT], (S, "My pa could shoe a horse in ten minutes."), camera="close-up")
clip("Eli Kane nods slowly, respectfully.",
     [E, KIT], (E, "Then your pa was a better man than me. Takes me twenty."), camera="close-up")
clip("The boy narrows his eyes.",
     [S, KIT], (S, "What do you do, mister?"), camera="close-up")
clip("Eli Kane, tearing a piece of cornbread.",
     [E, KIT], (E, "Cattle, mostly."), camera="close-up")
clip("The boy, still testing him.",
     [S, KIT], (S, "You a cowhand?"), camera="close-up", dur=4)
clip("Eli Kane, a small pause before he answers.",
     [E, KIT], (E, "I've been one."), camera="close-up, slow push in", dur=4)
clip("Nora sets down the coffee pot and points to the children's room.",
     [N, KIT], (N, "Sam. Lucy. Bed."), camera="medium shot", dur=4)
MARK["keep_him"] = clip("The little girl, dragging her rag doll toward the children's room, turns in the doorway.",
     [LU, KIT], (LU, "If he snores, can we keep him anyway?"), camera="medium shot from the table")

# ============== SCENE 2b (3:30-5:00): the porch, the paper marriage, N02 ==============
PART["v"] = "C"
clip("Night on the log-house porch, an oil lamp by the door, stars over the meadow: Nora stands with her cream knitted shawl around her shoulders; Eli sits on the porch step.",
     [N, E, FARM], (N, "It's a paper marriage, mister... I don't know your name."), camera="medium two-shot", night=True)
clip("Eli Kane looks up at her from the step.",
     [E, FARM], (E, "Eli. Eli Kane."), camera="close-up", night=True, dur=4)
clip("Nora, businesslike, pulling the cream shawl tighter.",
     [N, FARM], (N, "A paper marriage, Mr. Kane. You sleep in the barn. After the hearing, there's a judge in Denver who undoes such things."), camera="close-up", night=True)
clip("Eli Kane, almost smiling.",
     [E, FARM], (E, "You've thought this through."), camera="close-up", night=True, dur=4)
clip("Nora looks out at the dark meadow.",
     [N, FARM], (N, "I've had eleven months to think. And about four minutes to choose."), camera="close-up", night=True)
clip("Eli Kane, quietly.", [E, FARM], (E, "Why me?"), camera="close-up", night=True, dur=4)
clip("Nora turns and looks straight at him.",
     [N, FARM], (N, "You were the only man on that street who wasn't laughing."), camera="close-up", night=True)
clip("Eli Kane gazes out at the hay meadow, silver in the moonlight, round haystacks in rows.",
     [E, FARM], (E, "That's good grass for October."), camera="over his shoulder to the meadow", night=True)
clip("Nora, softer, the lamp light on her face.",
     [N, FARM], (N, "Best meadow on Bitter Creek. Will said it was the only thing in Colorado that never lied to him."), camera="close-up", night=True)
img("A wide hay meadow under the moon, round haystacks in silver light, tall cottonwoods along a creek, mountains black against the stars.", [FARM], night=True)
img("Close on a lamp-lit window of a log house at night, the meadow dark beyond.", [FARM], night=True, motion="slow drift")
img("A frontier grain store on main street at night, one lamp burning in the back window, sacks of grain stacked by the door, no legible sign.", [ST], night=True)
img("Inside a cluttered grain store office at night: a man in a brown suit and a goatee hunched over a desk under a lamp, a stack of unpaid bills held with a weight, his head in his hand.", [A], night=True, motion="slow drift")
img("Close on a folded letter with a red wax seal on a desk under a lamp, no legible writing, a gold watch beside it.", [], night=True)
img("A huge herd of longhorn cattle moving across an open autumn valley at sunset, riders on the flanks, a column of dust.", [], motion="slow drift")
img("Cowhands on horseback driving longhorn cattle across a wide river crossing at golden hour, splashing water.", [])
img("Close on a man's hand in a brown sleeve dipping a pen in an ink pot at night, a lamp, a blank paper (no legible writing).", [A], night=True)
img("The Whitlock hay meadow seen from the hillside in moonlight, the small log house with one lit window, a corral and a barn.", [FARM], night=True, motion="slow drift")
img("Inside a log kitchen at night: a high-backed dark wood chair at the head of an empty plank table, a three-legged stool pushed beside it, an oil lamp burning low.", [CHAIR, KIT], night=True)
img("A tall dark-bay horse with a silver-studded saddle tied by a log barn at night, moonlight glinting on the round silver conchos.", [SAD, FARM], night=True, motion="slow drift")
MARK["N02"] = narr("""What Nora did not know was that Asa's grain store was mortgaged to the roof.
That fall the Two Rivers Cattle Company was buying winter range along Bitter Creek, and Asa had already written to its agent.
Fifteen hundred dollars for the Whitlock place. All he needed was a judge's signature.
And nobody in Cedar Bluff knew who had just eaten supper at Will Whitlock's table.""")

# ============== SCENE 3 (5:00-9:30): Saturday - the cow, the dance, the ring ==============
PART["v"] = "F"
img("Main street on a bright Saturday morning: townsfolk gathered on the boardwalk in twos and threes, whispering and pointing, a buggy passing, golden aspens beyond.", [ST])
img("Two ladies in Sunday hats gossiping behind their fans on a boardwalk in front of a store window, no legible sign.", [ST], motion="slow drift")
img("A balding storekeeper in round spectacles and a checked vest laughing behind his counter, holding his belly, jars of candy and bolts of cloth on the shelves.", [HO])
img("The Whitlock farm at sunrise: smoke curling from the log-house chimney, mist on the creek, golden aspens catching the first light.", [FARM], motion="slow drift")
img("Close on a rooster crowing on a pole-rail corral fence at sunrise, the barn behind.", [FARM])
img("A tall man in a sheepskin-collared jacket stepping out of the barn door at dawn with hay on his shoulders, stretching his back.", [E, BARN], motion="slow drift")
narr("""By Saturday morning, the whole of Cedar Bluff was talking about the widow who had proposed to a stranger at the horse trough.
Edna Whitcomb said it was a scandal. Mr. Hobbs said it was the best thing he'd seen since the Fourth of July.""")
clip("Dawn in the log barn: the boy in his father's oversized hat drags the tall stranger by the sleeve to the milk cow and plants a wooden bucket under her.",
     [S, E, BARN], (S, "Ma says a husband milks the cow."), camera="medium shot")
clip("Eli Kane squats awkwardly on a tiny milking stool beside the cow, far too big for it.",
     [E, BARN], (E, "Your ma's a hard woman."), camera="medium shot")
MARK["cow"] = clip("The cow kicks the bucket over; milk flies across the straw; on the barn rail the little girl with the rag doll bursts out laughing.",
     [E, LU, BARN], camera="wide, the bucket flying", action_shot=True, dur=4)
clip("The boy stares at the stranger, milk on his boots.",
     [S, BARN], (S, "You never milked a cow?"), camera="close-up", dur=4)
MARK["close"] = clip("Eli Kane wipes milk off his mustache with great dignity.",
     [E, BARN], (E, "I've known a great many cows, son. We were never that close."), camera="close-up")
clip("The little girl runs to the barn door and shouts toward the house.",
     [LU, BARN], (LU, "Ma! He can't milk!"), camera="from behind her toward the house", dur=4)
clip("Nora on the porch, hiding a smile behind her hand.",
     [N, FARM], (N, "Then he'll learn."), camera="medium shot", dur=4)
clip("Sunny farmyard at noon: the little girl sets her rag doll on a fence post and pulls the big stranger by the hand into the middle of the yard.",
     [LU, E, FARM], (LU, "At a wedding you have to dance. Pa danced with Ma like this."), camera="medium shot")
MARK["boots"] = clip("The little girl steps up with both feet onto the stranger's big dusty boots and grabs his hands.",
     [LU, E, FARM], (LU, "Now you walk. Slow. Like a bear."), camera="low angle on the boots, tilt up")
clip("Eli Kane carefully waltzes the little girl around the sunny farmyard on top of his boots, very slowly, like a bear; she shrieks with joy.",
     [E, LU, FARM], camera="circling medium shot, golden light", dur=6)
clip("Nora watches from the doorway of the log house, then turns her face away so no one can see it.",
     [N, FARM], camera="close-up", dur=4)
clip("In the barn by the small forge, Nora stands at the open door, arms folded.",
     [N, E, BARN], (N, "The reverend will ask for a ring. I sold mine in March."), camera="medium two-shot")
clip("Eli Kane takes a square horseshoe nail from a tin can and cuts a length of string.",
     [E, BARN], (E, "Hold out your hand."), camera="close on the nail and the string, then up to his face", dur=4)
clip("Nora, suspicious.", [N, BARN], (N, "What for?"), camera="close-up", dur=4)
clip("Eli Kane, simply.", [E, BARN], (E, "Measuring."), camera="close-up", dur=4)
clip("He wraps the string around her ring finger. Their hands close together; an awkward silence, both looking only at the string.",
     [N, E, BARN], camera="close on the two hands", dur=6)
MARK["ring"] = clip("At the forge the horseshoe nail glows orange; Eli bends it around the horn of the anvil into a small ring with light hammer taps and drops it into a bucket of water in a burst of steam.",
     [E, RING, BARN], camera="close-up on the glowing nail and the anvil", action_shot=True, dur=8)

# ============== SCENE 4 (9:30-11:00): Saturday evening - fifty dollars; the corral at night ==============
clip("Sunset at the farm: a shiny black buggy rolls up to the porch, two riders behind it; Asa Whitlock stays seated in the buggy and holds out a few banknotes.",
     [A, E, FARM], (A, "Fifty dollars, Kane. Ride out tonight, and nobody need ever know your name."), camera="medium shot from the porch")
MARK["hen"] = clip("Eli Kane leans on a porch post, unhurried.",
     [E, FARM], (E, "Fifty? The lady offered me eleven and a hen. I'm holding out for the hen."), camera="close-up")
clip("Behind the buggy Asa's two hired riders snort with laughter despite themselves; Asa goes pale.",
     [A, FARM], (A, "You don't know who you're dealing with."), camera="medium shot of Asa, riders soft behind")
clip("Eli Kane, quietly.", [E, FARM], (E, "No. But I'm starting to see what you're dealing in."), camera="close-up")
clip("Asa Whitlock snaps, leaning out of the buggy.",
     [A, FARM], (A, "Fifteen hundred dollars is more than this whole family is worth-"), camera="close-up", action_shot=True)
clip("Asa stops short, realizing what he has said. Eli looks at him for a long moment.",
     [E, FARM], (E, "Is it, now."), camera="slow push in on Eli", dur=4)
clip("Asa Whitlock jerks the reins and turns the buggy around.",
     [A, FARM], (A, "See you in church, Kane. If you're still here."), camera="medium shot")
MARK["corral"] = clip("Night, moonlight: a shadowy hired man lifts the top rail off the pole corral; the horses burst out and gallop away into the darkness along the creek.",
     [FARM], camera="wide, low angle", night=True, action_shot=True, dur=6)
clip("In the dark barn on a bed of hay, Eli Kane opens his eyes at the sound of hooves.",
     [E, BARN], camera="close-up", night=True, dur=4)
img("A moonlit empty corral with its top rail lying on the ground, hoofprints in the dust.", [FARM], night=True)
img("A tall man in a sheepskin-collared jacket sitting awake on the hay in a dark barn, moonlight through the boards, his hat beside him.", [E, BARN], night=True, motion="slow drift")
img("Stars fading over the mountains above the Whitlock farm in the cold blue before dawn.", [FARM], night=True)
img("Hoofprints in the frosty mud along a creek at first light, leading away downstream.", [FARM])
img("Four loose horses grazing far down a misty creek valley at sunrise, golden aspens on the slopes.", [FARM], motion="slow drift")
img("A small white frontier church with a bell tower at the far end of main street at sunrise, empty street.", [ST])
img("Close on a pocket watch lying open on a barn beam at dawn, no legible numbers in focus.", [BARN], motion="slow drift")
img("The Whitlock log house at sunrise, a lamp just lit in the kitchen window.", [FARM])
narr("""Eli Kane slept in the barn that night, as agreed. He did not sleep much. A man with a great deal on his mind rarely does.
When the sun came up on Sunday, the Whitlock horses were two miles down Bitter Creek. And the church was three miles the other way.""")

# ============== SCENE 5 (11:00-12:30): Sunday dawn - the ride ==============
clip("Sunday dawn: Nora runs out onto the porch in her cream shawl, looking at the empty corral.",
     [N, FARM], (N, "The horses! Asa's men opened the corral."), camera="medium shot", action_shot=True)
clip("The boy runs out after her, his father's hat in his hand.",
     [S, FARM], (S, "The wedding's at eleven! We'll never-"), camera="medium shot", dur=4)
clip("Eli Kane is already throwing the silver-studded saddle onto the tall dark-bay horse, pulling the cinch tight.",
     [E, SAD, FARM], (E, "Put the coffee on, Mrs. Whitlock."), camera="medium shot")
MARK["ride"] = clip("The tall dark-bay horse gallops along the creek in bursts of spray, the rider low in the silver-studded saddle, golden aspens flashing past.",
     [E, SAD, FARM], camera="tracking shot alongside", action_shot=True, dur=6)
clip("The rider swings wide around a small band of four loose horses on the creek bank and turns them like an expert cattleman, waving his hat.",
     [E, SAD, FARM], camera="wide shot", action_shot=True, dur=6)
clip("Four horses gallop home along the meadow, the rider on the dark bay driving them from behind, dust and sunlight.",
     [E, SAD, FARM], camera="low wide angle, horses rushing past", action_shot=True, dur=6)
clip("The children cheer from the top rail of the corral fence as the horses pour back into the corral.",
     [S, LU, FARM], camera="medium shot of the children on the fence", action_shot=True, dur=4)
clip("Eli drops the corral rail back into place and pats the dark bay's neck.", [E, SAD, FARM], camera="medium shot", dur=4)
clip("The boy, breathless with admiration.",
     [S, FARM], (S, "Where'd you learn to ride like that?"), camera="close-up")
clip("Eli Kane, pulling off his gloves.", [E, FARM], (E, "Here and there. Mostly there."), camera="close-up")
clip("Nora hands him a tin cup of steaming coffee and, for the first time, smiles at him.",
     [N, E, FARM], camera="close two-shot, morning sun", dur=6)

# ============== SCENE 6 (12:30-15:00): the wedding ==============
clip("Reverend Amos Tate at the simple pulpit of the white church, Bible in hand, looking over the packed pews with amusement.",
     [TA, CH], (TA, "I'm told there's a wedding. I'm told it's a scandal. I've married folks for land, for cattle, and once for two pigs."), camera="medium shot from the aisle")
clip("Reverend Tate closes his Bible over one finger.", [TA, CH], (TA, "I never once asked why."), camera="close-up")
MARK["sham"] = clip("In the front pew Asa Whitlock rises to his feet and faces the church.",
     [A, CH], (A, "Reverend, this is a sham. And every soul in this church knows it."), camera="low angle", action_shot=True)
clip("Silence. At the back of the church Clara Mercer stands up.",
     [CL, CH], (CL, "Then every soul in this church can sit on the bride's side. Nobody else seems to."), camera="medium shot from the front, heads turning")
MARK["bride_side"] = clip("Clara Mercer walks up the aisle and sits on the empty bride's side; John Mercer follows her, then the balding storekeeper, then several more townsfolk fill the pews.",
     [CL, ME, HO, CH], camera="wide from the pulpit", dur=8)
clip("At the front, Reverend Tate turns to the tall groom.",
     [TA, E, CH], (TA, "Do you, Eli, take Nora to be your wife?"), camera="medium two-shot")
clip("Eli Kane, hat in hand.", [E, CH], (E, "I do."), camera="close-up", dur=4)
clip("Reverend Tate turns to the bride in her dark-green dress, a lace collar and a sprig of yellow aspen leaves in her hair.",
     [TA, N, CH], (TA, "Do you, Nora, take Eli?"), camera="medium two-shot")
clip("Nora pauses and looks at her children in the front pew, then back.",
     [N, CH], (N, "I do."), camera="close-up", dur=4)
clip("Reverend Tate holds out his palm.", [TA, CH], (TA, "The ring?"), camera="close-up", dur=4)
clip("The little girl proudly raises her rag doll: tied to the blue ribbon on its arm is a small dark iron ring; warm laughter ripples through the church.",
     [LU, RING, CH], camera="close-up on the doll and the ring", dur=4)
clip("Eli slides the dark iron ring onto Nora's finger.",
     [E, N, RING, CH], (E, "It's not much of a ring."), camera="close on the hands, then up")
MARK["hold"] = clip("Nora looks down at the iron ring on her hand.",
     [N, RING, CH], (N, "It's iron. It'll hold."), camera="close-up")
clip("Reverend Tate, smiling.", [TA, CH], (TA, "You may kiss the bride."), camera="medium shot", dur=4)
clip("Eli carefully kisses Nora on the cheek.", [E, N, CH], camera="close two-shot", dur=4)
clip("The little girl stands up on the front pew.",
     [LU, CH], (LU, "That's not how Pa did it!"), camera="medium shot", dur=4)
clip("The whole church bursts out laughing - with her now, not at her; Nora blushes and laughs.",
     [N, CH], camera="wide, then close on Nora laughing", dur=6)
img("The newlyweds stepping out of the white church into bright sunshine, first sparse snowflakes in the air, townsfolk on the steps.", [N, E, ST], snow=True)
img("Close on the small dark iron ring on a woman's hand holding a sprig of yellow aspen leaves, snowflakes melting on it.", [N, RING], snow=True, motion="slow drift")
img("A six-year-old girl with strawberry-blond curls dancing on the church steps with her rag doll, snowflakes in the sunlight.", [LU, ST], snow=True)
img("Townsfolk shaking hands with a tall man in a sheepskin-collared jacket on the church steps, snow beginning.", [E, ST], snow=True, motion="slow drift")
img("A man in a brown suit and bowler hat walking away alone down main street, his back to the camera, snowflakes falling.", [A, ST], snow=True)
img("The small gray farm wagon with the old brown mare leaving town, the dark-bay horse tied behind, a family on the seat, first snow in the sun.", [N, E, S, LU, WAG, SAD, ST], snow=True, motion="slow drift")
img("Golden aspens on the road home dusted with the first snow, the wagon small in the distance.", [FARM, WAG], snow=True)
img("The Whitlock farm in the afternoon sun under a light dusting of snow, smoke from the chimney.", [FARM], snow=True, motion="slow drift")
narr("""They were married at eleven o'clock on a Sunday morning, with a horseshoe nail for a ring and a six-year-old for a maid of honor.
Half the town had come to laugh. By noon, most of them were shaking the groom's hand.
Asa Whitlock was not among them.""")

# ============== SCENE 7 (15:00-16:30): Sunday evening - first snow, the confession that didn't happen ==============
clip("Evening on the porch, big slow snowflakes falling in the lamp light, the meadow white: Nora in her cream shawl stands beside Eli.",
     [N, E, FARM], (N, "You never said what you get out of this."), camera="medium two-shot", snow=True)
clip("Eli Kane, looking at the snow.",
     [E, FARM], (E, "A supper. A ring I made myself. And a little girl who stands on my boots."), camera="close-up", snow=True)
clip("Nora, quietly.", [N, FARM], (N, "And after Denver?"), camera="close-up", snow=True, dur=4)
clip("Eli looks out at the snowy meadow for a long time, then turns to her.",
     [E, FARM], (E, "Nora. Whatever happens tomorrow, I came to this valley for the wrong reasons."), camera="slow push in", snow=True)
clip("Nora, a faint smile.", [N, FARM], (N, "Most men do."), camera="close-up", snow=True, dur=4)
clip("Eli opens his mouth to say more; from inside the house comes the little girl's voice and he turns to the door.",
     [LU, E, FARM], (LU, "Mister Eli! Husbands say goodnight!"), camera="through the window, the girl in her nightgown at the glass", snow=True)
clip("A small lamp-lit children's room: Eli awkwardly tucks a quilt around the little girl; in the other bed the boy pretends to sleep.",
     [LU, E, KIT], (LU, "Are you going to be our pa?"), camera="medium shot from the doorway")
clip("Eli Kane, sitting on the edge of the little bed.",
     [E, KIT], (E, "I'm going to be here tomorrow. That's as far as I can see."), camera="close-up")
MARK["be_here"] = clip("The boy, eyes still shut, face to the wall.",
     [S, KIT], (S, "Then be here."), camera="close-up", dur=4)
img("Morning sun on fresh snow over the Whitlock meadow, the haystacks white-capped, long blue shadows.", [FARM], snow=True)
img("The small gray wagon and a rider on a dark bay on the snowy road into town, bright cold morning.", [WAG, SAD, FARM], snow=True, motion="slow drift")
img("Main street in fresh snow, townsfolk in coats streaming toward the town hall, breath steaming.", [ST], snow=True)
img("The steps of the town hall in the snow, people crowding at the double doors.", [ST], snow=True, motion="slow drift")
img("Inside a frontier courtroom: benches packed with townsfolk in coats, a black iron stove glowing, winter sunlight through tall windows.", [CT])
img("Two ladies in hats whispering on a courtroom bench, leaning together, eager.", [CT], motion="slow drift")
narr("""On Monday morning, the whole town came to the hearing. Some came for Nora. Some came for Asa.
Most came because Edna Whitcomb had promised it would be better than church.""")

# ============== SCENE 8 (16:30-19:30): the hearing - the reveal ==============
clip("The courtroom: Judge Voss at the raised desk, the marshal with a walrus mustache by the door, Nora with her two children on a bench, Eli at the back, Asa in front with papers.",
     [V, MA, N, A, CT], (V, "Mr. Whitlock. Your petition."), camera="wide from behind the benches")
clip("Asa Whitlock rises with his papers, addressing the judge and the room.",
     [A, CT], (A, "Your Honor, this marriage was made yesterday, with a horseshoe nail, to a saddle tramp nobody in this county has ever seen."), camera="medium shot")
clip("Asa Whitlock, warming to it.",
     [A, CT], (A, "He'll be gone within the week. And I have here an honest offer for my nephews' future."), camera="medium close-up")
clip("Asa holds up a folded letter with a red wax seal (no legible writing) for the room to see.",
     [A, CT], (A, "The Two Rivers Cattle Company will pay fifteen hundred dollars for that farm. I'd hold every penny in trust for the children."), camera="close on the letter, then Asa")
clip("Nora rises from the bench, the iron ring dark on her hand.",
     [N, CT], (N, "You'd sell Will's land? To strangers? To pay your own debts?"), camera="close-up", action_shot=True)
clip("Judge Voss frowns over his spectacles.",
     [V, CT], (V, "Two Rivers. That's the big outfit down on the Arkansas. Who speaks for them?"), camera="close-up")
MARK["door"] = clip("The courtroom double doors burst open: a dusty trail boss in leather chaps strides in with two cowboys, hat in hand.",
     [D, CT], (D, "Beg pardon, Judge. Mr. Kane - the herd's at the river crossing. Do we winter them on the Whitlock meadow, like you wrote?"), camera="low angle from the aisle", action_shot=True, dur=8)
clip("Dead silence. Every head in the courtroom turns slowly toward the tall man at the back.",
     [E, CT], camera="slow pan across the turning faces to Eli", dur=4)
clip("Asa Whitlock, the color draining from his face.", [A, CT], (A, "Mister... Kane?"), camera="close-up", dur=4)
clip("Eli Kane stands up at the back of the courtroom.",
     [E, CT], (E, "Eli Kane, Your Honor. I own the Two Rivers Cattle Company."), camera="low angle")
clip("Eli Kane walks slowly up the aisle.",
     [E, CT], (E, "I rode ahead of my herd to see the land I was buying. I found the family he meant to sell with it."), camera="tracking shot in front of him")
clip("Eli takes the sealed letter out of Asa's hand.",
     [E, A, CT], (E, "Two Rivers doesn't buy land from a man who'd sell his brother's children."), camera="close two-shot")
clip("Eli tears the letter in half and lets the pieces fall.", [E, CT], camera="close on the tearing paper", action_shot=True, dur=4)
clip("The trail boss scratches his head.", [D, CT], (D, "So... we don't winter there, boss?"), camera="medium close-up", dur=4)
clip("Eli Kane, glancing toward Nora.", [E, CT], (E, "We ask the lady."), camera="close-up", dur=4)
clip("A ripple of laughter; Judge Voss bangs his gavel.",
     [V, CT], (V, "Petition dismissed. And Mr. Whitlock - this court will remember your concern for those children. So will your congregation."), camera="medium shot")
clip("Asa Whitlock walks to the door through the silent courtroom; the ladies from the boardwalk look away from him.",
     [A, CT], camera="tracking shot behind Asa", dur=6)
clip("Judge Voss, dryly, taking up his cigar.",
     [V, CT], (V, "One more thing, Mr. Kane. Is that marriage a sham?"), camera="close-up")
clip("Eli looks across the room at Nora.",
     [E, CT], (E, "That's for my wife to say, Your Honor."), camera="close-up")
clip("Everyone looks at Nora. She rises, takes her children by the hand and walks out without a word.",
     [N, S, LU, CT], camera="wide, the room watching her go", dur=6)

# ============== SCENE 9 (19:30-21:00): the chair - finale ==============
clip("Noon at the farm, sun on thin snow and yellow aspens: Eli ties a bedroll behind the silver-studded saddle by the corral; Nora walks out to him.",
     [N, E, SAD, FARM], (N, "You let me beg a stranger on Main Street. And all along, you were the man buying my farm."), camera="medium two-shot", snow=True)
clip("Eli Kane, tightening a strap.",
     [E, FARM], (E, "On Friday, I was. By Saturday, I'd been kicked by your cow."), camera="close-up", snow=True)
clip("Nora almost laughs.", [N, FARM], (N, "And Denver?"), camera="close-up", snow=True, dur=4)
clip("Eli, hat in his hands.",
     [E, FARM], (E, "There's a judge there, you said. I'll ride, if you want me to."), camera="close-up", snow=True)
clip("From the porch the boy calls out.", [S, FARM], (S, "Supper's on. Ma made cornbread."), camera="medium shot", snow=True)
clip("Nora, turning to the house.",
     [N, FARM], (N, "You'd better come in, Mr. Kane. Before Sam changes his mind."), camera="close-up", snow=True)
clip("The kitchen, table set: Eli goes to the three-legged stool out of habit; the boy silently takes his father's high-backed chair at the head of the table and pulls it out for him.",
     [S, E, CHAIR, KIT], camera="medium shot, the chair in the center", dur=6)
MARK["sit"] = clip("The boy, holding the back of the chair.", [S, CHAIR, KIT], (S, "Sit down, Eli."), camera="close-up", dur=4)
clip("Silence. Eli looks at Nora; she turns to the stove so no one can see her face. Eli slowly sits in the high-backed chair.",
     [E, N, CHAIR, KIT], camera="slow push in", dur=6)
clip("Eli takes a gold ring from his vest pocket and sets it on the table in front of Nora; she shakes her head and raises her hand with the dark iron ring.",
     [N, E, RING, KIT], (N, "I'll keep this one. It held."), camera="close on the two rings, then up to Nora")
clip("The little girl tugs at her mother's sleeve.", [LU, KIT], (LU, "Is he staying? Ma, is he staying?"), camera="close-up")
clip("The boy, rolling his eyes.", [S, KIT], (S, "He can't even milk!"), camera="close-up", dur=4)
clip("The little girl, fierce.", [LU, KIT], (LU, "I'll teach him!"), camera="close-up", dur=4)
MARK["porch_dance"] = clip("Evening on the porch, slow snow in the lamp light: Nora steps up with both feet onto Eli's boots.",
     [N, E, FARM], (N, "Lucy says this is how it's done."), camera="low angle on the boots, tilt up to their faces", snow=True)
MARK["final"] = clip("They turn slowly on the snowy porch; in the lit window behind them the boy and the girl press their noses to the glass.",
     [N, E, S, LU, FARM], camera="wide, the window glowing", snow=True, dur=8)
img("Spring on the Whitlock meadow: red longhorn cattle grazing in green grass, the log house and the barn, aspens in new leaf.", [FARM])
img("Summer haymaking on the meadow: a tall man with a gray mustache and a teenage boy forking hay onto a wagon.", [E, FARM], motion="slow drift")
img("The high-backed dark wood chair at the head of a plank table set for a large family supper, lamplight.", [CHAIR, KIT])
img("A grown young man with dark hair on horseshoe, leading a cattle drive across the meadow, years later.", [FARM], motion="slow drift")
img("A young woman with strawberry-blond hair dancing a small child around on her boots in a sunny farmyard, years later.", [FARM])
img("Close on an old woman's hand with a dark iron ring, folded over a younger hand, lamplight.", [RING], motion="slow drift")
img("A gray-haired couple sitting on the porch of a log house at sunset, the meadow golden before them.", [FARM])
img("Autumn on Bitter Creek decades later: golden aspens, cattle on the meadow, the old log house with a new wing.", [FARM], motion="slow drift")
img("A worn milking stool and an overturned wooden bucket in a quiet barn, sunlight through the boards.", [BARN])
img("The small white church on main street in the snow, years later.", [ST], snow=True, motion="slow drift")
img("Golden aspens and a hay meadow on Bitter Creek at sunset, wide and peaceful.", [FARM])
narr("""Two Rivers cattle wintered on Bitter Creek for forty years, and not one acre of the Whitlock place was ever sold.
Sam Whitlock ran the outfit after Eli. Lucy taught three more Kane children to dance on their father's boots.
Eli never did learn to milk a cow. And Nora Kane wore an iron ring for fifty-one years.
She said gold was for people who weren't sure.""")
img("Night, gentle snow: the lamp glowing in the window of a log house by a creek, aspens silver in the moonlight.", [FARM], night=True, snow=True)
img("Close on the warm lamp in the window, snowflakes drifting past the glass.", [FARM], night=True, snow=True, motion="slow drift")
img("The valley at night under snow, one small light far away.", [FARM], night=True, snow=True)
img("Snow settling on a porch rail, the lamp light behind.", [FARM], night=True, snow=True, motion="slow drift")
narr("""That's the story of the Sunday bride. And if you ever pass Bitter Creek in October, folks there will still tell you about it.
Keep a light in the window.""")
SHOTS.append({"id": "E01", "type": "end", "clip": MARK["final"], "at": 3, "series": "TALES OF CEDAR BLUFF",
              "tagline": "Keep a light in the window", "duration_s": 12, "part": "F"})

# ============== 8 VERTICAL HOOKS (native 9:16, one line each, first frame = action) ==============
hook("H01", "humiliation", "Vertical 9:16. Sunny frontier main street: a woman in a dark-green dress standing in front of a tall stranger with a graying mustache at a wooden water trough, a dark-bay horse with a silver saddle behind him.",
     "She looks him straight in the eye and asks.", [N, E, SAD, ST], (N, "Mister. Are you married?"))
hook("H02", "threat", "Vertical 9:16. Main street: a big weathered hand holding the wrist of a man in a brown suit and bowler hat, close on the hands.",
     "The tall stranger speaks quietly, not letting go.", [E, A, ST], (E, "Nobody yet. Ask me again on Sunday."))
hook("H03", "joke", "Vertical 9:16. A log barn at dawn: a wooden milk bucket flying through the air, milk splashing, a cow's hind leg, a big man on a tiny stool.",
     "He wipes milk off his mustache with great dignity.", [E, BARN], (E, "I've known a great many cows, son. We were never that close."))
hook("H04", "kiss_proposal", "Vertical 9:16. Sunny farmyard: a six-year-old girl with strawberry-blond curls stepping up onto a big man's dusty boots, holding his hands.",
     "She grins up at him and gives orders.", [LU, E, FARM], (LU, "Now you walk. Slow. Like a bear."))
hook("H05", "threat", "Vertical 9:16. Night: horses bursting out of an open pole corral and galloping into the dark, moonlight, dust.",
     "At dawn the woman runs onto the porch in a cream shawl.", [N, FARM], (N, "The horses! Asa's men opened the corral."), night=True)
hook("H06", "humiliation", "Vertical 9:16. Inside a white church: a man in a brown suit and bowler hat jumping to his feet in the front pew, the congregation turning.",
     "He faces the church, loud and righteous.", [A, CH], (A, "Reverend, this is a sham. And every soul in this church knows it."))
hook("H07", "reveal", "Vertical 9:16. A courtroom double door bursting open, a dusty trail boss in leather chaps striding in, hat in hand.",
     "He speaks to the tall man at the back of the room.", [D, CT], (D, "Mr. Kane, the herd's at the river crossing. Where do we winter them?"))
hook("H08", "kiss_proposal", "Vertical 9:16. Close on a glowing orange horseshoe nail being bent around an anvil horn into a ring, sparks, steam.",
     "A woman's hand with a dark iron ring; she looks at it and smiles.", [N, RING, CH], (N, "It's iron. It'll hold."))


# ======================= BUILD =======================
def ref_text(refs):
    parts = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src:
            parts.append(f"{src['name']}: {src['look']}")
    return " | ".join(parts)


MINOR = {"CHAR_HOBBS", "CHAR_DUNBAR"}


def ref_files(refs):
    out = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        base = PREV if src and src.get("reuse_refs") else "visuals/refs"
        if r in CHARACTERS:
            out += [f"{base}/{r}_front.png"] + ([] if r in MINOR else [f"{base}/{r}_full.png"])
        else:
            out.append(f"{base}/{r}.png")
    return out


def light(s):
    return (NIGHT if s.get("night") else "") + (SNOW if s.get("snow") else "")


ids = [s["id"] for s in SHOTS]
assert len(ids) == len(set(ids)), "duplicate ids"
for s in SHOTS:
    if s["type"] == "image":
        s["full_prompt"] = s["prompt"] + " " + STYLE + light(s) + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else "")
        s["ref_files"] = ref_files(s["refs"])
        s["file"] = f"visuals/images/{P}_{s['id']}.png"
    elif s["type"] == "clip":
        s["start_frame_full_prompt"] = (s["start_frame_prompt"] + " First frame of the shot, characters in position" + (", mouths closed" if s["dialogue"] else "")
                                        + (", the action already in motion" if s["action_shot"] else "") + ". " + STYLE + light(s)
                                        + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else ""))
        s["ref_files"] = ref_files(s["refs"])
        present = [r for r in s["refs"] if r in CHARACTERS]
        if s["dialogue"]:
            d = s["dialogue"][0]
            c = CHARACTERS[d["speaker"]]
            assert len(d["line"].split()) <= 24, f"{s['id']}: line too long for one clip"
            assert d["speaker"] in s["refs"], f"{s['id']}: speaker not in refs"
            dl = (f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}"'
                  + (f" ONLY {c['name']} speaks. Everyone else keeps their mouth closed and only listens." if len(present) > 1 else "")
                  + " The line starts within the first second; after the line the speaker holds a natural expression, no extra words.")
        else:
            dl = " No dialogue, natural sound only (wind, creek, hooves, birds, crowd murmur where shown), nobody speaks."
        s["video_prompt"] = (s["action"] + (ACTION if s["action_shot"] else "") + (" Camera: " + s["camera"] + "." if s["camera"] else "")
                             + dl + " " + CLIP_STYLE)
        s["files"] = {"start_frame": f"visuals/images/{P}_{s['id']}_first.png", "video": f"visuals/video/{P}_{s['id']}.mp4"}
    # never a child and a weapon together; Eli carries no gun - keep weapon words out of every prompt
    for k in ("action", "prompt"):
        if k in s:
            assert not re.search(r"\b(gun|rifle|pistol|revolver|shotgun|holster)\b", s[k], re.I), f"{s['id']}: weapon word"
VSTYLE = STYLE.replace("16:9 widescreen", "9:16 vertical portrait frame") + " Bright, faces large and clearly lit."
for h in HOOKS:
    h["first_frame_full_prompt"] = h["first_frame"] + " " + VSTYLE + light(h) + " Characters/places: " + ref_text(h["refs"])
    d = h["dialogue"][0]
    c = CHARACTERS[d["speaker"]]
    assert len(d["line"].split()) <= 24
    h["video_prompt"] = (h["video"] + f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}" The line starts within the first second; no extra words. '
                         + CLIP_STYLE.replace("16:9", "9:16 vertical portrait frame, subjects large and centered"))
    h["ref_files"] = ref_files(h["refs"])
    h["files"] = {"start_frame": f"visuals/hooks/{P}_{h['id']}_first.png", "video": f"visuals/hooks/{P}_{h['id']}.mp4"}

REF_BG = ("Character reference sheet photo, photorealistic, 1881 American West period clothing, plain warm neutral studio background, "
          "soft even daylight, sharp focus, natural skin texture, no text, no logos, no watermark.")
REF_PROMPTS = []
for cid, c in CHARACTERS.items():
    if c.get("reuse_refs"):
        continue
    REF_PROMPTS.append({"file": f"visuals/refs/{cid}_front.png", "prompt": f"Head-and-shoulders portrait, facing the camera. {c['look']}. {REF_BG}"})
    if cid not in MINOR:
        REF_PROMPTS.append({"file": f"visuals/refs/{cid}_full.png", "prompt": f"Full-body standing pose. {c['look']}. {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"})
for group in (PROPS, LOCATIONS):
    for rid, r in group.items():
        if r.get("reuse_refs"):
            continue
        REF_PROMPTS.append({"file": f"visuals/refs/{rid}.png", "prompt": f"{r['look']}. Clear reference image of {r['name'].lower()}, no people unless needed for scale. " + STYLE})

# ======================= MUSIC (new cues + free cues from films 3 and 4) =======================
TAIL = (" Instrumental only, no vocals, no choir. Warm analog recording, cinematic western film score, 1880s American frontier feel, "
        "no modern drums, no synths, no electric guitar.")
CUES = [
    {"id": "M01", "covers": "cold open: street humiliation, the proposal at the trough", "target_s": 65, "mood": "humiliation turning to quiet nerve", "new": True, "instrumental": True,
     "prompt": "Slow tense western cue at 70 BPM in D minor: low sustained strings, a lonely solo fiddle line, sparse piano notes, a held breath of silence near the end, dignified and taut." + TAIL},
    {"id": "M02", "covers": "after the title: the first payoff, the road to Bitter Creek", "target_s": 70, "mood": "warm open road, light humor", "new": True, "instrumental": True,
     "prompt": "Warm open-road western cue at 92 BPM in G major: acoustic guitar picking, a gentle fiddle melody, soft upright bass, a hint of harmonica, golden autumn afternoon, hopeful." + TAIL},
    {"id": "M03", "covers": "supper, the porch at night, the cow, the dance", "target_s": 90, "mood": "homey tenderness with a smile", "new": True, "instrumental": True,
     "prompt": "Homey tender western cue at 76 BPM in C major: solo fiddle and pump organ, light plucked banjo, a playful little turn in the melody, warm kitchen lamplight, gentle humor." + TAIL},
    {"id": "M04s", "series_source": "S3:M01", "covers": "night: the open corral", "target_s": 45, "mood": "storm and dread"},
    {"id": "M05", "covers": "Sunday dawn: the ride after the horses", "target_s": 60, "mood": "galloping drive", "new": True, "instrumental": True,
     "prompt": "Driving western chase cue at 132 BPM in A minor turning to A major: galloping frame-drum rhythm, fast fiddle runs, low strings building, a triumphant swell as the horses come home." + TAIL},
    {"id": "M06", "covers": "the wedding", "target_s": 90, "mood": "small-town wedding, warm and a little funny", "new": True, "instrumental": True,
     "prompt": "Small-town wedding cue at 84 BPM in F major: reed pump organ playing a simple hymn-like melody, a fiddle joining in, soft warmth, a light lift of joy, first snow in sunshine." + TAIL},
    {"id": "M07s", "series_source": "S3:M03", "covers": "first snow evening, goodnight", "target_s": 90, "mood": "quiet tenderness"},
    {"id": "M08", "covers": "the hearing: tension, the door, the reveal", "target_s": 90, "mood": "silence, a blow, then warmth", "new": True, "instrumental": True,
     "prompt": "Courtroom suspense-to-warmth western cue at 72 BPM in E minor turning to E major: a slow ticking pizzicato, low held strings, a sudden full chord, then a warm rising theme on strings and fiddle." + TAIL},
    {"id": "M09s", "series_source": "S3:M04", "covers": "the chair, the porch dance, the epilogue", "target_s": 90, "mood": "warm triumph"},
]
first_of = lambda pred: next(s["id"] for s in SHOTS if pred(s))
ANCHORS = {
    "M01": MARK["open"],
    "M02": "T01",
    "M03": MARK["chair"],
    "M04s": MARK["corral"],
    "M05": first_of(lambda s: s["type"] == "clip" and "opened the corral" in json.dumps(s["dialogue"])),
    "M06": first_of(lambda s: s["type"] == "clip" and "married folks for land" in json.dumps(s["dialogue"])),
    "M07s": first_of(lambda s: s["type"] == "clip" and "what you get out of this" in json.dumps(s["dialogue"])),
    "M08": first_of(lambda s: s["type"] == "clip" and "Your petition." in json.dumps(s["dialogue"])),
    "M09s": first_of(lambda s: s["type"] == "clip" and "beg a stranger on Main Street" in json.dumps(s["dialogue"])),
}
# one anchor per cue: each cue plays from its anchor until the next cue starts (2 s crossfade)

SAMPLE_OPENING = [MARK["open"], MARK["trough"], MARK["supper_q"], MARK["ask_sunday"]]   # the owner checks these 4 first
SAMPLE_FULL = [MARK["open"], MARK["supper_q"], MARK["door"], MARK["sit"]]

for i, s in enumerate(SHOTS):
    if s.get("for"):
        j = next(k for k in range(i, len(SHOTS)) if SHOTS[k]["id"] == s["for"])
        assert all(SHOTS[k].get("for") == s["for"] for k in range(i, j)), f"{s['id']}: scene clips between it and {s['for']}"

# ---- still pacing under the narrator: a new picture every ~3 s (QC no_still_held_too_long) ----
WPM = 140
for n in [s for s in SHOTS if s["type"] == "narration"]:
    vis = [s for s in SHOTS if s.get("for") == n["id"]]
    sec = len(re.findall(r"[A-Za-z']+", n["text"])) / WPM * 60
    vsec = sum(v.get("duration_s", 3) if v["type"] == "clip" else 0 for v in vis)
    stills = [v for v in vis if v["type"] == "image"]
    per = (sec - vsec) / len(stills) if stills else 0
    n["est_s"] = round(sec, 1)
    assert vis, f"{n['id']}: no visuals"
    assert per <= 4.0, f"{n['id']}: {per:.1f} s per still (> 4 s) - add stills"
    assert vsec >= sec - 1 if not stills else True, f"{n['id']}: b-roll too short"


def estimate(shots, hooks, refs_needed):
    clips = [s for s in shots if s["type"] == "clip"]
    narrs = [s for s in shots if s["type"] == "narration"]
    words = sum(len(re.findall(r"[A-Za-z']+", n["text"])) for n in narrs)
    vsec = sum(c["duration_s"] for c in clips) + sum(h["duration_s"] for h in hooks)
    n_img = sum(s["type"] == "image" for s in shots) + len(clips) + len(hooks)
    est = {"clips": len(clips), "clips_dialogue": sum(bool(c["dialogue"]) for c in clips), "broll": sum(c["broll"] for c in clips),
           "stills": sum(s["type"] == "image" for s in shots), "hooks": len(hooks), "video_seconds": vsec,
           "images_incl_first_frames": n_img, "ref_images": refs_needed, "narration_words": words,
           "narration_min_at_140wpm": round(words / WPM, 1),
           "est_runtime_min": round((sum(c["duration_s"] for c in clips) * 0.85 + words / WPM * 60
                                     + sum(s.get("duration_s", 0) for s in shots if s["type"] in ("title_card", "end"))) / 60, 1),
           "usd_video": round(vsec * 0.10, 2), "usd_images": round(n_img * 0.067, 2), "usd_refs_approx": round(refs_needed * 0.17, 2)}
    est["usd_total_approx"] = round(est["usd_video"] + est["usd_images"] + est["usd_refs_approx"] + 1.0, 2)
    est["usd_with_15pct_reserve"] = round(est["usd_total_approx"] * 1.15, 2)
    return est


def refs_used(shots, hooks):
    files = set()
    for s in list(shots) + list(hooks):
        for f in s.get("ref_files", []):
            if f.startswith("visuals/refs/"):
                files.add(f)
                if f.endswith("_full.png"):
                    files.add(f.replace("_full.png", "_front.png"))
    return files


def production(sample, hooks_on, opening):
    p = {
        "schema_version": 1,
        "policy_retry_max": 3,
        "review_gates": {"references": {"enabled": True}, "audio": {"enabled": True},
                         "visuals": {"enabled": True},
                         "video_sample": {"enabled": True, "shot_ids": sample},
                         "videos": {"enabled": True}},
        "edit": {"engine": "v2",
                 "badge_at": [[MARK["N01"], 2.0]] + ([] if opening else [[MARK["ride"], 0.5]]),
                 "grade": "eq=contrast=1.05:saturation=1.15:gamma=1.13:brightness=0.03",
                 "title_id": "T01",
                 "series_projects": {"S2": "western_stagecoach_bride_v1", "S3": "western_barn_storm_v1", "S4": "western_widows_rifle_v1"},
                 "jobs": 4,
                 "dialogue_tail_seconds": 0.8, "narration_voice_offset_seconds": 0.4, "transition_seconds": 0.3,
                 "end_screen_tail_seconds": 0, "contact_sheet": "one_frame_per_timeline_visual"},
        "music_anchor_map": {k: v for k, v in ANCHORS.items() if v in {s["id"] for s in TL}} if opening else ANCHORS,
        "audio_mix": {"speech_active_rms_db": -20, "ambient_clip_rms_db": -23, "broll_ambient_rms_db": -34, "music_base_rms_db": -18,
                      "duck_under_speech_db": -15, "duck_under_clip_db": -7, "duck_attack_seconds": 0.15,
                      "duck_release_seconds": 0.6, "integrated_lufs": -14, "true_peak_db": -1.5},
        "voice": {"provider": "elevenlabs", "voice_id": "pqHfZKP75CvOlQylNhV4", "model": "eleven_multilingual_v2",
                  "speed": 1, "timestamps": True, "output_format": "mp3_44100_128", "stability": 0.55,
                  "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True, "context_chars": 400},
        "subtitle": {"language": "en", "name": "English"},
        "export": {"package_branch": "pkg/western_sunday_bride_v1", "film_branch": "film/western_sunday_bride_v1"},
        "qc": {"long_duration_min_seconds": 120 if opening else 600, "long_duration_max_seconds": 1500, "black_silence_max_seconds": 60},
    }
    if hooks_on:
        p["hooks"] = {"count": 8}
    return p


def doc(title, timeline, hooks, est, prod):
    return {"title": title, "series": "Tales of Cedar Bluff", "episode": 5,
            "working_title_youtube": "\"Marry Me by Sunday, or They Take My Children,\" the Widow Begged the Drifter | Full Western Movie",
            "setting": "Cedar Bluff, Colorado (a state since 1876), late October 1881: Main Street, the church, the town hall courtroom, the Whitlock farm on Bitter Creek",
            "format": {"aspect": "16:9 (hooks 9:16)", "fps": 24, "clip_durations_allowed_s": [4, 6, 8]},
            "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE, "reused_refs_from": PREV,
            "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "ref_prompts": REF_PROMPTS,
            "timeline": timeline, "hooks": hooks, "production": prod}


here = os.path.dirname(os.path.abspath(__file__))
w = lambda name, obj: json.dump(obj, open(f"{here}/{name}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- whole film ----
TL = SHOTS
est_full = estimate(SHOTS, HOOKS, len(REF_PROMPTS))
w("shotlist.json", doc("Marry Me by Sunday", SHOTS, HOOKS, est_full, production(SAMPLE_FULL, True, False)))
w("music_cues.json", {"film": "Marry Me by Sunday", "note": "6 new cues + 3 reused from film 3 (S3) at no cost", "cues": CUES})

# ---- factory test: refs + opening (part A, or A+B with OPENING_PARTS=AB) ----
parts = os.environ.get("OPENING_PARTS", "A")
TL = [copy.deepcopy(s) for s in SHOTS if s["part"] in parts and s["type"] != "end"]
used = refs_used(TL, [])
open_refs = [r for r in REF_PROMPTS if r["file"] in used]
est_open = estimate(TL, [], len(open_refs))
opening_doc = doc("Marry Me by Sunday - opening test", TL, [], est_open, production(SAMPLE_OPENING, False, True))
opening_doc["ref_prompts"] = open_refs
cue_ids = set(opening_doc["production"]["music_anchor_map"])
w("shotlist_opening.json", opening_doc)
w("music_cues_opening.json", {"film": "Marry Me by Sunday - opening test", "cues": [c for c in CUES if c["id"] in cue_ids]})

missing_refs = [r["file"] for r in REF_PROMPTS if r["file"] not in used]
print(json.dumps({"FULL": est_full, f"OPENING_{parts}": est_open, "opening_refs_not_made_in_test": missing_refs,
                  "opening_last_shot": TL[-1]["id"]}, indent=1))
