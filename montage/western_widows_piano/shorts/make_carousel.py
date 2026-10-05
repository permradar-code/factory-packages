#!/usr/bin/env python3
"""Image carousel (YouTube Post / Shorts feed) for "The Widow's Piano" — 9 cards, 4:5, 1080x1350."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

SRC = "/home/claude/car/src"
OUT = "/home/claude/car/out"
RYE = "/home/claude/sh/fonts/Rye-Regular.ttf"
INTER = "/home/claude/sh/fonts/Inter-ExtraBold.otf"
W, H = 1080, 1350
GOLD = (255, 214, 51)
WHITE = (255, 255, 255)
os.makedirs(OUT, exist_ok=True)

# (file, crop centre x as a fraction of width, lines [(text, font, size, colour)], top_label)
CARDS = [
    ("f_36.0.png", 0.50, [("THE WHOLE TOWN", "rye", 92, WHITE), ("CAME TO LAUGH", "rye", 92, WHITE), ("AT HER.", "rye", 92, GOLD)], True),
    ("I13.png", 0.47, [("Her mother's piano.", "inter", 64, WHITE), ("Sold to pay her late", "inter", 52, WHITE), ("husband's debt.", "inter", 52, WHITE)], False),
    ("f_33.6.png", 0.235, [("“Six dollars!", "rye", 76, GOLD), ("It will make", "rye", 76, GOLD), ("lovely kindling.”", "rye", 76, GOLD)], False),
    ("f_43.70.png", 0.47, [("Then a stranger", "inter", 64, WHITE), ("at the back of the crowd", "inter", 52, WHITE), ("raised one hand.", "inter", 64, WHITE)], False),
    ("f_50.2.png", 0.50, [("“Two hundred.", "rye", 96, GOLD), ("In gold.”", "rye", 96, GOLD)], False),
    ("I43.png", 0.53, [("That night, three riders", "inter", 58, WHITE), ("came down off the ridge", "inter", 58, WHITE), ("without a single light.", "inter", 58, WHITE)], False),
    ("I44.png", 0.52, [("They only lit their torches", "inter", 56, WHITE), ("when they reached", "inter", 56, WHITE), ("the barn.", "inter", 70, GOLD)], False),
    ("f_531.17.png", 0.51, [("“The next one", "rye", 96, GOLD), ("goes lower!”", "rye", 96, GOLD)], False),
    ("I46.png", 0.45, [("Who is the stranger?", "rye", 70, GOLD), ("And why did he come?", "inter", 54, WHITE), ("▶ Full story on the channel:", "inter", 46, WHITE), ("“The Widow's Piano”", "inter", 52, GOLD)], True),
]


def font(kind, size):
    return ImageFont.truetype(RYE if kind == "rye" else INTER, size)


def crop45(im, cx):
    iw, ih = im.size
    cw = int(ih * W / H)
    x = int(cx * iw - cw / 2)
    x = max(0, min(iw - cw, x))
    im = im.crop((x, 0, x + cw, ih)).resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))


def gradient(h0):
    g = Image.new("L", (1, H), 0)
    for y in range(H):
        a = 0 if y < h0 else int(235 * min(1, (y - h0) / (H - h0) * 1.6))
        g.putpixel((0, y), a)
    return g.resize((W, H))


def draw_text_block(im, lines, bottom_margin=90):
    d = ImageDraw.Draw(im)
    fonts = [font(k, s) for _, k, s, _ in lines]
    heights = [f.getbbox("Ag")[3] - f.getbbox("Ag")[1] for f in fonts]
    gap = 22
    total = sum(heights) + gap * (len(lines) - 1)
    y = H - bottom_margin - total
    for (txt, k, s, col), f, h in zip(lines, fonts, heights):
        tw = d.textlength(txt, font=f)
        x = (W - tw) / 2
        sw = 6 if k == "rye" else 5
        d.text((x, y - f.getbbox("Ag")[1]), txt, font=f, fill=col, stroke_width=sw, stroke_fill=(10, 8, 6))
        y += h + gap
    return total


for i, (fn, cx, lines, label) in enumerate(CARDS, 1):
    im = Image.open(f"{SRC}/{fn}").convert("RGB")
    im = crop45(im, cx)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    dark = Image.new("RGB", (W, H), (8, 6, 4))
    im = Image.composite(dark, im, gradient(int(H * 0.50)))
    draw_text_block(im, lines)
    d = ImageDraw.Draw(im)
    if label:  # channel name on the first and last card
        f = font("rye", 40)
        t = "TALES OF CEDAR BLUFF"
        d.text(((W - d.textlength(t, font=f)) / 2, 50), t, font=f, fill=WHITE, stroke_width=4, stroke_fill=(10, 8, 6))
    # slide counter, top-right
    f = font("inter", 30)
    t = f"{i}/{len(CARDS)}"
    d.text((W - 40 - d.textlength(t, font=f), 52 if not label else 110), t, font=f, fill=(235, 235, 235), stroke_width=3, stroke_fill=(10, 8, 6))
    im.save(f"{OUT}/card_{i:02d}.jpg", quality=93)
print("ok")
