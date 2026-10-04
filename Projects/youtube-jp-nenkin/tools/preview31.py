# -*- coding: utf-8 -*-
r"""preview31.py — XEM TRƯỚC toàn bộ slide của video 31 TRƯỚC khi có ảnh AI (duyệt chữ/bố cục).

Dùng đúng hàm `layers()` của build28 (chip chương · logo · telop · thẻ phụ · vòng khoanh), ghép
trạng thái CUỐI của mọi lớp thành 1 khung/ô. Ô chưa có ảnh ⇒ ô chờ xám ghi 「画像待ち」+ số ô —
CHỈ để duyệt, ⛔ không bao giờ đi vào bản render (build28 `art_for` vẫn chặn cứng khi thiếu ảnh).

Luật đứng sau (`render-background.md` §1.5): dựng khung lúc chưa có ảnh là ĐÚNG, cái cấm là ghép video.
CHẠY:  python tools/preview31.py   → 06_VIDEO/<stem>/_preview/slide_KKK.png + sheet_NN.png
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import build31  # noqa: E402,F401  (đặt STEM/VD/ART/OUT/PLAN/TELOP vào build28)
import build28 as b  # noqa: E402

PV = b.VD / "_preview"
b.OUT = PV / "_layers"
_orig_art = b.art_for


def _art_or_hold(k):
    p = b.ART / f"shot_{k:03d}.png"
    if p.exists():
        return p
    hold = PV / "_hold" / f"hold_{k:03d}.png"
    hold.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (1376, 768), (246, 241, 228))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([60, 60, 1316, 708], radius=30, outline=(170, 170, 170), width=6)
    f = b.font(90)
    d.text((420, 300), f"画像待ち  #{k:03d}", font=f, fill=(150, 150, 150))
    im.save(hold)
    return hold


b.art_for = _art_or_hold


def main() -> int:
    PV.mkdir(parents=True, exist_ok=True)
    b.OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((b.VD / b.PLAN_NAME).read_text(encoding="utf-8"))
    chap = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                       if c["chip_l"] else c["chip_r"]) for c in plan["chapters"]}
    outs = []
    for k, s in enumerate(plan["shots"]):
        sh = dict(b.TELOP[k]); sh["k"] = k
        sh.setdefault("size", 92); sh.setdefault("sub", [])
        bp, lays = b.layers(sh, chap.get(s["chap"], ""), k)
        fr = Image.open(bp).convert("RGBA")
        for lp, _t, _sl in lays:
            fr.alpha_composite(Image.open(lp).convert("RGBA"))
        d = ImageDraw.Draw(fr)
        cap = s["text"].strip()[:40] or "（前の行のつづき）"
        fc = b.font(40)
        d.text((b.CAP_X0 if hasattr(b, "CAP_X0") else 250, b.H - 110), cap, font=fc, fill=(33, 39, 48))
        op = PV / f"slide_{k:03d}.png"
        fr.convert("RGB").save(op)
        outs.append(op)
    # sheet 4×4, mỗi ô 480×270
    per, cw, ch = 16, 480, 270
    for n in range(0, len(outs), per):
        sheet = Image.new("RGB", (cw * 4, ch * 4), (60, 60, 60))
        for i, op in enumerate(outs[n:n + per]):
            sheet.paste(Image.open(op).resize((cw, ch)), ((i % 4) * cw, (i // 4) * ch))
        sheet.save(PV / f"sheet_{n // per:02d}.png")
    print(f"✅ {len(outs)} slide → {PV}  ·  {(len(outs) + per - 1) // per} sheet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
