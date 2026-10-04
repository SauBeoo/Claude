# -*- coding: utf-8 -*-
r"""strip_wm_flat27.py — xoá ✦ trên lô ảnh PHẲNG nền trơn (video 27, style いらすとや).

VÌ SAO KHÔNG DÙNG LẠI TOOL CŨ:
  · `strip_wm_crop.py` (co-dai) CẮT mép phải 0,908W — ở lô này cắt sẽ ăn mất nhân vật nằm
    sát mép (ảnh 3: hai người ngồi ở ~0,86–0,94W).
  · `strip_wm_thumb.py` (shokutaku) vá bằng trung vị TỪNG HÀNG — sinh ra cho nền gradient dọc.
  · `strip_wm_grain.py` (health) inpaint + ghép vân — sinh ra cho ảnh THẬT có vân gỗ/vệt nắng.
Lô này là ca DỄ NHẤT và chưa có tool: nền quanh ✦ là **kem phẳng tuyệt đối, không vân, không
gradient, không biên chất liệu** (`media-library.md` §2.10 ⑥b: trung vị hàng chỉ hỏng khi nền có
gradient chéo). ⇒ điền bằng màu nền cục bộ + nhiễu rất nhẹ là sạch.

🔴 KHÔNG hard-code vị trí: quét template ✦ lấy từ CHÍNH ảnh, tìm MỌI dấu (lô 2752×1536 từng có
2 dấu — `media-library.md` §2.10 ⑤). Hằng số chỉ dùng làm chỗ BẮT ĐẦU soi.

CHẠY:  python tools/strip_wm_flat27.py <thư mục vào> <thư mục ra>
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SPOT = (0.924, 0.870)   # chỗ soi đầu tiên, lô 1376×768 (đo bằng mắt trên crop 1:1)
R = 30                  # bán kính ✦ (đo: sao 4 cánh ~46px ngang)
THR = 0.55              # ngưỡng template match


def find_stars(g: np.ndarray, h: int, w: int):  # noqa: D401
    """Trả về mọi vị trí ✦. Template lấy từ chính ảnh tại SPOT rồi quét toàn khung."""
    cx, cy = int(w * SPOT[0]), int(h * SPOT[1])
    tpl = g[cy - R:cy + R, cx - R:cx + R]
    if tpl.size == 0:
        return []
    res = cv2.matchTemplate(g, tpl, cv2.TM_CCOEFF_NORMED)
    ys, xs = np.where(res >= THR)
    out = []
    for x, y in zip(xs, ys):
        c = (int(x + R), int(y + R))
        # 🔴 CHỈ NHẬN match trong VÙNG SOI quanh SPOT. Bản đầu quét toàn khung và trả
        # **17 dấu / 7 ảnh** trong khi thật chỉ có 1/ảnh — template ✦ là một blob sáng mờ nên
        # nó khớp với mọi mảng nền kem trơn, có cái rơi trúng giữa vật (0,764W/0,503H).
        # Đúng bẫy đã ghi ở `media-library.md` §2.10 ⑤: *template match trả 289 cụm rác*.
        # Vùng soi rộng ±8% quanh hằng số lô — đủ để bắt lệch giữa các lô, không đủ để ăn rác.
        if not (abs(c[0] / w - SPOT[0]) <= 0.08 and abs(c[1] / h - SPOT[1]) <= 0.08):
            continue
        # 🔴 ĐIỀU KIỆN THỨ HAI: vùng quanh phải là NỀN TRƠN. ✦ của lô này luôn nằm trên nền
        # kem phẳng; match rơi vào vật thì vành có nhiều màu, và `patch()` sẽ điền trung vị
        # của hỗn hợp đó -> ra MỘT KHỐI MÀU LẠ. Đã dính thật: dấu thứ 2 của ảnh 3
        # (0,929W/0,790H) rơi trúng cái ghế đỏ -> vá ra khối hồng chữ nhật, chỉ lộ khi soi 1:1.
        # ⇒ Thà bỏ sót một ✦ (soi mắt bắt được) còn hơn tự tay phá một vật (khó thấy hơn).
        y0, y1 = max(0, c[1] - R - 12), min(h, c[1] + R + 12)
        x0, x1 = max(0, c[0] - R - 12), min(w, c[0] + R + 12)
        ring = g[y0:y1, x0:x1]
        if ring.size == 0 or float(ring.std()) > 6.0:
            continue
        if all((c[0] - q[0]) ** 2 + (c[1] - q[1]) ** 2 > (2 * R) ** 2 for q in out):
            out.append(c)
    return out


def patch(img: np.ndarray, c, rng) -> None:
    """Điền vùng ✦ bằng màu nền cục bộ (trung vị vành ngoài) + nhiễu ±1,2."""
    x, y = c
    h, w = img.shape[:2]
    x0, x1 = max(0, x - R - 12), min(w, x + R + 12)
    y0, y1 = max(0, y - R - 12), min(h, y + R + 12)
    box = img[y0:y1, x0:x1].astype(np.float32)
    m = np.ones(box.shape[:2], bool)
    m[12:-12, 12:-12] = False          # chỉ lấy VÀNH làm mẫu nền
    bg = np.median(box[m], axis=0)
    fill = np.repeat(np.repeat(bg[None, None, :], box.shape[0], 0), box.shape[1], 1)
    fill += rng.normal(0, 1.2, fill.shape)
    core = np.zeros(box.shape[:2], bool)
    core[6:-6, 6:-6] = True
    box[core] = fill[core]
    img[y0:y1, x0:x1] = np.clip(box, 0, 255).astype(np.uint8)


def main() -> int:
    if len(sys.argv) < 3:
        print("dùng: python tools/strip_wm_flat27.py <in_dir> <out_dir>")
        return 1
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    files = sorted([p for p in src.iterdir()
                    if p.suffix.lower() in (".png", ".jpg", ".jpeg")])
    if not files:
        print(f"⛔ không thấy ảnh trong {src}")
        return 1
    tot = 0
    for p in files:
        img = cv2.imdecode(np.fromfile(str(p), np.uint8), cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        stars = find_stars(g, h, w)
        for c in stars:
            patch(img, c, rng)
        out = dst / (p.stem + ".png")
        cv2.imencode(".png", img)[1].tofile(str(out))
        tot += len(stars)
        pos = " · ".join(f"({c[0]/w:.3f}W,{c[1]/h:.3f}H)" for c in stars)
        print(f"  {p.name[:44]:<46} {w}x{h}  ✦ {len(stars)}  {pos}")
    print(f"\n→ {tot} dấu đã xoá trên {len(files)} ảnh · {dst}")
    print("⚠️ NGHIỆM THU: soi 1:1 CẢ 4 GÓC — sheet thu nhỏ cho qua ✦ (media-library.md §2.10 ⑥).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
