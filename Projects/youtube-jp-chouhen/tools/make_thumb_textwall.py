# -*- coding: utf-8 -*-
"""make_thumb_textwall.py — thumbnail 朗読 style TEXT-WALL **v5** (MẶC ĐỊNH kênh, chốt 2026-07-28).

═══════════════════════════════════════════════════════════════════════════════
v5 — NỀN ĐEN PHẲNG + CHÂN DUNG NỬA KHUNG (2026-07-28)
═══════════════════════════════════════════════════════════════════════════════

v5 KHÔNG đổi gì trong cách vẽ chữ của v4 (layout full-width, font M PLUS Black,
bảng màu wcyr, viền 0.032, giãn chữ 0.035, fat=0). Nó đổi đúng phần NỀN:

    --bgstyle flat   ← MẶC ĐỊNH MỚI: nền gần đen, KHÔNG ảnh phía sau chữ
    --portrait <ảnh> [--portrait-w 0.42] [--portrait-side right|left]
                     [--portrait-anchor top|center]
                     ← chân dung nhân vật (hoặc vật chứng) cắt gọn chiếm ~42%
                       khung một bên, hoà tan vào nền đen; chữ dồn nửa còn lại
    --bg <ảnh>       ← kiểu v4 (scene phủ toàn khung) vẫn chạy, THÔI mặc định

🚨 LUẬT ĐO trước khi vặn tiếp bất cứ thông số nào: chỉ so với video ĐĂNG ≤30
NGÀY, xếp theo view/ngày, đã lọc Shorts. Lý do thành luật — v4 (docstring dưới)
được hiệu chỉnh theo `ハレバレ 428K` và `ドロスカ 70K`, mà ハレバレ 8 ngày gần nhất
chỉ ăn 157–3.341 view/video: **428K là hit CŨ của một kênh đang chết.** Vặn theo
mốc chết = vặn sai hướng.

Đo lại đúng cửa sổ 30 ngày (246 video long-form, 2026-07-28) thì kết luận NGƯỢC
với v4:

    nhóm                                     sáng     bão hòa   %rực   %trắng
    スカっとゼミ! (17/50 slot top v/ngày)     57–72    84–108    19–24   4–11
    世界の中心でスカッと朗読 (4/50)            76–99    58–93     10–12   3–13
    嫁子 (11/50, video 91–151′)             158–162  123–131   35–41  15–18
    MINE 07-25  ← CTR 3,6%, CAO NHẤT KÊNH    57,1     89,4       9,1    6,3
    MINE 07-27 v4  (CTR 3,2%)               109,9    110,5      22,2   13,1

  ① "Kênh mình bét chỉ số" là SAI — chỉ số của kênh nằm gọn trong dải kênh đang
     thắng; kênh dẫn đầu (スカっとゼミ!) còn bão hòa/%rực THẤP HƠN kênh mình.
     → KHÔNG đẩy bão hòa/%rực lên nữa.
  ② Khác biệt cấu trúc thật: nhóm thắng dùng NỀN ĐEN PHẲNG, ảnh (nếu có) là
     CHÂN DUNG cắt gọn sang một bên, chữ chiếm phần còn lại — không phải chữ đè
     lên ảnh cảnh. Ở 120px cái neo mắt là KHUÔN MẶT, không phải màu.
  ③ Bằng chứng nội bộ trùng hướng: video CTR cao nhất kênh (3,6%) chính là bản
     nền đen không ảnh scene; hai bản v4 chữ-trên-scene được 3,2% và ở 120px
     thành mảng xám nhòe.

⚠️ Chân dung phải là NHÂN VẬT HƯ CẤU do AI gen — ảnh stock mặt người thật vi phạm
   luật thumbnail của kênh (`.claude/rules/youtube-compliance.md` §2). Không có
   ảnh chân dung thì dùng VẬT CHỨNG (túi tiền/chìa khoá/di chúc) — cùng cơ chế
   bố cục, không cần gen ảnh.
⚠️ Chưa chứng minh CTR lên — tương quan 2 chiều, không phải nhân quả. Đo lại
   2026-08-17, và KHÔNG thay thumbnail 07-25/07-27/07-06 (nhóm chứng).

Bản v4 nguyên trạng: make_thumb_textwall_v4_snapshot.py.

═══════════════════════════════════════════════════════════════════════════════
v4 (2026-07-27) — giữ nguyên phần chữ, ghi lại để tra cứu
═══════════════════════════════════════════════════════════════════════════════

v4 thay v3 sau khi mổ CTR (bản v3 giữ ở make_thumb_textwall_v3_backup.py).

LÝ DO ĐỔI — đo 20 thumbnail của 4 kênh đối thủ cùng rail related, 2026-07-27
(⚠️ mốc này CHỨA HIT CŨ, xem cảnh báo LUẬT ĐO ở trên):

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

Bảng màu: v4 chốt wcyr, NHƯNG user đã đổi sang p,y,c,r ngày 2026-07-28 (hồng mở + đỏ
đòn; bão hòa 130,5 · %rực 30,2 · đánh đổi tương phản 68,2→55,8). Đoạn dưới chỉ còn
giá trị lịch sử. Đã thử 4 bộ — cpyr 75.5 · wpyr 86.9 · cwyr 85.9 · wcyr 89.1
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

⭐ CÔNG THỨC CHỐT CỦA KÊNH (user duyệt 2026-07-28, mẫu 06_VIDEO/_thumb_v5_demo/CHOT_v5_5.png, đang trên sóng video 10).
   Dùng nguyên cho mọi video; chỉ đổi --lines và --bg. Luật đầy đủ + 6 đường đã LOẠI: CLAUDE.md.

   python tools/make_thumb_textwall.py 06_VIDEO/<x>/thumbnail.png \
     --lines "<dòng mở>" "<quote 1>" "<quote 2>" "<dòng đòn>" \
     --colors p,y,c,r --outline 0.048 --fat 0.008 \
     --weights "1.0,0.85,0.88,1.0" --split 1 --wide all --align center \
     --bg 06_VIDEO/_series_assets/scene_<NN>_ai.jpg --bg-target 104 --scrim 0.32

   → ảnh 2 người phủ toàn khung · phủ tối nhẹ TOÀN khung (không dải che) · 1 dòng neo mép
     trên + 3 dòng neo mép dưới · mọi dòng trải hết bề ngang · dòng mở và dòng đòn cùng cỡ
     lớn nhất · băng giữa hở trọn mặt. 4 dòng ≤12 ký. --split chọn theo VỊ TRÍ MẶT từng ảnh.
   → Không có ảnh người: bỏ --bg/--split/--wide, dùng 5 dòng nền đen (mặc định --bgstyle flat).

Chạy (các chế độ khác):
  python tools/make_thumb_textwall.py <out.png> --lines "d1" "d2" "d3" "d4" "dòng đỏ"
  # có chân dung nhân vật AI / ảnh vật chứng:
  python tools/make_thumb_textwall.py <out.png> --lines ... --portrait <ảnh> --portrait-w 0.42
  [--colors w,c,y,r]  ghi đè màu (w trắng · p hồng · c cyan · v tím · y vàng · o cam · r đỏ)
  [--bgstyle auto|flat|scene|grad|dark]  auto = có --bg thì scene, không thì FLAT (v5)
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
FONT_KEY_DEFAULT = FONT_KEY      # bản gốc, để --preset biết user có tự đặt --font hay không

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
    "r": (255, 24, 24),     # đỏ — dòng đòn cuối. ⚠️ tương phản CHỈ 4,3x trên nền tối và
                            # 1,6x trên nền ảnh (đo WCAG 2026-07-28) → BẮT BUỘC đi kèm quầng
                            # trắng, bỏ quầng là chữ nhoè với mắt 45–70.
    # ── v5.8: 3 màu "dễ chịu" thêm 2026-07-28 sau khi đo tương phản độ chói ──
    # Mắt 45–70 cần ≥7x trên nền tối và ≥4,5x khi chữ đè lên ảnh. Đo được:
    #   w 16,3/6,1 · e 15,6/5,8 · y 12,9/4,8 · s 12,3/4,6 · c 11,9/4,4 · a 9,6/3,6
    #   o 7,7/2,9 · v 5,0/1,9 · p 4,8/1,8 · r 4,3/1,6  ← p/v/r KHÔNG dùng cho dòng dài
    "e": (255, 246, 224),   # kem — màu NỀN của chữ (thay trắng gắt), êm mắt hơn w
    "s": (140, 235, 255),   # cyan nhạt — thoại phản diện, dịu hơn c mà tương phản cao hơn
    "a": (255, 183, 3),     # amber — thay r ở dòng đòn khi muốn êm mắt (9,6x vs 4,3x)
}
AUTO = {3: "wyr", 4: "wcyr", 5: "wpcyr", 6: "wwwwyr", 7: "wwwwwyr"}

# ── v5.7: TÔ MÀU TỪ KHOÁ trong lòng dòng (user chốt 2026-07-28, theo mẫu 娘の結婚式で) ──
# Cú pháp trong --lines:  夫は{愛人}と腕を組み   → 愛人 lấy màu --accent (mặc định đỏ)
#                         私は静かに[前列]を譲った → 前列 lấy màu --accent2 (mặc định vàng)
# Đây là thứ mẫu đối thủ dùng để "đẩy cảm xúc" mà không cần tăng số dòng: dòng vẫn
# trắng, chỉ 1–2 chữ ăn tiền được bơm màu, nên mắt bắt đúng từ khoá ở 120px.
def parse_hl(text):
    """'a{b}c[d]' -> (plain, [tag theo tung ky tu]) voi tag 0=goc 1=accent 2=accent2."""
    plain, tags, mode = [], [], 0
    for ch in text:
        if ch == "{": mode = 1; continue
        if ch == "[": mode = 2; continue
        if ch in "}]": mode = 0; continue
        plain.append(ch); tags.append(mode)
    return "".join(plain), tags


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


def apply_scrim(img, side, strength=0.62, span=0.72):
    """v5.1 — phủ tối MỘT BÊN ảnh cảnh để chữ đọc được, bên kia để hở mặt người.

    Đúng cách 3 thumbnail đối thủ user đưa 2026-07-28 (五十年ぶりの同窓会 / 冷酷CEO /
    親呼んでみろ) làm: ảnh cảnh phủ TOÀN KHUNG, nhưng nửa có chữ bị tối đi rõ rệt,
    nửa còn lại giữ nguyên độ sáng để mặt nhân vật vẫn là điểm neo mắt.

    Khác `--portrait`: portrait DÁN một dải ảnh lên nền đen (mất hết ảnh còn lại);
    scrim GIỮ TRỌN ảnh và chỉ hạ sáng phần dưới chữ. Dùng scrim khi ảnh có người
    đang tương tác (cần thấy cả cảnh), dùng portrait khi chỉ có 1 chân dung.

    - `strength` độ tối tối đa ở mép NGOÀI phía chữ (0.62 = còn 38% sáng)
    - `span`     dải chuyển tiếp tính theo bề ngang khung
    """
    if side == "full":
        a = np.asarray(img).astype(np.float32) * (1.0 - strength * 0.55)
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    xx = np.linspace(0, 1, W, dtype=np.float32)
    t = np.clip(xx / span, 0, 1) if side == "left" else np.clip((1 - xx) / span, 0, 1)
    k = (1.0 - strength * (1.0 - t) ** 1.4)[None, :, None]
    return Image.fromarray(np.clip(np.asarray(img).astype(np.float32) * k, 0, 255).astype(np.uint8))


def paste_panel(img, src, width_ratio=0.38, side="right", target=112, focus=0.5, zoom=1.0,
                focus_y=0.0):
    """v5.7 — dán ảnh thành PANEL chữ nhật, mép CỨNG, phần còn lại là nền đen.

    Khác `--portrait` (dải ảnh hoà tan dần vào nền) và khác `--bg` (ảnh phủ toàn khung):
    panel là một khối ảnh rõ mép, chiếm ~1/4–2/5 khung, còn lại đen tuyền để nhồi
    nhiều dòng chữ. Đây là cấu trúc mẫu 娘の結婚式で mà user chốt 2026-07-28 —
    "chủ thể chỉ 1/4, còn lại là text".
    """
    pw = round(W * width_ratio)
    im = Image.open(src).convert("RGB")
    sc = max(pw / im.width, H / im.height) * max(zoom, 1.0)
    im = im.resize((max(pw, round(im.width * sc)), max(H, round(im.height * sc))), Image.LANCZOS)
    x0 = int(round((im.width - pw) * min(max(focus, 0.0), 1.0)))
    y0 = int(round((im.height - H) * min(max(focus_y, 0.0), 1.0)))
    im = im.crop((x0, y0, x0 + pw, y0 + H))
    a = np.asarray(im).astype(np.float32) / 255.0
    if float(np.asarray(im.convert("L")).mean()) > 1:      # nang sang theo dich (gamma)
        lo_g, hi_g = 0.25, 3.0
        for _ in range(24):
            g = (lo_g + hi_g) / 2
            if (a ** g).mean() * 255 > target: lo_g = g
            else: hi_g = g
        a = np.clip(a ** ((lo_g + hi_g) / 2), 0, 1)
    im = Image.fromarray((a * 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.14)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=3))
    px = (W - pw) if side == "right" else 0
    img.paste(im, (px, 0))
    return px, pw


def bg_flat(seed=11):
    """v5 — nền GẦN ĐEN phẳng, đúng thứ nhóm thắng 30 ngày dùng.

    Không phải đen tuyệt đối: JPEG nén vùng đen tuyệt đối ra banding, và một
    chút nhô sáng ở giữa giúp chữ trắng không bị "dán lên hố". Công thức: đáy
    (7,7,9) + quầng elip rất nhẹ lên (22,22,28) ở giữa-trên + hạt nhiễu ±3.
    KHÔNG thêm sao/tia như bg_gradient — nhóm thắng để nền im, mọi chú ý dồn
    vào chữ và (nếu có) khuôn mặt.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.5) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.85)) ** 2)
    core = np.clip(1.0 - r, 0, 1) ** 1.8
    a = np.zeros((H, W, 3), np.float32)
    a[..., 0] = 7 + core * 15
    a[..., 1] = 7 + core * 15
    a[..., 2] = 9 + core * 19
    rng = np.random.default_rng(seed)
    a += rng.normal(0, 1.2, (H, W, 1))          # hạt mịn chống banding
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def paste_portrait(img, src, width_ratio=0.42, side="right", anchor="top",
                   feather=0.26, target=104, focus=0.5, zoom=1.0):
    """v5 — dán chân dung/vật chứng vào một BÊN khung, hoà tan vào nền đen.

    Cách nhóm thắng 30 ngày làm (世界の中心でスカッと朗読 + vài mẫu スカっとゼミ!):
    ảnh KHÔNG phủ toàn khung sau chữ, mà chiếm gọn ~40% một bên, cạnh trong
    fade dần về đen để chữ bên kia không phải tranh nền với nó.

    - `width_ratio`  bề ngang dải ảnh / bề ngang khung (0.30–0.50 là dải dùng được)
    - `anchor`       "top" cho chân dung (mặt nằm phần trên, cắt là mất mặt) ·
                     "center" cho vật chứng
    - `feather`      độ rộng vùng hoà tan, tính theo bề ngang dải ảnh
    - `target`       độ sáng trung bình đích của dải ảnh — chân dung phải SÁNG
                     hơn nền để làm điểm neo mắt; nhưng đừng vượt ~120 kẻo hút
                     hết chú ý khỏi chữ.
    - `focus`        TÂM CROP NGANG trong ảnh gốc, 0 = mép trái · 0.5 = giữa ·
                     1 = mép phải. Dải ảnh chỉ rộng ~0.6 lần chiều cao nên ảnh
                     16:9 bị cắt rất nhiều bề ngang; ảnh gen ra mà người lệch
                     một bên (rất hay xảy ra) thì crop giữa **cắt đúng người**.
                     Đo mắt vị trí mặt trong ảnh gốc rồi truyền số đó vào.

    ⚠️ Chân dung phải là nhân vật hư cấu (AI gen). Xem cảnh báo compliance ở đầu file.
    """
    bw = round(W * width_ratio)
    im = Image.open(src).convert("RGB")
    s = max(bw / im.width, H / im.height) * max(zoom, 1.0)
    im = im.resize((max(bw, round(im.width * s)), max(H, round(im.height * s))), Image.LANCZOS)
    x0 = int(round((im.width - bw) * min(max(focus, 0.0), 1.0)))
    y0 = 0 if anchor == "top" else (im.height - H) // 2
    im = im.crop((x0, y0, x0 + bw, y0 + H))

    # nâng sáng theo ĐÍCH bằng gamma (cùng cách bg_scene — ảnh AI của kênh rất tối)
    a = np.asarray(im).astype(np.float32) / 255.0
    if float(np.asarray(im.convert("L")).mean()) > 1:
        lo_g, hi_g = 0.25, 3.0
        for _ in range(24):
            g = (lo_g + hi_g) / 2
            if (a ** g).mean() * 255 > target:
                lo_g = g
            else:
                hi_g = g
        a = np.clip(a ** ((lo_g + hi_g) / 2), 0, 1)
    im = Image.fromarray((a * 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=3))

    # mask hoà tan: đục ở cạnh NGOÀI, trong suốt dần về cạnh TRONG (phía chữ)
    fw = max(1, round(bw * feather))
    ramp = np.ones(bw, np.float32)
    grad = np.linspace(0, 1, fw) ** 1.35
    if side == "right":
        ramp[:fw] = grad                       # mép trái (phía chữ) fade
        px = W - bw
    else:
        ramp[bw - fw:] = grad[::-1]            # mép phải fade
        px = 0
    mask = Image.fromarray((np.tile(ramp, (H, 1)) * 255).astype(np.uint8), "L")
    img.paste(im, (px, 0), mask)
    return px, bw


