# -*- coding: utf-8 -*-
"""make_thumb_scene.py — thumbnail 朗読 SCENE. Ảnh giữ nguyên (không lật).
v2 (2026-07-11, sau chẩn đoán video 01 chết CTR): TỐI ĐA 3 khối chữ, mỗi khối phải đọc
được ở 120px — BỎ các dòng phụ nhỏ. Đòn đinh dùng MÀU ĐỎ double-stroke (viền trắng
ngoài + đen trong, chuẩn thị trường スカッと); các dòng còn lại TRẮNG/VÀNG 袋文字 viền đen.
Bố cục CHỪA MẶT NHÂN VẬT: text dồn vào BĂNG TRÊN + BĂNG ĐÁY, để trống khoảng giữa.
Chạy: python tools/make_thumb_scene.py <scene.jpg> <out.png> [--dur H:MM:SS]
Sửa text trong TOP / BOTTOM (bám KHỐI 2 của script).
"""
import sys, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
YELLOW = (255, 224, 0)
WHITE = (255, 255, 255)
RED = (232, 28, 24)
BLACK = (6, 6, 6)

# BĂNG TRÊN (trên đầu nhân vật) — tối đa 2 dòng  [đang set: video 06 sankaiki — layout MỚI:
# 1 dòng trắng căn PHẢI trên đầu phản diện + cụm đáy căn GIỮA chữ TO (user 2026-07-17)]
# Mỗi dòng: (text, size, màu[, align]) — align: 'left' (mặc định) | 'center' | 'right'
# [video 09 aikagi-mudan-doukyo — ĐANG ACTIVE]
TOP = [
    ("義母「工房は仏間にｗ」", 124, WHITE, "center"),
    ("私「土地は誰の名義?」", 142, YELLOW, "center"),
]
# BĂNG ĐÁY — đòn đinh CỰC TO (đỏ double-stroke)
BOTTOM = [
    ("注文書に夫の名前ｗ", 158, RED, "center"),
]
# [video 08 sokurikon-ichioku — giữ để render lại]
# TOP = [("夫と愛人「離婚してくれ」", 104, WHITE, "center"), ("私「借金1億あるけど」", 122, YELLOW, "center")]
# BOTTOM = [("1か月後、鬼電がｗ", 158, RED, "center")]
# [video 07 kadan — giữ để render lại]
# TOP = [("「ゴミは引っ込んでろｗ」", 118, YELLOW, "left"), ("甘味処を夢見た夫が", 96, WHITE, "left")]
# BOTTOM = [("部長が土下座した", 170, RED, "center")]
# [video 06 sankaiki — giữ để render lại]
# TOP = [("義母の三回忌の夜", 118, WHITE, "right")]
# BOTTOM = [("「あんたの部屋はもうない」", 132, YELLOW, "center"), ("義母の声が響いた", 205, RED, "center")]
# [video 05 musume-no-sakubun — giữ để render lại]
# TOP = [("娘の作文を破った担任", 112, WHITE), ("「父親を呼べｗ」", 138, YELLOW)]
# BOTTOM = [("現れたのは警視正", 176, RED)]
# [video 04 settai-onzoushi — giữ để render lại]
# TOP = [("接待の料亭で", 112, WHITE), ("「底辺の旦那を呼べ」", 138, YELLOW)]
# BOTTOM = [("社長が90度頭を下げた", 176, RED)]
# [video 03 shimotsukiya — giữ để render lại]
# TOP = [("「中卒の爺さんが", 92, WHITE), ("社長ごっこですかｗ」", 114, YELLOW)]
# BOTTOM = [("社長が土下座した", 155, RED)]
# [video 02 moto-otto — giữ để render lại]
# TOP = [("元夫が若い女を連れて来た", 92, WHITE), ("「元嫁も式を祝えよw」", 114, YELLOW)]
# BOTTOM = [("顔面蒼白になった", 160, RED)]
# [video 01 musuko-hirouen — giữ để render lại]
# TOP = [("息子の披露宴で", 96, WHITE), ("夫が愛人を私の隣に", 116, YELLOW)]
# BOTTOM = [("頭取が90度頭を下げた", 152, RED)]


