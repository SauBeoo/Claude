# -*- coding: utf-8 -*-
"""make_avatar_icons.py — cắt ảnh cast thành icon avatar 320×320 đúng khuôn kênh.

VÌ SAO: layout `check`/`compare` của `make_stage.py` gọi icon **theo TÊN**
(`{"icon": "avatar_tanaka"}` → `assets/icons/avatar_tanaka.png`), nên muốn một モニター
xuất hiện trong bảng thì phải có file avatar — **không phải sửa tool**
(`nenkin/CLAUDE.md` §VISUAL). Trước 2026-08-14 chỉ có `avatar_matsumoto` + `avatar_suzuki`.

KHUÔN ĐO TỪ 2 AVATAR CÓ SẴN (đừng đoán): tròn **R=156** trong khung 320 · nền
**(243,232,210)** · vành **(26,42,74) dày 11px** · thân người rộng ~**0.66–0.70 × đường
kính**, neo **đỉnh bbox ở 13–14% chiều cao** (vai bị vòng tròn cắt ở đáy — đúng như bản gốc).

🔴 BẪY ĐÃ DÍNH (3 vòng thử): crop SÁT quanh đầu rồi phóng cho vừa vòng tròn ⇒ mặt to kín
khung, khác hẳn 2 avatar cũ. Phải lấy **cả bán thân** rồi thu nhỏ; và phải **soi ở 132px**
(cỡ thật trên thẻ) chứ không chỉ ở 320px.

CHẠY:  python tools/make_avatar_icons.py          (in ra sheet để duyệt mắt)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
CAST = PROJ / "assets" / "cast"
ICON = PROJ / "assets" / "icons"

S, R = 320, 156
RING = (26, 42, 74)
FILL = (243, 232, 210)
RING_W = 11

# (ảnh cast nguồn, tên avatar ra, crop nguồn hoặc None = cả ảnh, bề rộng/đường kính, neo đỉnh)
#
# `wf` = bề rộng THÂN ĐÃ CROP ÷ đường kính vòng tròn. Người đơn ~0.66–0.72; ảnh NHIỀU người
# (cặp vợ chồng, nhóm) phải nới lên 0.86–0.94, không thì mỗi cái đầu bé xuống dưới ngưỡng đọc
# được ở 132px. `box` chỉ cần khi ảnh gốc có ĐẠO CỤ/BỐI CẢNH chiếm chỗ (bàn, laptop, quầy) —
# crop bỏ đạo cụ đi rồi mới thu nhỏ, nếu không người sẽ bé tí trong vòng tròn.
#
# 🔴 ĐO `box` BẰNG LƯỚI, ĐỪNG ĐOÁN. Hai lần đoán đầu đều sai và chỉ lộ ra ở sheet: `ito_cafe`
# cắt lệch trái ⇒ kệ chai chiếm nửa khung, mặt bị mép phải cắt; `sensei_explain` lấy từ x=400
# trong khi đầu bắt đầu ở x≈180 ⇒ cắt mất nửa đầu. Cách đo 30 giây: vẽ lưới 100px lên ảnh gốc
#   (`ImageDraw.line` + nhãn toạ độ) → đọc hộp đầu+vai bằng mắt → điền vào đây.
# 🔴 ẢNH CÓ NỀN ĐỤC (kệ chai của `ito_cafe`) phải LÀM KHÁC: các ảnh cast khác nền trong suốt
# nên `wf 0.66–0.72` để lộ nền kem của vòng tròn — làm thế với ảnh nền đục thì thấy rõ MÉP
# CHỮ NHẬT của khối crop nằm trong vòng tròn. Cách đúng: crop một ô VUÔNG quanh mặt rồi
# `wf ≈ 1.03` + `top 0.00` để khối phủ kín vòng tròn, hết mép.
# ⚠️ Và với ảnh có BỐI CẢNH ĐẬM thì **đọc lưới bằng mắt vẫn sai** —
# tao đọc tâm mặt ở x≈315 trong khi đo bằng máy ra **x=408** (lệch 93px ⇒ nửa khung là kệ chai).
# Cách đo đúng: quét màu da いらすとや `r>245 · 185<g<225 · 145<b<185` rồi lấy trọng tâm.
JOBS = [
    # ── dàn モニター (roster ở `CLAUDE.md` §SIGNATURE)
    ("tanaka_smile.png", "avatar_tanaka", None, 0.70, 0.14),
    ("takahashi_work.png", "avatar_takahashi", (50, 50, 400, 510), 0.66, 0.14),
    ("sato_smile.png", "avatar_sato", None, 0.70, 0.14),
    ("josei_nod.png", "avatar_watanabe", None, 0.72, 0.13),
    ("ito_cafe.png", "avatar_ito", (228, 150, 588, 510), 1.03, 0.00),   # xem ghi chú NỀN ĐỤC
    ("yamada_happy.png", "avatar_yamada", None, 0.90, 0.16),
    ("suzuki_exec.png", "avatar_suzuki_exec", (150, 10, 545, 430), 0.70, 0.14),
    # ── vai trò / persona
    ("kenkyuin.png", "avatar_kenkyuin", (91, 15, 492, 430), 0.70, 0.14),
    ("sensei_explain.png", "avatar_sensei", (70, 20, 810, 780), 0.70, 0.14),
    ("kikite_nod.png", "avatar_kikite", None, 0.72, 0.13),
    # ── ○× cho khối クイズ / 誤解
    ("quiz_maru.png", "avatar_maru", None, 0.88, 0.15),
    ("quiz_batsu.png", "avatar_batsu", None, 0.88, 0.15),
    # ── "cùng thế hệ" cho khối シェア / 同世代
    ("seniors_work_group.png", "avatar_seniors", None, 0.94, 0.24),
]

# ⚠️ HAI HỌ VẼ KHÁC NHAU, biết mà chấp nhận: `avatar_matsumoto` + `avatar_suzuki` (2 bản có sẵn
# từ trước) thuộc họ vẽ CHI TIẾT/đổ bóng, giống `sensei_*` · `kikite_*` · `josei_*`; còn
# `tanaka/sato/yamada/ito/kenkyuin/quiz` là họ いらすとや PHẲNG. Đặt hai họ cạnh nhau trong CÙNG
# một thẻ thì lộ. Cách né: mỗi thẻ chỉ dùng avatar CÙNG HỌ, hoặc chỉ dùng 1 avatar + icon vật.


def build(src, dst, box, wf, top_f):
    im = Image.open(CAST / src).convert("RGBA")
    crop = im.crop(box) if box else im
    tw = int(2 * R * wf)
    crop = crop.resize((tw, int(crop.height * tw / crop.width)), Image.LANCZOS)
    bb = crop.getchannel("A").getbbox()

    base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    c = S // 2
    ImageDraw.Draw(base).ellipse([c - R, c - R, c + R, c + R], fill=FILL + (255,))

    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    lay.alpha_composite(crop, dest=((S - (bb[2] - bb[0])) // 2 - bb[0], int(S * top_f) - bb[1]))
    msk = Image.new("L", (S, S), 0)
    ImageDraw.Draw(msk).ellipse([c - R, c - R, c + R, c + R], fill=255)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (S, S), 0), msk))
    base.alpha_composite(lay)
    ImageDraw.Draw(base).ellipse([c - R, c - R, c + R, c + R], outline=RING + (255,), width=RING_W)
    base.save(ICON / f"{dst}.png")
    print(f"✅ {dst}.png  ← {src}  (thân {crop.size})")


def main():
    for src, dst, box, wf, top_f in JOBS:
        build(src, dst, box, wf, top_f)
    # sheet duyệt: hàng trên 320px (so với 2 avatar cũ), hàng dưới 132px = cỡ THẬT trên thẻ
    names = ["avatar_matsumoto", "avatar_suzuki"] + [j[1] for j in JOBS]
    cols = 5
    rows = (len(names) + cols - 1) // cols
    cell = S + 160
    sh = Image.new("RGB", (S * cols + 20, cell * rows + 20), (255, 250, 238))
    for i, n in enumerate(names):
        im = Image.open(ICON / f"{n}.png").convert("RGBA")
        x, y = S * (i % cols) + 10, cell * (i // cols) + 10
        sh.paste(im, (x, y), im)
        sm = im.resize((132, 132), Image.LANCZOS)   # cỡ THẬT trên thẻ
        sh.paste(sm, (x + (S - 132) // 2, y + S + 8), sm)
    out = PROJ / "assets" / "icons" / "_avatar_sheet.png"
    sh.save(out)
    print(f"→ duyệt mắt: {out}  (hàng dưới = 132px, cỡ thật trên thẻ)")


if __name__ == "__main__":
    main()
