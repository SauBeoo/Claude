# -*- coding: utf-8 -*-
r"""build_remotion_17.py — `project.json` cho TRỌN video 17 (12 chương, 14:10).

Khuôn đã user chốt qua 7 vòng demo (`build_remotion_17demo.py` là bản demo 108s):
khung 2 cast 2 mép · vùng giữa toàn ẢNH (photocard hero + sticker sup) · chữ **cắt giấy
dạng BANNER dải liền** · bảng số liệu + công thức vẽ bằng font.

🔴 NEO SCENE BẰNG **CHỈ SỐ DÒNG** của `timeline.json`, KHÔNG hardcode giây.
Bản demo hardcode frame (`dict(f=0, to=317, …)`) và mỗi lần sửa lời là phải tính lại tay —
đúng loại việc sẽ trôi. Ở đây scene khai bằng `L=<chỉ số dòng bắt đầu>`, builder tự tra giây
từ timeline ⇒ sửa lời, re-synth, chạy lại builder là khớp lại, không tính tay gì.

CHẠY:  python tools/build_remotion_17.py
"""
import json
import math
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
RV = Path(r"E:\Claude\Projects\remotion-vox")
STEM = "17_nenkin-sagi-jidoonsei-shikyuteishi"
NAME = "nenkin-17"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#E0A32A"

# ⭐ HÌNH GIỮA TO LÊN CHO MÀN ĐIỆN THOẠI (user chốt 2026-08-26 lần 8).
# Đo thật: hero 790px trên khung 1920 ⇒ trên màn 390px (bề rộng điện thoại) chỉ còn
# **162px** — thấy được nhưng chi tiết mất. Thủ phạm: cast chiếm 2×533 = **55,5% bề ngang**.
# 🔴 NÚT THẮT LÀ CHIỀU CAO, KHÔNG PHẢI BỀ NGANG. Photocard ratio ~1,49; trần dọc là từ
# y=140 (dưới tag) đến y≈900 (trên phụ đề) = 760px ⇒ hero rộng tối đa **1.132px (59% khung)**.
# Nới dải ngang thêm nữa cũng vô ích vì chiều cao đã hết chỗ.
# ⇒ Làm HAI việc: ① hạ CAST_H 620→500 (cast rộng 533→430; vẫn cao 46% khung, còn rõ người)
#                ② cho hero **CHỒNG LÊN cast** — cast vẽ SAU nên nằm trên, phần bị che là
#                   VIỀN GIẤY + tape ở rìa ảnh, không phải nội dung. Đây đúng chất collage:
#                   mảnh ảnh dán sau lưng người.
CAST_H, CAST_FEET_Y, CAST_MARGIN = 500, 1052, 4
CAST_RATIO = {
    "sensei_serious": 801 / 1280, "sensei_caution": 990 / 1280,
    "sensei_point": 1044 / 1280, "sensei_reassure": 965 / 1280,
    "sensei_conclude": 806 / 1280, "sensei_present": 1101 / 1280,
    "kikite_worried": 871 / 1280, "kikite_surprised": 1028 / 1280,
    "kikite_listen": 967 / 1280, "kikite_nod": 908 / 1280,
    "kikite_think": 923 / 1280, "kikite_relieved": 863 / 1280,
}
# dải sân khấu SUY TỪ cast rộng nhất (luật đã ghi ở CLAUDE.md §②)
_CW = round(CAST_H * max(CAST_RATIO.values()))
STAGE_X0 = CAST_MARGIN + _CW + 24
STAGE_X1 = 1920 - CAST_MARGIN - _CW - 24
CX = (STAGE_X0 + STAGE_X1) // 2
# 🔴 HW phải SUY TỪ DẢI, đừng hằng-số-hoá — chính cái gate này vừa bắt tao: thêm
# `sensei_present` (ratio 0,860) vào CAST_RATIO ⇒ `_CW` 506→533 ⇒ dải 852→**798px**, mà
# HW đang hardcode 830 ⇒ 34/39 photocard lọt ra ngoài dải và bị cast đè.
# Chọn giữ bộ cast phong phú (present/think/relieved dùng thật ở 12 chương) và cho hero
# co theo dải, thay vì bỏ cast để giữ hero to — mất 40px hero không ai thấy, mất biểu cảm
# thì cả video một vẻ mặt.
HERO_Y = 140
HERO_BOTTOM = 900          # trên vùng phụ đề
HW = round((HERO_BOTTOM - HERO_Y) * 1.49)      # 1.132px — trần theo CHIỀU CAO
HX = (1920 - HW) // 2
# 🔴 dấu phải là (mép trong cast − mép ngoài hero): bản đầu tao viết ngược nên in ra
# −40 và gate  sẽ KHÔNG BAO GIỜ chặn được.
HERO_BLEED = (CAST_MARGIN + _CW) - HX          # hero lấn vào cast bao nhiêu px mỗi bên
# Cửa sổ thời gian dành cho sup, theo TỈ LỆ thời lượng scene. Mốc vào của từng cái được
# CHIA ĐỀU trong cửa sổ này theo SỐ LƯỢNG sup của chính scene đó (xem vòng dựng sup) —
# nên scene 2 sticker và scene 5 sticker đều rải kín, không ai đứng im nửa scene.
SUP_ENTER0, SUP_ENTER1 = 0.12, 0.88
SUP_ROT = (-7, 7, -5)     # chỉ còn dùng cho sticker của scene có BẢNG
# ⛔ ĐÃ XOÁ: `SW` / `SUP_X` / `SUP_Y` / `SUP_DY` / `_EXT` — bộ toạ độ của thời sticker
# ĐÈ LÊN hero (3 chỗ trong dải sân khấu). Sau khi sticker ra ngoài ảnh, chúng thành hằng
# số chết. 🔴 Xoá chứ không để lại: hằng số chết là bẫy — người sau sẽ tinh chỉnh `SW` rồi
# render, thấy không gì đổi, và đi tìm lỗi ở chỗ khác.
# 📌 Cái đáng giữ là BÀI HỌC của hai lượt đó, không phải con số:
#   ① Trần 321px hồi "3 cái cùng sống" không phải giới hạn của KHUNG mà của **cách làm**
#      (3·SW < dải − 2·lề). Bỏ yêu cầu 3-cùng-sống thì trần thành ~900px.
#   ② Lần này y hệt, chỉ khác trục: bí theo chiều NGANG thì đừng kết luận "hết chỗ" —
#      chỗ trống của khung này nằm ở chiều DỌC, trên đầu cast.
#   ⇒ Hết đường ở một con số thì hỏi *"con số này do KHUNG hay do CÁCH LÀM?"*

