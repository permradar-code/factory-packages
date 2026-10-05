# -*- coding: utf-8 -*-
"""Source of truth for "The Stagecoach Bride" (Tales of Cedar Bluff, film 2).
Generates shotlist.json, screenplay.md and narration/*.txt.
Structure: cold open (the stagecoach attack, cut before the outcome) -> "Ten days earlier" -> story with an action
set piece every ~3 minutes -> romance and justice in the finale.
Setting: Cedar Bluff, Colorado, September 1880 (a state since 1876 - never write "Territory").
"""
import json, os, re

STYLE = ("Photorealistic cinematic film still, 16:9 widescreen, American West, Colorado, early autumn 1880, "
         "natural light, 35mm film grain, muted warm earth tones with golden aspen accents, shallow depth of field, "
         "period-accurate clothing and props. No text, no captions, no logos, no watermark, no modern objects.")
NIGHT = " Night scene: moonlight and warm firelight or lamplight, deep shadows, faces still clearly readable."
CLIP_STYLE = ("Cinematic live-action western drama, photorealistic, 16:9, Colorado 1880, natural light, film grain. "
              "Keep every character's face, hair, clothing and body exactly as in the start frame and references for the whole shot. "
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
   "voice": "shrill, mocking, upper-class American woman's voice"},
 "CHAR_MARSHAL": {"name": "Marshal Abel Hart", "role": "Deputy U.S. Marshal, 50, Caleb's boss", "reuse_refs": True,
   "look": "50-year-old lawman, thick gray walrus mustache, deep-set eyes, long gray wool coat, five-pointed silver star badge, brown wide-brimmed hat",
   "voice": "gruff, flat, authoritative American man's voice"},
 # ---- new faces (refs to make in Phase 1) ----
 "CHAR_ROSE": {"name": "Rose Calloway", "role": "the mail-order bride from St. Louis, 24",
   "look": "24-year-old American woman, an original fictional character (not a celebrity lookalike), slender, oval face, large warm dark-brown eyes, straight dark brows, a few faint freckles across the nose, full lips, fair skin, glossy dark-brown almost black hair pinned up with soft loose curls at the temples. "
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


def img(id_, prompt, refs, motion="slow push in", night=False, reuse=None):
    SHOTS.append({"id": id_, "type": "image", "prompt": prompt, "refs": refs, "motion": motion, "night": night,
                  **({"reuse_from": reuse} if reuse else {})})


def _dur(lines, action=False):
    w = sum(len(l.split()) for _, l in lines)
    if not lines:
        return 6
    return 4 if w <= 5 else 6 if w <= 12 else 8


def clip(id_, action, refs, lines=(), camera="", priority="core", night=False, action_shot=False, dur=None):
    lines = list(lines)
    speakers = []
    for sp, _ in lines:
        if sp not in speakers:
            speakers.append(sp)
    assert len(speakers) <= 1, f"{id_}: one speaker per clip"
    SHOTS.append({"id": id_, "type": "clip", "duration_s": dur or _dur(lines), "action": action, "camera": camera,
                  "dialogue": [{"speaker": sp, "line": l} for sp, l in lines], "refs": refs, "priority": priority,
                  "night": night, "action_shot": action_shot, "start_frame_prompt": action, "end_frame_prompt": None})


def narr(id_, text):
    SHOTS.append({"id": id_, "type": "narration", "text": text.strip()})


def card(id_, text, seconds):
    SHOTS.append({"id": id_, "type": "title_card", "text": text, "duration_s": seconds})


# =============== COLD OPEN: the stagecoach attack (stops before the outcome) ===============
clip("C01", "A dark-green stagecoach with yellow wheels races flat out along a narrow mountain road, six horses at full gallop, the old driver cracking the reins, dust boiling behind the wheels, the coach rocking on its leather straps.",
     ["PROP_STAGE", "LOC_PASS"], [], camera="low tracking shot alongside the galloping team", action_shot=True)
clip("C02", "Behind the coach, five riders with black bandanas over their faces gallop out of the pines, firing revolvers; gun smoke trails behind them.",
     ["CHAR_BUCK", "LOC_PASS"], [], camera="handheld tracking shot from the back of the coach toward the riders", action_shot=True)
clip("C03", "Inside the bouncing stagecoach a young woman in an ivory lace wedding dress clutches a small iron-banded strongbox to her chest. Across from her an old guard with a white beard and spectacles fires his coach gun out of the window, then turns to her and shouts.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "When I say jump, girl, you jump!")], camera="handheld inside the shaking coach", action_shot=True)
clip("C04", "The coach door flies open. The young woman in the ivory wedding dress leaps out with the strongbox in her arms and tumbles into the sagebrush, the dress and veil billowing; behind her the stagecoach swerves toward the edge of the road.",
     ["CHAR_ROSE", "PROP_BOX", "PROP_STAGE", "LOC_PASS"], [], camera="wide shot, the coach thundering past camera", action_shot=True)
narr("N00", """
Her name was Rose Calloway. She was twenty-four years old. She had never fired a gun, never seen a mountain, and never once seen the face of the man she had come two thousand miles to marry.

Within a week, the whole town of Cedar Bluff would call her a thief.

But the strangest part of this story is not how she ended up jumping from a stagecoach in her wedding dress.

It's what she was holding.
""")
card("T00", "TEN DAYS EARLIER", 3)
card("T01", "THE STAGECOACH BRIDE", 4)

# =============== ACT 1: the bride and the groom (open loops: the box, the watcher, Mercer's proposal) ===============
narr("N01", """
Cedar Bluff, Colorado. September, 1880.

Deputy Marshal Caleb Ward had faced down drunk miners, horse thieves, and a grizzly bear in a root cellar. None of it had prepared him for the problem he had that week. He did not know how to say hello.

For six months, Caleb had written a letter every Sunday to a woman in St. Louis. He had found her name in a matrimonial paper, between an advertisement for a hardware store and a notice about a lost mule. He wrote to her about the mountains, about the aspens turning gold, about a little town with no schoolteacher and no church organ. And every second Sunday, a letter came back.

Rose wrote about her father, a printer who had died the winter before and left her nothing but debts and a box of books. She wrote that she could cook a little, sew a lot, and read handwriting better than any banker. And in her last letter, she wrote that she would arrive on the fourteenth of September, wearing her mother's wedding dress, so that he would see her in it first.

Caleb read that line so many times the paper wore thin.

He had no idea that someone else in Cedar Bluff was counting the days until the fourteenth of September too.

And it was not for love.
""")
img("I01", "Wide establishing view of the small town of Cedar Bluff in a mountain valley in early autumn morning light, golden aspens on the slopes, thin chimney smoke, dirt road winding in.", ["LOC_STREET"], "slow aerial drift forward", reuse="pkg/western_widows_piano_v1/visuals/images/I01.png")
img("I02", "Caleb Ward sitting at the marshal's desk at night writing a letter with a dip pen by lamplight, a small stack of tied letters beside him.", ["CHAR_CALEB", "LOC_JAIL"], "slow push in", night=True)
img("I03", "A narrow room in a St. Louis boarding house: Rose Calloway in a plain dark dress reading a letter by a window, a box of old books on the floor beside her.", ["CHAR_ROSE"], "slow push in")
img("I04", "Close-up: a bundle of letters tied with a faded blue ribbon on a table beside a folded ivory lace wedding dress and a small lace veil.", [], "slow pan across")
clip("C05", "In the marshal's office Caleb stands in front of a small cracked mirror on the wall, nervously straightening his red bandana and rehearsing his greeting with a hopeful, awkward smile.",
     ["CHAR_CALEB", "LOC_JAIL"], [("CHAR_CALEB", "Miss Calloway. Welcome to Cedar Bluff, ma'am.")], camera="medium shot over his shoulder into the mirror")
clip("C06", "Behind him Marshal Abel Hart leans back in his chair with his boots on the desk and speaks without looking up from his newspaper.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Son, she's marrying you, not that mirror.")], camera="medium shot", priority="optional")
clip("C07", "On the boardwalk outside the mercantile Agatha Pell holds her white lace parasol and speaks loudly to two other ladies. They laugh behind their gloves.",
     ["CHAR_AGATHA", "LOC_STREET"], [("CHAR_AGATHA", "A bride by mail. Like a sack of flour from Denver.")], camera="medium shot, slight handheld", priority="optional")
