# -*- coding: utf-8 -*-
"""Source of truth for "The Widow's Rifle" (Tales of Cedar Bluff, film 4). Screenplay: script.md (v1, 10 Oct 2026).
Generates shotlist.json and music_cues.json for the factory (film_package_prepare), edit engine v2.
Setting: Cedar Bluff, Colorado (a state since 1876 - never "Territory"), September 1881: the harvest fair and the
Cole farm on Willow Creek. Bright golden-aspen days; only the torch scene is at night.
Rules (films 1-3):
  * one speaker per clip; the line starts in the first second; long lines are split over two clips;
  * every narration block gets its own silent b-roll / stills (field "for"), never dialogue clips;
  * no weapon pointed at a woman or a child, no wounded close-ups (Google refuses them);
  * Hannah's rifle is ALWAYS the same single-shot Sharps (no lever, no magazine) and she reloads after every shot;
  * Hannah wears ONE outfit for the whole film (+ grey shawl at night); wagons only with horses harnessed in front;
  * no legible text anywhere in generated pictures; text is shown only by title cards;
  * 8 native vertical hooks (production.hooks.count = 8), one line each.
"""
import json, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado, September 1881, "
         "bright natural sunlight, golden aspens, 35mm film grain, warm vivid colors, shallow depth of field, "
         "period-accurate clothing and props. No text, no letters, no captions, no logos, no watermark, no modern objects.")
NIGHT = " Night: moonlight and warm torch or lamp light, faces clearly lit and readable."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, Colorado 1881, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
              "Serious, grounded drama: natural, restrained acting and natural voices, no comedic or exaggerated performances. "
              "Characters only speak the exact lines given, in English, with lips in sync. No subtitles, no text on screen, no music.")
ACTION = (" Fast, dynamic action from the very first frame: the movement is already happening when the shot starts, "
          "no slow build-up. Realistic weight and physics: real recoil, real gun smoke, real dust.")
RIFLE = (" The rifle is a long single-shot 1874 Sharps buffalo rifle with a long octagonal barrel, a dark walnut stock, "
         "no lever and no magazine; it fires one shot and is reloaded by hand.")
PREV = "pkg/western_stagecoach_bride_v1/visuals/refs"   # approved refs from films 1-2

CHARACTERS = {
 "CHAR_HANNAH": {"name": "Hannah Cole", "role": "widow, 31, a buffalo hunter's daughter and a crack shot",
   "look": "31-year-old American frontier woman, an original fictional character who does not resemble any actress, slender and strong, a sun-browned face, steady gray eyes, a thin pale scar on her chin, dark-blond hair in a low practical knot, ALWAYS the same faded blue calico dress with a small white collar and a short brown wool jacket",
   "voice": "calm, low, steady American woman's voice, early thirties, never shrill"},
 "CHAR_TOMMY": {"name": "Tommy Cole", "role": "her son, 10",
   "look": "10-year-old boy, an original fictional character, straw-blond cowlick, freckles, an oversized faded man's shirt with the sleeves rolled up, brown suspenders, patched trousers, scuffed boots",
   "voice": "clear, serious American boy's voice, ten years old"},
 "CHAR_JONAH": {"name": "Jonah Reed", "role": "a quiet stranger, 44, secretly the new owner of the bank",
   "look": "44-year-old American man, an original fictional character (not a celebrity lookalike), tall and lean, a short graying beard, gray at the temples, calm dark eyes with fine lines, a worn charcoal-gray frock coat, a dark vest with a silver watch chain, reading spectacles in the breast pocket, a narrow-brimmed brown hat",
   "voice": "quiet, slow, dry American baritone, a little wry"},
 "CHAR_HALE": {"name": "Ambrose Hale", "role": "bank manager and fair judge, 55",
   "look": "55-year-old American man, an original fictional character, clean-shaven with gray mutton-chop side whiskers, small gold pince-nez, a black frock coat, a red carnation in the lapel, a gold watch chain",
   "voice": "smooth, polite, cold American man's voice"},
 "CHAR_LAVINIA": {"name": "Lavinia Hale", "role": "his wife, runs the sign-up table, 50",
   "look": "50-year-old American woman, an original fictional character, piled-up gray-brown curls under a plumed hat, a lilac silk bustle dress, a lace fan",
   "voice": "loud, sugary, mocking American society lady's voice"},
 "CHAR_CLAY": {"name": "Clay Hale", "role": "Hale's nephew, three-time county champion, 25",
   "look": "25-year-old American man, an original fictional character, handsome and cocky, clean-shaven, a white wide-brimmed hat, a burgundy velvet vest, white shirt, an engraved lever-action rifle",
   "voice": "confident, laughing young American man's voice"},
 "CHAR_HOBBS": {"name": "Mr. Hobbs", "role": "storekeeper, announcer of the match, 50",
   "look": "50-year-old balding storekeeper, an original fictional character, round spectacles, sleeve garters, a striped shirt and a checked vest, a speaking trumpet in his hand",
   "voice": "nasal, fussy, carrying American voice"},
 "CHAR_DUTCH": {"name": "Dutch", "role": "Hale's hired man, 40",
   "look": "40-year-old rough man, an original fictional character, heavy black stubble, a dusty brown duster, a battered hat, a bandana pulled down around his neck",
   "voice": "rough, loud American man's voice"},
 "CHAR_NED": {"name": "Ned", "role": "Hale's second hired man, 30",
   "look": "30-year-old wiry man, an original fictional character, sandy stubble, a gray slicker, a flat cap",
   "voice": "thin, sneering American man's voice"},
 "CHAR_CLERK": {"name": "the telegraph clerk", "role": "depot telegraph operator, 60",
   "look": "60-year-old man, an original fictional character, a green eyeshade, white mustache, sleeve garters",
   "voice": "dry, curious old American man's voice"},
 "CHAR_FRIEND": {"name": "Clay's friend", "role": "young bully, no lines",
   "look": "22-year-old young man, an original fictional character, a smirk, a straw hat, a checked shirt and suspenders",
   "voice": "-"},
 # ---- recurring residents (refs exist) ----
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50", "reuse_refs": True,
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
 "CHAR_CLARA": {"name": "Clara Mercer", "role": "the widow of film 1, now married to John Mercer", "reuse_refs": True,
   "look": "26-year-old American frontier woman, very pretty, slender, gray-green eyes, warm chestnut hair with copper highlights in a soft braided crown, a dark-green Sunday dress, small oval silver locket",
   "voice": "warm, low, steady American woman's voice, late twenties"},
 "CHAR_MERCER": {"name": "John Mercer", "role": "Union veteran, Clara's husband", "reuse_refs": True,
   "look": "40-year-old man, tall and lean, weathered tanned face, short dark-brown beard with gray at the chin, calm gray-blue eyes, long dark-brown canvas duster coat, black flat-brimmed hat",
   "voice": "deep, quiet, unhurried American baritone"},
}
PROPS = {
 "PROP_SHARPS": {"name": "The Sharps rifle",
   "look": "a long single-shot 1874 Sharps buffalo rifle: long octagonal blued barrel, tall front blade sight, dark walnut stock worn smooth, no lever, no magazine; crossed wooden shooting sticks beside it"},
 "PROP_GOLD": {"name": "The prize",
   "look": "a small brown leather pouch spilling twenty-dollar gold coins onto a wooden table"},
}
LOCATIONS = {
 "LOC_FAIR": {"name": "Cedar Bluff fairground",
   "look": "a sunny frontier county fair on a meadow at the edge of town: colored bunting and flags, a rope line holding back a crowd in Sunday clothes, a firing line with canvas mats, round black-and-white paper targets on posts far down the field, a small hanging iron plate further away, golden aspens and blue mountains beyond, a wooden depot clock tower in the distance"},
 "LOC_SIGNUP": {"name": "Sign-up table",
   "look": "a cloth-covered table under a striped canvas awning at the fair, a ledger and an ink pot on it, a line of men with rifles waiting, bunting overhead"},
 "LOC_COLE": {"name": "Cole farm",
   "look": "a small two-room log house with a porch and one loose porch board, a crooked wooden gate on a sagging hinge, a water barrel by the porch, a small barn, a dozen hens, an old gray mare, a clear creek and a stand of golden aspens, a simple wooden cross under the aspens by the creek"},
 "LOC_COLE_IN": {"name": "Cole kitchen",
   "look": "plain log kitchen: a rough plank table, an oil lamp, a cast-iron pot on a small stove, a coffee can of old nails by the door, empty pegs above the stone fireplace"},
 "LOC_BANK": {"name": "Cedar Bluff Savings Bank",
   "look": "small frontier bank interior: a marble-topped counter, a brass teller's cage, dark wood paneling, a tall wall clock with a large white dial and black hands, a green-shaded lamp, a door with frosted glass (no legible letters)"},
 "LOC_HALE_OFFICE": {"name": "Hale's office",
   "look": "a bank manager's back office at dusk: a heavy desk under a green-shaded lamp, a large hand-drawn survey map of a valley unrolled on the desk with a creek circled in red ink (no legible letters), a safe, dark paneling"},
 "LOC_DEPOT": {"name": "Cedar Bluff depot",
   "look": "a small wooden railroad depot with a clock in a little tower, a telegraph window with a brass grille, a bench on the platform, rails and golden hills beyond"},
 "LOC_STREET": {"name": "Cedar Bluff main street", "reuse_refs": True,
   "look": "small frontier town main street, dirt road, wooden false-front buildings, boardwalks, hitching rails, horses and wagons, mountains beyond; signs have no legible text"},
}

