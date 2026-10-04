# -*- coding: utf-8 -*-
r"""strip_wm_alpha29.py — gỡ ✦ khỏi thumbnail v2 video 29 bằng UN-BLEND alpha (2026-09-24).

VÌ SAO KHÔNG DÙNG TOOL CŨ: ✦ của lô này (1376×768, 3 ảnh) là **hình sao TRẮNG ĐẶC bán trong
suốt, rộng ~60px**, không phải nét mảnh ⇒ phép đóng/mở (`co-dai/tools/strip_wm_star.py`) không
chạm tới; trung vị hàng thì ra khối chữ nhật trên nếp áo. ✦ là lớp phủ `obs = (1−α)·nền + α·255`
nên đảo ngược được: `nền = (obs − α·255) / (1 − α)`.

α ƯỚC TỪ ẢNH NỀN MỊN NHẤT (T1, áo sơ mi) rồi ÁP CHUNG cho cả lô — hình sao giống hệt nhau về
vị trí/cỡ ở 3 ảnh (soi mắt 2026-09-24: tâm ~(1277,669) cả 3).
⚠️ Exit code không chứng minh sạch — soi 1:1 bằng mắt (media-library §2.10 ⑤b mục 6).

CHẠY:  python tools/strip_wm_alpha29.py      → _thumb_v2_raw/clean_*.png + sheet so sánh
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAW = Path(__file__).resolve().parents[1] / "06_VIDEO" / "29_shikaku-kakuninsho-8gatsu-85sai" / "_thumb_v2_raw"
BOX = (1225, 615, 1330, 725)          # x0,y0,x1,y1 — rộng hơn sao mỗi bên
REF = "Man_holding_sheet_at_hospital_20260924153407.jpeg"   # T1 — nền áo mịn nhất
FILES = {"T1": REF, "T2": "Man_holding_wallet_at_hospital_20260924153407.jpeg",
         "T3": "Man_holding_paper_with_text_20260924153407.jpeg"}


def star_mask(cx, cy, ra, rb, shape, ss=4):
    """Hình ✦ = astroid |x/a|^(2/3)+|y/b|^(2/3) ≤ 1, siêu lấy mẫu ss× để có mép mềm đúng."""
    h, w = shape
    ys, xs = np.mgrid[0:h * ss, 0:w * ss].astype(np.float32) / ss
    v = (np.abs((xs - cx) / ra) ** (2 / 3) + np.abs((ys - cy) / rb) ** (2 / 3)) <= 1
    return v.reshape(h, ss, w, ss).mean((1, 3)).astype(np.float32)


FIX = (1279, 671, 26)
FIX_BY = {"T3": (1281, 673, 28)}   # T3: ✦ đè biên giấy/ngón tay, dò riêng ra lệch 2px + to hơn
# khoá theo T2 — bản dò rõ nhất (điểm khớp 21,8); nền mịn của T1 làm máy dò lệch


def fit(p, fix=None):
    """Dò tâm + cỡ + α tốt nhất: sau un-blend, vành trong ≈ vành ngoài (độ lệch nhỏ nhất)."""
    g = p.mean(2)
    best = None
    fix = fix or FIX
    if fix:
        best = (0.0, fix[0] - BOX[0], fix[1] - BOX[1], fix[2])
    for ra in (() if fix else (22, 24, 26, 28)):
        for dx in range(-6, 7, 2):
            for dy in range(-6, 7, 2):
                cx, cy = 1277 - BOX[0] + dx, 669 - BOX[1] + dy
                m = star_mask(cx, cy, ra, ra * 0.95, g.shape)
                inn, ring = m > 0.9, (cv2.dilate((m > 0.02).astype(np.uint8), np.ones((9, 9))) > 0) & (m < 0.02)
                hp = g - cv2.GaussianBlur(g, (0, 0), 12)
                sc = hp[inn].mean() - hp[ring].mean()
                if best is None or sc > best[0]:
                    best = (sc, cx, cy, ra)
    _, cx, cy, ra = best
    m = star_mask(cx, cy, ra, ra * 0.95, g.shape)
    inn = m > 0.9
    ring = (cv2.dilate((m > 0.02).astype(np.uint8), np.ones((11, 11))) > 0) & (m < 0.02)
    bgv, obs = g[ring].mean(), g[inn].mean()
    # α từ chênh lệch tại chỗ: dùng nền nội suy mượt thay vì trung bình vành
    bg = cv2.inpaint(p.astype(np.uint8), ((m > 0.02) * 255).astype(np.uint8), 7, cv2.INPAINT_TELEA).mean(2)
    al = float(np.median(((g - bg) / np.clip(255 - bg, 20, None))[inn]))
    return m, max(0.0, min(al, 0.6)), (cx + BOX[0], cy + BOX[1], ra, best[0])


def main():
    x0, y0, x1, y1 = BOX
    tiles = []
    for tag, fn in FILES.items():
        im = cv2.imread(str(RAW / fn))
        p = im[y0:y1, x0:x1].astype(np.float32)
        m, al, info = fit(p, FIX_BY.get(tag))
        aa = (m * al)[..., None]
        out = np.clip((p - aa * 255) / (1 - aa), 0, 255)
        out = out.astype(np.uint8)
        # dải VIỀN mảnh quanh mép sao: hình astroid lệch mép thật 1–3px ⇒ nội suy lại riêng dải đó
        band = (cv2.dilate((m > 0.02).astype(np.uint8), np.ones((7, 7))) > 0) &                ~(cv2.erode((m > 0.97).astype(np.uint8), np.ones((5, 5))) > 0)
        out = cv2.inpaint(out, band.astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
        res = im.copy()
        res[y0:y1, x0:x1] = out
        cv2.imwrite(str(RAW / f"clean_{tag}.png"), res)
        print(f"{tag}: tâm ({info[0]},{info[1]}) · bán kính {info[2]} · điểm khớp {info[3]:.1f} · α {al:.3f}")
        big = lambda z: cv2.resize(z[y0 - 20:y1 + 20, x0 - 20:x1 + 20], None, fx=3, fy=3,
                                   interpolation=cv2.INTER_NEAREST)
        tiles.append(np.hstack([big(im), big(res)]))
    cv2.imwrite(str(RAW / "wm_check.png"), np.vstack(tiles))
    print("→ clean_T1/T2/T3.png + wm_check.png (trái: gốc · phải: sau gỡ, 3×)")


if __name__ == "__main__":
    main()
