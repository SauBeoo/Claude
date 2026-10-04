# -*- coding: utf-8 -*-
"""make_hook_slide_06.py — slide MỞ MÀN video 06 (加給年金).

⚠️ Bài học 2026-07-30: Pexels KHÔNG cấp được ảnh senior châu Á / giấy tờ 年金 cho beat này
(3 vòng fetch trả về: cặp vợ chồng Tây, thanh niên, và ông già cầm thiệp Valentine).
→ Slide mở màn dựng từ **chính trang 原典 của 日本年金機構** — 100% đúng chủ đề, không thể
lệch tệp, và mở màn luôn bằng móc nhận diện số 1 của kênh (原典を見せる).

Lớp: ảnh trang gốc (mờ + tối) → dải giấy trắng chiếu đúng câu 「届出が必要です」 khoanh đỏ
→ chữ hook vàng viền tối → nhãn nguồn.

Chạy: python tools/make_hook_slide_06.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "06_kakyu-nenkin-haiguusha-42man"
VID = PROJ / "06_VIDEO" / STEM
RAW = VID / "genten" / "_raw" / "p1_youken.jpg"
OUT = VID / "slides_img" / "slide_00.png"
W, H = 1920, 1080
FONT = "C:/Windows/Fonts/yugothb.ttc"
GOLD = (255, 205, 74)
RED = (214, 36, 44)
INK = (10, 14, 26)

# dải giấy: crop đúng dòng 「加給年金額加算のためには、届出が必要です。」 trên trang gốc
STRIP = (370, 624, 714, 650)
# nền: cả khối 受給要件
BG = (360, 520, 1190, 690)
LINES = [("一年、待っただけで", 88), ("42万円が消えた", 150)]
SUB = "加給年金 ―― 届出をした人にだけ、支払われるお金"
SRC_LABEL = "日本年金機構「加給年金額と振替加算」／2026年7月時点"


def main():
    if not RAW.exists():
        print(f"❌ thiếu {RAW}")
        return
    page = Image.open(RAW).convert("RGB")

    # ---- nền: trang gốc, cover-crop, mờ + tối ----
    bg = page.crop(BG)
    sc = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * sc), round(bg.height * sc)), Image.LANCZOS)
    x, y = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H))
    bg = bg.filter(ImageFilter.GaussianBlur(5))
    bg = ImageEnhance.Brightness(bg).enhance(0.34)
    bg = ImageEnhance.Color(bg).enhance(0.35)
    # ám navy cho hợp bản sắc kênh
    bg = Image.blend(bg, Image.new("RGB", (W, H), (14, 22, 44)), 0.34)

    d = ImageDraw.Draw(bg)

    # ---- dải giấy trắng: câu 原典 sắc nét + khoanh đỏ ----
    strip = page.crop(STRIP)
    s2 = 3.05
    sw, sh = int(strip.width * s2), int(strip.height * s2)
    strip = strip.resize((sw, sh), Image.LANCZOS)
    sx, sy = (W - sw) // 2, 168
    d.rounded_rectangle([sx - 34, sy - 26, sx + sw + 34, sy + sh + 26],
                        radius=16, fill=(252, 250, 245))
    bg.paste(strip, (sx, sy))
    d.rounded_rectangle([sx - 14, sy - 10, sx + sw + 14, sy + sh + 10],
                        radius=12, outline=RED, width=7)

    # ---- chữ hook ----
    yy = 500
    for text, size in LINES:
        f = ImageFont.truetype(FONT, size)
        tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, yy), text, font=f, fill=GOLD,
               stroke_width=max(8, size // 11), stroke_fill=INK)
        yy += size + 30

    f2 = ImageFont.truetype(FONT, 46)
    tw = d.textlength(SUB, font=f2)
    d.text(((W - tw) / 2, yy + 34), SUB, font=f2, fill=(255, 255, 255),
           stroke_width=7, stroke_fill=INK)

    f3 = ImageFont.truetype(FONT, 28)
    lw = d.textlength(SRC_LABEL, font=f3)
    d.text((W - lw - 62, H - 62), SRC_LABEL, font=f3, fill=(198, 196, 190))

    bg.save(OUT)
    for e in (".jpg",):
        p = OUT.with_suffix(e)
        if p.exists():
            p.unlink()
    print(f"✅ slide mở màn (nền 原典) → {OUT}")


if __name__ == "__main__":
    main()
