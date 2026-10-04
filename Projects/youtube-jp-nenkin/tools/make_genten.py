# -*- coding: utf-8 -*-
"""make_genten.py — vẽ slide 原典 (thẻ TRÍCH DẪN) cho entry có `"genten": {...}`.

⚠️ ĐỌC TRƯỚC — vì sao là THẺ TRÍCH DẪN, không phải ảnh chụp trang:
Khuôn 原典 chuẩn của kênh (`CLAUDE.md` §Chuẩn VISUAL) là **ảnh chụp thật** trang
cơ quan công + khoanh đỏ bằng Apple Pencil (`make_genten_06.py` đọc `genten/_raw/`).
Tool này là **bản dự phòng khi CHƯA có ảnh chụp**: nó vẽ một thẻ giấy ghi rõ
「引用」 + câu trích + tên cơ quan + mốc thời điểm. Nó KHÔNG bắt chước layout trang
web — dựng một hình trông như screenshot của trang thật = dựng giả hồ sơ, cấm.

→ Có ảnh chụp/screen-record rồi thì dùng khuôn thật; entry nào có file
`genten/_raw/slide_<i>.*` thì tool này BỎ QUA để không đè lên bản thật.

CHẠY:  python tools/make_genten.py 07_tokubetsu-shikyu-rourei-kosei-nenkin
"""
import json
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
PAPER = (247, 244, 236)
NAVY = (26, 42, 74)
RED = (200, 32, 40)
INK = (38, 42, 52)
GREY = (120, 124, 132)
F_BOLD = "C:/Windows/Fonts/yugothb.ttc"
F_REG = "C:/Windows/Fonts/yugothm.ttc"
# giấy 方眼 (grid) — cùng bản sắc với lớp drawn của kênh (channels.py: jp-pen + grid)
GRID = (226, 224, 214)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_jp(txt, n):
    return textwrap.wrap(txt, width=n) or [""]


def draw_card(spec, out: Path):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

    # nhãn 引用 + tiêu đề mục
    d.rounded_rectangle([120, 96, 372, 168], 12, fill=NAVY)
    d.text((150, 112), "引用", font=font(F_BOLD, 44), fill=PAPER)
    d.text((404, 110), spec.get("label", ""), font=font(F_BOLD, 50), fill=NAVY)

    # câu trích — khoanh đỏ (đây là "赤で囲んだところ" mà giọng đọc nói tới)
    quote = spec.get("quote", "")
    size = 66 if len(quote) <= 60 else 56 if len(quote) <= 90 else 48
    lines = wrap_jp(quote, max(14, int(1520 / size * 1.05)))
    fq = font(F_BOLD, size)
    lh = int(size * 1.55)
    block_h = lh * len(lines)
    top = (H - block_h) // 2 - 20
    d.rounded_rectangle([140, top - 56, W - 140, top + block_h + 44], 18,
                        outline=RED, width=9)
    for i, ln in enumerate(lines):
        d.text((188, top + i * lh), ln, font=fq, fill=INK)

    # nguồn + mốc thời điểm (bắt buộc — YMYL rule #3)
    src = spec.get("source", "")
    d.text((140, H - 148), f"出典：{src}", font=font(F_REG, 36), fill=GREY)
    d.text((140, H - 96), "令和8年8月時点", font=font(F_REG, 34), fill=GREY)
    d.text((W - 420, H - 96), "年金研究室", font=font(F_BOLD, 34), fill=NAVY)

    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    return out


def main():
    stem = sys.argv[1] if len(sys.argv) > 1 else None
    if not stem:
        sys.exit("dùng: python tools/make_genten.py <stem>")
    cfg = json.loads((PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json").read_text(encoding="utf-8"))
    vid = PROJ / "06_VIDEO" / stem
    out_dir = vid / "slides_img"
    raw = vid / "genten" / "_raw"
    n = 0
    for i, spec in enumerate(cfg):
        g = spec.get("genten")
        if not isinstance(g, dict):
            continue
        if list(raw.glob(f"slide_{i:02d}.*")):
            print(f"[{i:02d}] có ảnh chụp thật trong genten/_raw → BỎ QUA (dùng bản thật)")
            continue
        p = draw_card(g, out_dir / f"slide_{i:02d}.png")
        print(f"[{i:02d}] → {p.name}  「{g['quote'][:26]}…」")
        n += 1
    print(f"xong {n} thẻ 原典 (dự phòng — chưa phải screen-record iPad)")


if __name__ == "__main__":
    main()
