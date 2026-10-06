# -*- coding: utf-8 -*-
"""Source of truth for "The Stagecoach Bride" (Tales of Cedar Bluff, film 2).
Generates shotlist.json, screenplay.md and narration/*.txt.
v4 (6 Oct evening): ~18-19 min. Cold open = the title scene (the groom walks his bride down Main Street in handcuffs, in her
wedding dress, the town laughing) -> "THREE DAYS EARLIER" -> the stagecoach robbery in one continuous action sequence ->
then a payoff or an action scene every 2-3 minutes (people who humiliate Rose get put in their place) -> justice and romance.
Shot IDs are STABLE: shots kept from v3 keep their v3 IDs (frames already made stay valid); new shots are C102+;
timeline order is the list order, not the ID order. Narration is renumbered N01.. in order (no audio made yet).
v3 history: commit 316323b.
Setting: Cedar Bluff, Colorado, September 1880 (a state since 1876 - never write "Territory").
"""
import json, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado, early autumn 1880, "
         "natural light, 35mm film grain, muted warm earth tones with golden aspen accents, shallow depth of field, "
         "period-accurate clothing and props. No text, no captions, no logos, no watermark, no modern objects.")
NIGHT = " Night scene: moonlight and warm firelight or lamplight, deep shadows, faces still clearly readable."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, Colorado 1880, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
              "Serious, grounded drama: natural, restrained acting and natural voices, no comedic or exaggerated performances. "
              "Characters only speak the exact lines given, in English, with lips in sync. No subtitles, no text on screen, no music.")
ACTION = (" Fast, dynamic action from the very first frame: the movement is already happening when the shot starts, "
          "no slow build-up. Realistic weight and physics, real dust, real smoke.")

PREV = "pkg/western_widows_piano_v1/visuals/refs"   # approved refs from film 1: reuse, do not regenerate

CHARACTERS = {
 # ---- recurring residents (refs exist from film 1) ----
 "CHAR_CLARA": {"name": "Clara Whitmore", "role": "widow, rancher, 28; heart of the town", "reuse_refs": True,
   "look": "26-year-old American frontier woman, very pretty and feminine, an original fictional character (not a celebrity lookalike), slender, delicate heart-shaped face, bright clear gray-green eyes with long lashes, softly arched brows, small straight nose, full soft lips, glowing smooth fair skin with a natural rosy blush, a tiny beauty mark below her left eye, warm chestnut hair with copper highlights in a soft braided crown with loose wavy strands framing her face, faded dark-blue calico dress with a patched left elbow, small oval silver locket on a chain",
   "voice": "warm, low, steady American woman's voice, late twenties, never shrill"},
 "CHAR_LILY": {"name": "Lily Whitmore", "role": "Clara's daughter, 9", "reuse_refs": True,
   "look": "8-year-old girl, freckles, two light-brown braids tied with faded blue ribbons, pale yellow cotton pinafore dress over a white blouse, scuffed brown lace-up boots, carries a small rag doll",
   "voice": "bright, soft American little girl's voice, eight years old"},
 "CHAR_MERCER": {"name": "John Mercer", "role": "Union veteran, 41; still sleeps in Clara's barn", "reuse_refs": True,
   "look": "40-year-old man, tall and lean, weathered tanned face, short dark-brown beard with gray at the chin, gray at the temples, calm gray-blue eyes, long dark-brown canvas duster coat, black flat-brimmed hat, faded blue Union cavalry trousers, worn brown leather gun belt, walks with a slight limp on the left leg",
   "voice": "deep, quiet, unhurried American baritone, few words, never raises his voice"},
 "CHAR_AGATHA": {"name": "Agatha Pell", "role": "the town gossip, 50", "reuse_refs": True,
   "look": "50-year-old woman, tight gray bun, pinched face, high-collared plum-purple silk dress, ivory cameo brooch, white lace parasol",
   "voice": "cold, haughty, clipped upper-class American woman's voice in her fifties, quietly cutting, never shrill, never comic"},
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50, Caleb's boss", "reuse_refs": True,
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
 # ---- new faces (refs to make in Phase 1) ----
 "CHAR_ROSE": {"name": "Rose Calloway", "role": "the mail-order bride from St. Louis, 24",
   "look": "24-year-old American woman of remarkable, gentle natural beauty, an original fictional character who does not resemble any actress or celebrity, slender and graceful, a soft oval face with high cheekbones and a delicate rounded chin, large luminous warm dark-brown eyes with long dark lashes, straight dark brows, a light dusting of faint freckles across a small straight nose, soft full rosy lips with a shy natural smile, clear luminous fair skin, a tiny pale scar on her left eyebrow, glossy dark-brown almost black hair pinned up with soft loose curls framing her face. "
           "OUTFIT A (wedding, scenes up to her rescue): ivory lace 1880 wedding dress with a high collar, long fitted sleeves and a row of small pearl buttons, short lace veil pinned back from her face. "
           "OUTFIT B (after the rescue): a borrowed faded green gingham dress with a white collar, her hair in a simple low bun",
   "voice": "soft, clear, educated American woman's voice, mid-twenties, Midwestern, brave under pressure"},
 "CHAR_CALEB": {"name": "Caleb Ward", "role": "young deputy marshal, 28, the groom who wrote the letters",
   "look": "28-year-old American man, an original fictional character (not a celebrity lookalike), tall, lean and broad-shouldered, clean-shaven with a strong jaw, honest hazel eyes, light-brown wavy hair, light-tan flat-crowned hat, brown leather vest over a white collarless shirt, red bandana at the neck, small tin deputy star on the vest, single revolver in a plain holster",
   "voice": "earnest, warm young American man's voice with a slight Western drawl, a little shy"},
 "CHAR_CRANE": {"name": "Silas Crane", "role": "cattle buyer and new bank partner, secret gang boss, 52",
   "look": "52-year-old tall, elegant man, an original fictional character, silver hair combed straight back, short clipped silver beard, pale cold blue eyes, immaculate charcoal-gray three-piece suit, black string tie, silver watch chain, cream-colored wide-brimmed hat, silver-headed black cane",
   "voice": "soft, measured, cultured Southern gentleman's voice, never raises it, quietly menacing"},
 "CHAR_BUCK": {"name": "Buck Tolliver", "role": "Crane's foreman and gang leader, 35",
   "look": "35-year-old rough man, an original fictional character, a pale scar across the left cheek, unshaven black stubble, narrow dark eyes, black bandana around the neck (pulled over the face when masked), shaggy sheepskin-lined brown coat, battered gray hat, two revolvers",
   "voice": "rough, sneering, low American man's voice"},
 "CHAR_AMOS": {"name": "Amos Pruitt", "role": "old express-company guard on the stagecoach, 66",
   "look": "66-year-old man, short white beard, kind tired eyes behind small round spectacles, brown wool coat, battered brown hat, double-barreled coach gun",
   "voice": "raspy, kindly old American man's voice"},
}
PROPS = {
 "PROP_STAGE": {"name": "The stagecoach",
   "look": "dark-green Concord stagecoach with yellow spoked wheels, leather thoroughbraces, luggage rack on top, open window frames with roll-up leather curtains, pulled by a team of six brown horses; no lettering or company name anywhere"},
 "PROP_BOX": {"name": "The strongbox",
   "look": "small dark-green wooden strongbox with black iron bands and corners, a heavy brass padlock, size of a bread loaf, worn and scratched"},
 "PROP_HORSE": {"name": "Mercer's horse", "reuse_refs": True,
   "look": "tall dark bay horse with a white blaze on the face and black mane, worn brown western saddle with a rolled gray blanket"},
}
LOCATIONS = {
 "LOC_STREET": {"name": "Cedar Bluff main street", "reuse_refs": True,
   "look": "small frontier town main street, dirt road, wooden false-front buildings (mercantile, bank with brick front, saloon, livery), boardwalks, hitching rails, horses and wagons, mountains and golden aspens beyond; signs have no legible text"},
 "LOC_RANCH": {"name": "Whitmore ranch exterior", "reuse_refs": True,
   "look": "small weathered log-and-plank ranch house with a covered front porch, split-rail fence, small barn with a corral, dirt road leading up, foothills and golden aspen trees, a hill with a single wooden grave cross behind the house"},
 "LOC_KITCHEN": {"name": "Whitmore kitchen", "reuse_refs": True,
   "look": "simple kitchen in a log house, wood stove, rough wooden table with three chairs, tin plates, oil lamp, coffee pot"},
 "LOC_BARN": {"name": "Barn", "reuse_refs": True,
   "look": "small wooden barn interior, hay bales, a stall with the dark bay horse, hanging lantern, tools on the wall, a bedroll on the hay"},
 "LOC_PARLOR": {"name": "Whitmore parlor", "reuse_refs": True,
   "look": "plain warm parlor inside a log house, rough log walls, wide plank floor, oil lamp, lace curtain on a small window, rag rug, an upright walnut piano against the wall"},
 "LOC_PASS": {"name": "Raven Pass stage road",
   "look": "narrow dirt stage road climbing through a mountain pass, steep rocky slope on one side and a sagebrush hillside on the other, scattered pines and golden aspens, high granite peaks beyond, big sky"},
 "LOC_JAIL": {"name": "Marshal's office and jail",
   "look": "small log-and-plank marshal's office: a scarred desk with an oil lamp, a gun rack, a wanted-poster board with no legible text, a pot-bellied stove, and one iron-barred cell at the back with a narrow cot and a small barred window"},
 "LOC_CANYON": {"name": "Red Canyon",
   "look": "narrow winding canyon of red sandstone walls, a dry creek bed of pale stones, scattered junipers, boulders big enough to hide behind, a strip of blue sky above"},
 "LOC_CRANE": {"name": "Crane's ranch",
   "look": "large prosperous ranch: a two-story white clapboard house with a wide veranda, big red barn, long corrals full of cattle, a fancy black buggy by the porch, a line of horses at the hitching rail"},
 "LOC_STATION": {"name": "Way station at Raven Pass",
   "look": "lonely stage way station of rough logs with a corral and a water trough, a lantern on a post, the stage road running past, mountains behind"},
}

