# -*- coding: utf-8 -*-
"""contact_sheet.py — ghép ảnh slide thành contact sheet để DUYỆT BẰNG MẮT trước render.

Bắt buộc theo `.claude/rules/media-library.md` §3: ảnh stock hay lệch nội dung
(Pexels không bao giờ trả rỗng nên rác luôn thắng) — phải soi từng ô đặt cạnh
câu thoại tương ứng rồi mới cho render.

    python tools/contact_sheet.py 06_VIDEO/<slug>/slides_img_photo \
        04_SCRIPTS/<slug>_SLIDES_video.json -o 06_VIDEO/<slug>/_sheet.jpg [--from 0] [--cols 6]

Mỗi ô: số slide + query đã dùng, để đối chiếu nhanh cái nào cần đổi.
"""
import argparse
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FONT_JP = Path(r"C:\Windows\Fonts\YuGothM.ttc")


def load_font(size):
    for f in (FONT_JP, Path(r"C:\Windows\Fonts\meiryo.ttc")):
        if f.exists():
            try:
                return ImageFont.truetype(str(f), size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("img_dir")
    ap.add_argument("slides_json")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--cell", type=int, default=320)
    ap.add_argument("--from", dest="start", type=int, default=0)
    ap.add_argument("--to", dest="end", type=int, default=10**6)
    a = ap.parse_args()

    slides = json.load(io.open(a.slides_json, encoding="utf-8"))
    d = Path(a.img_dir)
    items = []
    for i, e in enumerate(slides):
        if not (a.start <= i <= a.end):
            continue
        hit = next((p for ext in (".jpg", ".jpeg", ".png", ".webp")
                    for p in [d / f"slide_{i:02d}{ext}"] if p.exists()), None)
        items.append((i, hit, e.get("q", "")))

    cw, ch = a.cell, int(a.cell * 9 / 16)
    lab = 34
    cols = a.cols
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * (ch + lab)), (18, 20, 26))
    dr = ImageDraw.Draw(sheet)
    f = load_font(13)

    miss = []
    for n, (i, p, q) in enumerate(items):
        x, y = (n % cols) * cw, (n // cols) * (ch + lab)
        if p:
            im = Image.open(p).convert("RGB")
            sc = max(cw / im.width, ch / im.height)
            im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            im = im.crop(((im.width - cw) // 2, (im.height - ch) // 2,
                          (im.width - cw) // 2 + cw, (im.height - ch) // 2 + ch))
            sheet.paste(im, (x, y))
        else:
            dr.rectangle([x, y, x + cw - 2, y + ch], fill=(70, 20, 20))
            dr.text((x + 8, y + ch // 2), "THIẾU ẢNH", font=load_font(20), fill=(255, 180, 180))
            miss.append(i)
        dr.text((x + 6, y + ch + 3), f"[{i}] {q[:44]}", font=f, fill=(230, 230, 235))
        dr.text((x + 6, y + ch + 18), (q[44:88] if len(q) > 44 else ""), font=f, fill=(150, 155, 165))
        dr.rectangle([x, y, x + cw - 1, y + ch + lab - 1], outline=(60, 64, 74))

    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.output, quality=88)
    print(f"contact sheet -> {a.output}  ({len(items)} ô, {rows}x{cols})")
    if miss:
        print("THIẾU ẢNH ở slot:", miss)


if __name__ == "__main__":
    main()
