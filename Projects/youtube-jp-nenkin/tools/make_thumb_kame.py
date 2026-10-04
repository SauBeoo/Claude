# -*- coding: utf-8 -*-
"""Thumbnail khuon KAME (カメ先生のもらえるお金) — 0 mat nguoi, chu chay tron be ngang.

Can cu: CHANNEL_BENCHMARK_takaichi-face_2026-09-07.md
  - kenh moi chay nhanh nhat ngach (37 ngay -> 5.460 sub) dung khuon nay, 0/9 thumbnail co mat
  - bo cast => hero lay tron be ngang (audience-45plus.md §6.10: BE NGANG mua legibility)

Cau truc: chip DOI TUONG (vang) -> hero 1-2 dong (trang + vang) -> [dong phu] -> dai do day.
Chu ve bang Noto Sans JP Black => luon sac net, khong bao gio nat kanji nhu anh AI gen.

Chay:  python tools/make_thumb_kame.py <slug-folder> [--only T2]
"""
import io, sys, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from PIL import Image, ImageDraw, ImageFont

W, H = 1376, 768
FONTDIR = Path(r"E:\Claude\Projects\_media_library\fonts")
BLACK_F = str(FONTDIR / "NotoSansJP-Black.otf")
BOLD_F  = str(FONTDIR / "NotoSansJP-Bold.otf")

NAVY_T   = (13, 28, 52)      # nen tren
NAVY_B   = (24, 47, 82)      # nen duoi
CHIP_BG  = (255, 212, 0)
CHIP_FG  = (12, 26, 48)
WHITE    = (255, 255, 255)
YELLOW   = (255, 214, 62)
BAR_BG   = (206, 27, 42)
BAR_FG   = (255, 255, 255)
STRIKE   = (232, 40, 46)

CHIP_Y0, CHIP_H = 16, 86
HERO_Y0, HERO_Y1 = 116, 614
BAR_Y0 = 628
HERO_W = int(W * 0.93)
GAP = 22
BAR_PAD_R = 110          # chua trong goc duoi-PHAI cho timestamp YouTube


def f(path, s):
    return ImageFont.truetype(path, s)


def tsize(d, txt, fnt):
    x0, y0, x1, y1 = d.textbbox((0, 0), txt, font=fnt)
    return x1 - x0, y1 - y0, x0, y0


