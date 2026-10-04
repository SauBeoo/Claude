# -*- coding: utf-8 -*-
r"""make_genten_21.py — dung THE 原典 1920x1080 cho video 21 tu anh chup THAT (genten_raw/, shoot_genten_21.py).

Moi the: nen giay kem · anh chup CAT quanh cau trich (phong to cho de doc) · KHUNG DO dung toa do cau
(toa do lay tu PyMuPDF search_for voi PDF, do bang mat voi trang HTML) · dong nguon goc DUOI-TRAI (font).
Goc TREN-TRAI de trong cho chu +NUM cua make_cells; goc DUOI-PHAI de trong (timestamp YouTube).
Ra: real_21/gt_<key>.png  + ghi MANIFEST.json (kind photo) de build_slides_21 doc ma `gt:<key>`.
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\21_umaredoshi-okane")
RAW, REAL = VD / "genten_raw", VD / "real_21"
FONT = r"C:\Windows\Fonts\YuGothB.ttc"
W, H = 1920, 1080
BOX = (80, 250, 1840, 900)      # vung dat anh chup: chua 0-250 tren cho +NUM, chua day cho dong nguon

# key: (file, crop(x0,y0,x1,y1) theo toa do anh tho, [khung do...], dong nguon, trang goc)
CARDS = {
 "kokkai1972": ("kokkai1972.png", (1330, 410, 2800, 570), [(1636, 462, 2692, 514)],
                "衆議院 予算委員会 昭和47年3月7日 高見三郎 文部大臣（国会会議録）",
                "https://kokkai.ndl.go.jp/txt/106805261X01119720307/144"),
 "kokkai1963": ("kokkai1963.png", (1040, 405, 1960, 476), [(1120, 415, 1648, 468)],
                "衆議院 文教委員会 昭和38年3月6日（国会会議録）",
                "https://kokkai.ndl.go.jp/txt/104305077X00819630306/119"),
 "kokkai1966": ("kokkai1966.png", (1380, 455, 3300, 570), [(2822, 462, 3285, 514), (1418, 510, 2150, 562)],
                "衆議院 逓信委員会 昭和41年6月9日（国会会議録）",
                "https://kokkai.ndl.go.jp/txt/105114816X02519660609/80"),
 "mext": ("mext_jugyoryo.png", (100, 400, 2072, 920), [(100, 774, 910, 842)],
          "文部科学省「国立大学と私立大学の授業料等の推移」",
          "https://www.mext.go.jp/b_menu/shingi/kokuritu/005/gijiroku/attach/1386502.htm"),
 "postal": ("postal_p1.png", (250, 780, 1420, 1270), [(262, 1022, 1410, 1172)],
            "郵政博物館 研究紀要 第8号「新たに発見された『お年玉付き年賀はがきの見本』」",
            "https://www.postalmuseum.jp/publication/research/research_08_09.pdf"),
 "housou": ("soumu_p3.png", (30, 300, 2140, 1000), [(40, 722, 2130, 826), (40, 836, 2130, 940)],
            "総務省 公共放送の在り方に関する検討分科会 資料1-3（受信料額の推移）",
            "https://www.soumu.go.jp/main_content/000683792.pdf"),
 "ntt": ("ntt_p2.png", (100, 120, 1260, 520), [(240, 318, 950, 358)],
         "NTT東日本 データブック 参考1（東京・単独電話の場合）",
         "https://www.ntt-east.co.jp/databook/pdf/2024_06-10.pdf"),
}


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
