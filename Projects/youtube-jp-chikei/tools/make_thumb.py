# -*- coding: utf-8 -*-
"""
make_thumb.py — bộ 3 thumbnail A/B khuôn **C-MAP** cho kênh 地形と地名の日本史.

VÌ SAO KHÔNG ĐI ĐƯỜNG "PROMPT AI BAKE CHỮ" (`ab-3title-3thumb.md` §3 mục 8):
Luật đó sinh ra để chống việc tool vẽ chữ đè lên **ảnh AI** — user cần thấy bộ mặt thật của
thumbnail ngay lúc gen. Ở kênh này nền KHÔNG phải ảnh AI: nó là **bản đồ 国土地理院** mình tự
dựng. Nên vẽ chữ bằng font là đường đúng, và còn tránh được bẫy nát kanji của model
(`media-library.md` §2.9). Nếu bao giờ đổi sang nền ảnh AI thì quay lại luật gốc.

Ba bản A/B đổi ĐÚNG MỘT BIẾN mỗi bản (`ab-3title-3thumb.md` §3):
    T1 baseline : nền hillshade + relief
    T2 đổi hình : nền 空中写真 1961  (chữ + layout GIỮ NGUYÊN)
    T3 đổi layout: nền 断面図, tỉ lệ chữ/hình đảo

Chạy:
    python tools/make_thumb.py 01_shibuya-tani --lat 35.6595 --lon 139.7005 --z 15 \
        --chip 渋谷 --sub "なぜ、ここが「谷」なのか" --hero 谷だった \
        --band "標高差 16m ─ 断面図でわかる" --sect-a 35.672,139.696 --sect-b 35.650,139.708
"""
import io, sys, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsi_map as G   # <- da tu wrap sys.stdout sang utf-8

# ⚠️ KHONG wrap sys.stdout lai o day: gsi_map da wrap khi import, wrap chong len lan 2 thi
# wrapper cu bi gc dong mat buffer => "ValueError: I/O operation on closed file" o print dau tien.

W, H = 1280, 720          # YouTube chuẩn; gate 168px/120px duyệt trên bản thu nhỏ
ROOT = Path(__file__).resolve().parents[1]


def outline_text(d, xy, s, font, fill, anchor="mm", ow=9, ocol=(12, 18, 28)):
    """袋文字 — viền đen dày + chữ màu. Tệp 45+ đọc ở 120px sống nhờ cái viền này."""
    x, y = xy
    for dx in range(-ow, ow + 1, 2):
        for dy in range(-ow, ow + 1, 2):
            if dx * dx + dy * dy <= ow * ow:
                d.text((x + dx, y + dy), s, font=font, fill=ocol + (255,), anchor=anchor)
    d.text(xy, s, font=font, fill=fill + (255,), anchor=anchor)


def fit_width(s, weight, target_w, start=200, floor=60):
    """Co cỡ tới khi lọt target_w. Hero PHẢI rộng ≥55% khung (03_THUMBNAIL §2 gate 1) —
    bề ngang mới là thứ mua được legibility, không phải chiều cao
    (`audience-45plus.md` §6.10 ca 10–12)."""
    sz = start
    while sz > floor:
        f = G.F(weight, sz)
        if f.getbbox(s)[2] - f.getbbox(s)[0] <= target_w:
            return f
        sz -= 2
    return G.F(weight, floor)


def darken(img, k=0.62):
    """Hạ sáng nền để 袋文字 nổi (feedback_thumbnail_bg_brightness: 0,55–0,75)."""
    return Image.eval(img.convert("RGB"), lambda v: int(v * k)).convert("RGBA")


def base_map(lat, lon, z, kind):
    """🔴 NEN THUMBNAIL KHAC NEN SLIDE — hai viec khac nhau, dung bung mot cong thuc.

    Ban dau lay y nguyen bo lop cua slide (`pale`+hillshade+relief, dung z cua slide) va no
    VI PHAM chinh gate 4 cua 03_THUMBNAIL_TITLE_FORMULA.md: `pale` la lop CO CHU, o z=15 thi
    khung day chu nho li ti va KHONG NHIN RA hinh thung lung o 168px. Slide can dia danh de
    nguoi xem doc; thumbnail chi can MOT HINH DANG doc duoc trong 0,3 giay.
    => Thumbnail: BO lop chu, lui 1 muc zoom cho thay tron hinh dang, tang mag cho net.
    """
    if kind == "T1":
        img, _ = G.compose(lat, lon, z - 1, ("relief", "hillshade"), W, H, mag=2.6)
    elif kind == "T2":
        img, _ = G.compose(lat, lon, z, ("air1961",), W, H, mag=2.2)
    else:
        img, _ = G.compose(lat, lon, z - 1, ("relief", "hillshade"), W, H, mag=3.0)
    return img


