# -*- coding: utf-8 -*-
"""Source of truth for "The Barn in the Storm" (Tales of Cedar Bluff, film 3). Screenplay: script.md (v1, 8 Oct 2026).
Generates shotlist.json, music_cues.json (empty - the edit reuses the series score) and screenplay_shots.md.
Setting: a valley ranch near Cedar Bluff, Colorado (a state since 1876 - never "Territory"), spring 1881.
Bright spring days between storms; night/rain only in the cold open, the porch/gate nights and the showdown.
Rules learned on film 2:
  * one speaker per clip; the line starts in the first second;
  * every narration block gets its own silent b-roll / stills (field "for": "N05"), never dialogue clips;
  * no weapon pointed at a woman or a child, no wounded close-ups (Google refuses them);
  * shorts are shot natively vertical in the same batch (hooks H01..H04).
"""
import json, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado, spring 1881, "
         "natural light, 35mm film grain, warm vivid colors, green spring grass and wildflowers, shallow depth of field, "
         "period-accurate clothing and props. No text, no captions, no logos, no watermark, no modern objects.")
NIGHT = " Night storm: heavy rain, lightning flashes and warm lantern or lamp light, faces clearly lit and readable."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, Colorado 1881, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
              "Serious, grounded drama: natural, restrained acting and natural voices, no comedic or exaggerated performances. "
              "Characters only speak the exact lines given, in English, with lips in sync. No subtitles, no text on screen, no music.")
ACTION = (" Fast, dynamic action from the very first frame: the movement is already happening when the shot starts, "
          "no slow build-up. Realistic weight and physics, real rain, real mud.")
PREV = "pkg/western_stagecoach_bride_v1/visuals/refs"   # approved refs from films 1-2

CHARACTERS = {
 "CHAR_WADE": {"name": "Wade Harlan", "role": "widowed rancher, 38, former Texas Ranger captain",
   "look": "38-year-old American man, an original fictional character (not a celebrity lookalike), tall and broad-shouldered, short dark beard with first streaks of gray, tired steady gray-blue eyes, weathered tanned face, sweat-darkened brown felt hat with a pinched crown, dark-blue work shirt with rolled sleeves, worn brown leather vest, plain gun belt, no badge",
   "voice": "low, slow, dry American man's voice with a Texas drawl, few words"},
 "CHAR_ELLIE": {"name": "Ellie Price", "role": "young widow on the run, 27",
   "look": "27-year-old American woman, an original fictional character who does not resemble any actress, slender, a gentle tired face with soft freckles, clear green eyes, strawberry-blond hair in a simple loose knot with strands falling free, a faded dark-blue calico dress with a darned patch on the left elbow, a gray knitted shawl",
   "voice": "soft, tired but stubborn American woman's voice, late twenties, a schoolteacher's careful diction"},
 "CHAR_MOLLY": {"name": "Molly Price", "role": "Ellie's daughter, 7",
   "look": "7-year-old girl, an original fictional character, reddish-blond hair in two short braids, freckles, a missing front tooth, a small brown calico dress with a white collar, oversized scuffed boots",
   "voice": "bright, direct American little girl's voice, seven years old"},
 "CHAR_PIKE": {"name": "Deacon Pike", "role": "hired gun, 45",
   "look": "45-year-old gaunt man, an original fictional character, a thin pale scar through his left eyebrow, clean-shaven hollow cheeks, cold pale eyes, black flat-brimmed hat, long dusty black duster coat, black string tie",
   "voice": "quiet, cold, slow American man's voice, almost polite"},
 "CHAR_GREER": {"name": "Thaddeus Greer", "role": "Vance's attorney, 50",
   "look": "50-year-old soft-faced man, an original fictional character, small steel-rimmed spectacles, neat gray side whiskers, black bowler hat, brown checked suit, a leather document folder",
   "voice": "smooth, oily, overly polite American lawyer's voice"},
 "CHAR_VANCE": {"name": "Lucius Vance", "role": "Leadville silver king, Sam's grandfather, 65",
   "look": "65-year-old thin rich man, an original fictional character, snow-white side whiskers, hard narrow face, black frock coat, gold watch chain, a black cane with a silver knob",
   "voice": "dry, cold, commanding old American man's voice"},
 "CHAR_WHITCOMB": {"name": "Edna Whitcomb", "role": "the town gossip, 55",
   "look": "55-year-old woman, an original fictional character, tight dark-gray curls under a lilac bonnet, a lace collar, a dove-gray bustle dress, a lorgnette on a chain, pursed lips",
   "voice": "sharp, sugary-poisonous middle-aged American woman's voice"},
 "CHAR_HOBBS": {"name": "Mr. Hobbs", "role": "storekeeper, 50",
   "look": "50-year-old balding storekeeper, an original fictional character, round spectacles, sleeve garters, a long white apron over a striped shirt",
   "voice": "nasal, fussy American shopkeeper's voice"},
 "CHAR_BARMAN": {"name": "the bartender", "role": "saloon bartender, 40",
   "look": "40-year-old bartender, an original fictional character, waxed handlebar mustache, slicked dark hair, white shirt with sleeve garters, a bar towel over the shoulder",
   "voice": "flat, wary American man's voice"},
 "CHAR_GUNMAN": {"name": "the hired gunman", "role": "one of Pike's men",
   "look": "35-year-old rough man, an original fictional character, red stubble, a yellow oilskin rain slicker, a battered brown hat, a rifle",
   "voice": "rough, low American man's voice"},
 # ---- recurring residents (refs exist) ----
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50", "reuse_refs": True,
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
 "CHAR_CLARA": {"name": "Clara Mercer", "role": "the widow of film 1, now married to John Mercer", "reuse_refs": True,
   "look": "26-year-old American frontier woman, very pretty, slender, gray-green eyes, warm chestnut hair with copper highlights in a soft braided crown, faded dark-blue calico dress, small oval silver locket",
   "voice": "warm, low, steady American woman's voice, late twenties"},
 "CHAR_MERCER": {"name": "John Mercer", "role": "Union veteran, Clara's husband", "reuse_refs": True,
   "look": "40-year-old man, tall and lean, weathered tanned face, short dark-brown beard with gray at the chin, calm gray-blue eyes, long dark-brown canvas duster coat, black flat-brimmed hat, worn brown leather gun belt",
   "voice": "deep, quiet, unhurried American baritone"},
 "CHAR_ROSE": {"name": "Rose Ward", "role": "the bride of film 2", "reuse_refs": True,
   "look": "24-year-old woman, glossy dark-brown hair pinned up with soft curls, warm dark-brown eyes, faint freckles, a soft rose-colored Sunday dress",
   "voice": "soft, clear American woman's voice"},
 "CHAR_CALEB": {"name": "Caleb Ward", "role": "the deputy of film 2", "reuse_refs": True,
   "look": "28-year-old man, clean-shaven, strong jaw, hazel eyes, light-tan flat-crowned hat, brown leather vest, red bandana, tin deputy star",
   "voice": "earnest, warm young American man's voice"},
}
PROPS = {
 "PROP_BABY": {"name": "Baby Sam",
   "look": "an eight-month-old baby boy with a fuzz of reddish hair, wrapped in a faded yellow knitted blanket"},
 "PROP_CRADLE": {"name": "The cradle",
   "look": "a small hand-carved pine rocking cradle with a heart cut into the headboard, dusty, half covered by a burlap feed sack"},
}
LOCATIONS = {
 "LOC_HARLAN": {"name": "Harlan ranch",
   "look": "lonely log ranch house with a covered front porch and a single lamp-lit window, a big weathered plank barn with tall double doors and a hay loft, a split-rail fence and a plank gate on the valley road, green spring meadows, cottonwoods and distant snowy peaks"},
 "LOC_HARLAN_IN": {"name": "Harlan kitchen",
   "look": "plain log kitchen and front room: an iron cook stove, a rough plank table with two chairs, an oil lamp, a tall case clock in the hall, a rag rug, a window with a simple curtain, a narrow staircase"},
 "LOC_LOFT": {"name": "Barn loft",
   "look": "hay loft of a big plank barn: a wooden ladder, loose hay, dusty beams with light falling through cracks, an old trunk, a small hand-carved cradle under a burlap sack in the corner"},
 "LOC_STORE": {"name": "Hobbs mercantile",
   "look": "frontier general store interior: a long wooden counter with a brass scale and candy jars, shelves of tins, bolts of cloth, small leather boots on a shelf, sacks of flour, sunlight through the front window"},
 "LOC_SALOON": {"name": "Cedar Bluff saloon",
   "look": "small frontier saloon: a dark wooden bar with a brass rail, bottles on shelves, oil lamps, a few card tables, rain streaming down the window"},
 "LOC_VANCE": {"name": "Vance study, Leadville",
   "look": "rich Victorian study: dark paneled walls, a heavy desk with silver ingots used as paperweights, a cigar box, tall window showing mine headframes and smokestacks of Leadville"},
 "LOC_STREET": {"name": "Cedar Bluff main street", "reuse_refs": True,
   "look": "small frontier town main street, dirt road, wooden false-front buildings, boardwalks, hitching rails, horses and wagons, mountains beyond; signs have no legible text"},
 "LOC_JAIL": {"name": "Marshal's office", "reuse_refs": True,
   "look": "small log-and-plank marshal's office: a scarred desk with an oil lamp, a gun rack, a wanted-poster board with no legible text, a pot-bellied stove"},
}

