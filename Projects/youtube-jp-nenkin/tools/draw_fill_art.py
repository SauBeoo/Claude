# -*- coding: utf-8 -*-
"""draw_fill_art.py — vẽ 4 ảnh ô `fill` cho video 10 bằng code (không cần AI).

VÌ SAO CÓ TOOL NÀY: quota gen ảnh của key Gemini = 0 (429 trên cả 3 model, đo 2026-08-10),
mà 4 ô `fill` chỉ cần VẬT ĐƠN trên nền trơn — thứ vẽ bằng vector còn sạch hơn AI và
khớp sẵn bảng màu kênh (`make_stage.py` đã vẽ 28 icon cùng cách). Ảnh cảnh có người
(`art_shindai*`) thì KHÔNG vẽ được kiểu này — vẫn phải gen.

Khung đích của `fill_art()` là 390×316 (tỉ lệ 1,234) và nó cover-crop → vẽ đúng tỉ lệ ×2.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(__file__).resolve().parents[1] / "06_VIDEO" / "10_shien-kyufukin-hagaki-9gatsu" / "art"
W, H = 780, 632                          # = 390×316 ×2

# bảng màu lấy y nguyên từ make_stage.py
INK, INK2 = (26, 42, 74), (60, 72, 96)
AMBER = (245, 179, 1)
RED, GREEN = (206, 68, 62), (32, 142, 104)
GREY, LINE = (168, 174, 184), (222, 226, 233)
BG = (250, 250, 247)
GOLD, GOLD_D = (240, 190, 60), (198, 148, 30)


def new():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def purse(d, cx, cy, w, h, body, edge, open_wide=False):
    """Ví gấp kiểu がま口 — thân hình vòm + gọng kim loại."""
    d.rounded_rectangle([cx - w // 2, cy - h // 2 + 26, cx + w // 2, cy + h // 2], 46,
                        fill=body, outline=edge, width=7)
    if open_wide:
        d.arc([cx - w // 2 - 6, cy - h // 2 - 6, cx + w // 2 + 6, cy - h // 2 + 92],
              200, 340, fill=edge, width=13)
        d.ellipse([cx - w // 2 + 26, cy - h // 2 + 20, cx + w // 2 - 26, cy - h // 2 + 74],
                  fill=(236, 236, 238), outline=edge, width=5)
    else:
        d.arc([cx - w // 2 - 6, cy - h // 2 + 4, cx + w // 2 + 6, cy - h // 2 + 96],
              200, 340, fill=edge, width=13)
    d.ellipse([cx - 9, cy - h // 2 + 12, cx + 9, cy - h // 2 + 30], fill=edge)


def coin(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=GOLD_D, width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], outline=GOLD_D, width=4)


def cal_page(d, x, y, w, h, circled=False, dim=False, angle=0):
    """Một tờ lịch bóc — KHÔNG chữ, không số (chỉ gợi bằng vạch)."""
    lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    body = (246, 246, 248) if dim else (255, 255, 255)
    band = GREY if dim else RED
    dl.rounded_rectangle([30, 30, 30 + w, 30 + h], 16, fill=body,
                         outline=GREY if dim else INK2, width=5)
    dl.rounded_rectangle([30, 30, 30 + w, 30 + int(h * 0.28)], 16, fill=band)
    dl.rectangle([30, 30 + int(h * 0.20), 30 + w, 30 + int(h * 0.28)], fill=band)
    for i in range(3):                      # vạch gợi ô lịch
        yy = 30 + int(h * 0.45) + i * int(h * 0.17)
        dl.line([44, yy, 30 + w - 14, yy], fill=LINE if not dim else (238, 238, 240), width=6)
    for i in range(2):                      # lỗ đóng gáy
        dl.ellipse([30 + 22 + i * (w - 74), 14, 30 + 44 + i * (w - 74), 36],
                   fill=BG, outline=GREY, width=4)
    if circled:
        dl.ellipse([30 + w * 0.22, 30 + h * 0.42, 30 + w * 0.80, 30 + h * 0.92],
                   outline=RED, width=11)
    if angle:
        lay = lay.rotate(angle, resample=Image.BICUBIC, expand=False)
    return lay


def f_67man():
    im, d = new()
    purse(d, 300, 330, 300, 300, (170, 122, 92), (108, 74, 54))
    for cx, cy, r in [(520, 452, 44), (610, 400, 40), (566, 330, 36),
                      (648, 480, 34), (470, 372, 30)]:
        coin(d, cx, cy, r)
    return im


def f_0en():
    """0円 = ĐÁM XU BỊ GẠCH ĐỎ — cặp âm/dương với `fill_67man` (cùng đám xu, khác màu).

    Hai bản trước vẽ 'ví mở rỗng' đều ra CÁI NỒI: thân bo tròn + miệng ellipse tối là
    hình cái nồi, không phải cái ví. Thay vì vá tiếp, đổi sang ngữ pháp hình đã chạy
    được ở `fill_22man`: **vạch đỏ chéo = mất**. Nhờ vậy 4 ảnh dùng chung một quy ước.
    """
    im, d = new()
    for cx, cy, r in [(300, 300, 52), (416, 250, 46), (392, 372, 42),
                      (486, 330, 38), (300, 424, 34)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=(224, 224, 228), outline=(160, 162, 170), width=6)
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  outline=(160, 162, 170), width=5)
    d.line([196, 486, 590, 176], fill=RED, width=18)
    return im


def f_2kigen():
    im, _ = new()
    im.paste(*_lay(cal_page(None, 0, 0, 250, 330, dim=True, angle=-4), 92, 132))
    im.paste(*_lay(cal_page(None, 0, 0, 250, 330, circled=True, angle=3), 392, 152))
    return im


def f_22man():
    """4 tháng BỊ MẤT. Bản đầu xếp 4 tờ nghiêng chồng nhau + vệt bay → thành một cục và
    lệch phải. Sửa: 4 tờ XÁM xếp đều, CANH GIỮA, một vạch đỏ gạch chéo cả nhóm."""
    im, d = new()
    n, w, h = 4, 150, 200
    gap = 22
    total = n * w + (n - 1) * gap
    x0, y0 = (W - total) // 2, (H - h) // 2 + 10
    for i in range(n):
        im.paste(*_lay(cal_page(None, 0, 0, w, h, dim=True), x0 + i * (w + gap) - 30, y0 - 30))
    d.line([x0 - 26, y0 + h + 40, x0 + total + 26, y0 - 34], fill=RED, width=16)
    return im


def _lay(lay, x, y):
    return lay, (x, y), lay


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("fill_67man.png", f_67man), ("fill_0en.png", f_0en),
                     ("fill_2kigen.png", f_2kigen), ("fill_22man.png", f_22man)]:
        fn().save(OUT / name)
        print("  ✓", name)
    print("— 4 ảnh ô fill (vẽ bằng code, style vector kênh) —")


if __name__ == "__main__":
    main()
