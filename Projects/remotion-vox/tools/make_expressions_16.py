# -*- coding: utf-8 -*-
r"""make_expressions_16.py — ve BO PICTOGRAM CAT GIAY (dau · sung · choang · lanh ·
hoi · vo le · ngu) cho video 16.

    py -3 tools/make_expressions_16.py

Vi sao VE chu khong gen anh: pictogram la hinh HINH HOC — ve bang PIL thi sac net,
lam lai duoc, doi mau/co trong mot dong, va khong ton luot gen cua user.

Chat lieu: GIAY CAT, khong phai manga bong bay —
  - mau PHANG lay tu palette kenh (navy #2A3A58 / vang #FFD700) + do dat, xanh nhat
  - VIEN TRANG day ~10px chay quanh silhouette (dilate alpha) = vet keo cat
  - khong gradient, khong glow, khong outline den
⚠️ Ly do rang buoc nay: kenh la anh tai lieu cho tep 60-80. Ky hieu kieu manga
   bong bay se doc ra "re tien" va pha style (cung tinh than voi lenh cam sticker
   hoat hinh o luat thumbnail).

Xuat -> public/projects/shokutaku-16-banana/assets/ex_*.png
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "projects" / "shokutaku-16-banana" / "assets"
S = 520                      # canvas vuong truoc khi crop
EDGE = 11                    # do day vien giay
NAVY = (42, 58, 88)
GOLD = (233, 179, 24)
RED = (176, 58, 48)
BLUE = (86, 124, 158)
FONT = r"C:\Windows\Fonts\arialbd.ttf"


def paper(im: Image.Image) -> Image.Image:
    """Them vien trang quanh silhouette + crop sat noi dung (giong process_cutout)."""
    a = np.array(im)
    mask = a[:, :, 3] > 40
    ring = ndimage.binary_dilation(mask, iterations=EDGE) & ~mask
    a[ring] = [255, 255, 255, 255]
    dil = ndimage.binary_dilation(mask, iterations=EDGE)
    ys, xs = np.where(dil)
    a = a[max(0, ys.min() - 6):ys.max() + 7, max(0, xs.min() - 6):xs.max() + 7]
    return Image.fromarray(a)


def itami():
    """ĐAU — sao gai (ZUKI). Nhon, khong deu -> doc ra 'nhoi'."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c, n = S // 2, 12
    pts = []
    for i in range(n * 2):
        r = (S * 0.46) if i % 2 == 0 else (S * 0.20)
        r *= 1 + 0.10 * math.sin(i * 2.1)      # lech nhe cho do may moc
        a = math.pi * i / n - math.pi / 2
        pts.append((c + r * math.cos(a), c + r * math.sin(a)))
    d.polygon(pts, fill=RED + (255,))
    return im


def mukumi():
    """SƯNG — khoi bau tron + 3 mui ten no ra ngoai."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = S // 2
    d.ellipse([c - 118, c - 96, c + 118, c + 96], fill=BLUE + (255,))
    for a_deg in (-90, 25, 155):
        a = math.radians(a_deg)
        x0, y0 = c + 128 * math.cos(a), c + 112 * math.sin(a)
        x1, y1 = c + 205 * math.cos(a), c + 188 * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=BLUE + (255,), width=26)
        h = 34
        d.polygon([(x1 + h * math.cos(a), y1 + h * math.sin(a)),
                   (x1 + h * math.cos(a + 2.5), y1 + h * math.sin(a + 2.5)),
                   (x1 + h * math.cos(a - 2.5), y1 + h * math.sin(a - 2.5))],
                  fill=BLUE + (255,))
    return im


def furatsuki():
    """CHOÁNG — xoan oc (kurakura)."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = S // 2
    pts = []
    for i in range(300):
        t = i / 300 * 4.6 * math.pi
        r = 18 + t * 15
        pts.append((c + r * math.cos(t), c + r * math.sin(t)))
    d.line(pts, fill=GOLD + (255,), width=27, joint="curve")
    return im


def hiyari():
    """LẠNH — ba giot/vach roi xuong."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (x, top, h) in enumerate(((150, 90, 250), (260, 40, 330), (370, 120, 220))):
        d.rounded_rectangle([x - 22, top, x + 22, top + h], radius=22, fill=BLUE + (255,))
        d.ellipse([x - 34, top + h - 34, x + 34, top + h + 34], fill=BLUE + (255,))
    return im


def glyph(ch, col, size=430):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    b = d.textbbox((0, 0), ch, font=f)
    d.text(((S - (b[2] - b[0])) / 2 - b[0], (S - (b[3] - b[1])) / 2 - b[1]),
           ch, font=f, fill=col + (255,))
    return im


def zzz():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (x, y, sz) in enumerate(((60, 300, 150), (185, 190, 190), (330, 60, 230))):
        f = ImageFont.truetype(FONT, sz)
        d.text((x, y), "Z", font=f, fill=NAVY + (255,))
    return im


SET = {
    "ex_itami": (itami, "ĐAU — nga/gay/va cham"),
    "ex_mukumi": (mukumi, "SUNG — nuoc dong o chan"),
    "ex_furatsuki": (furatsuki, "CHOANG — dung len hoa mat"),
    "ex_hiyari": (hiyari, "LANH — san lanh / mieng nhot"),
    "ex_hatena": (lambda: glyph("?", NAVY), "HOI — cau hoi mo"),
    "ex_hirameki": (lambda: glyph("!", GOLD), "VO LE — cu lat"),
    "ex_zzz": (zzz, "NGU — dem/tinh giac"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (fn, desc) in SET.items():
        p = paper(fn())
        p.save(OUT / f"{name}.png")
        print(f"  {name:14} {str(p.size):11} {desc}")
    print(f"\nOK -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
