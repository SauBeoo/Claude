# -*- coding: utf-8 -*-
r"""
make_vox_codai.py — thẻ hình kiểu VOX (explainer) cho kênh 古代の秘訣.

⛔⛔ LẠC HẬU 2026-08-06 — ĐỪNG DÙNG FILE NÀY NỮA.
    → Dùng `Projects/_media_library/make_vox.py` (tool dùng chung mọi kênh)
    → Quy trình: `.claude/skills/video-vox/SKILL.md` · Gate: `_media_library/check_vox.py`
    Lý do thay: user chấm bản này "không đúng lắm", và đo được vì sao — video 16 dùng
    **39 thẻ `title` trên 62 thẻ vox (63%)** = 39 khung giống hệt nhau (PowerPoint, +
    rủi ro inauthentic content), chỉ **1 thẻ** có ảnh thật + annotation, còn 58 ảnh
    full-khung thì KHÔNG có annotation nào. Bản mới: ảnh thật là NỀN để annotate đè lên,
    12 kind, safe-zone tự suy từ `channels.py`, và gate máy chặn việc lạm dụng thẻ chữ.
    File giữ lại để tra lịch sử (CLAUDE.md: không tự xoá file).

VÌ SAO CÓ TOOL NÀY (user chốt 2026-08-04, script #15 扇風機):
  Kịch bản #15 nói toàn thứ VÔ HÌNH — luồng khí, tầng nhiệt, hiệu ứng ống khói,
  bay hơi — cộng 2 bộ số liệu chính phủ (306/291 người · 54,9%/39,9%). Ảnh thật
  không diễn được mấy thứ đó. Đây đúng chỗ ngôn ngữ hình của Vox mạnh nhất:
  **chữ khổ lớn + sơ đồ + mũi tên tự vẽ + thẻ số đếm lên**.

3 QUYẾT ĐỊNH ĐÃ CHỐT (đừng tự đổi):
  1. **Ngôn ngữ Vox, NHỊP co-dai.** Chuyển động nằm TRONG khung (mũi tên tự vẽ,
     số đếm lên), KHÔNG nằm ở nhịp cắt. Mỗi thẻ giữ ≥10s → vẫn ≤6 lần đổi hình/phút
     theo `.claude/rules/audience-45plus.md` §2. ⛔ Đừng bê tool này sang làm cut nhanh.
  2. **Bảng màu VOX SÁNG** (trắng ngà + vàng + đỏ), KHÔNG phải navy/gold cũ của
     `bake_telop.py` / `make_diagrams_codai.py`. Nhất quán với khuôn thumbnail B1
     (khám kênh 2026-07-30 đã kết án nền tối moody).
  3. Font **Noto Sans JP Black/Bold/Medium** (OFL) ở `Projects/_media_library/fonts/`.

CƠ CHẾ GHÉP VÀO PIPELINE — KHÔNG phải mổ renderer:
  `video_render.py` đã nhận `"video": true` + `clips/clip_XX.mp4`, tự **loop+trim**
  theo độ dài cue. Nên mỗi thẻ Vox xuất ra 1 mp4 **dài 30 giây** = (hoạt hoạ 3–5s)
  + (giữ hình tĩnh tới 30s); renderer cắt đúng cue. Cue của kênh này chưa bao giờ
  quá 30s → không bao giờ bị loop lại đoạn hoạt hoạ.

KHAI BÁO TRONG SLIDES.json
--------------------------
    {"match": "...", "photo": false, "video": true,
     "vox": {"kind": "stat", ...}}

5 KIND:
  stat     — số khổng lồ đếm lên + cột so sánh + nhãn 出典 góc
  room     — mặt cắt căn nhà + mũi tên luồng khí tự vẽ (3 preset: exchange/mix/stack)
  flow     — ẢNH THẬT full khung + mũi tên đỏ tự vẽ + chữ hiện
  title    — thẻ tiêu đề chương, khối vàng trượt vào, chữ khổng lồ
  compare  — 2 panel ✗/○ + kết luận hiện dần

CHẠY
----
    python tools/make_vox_codai.py demo 06_VIDEO/_vox_demo          # 5 thẻ mẫu + sheet
    python tools/make_vox_codai.py 03_SCRIPTS/15_x_SLIDES.json 06_VIDEO/15_x/clips
    python tools/make_vox_codai.py <SLIDES> <clips_dir> --only 7 22 # chỉ vài slot
    python tools/make_vox_codai.py <SLIDES> <clips_dir> --still     # xuất PNG cuối (duyệt nhanh)

🔴 VÙNG CẤM ĐÁY — SỬA 2026-08-05: mốc thật là **y≥600**, KHÔNG phải y≥780.
   Đo trên bản render #16 (co-dai `sub_style: pill`, `sub_size: 26`): phụ đề **2 dòng**
   (mức thường của kênh, SUB_MAXLEN=42) ăn từ khoảng y=600 xuống. Mốc y≥780 cũ chỉ
   đúng cho phụ đề 1 DÒNG.
   ⛔ Hệ quả đã bắt được: `kind=flow` vẽ `body` ở y=682/734 → **bị hộp phụ đề đè, đọc
   không được**. ĐỪNG dùng `body` ở kind=flow trên kênh này; `head` (y=560) thì an toàn.
   Mọi chữ CÓ NGHĨA phải nằm trên y=600.
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
FPS = 15                  # hoạt hoạ 15fps là đủ mượt cho mũi tên/số; renderer chuẩn hoá 30
CLIP_SEC = 30.0           # tổng độ dài clip (anim + giữ hình) — renderer trim theo cue
SAFE_BOTTOM = 780         # dưới mốc này là vùng phụ đề, cấm chữ có nghĩa

FONTS = Path(r"E:\Claude\Projects\_media_library\fonts")
F_BLACK, F_BOLD, F_MED = (FONTS / f"NotoSansJP-{w}.otf" for w in ("Black", "Bold", "Medium"))

# ---- bảng màu VOX SÁNG (chốt 2026-08-04) ----
BG      = (247, 246, 242)     # trắng ngà ấm
PANEL   = (255, 255, 255)
INK     = (22, 24, 29)        # gần đen, không đen tuyệt đối
MUTED   = (138, 140, 149)
YELLOW  = (255, 210, 0)       # accent chính
RED     = (224, 58, 58)       # mũi tên / cảnh báo
BLUE    = (58, 122, 224)      # khí lạnh / vào
HOT     = (232, 96, 72)       # tầng nhiệt


def _f(path, size):
    return ImageFont.truetype(str(path), size)


def _tw(d, xy, s, font, fill, anchor="la", stroke=0, sfill=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=sfill or BG)


def ease(t):
    """ease-out cubic — chuyển động Vox không bao giờ tuyến tính."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _fit(text, font_path, max_w, start, min_size=40):
    """Giảm cỡ tới khi vừa chiều rộng — chữ khổ Vox hay tràn khung."""
    s = start
    while s > min_size:
        f = _f(font_path, s)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= max_w:
            return f
        s -= 4
    return _f(font_path, min_size)


