# -*- coding: utf-8 -*-
"""Film 2 "The Stagecoach Bride" - FIX1 batch (8 Oct 2026).

Why: the factory edit of v4 had too few visuals under the narrator (6:20 of narration, ~48% of the film),
so it looped dialogue clips (lips moving under the narrator) and held stills for 30 s. C61 and C102 came out
with the wrong bride. This batch generates only:
  * C61R, C102R - the cold-open crowd shots, re-staged so Rose is NOT in frame (no continuity risk);
  * B01..B5x    - silent b-roll clips that illustrate the narration line by line.
Everything else is reused from western_stagecoach_bride_v1. The edit is done outside the factory.
Run: python3 build_fix1.py  -> shotlist.json, music_cues.json next to this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "build_shotlist.py")
_code = open(SRC, encoding="utf-8").read().split("\nSHOTS = []")[0]
_ns = {}
exec(compile(_code, SRC, "exec"), _ns)          # STYLE, NIGHT, CLIP_STYLE, ACTION, PREV, CHARACTERS, PROPS, LOCATIONS
STYLE, NIGHT, CLIP_STYLE, ACTION, PREV = (_ns[k] for k in ("STYLE", "NIGHT", "CLIP_STYLE", "ACTION", "PREV"))
CHARACTERS, PROPS, LOCATIONS = _ns["CHARACTERS"], _ns["PROPS"], _ns["LOCATIONS"]

OUT = {"A": "A: ivory lace wedding dress",
       "A2": "A: the same ivory lace wedding dress, cleaned and carefully mended, veil pinned back",
       "A2S": "A: the same ivory lace wedding dress, mended, now smudged with soot at the hem and sleeves",
       "B": "B: faded green gingham dress, low bun"}

SHOTS = []


def clip(id_, for_, dur, action, refs, camera="", night=False, action_shot=False, rose=None, lines=()):
    SHOTS.append({"id": id_, "for": for_, "duration_s": dur, "action": action, "refs": refs, "camera": camera,
                  "night": night, "action_shot": action_shot, "rose": rose, "lines": list(lines)})


# ---------------- cold open re-stage (Rose kept OUT of frame) ----------------
clip("C61R", "cold open", 6,
     "Afternoon on the boardwalk of the main street: Agatha Pell steps forward from a crowd of townspeople, raises her closed white lace parasol and points it toward the street off-screen to the right, her chin high, cold and contemptuous. Only Agatha and the onlookers behind her are in frame; the street in front of her is out of frame.",
     ["CHAR_AGATHA", "LOC_STREET"], camera="medium shot from the street, the crowd behind her",
     lines=[("CHAR_AGATHA", "Look at her, ladies. A thief, delivered by mail.")])
clip("C102R", "cold open", 6,
     "Afternoon, main street boardwalk: townspeople laugh out loud and point toward the street off-screen; two well-dressed ladies in bonnets hide their smiles behind gloved hands; a man in a bowler hat shakes his head; a boy climbs a hitching rail to see better. Only the crowd is in frame.",
     ["LOC_STREET"], camera="slow pan along the laughing crowd")

# ---------------- N01: Rose hides on the mountain ----------------
clip("B01", "N01", 6, "Dusk on a rocky mountainside: Rose crouches hidden in a narrow gap between two huge granite boulders, clutching the small green strongbox to her chest, breathing hard, listening, her veil torn.",
     ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], camera="slow push in through the rocks", rose="A")
clip("B02", "N01", 6, "Dusk: four masked riders with rifles move slowly along the rocky slope below, scanning the boulders, one points uphill; seen from high above between the rocks, as if from Rose's hiding place.",
     ["CHAR_BUCK", "LOC_PASS"], camera="high angle looking down through a gap in the rocks")
clip("B03", "N01", 4, "Extreme close-up in the last light of day: Rose's trembling hands in lace sleeves tighten around the brass padlock of the green strongbox.",
     ["CHAR_ROSE", "PROP_BOX"], camera="extreme close-up, very slow push", rose="A")

# ---------------- N02: Silas Crane ----------------
clip("B04", "N02", 6, "Sunday morning inside a small white wooden church full of sunlight: Silas Crane sits alone in the front pew in his charcoal suit, silver-headed cane across his knees; the townspeople behind him; he turns his head slightly, a thin, cold smile.",
     ["CHAR_CRANE"], camera="slow dolly in from the aisle")

# ---------------- N03: the search ----------------
clip("B05", "N03", 6, "Night on the mountain stage road: Caleb rides slowly with a lantern held high, calling out into the dark rocks, his breath steaming in the cold air.",
     ["CHAR_CALEB", "LOC_PASS"], camera="wide tracking shot", night=True)
clip("B06", "N03", 6, "Grey dawn on the pass: John Mercer on his dark bay horse stops, leans down from the saddle and picks a torn scrap of white lace off a thorny bush, then looks up the slope.",
     ["CHAR_MERCER", "PROP_HORSE", "LOC_PASS"], camera="medium shot, slow push in")

# ---------------- N04: Mercer, the barn, the box ----------------
clip("B07", "N04", 6, "Evening at the Whitmore ranch: at the open kitchen door John Mercer touches the brim of his hat to Clara, who stands inside in the lamplight; he turns and walks out into the dusk; she watches him go.",
     ["CHAR_MERCER", "CHAR_CLARA", "LOC_RANCH"], camera="medium shot from inside the kitchen", night=True)
clip("B08", "N04", 6, "Night: John Mercer crosses the moonlit ranch yard toward the small barn carrying a lantern; in the house behind him a warm window glows and a woman's silhouette stands at it.",
     ["CHAR_MERCER", "LOC_RANCH"], camera="wide shot, static", night=True)
clip("B09", "N04", 6, "Sunny day on the main street: John Mercer helps Clara down from a wagon; on the boardwalk two older women lean together, whispering and smiling knowingly.",
     ["CHAR_MERCER", "CHAR_CLARA", "LOC_STREET"], camera="medium wide shot")
clip("B10", "N04", 6, "Night, kitchen table, oil lamp: a brass key turns in the heavy padlock of the green strongbox, the lid lifts, and inside is a second small steel lock fixed to an inner iron lid.",
     ["PROP_BOX", "LOC_KITCHEN"], camera="close-up from above", night=True)

# ---------------- N05: the roan with the loose shoe ----------------
clip("B11", "N05", 4, "Close-up at a ranch gate: the left front hoof of a tall roan horse stamps on the stones of the yard; the iron horseshoe is loose and rings.",
     ["LOC_RANCH"], camera="low close-up on the hoof")
clip("B12", "N05", 4, "John Mercer stands by the barn door, eyes narrowed, silently watching something at the gate.",
     ["CHAR_MERCER", "LOC_RANCH"], camera="close-up, very slow push")
clip("B13", "N05", 6, "Night at the ranch: a shaggy farm dog lying on the porch lifts its head, ears up, staring into the dark yard; then it goes still; a man's shadow slides along the barn wall.",
     ["LOC_RANCH"], camera="low angle from the porch", night=True)

# ---------------- N06: the box under the floor; Crane ----------------
clip("B14", "N06", 6, "Night, kitchen by lamplight: Clara kneels and lifts a loose floorboard; under it lies the green strongbox wrapped in a flour sack; she lays the board back down quietly.",
     ["CHAR_CLARA", "PROP_BOX", "LOC_KITCHEN"], camera="high angle close-up", night=True)
clip("B15", "N06", 6, "Night, a rich man's study with a fireplace: Silas Crane stands at the dark window, slowly crushes his cigar in a crystal ashtray, his reflection cold in the glass.",
     ["CHAR_CRANE", "LOC_CRANE"], camera="slow push in", night=True)

# ---------------- N07: mending the dress; the warrant ----------------
clip("B16", "N07", 6, "Evening, kitchen table by the oil lamp: Rose, in the gingham dress, carefully sews a torn seam of the ivory lace wedding dress spread across her lap, a small smile.",
     ["CHAR_ROSE", "LOC_KITCHEN"], camera="medium close-up", night=True, rose="B")
clip("B17", "N07", 6, "Afternoon: Caleb rides up the dirt road toward the Whitmore ranch, a folded paper warrant in his hand, his face grim.",
     ["CHAR_CALEB", "LOC_RANCH"], camera="wide shot, then he rides past camera")

# ---------------- N09: the jail, Ivanhoe, the address ----------------
clip("B18", "N09", 8, "Night inside the jail: Caleb sits on a stool outside the iron bars, reading aloud from an old leather-bound book by lamplight; behind the bars Rose sits on the cot in her mended wedding dress, listening.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_JAIL"], camera="slow dolly sideways along the bars", night=True, rose="A2")
clip("B19", "N09", 6, "Close-up, night: Rose behind the iron bars listens with a soft, amused smile, lamplight on her face, her lips closed.",
     ["CHAR_ROSE", "LOC_JAIL"], camera="close-up, very slow push", night=True, rose="A2")
clip("B20", "N09", 6, "Night exterior: the small log jail at the far end of the main street, one warm lit window, the street empty and silver in moonlight, a dog trotting past.",
     ["LOC_STREET", "LOC_JAIL"], camera="wide static shot", night=True)
clip("B21", "N09", 6, "Night, a log ranch house far out on the plain under the stars: an oil lamp burns in the window; aspens move softly in the wind.",
     ["LOC_RANCH"], camera="very slow push toward the lit window", night=True)

# ---------------- N10: hands through the bars ----------------
clip("B22", "N10", 6, "Extreme close-up by lamplight: a woman's hand in a lace sleeve reaches through the iron bars and a man's hand takes it; their fingers hold on.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_JAIL"], camera="extreme close-up", night=True, rose="A2")

# ---------------- N11: after the fire ----------------
clip("B23", "N11", 6, "Night, thick smoke pouring from the jail door: John Mercer drags a coughing Caleb out into the street, both blackened with soot, flames behind them.",
     ["CHAR_MERCER", "CHAR_CALEB", "LOC_STREET"], camera="handheld medium shot", night=True, action_shot=True)
clip("B24", "N11", 6, "Sunrise: the burned jail is a black, smoking shell of charred logs; townspeople stand silently in the street looking at it.",
     ["LOC_STREET"], camera="slow wide pan")
clip("B25", "N11", 6, "Early morning in the street: Clara wraps a shawl around Rose's shoulders and hands her a folded green gingham dress; Rose's wedding dress is smudged with soot.",
     ["CHAR_CLARA", "CHAR_ROSE", "LOC_STREET"], camera="medium shot", rose="A2S")
clip("B26", "N11", 6, "In the ashes by a hitching rail, John Mercer crouches and picks up a blackened horseshoe, turning it in his fingers to look at a nail snapped off short.",
     ["CHAR_MERCER", "LOC_STREET"], camera="close-up on his hands, then his face")

# ---------------- N12: the hairpin ----------------
clip("B27", "N12", 6, "Night, kitchen, oil lamp: Clara pulls a long hairpin from her braided hair and hands it to Rose; Rose bends it straight between her fingers.",
     ["CHAR_CLARA", "CHAR_ROSE", "LOC_KITCHEN"], camera="medium close-up", night=True, rose="B")
clip("B28", "N12", 6, "Extreme close-up by lamplight: a bent hairpin works inside a small steel lock; it clicks open and the inner iron lid lifts to reveal a bundle of folded letters tied with string.",
     ["PROP_BOX"], camera="extreme close-up", night=True)

# ---------------- N13: the handwriting, the clerk, Crane ----------------
clip("B29", "N13", 6, "Close-up on a table by lamplight: two letters lie side by side, one signed, one unsigned; a woman's finger traces the same looping capital letters on both.",
     ["LOC_KITCHEN"], camera="slow push in from above", night=True)
clip("B30", "N13", 6, "Denver, 1880, an express company office with ledgers and a wall clock: a nervous young clerk in sleeve garters and spectacles glances over his shoulder and slips a folded schedule into the gloved hand of a man in a charcoal suit.",
     [], camera="medium shot")
clip("B31", "N13", 6, "Night at a stage depot under a lantern: the same nervous young clerk presses a bundle of letters tied with string into the hands of Amos Pruitt, the old express guard; Amos nods gravely.",
     ["CHAR_AMOS"], camera="medium shot", night=True)
clip("B32", "N13", 6, "Night: in a rich man's study, Silas Crane drops a letter into the fireplace and watches it curl and burn, his face lit orange by the flames.",
     ["CHAR_CRANE", "LOC_CRANE"], camera="close-up", night=True)

# ---------------- N14: the empty house, the trail ----------------
clip("B33", "N14", 6, "Morning in Crane's empty study: an iron safe stands wide open and empty, papers scattered on the floor; the marshal walks in slowly, holding a folded warrant.",
     ["CHAR_MARSHAL", "LOC_CRANE"], camera="wide shot, slow push")
clip("B34", "N14", 6, "John Mercer kneels in the dust outside a big ranch house, touching fresh hoofprints with two fingers, then looks up toward distant red hills.",
     ["CHAR_MERCER", "LOC_CRANE"], camera="low medium shot")
clip("B35", "N14", 6, "Three riders gallop out across golden grassland toward red hills: the marshal in his gray coat, John Mercer on his dark bay, and Caleb with his left arm in a white sling.",
     ["CHAR_MARSHAL", "CHAR_MERCER", "CHAR_CALEB", "PROP_HORSE"], camera="wide tracking shot", action_shot=True)

# ---------------- N15: high ground ----------------
clip("B36", "N15", 6, "On the rim of a red sandstone canyon, Buck Tolliver lies behind a rock with a rifle, watching the canyon floor below.",
     ["CHAR_BUCK", "LOC_CANYON"], camera="over-the-shoulder looking down into the canyon")
clip("B37", "N15", 6, "John Mercer climbs silently around through tumbled red boulders behind the canyon rim, rifle on his back, moving low and careful.",
     ["CHAR_MERCER", "LOC_CANYON"], camera="tracking shot through the rocks")

# ---------------- N16: the decoy ----------------
clip("B38", "N16", 6, "Silas Crane rides alone at a trot up the dirt road toward the Whitmore ranch, his cream hat low, a revolver at his hip.",
     ["CHAR_CRANE", "LOC_RANCH"], camera="wide shot from the porch")
clip("B39", "N16", 6, "Inside the kitchen, Rose alone in her gingham dress dries a tin plate; she hears hoofbeats outside, stops, and slowly turns toward the window.",
     ["CHAR_ROSE", "LOC_KITCHEN"], camera="medium shot", rose="B")

# ---------------- N17: justice ----------------
clip("B40", "N17", 6, "A wood-paneled Denver courtroom, 1880: old Amos Pruitt, one arm in a sling, stands at the witness stand and raises his right hand to swear.",
     ["CHAR_AMOS"], camera="slow push in")
clip("B41", "N17", 6, "A barred iron prison wagon rolls away down a dusty road toward a stone penitentiary; through the bars Silas Crane and Buck Tolliver sit in chains, staring ahead.",
     ["CHAR_CRANE", "CHAR_BUCK"], camera="wide shot, the wagon rolls away from camera")

# ---------------- N18 / N19: the weddings, the light in the window ----------------
clip("B42", "N18", 6, "Golden sunset over the Whitmore ranch: long shadows, aspens glowing, smoke rising from the chimney, a woman standing on the porch.",
     ["LOC_RANCH"], camera="wide static shot")
clip("B43", "N19", 8, "A small October wedding outdoors under golden aspen trees: Clara in a simple cream dress and John Mercer in a dark suit stand before an old preacher; a few townspeople watch, and little Lily holds wildflowers.",
     ["CHAR_CLARA", "CHAR_MERCER", "CHAR_LILY"], camera="slow dolly in")
clip("B44", "N19", 6, "At the same aspen wedding, Rose in her gingham dress and Caleb in his vest stand beside the couple as witnesses, smiling at each other.",
     ["CHAR_ROSE", "CHAR_CALEB"], camera="medium shot", rose="B")
clip("B45", "N19", 6, "Spring: Rose in her ivory lace wedding dress and Caleb walk out of the little white church into sunshine and green grass; townspeople throw rice.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], camera="wide shot", rose="A2")
clip("B46", "N19", 6, "Night: an oil lamp burning in the window of a log ranch house, seen from outside through the glass, warm and steady.",
     ["LOC_RANCH"], camera="very slow push in toward the lamp", night=True)


# ---------------- build ----------------
def ref_text(refs):
    out = []
    for r in refs:
        src = CHARACTERS.get(r) or PROPS.get(r) or LOCATIONS.get(r)
        if src:
            out.append(f"{src['name']}: {src['look']}")
    return " | ".join(out)


def ref_files(refs, outfit_b):
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


timeline = []
for s in SHOTS:
    rose = OUT[s["rose"]] if s["rose"] else None
    lines = s["lines"]
    rw = f" Rose wears: {rose}." if rose else ""
    start = (s["action"] + rw + " First frame of the shot, characters in position"
             + (", mouths closed" if lines else ", everyone's mouth closed") + (", the action already in motion" if s["action_shot"] else "")
             + ". " + STYLE + (NIGHT if s["night"] else "") + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else ""))
    if lines:
        sp, line = lines[0]
        c = CHARACTERS[sp]
        dl = (f' Dialogue: {c["name"]} ({c["voice"]}) says: "{line}" ONLY {c["name"]} speaks; everyone else keeps their mouth closed.'
              " The line starts within the first second; after the line the speaker holds a natural expression, no extra words.")
    else:
        dl = " No dialogue: nobody speaks, every mouth stays closed. Natural ambient sound only (wind, hooves, fire, crowd murmur, crickets)."
    video = s["action"] + (ACTION if s["action_shot"] else "") + (" Camera: " + s["camera"] + "." if s["camera"] else "") + dl + " " + CLIP_STYLE
    timeline.append({
        "id": s["id"], "type": "clip", "duration_s": s["duration_s"], "action": s["action"], "camera": s["camera"],
        "dialogue": [{"speaker": a, "line": b} for a, b in lines], "refs": s["refs"], "priority": "core",
        "night": s["night"], "action_shot": s["action_shot"], "broll": not lines, "for": s["for"],
        "start_frame_prompt": s["action"], "start_frame_full_prompt": start, "video_prompt": video,
        "ref_files": ref_files(s["refs"], s["rose"] == "B"),
        "files": {"start_frame": f"visuals/images/{s['id']}_first.png", "video": f"visuals/video/{s['id']}.mp4"},
        **({"rose_outfit": rose} if rose else {}),
    })
# film mode needs one narration block; the edit does not use it
timeline.append({"id": "NX", "type": "narration", "text": "Tales of Cedar Bluff."})

secs = sum(t["duration_s"] for t in timeline if t["type"] == "clip")
shotlist = {
    "title": "The Stagecoach Bride - fix1 b-roll",
    "series": "Tales of Cedar Bluff", "episode": 2,
    "format": {"fps": 24},
    "estimate": {"clips": len(SHOTS), "clip_seconds": secs, "est_total_min_core": round(secs / 60 + 0.2, 1),
                 "api_usd_at_0_10_per_s": round(secs * 0.10, 1)},
    "timeline": timeline,
    "hooks": [],
    "production": {
        "schema_version": 1,
        "review_gates": {"references": {"enabled": False}, "audio": {"enabled": False},
                         "visuals": {"enabled": False}, "video_sample": {"enabled": False}, "videos": {"enabled": False}},
        "edit": {"dialogue_tail_seconds": 0.8, "narration_voice_offset_seconds": 0.4, "transition_seconds": 0.3,
                 "end_screen_tail_seconds": 0, "contact_sheet": "one_frame_per_timeline_visual"},
        "audio_mix": {"speech_active_rms_db": -20, "ambient_clip_rms_db": -24, "music_base_rms_db": -18,
                      "duck_under_speech_db": -15, "duck_under_clip_db": -6, "duck_attack_seconds": 0.15,
                      "duck_release_seconds": 0.6, "integrated_lufs": -14, "true_peak_db": -1.5},
        "voice": {"provider": "elevenlabs", "voice_id": "pqHfZKP75CvOlQylNhV4", "model": "eleven_multilingual_v2",
                  "speed": 1, "timestamps": True, "output_format": "mp3_44100_128", "stability": 0.55,
                  "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True},
        "subtitle": {"language": "en", "name": "English"},
        "export": {"package_branch": "pkg/western_stagecoach_bride_fix1", "film_branch": "film/western_stagecoach_bride_fix1"},
        "qc": {"long_duration_min_seconds": 1, "long_duration_max_seconds": 3600, "black_silence_max_seconds": 60},
    },
}
json.dump(shotlist, open(os.path.join(HERE, "shotlist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"film": "The Stagecoach Bride - fix1", "cues": []}, open(os.path.join(HERE, "music_cues.json"), "w", encoding="utf-8"), indent=1)
print(f"{len(SHOTS)} clips, {secs} s, ~${secs * 0.10:.1f} video + ~${len(SHOTS) * 0.067:.1f} first frames")
