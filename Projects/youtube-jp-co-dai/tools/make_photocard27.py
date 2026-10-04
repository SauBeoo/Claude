# -*- coding: utf-8 -*-
r"""make_photocard27.py — ảnh scene gen (1376×768) → "photocard" PNG cho Remotion video 27.

Chép nguyên `make_photocard26.py`, chỉ đổi STEM. Xem file đó để biết chi tiết cơ chế
(viền trắng bo tròn + bóng mềm, KHÔNG giấy xé/tape — khuôn ANIME).

CHẠY:  python tools/make_photocard27.py --src "C:\Users\tuana\Downloads\<folder>"          # xem bảng ghép
       python tools/make_photocard27.py --src "..." --apply                                  # ghi photocard/
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
STEM = "27_kankisen-abura-akujiru"
CUT_W = 1229
BORDER = 18
PAPER = (250, 246, 238)


def build(src, out, seed, rot):
    """ANIME: KHÔNG giấy xé, KHÔNG tape, KHÔNG xoay — khung ảnh bo tròn viền trắng đều + bóng mềm."""
    im = Image.open(src).convert("RGB")
    if im.width > CUT_W:
        im = im.crop((0, 0, CUT_W, im.height))
    w, h = im.size
    R = 36
    cw, ch = w + BORDER * 2, h + BORDER * 2
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    m = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), R + BORDER, fill=255)
    card.paste(Image.new("RGBA", (cw, ch), (255, 255, 255, 255)), (0, 0), m)
    mi = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mi).rounded_rectangle((0, 0, w - 1, h - 1), R, fill=255)
    card.paste(im.convert("RGBA"), (BORDER, BORDER), mi)
    pad = 26
    fin = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 112), (0, 0), card.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(11))
    fin.alpha_composite(sh, (pad + 8, pad + 11))
    fin.alpha_composite(card, (pad, pad))
    fin.save(out)
    return fin.size


def main():
    if "--src" not in sys.argv:
        print("dùng: python tools/make_photocard27.py --src <folder> [--apply] [--map prefix=card_x ...]")
        return 1
    src = Path(sys.argv[sys.argv.index("--src") + 1])
    apply = "--apply" in sys.argv
    vd = PROJ / "06_VIDEO" / STEM
    ten = [l.split()[0].replace(".png", "") for l in
           (vd / "art_prompts_photocard_TENFILE.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    files = sorted((p for p in src.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")),
                   key=lambda p: p.stat().st_mtime)
    manual = {}
    for i, a in enumerate(sys.argv):
        if a == "--map":
            k, v = sys.argv[i + 1].split("=", 1)
            manual[k] = v
    pairs = []
    if manual:
        for p in files:
            tgt = next((v for k, v in manual.items() if p.name.startswith(k)), None)
            if tgt:
                pairs.append((p, tgt))
    else:
        if len(files) != len(ten):
            print(f"⚠ folder có {len(files)} ảnh, TENFILE có {len(ten)} hero — ghép theo thứ tự "
                  f"{min(len(files), len(ten))} cái đầu, KIỂM BẢNG DƯỚI bằng mắt")
        pairs = list(zip(files, ten))
    dst = vd / "photocard"
    dst.mkdir(parents=True, exist_ok=True)
    rots = [-2.1, 1.7, -1.5, 2.2, -1.8, 1.4, -2.3, 1.6]
    for i, (p, tgt) in enumerate(pairs):
        rot = rots[i % len(rots)]
        if apply:
            sz = build(p, dst / f"{tgt}.png", i + 1, rot)
            print(f"   ✓ {tgt:<28} {sz[0]}×{sz[1]} ({rot:+.1f}°) ← {p.name[:50]}")
        else:
            print(f"   · {tgt:<28} ← {p.name[:60]}")
    if not apply:
        print("\n(xem trước — thêm --apply để ghi)")
    else:
        ims = [Image.open(dst / f"{t}.png").convert("RGB") for _, t in pairs]
        tw = 460
        ims = [im.resize((tw, int(tw * im.height / im.width))) for im in ims]
        cols, rows = 5, (len(ims) + 4) // 5
        sh = Image.new("RGB", (cols * tw, rows * ims[0].height), PAPER)
        for i, im in enumerate(ims):
            sh.paste(im, ((i % cols) * tw, (i // cols) * ims[0].height))
        sh.save(dst / "_photocard_sheet.jpg", quality=86)
        print(f"[SHEET] {dst / '_photocard_sheet.jpg'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
