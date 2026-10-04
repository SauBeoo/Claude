# -*- coding: utf-8 -*-
"""Thumbnail 3 tầng chuẩn kênh 古代の秘訣 (dựng lại layout đã duyệt ở video 06).

    tầng 1  chữ trắng viền đen, trên-trái            (fit ~60% bề ngang)
    tầng 2  TO NHẤT, nhiều màu trong 1 dòng          (fit ~99%) — ≥1/3 chiều cao khung
    tầng 3  chữ trắng trên BANNER ĐỎ sát đáy         (fit ~94%)
    badge   khối amber góc trên-phải: số tiền TO + dòng nhỏ

Nền: 1 ảnh, hoặc 2 ảnh chia đôi trước/sau (--photo A --photo2 B) như video 06.
Cỡ chữ TỰ TÍNH theo bề ngang → không phải đoán --size.

    python make_thumb_3dan.py out.png --photo bg.jpg [--photo2 bg2.jpg] \
        --line1 "..." --line2 "熱の7割|y" "は窓から|w" --line3 "..." \
        --badge "数百円" --badge-sub "すだれ・よしず"
"""
import argparse
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)
RED = (206, 26, 32)
AMBER = (245, 182, 12)
NAVY = (18, 30, 66)
COLS = {"w": WHITE, "y": YELLOW, "r": (255, 90, 80), "c": (120, 230, 255)}


def f(sz):
    return ImageFont.truetype(FONT, sz)


def measure(segs, sz):
    ft = f(sz)
    im = Image.new("RGB", (8, 8))
    d = ImageDraw.Draw(im)
    return sum(d.textlength(t, font=ft) for t, _ in segs)


def fit(segs, frac, lo=40, hi=340):
    """cỡ chữ lớn nhất mà tổng bề ngang ≤ frac * W"""
    target = W * frac
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if measure(segs, mid) <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo


def draw_segs(d, segs, x, y, sz, stroke):
    ft = f(sz)
    for t, c in segs:
        d.text((x, y), t, font=ft, fill=COLS.get(c, WHITE),
               stroke_width=stroke, stroke_fill=(0, 0, 0))
        x += d.textlength(t, font=ft)