def draw(kind, out, lat, lon, z, chip, sub, hero, band, sect=None):
    if kind == "T3" and sect:
        tmp = ROOT / "06_VIDEO" / "_thumb_tmp_sect.jpg"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        if G.card_section(tmp, sect[0], sect[1], title="", labels=()) is None:
            print("   [canh bao] DEM rong → T3 quay ve nen ban do")
            img = base_map(lat, lon, z, "T3")
        else:
            img = Image.open(tmp).convert("RGBA").resize((W, H), Image.LANCZOS)
    else:
        img = base_map(lat, lon, z, kind)

    img = darken(img, 0.66 if kind != "T3" else 0.80)
    d = ImageDraw.Draw(img, "RGBA")

    # ① chip 対象 góc trên-trái — nói ngay "bài này về ĐÂU"
    if chip:
        f = G.F("black", 62)
        bb = d.textbbox((0, 0), chip, font=f)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        d.rectangle((0, 22, w + 74, 22 + h + 46), fill=G.PAL["ink"] + (240,))
        d.text((38, 22 + h // 2 + 22), chip, font=f, fill=(255, 255, 255, 255), anchor="lm")

    # ② dòng phụ = câu hỏi なぜ
    if sub:
        f = fit_width(sub, "bold", int(W * 0.86), 78, 44)
        outline_text(d, (W // 2, 188), sub, f, (255, 233, 170), ow=7)

    # ③ HERO — biến quyết định. Rộng ≥55% khung, và tự co để không tràn.
    if kind == "T3":
        hy, hw = int(H * 0.40), 0.80
    else:
        hy, hw = int(H * 0.50), 0.86
    fh = fit_width(hero, "black", int(W * hw), 260, 90)
    outline_text(d, (W // 2, hy), hero, fh, (255, 255, 255), ow=11)
    bb = d.textbbox((W // 2, hy), hero, font=fh, anchor="mm")
    ratio_w = (bb[2] - bb[0]) / W
    ratio_h = (bb[3] - bb[1]) / H

    # ④ dải đỏ đáy — chở CON SỐ + lý do xem
    if band:
        f = fit_width(band, "bold", int(W * 0.90), 62, 34)
        bb2 = d.textbbox((0, 0), band, font=f)
        bh = bb2[3] - bb2[1]
        y0 = H - bh - 78
        d.rectangle((0, y0, W, y0 + bh + 46), fill=G.PAL["hi"] + (238,))
        d.rectangle((0, y0, 16, y0 + bh + 46), fill=(255, 226, 120, 255))
        d.text((W // 2, y0 + bh // 2 + 23), band, font=f, fill=(255, 255, 255, 255), anchor="mm")

    # ⑤ badge nhận diện — góc dưới TRÁI (góc dưới-phải là của timestamp YouTube)
    f = G.F("bold", 30)
    d.rectangle((0, H - 50, 330, H), fill=G.PAL["ink"] + (225,))
    d.text((18, H - 25), "地形と地名の日本史", font=f, fill=(226, 232, 240, 255), anchor="lm")

    img.convert("RGB").save(out, quality=95)
    prev = out.with_name(out.stem + "_prev168.png")
    img.convert("RGB").resize((168, 94), Image.LANCZOS).save(prev)
    prev2 = out.with_name(out.stem + "_prev120.png")
    img.convert("RGB").resize((120, 68), Image.LANCZOS).save(prev2)
    print("   -> %-34s hero rong %.1f%% / cao %.1f%%%s"
          % (out.name, ratio_w * 100, ratio_h * 100,
             "" if ratio_w >= 0.55 else "   🔴 HERO HEP < 55% — rut bot chu hero"))
    return ratio_w


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--z", type=int, default=15)
    ap.add_argument("--chip", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--hero", required=True)
    ap.add_argument("--band", default="")
    ap.add_argument("--sect-a", default=None)
    ap.add_argument("--sect-b", default=None)
    g = ap.parse_args()
    if len(g.hero) > 5:
        print("🔴 HERO %d ky — khuon doi 3–5 ky (03_THUMBNAIL_TITLE_FORMULA.md §2)" % len(g.hero))
    sect = None
    if g.sect_a and g.sect_b:
        sect = (tuple(float(v) for v in g.sect_a.split(",")),
                tuple(float(v) for v in g.sect_b.split(",")))
    o = ROOT / "06_VIDEO" / g.slug
    o.mkdir(parents=True, exist_ok=True)
    for kind in ("T1", "T2", "T3"):
        draw(kind, o / ("thumb_%s_%s.png" % (kind, g.slug)), g.lat, g.lon, g.z,
             g.chip, g.sub, g.hero, g.band, sect)
    print("Xong. DUYET BANG MAT tren *_prev168.png VA *_prev120.png truoc khi giao.")
