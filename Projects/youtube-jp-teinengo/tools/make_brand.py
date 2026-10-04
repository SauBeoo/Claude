"""Build channel identity for 定年後のこころ研究室: logo (800x800) + banner (2560x1440).

All text drawn with a real font (Noto Serif JP) -- no AI-baked kanji, no watermark.
Motif: a morning sun rising over a soft hill, one person standing on it = "the second start".
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

TITLE = "定年後のこころ研究室"
TAGLINE = "定年後の毎日が、もう一度楽しくなる心理学"

BG_TOP = np.array([252, 246, 234], float)     # warm morning cream (bright bg for 45+)
BG_BOT = np.array([250, 226, 200], float)     # soft peach near horizon
INK = (44, 52, 70)
SUN = (238, 150, 72)
HILL = (132, 170, 128)
HILL2 = (104, 146, 108)
PERSON = (60, 72, 96)


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


def sun(im, cx, cy, r):
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - r * 1.9, cy - r * 1.9, cx + r * 1.9, cy + r * 1.9], fill=SUN + (70,))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(r * 0.6)))
    ImageDraw.Draw(im).ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)


def hill(im, cx, top_y, half_w, col):
    """Soft rounded hill: top half of a wide ellipse, filled down to the bottom edge."""
    w, h = im.size
    d = ImageDraw.Draw(im)
    d.ellipse([cx - half_w, top_y, cx + half_w, top_y + half_w * 0.9], fill=col)
    d.rectangle([cx - half_w, top_y + half_w * 0.45, cx + half_w, h], fill=col)


def person(im, cx, base_y, r):
    """Head + shoulders seen from behind, standing on the hill and facing the sun."""
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r, base_y - r * 3.3, cx + r, base_y - r * 1.3], fill=PERSON)
    d.pieslice([cx - r * 1.7, base_y - r * 1.15, cx + r * 1.7, base_y + r * 2.1], 180, 360, fill=PERSON)


def text_center(d, cx, cy, s, f, fill):
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    d.text((cx - (x1 - x0) / 2 - x0, cy - (y1 - y0) / 2 - y0), s, font=f, fill=fill)
    return x1 - x0


def build_logo():
    S = 800
    im = paper(S, S, 7)
    sun(im, 400, 330, 120)
    hill(im, 250, 360, 330, HILL2)
    hill(im, 560, 390, 360, HILL)
    person(im, 480, 432, 34)
    # cream plate under the text so it reads on the hill
    plate = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([130, 520, 670, 690], radius=40, fill=(252, 246, 234, 235))
    im.alpha_composite(plate)
    d = ImageDraw.Draw(im)
    text_center(d, S / 2, 605, "定年後", font(140, 800), INK)
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([20, 20, S - 20, S - 20], outline=INK + (200,), width=8)
    im.alpha_composite(ring)
    return im.convert("RGB")


def build_banner():
    W, H = 2560, 1440
    im = paper(W, H, 5)
    # safe area (all devices): 1546x423 centered -> x 507..2053, y 508..931
    sun(im, 760, 700, 90)
    hill(im, 640, 790, 260, HILL2)
    hill(im, 860, 810, 240, HILL)
    person(im, 800, 830, 26)
    d = ImageDraw.Draw(im)
    text_center(d, 1530, 650, TITLE, font(96, 800), INK)
    ImageDraw.Draw(im).line([(1120, 745), (1940, 745)], fill=SUN, width=4)
    text_center(d, 1530, 815, TAGLINE, font(46, 600), INK)
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
