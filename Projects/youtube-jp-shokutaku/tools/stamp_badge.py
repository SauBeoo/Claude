# -*- coding: utf-8 -*-
"""stamp_badge.py — dán badge nhận diện kênh lên thumbnail ĐÃ ghép chữ.

Vì sao cần: `build_health_bg.py` chỉ vẽ badge khi dựng nền khuôn-navy. Thumbnail
kiểu FULL-BLEED (ảnh sáng trọn khung + cột chữ một bên, chuẩn v5 Phần E) không đi
qua tool đó nên trước giờ ra lò KHÔNG CÓ BADGE — lệch nhận diện với các video cũ
(bắt được ở video 05 kyabetsu, 2026-08-01).

    python tools/stamp_badge.py <in.png> <out.png> [--badge "60代の食卓"] [--pos tl|tr|bl|br]

⚠️ Badge mặc định 「60代の食卓」 = kênh shokutaku. Kênh health dùng 「健康ノート」 —
   luôn truyền --badge cho đúng kênh, bê nhầm là gắn sai nhận diện.
⚠️ Đặt badge vào góc KHÔNG có cột chữ (cột chữ phải → badge tl/bl) và soi lại 168px:
   badge phải NHỎ + ra rìa, không được tranh chỗ với dòng chính (`audience-45plus` §1).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BADGE_BG = (247, 199, 38)
BADGE_FG = (13, 27, 61)
FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"


def stamp(img, badge="60代の食卓", pos="tl", size=56, margin=44):
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_B, size)
    bb = d.textbbox((0, 0), badge, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 26
    bw, bh = tw + pad * 2, th + pad * 2
    W, H = img.size
    x0 = margin if pos in ("tl", "bl") else W - margin - bw
    y0 = margin if pos in ("tl", "tr") else H - margin - bh
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16,
                        fill=BADGE_BG, outline=BADGE_FG, width=6)
    d.text((x0 + pad - bb[0], y0 + pad - bb[1]), badge, font=font, fill=BADGE_FG)
    return img, (x0, y0, x0 + bw, y0 + bh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--badge", default="60代の食卓")
    ap.add_argument("--pos", choices=["tl", "tr", "bl", "br"], default="tl")
    ap.add_argument("--size", type=int, default=56)
    a = ap.parse_args()

    img = Image.open(a.inp).convert("RGB")
    img, box = stamp(img, a.badge, a.pos, a.size)
    out = Path(a.out)
    img.save(out, quality=95)
    for tag, w in (("480", 480), ("168", 168), ("120", 120)):
        img.resize((w, round(w * img.height / img.width)), Image.LANCZOS) \
           .save(out.with_name(f"{out.stem}_preview{tag}.png"))
    print(f"badge 「{a.badge}」 @{a.pos} {box} -> {out.name} + preview480/168/120")


if __name__ == "__main__":
    main()
