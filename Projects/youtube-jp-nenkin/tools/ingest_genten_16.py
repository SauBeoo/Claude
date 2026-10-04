# -*- coding: utf-8 -*-
r"""ingest_genten_16.py — dựng 2 原典ショット cho video 16 + khoanh ĐỎ + nhãn nguồn.

Khuôn chép từ `ingest_genten_14.py`: nguồn là SCREENSHOT/asset trang cơ quan công (KHÔNG gen
AI), canvas trắng 1880×1176 = 2× ô `art` 940×588 (AR 1,60), nhãn nguồn ở đáy.

Nguồn (verify nguyên văn 2026-08-24, trang còn sống):
  nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html (更新日 2026-06-17)
  - screenshot đầu trang (logo + H1 + 更新日): claude-chrome-screenshots-vp3Qgp\screenshot-...-1.jpg
  - screenshot đoạn 11月/12月精算 (zoom 1.6):   claude-chrome-screenshots-vp3Qgp\screenshot-...-0.jpg
  - hình ví dụ chính thức 6,000→4,600→還付:      0617.images/1.png (tải thẳng, 960×284)

2 shot:
  1. genten_01_kikou_seisan.png — logo+tiêu đề trang + đoạn 「令和8年11月まで改正前…12月に精算」
                                   khoanh đỏ cả đoạn (FACT #2)
  2. genten_02_kikou_rei.png    — hình ví dụ của 機構, khoanh đỏ cột 4,600円 (R8.12) +
                                   ô 精算後の還付額2,400円 (FACT #3)

CHẠY:  python tools/ingest_genten_16.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SHOT = Path(r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-vp3Qgp")
SCRATCH = Path(r"C:\Users\tuana\AppData\Local\Temp\claude\E--Claude"
               r"\1dead2fa-3ab7-457a-909f-6d82e7747576\scratchpad")
OUT = PROJ / "06_VIDEO" / "16_shotokuzei-12gatsu-seisan-kangen" / "art"
FONT = Path(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Bold.otf")

SS_PARA = SHOT / "screenshot-1787564841025-0.jpg"   # đoạn 精算 (zoom 1.6)
SS_HEAD = SHOT / "screenshot-1787564914555-1.jpg"   # đầu trang (logo + H1 + 更新日)
FIG = SCRATCH / "kikou_rei_1.png"                    # 0617.images/1.png 960×284

RED = (214, 40, 40)
NAVY = (26, 42, 74)
CW, CH = 1880, 1176
LABEL = "出典：日本年金機構「令和8年度税制改正による公的年金等に係る主な改正事項」（2026年6月17日更新）"


def canvas():
    return Image.new("RGB", (CW, CH), (255, 255, 255))


def label(im):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(FONT), 40)
    while f.getbbox(LABEL)[2] > CW - 120 and f.size > 24:
        f = ImageFont.truetype(str(FONT), f.size - 2)
    d.rectangle([0, CH - 92, CW, CH], fill=(244, 246, 250))
    d.text((CW / 2, CH - 46), LABEL, font=f, fill=NAVY, anchor="mm")


def fit_w(piece, w):
    return piece.resize((w, round(piece.height * w / piece.width)), Image.LANCZOS)


def shot01():
    head = Image.open(SS_HEAD).convert("RGB")
    logo = head.crop((112, 40, 492, 132))            # logo 日本年金機構
    title = head.crop((110, 330, 1450, 535))         # H1 + gạch cam + ページID/更新日
    para = Image.open(SS_PARA).convert("RGB").crop((95, 282, 1445, 418))  # đoạn 精算

    cv = canvas()
    lg = fit_w(logo, 640)
    tt = fit_w(title, 1720)
    pa = fit_w(para, 1720)
    # chia đều khe dọc trong vùng trên nhãn (CH-92) — thẻ 2 khối thì không thể cân (stage-zu §2)
    free = (CH - 92) - (lg.height + tt.height + pa.height)
    gap = free // 4
    cv.paste(lg, (80, gap))
    cv.paste(tt, (80, gap + lg.height + gap))
    y_para = gap + lg.height + gap + tt.height + gap
    cv.paste(pa, (80, y_para))
    d = ImageDraw.Draw(cv)
    d.rectangle([68, y_para - 14, 80 + pa.width + 12, y_para + pa.height + 14],
                outline=RED, width=10)
    label(cv)
    cv.save(OUT / "genten_01_kikou_seisan.png")
    print(f"  ✓ genten_01_kikou_seisan.png  (para {pa.width}×{pa.height} @y={y_para})")


def shot02():
    fig = Image.open(FIG).convert("RGB")
    d = ImageDraw.Draw(fig)
    # toạ độ trên ảnh gốc 960×284, đo mắt 2026-08-24
    d.rectangle([770, 122, 842, 236], outline=RED, width=5)   # cột 4,600円 (R8.12)
    d.rectangle([848, 84, 952, 146], outline=RED, width=5)    # 精算後の還付額 2,400円
    cv = canvas()
    fg = fit_w(fig, 1800)
    y = (CH - 92 - fg.height) // 2
    cv.paste(fg, (40, y))
    label(cv)
    cv.save(OUT / "genten_02_kikou_rei.png")
    print(f"  ✓ genten_02_kikou_rei.png  (fig {fg.width}×{fg.height} @y={y})")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (SS_PARA, SS_HEAD, FIG):
        if not p.exists():
            print(f"🔴 thiếu nguồn: {p}")
            return
    shot01()
    shot02()
    print("  ⛔ NGHIỆM THU: soi 1:1 — khung đỏ đúng chỗ, chữ đọc được, không cắt cụt.")


if __name__ == "__main__":
    main()
