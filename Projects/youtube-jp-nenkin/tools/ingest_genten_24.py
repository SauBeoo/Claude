# -*- coding: utf-8 -*-
"""ingest_genten_24.py — đóng khung 3 screenshot 原典 THẬT của video 24 (chụp trực tiếp
bằng Claude in Chrome trên 3 trang FAQ 日本年金機構: tetsuduki06 · shikyuyouken03 ·
shikyuyouken06 — URL đối chiếu FACT SHEET `03_SCRIPTS/24_*.md`) thành
card_genten24_01/01_b/02/02_b/03 — khoanh đỏ câu quote + qua make_photocard
(crop=False vì đây là canvas dựng, không phải ảnh AI có watermark).

SRC trỏ vào thư mục screenshot của phiên chụp — ảnh gốc chỉ tồn tại tạm trong Temp,
nên script này KHÔNG chạy lại được nguyên xi cho video sau; giữ lại làm mẫu quy trình
(chụp → khoanh đỏ theo bbox câu quote → make_photocard crop=False)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw
import make_photocard as MP

SRC = Path(r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-4MmVZu")
VDIR = Path(__file__).resolve().parents[1] / "06_VIDEO" / "24_shien-kyufukin-midori-futo-9gatsu"
RAW = VDIR / "genten"
RAW.mkdir(parents=True, exist_ok=True)
PC = VDIR / "photocard"

SHOTS = [
    ("screenshot-1788200231318-0.jpg", "genten24_01", (370, 335, 1180, 390)),   # 毎年9月の第1営業日から順次送付
    ("screenshot-1788200280598-1.jpg", "genten24_02", (600, 373, 720, 396)),    # 月額5,620円
    ("screenshot-1788200312125-2.jpg", "genten24_03", (365, 540, 1180, 582)),   # ご自身で認定請求の手続きが必要
]


def circle(im, box, pad=14, width=6):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    d.ellipse([x0 - pad, y0 - pad, x1 + pad, y1 + pad], outline=(200, 20, 20, 255), width=width)
    return im


def main():
    for fname, stem, box in SHOTS:
        im = Image.open(SRC / fname).convert("RGB")
        full = im.copy()
        circle(full, box, pad=16, width=6)
        raw_full = RAW / f"{stem}.png"
        full.save(raw_full)
        MP.build(raw_full, PC / f"card_{stem}.png", seed=hash(stem) % 1000, rot=None, crop=False)

        # "_b" chỉ cho genten24_01/02 (heroes cần 2 tấm) — macro zoom vào đúng câu quote
        if stem != "genten24_03":
            x0, y0, x1, y1 = box
            cw, ch = x1 - x0, y1 - y0
            mx0 = max(0, x0 - cw * 0.5)
            my0 = max(0, y0 - ch * 1.8)
            mx1 = min(im.width, x1 + cw * 0.5)
            my1 = min(im.height, y1 + ch * 1.8)
            zoom = im.crop((mx0, my0, mx1, my1)).convert("RGB")
            zoom = zoom.resize((zoom.width * 2, zoom.height * 2), Image.LANCZOS)
            zbox = ((x0 - mx0) * 2, (y0 - my0) * 2, (x1 - mx0) * 2, (y1 - my0) * 2)
            circle(zoom, zbox, pad=20, width=8)
            raw_b = RAW / f"{stem}_b.png"
            zoom.save(raw_b)
            MP.build(raw_b, PC / f"card_{stem}_b.png", seed=hash(stem + '_b') % 1000, rot=None, crop=False)
        print(f"   ok {stem}")
    print("done")


if __name__ == "__main__":
    main()
