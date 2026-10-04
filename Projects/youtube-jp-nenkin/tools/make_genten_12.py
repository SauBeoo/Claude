# -*- coding: utf-8 -*-
"""make_genten_12.py — dựng 3 thẻ 原典ショット cho video 12 (住民税の紙).

VÌ SAO CÓ TOOL NÀY (bắt được khi duyệt contact sheet 2026-08-14):
`genten/*.jpg` là ảnh chụp **CẢ TRANG** 1097×917. Đưa thẳng vào layout `art` thì:
  ① chữ bé như hạt gạo — cover-crop của `L_art` còn cắt mất mép;
  ② **KHÔNG CÓ KHOANH ĐỎ**, trong khi thoại đọc đúng câu 「赤で囲んだところ、ご覧ください」
     ⇒ nói một đằng, hình một nẻo. Đây là lỗi kiểu "claim không có bằng chứng trên màn hình".
Khuôn đúng của kênh: crop vùng câu đang đọc → phóng to → **KHOANH ĐỎ DÀY** → nhãn nguồn
(`CLAUDE.md` §Chuẩn VISUAL ⭐原典スライド, khuôn gốc `make_genten_06.py` của video 06).

⚠️ CHỈ crop + phóng + khoanh ảnh chụp THẬT của trang cơ quan công. Tuyệt đối không vẽ lại
layout trang web (= dựng giả hồ sơ, cấm — `youtube-compliance.md`).

Tỉ lệ ra: **1504×936 = 1.607**, đúng tỉ lệ hộp ảnh của `L_art`
(bw = CONTENT_X1+30 − (CONTENT_X0−30) = 940 · bh ≈ 585) ⇒ cover-crop KHÔNG cắt gì.

CHẠY:  python tools/make_genten_12.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "12_juminzei-koujo-shinkokusho-10gatsu"
RAW = PROJ / "06_VIDEO" / STEM / "genten"
OUT = PROJ / "06_VIDEO" / STEM / "art"

CW, CH = 1504, 936          # tỉ lệ 1.607 — khớp hộp `L_art`
PAPER = (250, 248, 242)
NAVY = (26, 42, 74)
RED = (208, 32, 40)
GREY = (108, 112, 122)
FONT = "C:/Windows/Fonts/yugothb.ttc"

PAD_X = 52                   # lề ngang
TOP = 34                     # lề trên
LAB_H = 62                   # dải nhãn nguồn dưới

# (file nguồn, crop trang gốc (l,t,r,b), [khung đỏ trong toạ độ CROP], nhãn nguồn, file ra)
SHOTS = [
    ("genten_01_nenkinkikou_148man-10gatsu.jpg",
     (35, 222, 1060, 778),
     [(13, 478, 1015, 545)],
     "日本年金機構「令和8年度税制改正による公的年金等に係る主な改正事項」／更新日 2026年6月17日",
     "genten_01_shot.png"),
    ("genten_02_nenkinkikou_hanikakudai-zu.jpg",
     (40, 178, 1010, 752),
     [(700, 240, 832, 350)],
     "日本年金機構「扶養親族等申告書の提出対象の範囲拡大イメージ」／更新日 2026年6月17日",
     "genten_02_shot.png"),
    ("genten_03_nenkinkikou_dashinai-baai-keisanshiki.jpg",
     (40, 82, 1030, 365),
     [(18, 152, 918, 212), (18, 242, 728, 280)],
     "日本年金機構 年金Q&A「扶養親族等申告書を提出しなかった場合は…」／更新日 2025年9月4日",
     "genten_03_shot.png"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for src, box, redboxes, label, dst in SHOTS:
        p = RAW / src
        if not p.exists():
            print(f"🔴 THIẾU ảnh nguồn: {p}")
            sys.exit(1)
        crop = Image.open(p).convert("RGB").crop(box)
        avail_w, avail_h = CW - PAD_X * 2, CH - TOP - LAB_H - 20
        sc = min(avail_w / crop.width, avail_h / crop.height)
        nw, nh = int(crop.width * sc), int(crop.height * sc)
        crop = crop.resize((nw, nh), Image.LANCZOS)

        cv = Image.new("RGB", (CW, CH), PAPER)
        # crop THẤP (ít dòng) thì neo lên trên, đừng canh giữa — canh giữa để lại
        # một khoảng trống lớn phía trên, nhìn như thẻ bị lỗi.
        ox, oy = (CW - nw) // 2, TOP + min(40, max(0, (avail_h - nh) // 2))
        cv.paste(crop, (ox, oy))
        d = ImageDraw.Draw(cv)
        # viền ảnh chụp — cho thấy rõ "đây là một trang web", không phải hình mình vẽ
        d.rectangle([ox - 2, oy - 2, ox + nw + 1, oy + nh + 1], outline=(206, 210, 218), width=3)

        # ⭐ KHOANH ĐỎ DÀY — đúng câu thoại 「赤で囲んだところ」
        for (l, t, r, b) in redboxes:
            d.rounded_rectangle([ox + l * sc, oy + t * sc, ox + r * sc, oy + b * sc],
                                12, outline=RED, width=7)

        # nhãn nguồn: dải navy mảnh dưới cùng
        d.rectangle([0, CH - LAB_H, CW, CH], fill=NAVY)
        f = ImageFont.truetype(FONT, 26)
        while f.getlength(label) > CW - 60 and f.size > 16:
            f = ImageFont.truetype(FONT, f.size - 1)
        d.text((30, CH - LAB_H / 2), label, font=f, fill=(226, 232, 242), anchor="lm")

        cv.save(OUT / dst)
        print(f"✅ {dst}  crop {box} → {nw}×{nh} (×{sc:.2f})  ·  {len(redboxes)} khung đỏ")


if __name__ == "__main__":
    main()
