# -*- coding: utf-8 -*-
"""clean_wm.py — xoá watermark ✦ (Gemini/Imagen) ở góc ảnh gen.

Công thức đã chốt (memory feedback_thumbnail_health_chi_dua_prompt):
  seed = điểm SÁNG NHẤT trong ô CHỈ chứa watermark
  → BFS ngưỡng ~60 quanh seed
  → ASSERT component < 4000 px và bbox không lan ra ngoài ô
  → giãn 3 px
  → fill median nền local (vành khăn quanh mask)

Ba cách SAI đã thử và loại: patch nền từ phía trên · fill bbox chữ nhật ·
BFS cả dải (lan sang chủ thể).

Dùng: python tools/clean_wm.py <in.jpg> <out.jpg> [--box x0,y0,x1,y1] [--thr 60]
Mặc định box = góc dưới phải 200×200 px.
"""
import argparse
import io
import sys
from collections import deque
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image

MAX_COMP = 4000     # px — vượt = BFS đã lan sang chủ thể, dừng chứ không vá bừa
DILATE = 3


def clean(src: Path, dst: Path, box, thr: int) -> bool:
    im = Image.open(src).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box
    px = im.load()

    # seed = sáng nhất trong ô
    best, seed = -1, None
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            v = r + g + b
            if v > best:
                best, seed = v, (x, y)
    sr, sg, sb = px[seed]
    print(f"   seed {seed} rgb=({sr},{sg},{sb})")

    # BFS trong ô, ngưỡng theo khoảng cách màu tới seed
    mask = set()
    q = deque([seed])
    mask.add(seed)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (x0 <= nx < x1 and y0 <= ny < y1) or (nx, ny) in mask:
                continue
            r, g, b = px[nx, ny]
            if abs(r - sr) + abs(g - sg) + abs(b - sb) <= thr * 3:
                mask.add((nx, ny))
                q.append((nx, ny))
        if len(mask) > MAX_COMP:
            break

    bx0 = min(p[0] for p in mask); bx1 = max(p[0] for p in mask)
    by0 = min(p[1] for p in mask); by1 = max(p[1] for p in mask)
    print(f"   component {len(mask)} px · bbox ({bx0},{by0})-({bx1},{by1}) "
          f"= {bx1-bx0+1}×{by1-by0+1}")

    if len(mask) > MAX_COMP:
        print(f"   ❌ BỎ QUA — component {len(mask)} > {MAX_COMP}: BFS đã lan sang chủ thể. "
              f"Siết --box hoặc hạ --thr, ĐỪNG vá bừa.")
        return False
    if bx0 <= x0 or by0 <= y0 or bx1 >= x1 - 1 or by1 >= y1 - 1:
        print("   ❌ BỎ QUA — mask chạm mép ô, tức đã ăn ra ngoài watermark.")
        return False

    # giãn
    grown = set(mask)
    for _ in range(DILATE):
        add = set()
        for x, y in grown:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                add.add((x + dx, y + dy))
        grown |= add
    grown = {p for p in grown if 0 <= p[0] < W and 0 <= p[1] < H}

    # median nền local = vành khăn quanh mask (giãn thêm 6 px, trừ phần mask)
    ring = set(grown)
    for _ in range(6):
        add = set()
        for x, y in ring:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                add.add((x + dx, y + dy))
        ring |= add
    ring = {p for p in ring if 0 <= p[0] < W and 0 <= p[1] < H} - grown
    rs = sorted(px[p] for p in ring)
    med = rs[len(rs) // 2]
    print(f"   fill median nền local = {med} (mẫu {len(rs)} px)")

    for p in grown:
        px[p] = med

    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=95)
    print(f"   ✅ {dst.name}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--box", default="", help="x0,y0,x1,y1 — mặc định góc dưới phải 200×200")
    ap.add_argument("--thr", type=int, default=60)
    a = ap.parse_args()

    src = Path(a.src)
    im = Image.open(src)
    W, H = im.size
    if a.box:
        box = tuple(int(v) for v in a.box.split(","))
    else:
        box = (W - 210, H - 210, W - 20, H - 20)
    print(f"{src.name} {W}×{H} · ô quét {box} · thr {a.thr}")
    ok = clean(src, Path(a.dst), box, a.thr)
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
