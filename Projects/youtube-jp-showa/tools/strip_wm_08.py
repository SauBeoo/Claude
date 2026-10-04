# -*- coding: utf-8 -*-
"""strip_wm_08.py — xoa dau ✦ tren 3 thumbnail video 08 (lo 1376x768, nen TOI).

Vi sao khong dung strip_wm_thumb.py cua shokutaku: tool do do "sang hon TRUNG VI HANG";
o day hang chua ca vien trang cua khung collage -> trung vi hang bi keo len, ✦ (gia tri 5-9
tren nen gan den) khong bao gio vuot nguong => bao "va 0 pixel" du ✦ van con.
Cach chay duoc (media-library.md §2.10 ⑥b): cv2.inpaint (Navier-Stokes) + ghep lai VAN tan so
cao lay tu mot vung toan-nen ben canh + nhieu nhe. Ban do bang mat, hang so theo LO.

Usage: python tools/strip_wm_08.py <indir> -o <outdir> [--cx 1273 --cy 672 --r 34]
"""
import argparse, sys
from pathlib import Path
import numpy as np
import cv2
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# chot BANG MAT tren sheet contrast-stretch (_thumb_check/_wm_stretch.jpg), lo 1376x768:
# sao 4 canh, tam ~ (1273, 672) = (0.925W, 0.875H) — khop hang so SPOTS cua shokutaku (0.928, 0.878)
CX, CY, R = 1273, 672, 22
# 🔴 Lan 1 dung r=34 + ghep van tu offset (-170,-40): inpaint keo THANH SOC va vung lay van dinh
# mep panel trang -> ra vet trang, TE HON ban goc (media-library §2.10 ⑤ "patch de lai vet").
# Nen quanh ✦ o lo nay gan DONG NHAT va rat toi (trung vi 1-16/255) => cach chac hon: to de bang
# TRUNG VI CUA VANH quanh sao + nhieu theo do lech chuan cua chinh vanh do, blend mem. Khong inpaint.


def strip(src: Path, dst: Path, cx: int, cy: int, r: int) -> int:
    im = cv2.imread(str(src)).astype(np.float32)
    h, w = im.shape[:2]
    y0, y1, x0, x1 = cy - r - 20, cy + r + 20, cx - r - 20, cx + r + 20
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    blk = im[y0:y1, x0:x1]
    ring = blk[(d > r + 5) & (d < r + 18)]              # vanh sach quanh sao
    med = np.median(ring, axis=0)
    sd = float(np.median(np.std(ring, axis=0)))
    rng = np.random.default_rng(abs(hash(src.name)) % (2 ** 32))
    fill = med[None, None, :] + rng.normal(0, max(sd * 0.45, 0.5), blk.shape)
    a = np.clip((r + 3 - d) / 6.0, 0, 1)[..., None]      # blend mem 6px
    im[y0:y1, x0:x1] = blk * (1 - a) + fill * a
    out = np.clip(im, 0, 255).astype(np.uint8)
    cv2.imwrite(str(dst), out, [cv2.IMWRITE_JPEG_QUALITY, 96])
    g = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY).astype(float)
    inner = g[cy - r:cy + r, cx - r:cx + r]
    ringg = g[cy - r - 16:cy + r + 16, cx - r - 16:cx + r + 16]
    return int(abs(np.median(inner) - np.median(ringg)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("indir"); ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--cx", type=int, default=CX); ap.add_argument("--cy", type=int, default=CY)
    ap.add_argument("--r", type=int, default=R)
    a = ap.parse_args()
    od = Path(a.outdir); od.mkdir(parents=True, exist_ok=True)
    for p in sorted(Path(a.indir).glob("*.jpg")):
        im = cv2.imread(str(p))
        if im.shape[1] != 1376 or im.shape[0] != 768:
            print(f"  [BO QUA] {p.name} {im.shape[1]}x{im.shape[0]} — hang so ✦ chi dung cho lo 1376x768")
            continue
        d = strip(p, od / p.name, a.cx, a.cy, a.r)
        print(f"  ✓ {p.name}  lech trung vi vung-va vs vanh: {d} (cang gan 0 cang khop nen)")
    print("\n⚠️ Exit code KHONG chung minh ✦ da sach — bat buoc soi MAT 1:1 goc duoi-phai tung anh.")
