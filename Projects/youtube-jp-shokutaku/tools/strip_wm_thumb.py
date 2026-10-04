# -*- coding: utf-8 -*-
r"""Go dau ✦ tren THUMBNAIL da bake chu (khong cat khung duoc vi chu chay ra sat mep).

    python tools\strip_wm_thumb.py <file-or-folder> [-o outdir]

Vi sao khong dung strip_wm_crop.py: tool do CAT mep phai. Voi thumbnail thi chu hero
chay toi ~0.97W nen cat la mat chu. O day phai VA.

Cach va (da thu 3 cach, chi cach nay chay):
  1. copy khoi texture ben canh   -> HONG: sao nam tren vung TUONG toi hon, nguon lay
                                      lech tong -> ra vet.
  2. tach lop alpha toan vung     -> chi go ~70%, con vet sao mo.
  3. DUNG LAI NEN THEO TRUNG VI TUNG HANG  -> sach. Tuong/ban la gradient MIN theo chieu
     doc nen trung vi cua chinh hang do khop gan nhu tuyet doi; loai pixel thuoc NET CHU
     khoi mat na de khong pha glyph; cong nhieu +-1.2 de khong "phang nhu nhua".

⚠️ DINH VI ✦ BANG MAY KHONG DUNG DUOC O DAY (da thu 4 lan): net chu dam ap dao moi phep
   do (template match tra 289 cum rac; residual-max tra toan mep chu). Vi tri lay tu
   DO BANG MAT tren nhieu mau, ghi thanh hang so duoi day theo TUNG LO kich thuoc.
"""
import argparse
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# (x/W, y/H) do bang MAT — theo tung lo kich thuoc cua generator
SPOTS = {
    (1376, 768): [(0.928, 0.878)],
    (2752, 1536): [(0.958, 0.926), (0.930, 0.890)],
    # chouhen 2026-08-14: thumbnail da resize 1280x720 (goc 1376x768). Vi tri chot BANG MAT
    # tren thumb_T1_wall (sao tren nen be tong, khong de net chu) -> (0.933W, 0.871H).
    (1280, 720): [(0.933, 0.871)],
}
R = {1280: 28, 1376: 30, 2752: 60}          # ban kinh vung xu ly theo be ngang