SHOTS, HOOKS = [], []
_N = {"C": 0, "B": 0, "I": 0, "N": 0}


def _next(k):
    _N[k] += 1
    return f"{k}{_N[k]:02d}"


def _dur(lines):
    w = sum(len(l.split()) for _, l in lines)
    return 6 if not lines else 4 if w <= 5 else 6 if w <= 13 else 8


def clip(action, refs, line=None, camera="", night=False, action_shot=False, dur=None, rifle=False):
    lines = [line] if line else []
    act = action + (RIFLE if rifle else "")
    SHOTS.append({"id": _next("C"), "type": "clip", "duration_s": dur or _dur(lines), "action": act, "camera": camera,
                  "dialogue": [{"speaker": a, "line": b} for a, b in lines], "refs": refs, "priority": "core",
                  "night": night, "action_shot": action_shot, "broll": False, "start_frame_prompt": act})
    return SHOTS[-1]["id"]


def broll(action, refs, camera="", night=False, dur=6):
    """silent clip under the narrator of the block that follows (field 'for')."""
    SHOTS.append({"id": _next("B"), "type": "clip", "duration_s": dur, "action": action, "camera": camera, "dialogue": [],
                  "refs": refs, "priority": "core", "night": night, "action_shot": False, "broll": True,
                  "start_frame_prompt": action, "for": None})
    return SHOTS[-1]["id"]