def bg_scene(src, brightness=1.0, target=88, sat=1.15, cool=0.0):
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
    # TÔNG LẠNH (opt-in, 2026-08-03). ⚠️ Docstring trên ghi "bỏ HẲN mọi can thiệp kênh
    # màu" vì 2026-07-27 user chê ám xanh — lần đó là ám xanh KHÔNG AI YÊU CẦU và kèm
    # cộng offset làm đục vùng tối. Đây khác: opt-in, chỉ NHÂN hệ số (không cộng offset
    # nên đáy vẫn về đen), và chạy TRƯỚC vòng gamma nên độ sáng vẫn về đúng target.
    # Dùng cho nhánh TRẦM: dập ám cam của scene AI mà không phải rút hết màu thành xám.
    if cool > 0:
        _c = np.asarray(im).astype(np.float32)
        _c[..., 0] *= 1 - 0.30 * cool          # R xuống — giết ám cam/vàng
        _c[..., 1] *= 1 - 0.07 * cool
        _c[..., 2] *= 1 + 0.16 * cool          # B lên — kéo về lam/teal
        im = Image.fromarray(np.clip(_c, 0, 255).astype(np.uint8))
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
    # Bão hoà: 1.15 = mặc định (giữ màu thật). Hạ xuống <1 cho nhánh "TRẦM" — đo
    # 2026-08-03: cái làm mẫu 14-T2 trông trầm KHÔNG phải tối hơn (nó p20 6, bằng
    # bản mình) mà là BÃO HOÀ 86 vs 137–145. Scene AI của kênh rực teal/cam sẵn.
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=75, threshold=3))


