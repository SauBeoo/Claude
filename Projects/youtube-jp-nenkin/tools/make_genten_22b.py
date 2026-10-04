# -*- coding: utf-8 -*-
r"""make_genten_22b.py — BO THE 原典 DAY DU cua video 22 (4 khoa, 10 the).

Thay `make_genten_22.py` (chi lam duoc khoa `nenkin_shiharai` cua ban DEMO). Bon khoa cua
`_scenes22.GENTEN`, moi khoa mot CHUOI TIET LO bang cach doi CHO KHOANH DO:

  | khoa            | scene | dai   | so the | anh nguon        |
  |-----------------|-------|-------|--------|------------------|
  | nenkin_shiharai |   13  | 21,1s |   4    | v_shiharai.png   |
  | nenkin_gessuu   |   32  | 12,0s |   2    | raw_shibou.png   |
  | nenkin_mynumber |   43  | 13,4s |   2    | raw_shibou.png   |
  | kokuzei_ichiji  |   79  |  5,8s |   2    | raw_ichiji.png   |

VI SAO PHAI >=2 THE moi khoa: gate (2) cua `check_frame_pace.py` chan khe dung yen >9s.
Doi cho khoanh giu nguyen khung, KHONG zoom, nen khong mat net (anh nguon chi rong 1400px).

VUNG CAM cua khuon video 22 — coi la rang buoc NGAY LUC DUNG THE, dung phat hien lai tren
ban render (bai hoc `make_genten_22.py`):
     logo       x 1790-1900 · y   20-130
     mascot     x 1642-1905 · y  530-830
     SUBSCRIBE  x   20- 260 · y  775-830
     telop band            y    0-210
     phu de                y  940-1020
=> hop dat anh: **x 40-1640 · y 225-713**, credit **y 720-768**.

DA AP mieng sua con treo trong `make_genten_22.py`: hop cu (`OX=275`, `DEST_W=1350`) siet
qua tay vi coi SUBSCRIBE nhu mot COT chay het khung, trong khi no la HINH CHU NHAT o
y 775-830 — khong giao doc voi bang (y<=713). Noi ra x 40-1640 => rong 1600 = **+18,5%**,
chu trong anh chup to len dung ti le do. Bai hoc: kiem giao nhau bang CA HAI truc.

TRAN UPSCALE 1,60x: qua muc do chu bat dau nhoe (nguon 1400px, khong co ban to hon).
Khoi nao hep hon thi len 1,60x roi CAN GIUA, khong keo cho du 1600.

YMYL: ban cat khong con logo co quan => baked dong credit nguon vao tung the.
CHAY:  python tools/make_genten_22b.py [--out <thu muc assets>]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
GT = os.path.join(VD, "_genten")
OUT_DEF = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-22full\assets"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Medium.otf"

CANVAS = (1920, 1080)
BG = (243, 234, 216)          # = theme.canvasColor
RED = (214, 45, 32)
BOX_X = (40, 1640)            # khe an toan ngang
BOX_Y = (225, 713)            # khe an toan doc
CRED_Y = 720
MAX_UP = 1.60                 # tran upscale

# ── BANG THE ────────────────────────────────────────────────────────────────
# khoa: (anh nguon, hop cat (x0,y0,x1,y1), credit, [(ten file, hop khoanh|None), ...])
#   hop khoanh trong HE TOA DO ANH NGUON. None = ban chua khoanh.
#   Toa do dong chu do bang MAY (nguong <200, dem pixel/hang) — xem docstring cua tung khoa.
CARDS = {
    # bang 「年金の支払月と支払対象月」 — bang chung dat nhat cua bai
    "nenkin_shiharai": dict(
        src="v_shiharai.png", crop=(194, 173, 1155, 466),
        credit="出典：日本年金機構「年金の支払月と支払対象月」",
        boxes=[("genten_shiharai.png",     None),
               ("genten_shiharai_all.png", (200, 179, 1149, 460)),   # ca bang
               ("genten_shiharai_col.png", (200, 179,  686, 460)),   # cot 支払月
               ("genten_shiharai_row.png", (200, 259, 1149, 300))],  # hang 4月
    ),
    # 「亡くなった月分までの年金については、未支給年金として…遺族が受け取ることができます」
    #   dong do bang may tren raw_shibou.png: 438-452 · 465-479 · 492-507
    "nenkin_gessuu": dict(
        src="raw_shibou.png", crop=(195, 375, 1215, 625),
        credit="出典：日本年金機構「年金を受けている方が亡くなったとき」",
        boxes=[("genten_gessuu.png",     None),
               ("genten_gessuu_box.png", (205, 433, 1205, 484))],
    ),
    # 「日本年金機構に個人番号（マイナンバー）が収録されている方は、原則として…省略できます」
    #   dong 547-561 + 574-588
    "nenkin_mynumber": dict(
        src="raw_shibou.png", crop=(195, 375, 1215, 625),
        credit="出典：日本年金機構「年金を受けている方が亡くなったとき」",
        boxes=[("genten_mynumber.png",     None),
               ("genten_mynumber_box.png", (205, 541, 1205, 594))],
    ),
    # 総収入金額 − 支出 − 特別控除額(最高50万円) ＝ 一時所得の金額   (dong 1274-1288)
    "kokuzei_ichiji": dict(
        src="raw_ichiji.png", crop=(195, 1150, 920, 1370),
        credit="出典：国税庁「一時所得」（タックスアンサー No.1490）",
        boxes=[("genten_ichiji.png",     None),
               ("genten_ichiji_box.png", (205, 1267, 850, 1293))],
    ),
}


def build(key: str, spec: dict, out: str) -> int:
    base = Image.open(os.path.join(GT, spec["src"])).convert("RGB")
    cx0, cy0, cx1, cy1 = spec["crop"]
    block = base.crop(spec["crop"])
    # scale: lap het be rong khe an toan, nhung khong vuot tran upscale, va khong cao qua khe
    sc = min((BOX_X[1] - BOX_X[0]) / block.width, MAX_UP,
             (BOX_Y[1] - BOX_Y[0]) / block.height)
    bw, bh = int(round(block.width * sc)), int(round(block.height * sc))
    block = block.resize((bw, bh), Image.LANCZOS)
    ox = BOX_X[0] + (BOX_X[1] - BOX_X[0] - bw) // 2          # can giua ngang
    oy = BOX_Y[0] + (BOX_Y[1] - BOX_Y[0] - bh) // 2          # can giua doc

    # GATE tai cho: hop dat phai nam trong khe an toan
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
        cx = max(300, ox + 10)                    # >=300: ne x-range cua SUBSCRIBE
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
