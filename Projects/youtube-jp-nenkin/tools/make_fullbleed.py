# -*- coding: utf-8 -*-
r"""make_fullbleed.py — dựng frame FULL-BLEED kiểu vox-director cho kênh nenkin.

⭐ VÌ SAO CÓ TOOL NÀY (user chốt 2026-08-26, lần 2): *"tao muốn video từ đầu đến cuối đều
dùng dạng vox-director kiểu như video này showcase-football.mp4"*. Tức **BỎ khung sân khấu**
(card kem + 2 cast hai mép + dải đen phụ đề) → ảnh collage **lấp trọn khung 16:9**, headline
cắt giấy, phụ đề đè lên ảnh. Đúng khuôn `E:\vox-director\assets\showcase-football.mp4`.

🔴 CHỖ LỆCH DUY NHẤT, VÀ LÀ LÝ DO TOOL NÀY TỒN TẠI: **headline được VẼ ĐÈ, không bake vào ảnh.**
- showcase-football bake headline vào ảnh được vì nó là **tiếng Anh** (Latin). Lô pho-30s bake
  **tiếng Việt có dấu** cũng ra đúng ("CHƯA TRÒN 130 NĂM" — đã soi ảnh thật `kf_1a.jpg`).
- Nhưng kênh này là **tiếng Nhật**, và `media-library.md` §2.9 + `ab-3title-3thumb.md` §3 mục 8
  đã ghi: **kanji rậm gen ra nát nét** (dính thật ở 還暦・封筒), 5 dòng gần như chắc méo.
  Tệp 45–70 + YMYL thì chữ nát là không chấp nhận được.
- ⇒ Ảnh gen **KHÔNG chữ** (dùng `art_prompts_collage.py`, khối NOTEXT), tool này vẽ banner
  giấy xé + chữ **Noto Sans JP** đè lên ⇒ chữ LUÔN sắc, look vẫn là banner cắt giấy.
- ⚠️ Cái mất: chữ không có nét "cắt từ giấy báo" thật như showcase-football. Bù bằng banner
  giấy xé vẽ tay + nghiêng nhẹ + bóng giấy. Muốn thử đường bake thì gen 1 ảnh so bằng mắt —
  đó là phép thử chưa ai làm, đừng đoán.

CHẠY:  python tools/make_fullbleed.py <slug>
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
FONTS = Path(r"E:\Claude\Projects\_media_library\fonts")
W, H = 1920, 1080

# Palette khớp lô ảnh collage (STYLE của art_prompts_collage.py)
CREAM = (247, 242, 230)
INK = (28, 42, 74)          # navy đậm — chữ chính
RED = (168, 32, 38)
MUSTARD = (214, 160, 48)
CHAR = (38, 36, 34)


def F(weight, size):
    f = {"black": "NotoSansJP-Black.otf", "bold": "NotoSansJP-Bold.otf",
         "med": "NotoSansJP-Medium.otf"}[weight]
    return ImageFont.truetype(str(FONTS / f), int(size))


def fit(text, weight, max_w, start, floor=40):
    s = start
    while s > floor:
        f = F(weight, s)
        b = f.getbbox(text)
        if b[2] - b[0] <= max_w:
            return f
        s -= 4
    return F(weight, floor)


def torn_edge(draw, box, fill, rng, amp=9, step=26, sides=("top", "bottom")):
    """Vẽ hộp có mép GIẤY XÉ (răng cưa ngẫu nhiên) — chữ ký thị giác của collage."""
    x0, y0, x1, y1 = box
    pts = []
    if "top" in sides:
        x = x0
        while x < x1:
            pts.append((x, y0 + rng.randint(-amp, amp)))
            x += step
        pts.append((x1, y0 + rng.randint(-amp, amp)))
    else:
        pts += [(x0, y0), (x1, y0)]
    if "bottom" in sides:
        x = x1
        while x > x0:
            pts.append((x, y1 + rng.randint(-amp, amp)))
            x -= step
        pts.append((x0, y1 + rng.randint(-amp, amp)))
    else:
        pts += [(x1, y1), (x0, y1)]
    draw.polygon(pts, fill=fill)


def tape(img, at, w=150, h=44, rot=-14, rng=None):
    """Miếng washi tape mờ — vox-director dùng ở mọi góc."""
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rectangle((0, 0, w, h), fill=(232, 222, 196, 205))
    for i in range(0, w, 9):     # sợi giấy
        d.line((i, 0, i, h), fill=(214, 202, 172, 70))
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (at[0] - t.width // 2, at[1] - t.height // 2))


def headline(img, text, rng, tone="cream", y=0.085, rot=-1.6, sub=None):
    """Banner giấy xé + chữ Noto Sans JP. Đây là thứ thay cho headline bake-trong-ảnh."""
    pad_x, pad_y = 54, 30
    f = fit(text, "black", int(W * 0.80) - pad_x * 2, 148, floor=64)
    b = f.getbbox(text)
    tw, th = b[2] - b[0], b[3] - b[1]
    bw, bh = tw + pad_x * 2, th + pad_y * 2 + 14

    lay = Image.new("RGBA", (bw + 60, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bg = CREAM if tone == "cream" else (MUSTARD if tone == "mustard" else RED)
    fg = INK if tone != "red" else CREAM
    torn_edge(d, (30, 30, 30 + bw, 30 + bh), bg, rng)
    d.text((30 + pad_x - b[0], 30 + pad_y - b[1]), text, font=f, fill=fg)
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)

    # bóng giấy thật
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 105), (0, 0), lay.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    x = (W - lay.width) // 2
    yy = int(H * y)
    img.alpha_composite(sh, (x + 7, yy + 9))
    img.alpha_composite(lay, (x, yy))

    tape(img, (x + 26, yy + 18), rot=-18, rng=rng)
    tape(img, (x + lay.width - 26, yy + 16), rot=13, rng=rng)

    if sub:
        fs = fit(sub, "bold", int(W * 0.62), 62, floor=38)
        bs = fs.getbbox(sub)
        sw = bs[2] - bs[0]
        sy = yy + lay.height + 12
        d2 = ImageDraw.Draw(img)
        sx = (W - sw) // 2
        d2.rectangle((sx - 26, sy - 10, sx + sw + 26, sy + (bs[3] - bs[1]) + 22),
                     fill=(*RED, 235))
        d2.text((sx - bs[0], sy - bs[1] + 6), sub, font=fs, fill=CREAM)
    return int(H * y) + lay.height


def scraps(img, rng, n=14):
    """Vụn giấy hình học rải quanh — vox-director rải rất nhiều, đây là 'nhiễu vui'."""
    pal = [RED, MUSTARD, INK, (74, 132, 128)]
    for _ in range(n):
        c = rng.choice(pal)
        x = rng.choice([rng.randint(20, 210), rng.randint(W - 230, W - 30)])
        y = rng.randint(40, H - 60)
        s = rng.randint(20, 46)
        k = rng.randint(0, 2)
        d = ImageDraw.Draw(img)
        if k == 0:
            d.polygon([(x, y), (x + s, y + rng.randint(4, 14)), (x + s // 2, y + s)],
                      fill=(*c, 232))
        elif k == 1:
            d.ellipse((x, y, x + s, y + s), fill=(*c, 232))
        else:
            for i in range(4):      # zigzag
                d.line((x + i * s // 2, y + (i % 2) * s // 2,
                        x + (i + 1) * s // 2, y + ((i + 1) % 2) * s // 2),
                       fill=(*c, 240), width=max(4, s // 8))


def build(src, out, title, sub=None, tone="cream", seed=0):
    rng = random.Random(seed)
    im = Image.open(src).convert("RGB")
    # cover-crop về 16:9 rồi phóng full-bleed
    sc = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * sc + 0.5), int(im.height * sc + 0.5)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                  (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    img = im.convert("RGBA")

    scraps(img, rng)
    if title:
        headline(img, title, rng, tone=tone, sub=sub)

    # ⚠️ CHỪA góc dưới-phải: YouTube đóng timestamp thời lượng ở đó
    # (`feedback_thumbnail_goc_duoi_phai_cua_youtube` — cùng luật, áp cho cả frame video).
    img.convert("RGB").save(out)
    return out


SPEC = [
    dict(src="art_denwa_furueru.png",     out="fb_00.png", tone="cream",
         title="その電話は、震えていた", sub=None, seed=1),
    dict(src="art_te_tomaru.png",         out="fb_01.png", tone="red",
         title="ここで、手が止まった", sub="マイナンバーカードの写真", seed=2),
    dict(src="art_tsucho_kakenaosu.png",  out="fb_02.png", tone="mustard",
         title="切って、かけ直す", sub="年金手帳の裏表紙の番号", seed=3),
    dict(src="bg_tsukue_denwa.png",       out="fb_03.png", tone="cream",
         title="本物は、急がない", sub=None, seed=4),
    dict(src="art_tsuri_nakama.png",      out="fb_04.png", tone="cream",
         title="「俺だったら、送ってたな」", sub=None, seed=5),
]


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if not slug:
        print("dùng: python tools/make_fullbleed.py <slug>")
        return 1
    vdir = PROJ / "06_VIDEO" / slug
    art = vdir / "art"
    dst = vdir / "fullbleed"
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for s in SPEC:
        p = art / s["src"]
        if not p.exists():
            print(f"🔴 THIẾU {s['src']}")
            continue
        build(p, dst / s["out"], s["title"], s.get("sub"), s["tone"], s["seed"])
        print(f"   ✓ {s['out']:<12} ← {s['src']:<28} [{s['tone']}] {s['title']}")
        n += 1
    print(f"\n✓ {n}/{len(SPEC)} frame full-bleed 1920×1080 → {dst}")
    print("⛔ DUYỆT MẮT: chữ có sắc không · banner có che mất chủ thể không · "
          "góc dưới-phải có trống cho timestamp không")
    return 0


if __name__ == "__main__":
    sys.exit(main())
