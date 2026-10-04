# -*- coding: utf-8 -*-
r"""ingest_genten_13.py — cắt 4 原典ショット cho video 13 + khoanh ĐỎ + nhãn nguồn.

VÌ SAO CÓ TOOL NÀY (không làm tay bằng ảnh chỉnh sửa):
`art` của `make_stage.py` **cover-crop về tỉ lệ 1,60** (940×588). Đưa ảnh tỉ lệ khác là bị cắt
mất chữ hai đầu — đúng lỗi đã dính ở video 11 (`media-library.md` §2.10 ②: chụp dải ngang 5:1
⇒ 「提出を受けていない場合」 hiển thị thành 「だけていない場合」). Tool này ép đúng 1,60 bằng cách
**pad nền trắng** khi vùng cần cắt dẹt hơn, chứ KHÔNG cắt bớt chữ.

🔴 SỐ TRANG TRONG FACT SHEET ĐÃ SAI — tool này ghi lại số ĐÚNG (đo bằng cách mở PDF thật):
    · 報酬比例部分の3/4        → ガイド **p.6**  (FACT SHEET ghi p.4 ✗)
    · 中高齢寡婦加算 635,500円 + 【ご注意ください】20年 → ガイド **p.7** (ghi p.5 ✗)
    · 65歳以降の調整 ①② + 支給停止 → ガイド **p.7** (ghi p.7 ✓)
    · 影響を受けない方 (1)(2)(3)  → 厚労省 **p.1** (ghi p.1 ✓)
  ⇒ Tên file cũng đổi theo trang thật, và `build_slides_13.py` + FACT SHEET phải khớp.

⚖️ Ảnh nguồn là **screenshot trang PDF của cơ quan công** (日本年金機構 / 厚生労働省), chụp qua
Chrome PDF viewer. KHÔNG gen bằng AI (gen = bịa nguồn, vi phạm YMYL #2). Toạ độ vùng cắt/khoanh
đo bằng MẮT trên screenshot 1568×772 rồi ghi thành PHÂN SỐ ⇒ đổi độ phân giải vẫn đúng.

CHẠY:  python tools/ingest_genten_13.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\tuana\AppData\Local\Temp\claude-chrome-screenshots-YIewg9")
OUT = PROJ / "06_VIDEO" / "13_izoku-nenkin-tsuki13man9sen" / "art"
FONT = Path(r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Bold.otf")

W0, H0 = 1568.0, 772.0        # khổ screenshot lúc đo toạ độ
RED = (214, 40, 40)
AR = 940 / 588               # = 1,5986 — tỉ lệ ô ảnh của layout `art`

# (file nguồn, tên ra, vùng cắt x0,y0,x1,y1, [các khung đỏ], nhãn nguồn)
JOBS = [
    ("screenshot-1786976254707-3.jpg", "genten_01_kikou_p6.png",
     (360, 150, 1180, 662),
     [(425, 252, 995, 315)],
     "日本年金機構『遺族年金ガイド 令和8年度版』6ページ"),

    ("screenshot-1786976726948-9.jpg", "genten_03_kikou_p7.png",
     (398, 92, 1166, 572),
     [(468, 220, 1130, 274), (478, 528, 1082, 552)],
     "日本年金機構『遺族年金ガイド 令和8年度版』7ページ"),

    ("screenshot-1786976354824-4.jpg", "genten_02_kikou_p7.png",
     (380, 408, 1200, 770),
     [(450, 486, 588, 518), (388, 698, 1190, 770)],
     "日本年金機構『遺族年金ガイド 令和8年度版』7ページ【ご注意ください】"),

    ("screenshot-1786976485909-6.jpg", "genten_04_mhlw_p1.png",
     (430, 55, 1480, 711),
     [(446, 346, 1470, 412)],
     "厚生労働省『遺族厚生年金の見直しに対して寄せられている指摘への考え方』1ページ"),
]


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    for src, name, box, reds, cap in JOBS:
        p = SRC / src
        if not p.exists():
            print(f"🔴 thiếu ảnh nguồn {src} — chụp lại rồi chạy lại")
            continue
        im = Image.open(p).convert("RGB")
        sx, sy = im.width / W0, im.height / H0
        x0, y0, x1, y1 = (box[0] * sx, box[1] * sy, box[2] * sx, box[3] * sy)
        crop = im.crop((int(x0), int(y0), int(x1), int(y1)))

        d = ImageDraw.Draw(crop)
        for rx0, ry0, rx1, ry1 in reds:      # khung ĐỎ, toạ độ đổi về gốc của bản cắt
            d.rounded_rectangle([rx0 * sx - x0, ry0 * sy - y0, rx1 * sx - x0, ry1 * sy - y0],
                                8, outline=RED, width=max(4, int(5 * sx)))

        # 🔴 chừa DẢI TRẮNG RIÊNG ở đáy cho nhãn nguồn. Bản đầu vẽ nhãn đè thẳng lên bản cắt
        # ⇒ nó nằm trên chữ của tài liệu (thấy rõ ở genten_03: 「出典…」 đè 「点ですでに65歳」).
        band = max(30, int(crop.height * 0.062))
        base = Image.new("RGB", (crop.width, crop.height + band), (255, 255, 255))
        base.paste(crop, (0, 0))
        crop = base
        # ép đúng tỉ lệ 1,60 bằng PAD NỀN TRẮNG — tuyệt đối không cắt bớt chữ
        w, h = crop.size
        tw_, th_ = (w, int(round(w / AR))) if w / h > AR else (int(round(h * AR)), h)
        tw_, th_ = max(tw_, w), max(th_, h)
        canvas = Image.new("RGB", (tw_, th_), (255, 255, 255))
        canvas.paste(crop, ((tw_ - w) // 2, (th_ - h) // 2))

        # nhãn nguồn góc dưới (bắt buộc theo `CLAUDE.md` §VISUAL: tên cơ quan + 年月時点)
        d2 = ImageDraw.Draw(canvas)
        f = ImageFont.truetype(str(FONT), max(15, int(th_ * 0.030)))
        t = f"出典：{cap}（2026年8月時点）"
        tw2 = d2.textlength(t, font=f)
        d2.text((11, th_ - f.size - 8), t, font=f, fill=(60, 72, 96))

        canvas.save(OUT / name)
        print(f"  ✓ {name}  {canvas.size[0]}×{canvas.size[1]} "
              f"(tỉ lệ {canvas.size[0]/canvas.size[1]:.3f}, cần {AR:.3f})")
    print(f"→ {OUT}")


if __name__ == "__main__":
    run()
