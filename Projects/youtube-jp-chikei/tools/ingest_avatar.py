# -*- coding: utf-8 -*-
"""
ingest_avatar.py — dua anh AI 16:9 thanh AVATAR vuong cho kenh.

VI SAO CAN TOOL RIENG: generator xuat 16:9 (1376x768), avatar YouTube la 1:1 va hien thi
nho nhat o 48px. Cat vuong o GIUA se an ~44% be ngang — phan mat la VIEN hoa van hai ben,
nen prompt da bat bo cuc TRON NAM GON GIUA KHUNG (09_BRAND/brand_prompts_BLOCKS.md §0).

    python tools/ingest_avatar.py "F:/Youtube/.../task_002_1_image.jpg"
    python tools/ingest_avatar.py <src> --shift-y -20      # dich khung cat len/xuong
"""
import io, sys, argparse
from pathlib import Path
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "09_BRAND"


def corners_sheet(im, dst):
    """Soi 4 goc o 1:1 — watermark ✦ chi lo o co that, sheet thu nho cho qua
    (media-library.md §2.10 ⑤b)."""
    W, H = im.size
    cw, ch = 300, 200
    cs = [(0, 0), (W - cw, 0), (0, H - ch), (W - cw, H - ch)]
    sheet = Image.new("RGB", (cw * 2 + 30, ch * 2 + 30), (255, 255, 255))
    for i, (x, y) in enumerate(cs):
        sheet.paste(im.crop((x, y, x + cw, y + ch)), (10 + (i % 2) * (cw + 10),
                                                      10 + (i // 2) * (ch + 10)))
    sheet.save(dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--shift-y", type=int, default=0, help="dich khung cat theo truc doc (px)")
    ap.add_argument("--shift-x", type=int, default=0)
    g = ap.parse_args()

    im = Image.open(g.src).convert("RGB")
    W, H = im.size
    print("nguon : %s  %dx%d" % (Path(g.src).name, W, H))

    OUT.mkdir(parents=True, exist_ok=True)
    corners_sheet(im, OUT / "_avatar_src_corners.png")
    print("      -> _avatar_src_corners.png  (SOI 4 GOC 1:1 tim ✦ TRUOC khi dung)")

    side = min(W, H)
    cx = W // 2 + g.shift_x
    cy = H // 2 + g.shift_y
    x0 = max(0, min(W - side, cx - side // 2))
    y0 = max(0, min(H - side, cy - side // 2))
    sq = im.crop((x0, y0, x0 + side, y0 + side)).resize((g.size, g.size), Image.LANCZOS)
    sq.save(OUT / "avatar.png")
    print("cat   : %dx%d tu (%d,%d) -> avatar.png %dx%d  (mat %.0f%% be ngang)"
          % (side, side, x0, y0, g.size, g.size, (W - side) / W * 100))

    for s in (176, 88, 48):
        sq.resize((s, s), Image.LANCZOS).save(OUT / ("avatar_prev%d.png" % s))
    # dan thu vao khung tron — YouTube hien avatar dang tron, goc vuong luon bi cat
    mask = Image.new("L", (g.size, g.size), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0, 0, g.size, g.size), fill=255)
    circ = Image.new("RGB", (g.size, g.size), (255, 255, 255))
    circ.paste(sq, (0, 0), mask)
    circ.resize((176, 176), Image.LANCZOS).save(OUT / "avatar_circle176.png")
    print("      -> avatar_prev176/88/48.png + avatar_circle176.png (xem dang TRON that)")
    print("\nDUYET BANG MAT truoc khi upload: avatar_prev48.png con doc duoc chu khong?")


if __name__ == "__main__":
    main()
