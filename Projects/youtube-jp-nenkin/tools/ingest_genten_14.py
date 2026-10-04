# -*- coding: utf-8 -*-
r"""ingest_genten_14.py — dựng 3 原典ショット cho video 14 + khoanh ĐỎ + nhãn nguồn.

Khuôn chép từ `ingest_genten_13.py`: nguồn là SCREENSHOT trang cơ quan công (KHÔNG gen AI —
gen = bịa nguồn, vi phạm YMYL #2), pad nền TRẮNG về đúng tỉ lệ 1,60 của ô `art` (940×588),
khoanh đỏ vẽ trên ảnh GỐC trước khi crop/scale. Toạ độ đo bằng MẮT trên từng ảnh nguồn
(2026-08-19, phiên chụp claude-chrome-screenshots-eDVwrn + PDF render 200dpi).

3 shot:
  1. genten_01_kikou_kyuchi.png   — nenkin.go.jp 0617.html, bảng 級地区分ごとの非課税限度額
                                     (단身者), khoanh cột 65歳以上 (155/151.5/148)
  2. genten_02_mhlw_kyuchi.png    — mhlw kyuchi.3010.pdf: ghép 2 mảnh
                                     p2 【２級地－１】新潟市 + p4 header/p5 rows 【３級地－１】上越市
  3. genten_03_joetsu_kaigo.png   — city.joetsu hokenryou.html, bảng 第9期,
                                     khoanh hàng 第3段階 (39,500円) + 第6段階 (89,100円)

CHẠY:  python tools/ingest_genten_14.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SHOT = Path(r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-eDVwrn")
PDFPNG = Path(r"C:\Users\tuana\AppData\Local\Temp\claude\E--Claude"
              r"\1e769467-4266-4c9f-8771-300ab920986d\scratchpad")
OUT = PROJ / "06_VIDEO" / "14_juminzei-hikazei-sakaime-148man" / "art"
FONT = Path(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Bold.otf")

RED = (214, 40, 40)
NAVY = (26, 42, 74)
CW, CH = 1880, 1176          # canvas 2× ô art 940×588 (AR 1,5986) cho nét


def canvas():
    return Image.new("RGB", (CW, CH), (255, 255, 255))


def label(im, txt):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(FONT), 40)
    while f.getbbox(txt)[2] > CW - 120 and f.size > 24:
        f = ImageFont.truetype(str(FONT), f.size - 2)
    d.rectangle([0, CH - 92, CW, CH], fill=(244, 246, 250))
    d.text((CW / 2, CH - 46), txt, font=f, fill=NAVY, anchor="mm")


def boxed(src, crop, boxes, bw=8):
    """Vẽ khung đỏ (toạ độ ẢNH GỐC) rồi crop — khung không bao giờ lệch theo scale."""
    im = src.copy()
    d = ImageDraw.Draw(im)
    for b in boxes:
        d.rectangle(b, outline=RED, width=bw)
    return im.crop(crop)


def fit_into(cv, piece, box):
    """Scale piece lọt hộp (x0,y0,x1,y1) giữ tỉ lệ, canh giữa."""
    bx0, by0, bx1, by1 = box
    bw, bh = bx1 - bx0, by1 - by0
    sc = min(bw / piece.width, bh / piece.height)
    p = piece.resize((int(piece.width * sc), int(piece.height * sc)), Image.LANCZOS)
    cv.paste(p, (bx0 + (bw - p.width) // 2, by0 + (bh - p.height) // 2))


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # ── 1. 年金機構 — bảng 級地区分ごとの非課税限度額 ──────────────────────────────
    src = Image.open(SHOT / "screenshot-1787147990192-1.jpg").convert("RGB")
    piece = boxed(src, (360, 130, 1195, 500), [(880, 332, 1152, 464)])
    cv = canvas()
    fit_into(cv, piece, (60, 40, CW - 60, CH - 120))
    label(cv, "日本年金機構「令和8年度税制改正による公的年金等に係る主な改正事項」（2026年6月17日更新）")
    cv.save(OUT / "genten_01_kikou_kyuchi.png")

    # ── 2. 厚労省 PDF — 新潟市 (2級地-1, p2) + 上越市 (3級地-1, p4 header + p5 rows) ──
    p2 = Image.open(PDFPNG / "kyuchi_hi_p2.png").convert("RGB")
    p5 = Image.open(PDFPNG / "kyuchi_hi_p5.png").convert("RGB")
    # header 【３級地－１】 nằm ở p4 (đầu section); render riêng
    import pymupdf
    doc = pymupdf.open(str(PDFPNG / "kyuchi.3010.pdf"))
    pix = doc[3].get_pixmap(dpi=200)
    p4 = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # crop x0=412: bỏ cột 「市」 của column kề bên trái (soi sheet lần 1 thấy dính)
    headA = p2.crop((130, 140, 400, 200))                        # 【２級地－１】
    rowsA = boxed(p2, (412, 1750, 712, 1860), [(418, 1798, 700, 1848)])   # 新潟市 khoanh đỏ
    headB = p4.crop((130, 135, 400, 195))                        # 【３級地－１】
    rowsB = boxed(p5, (412, 393, 712, 600), [(418, 476, 700, 520)])       # 上越市 khoanh đỏ

    cv = canvas()
    mid = CW // 2
    fit_into(cv, headA, (140, 60, mid - 120, 190))
    fit_into(cv, rowsA, (100, 220, mid - 80, 900))
    fit_into(cv, headB, (mid + 120, 60, CW - 140, 190))
    fit_into(cv, rowsB, (mid + 80, 220, CW - 100, 980))
    d = ImageDraw.Draw(cv)
    d.line([mid, 60, mid, CH - 140], fill=(222, 226, 233), width=4)
    label(cv, "厚生労働省「お住まいの地域の級地」級地区分（平成30年10月1日現在）kyuchi.3010.pdf")
    cv.save(OUT / "genten_02_mhlw_kyuchi.png")

    # ── 3. 上越市 — bảng 第9期 介護保険料, khoanh 第3段階 + 第6段階 ────────────────
    src = Image.open(SHOT / "screenshot-1787148490773-2.jpg").convert("RGB")
    piece = boxed(src, (505, 60, 1298, 715),
                  [(512, 356, 1292, 447), (512, 623, 1292, 707)])
    cv = canvas()
    fit_into(cv, piece, (160, 30, CW - 160, CH - 116))
    label(cv, "上越市「介護保険料」第9期（令和6年度から令和8年度）・2026年4月1日更新")
    cv.save(OUT / "genten_03_joetsu_kaigo.png")

    for f in ("genten_01_kikou_kyuchi.png", "genten_02_mhlw_kyuchi.png",
              "genten_03_joetsu_kaigo.png"):
        print("  ✓", OUT / f)


if __name__ == "__main__":
    main()
