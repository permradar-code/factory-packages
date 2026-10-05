# Task for Claude Code: 3 hook clips for Shorts — "The Widow's Piano"

**Project:** `western_widows_piano_v1` (Tales of Cedar Bluff).
**Talk to the user in Russian.**
**Why:** Shorts cut from the film have weak first frames (people standing and talking). 72% of viewers swiped away the first auction Short. Each Short needs a first frame where one concrete, loud action is already happening and is readable in half a second with the sound off. These three clips are made only for that. They will open Shorts; the rest of each Short is cut from the finished film.

## Where things are
- Repo `permradar-code/factory-packages`, branch `tools/montage` → `briefs/western_widows_piano/`: `shotlist.json` (characters, props, locations, exact looks), `BRIEF.md` (Flow rules).
- Existing refs and sources: branch `pkg/western_widows_piano_v1` → `visuals/refs/`.
- **Deliver into the same branch** `pkg/western_widows_piano_v1`, new folder `visuals/hooks/`: `H01_first.png`, `H01.mp4`, `H02_first.png`, `H02.mp4`, `H03_first.png`, `H03.mp4`. One commit "hooks". Add a `"hooks"` section to `manifest.json` (file, duration, aspect, credits, takes, note) and a short block to README.md.

## Format
- **Aspect: 9:16 vertical if Flow offers it for Omni 1.1 Flash** (first frame also 9:16). If only 16:9 is available, make 16:9 and **compose so that all action stays inside the central third of the frame** (it will be cropped to 9:16). Write in the manifest which one you used.
- Omni 1.1 Flash, 720p, 24 fps. First frames in Flow images (Nano Banana Pro) with references from `visuals/refs/`.
- **The action must start within the first 0.3 s of the clip.** No slow build-up, no establishing shot. The first frame of the video already shows motion beginning.
- Era lock in every prompt: Colorado, 1879, period clothing and objects. **Write "Colorado, 1879", never "Colorado Territory"** (Colorado has been a state since 1876; the old `style` string in shotlist.json still says Territory, do not copy that word).
- No text, no logos, no watermark, no modern objects, no music. Natural sound effects are welcome (thud, coins, fire, gunshot, horses).
- Faces: original fictional characters, never a celebrity lookalike. Do not work around the celebrity filter; if it triggers, change the face, not the filter.
- Flow pacing as in BRIEF.md: one request at a time, x1, pause 30–60 s, log every request with time. Check the credit balance before every video.

## The three hooks

### H01 — Gold on the auction table (4 s, 7 credits)
- **Refs:** CHAR_MERCER (hand and sleeve only), CHAR_DEKE (out of focus), LOC_PLATFORM.
- **First frame prompt:** Extreme close-up on a rough wooden auction table on a flatbed wagon, an open ledger and a wooden gavel on it. A man's weathered, tanned hand in the sleeve of a long dark-brown canvas duster coat is high above the table, gripping a heavy, bulging leather drawstring coin pouch, about to slam it down. In the soft-focus background: a skinny auctioneer in a yellow-and-brown checkered vest and brown bowler hat, mouth open in shock. Golden aspens and a brick bank front far behind. Photorealistic cinematic film still, Colorado, 1879, autumn, natural light, 35mm film grain, shallow depth of field. No text, no logos, no modern objects.
- **Video prompt:** At once the hand slams the heavy leather pouch onto the table with a loud thud; the drawstring bursts open and gold coins spill out, bouncing and rolling across the ledger and off the table edge, one coin spinning on its rim in the foreground. The auctioneer behind flinches and freezes, gavel raised. Camera: static extreme close-up, very slight push in. No dialogue, nobody speaks. Sound: heavy thud, ringing coins. Cinematic live-action western drama, photorealistic, Colorado, 1879, natural light, film grain. No subtitles, no text on screen, no music.
- **Reject if:** coins look like modern money or have readable text; the hand has extra fingers; the pouch appears from nowhere instead of being slammed down.

### H02 — Torch into the barn (4 s, 7 credits)
- **Refs:** LOC_BARN, PROP_HORSE.
- **First frame prompt:** Night. Inside the doorway of a small wooden barn with hay bales and a stall with a tall dark bay horse with a white blaze. A burning torch is flying through the air into the frame, already halfway to a stack of dry hay, sparks trailing behind it. Moonlight through the doorway, orange torch light on the hay. Photorealistic cinematic film still, Colorado, 1879, 35mm film grain. No text, no logos, no modern objects.
- **Video prompt:** At once the torch lands in the hay and the dry hay bursts into tall flames that race up the barn wall; the dark bay horse in the stall rears and screams; sparks and smoke fill the air. Camera: static medium shot from inside the barn, flames growing toward camera. No dialogue, nobody speaks. Sound: whoosh of fire, crackling, horse whinny. Cinematic live-action western drama, photorealistic, Colorado, 1879, night, film grain. No subtitles, no text on screen, no music.
- **Reject if:** the fire looks like CGI cartoon flames; the horse morphs; a person appears in frame.

### H03 — Clara's warning shot (6 s, 10 credits)
- **Refs:** CHAR_CLARA (front, full), LOC_RANCH. Keep Clara exactly as in the film: chestnut hair with copper highlights in a braided crown, faded dark-blue calico dress, dark shawl over her shoulders, small silver locket.
- **First frame prompt:** Night, on the covered porch of a small log ranch house. Close medium shot of Clara Whitmore, 26, pretty frontier widow, braided chestnut-copper hair, dark shawl over a faded dark-blue calico dress, holding an old double-barrel shotgun raised high, barrels pointed up into the night sky, her face fierce and determined, lit by the orange glow of a burning barn behind the camera. In the background beyond the porch rail, two dark horses rearing in the smoke. Photorealistic cinematic film still, Colorado, 1879, 35mm film grain. No text, no logos, no modern objects.
- **Video prompt:** Immediately Clara fires the shotgun into the air: a huge muzzle flash lights her face, the gun kicks back against her shoulder, smoke drifts. She lowers the barrels toward the yard and says the line. Camera: static close medium shot, slight shake on the shot. Dialogue: Clara Whitmore (warm, low, steady American woman's voice, late twenties, a little weary, never shrill — here hard and angry) says: "The next one goes lower!" ONLY Clara speaks. The shot is fired in the first half second; the line starts right after the shot; after the line she holds the aim, no extra words. Cinematic live-action western drama, photorealistic, Colorado, 1879, night, film grain. Keep Clara's face, hair and clothing exactly as in the start frame and references for the whole shot. She only speaks the exact line given, in English, with lips in sync. No subtitles, no text on screen, no music.
- **Reject if:** her face changes; the line is changed or extended; the gun looks modern; no visible muzzle flash.

## Limits
- One take each first; **max 2 regenerations per hook**. Budget: about 24 credits for one take of all three, at most ~72 with regenerations. If the balance would fall under **150** credits, stop and ask.
- Order: H01, H03, H02 (H01 and H03 matter most).
- **When done:** push, then tell the user in Russian which hooks worked, which aspect was used, credits spent, and the balance left.
