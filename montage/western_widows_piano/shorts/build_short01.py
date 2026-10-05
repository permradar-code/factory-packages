#!/usr/bin/env python3
"""Short #1 (auction) for Tales of Cedar Bluff.
Result first ("Two hundred. In gold.") -> << REWIND -> auction from the start -> "going twice..." loops back to the start.
Source: The Widow's Piano v2 (1080p). Output 1080x1920, 24 fps, -14 LUFS.
"""
import subprocess, os, json

FILM = os.environ.get("FILM", "/home/claude/film.mp4")
OUT = os.environ.get("OUT", "/home/claude/sh/short01_auction.mp4")
WD = "/home/claude/sh/s01"
FONTS = "/home/claude/sh/fonts"
os.makedirs(WD, exist_ok=True)

CW = 608  # 9:16 crop width from 1080 height

# (film_start, film_end, crop_center_x)
PIECES = [
    # S1: result first
    (43.625, 46.375, "MERCER_OPEN"),  # Mercer raises his hand: "Two hundred."
    (46.375, 49.375, 720),   # Deke: "Two hundred... dollars, mister?"
    (49.375, 51.250, 960),   # Mercer: "In gold."
    "REWIND",
    # S2..S6: from the beginning
    (0.000, 1.400, 1000),    # "Lot thirty-one!"
    (8.000, 12.333, 700),    # Lily: "Mama... are they selling Grandma's piano?"
    (25.833, 31.833, 1020),  # Pike: "Let's be generous, Deke. Start it at five dollars."
    (31.833, 35.208, 450),   # Agatha: "Six dollars! ..."
    (35.208, 37.792, 960),   # Clara in tears, crowd laughing
    (37.792, 42.950, 870),   # Deke: "going once... going twice..." -> loops to Mercer's hand
]
REWIND_DUR = 1.25

# captions in film time (from The_Widows_Piano.en.srt); style: W=white, Y=yellow
CAPS = [
    (44.60, 46.30, "Two hundred.", "Y"),
    (46.62, 49.10, "Two hundred...\ndollars, mister?", "W"),
    (49.45, 51.25, "In gold.", "Y"),
    (0.09, 1.40, "Lot thirty-one!", "W"),
    (8.73, 9.75, "Mama...", "W"),
    (9.75, 12.20, "are they selling\nGrandma's piano?", "W"),
    (26.44, 29.00, "Let's be\ngenerous, Deke.", "W"),
    (29.00, 31.83, "Start it at\nfive dollars.", "W"),
    (32.36, 34.10, "Six dollars!", "Y"),
    (34.10, 37.42, "It will make\nlovely kindling.", "W"),
    (38.70, 40.80, "Six dollars,\ngoing once...", "W"),
    (40.80, 42.95, "going twice...", "W"),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def crop_x(cx):
    return max(0, min(1920 - CW, int(cx - CW / 2)))


VF = "crop={w}:1080:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0,setsar=1,fps=24,format=yuv420p"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

parts, timeline, t = [], [], 0.0
for i, p in enumerate(PIECES):
    f = f"{WD}/p{i:02d}.mp4"
    if p == "REWIND":
        # fast reverse through the first 51 s of the film: every 42nd frame, reversed, with tape look
        n = int(REWIND_DUR * 24)
        vf = ("select='not(mod(n\\,42))',setpts=N/24/TB," + VF.format(w=CW, x=crop_x(960)).replace(",fps=24", "")
              + f",trim=end_frame={n},reverse,eq=saturation=0.55:contrast=1.15:brightness=0.03,"
              "noise=alls=22:allf=t,"
              "drawbox=y=ih*0.43:w=iw:h=6:color=white@0.35:t=fill,drawbox=y=ih*0.71:w=iw:h=4:color=white@0.25:t=fill,"
              f"drawtext=fontfile={FONTS}/Rye-Regular.ttf:text='<< REWIND':fontsize=130:fontcolor=white:"
              "borderw=8:bordercolor=black:x=(w-tw)/2:y=(h-th)/2-120")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", "51.5", "-i", FILM,
             "-f", "lavfi", "-t", str(REWIND_DUR), "-i", "anoisesrc=color=pink:amplitude=0.5:sample_rate=48000",
             "-filter_complex",
             f"[0:v]{vf}[v];"
             f"[1:a]highpass=f=900,lowpass=f=6000,volume=0.35,afade=t=in:d=0.08,afade=t=out:st={REWIND_DUR-0.2}:d=0.2,aformat=channel_layouts=stereo[a]",
             "-map", "[v]", "-map", "[a]", "-r", "24", "-t", str(REWIND_DUR)] + ENC + [f])
        timeline.append(("REWIND", t, t + REWIND_DUR))
        t += REWIND_DUR
    else:
        s, e, cx = p
        d = e - s
        xexpr = ("'560+min(t/0.9\\,1)*96'" if cx == "MERCER_OPEN" else crop_x(cx))
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", FILM, "-t", f"{d:.3f}",
             "-vf", VF.format(w=CW, x=xexpr),
             "-af", f"afade=t=in:d=0.03,afade=t=out:st={d-0.04:.3f}:d=0.04",
             "-r", "24"] + ENC + [f])
        timeline.append((s, e, t))
        t += d
    parts.append(f)

TOTAL = t
with open(f"{WD}/concat.txt", "w") as fh:
    fh.writelines(f"file '{p}'\n" for p in parts)


def film_to_short(ft):
    for item in timeline:
        if item[0] == "REWIND":
            continue
        s, e, off = item
        if s - 0.01 <= ft <= e + 0.01:
            return off + (ft - s)
    return None


def ts(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


ass = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    # captions: lower-middle, above the Shorts UI
    "Style: W,Inter ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,60,60,620,1",
    "Style: Y,Inter ExtraBold,108,&H0033D6FF,&H0033D6FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,9,3,2,60,60,620,1",
    # top hook / end card in the channel's western font
    "Style: Hook,Rye,100,&H0033D6FF,&H0033D6FF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,7,4,8,60,60,250,1",
    "Style: End,Rye,70,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,6,4,8,60,60,250,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
for a, b, txt, st in CAPS:
    sa, sb = film_to_short(a), film_to_short(b)
    ass.append(f"Dialogue: 0,{ts(sa)},{ts(sb)},{st},,0,0,0,,{{\\fad(60,60)}}" + txt.replace("\n", "\\N"))
s1_end = timeline[2][2] + (timeline[2][1] - timeline[2][0])
ass.append(f"Dialogue: 1,{ts(0)},{ts(s1_end)},Hook,,0,0,0,,THEY BID $6\\NFOR HER PIANO.")
ass.append(f"Dialogue: 1,{ts(TOTAL-4.3)},{ts(TOTAL)},End,,0,0,0,,{{\\fad(250,0)}}FULL STORY\\NON THE CHANNEL")
with open(f"{WD}/caps.ass", "w") as fh:
    fh.write("\n".join(ass) + "\n")

run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/concat.txt",
     "-vf", f"ass={WD}/caps.ass:fontsdir={FONTS}",
     "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
     "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", OUT])
print(json.dumps({"out": OUT, "duration": round(TOTAL, 2)}))
