# -*- coding: utf-8 -*-
"""make_thumb.py — thumbnail kênh 年金と老後のお金研究室 (nenkin) — BẢN RIÊNG của nenkin
(port từ health 2026-07-25; badge đảo màu navy/vàng 「年金研究室」; sổ xoay 8 khuôn: 03_THUMBNAIL_TITLE_FORMULA.md mục 5).
Theo 02_THUMBNAIL_TITLE_RULES.md (v3/v5) + 00_CHANNEL_BIBLE.md Mục 8 (dấu ấn riêng).
Chuẩn v3: CHỮ LÀ THUMBNAIL — cột 2–3 dòng lớn (MÓN trắng / TWIST vàng / STAKE đỏ to nhất)
xếp dọc nửa trái hoặc phải (--stack l|r), phủ 50–70%% khung; 袋文字 viền đen dày;
scrim full cạnh sau cột chữ; xuất kèm preview 480px + 120px (bài test mobile).
Chạy (v3, 3 dòng):
  python tools/make_thumb.py <photo.jpg> <out.png> --pop --stack l \
      --line1 "ブルーベリー" --line2 "夜に食べると" --line3 "眠れない!?" \
      --color1 white --color2 yellow --color3 red
Layout v2 cũ (2 dòng góc) vẫn chạy: --line1/--line2 --accent --accent-line --pos tr|bl...
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
WHITE = (255, 255, 255)
BLACK = (8, 8, 8)
ACCENTS = {"yellow": (255, 222, 0), "red": (255, 62, 48)}
COLORS = {"white": WHITE, "yellow": (255, 222, 0), "red": (255, 62, 48), "cyan": (150, 232, 236)}
# Màu nhận diện brand みんなの健康ノート (khóa cứng — bible Mục 8): navy đậm + 山吹色 amber
AMBER = (245, 182, 12)   # 山吹色 — nền badge
NAVY = (18, 30, 66)      # navy đậm — chữ + viền badge
PANEL_TOP = (30, 46, 92)  # nền panel chữ: navy sáng hơn (đỉnh)
PANEL_BOT = (7, 10, 22)   # navy thẫm gần đen (đáy) — gradient dọc, đủ tối cho chữ nổi


def font(sz):
    return ImageFont.truetype(FONT, sz)


def pop(img, sat=1.30, con=1.14, vig=95):
    """Bơm màu + vignette — chống 'cháo màu ấm' đơn điệu, đẩy chủ thể nổi khối."""
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Contrast(img).enhance(con)
    seed = Image.new("L", (9, 9), vig)
    for x in range(1, 8):
        for y in range(1, 8):
            seed.putpixel((x, y), 0)
    mask = seed.resize(img.size, Image.BICUBIC)
    img.paste(Image.new("RGB", img.size, (0, 0, 0)), (0, 0), mask)
    return img


def cover(src, focus="center", crop_px="", box=(0, 0, None, None)):
    """Cover-fit ảnh vào vùng box (mặc định full khung)."""
    bw = (box[2] if box[2] is not None else W) - box[0]
    bh = (box[3] if box[3] is not None else H) - box[1]
    im = Image.open(src).convert("RGB")
    if crop_px:
        x0, y0, x1, y1 = [int(v) for v in crop_px.split(",")]
        im = im.crop((x0, y0, x1, y1))
    s = max(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    if focus == "left":
        x0 = 0
    elif focus == "right":
        x0 = im.width - bw
    else:
        x0 = (im.width - bw) // 2
    y0 = (im.height - bh) // 2
    return im.crop((x0, y0, x0 + bw, y0 + bh))


def vgrad(w, h, top, bot):
    """Gradient dọc top→bot mượt (resize seed 1×2)."""
    seed = Image.new("RGB", (1, 2))
    seed.putpixel((0, 0), top); seed.putpixel((0, 1), bot)
    return seed.resize((w, h), Image.BILINEAR)


def panel_compose(src, side="r", frac=0.46, focus="center", crop_px="", fade=340):
    """Ảnh món một bên + nền GRADIENT navy (brand) bên kia đặt chữ (thay nền đen phẳng
    cũ 2026-07-25 — user muốn đẹp hơn). Gradient dọc PANEL_TOP→PANEL_BOT; fade blend ảnh
    TAN vào đúng gradient navy (không lộ mảng phẳng/mép cắt)."""
    pw = int(W * frac)
    canvas = vgrad(W, H, PANEL_TOP, PANEL_BOT)
    region = (W - pw, 0, W, H) if side == "r" else (0, 0, pw, H)
    photo = cover(src, focus, crop_px, box=region)
    canvas.paste(photo, (region[0], region[1]))
    fade = min(fade, pw)
    seed = Image.new("L", (2, 1))
    seed.putpixel((0, 0), 255); seed.putpixel((1, 0), 0)
    bg = vgrad(fade, H, PANEL_TOP, PANEL_BOT)  # nền fade = ĐÚNG gradient navy → blend liền mạch
    if side == "r":
        grad = seed.resize((fade, H), Image.BICUBIC)
        canvas.paste(bg, (W - pw, 0), grad)
    else:
        grad = seed.transpose(Image.FLIP_LEFT_RIGHT).resize((fade, H), Image.BICUBIC)
        canvas.paste(bg, (pw - fade, 0), grad)
    return canvas


def corner_scrim(img, corner="bl", w_frac=0.62, h_frac=0.52, strength=170):
    """Gradient tối ở góc chữ để 袋文字 nổi — mờ dần ra giữa khung."""
    gw, gh = int(W * w_frac), int(H * h_frac)
    # gradient 2 chiều mượt bằng resize BICUBIC từ seed 3x3
    seed = Image.new("L", (3, 3), 0)
    px = {"bl": (0, 2), "tl": (0, 0), "br": (2, 2), "tr": (2, 0)}[corner]
    seed.putpixel(px, strength)
    seed.putpixel(((px[0] + 1) % 3 if px[0] == 0 else px[0] - 1, px[1]), int(strength * 0.55))
    seed.putpixel((px[0], 1), int(strength * 0.55))
    grad = seed.resize((gw, gh), Image.BICUBIC)
    black = Image.new("RGB", (gw, gh), (0, 0, 0))
    ox = 0 if corner[1] == "l" else W - gw
    oy = 0 if corner[0] == "t" else H - gh
    img.paste(black, (ox, oy), grad)
    return img


def draw_line(d, x, y, text, f, fill, stroke):
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)


def draw_badge(img, text="年金研究室", pos="tl", margin=44):
    """Badge nhận diện kênh みんなの健康ノート (bible Mục 8): mẩu giấy note nền amber (山吹),
    chữ navy, viền navy + đổ bóng, nghiêng nhẹ như tờ note dán. Đóng cố định 1 góc MỌI thumbnail
    → dấu ấn nhận ra kênh trong 0.5s trên browse. Vẽ trên layer RGBA rồi xoay + dán."""
    fsz = 56
    f = font(fsz)
    pad_x, pad_y = 32, 18
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    bb = probe.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    pad = 26  # dư viền cho bóng + xoay
    layer = Image.new("RGBA", (bw + pad * 2, bh + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((pad + 7, pad + 9, pad + bw + 7, pad + bh + 9), radius=18, fill=(0, 0, 0, 95))  # bóng
    ld.rounded_rectangle((pad, pad, pad + bw, pad + bh), radius=18,
                         fill=NAVY + (255,), outline=AMBER + (255,), width=5)
    ld.text((pad + pad_x - bb[0], pad + pad_y - bb[1]), text, font=f, fill=AMBER + (255,))
    layer = layer.rotate(3, expand=True, resample=Image.BICUBIC)
    lw, lh = layer.size
    x = margin if pos.endswith("l") else W - lw - margin
    y = margin if pos.startswith("t") else H - lh - margin
    img.paste(layer, (x, y), layer)
    return img


def side_scrim(img, side="l", w_frac=0.60, strength=185):
    """Gradient tối full chiều cao ở nửa cột chữ (v3 stack) — chữ nổi trên mọi ảnh."""
    gw = int(W * w_frac)
    seed = Image.new("L", (5, 1), 0)
    if side == "l":
        vals = [strength, int(strength * 0.82), int(strength * 0.5), int(strength * 0.18), 0]
    else:
        vals = [0, int(strength * 0.18), int(strength * 0.5), int(strength * 0.82), strength]
    for i, v in enumerate(vals):
        seed.putpixel((i, 0), v)
    grad = seed.resize((gw, H), Image.BICUBIC)
    black = Image.new("RGB", (gw, H), (0, 0, 0))
    img.paste(black, (0 if side == "l" else W - gw, 0), grad)
    return img


def fit_font(d, text, size, max_w):
    """Co cỡ chữ để dòng (kèm stroke) không tràn quá max_w pixel."""
    while size > 80:
        f = font(size)
        st = max(14, size // 9)
        bb = d.textbbox((0, 0), text, font=f, stroke_width=st)
        if bb[2] - bb[0] <= max_w:
            return f, st, bb
        size -= 6
    f = font(size)
    st = max(14, size // 9)
    return f, st, d.textbbox((0, 0), text, font=f, stroke_width=st)


LIGHT_BOX = {"yellow", "cyan", "white"}


def render_stack(img, d, lines, colors, sizes, side="l", maxw=0.60, fill=False, boxes=None):
    """Layout v3: cột chữ xếp dọc nửa trái/phải.
    fill=True (chuẩn thị trường): tự phóng chữ tới khi khối chữ kín ~86%% chiều cao khung.
    boxes={idx: color}: dòng idx (1-based) nằm trong banner/box màu bo góc (chữ đen nếu màu sáng, trắng nếu đỏ)."""
    boxes = boxes or {}
    max_w = int(W * maxw)
    margin = 56
    gap = 22

    def fit_all(szs):
        out = []
        for text, size in zip(lines, szs):
            f, st, bb = fit_font(d, text, size, max_w)
            out.append((text, f, st, bb))
        return out

    sizes = list(sizes)
    fitted = fit_all(sizes)
    if fill:
        for _ in range(30):
            total = sum(bb[3] - bb[1] for _, _, _, bb in fitted) + gap * (len(fitted) - 1)
            if total >= H * 0.86:
                break
            sizes = [int(s * 1.06) for s in sizes]
            new = fit_all(sizes)
            ntotal = sum(bb[3] - bb[1] for _, _, _, bb in new) + gap * (len(new) - 1)
            if ntotal <= total:  # fit_font đã chặn trần bề ngang, không lớn thêm được
                break
            fitted = new

    total = sum(bb[3] - bb[1] for _, _, _, bb in fitted) + gap * (len(fitted) - 1)
    y = max(40, (H - total) // 2)
    for i, ((text, f, st, bb), color) in enumerate(zip(fitted, colors), start=1):
        lw, lh = bb[2] - bb[0], bb[3] - bb[1]
        x = margin if side == "l" else W - lw - margin
        if i in boxes:
            bc = COLORS[boxes[i]]
            pad_x, pad_y = 30, 14
            d.rounded_rectangle((x - pad_x, y - pad_y, x + lw + pad_x, y + lh + pad_y),
                                radius=18, fill=bc, outline=BLACK, width=6)
            tc = BLACK if boxes[i] in LIGHT_BOX else WHITE
            d.text((x, y - bb[1]), text, font=f, fill=tc)
        else:
            draw_line(d, x, y - bb[1], text, f, COLORS[color], st)
        y += lh + gap
    return img


def paste_inset(canvas, src, box, radius=26):
    """Cover-crop ảnh món vào box (x0,y0,x1,y1), bơm màu + bo góc, dán lên canvas."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    photo = pop(cover(src, "center", "", box=(0, 0, w, h)), vig=0)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    canvas.paste(photo, (x0, y0), mask)