narr("N02", """
Not everyone in Cedar Bluff thought the deputy's romance was sweet. Agatha Pell said a decent woman did not come by mail. Agatha said a great many things.

Out at the Whitmore ranch, the talk was gentler. It had been almost a year since a quiet stranger named John Mercer had bought back Clara Whitmore's piano and saved her land. He had never left. He mended her fences, broke her colts, and every night, after supper, he said good night at the kitchen door and walked out to sleep in the barn.

The whole town was waiting for him to ask her. Clara was waiting too, though she would rather have died than say so.

Before that September was over, he would ask. But first he would be shot at, burned out, and sent down a canyon after five armed men.

And it would all begin with a horse's hoof.
""")
img("I05", "Agatha Pell and two well-dressed ladies whispering on the boardwalk of the main street, glancing sideways, Agatha's lace parasol open.", ["CHAR_AGATHA", "LOC_STREET"], "slow pan right")
img("I06", "The Whitmore ranch in golden afternoon light: Mercer mending a fence rail, Lily sitting on the top rail watching him, Clara on the porch with a basket of laundry.", ["CHAR_MERCER", "CHAR_LILY", "CHAR_CLARA", "LOC_RANCH"], "slow pull out")
img("I07", "Evening: Mercer at the kitchen door with his hat in his hand saying good night, Clara by the stove looking after him, lamplight.", ["CHAR_MERCER", "CHAR_CLARA", "LOC_KITCHEN"], "slow push in", night=True)
clip("C08", "In the kitchen, Lily leans on the table on her elbows and asks her mother the question with mock innocence. Clara, drying a plate, tries not to smile.",
     ["CHAR_LILY", "CHAR_CLARA", "LOC_KITCHEN"], [("CHAR_LILY", "Mama, is Mr. Mercer ever going to ask you?")], camera="medium two-shot", priority="optional")

# =============== ACT 1b: the stagecoach and Silas Crane ===============
narr("N03", """
The stage from Denver came over Raven Pass twice a week. It carried mail, passengers, and once a month, in a small green strongbox, the gold that paid the miners at the Silver King.

For two years, that stage had been robbed. Not every time. Just often enough. Always on the pass. Always by masked riders. And always, somehow, on the one day the gold was aboard.

Nobody could catch them. Nobody could explain how they knew.

Silas Crane had come to Cedar Bluff that spring, after the banker Horace Pike was taken to Denver in irons. He bought Pike's share in the bank, bought cattle from half the ranchers in the valley, and paid for a new roof on the church. He had silver hair, a soft Southern voice, and the finest manners in the valley.

People liked him. People always liked him.

Rose Calloway would be the first person in Cedar Bluff to look at Silas Crane and see exactly what he was. It would very nearly get her killed.
""")
img("I08", "The dark-green stagecoach with yellow wheels climbing the mountain road over Raven Pass, six horses straining, golden aspens and granite peaks behind.", ["PROP_STAGE", "LOC_PASS"], "slow pan right")
img("I09", "Close-up of the small iron-banded green strongbox with a heavy brass padlock, sitting on the floor of the stagecoach.", ["PROP_BOX", "PROP_STAGE"], "slow push in")
img("I10", "An old wanted poster nailed to a post at the way station, weathered and torn, the text illegible, a drawing of masked riders.", ["LOC_STATION"], "slow push in")
img("I11", "Silas Crane in his charcoal suit and cream hat shaking hands with the preacher in front of a small white church, townspeople smiling around them.", ["CHAR_CRANE", "LOC_STREET"], "slow pan left")
img("I12", "Silas Crane on the veranda of his white ranch house, smoking a thin cigar and looking down at his long corrals full of cattle, cold pale eyes.", ["CHAR_CRANE", "LOC_CRANE"], "slow push in")
narr("N03b", """
It had taken Rose eleven days to get that far. A riverboat to Kansas City. Three days on the Kansas Pacific, sitting up all night on a wooden bench with her mother's dress folded in a carpetbag on her knees. Then Denver, loud and muddy and full of men who stared.

The stage was the last of it. Two days over the mountains with a corset salesman, a silent preacher, and an old express guard named Amos Pruitt, who gave her his coat when the wind came through the window and told her stories about the gold camps so she would not be afraid of the drop.

Amos never let a small green box out of his sight. Not once. Not even to eat.

On the last morning, at the way station below the pass, Rose changed into the wedding dress behind a blanket hung from the corral fence. Amos whistled when she came out. The preacher blushed.

None of them noticed the rider in the trees above the station. He watched the old guard lift the green box into the coach. Then he turned his horse and went up the mountain ahead of them.
""")
img("I46", "A crowded Kansas Pacific railroad car at night, Rose sitting upright on a wooden bench, a carpetbag on her knees, oil lamps swaying.", ["CHAR_ROSE"], "slow push in", night=True)
img("I47", "Morning at the lonely way station below the pass: Rose stepping out from behind a blanket hung on the corral fence in her ivory wedding dress, old Amos smiling, the stagecoach waiting.", ["CHAR_ROSE", "CHAR_AMOS", "PROP_STAGE", "LOC_STATION"], "slow pull out")
img("I48", "A lone rider half hidden among the pines on the slope above the way station, watching, then turning his horse uphill.", ["LOC_STATION"], "slow push in")
clip("C09", "Inside the rocking stagecoach Rose, in her ivory wedding dress, holds a bundle of letters in her lap. The old guard Amos, across from her with his coach gun, asks kindly; she answers with a shy smile.",
     ["CHAR_ROSE", "CHAR_AMOS", "PROP_STAGE"], [("CHAR_ROSE", "Six months of letters. And I've never even seen his face.")], camera="medium close-up, gentle rocking of the coach")
