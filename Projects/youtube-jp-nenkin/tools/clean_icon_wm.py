# -*- coding: utf-8 -*-
"""clean_icon_wm.py — xoá dấu ✦ (watermark Gemini) trên ICON NỀN PHẲNG.

KHÁC `clean_wm.py`: cái kia lo ảnh THẬT (JPEG, nền nhiều chi tiết) → phải BFS + fill
median. Ở ICON thì nền là **một màu phẳng**, nên cách đúng và sạch hơn hẳn là
**snap mọi pixel BỊ LÀM SÁNG về đúng màu nền**. Không inpaint, không mờ.

Ca gốc (user bắt được 2026-08-10): `assets/icons/warning.png` còn nguyên ✦ nằm sau dấu
chấm than, và nó là icon dùng nhiều nhất — 13/73 thẻ của video 10. 27 icon còn lại sạch.

Cách dùng:
    python tools/clean_icon_wm.py warning            # tự sao lưu .orig.png rồi vá
    python tools/clean_icon_wm.py warning --check     # chỉ đếm, không ghi
"""
import shutil
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ICONS = Path(__file__).resolve().parents[1] / "assets" / "icons"


def base_fill(px, w, h):
    """Màu nền phẳng = màu opaque xuất hiện nhiều nhất."""
    c = Counter()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b, a = px[x, y]
            if a > 200:
                c[(r, g, b)] += 1
    return c.most_common(1)[0][0]


def clean(name: str, write: bool) -> int:
    p = ICONS / f"{name}.png"
    im = Image.open(p).convert("RGBA")
    w, h = im.size
    px = im.load()
    br, bg, bb = base_fill(px, w, h)
    # ✦ là vệt SÁNG HƠN nền: cùng họ màu ấm nhưng g/b bị đẩy lên.
    # ⚠️ Vòng 1 dùng +10/+22 → hết vệt sáng nhưng CÒN VIỀN MỜ của hình thoi (pixel nằm
    # sát dưới ngưỡng). Siết về +3/+6: icon vốn nền PHẲNG nên snap rộng chỉ làm nó phẳng
    # hơn, không mất chi tiết. Pixel viền/anti-alias là màu TỐI nên đã bị `r >= br-12` loại.
    gt, bt = bg + 3, bb + 6
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 200 and r >= br - 12 and g >= gt and b >= bt:
                if write:
                    px[x, y] = (br, bg, bb, a)
                n += 1
    print(f"{name}: nền={br,bg,bb}  ngưỡng g≥{gt} b≥{bt}  → {n} pixel bị làm sáng")
    if write and n:
        orig = ICONS / f"{name}.orig.png"
        if not orig.exists():
            shutil.copy(p, orig)
            print(f"  ↳ sao lưu {orig.name}")
        im.save(p)
        print(f"  ✓ đã vá {p.name}")
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--check" not in sys.argv
    for name in args or ["warning"]:
        clean(name, write)


if __name__ == "__main__":
    main()
