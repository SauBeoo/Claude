#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""process_cutout.py — biến ảnh stock thành cutout kiểu sticker giấy Vox-collage.

Cách dùng (cặp input/output, bao nhiêu cặp cũng được):
    python process_cutout.py public/raw_phone.jpg public/el_phone.png \
                             public/raw_globe.jpg public/el_globe.png

Tuỳ chọn:
    --edge N      độ dày viền sticker trắng, px (mặc định 10)
    --margin N    lề quanh nội dung khi crop, px (mặc định 24)
    --max-dim N   co ảnh output về tối đa N px cạnh dài (mặc định 1600, 0 = không co)

Mỗi ảnh đi qua 4 bước:
  1. rembg cắt nền (chạy local, không cần API key).
  2. Dọn mask: giữ connected component lớn nhất + các mảnh ≥10% diện tích nó —
     bỏ bóng đổ / phản chiếu mà rembg đoán nhầm là foreground.
  3. Viền sticker trắng mỏng quanh silhouette (dilate mask).
  4. CROP SÁT nội dung + margin — bước quan trọng nhất: ảnh rembg trả ra
     thường 80% là padding trong suốt, không crop thì element to mấy cũng
     nhìn bé trong layout.

In cảnh báo nếu output vẫn "sparse" (nội dung < 30% khung sau crop) — soi lại
bằng mắt trước khi wire vào scene; thường là rembg cắt hỏng do ảnh nguồn
chụp trên nền giấy/trắng (xem SKILL.md bước 3: chọn lại ảnh nền trơn).
"""
import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from PIL import Image
from scipy import ndimage


def clean_mask(alpha, thresh=20, keep_ratio=0.10):
    """Trả mask bool: component lớn nhất + mảnh ≥ keep_ratio diện tích nó."""
    binary = alpha > thresh
    labels, n = ndimage.label(binary)
    if n == 0:
        return binary
    sizes = ndimage.sum(binary, labels, range(1, n + 1))
    biggest = sizes.max()
    keep = [i + 1 for i, s in enumerate(sizes) if s >= biggest * keep_ratio]
    return np.isin(labels, keep)


def process(src, dst, edge, margin, max_dim, model=None):
    from rembg import remove  # import chậm, để trong hàm

    im = Image.open(src).convert("RGB")
    if model:
        # 🔴 2026-08-16: u2net (mặc định) TRẢ VỀ NGUYÊN ẢNH ở ảnh chụp cảnh bàn/sàn —
        # không có ranh giới chủ thể↔nền rõ nên nó coi cả khung là foreground
        # ("nội dung 100%"). Đo trên slide_61 (chuối trên đĩa, bàn gỗ):
        #   u2net 100%  ·  isnet-general-use 13,2%  ·  u2netp 13,5%  ·  silueta 13,3%
        # ⇒ ảnh chụp thật (không phải stock nền trắng) thì truyền --model isnet-general-use.
        from rembg import new_session
        cut = remove(im, session=new_session(model)).convert("RGBA")
    else:
        cut = remove(im).convert("RGBA")
    arr = np.array(cut)

    mask = clean_mask(arr[:, :, 3])
    if not mask.any():
        print(f"  🔴 {src}: rembg không tách được gì — đổi ảnh nguồn khác")
        return False
    arr[:, :, 3] = np.where(mask, arr[:, :, 3], 0)

    # viền sticker: vành dilate quanh mask, tô trắng đặc
    # 🔴 2026-08-16: PHẢI chặn edge<=0. scipy hiểu iterations<1 là "lặp tới khi
    # KHÔNG ĐỔI NỮA" → mask phình ra CẢ KHUNG → vành trắng phủ kín ảnh → tool in
    # "nội dung 100%" và trả về đúng ảnh gốc. `--edge 0` (cutout không viền, dùng
    # cho kênh ảnh thật) im lặng hỏng vì lỗi này.
    dilated = mask
    if edge > 0:
        dilated = ndimage.binary_dilation(mask, iterations=edge)
        ring = dilated & ~mask
        arr[ring] = [255, 255, 255, 255]
    # làm mượt mép ngoài nhẹ để đỡ răng cưa
    a = arr[:, :, 3].astype(float)
    a = ndimage.gaussian_filter(a, sigma=0.7)
    arr[:, :, 3] = np.clip(a, 0, 255).astype(np.uint8)

    # crop theo bbox của mask đã dilate + margin
    ys, xs = np.where(dilated)
    y0, y1 = max(0, ys.min() - margin), min(arr.shape[0], ys.max() + margin + 1)
    x0, x1 = max(0, xs.min() - margin), min(arr.shape[1], xs.max() + margin + 1)
    arr = arr[y0:y1, x0:x1]

    out = Image.fromarray(arr)
    if max_dim and max(out.size) > max_dim:
        out.thumbnail((max_dim, max_dim), Image.LANCZOS)
    out.save(dst)

    fill = (np.array(out)[:, :, 3] > 20).mean()
    flag = "⚠️ SPARSE — soi mắt lại, có thể rembg cắt hỏng" if fill < 0.30 else "ok"
    print(f"  {dst}: {out.size[0]}x{out.size[1]}, nội dung {fill*100:.0f}% [{flag}]")
    return True


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("pairs", nargs="*")
    ap.add_argument("--edge", type=int, default=10)
    ap.add_argument("--margin", type=int, default=24)
    ap.add_argument("--max-dim", type=int, default=1600)
    ap.add_argument("--model", default=None,
                    help="model rembg (vd isnet-general-use). Bỏ trống = u2net mặc định. "
                         "Ảnh chụp cảnh thật thường CẦN isnet-general-use — xem chú thích process()")
    args = ap.parse_args()
    if not args.pairs or len(args.pairs) % 2:
        print(__doc__)
        sys.exit(1)
    ok = True
    for i in range(0, len(args.pairs), 2):
        ok &= process(args.pairs[i], args.pairs[i + 1], args.edge, args.margin,
                      args.max_dim, args.model)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
