#!/usr/bin/env python3
"""Vertical Shorts (1080x1920) from the finished film + the native vertical hook clips H01..H03.
Film segments: picture + mixed sound cut from the film, over a blurred copy, big caption under the picture.
Vertical clips: full screen with their own sound.
Usage: python3 shorts.py [name ...]     (default: all)
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
FILM = "/home/claude/wsb_edit/stagecoach_bride.mp4"
VERT = "/mnt/user-data/uploads/stagecoach_bride/visuals/video"
EDL = json.load(open("/home/claude/wsb_edit/edl_timed.json"))
OUTDIR = "/home/claude/wsb_edit/shorts"
W, H = 1080, 1920
END = "FULL MOVIE ON THE CHANNEL"
ev = {e["id"]: e for e in EDL["events"]}

SHORTS = {
    "short_jump": ("SHE JUMPED\nWITH THE BOX", [("film", "C03"), ("film", "C33"), ("vert", "H01"), ("film", "C05"),
                                                ("film", "C35")]),
    "short_box": ("SHE STILL HAD\nTHE BOX", [("film", "C87"), ("film", "C90"), ("film", "C91"), ("vert", "H02"),
                                            ("film", "C94")]),
    "short_fire": ("THEY SET THE JAIL\nON FIRE", [("film", "C67"), ("vert", "H03"), ("film", "C69"), ("film", "C70"),
                                                  ("film", "C68", 3.0)]),
}


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


def overlay(path, hook, caption, end, cap_y=1395):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.multiline_text((W // 2, 150), hook, font=ImageFont.truetype(FONT, 104), fill=(255, 214, 0), anchor="ma",
                     align="center", stroke_width=10, stroke_fill=(0, 0, 0), spacing=6)
    if caption:
        fc = ImageFont.truetype(FONT, 76)
        d.multiline_text((W // 2, cap_y), wrap(d, caption, fc, W - 120), font=fc, fill=(255, 255, 255), anchor="ma",
                         align="center", stroke_width=8, stroke_fill=(0, 0, 0), spacing=10)
    if end:
        d.text((W // 2, 1700), END, font=ImageFont.truetype(FONT, 70), fill=(255, 214, 0), anchor="ma",
               stroke_width=8, stroke_fill=(0, 0, 0))
    im.save(path)


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def build(name, hook, seq):
    tmp = f"{OUTDIR}/{name}_tmp"
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for k, item in enumerate(seq):
        kind, cid = item[0], item[1]
        last = k == len(seq) - 1
        png, out = f"{tmp}/ov{k:02d}.png", f"{tmp}/p{k:02d}.mp4"
        if kind == "film":
            e = ev[cid]
            st, dur = e["rstart"], (item[2] if len(item) > 2 else e["dur"])
            overlay(png, hook, " ".join(x["line"] for x in e.get("dialogue") or []), last)
            fc = ("[0:v]split[a][b];"
                  f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.12[bg];"
                  f"[b]crop=iw*0.82:ih,scale={W}:-2[fg];[bg][fg]overlay=0:(H-h)/2-40[v];[v][1:v]overlay=0:0[o]")
            af = f"afade=t=in:d=0.04,afade=t=out:st={dur-0.06:.3f}:d=0.06"
            cmd = ["-ss", f"{st:.3f}", "-t", f"{dur:.3f}", "-i", FILM]
        else:
            src = f"{VERT}/{cid}.mp4"
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                       capture_output=True, text=True).stdout)
            overlay(png, hook, "", last)
            fc = f"[0:v]scale={W}:{H}:flags=lanczos,eq=contrast=1.05:saturation=1.1[v];[v][1:v]overlay=0:0[o]"
            af = f"loudnorm=I=-17:TP=-2,afade=t=in:d=0.04,afade=t=out:st={dur-0.06:.3f}:d=0.06"
            cmd = ["-i", src]
        subprocess.run(["ffmpeg", "-v", "error", "-y", *cmd, "-i", png, "-filter_complex", fc, "-map", "[o]",
                        "-map", "0:a", "-af", af, "-t", f"{dur:.3f}", *ENC, out], check=True)
        parts.append(out)
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    out = f"{OUTDIR}/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-af", "loudnorm=I=-14:TP=-2", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                             capture_output=True, text=True).stdout)
    print(out, round(d, 1), "s")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    for n in (sys.argv[1:] or SHORTS):
        build(n, *SHORTS[n])
