# -*- coding: utf-8 -*-
"""
strip_wm.py — xoá watermark ✦ của model gen ảnh (Gemini/Imagen) khỏi thumbnail.

Dùng chung MỌI kênh chạy phương án "chữ bake trong ảnh AI" (health · chouhen · …).
Công thức đúng (đúc từ 3 cách SAI đã thử ở health video 22, memory
`feedback_thumbnail_health_chi_dua_prompt`):

    seed = điểm SÁNG NHẤT trong ô CHỈ chứa watermark
    → BFS lan theo ngưỡng chênh sáng (~60) từ seed
    → ASSERT: component < --max-px  VÀ  bbox không lan ra ngoài ô
    → giãn --grow px
    → fill bằng MEDIAN nền local (vành ngoài quanh mask), không phải patch từ phía trên
    → soi zoom ×4

Ba cách SAI, đừng làm lại:
  ① patch nền từ phía trên  → kéo chủ thể (vai/tóc) xuống chỗ vá
  ② fill bbox chữ nhật + mask ngưỡng → cắt mép chủ thể thành bậc vuông
  ③ BFS cả dải rộng → lan sang chủ thể (8.387 px thay vì 783)

Dùng:
    python strip_wm.py <in> <out> [--box 0.90,0.88,1.0,1.0] [--thr 60] [--grow 3]
    python strip_wm.py <in> --check          # chỉ đo, không ghi file
    python strip_wm.py <in> <out> --zoom out_zoom.png   # xuất ảnh soi ×4
"""
import argparse
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def find_wm(arr, box, thr, max_px):
    """BFS từ điểm sáng nhất trong `box`. Trả mask bool cùng cỡ arr, hoặc None."""
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = (int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))
    gray = arr.astype(np.int16).mean(axis=2)
    sub = gray[y0:y1, x0:x1]
    if sub.size == 0:
        return None, "ô rỗng"
    sy, sx = np.unravel_index(int(sub.argmax()), sub.shape)
    seed = (y0 + sy, x0 + sx)
    peak = gray[seed]
    floor = peak - thr

    mask = np.zeros((H, W), bool)
    q = deque([seed])
    mask[seed] = True
    n = 1
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if not (y0 <= ny < y1 and x0 <= nx < x1):   # KHÔNG cho lan ra ngoài ô
                continue
            if mask[ny, nx] or gray[ny, nx] < floor:
                continue
            mask[ny, nx] = True
            n += 1
            if n > max_px:
                return None, f"component {n}px > trần {max_px} — nó đang ăn vào chủ thể"
            q.append((ny, nx))
    ys, xs = np.nonzero(mask)
    bb = (xs.min(), ys.min(), xs.max(), ys.max())
    touch = bb[0] <= x0 or bb[1] <= y0 or bb[2] >= x1 - 1 or bb[3] >= y1 - 1
    return mask, (f"seed {seed[::-1]} sáng {peak:.0f} | {n} px | bbox {bb}"
                  + ("  ⚠️ bbox CHẠM mép ô → nới --box rồi chạy lại" if touch else ""))


def grow(mask, k):
    m = mask.copy()
    for _ in range(k):
        g = m.copy()
        g[1:, :] |= m[:-1, :]; g[:-1, :] |= m[1:, :]
        g[:, 1:] |= m[:, :-1]; g[:, :-1] |= m[:, 1:]
        m = g
    return m


