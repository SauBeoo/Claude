# -*- coding: utf-8 -*-
r"""strip_wm_thumb30.py — xoa dau (*) tren 3 thumbnail AI cua video 30 (lo 1376x768).

LUAT: `media-library.md` §2.10 (5)b — con (*) la CHUA XONG.

MAP file tai ve (zip "Thang 9 27 - 13_41") -> vai, doi chieu bang MAT voi thumb_prompts_TENFILE:
  T1 = Man_holding_bank_passbook_..._2  (so ngan hang + to thong bao, nen giay ke o)
  T2 = Man_checking_pension_passbook_... (truoc may in so)
  T3 = Man_holding_bank_passbook_...    (khuon kame-sensei, nen navy, ong gia goc duoi-phai)

CHON NHANH — moi ban mot cach (da thu va soi 1:1):
  T1: CAT x=1250 (0,908W) + trim 12 tren / 53 duoi. (*) de len BIEN tay+giay: inpaint
      tron nhoe ngon tay, phep MO/DONG khong an (✦ lo nay la KHOI sang ban trong suot,
      khong phai net manh), khu alpha khong co mat na chuan -> con vet. Chu chinh ket
      ~0,79W; banner y 19-169, ruy-bang do toi y 714 -> trim khong mat chu.
  T2: VA tron r=34 (inpaint NS + van lay tu ao phia tren). Nen ao tron -> sach.
      Khong cat duoc: banner 年金振込 chay toi ~0,96W.
  T3: VA bang MAT NA HINH SAO (|x|^.5+|y|^.5 <= r^.5, r=30, dilate 7) + Telea.
      Mat na tron r=34 an vao co ao -> nhoe. Khong cat duoc: pill vang ~0,93W,
      dai do chu 7月の紙を見て sat day.
VI TRI (*) CHOT BANG MAT tren luoi residual (may truot o T1/T3, peak 0,19/0,31):
  T1 (1279,670) · T2 (1279,670) = (0,930W · 0,872H) · T3 (1285,673) — mo, lech ~6px.

CHAY:  python tools/strip_wm_thumb30.py
"""
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = (r"C:\Users\tuana\AppData\Local\Temp\claude\E--Claude"
       r"\8eafe683-c5e7-4b41-9b3a-261b087cf8fe\scratchpad\t30")
VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\30_nenkin-furikomi-10gatsu-fueru-hito"
RAW = os.path.join(VD, "_thumb_raw")
OUT = os.path.join(VD, "_thumb_clean")

FILES = {
    "T1": "Man_holding_bank_passbook_20260927134322_2.jpg",
    "T2": "Man_checking_pension_passbook_20260927134322.jpg",
    "T3": "Man_holding_bank_passbook_20260927134322.jpg",
}
# (cx, cy, offset lay van (dx, dy)) — vung lay van phai cung CHAT LIEU (ao so mi) va khong trum sao
SPOT = {"T2": (1279, 670, (0, -110))}
T1_CUT = (1250, 12, 53)          # x cat, trim tren, trim duoi
T3_STAR = (1285, 673, 30)        # cx, cy, r (dinh sao)
OUT_WH = (1280, 720)
R = 34


def imread(p):
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)


def imwrite(p, a):
    ok, buf = cv2.imencode(".png", a)
    assert ok
    buf.tofile(p)


def patch(img, cx, cy, off, r=R, seed=30):
    """Inpaint NS roi GHEP LAI van tan so cao tu vung cung chat lieu (§2.10 (5)b muc 3)."""
    rng = np.random.default_rng(seed)
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(m, (cx, cy), r, 255, -1)
    out = cv2.inpaint(img, m, 7, cv2.INPAINT_NS)
    H, W = img.shape[:2]
    ox, oy = off
    s = r * 2
    sx0, sy0 = cx + ox - s, cy + oy - s
    sx0 = max(0, min(W - 2 * s, sx0))
    sy0 = max(0, min(H - 2 * s, sy0))
    src = img[sy0:sy0 + 2 * s, sx0:sx0 + 2 * s].astype(np.float32)
    detail = src - cv2.GaussianBlur(src, (0, 0), 6)
    y0, x0 = cy - s, cx - s
    y1, x1 = min(H, y0 + 2 * s), min(W, x0 + 2 * s)
    detail = detail[:y1 - y0, :x1 - x0]
    roi = out[y0:y1, x0:x1].astype(np.float32)
    d = cv2.distanceTransform(m[y0:y1, x0:x1], cv2.DIST_L2, 3)
    a = np.clip(d / max(1.0, d.max()), 0, 1)[..., None]
    noise = rng.normal(0, 0.8, roi.shape).astype(np.float32) * (a > 0)
    out[y0:y1, x0:x1] = np.clip(roi + detail * a + noise, 0, 255).astype(np.uint8)
    return out


def patch_star(img, cx, cy, r, seed=1):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    m = ((np.abs(xx - cx) ** .5 + np.abs(yy - cy) ** .5) <= r ** .5).astype(np.uint8) * 255
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    o = cv2.inpaint(img, m, 3, cv2.INPAINT_TELEA).astype(np.float32)
    o += np.random.default_rng(seed).normal(0, 1.0, o.shape) * (m[..., None] > 0)
    return np.clip(o, 0, 255).astype(np.uint8)


def cut(img, x, top, bot):
    H = img.shape[0]
    c = img[top:H - bot, :x]
    assert abs(c.shape[1] / c.shape[0] - 16 / 9) < 0.004, c.shape
    return c


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    for tag, fn in FILES.items():
        raw = os.path.join(RAW, fn)
        if not os.path.exists(raw):
            with open(os.path.join(SRC, fn), "rb") as f, open(raw, "wb") as g:
                g.write(f.read())
        a = imread(raw)
        if tag == "T1":
            o, how = cut(a, *T1_CUT), f"CAT {T1_CUT}"
        elif tag == "T2":
            cx, cy, off = SPOT[tag]
            o, how = patch(a, cx, cy, off), f"VA tron @({cx},{cy}) r={R}"
        else:
            o, how = patch_star(a, *T3_STAR), f"VA hinh sao {T3_STAR}"
        o = cv2.resize(o, OUT_WH, interpolation=cv2.INTER_AREA)
        # ⛔ ten trung gian NGOAI pattern thumb_T* (upload_pack bat nham)
        p = os.path.join(OUT, f"_wm_fixed_{tag}.png")
        imwrite(p, o)
        print(f"{tag}: {how} -> {os.path.basename(p)} {OUT_WH}")
    print(f"-> {OUT}\n⚠️ Nghiem thu = soi 1:1 ca 4 goc bang MAT, log nay chi la loi khai.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
