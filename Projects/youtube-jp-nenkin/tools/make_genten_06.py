# -*- coding: utf-8 -*-
"""make_genten_06.py — dựng slide 原典ショット cho video 06 (加給年金).

Nguồn = ảnh chụp trang CƠ QUAN CÔNG (nenkin.go.jp) đã lưu ở genten/_raw/.
Mỗi slide: crop vùng câu đang đọc → phóng to → KHOANH ĐỎ dày → nhãn nguồn góc dưới.
Ghi thẳng slides_img/slide_XX.png theo index entry có "genten": true trong SLIDES.json
→ chạy TRƯỚC fetch_photos (fetch bỏ qua file đã tồn tại).

Chạy: python tools/make_genten_06.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "06_kakyu-nenkin-haiguusha-42man"
SLIDES = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"
VID = PROJ / "06_VIDEO" / STEM
RAW = VID / "genten" / "_raw"
OUT = VID / "slides_img"
W, H = 1920, 1080
FONT = "C:/Windows/Fonts/yugothb.ttc"
PAPER = (247, 244, 236)
NAVY = (26, 42, 74)
RED = (208, 32, 40)

# match → (file raw, crop trang gốc (l,t,r,b), tiêu đề, nhãn nguồn,
#          [khung đỏ trong toạ độ CROP (l,t,r,b)])
SHOTS = {
    "こちらが、日本年金機構のページです。": (
        "p1_youken.jpg", (365, 531, 1180, 658),
        "加給年金の受給要件",
        "日本年金機構「加給年金額と振替加算」／2026年7月時点",
        [(185, 3, 330, 30), (2, 96, 280, 124)],
    ),
    "令和8年4月からの額で、配偶者の分が": (
        "p2_kingaku.jpg", (365, 372, 1180, 592),
        "加給年金額（令和8年4月から）",
        "日本年金機構「加給年金額と振替加算」／2026年7月時点",
        [(3, 55, 330, 105)],
    ),
    "こちらが、日本年金機構の、繰り下げ受給のページです": (
        "p3_kurisage.jpg", (370, 262, 1190, 405),
        "繰下げの注意点",
        "日本年金機構「年金の繰下げ受給」／2026年7月時点",
        [(5, 95, 815, 143)],
    ),
    "「繰下げ待機期間中は、加給年金額や": (
        "p3_kurisage.jpg", (378, 356, 1190, 404),
        "繰下げ待機期間中は",
        "日本年金機構「年金の繰下げ受給」／2026年7月時点",
        [(0, 0, 812, 48)],
    ),
    "「老齢基礎年金と老齢厚生年金は、別々に": (
        "p4_betsubetsu.jpg", (370, 356, 900, 402),
        "基礎年金と厚生年金は、別々に",
        "日本年金機構「年金の繰下げ受給」／2026年7月時点",
        [(0, 0, 530, 46)],
    ),
    "こちらが、日本年金機構の「年金の時効」のページです。": (
        "p5_jikou.jpg", (370, 12, 1190, 58),
        "年金の時効",
        "日本年金機構「年金の時効」／2026年7月時点",
        [(0, 0, 820, 46)],
    ),
}


def rrect(d, box, color, width, r=14):
    d.rounded_rectangle(box, radius=r, outline=color, width=width)


def build(raw_name, crop, title, source, boxes, dest):
    src = Image.open(RAW / raw_name).convert("RGB")
    piece = src.crop(crop)
    # phóng to vừa bề ngang an toàn 1680px
    # lấp tối đa vùng an toàn (rộng 1760, cao 690) — khán giả 60+ phải đọc được
    scale = min(1760 / piece.width, 690 / piece.height)
    scale = max(scale, 1.0)
    pw, ph = int(piece.width * scale), int(piece.height * scale)
    piece = piece.resize((pw, ph), Image.LANCZOS)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(FONT, 74)
    f_src = ImageFont.truetype(FONT, 30)
    f_tag = ImageFont.truetype(FONT, 34)

    # tiêu đề
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 74), title, font=f_title, fill=NAVY)
    d.line([(W / 2 - tw / 2, 168), (W / 2 + tw / 2, 168)], fill=(212, 175, 55), width=5)

    # nhãn 原典
    d.rounded_rectangle([88, 196, 400, 250], radius=10, fill=NAVY)
    d.text((110, 203), "原典を見る", font=f_tag, fill=(255, 255, 255))

    # ảnh trang gốc, viền xám
    x0, y0 = (W - pw) // 2, 292 + max(0, (690 - ph) // 2)
    d.rectangle([x0 - 10, y0 - 10, x0 + pw + 10, y0 + ph + 10], fill=(255, 255, 255),
                outline=(196, 190, 178), width=3)
    img.paste(piece, (x0, y0))

    # KHOANH ĐỎ
    for (l, t, r, b) in boxes:
        rrect(d, [x0 + l * scale - 8, y0 + t * scale - 8,
                  x0 + r * scale + 8, y0 + b * scale + 8], RED, 7)

    # nhãn nguồn
    sw = d.textlength(source, font=f_src)
    d.text((W - sw - 70, H - 74), source, font=f_src, fill=(110, 104, 92))
    img.save(dest)


def main():
    cfg = json.loads(SLIDES.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for i, spec in enumerate(cfg):
        if not spec.get("genten"):
            continue
        key = spec["match"]
        if key not in SHOTS:
            print(f"  ⚠ slot {i:02d}: chưa có SHOTS cho match «{key[:28]}»")
            continue
        raw, crop, title, source, boxes = SHOTS[key]
        if not (RAW / raw).exists():
            print(f"  ❌ thiếu ảnh gốc {raw}")
            continue
        dest = OUT / f"slide_{i:02d}.png"
        build(raw, crop, title, source, boxes, dest)
        print(f"  ✓ {dest.name}  ← {raw}  [{title}]")
        n += 1
    print(f"\n✅ {n} slide 原典 → {OUT}")


if __name__ == "__main__":
    main()
