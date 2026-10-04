# -*- coding: utf-8 -*-
"""
bake_telop.py — Nướng TELOP kiểu phim tài liệu Nhật lên ẢNH THẬT, cho kênh 古代の秘訣.

THAY cho card diagram phẳng (make_diagrams_codai.py): user chốt 2026-07-25 rằng card
vẽ icon PIL trông "xấu / PowerPoint". Cùng lượng thông tin「なぜ」nhưng đặt lên ảnh thật
→ nhìn như một bộ phim tài liệu, không phải slide thuyết trình.

2 KHUÔN:
  1. "telop"  — 1 ảnh full khung + dải tối gradient một bên + 3 tầng chữ
                (kicker nhỏ → head vàng to → body 1–2 dòng) [+ mũi tên đỏ trỏ vào ảnh]
  2. "split"  — 2 ảnh chia đôi + tiêu đề trên dải tối + nhãn/✗○/kết luận mỗi bên
                (dùng cho mọi so sánh: アルカリ✗ vs 酸○, 専用洗剤 vs 灰汁, tiền…)

Cách chạy (SAU fetch_photos / sau khi bỏ ảnh AI vào, TRƯỚC video_render):
    python tools/bake_telop.py 03_SCRIPTS/<x>_SLIDES.json 06_VIDEO/<x>/slides_img

Ảnh nguồn theo index của entry:
  - telop: slide_NN.jpg|png  (fetch_photos tải, hoặc ảnh AI user gen đặt đúng tên)
  - split: slide_NN_L.jpg|png + slide_NN_R.jpg|png  → nướng ra slide_NN.jpg
Bản gốc được cất ở <img_dir>/_raw/ nên chạy lại KHÔNG nướng đè lên bản đã nướng.

Khai báo trong SLIDES.json:
  {"match": "...", "photo": true, "q": "macro foam bubbles",
   "telop": {"kicker": "アルカリ ＋ 酸", "head": "二酸化炭素の泡",
             "body": ["汚れのすき間にもぐり込み、", "下から持ち上げてはがす"],
             "side": "left", "note": "この泡が、いま働いている",
             "arrow": [1150, 600]}}

  {"match": "...", "photo": true,
   "split": {"title": "白い水垢は「アルカリ性」", "sub": "同じ性質では落ちない",
             "left":  {"label": "アルカリの洗剤", "mark": "x", "verdict": "ほとんど効かない"},
             "right": {"label": "酢・クエン酸（酸）", "mark": "o", "verdict": "すっと溶ける"}}}
"""
import json
import math
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
GOLD = (255, 215, 0)
WHITE = (245, 245, 245)
DIM = (206, 212, 224)
RED = (232, 74, 62)
GREEN = (86, 196, 122)
INK = (16, 16, 20)

# Phụ đề burn-in 2 dòng ăn từ ~y=780 xuống (đo thật ở 06_proofA, 2026-07-25)
# → mọi chữ của telop phải nằm TRÊN mốc này.
SAFE_BOTTOM = 780

_fc = {}


def F(s):
    if s not in _fc:
        _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]


def at(d, txt, size, cx, y, fill=WHITE, stroke=0):
    f = F(size)
    d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=INK)


def lf(d, txt, size, x, y, fill=WHITE, stroke=0):
    d.text((x, y), txt, font=F(size), fill=fill, stroke_width=stroke, stroke_fill=INK)


def cover(im, w, h, zoom=1.0, ox=0.5, oy=0.5):
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = int((im.width - w) * ox), int((im.height - h) * oy)
    return im.crop((x, y, x + w, y + h))


def arrow(d, p1, p2, color=RED, width=13, head=30):
    d.line([p1, p2], fill=color, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    pts = [p2]
    for s in (150, -150):
        a = ang + math.radians(s)
        pts.append((p2[0] + head * math.cos(a), p2[1] + head * math.sin(a)))
    d.polygon(pts, fill=color)


def side_gradient(img, side="left", reach=1120, alpha=196):
    """Dải tối mờ dần (KHÔNG mép cắt thẳng) để chữ nổi trên ảnh sáng."""
    col = Image.new("L", (W, 1), 0)
    px = col.load()
    for x in range(W):
        t = (reach - x) / reach if side == "left" else (x - (W - reach)) / reach
        px[x, 0] = int(alpha * max(0.0, min(1.0, t)) ** 0.85)
    return Image.composite(Image.new("RGB", (W, H), (6, 10, 18)), img, col.resize((W, H)))


def mark(d, kind, cx, cy, s):
    if kind == "x":
        for a, b in (((-1, -1), (1, 1)), ((-1, 1), (1, -1))):
            d.line([(cx + a[0] * s, cy + a[1] * s), (cx + b[0] * s, cy + b[1] * s)],
                   fill=RED, width=26)
    else:
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=GREEN, width=24)


# ---------- khuôn 1: telop ----------

