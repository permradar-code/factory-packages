#!/usr/bin/env python3
"""Film 3 story Short in the format of the film-1 hits (short06 110k, short01 45k, short07 41k):
~32 s complete mini-story cut from the finished film (music and sound included), 9:16 crop on the speaker,
Rye hook title for the first seconds, big Inter ExtraBold captions (yellow = punch line),
"FULL STORY ON THE CHANNEL" over the last 3 s. No red pill, no frozen end card.

Usage: FILM=/home/claude/f3/film.mp4 python3 build_story_short.py mothers
Film: joined final/The_Barn_in_the_Storm_partNN.bin (936 s, 1920x1080).
Pieces: (film_start, film_end, crop_centre_x). Cut points = shot cuts of the film. Captions in film time.
"""
import json, os, re, subprocess, sys

FILM = os.environ.get("FILM", "/home/claude/f3/film.mp4")
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
OUTDIR = os.environ.get("OUT", "/home/claude/f3/shorts")
CW = 608
BRAND = os.environ.get("BRAND", "/home/claude/f3/brand")
BADGE, BELL, BADGE_LEN = f"{BRAND}/badge.mov", f"{BRAND}/bell.wav", 5.5   # overlays/subscribe_badge.py + subscribe_bell.py

SHORTS = {
    # Store scene: refused credit -> the gossip's insult -> gold coin -> "We called them mothers." -> "he does bite."
    "mothers": dict(
        out="short_mothers.mp4",
        pieces=[(354.70, 360.083, 1020), (360.083, 368.083, 1220), (368.083, 376.083, 1080),
                (376.083, 383.25, 1290), (383.25, 383.54, 640), (383.54, 385.667, 1120), (385.667, 388.375, 1160)],
        caps=[(354.90, 357.70, "No credit to strangers,\\Nma'am.", "W"),
              (357.70, 360.05, "Cash or nothing.", "W"),
              (360.88, 364.40, "A widow, sleeping under\\Na widower's roof.", "W"),
              (364.40, 367.90, "In my day we had a word\\Nfor women like that.", "W"),
              (368.68, 372.10, "Boots for the girl.\\NA sack of flour.", "W"),
              (372.10, 375.70, "And whatever else\\Nthe lady needs.", "W"),
              (376.53, 379.90, "In my day, Mrs. Whitcomb,\\Nwe had a word for women", "W"),
              (379.90, 383.35, "who walk forty miles\\Nthrough a storm to keep\\Ntheir children.", "W"),
              (383.80, 385.55, "We called\\Nthem mothers.", "Y"),
              (385.87, 388.30, "Mama...\\Nhe does bite.", "Y")],
        hook=("THEY SHAMED\\NTHE WIDOW.", 4.5),
    ),
    # Gate standoff: the hired gun recognises the quiet rancher -> fight -> "Drop it, Pike!" -> gun lowered.
    # Test short: animated SUBSCRIBE badge + bell over the last 5.5 s instead of "FULL STORY ON THE CHANNEL".
    "harlan": dict(
        out="short_harlan.mp4",
        badge=True,
        pieces=[(692.75, 698.75, 1080), (698.75, 701.79, 960), (701.79, 705.67, 960), (705.67, 708.33, 960),
                (715.79, 718.79, 600), (725.79, 728.50, 990), (731.79, 734.79, (1440, 400, 2.5)),
                (737.79, 739.71, 1080), (743.79, 746.21, 900), (746.21, 750.21, 900)],
        caps=[(693.47, 695.90, "Harlan.\\NCaptain Wade Harlan.", "W"),
              (695.90, 698.67, "Company D.\\NTexas Rangers.", "Y"),
              (699.73, 701.69, "That was a long time ago.", "W"),
              (702.63, 705.53, "You sent my brother to\\NHuntsville. He died there.", "W"),
              (706.38, 708.22, "Then you know\\Nhow this ends, Deacon.", "Y"),
              (744.10, 745.80, "Drop it, Pike!", "Y")],
        hook=("THREE HIRED GUNS\\NCAME FOR HER BABY.", 4.5),
    ),
}


def run(cmd):
    subprocess.run(cmd, check=True)


