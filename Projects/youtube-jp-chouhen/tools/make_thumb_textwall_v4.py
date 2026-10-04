# -*- coding: utf-8 -*-
"""make_thumb_textwall_v4.py — BẢN DEMO chờ duyệt, chưa thay v3.

Vì sao có bản này (đo 2026-07-27, 20 thumbnail của 4 kênh đối thủ cùng rail):

    kênh              sáng   bão hòa  tương phản  %pixel rực
    ハレバレ 70K       117.7   177.5      91.3       32.3%
    ドロスカ 80K        97.7   156.0      92.4       19.6%
    ゼミ 1.4K           61.5   114.9      86.8       23.4%
    人生ドラマ 684      99.0   116.7      80.2       13.2%
    真夜中の朗読便 1     61.1    97.0      75.3       10.1%   ← bét cả 4 cột

v3 thua ở ĐỘ RỰC chứ không thua ở cỡ chữ. Ba thứ v4 sửa:
  1. NỀN — v3 mặc định gần đen (10,10,14) hoặc scene ép tối 0.32. v4 có nền
     gradient sáng (xanh→tím + tia sáng) như ハレバレ/ドロスカ, và khi lót scene
     thì grade lạnh + nâng sáng thay vì dìm đen.
  2. MÀU CHỮ — v3 mặc định trắng (bão hòa = 0) cho 1–2 dòng đầu. v4 bỏ trắng
     thuần khỏi bộ auto, mọi dòng đều là màu bão hòa cao.
  3. VIỀN + BĂNG NỀN — viền scale theo cỡ chữ (v3 cố định 16px, chữ to thì viền
     hụt), thêm băng màu đặc sau dòng đòn (ドロスカ dùng băng vàng, 人生ドラマ băng đỏ).

Chạy giống v3, thêm cờ:
  --bgstyle grad|dark|scene   nền: gradient sáng (mặc định) | tối | ảnh scene
  --band                      bật băng màu đặc sau dòng cuối
"""
import argparse
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
BLACK = (6, 6, 6)

# Font — đo "độ dày mực" trên 「義母の三回忌の夜、追い出された」 cùng cỡ 110px
# (tỉ lệ pixel có mực / khung):
#     M PLUS 1p Black   28,17%   ← nặng nhất, mặc định
#     Noto Sans JP 900  24,76%
#     YuGothB           17,28%   ← font cũ của v3, mảnh hơn 63%
# Đây là lý do v3 phải "béo giả" bằng stroke và bị bịt lòng chữ hán. Font nặng
# thật thì lòng chữ được thiết kế mở sẵn, không cần stroke bù.
_FDIR = Path(__file__).parent / "fonts"
FONTS = {
    "mplus": (str(_FDIR / "MPLUS1p-Black.ttf"), None),
    "noto": (str(_FDIR / "NotoSansJP-var.ttf"), 900),   # variable → phải set trục Weight
    "yu": ("C:/Windows/Fonts/YuGothB.ttc", None),
}
FONT_KEY = "mplus"

# ⚠️ Đo lại 2026-07-27: bảng màu v3 KHÔNG phải thủ phạm. Thử 4 bộ trên cùng layout
# v4 (scene bg): cpyr 75.5 · wpyr 86.9 · cwyr 85.9 · wcyr 89.1 tương phản — bộ có
# TRẮNG thắng, và wcyr chính là mặc định cũ của v3. Trắng cho độ chói (tương phản),
# neon cho bão hòa; ハレバレ trộn đúng như vậy. Thứ hỏng ở v3 là layout + độ béo nét
# + nền, không phải màu. Giữ nguyên bộ cũ.
COLORS = {
    "w": (255, 252, 240),   # trắng ngà — giữ, là nguồn tương phản chính
    "p": (255, 46, 147),    # hồng neon
    "c": (0, 240, 255),     # cyan điện
    "v": (190, 96, 255),    # tím
    "y": (255, 226, 0),     # vàng neon
    "o": (255, 150, 0),     # cam
    "r": (255, 24, 24),     # đỏ — dòng đòn cuối
}
AUTO = {3: "wyr", 4: "wcyr", 5: "wpcyr"}


@lru_cache(maxsize=512)
def font(sz, key=None):
    path, wght = FONTS[key or FONT_KEY]
    f = ImageFont.truetype(path, sz)
    if wght:
        f.set_variation_by_axes([wght])
    return f


