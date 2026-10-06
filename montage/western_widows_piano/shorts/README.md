# Shorts and carousel for "The Widow's Piano"

Paths inside the scripts: film `/home/claude/film.mp4` (joined from branch `film/western_widows_piano_v1`),
hooks `/home/claude/wwp_pkg/visuals/hooks` (branch `pkg/western_widows_piano_v1`), fonts in `/home/claude/sh/fonts`
(Rye-Regular.ttf from this folder's parent + Inter ExtraBold).

| Script | Output | Notes |
|---|---|---|
| build_short01.py | short01_auction.mp4 (31.8 s) | Published 5 Oct morning (we5rffb-im0). By 6 Oct 11:40: 29.3k views, 76% stayed, +45 subs, wave flattened after ~1 day (~240 views/h tail). First frame = Mercer raising his hand: 72% swiped away. Weak hook. |
| build_short02.py | short02_fire.mp4 (12.7 s) | Film-only fire loop. Superseded by short05_shot. |
| build_short03.py | short03_auction_v2.mp4 (11.3 s) | Agatha + parasol first. Published 6 Oct morning as "She bid $6 to humiliate the widow…" (hU_xNEq9dB8): 5 views in 2 h, only from notifications — third auction cut, the feed treats it as a repeat. |
| build_hook_shorts.py gold | short04_gold.mp4 (13.6 s) | Opens on hook H01 (gold slammed on the table). |
| build_hook_shorts.py shot | short05_shot.mp4 (13.5 s) | Opens on hook H03 (Clara's warning shot), ends on H02 (barn erupts) -> loop. |
| build_story_shorts.py shotgun | short06_shotgun.mp4 (31.8 s) | Clara aims the shotgun (the A/B-winning thumbnail) → piano returned → "Yes, ma'am." |
| build_story_shorts.py justice | short07_justice.mp4 (31.7 s) | Riders gallop in → "That's fraud." → "In full." → Pike arrested, Agatha's parasol in the dust. |
| make_carousel.py | carousel/card_01..09.jpg (1080x1350) | YouTube image post (Posts / Shorts feed). |

Lesson: a Short needs a first frame with one concrete loud action, readable in 0.5 s without sound.
Generate dedicated hook clips in Flow (9:16 works for Omni 1.1 Flash) instead of cutting talking scenes from the film.

Results 6 Oct: short01 (32 s story) 28k views, 77% stayed, +44 subs; 12–14 s loops stalled at ~1.2k. For this audience (US 55+) Shorts must be 25–35 s mini-stories.