SHOTS = []
PRICE = {4: 7, 6: 10, 8: 12}
_N = {"C": 101, "I": 11, "N": 0}   # v4: new shots continue after the v3 numbering


def _next(kind, fixed=None):
    if fixed:
        return fixed
    _N[kind] += 1
    return f"{kind}{_N[kind]:02d}"


def img(prompt, refs, motion="slow push in", night=False, reuse=None, rose=None, id=None):
    s = {"id": _next("I", id), "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "night": night}
    if reuse:
        s["reuse_from"] = reuse
    if rose:
        s["rose_override"] = rose
    SHOTS.append(s)
    return s


def _dur(lines):
    w = sum(len(l.split()) for _, l in lines)
    if not lines:
        return 6
    return 4 if w <= 5 else 6 if w <= 9 else 8


def clip(action, refs, lines=(), camera="", priority="core", night=False, action_shot=False, dur=None, end=None, broll=False, rose=None, id=None):
    """broll=True: silent clip played under the narrator (does not add running time)."""
    lines = list(lines)
    assert len({sp for sp, _ in lines}) <= 1, "one speaker per clip"
    s = {"id": _next("C", id), "type": "clip", "duration_s": dur or _dur(lines), "action": action, "camera": camera,
         "dialogue": [{"speaker": sp, "line": l} for sp, l in lines], "refs": refs, "priority": priority,
         "night": night, "action_shot": action_shot, "broll": broll, "start_frame_prompt": action, "end_frame_prompt": end}
    if rose:
        s["rose_override"] = rose
    SHOTS.append(s)
    return s


def narr(text):
    SHOTS.append({"id": _next("N"), "type": "narration", "text": text.strip()})


def card(id_, text, seconds):
    SHOTS.append({"id": id_, "type": "title_card", "text": text, "duration_s": seconds})


OUTFITS = {"A": "A: ivory lace wedding dress",
           "A2": "A: the same ivory lace wedding dress, cleaned and carefully mended, veil pinned back",
           "B": "B: faded green gingham dress, low bun"}


def outfit(code):
    """Rose's outfit from this point on (A wedding dress, A2 the same dress mended, B gingham)."""
    SHOTS.append({"id": f"ROSE_OUTFIT_{code}", "type": "marker", "outfit": code})


TRAVEL = "her plain dark-gray travelling dress and a small black hat (not the wedding dress yet)"

# ======================= COLD OPEN: the title scene (all video, ~30 s) =======================
# The groom walks his mail-order bride down Main Street in handcuffs, in her mended wedding dress; the town laughs.
outfit("A2")
clip("Main street in the afternoon: Rose in her ivory lace wedding dress, her wrists in iron handcuffs, walks with her head held high beside Caleb, who holds her arm and will not look at her; townspeople crowd the boardwalks, staring and whispering.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], camera="slow tracking shot walking backwards in front of them", dur=6, id="C60")
clip("On the boardwalk Agatha Pell steps forward from the crowd, points her closed lace parasol at the young woman in handcuffs walking past, and speaks clearly so the whole street can hear.",
     ["CHAR_AGATHA", "LOC_STREET"], [("CHAR_AGATHA", "Look at her, ladies. A thief, delivered by mail.")], camera="medium shot, the crowd behind her", id="C61")
clip("Townspeople on the boardwalk laugh out loud and point at the bride in handcuffs; two well-dressed ladies hide their smiles behind their gloves; a man in a bowler hat shakes his head.",
     ["LOC_STREET"], camera="slow pan along the laughing crowd", dur=4)
clip("In the middle of the street Rose stops, turns to Caleb and speaks quietly, her chin up, her eyes wet but steady.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], [("CHAR_ROSE", "I wore it for you, Caleb. Like I promised.")], camera="close-up on Rose, the crowd blurred behind")
clip("Caleb, pale, his jaw tight, cannot meet her eyes; he takes her arm and answers in a low voice.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], [("CHAR_CALEB", "Keep walking, ma'am.")], camera="close-up on Caleb")
card("T00", "THREE DAYS EARLIER", 3)

# ======================= THE ROBBERY: one continuous action sequence =======================
outfit("A")
clip("Rose nods toward the small iron-banded green box at the old man's feet, curious.",
     ["CHAR_ROSE", "CHAR_AMOS", "PROP_BOX", "PROP_STAGE"], [("CHAR_ROSE", "What's in the box, Mr. Pruitt?")], camera="close-up on Rose", id="C28")
clip("Amos's smile fades; he looks out of the window at the rocks of the pass and answers quietly.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "Trouble, miss. The kind that has to reach the marshal.")], camera="close-up on Amos", id="C29")
clip("Masked riders burst out of the pines on both sides of the stage road at full gallop, firing; the lead horse of the stagecoach stumbles.",
     ["CHAR_BUCK", "PROP_STAGE", "LOC_PASS"], camera="wide tracking shot", action_shot=True,
     end="The riders flanking the racing stagecoach on both sides, dust and gun smoke everywhere.", id="C31")
clip("A dark-green stagecoach with yellow wheels races flat out along a narrow mountain road, six horses at full gallop, the old driver cracking the reins, dust boiling behind the wheels.",
     ["PROP_STAGE", "LOC_PASS"], camera="low tracking shot alongside the galloping team", action_shot=True, id="C01")
clip("Behind the coach, five riders with black bandanas over their faces gallop out of the pines, firing revolvers; gun smoke trails behind them.",
     ["CHAR_BUCK", "LOC_PASS"], camera="handheld tracking shot from the back of the coach toward the riders", action_shot=True, id="C02")
clip("The stagecoach careens along the edge of the road beside a sheer drop, horses rearing, the driver hauling on the reins.",
     ["PROP_STAGE", "LOC_PASS"], camera="low angle from the edge of the drop", action_shot=True,
     end="The coach swinging back onto the road at the last moment, one wheel over the edge, stones falling.", id="C32")
c03 = clip("Inside the bouncing stagecoach a young woman in an ivory lace wedding dress clutches a small iron-banded strongbox to her chest. Across from her an old guard with a white beard and spectacles fires his coach gun out of the window, then turns to her and shouts.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "When I say jump, girl, you jump!")], camera="handheld inside the shaking coach", action_shot=True,
     end="Same coach interior: the young woman has turned toward the open door, strongbox in her arms, the old guard pointing at the door.", id="C03")
clip("Inside the racing, bouncing coach old Amos, hit and pale, slumps against the seat and presses a small brass key into Rose's hand as she clutches the strongbox, gripping her wrist hard.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "Don't let Crane have it. Whatever they tell you.")], camera="close two-shot inside the shaking coach", action_shot=True, id="C33")
clip("The coach door flies open. The young woman in the ivory wedding dress leaps out with the strongbox in her arms and tumbles into the sagebrush, dress and veil billowing; behind her the stagecoach swerves toward the edge of the road.",
     ["CHAR_ROSE", "PROP_BOX", "PROP_STAGE", "LOC_PASS"], camera="wide shot, the coach thundering past camera", action_shot=True,
     end="The young woman in the torn ivory wedding dress lies in the sagebrush beside the road clutching the strongbox, looking up; the coach is a cloud of dust further down the road.", id="C04")
clip("Rose lies in the sagebrush in her torn wedding dress, breathing hard, dust settling around her; she looks down at the strongbox in her trembling hands, then up the road, terrified.",
     ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], camera="slow push in to her face", dur=6, id="C05")
clip("Rose in her torn ivory wedding dress scrambles up a rocky hillside through pines and sagebrush, clutching the strongbox, veil streaming, looking back at the road below.",
     ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], camera="tracking shot from the side", action_shot=True,
     end="Rose higher up the same hillside, crouching behind a boulder with the strongbox, looking down.", id="C34")
clip("Below on the stage road, Buck Tolliver pulls his bandana down, the pale scar on his cheek showing, and points up the hillside, shouting to his men.",
     ["CHAR_BUCK", "LOC_PASS"], [("CHAR_BUCK", "She went up the mountain! Find her!")], camera="low angle medium shot", action_shot=True, id="C35")
clip("Extreme close-up: trembling hands in torn lace sleeves gripping the small iron-banded green strongbox with its heavy brass padlock; dust drifting.",
     ["CHAR_ROSE", "PROP_BOX"], camera="static macro, very slow push in", broll=True, id="C06")
narr("""
Her name was Rose Calloway. She was twenty-four, from St. Louis, and she had never seen the face of the man she had come a thousand miles to marry.

She hid until dark between two boulders, in her mother's wedding dress, holding a box she could not open, while men with guns searched the rocks below.

In three days, her own groom would walk her down Main Street in handcuffs. But the strangest part of this story is not how she ended up on that mountain.

It's what she was holding.
""")
img("Rose hiding between two big granite boulders at dusk, the strongbox in her lap, her lace veil torn and dusty, eyes wide.", ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], "slow push in", id="I01")
img("Night on the mountainside: a lone small figure in a pale dress among the rocks under a sky full of stars.", ["CHAR_ROSE", "LOC_PASS"], "slow pull out", night=True, id="I02")
card("T01", "THE STAGECOACH BRIDE", 4)

# ======================= THE VILLAIN (the audience knows, the town doesn't) =======================
clip("Night, Crane's dark office in his white ranch house: Buck Tolliver, dusty from the ride, stands in the doorway with his hat in his hand and reports to the man at the window.",
     ["CHAR_BUCK", "CHAR_CRANE", "LOC_CRANE"], [("CHAR_BUCK", "She jumped with the box, boss. Went up the rocks.")], camera="medium shot on Buck", night=True)
clip("Silas Crane turns from the window with a thin cigar; his pale eyes are perfectly calm, his voice soft.",
     ["CHAR_CRANE", "CHAR_BUCK", "LOC_CRANE"], [("CHAR_CRANE", "Then find her. Mountains are full of sad accidents.")], camera="slow push in, close-up on Crane", night=True)
narr("""
Silas Crane had come to Cedar Bluff that spring. He bought the dead banker's share of the bank and paid for a new church roof. He had silver hair, a soft Southern voice, and the finest manners in the valley.

For two years, masked riders had robbed the stage on Raven Pass, always on the one day it carried the miners' gold. Nobody could explain how they knew.

People liked Silas Crane. People always liked him.
""")
clip("In front of a small white church on Main Street, Silas Crane in his charcoal suit and cream hat shakes the preacher's hand warmly; townspeople smile and tip their hats to him.",
     ["CHAR_CRANE", "LOC_STREET"], camera="slow pan", broll=True, dur=8, id="C21")
clip("Silas Crane on the veranda of his white ranch house at sunset, smoking a thin cigar, looking down at his long corrals full of cattle; his pale eyes are cold.",
     ["CHAR_CRANE", "LOC_CRANE"], camera="slow push in", broll=True, dur=8, id="C22")

# ======================= THE GROOM (same day, that morning) =======================
narr("""
That same morning in Cedar Bluff, the man she had come to marry was standing in front of a mirror.
""")
clip("In the small marshal's office Caleb stands in front of a cracked mirror on the wall, nervously straightening his red bandana and rehearsing his greeting with a hopeful, shy smile.",
     ["CHAR_CALEB", "LOC_JAIL"], [("CHAR_CALEB", "Miss Calloway. Welcome to Cedar Bluff, ma'am.")], camera="medium shot over his shoulder into the mirror", id="C07")
clip("Behind him Marshal Abel Hart leans back in his chair with his boots on the desk and speaks without looking up from his newspaper, dry and fond.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Son, she's marrying you, not that mirror.")], camera="medium shot", id="C08")
clip("Caleb turns and holds up a thick bundle of letters tied with a faded blue ribbon, earnest and a little defensive.",
     ["CHAR_CALEB", "CHAR_MARSHAL", "LOC_JAIL"], [("CHAR_CALEB", "Twenty-six letters, Abel. I know her better than anybody alive.")], camera="medium close-up on Caleb", id="C09")
clip("The marshal lowers his newspaper and looks at the young man for a long moment, then speaks quietly, with half a smile under his gray mustache.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Then you know more than most husbands ever do.")], camera="medium close-up on the marshal", id="C10")
clip("Night in the marshal's office: Caleb writes a letter at the desk with a dip pen by lamplight, pauses, smiles, and writes on.",
     ["CHAR_CALEB", "LOC_JAIL"], camera="slow push in", broll=True, night=True, dur=8, id="C12")
