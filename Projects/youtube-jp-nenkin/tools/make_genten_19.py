# -*- coding: utf-8 -*-
"""make_genten_19.py — 8 thẻ 原典 cho video 19 (3 nguồn × 2–3 nhịp máy quay).

⚠️ ĐÂY LÀ **THẺ TRÍCH DẪN**, KHÔNG phải ảnh chụp trang web, và cũng KHÔNG được
   trông giống ảnh chụp trang web — `make_genten.py` ghi rõ: *"dựng một hình trông
   như screenshot của trang thật = dựng giả hồ sơ, cấm"*.
   Thẻ ghi: nhãn 引用 · câu trích NGUYÊN VĂN · tên cơ quan · mốc thời điểm.
   Khoanh đỏ đặt trên **chính câu trích** ⇒ lời thoại 「赤で囲んだところ」 vẫn đúng sự thật.

Mọi câu trích dưới đây lấy từ FACT SHEET đã verify (03_SCRIPTS/19_*.md §GĐ0b).

CHẠY:  python tools/make_genten_19.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "06_VIDEO" / "19_kounenrei-koyou-keizoku-kyufu" / "photocard"
W, H = 1400, 900
PAPER, NAVY, RED, INK, GREY = (247, 244, 236), (26, 42, 74), (200, 32, 40), (38, 42, 52), (120, 124, 132)
GRID = (228, 226, 216)
F_B, F_R = "C:/Windows/Fonts/yugothb.ttc", "C:/Windows/Fonts/yugothm.ttc"

CARDS = [
    dict(file="card_genten19_01", zoom=0,
         org="厚生労働省／ハローワーク", doc="高年齢雇用継続給付の内容及び支給申請手続",
         when="令和8年8月版",
         quote=["60歳以上65歳未満の一般被保険者であること", "被保険者であった期間が5年以上あること",
                "60歳以後の賃金が60歳時点の75％未満に低下したこと"], mark=2),
    dict(file="card_genten19_01_b", zoom=1, org="厚生労働省／ハローワーク",
         doc="高年齢雇用継続給付の内容及び支給申請手続", when="令和8年8月版",
         quote=["60歳以後の賃金が", "60歳時点の75％未満に低下したこと"], mark=1),
    dict(file="card_genten19_01_c", zoom=2, org="厚生労働省／ハローワーク",
         doc="支給限度額・最低限度額", when="令和8年8月1日〜令和9年7月31日",
         quote=["支給限度額　397,369円", "最低限度額　2,562円",
                "賃金月額の上限　522,000円"], mark=0),
    dict(file="card_genten19_02", zoom=0, org="厚生労働省",
         doc="高年齢雇用継続給付の受給要件および支給率の変更について", when="令和7年4月1日〜",
         quote=["令和7年4月1日以降に60歳に達した日が対象の方は、",
                "各月に支払われた賃金の10％（変更後の支給率）を", "限度として支給"], mark=1),
    dict(file="card_genten19_02_b", zoom=1, org="厚生労働省",
         doc="高年齢雇用継続給付の支給率の変更", when="令和7年4月1日〜",
         quote=["賃金の10％", "（変更後の支給率）"], mark=0),
    dict(file="card_genten19_03", zoom=0, org="日本年金機構",
         doc="雇用保険の給付を受けられる場合（高年齢雇用継続給付との調整）", when="令和7年4月1日〜",
         quote=["支給停止される年金額は、最高で", "賃金（標準報酬月額）の4％に当たる額"], mark=1),
    dict(file="card_genten19_03_b", zoom=1, org="日本年金機構",
         doc="高年齢雇用継続給付との調整", when="令和7年4月1日〜",
         quote=["初回の高年齢雇用継続給付の支給申請が認められた場合は、",
                "その後に支給申請を行わなかったときでも、",
                "年金の一部支給停止は解除されません"], mark=2),
    dict(file="card_genten19_03_c", zoom=2, org="日本年金機構",
         doc="繰上げ支給の老齢厚生年金との調整", when="現行",
         quote=["調整の対象となるのは", "特別支給の老齢厚生年金",
                "繰上げ支給の老齢厚生年金（報酬比例部分）"], mark=2),
]


def build(c):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRID, width=1)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)

    fl = ImageFont.truetype(F_B, 30)
    # 🔴 TỰ CO CỠ CHỮ THEO BỀ RỘNG (user bắt ở 2:37 — 3/8 thẻ tràn chữ ra mép phải).
    #    Bản đầu đặt cỡ CỐ ĐỊNH, câu dài nhất (25 ký × 54px + lề 100) = 1450 > 1400.
    #    Chừa lề phải 110px cho vòng khoanh đỏ (nó nở thêm 26px mỗi bên).
    _avail = W - 100 - 110
    _sz = 54 if c["zoom"] == 0 else 66
    while _sz > 26:
        _f = ImageFont.truetype(F_B, _sz)
        if max(_f.getbbox(x)[2] for x in c["quote"]) <= _avail:
            break
        _sz -= 2
    fq = ImageFont.truetype(F_B, _sz)
    fo = ImageFont.truetype(F_R, 30)
    fd = ImageFont.truetype(F_R, 26)

    # nhãn 引用 — nói thẳng đây là TRÍCH DẪN, không phải ảnh chụp
    d.rectangle([70, 62, 210, 116], fill=NAVY)
    d.text((88, 72), "引用", font=fl, fill=PAPER)
    d.text((232, 76), c["doc"], font=fd, fill=GREY)

    y = 210 if c["zoom"] == 0 else 260
    step = 96 if c["zoom"] == 0 else 116
    boxes = []
    for i, line in enumerate(c["quote"]):
        d.text((100, y), line, font=fq, fill=INK)
        bb = d.textbbox((100, y), line, font=fq)
        boxes.append(bb)
        y += step

    # khoanh ĐỎ đúng dòng cốt lõi (lời thoại nói 「赤で囲んだところ」)
    bb = boxes[c["mark"]]
    d.rounded_rectangle([bb[0] - 26, bb[1] - 20, bb[2] + 26, bb[3] + 18],
                        radius=30, outline=RED, width=7)

    d.line([(100, H - 150), (W - 100, H - 150)], fill=GREY, width=2)
    d.text((100, H - 122), f"出典：{c['org']}", font=fo, fill=NAVY)
    d.text((100, H - 78), c["when"], font=fd, fill=GREY)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for c in CARDS:
        p = OUT / f"{c['file']}.png"
        build(c).save(p)
        print(f"  ✓ {c['file']}")
    print(f"{len(CARDS)} thẻ 原典 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
