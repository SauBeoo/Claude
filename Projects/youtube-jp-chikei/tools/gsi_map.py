# -*- coding: utf-8 -*-
"""
gsi_map.py — LỚP HÌNH LÕI của kênh 地形と地名の日本史.

VÌ SAO CÓ FILE NÀY:
Ngách 地形・地名・河川史 thắng bằng BẢN ĐỒ, không bằng ảnh minh hoạ. Đối thủ mạnh nhất
(楽しく地理を学べるチャンネル 72K view/8 phút, ソラからトラベル) quay tay Google Earth —
chậm, không chồng được lớp chuyên đề, và KHÔNG có dữ liệu địa hình thật. Tool này lấy thẳng
地理院タイル của 国土地理院: bản đồ nền, 陰影起伏図, 標高DEM, 治水地形分類図, 土地条件図,
ảnh hàng không 1961. Đây là moat của kênh — copy được nhưng phải biết code.

⚖️ LICENSE (bắt buộc, đừng bỏ): 地理院タイル dùng được cả thương mại, điều kiện là GHI 出典.
    Mọi ảnh tool xuất ra đều TỰ đóng dòng 出典 ở góc — không có tham số nào tắt.
    Ảnh hàng không cũ cũng là 国土地理院, ghi kèm năm chụp.
    Quy định: https://maps.gsi.go.jp/development/ichiran.html

⚠️ LỄ PHÉP VỚI SERVER: mọi tile được CACHE xuống `_tilecache/`. Đừng bỏ cache — một video
    20 ô hình = vài nghìn tile; kéo lại mỗi lần render là tự đi spam 国土地理院.

CLI:
    python tools/gsi_map.py demo
    python tools/gsi_map.py map  --lat 35.658 --lon 139.701 --z 15 --layers pale,hillshade
    python tools/gsi_map.py then --lat 35.658 --lon 139.701 --z 16
    python tools/gsi_map.py sect --a 35.66,139.69 --b 35.65,139.71
"""
import io, re, sys, math, time, argparse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "_tilecache"
FONTS = Path(r"E:\Claude\Projects\_media_library\fonts")
W, H = 1920, 1080
# Do phong mac dinh cua lop ban do — xem giai thich trong mosaic().
MAG = 2.0
UA = "chikei-nihonshi/1.0 (educational youtube channel)"

# ── tầng tile: (url, đuôi, zoom min, zoom max, tên trong dòng 出典) ──────────────
LAYERS = {
    "std":       ("https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",           "png",  5, 18, "標準地図"),
    "pale":      ("https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",          "png",  5, 18, "淡色地図"),
    "blank":     ("https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png",         "png",  5, 14, "白地図"),
    "hillshade": ("https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png",  "png",  2, 16, "陰影起伏図"),
    "relief":    ("https://cyberjapandata.gsi.go.jp/xyz/relief/{z}/{x}/{y}.png",        "png",  5, 15, "色別標高図"),
    "slope":     ("https://cyberjapandata.gsi.go.jp/xyz/slopemap/{z}/{x}/{y}.png",      "png",  3, 15, "傾斜量図"),
    "photo":     ("https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg", "jpg",  2, 18, "写真"),
    "chisui":    ("https://cyberjapandata.gsi.go.jp/xyz/lcmfc2/{z}/{x}/{y}.png",        "png", 14, 16, "治水地形分類図"),
    "condition": ("https://cyberjapandata.gsi.go.jp/xyz/lcm25k_2012/{z}/{x}/{y}.png",   "png", 14, 16, "土地条件図"),
    "air1961":   ("https://cyberjapandata.gsi.go.jp/xyz/gazo1/{z}/{x}/{y}.jpg",         "jpg", 14, 17, "空中写真(1961〜1964年)"),
    "air1974":   ("https://cyberjapandata.gsi.go.jp/xyz/gazo4/{z}/{x}/{y}.jpg",         "jpg", 14, 17, "空中写真(1974〜1978年)"),
    "airold10":  ("https://cyberjapandata.gsi.go.jp/xyz/ort_old10/{z}/{x}/{y}.png",     "png", 14, 17, "空中写真(1961〜1969年)"),
    "dem":       ("https://cyberjapandata.gsi.go.jp/xyz/dem_png/{z}/{x}/{y}.png",       "png",  1, 14, "標高タイル"),
}
# Lop phu duoi nguong nay coi nhu KHONG CO DU LIEU o vung do — xem compose().
COVER_MIN = 0.15
ALPHA = {"hillshade": 0.42, "relief": 0.50, "slope": 0.45, "chisui": 0.62, "condition": 0.62}