def img(prompt, refs, night=False, motion="slow push in"):
    SHOTS.append({"id": _next("I"), "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "night": night, "for": None})


def narr(text):
    nid = _next("N")
    for s in reversed(SHOTS):                 # b-roll and stills written just before a narration block belong to it
        if s["type"] == "narration":
            break
        if s.get("for", 1) is None:
            s["for"] = nid
    SHOTS.append({"id": nid, "type": "narration", "text": " ".join(text.split())})
    return nid


def card(id_, text, seconds, big=False, subtitle=None):
    row = {"id": id_, "type": "title_card", "text": text, "duration_s": seconds}
    if big:
        row["big"] = True
    if subtitle:
        row["subtitle"] = subtitle
    SHOTS.append(row)


def hook(id_, beat, first_frame, video, refs, line, night=False):
    HOOKS.append({"id": id_, "beat": beat, "duration_s": 8, "refs": refs, "first_frame": first_frame, "video": video,
                  "night": night, "dialogue": [{"speaker": line[0], "line": line[1]}]})


H, T, J, HA, L, CL, HO = "CHAR_HANNAH", "CHAR_TOMMY", "CHAR_JONAH", "CHAR_HALE", "CHAR_LAVINIA", "CHAR_CLAY", "CHAR_HOBBS"
R = "PROP_SHARPS"
MARK = {}

# ======================= COLD OPEN (0:00-0:38): humiliation, no narrator until 0:28 =======================
MARK["open"] = clip("Sunny fair, a cloth-covered sign-up table under a striped awning: close on a woman's work-worn hand pouring a few coins onto the table; behind it Lavinia Hale, in lilac silk and a plumed hat, fans herself and counts with one gloved finger.",
     [L, H, "LOC_SIGNUP"], (L, "One dollar... and sixty cents."), camera="close on the coins, rack focus to Lavinia")
clip("The sign-up table: Lavinia Hale raises her voice so the whole line of men with rifles can hear, smiling sweetly at the widow in the blue calico dress.",
     [L, H, "LOC_SIGNUP"], (L, "Entry is two dollars, Mrs. Cole. This is a rifle match. Not a church raffle."), camera="over Hannah's shoulder toward Lavinia")
clip("The line of men with rifles bursts out laughing; a freckled boy in an oversized shirt hugs a long single-shot buffalo rifle tighter to his chest.",
     [T, R, "LOC_SIGNUP"], camera="medium shot on the laughing men, the boy in front", dur=4)
clip("Hannah Cole, in her faded blue calico dress and brown jacket, answers evenly, chin up, eyes steady.",
     [H, "LOC_SIGNUP"], (H, "I'll have the rest by noon."), camera="close-up")
clip("Lavinia Hale leans back with a sugary smile and snaps her lace fan shut.",
     [L, "LOC_SIGNUP"], (L, "By noon Saturday you won't have a farm, dear. Ambrose told me all about it."), camera="close-up")
clip("Clay Hale, cocky in a white hat and burgundy velvet vest, an engraved lever-action rifle on his shoulder, grins at the line of men.",
     [CL, "LOC_SIGNUP"], (CL, "Let her shoot, Aunt Lavinia. I could use a laugh."), camera="medium shot, the line laughing behind him")
clip("The men roar with laughter; Hannah lowers her eyes. Over her shoulder a weathered man's hand reaches in and sets four silver dimes on the table one by one.",
     [J, H, "LOC_SIGNUP"], (J, "Forty cents, ma'am. Write her name down."), camera="close on the dimes, then up to the stranger's calm face")
clip("Lavinia Hale looks up at the tall stranger in a worn charcoal frock coat, her fan frozen mid-air.",
     [L, "LOC_SIGNUP"], (L, "And who might you be?"), camera="close-up, low angle")
clip("Jonah Reed, tall and lean with a graying beard, answers quietly, not smiling.",
     [J, "LOC_SIGNUP"], (J, "Somebody who'd like to see her shoot."), camera="close-up")
broll("Hannah walks through the parting fair crowd toward the firing line, her son carrying the long Sharps buffalo rifle beside her; people whisper and smirk behind fans.",
      [H, T, R, "LOC_FAIR"], camera="tracking shot from behind, crowd on both sides")
MARK["N00"] = narr("""Hannah Cole had until noon the next day to pay a two-hundred-and-fifty-dollar note. She had a ten-year-old boy,
and her father's old buffalo rifle. The prize that day was two hundred and fifty dollars in gold.
And the whole town of Cedar Bluff had come to watch her lose.""")
card("T01", "THE WIDOW'S RIFLE", 4.0, big=True)

# ======================= SCENE 1: qualifying - first payoff by ~1:10 =======================
clip("The firing line at the fair: Mr. Hobbs in a checked vest raises a speaking trumpet to announce, the crowd behind the rope.",
     [HO, "LOC_FAIR"], (HO, "Two hundred yards, folks! Clay Hale, three years running champion of the county fair!"), camera="medium shot")
clip("Clay Hale fires his engraved lever-action rifle three times from the shoulder with a showy grin; far down the field a flag boy waves white; Clay tips his white hat to the ladies.",
     [CL, "LOC_FAIR"], camera="medium shot, the targets far behind", action_shot=True, dur=6)
clip("Mr. Hobbs lowers the speaking trumpet, embarrassed, and announces the next name; snickers in the crowd.",
     [HO, "LOC_FAIR"], (HO, "And... Mrs. Thomas Cole."), camera="medium close-up", dur=4)
clip("Hannah Cole lies down on a canvas mat and rests the long Sharps on crossed wooden shooting sticks; her son kneels beside her with a cartridge in his fingers and whispers.",
     [H, T, R, "LOC_FAIR"], (T, "Breathe out, Ma. Like Grandpa said."), camera="low side angle at ground level", rifle=True)
clip("Close on Hannah's steady gray eye along the barrel; she breathes out and squeezes the trigger: a heavy boom, a cloud of white gun smoke, real recoil into her shoulder.",
     [H, R, "LOC_FAIR"], camera="extreme close-up to medium", action_shot=True, dur=4, rifle=True)
clip("Far down the sunny field a flag boy beside a round black-and-white target waves a white flag for a bullseye; the whole crowd behind the rope falls silent.",
     ["LOC_FAIR"], camera="long lens down the field, then the silent crowd", dur=4)
clip("Lavinia Hale stops fanning; Clay Hale's grin fades; in the crowd the tall stranger in the charcoal coat allows himself the smallest smile.",
     [L, CL, J, "LOC_FAIR"], camera="three quick reaction angles in one move", dur=4)
broll("Golden fair afternoon: bunting snapping in the wind, pies on a table, horses at a hitching rail, children running along the rope line.",
      ["LOC_FAIR"], camera="slow drift")
img("A worn bank letter and a small pile of coins on a plank kitchen table in morning light, a man's hat on a peg behind (no legible text).", ["LOC_COLE_IN"])
img("Hail-flattened wheat field under a gray sky beside a small log house.", ["LOC_COLE"], motion="slow drift")
narr("""Her husband Tom had borrowed the money two springs before, for seed and fence wire, from the Cedar Bluff Savings Bank.
Then the hail took the wheat, and the fever took Tom. The note came due on Saturday at noon.
Mr. Ambrose Hale, who ran the bank, had refused her an extension twice. He had been very polite about it both times.""")
img("A buffalo hunter with a long Sharps rifle on crossed sticks teaching a young girl to aim across a wide golden prairie, an old army camp far behind.", [R], motion="slow push in")
img("Close-up: a weathered man's hand guiding a girl's small hand on a rifle stock, grass bending in the wind.", [R])
narr("""Her father had hunted buffalo on the Arkansas and scouted for the army, back when the herds still darkened the plains.
He had no sons. So he taught his daughter to read the wind in the grass, to breathe out before the trigger,
and never to shoot at anything she did not mean to hit.""")

# ======================= SCENE 2: the bent sight - second payoff =======================
clip("Noon break at the fair: a smirking young man in a straw hat knocks a long rifle off the wooden rifle rack and grinds his boot heel on the barrel near the muzzle, then strolls away.",
     ["CHAR_FRIEND", R, "LOC_FAIR"], camera="low angle on the boot and the barrel", action_shot=True, dur=4)
clip("Hannah lifts her rifle and sights along the barrel; her son looks over her shoulder at the front sight.",
     [H, T, R, "LOC_FAIR"], (T, "Ma... it's bent."), camera="close two-shot", rifle=True, dur=4)
clip("Hannah, quiet and pale, lowers the rifle.",
     [H, R, "LOC_FAIR"], (H, "It'll shoot a foot to the left now. Maybe more."), camera="close-up", rifle=True)
clip("Behind Hannah the tall stranger in the charcoal coat holds out his hand for the rifle.",
     [J, H, "LOC_FAIR"], (J, "May I?"), camera="over Hannah's shoulder", dur=4)
clip("Jonah Reed takes a small file and a brass hammer from his vest, taps the front sight of the long rifle with two precise strokes and sights along the barrel at a fence post.",
     [J, R, "LOC_FAIR"], camera="close on his hands, then his eye along the barrel", dur=6, rifle=True)
clip("Jonah hands the rifle back to Hannah with a short nod.",
     [J, H, R, "LOC_FAIR"], (J, "Your father kept this rifle well, ma'am. Somebody today didn't."), camera="two-shot", rifle=True)
clip("Hannah studies the stranger's face, wary.",
     [H, "LOC_FAIR"], (H, "Who are you, mister?"), camera="close-up", dur=4)
clip("Jonah Reed answers with a dry half-smile.",
     [J, "LOC_FAIR"], (J, "Reed. Jonah Reed. I fixed rifles in the army. Mostly the boys shot better than I did."), camera="close-up")
broll("A stagecoach with four horses harnessed in front pulls up at a small depot; a tall man in a charcoal coat steps down with one carpetbag.",
      [J, "LOC_DEPOT"], camera="wide shot")
img("Night: a tall man in a charcoal frock coat asleep sitting up on a depot bench, hat over his eyes, his carpetbag beside him.", [J, "LOC_DEPOT"], night=True)
narr("""Nobody in Cedar Bluff knew who Jonah Reed was. He had come in on Thursday's stage with one carpetbag and asked for a room at the hotel,
but every room in town was taken for the fair. He spent Thursday night on a bench at the depot,
and Friday morning, it seemed, standing in line behind a widow who was forty cents short.""")
clip("Second round, three hundred yards: Hannah fires from the canvas mat, a cloud of white smoke; far away a white flag waves; she opens the breech and reloads by hand.",
     [H, R, "LOC_FAIR"], camera="side angle, then long lens to the flag", action_shot=True, dur=6, rifle=True)
clip("Mr. Hobbs shouts through the speaking trumpet over the murmuring crowd.",
     [HO, "LOC_FAIR"], (HO, "Final round tomorrow at eleven! Mrs. Cole and Clay Hale!"), camera="medium shot, crowd behind")
clip("At the judges' table Ambrose Hale, in gold pince-nez with a red carnation, checks his gold pocket watch and speaks to his nephew without looking at him.",
     [HA, CL, "LOC_FAIR"], (HA, "Tomorrow you'll win, Clay. And you'll take your time doing it."), camera="close two-shot")

# ======================= SCENE 2b: the map - villain's motive =======================
clip("Dusk, a bank manager's back office under a green-shaded lamp, a survey map unrolled on the desk with a creek circled in red: Ambrose Hale speaks to two rough men holding their hats.",
     [HA, "CHAR_DUTCH", "CHAR_NED", "LOC_HALE_OFFICE"], (HA, "Mrs. Cole will not be at the match tomorrow."), camera="medium shot across the desk")
clip("The back office: Dutch, black stubble and a dusty duster, turns his hat in his hands.",
     ["CHAR_DUTCH", "LOC_HALE_OFFICE"], ("CHAR_DUTCH", "And if she is?"), camera="close-up", dur=4)
clip("Ambrose Hale sets two gold coins on the map with a click, his face calm in the lamp light.",
     [HA, "LOC_HALE_OFFICE"], (HA, "Then she'll be too tired to hold a rifle steady. Frighten her. Nothing more. Tonight."), camera="close-up, the coins in the foreground")
img("Close-up on a hand-drawn survey map under a green lamp: a valley, a winding creek circled in red ink, a pencil line of a railroad (no legible letters).", ["LOC_HALE_OFFICE"])
img("Two small farms upstream along a sunny creek, seen from a hill, golden aspens.", ["LOC_COLE"], motion="slow drift")
narr("""What Ambrose Hale did not tell the town was what lay on that desk: a surveyor's map from the railroad.
The new line would need water every twenty miles, and the best water in the valley ran through Willow Creek. Right through the Cole farm.
Hale had already bought the two farms upstream. Quietly. Through his wife's name.""")

# ======================= SCENE 2c: the telegraph - Jonah's mystery =======================
clip("Late afternoon at the depot telegraph window: the white-mustached clerk in a green eyeshade reads a slip of paper and looks up at the tall stranger.",
     ["CHAR_CLERK", J, "LOC_DEPOT"], ("CHAR_CLERK", "Books, mister? You a schoolteacher?"), camera="through the brass grille")
card("T02", "DENVER. ARRIVED THURSDAY. BOOKS WORSE THAN FEARED. SAY NOTHING UNTIL MONDAY. — J. REED", 4.0)
clip("Jonah Reed puts on his hat at the telegraph window.",
     [J, "LOC_DEPOT"], (J, "Something like that."), camera="close-up", dur=4)

# ======================= SCENE 3: the gate hinge - work, not charity =======================
broll("Sunset: a tall man in a charcoal coat walks a dirt road along a clear creek toward a small log house, golden aspens, hens scattering by a crooked gate.",
      [J, "LOC_COLE"], camera="wide, the farm ahead")
img("A small two-room log house by a creek at sunset, an old gray mare grazing, a crooked gate on a sagging hinge.", ["LOC_COLE"], motion="slow push in")
narr("""The Cole place sat three miles up Willow Creek, where the aspens turned gold every September.
Eighty acres, a two-room house Tom had built with his own hands, a barn, a dozen hens, and an old gray mare named Jessie who was too stubborn to die.
It was not much. But it was the only thing Tommy Cole had left of his father.""")
clip("Sunset at the Cole farm: Hannah steps out onto the porch with the long Sharps rifle held across her body, facing the stranger at the gate.",
     [H, R, "LOC_COLE"], (H, "That's close enough, Mr. Reed."), camera="from behind Jonah toward the porch", rifle=True, dur=4)
clip("At the crooked gate Jonah Reed takes off his hat.",
     [J, "LOC_COLE"], (J, "Hotel's full for the fair, ma'am. I'll pay fifty cents a night for your barn. And I'll fix that gate hinge before supper."), camera="medium shot", dur=8)
clip("Hannah, rifle lowered across her body, firm.",
     [H, R, "LOC_COLE"], (H, "I don't take charity."), camera="close-up", dur=4, rifle=True)
clip("Jonah Reed glances at the sagging gate.",
     [J, "LOC_COLE"], (J, "It isn't charity, ma'am. It's a bad hinge."), camera="close-up", dur=4)
clip("On the porch the freckled boy snorts with laughter; Hannah holds her face straight, then lowers the rifle and turns to the door.",
     [H, T, "LOC_COLE"], (H, "Supper's at six. Wash at the pump."), camera="two-shot on the porch", dur=4)
clip("Lamp-lit supper at a plank table: soup and bread; Jonah passes the bread and notices a bank letter on the table; the boy leans forward.",
     [T, J, H, "LOC_COLE_IN"], (T, "Were you a soldier, Mr. Reed?"), camera="wide on the table", night=True, dur=4)
clip("Jonah Reed, lamp light on his face, answers the boy seriously.",
     [J, "LOC_COLE_IN"], (J, "I was a clerk who carried a rifle. Then a man who fixed them. Then a man who counted other people's money."), camera="close-up", night=True, dur=8)
clip("The boy wrinkles his nose.",
     [T, "LOC_COLE_IN"], (T, "That sounds boring."), camera="close-up", night=True, dur=4)
clip("Jonah allows a small smile and dips his bread.",
     [J, "LOC_COLE_IN"], (J, "It was. That's why I came to the fair."), camera="close-up", night=True, dur=4)
broll("Dusk: Jonah, sleeves rolled up, sets a new hinge on the crooked gate with a screwdriver; the gate swings true.", [J, "LOC_COLE"], camera="medium shot")
img("Close-up: a man's hands working a pump handle at a farm well at dusk, a wrench beside it.", [J, "LOC_COLE"])
narr("""Jonah Reed fixed the gate hinge before supper, and the pump handle after, and a loose board on the porch that Tom Cole had meant to fix for two years.
He did not ask about the note on the table. He had already read it.""")
clip("Dusk on the porch: Hannah steps on the porch board, it no longer creaks; she stops and looks down.",
     [H, "LOC_COLE"], (H, "Tom meant to fix that board for two years."), camera="low angle on the board, then up to her face")
clip("Jonah, at the foot of the porch steps, points with his chin at a coffee can of old nails by the door.",
     [J, "LOC_COLE"], (J, "I used his nails, ma'am. They were in the coffee can by the door. Seemed right."), camera="medium shot, the can in the foreground")
clip("Hannah says nothing for a long moment, nods once and goes inside.", [H, "LOC_COLE"], camera="close-up", dur=4)
clip("Twilight under golden aspens by the creek: Hannah stands at a simple wooden cross; Jonah stops a few steps away with a lantern.",
     [H, J, "LOC_COLE"], (H, "Tom always said I was the better shot. He never minded. Most men would have."), camera="wide, then closer", dur=8)
clip("Jonah Reed, lantern low, quietly.",
     [J, "LOC_COLE"], (J, "Most men are fools, ma'am."), camera="close-up", dur=4)
clip("Hannah turns her head toward him.",
     [H, "LOC_COLE"], (H, "And you, Mr. Reed?"), camera="close-up", dur=4)
clip("Jonah looks at the lantern flame.",
     [J, "LOC_COLE"], (J, "I'm a fool about other things."), camera="close-up", dur=4)
img("A smiling young farmer whistling behind a plow and an old gray mare in a spring field, a log house behind (memory, soft light).", ["LOC_COLE"], motion="slow drift")
img("A wooden cross under golden aspens beside a creek at twilight, a lantern glowing nearby.", ["LOC_COLE"])
narr("""Tom Cole had been a quiet man who whistled when he plowed and could not hit a barn door with a shotgun.
He used to say he married the best rifle in Colorado so he would never have to learn.
When the fever came, he made Hannah promise two things: that she would keep the farm for the boy, and that she would never let anyone make her feel small.
She had kept the first promise for nine months. The second was harder.""")

# ======================= SCENE 4: torches - threat and the rifle (thumbnail) =======================
img("Night: moonlight over a creek and a small log house; the lamp in the window goes out.", ["LOC_COLE"], night=True, motion="slow push in")
img("Night: inside a dark barn a man lies awake on a bed of straw, eyes open, listening.", [J], night=True)
narr("""Hannah put out the lamp a little after nine. Tommy was asleep with his boots still on.
In the barn, a man who had counted money for twenty years lay awake on a bed of straw, listening to the creek, and thinking about a bent front sight.
At a quarter past eleven, he heard horses.""")
clip("Night at the Cole farm gate: two riders with bandanas over their faces and burning torches rein in; Dutch shouts toward the dark house.",
     ["CHAR_DUTCH", "CHAR_NED", "LOC_COLE"], ("CHAR_DUTCH", "Mrs. Cole! Mr. Hale says a widow's got no business at a man's match!"), camera="low angle, torch light", night=True, action_shot=True, dur=8)
clip("Night: Ned fires his revolver into the water barrel by the porch; water spurts out of the holes in the moonlight.",
     ["CHAR_NED", "LOC_COLE"], camera="close on the barrel, then Ned", night=True, action_shot=True, dur=4)
clip("Night: Ned, torch high, sneers at the house.",
     ["CHAR_NED", "LOC_COLE"], ("CHAR_NED", "Stay home tomorrow. Or this barn burns tonight."), camera="medium shot", night=True)
clip("Night: the door opens; Hannah in a gray shawl over her blue dress steps onto the porch and brings the long Sharps to her shoulder toward the gate; in the barn doorway Jonah stands with a lantern and does not move.",
     [H, J, R, "LOC_COLE"], (H, "Put the torch down, mister."), camera="from the gate toward the porch", night=True, rifle=True)
clip("Night: Dutch laughs behind his bandana, torch held high.",
     ["CHAR_DUTCH", "LOC_COLE"], ("CHAR_DUTCH", "Or what?"), camera="close-up", night=True, dur=4)
clip("Night: a heavy rifle boom from the porch; the burning torch flies out of Dutch's hand in a burst of sparks and hisses in the wet ditch; the horses rear.",
     ["CHAR_DUTCH", "LOC_COLE"], camera="medium shot, sparks", night=True, action_shot=True, dur=4)
clip("Night: Hannah opens the breech, slides in a new cartridge and closes it, calm, the rifle back at her shoulder.",
     [H, R, "LOC_COLE"], (H, "I don't miss, gentlemen. Come to the fair tomorrow and watch."), camera="close-up, torchlight on her face", night=True, rifle=True)
clip("Night: the two riders wheel their horses and gallop off down the creek road; dust in the moonlight.",
     ["CHAR_DUTCH", "CHAR_NED", "LOC_COLE"], camera="wide", night=True, action_shot=True, dur=4)
clip("Night, quiet: Jonah walks up to the foot of the porch.",
     [J, "LOC_COLE"], (J, "Your father taught you that?"), camera="medium shot", night=True, dur=4)
clip("Night: Hannah lowers the rifle, looking at the dark road.",
     [H, R, "LOC_COLE"], (H, "My father taught me to shoot. My husband taught me not to be afraid."), camera="close-up", night=True, rifle=True)
img("Night: a man sitting on a porch step with a lantern and a coffee pot, the house dark behind him, stars above the aspens.", [J, "LOC_COLE"], night=True)
img("Pale dawn light on the porch, the lantern burned out, the man still sitting there.", [J, "LOC_COLE"], motion="slow drift")
narr("""Jonah sat on the porch until the sun came up, with a lantern and a pot of coffee that went cold before midnight.
Hannah knew he was there. For the first time since the winter, she slept through the night.""")

# ======================= SCENE 4b: the lesson - warmth, sets up the last joke =======================
MARK["lesson"] = clip("Misty sunrise by the creek: a tin can on a fence post; Jonah fires the long Sharps from the shoulder, the recoil knocks his hat off; the can does not move.",
     [J, R, "LOC_COLE"], camera="medium shot, the can in the foreground", action_shot=True, dur=4, rifle=True)
clip("The freckled boy, hands on his hips, judges him.",
     [T, "LOC_COLE"], (T, "You're supposed to hit it, Mr. Reed."), camera="close-up", dur=4)
clip("Jonah picks up his hat.",
     [J, "LOC_COLE"], (J, "I'm aware of that, son."), camera="close-up", dur=4)
clip("The boy, very serious.",
     [T, "LOC_COLE"], (T, "Ma says breathe out first."), camera="close-up", dur=4)
clip("Jonah breathes out loudly, reloads the single-shot rifle by hand and fires again: smoke, the can still standing; on the porch Hannah laughs into her coffee cup.",
     [J, H, R, "LOC_COLE"], (J, "I breathed."), camera="medium shot, Hannah in the background", dur=6, rifle=True)

# ======================= SCENE 5: the final - main payoff =======================
broll("Saturday morning at the fair: the whole town at the rope line, wind snapping the bunting and bending the grass, targets far down the field.",
      ["LOC_FAIR"], camera="wide crane-like shot")
img("Hannah and her son walk to the firing line through a quiet crowd; nobody stands near them except a tall man in a charcoal coat.", [H, T, J, R, "LOC_FAIR"])
narr("""By Saturday morning, half of Cedar Bluff had heard about the torches. The other half had heard about the forty cents.
Nobody laughed at Hannah Cole that morning. But nobody stood next to her either.
Except a ten-year-old boy, and a stranger who still had no room at the hotel.""")
clip("At the rope line Lavinia Hale, in lilac, speaks loudly to her circle of fine ladies behind her fan.",
     [L, "LOC_FAIR"], (L, "A widow with a strange man sleeping in her barn. And now she wants a prize for it."), camera="medium shot")
clip("Clara Mercer, in a dark-green Sunday dress, steps out of the crowd beside her husband John Mercer and faces Lavinia.",
     ["CHAR_CLARA", "CHAR_MERCER", L, "LOC_FAIR"], ("CHAR_CLARA", "Lavinia, the last stranger who slept in a widow's barn here paid two hundred in gold for my mother's piano."), camera="over Lavinia's shoulder", dur=8)
clip("Clara Mercer, a small smile.",
     ["CHAR_CLARA", "LOC_FAIR"], ("CHAR_CLARA", "Then I married him. I'd keep my voice down."), camera="close-up")
clip("The ladies around Lavinia titter behind their hands; John Mercer touches his hat brim toward the tall stranger, who nods back.",
     [L, "CHAR_MERCER", J, "LOC_FAIR"], camera="two quick angles", dur=4)
clip("At the judges' table Ambrose Hale makes a show of inspecting rifles and straightening papers, then looks at his gold watch.",
     [HA, "LOC_FAIR"], (HA, "We'll wait for the wind to settle, ladies and gentlemen."), camera="medium shot")
clip("Jonah leans down to Hannah at the firing line and speaks low.",
     [J, H, "LOC_FAIR"], (J, "He's not waiting for the wind. He's waiting for noon."), camera="close two-shot")
img("Close-up: the clock in the depot tower, its hands at twenty past eleven, golden hills behind (no letters on the dial).", ["LOC_DEPOT"])
img("Close-up: the depot tower clock, hands at twenty-five to twelve.", ["LOC_DEPOT"], motion="slow push in")
clip("Clay Hale fires three quick shots; Hannah fires three slow shots from the mat, reloading by hand each time; far away white flags wave for both.",
     [CL, H, R, "LOC_FAIR"], camera="intercut-style move along the firing line", action_shot=True, dur=8, rifle=True)
clip("Mr. Hobbs, excited, through the speaking trumpet; the crowd buzzing.",
     [HO, "LOC_FAIR"], (HO, "A tie! One shot each. The iron plate at six hundred yards!"), camera="medium shot")
clip("Clay Hale, standing, fires at the far iron plate: dust spurts to the right of the plate; no sound of steel. He goes pale.",
     [CL, "LOC_FAIR"], camera="over his shoulder, long lens to the plate", action_shot=True, dur=6)
clip("Hannah lies on the mat with the long Sharps on the crossed sticks; her son watches the grass bend in the wind and whispers.",
     [H, T, R, "LOC_FAIR"], (T, "Wind's from the left, Ma. A hand and a half."), camera="ground level, the grass in the foreground", rifle=True)
clip("A long silent breath; Hannah fires: a heavy boom and white smoke; a second later a faraway ringing clang of steel; the crowd explodes in cheers, hats in the air.",
     [H, R, "LOC_FAIR"], camera="close on Hannah, then wide on the crowd", action_shot=True, dur=6, rifle=True)
clip("Mr. Hobbs counts twenty-dollar gold coins into a leather pouch; Lavinia Hale closes her fan without a word.",
     [HO, L, "PROP_GOLD", "LOC_FAIR"], camera="close on the coins, then Lavinia", dur=4)
clip("Clay Hale walks up and offers Hannah his hand, unexpectedly honest.",
     [CL, H, "LOC_FAIR"], (CL, "That was a fine shot, ma'am."), camera="two-shot", dur=4)
clip("Hannah shakes his hand.",
     [H, CL, "LOC_FAIR"], (H, "Yours wasn't bad either, Mr. Hale. The wind just didn't like you today."), camera="two-shot")
img("Close-up: the depot tower clock, hands at eight minutes to twelve.", ["LOC_DEPOT"])
broll("Hannah and her son run across the dusty town square toward a small brick bank, the gold pouch in her hand, the rifle on the boy's shoulder.",
      [H, T, R, "LOC_STREET"], camera="tracking shot")
narr("""Old men in Cedar Bluff argued about that shot for years. Some said it was six hundred yards, some said seven.
Hobbs swore the plate rang so loud the horses at the depot spooked. But everybody agreed on one thing.
Clay Hale had missed by a foot. Hannah Cole had not missed at all.""")

# ======================= SCENE 6: the clock - reveal =======================
clip("Inside the small bank: Hannah pours gold coins out of the pouch onto the marble counter in front of Ambrose Hale behind the brass cage.",
     [H, HA, "PROP_GOLD", "LOC_BANK"], (H, "Two hundred and fifty dollars, Mr. Hale. In full."), camera="over Hale's shoulder", action_shot=True)
clip("Ambrose Hale, without looking at the money, nods at the tall wall clock whose hands show one minute past twelve.",
     [HA, "LOC_BANK"], (HA, "I'm afraid it's past noon, Mrs. Cole. The note is past due. The property belongs to the bank."), camera="close-up, the clock behind him", dur=8)
clip("The bank door opens; Jonah Reed walks in, Marshal Abel Hart behind him.",
     [J, "CHAR_MARSHAL", "LOC_BANK"], (J, "Your clock is four minutes fast, Mr. Hale. The depot says eleven fifty-seven."), camera="medium shot from the counter")
clip("Ambrose Hale stiffens behind the cage.",
     [HA, "LOC_BANK"], (HA, "And who are you to tell me how to run my bank?"), camera="close-up")
clip("Jonah lays folded papers with a wax seal on the marble counter and puts on his reading spectacles.",
     [J, "LOC_BANK"], (J, "It isn't your bank, Ambrose. It never was. The Denver owners sold it on Thursday. To me."), camera="close on the papers, then his face", dur=8)
clip("Behind the brass grille the young teller drops his pen; silence in the bank.", ["LOC_BANK"], camera="close-up", dur=4)
clip("Jonah Reed, spectacles on, calm.",
     [J, "LOC_BANK"], (J, "I came early to see how my bank treats people. Then I read your survey maps."), camera="close-up")
clip("Jonah Reed continues, looking straight at Hale.",
     [J, HA, "LOC_BANK"], (J, "You've been buying every farm along Willow Creek with the bank's money. In your wife's name."), camera="over Hale's shoulder", dur=8)
clip("Marshal Abel Hart holds out his hand across the counter.",
     ["CHAR_MARSHAL", HA, "LOC_BANK"], ("CHAR_MARSHAL", "I'll take your keys, Ambrose. The rest we'll talk about at my office."), camera="medium shot")
clip("Ambrose Hale slowly unhooks a ring of keys from his watch chain and puts it in the marshal's hand; Jonah dips a pen and stamps the note.",
     [HA, "CHAR_MARSHAL", J, "LOC_BANK"], camera="close on the keys, then the stamp coming down", dur=6)
clip("Hannah looks at Jonah across the counter.",
     [H, "LOC_BANK"], (H, "You could have just paid it on Friday."), camera="close-up", dur=4)
clip("Jonah, dry.",
     [J, "LOC_BANK"], (J, "You'd have thrown me off your porch."), camera="close-up", dur=4)
clip("Hannah, the faintest smile.",
     [H, "LOC_BANK"], (H, "Yes. I would have."), camera="close-up", dur=4)
broll("A stagecoach with four horses harnessed in front leaves town on a sunny Monday morning, a man in a black frock coat looking back from the window.",
      [HA, "LOC_STREET"], camera="wide")
img("A railroad water tower beside a sunny creek, golden aspens, a small farm in the distance.", ["LOC_COLE"], motion="slow drift")
narr("""Ambrose Hale left Cedar Bluff on the Monday stage and did not come back. The farms along Willow Creek went back to the people who had worked them,
and when the railroad built its water tower two years later, it paid Hannah Cole a fair price for the land under it.
Lavinia Hale never ran the sign-up table again.""")
img("Monday morning: farmers holding their hats wait in line at the open door of the small bank; a tall man in spectacles unlocks it himself.", [J, "LOC_STREET"])
img("Inside the bank a small brass plaque hangs over the teller's window (no legible letters), sunlight on the marble counter.", ["LOC_BANK"])
narr("""On Monday morning the new owner of the Cedar Bluff Savings Bank unlocked the doors himself.
By noon he had extended eleven notes, lowered the interest on every farm loan in the valley, and hung a small brass sign over the teller's window.
It said: no one in this bank is too small to be heard. Folks said it was the first time anybody in Cedar Bluff had read a bank sign twice.""")

# ======================= SCENE 7: the gate - proposal =======================
MARK["prop"] = clip("October sunset, golden aspens, first frost on the grass: Jonah kneels at the gate with a screwdriver; Hannah watches from the path.",
     [H, J, "LOC_COLE"], (H, "There are rooms at the hotel now, Mr. Reed."), camera="wide, the gate in the foreground")
clip("Jonah, not looking up.", [J, "LOC_COLE"], (J, "I know."), camera="close-up", dur=4)
clip("Hannah folds her arms.", [H, "LOC_COLE"], (H, "That gate hasn't squeaked in a month."), camera="close-up", dur=4)
clip("Jonah sets down the screwdriver, stands and takes off his hat.",
     [J, "LOC_COLE"], (J, "I know that too. Hannah, I've counted other people's money for twenty years. I've never had anything worth coming home to."), camera="medium close-up", dur=8)
clip("Jonah Reed, hat in his hands, quietly.",
     [J, "LOC_COLE"], (J, "Marry me. I'd like to fix this gate for the rest of my life."), camera="close-up")
clip("Hannah says nothing, her eyes wet.", [H, "LOC_COLE"], camera="close-up", dur=4)
clip("On the porch the freckled boy cups his hands around his mouth and shouts.",
     [T, "LOC_COLE"], (T, "Say yes, Ma! He's a terrible shot. Somebody's got to look after him!"), camera="medium shot")
MARK["yes"] = clip("Hannah laughs through her tears and nods; Jonah exhales; the boy jumps off the porch.", [H, J, T, "LOC_COLE"], camera="wide, golden light", dur=6)
img("A small white frontier church on main street before the first snow, a wedding party on the steps throwing rice, a boy in new boots in front.", [H, J, T, "LOC_STREET"])
img("A long Sharps rifle hanging on pegs above a stone fireplace in a log kitchen, firelight.", [R, "LOC_COLE_IN"])
img("A grown young man with straw-blond hair firing a long Sharps rifle at a county fair, crowd cheering (years later).", [R, "LOC_FAIR"], motion="slow drift")
narr("""They were married in the little white church on Main Street before the first snow.
Tommy Cole won the county fair rifle match eleven years later, with his grandfather's old Sharps, and he always said he'd learned to read the wind from his mother.
Jonah Reed never did learn to shoot straight. He said one champion in the family was plenty.
And every September, on the morning of the match, he fixed the gate, whether it needed it or not.""")
img("Night, frost: the lamp glowing in the window of the small log house by the creek, golden aspens silver in the moonlight.", ["LOC_COLE"], night=True, motion="slow push in")
narr("""That's the story of the widow's rifle. And if you ever pass through Cedar Bluff in September, folks there will still tell you about it.
Keep a light in the window.""")
SHOTS.append({"id": "E01", "type": "end", "clip": MARK["yes"], "at": 3, "series": "TALES OF CEDAR BLUFF",
              "tagline": "Keep a light in the window", "duration_s": 12})

# ======================= 8 VERTICAL HOOKS (native 9:16, one line each) =======================
hook("H01", "humiliation", "Vertical 9:16. Sunny fair sign-up table: close on a weathered man's hand setting four silver dimes on the cloth one by one, a woman in blue calico looking down, a lady in lilac with a fan behind the table.",
     "He puts down the coins and speaks quietly; the laughing line goes silent.", [J, H, L, "LOC_SIGNUP"], (J, "Forty cents, ma'am. Write her name down."))
hook("H02", "reveal", "Vertical 9:16. Ground level at a fair firing line: a woman lying behind a long single-shot buffalo rifle on crossed sticks, a freckled boy kneeling at her ear.",
     "The boy whispers; she breathes out." + RIFLE, [T, H, R, "LOC_FAIR"], (T, "Breathe out, Ma. Like Grandpa said."))
hook("H03", "threat", "Vertical 9:16. Close on a long rifle barrel with a bent front sight in a tall man's hands, a small file in his fingers, a fair in soft focus behind.",
     "He straightens the sight and hands the rifle back." + RIFLE, [J, R, "LOC_FAIR"], (J, "Somebody today didn't."))
hook("H04", "threat", "Vertical 9:16. Night porch: a woman in a gray shawl with a long single-shot rifle at her shoulder, torch light flickering on her face, sparks in the dark behind.",
     "She reloads calmly and speaks to the riders at the gate." + RIFLE, [H, R, "LOC_COLE"], (H, "I don't miss, gentlemen."), night=True)
hook("H05", "reveal", "Vertical 9:16. Ground level in tall bending grass: a freckled boy watching the wind, his mother behind a long rifle in soft focus.",
     "He whispers the wind call; she fires, white smoke." + RIFLE, [T, H, R, "LOC_FAIR"], (T, "Wind's from the left, Ma. A hand and a half."))
hook("H06", "threat", "Vertical 9:16. A frontier bank: a woman's hand slaps a pile of gold coins on a marble counter; a tall wall clock behind the cage.",
     "A tall man in a charcoal coat walks in and speaks to the manager.", [J, H, "PROP_GOLD", "LOC_BANK"], (J, "Your clock is four minutes fast, Mr. Hale."))
hook("H07", "reveal", "Vertical 9:16. Close on folded papers with a red wax seal laid on a marble bank counter; a man in spectacles behind them.",
     "He looks up at the manager, calm.", [J, "LOC_BANK"], (J, "It isn't your bank, Ambrose."))
hook("H08", "joke", "Vertical 9:16. A freckled boy on a log-house porch at golden sunset cupping his hands around his mouth to shout.",
     "He shouts across the yard, grinning.", [T, "LOC_COLE"], (T, "Say yes, Ma! He's a terrible shot!"))


# ======================= BUILD =======================
def ref_text(refs):
    parts = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src:
            parts.append(f"{src['name']}: {src['look']}")
    return " | ".join(parts)


MINOR = {"CHAR_HOBBS", "CHAR_DUTCH", "CHAR_NED", "CHAR_CLERK", "CHAR_FRIEND"}


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


ids = [s["id"] for s in SHOTS]
assert len(ids) == len(set(ids)), "duplicate ids"
for s in SHOTS:
    if s["type"] == "image":
        s["full_prompt"] = s["prompt"] + " " + STYLE + (NIGHT if s["night"] else "") + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else "")
        s["ref_files"] = ref_files(s["refs"])
        s["file"] = f"visuals/images/wr_{s['id']}.png"
    elif s["type"] == "clip":
        s["start_frame_full_prompt"] = (s["start_frame_prompt"] + " First frame of the shot, characters in position" + (", mouths closed" if s["dialogue"] else "")
                                        + (", the action already in motion" if s["action_shot"] else "") + ". " + STYLE + (NIGHT if s["night"] else "")
                                        + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else ""))
        s["ref_files"] = ref_files(s["refs"])
        present = [r for r in s["refs"] if r in CHARACTERS]
        if s["dialogue"]:
            d = s["dialogue"][0]
            c = CHARACTERS[d["speaker"]]
            assert len(d["line"].split()) <= 24, f"{s['id']}: line too long for one clip"
            dl = (f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}"'
                  + (f" ONLY {c['name']} speaks. Everyone else keeps their mouth closed and only listens." if len(present) > 1 else "")
                  + " The line starts within the first second; after the line the speaker holds a natural expression, no extra words.")
        else:
            dl = " No dialogue, natural sound only (wind, crowd murmur, hooves, birds, gunshots where shown), nobody speaks."
        s["video_prompt"] = (s["action"] + (ACTION if s["action_shot"] else "") + (" Camera: " + s["camera"] + "." if s["camera"] else "")
                             + dl + " " + CLIP_STYLE)
        s["files"] = {"start_frame": f"visuals/images/wr_{s['id']}_first.png", "video": f"visuals/video/wr_{s['id']}.mp4"}