def fit(d, txt, maxw, maxh, path=BLACK_F, lo=20, hi=420):
    """Co chu lon nhat ma van lot maxw x maxh."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        w, h, _, _ = tsize(d, txt, f(path, mid))
        if w <= maxw and h <= maxh:
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    return best


def draw_centered(d, txt, fnt, cy, color, y_is_top=False):
    w, h, ox, oy = tsize(d, txt, fnt)
    x = (W - w) // 2 - ox
    y = (cy if y_is_top else cy - h // 2) - oy
    d.text((x, y), txt, font=fnt, fill=color)
    return (x + ox, y + oy, x + ox + w, y + oy + h)


def build(spec, out: Path):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)

    # nen navy gradient doc
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(NAVY_T[i] + (NAVY_B[i] - NAVY_T[i]) * t) for i in range(3)))

    # ---- chip DOI TUONG
    chip = spec["chip"]
    cs = fit(d, chip, int(W * 0.82), CHIP_H - 26, BOLD_F, hi=90)
    cf = f(BOLD_F, cs)
    cw, ch, ox, oy = tsize(d, chip, cf)
    bw, bh = cw + 56, CHIP_H
    bx = (W - bw) // 2
    d.rounded_rectangle([bx, CHIP_Y0, bx + bw, CHIP_Y0 + bh], radius=14, fill=CHIP_BG)
    d.text((bx + 28 - ox, CHIP_Y0 + (bh - ch) // 2 - oy), chip, font=cf, fill=CHIP_FG)

    # ---- hero: co tung dong theo BE NGANG truoc, roi ha deu neu vuot chieu cao
    lines = spec["hero"]                      # [{"t":..,"c":"w"|"y","strike":bool}]
    sub = spec.get("sub")
    budget = HERO_Y1 - HERO_Y0
    if sub:
        budget -= 74
    sizes = [fit(d, L["t"], HERO_W, budget) for L in lines]
    hs = [tsize(d, L["t"], f(BLACK_F, s))[1] for L, s in zip(lines, sizes)]
    total = sum(hs) + GAP * (len(lines) - 1)
    if total > budget:
        k = budget / total
        sizes = [max(20, int(s * k)) for s in sizes]
        hs = [tsize(d, L["t"], f(BLACK_F, s))[1] for L, s in zip(lines, sizes)]
        total = sum(hs) + GAP * (len(lines) - 1)

    y = HERO_Y0 + (HERO_Y1 - HERO_Y0 - total - (74 if sub else 0)) // 2
    boxes = []
    for L, s, h in zip(lines, sizes, hs):
        col = YELLOW if L.get("c") == "y" else WHITE
        bb = draw_centered(d, L["t"], f(BLACK_F, s), y, col, y_is_top=True)
        boxes.append((bb, s, h))
        n = L.get("strike_n")
        if n:
            # gach do CHI tren n ky tu dau (con so cu), gan ngang — gach ca cau lam mat doc
            x0, y0, x1, y1 = bb
            sw = tsize(d, L["t"][:n], f(BLACK_F, s))[0]
            xa, xb = x0 - 14, x0 + sw + 14
            ym = (y0 + y1) // 2
            dy = int(h * 0.07)
            d.line([(xa, ym + dy), (xb, ym - dy)], fill=STRIKE, width=max(11, int(h * 0.10)))
        y += h + GAP

    if sub:
        sf = f(BOLD_F, fit(d, sub, int(W * 0.86), 60, BOLD_F, hi=70))
        draw_centered(d, sub, sf, y + 6, (226, 234, 246), y_is_top=True)

    # ---- dai do day
    d.rectangle([0, BAR_Y0, W, H], fill=BAR_BG)
    bar = spec["bar"]
    bs = fit(d, bar, W - 80 - BAR_PAD_R, (H - BAR_Y0) - 34, BOLD_F, hi=110)
    bf = f(BOLD_F, bs)
    bw2, bh2, ox2, oy2 = tsize(d, bar, bf)
    bx2 = (W - BAR_PAD_R - bw2) // 2
    d.text((bx2 - ox2, BAR_Y0 + ((H - BAR_Y0) - bh2) // 2 - oy2), bar, font=bf, fill=BAR_FG)

    im.save(out)
    prev = out.with_name(out.stem + "_prev168.png")
    im.resize((168, 94), Image.LANCZOS).save(prev)
    im.resize((120, 67), Image.LANCZOS).save(out.with_name(out.stem + "_prev120.png"))

    hero_h = max(h for _, _, h in boxes)
    hero_w = max(bb[2] - bb[0] for bb, _, _ in boxes)
    print(f"  {out.name}  hero cao {hero_h}px = {hero_h/H*100:.1f}% khung"
          f" · rong {hero_w}px = {hero_w/W*100:.1f}% · co {max(s for _,s,_ in boxes)}")
    return hero_h / H, hero_w / W


# ───────── SPEC video 21 (copy khoi nay cho video sau) ─────────
SPECS = {
    # T2 = khuon KAME, CHU GIONG HET T1 => phep do sach: chi doi KHUON HINH
    "T2": dict(
        name="thumb_T2_fuyo-205man.png",
        chip="年金に税金がかかる方へ",
        hero=[{"t": "158万円は古い", "c": "w", "strike_n": 5},
              {"t": "205万円", "c": "y"}],
        bar="出さないと年2万円",
    ),
    # T3 = khuon KAME + chu VAT + dong tu MAT (thu youtube-suggested-growth.md §6)
    "T3": dict(
        name="thumb_T3_fuyo-205man.png",
        chip="年金に税金がかかる方へ",
        hero=[{"t": "この秋 届く紙を出さないと", "c": "w"},
              {"t": "損します", "c": "y"}],
        bar="158万円の線は、もうありません",
    ),
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--only")
    a = ap.parse_args()
    dst = Path(a.folder)
    dst.mkdir(parents=True, exist_ok=True)
    print(f"KHUON KAME -> {dst}")
    for k, sp in SPECS.items():
        if a.only and k != a.only:
            continue
        build(sp, dst / sp["name"])
