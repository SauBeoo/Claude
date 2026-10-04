# -*- coding: utf-8 -*-
"""make_thumb_compare.py — thumbnail Layout C (❌ vs ？) kênh 60代からの食卓.
Kể chuyện 1 nhịp: TRÁI = cách ăn sai (dim + ❌ đỏ), PHẢI = đáp án bị GIẤU
(blur vùng bí ẩn + 「？」to) → curiosity gap bằng HÌNH (luật A8, 02_THUMBNAIL_TITLE_RULES.md).
Chữ: 2 label trắng viền đen; icon ❌/？ dùng 1 màu nhấn duy nhất.
Chạy:
  python tools/make_thumb_compare.py <left.jpg> <right.jpg> <out.png> \
    --label1 "そのまま" --label2 "正解はコレ" [--accent red] \
    [--blur-box 0.30,0.55,0.70,1.00] [--focus1 center] [--focus2 center]
blur-box = x0,y0,x1,y1 theo tỉ lệ panel phải (0–1).
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
PW = W // 2
FONT = "C:/Windows/Fonts/YuGothB.ttc"
WHITE = (255, 255, 255)
BLACK = (8, 8, 8)
ACCENTS = {"red": (232, 32, 28), "yellow": (255, 222, 0)}


def font(sz):
    return ImageFont.truetype(FONT, sz)


def cover(src, w, h, focus="center"):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = {"left": 0, "right": im.width - w}.get(focus, (im.width - w) // 2)
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def bottom_scrim(panel, strength=165, frac=0.34):
    gh = int(panel.height * frac)
    grad = Image.new("L", (1, gh), 0)
    for y in range(gh):
        grad.putpixel((0, y), int(strength * y / gh))
    panel.paste(Image.new("RGB", (panel.width, gh), (0, 0, 0)),
                (0, panel.height - gh), grad.resize((panel.width, gh)))
    return panel


def draw_x(d, cx, cy, s, color, width=46):
    # 2 nét chéo, viền đen trước cho nổi
    for w_, c in [(width + 22, BLACK), (width, color)]:
        d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=c, width=w_)
        d.line([(cx + s, cy - s), (cx - s, cy + s)], fill=c, width=w_)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("left"); ap.add_argument("right"); ap.add_argument("out")
    ap.add_argument("--label1", default="そのまま")
    ap.add_argument("--label2", default="正解はコレ")
    ap.add_argument("--accent", choices=list(ACCENTS), default="red")
    ap.add_argument("--blur-box", default="0.30,0.55,0.72,1.00")
    ap.add_argument("--hide", choices=["mosaic", "blur"], default="mosaic",
                    help="cách giấu đáp án: mosaic モザイク (mặc định, phản xạ 'bị che' mạnh) / blur")
    ap.add_argument("--focus1", default="center"); ap.add_argument("--focus2", default="center")
    ap.add_argument("--label-size", type=int, default=150)
    ap.add_argument("--q-size", type=int, default=330)
    ap.add_argument("--x-pos", default="0.50,0.34", help="tâm ❌ theo tỉ lệ panel trái")
    args = ap.parse_args()
    accent = ACCENTS[args.accent]

    # panel trái: cách sai — dim nhẹ
    left = cover(args.left, PW, H, args.focus1).point(lambda p: int(p * 0.72))
    left = bottom_scrim(left)
    # panel phải: đáp án giấu — sáng nguyên, blur vùng bí ẩn
    right = cover(args.right, PW, H, args.focus2)
    bx0, by0, bx1, by1 = [float(v) for v in args.blur_box.split(",")]
    box = (int(bx0 * PW), int(by0 * H), int(bx1 * PW), int(by1 * H))
    region = right.crop(box)
    if args.hide == "mosaic":
        rw, rh = region.size
        region = region.resize((max(1, rw // 26), max(1, rh // 26)), Image.LANCZOS)
        region = region.resize((rw, rh), Image.NEAREST)
    else:
        region = region.filter(ImageFilter.GaussianBlur(34))
    right.paste(region, box)
    right = bottom_scrim(right)

    img = Image.new("RGB", (W, H))
    img.paste(left, (0, 0)); img.paste(right, (PW, 0))
    d = ImageDraw.Draw(img)
    # vạch chia trắng
    d.rectangle([PW - 5, 0, PW + 5, H], fill=WHITE)

    # ❌ panel trái
    xx, xy = [float(v) for v in args.x_pos.split(",")]
    draw_x(d, int(xx * PW), int(xy * H), 150, accent)

    # 「？」 giữa vùng blur panel phải
    fq = font(args.q_size)
    qb = d.textbbox((0, 0), "？", font=fq, stroke_width=24)
    qcx = PW + (box[0] + box[2]) // 2 - (qb[2] - qb[0]) // 2
    qcy = (box[1] + box[3]) // 2 - (qb[3] - qb[1]) // 2 - qb[1]
    d.text((qcx, qcy), "？", font=fq, fill=accent, stroke_width=24, stroke_fill=BLACK)

    # labels: trái đáy, phải ĐỈNH panel (né vùng ？ ở đáy) — trắng viền đen
    fl = font(args.label_size)
    for text, px, top in [(args.label1, 0, False), (args.label2, PW, True)]:
        bb = d.textbbox((0, 0), text, font=fl, stroke_width=16)
        tw = bb[2] - bb[0]
        x = px + (PW - tw) // 2
        y = (40 - bb[1]) if top else (H - (bb[3] - bb[1]) - 52 - bb[1])
        d.text((x, y), text, font=fl, fill=WHITE, stroke_width=16, stroke_fill=BLACK)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
    img.resize((120, 68), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out)


if __name__ == "__main__":
    main()