def render_textwall(args):
    """Style 'nền đen + tường chữ (≤4 dòng) bên trái + 1–2 ảnh món bo góc bên phải'
    (mẫu thumbnail ranking senior). Nền đen làm chữ + món nổi bật tối đa."""
    canvas = Image.new("RGB", (W, H), (8, 8, 10))
    insets = [s for s in [args.inset1, args.inset2] if s]
    ix0 = int(W * 0.605)
    if len(insets) == 1:
        paste_inset(canvas, insets[0], (ix0, 96, W - 40, H - 96))
    elif len(insets) >= 2:
        paste_inset(canvas, insets[0], (ix0, 44, W - 40, H // 2 - 16))
        paste_inset(canvas, insets[1], (ix0, H // 2 + 16, W - 40, H - 44))
    d = ImageDraw.Draw(canvas)
    picks = [(args.line1, args.color1, args.size1), (args.line2, args.color2, args.size2),
             (args.line3, args.color3, args.size3), (args.line4, args.color4, args.size4)]
    lines = [t for t, _, _ in picks if t]
    colors = [c for t, c, _ in picks if t]
    sizes = [s for t, _, s in picks if t]
    render_stack(canvas, d, lines, colors, sizes, "l", args.maxw, args.fill)
    if args.badge:
        draw_badge(canvas, args.badge_text, args.badge_pos or "tr")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    canvas.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
    canvas.resize((120, 68), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK (textwall)", out, "+ preview480/preview120")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--line1", required=True, help="dòng 1 — v3: MÓN (trắng)")
    ap.add_argument("--line2", default="", help="dòng 2 — v3: TWIST (vàng)")
    ap.add_argument("--line3", default="", help="dòng 3 — v3: STAKE (đỏ, to nhất). Có line3 → tự dùng layout stack")
    ap.add_argument("--stack", choices=["l", "r"], default="", help="cột chữ v3 nửa trái/phải (mặc định l khi có line3)")
    ap.add_argument("--fill", action="store_true", help="phóng khối chữ kín ~86%% chiều cao (chuẩn thị trường)")
    ap.add_argument("--dim", type=float, default=0.0, help="0–0.5: làm tối toàn ảnh để chữ nổi (kiểu nền đen thị trường)")
    ap.add_argument("--maxw", type=float, default=0.60, help="bề ngang tối đa của cột chữ (tỉ lệ khung)")
    ap.add_argument("--box", nargs="*", default=[], help="dòng nằm trong banner màu, dạng N:color — vd 1:red")
    ap.add_argument("--panel", type=float, default=0.0, help="0.4–0.55: ảnh món cover phần này của khung, phần kia panel đen đặt chữ (chuẩn mẫu 1,3M — chữ KHÔNG bao giờ đè món)")
    ap.add_argument("--panel-side", choices=["l", "r"], default="r", help="phía đặt ẢNH (chữ nằm phía ngược lại)")
    ap.add_argument("--panel-fade", type=int, default=340, help="bề rộng gradient tan vào bóng tối (px) — 340 chuẩn v23, nhỏ = mép rõ")
    ap.add_argument("--color1", choices=list(COLORS), default="white")
    ap.add_argument("--color2", choices=list(COLORS), default="yellow")
    ap.add_argument("--color3", choices=list(COLORS), default="red")
    ap.add_argument("--size3", type=int, default=210)
    ap.add_argument("--accent", choices=list(ACCENTS), default="yellow")
    ap.add_argument("--pos", choices=["bl", "tl", "br", "tr"], default="bl", help="góc đặt chữ (layout v2 cũ)")
    ap.add_argument("--mosaic-box", default="", help="x0,y0,x1,y1 (tỉ lệ khung) — mosaic giấu đáp án + ？màu nhấn")
    ap.add_argument("--crop", default="", help="x0,y0,x1,y1 (pixel ảnh gốc) — crop sát chủ thể TRƯỚC khi cover")
    ap.add_argument("--pop", action="store_true", help="bơm màu + contrast + vignette")
    ap.add_argument("--accent-line", type=int, choices=[1, 2], default=2, help="dòng mang màu nhấn")
    ap.add_argument("--size1", type=int, default=185)
    ap.add_argument("--size2", type=int, default=160)
    ap.add_argument("--focus", choices=["left", "center", "right"], default="center")
    ap.add_argument("--arrow", action="store_true", help="mũi tên màu nhấn chỉ vào món (cạnh dòng 2)")
    ap.add_argument("--no-badge", dest="badge", action="store_false", help="tắt badge nhận diện 年金研究室 (mặc định BẬT)")
    ap.add_argument("--badge-text", default="年金研究室", help="chữ trên badge nhận diện")
    ap.add_argument("--badge-pos", default="", choices=["", "tl", "tr", "bl", "br"],
                    help="góc badge (mặc định: phía ẢNH, ngược cột chữ)")
    ap.add_argument("--textwall", action="store_true",
                    help="style nền đen + tường chữ ≤4 dòng trái + ảnh món bên phải (mẫu ranking senior)")
    ap.add_argument("--line4", default="", help="dòng 4 (textwall)")
    ap.add_argument("--color4", choices=list(COLORS), default="white")
    ap.add_argument("--size4", type=int, default=175)
    ap.add_argument("--inset1", default="", help="ảnh món inset TRÊN-phải (textwall)")
    ap.add_argument("--inset2", default="", help="ảnh món inset DƯỚI-phải (textwall)")
    ap.set_defaults(badge=True)
    args = ap.parse_args()

    if args.textwall:
        render_textwall(args)
        return

    for i, t in enumerate([args.line1, args.line2, args.line3]):
        if t and len(t) > 8:
            print(f"⚠️ dòng {i+1} dài {len(t)} ký tự (luật ≤8): '{t}' — cân nhắc rút gọn")

    stack = args.stack or ("l" if args.line3 else "")
    # Badge đặt phía ẢNH (ngược cột chữ) để không đè chữ; non-stack → tl
    badge_pos = args.badge_pos or ("tr" if stack == "l" else "tl" if stack == "r" else "tl")

    if args.panel > 0:
        stack = "l" if args.panel_side == "r" else "r"
        img = panel_compose(args.photo, args.panel_side, args.panel, args.focus, args.crop, args.panel_fade)
        if args.pop:
            img = pop(img, vig=0)
    else:
        img = cover(args.photo, args.focus, args.crop)
        if args.pop:
            img = pop(img)
        if args.dim > 0:
            img = ImageEnhance.Brightness(img).enhance(1.0 - args.dim)
        if stack:
            img = side_scrim(img, stack)
        else:
            img = corner_scrim(img, args.pos, strength=175)
    d = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    # mosaic giấu đáp án + 「？」 (curiosity gap bằng hình — luật A8)
    if args.mosaic_box:
        bx0, by0, bx1, by1 = [float(v) for v in args.mosaic_box.split(",")]
        box = (int(bx0 * W), int(by0 * H), int(bx1 * W), int(by1 * H))
        region = img.crop(box)
        rw, rh = region.size
        region = region.resize((max(1, rw // 15), max(1, rh // 15)), Image.LANCZOS)
        img.paste(region.resize((rw, rh), Image.NEAREST), box)
        d.rounded_rectangle(box, radius=20, outline=accent, width=9)
        qs = int(min(rw * 1.15, rh * 0.7))
        fq = font(qs)
        qb = d.textbbox((0, 0), "？", font=fq, stroke_width=qs // 12)
        qx = (box[0] + box[2]) // 2 - (qb[2] - qb[0]) // 2
        qy = (box[1] + box[3]) // 2 - (qb[3] - qb[1]) // 2 - qb[1]
        d.text((qx, qy), "？", font=fq, fill=accent, stroke_width=qs // 12, stroke_fill=BLACK)

    if stack:
        lines = [t for t in [args.line1, args.line2, args.line3] if t]
        colors = [c for t, c in zip([args.line1, args.line2, args.line3],
                                    [args.color1, args.color2, args.color3]) if t]
        sizes = [s for t, s in zip([args.line1, args.line2, args.line3],
                                   [args.size1, args.size2, args.size3]) if t]
        boxes = {}
        for spec in args.box:
            n, c = spec.split(":")
            boxes[int(n)] = c
        render_stack(img, d, lines, colors, sizes, stack, args.maxw, args.fill, boxes)
        if args.badge:
            draw_badge(img, args.badge_text, badge_pos)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
        img.resize((120, 68), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
        print("OK (stack v3)", out, "+ preview480/preview120")
        return

    f1, f2 = font(args.size1), font(args.size2)
    s1, s2 = max(14, args.size1 // 10), max(12, args.size2 // 10)
    bb1 = d.textbbox((0, 0), args.line1, font=f1, stroke_width=s1)
    h1 = bb1[3] - bb1[1]
    gap = 26
    if args.line2:
        bb2 = d.textbbox((0, 0), args.line2, font=f2, stroke_width=s2)
        h2 = bb2[3] - bb2[1]
    else:
        bb2, h2 = None, 0

    total = h1 + ((gap + h2) if args.line2 else 0)
    y = 44 if args.pos.startswith("t") else H - total - 64
    right = args.pos.endswith("r")
    x1_ = (W - (bb1[2] - bb1[0]) - 56) if right else 56

    c1 = accent if args.accent_line == 1 else WHITE
    c2 = accent if args.accent_line == 2 else WHITE
    draw_line(d, x1_, y - bb1[1], args.line1, f1, c1, s1)
    if args.line2:
        y2 = y + h1 + gap
        x2_ = (W - (bb2[2] - bb2[0]) - 56) if right else 56
        draw_line(d, x2_, y2 - bb2[1], args.line2, f2, c2, s2)
        if args.arrow:
            ax = x + (bb2[2] - bb2[0]) + 46
            cy = y2 + h2 // 2
            ah = int(h2 * 0.42)
            d.polygon([(ax, cy - ah), (ax, cy + ah), (ax + int(ah * 1.5), cy)],
                      fill=accent, outline=BLACK, width=8)

    if args.badge:
        draw_badge(img, args.badge_text, badge_pos)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview480.png"))
    img.resize((120, 68), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out, "+ preview480/preview120")


if __name__ == "__main__":
    main()
