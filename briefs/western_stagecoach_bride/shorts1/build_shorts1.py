# -*- coding: utf-8 -*-
"""Film 2 "The Stagecoach Bride" - SHORTS1: native vertical 9:16 clips for 4 Shorts (8 Oct 2026).

Why: Shorts cut from the 16:9 film looked small and dark. These clips are made vertical from the start:
close/medium shots, faces large, bright daylight, a line or action in the first second.
  arrest   : V01 V02 V03 V04
  jump     : V05 + H01 (existing) + V06 V07
  box      : V08 V09 + H02 (existing) + V10
  proposal : V02 (reused) V11 V12 V13
All clips go in as "hooks" (the factory's 9:16 path); the timeline only holds the one narration block film mode needs.
Run: python3 build_shorts1.py  -> shotlist.json, music_cues.json next to this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "build_shotlist.py")
_code = open(SRC, encoding="utf-8").read().split("\nSHOTS = []")[0]
_ns = {}
exec(compile(_code, SRC, "exec"), _ns)
STYLE, CLIP_STYLE, ACTION, PREV = (_ns[k] for k in ("STYLE", "CLIP_STYLE", "ACTION", "PREV"))
CHARACTERS, PROPS, LOCATIONS = _ns["CHARACTERS"], _ns["PROPS"], _ns["LOCATIONS"]

BRIGHT = (" Bright, high-key midday sunlight, vivid saturated colors, faces fully lit and clearly visible,"
          " no dark shadows, no night, no gloom.")
VSTYLE = STYLE.replace("16:9 widescreen", "9:16 vertical portrait frame").replace(
    "muted warm earth tones with golden aspen accents", "warm vivid colors with golden aspen accents") + BRIGHT
VCLIP = CLIP_STYLE.replace("16:9", "9:16 vertical portrait frame, subjects large and centered") + BRIGHT
OUT = {"A": "A: ivory lace wedding dress, short lace veil pinned back",
       "B": "B: faded green gingham dress with a white collar, hair in a simple low bun"}
TOWNSWOMAN = ("a sharp-tongued middle-aged townswoman in a dark-green bustle dress and a small feathered hat, "
              "an original fictional character")

SHOTS = []


def clip(id_, short, dur, action, refs, camera, lines=(), rose=None, action_shot=False):
    SHOTS.append({"id": id_, "short": short, "duration_s": dur, "action": action, "refs": refs, "camera": camera,
                  "lines": list(lines), "rose": rose, "action_shot": action_shot})


# ---------------- ARREST ----------------
clip("V01", "arrest", 8,
     "Sunlit main street of Cedar Bluff: Rose in her ivory lace wedding dress stands very close to Caleb, the young deputy, "
     "looking up at him with a shy, hopeful smile; Caleb looks down at her, pained, a pair of iron handcuffs in his hand.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_STREET"], "vertical medium close two-shot, both faces large in frame",
     lines=[("CHAR_ROSE", "I promised you'd see me in it first."), ("CHAR_CALEB", "And you're under arrest, ma'am.")], rose="A")
clip("V02", "arrest+proposal", 6,
     f"Sunny boardwalk of the main street: {TOWNSWOMAN} points her folded fan toward the street off-screen and sneers; "
     "behind her two townswomen in bonnets laugh behind gloved hands and a man in a bowler hat smirks.",
     ["LOC_STREET"], "vertical medium shot, slightly low angle, the laughing crowd behind her",
     lines=[("TOWNSWOMAN", "Look at her, ladies. Ordered by mail, delivered in irons.")])
clip("V03", "arrest", 6,
     "Sunlit main street: Rose in her ivory lace wedding dress walks slowly with her wrists in iron handcuffs, chin up, "
     "eyes wet with tears, a blurred crowd of townspeople watching behind her.",
     ["CHAR_ROSE", "LOC_STREET"], "vertical close-up tracking alongside her as she walks",
     lines=[("CHAR_ROSE", "I wore it for you, Caleb. Like I promised.")], rose="A")
clip("V04", "arrest", 6,
     "Inside a small log jail in daytime, bright sunlight streaming through the barred window: Rose in her ivory lace wedding "
     "dress holds the iron bars of the cell; Caleb stands just outside the bars, close to her.",
     ["CHAR_ROSE", "CHAR_CALEB", "LOC_JAIL"], "vertical close two-shot through the bars",
     lines=[("CHAR_ROSE", "I didn't steal anything, Caleb."), ("CHAR_CALEB", "I know.")], rose="A")

# ---------------- JUMP ----------------
clip("V05", "jump", 6,
     "Bright day, inside a racing dark-green stagecoach that bounces hard on a mountain road: old Amos Pruitt with a shotgun "
     "leans toward Rose, who clutches the small iron-banded green strongbox in her wedding dress; dust and sunlight through the window.",
     ["CHAR_AMOS", "CHAR_ROSE", "PROP_BOX", "PROP_STAGE"], "vertical handheld close two-shot inside the coach",
     lines=[("CHAR_AMOS", "When I say jump, girl, you jump!")], rose="A", action_shot=True)
clip("V06", "jump", 6,
     "Bright afternoon on a rocky mountain trail among golden aspens: a masked outlaw on a rearing horse reins in hard, "
     "rifle in one hand, and points up the slope; other riders gallop past in the dust.",
     ["CHAR_BUCK", "LOC_PASS"], "vertical low-angle medium shot",
     lines=[("CHAR_BUCK", "She went up the mountain! Find her!")], action_shot=True)
clip("V07", "jump", 6,
     "Bright afternoon: Rose in her torn ivory wedding dress scrambles up between huge sunlit boulders and golden aspens, "
     "the green strongbox clutched to her chest, and glances back over her shoulder, breathless.",
     ["CHAR_ROSE", "PROP_BOX", "LOC_PASS"], "vertical tracking shot from slightly below", rose="A", action_shot=True)

# ---------------- BOX ----------------
clip("V08", "box", 6,
     "Sunlit main street: Silas Crane, silver-haired in a charcoal suit, grips Rose's arm and presses a small derringer to her "
     "side; Rose, in her green gingham dress, holds the green strongbox against her chest.",
     ["CHAR_CRANE", "CHAR_ROSE", "PROP_BOX", "LOC_STREET"], "vertical medium close two-shot",
     lines=[("CHAR_CRANE", "The box, Miss Calloway. And then we'll take a little ride.")], rose="B")
clip("V09", "box", 6,
     "Sunlit main street: Caleb, his left arm in a white sling, steps out into the middle of the street, his right hand "
     "near his holstered revolver, eyes hard and steady.",
     ["CHAR_CALEB", "LOC_STREET"], "vertical medium shot, low angle",
     lines=[("CHAR_CALEB", "Let her go, Crane.")])
clip("V10", "box", 6,
     "Sunlit main street: Silas Crane kneels in the dust clutching his hurt wrist, his derringer lying out of reach; "
     "the marshal in a long gray coat steps over him with his revolver leveled.",
     ["CHAR_MARSHAL", "CHAR_CRANE", "LOC_STREET"], "vertical medium shot",
     lines=[("CHAR_MARSHAL", "Silas Crane. You're under arrest for robbing the mail.")])

# ---------------- PROPOSAL ----------------
clip("V11", "proposal", 8,
     "Sunlit main street full of townspeople: Caleb, his left arm in a white sling, kneels in the dust in front of Rose "
     "and holds up a small plain gold ring; Rose, in her green gingham dress, presses her hand to her mouth.",
     ["CHAR_CALEB", "CHAR_ROSE", "LOC_STREET"], "vertical medium two-shot, crowd behind",
     lines=[("CHAR_CALEB", "Rose Calloway. Will you marry me? Properly, this time.")], rose="B")
clip("V12", "proposal", 6,
     "Sunlit main street: close on Rose in her green gingham dress, laughing through happy tears and nodding; "
     "townspeople behind her start to cheer and clap.",
     ["CHAR_ROSE", "LOC_STREET"], "vertical close-up",
     lines=[("CHAR_ROSE", "Yes. Yes, Caleb.")], rose="B")
clip("V13", "proposal", 6,
     f"Sunny boardwalk: {TOWNSWOMAN} opens her mouth to make a remark; Clara, standing beside her with a basket on her arm, "
     "raises one finger without looking at her, a calm little smile.",
     ["CHAR_CLARA", "LOC_STREET"], "vertical medium two-shot",
     lines=[("CHAR_CLARA", "Not one word, Agatha.")])

VOICE = dict({k: v["voice"] for k, v in CHARACTERS.items()},
             TOWNSWOMAN="sharp, mocking, clipped middle-aged American woman's voice")
NAME = dict({k: v["name"] for k, v in CHARACTERS.items()}, TOWNSWOMAN="the townswoman")


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


hooks = []
for s in SHOTS:
    rose = OUT[s["rose"]] if s["rose"] else None
    rw = f" Rose wears: {rose}." if rose else ""
    start = ("Vertical 9:16 portrait frame. " + s["action"] + rw + " First frame of the shot, characters in position, mouths closed"
             + (", the action already in motion" if s["action_shot"] else "") + ". " + VSTYLE
             + (" Characters/places: " + ref_text(s["refs"]) if s["refs"] else ""))
    if s["lines"]:
        parts = []
        for k, (sp, line) in enumerate(s["lines"]):
            parts.append(("First " if k == 0 and len(s["lines"]) > 1 else "Then " if k else "")
                         + f'{NAME[sp]} ({VOICE[sp]}) says: "{line}"')
        dl = (" Dialogue: " + " ".join(parts) + " Only these exact lines are spoken, in this order; everyone else keeps their "
              "mouth closed. The first line starts within the first second; no extra words.")
    else:
        dl = " No dialogue: nobody speaks. Natural sound only (wind, hooves, dust, breathing)."
    video = (s["action"] + (ACTION if s["action_shot"] else "") + " Camera: " + s["camera"] + "." + dl + " " + VCLIP)
    hooks.append({
        "id": s["id"], "duration_s": s["duration_s"], "refs": s["refs"], "short": s["short"],
        "first_frame": s["action"], "first_frame_full_prompt": start,
        "video": s["action"], "video_prompt": video, "camera": s["camera"],
        "dialogue": [{"speaker": a, "line": b} for a, b in s["lines"]],
        "ref_files": ref_files(s["refs"], s["rose"] == "B"),
        "files": {"start_frame": f"visuals/hooks/{s['id']}_first.png", "video": f"visuals/hooks/{s['id']}.mp4"},
        **({"rose_outfit": rose} if rose else {}),
    })

secs = sum(h["duration_s"] for h in hooks)
shotlist = {
    "title": "The Stagecoach Bride - shorts1 (vertical)",
    "series": "Tales of Cedar Bluff", "episode": 2,
    "format": {"fps": 24},
    "estimate": {"clips": len(hooks), "clip_seconds": secs, "api_usd_at_0_10_per_s": round(secs * 0.10, 1)},
    "timeline": [{"id": "NX", "type": "narration", "text": "Tales of Cedar Bluff."}],
    "hooks": hooks,
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
        "export": {"package_branch": "pkg/western_stagecoach_bride_shorts1", "film_branch": "film/western_stagecoach_bride_shorts1"},
        "qc": {"long_duration_min_seconds": 1, "long_duration_max_seconds": 3600, "black_silence_max_seconds": 60},
    },
}
json.dump(shotlist, open(os.path.join(HERE, "shotlist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"film": "The Stagecoach Bride - shorts1", "cues": []}, open(os.path.join(HERE, "music_cues.json"), "w", encoding="utf-8"), indent=1)
print(f"{len(hooks)} vertical clips, {secs} s, ~${secs * 0.10:.1f} video + ~${len(hooks) * 0.067:.1f} first frames")