def draw_line(d, x, y, text, f, fill, sz, halo=False, fat_ratio=FAT, track=None,
              outline_ratio=None):
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
    # outline_ratio=0 → KHÔNG viền. Bắt buộc cho chữ nằm trên CHIP màu: chip đã tách
    # chữ khỏi ảnh rồi, thêm viền đen 4–6px nữa là 認・驚 vón cục (đúng lỗi bản thử
    # đầu 2026-07-28, xem cảnh báo trong docstring draw_line).
    _or = OUTLINE if outline_ratio is None else outline_ratio
    outline = 0 if _or <= 0 else max(4, round(sz * _or))
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
    if fat + outline > 0:
        for px, ch in pos:
            d.text((px, y), ch, font=f, fill=BLACK, stroke_width=fat + outline, stroke_fill=BLACK)
    # fill co the la 1 mau (tuple) HOAC list mau tung ky tu (to mau tu khoa)
    fills = fill if isinstance(fill, list) else [fill] * len(pos)
    for (px, ch), fl in zip(pos, fills):
        if fat:
            d.text((px, y), ch, font=f, fill=fl, stroke_width=fat, stroke_fill=fl)
        else:
            d.text((px, y), ch, font=f, fill=fl)


def main():
    global FONT_KEY
    ap = argparse.ArgumentParser(description="Thumbnail text-wall v4 — thumbnail chuẩn kênh chouhen")
    ap.add_argument("out")
    ap.add_argument("--lines", nargs="+", required=True)
    ap.add_argument("--colors", default="auto")
    ap.add_argument("--bg", default="")
    ap.add_argument("--bgstyle", default="auto",
                    choices=["auto", "flat", "grad", "dark", "scene"],
                    help="auto = có --bg thì lót scene, không có thì FLAT (nền gần đen, v5)")
    ap.add_argument("--portrait", default="",
                    help="v5 — ảnh chân dung nhân vật AI (hoặc vật chứng) dán một bên khung")
    ap.add_argument("--portrait-w", type=float, default=0.42,
                    help="bề ngang dải ảnh / bề ngang khung (0.30–0.50)")
    ap.add_argument("--portrait-side", default="right", choices=["right", "left"])
    ap.add_argument("--portrait-anchor", default="top", choices=["top", "center"],
                    help="top = chân dung (giữ mặt) · center = vật chứng")
    ap.add_argument("--portrait-target", type=float, default=104,
                    help="độ sáng trung bình đích của dải ảnh (nên 95–120)")
    ap.add_argument("--portrait-focus", type=float, default=0.5,
                    help="tâm crop NGANG trong ảnh gốc (0 trái · 0.5 giữa · 1 phải). "
                         "Ảnh 16:9 mà người lệch một bên thì PHẢI đặt, không thì cắt đúng người")
    ap.add_argument("--text-side", default="full", choices=["full", "left", "right"],
                    help="v5.1 — dồn chữ về một bên khung, bên kia để hở mặt nhân vật "
                         "(kiểu 3 thumbnail đối thủ 2026-07-28). Đi kèm --scrim")
    ap.add_argument("--text-w", type=float, default=0.60,
                    help="bề ngang vùng chữ / khung khi --text-side left|right (0.52–0.66)")
    ap.add_argument("--scrim", type=float, default=0.62,
                    help="độ phủ tối phía có chữ (0 = tắt). Chỉ áp với --bgstyle scene")
    ap.add_argument("--chip", default="",
                    help='chỉ số dòng (0-based, "0,2") được vẽ trên CHIP màu đặc ôm sát chữ, '
                         'chữ đảo sang đen/trắng theo độ sáng chip — kiểu 「若い女性は」 nền đỏ')
    # ── v5.2: TRÌNH BÀY CHỮ kiểu đối thủ (user 2026-07-28: "text của mày khác lắm") ──
    ap.add_argument("--panel-w", type=float, default=0.0,
                    help="v5.7 — dán ảnh thành PANEL mép cứng chiếm tỉ lệ này (0.25–0.42), phần "
                         "còn lại nền ĐEN để nhồi nhiều dòng chữ. Kiểu mẫu 娘の結婚式で")
    ap.add_argument("--panel-side", default="right", choices=["right", "left"])
    ap.add_argument("--panel-focus", type=float, default=0.5,
                    help="tâm crop ngang trong ảnh gốc cho panel (0 trái · 1 phải)")
    ap.add_argument("--panel-zoom", type=float, default=1.0, help="phóng ảnh panel cho mặt to")
    ap.add_argument("--panel-focus-y", type=float, default=0.0,
                    help="tâm crop DỌC của panel (0 mép trên · 1 mép dưới). Zoom cao thì PHẢI đặt, "
                         "không thì cắt mất mặt")
    ap.add_argument("--accent", default="r", help="màu từ khoá {…} (mặc định r đỏ)")
    ap.add_argument("--accent2", default="y", help="màu từ khoá [.…] (mặc định y vàng)")
    ap.add_argument("--indent", type=int, default=22,
                    help="lề trái (px) khi --align left, áp cho MỌI dòng kể cả dòng --wide "
                         "để mép trái thẳng hàng. 22 = sát mép · 56–96 = thụt vào")
    ap.add_argument("--align", default="center", choices=["center", "left"],
                    help="v5.2 — đối thủ căn LỀ TRÁI (mọi dòng cùng mép trái), không căn giữa")
    ap.add_argument("--block", default="fill", choices=["fill", "top", "center", "bottom"],
                    help="fill = giãn đều phủ hết chiều cao (v4/v5). top|center|bottom = NÉN "
                         "khối chữ sát nhau rồi neo — đúng cách đối thủ làm")
    ap.add_argument("--weights", default="",
                    help='hệ số cỡ chữ TỪNG DÒNG, vd "0.62,1,0.55,0.95". ≤1 (dòng nào để 1 là '
                         'dòng punch to nhất). Đối thủ phân cấp mạnh, không cho mọi dòng full-width')
    ap.add_argument("--shade", default="",
                    help='chỉ số dòng (hoặc "all") có DẢI ĐEN MỜ ôm sát chữ — kiểu 五十年ぶりの同窓会')
    ap.add_argument("--shade-alpha", type=int, default=150, help="độ đục dải mờ 0–255")
    ap.add_argument("--box", default="",
                    help='chỉ số dòng có KHUNG VIỀN màu (không tô) — kiểu 「ずっと毎晩欲しい」')
    ap.add_argument("--outline", type=float, default=OUTLINE,
                    help=f"độ dày viền ĐEN quanh chữ (tỉ lệ cỡ chữ, mặc định {OUTLINE}). Dày hơn = "
                         "màu chữ nổi khối hơn trên ảnh. ⚠️ >0.045 bắt đầu bịt lòng chữ hán")
    ap.add_argument("--halo", default="",
                    help='chỉ số dòng (hoặc "all") có QUẦNG TRẮNG quanh viền đen — cơ chế "nổi" '
                         'của dòng đòn v4, giờ gán được cho bất kỳ dòng nào (mặc định chỉ dòng đỏ)')
    ap.add_argument("--seethru", default="",
                    help='v5.4 — chỉ số dòng (hoặc "all") có RUỘT CHỮ LÀ ẢNH: viền màu + lòng chữ '
                         'hiện ảnh gốc chưa bị phủ tối. Dùng khi không muốn dải che nuốt nhân vật '
                         '(user chốt 2026-07-28: "che thì bỏ background đi chứ, để text nhìn xuyên hình")')
    ap.add_argument("--seethru-mix", type=float, default=0.0,
                    help="pha màu chữ vào ruột ảnh: 0 = ruột toàn ẢNH (thường KHÔNG đọc được trên "
                         "ảnh tương phản thấp) · 0.4–0.55 = vừa thấy ảnh vừa đọc được · 1 = màu đặc")
    ap.add_argument("--split", type=int, default=0,
                    help="v5.3 — chia chữ thành HAI KHỐI: N dòng đầu neo TRÊN, còn lại neo DƯỚI, "
                         "chừa băng giữa cho mặt nhân vật. Đúng cấu trúc mẫu 親呼んでみろｗ — dùng "
                         "khi ảnh có người ở GIỮA khung (không có cột trống nào cho chữ)")
    ap.add_argument("--wide", default="",
                    help='chỉ số dòng được TRẢI HẾT bề ngang khung, bỏ qua --text-w. Đối thủ '
                         'chỉ cho DÒNG CHỐT trải rộng (nó nằm DƯỚI mặt người), còn dòng bối '
                         'cảnh thì hẹp một bên để không nuốt mặt. Thường là dòng cuối.')
    ap.add_argument("--portrait-zoom", type=float, default=1.0,
                    help="phóng ảnh trước khi crop để MẶT TO hơn (1.4–1.8 khi ảnh gen ra "
                         "là toàn thân — đối thủ dùng cỡ bán thân, mặt là điểm neo mắt)")
    ap.add_argument("--bg-brightness", type=float, default=1.0,
                    help="hệ số nhân THÊM sau khi đã chuẩn hoá về --bg-target")
    ap.add_argument("--bg-cool", type=float, default=0.0,
                    help="TÔNG LẠNH nền scene, 0–1 (0 = tắt). Dập ám cam/vàng, kéo về lam-teal. "
                         "Nhánh TRẦM nên 0.55–0.75 KÈM --bg-sat 0.8–0.9 — hạ sat sâu (<0.5) là "
                         "ra ĐEN TRẮNG, không phải tông lạnh")
    ap.add_argument("--bg-sat", type=float, default=1.15,
                    help="bão hoà nền scene. 1.15 = mặc định (giữ màu thật) · **0.55 = nhánh "
                         "TRẦM** (khuôn 14-T2: bão hoà ~86 trong khi bản rực là 137–145). "
                         "\"Trầm\" của mẫu là BỚT RỰC, không phải tối hơn")
    ap.add_argument("--bg-target", type=float, default=88,
                    help="độ sáng trung bình đích của nền scene (0-255). Cao hơn = phông sáng hơn")
    ap.add_argument("--band", nargs="?", const="r", default=None,
                    help="dải tối ĐẶC full-width sau dòng chữ. Bỏ trống = chỉ dòng đòn đỏ "
                         "(hành vi cũ) · \"0,4\" = các dòng theo chỉ số · \"all\" = mọi dòng. "
                         "Mẫu 08 dùng \"0,4\" (dòng bối cảnh đầu + dòng đòn cuối nằm trên dải đen)")
    ap.add_argument("--preset", choices=["m08", "k1", "k2"], default=None,
                    help="k1/k2 = HAI KHUÔN ĐANG THI HÀNH (chốt 2026-08-12, "
                         "CHANNEL_DIAGNOSIS_2026-08-12.md §3.2) — k1 text-wall + dàn người "
                         "(mẫu 毎日スカッと 105K view) · k2 cảnh sáng kể chuyện (mẫu 語り茶屋 205K · "
                         "孤独な桜の木 44K). m08 = khuôn CŨ, nền dập gần đen — GIỮ để re-render "
                         "video cũ, ĐỪNG dùng cho video mới. Cờ truyền tay LUÔN thắng preset")
    ap.add_argument("--font", default=None, choices=list(FONTS),
                    help="mplus = M PLUS 1p Black (nặng nhất, mặc định) · noto = Noto Sans JP 900 · yu = font cũ")
    ap.add_argument("--mark", default=None,
                    help="DẤU NHẬN DIỆN KÊNH: vạch dọc màu + tên kênh dọc theo vạch ở mép "
                         "phải, vẽ SAU lớp chữ nên không bị nén 平体. Cùng vị trí/màu trên "
                         "mọi video = mắt người xem nhận ra kênh trong feed. "
                         'vd --mark "真夜中の朗読便"')
    ap.add_argument("--mark-style", choices=["circle", "edge", "hanko", "moon", "bar"], default="circle",
                    help="kiểu dấu nhận diện: hanko = con dấu đỏ tròn (mặc định) · "
                         "moon = trăng khuyết + vành khung · bar = vạch dọc (bản đầu)")
    ap.add_argument("--mark-short", default=None,
                    help="2 chữ trong con dấu hanko (mặc định 朗読)")
    ap.add_argument("--fat", type=float, default=None,
                    help="làm dày nét chữ (tỉ lệ cỡ chữ). Bỏ trống = trần an toàn theo "
                         f"font ({FAT_BY_FONT}); vượt trần là bịt lòng chữ hán")
    a = ap.parse_args()

    # ── PRESET "m08" — khuôn text-wall CHỐT của kênh, user duyệt bằng mắt 2026-08-03 ──
    # Gộp cả 4 biến đã phải đo mất 4 vòng mới ra (xem CLAUDE.md §THUMBNAIL). Dùng preset
    # thì không vòng nào bị quên; muốn đè biến nào thì cứ truyền cờ đó, preset nhường.
    if a.preset == "m08":
        if a.font is None:              a.font = "yu"    # ① font mộc của mẫu 08 (nhánh MỎNG)
        if a.fat is None:               a.fat = 0.0      # ② nét KHÔNG bơm (đặc nét 0.38–0.40)
        if a.bg_target == 88:           a.bg_target = 38 # ③ nền tắt gần hết, còn đọc được mặt
        if a.bg_sat == 1.15:            a.bg_sat = 0.90  # ④ GIỮ bão hoà — <0.5 là ra đen trắng
        if a.bg_cool == 0.0:            a.bg_cool = 0.75 # ⑤ tông LẠNH: hạ R, nâng B
        if a.band is None:              a.band = ""      # ⑥ KHÔNG dải đen sau chữ
        if not a.weights and len(a.lines) == 5:
            a.weights = "0.85,0.86,0.86,0.82,0.90"       # 5 dòng, không để 平体 squash
        if a.colors == "auto" and len(a.lines) == 5:
            a.colors = "w,c,p,y,r"

    # ── PRESET "k1" — TEXT-WALL + DÀN NGƯỜI (mẫu 毎日スカッと, video 105.183 view) ──
    # Chốt 2026-08-12. Nền ĐEN TUYỀN, chữ dồn 65–70% bề ngang TRÁI, cụm 3–5 nhân vật có
    # biểu cảm + 1 vật chứng dán thành PANEL 30–35% bên PHẢI, dòng đòn ĐỎ to nhất.
    # 🔴 Ảnh --bg PHẢI là ảnh có ≥2 người đang DIỄN đúng cảnh truyện — đó là biến của lượt
    #    này. Nền phòng trống = quay lại đúng lỗi của video 09 (367 view, không một bóng người).
    if a.preset == "k1":
        if a.font is None:              a.font = "yu"
        if a.fat is None:               a.fat = 0.0
        if a.panel_w == 0.0:            a.panel_w = 0.33   # dàn người chiếm 1/3 phải
        if a.band is None:              a.band = ""        # nền đã đen, không cần dải
        if not a.weights and len(a.lines) == 6:
            a.weights = "0.88,0.90,0.86,1.00,0.86,0.94"    # dòng 4 = đòn đỏ, to nhất
        if a.colors == "auto" and len(a.lines) == 6:
            a.colors = "w,y,w,r,w,c"

    # ── PRESET "k2" — CẢNH SÁNG KỂ CHUYỆN (mẫu 語り茶屋 205.890 view · 孤独な桜の木 44.127) ──
    # Chốt 2026-08-12. Ảnh cảnh photoreal SÁNG chiếm 70–75% khung, người diễn ở GIỮA,
    # chỉ 2–3 dải chữ kẹp trên–dưới (--split 1) trên dải đen mảnh.
    # ⚠️ Đây là khuôn NGƯỢC HẲN m08: m08 dập nền về p20≤10, k2 để nền SÁNG và đọc được cảnh.
    if a.preset == "k2":
        if a.font is None:              a.font = "yu"
        if a.fat is None:               a.fat = 0.0
        if a.bg_target == 88:           a.bg_target = 104  # nền SÁNG, thấy rõ ai đang làm gì
        if a.scrim == 0.62:             a.scrim = 0.28     # chỉ hạ nhẹ, KHÔNG dập
        if a.band is None:              a.band = "all"     # chữ nổi trên nền sáng bằng dải đen
        if a.split == 0 and len(a.lines) == 3:
            a.split = 1                                    # 1 dòng trên · 2 dòng dưới, chừa mặt
        if not a.weights and len(a.lines) == 3:
            a.weights = "0.94,0.96,0.96"
        if a.colors == "auto" and len(a.lines) == 3:
            a.colors = "w,y,r"

    if a.preset == "m08":
        print("   ⚠️ preset m08 = khuôn CŨ (nền dập gần đen, không người). Video MỚI dùng "
              "--preset k1 hoặc k2 — CLAUDE.md §THUMBNAIL, chốt 2026-08-12")
    if a.preset in ("k1", "k2") and not a.bg:
        # Cả 2 khuôn mới đứng trên ẢNH NGƯỜI ĐANG DIỄN — không có --bg thì chúng vô nghĩa,
        # và bản ra sẽ là đúng cái lỗi đang đi chữa (chữ đứng một mình trên nền trống).
        sys.exit("❌ --preset k1/k2 BẮT BUỘC có --bg: ảnh phải có ≥2 nhân vật biểu cảm rõ đang "
                 "DIỄN đúng cảnh truyện + ≥1 vật chứng (phong bì/giấy tờ/chìa khoá). "
                 "Đó chính là biến đang thử — CHANNEL_DIAGNOSIS_2026-08-12.md §3.2")

    # ⚠️ --font phải có default=None: trước đây default="mplus" nên preset KHÔNG phân biệt
    # được "user tự gõ --font mplus" với "để mặc định" → nhánh DÀY bị preset ép về yu, im lặng.
    if a.font is None:
        a.font = FONT_KEY_DEFAULT
    FONT_KEY = a.font
    font.cache_clear()
    if a.fat is None:
        a.fat = FAT_BY_FONT[a.font]

    # v5.7 — tách markup tô màu từ khoá: raw giữ {..}/[..], lines là text sạch để đo/vẽ
    raw = a.lines
    parsed = [parse_hl(t) for t in raw]
    lines = [pl for pl, _ in parsed]
    hl_tags = [tg for _, tg in parsed]
    if not 3 <= len(lines) <= 7:
        sys.exit("❌ Cần 3–7 dòng.")

    keys = AUTO[len(lines)] if a.colors == "auto" else a.colors.replace(",", "")
    if len(keys) != len(lines) or any(k not in COLORS for k in keys):
        sys.exit(f"❌ --colors phải là {len(lines)} ký tự trong {'/'.join(COLORS)}")

    if a.bgstyle == "auto":
        # có --panel-w thì ảnh chỉ là panel → nền phải ĐEN, không lót scene toàn khung
        a.bgstyle = "flat" if (a.panel_w > 0 or not a.bg) else "scene"
    if a.bgstyle == "scene" and a.bg:
        img = bg_scene(a.bg, a.bg_brightness, a.bg_target, a.bg_sat, a.bg_cool)
    elif a.bgstyle == "dark":
        img = Image.new("RGB", (W, H), (10, 10, 14))
    elif a.bgstyle == "grad":
        img = bg_gradient()
    else:
        img = bg_flat()

    # v5.4 — giữ một bản ảnh SẠCH (chưa phủ tối, chưa dải che) để làm ruột chữ xuyên hình.
    img_clean = img.copy()

    # v5.1 — ảnh cảnh phủ toàn khung + phủ tối phía có chữ + dồn chữ một bên.
    area_x0, area_w = 0, W
    if a.bgstyle == "scene" and a.scrim > 0:
        img = apply_scrim(img, a.text_side, a.scrim)
    if a.text_side != "full":
        tw_area = round(W * a.text_w)
        area_x0 = 0 if a.text_side == "left" else W - tw_area
        area_w = tw_area
        print(f"   chữ dồn {a.text_side} {tw_area}px ({a.text_w:.0%}) · scrim {a.scrim}")

    # v5.7 — PANEL ảnh mép cứng trên nền đen; chữ dồn hết về bên còn lại.
    if a.panel_w > 0 and a.bg:
        ppx, ppw = paste_panel(img, a.bg, a.panel_w, a.panel_side,
                               focus=a.panel_focus, zoom=a.panel_zoom,
                               focus_y=a.panel_focus_y)
        area_x0 = 0 if a.panel_side == "right" else ppw
        area_w = W - ppw
        print(f"   panel {a.panel_side} {ppw}px ({a.panel_w:.0%}) → vùng chữ {area_w}px")

    # v5 — dán chân dung TRƯỚC khi vẽ chữ, rồi thu vùng chữ về nửa còn lại.
    if a.portrait:
        px, bw = paste_portrait(img, a.portrait, a.portrait_w, a.portrait_side,
                                a.portrait_anchor, target=a.portrait_target,
                                focus=a.portrait_focus, zoom=a.portrait_zoom)
        # chữ được lấn vào ~1/3 vùng hoà tan (ở đó ảnh đã gần đen) để không hụt bề ngang
        bleed = round(bw * 0.26 * 0.34)
        if a.portrait_side == "right":
            area_x0, area_w = 0, W - bw + bleed
        else:
            area_x0, area_w = bw - bleed, W - bw + bleed
        print(f"   chân dung {Path(a.portrait).name} · {a.portrait_side} {bw}px "
              f"({a.portrait_w:.0%}) → vùng chữ {area_w}px")
    d = ImageDraw.Draw(img)

    # LAYOUT: mọi dòng căng full-width vùng chữ, rồi scale cả khối cho vừa chiều cao.
    # lề trái khi --align left phải TRỪ vào bề rộng cho phép, không thì dòng dài
    # (weight 1.0) bị đẩy tràn khỏi khung phải và mất chữ — bẫy phát hiện 2026-07-28.
    ind = a.indent if a.align == 'left' else 0
    margin_y, gap, max_w = 14, 10, area_w - 44 - ind
    sws = [(a.fat + a.outline + 0.045) if k == "r" else (a.fat + a.outline) for k in keys]
    wides = ({int(i) for i in a.wide.replace(" ", "").split(",") if i != ""}
             if a.wide.strip() != "all" else set(range(len(lines))))
    # bề ngang cho phép của TỪNG dòng: dòng --wide dùng cả khung, còn lại bó trong vùng chữ
    lmax = [(W - 44 - ind) if i in wides else max_w for i in range(len(lines))]
    sizes = [size_for_width(t, m, sw) for t, m, sw in zip(lines, lmax, sws)]

    # v5.2 — PHÂN CẤP CỠ CHỮ CHỦ ĐỘNG. v4 để "mọi dòng full-width" nên phân cấp chỉ
    # sinh ra từ số ký tự; đối thủ thì cố ý cho 1 dòng punch TO HẲN và dòng bối cảnh
    # nhỏ hẳn (五十年ぶり: dòng chốt gấp ~1,6 lần dòng đầu). Hệ số ≤1 để không tràn khung.
    if a.weights:
        ws = [float(x) for x in a.weights.replace(" ", "").split(",")]
        if len(ws) != len(lines):
            sys.exit(f"❌ --weights phải có đúng {len(lines)} số")
        if max(ws) > 1.0:
            print(f"⚠️ --weights >1 bị kẹp về 1 (dòng đã căng hết bề ngang khung)")
        sizes = [max(40, round(s * min(w, 1.0))) for s, w in zip(sizes, ws)]
        gap = 6                       # dòng phụ nhỏ lại thì khe phải hẹp, không thì rời rạc

    def heights(szs):
        return [font(s).getbbox(t)[3] - font(s).getbbox(t)[1] + round(2 * sw * s)
                for s, t, sw in zip(szs, lines, sws)]

    # v6 (2026-07-29) — 平体 SQUASH: trước đây nhiều dòng vượt chiều cao khung thì co
    # CỠ CHỮ cả khối → mọi dòng hẹp lại, dồn vào giữa, thừa 2 mép (user bắt lỗi trên
    # bản 6 dòng đầu tiên: "text co rúm lại, nằm giữa trung tâm"). Đối thủ nhét 5–6
    # dòng bằng cách giữ chữ căng full-width và NÉN CHIỀU DỌC glyph (平体 ~70–85%).
    # Làm đúng vậy: layout trên canvas ảo cao H/squash, vẽ lớp chữ riêng, cuối cùng
    # resize dọc về H → bề ngang không đổi, chữ chạm 2 mép. Sàn 0.66 — bẹt hơn nữa
    # khó đọc, lúc đó mới co cỡ chữ như cũ. seethru dán ảnh theo toạ độ thật nên
    # không đi đường này (giữ nhánh cũ).
    SQUASH_MIN = 0.66
    hs = heights(sizes)
    need = sum(hs) + gap * (len(lines) - 1) + 2 * margin_y
    squash = 1.0
    if need > H and not a.seethru.strip():
        squash = max(H / need, SQUASH_MIN)
    H2 = round(H / squash) if squash < 1.0 else H
    if squash < 1.0:
        print(f"   平体 squash {squash:.2f} — giữ chữ full-width, nén dọc lớp chữ")

    avail = H2 - 2 * margin_y - gap * (len(lines) - 1)
    for _ in range(60):
        hs = heights(sizes)
        if sum(hs) <= avail:
            break
        sizes = [max(40, round(s * 0.97)) for s in sizes]
    hs = heights(sizes)

    def _idxset(spec):
        if spec.strip() == "all":
            return set(range(len(lines)))
        return {int(i) for i in spec.replace(" ", "").split(",") if i != ""}

    chips, shades, boxes = _idxset(a.chip), _idxset(a.shade), _idxset(a.box)
    seethru = _idxset(a.seethru)
    halos = _idxset(a.halo)
    # --band: bỏ trống/"r" = giữ hành vi cũ (chỉ dòng đòn đỏ) · "0,4"/"all" = theo chỉ số
    if a.band is None:
        band_idx = set()
    elif a.band.strip() == "r":
        band_idx = {i for i, k in enumerate(keys) if k == "r"}
    else:
        band_idx = _idxset(a.band)
    shades -= seethru          # dải che vô nghĩa dưới chữ xuyên hình

    # v5.2 — NÉN KHỐI hay GIÃN ĐỀU.
    # v4 chia đều chỗ dư cho mọi khe → tường chữ phủ kín khung, các dòng rời nhau.
    # Đối thủ nén các dòng SÁT nhau thành một khối đặc rồi neo khối đó (thường lên
    # trên hoặc xuống dưới), chừa phần còn lại cho ảnh. Đó là khác biệt "text nhìn
    # khác" mà user chỉ ra 2026-07-28.
    if a.split > 0:
        # v5.3 — HAI KHỐI: N dòng đầu ép sát mép trên, phần còn lại ép sát mép dưới.
        # Ảnh của mình hay có nhân vật ở GIỮA khung (ảnh gen ra thường thế), không có
        # cột trống nào để dồn chữ như mẫu 五十年ぶり/冷酷CEO → phải kẹp trên-dưới như
        # mẫu 親呼んでみろｗ. Băng giữa còn lại chính là chỗ hở cho mặt.
        extra = 0
        ytop = margin_y
        hbot = sum(hs[a.split:]) + gap * max(0, len(hs) - a.split - 1)
        ybot = H2 - margin_y - hbot
        y0 = ytop
    elif a.block == "fill":
        extra = (avail - sum(hs)) / (len(lines) + 1) if len(lines) else 0
        y0 = margin_y + extra
    else:
        extra = 0
        blk = sum(hs) + gap * (len(lines) - 1)
        free = H2 - blk
        y0 = {"top": margin_y, "center": free / 2,
              "bottom": free - margin_y}[a.block]

    # v6 — lớp chữ riêng khi 平体: mọi thứ của chữ (dải mờ/band/chip/khung/glyph) vẽ
    # lên canvas ảo W×H2 trong suốt, cuối cùng nén dọc về H rồi đè lên ảnh.
    txt_layer = None
    if squash < 1.0:
        txt_layer = Image.new("RGBA", (W, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt_layer)

    # PASS 1 — đo vị trí từng dòng (không vẽ gì)
    lay, y = [], y0
    for idx, (text, key, sz, sw) in enumerate(zip(lines, keys, sizes, sws)):
        if a.split > 0 and idx == a.split:
            y = ybot
        f = font(sz)
        bb = d.textbbox((0, 0), text, font=f)
        pad = round(sw * sz)
        th = bb[3] - bb[1]
        tw = line_width(text, sz)          # có tính giãn chữ, khác textbbox
        ax0, aw = (0, W) if idx in wides else (area_x0, area_w)
        x = (ax0 + a.indent) if a.align == "left" else ax0 + (aw - tw) / 2
        lay.append(dict(text=text, key=key, sz=sz, f=f, bb=bb, pad=pad, th=th, tw=tw, x=x, y=y))
        y += th + 2 * pad + gap + extra

    # PASS 2 — dải ĐEN MỜ ôm sát chữ (kiểu 五十年ぶりの同窓会). Phải vẽ trước chữ và
    # phải qua lớp RGBA riêng, không thì mờ chồng mờ ở chỗ 2 dòng giáp nhau.
    if shades:
        if txt_layer is not None:
            # vẽ thẳng lên lớp chữ trong suốt (thay pixel, không chồng mờ) — nén dọc cùng chữ
            for i in shades:
                L = lay[i]
                px, py = round(L["sz"] * 0.12), round(L["sz"] * 0.05)
                d.rectangle([L["x"] - px, L["y"] - py,
                             L["x"] + L["tw"] + px, L["y"] + L["th"] + 2 * L["pad"] + py],
                            fill=(0, 0, 0, max(0, min(255, a.shade_alpha))))
        else:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            for i in shades:
                L = lay[i]
                px, py = round(L["sz"] * 0.12), round(L["sz"] * 0.05)
                od.rectangle([L["x"] - px, L["y"] - py,
                              L["x"] + L["tw"] + px, L["y"] + L["th"] + 2 * L["pad"] + py],
                             fill=(0, 0, 0, max(0, min(255, a.shade_alpha))))
            img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
            d = ImageDraw.Draw(img)

    # PASS 3 — chip / khung / chữ
    for idx, L in enumerate(lay):
        key, sz, f, bb, pad, th, tw, x, y = (L["key"], L["sz"], L["f"], L["bb"],
                                            L["pad"], L["th"], L["tw"], L["x"], L["y"])
        if idx in band_idx:
            # dải full-width KHUNG (không bó theo --text-w) — mẫu 08 kéo hết mép
            d.rectangle([0, y - 4, W, y + th + 2 * pad + 4], fill=(16, 16, 20))
        cr, cg, cb = COLORS[key]
        if idx in boxes:
            # KHUNG VIỀN màu, không tô — kiểu 「ずっと毎晩欲しい」 viền đỏ ở mẫu 冷酷CEO
            bx, by = round(sz * 0.13), round(sz * 0.06)
            d.rectangle([x - bx, y - by, x + tw + bx, y + th + 2 * pad + by],
                        outline=(cr, cg, cb), width=max(3, round(sz * 0.035)))
        if idx in seethru:
            # v5.4 — RUỘT CHỮ LÀ ẢNH. Ba lớp, thứ tự bắt buộc:
            #   ① viền đen ngoài cùng (tách chữ khỏi mọi nền)
            #   ② viền MÀU (cho chữ vẫn có bản sắc kênh)
            #   ③ lòng chữ = dán ảnh SẠCH qua mask glyph → nhân vật hiện xuyên qua chữ
            # Nhờ vậy chữ không nuốt ảnh: chỗ đậm nhất của khung lại chính là chỗ
            # người xem nhìn thấy cảnh. Đổi lại: chỉ đọc được khi vùng ảnh dưới chữ
            # tương phản thấp — soi 120px trước khi dùng cho dòng đòn.
            yb = y + pad - bb[1]
            draw_line(d, x, yb, L["text"], f, (cr, cg, cb), sz, fat_ratio=0.0,
                      track=TRACK * sz, outline_ratio=0.055,
                      halo=(idx in halos))
            mask = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(mask)
            cx = x
            for chh in L["text"]:
                md.text((cx, yb), chh, font=f, fill=255)
                cx += f.getlength(chh) + TRACK * sz
            fillsrc = img_clean
            if a.seethru_mix > 0:
                # pha màu chữ vào ruột ảnh — 0.4–0.55 là dải vừa thấy cảnh vừa đọc được
                fillsrc = Image.blend(img_clean, Image.new("RGB", (W, H), (cr, cg, cb)),
                                      min(max(a.seethru_mix, 0.0), 1.0))
            img.paste(fillsrc, (0, 0), mask)
            d = ImageDraw.Draw(img)
        elif idx in chips:
            # CHIP: khối màu đặc ôm SÁT chữ (không full-width như --band). Chữ đảo
            # sang đen khi chip sáng (vàng/cyan/trắng) — đúng cách đối thủ làm với
            # 「若い女性は」 nền đỏ chữ trắng và 「朝まで終わらない初夜で」 nền vàng chữ đen.
            ink = BLACK if (0.299 * cr + 0.587 * cg + 0.114 * cb) > 150 else (255, 255, 255)
            cpx, cpy = round(sz * 0.10), round(sz * 0.06)
            d.rectangle([x - cpx, y - cpy, x + tw + cpx, y + th + 2 * pad + cpy],
                        fill=(cr, cg, cb))
            draw_line(d, x, y + pad - bb[1], L["text"], f, ink, sz, fat_ratio=0.0,
                      track=TRACK * sz,
                      outline_ratio=0.0 if ink == BLACK else 0.018)
        else:
            base = COLORS[key]
            tg = hl_tags[idx]
            fills = ([base if t == 0 else (COLORS[a.accent] if t == 1 else COLORS[a.accent2])
                      for t in tg] if any(tg) else base)
            draw_line(d, x, y + pad - bb[1], L["text"], f, fills, sz,
                      halo=(key == "r" or idx in halos), fat_ratio=a.fat,
                      outline_ratio=a.outline)

    # v6 — nén dọc lớp chữ về khung thật rồi đè lên ảnh (平体)
    if txt_layer is not None:
        txt_layer = txt_layer.resize((W, H), Image.LANCZOS)
        img = Image.alpha_composite(img.convert("RGBA"), txt_layer).convert("RGB")

    # ⭐ DẤU NHẬN DIỆN KÊNH (user chốt 2026-08-04). Vẽ SAU lớp chữ + sau khi nén 平体 nên
    # KHÔNG bị co méo, và luôn ở đúng một vị trí/một màu trên mọi video → mắt người xem học
    # được "đây là kênh đó" trong feed. Thứ gánh việc nhận diện là HÌNH/MÀU, không phải chữ
    # (ở 168px chữ tên kênh không đọc nổi và không cần).
    # 3 kiểu (--mark-style): hanko = con dấu đỏ tròn kiểu 判子 · moon = trăng khuyết +
    # vành khung mảnh · bar = vạch dọc mép phải (bản đầu, user chê thô).
    if a.mark:
        d2 = ImageDraw.Draw(img, "RGBA")
        st = a.mark_style
        if st == "bar":
            BAR_W, PADR = 15, 26
            x0 = W - PADR - BAR_W
            for yy in range(H):
                tt = yy / max(H - 1, 1)
                d2.line([(x0, yy), (x0 + BAR_W, yy)],
                        fill=(int(150 + 85 * tt), int(20 + 55 * tt), int(30 + 10 * tt), 255))
            fm = font(38, "yu")
            tw = int(d2.textlength(a.mark, font=fm))
            strip = Image.new("RGBA", (tw + 24, 52), (0, 0, 0, 0))
            ds = ImageDraw.Draw(strip)
            ds.rounded_rectangle([0, 0, tw + 23, 51], radius=10, fill=(12, 12, 14, 224))
            ds.text((12, 6), a.mark, font=fm, fill=(255, 236, 210, 255))
            strip = strip.rotate(90, expand=True)
            img.paste(strip, (x0 - strip.width - 8, int(H * 0.5 - strip.height / 2)), strip)

        elif st == "hanko":
            # Con dấu 判子: vòng tròn đỏ son + 2 chữ dọc bên trong. Rất Nhật, nhận ra ở
            # 168px vì là KHỐI ĐỎ TRÒN, và khớp luôn dòng đòn 「…夫の判子」 của video này.
            R, PAD = 96, 34
            cx, cy = W - PAD - R, H - PAD - R
            lay = Image.new("RGBA", (R * 2 + 10, R * 2 + 10), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            RED = (198, 40, 34, 242)
            dl.ellipse([5, 5, R * 2 + 4, R * 2 + 4], outline=RED, width=10)
            fh = font(int(R * 0.72), "yu")
            chars = (a.mark_short or "朗読")[:2]
            for i, ch in enumerate(chars):
                w_ = dl.textlength(ch, font=fh)
                dl.text((R + 5 - w_ / 2, 18 + i * int(R * 0.82)), ch, font=fh, fill=RED)
            lay = lay.rotate(-4, resample=Image.BICUBIC)
            img.paste(lay, (cx - R - 5, cy - R - 5), lay)

        elif st == "circle":
            # ⭐ KIỂU CHỐT 2 (user chốt 2026-08-04: "làm cho tao 1 cái hình tròn đóng khung
            # vào cho vào góc phải ảnh"). Huy hiệu TRÒN góc trên-phải: vòng ngoài kem +
            # lòng navy đậm + vầng trăng khuyết (真夜中 = nửa đêm).
            # ⚠️ VÌ SAO VỪA khung: dòng 1 chạy ở weight 0.86 → rộng ~1650px, căn giữa nên
            # còn chừa ~135px mỗi bên. Huy hiệu Ø124 + lề 14 lọt đúng dải trống đó, KHÔNG
            # đè chữ. Đổi weights dòng 1 lên gần 1.0 thì sẽ đụng — nhớ kiểm lại.
            D, PAD = 124, 14
            x1, y1 = W - PAD - D, PAD
            cx, cy = x1 + D // 2, y1 + D // 2
            CREAM = (244, 230, 198, 255)
            lay = Image.new("RGBA", (D + 8, D + 8), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.ellipse([4, 4, D + 3, D + 3], fill=(16, 20, 34, 236))      # lòng navy
            dl.ellipse([4, 4, D + 3, D + 3], outline=CREAM, width=5)      # vòng đóng khung
            # trăng khuyết: đĩa kem trừ đi đĩa navy lệch phải
            r = int(D * 0.30)
            mc = (D + 8) // 2
            dl.ellipse([mc - r, mc - r, mc + r, mc + r], fill=CREAM)
            # ⚠️ SỬA 2026-08-06 (user bắt được trên thumbnail T3 video 18): hệ số cũ 0.9 đẩy
            # mép phải đĩa khoét tới x=136 trong khi vành huy hiệu chỉ tới x=127 → đĩa navy
            # TRÀN 9px ra ngoài vành kem, tạo một cái mỏm lệch trông như lỗi render. Có từ
            # 2026-08-04 nên video 16/17 đã lên sóng với nó. 0.42 → mép phải x=118, nằm trong
            # mép trong của vành (x≈122) và giữ nguyên hình trăng khuyết.
            # 🔴 Đổi hằng này thì phải đổi CẢ tools/stamp_mark.py (nhánh cho ảnh phương án B).
            dl.ellipse([mc - r + int(r * 0.72), mc - r - 2, mc + r + int(r * 0.42), mc + r + 2],
                       fill=(16, 20, 34, 236))
            img.paste(lay, (x1 - 4, y1 - 4), lay)

        elif st == "edge":
            # ⭐ KIỂU CHỐT: 2 thanh mảnh đỏ son sát mép TRÊN + DƯỚI, chạy hết bề ngang.
            # Lý do bỏ hanko/moon: khuôn text-wall của kênh PHỦ KÍN khung, không còn góc
            # trống nào → mọi dấu đặt ở góc đều bị dòng đòn đỏ đè lên (đỏ chồng đỏ, trông
            # như lỗi render). Thanh mép nằm NGOÀI vùng chữ nên không bao giờ đụng nhau,
            # và ở 168px nó là "hai vạch đỏ kẹp trên dưới" — nhận ra ngay trong feed.
            # TH=22: ở 168px (cỡ feed) cho ~2px — nhận ra được. Bản 13px chỉ ra ~1px, gần
            # như vô hình đúng ở cỡ mà nó cần phải nhìn thấy.
            TH = 22
            RED = (198, 40, 34, 255)
            d2.rectangle([0, 0, W - 1, TH - 1], fill=RED)
            d2.rectangle([0, H - TH, W - 1, H - 1], fill=RED)
            fm = font(27, "yu")
            tw = int(d2.textlength(a.mark, font=fm))
            d2.rectangle([W - tw - 30, H - TH - 34, W - 1, H - TH], fill=(198, 40, 34, 236))
            d2.text((W - tw - 15, H - TH - 31), a.mark, font=fm, fill=(255, 244, 232, 255))

        elif st == "moon":
            # Vành khung mảnh kem + trăng khuyết góc dưới phải (真夜中 = nửa đêm).
            CR = (243, 226, 190, 236)
            inset, thick = 12, 4
            d2.rectangle([inset, inset, W - inset - 1, H - inset - 1], outline=CR, width=thick)
            r, pad = 50, 46
            cx, cy = W - pad - r, H - pad - r
            m = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
            dm = ImageDraw.Draw(m)
            dm.ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=CR)
            dm.ellipse([int(r * 0.60), -8, r * 2 + 24, r * 2 + 7], fill=(0, 0, 0, 0))
            img.paste(m, (cx - r, cy - r), m)
            fm = font(30, "yu")
            tw = int(d2.textlength(a.mark, font=fm))
            d2.rounded_rectangle([cx - r - 18 - tw - 20, cy - 23, cx - r - 14, cy + 23],
                                 radius=9, fill=(14, 14, 16, 205))
            d2.text((cx - r - 18 - tw - 8, cy - 18), a.mark, font=fm, fill=CR)

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

    # ── GATE ĐỘ BÉO NÉT (2026-08-03) ─────────────────────────────────────────────
    # Mất 4 vòng chỉnh mới ra rằng "trông khác font" = nét bị bơm bởi --fat, không phải
    # sai font. Đo lại ngay sau khi render để khuôn không trôi lần nữa: cắt glyph ĐẦU
    # TIÊN của dòng VÀNG rồi tính tỉ lệ pixel mực trong bbox. Mẫu 08 = 0.383.
    # ⚠️ PHẢI cắt trong ĐÚNG Ô CHỮ của dòng vàng (lấy toạ độ từ `lay`), không dò cả khung:
    # nền sáng có mảng vàng (cửa gỗ, đèn) sẽ lọt vào mặt nạ màu và cho số rác — nhánh T2
    # từng bị báo 0.082 LỆCH oan vì lỗi này. Bỏ qua khi 平体 squash (toạ độ `lay` ở hệ H2).
    _yi = next((i for i, k in enumerate(keys) if k == "y"), None)
    if _yi is not None and squash >= 1.0:
        try:
            import numpy as _np
            _L = lay[_yi]
            _pad = round(_L["sz"] * 0.12)
            _box = (max(0, _L["x"] - _pad), max(0, _L["y"] - _pad),
                    min(W, _L["x"] + _L["tw"] + _pad),
                    min(H, _L["y"] + _L["th"] + 2 * _L["pad"] + _pad))
            _a = _np.asarray(img.convert("RGB").crop(_box), dtype=int)
            _m = (_a[:, :, 0] > 200) & (_a[:, :, 1] > 170) & (_a[:, :, 2] < 130)
            _ys, _xs = _np.where(_m)
            if len(_xs):
                _x0, _y0, _y1 = _xs.min(), _ys.min(), _ys.max()
                _col = _m[_y0:_y1 + 1, _x0:].any(axis=0)
                _run, _end = 0, _x0
                for _i, _v in enumerate(_col):          # cắt tới khe trắng đầu tiên
                    if not _v:
                        _run += 1
                        if _run > 12:
                            _end = _x0 + _i - _run
                            break
                    else:
                        _run = 0
                _g = _m[_y0:_y1 + 1, _x0:_end]
                _ar = _g.shape[1] / max(1, _g.shape[0])
                _hr = _g.shape[0] / max(1, _L["th"])     # cao glyph / cao dòng
                if not (0.72 <= _ar <= 1.30) or not (0.70 <= _hr <= 1.15):
                    # glyph cắt ra không vuông ⇒ nền cùng tông với chữ đã dính vào mặt nạ
                    # (hay gặp ở nhánh nền SÁNG). Nói thẳng là không đo được, đừng báo LỆCH oan.
                    print("   độ đặc nét: KHÔNG ĐO ĐƯỢC (nền cùng tông với chữ) — "
                          "so bằng mắt với bản T1, hoặc đo trên bản nền tối")
                else:
                    _d = _g.mean()
                    if a.font != "yu":
                        # nhánh DÀY (mplus/noto) cố ý nét đậm — 0.60–0.72 là ĐÚNG khuôn của nó,
                        # đừng báo LỆCH. Chỉ nhánh MỎNG mới soi theo mẫu 08.
                        print(f"   độ đặc nét glyph vàng = {_d:.3f}  (nhánh DÀY --font {a.font}, "
                              f"tham chiếu video 14 ≈ 0.71 — không soi theo mẫu 08)")
                    elif a.preset in ("k1", "k2"):
                        # Khuôn 08 là khuôn CŨ (5 dòng thoáng, nền dập đen). k1 nhồi 6 dòng nên
                        # 平体 squash nén dọc → đặc nét tự lên 0.48–0.55; mẫu 毎日スカッと cũng
                        # nét dày hơn 08 rõ rệt. Soi k1/k2 theo dải của 08 là báo LỆCH OAN và
                        # đẩy người sửa đi hạ --fat (đã ở 0, không hạ được nữa).
                        print(f"   độ đặc nét glyph vàng = {_d:.3f}  (preset {a.preset} — KHÔNG soi "
                              "theo mẫu 08; mẫu 毎日スカッと/語り茶屋 nét dày hơn 08. "
                              "Duyệt bằng mắt ở 168px + 120px)")
                    else:
                        _ok = 0.36 <= _d <= 0.42
                        print(f"   độ đặc nét glyph vàng = {_d:.3f} "
                              f"({'ĐẠT' if _ok else 'LỆCH'} khuôn 08 = 0.383, dải 0.36–0.42)"
                              + ("" if _ok else "  ← >0.42 = nét đang bị bơm, hạ --fat"))
        except Exception:
            pass
    print("OK", out)


if __name__ == "__main__":
    main()
