# -*- coding: utf-8 -*-
"""build_health_bg.py — dựng NỀN thumbnail theo KHUÔN KÊNH HEALTH.

Khuôn (đo từ mẫu `youtube-jp-health/06_VIDEO/28_kuroyanagi-tetsuko/thumbnail.png`):
  nền navy gradient + quầng sáng phía nhân vật · nhân vật chiếm ~46% bên PHẢI,
  mép trái tan dần vào navy (giả cutout, khỏi phải tách nền) · chữ do make_thumb.py
  ghép sau (3 dòng leo màu trắng → vàng → ĐỎ to nhất) · badge nhận diện kênh góc trên-phải.

    python tools/build_health_bg.py <ảnh nguồn> <ảnh nền ra.jpg> [--src-x 0.44] [--panel 0.46]
                                    [--fade 300] [--badge "60代の食卓"]

⚠️ Badge mặc định là 「60代の食卓」 (kênh shokutaku). Kênh health dùng 「健康ノート」 —
   bê nhầm badge sang kênh khác = gắn sai nhận diện, luôn truyền --badge cho đúng kênh.
⚠️ Đổi ảnh nguồn thì phải ĐO LẠI `--mosaic-box` của make_thumb (toạ độ tính trên khung
   SAU khi dựng nền, không phải ảnh gốc) — lỗi này đã dính một lần: mosaic lệch chỗ nên
   vật-đáp-án hiện nguyên trong khi chữ vừa hứa giấu nó.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
NAVY_TOP = np.array([13, 27, 61])
NAVY_BOT = np.array([26, 47, 92])
GLOW = (56, 86, 140)
BADGE_BG = (247, 199, 38)
BADGE_FG = (13, 27, 61)
FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"


def build(src_path, out_path, src_x=0.44, panel=0.46, fade=300, badge="60代の食卓"):
    src = Image.open(src_path).convert("RGB")

    grad = np.zeros((H, W, 3), dtype=np.uint8)
    for y in range(H):
        grad[y, :, :] = (NAVY_TOP + (NAVY_BOT - NAVY_TOP) * (y / H)).astype(np.uint8)
    bg = Image.fromarray(grad)

    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse([W * 0.62, -H * 0.25, W * 1.15, H * 1.1], fill=95)
    bg = Image.composite(Image.new("RGB", (W, H), GLOW), bg,
                         halo.filter(ImageFilter.GaussianBlur(150)))

    sw, sh = src.size
    crop = src.crop((int(sw * src_x), 0, sw, sh))
    ch = H
    crop = crop.resize((max(1, int(crop.width * ch / crop.height)), ch), Image.LANCZOS)
    pw = int(W * panel)
    if crop.width < pw:                      # ảnh hẹp hơn panel → nới src_x
        pw = crop.width
    crop = crop.crop((crop.width - pw, 0, crop.width, ch))

    mask = Image.new("L", (pw, ch), 255)
    dm = ImageDraw.Draw(mask)
    f = min(fade, pw)
    for i in range(f):
        dm.line([(i, 0), (i, ch)], fill=int(255 * (i / f) ** 1.4))
    bg.paste(crop, (W - pw, 0), mask)

    if badge:
        d = ImageDraw.Draw(bg)
        font = ImageFont.truetype(FONT_B, 56)
        bb = d.textbbox((0, 0), badge, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad, x1, y0 = 26, W - 46, 40
        x0, y1 = x1 - tw - pad * 2, y0 + th + pad * 2
        d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=BADGE_BG,
                            outline=BADGE_FG, width=6)
        d.text((x0 + pad - bb[0], y0 + pad - bb[1]), badge, font=font, fill=BADGE_FG)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=95)
    print(f"nền khuôn health -> {out_path}  ({W}x{H}, panel {pw}px = {pw/W:.0%}, badge: {badge or 'không'})")
    print("→ bước kế: make_thumb.py ... --stack l --color1 white --color2 yellow --color3 red")
    print("  ĐỪNG QUÊN đo lại --mosaic-box trên khung mới.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--src-x", type=float, default=0.44, help="cắt từ tỉ lệ ngang này của ảnh gốc")
    ap.add_argument("--panel", type=float, default=0.46, help="bề ngang vùng ảnh bên phải")
    ap.add_argument("--fade", type=int, default=300, help="bề rộng dải tan vào navy (px)")
    ap.add_argument("--badge", default="60代の食卓", help='"" để bỏ badge')
    a = ap.parse_args()
    build(a.src, a.out, a.src_x, a.panel, a.fade, a.badge)
