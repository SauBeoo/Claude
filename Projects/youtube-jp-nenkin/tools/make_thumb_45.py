# -*- coding: utf-8 -*-
"""make_thumb_45.py — KHUÔN A-45 của kênh nenkin: khuôn A (banner đen + dải đỏ dọc + màu tín hiệu)
NHƯNG đạt gate `.claude/rules/audience-45plus.md` §1:
  1. dòng chính ≤6 ký tự (mặc định dùng CON SỐ, 2–4 ký)
  2. dòng chính cao ≥1/3 khung (auto-scale theo --hero-h, mặc định 0.34)
  3. tổng ≤3 dòng chữ  → banner trên (1) + dòng điều kiện trắng (2) + số hero đỏ (3).
     Dải đỏ dọc trái GIỮ nhưng BỎ CHỮ (thành vạch màu nhận diện) · tag vàng BỎ.
  4. ≥1 mặt biểu cảm — do ảnh nền lo, tool chỉ cảnh báo nếu --no-face
  6. nền tương phản: scrim trái + làm sáng nhẹ vùng chủ thể

Dùng: python tools/make_thumb_45.py <out.png> --bg <scene.jpg> --banner1 ... --banner2 ...
      --l1 "..." --hero "42万"
"""
import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
RED = (226, 26, 26)
YEL = (255, 214, 0)
BH = 186          # banner đen trên (khuôn A = 168; 186 để nuốt phần bake cũ, giữ nguyên tỉ lệ nhìn)
VW = 96           # dải đỏ dọc trái


def font(s):
    return ImageFont.truetype(FONT, s)


def cover(src, focus="right"):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = {"left": 0, "right": im.width - W, "center": (im.width - W) // 2}[focus]
    y0 = (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))


def left_scrim(img, wfrac, strength=205):
    gw = int(W * wfrac)
    seed = Image.new("L", (5, 1), 0)
    for i, v in enumerate([strength, int(strength * .85), int(strength * .5), int(strength * .16), 0]):
        seed.putpixel((i, 0), v)
    img.paste(Image.new("RGB", (gw, H), (0, 0, 0)), (0, 0), seed.resize((gw, H), Image.BICUBIC))
    return img


