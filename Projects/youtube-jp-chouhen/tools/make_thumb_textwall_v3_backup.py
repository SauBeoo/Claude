# -*- coding: utf-8 -*-
"""make_thumb_textwall.py — thumbnail 朗読 style TEXT-WALL v3 (MẶC ĐỊNH kênh, chốt 2026-07-21).

Meta ngách スカッと (mổ xẻ 2026-07-21): video thắng — kể cả kênh 1.2k sub 70k+ view/video —
đều dùng "bức tường chữ": 4–5 dòng chữ khổng lồ full-width kể trọn setup trên nền tối,
gần như không có hình, đọc trọn drama trong 2 giây ở 120px (mẫu: 苦しみの物語, 嫁子のスカッと朗読劇場).

Cấu trúc dòng (màu auto theo vai trò, dòng CUỐI luôn ĐỎ double-stroke TO NHẤT):
  dòng 1–2  bối cảnh + hành động phản diện   → TRẮNG / HỒNG
  dòng 3    quote phản diện 「…ｗ」            → CYAN / TÍM
  dòng 4    phản ứng chính diện 私「…」        → VÀNG
  dòng cuối đòn/hậu quả bỏ lửng               → ĐỎ (halo trắng + viền đen)

Chạy:
  python tools/make_thumb_textwall.py <out.png> --lines "dòng1" "dòng2" "dòng3" "dòng4" "dòng đỏ"
  [--colors w,p,c,y,r]   ghi đè màu từng dòng (w trắng · p hồng · c cyan · v tím · y vàng · r đỏ)
  [--bg <scene.jpg>]     lót ảnh scene làm tối (mặc định nền đen thuần)
Tool tự hạ cỡ chữ cho lọt khung; mỗi dòng nên ≤14 ký (dài hơn = chữ nhỏ = chết ở feed).
Xuất kèm _preview.png (480px) + _preview120.png (120px) để duyệt 2 cấp.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
BLACK = (6, 6, 6)
COLORS = {
    "w": (255, 255, 255),   # trắng
    "p": (255, 105, 180),   # hồng
    "c": (0, 229, 255),     # cyan
    "v": (200, 120, 255),   # tím
    "y": (255, 224, 0),     # vàng
    "r": (232, 28, 24),     # đỏ — chỉ dành cho dòng đòn cuối
}
# màu auto theo số dòng (dòng cuối luôn đỏ)
AUTO = {3: "wyr", 4: "wcyr", 5: "wpcyr"}


def font(sz):
    return ImageFont.truetype(FONT, sz)


def fit(text, sz, max_w, stroke):
    """Hạ cỡ đến khi lọt max_w."""
    while sz > 40:
        bb = font(sz).getbbox(text, stroke_width=stroke)
        if bb[2] - bb[0] <= max_w:
            break
        sz -= 3
    return sz


def cover_dark(src, factor=0.32):
    """Lót ảnh scene, làm tối để chữ nổi.

    factor 0.32 = mặc định (ảnh scene sáng bình thường). Ảnh vốn đã tối (prompt
    'deep near-black shadow') bị 0.32 nhân thêm là mất hẳn chủ thể → truyền
    --bg-brightness 0.55–0.75. Duyệt lại 120px sau khi nâng: dòng đỏ phải còn đọc được.
    """
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
    return ImageEnhance.Brightness(im).enhance(factor)


def draw_line(d, x, y, text, f, fill, red=False):
    if red:
        # double-stroke chuẩn thị trường: quầng trắng ngoài → viền đen → ruột đỏ
        d.text((x, y), text, font=f, fill=(255, 255, 255), stroke_width=30, stroke_fill=(255, 255, 255))
        d.text((x, y), text, font=f, fill=fill, stroke_width=12, stroke_fill=BLACK)
    else:
        d.text((x, y), text, font=f, fill=fill, stroke_width=16, stroke_fill=BLACK)


def main():
    ap = argparse.ArgumentParser(description="Thumbnail text-wall v3 (meta スカッと)")
    ap.add_argument("out")
    ap.add_argument("--lines", nargs="+", required=True, help="3–5 dòng, dòng CUỐI = đòn đỏ")
    ap.add_argument("--colors", default="auto", help="vd w,p,c,y,r — mặc định auto theo vai trò")
    ap.add_argument("--bg", default="", help="ảnh scene lót nền (tự làm tối); bỏ trống = nền đen")
    ap.add_argument("--bg-brightness", type=float, default=0.32,
                    help="độ sáng nền sau khi lót (0.32 mặc định; ảnh vốn tối dùng 0.55–0.75)")
    a = ap.parse_args()

    lines = a.lines
    if not 3 <= len(lines) <= 5:
        sys.exit("❌ Cần 3–5 dòng (meta chuẩn 4–5 dòng).")
    for t in lines:
        if len(t) > 16:
            print(f"⚠️ Dòng >16 ký sẽ bị hạ cỡ nhỏ (chết ở feed): 「{t}」")

    keys = AUTO[len(lines)] if a.colors == "auto" else a.colors.replace(",", "")
    if len(keys) != len(lines) or any(k not in COLORS for k in keys):
        sys.exit(f"❌ --colors phải là {len(lines)} ký tự trong {'/'.join(COLORS)} (vd {AUTO[len(lines)]})")

    img = cover_dark(a.bg, a.bg_brightness) if a.bg else Image.new("RGB", (W, H), (10, 10, 14))
    d = ImageDraw.Draw(img)

    # chia khung dọc đều cho các dòng; dòng đỏ cuối được cấp cao hơn ~25%
    margin_y, gap, max_w = 30, 18, W - 90
    weights = [1.0] * (len(lines) - 1) + [1.3]
    unit = (H - 2 * margin_y - gap * (len(lines) - 1)) / sum(weights)
    y = margin_y
    for text, key, wgt in zip(lines, keys, weights):
        red = key == "r"
        slot = unit * wgt
        stroke = 42 if red else 16
        sz = fit(text, int(slot * 0.80), max_w, stroke)
        f = font(sz)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x = (W - tw) // 2
        draw_line(d, x, y + (slot - th) / 2 - bb[1], text, f, COLORS[key], red)
        y += slot + gap

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview.png"))
    img.resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out, "(+ _preview / _preview120 — duyệt 2 cấp)")


if __name__ == "__main__":
    main()