VSTYLE = STYLE.replace("16:9 widescreen", "9:16 vertical portrait frame") + " Bright, faces large and clearly lit."
for h in HOOKS:
    h["first_frame_full_prompt"] = h["first_frame"] + " " + VSTYLE + (NIGHT if h["night"] else "") + " Characters/places: " + ref_text(h["refs"])
    d = h["dialogue"][0]
    c = CHARACTERS[d["speaker"]]
    h["video_prompt"] = (h["video"] + f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}" The line starts within the first second; no extra words. '
                         + CLIP_STYLE.replace("16:9", "9:16 vertical portrait frame, subjects large and centered"))
    h["ref_files"] = ref_files(h["refs"])
    h["files"] = {"start_frame": f"visuals/hooks/wr_{h['id']}_first.png", "video": f"visuals/hooks/wr_{h['id']}.mp4"}

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

# ======================= MUSIC (4 new cues + 2 from film 3 at no cost) =======================
TAIL = (" Instrumental only, no vocals, no choir. Warm analog recording, cinematic western film score, 1880s American frontier feel, "
        "no modern drums, no synths, no electric guitar.")
CUES = [
    {"id": "M01", "covers": "cold open humiliation, the bent sight", "target_s": 60, "mood": "humiliation and quiet pride", "new": True, "instrumental": True,
     "prompt": "Slow aching western cue at 68 BPM in E minor: solo piano with a sparse melody, low sustained strings underneath, a lonely cello answering, dignified sadness that slowly gains resolve." + TAIL},
    {"id": "M02", "covers": "the fair, qualifying, the depot", "target_s": 75, "mood": "sunny small-town fair, light tension", "new": True, "instrumental": True,
     "prompt": "Bright but restrained western fair cue at 96 BPM in G major: fiddle and five-string banjo playing a simple tune, light upright bass and acoustic guitar, a hint of suspense in the low strings, sunny afternoon." + TAIL},
    {"id": "M03", "covers": "the map, the torches at night", "target_s": 60, "mood": "night threat", "new": True, "instrumental": True,
     "prompt": "Dark night-threat western cue at 72 BPM in D minor: low tremolo strings, muted horse-hoof percussion on a frame drum, a single harmonica bend, a rising tension that breaks off abruptly." + TAIL},
    {"id": "M04", "covers": "the final round, the six-hundred-yard shot, the bank", "target_s": 90, "mood": "building suspense to triumph", "new": True, "instrumental": True,
     "prompt": "Suspense-to-triumph western cue at 84 BPM in A minor turning to A major: a slow ticking pizzicato like a clock, strings building tension over a long crescendo, a held silence, then a full warm swell of strings and fiddle." + TAIL},
    {"id": "M05s", "series_source": "S3:M02", "covers": "walk to the farm, supper, the porch board, the grave", "target_s": 60, "mood": "bittersweet lullaby"},
    {"id": "M08s", "series_source": "S3:M01", "covers": "night, the torches", "target_s": 60, "mood": "storm and dread"},
    {"id": "M06s", "series_source": "S3:M03", "covers": "the lesson at sunrise", "target_s": 90, "mood": "quiet tenderness"},
    {"id": "M07s", "series_source": "S3:M04", "covers": "aftermath, the bank sign, the proposal, the wedding", "target_s": 60, "mood": "warm triumph"},
]
first_of = lambda pred: next(s["id"] for s in SHOTS if pred(s))
ANCHORS = {
    "M01": MARK["open"],
    "M02": "T01",
    "M03": first_of(lambda s: s["type"] == "clip" and "back office" in s["action"]),
    "M05s": first_of(lambda s: s["type"] == "narration" and s["text"].startswith("The Cole place")),   # b-roll is consumed by its narration
    "M08s": first_of(lambda s: s["type"] == "narration" and s["text"].startswith("Hannah put out the lamp")),
    "M06s": MARK["lesson"],
    "M04": first_of(lambda s: s["type"] == "narration" and s["text"].startswith("By Saturday morning")),
    "M07s": first_of(lambda s: s["type"] == "narration" and s["text"].startswith("Ambrose Hale left")),
}
# one anchor per cue: each cue plays from its anchor until the next cue starts (2 s crossfade)

