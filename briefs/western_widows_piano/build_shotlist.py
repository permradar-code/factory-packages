# -*- coding: utf-8 -*-
"""Source of truth for "The Widow's Piano". Generates shotlist.json, screenplay.md, narration/*.txt."""
import json, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado Territory, autumn 1879, "
         "natural light, 35mm film grain, muted warm earth tones with golden aspen accents, shallow depth of field, "
         "period-accurate clothing and props. No text, no captions, no logos, no watermark, no modern objects.")
FLASHBACK = " Flashback look: slightly desaturated, soft warm vignette."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, 1879 Colorado, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
              "Characters only speak the exact lines given, in English, with lips in sync. No subtitles, no text on screen, no music.")

CHARACTERS = {
 "CHAR_CLARA": {"name": "Clara Whitmore", "role": "heroine, widow, 28",
   "look": "28-year-old American frontier woman, an original fictional character who does not resemble any real person or celebrity, naturally beautiful and gentle, slender, softly rounded face, slightly wide-set gray-green eyes with a quiet sadness, a small faint beauty mark below her left eye, a slight bump on the bridge of her nose, warm auburn-brown hair in a braided crown with a few loose strands framing her face, clear fair skin, proud dignified expression, faded dark-blue calico dress with a patched left elbow, narrow black mourning ribbon at the collar, small oval silver locket on a chain",
   "voice": "warm, low, steady American woman's voice, late twenties, a little weary, never shrill"},
 "CHAR_LILY": {"name": "Lily Whitmore", "role": "Clara's daughter, 8",
   "look": "8-year-old girl, freckles, two light-brown braids tied with faded blue ribbons, pale yellow cotton pinafore dress over a white blouse, scuffed brown lace-up boots, carries a small rag doll",
   "voice": "bright, soft American little girl's voice, eight years old"},
 "CHAR_MERCER": {"name": "John Mercer", "role": "the stranger, 40, Union veteran",
   "look": "40-year-old man, tall and lean, weathered tanned face, short dark-brown beard with gray at the chin, gray at the temples, calm gray-blue eyes, long dark-brown canvas duster coat, black flat-brimmed hat, faded blue Union cavalry trousers, worn brown leather gun belt, walks with a slight limp on the left leg",
   "voice": "deep, quiet, unhurried American baritone, few words, never raises his voice"},
 "CHAR_PIKE": {"name": "Horace Pike", "role": "banker, villain, 55",
   "look": "55-year-old heavy-set man, clean-shaven chin with thick gray mutton-chop side-whiskers, small round gold spectacles, black frock coat, burgundy silk vest with a gold watch chain, gold signet ring, often holds a cigar with a gold paper band, oily polite smile",
   "voice": "smooth, slightly nasal, condescending American man's voice, fifties"},
 "CHAR_DEKE": {"name": "Deke Harlan", "role": "auctioneer, Pike's man, 35",
   "look": "35-year-old skinny man, sharp face, thin mustache, loud yellow-and-brown checkered vest over a dirty white shirt with sleeve garters, brown bowler hat, wooden gavel",
   "voice": "loud, fast, sing-song auctioneer voice with a twang"},
 "CHAR_AGATHA": {"name": "Agatha Pell", "role": "mercantile owner's wife, 50",
   "look": "50-year-old woman, tight gray bun, pinched face, high-collared plum-purple silk dress, ivory cameo brooch, white lace parasol",
   "voice": "shrill, mocking, upper-class American woman's voice"},
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50",
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
 "CHAR_SAM": {"name": "Samuel Whitmore", "role": "Clara's late husband (flashbacks only)",
   "look": "man in his thirties, sandy-blond hair, full sandy mustache, kind blue eyes, broad shoulders, faded work shirt and suspenders; in war flashbacks a dark-blue Union army sergeant's uniform with yellow chevrons",
   "voice": "none (no dialogue)"},
}
PROPS = {
 "PROP_PIANO": {"name": "Mother's piano",
   "look": "old upright parlor piano, dark walnut wood with a hand-carved floral panel on the front, two brass candle sconces, yellowed ivory keys with one cracked key near the middle, small engraved brass plate above the keys"},
 "PROP_HORSE": {"name": "Mercer's horse",
   "look": "tall dark bay horse with a white blaze on the face and black mane, worn brown western saddle with a rolled gray blanket"},
}
LOCATIONS = {
 "LOC_STREET": {"name": "Cedar Bluff main street",
   "look": "small 1879 frontier town main street, dirt road, wooden false-front buildings (mercantile, bank with brick front, saloon, livery), boardwalks, hitching rails, horses and wagons, mountains and golden aspens beyond; signs have no legible text"},
 "LOC_PLATFORM": {"name": "Auction platform",
   "look": "flatbed wagon used as an auction platform in front of the brick bank building, a small table with a ledger, crowd of townspeople in period clothes around it"},
 "LOC_RANCH": {"name": "Whitmore ranch exterior",
   "look": "small weathered log-and-plank ranch house with a covered front porch, split-rail fence, small barn with a corral, dirt road leading up, foothills and golden aspen trees, a hill with a single wooden grave cross behind the house"},
 "LOC_PARLOR": {"name": "Whitmore parlor",
   "look": "plain warm parlor inside a log house, rough log walls, wide plank floor, oil lamp, lace curtain on a small window, rag rug, a framed tintype of a man in Union uniform on a shelf, the piano against the wall"},
 "LOC_KITCHEN": {"name": "Whitmore kitchen",
   "look": "simple kitchen in a log house, wood stove, rough wooden table with three chairs, tin plates, oil lamp, coffee pot"},
 "LOC_BARN": {"name": "Barn",
   "look": "small wooden barn interior, hay bales, a stall with the dark bay horse, hanging lantern, tools on the wall"},
 "LOC_RIDGE": {"name": "North ridge",
   "look": "rocky granite ridge above the ranch, wind-bent pines, sagebrush, view down over the valley and the distant town"},
 "LOC_BANK": {"name": "Bank interior",
   "look": "dim bank interior, dark wood counter with brass teller grille, black iron safe, ledger books, brass lamp, framed valley map with pins on the wall"},
}

