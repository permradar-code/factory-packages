#!/usr/bin/env python3
"""Three YouTube thumbnails (1280x720) for film 3 from real frames + 2-3 huge words (TV audience, 65+).
A: $500 FOR THE BOY - the mother with the baby at the barn | Pike reading the bounty in the lightning
B: HE WAS A RANGER   - Wade and Pike, guns drawn at the gate
C: STAY ANYWAY       - Molly hugs Wade, Ellie on the porch
Usage: python3 thumbs.py [outdir]
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
FIX, SRC = "/mnt/user-data/uploads/stagecoach_bride/film3_barn_storm/flow", "/mnt/user-data/uploads/stagecoach_bride/film3_barn_storm/src/visuals/video"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wbs_edit/thumbs"
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 720


def frame(cid, t):
    p = f"{FIX}/{cid}.mp4" if os.path.exists(f"{FIX}/{cid}.mp4") else f"{SRC}/{cid}.mp4"
    png = f"{OUT}/_{cid}_{t}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf", "scale=1280:720", png], check=True)
    return Image.open(png).convert("RGB")


def grade(im, bright=1.07, contrast=1.14, color=1.28, sharp=1.6):
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    return ImageEnhance.Sharpness(im).enhance(sharp)


def panel(im, box, size):
    """crop box (x, y, w, h) and fit to size, keeping the box aspect by trimming"""
    x, y, w, h = box
    tw, th = size
    if w / h > tw / th:
        nw = h * tw / th; x += (w - nw) / 2; w = nw
    else:
        nh = w * th / tw; y += (h - nh) / 2; h = nh
    return im.crop((int(x), int(y), int(x + w), int(y + h))).resize(size, Image.LANCZOS)


def vignette(im, strength=0.35):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((-W * 0.25, -H * 0.3, W * 1.25, H * 1.3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(120))
    dark = ImageEnhance.Brightness(im).enhance(1 - strength)
    return Image.composite(im, dark, m)


def text(im, s, xy, size, fill=(255, 214, 0), anchor="la", stroke=10, max_w=None):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    while max_w and d.textlength(s, font=f) > max_w and size > 40:
        size -= 4; f = ImageFont.truetype(FONT, size)
    # soft shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=f, fill=(0, 0, 0, 170), anchor=anchor,
                            stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
    im.paste(Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(6))).convert("RGB"))
    d = ImageDraw.Draw(im)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke)


def divider(im, x):
    d = ImageDraw.Draw(im)
    d.rectangle((x - 4, 0, x + 4, H), fill=(0, 0, 0))
    d.rectangle((x - 1, 0, x + 1, H), fill=(255, 255, 255))


# ---------------- A: $500 FOR THE BOY
def thumb_a():
    mom = grade(frame("C01", 2.0), bright=1.18, color=1.25)
    pike = grade(frame("C07", 6.0), bright=1.0, color=1.15)
    im = Image.new("RGB", (W, H))
    LW = 660
    im.paste(panel(mom, (300, 20, 640, 700), (LW, H)), (0, 0))
    im.paste(panel(pike, (330, 0, 620, 720), (W - LW, H)), (LW, 0))
    im = vignette(im, 0.2)
    divider(im, LW)
    text(im, "$500", (LW + (W - LW) // 2, 300), 190, anchor="ma", fill=(255, 214, 0))
    text(im, "FOR THE BOY", (W // 2, H - 22), 118, anchor="ms", fill=(255, 255, 255), max_w=1220)
    return im


# ---------------- B: HE WAS A RANGER
def thumb_b():
    gate = grade(frame("C69", 3.0), bright=1.1, color=1.3)
    im = panel(gate, (100, 10, 1080, 608), (W, H))
    im = vignette(im, 0.22)
    text(im, "HE WAS A", (W // 2, H - 170), 100, anchor="ms", fill=(255, 255, 255))
    text(im, "TEXAS RANGER", (W // 2, H - 24), 150, anchor="ms", fill=(255, 214, 0), max_w=1220)
    return im


# ---------------- C: STAY ANYWAY
def thumb_c():
    hug = grade(frame("C83", 3.0), bright=1.08, color=1.25)
    im = panel(hug, (300, 0, 960, 540), (W, H))
    im = vignette(im, 0.2)
    text(im, "“STAY ANYWAY”", (W // 2, 12), 150, anchor="ma", fill=(255, 214, 0), max_w=1200)
    return im


if __name__ == "__main__":
    for name, fn in (("A_500_for_the_boy", thumb_a), ("B_texas_ranger", thumb_b), ("C_stay_anyway", thumb_c)):
        p = f"{OUT}/{name}.jpg"
        fn().save(p, quality=92)
        print(p, os.path.getsize(p))
    for f in os.listdir(OUT):
        if f.startswith("_"):
            os.remove(os.path.join(OUT, f))
