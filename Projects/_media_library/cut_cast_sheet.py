# -*- coding: utf-8 -*-
r"""
cut_cast_sheet.py — cắt SHEET biểu cảm (lưới N×M) → từng nhân vật PNG nền trong.

Dùng cho bộ nhân vật sân khấu (`make_stage.py`). Quy trình ở
`youtube-jp-nenkin/04_CAST_STAGE_PROMPTS.md` §0: user gen sheet nền TRẮNG → tool này cắt.

Làm gì
────────────────────────────────────────────────────────────────────────────────
  1. chia sheet thành lưới cols×rows (mặc định 4×2), ăn bớt viền mỗi ô để bỏ vạch ngăn
  2. `rembg` bóc nền trắng → RGBA
  3. dọn mảnh rác (giữ thành phần liên thông lớn nhất) — vạch ngăn/chấm lẻ hay sót lại
  4. autocrop theo alpha, chuẩn hoá CHIỀU CAO, lưu theo tên đặt sẵn
  5. xuất contact sheet để duyệt mắt (bắt buộc, `media-library.md` §3)

CHẠY
────────────────────────────────────────────────────────────────────────────────
    python cut_cast_sheet.py <sheet.jpg> <outdir> --names a b c ... [--cols 4 --rows 2]
                             [--height 1280] [--prefix sensei]
"""
import io, sys, argparse
from pathlib import Path
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from rembg import remove, new_session                      # noqa: E402

SESSION = new_session("isnet-anime")   # model hợp illustration hơn u2net mặc định


def largest_blob(a):
    """Giữ thành phần liên thông lớn nhất của mặt nạ alpha.
    Vạch ngăn ô + chấm nhiễu sống sót qua rembg sẽ làm bbox phình ra, autocrop thành vô
    nghĩa — nên phải dọn TRƯỚC khi crop, không phải sau."""
    m = a > 24
    h, w = m.shape
    lab = np.zeros((h, w), np.int32)
    cur, best, bestn = 0, 0, 0
    for y in range(h):
        for x in range(w):
            if not m[y, x] or lab[y, x]:
                continue
            cur += 1
            stack, n = [(y, x)], 0
            lab[y, x] = cur
            while stack:
                cy, cx = stack.pop()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        stack.append((ny, nx))
            if n > bestn:
                bestn, best = n, cur
    return np.where(lab == best, a, 0).astype(np.uint8)


def cut(sheet, outdir, names, cols, rows, height, quiet=False):
    im = Image.open(sheet).convert("RGB")
    W, H = im.size
    cw, ch = W / cols, H / rows
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    made = []
    for i in range(cols * rows):
        if i >= len(names) or not names[i]:
            continue
        r, c = divmod(i, cols)
        pad_x, pad_y = cw * 0.015, ch * 0.015          # ăn bớt viền → bỏ vạch ngăn
        cell = im.crop((int(c * cw + pad_x), int(r * ch + pad_y),
                        int((c + 1) * cw - pad_x), int((r + 1) * ch - pad_y)))
        # ép nền về trắng tuyệt đối giúp rembg cắt gọn hơn ảnh JPEG có nhiễu
        small = remove(cell, session=SESSION, post_process_mask=True)
        a = np.array(small.getchannel("A"))
        a = largest_blob(np.array(Image.fromarray(a).resize(
            (a.shape[1] // 4, a.shape[0] // 4), Image.NEAREST)))
        a = np.array(Image.fromarray(a).resize(small.size, Image.BILINEAR))
        px = np.array(small)
        px[..., 3] = np.minimum(px[..., 3], (a > 12) * 255)
        rgba = Image.fromarray(px)
        bb = rgba.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox()
        if not bb:
            print(f"  [!] ô {i} rỗng — bỏ")
            continue
        rgba = rgba.crop(bb)
        rgba = rgba.resize((max(int(rgba.width * height / rgba.height), 1), height),
                           Image.LANCZOS)
        p = out / f"{names[i]}.png"
        rgba.save(p)
        made.append(p)
        if not quiet:
            print(f"  ✓ {p.name}  ({rgba.width}×{rgba.height})")
    return made


def sheet_of(files, out, per_row=4, cell=(340, 460)):
    s = Image.new("RGB", (per_row * cell[0], ((len(files) + per_row - 1) // per_row) * cell[1]),
                  (245, 246, 248))
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGBA")
        k = min(cell[0] * .86 / im.width, cell[1] * .86 / im.height)
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        bx, by = (i % per_row) * cell[0], (i // per_row) * cell[1]
        s.paste(im, (bx + (cell[0] - im.width) // 2, by + (cell[1] - im.height) // 2), im)
    s.save(out, quality=92)
    print("  ✓", Path(out).name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("outdir")
    ap.add_argument("--names", nargs="+", required=True)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rows", type=int, default=2)
    ap.add_argument("--height", type=int, default=1280)
    ap.add_argument("--contact")
    a = ap.parse_args()
    files = cut(a.sheet, a.outdir, a.names, a.cols, a.rows, a.height)
    if a.contact:
        sheet_of(files, a.contact)