def is_glyph(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return ((r < 140) & (g < 120)) | ((r > 195) & (g > 145) & (b < 130))


def clean_one(a, cx, cy, r, rng, thr=6.0, guard=True, win=40):
    """guard=False: TAT bo ve net chu.

    🔴 Khi nao phai tat: `is_glyph` nhan "net chu" bang NGUONG MAU, nen o anh ma ✦ nam tren
    NEN GO/NAU (khong co chu gan do) thi chinh cai nen bi nhan la net chu => mat na ✦ bi
    `& (~glyph)` cat mat mot nua, va con VET SAO MO. Do duoc o thumbnail video 18: vung ✦
    co 3.676 px vuot nguong nhung tool chi va 1.852 (~50%).
    Giu guard=True khi ✦ nam DE LEN hoac SAT net chu — do la ca ma guard sinh ra de cuu.
    """
    y0, y1, x0, x1 = cy - r, cy + r, cx - r, cx + r
    # 🔴 `win` = cua so lay mau trung vi HANG, mo rong ra ngoai hop ✦ moi ben.
    # Rule ghi "trung vi hang khop gan tuyet doi" — dung, NHUNG chi khi ca hang la MOT chat
    # lieu. O thumbnail video 18, hang chua ✦ gom TAY AO XAM + GO NAU + DAI VANG, nen
    # median cua win=40 (mac dinh) keo ve xam va va ra VET XAM NGANG. Ha win cho cua so chi
    # con GO thi median khop. => ca nao ✦ nam gan bien chat lieu thi phai ha `win`.
    W0, W1 = max(0, cx - r - win), min(a.shape[1], cx + r + win)
    box = a[y0:y1, x0:x1]
    glyph = is_glyph(box) if guard else np.zeros(box.shape[:2], bool)
    fill = np.zeros_like(box)
    star = np.zeros(box.shape[:2], bool)
    for i in range(box.shape[0]):
        row = a[y0 + i, W0:W1]
        gl = is_glyph(row) if guard else np.zeros(row.shape[0], bool)
        clean = row[~gl] if (~gl).sum() > 20 else row
        med = np.median(clean, axis=0)
        fill[i, :] = med
        star[i] = (box[i].mean(axis=1) - med.mean() > thr) & (~glyph[i])
    if star.sum() == 0:
        return 0
    m = np.asarray(Image.fromarray((star * 255).astype(np.uint8))
                   .filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2)),
                   dtype=float) / 255
    m = m[..., None] * (~glyph)[..., None]
    a[y0:y1, x0:x1] = box * (1 - m) + fill * m
    a[y0:y1, x0:x1] += rng.normal(0, 1.2, box.shape) * (m > 0.2)
    return int(star.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("-o", "--outdir", default=None)
    ap.add_argument("--spot", action="append", default=None,
                    help="Toa do ✦ DO BANG MAT, dang 'x,y' chuan hoa (vd 0.960,0.924). "
                         "Lap nhieu lan neu lo co nhieu dau. De cap nhieu lo dung chung mot "
                         "kich thuoc nhung KHAC so dau — bang SPOTS chi la mac dinh.")
    # 🔴 NGUONG 6.0 LA SAN TUYET DOI, VA NO TRUOT KHI NEN CHAY TRANG (2026-08-18,
    # nenkin thumb 13): nen man cua co trung vi 244/max 252 nen ✦ chi nho duoc DUNG 6.00 ->
    # dieu kien "> 6" tra ve 0 pixel, tool bao "da va: [0]" ma sao van con nguyen.
    # Cai mat do la CHENH LECH, ma chenh lech bi TRAN CUA NEN chan lai -> phai cho ha nguong.
    # Cach chon: do max(box.mean - row_median) o dung vi tri ✦ roi lay ~40% so do.
    ap.add_argument("--thr", type=float, default=6.0,
                    help="nguong chenh so trung vi hang de nhan ✦ (mac dinh 6.0; "
                         "nen chay trang thi ha ve 2.0-3.0)")
    ap.add_argument("--no-guard", action="store_true",
                    help="TAT bo ve net chu (is_glyph). Dung khi ✦ nam tren NEN GO/NAU/anh "
                         "khong co chu gan do — nguong mau se nhan chinh cai nen la 'net "
                         "chu' va cat mat na ✦ mat mot nua (con vet sao mo). Giu guard khi "
                         "✦ de len hoac sat net chu.")
    ap.add_argument("--win", type=int, default=40,
                    help="be rong cua so lay mau trung vi hang (mac dinh 40). Ha ve 6-10 "
                         "khi ✦ nam gan BIEN CHAT LIEU (canh tay ao / dai mau khac) — cua "
                         "so rong keo median sang chat lieu ben canh, va ra VET NGANG.")
    ap.add_argument("--no-resize", action="store_true",
                    help="Giu nguyen kich thuoc goc thay vi ep ve 1920x1080.")
    a_ = ap.parse_args()
    t = Path(a_.target)
    files = sorted([p for p in t.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")]) \
        if t.is_dir() else [t]
    out = Path(a_.outdir) if a_.outdir else (t if t.is_dir() else t.parent) / "_wm_clean"
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    manual = None
    if a_.spot:
        manual = [tuple(float(v) for v in s.replace(" ", "").split(",")) for s in a_.spot]
        print(f"  ✦ lay tu --spot (do bang mat): {manual}")

    for f in files:
        im = Image.open(f).convert("RGB")
        W, H = im.size
        spots = manual or SPOTS.get((W, H))
        if spots is None:
            print(f"  {f.name}: BO QUA — chua co moc ✦ cho lo {W}x{H}, phai DO BANG MAT truoc")
            continue
        a = np.asarray(im).astype(float)
        r = R.get(W, max(20, W // 46))
        hits = [clean_one(a, int(W * fx), int(H * fy), r, rng, a_.thr, not a_.no_guard,
                          a_.win)
            for fx, fy in spots]
        o = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        if not a_.no_resize:
            o = o.resize((1920, 1080), Image.LANCZOS)
        p = out / (f.stem + ".jpg")
        o.save(p, quality=95)
        print(f"  {f.name} ({W}x{H}) -> {p.name}  pixel ✦ da va: {hits}")
    print(f"\n⚠️ Exit code KHONG chung minh ✦ da sach — soi mat goc duoi-phai tung anh.")


if __name__ == "__main__":
    main()