PAL = {"ink": (26, 38, 56), "paper": (243, 238, 228), "line": (198, 186, 166),
       "hi": (206, 58, 45), "hi2": (232, 168, 44), "water": (42, 104, 158), "sub": (110, 120, 136)}


def F(weight, size):
    f = {"black": "NotoSansJP-Black.otf", "bold": "NotoSansJP-Bold.otf",
         "med": "NotoSansJP-Medium.otf"}[weight]
    return ImageFont.truetype(str(FONTS / f), int(size))


# ── toán tile ──────────────────────────────────────────────────────────────────
def deg2px(lat, lon, z):
    n = 256 * 2 ** z
    x = (lon + 180.0) / 360.0 * n
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return x, y


def px2deg(x, y, z):
    n = 256 * 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon


def hav(p, q):
    R = 6371000.0
    dl, dp = math.radians(q[1] - p[1]), math.radians(q[0] - p[0])
    x = (math.sin(dp / 2) ** 2
         + math.cos(math.radians(p[0])) * math.cos(math.radians(q[0])) * math.sin(dl / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(x))


def fetch(layer, z, x, y, retry=3):
    url_t, ext, zmin, zmax, _ = LAYERS[layer]
    z = max(zmin, min(zmax, z))
    n = 2 ** z
    if not (0 <= y < n):
        return None
    x %= n
    p = CACHE / layer / str(z) / str(x) / ("%d.%s" % (y, ext))
    if p.exists():
        try:
            return Image.open(p).convert("RGBA")
        except Exception:
            p.unlink(missing_ok=True)
    url = url_t.format(z=z, x=x, y=y)
    for i in range(retry):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            d = urllib.request.urlopen(req, timeout=20).read()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(d)
            return Image.open(io.BytesIO(d)).convert("RGBA")
        except urllib.error.HTTPError as e:
            if e.code == 404:          # tile trống là chuyện thường ở lớp chuyên đề
                return None
            time.sleep(0.4 * (i + 1))
        except Exception:
            time.sleep(0.4 * (i + 1))
    return None


def mosaic(layer, lat, lon, z, w=W, h=H, mag=MAG):
    """Ghép tile thành ảnh w×h, tâm (lat, lon).

    `mag` = ĐỘ PHÓNG. mag=2 nghĩa là chỉ lấy w/2 × h/2 pixel bản đồ rồi phóng lên full
    khung ⇒ **chữ trên bản đồ to gấp đôi**. Đây KHÔNG phải tinh chỉnh thẩm mỹ: bản duyệt
    đầu tiên (mag=1, z=15) có chữ địa danh ~11px trên khung 1920 — đọc không nổi trên TV,
    vi phạm thẳng `audience-45plus.md` §1. Tile 256px phóng 2× bằng LANCZOS vẫn mượt.
    Lớp không có mức zoom đó thì `scale` phóng bù thêm.
    """
    _, _, zmin, zmax, _ = LAYERS[layer]
    zz = max(zmin, min(zmax, z))
    scale = 2 ** (z - zz) * mag
    cw, ch = int(math.ceil(w / scale)), int(math.ceil(h / scale))
    cx, cy = deg2px(lat, lon, zz)
    x0, y0 = cx - cw / 2, cy - ch / 2
    tx0, ty0 = int(math.floor(x0 / 256)), int(math.floor(y0 / 256))
    tx1, ty1 = int(math.floor((x0 + cw) / 256)), int(math.floor((y0 + ch) / 256))
    canvas = Image.new("RGBA", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), (0, 0, 0, 0))
    got = 0
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            im = fetch(layer, zz, tx, ty)
            if im is None:
                continue
            got += 1
            canvas.paste(im, ((tx - tx0) * 256, (ty - ty0) * 256))
    ox, oy = int(x0 - tx0 * 256), int(y0 - ty0 * 256)
    out = canvas.crop((ox, oy, ox + cw, oy + ch))
    if scale != 1:
        out = out.resize((w, h), Image.LANCZOS)
    # 🔴 "Co tile" KHONG co nghia la "co du lieu". Cac lop chuyen de (chisui / condition /
    # anh hang khong) chi phu MOT PHAN lanh tho — ngoai vung phu, server van tra 200 voi
    # tile TRONG SUOT. Dem so tile khong bat duoc cai do (da dinh that: the 治水地形分類図
    # cua Shibuya chi co mau o mep phai khung, tool bao OK). Nen tra ve them TI LE PHU do
    # tu alpha that.
    al = out.getchannel("A")
    cover = sum(i * c for i, c in enumerate(al.histogram())) / (255.0 * al.width * al.height)
    return out, got, cover


