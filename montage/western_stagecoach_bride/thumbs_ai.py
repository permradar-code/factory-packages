#!/usr/bin/env python3
"""Re-packaging thumbnails for film 2 (The Stagecoach Bride, 9 Oct: no handcuffs, heroine with a gun) from the Flow / Nano Banana key art (owner-approved concepts, 9 Oct):
bright poster stills, one short yellow quote like film 1's winner ("THAT'S FAR ENOUGH.").
Usage: python3 thumbs_ai.py [srcdir] [outdir]
"""
import os, sys
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")
SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/stagecoach_bride/film2_thumbs_ai/flow"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/wsb_edit/thumbs_ai"
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 720

# (source, text, anchor point, anchor, size)
THUMBS = {
    "1_wrong_bride": ("D_2.png", "WRONG BRIDE.", (34, 26), "la", 100),
    "2_laugh_now": ("C_2.png", "LAUGH NOW.", (34, 26), "la", 104),
    "3_she_jumped": ("B_2.png", "SHE JUMPED!", (34, 26), "la", 96),
    "4_marry_me": ("A.png", "“MARRY ME?”", (34, 26), "la", 100),
}


def fit(im):
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def text(im, s, xy, anchor, size):
    f = ImageFont.truetype(FONT, size)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 5, xy[1] + 7), s, font=f, fill=(0, 0, 0, 160), anchor=anchor,
                            stroke_width=9, stroke_fill=(0, 0, 0, 160))
    im = Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(6))).convert("RGB")
    ImageDraw.Draw(im).text(xy, s, font=f, fill=(255, 214, 0), anchor=anchor, stroke_width=8, stroke_fill=(0, 0, 0))
    return im


for name, (src, s, xy, anchor, size) in THUMBS.items():
    im = fit(Image.open(os.path.join(SRC, src)).convert("RGB"))
    im = ImageEnhance.Sharpness(ImageEnhance.Contrast(im).enhance(1.04)).enhance(1.3)
    im = text(im, s, xy, anchor, size)
    p = os.path.join(OUT, name + ".jpg")
    im.save(p, quality=92)
    print(p, os.path.getsize(p))
