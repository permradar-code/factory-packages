#!/usr/bin/env python3
"""Three YouTube thumbnails (1280x720) for film 2 from real frames of the film + short text.
A: HER OWN GROOM   - the walk in handcuffs | the ladies laughing
B: SHE JUMPED      - the jump from the stagecoach with the box
C: I WORE IT FOR YOU - Agatha points | Rose in tears
Usage: python3 thumbs.py [outdir]
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
FIX, SRC = "/home/claude/wsb_fix1/visuals/video", "/mnt/user-data/uploads/stagecoach_bride/visuals/video"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wsb_edit/thumbs"
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


# ---------------- A: HER OWN GROOM
def thumb_a():
    walk = grade(frame("C60", 4.5))
    laugh = grade(frame("C102R", 1.5))
    im = Image.new("RGB", (W, H))
    LW = 790
    box = (330, 18, 762, 702)
    im.paste(panel(walk, box, (LW, H)), (0, 0))
    im.paste(panel(laugh, (250, 30, 400, 560), (W - LW, H)), (LW, 0))
    im = vignette(im, 0.22)
    divider(im, LW)
    # red ring on the handcuffs (C60 frame coords 587,640 -> panel coords)
    sx = LW / box[2]; cx, cy = (587 - box[0]) * sx, (640 - box[1]) * sx
    d = ImageDraw.Draw(im)
    for r, wdt, col in ((62, 12, (0, 0, 0)), (60, 8, (230, 20, 20))):
        d.ellipse((cx - r * 1.3, cy - r, cx + r * 1.3, cy + r), outline=col, width=wdt)
    mid = LW + (W - LW) // 2
    text(im, "HER OWN", (mid, H - 175), 132, anchor="ms", max_w=W - LW - 30)
    text(im, "GROOM", (mid, H - 30), 150, anchor="ms", max_w=W - LW - 30)
    return im


# ---------------- B: SHE JUMPED
def thumb_b():
    jump = grade(frame("C04", 1.0), bright=1.05, color=1.3)
    im = panel(jump, (360, 10, 900, 506), (W, H))
    im = vignette(im, 0.22)
    text(im, "SHE JUMPED", (40, H - 30), 170, anchor="ls")
    return im


# ---------------- C: I WORE IT FOR YOU
def thumb_c():
    aga = grade(frame("C61R", 3.0))
    rose = grade(frame("C103", 3.5), bright=1.1)
    im = Image.new("RGB", (W, H))
    im.paste(panel(aga, (300, 0, 640, 720), (600, H)), (0, 0))
    im.paste(panel(rose, (40, 30, 600, 650), (W - 600, H)), (600, 0))
    im = vignette(im, 0.25)
    divider(im, 600)
    text(im, "“I WORE IT FOR YOU”", (W // 2, H - 26), 112, anchor="ms", fill=(255, 255, 255), max_w=1220)
    return im


if __name__ == "__main__":
    for name, fn in (("A_her_own_groom", thumb_a), ("B_she_jumped", thumb_b), ("C_i_wore_it_for_you", thumb_c)):
        p = f"{OUT}/{name}.jpg"
        fn().save(p, quality=92)
        print(p, os.path.getsize(p))
    for f in os.listdir(OUT):
        if f.startswith("_"):
            os.remove(os.path.join(OUT, f))