# fat = làm dày nét chữ bằng stroke cùng màu. TRẦN theo TỪNG FONT — soi bằng mắt
# trên dòng nặng 漢字 「義母の三回忌の夜、追い出された」, mốc là lúc chữ 義 bắt đầu vón:
#     yu    (YuGothB, mảnh)      → 0.02 sạch · 0.03 vón
#     mplus (M PLUS Black, nặng) → 0.01 sạch · 0.02 vón   ← font càng nặng càng cần ít
#     noto  (Noto JP 900)        → 0.015
# Font nặng đã tự có mực, ép thêm stroke chỉ tổ bịt lòng chữ. Xem draw_line.
FAT_BY_FONT = {"yu": 0.02, "mplus": 0.01, "noto": 0.015}
FAT = FAT_BY_FONT["mplus"]
# tổng độ nở mỗi bên do stroke, tính theo tỉ lệ cỡ chữ (khớp draw_line)
SW_NORMAL = FAT + 0.062
SW_RED = FAT + 0.062 + 0.045


def size_for_width(text, max_w, sw=SW_NORMAL, lo=40, hi=460):
    """Cỡ chữ để dòng CĂNG ĐÚNG hết bề ngang khung (nhị phân).

    Đây là điểm khác cốt lõi so với v3. v3 cấp cho mỗi dòng một ô cao bằng nhau
    rồi mới co chữ cho lọt → 4 dòng ra 4 cỡ gần bằng nhau, không có phân cấp, và
    dòng ngắn thì thừa chỗ trống hai bên. ハレバレ/ドロスカ làm ngược: MỌI dòng đều
    kéo căng full-width, nên dòng ngắn (「2ヶ月後…」) tự thành chữ khổng lồ còn dòng
    dài tự nhỏ lại — phân cấp cỡ chữ sinh ra miễn phí từ số ký tự.
    """
    while lo < hi:
        mid = (lo + hi + 1) // 2
        bb = font(mid).getbbox(text)
        # + nở stroke hai bên, nếu không dòng đòn cuối (stroke dày nhất) bị cụt chữ
        if (bb[2] - bb[0]) + 2 * sw * mid <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