def font(sz):
    return ImageFont.truetype(FONT, sz)


def fit_items(items, max_w, stroke):
    """Hạ cỡ từng dòng đến khi lọt max_w (giữ chữ TO nhất mà không tràn)."""
    out = []
    for item in items:
        text, sz, fill = item[0], item[1], item[2]
        align = item[3] if len(item) > 3 else "left"
        while sz > 40:
            bb = font(sz).getbbox(text, stroke_width=stroke)
            if bb[2] - bb[0] <= max_w:
                break
            sz -= 2
        out.append((text, sz, fill, align))
    return out


def align_x(d, text, f, stroke, align, margin):
    """Tính x theo align trong khung W với lề margin."""
    bb = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    tw = bb[2] - bb[0]
    if align == "center":
        return (W - tw) // 2
    if align == "right":
        return W - tw - margin
    return margin


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


def fk(d, x, y, text, f, fill, ow):
    if fill == RED:
        # double-stroke chuẩn thị trường: quầng trắng ngoài → viền đen mỏng → ruột đỏ
        d.text((x, y), text, font=f, fill=WHITE, stroke_width=ow + 16, stroke_fill=WHITE)
        d.text((x, y), text, font=f, fill=fill, stroke_width=10, stroke_fill=BLACK)
    else:
        d.text((x, y), text, font=f, fill=fill, stroke_width=ow, stroke_fill=BLACK)


def measure(items, gap):
    total = 0
    hs = []
    for text, sz, *_ in items:
        bb = font(sz).getbbox(text, stroke_width=20)
        h = bb[3] - bb[1]
        hs.append((h, bb[1]))
        total += h + gap
    return total - gap, hs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("out")
    # QUY TẮC (user chốt 2026-07-13, đồng bộ kr-romfan): KHÔNG badge thời lượng góc
    # thumbnail — YouTube tự hiện duration. --dur chỉ bật khi user yêu cầu rõ.
    ap.add_argument("--dur", default="")
    args = ap.parse_args()

    gap = 12
    top = fit_items(TOP, W - 84, 20)       # auto-fit chiều rộng, chừa lề
    bottom = fit_items(BOTTOM, W - 80, 42)
    top_h, _ = measure(top, gap)
    bot_h, _ = measure(bottom, gap)

    img = cover(args.scene).convert("RGB")
    img = band_scrim(img, 0, top_h + 60, 185, top=True)
    img = band_scrim(img, H - bot_h - 90, H, 175, top=False)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    # TOP
    y = 14
    for text, sz, fill, align in top:
        f = font(sz)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=20)
        x = align_x(d, text, f, 20, align, 42)
        fk(d, x, y - bb[1], text, f, fill, 18)
        y += (bb[3] - bb[1]) + gap

    # BOTTOM (neo đáy, xếp từ dưới lên)
    y = H - bot_h - 54
    for text, sz, fill, align in bottom:
        f = font(sz)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=26)
        x = align_x(d, text, f, 26, align, 40)
        fk(d, x, y - bb[1], text, f, fill, 24 if sz >= 140 else 18)
        y += (bb[3] - bb[1]) + gap

    # badge thời lượng (--dur "" = tắt)
    if args.dur:
        fb = font(36)
        bb = d.textbbox((0, 0), args.dur, font=fb)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        px, py = W - bw - 40, H - bh - 26
        d.rectangle([px - 14, py - 8, px + bw + 14, py + bh + 12], fill=(0, 0, 0))
        d.text((px, py - bb[1] + 2), args.dur, font=fb, fill=WHITE)

    out = Path(args.out)
    img.convert("RGB").save(out)
    img.convert("RGB").resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview.png"))
    img.convert("RGB").resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out)


if __name__ == "__main__":
    main()