clip("A narrow room in a St. Louis boarding house: Rose sits by the window reading a letter in soft daylight, smiling to herself; a box of old books on the floor beside her.",
     ["CHAR_ROSE"], camera="slow push in", broll=True, dur=8, rose=TRAVEL, id="C11")
clip("Close-up: a woman's hands fold an ivory lace wedding dress and a small lace veil into a worn carpetbag, beside a bundle of letters tied with a faded blue ribbon.",
     ["CHAR_ROSE"], camera="static close-up, slow push in", broll=True, dur=8, rose=TRAVEL, id="C13")
narr("""
For six months, Deputy Caleb Ward had written to a woman in St. Louis every Sunday. He had found her name in a matrimonial paper, between a hardware advertisement and a notice about a lost mule.

Rose wrote back about her father, a printer who had died and left her nothing but debts and a box of books. In her last letter she promised to come in her mother's wedding dress, so that he would see her in it first.
""")
clip("Afternoon at the stage stop on Main Street: Caleb waits in a clean shirt with a small bunch of wildflowers. On the boardwalk behind him Agatha Pell, with her closed white lace parasol, speaks coolly to two other ladies, loud enough for him to hear. They smile thinly behind their gloves.",
     ["CHAR_AGATHA", "CHAR_CALEB", "LOC_STREET"], [("CHAR_AGATHA", "A bride by mail. Like a sack of flour from Denver.")], camera="medium shot, Caleb in the foreground", id="C14")
clip("Clara, passing along the boardwalk with a basket on her arm, stops beside Agatha and answers her calmly, without raising her voice; one of the ladies stifles a laugh at Agatha, then Clara walks on.",
     ["CHAR_CLARA", "CHAR_AGATHA", "LOC_STREET"], [("CHAR_CLARA", "At least she's coming for love, Agatha.")], camera="medium two-shot, Clara in focus", id="C15")
