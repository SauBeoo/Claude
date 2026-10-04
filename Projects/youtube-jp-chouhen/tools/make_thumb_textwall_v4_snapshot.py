# -*- coding: utf-8 -*-
"""make_thumb_textwall.py — thumbnail 朗読 style TEXT-WALL **v4** (MẶC ĐỊNH kênh, chốt 2026-07-27).

v4 thay v3 sau khi mổ CTR (bản v3 giữ ở make_thumb_textwall_v3_backup.py).

LÝ DO ĐỔI — đo 20 thumbnail của 4 kênh đối thủ cùng rail related, 2026-07-27:

    kênh                sáng   bão hòa  tương phản  %pixel rực
    ハレバレ 70K        117.7   177.5      91.3       32.3%
    ドロスカ 80K         97.7   156.0      92.4       19.6%
    ゼミ 1.4K            61.5   114.9      86.8       23.4%
    人生ドラマ 684       99.0   116.7      80.2       13.2%
    真夜中の朗読便 1      61.1    97.0      75.3       10.1%  ← BÉT CẢ 4 CỘT

Khớp với số Studio: 8/10 video chỉ được phát 46–253 impressions rồi tắt, CTR 0–1,2%;
2 video được test thật (2.443 / 2.532 imp) có CTR 4,1% / 2,9%. Thumbnail im lặng
giữa rail toàn thumbnail đang gào = không ai bấm = YouTube cắt thử nghiệm.

v4 sửa 4 thứ (đo lại sau mỗi thứ, không đoán):
  1. LAYOUT — v3 cấp mỗi dòng một ô cao BẰNG NHAU rồi co chữ cho lọt → 4 dòng ra 4 cỡ
     gần bằng nhau, dòng ngắn thừa lề. v4 kéo MỌI dòng căng full-width rồi scale cả
     khối cho vừa cao → phân cấp cỡ chữ sinh ra miễn phí, đúng cách ハレバレ/ドロスカ làm.
  2. FONT — YuGothB là font Nhật đậm nhất Windows có sẵn nhưng mực chỉ 17,28%; M PLUS
     1p Black 28,17% (+63%), Noto JP 900 24,76%. Font nặng thật là cách duy nhất
     đóng khoảng cách; kèm sẵn trong tools/fonts/ (OFL, thương mại free).
  3. NỀN — v3 ép scene tối 0.32 làm chữ chìm. v4 chuẩn hoá độ sáng nền bằng GAMMA
     về mean 88 (ảnh scene gốc của kênh mean 27,5–80,9, chênh 3 lần → nhân hệ số
     cứng là cái tối vẫn tối cái sáng thì cháy), GIỮ NGUYÊN màu gốc (user chốt
     2026-07-27: không ám xanh), + UnsharpMask bù nét. Nền GRADIENT thì vẫn cố ý
     tối (navy+sao) vì ở đó độ sáng đến từ chữ.
  4. FAT theo font — làm dày nét bằng stroke cùng màu, trần khác nhau từng font
     (xem FAT_BY_FONT); vượt trần là bịt lòng chữ hán.

KHÔNG đổi: bảng màu. Đã thử 4 bộ — cpyr 75.5 · wpyr 86.9 · cwyr 85.9 · wcyr 89.1
tương phản; bộ CÓ TRẮNG thắng, và wcyr chính là mặc định cũ của v3. Trắng cho độ
chói, neon cho bão hòa.

KẾT QUẢ (cùng 4 dòng, nền scene): sáng 47,7→67,4 · bão hòa 90,5→184,2 ·
tương phản 79,2→84,3 · %rực 9,2→19,8. Vượt ドロスカ và ゼミ, còn thua ハレバレ.
⚠️ Mới là khớp CHỈ SỐ HÌNH ẢNH — chưa chứng minh CTR lên. Phải đọc lại
impressions/CTR trong Studio sau 2–3 tuần dùng thật.

Cấu trúc dòng (màu auto theo vai trò, dòng CUỐI luôn ĐỎ + quầng trắng, TO NHẤT):
  dòng 1–2  bối cảnh + hành động phản diện   → TRẮNG / HỒNG
  dòng 3    quote phản diện 「…ｗ」            → CYAN / TÍM
  dòng 4    phản ứng chính diện 私「…」        → VÀNG
  dòng cuối đòn/hậu quả bỏ lửng               → ĐỎ

Chạy:
  python tools/make_thumb_textwall.py <out.png> --lines "d1" "d2" "d3" "d4" "dòng đỏ"       --bg 06_VIDEO/_series_assets/scene_NN_ai.jpg
  [--colors w,c,y,r]  ghi đè màu (w trắng · p hồng · c cyan · v tím · y vàng · o cam · r đỏ)
  [--bgstyle auto|scene|grad|dark]  auto = có --bg thì scene, không thì grad (navy+sao)
  [--font mplus|noto|yu]            mplus = M PLUS 1p Black (mặc định)
  [--fat 0.01]                      bỏ trống = trần an toàn của font đang dùng
  [--band]                          băng tối đặc sau dòng đòn cuối
Mỗi dòng nên ≤14 ký — dòng NGẮN giờ TỰ thành chữ khổng lồ, đó là điểm ăn tiền.
Xuất kèm _preview.png (480px) + _preview120.png (120px) để duyệt 2 cấp.
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
FAT_BY_FONT = {"yu": 0.02, "mplus": 0.0, "noto": 0.008}
FAT = FAT_BY_FONT["mplus"]

# ⚠️ VIỀN + GIÃN CHỮ — user bắt lỗi 2026-07-27 lần 2: "chữ kanji cứ đè nét lên nhau".
# Hai triệu chứng, một gốc: viền đen 0.062 quá dày so với M PLUS Black.
#   ① TRONG chữ: stroke của PIL nở đều MỌI hướng, kể cả vào lòng chữ. Khe hở trong
#      義・忌 ở cỡ ~180px chỉ ~12px, viền 11px mỗi bên là bịt kín → chữ thành cục.
#   ② GIỮA các chữ: viền của 2 glyph cạnh nhau chạm nhau → 義母 dính liền.
# Sửa: hạ viền 0.062 → 0.032, bỏ fat với M PLUS (font đã đủ nặng), và GIÃN CHỮ
# 3,5% cỡ chữ để viền 2 glyph không chạm. Đừng vặn OUTLINE lên lại.
OUTLINE = 0.032
TRACK = 0.035
# tổng độ nở mỗi bên do stroke, tính theo tỉ lệ cỡ chữ (khớp draw_line)
SW_NORMAL = FAT + OUTLINE
SW_RED = FAT + OUTLINE + 0.045


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
        # bề rộng thật = tổng advance từng chữ + giãn chữ + nở stroke hai bên.
        # Thiếu 2 số hạng sau thì dòng đòn cuối (stroke dày nhất) bị cụt chữ.
        if line_width(text, mid) + 2 * sw * mid <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


def line_width(text, sz):
    f = font(sz)
    return sum(f.getlength(c) for c in text) + TRACK * sz * max(0, len(text) - 1)


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


def bg_scene(src, brightness=1.0, target=88):
    """Lót ảnh scene: nâng sáng, GIỮ MÀU GỐC (không ám màu), làm nét lại sau khi thu nhỏ.

    ⚠️ Hai bài học 2026-07-27, cùng một chỗ:
    ① user "sao ảnh mờ thế" — bản đầu đẩy kênh lam bằng `B * 1.22 + 26`. Cái **cộng
       thêm 26** nâng đáy kênh lam nên vùng tối không còn đen → đúng hiệu ứng sương
       mù/đục. Cộng với ép sáng 0.62 + bão hòa 1.55 = nền vừa tối vừa bệt vừa ám xanh.
    ② user "muốn phông sáng tí không ám xanh" — **bỏ HẲN mọi can thiệp kênh màu**
       (giữ đúng màu ảnh gốc) và nâng sáng.

    Nâng sáng bằng CHUẨN HOÁ THEO ĐÍCH, không nhân hệ số cứng: mỗi ảnh scene một độ
    sáng gốc khác nhau (cảnh đêm vs cảnh ngày chênh 3–4 lần), nhân cùng một số thì
    cảnh tối vẫn tối mà cảnh sáng thì cháy. Đây đo độ sáng thật của ảnh rồi kéo về
    `target`, hệ số kẹp trong [0.45, 2.4] để không ép quá tay.
    Còn lại: bão hòa 1.15 (nhẹ, giữ màu thật), contrast 1.10 dựng chiều sâu, và
    UnsharpMask bù nét mất khi thu 2752→1920.
    ⚠️ Nền sáng lên thì chữ phải gánh phần tương phản — đổi `target` là phải duyệt
    lại 120px: dòng đỏ cuối còn đọc được không.
    """
    im = Image.open(src).convert("RGB")
    if im.width < W or im.height < H:
        print(f"⚠️ ảnh nền {Path(src).name} chỉ {im.width}x{im.height} < {W}x{H} "
              f"— phóng to sẽ mờ, nên thay ảnh khác")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
    # Nâng sáng bằng GAMMA, không nhân tuyến tính. Ảnh scene AI của kênh rất tối
    # (đo 2026-07-27: mean gốc 27,5–80,9 — scene_07 cần x2,98 mới lên 82). Nhân
    # tuyến tính x3 thì vùng sáng cháy trắng; gamma kéo vùng tối lên mà giữ highlight.
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = float(np.asarray(im.convert("L")).mean())
    if lum > 1:
        lo_g, hi_g = 0.25, 3.0
        for _ in range(24):                       # dò gamma để mean chạm target
            g = (lo_g + hi_g) / 2
            if (a ** g).mean() * 255 > target:
                lo_g = g
            else:
                hi_g = g
        a = np.clip(a ** ((lo_g + hi_g) / 2), 0, 1)
    im = Image.fromarray((a * 255).astype(np.uint8))
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    im = ImageEnhance.Color(im).enhance(1.15)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=75, threshold=3))


def draw_line(d, x, y, text, f, fill, sz, halo=False, fat_ratio=FAT, track=None):
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
    outline = max(4, round(sz * OUTLINE))
    trk = TRACK * sz if track is None else track

    # Vẽ TỪNG KÝ TỰ với khoảng giãn `trk`, và chia làm 2 LƯỢT:
    #   lượt 1 vẽ hết viền đen (+ quầng trắng) — lượt 2 mới vẽ ruột màu.
    # Nếu vẽ viền+ruột từng chữ một thì viền của chữ sau đè lên ruột của chữ trước,
    # ra đúng cảnh "chữ dính vào nhau" user thấy.
    pos, cx = [], x
    for ch in text:
        pos.append((cx, ch))
        cx += f.getlength(ch) + trk
    if halo:
        hw = fat + outline + max(4, round(sz * 0.045))
        for px, ch in pos:
            d.text((px, y), ch, font=f, fill=(255, 255, 255),
                   stroke_width=hw, stroke_fill=(255, 255, 255))
    for px, ch in pos:
        d.text((px, y), ch, font=f, fill=BLACK, stroke_width=fat + outline, stroke_fill=BLACK)
    for px, ch in pos:
        if fat:
            d.text((px, y), ch, font=f, fill=fill, stroke_width=fat, stroke_fill=fill)
        else:
            d.text((px, y), ch, font=f, fill=fill)


def main():
    global FONT_KEY
    ap = argparse.ArgumentParser(description="Thumbnail text-wall v4 — thumbnail chuẩn kênh chouhen")
    ap.add_argument("out")
    ap.add_argument("--lines", nargs="+", required=True)
    ap.add_argument("--colors", default="auto")
    ap.add_argument("--bg", default="")
    ap.add_argument("--bgstyle", default="auto",
                    choices=["auto", "grad", "dark", "scene"],
                    help="auto = có --bg thì lót scene, không có thì nền navy+sao")
    ap.add_argument("--bg-brightness", type=float, default=1.0,
                    help="hệ số nhân THÊM sau khi đã chuẩn hoá về --bg-target")
    ap.add_argument("--bg-target", type=float, default=88,
                    help="độ sáng trung bình đích của nền scene (0-255). Cao hơn = phông sáng hơn")
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

    if a.bgstyle == "auto":
        a.bgstyle = "scene" if a.bg else "grad"
    if a.bgstyle == "scene" and a.bg:
        img = bg_scene(a.bg, a.bg_brightness, a.bg_target)
    elif a.bgstyle == "dark":
        img = Image.new("RGB", (W, H), (10, 10, 14))
    else:
        img = bg_gradient()
    d = ImageDraw.Draw(img)

    # LAYOUT: mọi dòng căng full-width, rồi scale cả khối cho vừa chiều cao.
    margin_y, gap, max_w = 14, 10, W - 44
    sws = [(a.fat + OUTLINE + 0.045) if k == "r" else (a.fat + OUTLINE) for k in keys]
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
        th = bb[3] - bb[1]
        tw = line_width(text, sz)          # có tính giãn chữ, khác textbbox
        x = (W - tw) / 2
        if a.band and key == "r":
            d.rectangle([0, y - 4, W, y + th + 2 * pad + 4], fill=(16, 16, 20))
        draw_line(d, x, y + pad - bb[1], text, f, COLORS[key], sz,
                  halo=(key == "r"), fat_ratio=a.fat)
        y += th + 2 * pad + gap + extra

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)

    # YouTube từ chối thumbnail > 2 MB ("Media larger than: 2097152"). Nền sáng +
    # UnsharpMask đẩy PNG lên 2,1–3,0 MB → LUÔN xuất kèm bản .jpg đã ép dưới ngưỡng
    # và dùng bản .jpg đó khi upload. (Bẫy này đã làm hỏng 1 lượt đẩy 2026-07-27.)
    LIMIT = 2 * 1024 * 1024
    jpg = out.with_suffix(".jpg")
    for q in (95, 92, 88, 84, 80):
        img.save(jpg, "JPEG", quality=q, subsampling=0, optimize=True)
        if jpg.stat().st_size <= LIMIT:
            break
    print(f"   → upload dùng {jpg.name} ({jpg.stat().st_size/1048576:.2f} MB, q{q}); "
          f"PNG {out.stat().st_size/1048576:.2f} MB chỉ để lưu")
    img.resize((480, 270), Image.LANCZOS).save(out.parent / (out.stem + "_preview.png"))
    img.resize((213, 120), Image.LANCZOS).save(out.parent / (out.stem + "_preview120.png"))
    print("OK", out)


if __name__ == "__main__":
    main()