clip("C10", "Amos chuckles, pats the small green strongbox at his feet, and looks out of the window at the pass with sudden worry.",
     ["CHAR_AMOS", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "Then he's a lucky man, miss. Lucky as this box.")], camera="medium close-up", priority="optional")

# =============== ACTION 1: the robbery ===============
narr("N04", """
They hit the stage at the top of the pass, just after noon, exactly where the road narrows between the rocks and a sixty-foot drop.

Five riders. Black bandanas. The first shot killed the lead horse. The second took the driver's hat clean off his head.

And the third found Amos Pruitt.
""")
img("I13", "Masked riders bursting out of the pines on both sides of the stage road at full gallop, guns raised, dust and gun smoke.", ["CHAR_BUCK", "LOC_PASS"], "fast push in")
img("I14", "The stagecoach careening at the edge of the road with a sheer drop beside it, horses rearing, the driver hauling on the reins.", ["PROP_STAGE", "LOC_PASS"], "slow push in")
clip("C11", "Inside the coach after the crash, dust drifting through the broken window, old Amos lies wounded against the seat and presses the strongbox and a small brass key into Rose's hands, gripping her wrist.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], [("CHAR_AMOS", "Don't let Crane have it. Whatever they tell you.")], camera="close two-shot inside the tilted coach")
clip("C12", "Rose in her torn ivory wedding dress runs up a rocky hillside through pines and sagebrush, clutching the strongbox, veil streaming, looking back over her shoulder at riders on the road below.",
     ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], [], camera="tracking shot from the side, then from behind", priority="optional", action_shot=True)
narr("N05", """
Rose did not know who Crane was. She did not know what was in the box. She only knew that an old man who had been kind to her for three days was bleeding on the floor of a stagecoach, and that he had asked her for one thing.

So she ran.

She ran in her mother's wedding dress, up a mountain she had never seen, with a box she could not open, while men with guns searched the rocks below and shouted to each other that she could not have gone far.

She hid until dark in a crack between two boulders. When the stars came out, she was still holding the box.

And somewhere below her, in the dark, someone was still looking for it.
""")
img("I15", "Rose hiding between two big granite boulders at dusk, the strongbox in her lap, her lace veil torn and dusty, breathing hard, eyes wide.", ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], "slow push in")
img("I16", "Below on the stage road, Buck Tolliver with his bandana pulled down, the pale scar on his cheek, pointing up the hillside and shouting to his men.", ["CHAR_BUCK", "LOC_PASS"], "slow push in")
img("I17", "Night on the mountainside: a lone small figure in a pale dress sitting among the rocks under a sky full of stars.", ["CHAR_ROSE", "LOC_PASS"], "slow pull out", night=True)

# =============== ACT 2: the search and the rescue ===============
narr("N06", """
The news reached Cedar Bluff at sundown. The stage robbed. The driver alive. The old guard, Amos Pruitt, found at the way station with a bullet in his side, too weak to say a word.

And the bride, gone.

Caleb Ward searched the pass all night with a lantern, calling a name into the dark that he had written forty-nine times and never once said out loud. He found the coach on its side at the edge of the drop, and a scrap of ivory lace on the step. He did not find her.

At dawn the marshal made him come down the mountain to sleep. He did not sleep.

It did not matter. By then, someone else had found her.
""")
img("I18", "Caleb Ward running out of the marshal's office at dusk, buckling his gun belt, the marshal behind him holding a telegram.", ["CHAR_CALEB", "CHAR_MARSHAL", "LOC_JAIL"], "fast push in", night=True)
img("I49", "Night on the mountain pass: Caleb alone with a lantern beside the overturned stagecoach at the edge of a drop, calling into the darkness.", ["CHAR_CALEB", "PROP_STAGE", "LOC_PASS"], "slow push in", night=True)
img("I19", "Mercer kneeling on the mountainside at first light, touching a torn scrap of ivory lace caught on a sagebrush.", ["CHAR_MERCER", "LOC_PASS"], "slow push in")
clip("C13", "Dawn among the boulders. Rose, exhausted and dusty in her torn wedding dress, raises a fist-sized rock to throw. Mercer stands a few steps away, hands open and calm, his dark bay horse behind him.",
     ["CHAR_MERCER", "CHAR_ROSE", "PROP_HORSE", "LOC_PASS"], [("CHAR_MERCER", "Easy, miss. If I meant you harm, you'd know it already.")], camera="over Rose's shoulder onto Mercer")