SHOTS, HOOKS = [], []
_N = {"C": 0, "B": 0, "I": 0, "N": 0}


def _next(k):
    _N[k] += 1
    return f"{k}{_N[k]:02d}"


def _dur(lines):
    w = sum(len(l.split()) for _, l in lines)
    return 6 if not lines else 4 if w <= 5 else 6 if w <= 13 else 8


def clip(action, refs, line=None, camera="", night=False, action_shot=False, dur=None):
    lines = [line] if line else []
    SHOTS.append({"id": _next("C"), "type": "clip", "duration_s": dur or _dur(lines), "action": action, "camera": camera,
                  "dialogue": [{"speaker": a, "line": b} for a, b in lines], "refs": refs, "priority": "core",
                  "night": night, "action_shot": action_shot, "broll": False, "start_frame_prompt": action})


CUR_N = [None]


def broll(action, refs, camera="", night=False, dur=6):
    """silent clip under the narrator of the block that follows (field 'for')."""
    SHOTS.append({"id": _next("B"), "type": "clip", "duration_s": dur, "action": action, "camera": camera, "dialogue": [],
                  "refs": refs, "priority": "core", "night": night, "action_shot": False, "broll": True,
                  "start_frame_prompt": action, "for": None})


def img(prompt, refs, night=False, motion="slow push in"):
    SHOTS.append({"id": _next("I"), "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "night": night, "for": None})


def narr(text):
    nid = _next("N")
    # b-roll and stills written just before a narration block belong to it
    for s in reversed(SHOTS):
        if s["type"] == "narration":
            break
        if s.get("for", 1) is None:
            s["for"] = nid
    SHOTS.append({"id": nid, "type": "narration", "text": " ".join(text.split())})


def card(id_, text, seconds):
    SHOTS.append({"id": id_, "type": "title_card", "text": text, "duration_s": seconds})


def hook(id_, first_frame, video, refs, line=None, night=False):
    HOOKS.append({"id": id_, "duration_s": 6, "refs": refs, "first_frame": first_frame, "video": video, "night": night,
                  "dialogue": [{"speaker": line[0], "line": line[1]}] if line else []})


W, E, M, BABY = "CHAR_WADE", "CHAR_ELLIE", "CHAR_MOLLY", "PROP_BABY"

# ======================= COLD OPEN =======================
clip("Night, pouring rain, lightning: the tall double doors of a plank barn stand open; Wade Harlan holds up a lantern; on the threshold a soaked young mother clutches a baby wrapped in a yellow blanket, a little girl clinging to her skirt.",
     [E, W, M, BABY, "LOC_HARLAN"], (E, "May we sleep in your barn, mister? Just till the rain stops."), camera="over Wade's shoulder toward the woman", night=True)
clip("Night, rain pouring off the brim of his hat: Wade Harlan looks down at the soaked woman, his face hard in the lantern light.",
     [W, "LOC_HARLAN"], (W, "No, ma'am."), camera="close-up", night=True)
clip("Night, rain: the young mother lowers her eyes, pulls her shawl over the baby and silently turns back toward the dark road, the little girl looking back over her shoulder.",
     [E, M, BABY, "LOC_HARLAN"], camera="medium shot from the barn door", night=True, dur=4)
clip("Night, rain: Wade Harlan pulls off his own oilskin coat and steps out into the rain after them.",
     [W, "LOC_HARLAN"], (W, "You'll sleep in the house."), camera="medium shot", night=True)
clip("Night, rain: the little girl, soaked, tugs her mother's sleeve and whispers, staring up at the big man.",
     [M, E, "LOC_HARLAN"], (M, "Does he bite, Mama?"), camera="low close-up on the girl", night=True)
clip("Night, rain: Wade Harlan drapes his coat over the mother and the baby; the corner of his mouth almost moves.",
     [W, E, BABY, "LOC_HARLAN"], (W, "Only on Sundays."), camera="close two-shot", night=True)
clip("Night, a ridge above the valley, lightning: three riders in rain slickers sit their horses; Deacon Pike unfolds a wet sheet of paper.",
     [W.replace("WADE", "PIKE"), "CHAR_GUNMAN"], ("CHAR_PIKE", "Five hundred dollars for the boy."), camera="medium shot, low angle, lightning behind", night=True)
clip("Night, the ridge in the rain: the red-stubbled gunman in a yellow slicker leans toward Pike.",
     ["CHAR_GUNMAN"], ("CHAR_GUNMAN", "And the woman?"), camera="close-up", night=True)
clip("Night, the ridge: Deacon Pike slowly crumples the wet paper in his gloved fist, rain dripping from his hat.",
     ["CHAR_PIKE"], ("CHAR_PIKE", "The woman doesn't matter."), camera="close-up", night=True)
broll("Night storm: far below, a single window of a log ranch house lights up warm; three riders start down the slope toward it.",
      ["CHAR_PIKE", "LOC_HARLAN"], camera="wide shot from the ridge", night=True)
narr("""Wade Harlan had not opened his door to anyone in three years. That night he opened it to a stranger, a little girl,
and a baby — and to the three men already on her trail.""")
card("T01", "THE BARN IN THE STORM", 4.0)
img("Rainy dusk at a lonely crossroads: a freight wagon stops; a young mother with a baby climbs down from under a tarp, a little girl hands down a carpet bag; the wagon drives on.",
      [E, M, BABY])
img("Close-up: a little girl's oversized scuffed boots sinking into a muddy road in the rain.", [M])
img("A young mother walks a muddy road in the rain carrying a baby in a yellow blanket, a little girl dragging a carpet bag beside her, mountains in the mist.", [E, M, BABY], motion="slow drift")
img("Close-up on a wet wooden bench: a worn leather Bible and a small pocket pistol lying on it.", [])
narr("""Ellie Price had left Leadville four days earlier, in the back of a freight wagon, under a tarp that smelled of coal oil and wet canvas.
She had sixty-one cents, a Bible, a small pocket pistol that had belonged to her husband, and two children who had never once asked her where they were going.
On the fourth day the teamster turned south and put them down at the crossroads. After that, they walked.""")

# ======================= SCENE 1: night in the house =======================
img("Night, inside a log ranch house: an oil lamp on a plank table, rain streaming down the window, a tall case clock in the hall.", ["LOC_HARLAN_IN"], night=True)
img("Night: Wade Harlan kneels at an iron cook stove and lights the kindling, rain hammering the window behind him.", [W, "LOC_HARLAN_IN"], night=True)
narr("""The house had been quiet for three years. Quiet enough that Wade could hear the clock in the hall, and every board that creaked under a woman's weight,
and the small, wet breathing of a baby who had cried himself to sleep.""")
clip("Night, lamp-lit kitchen: Wade Harlan nods toward the narrow staircase, speaking to the soaked woman by the stove.",
     [W, "LOC_HARLAN_IN"], (W, "There's a bed upstairs. Clean sheets."), night=True)
clip("Night, lamp-lit kitchen: Ellie Price, holding the sleeping baby, shakes her head, proud and wary.",
     [E, BABY, "LOC_HARLAN_IN"], (E, "We'll be gone before light, mister."), night=True)
clip("Night, lamp-lit kitchen: Wade Harlan pours hot coffee into a tin cup and sets it in front of her.",
     [W, "LOC_HARLAN_IN"], (W, "Harlan. And you'll be gone when the rain's gone. Not before."), night=True)
clip("Night: the little girl warms her hands at the stove and looks around the bare room.",
     [M, "LOC_HARLAN_IN"], (M, "Is this your house all by yourself?"), night=True)
clip("Night: Wade Harlan stops, his back half turned, and answers quietly.",
     [W, "LOC_HARLAN_IN"], (W, "It is now."), camera="close-up", night=True)
img("Night: a young mother asleep sitting up in a chair by the door, a baby asleep on her chest, the grip of a small pistol showing under her shawl.", [E, BABY, "LOC_HARLAN_IN"], night=True)
narr("""She slept sitting up, between her children and the door. Wade knew that kind of sleep. He had slept like that himself, a long time ago,
in a country where the next knock on the door could be the last.""")

img("Sunny main street: two townswomen in bonnets whisper behind their hands as a tall rancher rides past alone.", [W, "LOC_STREET"])
img("A man's hat hanging on a peg by an empty doorway; dust in the morning light of a silent house.", ["LOC_HARLAN_IN"])
img("Dawn: a tall rancher stands alone on the hill behind his house, hat in hand, before two wooden crosses.", [W, "LOC_HARLAN"])
narr("""In Cedar Bluff they said Wade Harlan had buried his heart on the hill behind his house. He came to town once a month for flour and coffee and nails,
paid in cash, tipped his hat to the ladies and said nothing at all. The ladies said he was rude. The men said he was dangerous.
The children said he was a ghost. None of them had ever been inside his gate.""")

# ======================= SCENE 2: morning, the cradle =======================
broll("Bright spring morning after the storm, wet grass sparkling: Wade Harlan steps out of the barn and stops - smoke rises from his chimney and the little girl is feeding the chickens in the yard.", [W, M, "LOC_HARLAN"])
clip("Bright morning, kitchen full of sunlight: Wade Harlan stands in the doorway; Ellie turns from the stove with a pan of biscuits.",
     [W, E, "LOC_HARLAN_IN"], (W, "You didn't have to do that."))
clip("Bright morning, kitchen: Ellie sets the biscuits on the table and lifts her chin.",
     [E, "LOC_HARLAN_IN"], (E, "I don't take charity, Mr. Harlan. I pay with what I have."))
clip("Bright morning, kitchen: Wade Harlan sits down slowly at the table and looks at the hot breakfast.",
     [W, "LOC_HARLAN_IN"], (W, "Then you're a rich woman. Nobody's cooked in that kitchen in three years."))
clip("Sunlit barn loft: the little girl, chasing a kitten through the hay, pulls a burlap sack off a small carved cradle and calls down excitedly.",
     [M, "PROP_CRADLE", "LOC_LOFT"], (M, "Mister! There's a baby bed up here! Whose is it?"))
clip("Barn: Wade Harlan stands at the foot of the loft ladder, frozen, looking up.",
     [W, "LOC_LOFT"], (W, "Leave it be, Molly. Please."), camera="low angle close-up")
img("A warm faded memory: a smiling young woman with dark hair holding a newborn on the porch of the log ranch house, spring flowers.", ["LOC_HARLAN"])
img("A small hill above the ranch: two wooden grave crosses, one large and one very small, wildflowers in the grass.", ["LOC_HARLAN"])
img("A memory by lamplight: Wade Harlan carving a small pine cradle at the kitchen table, wood shavings around him.", [W, "PROP_CRADLE", "LOC_HARLAN_IN"], night=True)
broll("Night: Ellie climbs the loft ladder with a candle, kneels beside the dusty carved cradle and gently touches the heart cut into its headboard.", [E, "PROP_CRADLE", "LOC_LOFT"], night=True)
narr("""Her name had been Anna. The boy had been called Daniel, after Wade's father. The fever came in the spring of seventy-eight and took them both in a single week.
Wade carved the cradle himself, the winter before the boy was born. After the funeral he carried it up to the loft, covered it with a feed sack,
and never climbed that ladder again.""")

# ======================= SCENE 2b: the porch =======================
clip("Night, the porch after the rain, crickets, a lamp: Ellie hands Wade a cup of coffee and sits on the step.",
     [E, W, "LOC_HARLAN"], (E, "She must have been very loved. Your wife."), night=True)
clip("Night, porch: Wade Harlan looks out at the dark meadow, almost smiling.",
     [W, "LOC_HARLAN"], (W, "Anna. She'd have had you dry and fed before you got through the door."), night=True)
clip("Night, porch: Ellie shakes her head softly.", [E, "LOC_HARLAN"], (E, "You didn't make me ask."), night=True)
clip("Night, porch: Wade Harlan turns the cup in his hands.", [W, "LOC_HARLAN"], (W, "I made you stand in the rain long enough to ask."), night=True)
clip("Night, porch: Ellie looks at him for a long moment.", [E, "LOC_HARLAN"], (E, "My husband would have liked you, Mr. Harlan."), night=True)
clip("Night, porch: Wade Harlan, still looking at the meadow.", [W, "LOC_HARLAN"], (W, "Wade."), camera="close-up", night=True)
img("A young miner in a work shirt writing a poem on the back of an assay slip by lamplight, smiling.", [])
img("The same young man reading letters aloud to a little red-braided girl on his knee in a small Leadville cabin.", [M])
img("Leadville silver mine: a tall wooden headframe, dust suddenly bursts from the mine entrance, miners run toward it.", [])
narr("""Henry Vance had been nothing like his father. He had married a schoolteacher's daughter against the old man's orders,
and worked his own shifts in his father's mine to prove he could. He wrote poems on the backs of assay slips, and was teaching Molly her letters,
and was going to buy a little farm in the valley when the boy was old enough to ride. Then, one Tuesday morning, a beam gave way four hundred feet underground.""")

# ======================= SCENE 2c: days on the ranch =======================
img("Sunny morning: the little girl in braids runs down the staircase; on the table a baby in a basket laughs as a rooster crows in the open door.", [M, BABY, "LOC_HARLAN_IN"])
img("Mended men's shirts drying on a clothesline in the sun beside the log house.", ["LOC_HARLAN"])
img("A jar of fresh wildflowers on a plank kitchen table in morning sunlight.", ["LOC_HARLAN_IN"])
narr("""The rain came and went for days, one storm after another rolling over the ridge. And somewhere in those days the house began to sound different.
A spoon against a pot. A little girl's boots on the stairs. A baby who laughed when the rooster crowed.
Wade found his shirts mended without being asked, and the clock in the hall wound again, and a jar of wildflowers on a table where nothing had stood for three years.""")
clip("Sunny day by the split-rail fence: the little girl sits on the top rail swinging her boots while Wade hammers a new rail.",
     [M, W, "LOC_HARLAN"], (M, "How come you never smile, Mister Wade?"))
clip("Sunny day, fence: Wade Harlan keeps hammering without looking up.", [W, "LOC_HARLAN"], (W, "Forgot how, I guess."))
clip("Sunny day, fence: the girl pulls the corners of her mouth up with her fingers into a huge grin.",
     [M, "LOC_HARLAN"], (M, "That's all right. I'll show you. It's easy."))
clip("Sunny day, fence: Wade Harlan turns his face away from the girl - and he is smiling.", [W, "LOC_HARLAN"], camera="close-up", dur=4)
broll("Sunny barn: Wade Harlan shows the little girl how to milk a brown cow; she squeals as the milk hits the pail.", [W, M, "LOC_HARLAN"])
img("A red-tailed hawk circling in a bright blue sky over green meadows.", [])
img("Three small rag dolls lined up on a sunny windowsill of a log house.", ["LOC_HARLAN_IN"])
narr("""He taught her to milk the brown cow and to tell a hawk from a buzzard by the way it held its wings. She taught him the names of all four of her dolls,
three of which she had left behind in Leadville. He never asked why they had left in such a hurry. Some questions, Wade knew, you only ask when you are ready to hear the answer.""")

# ======================= SCENE 3: town =======================
broll("Bright noon: a ranch wagon rolls into the sunny main street of Cedar Bluff; Wade drives, Ellie beside him with the baby, the girl in the back; townspeople turn to stare.", [W, E, M, BABY, "LOC_STREET"])
narr("""On the fourth day Wade hitched the wagon and drove them into Cedar Bluff. The girl needed shoes. The baby needed milk.
And Wade needed to know who sends three men through a storm after a widow with a baby.""")
clip("Sunny general store: the little girl stares at a pair of small new boots on the shelf; Ellie, holding the baby, speaks to the storekeeper.",
     [E, M, BABY, "LOC_STORE"], (E, "The small boots, please. I can pay half now, and the rest..."))
clip("General store: the balding storekeeper in a white apron folds his arms behind the counter.",
     ["CHAR_HOBBS", "LOC_STORE"], ("CHAR_HOBBS", "No credit to strangers, ma'am. Cash or nothing."))
clip("General store: a gossip in a lilac bonnet lowers her lorgnette and looks Ellie up and down.",
     ["CHAR_WHITCOMB", "LOC_STORE"], ("CHAR_WHITCOMB", "A widow, sleeping under a widower's roof. In my day we had a word for women like that."))
clip("General store: Wade Harlan steps up and sets a twenty-dollar gold coin on the counter with a click.",
     [W, "LOC_STORE"], (W, "Boots for the girl. A sack of flour. And whatever else the lady needs."))
clip("General store: Wade Harlan turns to the gossip in the lilac bonnet, calm and quiet.",
     [W, "CHAR_WHITCOMB", "LOC_STORE"], (W, "In my day, Mrs. Whitcomb, we had a word for women who walk forty miles through a storm to keep their children."))
clip("General store: Wade Harlan, close.", [W, "LOC_STORE"], (W, "We called them mothers."), camera="close-up")
clip("General store: the little girl hugs the new boots to her chest and whispers to her mother.", [M, E, "LOC_STORE"], (M, "Mama... he does bite."))
clip("Sunny main street: Clara Mercer hurries up to Ellie on the boardwalk and presses a bundle of children's clothes into her hands.",
     ["CHAR_CLARA", E, "LOC_STREET"], ("CHAR_CLARA", "Lily's outgrown these. And don't mind Edna Whitcomb. She said worse about me."))
broll("Golden sunset: the wagon rolls home along the valley road; in the back the little girl sleeps hugging her new boots in their paper.", [W, E, M, "LOC_HARLAN"])
img("Sunset: Ellie on the wagon seat beside Wade, looking away at the fields, a small tired smile.", [E, W])
narr("""They drove home with the sun going down behind the ridge. Molly fell asleep in the back of the wagon with the new boots in her arms, still in their paper.
Ellie didn't say a word for three miles. Then, without looking at him, she said, 'Nobody has stood up for me in a very long time, Wade.'
He didn't answer. He didn't know how. But he drove a little slower the rest of the way.""")

# ======================= SCENE 3b: Leadville =======================
img("Leadville, 1881: a crowded mining town of smokestacks and wooden headframes under gray mountains.", [])
img("A rich Victorian study with silver ingots on the desk and a window over the mine smokestacks.", ["LOC_VANCE"])
narr("""Five days earlier and two hundred miles away, in a study that smelled of cigars and silver polish,
a man who had never in his life been told no was hearing it for the first time.""")
clip("Rich study in Leadville: the attorney in a bowler hat and spectacles stands nervously by the desk, holding his folder.",
     ["CHAR_GREER", "LOC_VANCE"], ("CHAR_GREER", "She took the boy in the night, sir. And the girl."))
clip("Rich study: Lucius Vance stands at the tall window with his back to the room, leaning on his silver-knobbed cane.",
     ["CHAR_VANCE", "LOC_VANCE"], ("CHAR_VANCE", "Then send Pike. Bring me the boy. What happens to the woman is no concern of mine."))

# ======================= SCENE 4: the telegram =======================
clip("Marshal's office in daylight: Marshal Abel Hart hands Wade a folded telegram across the desk.",
     ["CHAR_MARSHAL", W, "LOC_JAIL"], ("CHAR_MARSHAL", "Wade. This came from Leadville yesterday."))
clip("Marshal's office: Wade Harlan reads the telegram, his jaw tightening.", [W, "LOC_JAIL"], (W, "They say she stole her own son?"))
clip("Marshal's office: the marshal taps the desk.", ["CHAR_MARSHAL", "LOC_JAIL"],
     ("CHAR_MARSHAL", "Papers say the court gave the boy to the old man. Papers say she's unfit."))
clip("Marshal's office: the marshal looks Wade in the eye.", ["CHAR_MARSHAL", "LOC_JAIL"],
     ("CHAR_MARSHAL", "I've never seen papers that could tell me who a mother is, Wade."))
img("Portrait of a hard old silver king in a black frock coat in his study, a cold stare.", ["CHAR_VANCE", "LOC_VANCE"])
img("Rainy funeral at a Leadville cemetery: a young widow in black holding a baby, a little girl beside her, men with umbrellas.", [E, M, BABY])
narr("""Lucius Vance owned half the silver in Leadville and every judge who mattered. His only son, Henry, had died under a fallen beam in a shaft his father refused to brace.
Henry left behind a wife the old man never wanted, a daughter he never visited, and a son. A boy was something Lucius Vance could use.""")

# ======================= SCENE 4b: the saloon =======================
clip("Night, rainy saloon: Deacon Pike stands at the bar, water dripping off his black duster, speaking to the bartender.",
     ["CHAR_PIKE", "LOC_SALOON"], ("CHAR_PIKE", "Woman with a baby. Red hair. Little girl. Came through in the rain."), night=True)
clip("Night, saloon: the bartender keeps polishing a glass, not looking up.", ["CHAR_BARMAN", "LOC_SALOON"],
     ("CHAR_BARMAN", "Lot of folks come through in the rain, mister."), night=True)
clip("Night, saloon: Deacon Pike lays a gold coin on the bar and slides it forward with one finger.", ["CHAR_PIKE", "LOC_SALOON"],
     ("CHAR_PIKE", "Five hundred dollars says somebody remembers."), night=True)
clip("Night, saloon: at a corner table by the rainy window, the gossip in the lilac bonnet sets down her teacup and stands up.",
     ["CHAR_WHITCOMB", "LOC_SALOON"], ("CHAR_WHITCOMB", "Try the Harlan place. The one with the lamp in the window."), night=True)
img("Night, rain: three riders in slickers ride out of town onto the dark valley road.", ["CHAR_PIKE", "CHAR_GUNMAN", "LOC_STREET"], night=True)
narr("""Edna Whitcomb would tell herself afterwards that she had only been doing her Christian duty. Nobody in Cedar Bluff ever quite believed her.""")

# ======================= SCENE 5: the truth =======================
clip("Sunset on the porch, distant lightning over the ridge: Wade Harlan holds the telegram out to Ellie.", [W, E, "LOC_HARLAN"], (W, "Henry Vance. Your husband."))
clip("Sunset, porch: Ellie holds the baby tighter.", [E, BABY, "LOC_HARLAN"], (E, "His father wants Sam. Not me. Not Molly."))
clip("Sunset, porch: Ellie, her voice breaking.", [E, "LOC_HARLAN"], (E, "He had a doctor sign a paper that says I'm not right in the head."))
clip("Sunset, porch: Ellie looks at him, eyes wet.", [E, "LOC_HARLAN"], (E, "There's a place in Denver for women like that. They don't come out."))
clip("Sunset, porch: Wade Harlan, quietly.", [W, "LOC_HARLAN"], (W, "So you walked."))
clip("Sunset, porch: Ellie nods.", [E, "LOC_HARLAN"], (E, "Forty miles. Molly carried the bag the last ten."))
broll("Night storm: Ellie with the baby and the little girl creeps across the muddy yard toward the gate - and stops: Wade stands at the gate with a lantern.", [E, M, BABY, W, "LOC_HARLAN"], night=True)
clip("Night storm, at the gate: Wade Harlan holds up the lantern.", [W, "LOC_HARLAN"], (W, "You're not walking out into the rain again, Ellie."), night=True)
clip("Night storm, at the gate: Ellie, rain on her face.", [E, BABY, "LOC_HARLAN"], (E, "They'll burn your house down to get him."), night=True)
clip("Night storm, at the gate: Wade Harlan takes the carpet bag from her hand.", [W, "LOC_HARLAN"], (W, "Then they'll have to come through the gate first."), night=True)
img("Night rain: Wade walking Ellie and the children back to the lit house under his lantern.", [W, E, M, "LOC_HARLAN"], night=True)
narr("""He didn't tell her what he had been before he was a rancher. He didn't tell her about the badge in the bottom of his trunk,
or the name men in Texas still said quietly. He only took the lantern from her hand and walked her back to the house.""")
img("Lamplight: an old trunk opened; under folded clothes lies a silver star in a ring and a revolver wrapped in an oiled cloth.", ["LOC_HARLAN_IN"], night=True)
img("Texas, 1870s: a column of Rangers riding across a dusty plain, a young Wade Harlan at their head.", [W])
img("Night, lamplight: Wade Harlan slowly loads the revolver from the trunk, one cartridge at a time, the silver star lying beside it.", [W, "LOC_HARLAN_IN"], night=True)
narr("""Before Colorado there had been Texas. Eleven years with Company D of the Frontier Battalion, from the Rio Grande to the Staked Plains.
He had ridden after cattle thieves and murderers and men who burned homesteads for sport, and he had brought most of them back.
When Anna married him, she asked for one thing: that he put the badge away for good. He had kept that promise for nine years.
He looked at it a long time that night. Then he loaded the Colt, and put the badge back in the trunk.""")
clip("Night, a small bedroom: the little girl kneels at the bed in her nightdress, hands folded; Wade stands unseen in the dark doorway.",
     [M, "LOC_HARLAN_IN"], (M, "And God bless Mama, and Sam, and Mister Wade, even though he doesn't smile much."), night=True)
clip("Night, bedroom: the girl opens one eye, thinking.", [M, "LOC_HARLAN_IN"], (M, "And please make the rain stop. But not too fast."), night=True)
broll("Stormy afternoon: black clouds roll over the ridge; down the valley road come a closed black buggy and three riders in long slickers.", ["CHAR_PIKE", "LOC_HARLAN"])
img("A gaunt gunman in a black hat reading a small Bible by a campfire, cold eyes.", ["CHAR_PIKE"], night=True)
narr("""The rain did not stop. It came back harder the next afternoon, black clouds rolling over the ridge from the west.
And with it, down the valley road, came a closed buggy and three riders in long slickers.
Wade knew the man in the black hat by reputation. In Texas they called him Deacon, because he liked to quote scripture.
Wade had put his younger brother in Huntsville prison in the summer of seventy-two. A man like Deacon Pike did not forget a thing like that. Neither did Wade.""")

img("Night: a young mother sits awake by a window with a sleeping baby, watching the dark road.", [E, BABY, "LOC_HARLAN_IN"], night=True)
img("Night: a little girl asleep clutching her new boots, a lamp turned low beside her.", [M, "LOC_HARLAN_IN"], night=True)
img("Night: a tall rancher sits on the porch in the rain with a rifle across his knees, watching the gate.", [W, "LOC_HARLAN"], night=True)
narr("""Nobody in the Harlan house slept much that night. Ellie sat by the window with the baby, watching the road. Molly slept in her new boots, because she said they might need to run.
And Wade sat on the porch with a rifle across his knees, the way he had sat outside a hundred camps on the Staked Plains, listening to the rain and waiting for morning.""")

# ======================= SCENE 6: at the gate =======================
clip("Rain, at the ranch gate: the attorney in a bowler hat leans out of the black buggy holding a document.",
     ["CHAR_GREER", "LOC_HARLAN"], ("CHAR_GREER", "Thaddeus Greer, attorney for Mr. Lucius Vance. I have a court order for the child."))
clip("Rain, the gate: on his horse, Deacon Pike slowly raises his head at the name.", ["CHAR_PIKE", "LOC_HARLAN"],
     ("CHAR_PIKE", "Harlan. Captain Wade Harlan. Company D. Texas Rangers."))
clip("Rain, the gate: Wade Harlan stands at the closed gate, coat open, hand near his holster.", [W, "LOC_HARLAN"],
     (W, "That was a long time ago."))
clip("Rain, the gate: Deacon Pike, cold and quiet.", ["CHAR_PIKE", "LOC_HARLAN"], ("CHAR_PIKE", "You sent my brother to Huntsville. He died there."))
clip("Rain, the gate: Wade Harlan, unmoving.", [W, "LOC_HARLAN"], (W, "Then you know how this ends, Deacon."))
clip("Inside the dark house, rain on the windows: Ellie kneels and puts the baby into her daughter's arms.", [E, M, BABY, "LOC_HARLAN_IN"],
     (E, "Take Sam up to the loft. Don't come down. Whatever you hear."), night=True)
clip("The barn loft in storm light: the little girl climbs off the ladder with the baby and lays him gently in the carved cradle, rocking it.",
     [M, BABY, "PROP_CRADLE", "LOC_LOFT"], dur=6)
clip("Rain at the gate: a gunshot snaps Wade Harlan's hat off his head; he draws and fires back in one motion.", [W, "LOC_HARLAN"],
     camera="medium shot", action_shot=True)
clip("Rain: the gunman in the yellow slicker tumbles off his horse into the mud, his rifle flying.", ["CHAR_GUNMAN", "LOC_HARLAN"],
     action_shot=True, dur=4)
clip("Rain: the second gunman runs for the barn door - and Ellie steps out of it with a pitchfork leveled, blocking his way.",
     [E, "CHAR_GUNMAN", "LOC_HARLAN"], action_shot=True)
clip("Rain at the gate: Wade Harlan and Deacon Pike face each other a few steps apart, revolvers raised, rain running off their hats.",
     [W, "CHAR_PIKE", "LOC_HARLAN"], camera="wide two-shot", action_shot=True)
clip("Rain: two riders burst out of the gray downpour at a gallop - John Mercer and Marshal Hart, rifles up.",
     ["CHAR_MERCER", "CHAR_MARSHAL", "LOC_HARLAN"], action_shot=True)
clip("Rain: John Mercer reins in hard beside the gate, rifle at his shoulder.", ["CHAR_MERCER", "LOC_HARLAN"],
     ("CHAR_MERCER", "Drop it, Pike!"), action_shot=True)
clip("Rain: Deacon Pike hesitates - then lets his revolver fall into the mud.", ["CHAR_PIKE", "LOC_HARLAN"], dur=4)

# ======================= SCENE 7: the papers =======================
clip("Lamp-lit kitchen, rain outside: the marshal lowers the court order and looks at the wet, hatless attorney by the stove.",
     ["CHAR_MARSHAL", "CHAR_GREER", "LOC_HARLAN_IN"], ("CHAR_MARSHAL", "Signed April ninth. Judge Kittredge was buried April second. I was at the funeral."), night=True)
clip("Kitchen: Ellie takes a folded letter out of her worn Bible and holds it out.", [E, "LOC_HARLAN_IN"],
     (E, "Henry wrote this the night before he went down that shaft. He knew."), night=True)
clip("Kitchen: the marshal reads the letter aloud.", ["CHAR_MARSHAL", "LOC_HARLAN_IN"],
     ("CHAR_MARSHAL", "My children are to remain with their mother. My father is not to raise them as he raised me."), night=True)
img("A Denver courtroom: the attorney in spectacles stands pale while a judge points at him.", ["CHAR_GREER"])
img("A stone prison yard at Cañon City: a gaunt man in prison stripes looks at the wall.", ["CHAR_PIKE"])
img("An old silver king alone in his dark study, holding a letter, his face gray.", ["CHAR_VANCE", "LOC_VANCE"], night=True)
narr("""Within the month, Thaddeus Greer was disbarred in three states. Deacon Pike went to Cañon City for twelve years.
And Lucius Vance, who had bought every judge in Lake County, found that a dead son's letter was the one thing his money could not buy back.""")
img("The storekeeper in his apron loads a sack of sugar onto a ranch wagon, smiling.", ["CHAR_HOBBS", "LOC_STREET"])
narr("""In Cedar Bluff, the story went around the way stories do. By Sunday, half the town had heard that Wade Harlan stood at his gate in the rain against three hired guns.
The other half had heard about the boots. Mr. Hobbs sent a sack of sugar out to the ranch with his compliments, and did not send a bill.""")

img("Night after the storm: lamplight in the kitchen, a young mother asleep at the table with her head on her arms, a man's coat around her shoulders.", [E, "LOC_HARLAN_IN"], night=True)
img("Dawn: the rain clouds breaking over the valley, sunlight hitting the wet meadows and the barn roof.", ["LOC_HARLAN"])
narr("""The storm blew itself out a little after midnight. When the last rider was gone and the house was quiet again, Ellie fell asleep at the kitchen table,
still holding Henry's letter. Wade put his coat around her shoulders and sat across from her until the window turned gray.
For the first time in three years, he did not want the night to end too fast.""")

# ======================= SCENE 8: after the storm =======================
clip("Dazzling morning sun through the barn: Wade Harlan climbs the loft ladder and pulls the burlap sack off the carved cradle.",
     [W, "PROP_CRADLE", "LOC_LOFT"], dur=6)
clip("Sunny bedroom: Wade carries the cradle in and sets it down beside the bed where the baby sleeps.",
     [W, BABY, "PROP_CRADLE", "LOC_HARLAN_IN"], dur=6)
clip("Sunny bedroom doorway: Ellie, touched, one hand on the frame.", [E, "LOC_HARLAN_IN"], (E, "Wade... you don't have to."))
clip("Sunny bedroom: Wade Harlan sets the baby into the cradle and rocks it once.", [W, BABY, "PROP_CRADLE", "LOC_HARLAN_IN"],
     (W, "It's waited long enough."))
clip("Bright morning on the porch steps: the little girl in her new boots looks up at Wade.", [M, "LOC_HARLAN"],
     (M, "Mister Wade? Can we stay till the rain stops?"))
clip("Bright morning: Wade Harlan looks up at the clear blue sky.", [W, "LOC_HARLAN"], (W, "Rain's stopped, Molly."))
clip("Bright morning: Wade Harlan crouches down to her height.", [W, "LOC_HARLAN"], (W, "Stay anyway."), camera="close-up")
clip("Bright morning: the girl throws her arms around Wade's neck; on the porch Ellie turns away, wiping her eyes, smiling.",
     [M, W, E, "LOC_HARLAN"], dur=6)

# ======================= FINALE =======================
broll("Sunny June wedding outside a little white church: Wade in a dark suit and Ellie in a simple cream dress; the little girl in new boots throws wildflowers at everyone.",
      [W, E, M, "LOC_STREET"])
img("Among the smiling wedding guests: a young couple (a deputy with a tin star and his dark-haired wife) and a bearded veteran with his chestnut-haired wife.",
    ["CHAR_CALEB", "CHAR_ROSE", "CHAR_MERCER", "CHAR_CLARA", "LOC_STREET"])
img("Night, distant storm: a warm lamp burns in the window of the Harlan ranch house, rain on the glass.", ["LOC_HARLAN"], night=True)
narr("""They were married in June, in the little white church on Main Street, with Molly in her new boots throwing wildflowers at everyone, including the preacher.
Mrs. Whitcomb was not invited. Nobody missed her. And on stormy nights, from then on, the lamp in the Harlan window stayed lit till morning - in case anyone else came knocking.""")
img("Years later: a tall young lawman with reddish hair and a silver star in a ring stands on the porch of the old ranch house.", ["LOC_HARLAN"])
img("Night rain: a lone traveler knocks at the barn door of a ranch; a lantern rises to meet him.", ["LOC_HARLAN"], night=True)
narr("""Sam Harlan - he took Wade's name the year he turned six - grew up to wear a silver star of his own. People who knew him said he never once turned away a stranger at the door.
When they asked him why, he said his father had taught him. And that his father had learned it one stormy night in the spring of 1881,
from a woman, a little girl, and a baby, who only asked to sleep in the barn.""")

# ======================= SHORTS (native 9:16) =======================
hook("H01", "Vertical 9:16. Night storm at a barn door: a soaked young mother holding a baby in a yellow blanket looks up into lantern light, a little girl clinging to her skirt.",
     "She asks to sleep in the barn, rain pouring, lightning behind.", [E, M, BABY, "LOC_HARLAN"], (E, "May we sleep in your barn, mister?"), night=True)
hook("H02", "Vertical 9:16. Sunny general store: a tall bearded rancher stands at the counter, a gold coin under his finger, looking at someone off-screen.",
     "He says it quietly, the whole store silent.", [W, "LOC_STORE"], (W, "We called them mothers."))
hook("H03", "Vertical 9:16. Rain at a ranch gate: a gaunt gunman in a black hat on horseback raises his head, rain dripping from the brim.",
     "He recognises the man at the gate.", ["CHAR_PIKE", "LOC_HARLAN"], ("CHAR_PIKE", "Captain Harlan. Company D. Texas Rangers."))
hook("H04", "Vertical 9:16. Bright morning on a porch: a little girl with braids and new boots looks up hopefully.",
     "She asks her question, hopeful.", [M, "LOC_HARLAN"], (M, "Can we stay till the rain stops?"))


# ======================= BUILD =======================
def ref_text(refs):
    parts = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src:
            parts.append(f"{src['name']}: {src['look']}")
    return " | ".join(parts)


MINOR = {"CHAR_HOBBS", "CHAR_BARMAN", "CHAR_GUNMAN", "CHAR_GREER"}


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
        s["file"] = f"visuals/images/{s['id']}.png"
    elif s["type"] == "clip":
        s["start_frame_full_prompt"] = (s["start_frame_prompt"] + " First frame of the shot, characters in position" + (", mouths closed" if s["dialogue"] else "")
                                        + (", the action already in motion" if s["action_shot"] else "") + ". " + STYLE + (NIGHT if s["night"] else "")
                                        + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else ""))
        s["ref_files"] = ref_files(s["refs"])
        present = [r for r in s["refs"] if r in CHARACTERS]
        if s["dialogue"]:
            d = s["dialogue"][0]
            c = CHARACTERS[d["speaker"]]
            dl = (f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}"'
                  + (f" ONLY {c['name']} speaks. Everyone else keeps their mouth closed and only listens." if len(present) > 1 else "")
                  + " The line starts within the first second; after the line the speaker holds a natural expression, no extra words.")
        else:
            dl = " No dialogue, natural sound only (rain, thunder, hooves, wind, birds), nobody speaks."
        s["video_prompt"] = (s["action"] + (ACTION if s["action_shot"] else "") + (" Camera: " + s["camera"] + "." if s["camera"] else "")
                             + dl + " " + CLIP_STYLE)
        s["files"] = {"start_frame": f"visuals/images/{s['id']}_first.png", "video": f"visuals/video/{s['id']}.mp4"}
