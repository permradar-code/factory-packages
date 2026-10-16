# Film 4 «The Widow's Rifle» + 4 Shorts — upload by API (ready to send, 16 Oct 2026)

For a new chat: read this file, `FACTORY_GUIDE.md` and `montage/western_widows_rifle/youtube_metadata.md`.
**Upload nothing until the owner writes «ок» / «загружаем».** Talk to the owner in Russian, simply.

## 0. Rules (do not break)
- Every upload is first `dry_run=true` → show the owner title, privacy and time → the real send only after «ок».
- Upload as `privacy="private"` (Studio: «Ограниченный доступ»). Going public / `publish_at` only with the owner's «ок».
  The owner wants to open the film after monetization is approved (YPP review is pending since ~13 Oct).
- The A/B test (title + thumbnail) is started by hand in Studio. While it runs, never change title or thumbnail
  (`confirm_title_change` stays false).
- Profile `new_channel` = Tales of Cedar Bluff (`UCRaldWksRYLzA_Xx_zUKqOg`). Playlist «Tales of Cedar Bluff — Full Western Stories» = `PLKIIpibv0c7c`.
- Quota: film with captions+thumbnail+playlist = 2,100 units, each Short = 1,600, a comment = 50; a day has 10,000
  (resets at 10:00 MSK). All five fit in one day (8,550) if nothing else used the quota — check `youtube_quota_status` first.
- Dry runs of the film and of Short 1 with these exact paths passed on 16 Oct (file sizes, 1280x720 thumbnail, quota OK).
- Keys are never printed, written or asked for. Banned in titles/thumbnails/first 30 s: thief, order/ordered, mail-order, arrest/handcuffs/jail.

## 1. Files on the server (`/opt/moiastro-engine/projects/western_widows_rifle_v1/`)
| What | Path |
|---|---|
| Film (13:47, 1080p, −14 LUFS) | `render/long.mp4` |
| English captions (188 cues) | `subtitles/long.srt` |
| Thumbnail A (main) | `thumbnails/a_not_alone.jpg` |
| Thumbnails B, C (A/B test, set by hand in Studio) | `thumbnails/b_forty_cents.jpg`, `thumbnails/c_one_shot.jpg` |
| Short 1 «Torches» (30.7 s) | `render/shorts/s4_torches_h04.mp4` |
| Short 2 «Bank» (32.4 s) | `render/shorts/s4_bank_h06.mp4` |
| Short 3 «Forty cents» (33.2 s) | `render/shorts/s4_forty_cents_h01.mp4` |
| Short 4 «Proposal» (32.7 s) | `render/shorts/s4_final_proposal.mp4` |

Owner downloads (SSH tunnel to localhost:8788): film preview `http://localhost:8788/api/montage/western_widows_rifle_v1/outputs/long/preview`,
captions `.../outputs/long/subtitles`, thumbnails `.../thumbnails/<name>.jpg`. Shorts have no Studio link yet:
`scp root@<server>:/opt/moiastro-engine/projects/western_widows_rifle_v1/render/shorts/s4_*.mp4 .`

**Use `file_path`, not `project_id`**, for the film: its factory QC is FAIL only because of `no_still_held_too_long`
(long stills under the narrator — accepted by the owner), so `project_id` would be refused.

## 2. Order
1. `youtube_quota_status()`.
2. Film: `youtube_publish_video(... dry_run=true)` with section 3 → show the owner → «ок» → same call without dry_run.
   Poll `youtube_upload_status(job_id)` until the video_id; captions, thumbnail and playlist are steps of the same job.
3. Put the film's video_id into the Shorts descriptions (replace `<FILM4_ID>`).
4. Shorts: dry_run → «ок» → upload private, one by one (section 4). Order of release (when the owner opens them):
   Torches 1–2 days after the film goes public, then one a day: Bank → Forty cents → Proposal.
5. Pinned comment on the film: `youtube_comment_post(video_id, text, dry_run=true)` → «ок» → send; pin by hand in Studio.
6. Manual steps in Studio (the API cannot) — give the owner this list:
   - Test & compare: 3 pairs (section 3.1), A is already on the video;
   - End screen: Subscribe + video «May We Sleep in Your Barn?» (55FeA5seYsA); after release also add film 4 to film 3's end screen;
   - Pin the comment;
   - For each Short: «Related video» = film 4;
   - Check «Altered or synthetic content = Yes» (the tool sends it, verify).

## 3. Film 4 — metadata

