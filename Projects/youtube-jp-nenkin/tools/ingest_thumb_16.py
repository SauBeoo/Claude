# -*- coding: utf-8 -*-
r"""ingest_thumb_16.py — nhận thumbnail T1 của video 16: cắt ✦ + ép 16:9.

⚖️ VÌ SAO CẮT MÀ KHÔNG VÁ (khác luật mặc định của `media-library.md` §2.10 ⑤b):
Luật nói thumbnail phải VÁ vì chữ hero thường chạy tới ~0,97W nên cắt là mất chữ. Ở ảnh NÀY
thì không: đo được hero rộng **69,9%** và kết thúc ở ~0,72W, còn ✦ ở **0,958W** — dư 0,2W
trống giữa chữ và dấu. Cắt phải tại 0,925W là sạch tuyệt đối, KHÔNG có vệt vá.
🔴 Và ở đây vá là lựa chọn TỆ: ✦ rơi đúng ranh giới tay áo hoạ tiết check + mặt bàn gỗ, tức
vùng CÓ VÂN — rule đã ghi patch trên nền vân để lại vệt chữ nhật (3/8 ảnh lô trước).

Lô 2752×1536: soi 1:1 thấy ĐÚNG MỘT dấu ở (0,958W · 0,926H). Mốc thứ hai mà rule ghi cho lô
2K, (0,930W · 0,890H), lô này KHÔNG có — ghi lại để lần sau khỏi đoán.

Cắt phải 0,925W ⇒ 2546px, rồi trim ĐÁY về đúng 16:9 (1432px) — trim đáy còn lợi kép vì phần
bị bỏ là dải giấy tờ dưới cùng, chỗ model in chữ Nhật giả nát nhất.

CHẠY:  python tools/ingest_thumb_16.py
"""
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\Downloads\Man_holding_bank_passbook_2K_202608251457.jpeg")
OUT = PROJ / "06_VIDEO" / "16_shotokuzei-12gatsu-seisan-kangen" / "thumb_T1_odoroki-ojiisan.png"
BAK = OUT.parent / "_thumb_orig"

EXPECT = (2752, 1536)
CUT_FX = 0.925          # mép phải: bỏ ✦ ở 0,958W, chừa lề an toàn


def main():
    if not SRC.exists():
        print(f"🔴 không thấy {SRC}")
        return
    im = Image.open(SRC).convert("RGB")
    if im.size != EXPECT:
        print(f"🔴 CHẶN: {im.size} ≠ lô {EXPECT} — toạ độ ✦ đo cho lô kia, soi lại bằng mắt")
        return
    BAK.mkdir(parents=True, exist_ok=True)
    if not (BAK / SRC.name).exists():
        im.save(BAK / SRC.name)
    w = int(im.width * CUT_FX)
    h = round(w / (16 / 9))
    im2 = im.crop((0, 0, w, h))          # cắt phải + trim đáy
    im2.save(OUT)
    print(f"  ✓ cắt phải tại {CUT_FX:.3f}W ({w}px, ✦ ở 0.958W đã ra ngoài)")
    print(f"  ✓ trim đáy về 16:9 → {im2.size[0]}×{im2.size[1]} = {im2.size[0]/im2.size[1]:.3f}")
    print(f"  → {OUT.name}")
    print("  ⛔ NGHIỆM THU: soi 1:1 cả 4 GÓC + soi TỪNG ký tự kanji (還/欄 dễ méo nhất)")


if __name__ == "__main__":
    main()
