# -*- coding: utf-8 -*-
r"""ingest_genten_20.py — 5 the 原典 THAT cua video 20.

Chup truc tiep bang Claude in Chrome tren trang da VERIFY:
  https://www.nenkin.go.jp/service/jukyu/seido/izokunenkin/jukyu-yoken/20150424.html
Khoanh do duoc ve NGAY TREN TRANG (inject outline) roi moi chup — khong ve khung
sau bang PIL, nen khong co rui ro lech bbox.

⚠️ Anh goc chi ton tai TAM trong Temp cua phien chup => script nay khong chay lai
   duoc nguyen xi cho video sau. Giu lam MAU QUY TRINH:
     inject outline do -> scrollIntoView -> screenshot / zoom(region) -> ingest

5 THE:
  genten20_01   header trang (logo 日本年金機構 + breadcrumb + tieu de + 更新日)
  genten20_02   muc「遺族厚生年金の年金額」, khoanh do ca khoi
  genten20_03   can canh cau 「…報酬比例部分の4分の3の額となります」
  genten20_04   muc「65歳以上…」 khoanh do + so do 支給/支給停止 cua chinh 年金機構
  genten20_05   can canh cau 併給 + so do

🔴 KHOI 原典 KHONG dinh luat "chu phai mo": no la BANG CHUNG, phai DOC DUOC.
   Vi vay khong crop mep, khong lam mo, khong ha do tuong phan.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "20_izoku-nenkin-yonbunno-san")
SRC = r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-auFRLo"
OUT = os.path.join(VD, "genten")

W, H = 1920, 1080
BG = (247, 243, 236)      # kem am — palette nenkin
EDGE = (206, 196, 180)

# 🔴 LO 2 (chup lai 2026-09-03) — user bat: *"anh screenshot dang chup mat chu"*.
#    Lo 1 dat `document.body.zoom = 1.1` => noi dung ~1070px + thanh cuon doc 17px
#    TRAN viewport 1097 => sinh thanh cuon NGANG va **cat mat chu o mep phai**.
#    Lo 2: zoom = 1 va cua so rong 1920 => docW 1905 < vw 1920, khong tran, va con
#    duoc chup o dung do phan giai goc (khoi phong len 1,75x nhu lo 1).
#    ⇒ Bai hoc: sau khi inject zoom, PHAI kiem `scrollWidth > innerWidth` truoc khi chup.
SHOTS = [
    ("screenshot-1788448716979-6.jpg", "genten20_01"),    # header trang
    ("screenshot-1788448735805-7.jpg", "genten20_02"),    # muc 年金額 + khung do
    ("screenshot-1788448840336-9.png", "genten20_03"),    # can canh cau 4分の3
    ("screenshot-1788448858796-10.jpg", "genten20_04"),   # muc 65歳以上 + so do
    ("screenshot-1788448905799-11.png", "genten20_05"),   # can canh + so do
]


def card(src, dst):
    im = Image.open(src).convert("RGB")
    # chua 8% le moi ben; anh RONG-THAP (zoom) thi fit theo BE NGANG va canh giua
    maxw, maxh = int(W * 0.90), int(H * 0.86)
    r = min(maxw / im.width, maxh / im.height)
    im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))),
                   Image.LANCZOS)
    cv = Image.new("RGB", (W, H), BG)
    x, y = (W - im.width) // 2, (H - im.height) // 2
    # vien mong cho to giay tach khoi nen
    fr = Image.new("RGB", (im.width + 6, im.height + 6), EDGE)
    cv.paste(fr, (x - 3, y - 3))
    cv.paste(im, (x, y))
    cv.save(dst, quality=95)
    return im.size


def main():
    os.makedirs(OUT, exist_ok=True)
    miss = 0
    for fn, name in SHOTS:
        s = os.path.join(SRC, fn)
        if not os.path.exists(s):
            print(f"  THIEU nguon: {fn}")
            miss += 1
            continue
        d = os.path.join(OUT, name + ".png")
        w, h = card(s, d)
        print(f"  {name}.png  <- {fn}  (anh {w}x{h} tren the {W}x{H})")
    print(("XONG: " if not miss else f"THIEU {miss} anh — ") + OUT)
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
