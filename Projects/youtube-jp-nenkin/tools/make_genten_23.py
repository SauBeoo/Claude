# -*- coding: utf-8 -*-
"""make_genten_23.py — dựng THẺ 原典 cho video 23 từ ảnh chụp trang gốc.

Nguồn: `06_VIDEO/23_.../genten_raw/*.png` (chụp bằng `chrome-headless-shell`, 2400px,
đã ĐỌC BẰNG MẮT 2026-09-12). Sổ URL + câu cần khoanh: `tools/_scenes23.py::GENTEN`.

🔴 BỐN LUẬT ĐÃ TRẢ GIÁ Ở VIDEO 13 / 22 — đừng phát minh lại:
 ① **Hộp khoanh phải SNAP vào ranh giới DÒNG CHỮ THẬT.** Đo mực theo hàng, lấy NỬA KHE
    trắng giữa hai dòng làm đệm. Padding đoán 6px đè lên chữ dòng dưới ở 2/2 thẻ đầu video 13.
    (Ở lô này khe đo được ~12px ⇒ nửa khe = 6px, trùng số cũ nhưng giờ là số ĐO, không phải đoán.)
 ② **Vùng cắt suy từ CHÍNH hộp khoanh**, không hằng số — cột nội dung mỗi trang rộng khác nhau;
    hằng số 990 làm 3/9 thẻ video 13 khoanh trượt ra ngoài khung.
 ③ **Trần upscale 1,60×.** Cắt hẹp rồi kéo 1920 là nhoè; thà chừa lề còn hơn phóng quá.
 ④ **`motion: "none"` cho MỌI chặng 原典** (việc của builder): thẻ dựng sẵn đúng 1920×1080 mà
    pan là CẮT MẤT BẰNG CHỨNG — mất chữ đầu mọi dòng, bắt được ở still frame 5760 video 22.
    Sự kiện hình của scene 原典 đến từ **đổi CHỖ KHOANH ĐỎ**, không từ pan.

⚠️ VÙNG CẤM của khung (3 overlay dán cứng + telop + phụ đề) — thẻ phải nằm trong khe an toàn:
    logo x1790–1900·y20–130 · mascot x1690–1910·y530–830 · SUBSCRIBE x20–260·y775–830
    telop band y0–210 · phụ đề y940–1020   ⇒ khe cho thẻ: **x 40–1640 · y 225–713**
    (Kiểm giao nhau bằng CẢ HAI trục: SUBSCRIBE là hình chữ nhật y775–830, không phải cột
     chạy hết khung — rút nó về "cột" là an toàn nhưng trả giá bằng 18,5% cỡ chữ.)

CHẠY:  python tools/make_genten_23.py          # dựng hết
       python tools/make_genten_23.py jidou    # chỉ một thẻ
"""
import io
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(PROJ, "06_VIDEO", "23_nenkin-seikyusho-todokanai", "genten_raw")
OUT = os.path.join(PROJ, "06_VIDEO", "23_nenkin-seikyusho-todokanai", "genten")

W, H = 1920, 1080
BOX = (40, 225, 1640, 713)          # khe an toàn cho thẻ, xem ghi chú vùng cấm
CREAM = (246, 242, 233)
AMBER = (200, 121, 30)              # ⚠️ hổ phách, KHÔNG đỏ — user chốt: bài nói về tiền ĐƯỢC
                                    #    NHẬN, không phải mối nguy (CLAUDE.md §②)
MAXUP = 1.60

# khoá: (file ảnh, [ (y_đầu_dòng, y_cuối_dòng) … ] các DÒNG cần khoanh)
# 🔴 Mốc dòng ĐO BẰNG MÁY từ chính ảnh (mực theo hàng), không gõ tay.
CARDS = {
    "soufu":      ("soufu.png",     [(438, 508)]),
    # 🔴 Mốc này bản đầu tao ĐOÁN (700,1000) ⇒ hộp khoanh trúng ô xám 令和8年, trượt khỏi
    #    bảng. Đo lại mực theo hàng: hàng 「最終記録が共済組合期間 → 共済組合から送付」 ở
    #    y 1089–1158. ⇒ luật ② không chỉ áp cho BỀ NGANG: mốc DỌC cũng phải đo, đừng ước.
    "kyosai":     ("soufu.png",     [(1089, 1158)]),  # bảng 送付パターン — 共済は共済から
    "kikou10":    ("kikou10.png",   [(414, 483)]),
    "saisoufu":   ("saisoufu.png",  [(525, 540)]),
    "michi3":     ("saisoufu.png",  [(552, 623)]),
    "jidou":      ("tokubetsu.png", [(438, 480)]),
    "zenjitsu":   ("tokubetsu.png", [(802, 844)]),
    "shorui":     ("tokubetsu.png", [(857, 898)]),
    "tokubetsu":  ("tokubetsu.png", [(965, 980)]),
    "horyu":      ("horyu.png",     [(593, 635)]),
    "kurisage":   ("horyu.png",     [(1050, 1175)]),
}


