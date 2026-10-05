# Shorts and carousel for "The Widow's Piano"

Paths inside the scripts: film `/home/claude/film.mp4` (joined from branch `film/western_widows_piano_v1`),
hooks `/home/claude/wwp_pkg/visuals/hooks` (branch `pkg/western_widows_piano_v1`), fonts in `/home/claude/sh/fonts`
(Rye-Regular.ttf from this folder's parent + Inter ExtraBold).

| Script | Output | Notes |
|---|---|---|
| build_short01.py | short01_auction.mp4 (31.8 s) | Published 5 Oct morning. First frame = Mercer raising his hand: 72% swiped away. Weak hook. |
| build_short02.py | short02_fire.mp4 (12.7 s) | Film-only fire loop. Superseded by short05_shot. |
| build_short03.py | short03_auction_v2.mp4 (11.3 s) | Agatha + parasol first. Not published (first frame still "a person standing"). |
| build_hook_shorts.py gold | short04_gold.mp4 (13.6 s) | Opens on hook H01 (gold slammed on the table). |
| build_hook_shorts.py shot | short05_shot.mp4 (13.5 s) | Opens on hook H03 (Clara's warning shot), ends on H02 (barn erupts) -> loop. |
| make_carousel.py | carousel/card_01..09.jpg (1080x1350) | YouTube image post (Posts / Shorts feed). |

Lesson: a Short needs a first frame with one concrete loud action, readable in 0.5 s without sound.
Generate dedicated hook clips in Flow (9:16 works for Omni 1.1 Flash) instead of cutting talking scenes from the film.
