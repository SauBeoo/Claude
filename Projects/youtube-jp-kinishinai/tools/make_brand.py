"""Build channel identity for 他人の目を気にしない心理学: logo (800x800) + banner (2560x1440).

All text drawn with a real font (Noto Serif JP) -- no AI-baked kanji, no watermark.
Motif: one person in colour standing upright, a few faded grey figures around them
= "the others are there, but they no longer weigh on you".
Usage: python tools/make_brand.py            -> 00_BRAND/logo.png, banner.png + previews
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "00_BRAND"
FONT = OUT / "assets" / "NotoSerifJP.ttf"

TITLE = "他人の目を気にしない心理学"
TAGLINE = "60代からは、自分の気持ちを大切に生きる"

BG_TOP = np.array([244, 248, 250], float)     # airy pale sky (bright bg for 45+)
BG_BOT = np.array([226, 236, 242], float)
INK = (40, 50, 72)
HERO = (70, 128, 178)                         # the viewer: clear blue
GHOST = (176, 184, 194)                       # the others: faded grey
ACCENT = (232, 164, 76)


def font(size, weight=700):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def paper(w, h, seed):
    t = np.linspace(0, 1, h)[:, None, None]
    img = BG_TOP * (1 - t) + BG_BOT * t
    img = np.broadcast_to(img, (h, w, 3)).copy()
    img += np.random.default_rng(seed).normal(0, 1.4, img.shape)   # grain, kills banding
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


def person(im, cx, base_y, r, col, alpha=255):
    """Head + shoulders, the same figure family as kyori/teinengo."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, base_y - r * 3.3, cx + r, base_y - r * 1.3], fill=col + (alpha,))
    d.pieslice([cx - r * 1.7, base_y - r * 1.15, cx + r * 1.7, base_y + r * 2.1], 180, 360, fill=col + (alpha,))
    im.alpha_composite(layer)


def glow(im, cx, cy, r):
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT + (90,))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(r * 0.45)))


def text_center(d, cx, cy, s, f, fill):
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    d.text((cx - (x1 - x0) / 2 - x0, cy - (y1 - y0) / 2 - y0), s, font=f, fill=fill)
    return x1 - x0


def build_logo():
    S = 800
    im = paper(S, S, 7)
    # the others: small, faded, kept back; the viewer: large, in colour, centred
    for cx, r in ((175, 40), (625, 40), (270, 30), (530, 30)):
        person(im, cx, 440, r, GHOST, 150)
    glow(im, 400, 330, 190)
    person(im, 400, 440, 62, HERO)
    d = ImageDraw.Draw(im)
    text_center(d, S / 2, 600, "気にしない", font(104, 800), INK)
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([20, 20, S - 20, S - 20], outline=INK + (200,), width=8)
    im.alpha_composite(ring)
    return im.convert("RGB")


def build_banner():
    W, H = 2560, 1440
    im = paper(W, H, 5)
    # safe area (all devices): 1546x423 centered -> x 507..2053, y 508..931
    for cx, r in ((600, 28), (900, 28), (660, 22), (840, 22)):
        person(im, cx, 800, r, GHOST, 150)
    glow(im, 750, 720, 150)
    person(im, 750, 800, 46, HERO)
    d = ImageDraw.Draw(im)
    text_center(d, 1480, 650, TITLE, font(78, 800), INK)
    ImageDraw.Draw(im).line([(1080, 745), (1880, 745)], fill=ACCENT, width=4)
    text_center(d, 1480, 815, TAGLINE, font(46, 600), INK)
    return im.convert("RGB")


def main():
    OUT.mkdir(exist_ok=True)
    logo = build_logo()
    logo.save(OUT / "logo.png", optimize=True)
    for px in (98, 48):
        p = logo.resize((px, px), Image.LANCZOS)
        m = Image.new("L", (px, px), 0)
        ImageDraw.Draw(m).ellipse([0, 0, px - 1, px - 1], fill=255)
        bg = Image.new("RGB", (px, px), (255, 255, 255))
        bg.paste(p, (0, 0), m)
        bg.save(OUT / f"_preview_logo_{px}.png")
    banner = build_banner()
    banner.save(OUT / "banner.png", optimize=True)
    banner.crop((0, 508, 2560, 931)).resize((1280, 212), Image.LANCZOS).save(OUT / "_preview_banner_desktop.png")
    banner.crop((507, 508, 2053, 931)).save(OUT / "_preview_banner_safe.png")
    for f in ("logo.png", "banner.png"):
        print(f, round((OUT / f).stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