def bake_telop(src, spec, out):
    img = cover(Image.open(src).convert("RGB"), W, H,
                zoom=float(spec.get("zoom", 1.0)),
                ox=float(spec.get("ox", 0.5)), oy=float(spec.get("oy", 0.5)))
    side = spec.get("side", "left")
    img = side_gradient(img, side)
    d = ImageDraw.Draw(img, "RGBA")

    x = 96 if side == "left" else W - 96 - 760
    y = int(spec.get("y", 252))
    kicker, head = spec.get("kicker"), spec.get("head", "")
    if kicker:
        d.rectangle([x, y + 6, x + 13, y + 118], fill=GOLD)
        lf(d, kicker, 62, x + 38, y, WHITE, 6)
        y += 88
    lf(d, head, 100, x + 38, y, GOLD, 9)
    y += 160
    for ln in spec.get("body", []):
        lf(d, ln, 50, x + 38, y, WHITE, 5)
        y += 72
        if y > SAFE_BOTTOM - 60:
            break

    if spec.get("arrow"):
        tail = (x + 780, min(y + 40, SAFE_BOTTOM - 90)) if side == "left" \
            else (x - 40, min(y + 40, SAFE_BOTTOM - 90))
        arrow(d, tail, tuple(spec["arrow"]))
        if spec.get("note"):
            lf(d, spec["note"], 42, tail[0] - 74, tail[1] + 36, (255, 200, 190), 6)
    elif spec.get("note"):
        lf(d, spec["note"], 42, x + 38, min(y + 16, SAFE_BOTTOM - 60), (255, 200, 190), 6)

    safe_save(img.convert("RGB"), out)


# ---------- khuôn 2: split-screen ----------

def bake_split(src_l, src_r, spec, out):
    hw = W // 2
    img = Image.new("RGB", (W, H))
    for k, src in ((0, src_l), (1, src_r)):
        half = cover(Image.open(src).convert("RGB"), hw, H)
        img.paste(Image.blend(half, Image.new("RGB", (hw, H), (10, 14, 24)),
                              float(spec.get("dim", 0.34))), (k * hw, 0))
    d = ImageDraw.Draw(img, "RGBA")

    d.rectangle([0, 0, W, 200], fill=(8, 12, 20, 190))
    at(d, spec.get("title", ""), 76, W / 2, 34, GOLD, 7)
    if spec.get("sub"):
        at(d, spec["sub"], 42, W / 2, 138, DIM)
    d.rectangle([hw - 6, 200, hw + 6, H], fill=(230, 230, 235, 200))

    for k, key in ((0, "left"), (1, "right")):
        s = spec.get(key) or {}
        cx = hw / 2 + k * hw
        at(d, s.get("label", ""), 62, cx, 268, WHITE, 7)
        if s.get("mark"):
            mark(d, s["mark"], cx, 524, 90)
        col = RED if s.get("mark") == "x" else GREEN
        at(d, s.get("verdict", ""), 56, cx, SAFE_BOTTOM - 76, col, 7)

    safe_save(img, out)


# ---------- CLI ----------

def find(img_dir, stem):
    return next((p for ext in (".jpg", ".jpeg", ".png")
                 if (p := img_dir / f"{stem}{ext}").exists()), None)


def safe_save(img, out, quality=93):
    """⚠️ BẮT BUỘC ghi qua file tạm rồi os.replace.

    Ảnh do fetch_photos tải về là HARDLINK tới file trong kho chung
    (`Projects/_media_library`) — mở đúng đường dẫn đó mà save là ghi thẳng vào
    inode của kho → ảnh gốc trong kho bị nướng chữ, video sau lấy lại sẽ bị
    nướng telop 2 lần (đã xảy ra 2026-07-25 với ảnh bọt của video 06).
    os.replace tạo inode MỚI ở đường dẫn này → kho giữ nguyên bản sạch.
    """
    fmt = "PNG" if out.suffix.lower() == ".png" else "JPEG"
    tmp = out.with_name(out.name + ".tmp")
    img.save(tmp, format=fmt, quality=quality)
    os.replace(tmp, out)


def raw_of(img_dir, stem):
    """Trả bản gốc (cất ở _raw/), tự cất lần đầu → chạy lại không nướng đè."""
    raw_dir = img_dir / "_raw"
    raw_dir.mkdir(exist_ok=True)
    kept = find(raw_dir, stem)
    if kept:
        return kept
    cur = find(img_dir, stem)
    if cur is None:
        return None
    dst = raw_dir / cur.name
    shutil.copy2(cur, dst)
    return dst


def main():
    if len(sys.argv) < 3:
        raise SystemExit("dùng: python bake_telop.py <SLIDES.json> <folder ảnh>")
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    img_dir = Path(sys.argv[2])
    n, miss = 0, []
    for i, spec in enumerate(cfg):
        if spec.get("telop"):
            src = raw_of(img_dir, f"slide_{i:02d}")
            if src is None:
                miss.append(f"[{i:02d}] telop: thiếu slide_{i:02d}.jpg")
                continue
            out = img_dir / f"slide_{i:02d}{src.suffix if src.suffix != '.png' else '.jpg'}"
            bake_telop(src, spec["telop"], out)
            print(f"[{i:02d}] telop → {out.name}: {spec['telop'].get('head', '')}")
            n += 1
        elif spec.get("split"):
            l = raw_of(img_dir, f"slide_{i:02d}_L")
            r = raw_of(img_dir, f"slide_{i:02d}_R")
            if l is None or r is None:
                miss.append(f"[{i:02d}] split: cần slide_{i:02d}_L + slide_{i:02d}_R")
                continue
            out = img_dir / f"slide_{i:02d}.jpg"
            bake_split(l, r, spec["split"], out)
            print(f"[{i:02d}] split → {out.name}: {spec['split'].get('title', '')}")
            n += 1
    for m in miss:
        print("⚠️ " + m)
    print(f"Xong. {n} khung đã nướng telop → {img_dir}")


if __name__ == "__main__":
    main()