def compose(lat, lon, z, layers=("pale", "hillshade"), w=W, h=H, mag=MAG):
    base = Image.new("RGBA", (w, h), PAL["paper"] + (255,))
    used = []
    for i, ly in enumerate(layers):
        im, got, cover = mosaic(ly, lat, lon, z, w, h, mag)
        if got == 0:
            print("   [BO QUA] lop '%s': khong co tile o z=%d" % (ly, z))
            continue
        if i > 0 and cover < COVER_MIN:
            # Lop phu ma gan nhu trong suot = VUNG NAY KHONG CO DU LIEU, khong phai loi
            # ky thuat. Vd: 治水地形分類図 chi phu dong bang ngap lut cua cac song lon; dai
            # dat (Shibuya, Yamanote) khong co. Bao to de nguoi dung DOI LOP, dung de ra
            # mot the ban do trong ma tuong la dung.
            print("   [🔴 PHU %.0f%% < %.0f%%] lop '%s' gan nhu KHONG CO DU LIEU quanh "
                  "(%.4f, %.4f). Vung nay chon lop khac di (hillshade/relief/slope)."
                  % (cover * 100, COVER_MIN * 100, ly, lat, lon))
            continue
        used.append(LAYERS[ly][4])
        if i == 0:
            base = Image.alpha_composite(base, im)
        else:
            a = ALPHA.get(ly, 0.5)
            im2 = im.copy()
            im2.putalpha(im2.getchannel("A").point(lambda v: int(v * a)))
            base = Image.alpha_composite(base, im2)
    return base, used


# ── độ cao ─────────────────────────────────────────────────────────────────────
def elev(lat, lon, z=14):
    """標高 (m) từ dem_png. RGB(128,0,0) = không có dữ liệu."""
    x, y = deg2px(lat, lon, z)
    im = fetch("dem", z, int(x // 256), int(y // 256))
    if im is None:
        return None
    r, g, b, _ = im.getpixel((int(x) % 256, int(y) % 256))
    if (r, g, b) == (128, 0, 0):
        return None
    v = r * 65536 + g * 256 + b
    return (v if v < 2 ** 23 else v - 2 ** 24) * 0.01


def profile(a, b, n=260, z=14):
    out = []
    for i in range(n + 1):
        t = i / n
        la, lo = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        out.append((hav(a, (la, lo)), elev(la, lo, z)))
    return out


# ── vẽ đè ──────────────────────────────────────────────────────────────────────
def halo_text(d, xy, s, font, fill, anchor="la", halo=3, hcol=(255, 255, 255)):
    x, y = xy
    for dx in range(-halo, halo + 1):
        for dy in range(-halo, halo + 1):
            if dx or dy:
                d.text((x + dx, y + dy), s, font=font, fill=hcol + (230,), anchor=anchor)
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def credit(img, used, extra=""):
    """Dòng 出典 — ĐIỀU KIỆN LICENSE. Không có tham số nào tắt được, đừng thêm."""
    d = ImageDraw.Draw(img, "RGBA")
    txt = "出典：国土地理院ウェブサイト（" + "・".join(dict.fromkeys(used)) + "）"
    if extra:
        txt += "  " + extra
    f = F("med", 21)
    bb = d.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.rectangle((img.width - w - 30, img.height - h - 28, img.width - 8, img.height - 6),
                fill=(255, 255, 255, 205))
    d.text((img.width - w - 19, img.height - h - 22), txt, font=f, fill=PAL["ink"] + (255,))
    return img


def pin(img, lat, lon, clat, clon, z, label, color=None, r=13, mag=MAG):
    # 🔴 pin PHAI dung cung `mag` voi mosaic(): mosaic phong anh len `mag` lan nen khoang
    # cach pixel giua 2 toa do cung phai nhan `mag`. Quen => pin roi sai cho, va sai NHE
    # (vai chuc px) nen rat de cho qua khi duyet mat.
    color = color or PAL["hi"]
    cx, cy = deg2px(clat, clon, z)
    px, py = deg2px(lat, lon, z)
    x, y = img.width / 2 + (px - cx) * mag, img.height / 2 + (py - cy) * mag
    if not (-60 < x < img.width + 60 and -60 < y < img.height + 60):
        return img
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), fill=(255, 255, 255, 235))
    d.ellipse((x - r, y - r, x + r, y + r), fill=color + (255,))
    d.ellipse((x - r + 5, y - r + 5, x + r - 5, y + r - 5), fill=(255, 255, 255, 255))
    if label:
        halo_text(d, (x + r + 12, y), label, F("bold", 40), color + (255,), anchor="lm")
    return img


