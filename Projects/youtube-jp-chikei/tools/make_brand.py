# -*- coding: utf-8 -*-
"""
make_brand.py — avatar + banner kênh 地形と地名の日本史, dựng từ ĐỊA HÌNH THẬT.

Vì sao không gen bằng AI: bản sắc kênh là **dữ liệu địa hình thật**, nên logo cũng nên là
đường cắt địa hình thật (断面図 代々木→渋谷, lấy từ 標高タイル của 国土地理院) thay vì một hình
minh hoạ. Kèm theo: chữ Nhật luôn sắc nét (font, không phải model gen), và không dính
watermark ✦ nên khỏi cả vòng xoá watermark (`media-library.md` §2.10 ⑤b).

    python tools/make_brand.py                              # dung duong dia hinh that
    python tools/make_brand.py --bg 09_BRAND/ai_banner_B2.png  # dong chu len NEN AI gen
    python tools/make_brand.py --bg-avatar 09_BRAND/ai_avatar_A1_plate.png

CO `--bg`: anh AI chi lam NEN, chu van do Noto Sans JP ve => kanji khong bao gio nat.
Prompt gen nen: 09_BRAND/brand_prompts_PLATE.txt (xem brand_prompts_BLOCKS.md).
"""
import io, sys, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsi_map as G   # da wrap stdout sang utf-8

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "09_BRAND"
INK, PAPER, RED, WATER = G.PAL["ink"], G.PAL["paper"], G.PAL["hi"], G.PAL["water"]

# Tuyến 代々木(cao nguyên) → 渋谷(đáy thung lũng): chính đường cắt của video #1.
A, B = (35.6720, 139.6960), (35.6500, 139.7080)


def ridge(n=220):
    pts = [(d, h) for d, h in G.profile(A, B, n=n) if h is not None]
    if len(pts) < 10:
        raise SystemExit("DEM rong — khong dung duoc duong dia hinh that")
    dmax = max(p[0] for p in pts)
    lo = min(p[1] for p in pts)
    hi = max(p[1] for p in pts)
    return pts, dmax, lo, hi


def fit_bg(path, w, h):
    """Anh AI ra 16:9; cat GIUA khung ve dung ti le can, roi resize.

    Avatar la 1:1 nen buoc nay an ~44% be ngang — day la ly do prompt bat bo cuc TRON,
    DOI XUNG, nam gon giua khung (09_BRAND/brand_prompts_BLOCKS.md §0).
    """
    im = Image.open(path).convert("RGBA")
    want = w / h
    have = im.width / im.height
    if have > want:                       # anh rong hon -> cat hai ben
        nw = int(im.height * want)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    elif have < want:                     # anh cao hon -> cat tren duoi
        nh = int(im.width / want)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
    return im.resize((w, h), Image.LANCZOS)


def avatar(size=800, bg=None):
    pts, dmax, lo, hi = ridge()
    img = Image.new("RGBA", (size, size), PAPER + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    if bg:
        img.paste(fit_bg(bg, size, size), (0, 0))
        d = ImageDraw.Draw(img, "RGBA")
        # Chu 地形 se de len anh AI => cham nhe mot dia sang o giua cho chu bam vao,
        # neu khong thi nen nhieu chi tiet an mat net chu o 48px.
        veil = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(veil).ellipse((int(size * .10), int(size * .10),
                                      int(size * .90), int(size * .90)),
                                     fill=PAPER + (150,))
        img = Image.alpha_composite(img, veil.filter(ImageFilter.GaussianBlur(size * .02)))
        d = ImageDraw.Draw(img, "RGBA")
        f = G.F("black", int(size * 0.26))
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                if dx or dy:
                    d.text((size / 2 + dx, int(size * 0.47) + dy), "地形", font=f,
                           fill=(255, 255, 255, 235), anchor="mm")
        d.text((size / 2, int(size * 0.47)), "地形", font=f, fill=INK + (255,), anchor="mm")
        OUT.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(OUT / "avatar.png")
        for s2 in (176, 88, 48):
            img.convert("RGB").resize((s2, s2), Image.LANCZOS).save(OUT / ("avatar_prev%d.png" % s2))
        print("   -> avatar.png (nen AI: %s)" % Path(bg).name)
        return
    d.ellipse((0, 0, size, size), fill=INK + (255,))
    pad = int(size * 0.14)
    d.ellipse((pad, pad, size - pad, size - pad), fill=PAPER + (255,))

    # đường địa hình thật, chiếm nửa dưới đĩa
    x0, x1 = int(size * 0.20), int(size * 0.80)
    y0, y1 = int(size * 0.50), int(size * 0.76)
    fx = lambda dd: x0 + (x1 - x0) * dd / dmax
    fy = lambda hh: y1 - (y1 - y0) * (hh - lo) / max(1e-6, hi - lo)
    line = [(fx(p[0]), fy(p[1])) for p in pts]
    d.polygon(line + [(x1, y1 + 60), (x0, y1 + 60)], fill=(176, 158, 130, 255))
    d.line(line, fill=INK + (255,), width=int(size * 0.022))

    # chấm nước ở đáy thung lũng — nhân vật chính của kênh
    lowest = min(pts, key=lambda p: p[1])
    cx, cy = fx(lowest[0]), fy(lowest[1])
    r = int(size * 0.035)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WATER + (255,))

    # chữ: 2 ký, to hết mức — avatar hiển thị ~48px nên chữ nhiều là mất sạch
    f = G.F("black", int(size * 0.26))
    d.text((size / 2, int(size * 0.335)), "地形", font=f, fill=INK + (255,), anchor="mm")
    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT / "avatar.png")
    for s in (176, 88, 48):
        img.convert("RGB").resize((s, s), Image.LANCZOS).save(OUT / ("avatar_prev%d.png" % s))
    print("   -> avatar.png (+ prev 176/88/48)")