clip("The marshal rides up hard and reins in beside Caleb at the stage stop, grim.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_STREET"], [("CHAR_MARSHAL", "Caleb. The stage was hit on the pass.")], camera="medium shot, the marshal in the saddle", id="C36")
clip("The wildflowers fall from Caleb's hand into the dust as he runs for his horse.",
     ["CHAR_CALEB", "LOC_STREET"], camera="low angle on the flowers, Caleb running out of focus", dur=4, id="C37")
clip("Night on the pass. Caleb, alone with a lantern beside the overturned stagecoach at the edge of the drop, shouts into the darkness.",
     ["CHAR_CALEB", "PROP_STAGE", "LOC_PASS"], [("CHAR_CALEB", "Rose! Rose Calloway!")], camera="wide, then push in", night=True, id="C38")
narr("""
He searched the pass all night, calling a name he had written twenty-six times and never once said out loud.

He did not find her.

Someone else did.
""")

# ======================= THE STRANGER FINDS HER =======================
clip("Dawn among the boulders. Rose, exhausted and dusty in her torn wedding dress, raises a fist-sized rock. A few steps away Mercer stands with his hands open, calm, his dark bay horse behind him.",
     ["CHAR_MERCER", "CHAR_ROSE", "PROP_HORSE", "LOC_PASS"], [("CHAR_MERCER", "Easy, miss. If I meant you harm, you'd know it already.")], camera="over Rose's shoulder onto Mercer", id="C39")
clip("Rose, the rock still raised, trembling, asks him.",
     ["CHAR_ROSE", "CHAR_MERCER", "LOC_PASS"], [("CHAR_ROSE", "Are you one of them?")], camera="close-up on Rose", id="C40")
clip("Mercer slowly takes off his hat.",
     ["CHAR_MERCER", "CHAR_ROSE", "LOC_PASS"], [("CHAR_MERCER", "No, ma'am. I'm the one who found you first.")], camera="close-up on Mercer", id="C41")
img("Mercer leading his dark bay horse down the mountain at sunrise, Rose riding in the saddle in her ruined wedding dress, the strongbox in her arms.", ["CHAR_MERCER", "CHAR_ROSE", "PROP_HORSE", "PROP_BOX", "LOC_PASS"], "slow tracking drift", id="I03")
clip("In the warm Whitmore kitchen Clara wraps a shawl around Rose's shoulders over the torn wedding dress, sets a cup of coffee in front of her and speaks firmly, one hand on her shoulder.",
     ["CHAR_CLARA", "CHAR_ROSE", "LOC_KITCHEN"], [("CHAR_CLARA", "You'll stay here. Nobody touches a woman under my roof.")], camera="medium two-shot, warm light", id="C42")
outfit("B")
clip("A small bedroom at sunset. Rose wakes; a little girl with braids and a rag doll sits at the foot of the bed, staring at her with curiosity.",
     ["CHAR_LILY", "CHAR_ROSE"], [("CHAR_LILY", "Are you the bride?")], camera="medium shot from the foot of the bed", id="C43")
clip("Rose, still sleepy, smiles sadly at the girl.",
     ["CHAR_ROSE", "CHAR_LILY"], [("CHAR_ROSE", "I was supposed to be.")], camera="close-up on Rose", id="C44")
clip("Evening in the Whitmore kitchen at supper, Rose at the table in a borrowed gingham dress. Lily leans on the table on her elbows and asks her mother the question with mock innocence, glancing at Mercer by the door.",
     ["CHAR_LILY", "CHAR_CLARA", "CHAR_MERCER", "CHAR_ROSE", "LOC_KITCHEN"], [("CHAR_LILY", "Mama, is Mr. Mercer ever going to ask you?")], camera="medium shot", night=True, id="C16")
clip("Clara, drying a plate by the stove, blushes and tries not to smile; behind her Mercer looks down at his hat and Rose hides a smile.",
     ["CHAR_CLARA", "CHAR_MERCER", "LOC_KITCHEN"], [("CHAR_CLARA", "Eat your supper, Lily.")], camera="medium close-up on Clara", night=True, id="C17")
narr("""
It had been almost a year since a quiet stranger named John Mercer saved Clara Whitmore's ranch. He had never left. Every night after supper he said good night at the kitchen door and went out to sleep in the barn.

The whole town was waiting for him to ask her.

That night, after Lily was asleep, they tried the box. The brass key from Amos opened the padlock. Inside was a second lock, a small steel one, and no key that any of them had.
""")
clip("Golden afternoon at the Whitmore ranch: Mercer hammers a new split rail into the fence while Lily sits on the top rail swinging her legs, watching him.",
     ["CHAR_MERCER", "CHAR_LILY", "LOC_RANCH"], camera="slow pull out", broll=True, dur=8, id="C18")
img("Kitchen table: the open iron-banded strongbox revealing a second small steel lock inside, the brass key on the table, Clara, Rose and Mercer leaning over it.", ["PROP_BOX", "CHAR_CLARA", "CHAR_ROSE", "CHAR_MERCER", "LOC_KITCHEN"], "slow push in", night=True, id="I04")
clip("Mercer lifts the strongbox and shakes it gently beside his ear, frowning.",
     ["CHAR_MERCER", "PROP_BOX", "LOC_KITCHEN"], [("CHAR_MERCER", "Gold would rattle.")], camera="close-up", night=True, id="C45")
clip("Clara looks from the box to Rose, worried.",
     ["CHAR_CLARA", "CHAR_ROSE", "LOC_KITCHEN"], [("CHAR_CLARA", "Then what is worth killing for?")], camera="close-up on Clara", night=True, id="C46")

# ======================= PAYOFF: Crane's visit (Mercer puts him in his place) =======================
clip("Morning at the Whitmore ranch. Silas Crane stands on the porch with his cream hat in his hand and a basket of oranges, speaking with soft courtesy to Clara in the doorway.",
     ["CHAR_CRANE", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_CRANE", "Five hundred dollars for the box, Mrs. Whitmore. No questions asked.")], camera="medium two-shot", id="C47")
clip("Clara, arms folded in the doorway, answers flatly.",
     ["CHAR_CLARA", "CHAR_CRANE", "LOC_RANCH"], [("CHAR_CLARA", "I haven't seen any box, Mr. Crane.")], camera="close-up on Clara", id="C48")
clip("Crane smiles politely; his pale eyes move slowly over the windows and the barn.",
     ["CHAR_CRANE", "LOC_RANCH"], [("CHAR_CRANE", "Lovely house. So many doors.")], camera="close-up on Crane", id="C49")
clip("Mercer steps out of the barn door behind Crane with a rifle held loosely across his chest and speaks quietly, without any expression; Crane's smile freezes, he puts on his hat and walks back to his buggy.",
     ["CHAR_MERCER", "CHAR_CRANE", "LOC_RANCH"], [("CHAR_MERCER", "Mrs. Whitmore said good day, Mr. Crane.")], camera="low angle on Mercer, Crane in the foreground out of focus")
img("Close-up at ground level: the left front hoof of a tall roan horse held at the ranch gate, a horseshoe with one nail head missing; in soft focus behind, Mercer watching from the barn door.", ["CHAR_MERCER", "LOC_RANCH"], "slow push in", id="I05")
narr("""
Mercer was not watching Crane. He was watching the tall roan that Crane's man held at the gate, and the shoe on its left front hoof that rang wrong on the stones of the yard.

That night, the dog in the yard went quiet all at once.
""")

# ======================= ACTION: the night in the barn =======================
clip("Night inside the barn: Mercer and a masked man in a black bandana crash together into the hay, a lantern smashes and flares on the floor, horses rear in their stalls, a knife glints.",
     ["CHAR_MERCER", "LOC_BARN"], camera="handheld, low and close", night=True, action_shot=True,
     end="The masked man breaking free and running for the back door of the barn, Mercer on one knee in the hay.", id="C50")
clip("A masked rider on a tall roan horse gallops out of the moonlit ranch yard across stony ground, sparks flying from the horseshoes; Mercer limps out of the barn door behind him.",
     ["CHAR_MERCER", "LOC_RANCH"], camera="wide static shot from the porch", night=True, action_shot=True, id="C51")
narr("""
The man got away. But as he crossed the yard, Mercer heard it again. A loose shoe, ringing on the left front hoof.

The box was not in the barn. It was under a loose board in Clara's kitchen. And Silas Crane had run out of patience.
""")

# ======================= THE ARREST (in her wedding dress) =======================
clip("In the marshal's office Silas Crane leans lightly on his silver-headed cane and speaks softly, almost sadly, laying a folded paper on the desk.",
     ["CHAR_CRANE", "CHAR_MARSHAL", "LOC_JAIL"], [("CHAR_CRANE", "That box holds my gold, Marshal. And that woman was in on it.")], camera="slow push in on Crane", id="C52")
clip("The marshal stands up heavily, puts on his hat and gives the order, not unkindly.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Bring her in, Caleb. The law's the law.")], camera="medium two-shot", id="C53")
clip("Caleb, pale, answers his boss.",
     ["CHAR_CALEB", "CHAR_MARSHAL", "LOC_JAIL"], [("CHAR_CALEB", "She's no thief, Abel.")], camera="close-up on Caleb", id="C54")