clips = [s for s in SHOTS if s["type"] == "clip"]
narrs = [s for s in SHOTS if s["type"] == "narration"]
words = sum(len(re.findall(r"[A-Za-z']+", n["text"])) for n in narrs)
vsec = sum(c["duration_s"] for c in clips) + sum(h["duration_s"] for h in HOOKS)
n_img = sum(s["type"] == "image" for s in SHOTS) + len(clips) + len(HOOKS)
est = {"clips": len(clips), "clips_dialogue": sum(bool(c["dialogue"]) for c in clips), "broll": sum(c["broll"] for c in clips),
       "hooks": len(HOOKS), "video_seconds": vsec, "images_incl_first_frames": n_img, "ref_images": len(REF_PROMPTS),
       "narration_words": words, "narration_min_at_140wpm": round(words / 140, 1),
       "usd_video": round(vsec * 0.10, 1), "usd_images": round(n_img * 0.067, 1), "usd_refs_approx": round(len(REF_PROMPTS) * 0.17, 1)}
est["usd_total_approx"] = round(est["usd_video"] + est["usd_images"] + est["usd_refs_approx"] + 1.5, 1)

out = {"title": "The Widow's Rifle", "series": "Tales of Cedar Bluff", "episode": 4,
       "working_title_youtube": "They Laughed When the Widow Signed Up for the Shooting Match — Then She Fired | Full Western Movie",
       "setting": "Cedar Bluff, Colorado (a state since 1876), September 1881: the harvest fair and the Cole farm on Willow Creek",
       "format": {"aspect": "16:9 (hooks 9:16)", "fps": 24, "clip_durations_allowed_s": [4, 6, 8]},
       "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE, "reused_refs_from": PREV,
       "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "ref_prompts": REF_PROMPTS,
       "timeline": SHOTS, "hooks": HOOKS,
       "production": {
           "schema_version": 1,
           "hooks": {"count": 8},
           "policy_retry_max": 3,
           "review_gates": {"references": {"enabled": True}, "audio": {"enabled": False},
                            "visuals": {"enabled": True}, "video_sample": {"enabled": True}, "videos": {"enabled": False}},
           "edit": {"engine": "v2",
                    "badge_at": [[MARK["N00"], 2.0], [MARK["lesson"], 0.5]],
                    "grade": "eq=contrast=1.05:saturation=1.15:gamma=1.13:brightness=0.03",
                    "title_id": "T01",
                    "series_projects": {"S2": "western_stagecoach_bride_v1", "S3": "western_barn_storm_v1"},
                    "jobs": 4,
                    "dialogue_tail_seconds": 0.8, "narration_voice_offset_seconds": 0.4, "transition_seconds": 0.3,
                    "end_screen_tail_seconds": 0, "contact_sheet": "one_frame_per_timeline_visual"},
           "music_anchor_map": ANCHORS,
           "audio_mix": {"speech_active_rms_db": -20, "ambient_clip_rms_db": -23, "broll_ambient_rms_db": -34, "music_base_rms_db": -18,
                         "duck_under_speech_db": -15, "duck_under_clip_db": -7, "duck_attack_seconds": 0.15,
                         "duck_release_seconds": 0.6, "integrated_lufs": -14, "true_peak_db": -1.5},
           "voice": {"provider": "elevenlabs", "voice_id": "pqHfZKP75CvOlQylNhV4", "model": "eleven_multilingual_v2",
                     "speed": 1, "timestamps": True, "output_format": "mp3_44100_128", "stability": 0.55,
                     "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True, "context_chars": 400},
           "subtitle": {"language": "en", "name": "English"},
           "export": {"package_branch": "pkg/western_widows_rifle_v1", "film_branch": "film/western_widows_rifle_v1"},
           "qc": {"long_duration_min_seconds": 600, "long_duration_max_seconds": 1500, "black_silence_max_seconds": 60},
       }}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(f"{here}/shotlist.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"film": "The Widow's Rifle", "note": "4 new cues + 4 reused from film 3 (S3) at no cost", "cues": CUES},
          open(f"{here}/music_cues.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(est, indent=1))
