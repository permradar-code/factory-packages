#!/usr/bin/env python3
"""Vertical Short (1080x1920) from the finished film: the arrest on Main Street.
Segments are cut from the final film (picture + mixed sound), stacked over a blurred copy,
with a fixed hook line on top and the spoken line as a big caption under the picture.
Usage: python3 short_cold_open.py [film.mp4] [out.mp4]
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
FILM = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wsb_edit/stagecoach_bride.mp4"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/wsb_edit/short_arrest.mp4"
EDL = json.load(open("/home/claude/wsb_edit/edl_timed.json"))
TMP = "/home/claude/wsb_edit/short_tmp"
os.makedirs(TMP, exist_ok=True)
W, H = 1080, 1920
HOOK = "HER OWN GROOM\nARRESTED HER"
# (clip id, seconds to keep from the clip start in the film or None = whole)
SEQ = [("C58", None), ("C109", None), ("C59", None), ("C103", None), ("C104", None), ("C102R", 2.0),
       ("C61R", None), ("C110", None), ("C63", None), ("C64", None)]
END = "FULL MOVIE ON THE CHANNEL"

ev = {e["id"]: e for e in EDL["events"]}


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return "\n".join(lines)


def overlay(path, caption, end=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fh = ImageFont.truetype(FONT, 104)
    d.multiline_text((W // 2, 150), HOOK, font=fh, fill=(255, 214, 0), anchor="ma", align="center",
                     stroke_width=10, stroke_fill=(0, 0, 0), spacing=6)
    if caption:
        fc = ImageFont.truetype(FONT, 76)
        txt = wrap(d, caption, fc, W - 120)
        d.multiline_text((W // 2, 1395), txt, font=fc, fill=(255, 255, 255), anchor="ma", align="center",
                         stroke_width=8, stroke_fill=(0, 0, 0), spacing=10)
    if end:
        fe = ImageFont.truetype(FONT, 70)
        d.text((W // 2, 1700), END, font=fe, fill=(255, 214, 0), anchor="ma", stroke_width=8, stroke_fill=(0, 0, 0))
    im.save(path)


parts = []
for k, (cid, keep) in enumerate(SEQ):
    e = ev[cid]
    st, dur = e["rstart"], keep or e["dur"]
    cap = " ".join(x["line"] for x in e.get("dialogue") or [])
    png = f"{TMP}/ov{k:02d}.png"
    overlay(png, cap, end=(k == len(SEQ) - 1))
    out = f"{TMP}/p{k:02d}.mp4"
    fc = ("[0:v]split[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.12[bg];"
          f"[b]crop=iw*0.82:ih,scale={W}:-2[fg];"
          "[bg][fg]overlay=0:(H-h)/2-40[v];[v][1:v]overlay=0:0[o]")
    af = f"afade=t=in:d=0.04,afade=t=out:st={dur-0.06:.3f}:d=0.06"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st:.3f}", "-t", f"{dur:.3f}", "-i", FILM, "-i", png,
                    "-filter_complex", fc, "-map", "[o]", "-map", "0:a", "-af", af,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out], check=True)
    parts.append(out)

with open(f"{TMP}/list.txt", "w") as fh:
    fh.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt",
                "-af", "loudnorm=I=-14:TP=-2", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT],
               check=True)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT],
                         capture_output=True, text=True).stdout)
print(OUT, round(d, 2), "s")