def fit_w(d, text, maxw, start, floor=60):
    """to nhất có thể mà vẫn lọt maxw"""
    s = start
    while s > floor:
        f = font(s)
        st = max(10, s // 9)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=st)
        if bb[2] - bb[0] <= maxw:
            return f, st, bb
        s -= 4
    f = font(s)
    st = max(10, s // 9)
    return f, st, d.textbbox((0, 0), text, font=f, stroke_width=st)


NAVY = (16, 30, 72)
YAMABUKI = (255, 190, 0)


def badge(img, text="年金研究室", pos="br", h=92, angle=-4.0):
    """Con dấu nhận diện kênh — navy đậm / chữ vàng 山吹, nghiêng nhẹ + bóng.
    Phần BẤT BIẾN của mọi thumbnail nenkin (03_THUMBNAIL_TITLE_FORMULA.md §5b):
    mọi thứ khác xoay, badge KHÔNG đổi. Luôn đặt ở góc phía ẢNH (đối diện cột chữ)."""
    fs = int(h * 0.62)
    f = font(fs)
    pad_x, pad_y = int(h * 0.30), int(h * 0.19)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    bb = tmp.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bw, bh = tw + pad_x * 2, th + pad_y * 2

    lay = Image.new("RGBA", (bw + 16, bh + 16), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((8, 8, 8 + bw, 8 + bh), radius=int(h * 0.16),
                         fill=NAVY + (255,), outline=YAMABUKI + (255,), width=max(3, h // 26))
    ld.text((8 + pad_x - bb[0], 8 + pad_y - bb[1]), text, font=f, fill=YAMABUKI + (255,))
    lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)

    m = 40
    x = W - lay.width - m if pos.endswith("r") else m
    y = H - lay.height - m if pos.startswith("b") else BH + m

    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 120), (0, 0), lay.split()[3])
    img.paste(Image.alpha_composite(
        Image.new("RGBA", lay.size, (0, 0, 0, 0)), sh).convert("RGB"),
        (x + 6, y + 7), sh.split()[3])
    img.paste(lay.convert("RGB"), (x, y), lay.split()[3])
    return img


def fit_h(d, text, target_h, maxw, cap=560):
    """scale theo CHIỀU CAO mực (gate ≥1/3 khung), vẫn không được tràn maxw"""
    s = 40
    best = None
    while s < cap:
        f = font(s)
        st = max(12, s // 10)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=st)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w > maxw:
            break
        best = (f, st, bb)
        if h >= target_h:
            break
        s += 4
    if best is None:
        best = (font(40), 12, d.textbbox((0, 0), text, font=font(40), stroke_width=12))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--bg", required=True)
    ap.add_argument("--banner1", default="")           # vàng
    ap.add_argument("--banner2", default="")           # đỏ (viền trắng)
    ap.add_argument("--l1", default="")                # dòng điều kiện, trắng viền đen
    ap.add_argument("--hero", required=True)           # ≤6 ký, ĐỎ viền trắng — dòng chính
    ap.add_argument("--hero-h", type=float, default=0.34, help="chiều cao mực dòng chính / H (gate ≥0.333)")
    ap.add_argument("--hero-maxw", type=float, default=0.66, help="bề ngang tối đa dòng chính / W")
    ap.add_argument("--l1-maxw", type=float, default=0.47)
    ap.add_argument("--bottom", type=int, default=1006, help="đáy khối chữ (px)")
    ap.add_argument("--scrim", type=float, default=0.60)
    ap.add_argument("--badge", default="年金研究室", help="con dấu nhận diện kênh (rỗng = tắt)")
    ap.add_argument("--badge-pos", default="br", choices=["br", "tr", "bl"])
    ap.add_argument("--badge-h", type=int, default=92)
    args = ap.parse_args()

    img = cover(args.bg, focus="right")
    img = left_scrim(img, wfrac=args.scrim)
    d = ImageDraw.Draw(img)

    # ── 1. banner đen trên ──────────────────────────────────────────────
    d.rectangle((0, 0, W, BH), fill=BLACK)
    txt = (args.banner1 + ("　" if args.banner1 and args.banner2 else "") + args.banner2)
    if txt.strip():
        f1, st1, bb1 = fit_w(d, txt, W - 90, 118, floor=64)
        tx, ty = 54, (BH - (bb1[3] - bb1[1])) // 2 - bb1[1]
        if args.banner1:
            d.text((tx, ty), args.banner1 + ("　" if args.banner2 else ""), font=f1, fill=YEL,
                   stroke_width=st1, stroke_fill=BLACK)
        if args.banner2:
            w0 = d.textbbox((0, 0), args.banner1 + "　", font=f1, stroke_width=st1)[2] if args.banner1 else 0
            d.text((tx + w0, ty), args.banner2, font=f1, fill=RED, stroke_width=st1, stroke_fill=WHITE)

    # ── 2. dải đỏ dọc trái (KHÔNG chữ — gate ≤3 dòng) ───────────────────
    d.rectangle((0, BH, VW, H), fill=RED)

    left = VW + 40

    # ── 3. dòng chính (số) — scale theo CHIỀU CAO ───────────────────────
    fh, sth, bbh = fit_h(d, args.hero, int(H * args.hero_h), int(W * args.hero_maxw))
    hero_h = bbh[3] - bbh[1]
    hero_y = args.bottom - hero_h
    d.text((left, hero_y - bbh[1]), args.hero, font=fh, fill=RED, stroke_width=sth, stroke_fill=WHITE)

    # ── 4. dòng điều kiện trắng, ngay trên số ───────────────────────────
    if args.l1:
        f2, st2, bb2 = fit_w(d, args.l1, int(W * args.l1_maxw), 132, floor=70)
        h2 = bb2[3] - bb2[1]
        y2 = hero_y - 26 - h2
        y2 = max(y2, BH + 24)
        d.text((left, y2 - bb2[1]), args.l1, font=f2, fill=WHITE, stroke_width=st2, stroke_fill=BLACK)

    # ── 5. badge nhận diện kênh (bất biến) ──────────────────────────────
    if args.badge.strip():
        img = badge(img, args.badge, pos=args.badge_pos, h=args.badge_h)

    o = Path(args.out)
    o.parent.mkdir(parents=True, exist_ok=True)
    img.save(o)
    img.resize((480, 270), Image.LANCZOS).save(o.parent / (o.stem + "_preview480.png"))
    img.resize((168, 95), Image.LANCZOS).save(o.parent / (o.stem + "_preview168.png"))
    pct = hero_h / H * 100
    print(f"OK {o}  | dòng chính '{args.hero}' = {len(args.hero)} ký, cao {hero_h}px = {pct:.1f}% khung "
          f"({'ĐẠT' if pct >= 33.3 else 'CHƯA ĐẠT'} gate ≥1/3) | 3 dòng chữ")


if __name__ == "__main__":
    main()
