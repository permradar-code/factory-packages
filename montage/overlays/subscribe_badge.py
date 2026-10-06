"""Animated "Subscribe" badge for Tales of Cedar Bluff (western style).

Renders a transparent overlay clip (MOV, PNG codec with alpha) that slides in at the
bottom-left, a cursor clicks SUBSCRIBE, the button turns grey, the bell rings, and the
badge slides out. Optional preview: composite over a piece of a film.

Usage:
  python subscribe_badge.py --out badge.mov [--preview film.mp4 --at 275 --preview-out prev.mp4]
"""
import argparse, math, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
W, H, FPS, DUR = 1920, 1080, 30, 5.5
S = 2  # supersampling for the badge region

GOLD = (214, 176, 98)
CREAM = (240, 228, 200)
WOOD = (38, 24, 15)
RED = (196, 30, 36)
GREY = (90, 90, 90)

CARD_W, CARD_H = 660, 150
X0, Y0 = 80, H - 80 - CARD_H  # resting position (bottom-left, TV-safe margin)
REG_W, REG_H = 900, 330       # region rendered per frame (card + cursor room)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size * S)


F_TITLE = font("Rye-Regular.ttf", 34)
F_MONO = font("Rye-Regular.ttf", 40)
F_SUB = font("Inter-ExtraBold.otf", 21)
F_BTN = font("Inter-ExtraBold.otf", 23)


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in(t):
    return t ** 3


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def draw_bell(angle, rays):
    sz = 70 * S
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = sz // 2
    r = 17 * S
    d.pieslice([c - r, c - r - 6 * S, c + r, c + r - 6 * S], 180, 360, fill=CREAM)
    d.polygon([(c - r, c - 6 * S), (c + r, c - 6 * S), (c + r + 5 * S, c + 12 * S), (c - r - 5 * S, c + 12 * S)], fill=CREAM)
    d.rounded_rectangle([c - r - 8 * S, c + 10 * S, c + r + 8 * S, c + 15 * S], radius=2 * S, fill=CREAM)
    d.ellipse([c - 5 * S, c + 15 * S, c + 5 * S, c + 23 * S], fill=CREAM)
    d.ellipse([c - 3 * S, c - r - 11 * S, c + 3 * S, c - r - 5 * S], fill=CREAM)
    im = im.rotate(angle, resample=Image.BICUBIC, center=(c, c - r))
    if rays > 0:
        d = ImageDraw.Draw(im)
        a = int(255 * rays)
        for side in (-1, 1):
            for ang in (-35, 0, 35):
                rad = math.radians(ang)
                x1 = c + side * (24 * S) * math.cos(rad)
                y1 = c - 4 * S + (24 * S) * math.sin(rad)
                x2 = c + side * (33 * S) * math.cos(rad)
                y2 = c - 4 * S + (33 * S) * math.sin(rad)
                d.line([(x1, y1), (x2, y2)], fill=GOLD + (a,), width=3 * S)
    return im


def draw_cursor():
    sz = 60 * S
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
    pts = [(4 * S + x * S, 4 * S + y * S) for x, y in pts]
    d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0))
    d.line(pts + [pts[0]], fill=(0, 0, 0), width=2 * S)
    return im


CURSOR = draw_cursor()