def banner(W=2560, H=1440, bg=None):
    """Vùng an toàn mọi thiết bị = 1546×423 giữa khung. Chữ chỉ được nằm trong đó."""
    pts, dmax, lo, hi = ridge()
    img = Image.new("RGBA", (W, H), INK + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    if bg:
        img.paste(fit_bg(bg, W, H), (0, 0))
        # Dai toi vat ngang dung sau vung an toan: prompt da xin "middle third clean",
        # nhung anh gen khong bao gio sach tuyet doi — lop nay bao hiem cho do doc cua chu.
        veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(veil).rectangle((0, sy0 - 40, W, sy0 + 423 + 40), fill=INK + (168,))
        img = Image.alpha_composite(img, veil.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(img, "RGBA")
        _band_text(img, d, W, H, sx0, sy0, ow=9)
        OUT.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(OUT / "banner.png")
        img.convert("RGB").crop((sx0, sy0, sx0 + 1546, sy0 + 423)).save(OUT / "banner_safearea.png")
        img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(OUT / "banner_prev.png")
        print("   -> banner.png (nen AI: %s)" % Path(bg).name)
        return

    # dải địa hình chạy hết bề ngang, đặt dưới khối chữ
    x0, x1 = 0, W
    y0, y1 = int(H * 0.60), int(H * 0.86)
    fx = lambda dd: x0 + (x1 - x0) * dd / dmax
    fy = lambda hh: y1 - (y1 - y0) * (hh - lo) / max(1e-6, hi - lo)
    line = [(fx(p[0]), fy(p[1])) for p in pts]
    d.polygon(line + [(W, H), (0, H)], fill=(38, 54, 82, 255))
    d.line(line, fill=(120, 152, 196, 255), width=7)
    lowest = min(pts, key=lambda p: p[1])
    d.ellipse((fx(lowest[0]) - 17, fy(lowest[1]) - 17, fx(lowest[0]) + 17, fy(lowest[1]) + 17),
              fill=WATER + (255,))

    # 🔴 Moc doc phai GIAN: ban dau title@108 / sub@214 => chi con ~10px ho giua chu 132px
    # va chu 60px, nhin nhu dinh nhau. Giu it nhat ~40px ho giua hai khoi chu.
    _band_text(img, d, W, H, sx0, sy0)
    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT / "banner.png")
    img.convert("RGB").crop((sx0, sy0, sx0 + 1546, sy0 + 423)).save(OUT / "banner_safearea.png")
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(OUT / "banner_prev.png")
    print("   -> banner.png (+ safearea + prev)")


def _outline(d, xy, s, font, fill, ow=0, ocol=(10, 14, 24)):
    """袋文字. `ow=0` = khong vien (nen phang tu dung); `ow>0` cho NEN AI ruc ro —
    dai toi mo mot minh KHONG du khi nen nhieu mau (bai hoc thumbnail: chu tren nen
    ruc phai co vien den day, audience-45plus §1)."""
    if ow:
        x, y = xy
        for dx in range(-ow, ow + 1, 2):
            for dy in range(-ow, ow + 1, 2):
                if dx * dx + dy * dy <= ow * ow and (dx or dy):
                    d.text((x + dx, y + dy), s, font=font, fill=ocol + (255,), anchor="mm")
    d.text(xy, s, font=font, fill=fill, anchor="mm")


def _band_text(img, d, W, H, sx0, sy0, ow=0):
    """Khoi chu cua banner — tach ra de ca ban dia-hinh-that lan ban nen-AI dung CHUNG."""
    _outline(d, (W // 2, sy0 + 92), "地形と地名の日本史", G.F("black", 132),
             (255, 255, 255, 255), ow)
    _outline(d, (W // 2, sy0 + 236), "その地形が、その歴史を決めた", G.F("bold", 60),
             (255, 226, 140, 255), max(0, ow - 3))
    _outline(d, (W // 2, sy0 + 336), "国土地理院の地図データで読み解く ／ 毎週 火・金・日 20時",
             G.F("med", 44), (222, 232, 245, 255) if ow else (196, 208, 226, 255), max(0, ow - 4))
    bw = 980
    d.rectangle((W // 2 - bw // 2, sy0 + 392, W // 2 + bw // 2, sy0 + 400), fill=RED + (255,))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", default=None, help="anh AI lam nen BANNER (PLATE, khong chu)")
    ap.add_argument("--bg-avatar", default=None, help="anh AI lam nen AVATAR")
    g = ap.parse_args()
    avatar(bg=g.bg_avatar)
    banner(bg=g.bg)
    print("Xong:", OUT)
    print("DUYET: 09_BRAND/avatar_prev48.png (chu con doc duoc?) va banner_safearea.png")
