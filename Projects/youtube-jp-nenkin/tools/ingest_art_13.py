# -*- coding: utf-8 -*-
r"""ingest_art_13.py — nhận ảnh AI entry 0 của video 13: vá chữ nát → cắt ✦ → ép 1,60.

BA VIỆC, THEO ĐÚNG THỨ TỰ NÀY:

① 🔴 **VÁ CHỮ NHẬT NÁT trên tờ giấy xanh.** Prompt đã ghi `no characters written anywhere` mà
   model vẫn in 4 ký tự (2×2) ở ~(2168,388)–(2200,410). Đúng bẫy `media-library.md` §2.10 ⑤b
   mục 5: *"phong bì/giấy tờ rất hay bị model in chữ Nhật giả lên, và chữ đó LUÔN nát"*.
   ⚖️ Ở ĐÂY VÁ ĐƯỢC (khác ca thumbnail phải loại ảnh): vùng chữ nằm trên **giấy trơn**, không
   đè lên nét chữ nào cần giữ, và cách đường kẻ ngang 2px — nên dựng lại nền là sạch tuyệt đối.
   Cách vá = **trung vị TỪNG HÀNG** lấy từ hai dải giấy trơn hai bên + nhiễu ±1,2 (giống
   `youtube-jp-shokutaku/tools/strip_wm_thumb.py`) — copy khối texture bên cạnh thì ra vệt.

② **CẮT WATERMARK ✦ — soi bằng MẮT, không dò bằng máy** (§2.10 ⑤: máy trượt 4/4 ở ảnh có chữ,
   7/8 ở lô nền kem). Đã soi 1:1 cả 4 góc: lô 2752×1536 này có **ĐÚNG MỘT** dấu, ở
   **(0,960W · 0,925H)** — khớp mốc `(0,958W · 0,926H)` mà rule ghi cho lô 2K, và **không** có
   dấu thứ hai ở (0,930W · 0,890H) như rule cảnh báo. Ghi lại để lô sau khỏi đoán.

③ **ÉP TỈ LỆ 1,60** (ô ảnh của layout `art` = 940×588). Cắt `x 0..2458` vừa bỏ ✦ (ở 2643) vừa
   ra đúng 2458×1536 = 1,600. ⚠️ Mất ~1/3 bề phải của phong bì TRẮNG; phong bì XANH (chủ thể
   thật, tờ 通知書) và cuốn 通帳 còn nguyên. Đánh đổi có chủ ý: model không tuân câu "chừa 15%
   bên phải trống" trong prompt (§2.10 ⑥ — model nghe VỊ TRÍ, không nghe TỈ LỆ).

CHẠY:  python tools/ingest_art_13.py            # xử lý + ghi vào 06_VIDEO/.../art/
       python tools/ingest_art_13.py --restore   # trả lại bản gốc từ _wm_orig/
"""
import random
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\Downloads\Japanese_bank_passbook_on_table_202608172137.jpeg")
VDIR = PROJ / "06_VIDEO" / "13_izoku-nenkin-tsuki13man9sen"
OUT = VDIR / "art" / "art_tsucho_tsuuchi.png"
BAK = VDIR / "art" / "_wm_orig"

EXPECT = (2752, 1536)          # lô này; ảnh khác cỡ ⇒ toạ độ ✦ khác ⇒ CHẶN
TXT = (2162, 384, 2206, 412)   # ô chứa 4 ký tự nát (đã nới lề 6px, chưa chạm đường kẻ)
SIDE = 46                      # bề rộng dải giấy trơn lấy mẫu ở hai bên
CUT_W = 2458                   # 2458×1536 = 1,600 và bỏ ✦ ở x=2643


def patch_text(im):
    """Dựng lại nền giấy theo TRUNG VỊ TỪNG HÀNG — giấy là gradient mịn theo chiều dọc."""
    px = im.load()
    x0, y0, x1, y1 = TXT
    rnd = random.Random(13)
    for y in range(y0, y1):
        samp = [px[x, y] for x in range(x0 - SIDE, x0 - 4)] + \
               [px[x, y] for x in range(x1 + 4, x1 + SIDE)]
        samp.sort(key=lambda c: c[0] + c[1] + c[2])
        med = samp[len(samp) // 2]
        for x in range(x0, x1):
            px[x, y] = tuple(max(0, min(255, med[i] + int(rnd.uniform(-1.2, 1.2))))
                             for i in range(3))
    return im


def main():
    (VDIR / "art").mkdir(parents=True, exist_ok=True)
    BAK.mkdir(parents=True, exist_ok=True)
    if "--restore" in sys.argv:
        b = BAK / SRC.name
        if b.exists():
            Image.open(b).save(OUT)
            print(f"↩ trả lại bản gốc → {OUT.name}")
        else:
            print("🔴 không có backup trong _wm_orig/")
        return
    if not SRC.exists():
        print(f"🔴 không thấy {SRC}")
        return
    im = Image.open(SRC).convert("RGB")
    if im.size != EXPECT:
        print(f"🔴 CHẶN: ảnh {im.size} ≠ lô {EXPECT} — toạ độ ✦ và ô chữ đo cho lô kia, "
              f"soi lại bằng mắt rồi sửa EXPECT/TXT trước khi chạy")
        return
    if not (BAK / SRC.name).exists():
        im.save(BAK / SRC.name)          # backup bản THÔ, không ghi đè
    before = im.crop(TXT).convert("L")
    im = patch_text(im)
    after = im.crop(TXT).convert("L")
    sd_b = (max(before.getdata()) - min(before.getdata()))
    sd_a = (max(after.getdata()) - min(after.getdata()))
    im = im.crop((0, 0, CUT_W, im.height))
    im.save(OUT)
    print(f"  ✓ vá chữ: biên độ sáng trong ô {sd_b} → {sd_a} (càng nhỏ càng phẳng)")
    print(f"  ✓ cắt ✦ + ép tỉ lệ: {im.size[0]}×{im.size[1]} = {im.size[0]/im.size[1]:.3f} (cần 1,599)")
    print(f"  → {OUT}")
    print(f"  ⛔ NGHIỆM THU: soi 1:1 ô chữ đã vá + cả 4 GÓC. Sheet thu nhỏ CHO QUA ✦.")


if __name__ == "__main__":
    main()
