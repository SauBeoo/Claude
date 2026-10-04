# -*- coding: utf-8 -*-
"""
make_genten_22.py — bộ thẻ 原典 scene 13 video 22 (bảng 支払月/支払対象月, 日本年金機構).

Xuất **4 bản** của cùng một trang, khác nhau ở CHỖ KHOANH ĐỎ — để scene 21,1s chạy thành
một chuỗi tiết lộ thay vì một tấm đứng im:

  | file                      | khoanh gì                | ăn với câu nào                       |
  |---------------------------|--------------------------|--------------------------------------|
  | `genten_shiharai.png`     | (không khoanh)           | 「こちらが、日本年金機構のページです」   |
  | `genten_shiharai_all.png` | cả bảng                  | 「赤で囲んだところを、ご覧ください」     |
  | `genten_shiharai_col.png` | cột 年金の支払月          | 「年六回…偶数月の十五日に支払われます」 |
  | `genten_shiharai_row.png` | hàng 4月 → 2月、3月分     | 「前月までの二か月分の年金が…」        |

🔴 VÌ SAO KHÔNG DÙNG ZOOM để tạo sự kiện: ảnh nguồn chỉ rộng 1400px, cắt hẹp rồi kéo lên
   1920 là 2,8× ⇒ chữ nhoè. Đổi CHỖ KHOANH thì giữ nguyên khung, không upscale thêm một
   pixel nào, mà vẫn là thay đổi hình THẬT (không phải cắt lại cùng một tấm để lừa phép
   đếm sự kiện của gate).

🔴🔴 THẺ DỰNG THEO TOẠ ĐỘ CUỐI, KHÔNG "CẮT 16:9 RỒI ĐỂ NÓ LẤP KHUNG" (sửa 2026-09-10 sau
   khi soi still frame 2052). Bản đầu cắt 16:9 rồi `fit: cover`, và **hai chỗ đè**:
     · dải credit đặt y 966–1016 ⇒ **đè thẳng lên phụ đề** (phụ đề chiếm y≈940–1020);
     · bảng chạy sát mép trái ⇒ **nút SUBSCRIBE (x 20–260 · y 775–830) che ô 「12月」**.
   ⇒ Khung 1920×1080 này đã có **3 overlay dán cứng** của khuôn video 22, phải coi chúng là
     vùng CẤM ngay lúc dựng thẻ, đừng phát hiện lại trên bản render:
        logo       x 1790–1900 · y   20–130
        mascot     x 1642–1905 · y  530–830   (CU — rong hon ong gia 48px)
        SUBSCRIBE  x   20– 260 · y  775–830
        telop band            y    0–210
        phụ đề                y  940–1020
   ⇒ Bảng đặt trong hộp **x 275–1625 · y 245–666**, credit ở **y 700–750, x 285** — lọt
     đúng khe giữa SUBSCRIBE và phụ đề.

⏳ **VIỆC CÒN MỞ — hộp trên đang SIẾT QUÁ TAY, bảng có thể to hơn ~18%.** Nhận ra 2026-09-10
   sau khi đã render: tao coi 5 vùng cấm như **CỘT/DẢI chạy hết khung**, nhưng chúng là
   **HÌNH CHỮ NHẬT**. Cụ thể `SUBSCRIBE` ở **y 775–830**, mà bảng chỉ chiếm **y 245–657** —
   **hai thứ không giao nhau theo chiều dọc**, nên `OX = 275` (đặt để né x<260 của SUBSCRIBE)
   là vô cớ.
   ⇒ Bảng lẽ ra đặt được ở **x 40–1640 · y 225–713** (rộng 1600 thay vì 1350 = **+18,5%**,
     chữ trong ảnh chụp to lên đúng tỉ lệ đó — đáng kể với tệp 45+), credit dời xuống
     **y 720–768 · x 300** (phải ≥300 để né x-range của SUBSCRIBE khi hai thứ CÓ giao dọc).
   📌 Bài học: **kiểm giao nhau bằng CẢ HAI trục.** Rút một vùng cấm về "cột chạy hết chiều
     cao" là an toàn nhưng trả giá bằng chỗ — và ở đây giá là 18,5% cỡ chữ của bằng chứng
     原典, tức đúng thứ bài này bán.
   ⚠️ Sửa được ngay bằng `DEST_W = 1600` + `OX = 40` + `OY = 225` + credit `y 720`, nhưng
     **phải render lại video** mới thấy ⇒ chờ chốt, đừng đổi lặng lẽ.
⚖️ YMYL: bản cắt không còn logo 日本年金機構 nên baked dòng credit nguồn.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
SRC = os.path.join(VD, "_genten", "v_shiharai.png")
OUT = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-22i2v\assets"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Medium.otf"

# ── dòng kẻ ĐO bằng máy trên v_shiharai.png (ngưỡng <238, đếm pixel/hàng) ────
TAB_X = (200, 1149)          # mép trái/phải bảng
COL_X = 686                  # vách giữa 2 cột
TAB_Y = (179, 460)           # dòng kẻ đỉnh/đáy bảng
ROW4_Y = (259, 300)          # hàng 「4月 | 2月、3月分」

# vùng cắt quanh bảng (nới 6px cho lọt nét viền) + chỗ đặt trên khung cuối
CROP = (194, 173, 1155, 466)
DEST_W = 1350
OX, OY = 275, 245
CANVAS = (1920, 1080)
BG = (243, 234, 216)         # = theme.canvasColor, để thẻ hoà với scene khối chữ
RED = (214, 45, 32)
CREDIT = "出典：日本年金機構「年金の支払月と支払対象月」"

VARIANTS = {                 # tên file → hộp khoanh trong hệ ảnh NGUỒN (None = không khoanh)
    "genten_shiharai.png":     None,
    "genten_shiharai_all.png": (TAB_X[0], TAB_Y[0], TAB_X[1], TAB_Y[1]),
    "genten_shiharai_col.png": (TAB_X[0], TAB_Y[0], COL_X, TAB_Y[1]),
    "genten_shiharai_row.png": (TAB_X[0], ROW4_Y[0], TAB_X[1], ROW4_Y[1]),
}


def main() -> int:
    base = Image.open(SRC).convert("RGB")
    block = base.crop(CROP)
    sc = DEST_W / block.width
    bw, bh = DEST_W, int(round(block.height * sc))
    block = block.resize((bw, bh), Image.LANCZOS)

    # kiểm hộp đặt không lấn 3 overlay — gate tại chỗ, đừng để phát hiện trên bản render
    if OX < 270 or OX + bw > 1630 or OY < 220 or OY + bh > 690:
        print(f"🔴 hộp bảng ({OX},{OY})–({OX+bw},{OY+bh}) ra ngoài khe an toàn "
              f"x 270–1630 · y 220–690 — sẽ bị overlay che")
        return 1

    f = ImageFont.truetype(FONT, 30)
    for name, hb in VARIANTS.items():
        card = Image.new("RGB", CANVAS, BG)
        card.paste(block, (OX, OY))
        d = ImageDraw.Draw(card)
        # viền mảnh cho khối trông như một mảnh trang giấy dán lên, không phải trôi lơ lửng
        d.rectangle([OX - 2, OY - 2, OX + bw + 1, OY + bh + 1], outline=(206, 198, 182), width=2)
        if hb:
            x0 = OX + (hb[0] - CROP[0]) * sc - 3
            y0 = OY + (hb[1] - CROP[1]) * sc - 2
            x1 = OX + (hb[2] - CROP[0]) * sc + 3
            y1 = OY + (hb[3] - CROP[1]) * sc + 2
            for w in (6, 5):
                d.rounded_rectangle([x0 - w // 2, y0 - w // 2, x1 + w // 2, y1 + w // 2],
                                    radius=9, outline=RED, width=w)
        # credit: khe giữa SUBSCRIBE (đáy 830 nhưng x<260) và phụ đề (đỉnh 940)
        tw = d.textlength(CREDIT, font=f)
        d.rectangle([OX + 10, 700, OX + 10 + tw + 36, 750], fill=(28, 42, 74))
        d.text((OX + 28, 710), CREDIT, font=f, fill=(255, 255, 255))
        card.save(os.path.join(OUT, name))
        print(f"  ✓ {name:<26} khoanh {hb if hb else '(không)'}")

    print(f"\n✅ {len(VARIANTS)} thẻ vào {OUT}")
    print(f"   bảng {bw}×{bh} tại ({OX},{OY}) — scale {sc:.3f}× từ nguồn, không upscale quá")
    print(f"   né: logo · mascot(x1642+,y530+) · SUBSCRIBE(x<260,y775+) · telop(y<210) "
          f"· phụ đề(y>940)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