# ⭐⭐ SCENE CÓ ẢNH: STICKER RA **NGOÀI** MẢNH ẢNH (user chốt 2026-08-26:
# *"sticker không đè vào ảnh mà nó ở bên ngoài ảnh. Nếu sticker mà không đè lên nhau thì
# có thể giữ nguyên không mất đi"*).
# 🔴 Chỗ trống nằm ở đâu — đo, không đoán: hero chiếm x 394…1526 · y 140…900, còn CAST chỉ
# CAO 500px và đứng ở CHÂN khung ⇒ cast chiếm y **552…1052**. Nên **hai góc TRÊN của khung
# thật sự trống**: phải x 1526…1920 · trái x 4…394, cả hai từ y 0 tới 552.
#   → Đây là lý do không phải thu nhỏ hero: chỗ trống đến từ **chiều DỌC** (trên đầu cast),
#     không phải từ chiều ngang. Nếu chỉ tìm theo chiều ngang thì kết luận sai là
#     "không còn chỗ, buộc phải bóp hero" (đo thử: hero phải tụt 1132→744px).
# Trần bề ngang: làn phải = 1920−1526 = 394px ⇒ w·1,114 ≤ 394−12 ⇒ **w ≤ 343**. Lấy 330.
# Lề trên bên TRÁI phải chừa dải tiêu đề (`trk-tag` ở x74 y58, tag dài nhất ~500px rộng)
#   ⇒ slot trái bắt đầu từ y 185.
OUT_W = 330
OUT_XY = ((1555, 110), (25, 185))     # (phải-trên, trái-trên)
OUT_ROT = (-6, 6)
# CHỈ 2 slot ⇒ scene khai >2 sticker thì TIẾP SỨC **TRONG CÙNG SLOT** (j và j+2). Hai slot
# rời nhau hoàn toàn nên hai cái đang sống không bao giờ đè nhau — đúng điều kiện user cho
# phép "giữ nguyên không mất đi", mà vẫn còn chuyển động ở scene dài.
# Bộ toạ độ RIÊNG cho scene có bảng/công thức (xem khối giải thích ở vòng dựng sup).
# ⚠️ `w` của bảng (810/830) là BỀ RỘNG HỘP CHỨA, không phải bề rộng MỰC. Đo trên still
#    `out/n17demo5/k_tbl_note.png`: ô giá trị phải nhất dừng ở **x≈1130**. Gate phải dùng
#    mốc MỰC đo được, dùng mốc hộp (1304) thì báo oan và không còn chỗ nào đặt sticker.
TBL_INK_X1 = 1140                 # mép phải của MỰC bảng, đo bằng mắt trên still 1:1
# Relay cũng nới được làn bảng: làn trống là 1140→1462 = 322px ⇒ SW·1,114 ≤ 322 ⇒ ≤289.
SW_TBL = 280
_EXT_TBL = round((SW_TBL * math.cos(math.radians(7))
                  + SW_TBL * math.sin(math.radians(7)) - SW_TBL) / 2) + 4
SW_TBL_X = STAGE_X1 - SW_TBL - _EXT_TBL
SW_TBL_Y = (250, 480, 610)        # 3 chỗ cho mắt thấy đổi; relay nên không cần loại trừ
PX = STAGE_X0 + 20

