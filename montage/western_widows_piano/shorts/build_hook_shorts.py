#!/usr/bin/env python3
"""Shorts that open on the Flow hook clips (H01/H02/H03, 720x1280) and continue with scenes from the film.
Usage: python3 build_hook_shorts.py gold|shot
"""
import subprocess, os, sys, json, re

FILM = "/home/claude/film.mp4"
HOOKS = "/home/claude/wwp_pkg/visuals/hooks"
FONTS = "/home/claude/sh/fonts"
CW = 608

SHORTS = {
    # Gold slammed on the table -> back to the auction -> "In gold." loops into the slam
    "gold": dict(
        out="/home/claude/sh/short04_gold.mp4",
        pieces=[
            ("hook", "H01", 0.00, 2.30),
            ("film", 31.95, 35.21, 420, (520, 924)),  # Agatha: "Six dollars! ..."
            ("film", 35.21, 37.40, 960, None),        # Clara in tears, crowd laughing
            ("film", 41.00, 42.95, 870, None),        # "going twice..."
            ("film", 43.625, 45.90, (860, 960, 0.9), None),  # "Two hundred."
            ("film", 49.375, 51.00, 960, None),       # "In gold."
        ],
        caps=[  # (piece index, start, end, text, style) in piece-local time
            (1, 0.80, 2.25, "Six dollars!", "Y"),
            (1, 2.35, 3.26, "It will make\\Nlovely kindling.", "W"),
            (2, 0.00, 2.19, "It will make\\Nlovely kindling.", "W"),
            (3, 0.00, 1.95, "going twice...", "W"),
            (4, 0.925, 2.275, "Two hundred.", "Y"),
            (5, 0.075, 1.625, "In gold.", "Y"),
        ],
        hook=("THEY BID $6.\\NHE PAID IN GOLD.", 0.0, 4.6),
        end=3.0,
    ),
    # Clara's warning shot -> Mercer pins the rider -> torch lit -> barn goes up -> loops into the shot
    "shot": dict(
        out="/home/claude/sh/short05_shot.mp4",
        pieces=[
            ("hook", "H03", 0.00, 3.15),
            ("film", 533.96, 537.50, (900, 1180), None),  # "Tell Pike the lady isn't selling."
            ("film", 520.75, 524.60, 1060, None),         # torch lit, narration
            ("hook", "H02", 0.00, 2.95),                  # torch lands, barn erupts, horse rears
        ],
        caps=[
            (0, 1.70, 3.15, "The next one\\Ngoes lower!", "Y"),
            (1, 1.11, 3.44, "Tell Pike the lady\\Nisn't selling.", "W"),
            (2, 0.07, 1.85, "They only lit\\Ntheir torches...", "W"),
            (2, 1.85, 3.80, "...when they\\Nreached the barn.", "W"),
        ],
        hook=("THEY CAME TO\\NBURN HER OUT.", 0.0, 3.15),
        end=3.0,
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
    m, s = divmod(x, 60)
    return f"0:{int(m):02d}:{s:05.2f}"


def build(name):
    cfg = SHORTS[name]
    wd = f"/home/claude/sh/{name}"
    os.makedirs(wd, exist_ok=True)
    ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    parts, offs, t = [], [], 0.0
    for i, p in enumerate(cfg["pieces"]):
        raw = f"{wd}/raw{i:02d}.mp4"
        if p[0] == "hook":
            _, h, s, e = p
            d = e - s
            vf = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.4:5:5:0,setsar=1,fps=24,format=yuv420p"
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s}", "-i", f"{HOOKS}/{h}.mp4", "-t", f"{d:.3f}", "-vf", vf] + ENC + [raw])
        else:
            _, s, e, cx, zoom = p
            d = e - s
            cw, ch = zoom if zoom else (CW, 1080)
            if isinstance(cx, tuple):
                a, b = cx2x(cx[0]), cx2x(cx[1])
                pd = cx[2] if len(cx) > 2 else d
                x = f"'{a}+({b}-{a})*min(t/{pd:.3f}\\,1)'"
            else:
                x = max(0, min(1920 - cw, int(cx - cw / 2)))
            vf = f"crop={cw}:{ch}:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0,setsar=1,fps=24,format=yuv420p"
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", FILM, "-t", f"{d:.3f}", "-vf", vf] + ENC + [raw])
        # level-match every piece to the same mean loudness, short fades against clicks
        g = -20.0 - mean_db(raw)
        f = f"{wd}/p{i:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "copy",
             "-af", f"volume={g:.2f}dB,afade=t=in:d=0.02,afade=t=out:st={d-0.04:.3f}:d=0.04",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", f])
        parts.append(f); offs.append(t); t += d
    total = t
    open(f"{wd}/concat.txt", "w").writelines(f"file '{p}'\n" for p in parts)

    ass = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: W,Inter ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,60,60,620,1",
        "Style: Y,Inter ExtraBold,108,&H0033D6FF,&H0033D6FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,9,3,2,60,60,620,1",
        "Style: Hook,Rye,96,&H0033D6FF,&H0033D6FF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,7,4,8,60,60,250,1",
        "Style: End,Rye,70,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,6,4,8,60,60,250,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for pi, a, b, txt, st in cfg["caps"]:
        ass.append(f"Dialogue: 0,{ts(offs[pi]+a)},{ts(offs[pi]+b)},{st},,0,0,0,,{{\\fad(50,50)}}{txt}")
    htxt, ha, hb = cfg["hook"]
    ass.append(f"Dialogue: 1,{ts(ha)},{ts(hb)},Hook,,0,0,0,,{htxt}")
    ass.append(f"Dialogue: 1,{ts(total-cfg['end'])},{ts(total)},End,,0,0,0,,{{\\fad(250,0)}}FULL STORY\\NON THE CHANNEL")
    open(f"{wd}/caps.ass", "w").write("\n".join(ass) + "\n")

    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/concat.txt",
         "-vf", f"ass={wd}/caps.ass:fontsdir={FONTS}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", cfg["out"]])
    print(json.dumps({"out": cfg["out"], "duration": round(total, 2)}))


for n in (sys.argv[1:] or SHORTS):
    build(n)
