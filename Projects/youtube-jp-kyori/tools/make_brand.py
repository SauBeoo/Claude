"""Build channel identity for 心の距離の心理学: logo (800x800) + banner (2560x1440).

All text drawn with a real font (Noto Serif JP) -- no AI-baked kanji, no watermark.
Motif: two soft circles (two people) with a dashed gap between them = "distance of the heart".
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

TITLE = "心の距離の心理学"
TAGLINE = "60代からの人間関係を、心理学でひもとく"

BG_TOP = np.array([250, 244, 232], float)     # warm cream (bright bg for 45+)
BG_BOT = np.array([240, 228, 208], float)
INK = (38, 48, 72)                            # deep navy text
TERRA = (214, 120, 92)                        # person A
SAGE = (118, 160, 140)                        # person B
DASH = (160, 140, 120)


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


def person(im, cx, cy, r, col):
    """Head circle + shoulder arc, with a soft shadow."""
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse([cx - r, cy - r + 10, cx + r, cy + r + 10], fill=(90, 70, 50, 60))
    sd.pieslice([cx - r * 1.7, cy + r * 1.15 + 10, cx + r * 1.7, cy + r * 4.4 + 10], 180, 360,
                fill=(90, 70, 50, 60))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r * 0.25)))
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.pieslice([cx - r * 1.7, cy + r * 1.15, cx + r * 1.7, cy + r * 4.4], 180, 360, fill=col)


def dashes(im, x0, x1, y, width, seg, gap):
    d = ImageDraw.Draw(im)
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + seg, x1), y)], fill=DASH, width=width)
        x += seg + gap


def text_center(d, cx, cy, s, f, fill):
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    d.text((cx - (x1 - x0) / 2 - x0, cy - (y1 - y0) / 2 - y0), s, font=f, fill=fill)
    return x1 - x0


def build_logo():
    S = 800
    im = paper(S, S, 7)
    # two people, a gap between them -- the whole idea of the channel in one glance
    person(im, 245, 250, 78, TERRA)
    person(im, 555, 250, 78, SAGE)
    dashes(im, 345, 460, 272, 10, 18, 14)
    d = ImageDraw.Draw(im)
    text_center(d, S / 2, 590, "心の距離", font(128, 800), INK)
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([20, 20, S - 20, S - 20], outline=INK + (200,), width=8)
    im.alpha_composite(ring)
    return im.convert("RGB")


def build_banner():
    W, H = 2560, 1440
    im = paper(W, H, 5)
    # safe area (all devices): 1546x423 centered -> x 507..2053, y 508..931
    person(im, 640, 650, 52, TERRA)
    person(im, 890, 650, 52, SAGE)
    dashes(im, 708, 822, 668, 7, 14, 11)
    d = ImageDraw.Draw(im)
    text_center(d, 1510, 650, TITLE, font(120, 800), INK)
    ImageDraw.Draw(im).line([(1100, 752), (1920, 752)], fill=TERRA, width=4)
    text_center(d, 1510, 822, TAGLINE, font(52, 600), INK)
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
