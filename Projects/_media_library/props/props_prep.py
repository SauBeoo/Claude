# -*- coding: utf-8 -*-
"""props_prep.py — chuẩn hoá bộ đạo cụ analog cho lớp vox collage (2026-08-08).

Hai đường xử lý, chọn theo BẢN CHẤT prop:
  KEY  — vết mực/sáp/dấu trên giấy trắng: alpha = độ lệch màu khỏi NỀN (ước lượng từ
         4 góc). Giữ nguyên texture sáp + mép antialias. ⛔ KHÔNG rembg loại này —
         rembg sinh ra cho VẬT, nó ăn mất nét mảnh (đuôi mũi tên, mép grunge con dấu).
  CUT  — vật đặc (đinh, kẹp, dây, giấy xé, băng dính): rembg + lọc haze như cutout
         thường (mượn load_cutout của make_vox — cùng tham số đã hiệu chuẩn).

Output: props/<tên>.png (RGBA, trim bbox, cạnh dài ≤1400) + INDEX.json (kind, method,
anchor mũi tên tail/head để make_vox xoay theo vector) + _props_sheet.jpg duyệt mắt.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW = HERE / "_raw"

# tên raw (prefix) → (tên chuẩn, phương pháp, kind)
MAP = {
    "Red_crayon_arrow_on_paper":       ("arrow_straight", "key", "arrow"),
    "Red_crayon_drawing_arrow":        ("arrow_hook",     "key", "arrow"),
    "Red_crayon_drawn_arrow":          ("arrow_curve",    "key", "arrow"),
    "Red_wax_crayon_circled_ellipse":  ("circle_1",       "key", "circle"),
    "Red_crayon_hand-drawn_circle":    ("circle_2",       "key", "circle"),
    "Red_crayon_X_cross":              ("cross_x",        "key", "mark"),
    "Red_rubber_stamp_imprint":        ("stamp_round",    "key", "stamp"),
    "Blank_red_rubber_stamp_imprint":  ("stamp_rect",     "key", "stamp"),
    "Dried_coffee_cup_ring_stain":     ("stain_coffee",   "key", "decor"),
    "Red_fingerprint_on_white":        ("smudge_ink",     "key", "decor"),
    "Red_cotton_twine_curve":          ("string_arc",     "cut", "string"),
    "Red_cotton_twine_sagging":        ("string_sag",     "cut", "string"),
    "Red_push_pin_photographed":       ("pin_red",        "cut", "pin"),
    "Vintage_brass_thumbtack":         ("pin_brass",      "cut", "pin"),
    "Blank_aged_washi_paper_strip":    ("label_strip",    "cut", "label"),
    "Torn_kraft_paper_macro":          ("label_tag",      "cut", "label"),
    "Aged_manila_paper_torn_edges":    ("label_wide",     "cut", "label"),
    "Beige_washi_masking_tape_strip":  ("tape_1",         "cut", "tape"),
    "Tear_of_masking_tape":            ("tape_2",         "cut", "tape"),
    "Rusty_metal_paper_clip":          ("clip_1",         "cut", "decor"),
}


def key_alpha(im, strength=2.2, floor=14):
    """Key theo ĐỘ ĐỎ: alpha ~ (R − trung bình(G,B)). Vết sáp/mực/dấu ĐỎ giữ nguyên
    texture + mép antialias; giấy nền (trắng HAY xám, R≈G≈B) tự về 0 — chữa dứt bệnh
    'bóng ma tờ giấy' của keying khoảng-cách-màu (vòng 1+2, arrow_straight gen trên
    giấy xám texture). Vết nâu (cà phê) ra alpha lửng = đúng bản chất vết ố."""
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    redness = a[:, :, 0] - (a[:, :, 1] + a[:, :, 2]) / 2.0
    alpha = np.clip((redness - 9.0) * 3.4, 0, 255)
    out = np.dstack([a, alpha]).astype("uint8")
    return Image.fromarray(out, "RGBA")


def trim(im, pad=6):
    bb = im.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad),
                    min(im.width, x1 + pad), min(im.height, y1 + pad)))


def arrow_anchors(im, name):
    """Anchor (tail, head) theo pixel ảnh đã trim — make_vox xoay prop theo vector này.
    Cả 3 mũi tên đều trỏ sang PHẢI (đã duyệt mắt sheet raw):
      straight: tail = mép trái, head = mép phải (cùng hàng)
      curve:    tail = mép trái (đầu cung), head = mũi dưới-phải
      hook:     tail = đỉnh TRÊN của nét dọc, head = mép phải
    """
    a = np.asarray(im.getchannel("A"), dtype=np.uint8)
    ys, xs = np.nonzero(a > 60)
    if len(xs) == 0:
        return None
    left = int(xs.min()); right = int(xs.max()); top = int(ys.min())
    y_at_left = int(np.median(ys[xs <= left + 8]))
    y_at_right = int(np.median(ys[xs >= right - 8]))
    x_at_top = int(np.median(xs[ys <= top + 8]))
    if name == "arrow_hook":
        tail = (x_at_top, top)
    else:
        tail = (left, y_at_left)
    head = (right, y_at_right)
    return {"tail": tail, "head": head}


def main():
    from make_vox import load_cutout               # tham số lọc haze đã hiệu chuẩn
    from rembg import remove

    idx = {}
    outs = []
    raws = {p.stem.rsplit("_2026", 1)[0]: p for p in sorted(RAW.glob("*.*"))}
    for prefix, (name, method, kind) in MAP.items():
        src = next((p for k, p in raws.items() if k.startswith(prefix[:28])), None)
        if src is None:
            print(f"  ✗ THIẾU raw cho {name} (prefix {prefix})")
            continue
        im = Image.open(src).convert("RGB")
        if method == "key":
            out = trim(key_alpha(im))
        else:
            tmp = HERE / f"_cut_{name}.png"
            remove(im).save(tmp)
            out = load_cutout(tmp, max_h=1400)
            tmp.unlink(missing_ok=True)
        if max(out.size) > 1400:
            sc = 1400 / max(out.size)
            out = out.resize((int(out.width * sc), int(out.height * sc)), Image.LANCZOS)
        meta = {"kind": kind, "method": method, "w": out.width, "h": out.height,
                "src": src.name}
        if kind == "arrow":
            meta["anchors"] = arrow_anchors(out, name)
        out.save(HERE / f"{name}.png")
        idx[name] = meta
        outs.append((name, out))
        print(f"  ✓ {name:16s} {method}  {out.width}×{out.height}"
              + (f"  anchors={meta.get('anchors')}" if kind == "arrow" else ""))

    (HERE / "INDEX.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    # contact sheet nền carô (thấy vùng trong suốt)
    cols, cell = 4, 440
    rows = (len(outs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell, rows * (cell + 30)), (40, 40, 44))
    d = ImageDraw.Draw(sh)
    try:
        f = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        f = ImageFont.load_default()
    for i in range(0, cols * cell, 44):
        for j in range(0, rows * (cell + 30), 44):
            if (i // 44 + j // 44) % 2:
                d.rectangle([i, j, i + 44, j + 44], fill=(52, 52, 58))
    for i, (name, im) in enumerate(outs):
        t = im.copy()
        t.thumbnail((cell - 20, cell - 20))
        x, y = (i % cols) * cell, (i // cols) * (cell + 30)
        sh.paste(t, (x + (cell - t.width) // 2, y + (cell - 20 - t.height) // 2), t)
        d.text((x + 10, y + cell - 16), name, font=f, fill=(255, 220, 80))
    sh.save(HERE / "_props_sheet.jpg", quality=90)
    print(f"\n✅ {len(outs)}/20 prop → {HERE}\\_props_sheet.jpg — DUYỆT MẮT trước khi nối vào tool")


if __name__ == "__main__":
    main()
