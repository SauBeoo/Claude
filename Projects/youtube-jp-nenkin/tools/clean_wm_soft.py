# -*- coding: utf-8 -*-
"""clean_wm_soft.py — xoá ✦ Gemini trên ẢNH MINH HOẠ nền phẳng/gradient mượt.

BA TOOL, BA CA KHÁC NHAU — đừng dùng lẫn:
  · `clean_wm.py`       ảnh THẬT (JPEG, nền nhiều chi tiết) — BFS ngưỡng ~60 + fill median.
  · `clean_icon_wm.py`  ICON nền MỘT MÀU — snap pixel bị làm sáng về đúng màu nền.
  · `clean_wm_soft.py`  (file này) ảnh MINH HOẠ nền phẳng/gradient — ✦ chỉ sáng hơn nền
                        **+3…+7 mức**, nên BFS thr 60 của clean_wm loang hết ảnh và exit 2
                        (đo thật trên 12 ảnh video 10 nenkin: 12/12 fail).

CÁCH: ước lượng nền bằng median filter (bán kính lớn) → chỗ nào sáng hơn nền quá ngưỡng
nhỏ thì thay bằng chính giá trị nền. Giữ guard của clean_wm: vùng phát hiện phải NHỎ,
không thì bail (để không xoá mất chủ thể sáng).

Dùng: python tools/clean_wm_soft.py <in> <out> [--delta 2.5] [--box x0,y0,x1,y1]
      python tools/clean_wm_soft.py <in> --check
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAX_AREA = 9000      # px — ✦ thật ~800–4000; lớn hơn = đang bắt vào chủ thể
MAX_SIDE = 150       # px — bbox của ✦ không quá cỡ này


def components(mask):
    """Nhãn thành phần liên thông 4-hướng, không cần scipy."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    cur = 0
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or lab[y, x]:
                continue
            cur += 1
            stack = [(y, x)]
            lab[y, x] = cur
            while stack:
                cy, cx = stack.pop()
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        stack.append((ny, nx))
    return lab, cur


def clean(src: Path, dst: Path | None, delta: float, box=None, radius=21):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box or (W - 300, H - 250, W - 10, H - 10)
    crop = im.crop((x0, y0, x1, y1))
    bg = crop.filter(ImageFilter.MedianFilter(size=radius))
    a = np.asarray(crop).astype(np.float32)
    b = np.asarray(bg).astype(np.float32)
    diff = a.mean(2) - b.mean(2)
    mask = diff > delta
    if not mask.any():
        print(f"  {src.name}: KHÔNG thấy vệt sáng nào (delta {delta}) — bỏ qua")
        return False
    lab, n = components(mask)
    best, area = 0, 0
    for k in range(1, n + 1):
        s = int((lab == k).sum())
        if s > area:
            best, area = k, s
    sel = lab == best
    ys, xs = np.nonzero(sel)
    bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    print(f"  {src.name}: vệt {area}px  bbox {bw}×{bh} @({x0+xs.min()},{y0+ys.min()})", end="")
    if area > MAX_AREA or bw > MAX_SIDE or bh > MAX_SIDE:
        print("  → 🔴 QUÁ LỚN, BAIL (có thể là chủ thể, không phải ✦)")
        return False
    # giãn 3px cho hết mép mờ
    m = Image.fromarray((sel * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    sel2 = np.asarray(m) > 0
    out = a.copy()
    out[sel2] = b[sel2]
    im.paste(Image.fromarray(out.astype(np.uint8)), (x0, y0))
    if dst:
        im.save(dst)
        print(f"  → ✓ {dst.name}")
    else:
        print("  → (check, không ghi)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--delta", type=float, default=2.5)
    ap.add_argument("--box", default="")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    box = tuple(int(v) for v in a.box.split(",")) if a.box else None
    ok = clean(Path(a.src), None if a.check else Path(a.dst or a.src), a.delta, box)
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