### 3.1 Title / thumbnail pairs (A goes in the upload, B and C go into Test & compare by hand)
| Pair | Title | Thumbnail |
|---|---|---|
| A (upload) | The Banker Came for the Widow's Farm — Unaware the Stranger Owned His Bank \| Full Western Movie | `a_not_alone.jpg` |
| B | "Forty Cents Short, Ma'am?" The Town Laughed — The Stranger Behind Her Didn't \| Full Western Movie | `b_forty_cents.jpg` |
| C | The Whole Town Came to Watch the Widow Lose — Then She Picked Up Her Rifle \| Full Western Movie | `c_one_shot.jpg` |

### 3.2 Call
```
youtube_publish_video(
  file_path="/opt/moiastro-engine/projects/western_widows_rifle_v1/render/long.mp4",
  kind="long",
  title="The Banker Came for the Widow's Farm — Unaware the Stranger Owned His Bank | Full Western Movie",
  description=<3.3>,
  tags=<3.4>,
  subtitles_srt="/opt/moiastro-engine/projects/western_widows_rifle_v1/subtitles/long.srt",
  thumbnail="/opt/moiastro-engine/projects/western_widows_rifle_v1/thumbnails/a_not_alone.jpg",
  playlist_id="PLKIIpibv0c7c",
  category_id="1", language="en", default_audio_language="en",
  contains_synthetic_media=true, made_for_kids=false,
  privacy="private", dry_run=true)
```

### 3.3 Description
```
Hannah Cole had until noon Saturday to pay a $250 note — and only $1.60 to her name. So the widow carried her father's old buffalo rifle to the Cedar Bluff fair, where the whole town came to watch her lose.

Nobody paid any attention to the quiet stranger standing behind her in line. He paid her forty cents without a word… and he knew something about the Cedar Bluff Savings Bank that nobody else did.

Would you have stood beside her? Tell us where you're watching from tonight 👇

⏱ Chapters
0:00 "Forty cents, ma'am"
1:02 The county fair rifle match
1:33 The note at the bank
2:00 Her father's buffalo rifle
2:25 A bent front sight
2:56 Nobody knew Jonah Reed
3:20 "Frighten her. Nothing more."
3:50 The railroad map
4:27 Fifty cents for the barn
5:44 Tom's nails
6:13 The best rifle in Colorado
7:08 Torches at midnight
7:48 A night on the porch
8:22 Nobody stood next to her
9:12 Six hundred yards
9:55 The shot they argued about for years
10:19 "Your clock is four minutes fast"
11:28 What became of Ambrose Hale
11:50 A sign over the teller's window
12:20 "Marry me"
12:52 Eleven years later
13:23 Keep a light in the window

▶ Watch next: "May We Sleep in Your Barn?" — https://youtu.be/55FeA5seYsA
🔔 A new tale from Cedar Bluff, Colorado, every week — subscribe: https://www.youtube.com/@TalesofCedarBluff?sub_confirmation=1

All characters and events are fictional. Created with the help of AI.

#WesternMovie #OldWest #WesternStory #CowboyStory #FrontierLove

ABOUT THE PRODUCTION

This is an original fictional Western developed for Tales of Cedar Bluff. Hannah Cole's last chance at the county fair rifle match, the quiet stranger who paid her forty cents, and the secret behind the Cedar Bluff Savings Bank were shaped into a complete screenplay. Story development, creative direction, scene planning, shot selection, editing, music and sound design are part of our production process. Cinematic visuals and character voices are created with the assistance of generative AI. All characters and events are fictional.
```

### 3.4 Tags
```
["full western movie", "western movie", "western movies full length", "free western movies", "full movie", "cowboy movie", "cowboy stories", "western stories", "old west story", "frontier story", "western romance", "widow story", "shooting match", "hidden owner", "secret millionaire", "quiet stranger", "Tales of Cedar Bluff", "Cedar Bluff"]
```

### 3.5 Pinned comment
```
Forty cents short — and a stranger paid it without a word. Would you have done the same? 🤠 Tell us where you're watching from tonight 👇
```

### 3.6 Release
~16:00 MSK (9:00 ET), Thu–Sat (film 3: Thu 15:54 MSK → 277k in 48 h) — only when the owner says so.

## 4. Shorts — metadata
Same for all four: `kind="short"`, `privacy="private"`, `category_id="1"`, `language="en"`, `default_audio_language="en"`,
`contains_synthetic_media=true`, `made_for_kids=false`, no thumbnail, no playlist, no captions (burned in).
Titles: a short story line + 🤠, no hashtags in the title (that is how the hits were titled). `<FILM4_ID>` = film 4 video_id.
Tags for all: `["western", "western shorts", "old west", "cowboy story", "widow", "Tales of Cedar Bluff"]`.

