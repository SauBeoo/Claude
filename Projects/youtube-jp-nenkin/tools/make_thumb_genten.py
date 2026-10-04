# -*- coding: utf-8 -*-
"""make_thumb_genten.py — KHUÔN 原典 của kênh nenkin (user chốt 2026-08-03).

Bộ mặt: TRANG TÀI LIỆU + CON SỐ BỊ KHOANH ĐỎ BẰNG TAY + mũi tên trỏ.
Đây là móc nhận diện riêng của kênh (persona 研究室, chuẩn visual CLAUDE.md
§原典スライド) — không kênh nào trong ngách 年金 làm bộ mặt kiểu này, nên
"nhìn thấy là biết kênh mình" theo đúng nghĩa, không phải chỉ đổi màu chữ.

Khác khuôn A-45 ở chỗ: nền không còn là ảnh người mà là GIẤY; ảnh người
thu về ảnh cắt tròn góc phải. Giữ lại banner đen + badge để không mất
nhận diện đã có.

Gate `.claude/rules/audience-45plus.md` §1:
  1. dòng chính ≤6 ký (dùng 2–4 ký: số tiền / số tuổi)
  2. dòng chính cao ≥1/3 khung — tool tự scale, in ĐẠT/CHƯA ĐẠT
  3. đúng 3 khối chữ: banner (1) + nhãn mục trên giấy (2) + số hero (3)
  4. ≥1 mặt biểu cảm — ảnh cắt tròn, --face để canh đúng mặt
  6. nền sáng: giấy kẻ ô

Dùng:
  python tools/make_thumb_genten.py <out.png> --bg <scene.jpg> --face cx,cy,r
      --banner1 "2026年 年金改正" --banner2 "働きながら年金"
      --label "支給停止調整額" --hero "65万"
--face: tâm mặt + bán kính tính theo TỈ LỆ ảnh gốc (0–1), vd 0.48,0.20,0.13
"""
import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from make_drawn import paper, seeded, sketch_ellipse, sketch_arrow, stroke  # noqa: E402

W, H = 1920, 1080
FONT_B = "C:/Windows/Fonts/YuGothB.ttc"
FONT_R = "C:/Windows/Fonts/YuGothR.ttc"
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
INK = (28, 32, 40)
RED = (214, 22, 22)
YEL = (255, 214, 0)
NAVY = (16, 30, 72)
YAMABUKI = (255, 190, 0)
BH = 152                      # banner đen trên
PANEL = (40, 214, 1362, 1010)  # trang tài liệu


def font(path, s):
    return ImageFont.truetype(path, s)


