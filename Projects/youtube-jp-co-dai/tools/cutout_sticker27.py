# -*- coding: utf-8 -*-
r"""cutout_sticker27.py — cắt nền MAGENTA lô sticker video 27 → 06_VIDEO/27_*/sticker/el_*.png

Chép cơ chế `cutout_sticker26.py` nguyên vẹn (tách theo khoảng cách màu tới magenta, loại
pixel ngả magenta rồi erode 1px, giữ blob lớn nhất, nghiệm thu đếm pixel ngả tím).

🔴 Ghép tên: generator đặt tên theo NỘI DUNG ảnh, không theo SPEC ⇒ điền MAP tiền tố → tên
   đích SAU KHI xem folder gen (đối chiếu bằng mắt), hoặc dùng --order nếu gen đúng thứ tự FLOW.

CHẠY:  python tools/cutout_sticker27.py --src "C:\Users\tuana\Downloads\<folder>" [--apply] [--order]
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
STEM = "27_kankisen-abura-akujiru"

# tiền tố tên file generator (đủ dài để duy nhất) → tên đích. ĐIỀN SAU KHI XEM FOLDER GEN.
MAP = {
    # "Some_generator_filename_prefix": "el_ten_dich.png",
}

TOL = 118.0
PAPER = (242, 237, 228)


def _imread(p):
    buf = np.fromfile(str(p), dtype=np.uint8)
    return cv2.imdecode(buf, cv2.IMREAD_COLOR)


def _imwrite(p, im):
    ok, buf = cv2.imencode(p.suffix, im)
    if ok:
        buf.tofile(str(p))
    return ok


def cutout(bgr):
    rgb = bgr[:, :, ::-1].astype(np.float32)
    dist = np.linalg.norm(rgb - np.array([255, 0, 255], np.float32), axis=2)
    mask = (dist > TOL).astype(np.uint8)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    tinted = (r - g > 34) & (b - g > 34)
    mask[tinted] = 0
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n > 1:
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        mask = (lab == big).astype(np.uint8)
    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None, 0
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    out = np.dstack([bgr, (mask * 255).astype(np.uint8)])[y0:y1, x0:x1]
    o = out.astype(np.int32)
    solid = o[..., 3] > 250
    viol = int((solid & (o[..., 2] - o[..., 1] > 40) & (o[..., 0] - o[..., 1] > 40)).sum())
    return out, viol


def main():
    if "--src" not in sys.argv:
        print("dùng: python tools/cutout_sticker27.py --src <folder> [--apply] [--order]")
        return 1
    src = Path(sys.argv[sys.argv.index("--src") + 1])
    apply = "--apply" in sys.argv
    dst = PROJ / "06_VIDEO" / STEM / "sticker"
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    order = {}
    if "--order" in sys.argv:
        ten = [l.split()[0] for l in (PROJ / "06_VIDEO" / STEM / "sticker_prompts_TENFILE.txt")
               .read_text(encoding="utf-8").splitlines() if l.strip()]
        byt = sorted(files, key=lambda q: q.stat().st_mtime)
        if len(byt) != len(ten):
            print(f"⚠ folder {len(byt)} ảnh ≠ TENFILE {len(ten)} — ghép {min(len(byt), len(ten))} cái đầu, SOI BẢNG")
        order = {q.name: t for q, t in zip(byt, ten)}
    done, un = 0, []
    tiles = []
    for p in files:
        tgt = order.get(p.name) or next((v for k, v in MAP.items() if p.name.startswith(k)), None)
        if not tgt:
            un.append(p.name)
            continue
        im = _imread(p)
        if im is None:
            print(f"🔴 đọc không được {p.name}")
            continue
        out, viol = cutout(im)
        if out is None:
            print(f"🔴 {p.name}: không tách được (nền không phải magenta?)")
            continue
        flag = "⚠ TÍM" if viol > 50 else "ok"
        print(f"   {'✓' if apply else '·'} {tgt:<22} {out.shape[1]}×{out.shape[0]}  tím={viol:<5} {flag}  ← {p.name[:48]}")
        if apply:
            _imwrite(dst / tgt, out)
            done += 1
        tiles.append((tgt, out))
    if un:
        print(f"\n⚠ {len(un)} ảnh không khớp MAP (điền MAP rồi chạy lại):")
        for u in un:
            print(f"     {u}")
    if tiles:
        h = 260
        cols = []
        for _, o in tiles:
            s = h / o.shape[0]
            r = cv2.resize(o, (max(1, int(o.shape[1] * s)), h))
            bg = np.full((h, r.shape[1], 3), PAPER[::-1], np.uint8)
            a = r[..., 3:4].astype(np.float32) / 255
            comp = (r[..., :3] * a + bg * (1 - a)).astype(np.uint8)
            cols.append(comp)
        sheet = np.hstack(cols)
        _imwrite(dst / "_sticker_sheet.jpg", sheet)
        print(f"[SHEET] {dst / '_sticker_sheet.jpg'}")
    print(f"\n{'✓ ghi' if apply else '· xem trước'} {done if apply else len(tiles)} sticker → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