def cover(im, box_w, box_h, crop=None):
    im = im.convert("RGB")
    if crop:
        x0, y0, x1, y1 = (int(v) for v in crop.split(","))
        im = im.crop((x0, y0, x1, y1))
    r = max(box_w / im.width, box_h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l = (im.width - box_w) // 2
    t = (im.height - box_h) // 2
    return im.crop((l, t, l + box_w, t + box_h))


def parse(vals):
    """"文字|y" -> [("文字","y")]; không có |màu thì trắng"""
    out = []
    for v in vals or []:
        if "|" in v:
            t, c = v.rsplit("|", 1)
        else:
            t, c = v, "w"
        out.append((t, c))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--photo", required=True)
    ap.add_argument("--photo2", help="ảnh nửa phải (bố cục trước/sau như video 06)")
    ap.add_argument("--line1", default="")
    ap.add_argument("--line2", nargs="*", default=[], help='mỗi khúc "chữ|màu" (w/y/r/c)')
    ap.add_argument("--line3", default="")
    ap.add_argument("--badge", default="", help="số tiền TO trên badge")
    ap.add_argument("--badge-sub", default="")
    ap.add_argument("--badge-size", type=int, default=108,
                    help="cỡ chữ badge góc trên-phải (mặc định 108 = như cũ). Mọi kích "
                         "thước khối badge scale theo. Thêm 2026-07-30: 108 lấn át tầng 2 "
                         "khi tầng 2 ngắn; 72-84 cân hơn.")
    ap.add_argument("--badge-pos", choices=("tr", "bl", "br"), default="tr",
                    help="góc đặt badge. Mặc định tr (như cũ) — NHƯNG tr trùng chỗ dấu 「秘」 "
                         "của stamp_brand.py, dùng tr thì phải stamp --pos tl. Khi bố cục "
                         "KHÔNG có banner tầng 3 thì dùng bl (đúng spec đã khoá: badge "
                         "dưới-TRÁI, 秘 trên-phải, dưới-phải để trống cho timestamp YouTube). "
                         "Thêm 2026-08-06 (video 16 co-dai).")
    ap.add_argument("--size3", type=int, default=0,
                    help="ép cỡ chữ banner tầng 3 (0 = tự). Chữ NGẮN (<=7 ký) auto chạm "
                         "trần 230px → banner cao 327px = 30%% khung, nuốt mất ảnh hero. "
                         "Đặt 140-170 để banner còn ~20%%. Thêm 2026-07-30 (video 14 co-dai).")
    ap.add_argument("--crop", default="", help="x0,y0,x1,y1 pixel ảnh gốc — crop sát chủ thể")
    ap.add_argument("--crop2", default="", help="crop cho --photo2")
    ap.add_argument("--frac2", type=float, default=0.0,
                    help="bề ngang tối đa tầng 2 (0 = tự: 0.90 khi có badge, 0.99 khi không)")
    ap.add_argument("--dim", type=float, default=0.18, help="hạ sáng nền cho chữ nổi")
    ap.add_argument("--bright", type=float, default=1.0,
                    help="NÂNG sáng ảnh nền (1.0 = như cũ, 1.3-1.6 khi ảnh gen ra nền tối "
                         "sì). Áp TRƯỚC --dim. Thêm 2026-07-30: ảnh navy tối + dim làm "
                         "thumbnail chìm ở 120px; nâng sáng rồi mới hạ dim mới giữ được "
                         "tương phản chữ. Kèm --sat để bù màu bị nhạt khi nâng sáng.")
    ap.add_argument("--sat", type=float, default=1.0,
                    help="độ rực màu nền (1.0 = như cũ; 1.1-1.25 bù cho --bright)")
    ap.add_argument("--blur-box", nargs="*", default=[],
                    help="x0,y0,x1,y1 trên khung 1920x1080 — làm mờ (xoá logo hãng, mặt người)")
    ap.add_argument("--divider", type=int, default=6, help="bề dày vạch chia 2 ảnh")
    # --- thêm 2026-08-03 (video 08): bố cục CHIỀU SÂU cần căn trái + chèn mặt ---
    ap.add_argument("--align2", choices=("center", "left", "right"), default="center",
                    help="căn tầng 2; 'left' cho ảnh có chủ thể nằm bên phải")
    ap.add_argument("--y2", type=int, default=0, help="ép toạ độ Y của tầng 2 (px)")
    ap.add_argument("--face", help="ảnh mặt (stock ẩn danh) chèn dạng ワイプ tròn — "
                                   "gate audience-45plus §1 mục 4 đòi ≥1 mặt biểu cảm")
    ap.add_argument("--face-box", default="40,720,300",
                    help="x,y,đường kính của khung mặt tròn")
    ap.add_argument("--face-warm", type=float, default=1.0,
                    help="hệ số ám vàng cho mặt, khớp tông nắng của nền")
    a = ap.parse_args()

    if a.photo2:
        canvas = Image.new("RGB", (W, H))
        canvas.paste(cover(Image.open(a.photo), W // 2, H, a.crop), (0, 0))
        canvas.paste(cover(Image.open(a.photo2), W - W // 2, H, a.crop2), (W // 2, 0))
        if a.divider:
            ImageDraw.Draw(canvas).rectangle(
                [W // 2 - a.divider // 2, 0, W // 2 + a.divider // 2, H], fill=(255, 146, 40))
    else:
        canvas = cover(Image.open(a.photo), W, H, a.crop)

    # xoá nhãn hiệu/mặt người đọc được (compliance: không tên thương hiệu thật)
    for b in a.blur_box:
        x0, y0, x1, y1 = (int(v) for v in b.split(","))
        reg = canvas.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(14))
        canvas.paste(reg, (x0, y0))

    if a.bright != 1.0:
        canvas = ImageEnhance.Brightness(canvas).enhance(a.bright)
    if a.sat != 1.0:
        canvas = ImageEnhance.Color(canvas).enhance(a.sat)

    if a.dim > 0:
        canvas = Image.blend(canvas, Image.new("RGB", (W, H), (0, 0, 0)), a.dim)

    d = ImageDraw.Draw(canvas)

    # tầng 1 — trên-trái
    if a.line1:
        s1 = [(a.line1, "w")]
        z1 = fit(s1, 0.60, hi=150)
        draw_segs(d, s1, 44, 26, z1, max(6, z1 // 12))
        y2 = 26 + int(z1 * 1.22)
    else:
        y2 = 40

    # tầng 2 — TO NHẤT, nhiều màu
    s2 = parse(a.line2)
    if s2:
        # có badge góc trên-phải → hạ bề ngang tầng 2 để chữ không chạm khối badge
        frac2 = a.frac2 or (0.90 if a.badge else 0.99)
        z2 = fit(s2, frac2, hi=400)
        wid = measure(s2, z2)
        x2 = {"center": (W - wid) / 2, "left": 48, "right": W - wid - 48}[a.align2]
        draw_segs(d, s2, x2, a.y2 or y2, z2, max(10, z2 // 11))

    # tầng 3 — banner đỏ sát đáy
    if a.line3:
        s3 = [(a.line3, "w")]
        z3 = a.size3 or fit(s3, 0.90, hi=230)
        wid = measure(s3, z3)
        bh = int(z3 * 1.42)
        by = H - bh - 26
        d.rounded_rectangle([26, by, W - 26, by + bh], radius=14, fill=RED)
        draw_segs(d, s3, (W - wid) / 2, by + int(bh * 0.11), z3, max(6, z3 // 14))

    # badge amber góc trên-phải
    if a.badge:
        zb = a.badge_size
        k = zb / 108.0                       # hệ số scale, =1.0 giữ y hệt bản cũ
        zs = round(46 * k)
        ftb, fts = f(zb), f(zs)
        wb = d.textlength(a.badge, font=ftb)
        ws = d.textlength(a.badge_sub, font=fts) if a.badge_sub else 0
        bw = int(max(wb, ws)) + round(56 * k)
        bh = int(zb * 1.25 + (zs * 1.2 if a.badge_sub else 0)) + round(18 * k)
        x0 = 40 if a.badge_pos == "bl" else W - bw - 40
        y0 = H - bh - 40 if a.badge_pos in ("bl", "br") else 24
        ty = y0 + round(8 * k)
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=round(18 * k), fill=AMBER,
                            outline=NAVY, width=max(2, round(5 * k)))
        d.text((x0 + (bw - wb) / 2, ty), a.badge, font=ftb, fill=NAVY)
        if a.badge_sub:
            d.text((x0 + (bw - ws) / 2, ty + int(zb * 1.18)), a.badge_sub, font=fts, fill=NAVY)

    # mặt ワイプ tròn (gate 45+ §1 mục 4) — ảnh stock ẩn danh, KHÔNG mặt người thật cụ thể
    if a.face:
        fx, fy, fd = (int(v) for v in a.face_box.split(","))
        fim = cover(Image.open(a.face), fd, fd)
        if a.face_warm != 1.0:
            r, g, b = fim.split()
            r = ImageEnhance.Brightness(r).enhance(a.face_warm)
            b = ImageEnhance.Brightness(b).enhance(2 - a.face_warm)
            fim = Image.merge("RGB", (r, g, b))
        mask = Image.new("L", (fd, fd), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, fd - 1, fd - 1], fill=255)
        ring = max(6, fd // 34)
        d.ellipse([fx - ring, fy - ring, fx + fd + ring, fy + fd + ring], fill=WHITE)
        canvas.paste(fim, (fx, fy), mask)

    canvas.save(a.out)
    print("->", a.out)


if __name__ == "__main__":
    main()
