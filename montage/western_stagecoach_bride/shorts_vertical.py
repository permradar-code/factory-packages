#!/usr/bin/env python3
"""Full-screen vertical Shorts (1080x1920) from native 9:16 clips (shorts1 batch V01..V13 + hooks H01/H02).
Each clip is trimmed to its speech (or kept whole if silent), shown full screen, with big 2-4-word captions
timed over the speech, a hook line at the top and "FULL MOVIE ON THE CHANNEL" on the last seconds.
Usage: python3 shorts_vertical.py [name ...]
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
V = "/mnt/user-data/uploads/stagecoach_bride/shorts1"
H = "/mnt/user-data/uploads/stagecoach_bride/visuals/video"
OUT = "/home/claude/wsb_edit/shorts_v"
W, HH = 1080, 1920
END = "FULL MOVIE ON THE CHANNEL"

LINES = {
    "V01": ["I promised you'd see me in it first.", "And you're under arrest, ma'am."],
    "V02": ["Look at her, ladies. Ordered by mail, delivered in irons."],
    "V03": ["I wore it for you, Caleb. Like I promised."],
    "V04": ["I didn't steal anything, Caleb.", "I know."],
    "V05": ["When I say jump, girl, you jump!"],
    "V06": ["She went up the mountain! Find her!"],
    "V09": ["Let her go, Crane."],
    "V11": ["Rose Calloway. Will you marry me? Properly, this time."],
    "V12": ["Yes. Yes, Caleb."],
    "V13": ["Not one word, Agatha."],
}
SHORTS = {
    "vshort_arrest": ("HER OWN GROOM\nARRESTED HER", ["V01", "V02", "V03", "V04"]),
    "vshort_jump": ("SHE JUMPED\nWITH THE BOX", ["V05", "H01", "V06", "V07"]),
    "vshort_proposal": ("THE TOWN LAUGHED…\nTHEN HE KNELT", ["V02", "V11", "V12", "V13"]),
}


def src(cid):
    return f"{H}/{cid}.mp4" if cid.startswith("H") else f"{V}/{cid}.mp4"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def speech_frames(p):
    sr = 16000
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-af", "highpass=f=150,lowpass=f=4000", "-ac", "1", "-ar",
                          str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = sr // 50
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    return db > max(db.max() - 22, -45)          # 20 ms frames


def segments(mask):
    segs, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        if not m and start is not None:
            segs.append([start, i]); start = None
    if start is not None:
        segs.append([start, len(mask)])
    merged = []
    for s in segs:                                 # bridge gaps < 0.2 s
        if merged and s[0] - merged[-1][1] < 10:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [(a * 0.02, b * 0.02) for a, b in merged if b - a >= 5]


def chunks(line, n=3):
    w = line.split()
    out, cur = [], []
    for word in w:
        cur.append(word)
        if len(cur) >= n or word[-1] in ".,!?":
            out.append(" ".join(cur)); cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def caption_plan(cid, d):
    """[(t0, t1, text)] relative to the clip, plus the trim window (a, b)."""
    lines = LINES.get(cid)
    if not lines:
        return [], (0.0, min(d, 5.0))
    segs = segments(speech_frames(src(cid)))
    if not segs:
        return [], (0.0, d)
    s0, s1 = segs[0][0], segs[-1][1]
    spans = [(s0, s1)]
    if len(lines) == 2 and len(segs) >= 2:        # split at the biggest pause
        gaps = [(segs[i + 1][0] - segs[i][1], i) for i in range(len(segs) - 1)]
        _, k = max(gaps)
        spans = [(s0, segs[k][1]), (segs[k + 1][0], s1)]
    elif len(lines) == 2:
        tot = sum(len(l) for l in lines); mid = s0 + (s1 - s0) * len(lines[0]) / tot
        spans = [(s0, mid), (mid, s1)]
    caps = []
    for line, (a, b) in zip(lines, spans):
        parts = chunks(line)
        tot = sum(len(p) for p in parts)
        t = a
        for p in parts:
            dt = (b - a) * len(p) / tot
            caps.append((t, t + dt, p)); t += dt
    a = max(0.0, s0 - 0.3)
    b = min(d, s1 + 0.6)
    return caps, (a, b)


def png(path, hook, text, end):
    im = Image.new("RGBA", (W, HH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.multiline_text((W // 2, 120), hook, font=ImageFont.truetype(FONT, 84), fill=(255, 214, 0), anchor="ma",
                     align="center", stroke_width=9, stroke_fill=(0, 0, 0), spacing=4)
    if text:
        f = ImageFont.truetype(FONT, 104)
        while d.textlength(text, font=f) > W - 110:
            f = ImageFont.truetype(FONT, f.size - 6)
        d.text((W // 2, 1180), text.upper(), font=f, fill=(255, 255, 255), anchor="ma", stroke_width=10,
               stroke_fill=(0, 0, 0))
    if end:
        d.text((W // 2, 1420), END, font=ImageFont.truetype(FONT, 66), fill=(255, 214, 0), anchor="ma",
               stroke_width=8, stroke_fill=(0, 0, 0))
    im.save(path)


def build(name, hook, seq):
    tmp = f"{OUT}/{name}_tmp"
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for k, cid in enumerate(seq):
        p = src(cid)
        d = dur(p)
        caps, (a, b) = caption_plan(cid, d)
        L = b - a
        last = k == len(seq) - 1
        # overlay timeline: one PNG per caption state
        states, t = [], 0.0
        events = sorted({0.0, L, *[max(0, c0 - a) for c0, _, _ in caps], *[min(L, c1 - a) for _, c1, _ in caps]}
                        | ({max(0.0, L - 2.0)} if last else set()))
        for i in range(len(events) - 1):
            t0, t1 = events[i], events[i + 1]
            if t1 - t0 < 0.02:
                continue
            mid = (t0 + t1) / 2 + a
            txt = next((c for c0, c1, c in caps if c0 <= mid < c1), "")
            states.append((t0, t1, txt, last and t0 >= L - 2.01))
        inputs, fc, prev = ["-ss", f"{a:.3f}", "-t", f"{L:.3f}", "-i", p], [], "[v0]"
        fc.append(f"[0:v]scale={W}:{HH}:flags=lanczos,eq=contrast=1.04:saturation=1.08,fps=24[v0]")
        for j, (t0, t1, txt, end) in enumerate(states):
            img = f"{tmp}/c{k:02d}_{j:02d}.png"
            png(img, hook, txt, end)
            inputs += ["-i", img]
            fc.append(f"{prev}[{j + 1}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})'[o{j}]")
            prev = f"[o{j}]"
        out = f"{tmp}/p{k:02d}.mp4"
        af = f"loudnorm=I=-16:TP=-2,afade=t=in:d=0.03,afade=t=out:st={max(0, L - 0.08):.3f}:d=0.08"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", prev,
                        "-map", "0:a", "-af", af, "-t", f"{L:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                        out], check=True)
        parts.append(out)
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in parts)
    out = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-af", "loudnorm=I=-14:TP=-2", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    print(out, round(dur(out), 1), "s")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or SHORTS):
        build(n, *SHORTS[n])
