# -*- coding: utf-8 -*-
r"""find_sparkles.py — DÒ watermark ✦ thay vì đoán bằng hộp cố định.

🔴 Vì sao phải viết cái này (bẫy dính 2026-08-05 ở video 08 緑茶):
    Cả co-dai và 9 bản shokutaku đầu đều có ✦ ở đúng một chỗ (~x2630 y1420 trên khung
    2752×1536), nên tao hard-code `WM_BOX`. Bản 08 gen ra ✦ ở **(2562,1332)** — lệch khỏi
    hộp → clone chạy vào chỗ trống, watermark còn nguyên, và **không có cảnh báo nào**:
    lệnh vẫn in "✦off(...)" như thành công. Vị trí ✦ KHÔNG cố định ⇒ phải dò.

Cách dò: ✦ là ngôi sao 4 cánh SÁNG HƠN nền, nằm trên vùng nền MỊN.
    ① trừ nền bằng median blur kernel lớn → còn lại vệt sáng cục bộ
    ② lọc theo diện tích + tỉ lệ cạnh (gần vuông) + độ đặc thấp (sao 4 cánh rỗng góc)
    ③ đòi vùng quanh nó phải MỊN (std thấp) → loại lá trà, hạt đậu, bọt sữa…
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_sparkles(im: Image.Image, quad=(0.80, 0.76), pad: int = 16) -> list[tuple[int, int, int, int]]:
    """Trả list box (x0,y0,x1,y1) của các ✦ tìm được ở góc dưới–phải khung.

    ⚠️ `quad` cố ý CHẶT (0.80, 0.76): mọi ✦ quan sát được ở cả co-dai và shokutaku đều nằm
    trong góc dưới–phải (source x≈94%, y≈90%). Nới quad ra giữa khung thì bộ lọc hình dạng
    bắt luôn **dương tính giả** — đã dính: đáy ly sữa (04) và điểm sáng trên lọ mật (09).
    Vá vào mấy chỗ đó là phá ảnh, tệ hơn để nguyên watermark.
    """
    a = np.array(im.convert("RGB"))
    H, W = a.shape[:2]
    ox, oy = int(W * quad[0]), int(H * quad[1])
    lum = cv2.cvtColor(a[oy:, ox:], cv2.COLOR_RGB2GRAY)
    bg = cv2.medianBlur(lum, 61)
    diff = cv2.subtract(lum, bg)
    m = cv2.morphologyEx((diff > 3).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for j in range(1, n):
        x, y, w, h, ar = (st[j, cv2.CC_STAT_LEFT], st[j, cv2.CC_STAT_TOP],
                          st[j, cv2.CC_STAT_WIDTH], st[j, cv2.CC_STAT_HEIGHT], st[j, cv2.CC_STAT_AREA])
        if not (500 <= ar <= 22000):
            continue
        if not (0.50 <= w / max(h, 1) <= 2.00):
            continue
        if ar / (w * h) > 0.88:            # sao 4 cánh rỗng 4 góc → độ đặc thấp
            continue
        # vùng quanh phải MỊN (loại lá trà / hạt / hoa văn)
        r = 26
        yy0, yy1 = max(0, y - r), min(lum.shape[0], y + h + r)
        xx0, xx1 = max(0, x - r), min(lum.shape[1], x + w + r)
        ring = lum[yy0:yy1, xx0:xx1].astype(np.float32).copy()
        ring[y - yy0:y - yy0 + h, x - xx0:x - xx0 + w] = np.nan
        if np.nanstd(ring) > 12.0:
            continue
        out.append((ox + x - pad, oy + y - pad, ox + x + w + pad, oy + y + h + pad))
    return out


def main() -> None:
    for f in sys.argv[1:]:
        p = Path(f)
        im = Image.open(p)
        bs = find_sparkles(im)
        print(f"{p.name}: {len(bs)} ✦ " + (", ".join(f"({b[0]},{b[1]})–({b[2]},{b[3]})" for b in bs) or "— sạch"))


if __name__ == "__main__":
    main()