def fit_w(d, text, maxw, start, f=FONT_B, floor=40, stroke_k=9):
    s = start
    while s > floor:
        ft = font(f, s)
        st = max(0, s // stroke_k) if stroke_k else 0
        bb = d.textbbox((0, 0), text, font=ft, stroke_width=st)
        if bb[2] - bb[0] <= maxw:
            return ft, st, bb
        s -= 4
    ft = font(f, s)
    st = max(0, s // stroke_k) if stroke_k else 0
    return ft, st, d.textbbox((0, 0), text, font=ft, stroke_width=st)


def fit_h(d, text, target_h, maxw, f=FONT_B, cap=620):
    """scale theo CHIỀU CAO mực (gate ≥1/3 khung), không tràn maxw."""
    s, best = 40, None
    while s < cap:
        ft = font(f, s)
        bb = d.textbbox((0, 0), text, font=ft)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w > maxw:
            break
        best = (ft, bb)
        if h >= target_h:
            break
        s += 4
    return best or (font(f, 40), d.textbbox((0, 0), text, font=font(f, 40)))


def face_cutout(src, face, d_px):
    """Ảnh cắt tròn quanh mặt + viền vàng + bóng. face = (cx,cy,r) tỉ lệ 0–1."""
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    cx, cy, r = face[0] * iw, face[1] * ih, face[2] * min(iw, ih)
    box = (cx - r, cy - r, cx + r, cy + r)
    crop = im.crop(tuple(int(v) for v in box)).resize((d_px, d_px), Image.LANCZOS)

    mask = Image.new("L", (d_px * 4, d_px * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d_px * 4 - 1, d_px * 4 - 1), fill=255)
    mask = mask.resize((d_px, d_px), Image.LANCZOS)

    pad = 26
    lay = Image.new("RGBA", (d_px + pad * 2, d_px + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((pad - 4, pad + 4, pad + d_px + 4, pad + d_px + 12),
                               fill=(0, 0, 0, 105))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    ring = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((pad - 9, pad - 9, pad + d_px + 9, pad + d_px + 9),
                                 fill=YAMABUKI + (255,))
    lay.alpha_composite(ring)
    lay.paste(crop, (pad, pad), mask)
    return lay


def badge(img, text="年金研究室", h=118, angle=-4.0, margin=34, pos="bl"):
    """⚠️ MẶC ĐỊNH góc dưới TRÁI: YouTube in timestamp thời lượng ở góc dưới PHẢI
    và đè lên badge (bắt được khi 3 bản đầu đã lên sóng 2026-08-03). Đừng đổi về 'br'."""
    fs = int(h * 0.62)
    f = font(FONT_B, fs)
    px_, py_ = int(h * 0.30), int(h * 0.19)
    bb = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=f)
    bw, bh = bb[2] - bb[0] + px_ * 2, bb[3] - bb[1] + py_ * 2
    lay = Image.new("RGBA", (bw + 16, bh + 16), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((8, 8, 8 + bw, 8 + bh), radius=int(h * 0.16),
                         fill=NAVY + (255,), outline=YAMABUKI + (255,), width=max(3, h // 26))
    ld.text((8 + px_ - bb[0], 8 + py_ - bb[1]), text, font=f, fill=YAMABUKI + (255,))
    lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    x = margin if pos.endswith("l") else W - lay.width - margin
    y = margin + BH if pos.startswith("t") else H - lay.height - margin
    img.paste(lay.convert("RGB"), (x, y), lay.split()[3])
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--bg", required=True, help="ảnh người — chỉ dùng phần MẶT cắt tròn")
    ap.add_argument("--face", default="0.5,0.25,0.13", help="cx,cy,r theo tỉ lệ ảnh gốc")
    ap.add_argument("--banner1", default="")
    ap.add_argument("--banner2", default="")
    ap.add_argument("--label", required=True, help="nhãn mục trên trang giấy")
    ap.add_argument("--hero", required=True, help="2–4 ký: số tiền / số tuổi")
    ap.add_argument("--hero-h", type=float, default=0.34)
    ap.add_argument("--face-d", type=int, default=430)
    ap.add_argument("--badge", default="年金研究室")
    ap.add_argument("--badge-pos", default="bl", choices=["bl", "br", "tl", "tr"],
                    help="MẶC ĐỊNH bl — góc dưới PHẢI bị YouTube đè timestamp thời lượng")
    a = ap.parse_args()

    rng = seeded(a.hero, a.label, "genten")
    img = paper("grid", seed=a.hero).convert("RGB")
    d = ImageDraw.Draw(img)

    # ── trang tài liệu: khối trắng + bóng, hơi nghiêng ───────────────────
    px0, py0, px1, py1 = PANEL
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((px0 + 10, py0 + 14, px1 + 14, py1 + 16), fill=(0, 0, 0, 120))
    img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)),
                                    sh.filter(ImageFilter.GaussianBlur(14))).convert("RGB"),
              (0, 0), sh.filter(ImageFilter.GaussianBlur(14)).split()[3])
    d.rectangle((px0, py0, px1, py1), fill=(253, 252, 249), outline=(206, 203, 194), width=3)

    # ── nhãn mục (dòng chữ 2) + gạch chân tay ────────────────────────────
    f2, _, bb2 = fit_w(d, a.label, px1 - px0 - 110, 90, f=FONT_B, stroke_k=0)
    lx, ly = px0 + 54, py0 + 44
    d.text((lx - bb2[0], ly - bb2[1]), a.label, font=f2, fill=INK)
    lw = bb2[2] - bb2[0]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    stroke(od, (lx, ly + (bb2[3] - bb2[1]) + 18), (lx + lw, ly + (bb2[3] - bb2[1]) + 18),
           INK, 4, rng, passes=1, amp=1.6)

    # ── dòng giả (thanh xám) = chất "trang tài liệu", KHÔNG phải chữ ─────
    ty = ly + (bb2[3] - bb2[1]) + 62
    for wfrac in (0.72, 0.52):
        d.rounded_rectangle((px0 + 54, ty, px0 + 54 + int((px1 - px0 - 108) * wfrac), ty + 16),
                            radius=8, fill=(222, 220, 214))
        ty += 34

    # ── dòng chính: SỐ trên giấy (dòng chữ 3) ───────────────────────────
    fh, bbh = fit_h(d, a.hero, int(H * a.hero_h), px1 - px0 - 150)
    hw, hh = bbh[2] - bbh[0], bbh[3] - bbh[1]
    hx = px0 + (px1 - px0 - hw) // 2
    hy = py1 - 132 - hh
    d.text((hx - bbh[0], hy - bbh[1]), a.hero, font=fh, fill=INK)

    # ── KHOANH ĐỎ TAY + mũi tên trỏ ─────────────────────────────────────
    m = int(hh * 0.30)
    ell = (hx - m, hy - int(m * 0.72), hx + hw + m, hy + hh + int(m * 0.72))
    # 2 lượt khoanh (1 lượt để lại nửa vòng nhạt, nhìn như lỗi in)
    for k in range(2):
        sketch_ellipse(od, ell, RED, width=13, rng=seeded(a.hero, "ell", k), laps=1, over=0.26)
    # mũi tên: xuất phát từ khoảng trống phải, DƯỚI ảnh tròn và TRÊN badge
    ay = min(H - 250, py0 + a.face_d + 150)
    sketch_arrow(od, (min(W - 150, ell[2] + 300), ay),
                 (ell[2] + 18, (ell[1] + ell[3]) // 2 + 20), RED, width=11, rng=rng)

    # ── thanh giả dưới cùng ─────────────────────────────────────────────
    d.rounded_rectangle((px0 + 54, py1 - 78, px0 + 54 + int((px1 - px0 - 108) * 0.44), py1 - 62),
                        radius=8, fill=(222, 220, 214))
    img.paste(ov.convert("RGB"), (0, 0), ov.split()[3])

    # ── ảnh mặt cắt tròn ────────────────────────────────────────────────
    face = tuple(float(v) for v in a.face.split(","))
    cut = face_cutout(a.bg, face, a.face_d)
    img.paste(cut.convert("RGB"), (W - cut.width - 46, py0 + 8), cut.split()[3])

    # ── banner đen trên (dòng chữ 1) ────────────────────────────────────
    d.rectangle((0, 0, W, BH), fill=BLACK)
    txt = a.banner1 + ("　" if a.banner1 and a.banner2 else "") + a.banner2
    if txt.strip():
        f1, st1, bb1 = fit_w(d, txt, W - 84, 104, floor=56)
        tx, ty2 = 50, (BH - (bb1[3] - bb1[1])) // 2 - bb1[1]
        if a.banner1:
            d.text((tx, ty2), a.banner1 + ("　" if a.banner2 else ""), font=f1, fill=YEL,
                   stroke_width=st1, stroke_fill=BLACK)
        if a.banner2:
            w0 = d.textbbox((0, 0), a.banner1 + "　", font=f1, stroke_width=st1)[2] if a.banner1 else 0
            d.text((tx + w0, ty2), a.banner2, font=f1, fill=RED, stroke_width=st1, stroke_fill=WHITE)

    if a.badge.strip():
        img = badge(img, a.badge, pos=a.badge_pos)

    o = Path(a.out)
    o.parent.mkdir(parents=True, exist_ok=True)
    img.save(o)
    img.resize((480, 270), Image.LANCZOS).save(o.parent / (o.stem + "_preview480.png"))
    img.resize((168, 95), Image.LANCZOS).save(o.parent / (o.stem + "_preview168.png"))
    pct = hh / H * 100
    print(f"OK {o} | hero '{a.hero}' {len(a.hero)} ký, cao {hh}px = {pct:.1f}% khung "
          f"({'ĐẠT' if pct >= 33.3 else 'CHƯA ĐẠT'} gate ≥1/3) | 3 khối chữ | mặt d={a.face_d}px")


if __name__ == "__main__":
    main()
