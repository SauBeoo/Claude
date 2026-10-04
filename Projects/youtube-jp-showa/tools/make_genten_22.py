# -*- coding: utf-8 -*-
r"""make_genten_21.py — dung THE 原典 1920x1080 cho video 22 tu anh chup THAT (genten_raw/, shoot_genten_22.py).

Moi the: nen giay kem · anh chup CAT quanh cau trich (phong to cho de doc) · KHUNG DO dung toa do cau
(toa do lay tu PyMuPDF search_for voi PDF, do bang mat voi trang HTML) · dong nguon goc DUOI-TRAI (font).
Goc TREN-TRAI de trong cho chu +NUM cua make_cells; goc DUOI-PHAI de trong (timestamp YouTube).
Ra: real_22/gt_<key>.png  + ghi MANIFEST.json (kind photo) de build_slides_22 doc ma `gt:<key>`.
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\22_kieta-shigoto")
RAW, REAL = VD / "genten_raw", VD / "real_22"
FONT = r"C:\Windows\Fonts\YuGothB.ttc"
W, H = 1920, 1080
BOX = (80, 250, 1840, 900)      # vung dat anh chup: chua 0-250 tren cho +NUM, chua day cho dong nguon

# key: (dong nguon) — anh + toa do khung do lay tu genten_raw/boxes.json (shoot_genten_22.py do bang DOM, khong do mat)
SRCS = {
 "k1959": "国会 昭和34年11月26日（国会会議録）",
 "k1964": "国会 昭和39年3月27日（国会会議録）",
 "k1966": "国会 昭和41年5月27日 ※運輸省調（国会会議録）",
 "k1966b": "国会 昭和41年3月31日（国会会議録）",
 "kisoku15": "国会 昭和41年10月11日（国会会議録）",
 "k1971": "国会 昭和46年3月23日（国会会議録）",
 "k1972": "国会 昭和47年5月8日（国会会議録）",
 "k1976": "国会 昭和51年8月12日（国会会議録）",
 "k1980": "国会 昭和55年3月5日 日本電信電話公社総裁（国会会議録）",
 "k1981": "国会 昭和56年3月20日（国会会議録）",
 "k1985": "国会 昭和60年5月23日 労働省（国会会議録）",
 "sekitan": "国会 昭和40年3月24日（国会会議録）",
 "roki63": "労働基準法（昭和22年法律第49号）第63条（e-Gov 法令検索）",
}
BX = json.loads((RAW / "boxes.json").read_text(encoding="utf-8"))


def _spec(key):
    b = BX[key]
    im = Image.open(RAW / (key + ".png"))
    return (key + ".png", (0, 0, im.width, im.height), [tuple(r) for r in b["rects"]], SRCS[key], b["url"])


CARDS = {k: _spec(k) for k in SRCS}


def card(key, spec):
    fn, crop, boxes, src, url = spec
    im = Image.open(RAW / fn).convert("RGB")
    x0, y0, x1, y1 = crop
    part = im.crop(crop)
    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    s = min(bw / part.width, bh / part.height)
    part = part.resize((int(part.width * s), int(part.height * s)), Image.LANCZOS)
    ox = BOX[0] + (bw - part.width) // 2
    oy = BOX[1] + (bh - part.height) // 2
    cv = Image.new("RGB", (W, H), (244, 239, 228))
    d = ImageDraw.Draw(cv)
    d.rectangle((ox - 14, oy - 14, ox + part.width + 14, oy + part.height + 14), fill=(255, 255, 255), outline=(200, 190, 170), width=3)
    cv.paste(part, (ox, oy))
    for bx0, by0, bx1, by1 in boxes:
        X0 = ox + (bx0 - x0) * s; Y0 = oy + (by0 - y0) * s
        X1 = ox + (bx1 - x0) * s; Y1 = oy + (by1 - y0) * s
        d.rounded_rectangle((X0 - 8, Y0 - 6, X1 + 8, Y1 + 6), radius=10, outline=(210, 30, 30), width=7)
    f = ImageFont.truetype(FONT, 34)
    d.text((80, 952), "出典：" + src, font=f, fill=(60, 50, 40))
    out = REAL / ("gt_%s.png" % key)
    cv.save(out)
    return out, url, src


def main():
    manp = REAL / "MANIFEST.json"
    man = json.loads(manp.read_text(encoding="utf-8"))
    for key, spec in CARDS.items():
        out, url, src = card(key, spec)
        man["gt:" + key] = {"file": out.name, "kind": "photo", "license": "官公庁・公的機関の公開資料（原典 screenshot）",
                            "author": src, "page": url, "url": url}
        print("OK", out.name)
    manp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