def mean_db(f):
    r = subprocess.run(["ffmpeg", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+) dB", r).group(1))


def cx2x(cx):
    return max(0, min(1920 - CW, int(cx - CW / 2)))


def ts(x):
    m, s = divmod(max(0.0, x), 60)
    return f"0:{int(m):02d}:{s:05.2f}"


def build(name):
    cfg = SHORTS[name]
    wd = f"{OUTDIR}/{name}"
    os.makedirs(wd, exist_ok=True)
    ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    parts, timeline, t = [], [], 0.0
    # one loudness gain for the whole cut so the film's own mix (dialogue vs music) is kept between shots
    s0, e0 = cfg["pieces"][0][0], cfg["pieces"][-1][1]
    probe = f"{wd}/probe.wav"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s0:.3f}", "-i", FILM, "-t", f"{e0 - s0:.3f}", "-vn", probe])
    g = -20.0 - mean_db(probe)
    pieces = cfg["pieces"]
    for i, (s, e, cx) in enumerate(pieces):
        d = e - s
        if isinstance(cx, tuple):          # pan (from_x, to_x[, seconds])
            a, b = cx2x(cx[0]), cx2x(cx[1])
            pd = cx[2] if len(cx) > 2 else d
            x = f"'{a}+({b}-{a})*min(t/{pd:.3f}\\,1)'"
        else:
            x = cx2x(cx)
        vf = f"crop={CW}:1080:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0,setsar=1,fps=24,format=yuv420p"
        # short fades only where the cut jumps in film time (keeps continuous scenes seamless)
        jump_in = i > 0 and abs(pieces[i - 1][1] - s) > 0.05
        jump_out = i < len(pieces) - 1 and abs(pieces[i + 1][0] - e) > 0.05
        af = f"volume={g:.2f}dB"
        if jump_in:
            af += ",afade=t=in:d=0.03"
        if jump_out:
            af += f",afade=t=out:st={d - 0.04:.3f}:d=0.04"
        f = f"{wd}/p{i:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", FILM, "-t", f"{d:.3f}", "-vf", vf,
             "-af", af] + ENC + [f])
        parts.append(f); timeline.append((s, e, t)); t += d
    total = t
    open(f"{wd}/concat.txt", "w").writelines(f"file '{p}'\n" for p in parts)

    def f2s(ft):
        for s, e, off in timeline:
            if s - 0.05 <= ft <= e + 0.05:
                return off + min(max(ft, s), e) - s
        return total

    ass = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: W,Inter ExtraBold,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,50,50,620,1",
        "Style: Y,Inter ExtraBold,104,&H0033D6FF,&H0033D6FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,9,3,2,50,50,620,1",
        "Style: Hook,Rye,96,&H0033D6FF,&H0033D6FF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,7,4,8,60,60,250,1",
        "Style: End,Rye,70,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,6,4,8,60,60,250,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for a, b, txt, st in cfg["caps"]:
        ass.append(f"Dialogue: 0,{ts(f2s(a))},{ts(f2s(b))},{st},,0,0,0,,{{\\fad(50,50)}}{txt}")
    htxt, hdur = cfg["hook"]
    ass.append(f"Dialogue: 1,{ts(0)},{ts(hdur)},Hook,,0,0,0,,{htxt}")
    if not cfg.get("badge"):
        ass.append(f"Dialogue: 1,{ts(total - 3.0)},{ts(total)},End,,0,0,0,,{{\\fad(250,0)}}FULL STORY\\NON THE CHANNEL")
    open(f"{wd}/caps.ass", "w").write("\n".join(ass) + "\n")
    out = f"{OUTDIR}/{cfg['out']}"
    inputs = ["-f", "concat", "-safe", "0", "-i", f"{wd}/concat.txt"]
    vchain = f"[0:v]ass={wd}/caps.ass:fontsdir={FONTS}[v]"
    achain = f"[0:a]afade=t=in:d=0.05,afade=t=out:st={total - 0.4:.3f}:d=0.4[a0]"
    if cfg.get("badge"):
        # animated SUBSCRIBE badge over the last 5.5 s,
        # with its click + bell sound (overlays/subscribe_bell.py) at the same moment
        at = max(0.0, total - BADGE_LEN)
        inputs += ["-itsoffset", f"{at:.3f}", "-i", BADGE, "-i", BELL]
        # card lands at x 210-870, y 1370-1520: under the captions, clear of faces, left of the Shorts buttons
        vchain = (f"[1:v]crop=900:380:0:700[bd];"
                  f"[0:v]ass={wd}/caps.ass:fontsdir={FONTS}[vs];[vs][bd]overlay=130:1220:eof_action=pass[v]")
        ms = int(round(at * 1000))
        achain += f";[2:a]adelay={ms}|{ms}[bl];[a0][bl]amix=inputs=2:duration=first:normalize=0[a1]"
        alast = "[a1]"
    else:
        alast = "[a0]"
    achain += f";{alast}loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", vchain + ";" + achain,
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out])
    print(json.dumps({"out": out, "duration": round(total, 2)}))


for n in (sys.argv[1:] or SHORTS):
    build(n)
