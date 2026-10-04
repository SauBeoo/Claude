# -*- coding: utf-8 -*-
r"""ingest_genten_18.py — dựng 3 原典ショット cho video 18 (khoanh ĐỎ + nhãn nguồn).

Khuôn chép từ `ingest_genten_16.py`: nguồn là SCREENSHOT thật của trang cơ quan công
(KHÔNG gen AI), canvas trắng, khoanh đỏ ô/dòng cần chỉ, nhãn nguồn ở đáy.

Nguồn (verify nguyên văn 2026-08-29, trang còn sống, browser session này đã mở tận nơi):
  nenkin.go.jp/service/jukyu/seido/roureinenkin/kuriage-kurisage/20140421-01.html (更新日 2024-08-19)
  nenkin.go.jp/service/jukyu/seido/roureinenkin/kuriage-kurisage/20140421-02.html (更新日 2026-08-12)

3 shot (khớp FACT SHEET script 18):
  genten_01_kuriage_gengaku.png — 2 bảng 減額率早見表, khoanh đỏ dòng 60歳=24.0% (FACT #1)
  genten_02_kuriage_chuiten.png — 13 dòng 繰上げ請求の注意点, khoanh dòng 3 (取消し) + dòng 11 (障害年金)
  genten_03_kurisage.png        — bảng 増額率早見表 (khoanh 70歳=42.0%) + dòng 1 注意点 (加給年金)

CHẠY:  python tools/ingest_genten_18.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SHOT = Path(r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-c3x9ye")
OUT = PROJ / "06_VIDEO" / "18_nenkin-60sai-kuriage-tsuki4man3sen" / "art"
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Bold.otf")

RED = (214, 40, 40)
NAVY = (26, 42, 74)
CW = 1880

S2 = SHOT / "screenshot-1788020338045-2.jpg"   # shot1: 2 bảng 減額率早見表
S3 = SHOT / "screenshot-1788020421639-3.jpg"   # shot2: 13 dòng 注意点(繰上げ)
S6 = SHOT / "screenshot-1788020672719-6.jpg"   # shot3a: bảng 増額率早見表
S7 = SHOT / "screenshot-1788020761058-7.jpg"   # shot3b: 繰下げの注意点(dòng1=加給年金)

LABEL1 = "出典：日本年金機構「年金の繰上げ受給」（2024年8月19日更新）"
LABEL2 = LABEL1
LABEL3 = "出典：日本年金機構「年金の繰下げ受給」（2026年8月12日更新）"


def font_fit(text, size, maxw):
    f = ImageFont.truetype(str(FONT), size)
    while f.getbbox(text)[2] > maxw and f.size > 24:
        f = ImageFont.truetype(str(FONT), f.size - 2)
    return f


def canvas(h):
    return Image.new("RGB", (CW, h), (255, 255, 255))


def paste_fit(im, piece_box, x, y, w):
    piece = im.crop(piece_box)
    h = round(piece.height * w / piece.width)
    piece = piece.resize((w, h), Image.LANCZOS)
    return piece, h


def circle(d, box, width=6):
    d.rounded_rectangle(box, radius=10, outline=RED, width=width)


def label_bar(im, y0, h, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, y0, CW, y0 + h], fill=(244, 246, 250))
    f = font_fit(text, 38, CW - 120)
    d.text((CW / 2, y0 + h / 2), text, font=f, fill=NAVY, anchor="mm")


def build_shot1():
    """2 bảng 減額率早見表 — khoanh dòng 60歳=24.0% của bảng 昭和37年4月2日以降."""
    im = Image.open(S2).convert("RGB")
    piece, ph = paste_fit(im, (368, 165, 1188, 730), 60, 40, CW - 120)
    im2 = canvas(ph + 40 + 90)
    im2.paste(piece, (60, 40))
    d = ImageDraw.Draw(im2)
    scale = (CW - 120) / (1188 - 368)
    # dòng "60歳 24.0%" của bảng dưới (bảng 昭和37年4月2日以降) trong ảnh gốc y≈555..585,
    # x của cột 割合 (giá trị) x≈960..1145 — đo trên screenshot gốc (đã soát bằng mắt).
    bx0, by0 = 368 + (960 - 368), 555
    bx1, by1 = 368 + (1150 - 368), 590
    rx0 = 60 + (bx0 - 368) * scale
    ry0 = 40 + (by0 - 165) * scale
    rx1 = 60 + (bx1 - 368) * scale
    ry1 = 40 + (by1 - 165) * scale
    circle(d, [rx0, ry0, rx1, ry1])
    label_bar(im2, ph + 40, 90, LABEL1)
    im2.save(OUT / "genten_01_kuriage_gengaku.png")
    print("✓ genten_01_kuriage_gengaku.png", im2.size)


def build_shot2():
    """13 dòng 繰上げ請求の注意点 — khoanh dòng 3 (取消し) và dòng 11 (障害年金)."""
    im = Image.open(S3).convert("RGB")
    piece, ph = paste_fit(im, (368, 55, 1188, 640), 60, 40, CW - 120)
    im2 = canvas(ph + 40 + 90)
    im2.paste(piece, (60, 40))
    d = ImageDraw.Draw(im2)
    scale = (CW - 120) / (1188 - 368)

    def draw_line(y0, y1):
        rx0 = 60
        rx1 = CW - 60
        ry0 = 40 + (y0 - 55) * scale
        ry1 = 40 + (y1 - 55) * scale
        circle(d, [rx0, ry0, rx1, ry1])

    draw_line(214, 250)   # dòng 3: 取消しすることはできません
    draw_line(524, 550)   # dòng 11: 障害基礎（厚生）年金を請求することができません
    label_bar(im2, ph + 40, 90, LABEL2)
    im2.save(OUT / "genten_02_kuriage_chuiten.png")
    print("✓ genten_02_kuriage_chuiten.png", im2.size)


def build_shot3a():
    """Bảng 増額率早見表 — khoanh 70歳=42.0%. Canvas NGANG (~1.6) để vừa hero box 1132×760.
    Lý do tách 2 card (2026-08-30): bản gộp cao 1861px → fit bề ngang là tràn xuống phụ đề;
    và lời ở L=83 (「七十歳まで待てば42%」) với L=87–89 (加給年金 dòng 1) là HAI ý khác nhau."""
    im6 = Image.open(S6).convert("RGB")
    # cắt bảng: từ heading 繰下げ増額率早見表 tới hết dòng 72歳 (bỏ 73–75 cho vừa khổ ngang)
    # x1=958: bỏ mũi tên chuột lọt ở mép phải screenshot (đã thấy khi soi 1:1); y1=620 dừng ở 72歳
    piece, ph = paste_fit(im6, (440, 270, 958, 620), 60, 40, CW - 120)
    im2 = canvas(ph + 40 + 90)
    im2.paste(piece, (60, 40))
    d = ImageDraw.Draw(im2)
    scale6 = (CW - 120) / (958 - 440)
    rx0 = 60 + (820 - 440) * scale6
    rx1 = 60 + (950 - 440) * scale6
    ry0 = 40 + (500 - 270) * scale6
    ry1 = 40 + (530 - 270) * scale6
    circle(d, [rx0, ry0, rx1, ry1])
    label_bar(im2, ph + 40, 90, LABEL3)
    im2.save(OUT / "genten_03_kurisage.png")
    print("✓ genten_03_kurisage.png", im2.size)


def build_shot3b():
    """繰下げの注意点 heading + dòng 1 (加給年金額…受け取ることができません) khoanh đỏ."""
    im7 = Image.open(S7).convert("RGB")
    piece, ph = paste_fit(im7, (368, 45, 1188, 330), 60, 40, CW - 120)
    im2 = canvas(ph + 40 + 90)
    im2.paste(piece, (60, 40))
    d = ImageDraw.Draw(im2)
    scale7 = (CW - 120) / (1188 - 368)
    ry0 = 40 + (150 - 45) * scale7
    ry1 = 40 + (188 - 45) * scale7
    circle(d, [60, ry0, CW - 60, ry1])
    label_bar(im2, ph + 40, 90, LABEL3)
    im2.save(OUT / "genten_03b_kakyu.png")
    print("✓ genten_03b_kakyu.png", im2.size)


def main():
    build_shot1()
    build_shot2()
    build_shot3a()
    build_shot3b()
    return 0


if __name__ == "__main__":
    sys.exit(main())