img("I20", "Mercer leading his dark bay horse down the mountain at sunrise, Rose riding in the saddle in her ruined wedding dress, the strongbox in her arms.", ["CHAR_MERCER", "CHAR_ROSE", "PROP_HORSE", "PROP_BOX", "LOC_PASS"], "slow tracking drift")
img("I21", "The Whitmore ranch at morning: Clara running down the porch steps toward the horse, Lily in the doorway.", ["CHAR_CLARA", "CHAR_LILY", "LOC_RANCH"], "slow push in")
clip("C14", "In the warm kitchen Clara wraps a shawl around Rose's shoulders, sets a cup of coffee in front of her, and speaks firmly, one hand on the young woman's shoulder.",
     ["CHAR_CLARA", "CHAR_ROSE", "LOC_KITCHEN"], [("CHAR_CLARA", "You'll stay here. Nobody touches a woman under my roof.")], camera="medium two-shot, warm lamplight")
narr("N07", """
Rose slept fourteen hours in Clara's bed. When she woke, there was a faded green gingham dress folded on the chair, the smell of bacon, and a little girl sitting at the foot of the bed with a rag doll, staring at her.

"Are you the bride?" Lily asked.

"I was supposed to be," said Rose.

That afternoon they tried to open the box. The brass key from Amos fit the padlock. But inside was a second lock, a small steel one, and no key that any of them had.

Mercer turned the box over in his hands for a long time. Then he shook it gently, next to his ear.

"Gold would rattle," he said.

So what, asked Clara, would five armed men want with a box that doesn't rattle?

Nobody had an answer. But the next day, the man who did came calling.
""")
img("I22", "Rose waking in a small bedroom, a faded green gingham dress folded on a chair, Lily sitting at the foot of the bed with her rag doll, staring with curiosity.", ["CHAR_ROSE", "CHAR_LILY"], "slow push in")
img("I23", "Kitchen table: the open iron-banded strongbox revealing a second small steel lock inside, the brass key on the table, Clara, Rose and Mercer leaning over it.", ["PROP_BOX", "CHAR_CLARA", "CHAR_ROSE", "CHAR_MERCER", "LOC_KITCHEN"], "slow push in")

# =============== ACT 2b: Crane's visit (the clue is planted) ===============
narr("N07b", """
Silas Crane drove up to the Whitmore ranch on Wednesday in his black buggy, with a basket of oranges for the little girl and one of his men waiting on horseback by the gate.

He was so very sorry to hear about the poor bride. Such a terrible thing. He understood she might have something that belonged to his company. A small green box. There would be a reward, of course. Five hundred dollars for its safe return, and no questions asked.

Clara said she had not seen any box.

Crane smiled, and looked for a long time at the barn, and at the porch, and at the window of the room where Rose was hiding. Then he tipped his cream-colored hat and drove away.

"That man," said Clara, when the dust had settled, "just counted my doors."

Mercer did not answer. He had not been watching Crane at all. He had been watching the horse by the gate. A tall roan, with a shoe on the left front hoof that rang wrong on the stones of the yard.

He did not know yet why that mattered.
""")
img("I50", "A fancy black buggy coming up the dirt road to the Whitmore ranch, Silas Crane in his cream hat holding the reins, a basket of oranges on the seat, a rider on a tall roan horse following behind.", ["CHAR_CRANE", "LOC_RANCH"], "slow push in")
img("I51", "Silas Crane on the Whitmore porch, smiling politely, hat in hand, his cold eyes on the house; Clara in the doorway with her arms folded, unsmiling.", ["CHAR_CRANE", "CHAR_CLARA", "LOC_RANCH"], "slow push in")
img("I52", "Rose peeking through a gap in a lace curtain at the buggy in the yard, frightened.", ["CHAR_ROSE"], "slow push in")
img("I53", "Close-up at ground level: the left front hoof of a tall roan horse standing by the ranch gate, a horseshoe with one nail head missing; in soft focus behind, Mercer watching from the barn door.", ["CHAR_MERCER", "LOC_RANCH"], "slow push in")

narr("N07c", """
That night, the dog in the yard went quiet all at once.

Mercer was awake before the barn door creaked. A man in a black bandana was already inside, tearing through the hay with a knife, looking for something small and green.

They went down together in the dark. A lantern smashed. The horses screamed. The man slashed once, caught nothing but Mercer's coat, and was out the back of the barn and onto his horse before Mercer could get up off the floor with his bad leg.

But as the rider crossed the stony yard at a gallop, Mercer heard it again. The same wrong note. A loose shoe, ringing on the left front hoof.

In three days, that sound would save four lives.
""")
img("I59", "Night inside the barn: Mercer grappling with a masked man in a black bandana among scattered hay, a smashed lantern burning on the floor, horses rearing in their stalls, a knife glinting.", ["CHAR_MERCER", "LOC_BARN"], "fast push in", night=True)
img("I60", "Moonlit ranch yard: a masked rider on a tall roan horse galloping away across stony ground toward the road, sparks from the horseshoes, Mercer limping out of the barn door behind him.", ["CHAR_MERCER", "LOC_RANCH"], "slow pan right", night=True)

