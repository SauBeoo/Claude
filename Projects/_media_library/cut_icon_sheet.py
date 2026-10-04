# -*- coding: utf-8 -*-
r"""
cut_icon_sheet.py — cắt TỜ ICON (lưới N×M nền trắng) → từng icon PNG nền trong.

Khác `cut_cast_sheet.py` ở chỗ KHÔNG dùng rembg:
────────────────────────────────────────────────────────────────────────────────
rembg đoán "vật thể" — với icon line-art phẳng nó hay ăn mất nét mảnh hoặc giữ lại
mảng trắng. Icon thì có cách đúng và tất định hơn: **flood-fill từ 4 mép**. Trắng nào
NỐI được ra mép = nền → xoá; trắng nào bị nét bao kín (ruột nhà, mặt đồng hồ, thân
lịch) = phần của hình → GIỮ. Không có mô hình, không ngẫu nhiên, chạy lại ra đúng file cũ.

CHẠY
────────────────────────────────────────────────────────────────────────────────
    python cut_icon_sheet.py <sheet.jpg> <outdir> --names a b c ... --cols 7 --rows 4
                             [--size 512] [--contact out.jpg]
"""
import io, sys, argparse
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

WHITE = 238          # ngưỡng coi là "trắng nền" (JPEG có nhiễu nên đừng để 250)


def cut_cell(cell):
    """1 ô → RGBA nền trong. Trả None nếu ô rỗng."""
    a = np.array(cell.convert("RGB")).astype(np.int16)
    lum = a.mean(axis=2)
    bg = lum >= WHITE
    h, w = bg.shape

    # flood-fill từ 4 mép: chỉ trắng NỐI RA MÉP mới là nền
    seen = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bg[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bg[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))

    rgba = np.dstack([np.array(cell.convert("RGB")),
                      np.where(seen, 0, 255).astype(np.uint8)])
    im = Image.fromarray(rgba, "RGBA")
    bb = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bb or (bb[2] - bb[0]) < 12 or (bb[3] - bb[1]) < 12:
        return None
    return im.crop(bb)


def cut(sheet, outdir, names, cols, rows, size):
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
        px, py = cw * 0.02, ch * 0.02          # ăn bớt viền → bỏ vạch ngăn ô
        cell = im.crop((int(c * cw + px), int(r * ch + py),
                        int((c + 1) * cw - px), int((r + 1) * ch - py)))
        ic = cut_cell(cell)
        if ic is None:
            print(f"  [!] ô {i} ({names[i]}) rỗng — bỏ")
            continue
        k = size / max(ic.width, ic.height)     # vừa khung vuông, giữ tỉ lệ
        ic = ic.resize((max(int(ic.width * k), 1), max(int(ic.height * k), 1)),
                       Image.LANCZOS)
        sq = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sq.alpha_composite(ic, ((size - ic.width) // 2, (size - ic.height) // 2))
        p = out / f"{names[i]}.png"
        sq.save(p)
        made.append(p)
        print(f"  ✓ {p.name}")
    return made


def contact(files, out, per_row=7, cell=190):
    rows = (len(files) + per_row - 1) // per_row
    s = Image.new("RGB", (per_row * cell, rows * (cell + 26)), (255, 255, 255))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(s)
    try:
        f = ImageFont.truetype(str(Path(__file__).parent / "fonts" / "NotoSansJP-Medium.otf"), 15)
    except Exception:
        f = None
    for i, p in enumerate(files):
        im = Image.open(p).convert("RGBA").resize((cell - 30, cell - 30), Image.LANCZOS)
        bx, by = (i % per_row) * cell, (i // per_row) * (cell + 26)
        s.paste(im, (bx + 15, by + 8), im)
        d.text((bx + cell / 2, by + cell + 6), p.stem, font=f, fill=(90, 95, 105), anchor="ma")
    s.save(out, quality=92)
    print("  ✓", Path(out).name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("outdir")
    ap.add_argument("--names", nargs="+", required=True)
    ap.add_argument("--cols", type=int, default=7)
    ap.add_argument("--rows", type=int, default=4)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--contact")
    a = ap.parse_args()
    files = cut(a.sheet, a.outdir, a.names, a.cols, a.rows, a.size)
    if a.contact:
        contact(files, a.contact)