# ⛔ `el_police_badge` BỊ LOẠI KHỎI CẢ 9 SCENE (2026-08-26, cùng lượt phóng SW 150→280).
#    Asset đó thực chất là **một cái vành TRỐNG RUỘT** — generator không vẽ được huy hiệu vì
#    prompt cấm chữ. Ở 150px nó qua được như một con dấu trừu tượng; ở 280px nó đọc ra là
#    **cái đĩa trắng**, vô nghĩa và ăn 1/4 khung. Đây là bài học riêng, đáng ghi:
#    **PHÓNG TO LÀ MỘT PHÉP KIỂM CHẤT LƯỢNG ASSET** — sticker yếu chỉ sống được nhờ nhỏ.
#    Thay bằng asset CÓ NGHĨA theo từng scene (hand_stop cho câu phủ định · smartphone cho
#    số điện thoại · calendar cho năm · newspaper cho công bố · passbook cho tiền).
# ══════════════════════════════════════════════════════════════════════════════
# 25 SCENE — `L` = chỉ số dòng timeline nơi scene BẮT ĐẦU.
#   hero  : photocard (None = để trống vùng giữa cho bảng/công thức)
#   sup   : list sticker (tên file, không tiền tố assets/)
#   tag   : chữ trên banner góc trên-trái
#   l / r : cast trái / phải
# ══════════════════════════════════════════════════════════════════════════════
SCENES = [
    # ── 第1章 cold open ──────────────────────────────────────────────────────
    dict(L=0,  tag="電話",        hero="card_denwa",        sup=["el_smartphone"],
         l="sensei_serious",  r="kikite_listen",    sp=["#C8B88A", "#9FB6C8"]),
    dict(L=3,  tag="機械の声",     hero="card_kikai",        sup=["el_speaker_robot", "el_burst_red"],
         l="sensei_caution",  r="kikite_worried",   sp=["#C87A72", "#C8B88A"]),
    dict(L=5,  tag="支給停止",     hero="card_c2_te_tomaru",  sup=["el_mynumber_card"],
         l="sensei_caution",  r="kikite_surprised", sp=["#B44A4A", "#8A93A8"]),
    dict(L=7,  tag="あなたの話",    hero="card_madoguchi",    sup=["el_calendar", "el_senior_phone", "el_smartphone"],
         l="sensei_point",    r="kikite_worried",   sp=["#8FA9C0", "#C8B88A"]),
    dict(L=10, tag="この研究室",    hero="card_tsukue",       sup=["el_nenkin_techo", "el_newspaper", "el_passbook"],
         l="sensei_present",  r="kikite_nod",       sp=["#9FB6C8", "#C8B88A"]),
    # ── 第2章 オペレーター ───────────────────────────────────────────────────
    # sup KHÔNG dùng el_senior_phone: hero mới đã có ông cụ áp điện thoại ⇒ sticker cùng
    # chủ thể là lặp NGHĨA (cùng lỗi đã sửa ở scene 手が止まった).
    dict(L=11, tag="人の声",       hero="card_c2_hito_no_koe", sup=["el_nenkin_techo", "el_teacup"],
         l="sensei_explain" if False else "sensei_serious", r="kikite_think",
         sp=["#C87A72", "#9FB6C8"]),
    dict(L=14, tag="ふつうの質問",  hero="card_yonhon",       sup=["el_calendar", "el_newspaper"],
         l="sensei_explain" if False else "sensei_point", r="kikite_think",
         sp=["#C8B88A", "#9FB6C8"]),
    dict(L=16, tag="渡さないもの",  hero="card_c4_mynumber",  sup=["el_passbook", "el_mynumber_card", "el_smartphone"],
         l="sensei_caution",  r="kikite_worried",   sp=["#B44A4A", "#C8B88A"]),
    dict(L=20, tag="手が止まった",  hero="card_te",           sup=["el_hand_stop"],
         l="sensei_caution",  r="kikite_surprised", sp=["#B44A4A", "#8A93A8"]),
    # ── 第3章 止まった、ひと言 ───────────────────────────────────────────────
    dict(L=22, tag="切った",       hero="card_c3_kiru",      sup=["el_speaker_robot"],
         l="sensei_serious",  r="kikite_think",     sp=["#8A93A8", "#C8B88A"]),
    dict(L=25, tag="本物の番号",    hero="card_c3_techo",     sup=["el_nenkin_techo"],
         l="sensei_point",    r="kikite_nod",       sp=["#C8B88A", "#9FB6C8"]),
    dict(L=27, tag="ございません",  hero="card_kakenaosu",    sup=["el_hand_stop"],
         l="sensei_reassure", r="kikite_relieved",  sp=["#8FA9C0", "#C8B88A"]),
    # ── 第4章 5つの「絶対にしないこと」 ─────────────────────────────────────
    dict(L=30, tag="原典",        hero="card_c4_genten",    sup=["el_newspaper"],
         l="sensei_present",  r="kikite_listen",    sp=["#9FB6C8", "#C8B88A"]),
    dict(L=32, tag="5つ",         hero=None,                sup=["el_speaker_robot", "el_passbook", "el_smartphone"],
         l="sensei_explain" if False else "sensei_point", r="kikite_think",
         sp=["#8A93A8", "#C8B88A"], stat="gotsu"),
    dict(L=38, tag="3つ当てはまる", hero=None,               sup=["el_burst_red"],
         l="sensei_caution",  r="kikite_surprised", sp=["#B44A4A", "#8A93A8"], stat="atehamaru"),
    dict(L=40, tag="警察庁も",      hero="card_c4_keisatsu",  sup=["el_newspaper", "el_mynumber_card", "el_burst_red"],
         l="sensei_serious",  r="kikite_worried",   sp=["#C87A72", "#C8B88A"]),
    # ── 第5章 なぜ「もっともらしく」 ───────────────────────────────────────
    dict(L=43, tag="巧妙な理由",    hero="card_c5_futatsu_koe", sup=["el_speaker_robot", "el_senior_phone", "el_nenkin_techo"],
         l="sensei_explain" if False else "sensei_point", r="kikite_think",
         sp=["#C87A72", "#9FB6C8"]),
    dict(L=45, tag="時期を狙う",    hero="card_c5_jiki",      sup=["el_calendar", "el_newspaper", "el_speaker_robot"],
         l="sensei_caution",  r="kikite_worried",   sp=["#C8B88A", "#9FB6C8"]),
    dict(L=47, tag="9110 と 188",  hero=None,                sup=["el_smartphone"],
         l="sensei_present",  r="kikite_nod",       sp=["#8FA9C0", "#C8B88A"], stat="denwa"),
    # ── 第6章 CTA ───────────────────────────────────────────────────────────
    dict(L=48, tag="お願い",       hero="card_kazoku",       sup=["el_smartphone", "el_teacup", "el_newspaper"],
         l="sensei_reassure", r="kikite_nod",       sp=["#C8B88A", "#9FB6C8"]),
    # ── 第7章 本物の通知書 ─────────────────────────────────────────────────
    dict(L=49, tag="本物の姿",      hero="card_c7_honmono",   sup=["el_newspaper", "el_nenkin_techo", "el_passbook", "el_hand_stop"],
         l="sensei_point",    r="kikite_listen",    sp=["#C8B88A", "#8FA9C0"]),
    dict(L=54, tag="急がない",      hero="card_c7_isoganai",  sup=["el_calendar", "el_newspaper", "el_teacup"],
         l="sensei_reassure", r="kikite_relieved",  sp=["#8FA9C0", "#C8B88A"]),
    # ── 第8章 số liệu ──────────────────────────────────────────────────────
    dict(L=55, tag="令和7年",      hero=None,                sup=["el_calendar", "el_coin_stack"],
         l="sensei_present",  r="kikite_listen",    sp=["#8A93A8", "#C8B88A"], stat="r7"),
    dict(L=57, tag="令和8年",      hero=None,                sup=["el_chart_up", "el_coin_stack", "el_calendar"],
         l="sensei_serious",  r="kikite_worried",   sp=["#B44A4A", "#C8B88A"],
         stat="r8", formula="1,816億円 ÷ 182日 ≒ 10億円"),
    dict(L=58, tag="読み方",       hero=None,                sup=["el_coin_stack", "el_chart_up", "el_newspaper"],
         l="sensei_explain" if False else "sensei_point", r="kikite_nod",
         sp=["#8FA9C0", "#9FB6C8"], stat="yomikata"),
    # ── 第9章 すること3つ ──────────────────────────────────────────────────
    dict(L=59, tag="すること3つ",   hero=None,                sup=["el_nenkin_techo"],
         l="sensei_point",    r="kikite_think",     sp=["#C8B88A", "#9FB6C8"], stat="mitsu"),
    dict(L=60, tag="渡さない",      hero="card_c9_watasanai", sup=["el_mynumber_card"],
         l="sensei_caution",  r="kikite_worried",   sp=["#B44A4A", "#8A93A8"]),
    dict(L=61, tag="かけ直す",      hero="card_c9_kakenaosu", sup=["el_nenkin_techo"],
         l="sensei_point",    r="kikite_nod",       sp=["#8A93A8", "#C8B88A"]),
    dict(L=62, tag="相談する",      hero="card_c9_soudan",    sup=["el_smartphone"],
         l="sensei_reassure", r="kikite_relieved",  sp=["#8FA9C0", "#C8B88A"]),
    dict(L=63, tag="メールもSMSも", hero="card_c9_mail_sms",  sup=["el_smartphone", "el_mynumber_card", "el_burst_red"],
         l="sensei_caution",  r="kikite_worried",   sp=["#C87A72", "#C8B88A"]),
    dict(L=64, tag="たったひと言",  hero="card_c9_hitokoto",  sup=["el_mynumber_card"],
         l="sensei_serious",  r="kikite_relieved",  sp=["#8FA9C0", "#C8B88A"]),
    # ── 第10章 ○×クイズ ───────────────────────────────────────────────────
    dict(L=66, tag="○×クイズ",     hero="card_c10_quiz",     sup=["el_speaker_robot", "el_calendar", "el_hand_stop"],
         l="sensei_present",  r="kikite_think",     sp=["#8A93A8", "#C8B88A"]),
    dict(L=69, tag="クイズ 2",      hero="card_c10_quiz",     sup=["el_calendar", "el_senior_phone", "el_smartphone"],
         l="sensei_point",    r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    dict(L=71, tag="クイズ 3",      hero="card_c10_quiz",     sup=["el_mynumber_card", "el_passbook", "el_hand_stop"],
         l="sensei_reassure", r="kikite_nod",       sp=["#8FA9C0", "#C8B88A"]),
    # ── 第11章 釣り + 奥さま ───────────────────────────────────────────────
    dict(L=73, tag="その日の午後",  hero="card_tsuri",        sup=["el_two_anglers", "el_smartphone", "el_teacup"],
         l="sensei_reassure", r="kikite_relieved",  sp=["#C8B88A", "#8FA9C0"]),
    dict(L=78, tag="その夜",       hero="card_c11_okusama",  sup=["el_teacup", "el_smartphone", "el_newspaper"],
         l="sensei_reassure", r="kikite_relieved",  sp=["#C8B88A", "#9FB6C8"]),
    # ── 第12章 研究ノート + đóng bài ───────────────────────────────────────
    # 5 sticker cho scene 46,7s (dài nhất video) — chọn theo 5 dòng ノート ①機構 ②もっともらしさ
    # ③迷ったら ④相談先 ⑤本物の通知, nhưng ⚠️ mốc vào là CHIA ĐỀU thời lượng, **không** khớp
    # cue từng dòng nói. Muốn khớp thì phải cho `sup` nhận thêm chỉ số dòng timeline.
    dict(L=84, tag="研究ノート",    hero=None,                sup=["el_nenkin_techo", "el_speaker_robot", "el_hand_stop", "el_smartphone", "el_newspaper"],
         l="sensei_conclude", r="kikite_nod",       sp=["#8A93A8", "#C8B88A"], stat="note"),
    dict(L=90, tag="今日のお願い",  hero="card_c12_okuru",    sup=["el_smartphone"],
         l="sensei_reassure", r="kikite_nod",       sp=["#C8B88A", "#8FA9C0"]),
    dict(L=92, tag="次回予告",      hero="card_c12_jikai",    sup=["el_coin_stack", "el_chart_up", "el_calendar"],
         l="sensei_present",  r="kikite_listen",    sp=["#9FB6C8", "#C8B88A"]),
]

# banner PUNCH — chữ đâm, neo theo chỉ số dòng
PUNCH = [
    (0,  "机の上で、震えた",          INK),
    (4,  "「支給が停止されます」",      RED),
    (5,  "支給停止。",                RED),
    (8,  "1を、押した",              RED),
    (19, "マイナンバーカードの写真",    RED),
    (20, "——ここで、手が止まった",     RED),
    (26, "「ございません」",           INK),
    (38, "5つのうち、3つ",            RED),
    (43, "機械の声 → 人の声",         INK),
    (53, "本物は、紙で来る",           INK),
    (54, "本物は、急がない",           INK),
    (60, "渡さない",                 RED),
    (61, "切って、かけ直す",           INK),
    (65, "たったひと言で、助かった",    INK),
    (83, "止めた、その一瞬",           INK),
    (91, "「切っていいからね」",        INK),
]

# bảng số liệu — key khớp `stat=` ở SCENES
STAT = {
    "gotsu": ("電話で口座番号を聞く|✕" + NL + "自動音声で支給停止|✕" + NL
              + "ATM操作を指示|✕" + NL + "LINEで手続き案内|✕" + NL + "手数料を求める|✕", 44),
    "atehamaru": ("自動音声で始まった|✕" + NL + "支給停止を告げた|✕" + NL
                  + "*口座番号を尋ねた|✕", 50),
    "denwa": ("警察相談専用電話|#9110" + NL + "*消費者ホットライン|188", 54),
    "r7": ("特殊詐欺 ぜんたい|3,257億円" + NL + "*うち 還付金をかたる詐欺|2,087件", 48),
    "r8": ("半年で|1,816億円" + NL + "*前の年より|＋5割以上", 48),
    "yomikata": ("*特殊詐欺 ぜんたいの数字|◯" + NL + "年金機構をかたる分だけ|✕", 46),
    "mitsu": ("① 渡さない|口座番号・写真" + NL + "② 切ってかけ直す|本物の番号"
              + NL + "*③ 相談する|9110 / 188", 44),
    "note": ("① 機構がしないこと|5つ" + NL + "② もっともらしさ|証拠ではない"
             + NL + "③ 迷ったら|切ってかけ直す" + NL + "④ 相談先|9110 / 188"
             + NL + "*⑤ 本物の通知|紙で届く・急かさない", 40),
}


# ⭐ TRẦN KÝ TỰ MỖI KHỐI PHỤ ĐỀ. `audience-45plus.md` §3 mục 1: **≤2 dòng/khối**.
# Caption của Remotion ở fontSize 44 trên khung 1920 chứa ~**40 ký full-width/dòng**
# ⇒ trần 1 khối = 80 ký. Đo trên timeline thật: **14/96 dòng vượt**, dòng dài nhất 151 ký
# → ra **4 dòng** phụ đề (thấy tận mắt ở still frame 8500: 3 dòng che gần hết đáy khung).
# 🔴 Pipeline ffmpeg cũ có `SUB_MAXLEN=42` tự chẻ, còn `CaptionLayer` của Remotion lấy
# NGUYÊN dòng timeline làm một khối ⇒ đổi engine dựng hình là **mất luôn cái chẻ đó**.
# Đây là loại lỗi chỉ lộ khi soi frame, không gate nào của builder bắt được.
CAP_MAX = 78
CAP_CUT = "。、」）"          # cắt SAU dấu câu — cắt giữa cụm là đọc bị ngắt hơi sai


def split_caption(line):
    """Chẻ 1 dòng timeline thành nhiều khối ≤CAP_MAX ký, chia giây theo TỈ LỆ ký tự."""
    t = line["text"]
    if len(t) <= CAP_MAX:
        return [line]
    # điểm cắt ưu tiên: sau dấu câu, gần giữa đoạn còn lại nhất
    parts, buf = [], ""
    for ch in t:
        buf += ch
        if ch in CAP_CUT and len(buf) >= CAP_MAX * 0.55:
            parts.append(buf)
            buf = ""
    if buf:
        if parts and len(parts[-1]) + len(buf) <= CAP_MAX:
            parts[-1] += buf
        else:
            parts.append(buf)
    # còn khối nào vẫn quá dài (câu không có dấu) → cắt cứng
    fixed = []
    for p in parts:
        while len(p) > CAP_MAX:
            fixed.append(p[:CAP_MAX])
            p = p[CAP_MAX:]
        if p:
            fixed.append(p)
    span = line["end"] - line["start"]
    tot = sum(len(p) for p in fixed)
    out, t0 = [], line["start"]
    for p in fixed:
        d = span * len(p) / tot
        out.append({"start": round(t0, 3), "end": round(t0 + d, 3), "text": p})
        t0 += d
    return out


def stick(i, asset, f, dur, x, y, w, rot=0, ent="rise", amp=5, ph=0.0, sh="lg"):
    return {"id": i, "kind": "sticker", "from": f, "durationInFrames": max(1, dur),
            "asset": f"assets/{asset}.png",
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": ent, "delayFrames": 0, "params": {}},
            "exit": None, "idle": {"amp": amp, "phase": ph}, "shadow": sh}


def txt(i, content, f, dur, preset, color=INK, layout=None, size=None):
    return {"id": i, "kind": "text", "from": f, "durationInFrames": max(1, dur),
            "content": content, "preset": preset, "color": color,
            "animation": "pop", "animationParams": {"restDeg": -1.5},
            "layout": layout or {}, "fontSize": size}


def main():
    tl = json.loads((PROJ / "06_VIDEO" / STEM / "timeline.json").read_text(encoding="utf-8"))
    lines = tl["lines"]
    F = lambda idx: round(lines[idx]["start"] * FPS)          # noqa: E731
    DUR = round(tl["total"] * FPS)

    # ── mốc frame từng scene, suy từ timeline ────────────────────────────────
    for k, s in enumerate(SCENES):
        s["f"] = F(s["L"])
        s["to"] = F(SCENES[k + 1]["L"]) if k + 1 < len(SCENES) else DUR

    bad = [f"  scene {k} (dòng {s['L']}) chỉ {(s['to']-s['f'])/FPS:.1f}s"
           for k, s in enumerate(SCENES) if s["to"] - s["f"] < 6 * FPS]
    if bad:
        print("🔴 scene ngắn hơn 6s (audience-45plus §2 mục 2):")
        print(NL.join(bad))
        return 1

    # 🔴 GATE: scene có BẢNG/CÔNG THỨC thì KHÔNG được có photocard hero.
    # Bảng vẽ ở y=240, photocard chiếm y 150–706 ⇒ bảng nằm GIỮA ảnh và bị ảnh che.
    # Đã dính thật ở 3 scene (5つ · 読み方 · 研究ノート) — thấy ở frame 760 của bản render
    # đầu: nhãn 「…ないこと」「…ともらしさ」 bị photocard cắt mất. Vùng giữa chỉ chở ĐƯỢC
    # MỘT thứ: hoặc ảnh, hoặc chữ.
    clash = [f"  scene {k} (dòng {s['L']}) tag={s['tag']} hero={s['hero']} +{s.get('stat') or s.get('formula')}"
             for k, s in enumerate(SCENES)
             if (s.get("stat") or s.get("formula")) and s.get("hero")]
    if clash:
        print("🔴 scene có bảng/công thức MÀ VẪN có hero — bảng sẽ bị ảnh che:")
        print(NL.join(clash))
        return 1

    trk_bg, cl, cr, hero, sup1, sup2, sup3 = [], [], [], [], [], [], []
    tag, punch, stat, formula = [], [], [], []
    cy = CAST_FEET_Y - CAST_H

    for k, s in enumerate(SCENES):
        f, to = s["f"], s["to"]
        d = to - f
        trk_bg.append(dict(id=f"bg-{k}", kind="background", **{"from": f},
                           durationInFrames=d, paper="assets/paper.jpg",
                           tint="#F2EDE4", tintOpacity=0.55, grid=True, dots=True,
                           splash=s["sp"]))
        wl = round(CAST_H * CAST_RATIO[s["l"]])
        wr = round(CAST_H * CAST_RATIO[s["r"]])
        ent = "rise" if k == 0 else "none"
        cl.append(stick(f"cl-{k}", s["l"], f, d, CAST_MARGIN, cy, wl, ent=ent,
                        amp=3, ph=0.4, sh="sm"))
        cr.append(stick(f"cr-{k}", s["r"], f, d, 1920 - wr - CAST_MARGIN, cy, wr,
                        ent=ent, amp=3, ph=2.7, sh="sm"))
        if s.get("hero"):
            hero.append(stick(f"h-{k}", s["hero"], f + 6, d - 6, HX, HERO_Y, HW,
                              ent=["grow", "rise", "flip", "zoom-through"][k % 4], amp=5))
        # ⭐ STICKER VÀO TỪ TỪ, RẢI THEO % THỜI LƯỢNG SCENE (user chốt 2026-08-26 lần 8:
        # *"sticker hiển thị từ từ để có sự liền mạch, không để video đứng im quá lâu"*).
        # 🔴 Bản trước vào ở `f + 24 + j*18` — mốc CỐ ĐỊNH tính từ đầu scene ⇒ mọi sticker
        # dồn hết vào giây 0,8–1,4 rồi **đứng im tới hết scene**, mà scene dài nhất 46,7s.
        # Rải theo TỈ LỆ nên scene càng dài thì khoảng cách càng giãn, luôn có thứ mới hiện.
        # 🔴 sup thứ 3 PHẢI có track + toạ độ riêng: bản trước `sup1 if j==0 else sup2` cho
        # j=1 và j=2 vào CÙNG track, CÙNG x ⇒ hai sticker chồng khít lên nhau.
        # 🔴 SCENE CÓ BẢNG/CÔNG THỨC DÙNG BỘ TOẠ ĐỘ RIÊNG (bắt được khi phóng SW lên 280).
        # Bảng chiếm x 474..1304 · y 240..~700 ⇒ 3 chỗ đặt thường (#1 ở x 862, #2 ở x 478)
        # nằm ĐÈ ngay lên cột nhãn và ô giá trị. Và vì track `trk-stat` vẽ SAU sticker, chữ
        # bảng đè lên sticker ⇒ chữ nằm trên một mảng hình rối = KHÔNG ĐỌC ĐƯỢC.
        # Ở SW=150 nó lọt vì sticker nhỏ, nấp được trong khe. Không phải "trước đúng nay sai"
        # — trước cũng sai, chỉ chưa nhìn ra.
        # Đo thật: ô giá trị của bảng dừng ở x≈1130 ⇒ dải x 1240..1450 là chỗ TRỐNG duy nhất.
        # Chỉ nhận 2 sticker, xếp DỌC. Cỡ 200 < 280 vì hình học không cho hơn — bảng là
        # NỘI DUNG ở những scene này, sticker là trang trí, đừng cho trang trí đánh nhau với nó.
        tbl = bool(s.get("stat") or s.get("formula"))
        sups = s.get("sup") or []          # ⭐ KHÔNG còn trần 3 — relay nối bao nhiêu cũng được
        # ⭐ TIẾP SỨC: sticker j sống từ mốc vào của nó tới ĐÚNG mốc vào của j+1 (cái cuối
        # sống tới hết scene). Không có khe trống giữa hai cái ⇒ đổi liền mạch, không nháy.
        # 🔴 Mốc vào TÍNH TỪ SỐ LƯỢNG, không lấy từ bảng 3 phần tử cố định: bảng cố định
        # (0,14/0,46/0,72) làm scene 2-sticker để cái sau vào ở 46% rồi đứng im 54% thời
        # lượng — scene 研究ノート 46,7s ⇒ **25,1s không đổi gì**, đúng cái user đã phàn nàn.
        n = len(sups)
        st = [f + max(18, int(d * (SUP_ENTER0 + i * (SUP_ENTER1 - SUP_ENTER0) / n)))
              for i in range(n)]
        # 🔴 SỐ CHỖ ĐẶT và BƯỚC TIẾP SỨC là HAI đại lượng khác nhau — gộp là sinh lỗi:
        #   · scene có BẢNG: 3 chỗ đặt (cho mắt thấy đổi) nhưng **bước 1** ⇒ vẫn 1-tại-1-lúc.
        #     3 chỗ đó chồng nhau theo chiều dọc (250/480/610, cao tới 281) nên **bắt buộc**
        #     phải 1-tại-1-lúc. Đây là bản user đã duyệt ở `demo_note.mp4`, không đổi.
        #   · scene có ẢNH: 2 chỗ RỜI HẲN NHAU ⇒ **bước 2**, hai cái sống cùng lúc được.
        #   ⚠️ Bản đầu tao lấy `step = số chỗ` cho cả hai ⇒ scene bảng cho 3 cái cùng sống
        #     và gate không-gian bắt ngay 8 cặp đè nhau. Gate mới trả tiền ngay lượt đầu.
        npos = len(SW_TBL_Y) if tbl else len(OUT_XY)
        step = 1 if tbl else len(OUT_XY)
        for j, el in enumerate(sups):
            trk = (sup1, sup2, sup3)[j % 3]
            f0 = st[j]
            nxt = j + step                         # cái kế TRONG CÙNG CHỖ ĐẶT
            fend = st[nxt] if nxt < n else to
            if tbl:
                sx, sy, sw = SW_TBL_X, SW_TBL_Y[j % npos], SW_TBL
                rot = SUP_ROT[j % 3]
            else:
                sx, sy = OUT_XY[j % npos]
                sw, rot = OUT_W, OUT_ROT[j % npos]
            trk.append(stick(f"s{j}-{k}", el, f0, fend - f0, sx, sy, sw,
                             rot=rot, ent="pop", amp=5, ph=1.2 + j * 2, sh="sm"))
        tag.append(txt(f"tag-{k}", s["tag"], f + 4, d - 4, "papercut-banner",
                       layout={"x": 74, "y": 58}, size=64))
        if s.get("stat"):
            body, sz = STAT[s["stat"]]
            f_st = f + max(20, int(d * 0.10))
            stat.append(txt(f"st-{k}", body, f_st, to - f_st - 4, "papercut-stat",
                            color=AMBER, layout={"x": STAGE_X0 + 16, "y": 240, "w": 810},
                            size=sz))
        if s.get("formula"):
            stat_off = 150 if s.get("stat") else 0
            formula.append(txt(f"fm-{k}", s["formula"], f + int(d * 0.55),
                               d - int(d * 0.55) - 6, "papercut-formula",
                               color=AMBER,
                               layout={"x": STAGE_X0 + 16, "y": 430 + stat_off, "w": 830},
                               size=58))

    for idx, body, col in PUNCH:
        f = F(idx)
        end = round(lines[idx]["end"] * FPS)
        punch.append(txt(f"p-{idx}", body, f + 8, max(60, end - f - 8),
                         "papercut-banner", color=col, layout={"x": PX}, size=62))

    T = lambda i, n, ty, c: {"id": i, "name": n, "type": ty, "muted": False,   # noqa: E731
                             "hidden": False, "locked": False, "clips": c}
    tracks = [
        T("trk-bg", "nền giấy", "background", trk_bg),
        T("trk-hero", "hero ảnh", "sticker", hero),
        T("trk-sup1", "phụ 1", "sticker", sup1),
        T("trk-sup2", "phụ 2", "sticker", sup2),
        T("trk-sup3", "phụ 3", "sticker", sup3),
        T("trk-cast-l", "cast trái", "sticker", cl),
        T("trk-cast-r", "cast phải", "sticker", cr),
        T("trk-stat", "bảng số liệu", "text", stat),
        T("trk-formula", "công thức", "text", formula),
        T("trk-tag", "tag", "text", tag),
        T("trk-punch", "punch", "text", punch),
        T("trk-voice", "giọng", "audio",
          [{"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
            "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]),
    ]
    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": "nenkin", "fps": FPS,
                 "width": 1920, "height": 1080,
                 "createdAt": "2026-08-26T00:00:00.000Z",
                 "modifiedAt": "2026-08-26T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        "sceneMarkers": [{"id": f"sc-{k}", "atFrame": s["f"], "label": s["tag"]}
                         for k, s in enumerate(SCENES)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44,
                     "lines": [{"text": c["text"],
                                "startMs": round(c["start"] * 1000),
                                "endMs": round(c["end"] * 1000)}
                               for l in lines for c in split_caption(l)],
                     "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }

    out = RV / "projects" / NAME
    out.mkdir(parents=True, exist_ok=True)
    (out / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    # ── GATE: mọi asset khai báo phải TỒN TẠI (render-background §1.5) ──────
    ad = RV / "public" / "projects" / NAME / "assets"
    ad.mkdir(parents=True, exist_ok=True)
    src = PROJ / "06_VIDEO" / STEM
    for p in list((src / "photocard").glob("*.png")) + list((src / "sticker").glob("*.png")):
        shutil.copy(p, ad / p.name)
    for c in CAST_RATIO:
        f = PROJ / "assets" / "cast" / f"{c}.png"
        if f.exists():
            shutil.copy(f, ad / f.name)
    old = RV / "public" / "projects" / "nenkin-17-demo" / "assets" / "paper.jpg"
    if old.exists():
        shutil.copy(old, ad / "paper.jpg")

    want = {c["asset"].split("/")[-1] for t in tracks if t["type"] == "sticker"
            for c in t["clips"]}
    want |= {"paper.jpg"}
    miss = sorted(w for w in want if not (ad / w).exists())

    # ── GATE: sticker NGOÀI ảnh · trong khung · không đè cast · không đè nhau ─
    # 🔴 Gate ĐỔI BẢN CHẤT lần thứ hai. Lịch sử để lần sau đừng khôi phục bản cũ:
    #   ① "sup phải nằm trong DẢI SÂN KHẤU" — đúng khi sup nằm ĐÈ lên hero. Nay sup ra
    #      ngoài hero (§OUT_XY) nên nó **cố tình** ở ngoài dải ⇒ giữ gate cũ là chặn đúng
    #      thứ thiết kế mới yêu cầu.
    #   ② "chỉ 1 sup sống mỗi frame" — relay toàn cục. Nay 2 slot rời nhau được sống cùng
    #      lúc (user cho phép), nên bất biến thật là **không đè nhau trong KHÔNG GIAN**.
    # ⇒ Bốn điều kiện dưới là bất biến MỚI, đo trên hộp đã tính phép xoay.
    HERO_BLEED_MAX = 90
    aspect = {}
    for p in (src / "sticker").glob("*.png"):
        with Image.open(p) as im:
            aspect[p.name] = im.width / im.height

    def _rect(c):
        """Hộp bao ĐÃ tính phép xoay — xoay 6–7° làm hộp phình ~20px mỗi chiều."""
        L = c["layout"]
        w = L["w"]
        h = w / aspect.get(c["asset"].split("/")[-1], 1.0)
        th = math.radians(abs(L.get("rotation", 0)))
        ww = w * math.cos(th) + h * math.sin(th)
        hh = h * math.cos(th) + w * math.sin(th)
        cx, cy = L["x"] + w / 2, L["y"] + h / 2
        return (cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)

    def _hit(a, b, pad=0):
        return (a[0] < b[2] - pad and b[0] < a[2] - pad
                and a[1] < b[3] - pad and b[1] < a[3] - pad)

    supclips = [c for t in tracks if t["id"] in ("trk-sup1", "trk-sup2", "trk-sup3")
                for c in t["clips"]]
    tbl_scene = {k for k, s in enumerate(SCENES) if s.get("stat") or s.get("formula")}
    heroR = (HX, HERO_Y, HX + HW, HERO_BOTTOM)
    lost, onhero, oncast = [], [], []
    for c in supclips:
        k = int(c["id"].split("-")[1])
        r = _rect(c)
        if r[0] < 4 or r[2] > 1916 or r[1] < 4 or r[3] > HERO_BOTTOM:
            lost.append(c["id"])                       # lọt khỏi khung / xuống vùng phụ đề
        if k not in tbl_scene and _hit(r, heroR, pad=6):
            onhero.append(c["id"])                     # ⛔ điều user vừa cấm
        s = SCENES[k]
        for side, ratio in (("l", CAST_RATIO[s["l"]]), ("r", CAST_RATIO[s["r"]])):
            cw = round(CAST_H * ratio)
            cx0 = CAST_MARGIN if side == "l" else 1920 - cw - CAST_MARGIN
            if _hit(r, (cx0, CAST_FEET_Y - CAST_H, cx0 + cw, CAST_FEET_Y), pad=6):
                oncast.append(c["id"])
    # đè nhau trong không gian, chỉ xét cặp CÙNG SỐNG một frame
    pairs = []
    for i, a in enumerate(supclips):
        for b in supclips[i + 1:]:
            if a["from"] < b["from"] + b["durationInFrames"] \
               and b["from"] < a["from"] + a["durationInFrames"] \
               and _hit(_rect(a), _rect(b), pad=6):
                pairs.append((a["id"], b["id"]))
    for lab, bad in (("lọt khỏi khung / chạm phụ đề", lost),
                     ("ĐÈ LÊN ẢNH HERO", onhero),
                     ("đè lên cast", oncast),
                     ("đè lên nhau", pairs)):
        if bad:
            print(f"🔴 sticker {lab}: {len(bad)} — {bad[:8]}")
            return 1
    if HERO_BLEED > HERO_BLEED_MAX:
        print(f"🔴 hero lấn vào cast {HERO_BLEED}px > trần {HERO_BLEED_MAX}px — "
              f"cast sẽ che nội dung ảnh, không chỉ viền")
        return 1

    ns = sum(len(t["clips"]) for t in tracks if t["type"] == "sticker")
    nt = sum(len(t["clips"]) for t in tracks if t["type"] == "text")
    print(f"✓ {out / 'project.json'}")
    print(f"   {DUR} frame ({DUR/FPS/60:.2f}′) · {len(SCENES)} scene · {ns} sticker "
          f"· {nt} text · {len(lines)} dòng phụ đề")
    print(f"   dải sân khấu {STAGE_X0}–{STAGE_X1} ({STAGE_X1-STAGE_X0}px) · "
          f"cast rộng {_CW}px")
    print(f"   HERO {HW}px = {HW*100//1920}% khung (lấn cast {HERO_BLEED}px/bên) · "
          f"trên màn 390px ≈ {round(HW*390/1920)}px")
    print(f"   STICKER scene-ẢNH {OUT_W}px NGOÀI hero ({len(OUT_XY)} chỗ góc trên, "
          f"2 cái sống cùng lúc) · scene-BẢNG {SW_TBL}px làn x={SW_TBL_X} "
          f"({len(SW_TBL_Y)} chỗ, 1-tại-1-lúc) · trên màn 390px ≈ "
          f"{round(OUT_W*390/1920)}px")
    print(f"   scene ngắn nhất {min((s['to']-s['f'])/FPS for s in SCENES):.1f}s · "
          f"dài nhất {max((s['to']-s['f'])/FPS for s in SCENES):.1f}s · "
          f"{len(SCENES)/(DUR/FPS/60):.2f} scene/phút")

    # ── GATE: sticker của scene có BẢNG không được đè lên mực bảng ─────────
    # Track `trk-stat` vẽ SAU sticker ⇒ chữ bảng nằm TRÊN hình ⇒ đè là mất đọc.
    over = [s["tag"] for s in SCENES
            if (s.get("stat") or s.get("formula")) and (s.get("sup") or [])
            and SW_TBL_X < TBL_INK_X1]
    if over:
        print(f"🔴 sticker đè mực bảng ở {len(over)} scene (SW_TBL_X={SW_TBL_X} < "
              f"{TBL_INK_X1}) — hạ SW_TBL hoặc thu bảng")
        return 1
    if max(SW_TBL_Y) + SW_TBL > HERO_BOTTOM:
        print(f"🔴 sticker bảng slot cuối chạm vùng phụ đề "
              f"({max(SW_TBL_Y)+SW_TBL} > {HERO_BOTTOM})")
        return 1

    # ── GATE: clip cùng TRACK không được trùng thời gian ───────────────────
    # ⚠️ Gate "chỉ 1 sup sống mỗi frame" ĐÃ BỎ — nó là bất biến của bản relay-toàn-cục,
    # và bản mới cố tình cho 2 slot rời nhau sống cùng lúc. Thay bằng gate KHÔNG-GIAN ở
    # trên. Cái còn phải giữ là bất biến của TRACK: một track chỉ vẽ được một clip.
    # (Bước tiếp sức nhảy `nslot` bậc mà track quay vòng theo 3 ⇒ đúng khi nslot ≤ 3.)
    dupe = []
    for t in tracks:
        if t["type"] != "sticker":
            continue
        iv = sorted((c["from"], c["from"] + c["durationInFrames"], c["id"])
                    for c in t["clips"])
        for a, b in zip(iv, iv[1:]):
            if b[0] < a[1]:
                dupe.append(f"{t['id']}: {a[2]} × {b[2]}")
    if dupe:
        print(f"🔴 clip trùng thời gian trên CÙNG track: {len(dupe)} — {dupe[:6]}")
        return 1

    # ── GATE: mọi khối phụ đề ≤2 dòng (audience-45plus §3) ─────────────────
    caps = proj["captions"]["lines"]
    longc = [c for c in caps if len(c["text"]) > CAP_MAX]
    print(f"   phụ đề: {len(lines)} dòng timeline → {len(caps)} khối · "
          f"dài nhất {max(len(c['text']) for c in caps)} ký (trần {CAP_MAX})")
    if longc:
        print(f"🔴 {len(longc)} khối phụ đề > {CAP_MAX} ký ⇒ sẽ ra ≥3 dòng:")
        for c in longc[:5]:
            print(f"     · {len(c['text'])} ký | {c['text'][:40]}")
        return 1
    if miss:
        print(f"🔴 THIẾU {len(miss)} asset:")
        for m in miss:
            print(f"     · {m}")
        return 1
    if lost:
        print(f"🔴 sticker lọt khỏi dải (cast sẽ đè): {lost}")
        return 1
    print(f"   ✓ {len(want)} asset đủ · mọi sticker trong dải")
    return 0


if __name__ == "__main__":
    sys.exit(main())