SHOTS = []  # ordered timeline
def img(id_, prompt, refs, motion="slow push in", flash=False):
    SHOTS.append({"id": id_, "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "flashback": flash})
PRICE = {4: 7, 6: 10, 8: 12}
def _dur(lines):
    w = sum(len(l.split()) for _, l in lines)
    if not lines: return 6
    return 4 if w <= 5 else 6 if w <= 12 else 8
def clip(id_, action, refs, lines=(), camera="", priority="core", end_frame=None, start_frame_prompt=None):
    lines = list(lines)
    speakers = []
    for sp, _ in lines:
        if sp not in speakers: speakers.append(sp)
    if len(speakers) <= 1:
        SHOTS.append({"id": id_, "type": "clip", "duration_s": _dur(lines), "action": action, "camera": camera,
                      "dialogue": [{"speaker": sp, "line": l} for sp, l in lines], "refs": refs,
                      "priority": priority, "start_frame_prompt": start_frame_prompt or action, "end_frame_prompt": end_frame})
        return
    # one speaker per clip: split into shot / reverse shot, one line each
    for i, (sp, l) in enumerate(lines):
        name = CHARACTERS[sp]["name"]
        others = [CHARACTERS[r]["name"] for r in refs if r in CHARACTERS and r != sp]
        frame = (f"Medium close-up on {name}" + (f", {' and '.join(others)} seen partly from behind, out of focus in the foreground" if others else "") + ".")
        part_action = (action + f" THIS SHOT: {'reverse angle, ' if i else ''}{frame} {name} speaks; nobody else talks.")
        SHOTS.append({"id": f"{id_}{'abcdefgh'[i]}", "type": "clip", "duration_s": _dur([(sp, l)]), "action": part_action,
                      "camera": "static or very slow push in", "dialogue": [{"speaker": sp, "line": l}],
                      "refs": [sp] + [r for r in refs if r != sp], "priority": priority, "split_from": id_,
                      "start_frame_prompt": part_action, "end_frame_prompt": None})
def narr(id_, text):
    SHOTS.append({"id": id_, "type": "narration", "text": text.strip()})
def card(id_, text, seconds):
    SHOTS.append({"id": id_, "type": "title_card", "text": text, "duration_s": seconds})

# ---------------- SCENE 1: THE AUCTION (cold open) ----------------
clip("C01", "Wide high shot over the crowded main street at midday. An old upright piano stands on a flatbed wagon in front of the brick bank. Deke Harlan in a checkered vest bangs his wooden gavel on a small table and shouts to the crowd.",
     ["LOC_STREET","LOC_PLATFORM","CHAR_DEKE","PROP_PIANO"], [("CHAR_DEKE","Lot thirty-one! One upright parlor piano, property of the late Samuel Whitmore, sold by order of the court!")],
     camera="slow crane down from above the rooftops toward the wagon")
clip("C02", "At the edge of the crowd Clara stands very still, holding Lily's hand. Townspeople glance at her and whisper. Lily looks up at her mother.",
     ["CHAR_CLARA","CHAR_LILY","LOC_STREET"], [("CHAR_LILY","Mama... are they selling Grandma's piano?"),("CHAR_CLARA","Hold my hand, Lily. Just hold my hand.")],
     camera="medium two-shot, slow push in on Clara's face")
clip("C03", "Agatha Pell under a white lace parasol leans toward two other well-dressed women and speaks loudly enough for everyone to hear. The women laugh behind their gloves.",
     ["CHAR_AGATHA","LOC_STREET"], [("CHAR_AGATHA","A dirt farmer's widow with a parlor piano. Pride goeth before the fall, ladies.")],
     camera="medium shot, slight handheld")
clip("C04", "Horace Pike stands on the bank steps with his thumbs in his silk vest, cigar in hand, and calls out with an oily smile. Laughter ripples through the crowd.",
     ["CHAR_PIKE","LOC_PLATFORM"], [("CHAR_PIKE","Let's be generous, Deke. Start it at five dollars.")], camera="low angle medium shot")
clip("C05", "Agatha lifts her parasol like a bidding paddle and calls out a bid. The crowd laughs. Cut to a close-up of Clara: her eyes are wet but her chin stays up.",
     ["CHAR_AGATHA","CHAR_CLARA","LOC_STREET"], [("CHAR_AGATHA","Six dollars! It will make lovely kindling.")], camera="medium shot then close-up")
clip("C06", "Deke points the gavel around the grinning crowd, dragging out the call.",
     ["CHAR_DEKE","LOC_PLATFORM","PROP_PIANO"], [("CHAR_DEKE","Six dollars, going once... going twice...")], camera="medium shot, slow push in", priority="optional")
clip("C07", "At the very back of the crowd, beside a dark bay horse, a tall man in a long dark duster slowly raises one hand. People nearest to him turn around. The street goes quiet.",
     ["CHAR_MERCER","PROP_HORSE","LOC_STREET"], [("CHAR_MERCER","Two hundred.")], camera="slow push in from behind the crowd to the man's face")
clip("C08", "The crowd turns. Pike's smile fades. Deke stammers, gavel frozen in the air. The stranger answers calmly.",
     ["CHAR_DEKE","CHAR_PIKE","CHAR_MERCER","LOC_PLATFORM"], [("CHAR_DEKE","Two hun... two hundred... dollars, mister?"),("CHAR_MERCER","In gold.")],
     camera="quick reaction shots")
clip("C09", "Deke weakly taps the gavel. Mercer walks through the parting crowd, limping slightly, and drops a heavy leather coin pouch on the auction table.",
     ["CHAR_DEKE","CHAR_MERCER","LOC_PLATFORM"], [("CHAR_DEKE","...Sold."),("CHAR_MERCER","Deliver it to the Whitmore place. Tonight.")], camera="tracking shot following Mercer")
clip("C10", "Across the street Clara and the stranger look at each other for a long moment. He touches the brim of his hat, turns and walks away to his horse. Clara stands frozen, Lily at her side. No dialogue.",
     ["CHAR_CLARA","CHAR_LILY","CHAR_MERCER","LOC_STREET"], [], camera="over-the-shoulder, slow push in on Clara")
card("T01", "THE WIDOW'S PIANO", 5)

# ---------------- SCENE 2: WHO CLARA IS ----------------
narr("N01", """
Cedar Bluff, Colorado Territory. October, 1879.

Until that morning, Clara Whitmore had not cried in front of a single soul. Not at her husband's funeral. Not when the letters from the bank began to arrive. And not when the sheriff nailed the court's notice to her door.

If this story finds its way to your heart, stay with Clara until the very end, and tell me in the comments where you are watching from tonight.

Samuel Whitmore had been a good man. He came home from the war with a scar he never talked about, a Union coat he never wore again, and a dream of a hundred and sixty acres under the Colorado sky. For seven years, he and Clara built that dream with their own hands. A cabin of pine logs. A barn. A fence of split rails. And a little girl named Lily.

Then came the summer of the great drought. The creek dried to a trickle. The corn burned in the field. And for the first time in his life, Sam Whitmore walked into the Cedar Bluff Bank with his hat in his hand.

Horace Pike was happy to help. He was always happy to help.

Three hundred dollars, for seed and a winter's flour. Sam signed the note without reading the small print. Men like Sam never did.

That winter, a fever came through the valley. It took four men in Cedar Bluff. One of them was Sam.

Clara buried him on the hill behind the house, under the aspens he had planted. And then she did what women on the frontier had always done. She kept going.

She sold eggs. She took in mending. And three afternoons a week, the children of Cedar Bluff came to her parlor to learn the piano. Her mother's piano, carried across the plains in a wagon in 1858. The only beautiful thing she owned.

But Horace Pike's interest grew faster than any corn. Three hundred became four hundred. Four hundred became four hundred and eighty. With penalties on top.

Clara was not the first widow in the valley to owe Horace Pike money. The Hendersons had lost their place the spring before. The Kowalski farm, the autumn before that. And each time, Pike bought the land himself, at auction, for whatever he pleased.

So when the court ordered her household goods sold to pay the arrears, Clara understood exactly what Pike wanted.

He didn't want her piano. He wanted her to know she had nothing left.
""")
img("I01", "Wide establishing view of the small town of Cedar Bluff in a mountain valley at morning, golden aspens on the slopes, thin chimney smoke, dirt road winding in.", ["LOC_STREET"], "slow aerial drift forward")
img("I02", "An old framed tintype photograph on a wooden shelf: a young couple on their wedding day, the man in a dark Union army coat, the woman in a simple light dress. Soft lamplight.", ["CHAR_SAM","CHAR_CLARA","LOC_PARLOR"], "slow push in", flash=True)
img("I03", "Sam Whitmore and Clara building the log cabin together, Sam lifting a pine log, Clara holding the other end, laughing, bright summer day.", ["CHAR_SAM","CHAR_CLARA","LOC_RANCH"], "slow pan right", flash=True)
img("I04", "Sam lifting a laughing little girl (Lily, about 3 years old) onto his shoulders in front of the new barn, sunset light.", ["CHAR_SAM","LOC_RANCH"], "slow push in", flash=True)
img("I05", "Drought: cracked dry earth, burnt brown corn stalks in a field, Sam standing in the middle looking up at a white, cloudless sky, heat haze.", ["CHAR_SAM","LOC_RANCH"], "slow pull out", flash=True)
img("I06", "Sam standing at the bank counter holding his hat in both hands, Horace Pike behind the brass teller grille sliding a paper toward him with a polite smile.", ["CHAR_SAM","CHAR_PIKE","LOC_BANK"], "slow push in", flash=True)
img("I07", "Close-up of a hand signing a loan note with a dip pen at the bank counter, Pike's gold signet ring visible on the hand holding the paper down.", ["CHAR_PIKE","LOC_BANK"], "slow push in", flash=True)
img("I08", "Winter night: Sam lying ill with fever in a narrow bed, Clara sitting beside him holding his hand, a single oil lamp, frost on the window.", ["CHAR_SAM","CHAR_CLARA"], "very slow push in", flash=True)
img("I09", "Snowy hillside behind the ranch house: a fresh grave with a simple wooden cross under bare aspens, Clara and little Lily standing in black shawls, backs to camera.", ["CHAR_CLARA","CHAR_LILY","LOC_RANCH"], "slow pull out")
img("I10", "Clara in the henhouse at dawn collecting eggs into a basket, breath visible in the cold air.", ["CHAR_CLARA","LOC_RANCH"], "slow pan left")
img("I11", "Clara sewing by lamplight at the kitchen table, a pile of other people's clothes to mend beside her.", ["CHAR_CLARA","LOC_KITCHEN"], "slow push in")
img("I12", "Afternoon in the parlor: Clara sitting beside a small girl at the piano, guiding her hands on the keys, warm window light.", ["CHAR_CLARA","PROP_PIANO","LOC_PARLOR"], "slow pan right")
img("I13", "Close-up detail of the old walnut piano: hand-carved floral panel, brass candle sconce, yellowed keys with one cracked key, Clara's fingers resting on the keys.", ["PROP_PIANO","CHAR_CLARA"], "slow pan across the carving")
img("I14", "Flashback: a covered wagon crossing the open prairie in 1858, the shape of an upright piano tied under canvas in the back, a young girl walking beside it.", ["PROP_PIANO"], "slow pan right", flash=True)
img("I15", "Kitchen table covered with opened envelopes and bank letters, an oil lamp, Clara's tired hands pressed flat on the papers.", ["CHAR_CLARA","LOC_KITCHEN"], "slow push in")
img("I16", "Horace Pike alone in his bank office, reading a ledger with a satisfied smile, cigar smoke curling, a framed valley map with several pins on the wall behind him.", ["CHAR_PIKE","LOC_BANK"], "slow push in")
img("I17", "An abandoned homestead with boarded windows and a broken gate, tumbleweeds in the yard, gray overcast sky.", [], "slow pull out")
img("I18", "A grieving widow and two children sitting on a wagon loaded with their belongings, leaving a farm, Pike watching from his black buggy in the background.", ["CHAR_PIKE"], "slow pan left")
img("I19", "A sheriff hammering a paper notice onto the wooden front door of the Whitmore house, Clara watching from the porch with her arms folded.", ["CHAR_CLARA","LOC_RANCH"], "slow push in")
img("I20", "Back to the present: Clara and Lily walking home along a dusty road at dusk after the auction, empty-handed, long shadows, golden aspens.", ["CHAR_CLARA","CHAR_LILY"], "slow tracking drift")

# ---------------- SCENE 3: THE PIANO RETURNS ----------------
narr("N02", """
That evening, the parlor felt like a church after a funeral.

There was a pale square on the floorboards where the piano had stood for six years. Clara swept around it twice before she understood that she was afraid to step on it.

Lily fell asleep without asking for a song.

And Clara sat by the window until the lamp burned low, wondering who the stranger was, and what a man like that could possibly want with a widow's piano.
""")
img("I21", "The empty parlor at evening: a pale clean rectangle on the dusty plank floor against the wall where a piano used to stand, an oil lamp, long shadows.", ["LOC_PARLOR"], "slow push in")
img("I22", "Clara sweeping the parlor floor with a broom, stopping at the edge of the pale square on the floorboards.", ["CHAR_CLARA","LOC_PARLOR"], "slow push in")
img("I23", "Lily asleep in a small bed holding her rag doll, moonlight through a lace curtain.", ["CHAR_LILY"], "very slow push in")
img("I24", "Clara sitting by the dark window, face lit by a nearly burned-out oil lamp, looking out at the road.", ["CHAR_CLARA","LOC_PARLOR"], "slow push in")
img("I25", "Sunrise over the ranch: a freight wagon with a large canvas-covered shape in the back coming up the dirt road, a rider on a dark bay horse beside it.", ["LOC_RANCH","PROP_HORSE","CHAR_MERCER"], "slow push in")
clip("C11", "Morning. Clara stands on the porch and raises a double-barreled shotgun as the wagon and the rider stop at her gate.",
     ["CHAR_CLARA","LOC_RANCH"], [("CHAR_CLARA","That's far enough. If you've come to collect, mister, there's nothing left to sell.")], camera="low angle from the yard toward the porch")
clip("C12", "Mercer takes off his hat and holds it against his chest, calm, standing by his horse at the gate.",
     ["CHAR_MERCER","PROP_HORSE","LOC_RANCH"], [("CHAR_MERCER","I didn't come to collect, ma'am. I came to return something.")], camera="medium close-up")
clip("C13", "Two hired men lift the piano off the wagon. Clara slowly lowers the shotgun but keeps her voice hard.",
     ["CHAR_CLARA","PROP_PIANO","LOC_RANCH"], [("CHAR_CLARA","I don't take charity. Not from the bank, and not from strangers.")], camera="medium shot")
clip("C14", "Mercer nods toward a broken section of split-rail fence. Behind Clara, Lily peeks out of the doorway, smiling.",
     ["CHAR_MERCER","CHAR_LILY","LOC_RANCH"], [("CHAR_MERCER","Then don't call it charity. Your east fence is down. I'll fix it for a hot supper.")], camera="medium shot, rack focus to Lily")
clip("C15", "Inside the parlor Lily runs to the returned piano and presses a key. Clara watches from the doorway and her face softens, then she turns to Mercer outside.",
     ["CHAR_LILY","CHAR_CLARA","CHAR_MERCER","PROP_PIANO","LOC_PARLOR"], [("CHAR_CLARA","One supper. And you sleep in the barn."),("CHAR_MERCER","Yes, ma'am.")], camera="slow push in")

narr("N03", """
One supper became two. Two became a week.

The stranger gave his name only as Mercer, and he gave little else. He was up before the rooster. He rebuilt the east fence, rehung the barn door, and split enough wood to last until Christmas. He never asked for wages, and he never asked questions.

Lily followed him everywhere like a small shadow. He showed her how to brush a horse in long strokes, the way the hair grows, and how to talk to an animal so it learns to trust you. Clara watched from the kitchen window and told herself not to get used to it.

At supper, the three of them ate mostly in silence. It was not an unkind silence.

And at night, for the first time since Sam died, Clara played again.

She played the old songs. And always, at the very end, she played Shenandoah. The song Sam used to whistle while he worked.

She did not know that out on the porch step, in the dark, the stranger sat with his hat in his hands and his eyes closed, listening to every note.
""")
img("I26", "Mercer at dawn hammering a new split rail into the fence, breath visible, mountains behind.", ["CHAR_MERCER","LOC_RANCH"], "slow pan right")
img("I27", "Mercer splitting firewood with an axe beside the barn, a tall neat woodpile growing, Lily sitting on a stump watching him.", ["CHAR_MERCER","CHAR_LILY","LOC_RANCH"], "slow push in")
img("I28", "Mercer kneeling beside Lily in the corral, guiding her small hand as she brushes the dark bay horse.", ["CHAR_MERCER","CHAR_LILY","PROP_HORSE"], "slow push in")
img("I29", "Clara watching through the kitchen window, a dish towel in her hands, a faint smile she is trying to hide.", ["CHAR_CLARA","LOC_KITCHEN"], "slow push in")
img("I30", "Supper at the rough wooden kitchen table: Clara, Lily and Mercer eating in quiet lamplight, tin plates, coffee pot.", ["CHAR_CLARA","CHAR_LILY","CHAR_MERCER","LOC_KITCHEN"], "slow pan left")
img("I31", "Night: the ranch house seen from the yard, one warm glowing window, the silhouette of a woman playing a piano inside.", ["LOC_RANCH"], "very slow push in")
img("I32", "Close-up of Clara playing the piano by lamplight, eyes half closed.", ["CHAR_CLARA","PROP_PIANO","LOC_PARLOR"], "slow push in")
img("I33", "Mercer sitting alone on the dark porch step, hat in his hands, eyes closed, listening, lamplight spilling through the door crack.", ["CHAR_MERCER","LOC_RANCH"], "very slow push in")
clip("C16", "Night on the porch. Clara stops playing and steps out with two tin cups of coffee, hands one to Mercer and stands beside him.",
     ["CHAR_CLARA","CHAR_MERCER","LOC_RANCH"], [("CHAR_CLARA","My husband used to whistle that song."),("CHAR_MERCER","Lot of men did. Back then.")], camera="two-shot, lamplight from the door")

# ---------------- SCENE 4: THE RIDGE ----------------
narr("N04", """
On the fourth morning, a calf went missing, and Mercer rode up to the north ridge to look for it.

He found the calf. He also found something else.

Wooden stakes, driven into the rock in a straight line, each with a strip of red cloth snapping in the wind. Surveyor's stakes. Fresh ones.

The rock around them had been chipped and split, and in the morning sun, the broken stone glittered.

And there, in the dust beside the stakes, lay the stub of an expensive cigar, still wrapped in its gold paper band.

There was only one man in Cedar Bluff who smoked cigars like that.
""")
img("I34", "Mercer riding the dark bay horse up a rocky granite ridge in morning light, wind in the pines.", ["CHAR_MERCER","PROP_HORSE","LOC_RIDGE"], "slow tracking drift")
img("I35", "A brown calf standing among sagebrush on the ridge, looking at the camera.", ["LOC_RIDGE"], "slow push in")
img("I36", "A line of fresh wooden surveyor's stakes driven into the rocky ground, red cloth strips snapping in the wind, valley far below.", ["LOC_RIDGE"], "slow pan along the stakes")
img("I37", "Close-up of chipped and broken granite with bright silvery metallic veins glittering in the sun.", ["LOC_RIDGE"], "slow push in")
img("I38", "Close-up in the dust: a half-smoked cigar stub still wrapped in a gold paper band, beside a fresh boot print.", ["LOC_RIDGE"], "slow push in")
clip("C17", "Mercer crouches by the stakes, cracks a rock open with the hilt of his knife, turns the glittering piece in his fingers, then looks down toward the town.",
     ["CHAR_MERCER","LOC_RIDGE"], [("CHAR_MERCER","Silver. So that's what you're after.")], camera="close-up then over-the-shoulder toward the valley")

# ---------------- SCENE 5: PIKE'S VISIT ----------------
clip("C18", "A shiny black buggy pulls up in front of the ranch house. Horace Pike steps down, adjusting his spectacles, and smiles at Clara on the porch.",
     ["CHAR_PIKE","CHAR_CLARA","LOC_RANCH"], [("CHAR_PIKE","Mrs. Whitmore. I've come with a kindness.")], camera="medium wide shot")
clip("C19", "Pike holds out a folded paper. Clara does not take it.",
     ["CHAR_PIKE","CHAR_CLARA","LOC_RANCH"], [("CHAR_PIKE","Five hundred for the land. Clears your debt and buys you a ticket east."),("CHAR_CLARA","It's not for sale.")],
     camera="over-the-shoulder shots")
clip("C20", "Pike notices Mercer leaning on the barn door with an axe, studies him over his spectacles.",
     ["CHAR_PIKE","CHAR_MERCER","LOC_RANCH"], [("CHAR_PIKE","And who might you be?"),("CHAR_MERCER","A man who pays his debts.")], camera="reaction shots, slow push in on Pike")
clip("C21", "Pike climbs back into the buggy, the smile gone, and speaks coldly before driving off in a cloud of dust.",
     ["CHAR_PIKE","LOC_RANCH"], [("CHAR_PIKE","The note comes due Saturday, Mrs. Whitmore. The court doesn't care about pianos.")], camera="medium shot, buggy pulls away", priority="optional")
narr("N05", """
That night, Clara counted everything she had on the kitchen table. Egg money. Lesson money. The silver locket her mother had left her.

Sixty-three dollars.

The stranger's gold had paid the arrears. But the note itself, four hundred and eighty dollars, came due on Saturday. If it wasn't paid, the court would sell the land, the house, and everything in it.

And everyone in Cedar Bluff knew who would be the only bidder.
""")
img("I39", "Kitchen table at night: a few coins, folded dollar bills, an egg basket and a silver locket laid out under an oil lamp, Clara's hands counting.", ["CHAR_CLARA","LOC_KITCHEN"], "slow push in")
img("I40", "Clara sitting alone at the kitchen table, head in her hands, lamp low.", ["CHAR_CLARA","LOC_KITCHEN"], "slow pull out")
img("I41", "Clara standing in the dark parlor looking at the piano, moonlight on the carved walnut.", ["CHAR_CLARA","PROP_PIANO","LOC_PARLOR"], "slow push in")
img("I42", "Horace Pike in his dark bank office at night, pinning a new pin into the valley map on the wall, cigar glowing.", ["CHAR_PIKE","LOC_BANK"], "slow push in")

# ---------------- SCENE 6: NIGHT THREAT ----------------
narr("N06", """
Somewhere past midnight, the horses in the corral began to stamp and snort.

Three riders came down off the ridge without a light between them. They only lit their torches when they reached the barn.
""")
img("I43", "Night: three riders silhouetted on the ridge against a starry sky, no lights, bandanas over their faces.", ["LOC_RIDGE"], "slow push in")
img("I44", "Close-up: a match flaring to light a pitch torch in the dark beside the barn wall, a masked face lit orange.", ["LOC_BARN"], "slow push in")
clip("C22", "A masked rider throws a burning torch onto the hay by the barn wall. Flames catch. Mercer bursts out of the barn and drags the burning hay away with a pitchfork.",
     ["CHAR_MERCER","LOC_BARN","LOC_RANCH"], [], camera="fast handheld, firelight")
clip("C23", "Clara on the porch in a nightgown and shawl fires the shotgun into the air. The horses rear.",
     ["CHAR_CLARA","LOC_RANCH"], [("CHAR_CLARA","The next one goes lower!")], camera="low angle, muzzle flash")
clip("C24", "Mercer pulls one rider off his horse and pins him to the ground. The bandana slips: it is Deke Harlan, terrified.",
     ["CHAR_MERCER","CHAR_DEKE","LOC_RANCH"], [("CHAR_MERCER","Tell Pike the lady isn't selling.")], camera="close-up struggle, firelight")
img("I45", "Dawn: the barn wall blackened with soot but still standing, water buckets on the ground, smoke drifting.", ["LOC_BARN","LOC_RANCH"], "slow pan left")
img("I46", "Dawn: Clara and Mercer sitting on the porch steps, exhausted, ash on their faces, a shotgun leaning on the rail.", ["CHAR_CLARA","CHAR_MERCER","LOC_RANCH"], "slow push in")
clip("C25", "On the porch steps at dawn, Clara turns to Mercer, shaken. He looks out at the road for a long time before answering.",
     ["CHAR_CLARA","CHAR_MERCER","LOC_RANCH"], [("CHAR_CLARA","Why are you doing this? You don't even know us."),("CHAR_MERCER","Ask me Saturday.")], camera="slow two-shot")

# ---------------- SCENE 7: LOW POINT ----------------
narr("N07a", """
When the sun came up, the barn wall was black with soot, but it was still standing.

And by the next morning, the stranger was gone.

His horse was gone from the stall. His bedroll was gone from the hay. There was no note. Only a mended fence, a full woodpile, and a little girl standing at the window.
""")
img("I47", "Morning light in the barn: an empty horse stall, a flattened spot in the hay where a bedroll used to be.", ["LOC_BARN"], "slow push in")
img("I48", "Clara standing at the gate looking down the long empty road, wind moving her skirt.", ["CHAR_CLARA","LOC_RANCH"], "slow pull out")
img("I49", "Lily at the window with her rag doll, waiting, breath fogging the glass.", ["CHAR_LILY","LOC_PARLOR"], "slow push in")
clip("C26", "In the parlor Lily turns from the window to her mother. Clara kneels and hugs her.",
     ["CHAR_LILY","CHAR_CLARA","LOC_PARLOR"], [("CHAR_LILY","He'll come back, Mama. He said Saturday."),("CHAR_CLARA","Men say a lot of things, sweetheart.")], camera="medium shot, slow push in")
narr("N07b", """
Clara told herself she had expected it. Men left. That was the way of the world. The war had taught her that, and the fever had taught her again.

On Thursday, Pike's man rode out and nailed a new notice to her gatepost. The Whitmore homestead, to be sold at public auction, Saturday at noon.

On Friday, Clara took Sam's old Union coat out of the trunk, folded it, and laid it on top of her few dresses.

And that night, she closed the lid of her mother's piano, and did not play.
""")
img("I50", "Deke Harlan smirking as he hammers a paper notice onto the Whitmore gatepost.", ["CHAR_DEKE","LOC_RANCH"], "slow push in")
img("I51", "A lone rider on a dark bay horse galloping across the open plains at night toward the distant lights of a city.", ["PROP_HORSE","CHAR_MERCER"], "slow tracking drift")
img("I52", "Clara kneeling by an open wooden trunk, folding a faded dark-blue Union army coat with sergeant's chevrons.", ["CHAR_CLARA","LOC_PARLOR"], "slow push in")
img("I53", "Close-up: Clara's hand slowly closing the wooden lid over the piano keys in the dark.", ["CHAR_CLARA","PROP_PIANO"], "very slow push in")

# ---------------- SCENE 8: SATURDAY ----------------
img("I54", "Saturday noon: the main street crowded again around the auction wagon, bright sun, more people than before.", ["LOC_STREET","LOC_PLATFORM"], "slow crane down")
img("I55", "Clara and Lily in their best faded Sunday dresses standing near the platform, holding hands.", ["CHAR_CLARA","CHAR_LILY","LOC_PLATFORM"], "slow push in")
img("I56", "Pike seated at the auction table with an open ledger and a neat stack of gold coins, smiling, cigar in hand.", ["CHAR_PIKE","LOC_PLATFORM"], "slow push in")
clip("C27", "Deke stands on the wagon and shouts to the crowd. Pike lifts one finger lazily.",
     ["CHAR_DEKE","CHAR_PIKE","LOC_PLATFORM"], [("CHAR_DEKE","The Whitmore homestead, one hundred sixty acres! Opening bid from Mr. Pike: four hundred eighty dollars!")], camera="medium shot")
clip("C28", "Agatha whispers to her friends with satisfaction. Clara squeezes Lily's hand.",
     ["CHAR_AGATHA","CHAR_CLARA","CHAR_LILY","LOC_STREET"], [("CHAR_AGATHA","Well. Now she'll finally learn her place.")], camera="medium shot then close-up on joined hands", priority="optional")
clip("C29", "Hoofbeats. Three riders gallop into the street through the dust: Mercer, a gray-mustached U.S. Marshal with a silver star, and a thin clerk with a leather satchel. The crowd turns.",
     ["CHAR_MERCER","CHAR_MARSHAL","PROP_HORSE","LOC_STREET"], [], camera="low wide shot, riders coming toward camera")
clip("C30", "Mercer dismounts and walks, limping, straight to Pike's table.",
     ["CHAR_MERCER","CHAR_PIKE","LOC_PLATFORM"], [("CHAR_MERCER","Before anyone bids, the marshal has a question for Mr. Pike.")], camera="tracking shot")
clip("C31", "The marshal holds up official papers with a seal. Pike rises, red-faced, blustering.",
     ["CHAR_MARSHAL","CHAR_PIKE","LOC_PLATFORM"], [("CHAR_MARSHAL","Horace Pike. You filed a silver claim in Denver on land you don't own. That's fraud."),("CHAR_PIKE","Preposterous!")],
     camera="medium two-shot")
clip("C32", "Mercer drops a heavy leather coin pouch onto Pike's open ledger. The clerk stamps a paper.",
     ["CHAR_MERCER","CHAR_PIKE","LOC_PLATFORM"], [("CHAR_MERCER","Four hundred eighty. The Whitmore note is paid. In full.")], camera="close-up on the pouch, then Pike's face")
clip("C33", "The marshal snaps handcuffs on Pike. The crowd gasps. Agatha drops her lace parasol into the dust.",
     ["CHAR_MARSHAL","CHAR_PIKE","CHAR_AGATHA","LOC_PLATFORM"], [], camera="wide then insert of the parasol falling")
img("I57", "Pike in handcuffs being led away by the marshal through the silent crowd, spectacles askew.", ["CHAR_PIKE","CHAR_MARSHAL","LOC_STREET"], "slow tracking drift")
img("I58", "The thin clerk handing Clara a stamped official paper; she holds it with trembling hands.", ["CHAR_CLARA","LOC_PLATFORM"], "slow push in")

# ---------------- SCENE 9: THE REVEAL ----------------
clip("C34", "The crowd drifts away. Clara walks up to Mercer by his horse, the paper in her hand, eyes wet.",
     ["CHAR_CLARA","CHAR_MERCER","PROP_HORSE","LOC_STREET"], [("CHAR_CLARA","It's Saturday. Why?")], camera="medium two-shot, slow push in")
clip("C35", "Mercer takes a worn, many-times-folded letter from inside his coat and hands it to her.",
     ["CHAR_MERCER","CHAR_CLARA","LOC_STREET"], [("CHAR_MERCER","Shiloh. April of 'sixty-two. Your husband carried me two miles with a ball in my leg.")], camera="close-up on the letter, then Mercer")
clip("C36", "Close on Mercer, then Clara covering her mouth, tears running.",
     ["CHAR_MERCER","CHAR_CLARA","LOC_STREET"], [("CHAR_MERCER","He made me promise. If I ever got west, his Clara would never sell her mother's piano.")], camera="slow push in, shot-reverse-shot")
narr("N08", """
The letter was soft as cloth from being folded and unfolded a thousand times. The handwriting was Sam's.

John Mercer had been a twenty-two-year-old private when the line broke at Shiloh. A musket ball shattered his leg. He would have died in the mud if a sergeant from Ohio had not thrown him over his shoulders and carried him two miles to the surgeons' tents, whistling Shenandoah the whole way, so the boy would not hear his own screaming.

After the war, Sam wrote to him once. Just once. One promise.

It took Mercer fifteen years and a cattle business in Wyoming before he could keep it. By the time he found Cedar Bluff, Sam had been in the ground for a year.

He had come too late for his friend.

But he had not come too late for her.
""")
img("I59", "Close-up of an old, soft, much-folded letter in faded brown ink held in a woman's trembling hands; the handwriting is not legible.", ["CHAR_CLARA"], "slow push in")
img("I60", "Flashback, battlefield of Shiloh 1862: gun smoke drifting through trees, a Union sergeant with a sandy mustache carrying a wounded young private over his shoulders.", ["CHAR_SAM"], "slow tracking drift", flash=True)
img("I61", "Flashback: a field surgeon's tent at dusk, lanterns, the sergeant setting the wounded private down on a cot.", ["CHAR_SAM"], "slow push in", flash=True)
img("I62", "Flashback: two Union soldiers by a campfire at night, the sergeant whittling and whistling, the younger man with a bandaged leg smiling.", ["CHAR_SAM"], "slow push in", flash=True)
img("I63", "Mercer years later on a Wyoming cattle ranch, rereading the same old letter by a campfire under the stars.", ["CHAR_MERCER"], "slow push in")
img("I64", "Present: Mercer standing in the street with his hat in his hands, looking at Clara with quiet emotion.", ["CHAR_MERCER","LOC_STREET"], "slow push in")

# ---------------- SCENE 10: FINALE ----------------
narr("N09", """
Horace Pike was taken to Denver in irons that same afternoon. Before the month was out, the Hendersons had their deed back.

And that evening, as the sun went down behind the aspens, the windows of the Whitmore house glowed gold, and the sound of a piano drifted out over the valley for the first time in a week.

Clara played Shenandoah. Lily sat beside her on the bench.

And in the doorway, a tall man stood with his hat in his hands, waiting to be asked in.
""")
img("I65", "Pike in the back of a barred prison wagon leaving town, the marshal riding beside it.", ["CHAR_PIKE","CHAR_MARSHAL"], "slow pull out")
img("I66", "The Whitmore ranch at golden sunset, chimney smoke, warm light in every window, aspens glowing.", ["LOC_RANCH"], "slow push in")
img("I67", "Parlor at evening: Clara playing the piano, Lily beside her on the bench resting her head on her mother's arm.", ["CHAR_CLARA","CHAR_LILY","PROP_PIANO","LOC_PARLOR"], "slow push in")
img("I68", "Mercer standing in the open doorway of the parlor, hat in his hands, lamplight on his face.", ["CHAR_MERCER","LOC_PARLOR"], "slow push in")
clip("C37", "Clara stops playing, looks up at Mercer in the doorway and speaks softly. For the first time in the film, Mercer smiles.",
     ["CHAR_CLARA","CHAR_MERCER","CHAR_LILY","PROP_PIANO","LOC_PARLOR"], [("CHAR_CLARA","Supper's at six, Mr. Mercer. Every night, if you'd like."),("CHAR_MERCER","I'd like that, ma'am.")],
     camera="shot-reverse-shot, warm lamplight")
clip("C38", "Final wide shot: the ranch house at dusk with warm glowing windows. The camera slowly rises and pulls back over the valley as the first stars appear. No dialogue.",
     ["LOC_RANCH"], [], camera="slow crane up and pull back")
narr("N10", """
Thank you for riding along with Clara, Lily, and Mercer tonight. If this story warmed your heart, there are more waiting for you on this channel.

Until next time, keep a light in the window.
""")
img("I69", "The valley at night under a sky full of stars, a single warm window glowing far below.", ["LOC_RANCH"], "slow pull out")
card("T02", "", 3)

# ---------------- OUTPUT ----------------
def wc(t): return len(re.findall(r"[A-Za-z']+", t))
clips=[s for s in SHOTS if s["type"]=="clip"]; images=[s for s in SHOTS if s["type"]=="image"]; narrs=[s for s in SHOTS if s["type"]=="narration"]
words=sum(wc(n["text"]) for n in narrs)
WPM=140
est = {"clips": len(clips), "clips_core": sum(c["priority"]=="core" for c in clips), "clips_optional": sum(c["priority"]=="optional" for c in clips),
       "images": len(images), "narration_words": words, "narration_min": round(words/WPM,1),
       "clip_min": round(sum(c["duration_s"] for c in clips)/60,1), "clips_4s": sum(c["duration_s"]==4 for c in clips), "clips_6s": sum(c["duration_s"]==6 for c in clips), "clips_8s": sum(c["duration_s"]==8 for c in clips), "credits_one_take": sum(PRICE[c["duration_s"]] for c in clips), "credits_core_one_take": sum(PRICE[c["duration_s"]] for c in clips if c["priority"]=="core"),
       "est_total_min": round(words/WPM + sum(c["duration_s"] for c in clips)/60 + 1.0, 1)}

# resolve prompts with style + refs
def ref_text(refs):
    parts=[]
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src: parts.append(f"{src['name']}: {src['look']}")
    return " | ".join(parts)
for s in SHOTS:
    if s["type"]=="image":
        s["full_prompt"] = s["prompt"] + " " + STYLE + (FLASHBACK if s["flashback"] else "") + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else "")
        s["file"] = f"visuals/images/{s['id']}.png"
    elif s["type"]=="clip":
        s["start_frame_full_prompt"] = s["start_frame_prompt"] + " First frame of the shot, characters in position, mouths closed. " + STYLE + " Characters/places: " + ref_text(s["refs"])
        dl = " ".join(f'{CHARACTERS[d["speaker"]]["name"]} ({CHARACTERS[d["speaker"]]["voice"]}) says: "{d["line"]}"' for d in s["dialogue"])
        spk = [d["speaker"] for d in s["dialogue"]]
        present = [r for r in s["refs"] if r in CHARACTERS]
        only = (f" ONLY {CHARACTERS[spk[0]]['name']} speaks. Everyone else keeps their mouth closed and only listens." if spk and len(present) > 1 else "")
        timing = (" The line starts within the first second; after the line the speaker holds a natural expression, no extra words." if spk else "")
        s["video_prompt"] = (s["action"] + (" Camera: " + s["camera"] + "." if s["camera"] else "") + (" Dialogue: " + dl + only + timing if dl else " No dialogue, natural ambient sound only, nobody speaks.") + " " + CLIP_STYLE)
        s["credits"] = PRICE[s["duration_s"]]
        s["files"] = {"start_frame": f"visuals/images/{s['id']}_first.png", "video": f"visuals/video/{s['id']}.mp4"}

out = {"title": "The Widow's Piano", "working_title_youtube": "They Auctioned the Widow's Piano for Her Husband's Debt — Then a Silent Stranger Raised One Hand",
       "format": {"aspect": "16:9", "video_model": "Omni 1.1 Flash 720p", "image_model": "Nano Banana Pro", "fps": 24, "clip_durations_allowed_s": [4,6,8], "credits_by_duration": {"4": 7, "6": 10, "8": 12}},
       "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE,
       "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "timeline": SHOTS}
os.makedirs("narration", exist_ok=True)
json.dump(out, open("shotlist.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
for n in narrs: open(f"narration/{n['id']}.txt","w",encoding="utf-8").write(n["text"]+"\n")

# screenplay.md
L=[f"# THE WIDOW'S PIANO\n", f"*{out['working_title_youtube']}*\n",
   f"Оценка: ~{est['est_total_min']} мин · клипов {est['clips']} (4 с: {est['clips_4s']}, 6 с: {est['clips_6s']}, 8 с: {est['clips_8s']}; ~{est['credits_one_take']} кредитов за один дубль; обязательных {est['clips_core']}, по желанию {est['clips_optional']}) · картинок {est['images']} · текст рассказчика {words} слов (~{est['narration_min']} мин)\n",
   "Обозначения: **C** — видеоклип 4–8 с, в каждом говорит один персонаж (персонажи говорят в кадре) · **I** — картинка с движением камеры под голос рассказчика · **N** — текст рассказчика · **T** — титр.\n"]
for s in SHOTS:
    if s["type"]=="clip":
        tag = "" if s["priority"]=="core" else " *(по желанию — можно заменить картинкой)*"
        L.append(f"\n**{s['id']} · КЛИП {s['duration_s']} с**{tag} — {s['action']}" + (f"  \n_Камера: {s['camera']}_" if s['camera'] else ""))
        for d in s["dialogue"]:
            L.append(f"> **{CHARACTERS[d['speaker']]['name'].upper()}:** {d['line']}")
    elif s["type"]=="image":
        L.append(f"- {s['id']} · {s['prompt']} _({s['motion']})_")
    elif s["type"]=="narration":
        L.append(f"\n**{s['id']} · РАССКАЗЧИК**\n")
        L.append("\n".join("> " + p if p.strip() else ">" for p in s["text"].split("\n")))
    else:
        L.append(f"\n**{s['id']} · ТИТР** — {s['text'] or '(чёрный экран)'} ({s['duration_s']} с)")
open("screenplay.md","w",encoding="utf-8").write("\n".join(L)+"\n")
print(json.dumps(est, ensure_ascii=False))
