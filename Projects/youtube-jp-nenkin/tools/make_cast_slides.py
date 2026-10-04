# -*- coding: utf-8 -*-
"""make_cast_slides.py — ghép slide NHÂN VẬT モニター cho kênh nenkin (user chốt 2026-07-22).

SLIDES.json entry mới:  {"match": "...", "photo": true, "cast": "tanaka_smile",
                          "label": "田中さん(67)・横浜"}   ← label tùy chọn (mặc định suy từ tên)
→ tool này vẽ slide 1920x1080 (nền giấy lab + nhân vật いらすとや + name-tag) và LƯU THẲNG
  `slides_img/slide_XX.png` đúng index entry — chạy TRƯỚC fetch_photos (fetch bỏ qua entry có
  "cast"), video_render dùng file theo index như ảnh thường.

Chạy:  python tools/make_cast_slides.py 03_SCRIPTS/<stem>_SLIDES.json 06_VIDEO/<stem>/slides_img
⚠️ License いらすとや: đếm tổng ảnh いらすとや (cast) trong 1 video ≤20 — tool tự đếm và báo.
Ảnh nhân vật: assets/cast/*.png (tải bởi tools/fetch_irasutoya.py; hồ sơ モニター trong CLAUDE.md).
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
CAST_DIR = PROJ / "assets" / "cast"
W, H = 1920, 1080
FONT = "C:/Windows/Fonts/yugothb.ttc"

# label mặc định theo hồ sơ モニター (CLAUDE.md — số đời nhân vật cố định)
DEFAULT_LABELS = {
    "tanaka":    "田中さん(67)・横浜",
    "sato":      "佐藤さん(66)・仙台",
    "suzuki":    "鈴木さん(65)・名古屋",
    "takahashi": "高橋さん(65)・東京",
    "yamada":    "山田さんご夫妻・大阪",
    "ito":       "伊藤さん(68)・福岡",
    "kenkyuin":  "研究員",
}


def lab_paper_bg():
    """Nền giấy sổ lab: kem sáng + lưới mờ + viền navy nhẹ (đồng bộ 研究ノート)."""
    img = Image.new("RGB", (W, H), (247, 244, 236))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 64):
        d.line([(x, 0), (x, H)], fill=(233, 228, 214), width=1)
    for y in range(0, H, 64):
        d.line([(0, y), (W, y)], fill=(233, 228, 214), width=1)
    d.rectangle([24, 24, W - 24, H - 24], outline=(42, 58, 88), width=4)
    return img


def compose(cast_png, label, out_path):
    img = lab_paper_bg()
    ch = Image.open(cast_png).convert("RGBA")
    max_h = int(H * 0.66)
    ch.thumbnail((int(W * 0.62), max_h), Image.LANCZOS)
    x = (W - ch.width) // 2
    y = int(H * 0.50) - ch.height // 2 - 20
    img.paste(ch, (x, y), ch)
    if label:
        d = ImageDraw.Draw(img, "RGBA")
        f = ImageFont.truetype(FONT, 64)
        bb = d.textbbox((0, 0), label, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        bx = (W - tw) // 2
        by = y + ch.height + 28
        pad = 26
        d.rounded_rectangle([bx - pad, by - pad + bb[1], bx + tw + pad, by + th + pad + bb[1]],
                            18, fill=(42, 58, 88, 235))
        d.text((bx, by), label, font=f, fill=(255, 255, 255))
    img.save(out_path)


def main():
    slides_json, img_dir = Path(sys.argv[1]), Path(sys.argv[2])
    img_dir.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(slides_json.read_text(encoding="utf-8"))
    n = 0
    seen = set()
    for i, spec in enumerate(cfg):
        cast = spec.get("cast")
        if not cast:
            continue
        src = CAST_DIR / f"{cast}.png"
        if not src.exists():
            sys.exit(f"[LỖI] không có assets/cast/{cast}.png — xem fetch_irasutoya.py")
        label = spec.get("label")
        if label is None:
            key = cast.split("_")[0]
            label = DEFAULT_LABELS.get(key, "")
        out = img_dir / f"slide_{i:02d}.png"
        compose(src, label, out)
        n += 1
        seen.add(cast)
        print(f"  slide_{i:02d}: {cast} 「{label}」")
    print(f"XONG {n} cast slide ({len(seen)} ảnh いらすとや khác nhau) → {img_dir}")
    # License いらすとや đếm theo SỐ ẢNH KHÁC NHAU ("1つの制作物に20点まで"), không phải
    # số lần dùng lại trong cùng video — trước 2026-08-04 tool đếm số ENTRY nên báo động
    # sai (24 entry mà chỉ 11 ảnh). Tái dùng cùng một nhân vật là ĐÚNG thiết kế: cast cố
    # định là signature của kênh (CLAUDE.md §SIGNATURE), không phải vi phạm license.
    if len(seen) > 20:
        print(f"⚠️ {len(seen)} ảnh いらすとや KHÁC NHAU trong 1 video — VƯỢT hạn 20 điểm "
              f"của license! Giảm số nhân vật/biểu cảm khác nhau (dùng lại thì không sao).")


if __name__ == "__main__":
    main()
