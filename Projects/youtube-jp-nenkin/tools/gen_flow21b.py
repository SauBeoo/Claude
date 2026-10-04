# -*- coding: utf-8 -*-
r"""gen_flow21b.py — 54 prompt clip AI cho video 21 (bản viết lại).

Chỉ KHAI BÁO cảnh. Mọi hằng số (STYLE/MOTION/AVOID/FRAMING) nằm ở
`videogen_nenkin.py` → `youtube-jp-showa/tools/videogen_lib.py` — khuôn có số chứng minh
(cùng lô 22 clip: v1 **22/22 lỗi** → v2 **2/22 lỗi**).

Ba luật khiến file này trông "nhàm" một cách CỐ Ý, mỗi luật đổi bằng một lô clip hỏng:
  ① **Vật ở TƯ THẾ CUỐI ngay frame đầu.** Không mở/gấp/nhặt/đặt/lật. 58/73 clip v21 có thao
     tác đổi trạng thái vật, 4/6 soi kỹ hỏng (nắp hộp thư đóng rồi mở lại, phong bì biến mất,
     bút đỏ nhân đôi, thao tác chạy ngược).
  ② **Kính ĐEO SẴN**, tả trong CAST, không bao giờ có động từ đeo/tháo. Ca hỏng tệ nhất.
  ③ **Không ai viết chữ.** Hành động dùng KÝ HIỆU (vòng tròn đỏ · gạch chân · mũi tên).
     11/84 shot v21 có người viết số → chữ nát vô nghĩa. Con số nay do THẺ chở (49,9% video).

⇒ Việc của footage là **sự kiện vật lý + cử chỉ người**, không phải chở dữ kiện. Đó cũng là
lý do footage rút từ 74,0% xuống 50,1%.

CHẠY:  python tools/gen_flow21b.py       → flow21b_FLOW.txt · _TENFILE.txt · _BLOCKS.md
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from videogen_nenkin import build_n, gate_n, write_n            # noqa: E402

VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "21_fuyo-shinkokusho-205man")

# ── BỐI CẢNH ───────────────────────────────────────────────────────────────────
P = {
 "ima":   "the living room of an ordinary Japanese suburban house, a low wooden table, a net curtain at the window, a potted plant in the corner",
 "ima2":  "the living room of a different Japanese suburban house, a low table with a cloth runner, a sideboard, a bright window with a net curtain",
 "dai":   "the kitchen of an ordinary Japanese house, a small dining table by the window, a kettle on the stove, plain tiled wall",
 "tsuku": "a small study corner of a Japanese house, a wooden desk, a desk lamp, a plain handheld calculator, a window to one side",
 "genkan":"the entrance hall of a Japanese house, a shoe cupboard, a frosted glass front door letting in daylight",
 "posuto":"the front gate of an ordinary Japanese house, a low wall-mounted letterbox, a clipped hedge, a quiet residential street behind",
}

# ── CAST + PROP ──
# 🔴 2026-09-06, user: *"cái tờ giấy gen ra nó trắng tinh"*. Nguyên nhân là chính tao: AVOID
# cấm "any letters, words, numbers, kanji ... on any paper, form" nên model trả về tờ giấy
# TRẮNG TRƠN — trông giả ngay, vì tờ 申告書 thật có LƯỚI Ô KẺ in sẵn.
# ⇒ Lằn ranh đúng đã ghi ở `media-library.md` §2.10 ⑦: *"giấy tờ chung chung, Ô KẺ TRỐNG,
#   không chữ — cấm dựng bản sao giấy tờ chính thức"*. Ô kẻ ĐƯỢC, chữ thì KHÔNG.
# ⇒ Cách chữa là tả TÍCH CỰC cái giấy CÓ gì (lưới ô, dòng kẻ, tông xanh nhạt), giữ nguyên
#   AVOID cấm chữ. Đúng nguyên tắc "model đọc TỪ KHOÁ, không đọc phủ định" — chỉ cấm thôi
#   thì model bỏ luôn cả thứ mình muốn giữ.
# ⚖️ CỐ Ý **không** tả đúng bố cục tờ thật: giấy phải trông là "một tờ đơn có ô kẻ", không
#   phải bản sao nhận ra được — bản sao giấy tờ chính thức là thứ compliance cấm.
C = {
 "m1": "a man in his mid-sixties in a plain grey knitted cardigan over a white shirt, wearing thin metal-rimmed glasses",
 "w1": "a woman in her early sixties in a plain navy blouse with a plain unmarked beige apron",
 "m2": "a man in his late sixties with short grey hair, in a plain brown zip-up cardigan, wearing thin metal-rimmed glasses",
 "w2": "a woman in her mid-sixties with short grey hair, in a plain grey cardigan over a cream blouse",
 # PROP — dùng token như cast, để MỖI clip tự mang mô tả (t2v không có bộ nhớ giữa clip)
 "youshi": "a sheet ruled into a grid of small empty boxes, a plain pale-green printed form",
 "fuutou": "a plain white unmarked window envelope with one transparent address window",
 "folder": "a plain manila card folder with a smooth blank unmarked cover",
}

# ── 54 SHOT ── (id, khối, ACT 3 nhịp, preset, FRAMING, tier)
S = [
 # 0:00 — phong bì đến nhà
 ("A01", "HOOK", "A_M1 stands at the gate holding A_FUUTOU already in one hand, then a breeze stirs the hedge beside him, then he looks down at it and shifts his weight", "posuto", "wide", "Q"),
 # 0:21 — 聞き手: hồi đi làm công ty làm hộ / không còn 年末調整
 ("A02", "KAIWA", "A_M1 sits at the low table with both hands resting flat on the wood beside A_FUUTOU, then the net curtain moves in the draught behind him, then he tilts his head slightly and looks aside", "ima", "medium", "Q"),
 ("A03", "KAIWA", "A_W1 stands in the kitchen doorway with a folded cloth over one arm, then steam rises from the kettle behind her, then she brings her arms together and looks toward the table", "dai", "wide", "F"),
 ("A04", "KAIWA", "A_M1 sits back in the chair with A_FUUTOU flat on the table in front of him, then the shadow of the window frame moves across the wood, then he rubs the back of his neck and looks up", "ima", "medium", "Q"),
 # 0:55 — まず、事実から + persona
 ("A05", "PERSONA", "A_M1 sits upright at the table with both palms flat on the surface, then a breeze moves the net curtain at the window, then he nods once and looks down at A_YOUSHI", "ima", "medium", "Q"),
 ("A06", "PERSONA", "A_W1 settles onto the cushion beside A_M1 with her hands in her lap, then the sleeve of her blouse catches the light, then she straightens and looks at the table", "ima", "wide", "F"),
 # 1:19 — お願い①: xem ngày hạn trên chính tờ giấy
 ("A07", "TODO1", "A_M1 sits at the desk with a red pen already in one hand and A_YOUSHI flat in front of him, then he draws a slow red circle around one line while the shadow of his hand moves across the same sheet, then he taps the circle twice and sits back", "tsuku", "ots", "Q"),
 ("A08", "TODO1", "A_W1 stands beside the desk looking down at A_YOUSHI, then a breeze moves the net curtain, then she points at the circled line and lets her arm drop", "tsuku", "wide", "F"),
 ("A09", "TODO1", "A_M1 rests both forearms on the desk on either side of A_YOUSHI, then the lamp light glints on his glasses, then he shakes his head slowly and straightens up", "tsuku", "medium", "Q"),
 # 1:53 — その数字はもう使われていません
 ("A10", "SEN", "A_M1 sits at the table with one hand resting on A_FOLDER, then the curtain sways at the window, then he turns one palm upward and looks aside", "ima", "medium", "Q"),
 # 3:22 — あなたの場合はいくら変わるのか
 ("A11", "KEISAN", "A_M1 sits at the table with A_YOUSHI flat in front of him and a plain calculator beside it, then the shadow of the window frame moves over the table, then he rests one fingertip on the same sheet and looks up", "ima", "ots", "Q"),
 # 3:53 — 配偶者控除 / 紙一枚で
 ("A12", "KEISAN", "A_W1 sits across the table from A_M1 with both hands around a teacup, then steam rises from the cup, then she squares her shoulders and looks at him", "ima", "wide", "Q"),
 ("A13", "KEISAN", "A_M1 holds A_YOUSHI up at chest height in both hands, then dust drifts in the light from the window, then he brings it down to the table and rests his palm on it", "ima", "medium", "Q"),
 # 4:53 — そういうことになります + 山田夫妻
 ("A14", "YAMADA", "A_M1 sits back with both hands on his knees, then the curtain moves behind him, then he lets his shoulders drop and looks down", "ima", "medium", "F"),
 ("A15", "YAMADA", "A_M2 and A_W2 sit side by side at their own low table with a single form between them, then a breeze stirs the plant on the windowsill, then A_M2 moves one hand toward A_YOUSHI and stops", "ima2", "wide", "Q"),
 ("A16", "YAMADA", "A_W2 rests one elbow on the table over A_YOUSHI, then the light catches the hem of her sleeve, then she turns her face toward A_M2 and settles back", "ima2", "medium", "Q"),
 # 5:48 — 家族の人数で
 ("A17", "YAMADA", "A_M2 holds three fingers raised at chest height, then the shadow of the window frame crosses his arm, then he brings the hand down onto the table and looks at it", "ima2", "medium", "Q"),
 ("A18", "YAMADA", "A_W2 stands at the sideboard where three plain framed photographs already stand in a row, then a breeze moves the curtain beside them, then she rests one hand on the wood and looks along the row", "ima2", "wide", "F"),
 # 6:17 — お願い② + よくある誤解
 ("A19", "TODO2", "A_W1 sits at the kitchen table with her hands together in front of her, then steam drifts from the kettle behind her, then she looks toward the window and shifts her weight", "dai", "medium", "Q"),
 ("A20", "TODO2", "A_M1 sits at the low table with A_YOUSHI and the plain calculator in front of him, then dust drifts in the window light, then he moves the calculator a little closer and rests his hand beside it", "ima", "ots", "Q"),
 ("A21", "GOKAI", "A_M1 sits upright and turns one hand palm up over the table, then the curtain sways at the window, then he brings the hand back down and looks at A_YOUSHI", "ima", "medium", "F"),
 # 6:57 — 同じなら何が変わる / 控除が消える
 ("A21b", "GOKAI", "A_M1 sits at the desk with A_YOUSHI square in front of him and both hands resting either side of it, then the lamp light glints on his glasses, then he draws one fingertip slowly down the left edge of the sheet and stops", "tsuku", "ots", "Q"),
 ("A22", "GOKAI", "A_W1 sits opposite with both hands around the teacup, then steam rises between them, then she tilts her head and looks at A_YOUSHI", "ima", "wide", "Q"),
 ("A23", "GOKAI", "A_M1 draws a slow red line under one row on A_YOUSHI with a red pen already in one hand, then the shadow of his hand moves across the same sheet, then he lifts the pen clear and rests his wrist on the table", "ima", "ots", "Q"),
 ("A24", "GOKAI", "A_M1 sits with both palms flat on the table on either side of A_YOUSHI, then a breeze moves the curtain, then he spreads his fingers slightly and looks up", "ima", "medium", "F"),
 # 7:21 — 引く前の額が大きくなる
 ("A25", "GOKAI", "A_M1 holds one hand low and the other higher above the table to show a gap between them, then the light catches his sleeve, then he holds the two hands still and looks between them", "ima", "medium", "Q"),
 # 7:35 — CTA giữa
 ("A26", "CTA", "A_W1 stands by the window with the net curtain moving beside her, then she turns her shoulders toward the room, then she rests one hand on the sill and looks out", "ima", "wide", "F"),
 ("A27", "CTA", "A_M1 sits at the table with both hands loosely together, then the shadow of the frame moves over the wood, then he separates them and lays them flat", "ima", "medium", "F"),
 ("A28", "CTA", "A_M2 and A_W2 sit together on the sofa with a plain cushion between them, then a breeze stirs the curtain, then A_W2 shifts her weight and leans a little toward A_M2", "ima2", "wide", "F"),
 ("A29", "CTA", "A_M1 stands in the doorway of the room with one hand on the frame, then the curtain moves behind him, then he shifts his weight in place and looks toward the table", "ima", "wide", "F"),
 # 8:03 — なぜ私にも紙が来る / 住民税のため
 ("A30", "JUMIN", "A_W1 sits at the kitchen table with A_FUUTOU flat in front of her, then steam drifts from the cup beside it, then she turns both palms upward and looks aside", "dai", "medium", "Q"),
 ("A31", "JUMIN", "A_M1 sits at the low table with one sheet of A_YOUSHI on the left and a second sheet of A_YOUSHI on the right, a hand's width of bare table between them, then dust drifts in the window light, then he moves one fingertip from the left sheet across to the right one and stops", "ima", "medium", "Q"),
 ("A32", "JUMIN", "A_M1 rests his chin on one hand at the table, then the curtain sways at the window, then he brings the hand down and nods once", "ima", "medium", "F"),
 # 8:27 — 正しく計算するため / 期限を過ぎたら
 ("A33", "KIGEN", "A_W1 stands beside a plain wall calendar already showing the current month, then a breeze moves the corner of the page, then she rests one finger below the grid and lowers her arm", "dai", "wide", "Q"),
 ("A34", "KIGEN", "A_M1 sits at the desk looking down at A_YOUSHI with both forearms on the wood, then the lamp light glints on his glasses, then he lifts his chin and looks toward the window", "tsuku", "medium", "Q"),
 ("A35", "KIGEN", "A_W1 sits with one hand over her mouth and the other in her lap, then the light catches her sleeve, then she brings the hand down and looks at the table", "dai", "medium", "F"),
 # 8:59 — あとから出せば戻ってくる / その年が終わったら
 ("A36", "SAKANOBORU", "A_M1 holds A_YOUSHI loosely in one hand at chest height, then a breeze moves the curtain beside him, then he brings it against his chest and lets his shoulders drop", "ima", "medium", "Q"),
 ("A37", "SAKANOBORU", "A_W1 stands at the entrance hall with one hand resting on the shoe cupboard, then dust drifts in the light from the glass door, then she straightens up and looks toward the door", "genkan", "wide", "F"),
 # 9:25 — 落とし穴 + 安心していた
 ("A38", "OTOSHIANA", "A_M1 sits very still at the table with both hands flat beside A_YOUSHI, then the shadow of the frame creeps across the wood, then he draws both hands back toward himself and looks down", "ima", "medium", "Q"),
 ("A39", "OTOSHIANA", "A_W1 sits opposite with her fingers around the teacup, then steam rises from it, then she loosens her grip and looks up", "ima", "wide", "Q"),
 ("A40", "OTOSHIANA", "A_M2 sits alone at his table with one arm along the back of the chair, then a breeze stirs the plant on the sill, then he brings the arm down and leans a little toward the table", "ima2", "wide", "F"),
 # 10:16 — 払いすぎても返ってこない / こちらから出す
 ("A41", "OTOSHIANA", "A_M1 sits with A_YOUSHI flat in front of him and both hands away from it, then dust drifts in the window light, then he brings one hand back onto the same sheet and holds it there", "ima", "ots", "Q"),
 ("A42", "OTOSHIANA", "A_M1 stands at the gate with a plain unmarked white envelope already in one hand, then a breeze moves the hedge beside him, then he raises it a little and looks along the street", "posuto", "wide", "Q"),
 # 10:43 — 気になっている点
 ("A43", "QA", "A_W1 sits at the kitchen table with her hands together and her head tilted, then steam drifts from the kettle, then she raises one finger and brings it down again", "dai", "medium", "Q"),
 ("A44", "QA", "A_M1 sits at the low table and turns one hand palm up beside A_YOUSHI, then the curtain sways, then he turns it back over and rests it flat", "ima", "medium", "F"),
 # 11:16 — ご家族が多いお宅ほど
 ("A45", "QA", "A_M2 and A_W2 sit at their table with three plain teacups already standing in a row between them, then a breeze moves the curtain, then A_M2 rests a hand beside the cups and looks along them", "ima2", "wide", "Q"),
 ("A46", "QA", "A_W2 sits with both hands in her lap looking down at A_YOUSHI, then the light catches the hem of her sleeve, then she lifts her chin and looks toward A_M2", "ima2", "wide", "F"),
 # 12:23 — disclaimer + CTA đăng ký
 ("A47", "END", "A_M1 sits back from the table with A_YOUSHI flat in front of him, then the shadow of the window frame moves across it, then he rests both hands in his lap and looks down", "ima", "medium", "F"),
 ("A48", "END", "A_W1 stands at the window with the net curtain moving beside her, then she rests one hand on the sill, then she turns her shoulders back toward the room", "ima", "wide", "F"),
 ("A49", "END", "A_M1 sits at the desk under the lamp with both forearms on the wood, then the lamp light glints on his glasses, then he sits up straighter and looks toward the window", "tsuku", "medium", "Q"),
 ("A50", "END", "A_M2 and A_W2 sit side by side with a single form on the table between them, then a breeze stirs the plant on the sill, then they both look down at it and settle", "ima2", "wide", "F"),
 # 12:54 — 次回予告 (未支給年金)
 ("A51", "NEXT", "A_W1 stands in the entrance hall holding A_FUUTOU held in both hands, then dust drifts in the light from the glass door, then she brings her hands down and looks at it", "genkan", "wide", "Q"),
 ("A52", "NEXT", "A_M1 sits at the low table with A_YOUSHI in front of him and one hand resting on its edge, then the curtain sways at the window, then he moves the hand to the middle of the sheet and stops", "ima", "ots", "Q"),
 ("A53", "NEXT", "A_W1 sits at the kitchen table with both hands around a cup, then steam rises from it, then she looks toward the window and shifts her weight", "dai", "medium", "F"),
 # 13:19 — chữ ký đóng bài
 ("A54", "NEXT", "A_M1 stands at the window with one hand on the frame looking out, then a breeze moves the net curtain beside him, then he brings the hand down and turns his shoulders back toward the room", "ima", "wide", "Q"),
]

# ── LO GEN LAI (2026-09-06) — chi nhung shot CAN, khong gen lai ca 54 ─────────
# Chot sau khi soi 54 clip (sheet 4-frame) + soi day 12 clip nghi.
# 🔴 Bai hoc do luong: trong 12 clip soi day, **6 cai hoa ra BINH THUONG**
#    (004 · 007 · 023 · 035 · 028 khong morph · 017 khong sai du kien) — sheet thua
#    BAO OAN nhieu. Nen danh sach nay chi gom cai DA XAC MINH hoac co nguyen nhan
#    ro rang nam trong prompt cua chinh minh.
# ── LO GEN LAI VONG 2 (chi 3 shot) ───────────────────────────────────────────
REGEN2 = {
 "A21b": "SHOT MOI — dong khe 9,4s @6:35 (scene 26: 27,1s can 4 shot, dang co 3)",
 "A31":  "lo truoc ra MOT to giay; shot nay de SO SANH hai so nen phai thay HAI to",
 "A46":  "m2 ra dan ong TRE khong kinh; da them 'short grey hair' vao mo ta cast",
}

REGEN = {
 "A27": "ban tay trai thanh cuc thit khong ngon (3 frame cuoi) — DA XAC MINH",
 "A42": "phong bi TU HIEN RA o giay 1,5; giay 0,5 hai tay trang khong — DA XAC MINH",
 "A28": "w2 ra toc den, lech han A50 (toc bac) => cung nhan vat thanh 2 nguoi",
 "A45": "w2 ra phu nu TRE toc den",
 "A40": "cui toi khi dau ra khoi khung -> than khong dau; framing da doi sang wide",
 "A46": "hai than nguoi khong dau canh nhau; framing da doi sang wide",
 "A11": "giay trang tron — shot ots can giay",
 "A13": "giay trang tron — nhan vat GIO TO GIAY len truoc nguc",
 "A20": "giay trang tron — shot ots can giay",
 "A31": "chi ra MOT to giay, ma shot nay de SO SANH hai so",
 "A36": "giay trang tron — to giay ap vao nguc",
 "A41": "giay trang tron — shot ots can giay",
 "A51": "giay trang tron — hai tay giu to giay",
 "A52": "giay trang tron — shot ots can giay",
}

rows = build_n(S, P, C)
n_red, _ = gate_n(rows, S, P, C, whitelist_no_human={}, interior=set(P) - {"posuto"}, strict=True)
write_n(rows, VD, prefix="flow21b")
print(f"\n{len(rows)} prompt → {VD}\\flow21b_FLOW.txt")
write_n(rows, VD, prefix="flow21b_REGEN", only=set(REGEN))
write_n(rows, VD, prefix="flow21b_REGEN2", only=set(REGEN2))
print(f"{len(REGEN)} prompt GEN LAI -> {VD}\flow21b_REGEN_FLOW.txt")
print(f"{len(REGEN2)} prompt GEN LAI VONG 2 -> flow21b_REGEN2_FLOW.txt")
for _k in REGEN2:
    print(f"   {_k}  {REGEN2[_k]}")
sys.exit(1 if n_red else 0)
