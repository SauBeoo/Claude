# -*- coding: utf-8 -*-
"""
harden_mascot.py — chữa "mascot trông như bóng ma" (user 2026-09-09).

🔴 NGUYÊN NHÂN đo được, không phải cảm giác: lô PNG do `mascot_chroma.py` xuất ra có
   **9.939 pixel BÁN TRONG SUỐT** trên 72.028 pixel đặc (13,8%). Chúng nằm thành một
   vành mềm quanh mép — nặng nhất ở gấu áo len và cánh tay trái, chỗ `y=277` có
   **semi 66 > solid 58**. Trên nền kem của khung, vành mềm đó đọc ra thành **quầng
   sương**, tức đúng cái user gọi là bóng ma.

⇒ Cách chữa: **NHỊ PHÂN HOÁ alpha** rồi **co 1px**.
   · ngưỡng 140: pixel nào chắc chắn thuộc nhân vật thì đặc hẳn, còn lại bỏ hẳn —
     không còn dải chuyển tiếp để mắt đọc ra sương.
   · co 1px: vành ngoài cùng luôn là pixel đã nhiễm màu nền, giữ lại là còn viền.
     (Cùng bài học `media-library.md` §2.10 ⑨②: *suy màu từ chính pixel đã nhiễm thì
     không bao giờ sạch — phải CO MASK vào trong.*)

⚠️ Việc này KHÔNG khôi phục được phần thân dưới: nguồn green-screen vốn chỉ có nửa
   người. Sau khi làm cứng mép, nó đọc ra là **ảnh cắt dán nửa thân** — bình thường
   với mascot góc khung — thay vì một bóng mờ đang tan.

    python tools/harden_mascot.py            # xử lý cả 3 bộ tư thế
"""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-22d2\assets"
POSES = ("ojii_13", "ojii_14", "ojii_15")
THRESH = 140          # dưới ngưỡng = nền, trên = nhân vật
ERODE = 1             # số pixel co vào để cắt vành đã nhiễm màu nền


def erode_mask(m: np.ndarray, n: int) -> np.ndarray:
    """Co mask n pixel bằng phép AND 4 hướng — không cần scipy/cv2."""
    for _ in range(n):
        p = np.pad(m, 1, mode="constant", constant_values=False)
        m = (p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])
    return m


def main() -> int:
    tot_before = tot_after = n_file = 0
    for pose in POSES:
        d = os.path.join(BASE, pose)
        if not os.path.isdir(d):
            print("🔴 không thấy", d); return 1
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(".png"):
                continue
            p = os.path.join(d, fn)
            a = np.array(Image.open(p).convert("RGBA"))
            al = a[:, :, 3]
            tot_before += int(((al > 8) & (al < 250)).sum())
            m = erode_mask(al >= THRESH, ERODE)
            a[:, :, 3] = np.where(m, 255, 0).astype(np.uint8)
            tot_after += int(((a[:, :, 3] > 8) & (a[:, :, 3] < 250)).sum())
            Image.fromarray(a, "RGBA").save(p)
            n_file += 1
        print("  ✓ %s — %d frame" % (pose, len(os.listdir(d))))
    print("\n%d file · pixel bán trong suốt: %d -> %d" % (n_file, tot_before, tot_after))
    print("✅ mép đã cứng, hết vành sương" if tot_after == 0 else "🔴 còn vành, hạ THRESH")
    return 0 if tot_after == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