def ink_cols(a, y0, y1):
    """Mép trái/phải THẬT của mực trong dải dòng — vùng cắt suy từ đây (luật ②)."""
    band = a[y0:y1]
    col = (band < 150).sum(axis=0)
    nz = np.nonzero(col > 0)[0]
    return (int(nz[0]), int(nz[-1])) if len(nz) else (0, a.shape[1] - 1)


def snap(a, y0, y1):
    """Nới hộp ra NỬA KHE trắng trên/dưới — luật ①."""
    def gap(y, step):
        n = 0
        while 0 <= y + n * step < a.shape[0] and n < 40:
            if (a[y + n * step] < 150).sum() > 3:
                break
            n += 1
        return max(2, n // 2)
    return y0 - gap(y0 - 1, -1), y1 + gap(y1 + 1, 1)


def build(key, plain=False):
    """`plain=True` → đúng vùng cắt ấy nhưng CHƯA khoanh, ghi ra `genten_<key>_plain.png`.

    Dùng cho scene 原典 dài hơn 9,0s: chặng 1 là trang chưa khoanh (lúc lời đọc mới nói
    「機構のページです」), chặng 2 mới khoanh vào đúng câu — sự kiện hình đến từ **đổi chỗ
    khoanh**, không từ pan (luật ④). Vùng cắt vẫn suy từ hộp khoanh nên hai chặng khớp
    khung tuyệt đối, không xê dịch một pixel.
    """
    fn, lines = CARDS[key]
    src = Image.open(os.path.join(RAW, fn)).convert("RGB")
    a = np.array(src.convert("L"))

    boxes = []
    for y0, y1 in lines:
        sy0, sy1 = snap(a, y0, y1)
        x0, x1 = ink_cols(a, sy0, sy1)
        boxes.append((x0 - 14, sy0, x1 + 14, sy1))

    # ── vùng cắt suy từ chính hộp khoanh (luật ②) ──────────────────────────
    # 🔴 NHƯNG bề ngang phải lấy từ mực của TOÀN DẢI sắp cắt, không phải của riêng dòng được
    #    khoanh: dòng ngữ cảnh ở trên/dưới thường DÀI HƠN dòng khoanh ⇒ cắt theo dòng khoanh
    #    là xén cụt chúng. Đã dính ở thẻ `tokubetsu`: dòng đầu đứt giữa chữ 「…に限〜」.
    #    Mất chữ = mất bằng chứng, đúng thứ thẻ 原典 sinh ra để chống.
    by0 = min(b[1] for b in boxes); by1 = max(b[3] for b in boxes)
    pad_x, pad_y = 70, 54
    cy0, cy1 = max(0, by0 - pad_y), min(src.height, by1 + pad_y)
    bx0, bx1 = ink_cols(a, cy0, cy1)          # mực của CẢ dải, không chỉ dòng khoanh
    bx0 = min(bx0, min(b[0] for b in boxes)); bx1 = max(bx1, max(b[2] for b in boxes))
    cx0, cx1 = max(0, bx0 - pad_x), min(src.width, bx1 + pad_x)

    crop = src.crop((cx0, cy0, cx1, cy1))
    d = ImageDraw.Draw(crop)
    for x0, y0, x1, y1 in ([] if plain else boxes):
        d.rounded_rectangle([x0 - cx0, y0 - cy0, x1 - cx0, y1 - cy0],
                            radius=10, outline=AMBER, width=5)

    # ── fit vào khe an toàn, TRẦN 1,60× (luật ③) ───────────────────────────
    tw, th = BOX[2] - BOX[0], BOX[3] - BOX[1]
    k = min(tw / crop.width, th / crop.height, MAXUP)
    nw, nh = int(crop.width * k), int(crop.height * k)
    crop = crop.resize((nw, nh), Image.LANCZOS)

    card = Image.new("RGB", (W, H), CREAM)
    px = BOX[0] + (tw - nw) // 2
    py = BOX[1] + (th - nh) // 2
    card.paste(crop, (px, py))
    ImageDraw.Draw(card).rectangle([px - 2, py - 2, px + nw + 1, py + nh + 1],
                                   outline=(206, 198, 184), width=2)

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"genten_{key}{'_plain' if plain else ''}.png")
    card.save(p)
    warn = "  ⚠️ dưới trần phóng, thẻ chưa lấp hết khe" if k < 1.0 else ""
    print(f"  {key:<10} cắt {cx1-cx0}×{cy1-cy0} → ×{k:.2f} → {nw}×{nh}{warn}")
    return p


def main():
    plain = "--plain" in sys.argv
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(CARDS)
    print(f"dựng {len(keys)} thẻ 原典{' (bản CHƯA khoanh)' if plain else ''} → {OUT}")
    for k in keys:
        build(k, plain=plain)
    print("\n⚠️ BƯỚC BẮT BUỘC: soi 1:1 từng thẻ — hộp khoanh có đè chữ dòng dưới không,"
          "\n   chữ có đọc được ở 1920 không. Sheet thu nhỏ CHO QUA lỗi này.")


if __name__ == "__main__":
    main()