### 4.1 Torches — `render/shorts/s4_torches_h04.mp4`
Title: `They Came at Midnight to Burn the Widow's Barn — She Didn't Miss 🤠`
```
Three riders with torches came for the widow's barn at midnight. "Stay home tomorrow. Or this barn burns tonight."
She was holding her father's buffalo rifle.

▶ Full story: https://youtu.be/<FILM4_ID> — link above (Related video)

A new tale from Cedar Bluff, Colorado, every week.
All characters and events are fictional. Created with the help of AI.

#shorts #western #oldwest #cowboy #westernstories

PRODUCTION NOTE

This midnight standoff is an edited scene from our original Western The Widow's Rifle. Script development, shot selection, dramatic timing, and editing are part of our creative production.
```

### 4.2 Bank — `render/shorts/s4_bank_h06.mp4`
Title: `The Banker Took Her Farm Four Minutes Early — He Didn't Know Who Owned the Bank 🤠`
```
She paid the note in full, in gold. "I'm afraid it's past noon, Mrs. Cole. The property belongs to the bank."
Then the quiet stranger checked the clock.

▶ Full story: https://youtu.be/<FILM4_ID> — link above (Related video)

A new tale from Cedar Bluff, Colorado, every week.
All characters and events are fictional. Created with the help of AI.

#shorts #western #oldwest #cowboy #westernstories

PRODUCTION NOTE

The bank scene is an edited moment from our original Western The Widow's Rifle. Script development, shot selection, dramatic timing, and editing are part of our creative production.
```

### 4.3 Forty cents — `render/shorts/s4_forty_cents_h01.mp4`
Title: `"Forty Cents Short, Ma'am?" The Town Laughed — Then a Stranger Paid It 🤠`
```
One dollar and sixty cents — and the entry was two dollars. The whole fair laughed at the widow.
The man behind her in line didn't.

▶ Full story: https://youtu.be/<FILM4_ID> — link above (Related video)

A new tale from Cedar Bluff, Colorado, every week.
All characters and events are fictional. Created with the help of AI.

#shorts #western #oldwest #cowboy #westernstories

PRODUCTION NOTE

The sign-up table scene opens our original Western The Widow's Rifle. Script development, shot selection, dramatic timing, and editing are part of our creative production.
```

### 4.4 Proposal — `render/shorts/s4_final_proposal.mp4`
Title: `The Quiet Stranger Owned the Bank — Then He Asked the Widow to Marry Him 🤠`
```
He counted other people's money for twenty years. He never had anything worth coming home to.
"Say yes, Ma! He's a terrible shot. Somebody's got to look after him!"

▶ Full story: https://youtu.be/<FILM4_ID> — link above (Related video)

A new tale from Cedar Bluff, Colorado, every week.
All characters and events are fictional. Created with the help of AI.

#shorts #western #oldwest #cowboy #westernstories

PRODUCTION NOTE

The proposal is the closing scene of our original Western The Widow's Rifle. Script development, shot selection, dramatic timing, and editing are part of our creative production.
```

## 5. How to write descriptions for the next videos (same channel style)
Checked on 16 Oct from the live descriptions of films 2–3 and the Shorts (`youtube_video_update(..., dry_run=true, tags=["x"])`
returns the current description untouched in `would_send` — a free way to read it).

**Film:** 2–3 lines of the story (humiliation → quiet stranger → a secret), a question for the comments, `⏱ Chapters`
(from `film_timeline`: narrator blocks and key lines; first 0:00, ≥10 s apart), «Watch next» link to the previous film,
subscribe line, `All characters and events are fictional. Created with the help of AI.`, 3–5 hashtags, then the block:
```
ABOUT THE PRODUCTION

This is an original fictional Western developed for Tales of Cedar Bluff. <2–3 story elements of THIS film> were shaped into a complete screenplay. Story development, creative direction, scene planning, shot selection, editing, music and sound design are part of our production process. Cinematic visuals and character voices are created with the assistance of generative AI. All characters and events are fictional.
```
**Short:** 2 lines of the scene + the strong line, `▶ Full story: https://youtu.be/<id> — link above (Related video)`,
«A new tale…», the fictional/AI line, `#shorts #western #oldwest #cowboy #westernstories`, then:
```
PRODUCTION NOTE

<This scene> is an edited scene from our original Western <Film name>. Script development, shot selection, dramatic timing, and editing are part of our creative production.
```
Only true statements about the human work (the owner writes/approves the script, reviews every cut, fixes glitches by
timecode, picks titles/thumbnails). The AI line always stays.
