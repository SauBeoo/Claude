# -*- coding: utf-8 -*-
"""make_thumb.py — thumbnail kênh 사우 오디오 (port style SCENE v2 từ chouhen).
Ảnh nền = ảnh thật Pexels (license free thương mại). TỐI ĐA 3 khối chữ, đọc được ở 120px.
Text 3 tầng theo KHỐI 3 của script: tầng dẫn (trắng) → tầng key CỰC TO (nhấn ĐỎ
double-stroke từng từ) → tầng hệ quả (vàng). Băng trên + băng đáy, chừa mặt nhân vật.

Chạy: python tools/make_thumb.py <photo.jpg> <out.png>
Sửa TOP / BOTTOM bám KHỐI 3 của script (mỗi dòng = list segment (text, màu) để nhấn đỏ giữa câu).

⚠️ QUY TẮC KÊNH (user chốt 2026-07-13): KHÔNG in badge thời lượng góc màn hình
(YouTube tự hiện duration trên thumbnail rồi — in thêm là thừa/rác). Mặc định tắt;
flag --dur chỉ giữ cho trường hợp đặc biệt user yêu cầu rõ.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/malgunbd.ttf"  # Malgun Gothic Bold — chuẩn phụ đề kênh
YELLOW = (255, 224, 0)
WHITE = (255, 255, 255)
RED = (232, 28, 24)
BLACK = (6, 6, 6)

# ============ TEXT — sửa mỗi video (bám KHỐI 3 script) ============
# Mỗi dòng: (size, [(segment, màu), ...]) — segment RED tự vẽ double-stroke.
# [đang set: video 03 yedae-baegyeou-saida]
TOP = [
    (84, [("천사라던 백여우", WHITE)]),
    (168, [("민낯", RED), (" 공개", WHITE)]),
]
BOTTOM = [
    (98, [("카메라 한 대로 끝", YELLOW)]),
]
# Layout --right: ảnh có chủ thể bên TRÁI, dồn text vào vùng trống bên phải
# (mỗi dòng ngắn hơn nên tách tầng key làm 2 dòng, size chỉnh riêng).
RIGHT = [
    (70, [("동물 속마음이 들려요", WHITE)]),
    (138, [("남편 바람", WHITE)]),
    (150, [("딱", RED), (" 걸림", WHITE)]),
    (78, [("고양이가 다 말했다", YELLOW)]),
]
RIGHT_ZONE = (1060, 1920)  # vùng x chứa text
# ==================================================================


def font(sz):
    return ImageFont.truetype(FONT, sz)


def cover(src):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))


def band_scrim(img, y0, y1, strength, top=True):
    h = y1 - y0
    grad = Image.new("L", (1, h), 0)
    for y in range(h):
        t = (1 - y / h) if top else (y / h)
        grad.putpixel((0, y), int(strength * t))
    img.paste(Image.new("RGB", (W, h), (0, 0, 0)), (0, y0), grad.resize((W, h)))
    return img


def seg_draw(d, x, y, text, f, fill, ow):
    if fill == RED:
        # double-stroke chuẩn thị trường: quầng trắng ngoài → viền đen mỏng → ruột đỏ
        d.text((x, y), text, font=f, fill=WHITE, stroke_width=ow + 16, stroke_fill=WHITE)
        d.text((x, y), text, font=f, fill=fill, stroke_width=10, stroke_fill=BLACK)
    else:
        d.text((x, y), text, font=f, fill=fill, stroke_width=ow, stroke_fill=BLACK)


def line_h(sz, segs, ow):
    f = font(sz)
    text = "".join(s for s, _ in segs)
    bb = f.getbbox(text, stroke_width=ow + 16)
    return bb[3] - bb[1], bb[1]


def draw_line(d, x, y, sz, segs, ow):
    f = font(sz)
    # vẽ 2 lượt: lượt 1 các segment thường, lượt 2 segment RED (đè lên, halo trắng không bị che)
    cx = x
    pos = []
    for text, fill in segs:
        pos.append((cx, text, fill))
        cx += d.textlength(text, font=f)
    for px, text, fill in pos:
        if fill != RED:
            seg_draw(d, px, y, text, f, fill, ow)
    for px, text, fill in pos:
        if fill == RED:
            seg_draw(d, px, y, text, f, fill, ow)


def block_h(block, gap, ow):
    total = 0
    for sz, segs in block:
        h, _ = line_h(sz, segs, ow)
        total += h + gap
    return total - gap


def hband_scrim(img, x0, x1, strength):
    """Scrim ngang: tối dần từ x0 → x1 (đệm contrast cho text vùng phải)."""
    w = x1 - x0
    grad = Image.new("L", (w, 1), 0)
    for x in range(w):
        grad.putpixel((x, 0), int(strength * (x / w)))
    img.paste(Image.new("RGB", (w, H), (0, 0, 0)), (x0, 0), grad.resize((w, H)))
    return img


def render_right(img):
    d = ImageDraw.Draw(img)
    gap = 22
    ow = 16
    heights = [line_h(sz, segs, ow) for sz, segs in RIGHT]
    total = sum(h for h, _ in heights) + gap * (len(RIGHT) - 1)
    y = (H - total) // 2 - 10
    cx = (RIGHT_ZONE[0] + RIGHT_ZONE[1]) // 2
    for (sz, segs), (h, off) in zip(RIGHT, heights):
        f = font(sz)
        w = sum(d.textlength(t, font=f) for t, _ in segs)
        draw_line(d, cx - w // 2, y - off, sz, segs, ow)
        y += h + gap
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--dur", default="")
    ap.add_argument("--right", action="store_true",
                    help="text dồn cột phải (ảnh chủ thể bên trái), thay cho băng trên/dưới")
    args = ap.parse_args()

    if args.right:
        img = cover(args.photo).convert("RGB")
        img = hband_scrim(img, RIGHT_ZONE[0] - 120, W, 150)
        img = img.convert("RGBA")
        img = render_right(img)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(out)
        img.convert("RGB").resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
        img.convert("RGB").resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
        print("OK", out)
        return

    gap = 14
    top_h = block_h(TOP, gap, 18)
    bot_h = block_h(BOTTOM, gap, 18)

    img = cover(args.photo).convert("RGB")
    img = band_scrim(img, 0, top_h + 70, 190, top=True)
    img = band_scrim(img, H - bot_h - 100, H, 180, top=False)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    # TOP
    x, y = 44, 18
    for sz, segs in TOP:
        f = font(sz)
        text = "".join(s for s, _ in segs)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=20)
        draw_line(d, x, y - bb[1], sz, segs, 18)
        y += (bb[3] - bb[1]) + gap

    # BOTTOM (neo đáy)
    y = H - bot_h - 56
    for sz, segs in BOTTOM:
        f = font(sz)
        text = "".join(s for s, _ in segs)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=24)
        draw_line(d, 44, y - bb[1], sz, segs, 20 if sz >= 140 else 16)
        y += (bb[3] - bb[1]) + gap

    # badge thời lượng (--dur "" = tắt)
    if args.dur:
        fb = font(38)
        bb = d.textbbox((0, 0), args.dur, font=fb)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        px, py = W - bw - 40, H - bh - 26
        d.rectangle([px - 14, py - 8, px + bw + 14, py + bh + 12], fill=(0, 0, 0))
        d.text((px, py - bb[1] + 2), args.dur, font=fb, fill=WHITE)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out)
    img.convert("RGB").resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
    img.convert("RGB").resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out)


if __name__ == "__main__":
    main()
