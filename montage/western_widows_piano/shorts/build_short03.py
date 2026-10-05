#!/usr/bin/env python3
"""Short #3 (auction v2, micro loop ~11 s) for Tales of Cedar Bluff.
Shotgun blast first -> "The next one goes lower!" -> Mercer pins the rider -> barn on fire -> torch being lit
("They only lit their torches when they reached the barn.") -> loops back to the blast.
"""
import subprocess, os, json

FILM = os.environ.get("FILM", "/home/claude/film.mp4")
OUT = os.environ.get("OUT", "/home/claude/sh/short03_auction_v2.mp4")
WD = "/home/claude/sh/s03"
FONTS = "/home/claude/sh/fonts"
os.makedirs(WD, exist_ok=True)
CW = 608

# (film_start, film_end, crop_center or (center_from, center_to) for a pan)
PIECES = [
    (31.95, 35.21, 420),             # Agatha snaps her parasol open: "Six dollars! ..."
    (35.21, 37.40, 960),             # Clara in tears, the crowd laughing: "...lovely kindling."
    (41.00, 42.95, 870),             # Deke with the gavel: "going twice..."
    (43.625, 45.90, (860, 960, 0.9)),  # Mercer raises his hand: "Two hundred."
    (49.375, 51.00, 960),            # "In gold." -> loops back to the parasol
]
CAPS = [
    (32.75, 34.20, "Six dollars!", "Y"),
    (34.30, 37.40, "It will make\nlovely kindling.", "W"),
    (41.00, 42.95, "going twice...", "W"),
    (44.55, 45.90, "Two hundred.", "Y"),
    (49.45, 51.00, "In gold.", "Y"),
]
HOOK = ("THEY LAUGHED\\NAT THE WIDOW.", 5.45)


def run(cmd):
    subprocess.run(cmd, check=True)


def cx2x(cx):
    return max(0, min(1920 - CW, int(cx - CW / 2)))


ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
parts, timeline, t = [], [], 0.0
for i, (s, e, cx) in enumerate(PIECES):
    d = e - s
    if isinstance(cx, tuple):
        a, b = cx2x(cx[0]), cx2x(cx[1])
        pd = cx[2] if len(cx) > 2 else d
        x = f"'{a}+({b}-{a})*min(t/{pd:.3f}\\,1)'"
    else:
        x = cx2x(cx)
    cw, ch = (520, 924) if i == 0 else (CW, 1080)   # tighter on Agatha so her face reads at a glance
    if i == 0:
        x = max(0, int(cx - cw / 2))
    vf = f"crop={cw}:{ch}:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0,setsar=1,fps=24,format=yuv420p"
    af = f"afade=t=in:d=0.02,afade=t=out:st={d-0.04:.3f}:d=0.04"
    f = f"{WD}/p{i:02d}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", FILM, "-t", f"{d:.3f}", "-vf", vf, "-af", af, "-r", "24"] + ENC + [f])
    parts.append(f); timeline.append((s, e, t)); t += d
TOTAL = t
open(f"{WD}/concat.txt", "w").writelines(f"file '{p}'\n" for p in parts)


def f2s(ft):
    for s, e, off in timeline:
        if s - 0.01 <= ft <= e + 0.01:
            return off + min(max(ft, s), e) - s
    raise ValueError(ft)


def ts(x):
    m, s = divmod(x, 60)
    return f"0:{int(m):02d}:{s:05.2f}"


ass = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: W,Inter ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,60,60,620,1",
    "Style: Y,Inter ExtraBold,108,&H0033D6FF,&H0033D6FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,9,3,2,60,60,620,1",
    "Style: Hook,Rye,100,&H0033D6FF,&H0033D6FF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,7,4,8,60,60,250,1",
    "Style: End,Rye,70,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,6,4,8,60,60,250,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
for a, b, txt, st in CAPS:
    ass.append(f"Dialogue: 0,{ts(f2s(a))},{ts(f2s(b))},{st},,0,0,0,,{{\\fad(60,60)}}" + txt.replace("\n", "\\N"))
ass.append(f"Dialogue: 1,{ts(0)},{ts(HOOK[1])},Hook,,0,0,0,,{HOOK[0]}")
ass.append(f"Dialogue: 1,{ts(TOTAL-3.2)},{ts(TOTAL)},End,,0,0,0,,{{\\fad(250,0)}}FULL STORY\\NON THE CHANNEL")
open(f"{WD}/caps.ass", "w").write("\n".join(ass) + "\n")

run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/concat.txt",
     "-vf", f"ass={WD}/caps.ass:fontsdir={FONTS}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
     "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
     "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", OUT])
print(json.dumps({"out": OUT, "duration": round(TOTAL, 2)}))
