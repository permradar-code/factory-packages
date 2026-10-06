#!/usr/bin/env python3
"""30-second story Shorts cut from the film (the format that worked: strong first frame + a complete mini-story).
Usage: python3 build_story_shorts.py shotgun|justice
Pieces: (film_start, film_end, crop_centre_x or (from_x, to_x[, pan_seconds])). Captions in film time.
"""
import subprocess, os, sys, json, re

FILM = "/home/claude/film.mp4"
FONTS = "/home/claude/sh/fonts"
CW = 608

SHORTS = {
    "shotgun": dict(
        out="/home/claude/sh/short06_shotgun.mp4",
        pieces=[(280.67, 286.21, 860), (286.21, 291.17, 900), (291.17, 297.17, (1050, 420, 2.5)),
                (297.17, 303.38, 680), (303.38, 305.17, 640), (305.17, 309.92, 860), (309.92, 312.42, 1000)],
        caps=[(281.34, 283.40, "That's far enough.", "Y"),
              (283.40, 285.84, "If you've come to collect,\\Nmister, there's nothing\\Nleft to sell.", "W"),
              (287.20, 290.82, "I didn't come to collect,\\Nma'am. I came to\\Nreturn something.", "W"),
              (291.88, 297.10, "I don't take charity.\\NNot from the bank,\\Nand not from strangers.", "W"),
              (297.86, 301.40, "Then don't call it charity.\\NYour east fence is down.", "W"),
              (301.40, 305.17, "I'll fix it for a hot supper.", "Y"),
              (306.36, 309.56, "One supper.\\NAnd you sleep in the barn.", "W"),
              (310.30, 312.42, "Yes, ma'am.", "Y")],
        hook=("SHE AIMED AT\\NTHE STRANGER.", 5.5),
    ),
    "justice": dict(
        out="/home/claude/sh/short07_justice.mp4",
        pieces=[(637.40, 641.90, 960), (642.25, 648.25, 760), (648.25, 656.25, 1300), (656.25, 658.96, 880),
                (658.96, 660.46, 520), (660.46, 664.92, 330), (664.92, 669.42, (1100, 1500, 4.0))],
        caps=[(642.66, 648.20, "Before anyone bids,\\Nthe marshal has a\\Nquestion for Mr. Pike.", "W"),
              (648.66, 652.60, "Horace Pike. You filed\\Na silver claim in Denver\\Non land you don't own.", "W"),
              (652.60, 656.25, "That's fraud.", "Y"),
              (656.64, 658.60, "Preposterous!", "W"),
              (659.23, 662.30, "Four hundred eighty.\\NThe Whitmore note is paid.", "W"),
              (662.30, 664.57, "In full.", "Y")],
        hook=("THE BANKER CAME\\NTO TAKE HER LAND.", 4.5),
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
    wd = f"/home/claude/sh/{name}"
    os.makedirs(wd, exist_ok=True)
    ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    parts, timeline, t = [], [], 0.0
    for i, (s, e, cx) in enumerate(cfg["pieces"]):
        d = e - s
        if isinstance(cx, tuple):
            a, b = cx2x(cx[0]), cx2x(cx[1])
            pd = cx[2] if len(cx) > 2 else d
            x = f"'{a}+({b}-{a})*min(t/{pd:.3f}\\,1)'"
        else:
            x = cx2x(cx)
        vf = f"crop={CW}:1080:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0,setsar=1,fps=24,format=yuv420p"
        raw = f"{wd}/raw{i:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", FILM, "-t", f"{d:.3f}", "-vf", vf] + ENC + [raw])
        g = -20.0 - mean_db(raw)
        f = f"{wd}/p{i:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "copy",
             "-af", f"volume={g:.2f}dB,afade=t=in:d=0.02,afade=t=out:st={d-0.04:.3f}:d=0.04",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", f])
        parts.append(f); timeline.append((s, e, t)); t += d
    total = t
    open(f"{wd}/concat.txt", "w").writelines(f"file '{p}'\n" for p in parts)

    def f2s(ft):
        best = None
        for s, e, off in timeline:
            if s - 0.05 <= ft <= e + 0.05:
                return off + min(max(ft, s), e) - s
            if ft < s and best is None:
                best = off
        return best if best is not None else total

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
    ass.append(f"Dialogue: 1,{ts(total-3.0)},{ts(total)},End,,0,0,0,,{{\\fad(250,0)}}FULL STORY\\NON THE CHANNEL")
    open(f"{wd}/caps.ass", "w").write("\n".join(ass) + "\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/concat.txt",
         "-vf", f"ass={wd}/caps.ass:fontsdir={FONTS}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", cfg["out"]])
    print(json.dumps({"out": cfg["out"], "duration": round(total, 2)}))


for n in (sys.argv[1:] or SHORTS):
    build(n)
