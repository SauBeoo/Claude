"""Build channel identity for 人生哲学の夜話: logo (800x800) + banner (2560x1440).

All text drawn with a real font (Noto Serif JP) -- no AI-baked kanji, no watermark.
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

TITLE = "人生哲学の夜話"
TAGLINE = "眠る前に、心がほどける人生の話"

SKY_TOP = np.array([10, 16, 38], float)       # deep night navy
SKY_BOT = np.array([38, 44, 82], float)       # dusk indigo near horizon
MOON = (242, 214, 150)                        # warm moonlight
CREAM = (246, 236, 214)


def font(size, weight=700):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def sky(w, h, seed):
    t = np.linspace(0, 1, h)[:, None, None] ** 1.3
    img = SKY_TOP * (1 - t) + SKY_BOT * t
    img = np.broadcast_to(img, (h, w, 3)).copy()
    rng = np.random.default_rng(seed)
    img += rng.normal(0, 1.2, img.shape)        # fine grain, kills banding
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def stars(im, n, seed, box=None, rmax=2.2):
    rng = np.random.default_rng(seed)
    w, h = im.size
    x0, y0, x1, y1 = box or (0, 0, w, h)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(0.6, rmax) * (1 if rng.random() > 0.08 else 1.8)
        a = int(rng.uniform(90, 235))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 248, 230, a))
    glow = layer.filter(ImageFilter.GaussianBlur(2.5))
    im.alpha_composite(glow)
    im.alpha_composite(layer)


def moon(im, cx, cy, r, cut=0.36):
    """Crescent with a soft halo."""
    w, h = im.size
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - r * 2.2, cy - r * 2.2, cx + r * 2.2, cy + r * 2.2],
                                 fill=MOON + (60,))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(r * 0.9)))
    mask = Image.new("L", im.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    ox, oy = cx + r * cut * 1.5, cy - r * cut * 0.9
    md.ellipse([ox - r * 0.92, oy - r * 0.92, ox + r * 0.92, oy + r * 0.92], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    body = Image.new("RGBA", im.size, MOON + (255,))
    im.paste(body, (0, 0), mask)


def ridges(im, base_y, layers, seed):
    """Layered distant mountains, each darker and nearer."""
    rng = np.random.default_rng(seed)
    w, h = im.size
    xs = np.arange(w)
    for i, (off, amp, col) in enumerate(layers):
        ph = rng.uniform(0, 6.28, 4)
        y = (base_y + off
             + amp * (0.55 * np.sin(xs / w * 6.28 * 1.3 + ph[0])
                      + 0.30 * np.sin(xs / w * 6.28 * 3.1 + ph[1])
                      + 0.15 * np.sin(xs / w * 6.28 * 7.7 + ph[2])))
        poly = [(0, h)] + list(zip(xs.tolist(), y.tolist())) + [(w, h)]
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(poly, fill=col)
        im.alpha_composite(layer)


def text_center(d, cx, cy, s, f, fill, shadow=True):
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    x, y = cx - (x1 - x0) / 2 - x0, cy - (y1 - y0) / 2 - y0
    if shadow:
        d.text((x + 3, y + 4), s, font=f, fill=(0, 0, 0, 140))
    d.text((x, y), s, font=f, fill=fill)
    return x1 - x0, y1 - y0


def build_logo():
    S = 800
    im = sky(S, S, 7).convert("RGBA")
    stars(im, 70, 11, (60, 60, 740, 470), rmax=2.4)
    moon(im, 560, 215, 92)
    ridges(im, 610, [(0, 40, (30, 34, 62, 255)), (60, 30, (18, 21, 42, 255))], 3)
    d = ImageDraw.Draw(im)
    # 2 chars only: must stay legible at 98px in a circle crop
    text_center(d, S / 2, 455, "夜話", font(300, 800), CREAM)
    # thin inner ring keeps the mark readable against dark UI
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([22, 22, S - 22, S - 22], outline=MOON + (150,), width=6)
    im.alpha_composite(ring)
    return im.convert("RGB")


def build_banner():
    W, H = 2560, 1440
    im = sky(W, H, 5).convert("RGBA")
    stars(im, 900, 21, (0, 0, W, 1020))
    moon(im, 1905, 640, 112)                  # right half of safe area, clear of the title
    ridges(im, 1000, [(-40, 70, (40, 44, 80, 255)), (40, 55, (26, 29, 56, 255)),
                      (120, 40, (14, 17, 36, 255))], 9)
    d = ImageDraw.Draw(im)
    # safe area (all devices): 1546x423 centered -> x 507..2053, y 508..931
    text_center(d, 1150, 668, TITLE, font(150, 800), CREAM)
    line = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(line).line([(730, 772), (1570, 772)], fill=MOON + (170,), width=3)
    im.alpha_composite(line)
    d = ImageDraw.Draw(im)
    text_center(d, 1150, 842, TAGLINE, font(64, 500), MOON)
    return im.convert("RGB")


def main():
    OUT.mkdir(exist_ok=True)
    logo = build_logo()
    logo.save(OUT / "logo.png", optimize=True)
    # preview at real display sizes
    for px in (98, 48):
        p = logo.resize((px, px), Image.LANCZOS)
        m = Image.new("L", (px, px), 0)
        ImageDraw.Draw(m).ellipse([0, 0, px - 1, px - 1], fill=255)
        bg = Image.new("RGB", (px, px), (255, 255, 255))
        bg.paste(p, (0, 0), m)
        bg.save(OUT / f"_preview_logo_{px}.png")
    banner = build_banner()
    banner.save(OUT / "banner.png", optimize=True)
    # what a TV shows vs what desktop/mobile crops to
    banner.crop((0, 508, 2560, 931)).resize((1280, 212), Image.LANCZOS).save(OUT / "_preview_banner_desktop.png")
    banner.crop((507, 508, 2053, 931)).save(OUT / "_preview_banner_safe.png")
    for f in ("logo.png", "banner.png"):
        print(f, round((OUT / f).stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