VSTYLE = STYLE.replace("16:9 widescreen", "9:16 vertical portrait frame") + " Bright, faces large and clearly lit."
for h in HOOKS:
    h["first_frame_full_prompt"] = h["first_frame"] + " " + VSTYLE + (NIGHT if h["night"] else "") + " Characters/places: " + ref_text(h["refs"])
    d = h["dialogue"][0]
    c = CHARACTERS[d["speaker"]]
    h["video_prompt"] = (h["video"] + f' Dialogue: {c["name"]} ({c["voice"]}) says: "{d["line"]}" The line starts within the first second; no extra words. '
                         + CLIP_STYLE.replace("16:9", "9:16 vertical portrait frame, subjects large and centered"))
    h["ref_files"] = ref_files(h["refs"])
    h["files"] = {"start_frame": f"visuals/hooks/{h['id']}_first.png", "video": f"visuals/hooks/{h['id']}.mp4"}

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

clips = [s for s in SHOTS if s["type"] == "clip"]
narrs = [s for s in SHOTS if s["type"] == "narration"]
words = sum(len(re.findall(r"[A-Za-z']+", n["text"])) for n in narrs)
vsec = sum(c["duration_s"] for c in clips) + sum(h["duration_s"] for h in HOOKS)
n_img = sum(s["type"] == "image" for s in SHOTS) + len(clips) + len(HOOKS)
est = {"clips": len(clips), "clips_dialogue": sum(bool(c["dialogue"]) for c in clips), "broll": sum(c["broll"] for c in clips),
       "hooks": len(HOOKS), "video_seconds": vsec, "images_incl_first_frames": n_img, "ref_images": len(REF_PROMPTS),
       "narration_words": words, "narration_min_at_130wpm": round(words / 130, 1),
       "usd_video": round(vsec * 0.10, 1), "usd_images": round(n_img * 0.067, 1), "usd_refs_approx": round(len(REF_PROMPTS) * 0.17, 1)}
