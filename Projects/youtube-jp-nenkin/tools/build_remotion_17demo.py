# -*- coding: utf-8 -*-
r"""build_remotion_17demo.py — sinh `project.json` cho `remotion-vox` project
`nenkin-17-demo`: **khung 2 nhân vật 2 bên + vùng giữa TOÀN STICKER ẢNH** (kiểu okura-demo).

⭐ USER CHỐT 2026-08-26 (lần 4): *"toàn bộ frame đều là ảnh hết. Vẫn giữ khung 2 nhân vật
2 bên. Tôi muốn làm các remotion giống okura-demo"*.
⇒ Bỏ hẳn đường `make_stage` (card chữ + thẻ `check`/`big`). Mọi frame là ảnh.

🔴 CÁCH GIỮ 2 CAST TRONG REMOTION — không cần viết component mới:
`remotion-vox` KHÔNG có component `Cast`/`Stage` (kiểm `src/components/`: chỉ Background ·
Sticker · TextClip · Footage · CaptionLayer). Nhưng track **`sticker`** đã đủ: 2 track riêng
`trk-cast-l` / `trk-cast-r`, mỗi track là chuỗi clip cast nối tiếp (đổi biểu cảm theo đoạn),
ghim `x` ở 2 mép, `idle.amp` nhỏ để không "chết cứng". ⇒ 0 dòng code mới.

📐 KHUNG (1920×1080): cast trái chiếm ~x 0–330, cast phải ~x 1590–1920 (khớp `ZU_CAST`
528/1525 của make_stage) ⇒ **vùng sân khấu giữa còn x 340–1580**. Mọi sticker nội dung phải
nằm trong dải đó, nếu không cast đè lên.

⚠️ LÔ DEMO NÀY DÙNG TÀI SẢN TẠM: sticker là 6 icon phẳng của `_media_library/stage_icons`
(vector navy, KHÔNG phải collage) — cố ý, để duyệt **LAYOUT + nhịp** trước khi user gen 15
sticker collage thật (`tools/sticker_prompts_collage.py` đã xuất prompt). Bộ thật sẽ thay
đúng tên file `el_*.png`.

CHẠY:  python tools/build_remotion_17demo.py
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NL = chr(10)            # viết thế này để khỏi lệ thuộc escape trong f-string/heredoc
INK = "#1C2A4A"         # navy đậm — chữ trên băng giấy kem (khớp ảnh mẫu)
RED = "#A82026"         # đỏ mực — dành cho câu ĐÂM
RV = Path(r"E:\Claude\Projects\remotion-vox")
NAME = "nenkin-17-demo"
FPS = 30
DUR = 108 * FPS         # 108s = voice.mp3 ghép: 第1章 (46s) + 第8章 số liệu (62s)

CAST_H = 620            # 🔴 cố định CHIỀU CAO, KHÔNG cố định w — xem CAST bên dưới
CAST_FEET_Y = 1052      # mốc chân chung cho mọi cast
CAST_MARGIN = 4

# 🔴 CAST: cố định CHIỀU CAO rồi suy `w` theo tỉ lệ ảnh. Bộ cast của kênh có ratio lệch
# nhau **0,626 → 0,816** (sensei_serious 801×1280 vs sensei_point 1044×1280) ⇒ nếu đặt
# cùng `w` thì ảnh hẹp-cao bị kéo cao hơn hẳn, **chân không cùng mốc** và người cao người
# thấp — đúng lỗi đã thấy ở still đầu tiên. Schema `LayoutSchema` chỉ có {x,y,w} (không có
# h) nên phải tự tính: `w = CAST_H × ratio`, `y = CAST_FEET_Y − CAST_H`.
# ⓘ `media-library.md` §2.10 ⑨ ⑦ nói cân theo CỠ ĐẦU — đúng khi crop mỗi ảnh một kiểu.
# Bộ `assets/cast` của kênh cùng một nguồn, cao 1280px và crop đồng nhất, nên cân theo
# chiều cao là đủ; ngày nào trộn cast từ lô khác thì phải quay về đo đầu.
# ⚠️ CHỈ đưa vào đây những cast THẬT SỰ DÙNG — `_CW` lấy max của dict này, nên thêm một
# ảnh rộng là **bóp dải sân khấu của cả video**. Đo thật: `sensei_explain` ratio 1,004 ⇒
# w@620 = **622px** ⇒ dải còn 620px < bảng số liệu 810px ⇒ bảng lọt ra ngoài. Đã bỏ nó,
# dùng `sensei_reassure` (0,754) + `sensei_conclude` (0,630) — cả hai ≤ `sensei_point`
# 0,816 nên dải giữ nguyên 852px.
CAST_RATIO = {
    "sensei_serious": 801 / 1280, "sensei_caution": 990 / 1280,
    "sensei_point": 1044 / 1280, "sensei_reassure": 965 / 1280,
    "sensei_conclude": 806 / 1280,
    "kikite_worried": 871 / 1280, "kikite_surprised": 1028 / 1280,
    "kikite_listen": 967 / 1280, "kikite_nod": 908 / 1280,
}

# 🔴 DẢI SÂN KHẤU PHẢI SUY TỪ CAST RỘNG NHẤT, đừng đặt số cố định.
# Bản đầu tao hằng-số hoá `STAGE_X0=340 / X1=1580` (bê từ `ZU_CAST` 528/1525 của make_stage)
# rồi gate báo "✓ mọi sticker trong dải" — nhưng cast ở đây cao 620px nên ảnh rộng nhất
# (`sensei_point`, ratio 0,816) chiếm tới **x 4–510**, tức gate cho qua sticker ở x=380 mà
# thực tế **cast đè lên nó** (thấy rõ ở still frame 850: sổ 通帳 nằm dưới tay sensei).
# ⇒ gate chỉ có nghĩa khi ngưỡng của nó được TÍNH từ chính thứ nó bảo vệ.
_CW = round(CAST_H * max(CAST_RATIO.values()))     # cast rộng nhất
STAGE_X0 = CAST_MARGIN + _CW + 24
STAGE_X1 = 1920 - CAST_MARGIN - _CW - 24

# phụ đề (cắt từ subs.srt của demo17s, đã quy sang frame @30fps)
LINES = [
    (0, 154, "その電話は、机の上のスマートフォンを、震わせました。"),
    (154, 190, "出ますか。"),
    (190, 267, "それとも、出ませんか。"),
    (267, 317, "——出た、とします。"),
    (317, 386, "機械の声が、言います。"),
    (386, 478, "「こちらは、日本年金機構です。"),
    (478, 602, "書類の提出が確認できないため、来月から、"),
    (602, 682, "年金の支給が停止されます。"),
    (682, 762, "至急、1を押してください」"),
    (762, 816, "支給停止。"),
    (816, 953, "その四文字が、頭の中で膨らんでいく間に、指は、"),
    (953, 1049, "もう1のボタンに向かっています。"),
    (1049, 1154, "これは、あなたの話かもしれません。"),
    (1154, 1297, "実際にこの電話を受けたのは、鈴木さん、65歳。"),
    (1297, 1380, "今年、会社を退職したばかりの、平日の昼下がりでした。"),
    # ── 第8章 số liệu (ghép từ giây 215,1 của voice gốc, dời về mốc 46s) ──
    (1382, 1505, "最後に、数字を、確かめておきます。"),
    (1505, 1566, "警察庁の統計です。"),
    (1566, 1727, "令和7年、1年間の特殊詐欺の被害総額は、全国で、"),
    (1727, 1800, "およそ3,257億円。"),
    (1800, 1921, "このうち、還付金をかたる詐欺だけで、"),
    (1921, 2028, "2,087件が確認されています。"),
    (2028, 2135, "そして、今年——令和8年の上半期、"),
    (2135, 2293, "1月から6月までの被害額は、およそ1,816億円。"),
    (2293, 2451, "前の年の同じ時期と比べて、5割以上、増えています。"),
    (2451, 2564, "1日あたり、およそ10億円の被害が、"),
    (2564, 2652, "いまも出続けている計算です。"),
    (2652, 2739, "これは、あらゆる手口を合わせた、"),
    (2739, 2804, "特殊詐欺全体の数字です。"),
    (2804, 2929, "年金機構をかたる手口だけの数字ではありません。"),
    (2929, 3054, "ただ、その中に、鈴木さんが受けたような電話が、"),
    (3054, 3113, "確かに含まれています。"),
    (3113, 3240, "数字が小さくなる気配は、いまのところ、ありません。"),
]

# ── 4 SCENE (mốc frame theo đúng nhịp lời đọc ở trên) ────────────────────────
SCENES = [
    dict(f=0,    to=317,  tag="電話",     splash=["#C8B88A", "#9FB6C8"]),
    dict(f=317,  to=762,  tag="機械の声", splash=["#C87A72", "#C8B88A"]),
    dict(f=762,  to=1049, tag="支給停止", splash=["#B44A4A", "#8A93A8"]),
    dict(f=1049, to=1382, tag="あなたの話", splash=["#8FA9C0", "#C8B88A"]),
    # ── 3 scene SỐ LIỆU + CÔNG THỨC (user chốt 2026-08-26 lần 6) ──
    dict(f=1382, to=2028, tag="令和7年",   splash=["#8A93A8", "#C8B88A"]),
    dict(f=2028, to=2652, tag="令和8年",   splash=["#B44A4A", "#C8B88A"]),
    dict(f=2652, to=DUR,  tag="読み方",    splash=["#8FA9C0", "#9FB6C8"]),
]


def bg(i, s):
    return dict(id=f"bg-{i}", kind="background", **{"from": s["f"]},
                durationInFrames=s["to"] - s["f"],
                paper="assets/paper.jpg", tint="#F2EDE4", tintOpacity=0.55,
                grid=True, dots=True, splash=s["splash"])


def stick(id_, asset, f, dur, x, y, w, rot=0, ent="rise", delay=0, amp=5, ph=0.0, sh="lg"):
    return {"id": id_, "kind": "sticker", "from": f, "durationInFrames": dur,
            "asset": asset,
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": ent, "delayFrames": delay, "params": {}},
            "exit": None, "idle": {"amp": amp, "phase": ph}, "shadow": sh}


def txt(id_, content, f, dur, preset, color="#FFE01B", anim="pop", layout=None):
    return {"id": id_, "kind": "text", "from": f, "durationInFrames": dur,
            "content": content, "preset": preset, "color": color,
            "animation": anim, "animationParams": {"restDeg": -1.5},
            "layout": layout or {}, "fontSize": None}


def main():
    # ── track nền ────────────────────────────────────────────────────────────
    trk_bg = [bg(i + 1, s) for i, s in enumerate(SCENES)]

    # ── 2 CAST ghim 2 mép, đổi biểu cảm theo scene ──────────────────────────
    # y đặt sao cho chân cast chạm gần đáy khung; w = CAST_W.
    cast_l, cast_r = [], []
    L = ["sensei_serious", "sensei_caution", "sensei_caution", "sensei_point",
         "sensei_reassure", "sensei_serious", "sensei_conclude"]
    R = ["kikite_listen", "kikite_worried", "kikite_surprised", "kikite_worried",
         "kikite_listen", "kikite_worried", "kikite_nod"]
    cy = CAST_FEET_Y - CAST_H
    for i, s in enumerate(SCENES):
        d = s["to"] - s["f"]
        # entrance chỉ ở scene đầu; các scene sau đổi ảnh mà không "nhảy vào" lại
        ent = "rise" if i == 0 else "none"
        wl = round(CAST_H * CAST_RATIO[L[i]])
        wr = round(CAST_H * CAST_RATIO[R[i]])
        cast_l.append(stick(f"cl-{i+1}", f"assets/{L[i]}.png", s["f"], d,
                            x=CAST_MARGIN, y=cy, w=wl, ent=ent, amp=3, ph=0.4, sh="sm"))
        cast_r.append(stick(f"cr-{i+1}", f"assets/{R[i]}.png", s["f"], d,
                            x=1920 - wr - CAST_MARGIN, y=cy, w=wr, ent=ent,
                            amp=3, ph=2.7, sh="sm"))

    # ── HERO = MẢNH ẢNH DÁN (photocard) · SUP = sticker vật ─────────────────
    # ⭐ user chốt 2026-08-26 lần 5: đưa 5 ảnh collage trong Downloads vào frame.
    # Ảnh đó là SCENE đầy đủ nên không cutout được (rembg cắt cả mảng giấy) ⇒
    # `tools/make_photocard.py` đóng khung chúng thành mảnh ảnh xé mép + tape + bóng,
    # rồi dán vào dải sân khấu như một mảnh giấy. Đây là hero của mỗi scene.
    # ⚠️ photocard ~1360×910 (ratio 1,49) — dải chỉ 852px ⇒ đặt w = 830 là vừa,
    # cao ≈ 556, đủ chỗ cho tag ở trên và punch/phụ đề ở dưới.
    # 🔴 Dải chỉ ~852px (cast ăn 2×506). Bản đầu tao bê layout của `okura-demo`
    # (hero w=900 ở x=480, sup ở x=150 và x=1400) — nhưng okura **không có cast** nên nó
    # dùng trọn 1920. Ở đây hero 600 + 2 sup 250 hai bên là **1.100px > 852**, không vừa.
    # ⇒ hero hạ về ~480–520 và sup xếp **thấp hơn hero** (chồng lớp theo chiều DỌC, đúng
    # chất collage) thay vì đứng hai bên.
    cx = (STAGE_X0 + STAGE_X1) // 2
    HW = 830                                  # photocard hero (dải 852 → chừa 11px mỗi bên)
    SW = 150                                  # sup vật
    hx = cx - HW // 2
    # 🔴 SUP CHỈ ĐƯỢC ĐỨNG BÊN PHẢI-DƯỚI. Dải punch (`papercut-punch`) neo `bottom:110`
    # và bắt đầu ở x = STAGE_X0+20 ⇒ nó chiếm trọn góc TRÁI-DƯỚI. Bản trước tao để sup ở
    # `sxl` cùng vùng đó ⇒ punch đè lên sup (thấy rõ ở still frame 850: máy tính nằm dưới
    # dải chữ). Photocard chiếm y 150–706, nên khe cho sup chỉ là y≈712–862.
    # 🔴 ĐỔI 712 → 590 (2026-08-26 lần 7): khi punch đổi sang `papercut-banner` thì nó
    # `nowrap` nên rộng ~760px và neo `bottom:150` ⇒ chiếm y ≈ 790–930. Photocard chiếm
    # y 150–706. Khe còn lại cho sup chỉ **78px** — không đủ cho sticker 150px, và bản
    # trước sup bị banner đè (đã thấy ở still `_bn_150`: lịch nằm dưới dải chữ).
    # ⇒ Sup **CHỒNG LÊN góc dưới-phải photocard** — đúng chất collage (sticker dán đè lên
    # mảnh ảnh), và là cách okura-demo vẫn làm. Không cần nới gate: 1234–1384 vẫn trong dải.
    SUP_Y = 590
    sxr = STAGE_X1 - SW - 2
    sxr2 = sxr - SW - 18                      # chỗ thứ hai, vẫn nằm bên phải punch
    hero, sup1, sup2 = [], [], []

    # scene 1 — điện thoại rung (ảnh: bàn + điện thoại + cốc trà + báo)
    hero.append(stick("h-1", "assets/card_denwa.png", 8, 309, x=hx, y=150, w=HW,
                      ent="grow", amp=5))
    sup1.append(stick("s1-1", "assets/el_calendar.png", 96, 221, x=sxr, y=SUP_Y, w=SW,
                      rot=-7, ent="pop", amp=4, ph=1.2, sh="sm"))

    # scene 2 — giọng máy (dùng lại mảnh bàn-điện thoại nhạt)
    hero.append(stick("h-2", "assets/card_kikai.png", 330, 432, x=hx, y=150, w=HW,
                      ent="rise", amp=5))
    sup1.append(stick("s1-2", "assets/el_burst_red.png", 392, 370, x=sxr, y=SUP_Y, w=SW,
                      rot=-9, ent="punch", amp=4, ph=0.8, sh="sm"))
    sup2.append(stick("s2-2", "assets/el_smartphone.png", 440, 322, x=sxr2, y=SUP_Y + 6, w=SW,
                      rot=7, ent="pop", amp=4, ph=3.4, sh="sm"))

    # scene 3 — 支給停止 (đỉnh: mảnh ảnh bàn tay dừng trên điện thoại, nền đỏ)
    hero.append(stick("h-3", "assets/card_te.png", 770, 279, x=hx, y=150, w=HW,
                      ent="zoom-through", amp=6))
    sup1.append(stick("s1-3", "assets/el_mynumber_card.png", 826, 223, x=sxr, y=SUP_Y, w=SW,
                      rot=-6, ent="pop", amp=4, ph=2.0, sh="sm"))

    # scene 4 — あなたの話 (mảnh ảnh gọi lại số thật)
    # 🔴 `DUR - 1055` là BẪY: khi DUR nới từ 46s→108s (thêm 3 scene số liệu), photocard này
    # tự kéo dài tới HẾT VIDEO và bảng `papercut-stat` đè lên nó (đã thấy ở still 1700 —
    # nhãn 「特殊詐欺 ぜんたい」 bị ảnh che). Sup `s1-4` tao đã chốt cứng 262 nhưng quên hero.
    # ⇒ Trong builder, **đừng dùng `DUR - x` cho clip không thật sự chạy tới cuối**; chốt
    # bằng mốc scene (1382 = đầu scene số liệu).
    hero.append(stick("h-4", "assets/card_madoguchi.png", 1055, 1382 - 1055, x=hx, y=150,
                      w=HW, ent="flip", amp=5))
    sup1.append(stick("s1-4", "assets/el_nenkin_techo.png", 1120, 262, x=sxr,
                      y=SUP_Y, w=SW, rot=5, ent="pop", amp=4, ph=1.6, sh="sm"))

    # ══ scene 5–7: SỐ LIỆU + CÔNG THỨC ══════════════════════════════════════
    # 🔴 Ở 3 scene này KHÔNG có photocard hero — vùng giữa để cho BẢNG/CÔNG THỨC
    # (`papercut-stat` / `papercut-formula`). Số do FONT vẽ nên luôn sắc; ⛔ tuyệt đối
    # không nhờ ảnh AI vẽ số (số/kanji AI gen là nát nét, `media-library.md` §2.9).
    sup1.append(stick("s1-5", "assets/el_police_badge.png", 1420, 600, x=sxr, y=SUP_Y, w=SW,
                      rot=-6, ent="pop", amp=4, ph=1.0, sh="sm"))
    sup1.append(stick("s1-6", "assets/el_coin_stack.png", 2060, 580, x=sxr, y=SUP_Y, w=SW,
                      rot=7, ent="punch", amp=4, ph=2.4, sh="sm"))
    sup1.append(stick("s1-7", "assets/el_chart_up.png", 2690, DUR - 2690, x=sxr,
                      y=SUP_Y, w=SW, rot=-5, ent="pop", amp=4, ph=3.8, sh="sm"))

    # ── TAG (khối màu góc trên) + PUNCH (dải đen chữ vàng) ──────────────────
    # 🔴 `TextClip.tsx` mặc định `left: 90` cho CẢ tag và punch → dải punch nằm ở x 90–…,
    # tức ĐÈ LÊN CAST TRÁI (cast chiếm x 4–~500). Đã thấy ở still đầu: punch đè chân cast.
    # ⇒ punch phải đẩy vào dải sân khấu; tag thì để x=90 được vì cast trái cao 620px, đỉnh
    # ở y=432, còn tag nằm y≈60–190 nên không giao nhau.
    # ⭐ CHỮ CẮT GIẤY (user chốt 2026-08-26 lần 5: *"text trình bày tao cũng muốn có dạng
    # chữ cắt giấy cơ"*) → preset **`papercut`** / **`papercut-punch`** MỚI thêm vào
    # `remotion-vox/src/components/TextClip.tsx`: mỗi KÝ TỰ là một mảnh giấy kem riêng,
    # có vành mực, bóng giấy và độ nghiêng riêng.
    # 🔴 Nghiêng/lệch là TIỀN ĐỊNH theo chỉ số ký tự (hash), KHÔNG random — Remotion render
    # từng frame độc lập, random thì mỗi frame ra một góc khác ⇒ chữ rung lập bập.
    # ⓘ Thêm preset MỚI, không sửa `tag`/`punch`/`plain` ⇒ 15 project khác không đổi gì.
    # ⭐ user chot 2026-08-26 (lan 7), theo anh mau: MOT DAI giay xe LIEN + chu navy dam,
    # khong phai tung ky tu mot o roi (o roi doc ra "ransom note").
    tag = [txt(f"tag-{i+1}", s["tag"], s["f"] + 4, s["to"] - s["f"] - 4,
               "papercut-banner", color=INK, layout={"x": 74, "y": 58})
           for i, s in enumerate(SCENES)]
    PX = STAGE_X0 + 20
    punch = [
        txt("p-1", "机の上で、震えた", 120, 190, "papercut-banner", color=INK, layout={"x": PX}),
        txt("p-2", "「支給が停止されます」", 480, 270, "papercut-banner", color=RED,
            layout={"x": PX}),
        txt("p-3", "支給停止。", 766, 190, "papercut-banner", color=RED,
            layout={"x": PX}),
        txt("p-4", "これは、あなたの話", 1060, 260, "papercut-banner", color=INK, layout={"x": PX}),
    ]

    # ══ BẢNG SỐ LIỆU + CÔNG THỨC (user chốt 2026-08-26 lần 6) ═══════════════
    # `papercut-stat`   : mỗi dòng `nhãn|số`, dòng CUỐI được nhấn (nền vàng).
    # `papercut-formula`: tách theo khoảng trắng; toán tử (÷ × − ＋ = ≒) để TRẦN,
    #                     hạng sau `=` là ĐÁP SỐ nên tự nhấn + to hơn 1,16×.
    # 🔴 CÔNG THỨC PHẢI TỰ TÍNH RA ĐƯỢC TỪ SỐ CÓ TRONG FACT SHEET, không bịa:
    #    1.816億円 ÷ 182 ngày (1/1→30/6) ≒ 10億円/ngày — chính là câu 「1日あたり、
    #    およそ10億円」 trong lời đọc. Đây là phép chia lại từ 2 số đã verify, không
    #    phải số mới ⇒ không phạm luật YMYL "cấm bịa số".
    SX = STAGE_X0 + 16
    stat = [
        txt("st-1",
            "特殊詐欺 ぜんたい|3,257億円" + NL + "*うち 還付金をかたる詐欺|2,087件",
            1580, 440, "papercut-stat",
            layout={"x": SX, "y": 300, "w": 810}),
        txt("st-2",
            "令和7年 1年間|3,257億円" + NL + "*令和8年 上半期だけで|1,816億円",
            2140, 300, "papercut-stat",
            layout={"x": SX, "y": 250, "w": 810}),
        txt("st-3",
            "*特殊詐欺 ぜんたいの数字|◯" + NL + "年金機構をかたる分だけ|✕",
            2700, 420, "papercut-stat",
            layout={"x": SX, "y": 300, "w": 810}),
    ]
    formula = [
        # 5割以上 tăng → so 2 kỳ
        txt("fm-1", "1,816億円 ÷ 182日 ≒ 10億円", 2460, 180, "papercut-formula",
            layout={"x": SX, "y": 360, "w": 830}),
    ]

    tracks = [
        {"id": "trk-bg", "name": "nền giấy", "type": "background", "muted": False,
         "hidden": False, "locked": False, "clips": trk_bg},
        {"id": "trk-hero", "name": "hero ảnh", "type": "sticker", "muted": False,
         "hidden": False, "locked": False, "clips": hero},
        {"id": "trk-sup1", "name": "phụ 1", "type": "sticker", "muted": False,
         "hidden": False, "locked": False, "clips": sup1},
        {"id": "trk-sup2", "name": "phụ 2", "type": "sticker", "muted": False,
         "hidden": False, "locked": False, "clips": sup2},
        # cast vẽ SAU sticker nội dung ⇒ luôn nằm trên, không bị ảnh đè
        {"id": "trk-cast-l", "name": "cast trái", "type": "sticker", "muted": False,
         "hidden": False, "locked": False, "clips": cast_l},
        {"id": "trk-cast-r", "name": "cast phải", "type": "sticker", "muted": False,
         "hidden": False, "locked": False, "clips": cast_r},
        {"id": "trk-tag", "name": "tag", "type": "text", "muted": False,
         "hidden": False, "locked": False, "clips": tag},
        {"id": "trk-punch", "name": "punch", "type": "text", "muted": False,
         "hidden": False, "locked": False, "clips": punch},
        {"id": "trk-stat", "name": "bảng số liệu", "type": "text", "muted": False,
         "hidden": False, "locked": False, "clips": stat},
        {"id": "trk-formula", "name": "công thức", "type": "text", "muted": False,
         "hidden": False, "locked": False, "clips": formula},
        {"id": "trk-voice", "name": "giọng", "type": "audio", "muted": False,
         "hidden": False, "locked": False,
         "clips": [{"id": "v-1", "kind": "audio", "from": 0, "durationInFrames": DUR,
                    "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]},
    ]

    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": "nenkin",
                 "fps": FPS, "width": 1920, "height": 1080,
                 "createdAt": "2026-08-26T00:00:00.000Z",
                 "modifiedAt": "2026-08-26T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        # ⚠️ Ba chỗ schema KHÁC dự đoán ban đầu (bắt được bằng `remotion still`, 2026-08-26):
        #  ① sceneMarkers dùng khoá **`atFrame`**, không phải `frame`.
        #  ② captions.lines dùng **`{text, startMs, endMs}`** (mili-giây), KHÔNG phải
        #     `{from, durationInFrames}` như clip — phụ đề đo bằng ms, clip đo bằng frame.
        #  ③ captions.source là **enum** `none|voicevox-mora|whisper|srt-interpolated`;
        #     "srt" không hợp lệ. Nguồn của mình là subs.srt → `srt-interpolated`.
        # 📌 Đọc `src/schema/project.ts` trước khi sinh JSON, đừng suy từ project mẫu.
        "sceneMarkers": [{"id": f"sc-{i+1}", "atFrame": s["f"], "label": s["tag"]}
                         for i, s in enumerate(SCENES)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44,
                     "lines": [{"text": t,
                                "startMs": round(a / FPS * 1000),
                                "endMs": round(b / FPS * 1000)}
                               for a, b, t in LINES],
                     "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236", "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }

    out = RV / "projects" / NAME
    out.mkdir(parents=True, exist_ok=True)
    (out / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    # ── kiểm: mọi sticker nội dung nằm trong dải sân khấu ───────────────────
    bad = []
    for tr in tracks:
        if tr["id"] in ("trk-cast-l", "trk-cast-r") or tr["type"] != "sticker":
            continue
        for c in tr["clips"]:
            x, w = c["layout"]["x"], c["layout"]["w"]
            if x < STAGE_X0 or x + w > STAGE_X1:
                bad.append(f"  {c['id']}: x {x}–{x+w} ngoài dải {STAGE_X0}–{STAGE_X1}")
    ns = sum(len(t["clips"]) for t in tracks if t["type"] == "sticker")
    nt = sum(len(t["clips"]) for t in tracks if t["type"] == "text")
    print(f"✓ {out / 'project.json'}")
    print(f"   {DUR} frame ({DUR/FPS:.0f}s) · {len(SCENES)} scene · {ns} sticker · {nt} text "
          f"· {len(LINES)} dòng phụ đề")
    if bad:
        print("🔴 sticker LỌT ra vùng cast (sẽ bị cast đè):")
        print("\n".join(bad))
        return 1
    print(f"   ✓ mọi sticker nội dung nằm trong dải sân khấu {STAGE_X0}–{STAGE_X1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
