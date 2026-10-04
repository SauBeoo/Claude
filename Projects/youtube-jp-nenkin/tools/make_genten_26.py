# -*- coding: utf-8 -*-
r"""make_genten_26.py — BO THE 原典 cua video 26 (4 khoa, 9 the).

Copy khuon tu `make_genten_25.py`. Anh nguon do `tools/shoot_genten_26.py` chup.

  | khoa            | scene | dai   | so the | anh nguon                  |
  |-----------------|-------|-------|--------|----------------------------|
  | shinjuku_dankai |   33  |  7,7s |   2    | raw_shinjuku_dankai.png    |
  | joetsu_dankai   |   52  |  5,9s |   2    | raw_joetsu_dankai.png      |
  | mhlw_kaigo      |   76  | 14,9s |   3    | raw_kaigo_p1.png           |
  | shinjuku_9ki    |   77  |  7,5s |   2    | raw_shinjuku_9ki.png       |

VI SAO MOI KHOA >=2 THE: gate (2) cua `check_frame_pace.py` chan khe dung yen >9s.
Doi CHO KHOANH DO giu nguyen khung, KHONG zoom => khong mat net (bai hoc video 22 §5).

VUNG CAM (3 overlay dan cung cua khuon nenkin) — rang buoc NGAY LUC DUNG THE:
     logo       x 1790-1900 · y   20-130
     mascot     x 1642-1905 · y  530-830
     SUBSCRIBE  x   20- 260 · y  775-830
     telop band            y    0-210
     phu de                y  940-1020
  => hop dat anh: **x 40-1640 · y 225-713**, credit **y 720-768**.

🔴 HAI BAY DA DINH LUC CHUP (2026-09-16) — ghi de lo sau khoi mat mot vong:
  1. `city.shinjuku.lg.jp` tra **403 Forbidden** cho UA mac dinh cua chrome-headless-shell
     => phai truyen `--user-agent=` cua Chrome that.
  2. Co UA that roi thi no lai day sang **trang dich may J-SERVER** (vi Accept-Language la
     tieng Anh) => phai them `--lang=ja-JP --accept-lang=ja-JP,ja;q=0.9`.
     ⚠️ Ca hai lan deu ra anh "thanh cong" (rc=0, file >100KB) — chi lo khi SOI BANG MAT.
  3. Con so 6,225 nam trong PDF 48 trang, khong o HTML => render trang 1 bang PyMuPDF.

TOA DO: moi hop khoanh do SNAP vao duong ke that cua bang (do bang may: nguong <200,
dem pixel/hang va /cot) hoac vao bbox muc cua dung dong chu do.

YMYL: ban cat khong con logo co quan => baked dong credit nguon vao tung the.
CHAY:  python tools/make_genten_26.py [--out <thu muc assets>]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\26_kaigo-hokenryo-dankai-setai"
GT = os.path.join(VD, "genten_raw")
OUT_DEF = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-26\assets"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Medium.otf"

CANVAS = (1920, 1080)
BG = (243, 234, 216)          # = theme.canvasColor
RED = (214, 45, 32)
BOX_X = (40, 1640)
BOX_Y = (225, 713)
CRED_Y = 720
MAX_UP = 1.60

SJ = "出典：新宿区「介護保険料の決まり方」（令和8年度）"
JT = "出典：上越市「介護保険料」第9期（令和6年度〜令和8年度）"
MH = "出典：厚生労働省「第9期計画期間における介護保険の第1号保険料について」"
S9 = "出典：新宿区「第9期（令和6年度〜令和8年度）の介護保険料設定の考え方」"

# ── BANG THE ────────────────────────────────────────────────────────────────
# khoa: src · crop (x0,y0,x1,y1) · credit · [(ten file, hop khoanh|None), ...]
#   hop khoanh trong HE TOA DO ANH NGUON.
CARDS = {
    # ── ① 新宿区 bang 18段階 — scene 33 (7,7s) ⇒ 2 the ──────────────────────
    # Duong ke cua bang do bang may:
    #   hang (cot 段階 x810-965): 1592 header · 1764 · 1998 · 2108 · 2218 · 2328 · 2438 …
    #     => 第1段階 1764-1998 · 第2 1998-2108 · 第3 2108-2218 · 第4 2218-2328 · 第5 2328-2438
    #   cot: 802 | 972 | 1214 | 1992 | 2193 | 2371 | 2614
    #     => 段階 802-972 · 課税区分 972-1214 · 所得条件 1214-1992 · 割合 · 年額 · 月額
    # The 1 khoanh cot 課税区分 cua 第1〜3 = 「世帯全員 住民税非課税」
    #   🔴 Bat dau o **1832**, KHONG o 1764: trong 第1段階 co mot hang con full-width
    #   (「生活保護受給者、中国残留邦人等支援給付受給者」, rule 1764-1826) khong co cot
    #   課税区分 => khoanh tu 1764 thi canh trai cat ngang chu 「受給者」 (da thay o vong 1).
    "shinjuku_dankai_a": dict(
        src="raw_shinjuku_dankai.png", crop=(802, 1764, 1992, 2218), credit=SJ,
        boxes=[("genten_sj_setai1.png", (972, 1832, 1214, 2212))],
    ),
    # The 2 lui xuong 第2〜5 (cat tu 1998 chu KHONG tu 2108: o 未 2108 thi o gop
    # 「世帯全員 住民税非課税」 cua 第2+第3 bi cat doi chu), khoanh cot 課税区分 cua 第4・5 = 「本人が住民税非課税で
    # 世帯員が住民税課税」 — 第3段階 xuat hien o CA HAI the => mat noi duoc mach.
    "shinjuku_dankai_b": dict(
        src="raw_shinjuku_dankai.png", crop=(802, 1998, 1992, 2438), credit=SJ,
        boxes=[("genten_sj_setai2.png", (972, 2224, 1214, 2432))],
    ),

    # ── ② 上越市 bang 17段階 — scene 52 (5,9s) ⇒ 2 the ─────────────────────
    #   hang: 2004 header · 2125 · 2346 · 2567 · 2788 · 3010 · 3231
    #     => 第1 2125-2346 · 第2 2346-2567 · 第3 2567-2788 · 第4 2788-3010 · 第5 3010-3231
    #   cot: 857 | 1028 | 1243 | 1971 | 2229 | 2486 | 2743
    #     => 段階 · 割合 · 所得段階の要件 · 第8期保険料 · 第9期保険料 · 第8期との差
    "joetsu_dankai_a": dict(
        src="raw_joetsu_dankai.png", crop=(857, 2346, 2486, 2788), credit=JT,
        boxes=[("genten_jt_dan3.png", (2235, 2573, 2480, 2782))],
    ),
    "joetsu_dankai_b": dict(
        src="raw_joetsu_dankai.png", crop=(857, 2788, 2486, 3231), credit=JT,
        boxes=[("genten_jt_dan5.png", (2235, 3016, 2480, 3225))],
    ),

    # ── ③ 厚労省 全国平均 6,225円 — scene 76 (14,9s) ⇒ 3 the ────────────────
    # PDF 48 trang, con so o TRANG 1. Khung hop: duong ke ngang y770 va y1127,
    # muc ngang x446-1957. bbox muc do bang may:
    #   6,014円 (701,947)-(887,995) · 6,225円 (1517,947)-(1702,995) · (+3.5%) (1561,1029)-(1662,1058)
    "mhlw_kaigo": dict(
        src="raw_kaigo_p1.png", crop=(436, 760, 1967, 1140), credit=MH,
        boxes=[("genten_mhlw.png",      None),
               ("genten_mhlw_8ki.png",  (701, 947, 887, 995)),
               ("genten_mhlw_9ki.png",  (1517, 947, 1702, 995))],
    ),

    # ── ④ 新宿区 9段階→13段階 — scene 77 (7,5s) ⇒ 2 the ────────────────────
    # 4 dong chu cua muc 2, do bang may: 1792-1820 · 1840-1869 · 1888-1917 · 1937-1965
    #   dong 2 = 「…標準段階を9段階から13段階へと改訂しました。」  bbox (803,1839)-(2012,1869)
    #   dong 4 = 「画での16段階から18段階の多段階化の措置を行いました。」 (804,1936)-(1612,1965)
    "shinjuku_9ki": dict(
        src="raw_shinjuku_9ki.png", crop=(780, 1780, 2740, 1980), credit=S9,
        boxes=[("genten_9ki_13.png", (803, 1839, 2012, 1869)),
               ("genten_9ki_18.png", (804, 1936, 1612, 1965))],
    ),
}


def build(key: str, spec: dict, out: str) -> int:
    base = Image.open(os.path.join(GT, spec["src"])).convert("RGB")
    cx0, cy0, cx1, cy1 = spec["crop"]
    block = base.crop(spec["crop"])
    sc = min((BOX_X[1] - BOX_X[0]) / block.width, MAX_UP,
             (BOX_Y[1] - BOX_Y[0]) / block.height)
    bw, bh = int(round(block.width * sc)), int(round(block.height * sc))
    block = block.resize((bw, bh), Image.LANCZOS)
    ox = BOX_X[0] + (BOX_X[1] - BOX_X[0] - bw) // 2
    oy = BOX_Y[0] + (BOX_Y[1] - BOX_Y[0] - bh) // 2

    if ox < BOX_X[0] or ox + bw > BOX_X[1] or oy < BOX_Y[0] or oy + bh > BOX_Y[1]:
        print(f"  GATE DO {key}: hop ({ox},{oy})-({ox+bw},{oy+bh}) ra ngoai "
              f"x {BOX_X} · y {BOX_Y}")
        return 0

    f = ImageFont.truetype(FONT, 30)
    n = 0
    for name, hb in spec["boxes"]:
        card = Image.new("RGB", CANVAS, BG)
        card.paste(block, (ox, oy))
        d = ImageDraw.Draw(card)
        d.rectangle([ox - 2, oy - 2, ox + bw + 1, oy + bh + 1],
                    outline=(206, 198, 182), width=2)
        if hb:
            # GATE: hop khoanh phai nam TRONG anh nguon da cat
            if not (cx0 <= hb[0] and cx1 >= hb[2] and cy0 <= hb[1] and cy1 >= hb[3]):
                print(f"  GATE DO {name}: hop khoanh {hb} nam ngoai crop {spec['crop']}")
                return 0
            x0 = ox + (hb[0] - cx0) * sc - 4
            y0 = oy + (hb[1] - cy0) * sc - 3
            x1 = ox + (hb[2] - cx0) * sc + 4
            y1 = oy + (hb[3] - cy0) * sc + 3
            if x0 < 8 or x1 > CANVAS[0] - 8 or y0 < BOX_Y[0] - 8 or y1 > BOX_Y[1] + 8:
                print(f"  GATE DO {name}: vong khoanh ({int(x0)},{int(y0)})-"
                      f"({int(x1)},{int(y1)}) tran ra ngoai khe")
                return 0
            for w in (6, 5):
                d.rounded_rectangle([x0 - w // 2, y0 - w // 2, x1 + w // 2, y1 + w // 2],
                                    radius=9, outline=RED, width=w)
        tw = d.textlength(spec["credit"], font=f)
        cx = max(300, ox + 10)
        d.rectangle([cx, CRED_Y, cx + tw + 36, CRED_Y + 48], fill=(28, 42, 74))
        d.text((cx + 18, CRED_Y + 9), spec["credit"], font=f, fill=(255, 255, 255))
        card.save(os.path.join(out, name))
        n += 1
        print(f"  ok {name:<26} khoanh {hb if hb else '(khong)'}")
    print(f"     khoi {bw}x{bh} tai ({ox},{oy}) — scale {sc:.3f}x")
    return n


def main() -> int:
    out = OUT_DEF
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    tot = 0
    for key, spec in CARDS.items():
        print(f"[{key}]  <- {spec['src']}")
        tot += build(key, spec, out)
    need = sum(len(s["boxes"]) for s in CARDS.values())
    print(f"\n{'OK' if tot == need else 'GATE DO'}  {tot}/{need} the -> {out}")
    return 0 if tot == need else 1


if __name__ == "__main__":
    sys.exit(main())