clip("The marshal holds his gaze.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Then prove it. But bring her in.")], camera="close-up on the marshal", id="C55")
narr("""
Rose had spent two days mending her mother's wedding dress by the kitchen lamp. She had promised him he would see her in it first.

He came for her that afternoon. With a warrant.
""")
clip("Clara steps out onto the porch and raises a double-barreled shotgun at the young deputy as he dismounts at the gate.",
     ["CHAR_CLARA", "LOC_RANCH"], [("CHAR_CLARA", "Not one more step, Deputy.")], camera="low angle from the yard toward the porch", id="C56")
outfit("A2")
clip("Rose, in her mended ivory wedding dress, comes out beside Clara and gently pushes the shotgun barrels down, her eyes on Caleb.",
     ["CHAR_ROSE", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_ROSE", "It's all right, Clara. I'll go.")], camera="medium shot", id="C57")
clip("At the gate, face to face for the first time, Rose in her wedding dress looks up at Caleb for a long moment.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_RANCH"], [("CHAR_ROSE", "You're taller than I imagined.")], camera="close-up on Rose, golden light", id="C58")
clip("Rose smooths the mended lace of her wedding dress with one hand and gives him a small, brave smile.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_RANCH"], [("CHAR_ROSE", "I promised you'd see me in it first.")], camera="medium close-up on Rose, golden light")
clip("Caleb takes off his hat, miserable, the warrant in his other hand.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_RANCH"], [("CHAR_CALEB", "And you're under arrest, ma'am.")], camera="close-up on Caleb", id="C59")
narr("""
The jail was at the far end of Main Street. Caleb had to walk her past every door in Cedar Bluff.
""")
img("Close-up of Rose's face as she walks: chin up, eyes straight ahead, a single tear on her cheek that she does not wipe away.", ["CHAR_ROSE", "LOC_STREET"], "very slow push in", id="I06")

# ======================= PAYOFF: Clara silences Agatha =======================
clip("On the boardwalk, as the bride in handcuffs passes, Clara steps in front of Agatha Pell and speaks to her quietly, very close, so that only the ladies around them can hear.",
     ["CHAR_CLARA", "CHAR_AGATHA", "LOC_STREET"], [("CHAR_CLARA", "One more word, Agatha, and I'll tell them about Denver.")], camera="close two-shot, Clara in focus")
clip("Agatha Pell goes pale, lowers her parasol and says nothing; the two ladies beside her slowly step away from her, exchanging looks.",
     ["CHAR_AGATHA", "LOC_STREET"], camera="medium close-up on Agatha", dur=4)
clip("Main street in the afternoon: Rose in her wedding dress and handcuffs walks on beside Caleb toward the small log jail at the end of the street; the crowd has gone quiet.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET", "LOC_JAIL"], camera="wide shot from behind them", broll=True, dur=8)