def title_band(img, main, sub=""):
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, img.width, 132 if sub else 104), fill=PAL["ink"] + (232,))
    d.text((56, 30 if sub else 26), main, font=F("black", 54), fill=(255, 255, 255, 255))
    if sub:
        d.text((58, 92), sub, font=F("med", 30), fill=(212, 220, 232, 255))
    return img


# ── sản phẩm ───────────────────────────────────────────────────────────────────
def card_map(out, lat, lon, z, layers, title=None, sub=None, pins=(), extra="", mag=MAG):
    img, used = compose(lat, lon, z, layers, mag=mag)
    for p in pins:
        col = {"hi": PAL["hi"], "water": PAL["water"], "hi2": PAL["hi2"]}.get(p.get("color", "hi"), PAL["hi"])
        pin(img, p["lat"], p["lon"], lat, lon, z, p.get("label", ""), col, mag=mag)
    if title:
        title_band(img, title, sub or "")
    credit(img, used, extra)
    img.convert("RGB").save(out, quality=94)
    print("   ->", out.name)
    return out


def card_then_now(out, lat, lon, z, title=None, old="air1961", mag=MAG):
    a, ua = compose(lat, lon, z, (old,), mag=mag)
    b, ub = compose(lat, lon, z, ("photo",), mag=mag)
    img = Image.new("RGBA", (W, H))
    img.paste(a, (0, 0))
    img.paste(b.crop((W // 2, 0, W, H)), (W // 2, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.line((W // 2, 0, W // 2, H), fill=(255, 255, 255, 255), width=5)
    # Nhan dat o DINH moi nua, khong dat o day: day khung la cho cua dong 出典 (dinh that o
    # ban duyet dau tien — nhan 現在 bi dong 出典 de len). Va cat chu "空中写真" ra khoi ten
    # lop de con lai cap ngoac trong ("(1961〜1964年)") nen lay nam bang regex.
    yr = re.search(r"(\d{4})", LAYERS[old][4])
    labs = ((W // 4, (yr.group(1) + "年" if yr else "むかし")), (W * 3 // 4, "現在"))
    top = 132 if title else 24
    for x, s in labs:
        f = F("black", 52)
        bb = d.textbbox((0, 0), s, font=f)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        d.rectangle((x - w // 2 - 30, top + 16, x + w // 2 + 30, top + h + 52),
                    fill=PAL["ink"] + (238,))
        d.text((x, top + h // 2 + 34), s, font=f, fill=(255, 255, 255, 255), anchor="mm")
    if title:
        title_band(img, title)
    credit(img, ua + ub)
    img.convert("RGB").save(out, quality=94)
    print("   ->", out.name)
    return out


def card_section(out, a, b, title="断面図", labels=(), z=14):
    """断面図 — thứ không đối thủ nào trong ngách đang có."""
    pts = [(d, h) for d, h in profile(a, b, z=z) if h is not None]
    if len(pts) < 10:
        print("   [canh bao] DEM rong o tuyen nay")
        return None
    img = Image.new("RGBA", (W, H), PAL["paper"] + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = 150, W - 90, 250, H - 190
    dmax = max(p[0] for p in pts)
    hmin, hmax = min(p[1] for p in pts), max(p[1] for p in pts)
    pad = max(2.0, (hmax - hmin) * 0.32)
    lo, hi = hmin - pad, hmax + pad
    fx = lambda dd: x0 + (x1 - x0) * dd / dmax
    fy = lambda hh: y1 - (y1 - y0) * (hh - lo) / (hi - lo)
    d.polygon([(fx(p[0]), fy(p[1])) for p in pts] + [(x1, y1), (x0, y1)], fill=(176, 158, 130, 255))
    d.line([(fx(p[0]), fy(p[1])) for p in pts], fill=PAL["ink"] + (255,), width=5)
    # 🔴 Buoc truc phai cho ra 5-8 NHAN, khong phai "1m moi vach". Ban dau tinh step bang
    # log10 tron => range 34m ra step 1m = 34 nhan chong len nhau, khong doc duoc gi.
    # Cach dung: lay buoc "dep" gan nhat voi rng/6.
    rng = max(1.0, hi - lo)
    raw = rng / 6.0
    p10 = 10 ** math.floor(math.log10(raw))
    step = min((1, 2, 2.5, 5, 10), key=lambda m: abs(m * p10 - raw)) * p10
    v = math.ceil(lo / step) * step
    while v <= hi:
        y = fy(v)
        if y0 - 2 <= y <= y1:
            d.line((x0, y, x1, y), fill=PAL["line"] + (190,), width=2)
            d.text((x0 - 18, y), ("%.0fm" if step >= 1 else "%.1fm") % v,
                   font=F("med", 30), fill=PAL["sub"] + (255,), anchor="rm")
        v += step
    d.line((x0, y1, x1, y1), fill=PAL["ink"] + (255,), width=4)
    for frac in (0, .25, .5, .75, 1):
        d.text((fx(dmax * frac), y1 + 16), "%.1fkm" % (dmax * frac / 1000),
               font=F("med", 28), fill=PAL["sub"] + (255,), anchor="ma")
    for lb in labels:
        x = fx(dmax * lb["at"])
        hh = min(pts, key=lambda p: abs(p[0] - dmax * lb["at"]))[1]
        y = fy(hh)
        col = PAL["water"] if lb.get("color") == "water" else PAL["hi"]
        d.line((x, y, x, y0 + 46), fill=col + (235,), width=4)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=col + (255,))
        halo_text(d, (x, y0 + 36), lb["text"], F("bold", 36), col + (255,), anchor="mb")
        halo_text(d, (x, y + 30), "%.0fm" % hh, F("bold", 32), PAL["ink"] + (255,), anchor="mt")
    title_band(img, title, "標高差 %.0fm ／ 全長 %.1fkm" % (hmax - hmin, dmax / 1000))
    credit(img, ["標高タイル"])
    img.convert("RGB").save(out, quality=94)
    print("   ->", out.name)
    return out


def demo():
    o = ROOT / "06_VIDEO" / "_demo_gsi"
    o.mkdir(parents=True, exist_ok=True)
    print("Shibuya — bo anh mau:")
    card_map(o / "01_nen_dia_hinh.jpg", 35.6595, 139.7005, 15, ("pale", "hillshade"),
             "渋谷は、なぜ「谷」なのか", "淡色地図＋陰影起伏図",
             pins=[{"lat": 35.6595, "lon": 139.7005, "label": "スクランブル交差点"}])
    card_map(o / "02_mau_do_cao.jpg", 35.6595, 139.7005, 14, ("relief", "hillshade"),
             "色でわかる、谷の形", "色別標高図")
    # ⚠️ chisui KHONG phu Shibuya (dai dat) — lay dong bang Tone/Edogawa lam vi du dung.
    card_map(o / "03_chisui_tonegawa.jpg", 35.8300, 139.8600, 15, ("pale", "chisui"),
             "治水地形分類図が示す、旧河道", "自然堤防・後背湿地・旧河道（利根川・江戸川流域）")
    card_then_now(o / "04_1961_vs_nay.jpg", 35.6595, 139.7005, 16, "60年で、川は消えた")
    card_section(o / "05_dut_diem.jpg", (35.6720, 139.6960), (35.6500, 139.7080),
                 "代々木から渋谷への断面", labels=[{"at": 0.62, "text": "渋谷川の谷底", "color": "water"}])
    print("Xong:", o)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["demo", "map", "then", "sect", "elev"])
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--z", type=int, default=15)
    ap.add_argument("--layers", default="pale,hillshade")
    ap.add_argument("--title", default=None)
    ap.add_argument("--sub", default=None)
    ap.add_argument("--a", default=None)
    ap.add_argument("--b", default=None)
    ap.add_argument("--out", default=None)
    g = ap.parse_args()
    if g.cmd == "demo":
        demo()
    elif g.cmd == "map":
        card_map(Path(g.out or "map.jpg"), g.lat, g.lon, g.z, tuple(g.layers.split(",")), g.title, g.sub)
    elif g.cmd == "then":
        card_then_now(Path(g.out or "thennow.jpg"), g.lat, g.lon, g.z, g.title)
    elif g.cmd == "sect":
        card_section(Path(g.out or "section.jpg"),
                     tuple(float(v) for v in g.a.split(",")),
                     tuple(float(v) for v in g.b.split(",")), g.title or "断面図")
    elif g.cmd == "elev":
        print(elev(g.lat, g.lon))
