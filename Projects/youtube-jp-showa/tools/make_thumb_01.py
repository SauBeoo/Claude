# -*- coding: utf-8 -*-
"""Thumbnail 3xA/B video 01 kyushoku (T1 baseline / T2 doi 1 bien hinh / T3 doi layout).

Khuon 45+ (audience-45plus $1): chu chinh cuc to, <=3 dong, nen sang, gate 168px.
Khuon nganh 記憶装置: vat khong lo + ten de tai (chua co mat nguoi — ghi nhan trong script).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
ASSET = os.path.join(ROOT, "06_VIDEO", "_asset_test")
OUT = os.path.join(ROOT, "06_VIDEO", "01_kyushoku")
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Black.otf"

W, H = 1280, 720
RED = (206, 32, 41)
CREAM = (255, 244, 214)
DARK = (40, 26, 12)
YELLOW = (255, 205, 40)

# ── BO CHU DUNG CHUNG CHO CA T1/T2/T3 ────────────────────────────────
# ab-3title-3thumb $3 luat 6: bien thu cua T1/T2/T3 la HINH, chu phai GIONG NHAU.
# audience-45plus $1 gate 7: che anh di van biet video noi ve cai gi —
#   (1) VE CAI GI = 給食 (keyword do duoc cao nhat, 460 diem)
#   (2) CHUYEN GI = 消えた10品 (khung mat mat, khuon proof 5.283 v/ngay)
#   (3) HOI NGUOC = どれがあった？
TOP = "昭和の給食"      # banner do, goc tren trai
HERO = "消えた10品"      # dong chinh — to nhat
BOTTOM = "どれがあった？"  # dai duoi
TOP_SZ, HERO_SZ, BOT_SZ = 100, 186, 86


def f(size):
    return ImageFont.truetype(FONT, size)


def text_outline(d, xy, s, font, fill, outline, ow, anchor="la"):
    x, y = xy
    for dx in range(-ow, ow + 1, max(2, ow // 4)):
        for dy in range(-ow, ow + 1, max(2, ow // 4)):
            if dx * dx + dy * dy <= ow * ow:
                d.text((x + dx, y + dy), s, font=font, fill=outline, anchor=anchor)
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def paste_tray(cv, zoom=1.0, cx_frac=0.72):
    """Dan khay kujira (nen trang cat san) vao ben phai canvas."""
    tray = Image.open(os.path.join(ASSET, "kujira_orig.jpg")).convert("RGB")
    th = int(H * 1.04 * zoom)
    tw = int(tray.width * th / tray.height)
    tray = tray.resize((tw, th), Image.LANCZOS)
    # nen trang cua anh -> lam mask de hoa vao nen cream: don gian dan thang,
    # vien trang tren nen cream sang van sach (da duyet mat)
    mask = tray.convert("L").point(lambda v: 0 if v > 246 else 255)
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(2))
    cx = int(W * cx_frac)
    cv.paste(tray, (cx - tw // 2, H - th + 10), mask)


def banner(d, _cv, s, size, xy, pad=18):
    font = f(size)
    bb = d.textbbox((0, 0), s, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    x, y = xy
    d.rectangle([x, y, x + w + pad * 2, y + h + pad * 2 - bb[1] + 6], fill=RED)
    d.text((x + pad, y + pad - bb[1]), s, font=font, fill=(255, 255, 255))


def strip(d, s, size, y, pad=16):
    """Dai do chay tu mep trai, chu trang — dung cho dong duoi."""
    font = f(size)
    bb = d.textbbox((0, 0), s, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.rectangle([0, y, w + pad * 2 + 24, y + h + pad * 2 - bb[1] + 4], fill=RED)
    d.text((24 + pad // 2, y + pad - bb[1]), s, font=font, fill=(255, 255, 255))


def draw_text_block(d, hero_fill, hero_outline):
    """Bo chu DUNG CHUNG — chi doi mau chu cho hop nen tung layout."""
    banner(d, None, TOP, TOP_SZ, (30, 24))
    text_outline(d, (26, 470), HERO, f(HERO_SZ), hero_fill, hero_outline, 16, anchor="ls")
    strip(d, BOTTOM, BOT_SZ, 500)


def make_T(variant):
    cv = Image.new("RGB", (W, H), CREAM)

    if variant in ("T1", "T2"):
        # T1 baseline vs T2 = DUNG MOT bien: do zoom/vi tri cua khay
        if variant == "T1":
            paste_tray(cv, zoom=0.96, cx_frac=0.80)
        else:
            paste_tray(cv, zoom=1.30, cx_frac=0.86)
        d = ImageDraw.Draw(cv)
        draw_text_block(d, RED, (255, 255, 255))
    else:
        # T3 = doi LAYOUT (agepan full-bleed thay khay tren nen cream) — chu giu nguyen
        ag = Image.open(os.path.join(ASSET, "agepan_orig.jpg")).convert("RGB")
        cw = ag.width
        ch = int(cw * H / W)
        top = int(ag.height * 0.28)
        ag = ag.crop((0, top, cw, min(top + ch, ag.height)))
        ag = ag.resize((W, H), Image.LANCZOS)
        cv.paste(ag, (0, 0))
        # scrim sang phia trai de chu do/trang van doc duoc tren anh
        sc = Image.new("L", (W, H), 0)
        ds = ImageDraw.Draw(sc)
        ds.polygon([(0, 0), (int(W * 0.72), 0), (int(W * 0.52), H), (0, H)], fill=210)
        sc = sc.filter(ImageFilter.GaussianBlur(70))
        cv.paste(Image.new("RGB", (W, H), CREAM), (0, 0), sc)
        d = ImageDraw.Draw(cv)
        draw_text_block(d, RED, (255, 255, 255))

    return cv


def main():
    os.makedirs(OUT, exist_ok=True)
    names = {"T1": "thumb_T1_kyushoku.png", "T2": "thumb_T2_kyushoku_zoom.png",
             "T3": "thumb_T3_agepan_oboeteru.png"}
    for v, name in names.items():
        im = make_T(v)
        p = os.path.join(OUT, name)
        im.save(p)
        im.resize((168, 94), Image.LANCZOS).save(p.replace(".png", "_prev168.png"))
        im.resize((120, 68), Image.LANCZOS).save(p.replace(".png", "_prev120.png"))
        print("OK", name)
    # contact sheet 3 ban + 168px de duyet 1 phat
    sheet = Image.new("RGB", (W, H * 3 // 2 + 130), (24, 24, 24))
    for i, name in enumerate(names.values()):
        im = Image.open(os.path.join(OUT, name)).resize((W // 2, H // 2))
        sheet.paste(im, ((i % 2) * W // 2, (i // 2) * H // 2))
        pv = Image.open(os.path.join(OUT, name.replace(".png", "_prev168.png")))
        sheet.paste(pv, (i * 200 + 40, H + 30))
    sheet.save(os.path.join(OUT, "_thumb_sheet.jpg"), quality=90)
    print("OK _thumb_sheet.jpg")


if __name__ == "__main__":
    main()