# =============== ACT 2c: the accusation and the arrest ===============
narr("N08", """
On Thursday morning, Silas Crane walked into the marshal's office with his hat in his hand and a paper in his pocket.

The paper was a bill of lading, signed in his own neat hand. It said the green strongbox belonged to the Crane Cattle and Mining Company, and that it held eleven thousand dollars in gold.

And then, very gently, as if it pained him, Silas Crane told the marshal what everyone in town would be saying by supper.
""")
img("I24", "Silas Crane in his charcoal suit standing at the marshal's desk, placing a folded paper on it with a sorrowful expression, Caleb watching from the window.", ["CHAR_CRANE", "CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], "slow push in")
clip("C15", "In the marshal's office Silas Crane leans lightly on his silver-headed cane and speaks softly, almost sadly, to the marshal.",
     ["CHAR_CRANE", "CHAR_MARSHAL", "LOC_JAIL"], [("CHAR_CRANE", "That box holds my gold, Marshal. And that woman was in on it.")], camera="slow push in on Crane")
clip("C17", "The marshal stands up heavily and puts on his hat. He looks Caleb in the eye and gives the order, not unkindly.",
     ["CHAR_MARSHAL", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_MARSHAL", "Bring her in, Caleb. The law's the law.")], camera="medium two-shot", priority="optional")
narr("N09", """
The marshal gave the warrant to Caleb. Maybe he thought it would be kinder. Maybe he wanted to see what the boy would do.

And if you're still riding with me tonight, tell me in the comments: would you have trusted Rose Calloway, or would you have believed the man with the silver hair?

Caleb rode out to the Whitmore place alone. He had dreamed for six months about the moment he would first see her face.

He had never dreamed it would be with a warrant in his pocket.
""")
img("I25", "Caleb riding alone up the dirt road to the Whitmore ranch, his face grim, a folded warrant visible in his vest pocket.", ["CHAR_CALEB", "LOC_RANCH"], "slow push in")
clip("C18", "Clara steps out onto the porch and raises a double-barreled shotgun at the young deputy as he dismounts at the gate.",
     ["CHAR_CLARA", "LOC_RANCH"], [("CHAR_CLARA", "Not one more step, Deputy.")], camera="low angle from the yard toward the porch")
clip("C19", "Rose, in the faded green gingham dress, comes out beside Clara and gently pushes the shotgun barrels down, her eyes on Caleb.",
     ["CHAR_ROSE", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_ROSE", "It's all right. I'll go.")], camera="medium shot")
img("I26", "Caleb and Rose face to face for the first time at the gate of the ranch, a few feet apart, both silent, golden afternoon light.", ["CHAR_CALEB", "CHAR_ROSE", "LOC_RANCH"], "very slow push in")
narr("N10", """
So that was how they met. Not at the stage stop, with flowers. At a ranch gate, with a shotgun and a warrant.

Caleb took off his hat. Rose looked at him for a long moment, at the freckles on his ears, at the hands that had written forty-nine letters.

"You're taller than I imagined," she said.

"You're... you're under arrest," said Caleb, and wished the ground would open.

It was not how either of them had imagined it. And it was about to get worse.
""")

# =============== ACT 2d: the walk of shame ===============
narr("N10b", """
The jail was at the far end of Main Street. To get there, Caleb had to walk her past every door in Cedar Bluff.

Word had gone ahead of them. The boardwalks were full. Men stopped loading wagons. Women came out of the mercantile with their parcels still in their arms. Somebody said the word thief, and then everybody was saying it.
""")
img("I54", "Main street in the afternoon: Rose in the faded green gingham dress, her wrists in iron handcuffs, walking with her head held high beside Caleb; townspeople crowding the boardwalks, staring and whispering.", ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], "slow tracking drift")
clip("C16", "On the boardwalk Agatha Pell steps forward from the crowd, points her closed lace parasol at the young woman in handcuffs walking past, and speaks loudly so the whole street can hear.",
     ["CHAR_AGATHA", "LOC_STREET"], [("CHAR_AGATHA", "Look at her, ladies. A thief, delivered by mail.")], camera="medium shot, the crowd behind her")
img("I55", "Close-up of Rose's face as she walks: chin up, eyes fixed straight ahead, a single tear on her cheek that she does not wipe away.", ["CHAR_ROSE", "LOC_STREET"], "very slow push in")
narr("N10c", """
Rose Calloway kept her chin up all the way to the jail. She did not look at Agatha Pell. She did not look at anyone.

Only when the cell door closed behind her did she let herself shake.

Caleb saw it. He never forgot it. And he made himself a promise right there, with the key still in his hand.
""")

# =============== ACT 2e: the night in jail ===============
img("I27", "Night: Rose sitting on the narrow cot in the barred cell of the small jail, the green dress, lamplight through the bars.", ["CHAR_ROSE", "LOC_JAIL"], "slow push in", night=True)
clip("C20", "Night in the jail. Caleb sits on a stool outside the cell bars, turning his hat in his hands, and speaks quietly without looking at her.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "I wrote you every Sunday for six months. I meant every word.")], camera="medium close-up through the bars", night=True)
clip("C21", "Rose comes to the bars and holds them, looking straight at Caleb, her voice steady.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_JAIL"], [("CHAR_ROSE", "I didn't steal anything, Caleb.")], camera="close-up through the bars", night=True)
narr("N11", """
He believed her. He could not have said why. Maybe because a thief would have asked for a lawyer, and Rose Calloway asked for a book.

He read to her that night through the bars, from a battered copy of Ivanhoe he kept in the desk drawer. She corrected his pronunciation twice.

Somewhere around midnight she asked him why a man who could write letters like his had needed a matrimonial paper to find a wife. Caleb thought about it for a long while.

"Because out here," he said at last, "nobody ever asked me what I was thinking. You did. Every second Sunday."

Rose did not say anything. But she put her hand through the bars, and he held it, and neither of them let go.

At two in the morning, the window of the marshal's office exploded.
""")

# =============== ACTION 2: the night raid on the jail ===============
clip("C22", "Night. A burning torch smashes through the window of the marshal's office and lands on the floor, flames racing across spilled lamp oil; through the broken window masked riders fire revolvers.",
     ["CHAR_BUCK", "LOC_JAIL"], [], camera="static wide shot inside the office", night=True, action_shot=True)
clip("C23", "In the smoke-filled jail Caleb throws himself in front of the cell bars, revolver up, shouting over his shoulder to Rose; a bullet hits his left shoulder and he staggers but keeps firing at the window.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], [("CHAR_CALEB", "Stay behind me, Rose!")], camera="handheld medium shot, smoke and muzzle flashes", night=True, action_shot=True)
clip("C24", "The jail door is kicked open; Mercer storms in through the smoke with a rifle, firing at the window, then grabs the keys from the desk.",
     ["CHAR_MERCER", "LOC_JAIL"], [], camera="low angle from the floor", night=True, priority="optional", action_shot=True)
narr("N12", """
They wanted the box. They thought it was in the jail. It was not. It was under a loose board in Clara Whitmore's kitchen.

Mercer had been watching the jail since midnight. Something about that roan horse had kept him awake. He got there in time to drag Caleb out of the smoke, and to unlock a cell door with a ring of keys too hot to hold.

By sunrise, the marshal's office was a black shell. Caleb had a bullet hole in his shoulder and a girl's hand in his.

And in the ashes by the hitching rail, John Mercer found a horseshoe, thrown in the night by one of the raiders' horses.

One nail on the left side was snapped off short.
""")
img("I28", "Dawn: the burned-out marshal's office smoking, townspeople with water buckets, Caleb sitting on the boardwalk with his shoulder bandaged, Rose kneeling beside him holding his hand.", ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], "slow pull out")
img("I29", "Close-up: a worn horseshoe in Mercer's weathered palm, one nail on the left side snapped off short and bent, ash on his fingers.", ["CHAR_MERCER"], "slow push in")

# =============== ACT 3: the proof ===============
clip("C25", "On the dusty road Mercer holds up the horseshoe and speaks to Caleb, who stands with his arm in a sling. Mercer's face is grim and certain.",
     ["CHAR_MERCER", "CHAR_CALEB", "LOC_STREET"], [("CHAR_MERCER", "Broken nail, left fore. That horse stood at Clara's gate.")], camera="low angle close on the horseshoe, then up to Mercer")
narr("N13", """
The tall roan with the broken nail belonged to a man named Buck Tolliver. Buck was Silas Crane's foreman.

But a horseshoe was not proof. Not against the most respected man in the valley. They needed what was in the box.

That night, at the Whitmore kitchen table, Rose Calloway asked Clara for a hairpin.

The men looked at each other. Clara handed it over. And the bride who came by mail bent over the steel lock, listened, turned the pin twice, and opened it in less than a minute. Her father had printed handbills for every locksmith in St. Louis. He had believed that a girl should know how things work.

Inside there was no gold at all. There was a stack of letters, tied with string, in a fine, slanting hand.
""")
img("I30", "Mercer and Caleb on horseback on a rise at dusk, looking down at a large white ranch house with a red barn and corrals, a tall roan horse among the horses at the rail.", ["CHAR_MERCER", "CHAR_CALEB", "LOC_CRANE"], "slow push in")
img("I31", "Night, the Whitmore kitchen: Rose bent over the strongbox picking the small steel lock with a hairpin, Clara holding the lamp close, Mercer and Caleb watching in astonishment.", ["CHAR_ROSE", "CHAR_CLARA", "CHAR_MERCER", "CHAR_CALEB", "PROP_BOX", "LOC_KITCHEN"], "slow push in", night=True)
img("I32", "Close-up: inside the open strongbox, a thick stack of old letters tied with string, the handwriting not legible.", ["PROP_BOX"], "slow push in", night=True)
clip("C26", "Clara reads one of the letters by lamplight; her face goes pale. She looks up at the others across the kitchen table.",
     ["CHAR_CLARA", "LOC_KITCHEN"], [("CHAR_CLARA", "Every gold shipment date, for two years.")], camera="slow push in on Clara", night=True, priority="optional")
narr("N14", """
The letters were unsigned. Every one of them. Shipment dates, hours, which stage, which guard. Somebody in Denver had been selling the gold schedule for two years, and somebody in Cedar Bluff had been buying it.

Unsigned letters prove nothing, said the marshal.

Rose asked him for one thing. The bill of lading Crane had left on his desk, the one that called her a thief.

She laid it on the table next to the letters, under the lamp, and she showed them. The tall, leaning capitals. The little hook on every letter C. The way the writer crossed his T's twice, like a man who never trusts a thing to stay done.

"My father set type for thirty years," Rose said. "He taught me that a man can change his name. He can't change his hand."

The same man had written both. Silas Crane had signed his own confession and handed it to the law.

For the first time, they had proof.

And up in his white house on the hill, Silas Crane already knew it.
""")
img("I56", "Close-up on the kitchen table under an oil lamp: a printed bill of lading and an old handwritten letter side by side, Rose's finger pointing at matching curved capital letters; the words themselves are not legible.", ["CHAR_ROSE", "LOC_KITCHEN"], "slow push in", night=True)
img("I33", "A nervous clerk in a Denver express office at night, sliding a bundle of letters across a counter to old Amos Pruitt, lamplight.", ["CHAR_AMOS"], "slow push in", night=True)

# =============== ACTION 3: the chase in Red Canyon ===============
narr("N15", """
Crane was not a patient man. When the marshal rode out to his ranch at dawn with a warrant, the white house was empty, the safe was open, and six of the best horses were gone.

Mercer read the ground for less than a minute. Red Canyon, he said. The old trail south to New Mexico.

Caleb rode with his arm in a sling. Nobody could talk him out of it.

Rose watched them go from the porch with the box in her lap. Clara stood beside her with the shotgun.

Neither of them knew that the trail south was a lie.
""")
img("I34", "Crane's empty office in the white ranch house, the iron safe door hanging open, papers scattered on the floor, a cream-colored hat left on the desk.", ["LOC_CRANE"], "slow push in")
clip("C27", "Five riders gallop flat out through a narrow red sandstone canyon, Silas Crane in his cream hat in the middle, dust and pebbles flying; far behind, two riders chase them.",
     ["CHAR_CRANE", "CHAR_BUCK", "LOC_CANYON"], [], camera="low wide shot, riders racing past camera", action_shot=True)
clip("C28", "Rifle shots crack from the canyon rim. Mercer leaps from his horse and drags Caleb down behind a big boulder as bullets kick up dust and splinter the rock beside them.",
     ["CHAR_MERCER", "CHAR_CALEB", "LOC_CANYON"], [], camera="handheld, low behind the boulder", priority="optional", action_shot=True)
img("I35", "Mercer and Caleb crouched behind a boulder in the red canyon, rifles raised, gun smoke drifting, dust in the air.", ["CHAR_MERCER", "CHAR_CALEB", "LOC_CANYON"], "slow push in")
img("I36", "Buck Tolliver on the canyon rim, bandana down, aiming a rifle into the canyon, the sun behind him.", ["CHAR_BUCK", "LOC_CANYON"], "slow push in")
narr("N16", """
Buck Tolliver had picked the place well. High rock, sun at his back, two men pinned in a dry creek bed with nowhere to go.

What Buck did not know was that the Union cavalry had taught John Mercer one thing above all others. When a man holds the high ground, you do not go up. You go around.

It took Mercer forty minutes to climb the back of the canyon wall with a bad leg. It took him four seconds to put Buck Tolliver on his face in the dirt.

"Where's Crane?" Mercer asked.

Buck spat blood and laughed. "Ask the bride."

The riders in the canyon had been a decoy. Silas Crane had never gone south at all.

He had gone back to Cedar Bluff. Back to the one thing he still needed.
""")
img("I37", "Mercer climbing a steep red rock wall from behind, rifle slung over his back, sweat on his face.", ["CHAR_MERCER", "LOC_CANYON"], "slow tilt up")
img("I38", "Buck Tolliver face down in the red dust on the canyon rim, his rifle kicked away, Mercer standing over him.", ["CHAR_MERCER", "CHAR_BUCK", "LOC_CANYON"], "slow push in")
img("I57", "Mercer and Caleb galloping flat out back along a dirt road toward a distant small town, dust behind them, desperate faces.", ["CHAR_MERCER", "CHAR_CALEB", "PROP_HORSE"], "fast push in")

# =============== ACTION 4: the showdown on Main Street ===============
narr("N17", """
Crane came into Cedar Bluff at noon, by the back way, with two men and a derringer in his sleeve. As long as those letters existed, he would hang. And he knew exactly where they were.

Clara had gone to town for the doctor. Lily was at the schoolhouse.

Rose Calloway was alone in the kitchen, and she was holding the box.
""")
img("I39", "Silas Crane walking slowly into the Whitmore kitchen through the open door, cream hat, cane in one hand, a small derringer half hidden in the other.", ["CHAR_CRANE", "LOC_KITCHEN"], "slow push in")
clip("C29", "In the kitchen Crane stops across the table from Rose, smiling coldly, the small derringer pointed at her, and holds out his free hand for the strongbox she is clutching.",
     ["CHAR_CRANE", "CHAR_ROSE", "PROP_BOX", "LOC_KITCHEN"], [("CHAR_CRANE", "The box, Miss Calloway. And then we'll take a little ride.")], camera="slow push in on Crane over Rose's shoulder")
narr("N17b", """
He needed a hostage to get out of the valley, and a bride was the best hostage of all.

He walked her down Main Street at noon with the derringer against her ribs and the box in her arms, past the same boardwalks where the town had called her a thief three days before.

Nobody said a word now.

And at the end of the street, in front of the burned-out jail, a young deputy with one arm in a sling stepped off his lathered horse and into the middle of the road.
""")
img("I40", "Main street at noon, deserted, Silas Crane pushing Rose ahead of him toward a saddled horse, the strongbox in her arms, townspeople watching silently from doorways.", ["CHAR_CRANE", "CHAR_ROSE", "PROP_BOX", "LOC_STREET"], "slow push in")
clip("C30", "On the dusty main street at high noon Caleb steps out into the middle of the road, his left arm in a sling, his right hand by his revolver, facing Crane and two of his men. The townspeople pull back into the doorways.",
     ["CHAR_CALEB", "CHAR_CRANE", "LOC_STREET"], [], camera="low wide shot down the empty street", action_shot=True)
clip("C31", "Rose suddenly swings the heavy iron-banded strongbox with both hands into Crane's wrist; the small derringer flies out of his hand and spins into the dust.",
     ["CHAR_ROSE", "CHAR_CRANE", "PROP_BOX", "LOC_STREET"], [], camera="close-up, slow motion feel", action_shot=True, dur=4)
narr("N18", """
Caleb never had to draw. From the rooftop of the livery, John Mercer's rifle had been on Crane's two men since the moment they turned into Main Street, and they knew it.

Afterwards, half the town claimed to have seen the whole thing, and the story grew a little every time it was told.

But the truth was simple. Silas Crane had spent his whole life underestimating people. Ranchers. Old guards. Shy deputies.

And a bride who came by mail.
""")
clip("C32", "The marshal snaps handcuffs on Silas Crane in the middle of the main street. Crane's cream hat lies in the dust beside the derringer.",
     ["CHAR_MARSHAL", "CHAR_CRANE", "LOC_STREET"], [("CHAR_MARSHAL", "Silas Crane. You're under arrest for robbing the mail.")], camera="medium two-shot", priority="optional")
img("I58", "Mercer on the flat roof of the livery stable, kneeling with a rifle aimed down at the main street, calm and steady.", ["CHAR_MERCER", "LOC_STREET"], "slow push in")
img("I41", "The marshal leading a handcuffed Silas Crane down the main street, Crane bareheaded, his silver hair disordered, the townspeople silent on the boardwalks.", ["CHAR_MARSHAL", "CHAR_CRANE", "LOC_STREET"], "slow tracking drift")
img("I42", "Agatha Pell on the boardwalk, her parasol lowered, her mouth open in shock.", ["CHAR_AGATHA", "LOC_STREET"], "slow push in")

# =============== FINALE ===============
narr("N19", """
Amos Pruitt lived. He testified in Denver in November with his arm in a sling and his spectacles mended with wire, and in front of the whole courtroom he shook the bride's hand.

Silas Crane went to the penitentiary at Cañon City. Buck Tolliver went with him.

And on a golden Sunday afternoon in Cedar Bluff, on the same street where the whole town had called her a thief, Deputy Caleb Ward got down on one knee in the dirt.
""")
clip("C33", "On the sunny main street, Caleb, his arm still in a sling, kneels on one knee in the dust in front of Rose and holds up a small plain ring. Townspeople gather around smiling.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], [("CHAR_CALEB", "Rose Calloway. Will you marry me? Properly, this time.")], camera="slow push in on Caleb")
clip("C34", "Rose laughs through her tears, pulls Caleb to his feet and answers him. The crowd behind them cheers and throws hats in the air.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], [("CHAR_ROSE", "I came a thousand miles to say yes.")], camera="medium close-up, then the crowd")
img("I43", "Agatha Pell, stiff and red-faced, shaking Rose's hand on the boardwalk while the townspeople watch, Rose smiling graciously.", ["CHAR_AGATHA", "CHAR_ROSE", "LOC_STREET"], "slow push in")
narr("N20", """
Even Agatha Pell came to shake the bride's hand. It was said to be the first apology she had made since the war, and very possibly the last.

But the best moment of that day happened later, at sunset, and almost nobody saw it.
""")
clip("C35", "Evening at the Whitmore ranch. On the porch, Mercer stands before Clara with his hat in his hands, nervous for the first time in his life.",
     ["CHAR_MERCER", "CHAR_CLARA", "LOC_RANCH"], [("CHAR_MERCER", "Clara... I reckon I've slept in that barn long enough.")], camera="medium two-shot, sunset light")
clip("C36", "Clara looks at him for a long moment, then smiles and answers softly. In the window behind them, Lily grins.",
     ["CHAR_CLARA", "CHAR_MERCER", "CHAR_LILY", "LOC_RANCH"], [("CHAR_CLARA", "About time, John Mercer.")], camera="close-up on Clara, Lily in soft focus behind")
narr("N21", """
They were married in October, when the aspens turned gold, in the little white church at the end of Main Street. Caleb and Rose stood up for them. And the following spring, it was their turn.

Thank you for riding along to Cedar Bluff tonight. If this story warmed your heart, tell me in the comments where you're watching from, and subscribe, because there are more stories waiting in this little town.

Until next time, keep a light in the window.
""")
img("I44", "Golden sunset over the Whitmore ranch, warm light in every window, two couples on the porch: Clara and Mercer, Rose and Caleb, Lily on the steps.", ["CHAR_CLARA", "CHAR_MERCER", "CHAR_ROSE", "CHAR_CALEB", "CHAR_LILY", "LOC_RANCH"], "slow pull out")
img("I45", "The valley at night under a sky full of stars, a single warm window glowing far below.", ["LOC_RANCH"], "slow pull out", night=True, reuse="pkg/western_widows_piano_v1/visuals/images/I69.png")
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


clips = [s for s in SHOTS if s["type"] == "clip"]
images = [s for s in SHOTS if s["type"] == "image"]
narrs = [s for s in SHOTS if s["type"] == "narration"]
words = sum(wc(n["text"]) for n in narrs)
WPM = 140
core = [c for c in clips if c["priority"] == "core"]
est = {"clips": len(clips), "clips_core": len(core), "clips_optional": len(clips) - len(core),
       "images_new": sum("reuse_from" not in i for i in images), "images_reused": sum("reuse_from" in i for i in images),
       "narration_words": words, "narration_chars": sum(len(n["text"]) for n in narrs), "narration_min": round(words / WPM, 1),
       "clip_min_core": round(sum(c["duration_s"] for c in core) / 60, 1), "clip_min_all": round(sum(c["duration_s"] for c in clips) / 60, 1),
       "credits_core_one_take": sum(PRICE[c["duration_s"]] for c in core), "credits_optional_one_take": sum(PRICE[c["duration_s"]] for c in clips if c["priority"] != "core"),
       "credits_hooks": sum(PRICE[h["duration_s"]] for h in HOOKS),
       "est_total_min_core": round(words / WPM + sum(c["duration_s"] for c in core) / 60 + 0.5, 1)}


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


_switch = next(i for i, x in enumerate(SHOTS) if x["id"] == "I20")
for i, s in enumerate(SHOTS):
    b = i > _switch
    if "CHAR_ROSE" in s.get("refs", []):
        s["rose_outfit"] = ("her plain dark-gray travelling dress and a small black hat (not the wedding dress yet)" if s["id"] in ("I03", "I46")
                            else "B: faded green gingham dress, low bun" if b else "A: ivory lace wedding dress")
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

for h in HOOKS:
    h["first_frame_full_prompt"] = h["first_frame"] + " " + STYLE.replace("16:9 widescreen", "9:16 vertical") + " Characters/places: " + ref_text(h["refs"])
    h["video_prompt"] = h["video"] + ACTION + " " + CLIP_STYLE.replace("16:9", "9:16 vertical")
    h["ref_files"] = ref_files(h["refs"], h["id"] != "H01")
    h["credits"] = PRICE[h["duration_s"]]
    h["files"] = {"start_frame": f"visuals/hooks/{h['id']}_first.png", "video": f"visuals/hooks/{h['id']}.mp4"}

TITLE = "The Stagecoach Bride"
YT = "They Called the Mail-Order Bride a Thief and Made Her Groom Arrest Her — They Didn't Know What Was in Her Box"
out = {"title": TITLE, "series": "Tales of Cedar Bluff", "episode": 2, "working_title_youtube": YT,
       "setting": "Cedar Bluff, Colorado (a state since 1876), September 1880, golden aspens",
       "format": {"aspect": "16:9 (hooks 9:16)", "video_model": "Omni 1.1 Flash 720p", "image_model": "Nano Banana Pro", "fps": 24,
                  "clip_durations_allowed_s": [4, 6, 8], "credits_by_duration": {"4": 7, "6": 10, "8": 12}},
       "estimate": est, "style": STYLE, "clip_style": CLIP_STYLE, "reused_refs_from": PREV,
       "characters": CHARACTERS, "props": PROPS, "locations": LOCATIONS, "timeline": SHOTS, "hooks": HOOKS}

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{here}/narration", exist_ok=True)
json.dump(out, open(f"{here}/shotlist.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for n in narrs:
    open(f"{here}/narration/{n['id']}.txt", "w", encoding="utf-8").write(n["text"] + "\n")

L = [f"# {TITLE.upper()}\n", f"*Tales of Cedar Bluff, фильм 2 · {YT}*\n",
     f"Оценка: ~{est['est_total_min_core']} мин (только обязательные клипы) · клипов {est['clips']} (обязательных {est['clips_core']} ≈ {est['credits_core_one_take']} кредитов за один дубль, по желанию {est['clips_optional']} ≈ {est['credits_optional_one_take']}) · хуки для шортсов 3 ≈ {est['credits_hooks']} · картинок новых {est['images_new']}, из первого фильма {est['images_reused']} · рассказчик {words} слов, {est['narration_chars']} символов (~{est['narration_min']} мин)\n",
     "Обозначения: **C** — видеоклип 4–8 с, говорит один персонаж · **I** — картинка с движением камеры под голос рассказчика · **N** — рассказчик · **T** — титр · ⚡ — экшен-клип.\n"]
for s in SHOTS:
    if s["type"] == "clip":
        tag = "" if s["priority"] == "core" else " *(по желанию)*"
        L.append(f"\n**{s['id']} · КЛИП {s['duration_s']} с{' ⚡' if s['action_shot'] else ''}**{tag} — {s['action']}" + (f"  \n_Камера: {s['camera']}_" if s['camera'] else ""))
        for d in s["dialogue"]:
            L.append(f"> **{CHARACTERS[d['speaker']]['name'].upper()}:** {d['line']}")
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
