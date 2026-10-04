# -*- coding: utf-8 -*-
r"""strip_wm_thumb23.py — xoa dau (*) tren 3 thumbnail AI cua video 23 (lo 1376x768).

LUAT: `media-library.md` §2.10 (5)b — **moi anh AI, moi kenh, khong ngoai le**: con (*)
la CHUA XONG, khong duoc goi upload.

CHON NHANH THEO §6d — theo viec CHU co chay sat mep khong, KHONG theo "anh slide hay
thumbnail":
  · T2: (*) nam tren nen xanh-xam **PHANG**, khong dinh bien chat lieu, va chu gan nhat
        (ruy-bang 5年で消えます) ket o ~0,66W ⇒ **VA** (inpaint + ghep lai van) — va o day
        va TOT HON cat, vi cat mep phai se xen mat ban tay dang cam buu thiep.
  · T3: quet template toan anh => **khong co dau nao**, khong dung toi.
  · T1: (*) dap **DE LEN net chu** cua the do 今すぐ確認! ⇒ §5: **LOAI ANH, GEN LAI**,
        dung co cuu. (T1 con hong nang hon vi model tu them 3 khoi chu.)

VI TRI (*) CHOT BANG MAT roi doi chieu template — khong tin mot minh phep do may
(§5: dinh vi bang may da truot 4/4 o anh co chu):
  T2 ~ (0,927W · 0,857H) — khop hang so da ghi cho lo 1376x768 la (0,928W · 0,878H).

CHAY:  python tools/strip_wm_thumb23.py            # quet + va
       python tools/strip_wm_thumb23.py --scan     # chi quet, khong ghi
"""
import io
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\23_nenkin-seikyusho-todokanai")
RAW = os.path.join(VD, "_thumb_raw")
OUT = os.path.join(VD, "_thumb_clean")

# ⛔ Ten trung gian phai NGOAI pattern `thumb_T*` — neu khong `upload_pack.py` quet duoc
#    ca file chua dong dau va gom nham (`media-library.md` §2.10 (7), dinh that o chouhen 36).
FILES = {
    "T1": "Man_holding_postcard_with_envelope_20260913151016.jpeg",
    "T2": "Hands_holding_postcard_for_pension_20260913151016.jpeg",
    "T3": "Japanese_pension_information_You\u2026_20260913151016.jpeg",
}
SPOT = {"T2": (0.930, 0.874)}          # chot bang MAT roi DO LAI bang may
# 🔴 Ban kinh phai DUNG CO sao (§6b): do duoc bbox **48x48px** (residual >6 so trung vi
#    151px, nen o day PHANG nen phep do nay tin duoc — canh bao "may truot 4/4" cua §5 la
#    cho anh CO CHU). r=30 de lai mot vet sang o canh duoi cua sao; 34 moi trum het.
R = 34


def imread(p):
    """cv2.imread KHONG doc duoc path non-ASCII tren Windows (tra None, im lang)."""
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)


def imwrite(p, a):
    ok, buf = cv2.imencode(".png", a)
    assert ok
    buf.tofile(p)


def patch(img, cx, cy, r=R):
    """Inpaint (Navier-Stokes) roi GHEP LAI van tan so cao — §6b.

    Inpaint xoa sach sao va giu dung gradient, nhung lam MAT van (muot nhu nhua);
    lop high-pass lay tu mot vung toan-nen ben canh la phan bu dung cho do.
    """
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(m, (cx, cy), r, 255, -1)
    out = cv2.inpaint(img, m, 7, cv2.INPAINT_NS)

    # van lay tu vung ben TRAI (nen phang, khong co sao khac o do)
    ox, oy = -190, 0
    src = img[max(0, cy + oy - r * 2):cy + oy + r * 2,
              max(0, cx + ox - r * 2):cx + ox + r * 2]
    if src.size:
        blur = cv2.GaussianBlur(src, (0, 0), 6)
        detail = src.astype(np.float32) - blur.astype(np.float32)
        h, w = detail.shape[:2]
        y0, x0 = cy - h // 2, cx - w // 2
        roi = out[y0:y0 + h, x0:x0 + w].astype(np.float32)
        d = cv2.distanceTransform(m[y0:y0 + h, x0:x0 + w], cv2.DIST_L2, 3)
        a = np.clip(d / max(1.0, d.max()), 0, 1)[..., None]
        out[y0:y0 + h, x0:x0 + w] = np.clip(roi + detail * a, 0, 255).astype(np.uint8)
    noise = np.random.normal(0, 0.8, out.shape).astype(np.float32)
    return np.clip(out.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def main():
    scan_only = "--scan" in sys.argv
    os.makedirs(OUT, exist_ok=True)

    t2 = imread(os.path.join(RAW, FILES["T2"]))
    H, W = t2.shape[:2]
    cx, cy = int(SPOT["T2"][0] * W), int(SPOT["T2"][1] * H)
    tmpl = t2[cy - 26:cy + 26, cx - 26:cx + 26].copy()

    # ── QUET: dung chinh (*) cua T2 lam template, do tren CA BA anh ──────────
    print("QUET template (*) tren ca 3 anh — peak >0,80 la co dau:")
    for tag, fn in FILES.items():
        a = imread(os.path.join(RAW, fn))
        if a is None:
            print(f"  {tag}: 🔴 khong doc duoc"); continue
        res = cv2.matchTemplate(a, tmpl, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(res)
        print(f"  {tag}: peak {mx:.3f} @ ({loc[0]+26},{loc[1]+26}) "
              f"= ({(loc[0]+26)/a.shape[1]:.3f}W · {(loc[1]+26)/a.shape[0]:.3f}H)")

    if scan_only:
        return 0

    # ── T2: VA ──────────────────────────────────────────────────────────────
    fixed = patch(t2, cx, cy)
    p = os.path.join(OUT, "_wm_fixed_T2.png")
    imwrite(p, fixed)
    res = cv2.matchTemplate(fixed, tmpl, cv2.TM_CCOEFF_NORMED)
    _, mx, _, _ = cv2.minMaxLoc(res)
    print(f"\nT2 da va -> {os.path.basename(p)} · peak sau va {mx:.3f} "
          f"(goc 1,000; ve muc nhieu la sach)")

    # ── T3: khong co dau, chi doi duoi file ─────────────────────────────────
    t3 = imread(os.path.join(RAW, FILES["T3"]))
    imwrite(os.path.join(OUT, "_wm_fixed_T3.png"), t3)
    print("T3 khong co dau -> chi chuyen sang PNG")
    print(f"\n⛔ T1 KHONG xuat: (*) dap len net chu the 今すぐ確認!, va model tu them "
          f"3 khoi chu (緊急事態 cat doi banner) => GEN LAI.")
    print(f"   -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