def bg_gradient(seed=7):
    """Nền navy sâu + quầng sáng xanh giữa + sao, đúng công thức ハレバレ.

    Cố ý GIỮ NỀN TỐI: cột "tương phản" của ハレバレ là 91 vì nền navy tối tương phản
    với chữ neon. Bản thử đầu tiên dùng nền tím sáng đều → tương phản tụt còn 64.
    Độ sáng trung bình phải đến từ CHỮ, không phải từ nền.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 0.5, H * 0.46
    r = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    core = np.clip(1.0 - r * 1.25, 0, 1) ** 2.1
    a = np.zeros((H, W, 3), np.float32)
    a[..., 0] = 8 + core * 42
    a[..., 1] = 14 + core * 86
    a[..., 2] = 46 + core * 165
    ang = np.arctan2(yy - cy, xx - cx)
    rays = (np.sin(ang * 20) * 0.5 + 0.5) ** 4 * np.clip(1 - r * 1.5, 0, 1)
    a += (rays * 52)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    # sao lấm tấm
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(im)
    for _ in range(220):
        sx, sy = rng.integers(0, W), rng.integers(0, H)
        rad = rng.integers(1, 4)
        v = int(rng.integers(150, 255))
        d.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=(v, v, min(255, v + 20)))
    return im


def bg_scene(src, brightness=0.62):
    """Lót ảnh scene nhưng GRADE LẠNH + nâng sáng, thay vì dìm đen như v3."""
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
    im = ImageEnhance.Brightness(im).enhance(brightness)
    im = ImageEnhance.Color(im).enhance(1.55)
    a = np.asarray(im).astype(np.float32)
    a[..., 2] = np.clip(a[..., 2] * 1.22 + 26, 0, 255)    # đẩy xanh dương
    a[..., 0] = np.clip(a[..., 0] * 1.05, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def draw_line(d, x, y, text, f, fill, sz, halo=False, fat_ratio=FAT):
    """Viền đen quanh chữ + (tuỳ chọn) quầng trắng cho dòng đòn.

    ⚠️ Bài học 2026-07-27 (user bắt lỗi): bản thử đầu "béo giả" nét chữ bằng cách
    vẽ stroke CÙNG MÀU với ruột, dày 5,5% cỡ chữ. Chỉ số hình ảnh đẹp lên thật,
    nhưng 漢字 nét dày đặc (義・鬱・驚) bị BỊT KÍN các khoảng hở bên trong → chữ vón
    thành cục đen, đọc không ra. Stroke của PIL nở đều mọi hướng nên mọi cách làm
    dày kiểu này đều ăn vào lòng chữ.
    → Độ đậm phải lấy từ CỠ CHỮ (layout full-width của v4 đã to sẵn), không lấy từ
      stroke. fat mặc định = 0. Viền đen chỉ để tách chữ khỏi nền.
    """
    fat = round(sz * fat_ratio)
    outline = max(5, round(sz * 0.062))
    if halo:
        d.text((x, y), text, font=f, fill=(255, 255, 255),
               stroke_width=fat + outline + max(5, round(sz * 0.045)),
               stroke_fill=(255, 255, 255))
    d.text((x, y), text, font=f, fill=BLACK, stroke_width=fat + outline, stroke_fill=BLACK)
    if fat:
        d.text((x, y), text, font=f, fill=fill, stroke_width=fat, stroke_fill=fill)
    else:
        d.text((x, y), text, font=f, fill=fill)


def main():
    global FONT_KEY
    ap = argparse.ArgumentParser(description="Thumbnail text-wall v4 (bản demo)")
    ap.add_argument("out")
    ap.add_argument("--lines", nargs="+", required=True)
    ap.add_argument("--colors", default="auto")
    ap.add_argument("--bg", default="")
    ap.add_argument("--bgstyle", default="grad", choices=["grad", "dark", "scene"])
    ap.add_argument("--bg-brightness", type=float, default=0.62)
    ap.add_argument("--band", action="store_true", help="băng màu đặc sau dòng đòn cuối")
    ap.add_argument("--font", default=FONT_KEY, choices=list(FONTS),
                    help="mplus = M PLUS 1p Black (nặng nhất, mặc định) · noto = Noto Sans JP 900 · yu = font cũ")
    ap.add_argument("--fat", type=float, default=None,
                    help="làm dày nét chữ (tỉ lệ cỡ chữ). Bỏ trống = trần an toàn theo "
                         f"font ({FAT_BY_FONT}); vượt trần là bịt lòng chữ hán")
    a = ap.parse_args()

    FONT_KEY = a.font
    font.cache_clear()
    if a.fat is None:
        a.fat = FAT_BY_FONT[a.font]

    lines = a.lines
    if not 3 <= len(lines) <= 5:
        sys.exit("❌ Cần 3–5 dòng.")

    keys = AUTO[len(lines)] if a.colors == "auto" else a.colors.replace(",", "")
    if len(keys) != len(lines) or any(k not in COLORS for k in keys):
        sys.exit(f"❌ --colors phải là {len(lines)} ký tự trong {'/'.join(COLORS)}")

    if a.bgstyle == "scene" and a.bg:
        img = bg_scene(a.bg, a.bg_brightness)
    elif a.bgstyle == "dark":
        img = Image.new("RGB", (W, H), (10, 10, 14))
    else:
        img = bg_gradient()
    d = ImageDraw.Draw(img)

    # LAYOUT: mọi dòng căng full-width, rồi scale cả khối cho vừa chiều cao.
    margin_y, gap, max_w = 14, 10, W - 44
    sws = [(a.fat + 0.062 + 0.045) if k == "r" else (a.fat + 0.062) for k in keys]
    sizes = [size_for_width(t, max_w, sw) for t, sw in zip(lines, sws)]

    def heights(szs):
        return [font(s).getbbox(t)[3] - font(s).getbbox(t)[1] + round(2 * sw * s)
                for s, t, sw in zip(szs, lines, sws)]

    avail = H - 2 * margin_y - gap * (len(lines) - 1)
    for _ in range(60):
        hs = heights(sizes)
        if sum(hs) <= avail:
            break
        sizes = [max(40, round(s * 0.97)) for s in sizes]
    hs = heights(sizes)
    # còn dư chiều cao thì giãn đều gap cho tường chữ phủ kín khung
    extra = (avail - sum(hs)) / (len(lines) + 1) if len(lines) else 0
    y = margin_y + extra
    for text, key, sz, sw in zip(lines, keys, sizes, sws):
        f = font(sz)
        bb = d.textbbox((0, 0), text, font=f)
        pad = round(sw * sz)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x = (W - tw) // 2 - bb[0]
        if a.band and key == "r":
            d.rectangle([0, y - 4, W, y + th + 2 * pad + 4], fill=(16, 16, 20))
        draw_line(d, x, y + pad - bb[1], text, f, COLORS[key], sz,
                  halo=(key == "r"), fat_ratio=a.fat)
        y += th + 2 * pad + gap + extra

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview.png"))
    img.resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out)


if __name__ == "__main__":
    main()
