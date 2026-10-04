# -*- coding: utf-8 -*-
r"""strip_wm_crop29.py — xoá ✦ trên 95 ảnh minh hoạ của v29 bằng **CẮT KHUNG**.

🔴 VÌ SAO PHẢI VIẾT LẠI (đọc trước khi ai đó "cải tiến" ngược lại):
`ingest_art29.py` báo "✦ đã vá 90/90" — **báo láo**. Dựng sheet crop 1:1 tại toạ độ chuẩn thì
✦ còn ở hơn 20 ảnh. Đúng `media-library.md` §2.10 ⑤: *số đo và exit code KHÔNG chứng minh ✦
đã sạch*; §5: *định vị ✦ bằng máy đã thất bại 4/4 lần*.

Sau đó thử **vá bằng snap-màu-palette** (hợp lý với ảnh vector phẳng) — 3 vòng, hỏng cả 3 theo
hai hướng ngược nhau, ghi lại để khỏi đi lại:
  ① palette gom trên CẢ hộp → ✦ to ~8% diện tích nên **tự lọt vào palette**, trượt 7 ảnh.
  ② palette lấy từ VÀNH + nới trần lên 175 → sạch ✦ nhưng **ăn vào hình**: dải chống răng cưa
     dọc biên hai mảng màu cũng nằm trong ngưỡng ⇒ ô 11/38/87 mọc mảng kem cắt vào vật.
  ③ thêm lọc cụm (giữ cụm cỡ ✦, bỏ cụm chạm mép hộp) → hết phá biên nhưng **vá được 6/95**:
     ✦ có cánh mảnh dính vào dải biên/nhiễu nên cụm của nó cũng chạm mép.
  ⇒ Mỗi lần siết là bỏ sót, mỗi lần nới là phá hình. Đó là dấu hiệu **sai đường**, không phải
     thiếu tinh chỉnh.

✅ ĐƯỜNG ĐÚNG cho lô này — CẮT, và `media-library.md` §2.10 ⑤ đã nói sẵn: *"Cắt mép phải cho ✦
ra ngoài khung thì sạch tuyệt đối"*. Điều kiện của §6d để được cắt: **chữ không chạy sát mép**.
Lô này là ảnh minh hoạ vector KHÔNG bake chữ (ảnh 原典 có chữ nằm riêng ở `genten/`, tool này
không đụng tới) ⇒ đủ điều kiện, và cắt không có rủi ro phá biên nào.

Số: ✦ tâm 0,930W, rộng ~70px ⇒ mép trái ✦ ≈ 0,912W. Cắt phải tại **0,905W** là ✦ ra ngoài hẳn.
Rồi trim chiều cao về 16:9 **chia đôi trên/dưới** (§6d: trim hết ở đáy thì clip mất chân vật),
cuối cùng resize lại 1920×1080 để `build28.py` không phải đổi gì.
⚠️ Góc trên-trái giữ nguyên ⇒ `im.getpixel((6,6))` mà builder dùng lấy màu canvas vẫn đúng.

🔴🔴 CHỪA ẢNH 原典 RA — lỗi đã suýt lọt: ô 35/36 (ảnh chụp trang 千葉県広域連合) bị cắt **mất chữ
ở mép phải VÀ mất một phần khung khoanh đỏ**. Đó là BẰNG CHỨNG NGUỒN của một kênh YMYL, cắt cụt
là hỏng nặng hơn mọi dấu ✦. Và chúng vốn **không có ✦** vì là ảnh chụp màn hình, không phải ảnh AI.
Nhận diện bằng **số cụm mực nhỏ** (nét chữ): 5 ảnh 原典 đo được ≥1.271, ảnh minh hoạ vector cao
nhất chỉ 176 ⇒ khoảng cách gần 8 lần, ngưỡng 600 tách sạch mà không cần liệt kê tay chỉ số ô
(chỉ số ô trôi khi đổi plan — bài học đã trả giá hai lần ở `img29_prompts.py`/`telop29.py`).
"""
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage
from PIL import Image

VD = Path(__file__).resolve().parents[1] / "06_VIDEO" / "29_shikaku-kakuninsho-8gatsu-85sai"
ART = VD / "art_final"
BAK = VD / "_wm_orig"
CUT = 0.905
WM = (0.930, 0.872)
TEXTY = 600          # ≥ngần này cụm mực nhỏ ⇒ ảnh 原典 (chụp màn hình) ⇒ KHÔNG cắt


def texty(f: Path) -> int:
    """Đếm cụm mực nhỏ = nét chữ. Ảnh 原典 1.271–2.056 · ảnh vector ≤176."""
    a = np.asarray(Image.open(f).convert("L")).astype(int)
    lab, n = ndimage.label(a < 140)
    if not n:
        return 0
    sz = np.bincount(lab.ravel())[1:]
    return int(((sz >= 6) & (sz <= 400)).sum())


def crop(f: Path):
    im = Image.open(f).convert("RGB")
    W, H = im.size
    x1 = int(W * CUT)
    h2 = int(x1 / 16 * 9)
    dy = (H - h2) // 2
    return im.crop((0, dy, x1, dy + h2)).resize((W, H), Image.LANCZOS)


def peak(f: Path, tmpl) -> float:
    """Nghiệm thu bằng MÁY nhưng ĐÚNG CHIỀU: template lấy từ chính ảnh gốc, tìm lại trên bản
    đã cắt. Peak phải tụt về mức nhiễu. Khác hẳn local-contrast/residual (đã trượt 4/4)."""
    a = cv2.cvtColor(np.asarray(Image.open(f).convert("RGB")), cv2.COLOR_RGB2GRAY)
    return float(cv2.matchTemplate(a, tmpl, cv2.TM_CCOEFF_NORMED).max())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    BAK.mkdir(exist_ok=True)
    fs = sorted(ART.glob("shot_*.png"))
    worst, keptext = [], []
    for f in fs:
        if not (BAK / f.name).exists():
            shutil.copy2(f, BAK / f.name)
        src = BAK / f.name
        if texty(src) >= TEXTY:
            shutil.copy2(src, f)          # ảnh 原典 → trả nguyên bản, không cắt
            keptext.append(f.name)
            continue
        im0 = Image.open(src).convert("RGB")
        W, H = im0.size
        g0 = cv2.cvtColor(np.asarray(im0), cv2.COLOR_RGB2GRAY)
        cx, cy = int(W * WM[0]), int(H * WM[1])
        tmpl = g0[cy - 45:cy + 45, cx - 45:cx + 45]
        crop(src).save(f)
        worst.append((peak(f, tmpl), f.name))
    worst.sort(reverse=True)
    print(f"CHỪA {len(keptext)} ảnh 原典 (không cắt): {keptext}")
    print(f"{len(fs)} ảnh · cắt phải tại {CUT:.3f}W + trim 16:9 chia đôi + resize lại 1920×1080")
    print("peak khớp lại mẫu ✦ (càng thấp càng sạch), 8 ảnh cao nhất:")
    for p, n in worst[:8]:
        print(f"   {p:.3f}  {n}")
    print("⛔ Peak thấp CHƯA phải nghiệm thu — vẫn phải dựng sheet crop 1:1 và SOI MẮT (§2.10 ⑤b).")