def badge_frame(t):
    """Return (RGBA region image at 1x, x offset of region) for time t."""
    # slide in / out
    if t < 0.5:
        p = ease_out(t / 0.5)
    elif t > DUR - 0.6:
        p = 1 - ease_in((t - (DUR - 0.6)) / 0.6)
    else:
        p = 1.0
    dx = int((1 - p) * -(CARD_W + 120))
    alpha = clamp(p * 1.4)

    clicked = t >= 1.75
    press = 1.6 <= t < 1.75

    reg = Image.new("RGBA", (REG_W * S, REG_H * S), (0, 0, 0, 0))
    # card shadow
    sh = Image.new("RGBA", reg.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([10 * S, 70 * S, (10 + CARD_W) * S, (70 + CARD_H) * S],
                                         radius=22 * S, fill=(0, 0, 0, 150))
    reg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * S)))

    d = ImageDraw.Draw(reg)
    cx, cy = 0, 60 * S  # card top-left inside region
    d.rounded_rectangle([cx, cy, cx + CARD_W * S, cy + CARD_H * S], radius=22 * S,
                        fill=WOOD + (235,), outline=GOLD, width=3 * S)
    d.rounded_rectangle([cx + 7 * S, cy + 7 * S, cx + (CARD_W - 7) * S, cy + (CARD_H - 7) * S],
                        radius=17 * S, outline=GOLD + (110,), width=1 * S)
    # monogram medallion
    mx, my, mr = cx + 78 * S, cy + 75 * S, 50 * S
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(60, 38, 22), outline=GOLD, width=3 * S)
    d.ellipse([mx - mr + 7 * S, my - mr + 7 * S, mx + mr - 7 * S, my + mr - 7 * S], outline=GOLD + (120,), width=1 * S)
    d.text((mx, my + 2 * S), "CB", font=F_MONO, fill=GOLD, anchor="mm")
    # titles
    tx = cx + 146 * S
    d.text((tx, cy + 42 * S), "Tales of Cedar Bluff", font=F_TITLE, fill=GOLD, anchor="lm")
    d.text((tx, cy + 80 * S), "A NEW STORY EVERY WEEK", font=F_SUB, fill=CREAM, anchor="lm")
    # button
    bw, bh = 214, 50
    bx, by = tx, cy + 96 * S
    sc = 0.93 if press else 1.0
    bcx, bcy = bx + bw * S / 2, by + bh * S / 2
    hw, hh = bw * S * sc / 2, bh * S * sc / 2
    d.rounded_rectangle([bcx - hw, bcy - hh, bcx + hw, bcy + hh], radius=int(hh),
                        fill=GREY if clicked else RED)
    label = "SUBSCRIBED  ✓" if clicked else "SUBSCRIBE"
    d.text((bcx, bcy + 1 * S), label, font=F_BTN, fill=(255, 255, 255), anchor="mm")
    # click ripple
    if 1.65 <= t < 2.2:
        q = (t - 1.65) / 0.55
        rr = (16 + 34 * q) * S
        d.ellipse([bcx + 30 * S - rr, bcy - rr, bcx + 30 * S + rr, bcy + rr],
                  outline=(255, 255, 255, int(170 * (1 - q))), width=2 * S)
    # bell
    angle, rays = 0.0, 0.0
    if 1.85 <= t < 2.9:
        q = (t - 1.85) / 1.05
        angle = 22 * math.sin(q * math.pi * 6) * (1 - q)
        rays = math.sin(q * math.pi)
    bell = draw_bell(angle, rays)
    reg.alpha_composite(bell, (int(bx + (bw + 22) * S), int(by - 10 * S)))

    # cursor: moves in 0.8-1.6, clicks, leaves 2.3-3.0
    if 0.8 <= t < 3.0:
        tgt = (bcx + 30 * S, bcy + 6 * S)
        start = (tgt[0] + 260 * S, tgt[1] + 150 * S)
        if t < 1.6:
            q = ease_out((t - 0.8) / 0.8)
            pos = (start[0] + (tgt[0] - start[0]) * q, start[1] + (tgt[1] - start[1]) * q)
            ca = clamp((t - 0.8) / 0.2)
        elif t < 2.3:
            pos, ca = tgt, 1.0
        else:
            q = ease_in((t - 2.3) / 0.7)
            pos = (tgt[0] + 200 * S * q, tgt[1] + 120 * S * q)
            ca = 1 - q
        cur = CURSOR.copy()
        if ca < 1:
            cur.putalpha(cur.getchannel("A").point(lambda v: int(v * ca)))
        reg.alpha_composite(cur, (int(pos[0]), int(pos[1])))

    reg = reg.resize((REG_W, REG_H), Image.LANCZOS)
    if alpha < 1:
        reg.putalpha(reg.getchannel("A").point(lambda v: int(v * alpha)))
    return reg, dx


def render(out_mov):
    tmp = tempfile.mkdtemp()
    n = int(DUR * FPS)
    for i in range(n):
        t = i / FPS
        reg, dx = badge_frame(t)
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fr.alpha_composite(reg, (X0 + dx, Y0 - 60)) if X0 + dx >= 0 else fr.paste(reg, (X0 + dx, Y0 - 60), reg)
        fr.save(os.path.join(tmp, f"f{i:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i",
                    os.path.join(tmp, "f%04d.png"), "-c:v", "png", "-pix_fmt", "rgba", out_mov], check=True)
    return out_mov


def preview(badge, film, at, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(at), "-t", str(DUR), "-i", film,
                    "-i", badge, "-filter_complex",
                    "[0:v]scale=1920:1080,setsar=1[b];[b][1:v]overlay=0:0:format=auto,scale=1280:720[v]",
                    "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "128k", "-shortest", out], check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="subscribe_badge.mov")
    ap.add_argument("--preview")
    ap.add_argument("--at", type=float, default=275)
    ap.add_argument("--preview-out", default="subscribe_preview.mp4")
    a = ap.parse_args()
    render(a.out)
    if a.preview:
        preview(a.out, a.preview, a.at, a.preview_out)