# ======================= THE NIGHT IN JAIL =======================
clip("Night in the jail. Caleb sits on a stool outside the cell bars, turning his hat in his hands, speaking quietly without looking at her.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "I wrote you every Sunday for six months. I meant every word.")], camera="medium close-up through the bars", night=True, id="C62")
clip("Rose, in her wedding dress, comes to the bars and holds them, looking straight at him.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_ROSE", "I didn't steal anything, Caleb.")], camera="close-up through the bars", night=True, id="C63")
clip("Caleb finally looks up at her.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "I know.")], camera="close-up on Caleb", night=True, id="C64")
narr("""
He read to her that night through the bars, from a battered copy of Ivanhoe. She corrected his pronunciation twice.
""")
clip("Late at night in the jail, lamplight low. Rose sits on the floor against the bars, Caleb on the other side with an old book open on his knee; she asks him softly.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_ROSE", "Why did a man who writes like you need a matrimonial paper?")], camera="close two-shot through the bars", night=True, id="C65")
clip("Caleb closes the book and thinks before he answers.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "Out here, nobody ever asked what I was thinking. You did.")], camera="close-up on Caleb", night=True, id="C66")
narr("""
She put her hand through the bars, and he held it, and neither of them let go.

At two in the morning, the window exploded.
""")

# ======================= ACTION: the night raid on the jail =======================
clip("Night outside the small log jail on Main Street: masked riders circle in the street at a gallop, two of them hurling burning torches at the jail window.",
     ["CHAR_BUCK", "LOC_JAIL", "LOC_STREET"], camera="wide shot from across the street", night=True, action_shot=True, id="C67")
clip("A burning torch smashes through the window of the marshal's office and lands on the floor; flames race across spilled lamp oil.",
     ["LOC_JAIL"], camera="static wide shot inside the office", night=True, action_shot=True,
     end="Flames spreading across the floorboards and up the desk legs, smoke filling the room.", id="C68")
clip("In the smoke-filled jail Caleb throws himself in front of the cell bars, revolver up, shouting over his shoulder to Rose; a bullet hits his left shoulder and he staggers but keeps firing at the window.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "Stay behind me, Rose!")], camera="handheld medium shot, smoke and muzzle flashes", night=True, action_shot=True,
     end="Caleb kneeling in front of the cell bars clutching his left shoulder, revolver still raised, Rose in her wedding dress reaching for him through the bars.", id="C69")
clip("The jail door is kicked open; Mercer storms in through the smoke with a rifle, firing at the window, then grabs the ring of keys from the burning desk.",
     ["CHAR_MERCER", "LOC_JAIL"], camera="low angle from the floor", night=True, action_shot=True, id="C70")
narr("""
They wanted the box. It was not in the jail.

Mercer dragged Caleb out of the smoke and unlocked the cell with keys too hot to hold. By sunrise the jail was a black shell, Clara had brought Rose a dress, and the marshal released her into Clara's keeping.

And in the ashes by the hitching rail, Mercer found a horseshoe. One nail on the left side was snapped off short.
""")
outfit("B")
img("Dawn: the burned-out jail smoking, townspeople with water buckets, Caleb on the boardwalk with his shoulder bandaged, Rose kneeling beside him holding his hand.", ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], "slow pull out", id="I07")
clip("At dawn on the boardwalk Rose ties a bandage around Caleb's shoulder, her hands shaking, and speaks to him angrily, close to tears.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], [("CHAR_ROSE", "You could have been killed.")], camera="close two-shot", id="C71")
clip("Caleb manages a tired smile.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], [("CHAR_CALEB", "I wrote you I'd look after you. Meant that too.")], camera="close-up on Caleb", id="C72")
clip("Mercer holds up a worn horseshoe with one broken nail and speaks to Caleb, grim and certain.",
     ["CHAR_MERCER", "CHAR_CALEB", "LOC_STREET"], [("CHAR_MERCER", "Broken nail, left fore. That horse stood at Clara's gate.")], camera="low angle close on the horseshoe, then up to Mercer", id="C73")
clip("Caleb stares at the horseshoe; his jaw tightens.",
     ["CHAR_CALEB", "CHAR_MERCER", "LOC_STREET"], [("CHAR_CALEB", "Buck Tolliver's roan.")], camera="close-up on Caleb", id="C74")

# ======================= PAYOFF: the proof =======================
narr("""
But a horseshoe was not proof against the most respected man in the valley. They needed what was in the box.

That night, Rose Calloway asked Clara for a hairpin.
""")
clip("Night, the Whitmore kitchen: Rose bends over the strongbox picking the small steel lock with a hairpin; it clicks open. She glances up at the astonished faces around the table.",
     ["CHAR_ROSE", "CHAR_CLARA", "CHAR_MERCER", "PROP_BOX", "LOC_KITCHEN"], [("CHAR_ROSE", "My father printed handbills for every locksmith in St. Louis.")], camera="slow push in", night=True, id="C75")
clip("Clara lifts a letter from a stack tied with string inside the box and reads by lamplight; her face goes pale.",
     ["CHAR_CLARA", "PROP_BOX", "LOC_KITCHEN"], [("CHAR_CLARA", "Every gold shipment date. For two years.")], camera="close-up on Clara", night=True, id="C76")
clip("The marshal, standing at the end of the table, shakes his head.",
     ["CHAR_MARSHAL", "LOC_KITCHEN"], [("CHAR_MARSHAL", "Unsigned letters prove nothing.")], camera="medium close-up", night=True, id="C77")
clip("Rose lays a printed bill of lading next to one of the letters under the lamp and taps the matching curved capital letters with her finger, looking up at the marshal.",
     ["CHAR_ROSE", "CHAR_MARSHAL", "LOC_KITCHEN"], [("CHAR_ROSE", "A man can change his name. He can't change his hand.")], camera="close-up on the papers, then Rose", night=True, id="C78")
narr("""
The same hand had written both. Silas Crane had signed his own confession and handed it to the law.

A frightened clerk in Denver had been selling him the gold schedule. When the clerk lost his nerve, he gave Crane's letters to the only honest man he knew. Amos Pruitt.

There had never been any gold in that box. Crane had invented it, so the bride would hang before anyone read what she was carrying.
""")
img("Close-up on the kitchen table under an oil lamp: a printed bill of lading and an old handwritten letter side by side, a woman's finger on matching curved capital letters; the words are not legible.", ["CHAR_ROSE", "LOC_KITCHEN"], "slow push in", night=True, id="I08")
clip("Night on the Whitmore porch. Clara sits on the step beside Mercer, both looking out at the dark road, and asks him quietly.",
     ["CHAR_CLARA", "CHAR_MERCER", "LOC_RANCH"], [("CHAR_CLARA", "Why do you stay, John?")], camera="medium two-shot from the yard", night=True, id="C79")
clip("Mercer turns his hat in his hands and does not look at her.",
     ["CHAR_MERCER", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_MERCER", "You know why.")], camera="close-up on Mercer", night=True, id="C80")

# ======================= ACTION: Red Canyon =======================
narr("""
At dawn the marshal rode out with a warrant. Crane's house was empty and the safe stood open. Mercer read the ground for less than a minute.

Red Canyon, he said. Caleb rode with his arm in a sling. Nobody could talk him out of it.
""")
img("Crane's empty office in the white ranch house, the iron safe door hanging open, papers scattered on the floor, a cream-colored hat left on the desk.", ["LOC_CRANE"], "slow push in", id="I09")
clip("Riders gallop flat out through a narrow red sandstone canyon, dust and pebbles flying; far behind, two riders chase them.",
     ["CHAR_BUCK", "LOC_CANYON"], camera="low wide shot, riders racing past camera", action_shot=True,
     end="The riders further down the same canyon near a bend, the two pursuers closer now.", id="C81")
clip("Rifle shots crack from the canyon rim. Mercer leaps from his horse and drags Caleb down behind a big boulder as bullets kick up dust and splinter the rock beside them.",
     ["CHAR_MERCER", "CHAR_CALEB", "LOC_CANYON"], camera="handheld, low behind the boulder", action_shot=True,
     end="Mercer and Caleb crouched behind the boulder, rifles up, dust settling around them.", id="C82")
narr("""
Buck Tolliver had the high ground. But the war had taught John Mercer one thing above all others.

You don't go up. You go around.
""")
clip("Mercer climbs a steep red rock wall from behind, rifle slung across his back, his bad leg dragging, pebbles falling away under his boots.",
     ["CHAR_MERCER", "LOC_CANYON"], camera="low angle tilting up the rock face", action_shot=True, priority="optional", id="C83")
clip("On the canyon rim Mercer rises up behind Buck Tolliver, who is aiming a rifle down into the canyon, and slams him face down into the red dust, kicking the rifle away.",
     ["CHAR_MERCER", "CHAR_BUCK", "LOC_CANYON"], camera="medium shot along the rim", action_shot=True,
     end="Buck face down in the red dust, Mercer's boot on his back, the rifle out of reach.", id="C84")
clip("Mercer, kneeling on Buck's back, pulls him up by the collar.",
     ["CHAR_MERCER", "CHAR_BUCK", "LOC_CANYON"], [("CHAR_MERCER", "Where's Crane?")], camera="close two-shot", id="C85")
clip("Buck spits dust and laughs up at him.",
     ["CHAR_BUCK", "CHAR_MERCER", "LOC_CANYON"], [("CHAR_BUCK", "Ask the bride.")], camera="close-up on Buck", id="C86")
narr("""
The canyon was a decoy. Crane had gone back to Cedar Bluff for the one thing he still needed.

Clara had taken Lily into town. Rose was alone in the kitchen.
""")
img("Mercer and Caleb galloping flat out back along a dirt road toward a distant small town, dust behind them.", ["CHAR_MERCER", "CHAR_CALEB", "PROP_HORSE"], "fast push in", id="I10")

# ======================= ACTION + PAYOFF: the showdown on Main Street =======================
clip("In the kitchen Silas Crane stops across the table from Rose, smiling coldly, a small derringer pointed at her, and holds out his free hand for the strongbox she is clutching.",
     ["CHAR_CRANE", "CHAR_ROSE", "PROP_BOX", "LOC_KITCHEN"], [("CHAR_CRANE", "The box, Miss Calloway. And then we'll take a little ride.")], camera="slow push in on Crane over Rose's shoulder", id="C87")
clip("Noon on the deserted main street: Silas Crane walks Rose forward at gunpoint, the derringer at her ribs, the strongbox in her arms; townspeople watch silently from the doorways.",
     ["CHAR_CRANE", "CHAR_ROSE", "PROP_BOX", "LOC_STREET"], camera="slow tracking shot walking backwards in front of them", id="C88")
clip("At the end of the street Caleb steps off his lathered horse into the middle of the road, his left arm in a sling, his right hand by his revolver.",
     ["CHAR_CALEB", "LOC_STREET"], camera="low wide shot down the empty street", action_shot=True, id="C89")
clip("Caleb, steady, eyes on Crane.",
     ["CHAR_CALEB", "CHAR_CRANE", "LOC_STREET"], [("CHAR_CALEB", "Let her go, Crane.")], camera="close-up on Caleb", id="C90")
clip("Crane smiles, the derringer still pressed to Rose's side.",
     ["CHAR_CRANE", "CHAR_ROSE", "LOC_STREET"], [("CHAR_CRANE", "With one arm, Deputy? Step aside.")], camera="close-up on Crane", id="C91")
clip("Rose suddenly swings the heavy iron-banded strongbox with both hands into Crane's wrist; the derringer flies out of his hand and spins into the dust.",
     ["CHAR_ROSE", "CHAR_CRANE", "PROP_BOX", "LOC_STREET"], camera="close-up, slow motion feel", action_shot=True, dur=4,
     end="The derringer lying in the dust, Crane clutching his wrist, Rose holding the strongbox raised in both hands.", id="C92")
clip("On the flat roof of the livery stable Mercer kneels with his rifle aimed down at Crane's two men in the street, perfectly calm.",
     ["CHAR_MERCER", "LOC_STREET"], camera="low angle from the street up to the roof", id="C93")
clip("The marshal snaps handcuffs on Silas Crane in the middle of the street; Crane's cream hat lies in the dust beside the derringer.",
     ["CHAR_MARSHAL", "CHAR_CRANE", "LOC_STREET"], [("CHAR_MARSHAL", "Silas Crane. You're under arrest for robbing the mail.")], camera="medium two-shot", id="C94")
narr("""
Silas Crane had spent his whole life underestimating people. Ranchers. Old guards. Shy deputies.

And a bride who came by mail.

Amos Pruitt lived to testify in Denver. Crane and Buck Tolliver went to the penitentiary at Cañon City.

And a week later, on the same street where the town had laughed at her, Caleb Ward got down on one knee.
""")
img("Agatha Pell on the boardwalk, her parasol lowered, staring in shock as Crane is led away.", ["CHAR_AGATHA", "LOC_STREET"], "slow push in", id="I11")

# ======================= FINALE (with the last payoff for Agatha) =======================
clip("On the sunny main street Caleb, his arm still in a sling, kneels in the dust in front of Rose and holds up a small plain ring. Townspeople gather around.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], [("CHAR_CALEB", "Rose Calloway. Will you marry me? Properly, this time.")], camera="slow push in on Caleb", id="C95")
clip("Rose laughs through her tears and pulls Caleb to his feet. The crowd behind them cheers and throws hats in the air.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], [("CHAR_ROSE", "I came a thousand miles to say yes.")], camera="medium close-up, then the crowd", id="C96")
clip("Agatha Pell, stiff and red-faced, steps up in front of the whole street and offers Rose her gloved hand.",
     ["CHAR_AGATHA", "CHAR_ROSE", "LOC_STREET"], [("CHAR_AGATHA", "Miss Calloway. I was mistaken.")], camera="medium close-up on Agatha", id="C97")
clip("Rose takes Agatha's hand graciously.",
     ["CHAR_ROSE", "CHAR_AGATHA", "LOC_STREET"], [("CHAR_ROSE", "Then come to the wedding, Mrs. Pell.")], camera="close-up on Rose", id="C98")
narr("""
But the best moment of that day happened at sunset, and almost nobody saw it.
""")
clip("Evening at the Whitmore ranch. On the porch Mercer stands before Clara with his hat in his hands, nervous for the first time in his life.",
     ["CHAR_MERCER", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_MERCER", "Clara, I reckon I've slept in that barn long enough.")], camera="medium two-shot, sunset light", id="C99")
clip("Clara looks at him for a long moment, then smiles. In the window behind them, Lily grins.",
     ["CHAR_CLARA", "CHAR_MERCER", "CHAR_LILY", "LOC_RANCH"], [("CHAR_CLARA", "About time, John Mercer.")], camera="close-up on Clara, Lily in soft focus behind", id="C100")
clip("Final wide shot: the ranch house at dusk with warm glowing windows; the camera slowly rises and pulls back over the valley as the first stars appear.",
     ["LOC_RANCH"], camera="slow crane up and pull back", broll=True, dur=8, id="C101")
narr("""
They were married in October, when the aspens turned gold. Caleb and Rose stood up for them, and the next spring it was their turn.

Would you have stood up for Rose on that street, or stayed quiet like the rest of the town? Tell me in the comments, and tell me where you're watching from. And subscribe, because there are more stories waiting in Cedar Bluff.

Until next time, keep a light in the window.
""")
card("T02", "", 3)

# =============== HOOK CLIPS FOR SHORTS (9:16, made after the film clips) ===============
HOOKS = [
    {"id": "H01", "duration_s": 4, "refs": ["CHAR_ROSE", "PROP_BOX", "PROP_STAGE", "LOC_PASS"],
     "first_frame": "Vertical 9:16. Close on a young woman in an ivory lace wedding dress in mid-air, leaping out of the open door of a racing dark-green stagecoach, the iron-banded strongbox clutched to her chest, veil flying, dust and sagebrush below.",
     "video": "She lands hard in the sagebrush and rolls, the stagecoach thundering past behind her in a cloud of dust, gunshots in the distance. No dialogue."},
    {"id": "H02", "duration_s": 4, "refs": ["CHAR_ROSE", "CHAR_CRANE", "PROP_BOX", "LOC_STREET"],
     "first_frame": "Vertical 9:16. Close-up: the heavy iron-banded strongbox already swinging through the frame toward a man's wrist holding a small derringer; a silver-headed cane and a charcoal sleeve.",
     "video": "The box smashes into the wrist, the derringer flies out of his hand and spins into the dust in slow motion. No dialogue."},
    {"id": "H03", "duration_s": 4, "refs": ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"],
     "first_frame": "Vertical 9:16. Night, inside a small jail: a burning torch crashing through the window glass, shards and sparks in the air, a young woman behind iron bars in the background.",
     "video": "The torch hits the floor and flames race across spilled oil; a young deputy leaps in front of the cell bars as muzzle flashes light the window. No dialogue."},
]

# ---------------- OUTPUT ----------------
def wc(t):
    return len(re.findall(r"[A-Za-z']+", t))


_o = "A"
for s in SHOTS:
    if s["type"] == "marker":
        _o = s["outfit"]
    else:
        s["_o"] = _o
SHOTS = [s for s in SHOTS if s["type"] != "marker"]
_ids = [s["id"] for s in SHOTS]
assert len(_ids) == len(set(_ids)), "duplicate shot IDs"

clips = [s for s in SHOTS if s["type"] == "clip"]
images = [s for s in SHOTS if s["type"] == "image"]
narrs = [s for s in SHOTS if s["type"] == "narration"]
words = sum(wc(n["text"]) for n in narrs)
WPM = 140
core = [c for c in clips if c["priority"] == "core"]
opt = [c for c in clips if c["priority"] == "optional"]
on_screen = [c for c in core if not c["broll"]]
cards = sum(s["duration_s"] for s in SHOTS if s["type"] == "title_card")
est = {"clips": len(clips), "clips_core": len(core), "clips_optional": len(opt),
       "clips_dialogue": sum(bool(c["dialogue"]) for c in clips), "clips_action": sum(c["action_shot"] for c in clips),
       "clip_seconds_core": sum(c["duration_s"] for c in core), "clip_seconds_optional": sum(c["duration_s"] for c in opt),
       "images_new": sum("reuse_from" not in i for i in images), "images_reused": sum("reuse_from" in i for i in images),
       "narration_words": words, "narration_chars": sum(len(n["text"]) for n in narrs), "narration_min": round(words / WPM, 1),
       "credits_core_one_take": sum(PRICE[c["duration_s"]] for c in core), "credits_optional_one_take": sum(PRICE[c["duration_s"]] for c in opt),
       "credits_hooks": sum(PRICE[h["duration_s"]] for h in HOOKS),
       "api_usd_core_at_0_10_per_s": round(sum(c["duration_s"] for c in core) * 0.10, 1),
       "est_total_min_core": round((words / WPM * 60 + sum(c["duration_s"] for c in on_screen) + cards) / 60 * 1.08, 1)}


def ref_text(refs):
    parts = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src:
            parts.append(f"{src['name']}: {src['look']}")
    return " | ".join(parts)


def ref_files(refs, outfit_b=False):
    out = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        base = PREV if src and src.get("reuse_refs") else "visuals/refs"
        if r in CHARACTERS:
            full = "_full_B" if (r == "CHAR_ROSE" and outfit_b) else "_full"
            out += [f"{base}/{r}_front.png", f"{base}/{r}{full}.png"]
        else:
            out.append(f"{base}/{r}.png")
    return out


for s in SHOTS:
    o = s.pop("_o", "A")
    b = o == "B"
    if "CHAR_ROSE" in s.get("refs", []):
        s["rose_outfit"] = s.pop("rose_override", None) or OUTFITS[o]
    if s["type"] == "image":
        s["full_prompt"] = s["prompt"] + (f" Rose wears: {s['rose_outfit']}." if "rose_outfit" in s else "") + " " + STYLE + (NIGHT if s["night"] else "") + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else "")
        s["ref_files"] = ref_files(s["refs"], b)
        s["file"] = f"visuals/images/{s['id']}.png"
    elif s["type"] == "clip":
        s["start_frame_full_prompt"] = (s["start_frame_prompt"] + (f" Rose wears: {s['rose_outfit']}." if "rose_outfit" in s else "") + " First frame of the shot, characters in position" + (", mouths closed" if s["dialogue"] else "")
                                        + (", the action already in motion" if s["action_shot"] else "") + ". " + STYLE + (NIGHT if s["night"] else "")
                                        + " Characters/places: " + ref_text(s["refs"]))
        s["ref_files"] = ref_files(s["refs"], b)
        dl = " ".join(f'{CHARACTERS[d["speaker"]]["name"]} ({CHARACTERS[d["speaker"]]["voice"]}) says: "{d["line"]}"' for d in s["dialogue"])
        spk = [d["speaker"] for d in s["dialogue"]]
        present = [r for r in s["refs"] if r in CHARACTERS]
        only = (f" ONLY {CHARACTERS[spk[0]]['name']} speaks. Everyone else keeps their mouth closed and only listens." if spk and len(present) > 1 else "")
        timing = (" The line starts within the first second; after the line the speaker holds a natural expression, no extra words." if spk else "")
        s["video_prompt"] = (s["action"] + (ACTION if s["action_shot"] else "") + (" Camera: " + s["camera"] + "." if s["camera"] else "")
                             + (" Dialogue: " + dl + only + timing if dl else " No dialogue, natural sound effects only (hooves, gunshots, fire, wind), nobody speaks.")
                             + " " + CLIP_STYLE)
        s["credits"] = PRICE[s["duration_s"]]
        s["files"] = {"start_frame": f"visuals/images/{s['id']}_first.png", "video": f"visuals/video/{s['id']}.mp4"}
        if s.get("end_frame_prompt"):
            s["end_frame_full_prompt"] = (s["end_frame_prompt"] + (f" Rose wears: {s['rose_outfit']}." if "rose_outfit" in s else "")
                                          + " Last frame of the same shot: same characters, same costumes, same place and light as the first frame. "
                                          + STYLE + (NIGHT if s["night"] else "") + " Characters/places: " + ref_text(s["refs"]))
            s["files"]["end_frame"] = f"visuals/images/{s['id']}_last.png"

for h in HOOKS:
    h["first_frame_full_prompt"] = h["first_frame"] + " " + STYLE.replace("16:9 widescreen", "9:16 vertical") + " Characters/places: " + ref_text(h["refs"])
    h["video_prompt"] = h["video"] + ACTION + " " + CLIP_STYLE.replace("16:9", "9:16 vertical")
    h["ref_files"] = ref_files(h["refs"], h["id"] != "H01")
    h["credits"] = PRICE[h["duration_s"]]
    h["files"] = {"start_frame": f"visuals/hooks/{h['id']}_first.png", "video": f"visuals/hooks/{h['id']}.mp4"}


# ---------------- REFERENCE PROMPTS (Phase 1) ----------------
REF_BG = ("Character reference sheet photo, photorealistic, 1880 American West period clothing, plain warm neutral studio background, "
          "soft even daylight, sharp focus, natural skin texture, no text, no logos, no watermark.")
REF_PROMPTS = []
for cid, c in CHARACTERS.items():
    if c.get("reuse_refs"):
        continue
    look = c["look"]
    if cid == "CHAR_ROSE":
        base, outfit_a, outfit_b = look.split(" OUTFIT A")[0], "OUTFIT A" + look.split("OUTFIT A")[1].split(" OUTFIT B")[0], "OUTFIT B" + look.split("OUTFIT B")[1]
        REF_PROMPTS += [
            {"file": f"visuals/refs/{cid}_front.png", "prompt": f"Head-and-shoulders portrait, facing the camera, calm gentle expression. {base} {outfit_a.rstrip('. ')}. {REF_BG}"},
            {"file": f"visuals/refs/{cid}_34.png", "prompt": f"Three-quarter view portrait from the waist up, slight smile. {base} {outfit_a.rstrip('. ')}. {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"},
            {"file": f"visuals/refs/{cid}_full.png", "prompt": f"Full-body standing pose, the whole dress visible. {base} {outfit_a.rstrip('. ')}. {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"},
            {"file": f"visuals/refs/{cid}_full_B.png", "prompt": f"Full-body standing pose. {base} {outfit_b.rstrip('. ')}. {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"},
        ]
    else:
        REF_PROMPTS += [
            {"file": f"visuals/refs/{cid}_front.png", "prompt": f"Head-and-shoulders portrait, facing the camera. {look} {REF_BG}"},
            {"file": f"visuals/refs/{cid}_34.png", "prompt": f"Three-quarter view portrait from the waist up. {look} {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"},
            {"file": f"visuals/refs/{cid}_full.png", "prompt": f"Full-body standing pose. {look} {REF_BG}", "use_ref": f"visuals/refs/{cid}_front.png"},
        ]
for group in (PROPS, LOCATIONS):
    for rid, r in group.items():
        if r.get("reuse_refs"):
            continue
        REF_PROMPTS.append({"file": f"visuals/refs/{rid}.png", "prompt": f"{r['look']}. Clear reference image of {r['name'].lower()}, no people unless needed for scale. " + STYLE})

TITLE = "The Stagecoach Bride"
YT = "They Laughed as the Groom Led His Mail-Order Bride Away in Chains — They Didn't Know What Was in Her Box"
out = {"title": TITLE, "series": "Tales of Cedar Bluff", "episode": 2, "working_title_youtube": YT,
       "setting": "Cedar Bluff, Colorado (a state since 1876), September 1880, golden aspens",
       "format": {"aspect": "16:9 (hooks 9:16)", "video_model": "Omni 1.1 Flash 720p", "image_model": "Nano Banana Pro", "fps": 24,
                  "clip_durations_allowed_s": [4, 6, 8], "credits_by_duration": {"4": 7, "6": 10, "8": 12}},
       "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE, "reused_refs_from": PREV,
       "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "ref_prompts": REF_PROMPTS, "timeline": SHOTS, "hooks": HOOKS}

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{here}/narration", exist_ok=True)
json.dump(out, open(f"{here}/shotlist.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for n in narrs:
    open(f"{here}/narration/{n['id']}.txt", "w", encoding="utf-8").write(n["text"] + "\n")

L = [f"# {TITLE.upper()}\n", f"*Tales of Cedar Bluff, фильм 2 · {YT}*\n",
     f"Оценка: ~{est['est_total_min_core']} мин · клипов {est['clips']} (обязательных {est['clips_core']}: {est['clip_seconds_core']} с ≈ {est['credits_core_one_take']} кредитов Flow или ≈ ${est['api_usd_core_at_0_10_per_s']} через API; по желанию {est['clips_optional']}: ≈ {est['credits_optional_one_take']} кредитов) · с репликами {est['clips_dialogue']}, экшен {est['clips_action']} · хуки 3 ≈ {est['credits_hooks']} · картинок новых {est['images_new']}, из первого фильма {est['images_reused']} · рассказчик {words} слов, {est['narration_chars']} символов (~{est['narration_min']} мин)\n",
     "Обозначения: **C** — видеоклип 4–8 с, говорит один персонаж · **I** — картинка с движением камеры под голос рассказчика · **N** — рассказчик · **T** — титр · ⚡ — экшен-клип.\n"]
for s in SHOTS:
    if s["type"] == "clip":
        tag = {"core": "", "optional": " *(по желанию)*"}[s["priority"]] + (" *(под рассказчика)*" if s["broll"] else "")
        L.append(f"\n**{s['id']} · КЛИП {s['duration_s']} с{' ⚡' if s['action_shot'] else ''}**{tag} — {s['action']}" + (f"  \n_Камера: {s['camera']}_" if s['camera'] else ""))
        for d in s["dialogue"]:
            L.append(f"> **{CHARACTERS[d['speaker']]['name'].upper()}:** {d['line']}")
        if s.get("end_frame_prompt"):
            L.append(f"_Последний кадр: {s['end_frame_prompt']}_")
        if s.get("montage_note"):
            L.append(f"_Монтаж: {s['montage_note']}_")
    elif s["type"] == "image":
        L.append(f"- {s['id']} · {s['prompt']} _({s['motion']}{'; из первого фильма' if 'reuse_from' in s else ''})_")
    elif s["type"] == "narration":
        L.append(f"\n**{s['id']} · РАССКАЗЧИК**\n")
        L.append("\n".join("> " + p if p.strip() else ">" for p in s["text"].split("\n")))
    else:
        L.append(f"\n**{s['id']} · ТИТР** — {s['text'] or '(чёрный экран)'} ({s['duration_s']} с)")
L.append("\n## Хуки для шортсов (9:16, делать после клипов фильма)\n")
for h in HOOKS:
    L.append(f"- **{h['id']}** ({h['duration_s']} с) — {h['first_frame']} → {h['video']}")
open(f"{here}/screenplay.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print(json.dumps(est, ensure_ascii=False))