# ══════════════════════════════════════════════════════════════════ primitives

def arrow(d, pts, color=RED, width=14, head=34, prog=1.0, dashed=False):
    """Vẽ mũi tên theo polyline, chỉ vẽ `prog` phần đầu (0..1) → hiệu ứng tự vẽ."""
    if prog <= 0 or len(pts) < 2:
        return
    seg = [(math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    total = sum(seg) or 1
    want = total * prog
    path, acc = [pts[0]], 0.0
    for i, L in enumerate(seg):
        if acc + L <= want:
            path.append(pts[i + 1]); acc += L
        else:
            r = (want - acc) / L
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r
            y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r
            path.append((x, y)); break
    if len(path) < 2:
        return
    if dashed:
        for i in range(len(path) - 1):
            if i % 2 == 0:
                d.line([path[i], path[i + 1]], fill=color, width=width)
    else:
        d.line(path, fill=color, width=width, joint="curve")
    # đầu mũi — chỉ hiện khi gần xong để không "bay" giữa đường
    if prog > 0.92:
        (x0, y0), (x1, y1) = path[-2], path[-1]
        a = math.atan2(y1 - y0, x1 - x0)
        d.polygon([(x1, y1),
                   (x1 - head * math.cos(a - .45), y1 - head * math.sin(a - .45)),
                   (x1 - head * math.cos(a + .45), y1 - head * math.sin(a + .45))], fill=color)


def curve(p0, p1, bend=0.28, n=26):
    """Polyline cong (quadratic) — mũi tên Vox luôn cong, không thẳng cứng."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    cx, cy = mx - dy * bend, my + dx * bend
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t * t * p1[1])
            for t in [i / n for i in range(n + 1)]]


def src_label(d, text):
    """Nhãn 出典 — chữ ký minh bạch kiểu Vox.
    ⚠️ Đặt ở y=SAFE_BOTTOM-6, KHÔNG phải đáy khung: đáy là vùng phụ đề burn-in
    (bắt được khi duyệt sheet demo đầu tiên — bản cũ để y=H-44 thì phụ đề đè mất).
    Đặt TRÁI vì góc dưới PHẢI là của YouTube (timestamp thời lượng)."""
    if not text:
        return
    _tw(d, (1800, 132), f"出典：{text}", _f(F_MED, 27), MUTED, anchor="rs")


def kicker(d, text, y=118):
    """Dòng dẫn nhỏ + gạch vàng dưới — mở đầu mọi thẻ Vox."""
    if not text:
        return
    f = _f(F_BOLD, 34)
    _tw(d, (120, y), text, f, INK)
    w = f.getbbox(text)[2]
    d.rectangle([120, y + 50, 120 + max(w, 90), y + 58], fill=YELLOW)


# ══════════════════════════════════════════════════════════════════ kind: stat

def k_stat(v, t):
    """Số khổng lồ đếm lên + (tuỳ chọn) cột so sánh. t = giây kể từ đầu clip."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    kicker(d, v.get("kicker", ""))

    big = str(v["big"])
    p = ease(t / v.get("count_sec", 1.8))
    # ⚠️ NĂM không được có dấu phẩy hàng nghìn (bắt được ở vòng duyệt sheet: 1894 →
    # in ra 「1,894」). Tự nhận 4 chữ số trong 1000–2999 là năm; ghi đè bằng "comma".
    digits = big.replace(",", "")
    is_year = digits.isdigit() and len(digits) == 4 and 1000 <= int(digits) <= 2999
    use_comma = v.get("comma", not is_year)
    try:                                  # số thì đếm lên; chữ thì hiện thẳng
        n = int(round(int(digits) * p))
        shown = f"{n:,}" if use_comma else str(n)
    except ValueError:
        shown, p = big, 1.0
    # ⚠️ Số khổ Vox có bbox cao hơn size danh nghĩa → phải đo bbox thật để đặt
    # sub/note, đừng nhân hệ số theo size (bản đầu nhân 1.02 → sub bị số đè lên).
    fb = _fit(shown + v.get("unit", ""), F_BLACK, 1120, 272)
    y = 234
    _tw(d, (120, y), shown, fb, INK)
    bb = fb.getbbox(shown)
    wnum, hnum = bb[2] - bb[0], bb[3]
    if v.get("unit"):
        _tw(d, (120 + wnum + 22, y + hnum - 96), v["unit"], _f(F_BOLD, 92), INK)
    if v.get("sub"):
        _tw(d, (124, y + hnum + 44), v["sub"], _f(F_MED, 48), MUTED)

    bars = v.get("bars") or []
    if bars:
        bx, by, bw = 1120, 270, 640
        mx = max(b[1] for b in bars) or 1
        for i, (lab, val) in enumerate(bars):
            yy = by + i * 136
            bp = ease((t - 1.4 - i * 0.35) / 1.1)
            L = int(bw * (val / mx) * bp)
            col = RED if i == 0 else BLUE
            d.rectangle([bx, yy, bx + L, yy + 74], fill=col)
            _tw(d, (bx, yy - 14), lab, _f(F_BOLD, 38), INK, anchor="ls")
            if bp > 0.98:
                # ⚠️ Nhãn số phải KẸP trong khung: bản đầu đặt cứng bx+L+22 → 50,173
                # bị cắt thành 「50,17」. Hết chỗ bên ngoài thì vẽ TRONG cột, chữ trắng.
                fv = _f(F_BLACK, 56)
                s = f"{val:,}"
                wv = fv.getbbox(s)[2] - fv.getbbox(s)[0]
                if bx + L + 22 + wv <= W - 120:
                    _tw(d, (bx + L + 22, yy + 37), s, fv, col, anchor="lm")
                else:
                    _tw(d, (bx + L - 20, yy + 37), s, fv, (255, 255, 255), anchor="rm",
                        stroke=0, sfill=col)
    if v.get("note") and t > 3.0:
        _tw(d, (120, 690), v["note"], _fit(v["note"], F_BOLD, 1680, 60), INK)
    src_label(d, v.get("source"))
    return im


# ══════════════════════════════════════════════════════════════════ kind: room

def _house(d, floors=1):
    """Mặt cắt căn nhà — trắng trên nền ngà, nét dày kiểu Vox.
    ⚠️ Tỉ lệ đã sửa sau khi duyệt sheet demo đầu: bản cũ (yt=330..yb=700) rộng 1320
    × cao 370 → trông như hộp bánh, không ra căn nhà. Nay cao ~390–460."""
    # ⚠️ floors="tall" (preset mix) = nhà HẸP + CAO. Lý do: mix nói về tầng nhiệt theo
    # CHIỀU DỌC, mà nhà rộng-dẹt thì mũi tên đi lên trông gần như NẰM NGANG — bắt được
    # ở vòng duyệt sheet thứ hai. Đừng gộp lại thành một tỉ lệ chung.
    if floors == "tall":
        x0, x1, yt, mid, yb = 520, 1400, 196, None, 650
        floors = 1
    elif floors == 2:
        x0, x1, yt, mid, yb = 320, 1600, 196, 430, 660
    else:
        x0, x1, yt, mid, yb = 320, 1600, 250, None, 620
    d.rectangle([x0, yt, x1, yb], fill=PANEL, outline=INK, width=9)
    d.rectangle([x0 - 70, yb, x1 + 70, yb + 24], fill=INK)          # nền đất
    if floors == 2:
        d.line([x0, mid, x1, mid], fill=INK, width=8)               # sàn tầng 2
        for i in range(6):                                          # cầu thang
            xs = 900 + i * 26
            d.line([xs, yb - 18 - i * 34, xs + 66, yb - 18 - i * 34], fill=INK, width=7)
        d.line([900, yb - 18, 1056, mid], fill=(206, 206, 200), width=5)
    return x0, x1, yt, yb


def _window(d, x, y, wide=True, side="left"):
    w, h = (30, 150) if wide else (30, 76)
    d.rectangle([x - w // 2, y - h // 2, x + w // 2, y + h // 2], fill=BG, outline=INK, width=7)


def _fan(d, cx, cy, s=52, face="right"):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=PANEL, outline=INK, width=8)
    for k in range(3):
        a = k * 2.094 + (0 if face == "right" else 0.5)
        d.line([cx, cy, cx + s * 0.78 * math.cos(a), cy + s * 0.78 * math.sin(a)],
               fill=INK, width=7)
    d.line([cx, cy + s, cx, cy + s + 30], fill=INK, width=9)
    d.line([cx - 30, cy + s + 30, cx + 30, cy + s + 30], fill=INK, width=9)


def k_room(v, t):
    """Mặt cắt nhà + luồng khí. preset: exchange (2 cửa sổ) / mix (tầng nhiệt) / stack (ống khói)."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    kicker(d, v.get("kicker", ""))
    preset = v.get("preset", "exchange")
    floors = 2 if preset == "stack" else ("tall" if preset == "mix" else 1)
    x0, x1, yt, yb = _house(d, floors)

    # tầng nhiệt đỏ dưới trần
    if v.get("heat", True):
        band = Image.new("RGB", (x1 - x0 - 18, 150), HOT)
        m = Image.linear_gradient("L").resize((x1 - x0 - 18, 150))
        im.paste(band, (x0 + 9, yt + 9), m.transpose(Image.FLIP_TOP_BOTTOM).point(lambda p: p // 2))
        d = ImageDraw.Draw(im)
        _tw(d, (x0 + 34, yt + 30), "熱", _f(F_BLACK, 62), (255, 255, 255))

    # ⚠️ Nhãn trong sơ đồ phải nằm ĐÚNG chỗ nó nói tới và KHÔNG đè nhau/đè mũi tên
    # (bản đầu: 「かき混ぜる」 đè lên cái quạt · 「足元は涼しい」 đặt trên trần ·
    #  「階段が煙突になる」 đè lên dòng head). Toạ độ dưới đây đã duyệt bằng mắt.
    if preset == "exchange":
        _window(d, x1, 420, True, "right")
        _window(d, x0, 540, False, "left")
        _fan(d, x1 - 210, 450, 50, "right")
        arrow(d, curve((x1 - 130, 432), (x1 + 190, 366), .16), RED, 16, 38, ease(t / 2.2))
        arrow(d, curve((x0 - 180, 546), (x0 + 250, 574), -.12), BLUE, 13, 32, ease((t - 1.3) / 2.0))
        if t > 2.6:
            _tw(d, (x1 + 130, 300), "熱が出る", _f(F_BLACK, 52), RED, anchor="ma")
            _tw(d, (x0 - 110, 640), "涼しい空気", _f(F_BLACK, 44), BLUE, anchor="ma")
    elif preset == "mix":
        cx = (x0 + x1) // 2
        _fan(d, cx, yb - 84, 50, "up")
        for i, dx in enumerate((-210, 0, 210)):
            arrow(d, curve((cx, yb - 142), (cx + dx, yt + 176), .07 * (1 if dx >= 0 else -1)),
                  RED, 13, 30, ease((t - 0.5 - i * 0.3) / 1.6))
        if t > 2.4:
            _tw(d, (cx, yt + 44), "かき混ぜる", _f(F_BLACK, 54), (255, 255, 255), anchor="ma")
            _tw(d, (250, 300), "頭の上は\n熱い", _f(F_BLACK, 50), HOT, anchor="ma")
            _tw(d, (250, 560), "足元は\n涼しい", _f(F_BLACK, 50), BLUE, anchor="ma")
    else:  # stack — 2 tầng, cầu thang làm ống khói
        _window(d, x0, yb - 70, False, "left")
        _window(d, x1, 286, True, "right")
        arrow(d, curve((x0 - 180, yb - 64), (880, yb - 40), -.09), BLUE, 13, 32, ease(t / 1.8))
        arrow(d, curve((884, yb - 60), (1090, 400), .10), RED, 15, 0, ease((t - 1.0) / 1.5))
        arrow(d, curve((1090, 400), (x1 + 190, 258), .12), RED, 16, 38, ease((t - 2.0) / 1.8))
        if t > 3.2:
            _tw(d, (1330, 500), "階段が煙突になる", _f(F_BLACK, 50), INK, anchor="ma")

    if v.get("head") and t > 0.4:
        _tw(d, (120, 690), v["head"], _fit(v["head"], F_BLACK, 1680, 76), INK)
    src_label(d, v.get("source"))
    return im


# ══════════════════════════════════════════════════════════════════ kind: flow

def k_flow(v, t, bg=None):
    """ẢNH THẬT full khung + dải tối nhẹ + mũi tên đỏ tự vẽ + chữ hiện."""
    if bg is None:
        im = Image.new("RGB", (W, H), (222, 222, 216))
    else:
        im = bg.copy()
    # dải sáng phía dưới để chữ đọc được trên ảnh (Vox dùng scrim, không dùng nền đục)
    scrim = Image.new("L", (W, H), 0)
    ImageDraw.Draw(scrim).rectangle([0, 470, W, H], fill=200)
    im = Image.composite(Image.new("RGB", (W, H), (250, 250, 246)), im,
                         scrim.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(im)
    for i, a in enumerate(v.get("arrows", [])):
        p0, p1 = (a[0], a[1]), (a[2], a[3])
        arrow(d, curve(p0, p1, a[4] if len(a) > 4 else .22), RED, 15, 36,
              ease((t - 0.6 - i * 0.5) / 1.8))
    if v.get("head"):
        _tw(d, (120, 560), v["head"], _fit(v["head"], F_BLACK, 1680, 84), INK)
    if v.get("body") and t > 1.6:
        for i, ln in enumerate(v["body"][:2]):
            _tw(d, (124, 682 + i * 52), ln, _f(F_MED, 44), (60, 62, 70))
    kicker(d, v.get("kicker", ""))
    src_label(d, v.get("source"))
    return im


# ══════════════════════════════════════════════════════════════════ kind: title

def k_title(v, t):
    """Thẻ tiêu đề chương — khối vàng trượt vào, chữ khổng lồ."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    p = ease(t / 0.9)
    d.rectangle([0, 300, int(1560 * p), 560], fill=YELLOW)
    if v.get("num"):
        _tw(d, (120, 236), v["num"], _f(F_BLACK, 96), INK)
    if t > 0.55:
        f = _fit(v["title"], F_BLACK, 1400, 108)
        _tw(d, (120, 430 - f.size * 0.5), v["title"], f, INK)
    if v.get("sub") and t > 1.1:
        _tw(d, (124, 620), v["sub"], _fit(v["sub"], F_BOLD, 1600, 52), (70, 72, 80))
    src_label(d, v.get("source"))
    return im


# ══════════════════════════════════════════════════════════════════ kind: compare

def k_compare(v, t):
    """2 panel ✗/○ — kết luận mỗi bên hiện dần."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    kicker(d, v.get("kicker", ""))
    if v.get("title"):
        _tw(d, (120, 200), v["title"], _fit(v["title"], F_BLACK, 1680, 78), INK)
    for i, side in enumerate(("left", "right")):
        s = v.get(side) or {}
        px = 120 + i * 880
        pw = 800
        d.rounded_rectangle([px, 340, px + pw, 700], 28, fill=PANEL, outline=INK, width=7)
        bad = s.get("mark", "x") == "x"
        col = RED if bad else (46, 160, 96)
        if t > 0.4 + i * 0.4:
            cx, cy = px + 92, 428
            if bad:
                d.line([cx - 34, cy - 34, cx + 34, cy + 34], fill=col, width=15)
                d.line([cx + 34, cy - 34, cx - 34, cy + 34], fill=col, width=15)
            else:
                d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=col, width=15)
        _tw(d, (px + 168, 400), s.get("label", ""), _fit(s.get("label", ""), F_BOLD, 580, 52), INK)
        if t > 1.5 + i * 0.4 and s.get("verdict"):
            f = _fit(s["verdict"], F_BLACK, pw - 80, 62)
            _tw(d, (px + 40, 560), s["verdict"], f, col)
    if v.get("note") and t > 2.6:
        _tw(d, (120, SAFE_BOTTOM - 56), v["note"], _fit(v["note"], F_BOLD, 1680, 56), INK)
    src_label(d, v.get("source"))
    return im


KINDS = {"stat": k_stat, "room": k_room, "flow": k_flow, "title": k_title, "compare": k_compare}


# ══════════════════════════════════════════════════════════════════ build clip

def build(v, out_mp4, bg_img=None, still_only=False):
    """Render frames cho cửa sổ hoạt hoạ rồi ghép: anim + giữ hình tĩnh tới CLIP_SEC."""
    kind = v.get("kind", "stat")
    fn = KINDS[kind]
    anim = float(v.get("anim_sec", 4.0))
    tmp = out_mp4.parent / f"_tmp_{out_mp4.stem}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    def frame(t):
        return fn(v, t, bg_img) if kind == "flow" else fn(v, t)

    last = frame(anim)
    if still_only:
        p = out_mp4.with_suffix(".png")
        last.save(p, quality=95)
        shutil.rmtree(tmp)
        return p

    n = int(anim * FPS)
    for i in range(n):
        frame(i / FPS).save(tmp / f"f{i:04d}.png")
    last.save(tmp / f"f{n:04d}.png")

    hold = out_mp4.parent / f"_hold_{out_mp4.stem}.png"
    last.save(hold)
    a = tmp.parent / f"_a_{out_mp4.stem}.mp4"
    b = tmp.parent / f"_b_{out_mp4.stem}.mp4"
    q = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-r", "30"]
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"),
                    *q, str(a)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-t",
                    f"{max(1.0, CLIP_SEC - anim):.2f}", "-i", str(hold), *q, str(b)],
                   check=True, capture_output=True)
    lst = tmp.parent / f"_cat_{out_mp4.stem}.txt"
    lst.write_text(f"file '{a.name}'\nfile '{b.name}'\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out_mp4)], check=True, capture_output=True)
    for p in (a, b, lst, hold):
        p.unlink(missing_ok=True)
    shutil.rmtree(tmp)
    return out_mp4


def _load_bg(img_dir, idx):
    if not img_dir:
        return None
    for ext in (".jpg", ".jpeg", ".png"):
        for cand in (img_dir / f"slide_{idx:02d}{ext}", img_dir / "_raw" / f"slide_{idx:02d}{ext}"):
            if cand.exists():
                im = Image.open(cand).convert("RGB")
                sc = max(W / im.width, H / im.height)
                im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
                return im.crop(((im.width - W) // 2, (im.height - H) // 2,
                                (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    return None


DEMO = [
    {"kind": "stat", "kicker": "令和6年夏・東京23区", "big": "306", "unit": "人",
     "sub": "暑さで亡くなった方", "bars": [["屋内", 291], ["屋外", 15]],
     "note": "亡くなった方の95％は、家の中だった", "source": "東京都監察医務院"},
    {"kind": "room", "preset": "exchange", "kicker": "一つ目・窓は二つ",
     "head": "冷やすのではなく、入れ替える"},
    {"kind": "room", "preset": "mix", "kicker": "二つ目・部屋に夏が二つ",
     "head": "天井にたまった熱を、かき混ぜて落とす"},
    {"kind": "room", "preset": "stack", "kicker": "五つ目・扇風機を止める",
     "head": "羽根も、電気も、いらない"},
    {"kind": "title", "num": "五つ目", "title": "ここで、扇風機を止める",
     "sub": "いちばんよく効く置き方は、置かないことだった"},
    # ⚠️ compare CHỈ có nghĩa khi hai bên ĐỐI NHAU (✗ vs ○). Demo đầu đặt ○ cả hai
    # → thẻ mất hết tương phản, nhìn ra ngay ở sheet. Đừng lặp lại.
    {"kind": "compare", "kicker": "同じ1台の扇風機", "title": "向きだけで、仕事が変わる",
     "left": {"label": "体に向ける", "mark": "x", "verdict": "部屋の熱はそのまま"},
     "right": {"label": "窓の外へ向ける", "mark": "o", "verdict": "熱が出ていく"},
     "note": "乾かしているのは、部屋ではなく、あなた"},
]


def sheet(paths, out):
    cols, tw = 3, 620
    rows = (len(paths) + cols - 1) // cols
    th = int(tw * H / W)
    sh = Image.new("RGB", (cols * tw, rows * th), (30, 30, 32))
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        sh.paste(im, ((i % cols) * tw, (i // cols) * th))
    sh.save(out, quality=92)
    print(f"[SHEET] {out}")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    still = "--still" in a
    a = [x for x in a if x != "--still"]

    if a[0] == "demo":
        out = Path(a[1]); out.mkdir(parents=True, exist_ok=True)
        outs = []
        for i, v in enumerate(DEMO):
            p = build(v, out / f"vox_{i:02d}.mp4", still_only=True)
            outs.append(p); print(f"[{v['kind']:8s}] {p.name}")
        sheet(outs, out / "_vox_sheet.jpg")
        if "--mp4" in sys.argv:
            for i, v in enumerate(DEMO):
                print("[mp4]", build(v, out / f"vox_{i:02d}.mp4").name)
        return

    slides = Path(a[0]); clips = Path(a[1]); clips.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in a[2:] if x.isdigit()} or None
    img_dir = clips.parent / "slides_img"
    cfg = json.loads(slides.read_text(encoding="utf-8"))
    n = 0
    for i, e in enumerate(cfg):
        v = e.get("vox")
        if not v or (only and i not in only):
            continue
        bg = _load_bg(img_dir, i) if v.get("kind") == "flow" else None
        if v.get("kind") == "flow" and bg is None:
            print(f"  ⚠ slot {i:02d} kind=flow nhưng thiếu slides_img/slide_{i:02d}.* → nền phẳng")
        p = build(v, clips / f"clip_{i:02d}.mp4", bg, still_only=still)
        print(f"  [{i:02d}] {v.get('kind'):8s} → {p.name}")
        n += 1
    print(f"— xuất {n} thẻ vox —")
    if n and still:
        sheet(sorted(clips.glob("clip_*.png")), clips / "_vox_sheet.jpg")


if __name__ == "__main__":
    main()