est["usd_total_approx"] = round(est["usd_video"] + est["usd_images"] + est["usd_refs_approx"] + 1.5, 1)

out = {"title": "The Barn in the Storm", "series": "Tales of Cedar Bluff", "episode": 3,
       "working_title_youtube": "A Widowed Rancher Let a Mother and Her Baby Sleep in His Barn — Three Days Later, Three Men Came for the Child",
       "setting": "valley ranch near Cedar Bluff, Colorado (a state since 1876), spring 1881",
       "format": {"aspect": "16:9 (hooks 9:16)", "fps": 24, "clip_durations_allowed_s": [4, 6, 8]},
       "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE, "reused_refs_from": PREV,
       "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "ref_prompts": REF_PROMPTS,
       "timeline": SHOTS, "hooks": HOOKS,
       "production": {
           "schema_version": 1,
           "review_gates": {"references": {"enabled": True}, "audio": {"enabled": False},
                            "visuals": {"enabled": True}, "video_sample": {"enabled": False}, "videos": {"enabled": False}},
           "edit": {"dialogue_tail_seconds": 0.8, "narration_voice_offset_seconds": 0.4, "transition_seconds": 0.3,
                    "end_screen_tail_seconds": 0, "contact_sheet": "one_frame_per_timeline_visual"},
           "audio_mix": {"speech_active_rms_db": -20, "ambient_clip_rms_db": -24, "music_base_rms_db": -18,
                         "duck_under_speech_db": -15, "duck_under_clip_db": -6, "duck_attack_seconds": 0.15,
                         "duck_release_seconds": 0.6, "integrated_lufs": -14, "true_peak_db": -1.5},
           "voice": {"provider": "elevenlabs", "voice_id": "pqHfZKP75CvOlQylNhV4", "model": "eleven_multilingual_v2",
                     "speed": 1, "timestamps": True, "output_format": "mp3_44100_128", "stability": 0.55,
                     "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True, "context_chars": 400},
           "subtitle": {"language": "en", "name": "English"},
           "export": {"package_branch": "pkg/western_barn_storm_v1", "film_branch": "film/western_barn_storm_v1"},
           "qc": {"long_duration_min_seconds": 1, "long_duration_max_seconds": 3600, "black_silence_max_seconds": 60},
       }}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(f"{here}/shotlist.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"film": "The Barn in the Storm", "note": "score is reused from films 1-2 in the edit", "cues": []},
          open(f"{here}/music_cues.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(est, indent=1))