def texture_fill(arr, m):
    """Vá bằng PATCH TEXTURE lấy từ vùng lân cận, không phải median phẳng.

    Median (mặc định) đúng cho nền TRƠN, nhưng trên nền có vân (gỗ, vải, đá) nó để lại
    một mảng phẳng đúng hình ✦ — nhìn ×4 là thấy ngay (ca ảnh AI co-dai video 17,
    2026-08-09). Ở đây: chọn vùng cho (donor) cùng kích thước ở lân cận, chấm điểm bằng
    độ lệch trung bình/độ tương phản so với vành nền quanh mask, rồi blend có FEATHER
    để không lộ đường viền vuông.
    Vẫn giữ nguyên nguyên tắc cũ: KHÔNG cv2.inpaint, KHÔNG kéo nền từ phía trên một cách
    mù quáng — donor phải tự chứng minh là giống nền quanh chỗ vá.
    """
    H, W = arr.shape[:2]
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    bw, bh = x1 - x0, y1 - y0
    ring = grow(m, 6) & ~m
    ref = arr[ring].astype(np.float32)
    ref_mu, ref_sd = ref.mean(axis=0), ref.std(axis=0)

    best, best_score = None, None
    for dx, dy in ((-bw - 8, 0), (bw + 8, 0), (0, -bh - 8), (0, bh + 8),
                   (-bw - 8, -bh - 8), (bw + 8, -bh - 8),
                   (-bw - 8, bh + 8), (bw + 8, bh + 8),
                   (-2 * bw, 0), (0, -2 * bh)):
        sx, sy = x0 + dx, y0 + dy
        if sx < 0 or sy < 0 or sx + bw > W or sy + bh > H:
            continue
        if m[sy:sy + bh, sx:sx + bw].any():      # donor không được dính chính watermark
            continue
        cand = arr[sy:sy + bh, sx:sx + bw].astype(np.float32)
        score = (np.abs(cand.reshape(-1, 3).mean(axis=0) - ref_mu).sum()
                 + np.abs(cand.reshape(-1, 3).std(axis=0) - ref_sd).sum())
        if best_score is None or score < best_score:
            best, best_score = (sx, sy), score
    if best is None:
        return None, None

    sx, sy = best
    alpha = m[y0:y1, x0:x1].astype(np.float32)
    for _ in range(3):                            # feather: làm mềm mép mask
        a = alpha.copy()
        a[1:, :] = np.maximum(a[1:, :], alpha[:-1, :] * .6)
        a[:-1, :] = np.maximum(a[:-1, :], alpha[1:, :] * .6)
        a[:, 1:] = np.maximum(a[:, 1:], alpha[:, :-1] * .6)
        a[:, :-1] = np.maximum(a[:, :-1], alpha[:, 1:] * .6)
        alpha = a
    alpha = np.clip(alpha, 0, 1)[..., None]

    out = arr.copy()
    dst = out[y0:y1, x0:x1].astype(np.float32)
    donor = arr[sy:sy + bh, sx:sx + bw].astype(np.float32)
    out[y0:y1, x0:x1] = np.clip(dst * (1 - alpha) + donor * alpha, 0, 255).astype(np.uint8)
    return out, (sx, sy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--box", default="0.90,0.88,1.0,1.0",
                    help="ô CHỈ chứa watermark, tỉ lệ x0,y0,x1,y1 (mặc định góc dưới-phải)")
    ap.add_argument("--thr", type=float, default=60, help="ngưỡng chênh sáng khi BFS")
    ap.add_argument("--grow", type=int, default=3, help="giãn mask (px)")
    ap.add_argument("--max-px", type=int, default=4000, help="trần kích thước component")
    ap.add_argument("--check", action="store_true", help="chỉ đo, không ghi")
    ap.add_argument("--zoom", help="xuất ảnh soi ×4 quanh vùng vá")
    ap.add_argument("--fill", choices=["median", "texture"], default="median",
                    help="median = nền TRƠN (mặc định, giữ nguyên hành vi cũ) · "
                         "texture = nền CÓ VÂN (gỗ/vải/đá), clone patch lân cận + feather")
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGB")
    arr = np.array(im)
    box = tuple(float(v) for v in a.box.split(","))
    mask, info = find_wm(arr, box, a.thr, a.max_px)
    if mask is None:
        sys.exit(f"❌ {info}")
    print(f"{Path(a.src).name}: {info}")
    if a.check:
        return
    if not a.out:
        sys.exit("cần <out>")

    m = grow(mask, a.grow)
    if a.fill == "texture":
        out, donor = texture_fill(arr, m)
        if out is None:
            sys.exit("❌ không tìm được vùng cho (donor) hợp lệ — dùng --fill median")
        print(f"   vá {int(m.sum())} px bằng PATCH TEXTURE lấy từ (x={donor[0]}, y={donor[1]})")
    else:
        ring = grow(m, 6) & ~m                  # vành nền quanh mask
        med = (np.median(arr[ring], axis=0).astype(np.uint8) if ring.any()
               else np.array([0, 0, 0], np.uint8))
        out = arr.copy()
        out[m] = med
        print(f"   vá {int(m.sum())} px bằng median nền local RGB{tuple(int(v) for v in med)}")

    img = Image.fromarray(out)
    img.save(a.out)
    print(f"OK {a.out}")

    if a.zoom:
        ys, xs = np.nonzero(m)
        pad = 40
        bb = (max(0, xs.min() - pad), max(0, ys.min() - pad),
              min(img.width, xs.max() + pad), min(img.height, ys.max() + pad))
        cr = img.crop(bb)
        cr.resize((cr.width * 4, cr.height * 4), Image.NEAREST).save(a.zoom)
        print(f"   soi ×4 → {a.zoom}")


if __name__ == "__main__":
    main()
