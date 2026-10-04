# -*- coding: utf-8 -*-
r"""_motion19_real.py — OVERRIDE motion cho ban NGUOI THAT (photoreal) cua video 19.

User chot 2026-09-03: *"Toi muon lam dang nguoi that di, cho toi prompt gen anh
va video dang nguoi that."*

🔴 VI SAO PHAI CO FILE NAY, khong dung lai `_motion19.py` nguyen xi:
   9/74 motion cua ban collage la **SIEU THUC** — giay bay khoi tuong, san nha
   tach doi, xap tien bi xe roi bay ra khoi khung. Voi giay cat dan thi do la
   ngon ngu dung; voi NGUOI THAT thi no thanh quai di (vat the bay lo lung,
   nguoi bi keo tach ra) — dung cai lam video AI trong "sai sai".
   65 motion con lai von da TA THUC (tay mo ngan keo, keo cat giay, cua quay
   khoa cung) nen dung lai duoc — file nay chi ghi de 9 cai.

📐 NGUYEN TAC CHUYEN: giu **HANG NANG LUONG** va giu **NGHIA cua cau loi**,
   doi cach thi hanh tu "phep la" sang "may quay + dien xuat":
     giay bay khoi ke      -> may LUI ra, lo dan xap phong bi bi bo quen sau lung
     san nha tach doi      -> hai nguoi buoc ve hai huong, may giu giua
     xap tien bi xe bay    -> ban tay RUT di mot nua xap, dat sang ben, khoang trong
   Peak van la peak: cai manh nam o **hanh dong dut khoat + may day**, khong o
   phep la.

⚠️ COMPLIANCE (`youtube-compliance.md` §2.1): anh/canh AI **realistic** trong
   video => phai TICK "altered/synthetic content" luc upload. Nhan vat phai HU
   CAU; cam dung mat nguoi that cu the, cam dan dung su kien/dia diem co that.
"""

# chi ghi de 9 key — phan con lai lay tu _motion19.M
OVERRIDE = {

# [0-10s] 「あなたが五年で受け取り損ねるのは、およそ百六十八万円です」
# collage: nan quat tien bay khoi ke  ->  real: may LUI ra, lo xap phong bi bi bo quen
"hataraku": dict(lv="peak", cam="pull_out", m=(
    "the man works on without pausing - he sets a box on the shelf, checks it, reaches "
    "for the next - while the camera pulls slowly back to reveal the company notice board "
    "on the wall behind him, where a single sun-faded sheet of paper hangs curling at the "
    "corners, clearly unread for a long time; he never turns to look at it; the daylight "
    "from the high window moves slowly across the board")),

# collage: 2 to tien lot ra khoi thung  ->  real: phong bi tuot ra, roi xuong, khong ai nhat
"hataraku_b": dict(lv="peak", cam="push", m=(
    "the gloved hands lift the box, push it home along the shelf and pat it square, then "
    "rest flat on the lid for a moment before withdrawing; dust lifts off the cardboard "
    "and turns slowly in the shaft of window light")),

# collage: 2 to tien duoc dat len chong  ->  real: dem tien vao tay, dut khoat
"koyou_hoken_b": dict(lv="mid", cam="static", m=(
    "extreme close-up: the uniformed hand counts three folded ten-thousand-yen notes onto "
    "the older open palm one at a time, each landing with a small definite press; the "
    "older fingers close over them on the last one")),

# collage: thuoc ke SLAM chan chong xu  ->  real: ban tay dan thuoc xuong, xu do
"jougen": dict(lv="peak", cam="push_hard", m=(
    "a hand brings a flat wooden ruler down across the top of the growing coin stack and "
    "holds it there, pressing; the stack compresses, three coins are knocked off the side "
    "and roll away across the desk; the ruler does not lift and the hand does not let go")),

# collage: xap tien bi XE, bay khoi khung  ->  real: RUT di mot nua xap, khoang trong o lai
"84man": dict(lv="peak", cam="push_hard", m=(
    "two hands take hold of the banded stack of notes on the dark table and draw a large "
    "portion of it away in one steady pull, sliding it right out of frame; what is left "
    "settles visibly shorter and slightly askew, and the bare table where the rest stood "
    "is left empty under the hard light")),

# collage: phong bi rong tu bay khoi ban  ->  real: tay cho, roi ha xuong
"zero": dict(lv="peak", cam="push_hard", m=(
    "the open palm is held out flat and waits, completely still, for a long beat while "
    "nothing is put into it; then the fingers slowly curl closed on nothing and the hand "
    "lowers out of frame; the empty envelope beside it never moves; the cold flat light "
    "does not change")),

# collage: san nha SPLITS hai nguoi  ->  real: hai nguoi buoc ve hai huong
"futari": dict(lv="peak", cam="push", m=(
    "the two men stand shoulder to shoulder for a moment, then walk apart in opposite "
    "directions, the camera holding still between them so the gap opens across the frame; "
    "the uneasy one glances back once at the other, who does not look up from the envelope "
    "in his hand; the corridor behind them stays empty")),

# collage: kinh lup nem dia sang len giay  ->  real: dat kinh xuong, rut tay
"meisai_check_b": dict(lv="mid", cam="static", m=(
    "the magnifying glass is set down beside the payslip and rocks once on its rim before "
    "settling; the hand withdraws from frame; the sheet is left alone on the table with "
    "one line still marked by a fingernail crease")),

# collage: 4 trang lich bi boc bay khoi khung  ->  real: lat tung trang, dut khoat
"4kagetsu": dict(lv="peak", cam="push", m=(
    "a hand flips the calendar pages over one after another, faster each time - one, two, "
    "three - each page slapping down against the wall; on the fourth the hand stops with "
    "the page half-lifted and holds it there, not turning it")),
}
