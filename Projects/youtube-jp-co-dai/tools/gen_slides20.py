# -*- coding: utf-8 -*-
"""Sinh 20_sentei-koshin-akinasu_SLIDES.json + bo prompt anh (FLOW/NAMES).

⭐ LOP HINH KE THANH MOT CAU CHUYEN (user chot 2026-08-16):
   Khong phai 80 anh minh hoa roi rac, ma la MOT phong su ngan ve HAI LUONG CA TIM
   canh nhau, keo dai tu cuoi thang 7 den thang 10.

   NEO LAP LAI (phai xuat hien dung nhu nhau moi lan):
     - LUONG CUA TOI      : coc tre, dat nau do, cay met  -> HO DAT TRONG  -> van trong
     - LUONG BEN CANH     : cung khung hinh -> bi cat trui -> nay mam -> QUA TIM thang 9
     - MU ROM (mac wara)  : nhan vat, KHONG BAO GIO CO MAT. Cuoi bai = mu treo tren coc
     - KEO CAT CANH       : mo chuyen (tay ong hang xom) -> dong chuyen (tay nguoi ke)
     - SCOPP (xeng)       : buoc thu 4 bi giau, chi lo ra o hoi 2
     - TAM BANG GO GHI NGAY: truc lich, xuat hien 4 lan

   3 HOI:
     I  (0-4')   cuoi thang 7: luong met -> hoa -> han chot -> KY UC (toi nho cay /
                 ong ay cat) -> thang 9: ben kia 20 qua tim, ben nay cai ho
     II (4-14')  quay lai thang 7, lan nay LAM DUNG: doc -> cat -> trao -> dao
     III(14-19') lich chay toi thang 10 -> cua hang -> sach co 1697 -> tuc ngu -> mu rom

Dung script vi 2 ly do (giu nguyen tu gen_slides19.py):
  1) moi `match` PHAI la substring DUY NHAT cua mot dong _TTS.md — sai la render gay
  2) cue chon bang luat >=75 ky/slide => ~4,2 doi hinh/phut (audience-45plus.md §2)
"""
import re, json
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "20_sentei-koshin-akinasu"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"
DUR = 1170          # ~19,5 phut

L = [re.sub(r"\[[^\]]*\]", "", l).strip()
     for l in (PROJ / "03_SCRIPTS" / f"{SLUG}_TTS.md").read_text(encoding="utf-8").split("\n")]
L = [l for l in L if l and not l.startswith(("#", "TARGET_QUERY", "INTENT"))]


def P(n):
    return f"{VD}/ai_clean/{n}.jpeg"


# ══ THE VOX ═════════════════════════════════════════════════════════════════
# 19 the. Moi the la mot NUT cua cau chuyen, khong phai mot o infographic roi.
VOX = {
 2:  ("stat", {"kicker": "鋏を入れられる残り", "big": "10", "unit": "日",
               "sub": "7月下旬から8月上旬まで",
               "note": "この幅を外すと、秋には間に合いません"}, "wall_calendar_late_july"),
 33: ("compare", {"kicker": "花の真ん中を見る", "title": "棒が長いか、短いか",
                  "left": {"label": "長花柱花", "mark": "o", "verdict": "まだ実になる"},
                  "right": {"label": "短花柱花", "mark": "x", "verdict": "もう実にならない"}},
      "eggplant_flower_face_on"),
 37: ("compare", {"kicker": "葉の色で原因が分かれる", "title": "同じ短い花でも",
                  "left": {"label": "株ごと薄い黄緑", "mark": "x", "verdict": "肥料が足りない"},
                  "right": {"label": "葉は濃い緑", "mark": "x", "verdict": "暑さのほう"}},
      "eggplant_leaf_two_tones"),
 23: ("flow", {"kicker": "順番でしか効きません", "head": "読む・切る・渡す、そして",
               "pins": [[1300, 235, "読む"], [1300, 350, "切る"], [1300, 465, "渡す"]],
               "arrows": [[1260, 300, 980, 390, 0.18]]}, "three_tools_on_soil"),
 26: ("stat", {"kicker": "6月から一度も休まず", "big": "70", "unit": "日",
               "sub": "人間なら2か月ぶっ通し",
               "note": "疲れです。寿命ではありません"}, "worn_eggplant_stem_base"),
 45: ("process", {"kicker": "切る量", "title": "拍子抜けするほど乱暴に",
                  "steps": [{"label": "主枝を半分まで", "sub": "3分の2でも構いません"},
                            {"label": "太い枝を3本残す", "sub": "あとは落とす"},
                            {"label": "古い葉も全部", "sub": "終わるとほとんど棒", "hot": True}]},
      "pruning_shears_on_thick_stem"),
 # ⚠ k_title: `source` in ra nhan 「出典：」 => KHONG duoc dung lam kicker (kenh nay
 #   moat la NGUON THAT, dan nhan 出典 gia la tu ban re do tin). `num` in so thu tu
 #   o goc trai => bo luon, khong phai buoc so 1.
 50: ("title", {"title": "重り",
                "sub": "実は、ごほうびではありません。いま株を縛っているものです"},
      "single_dull_eggplant_hanging"),
 55: ("timeline", {"kicker": "この幅しかない", "title": "遅れると涼しくなります",
                   "marks": [["7月末", "いちばん良い"], ["8月頭", "まだ間に合う"],
                             ["8月末", "もう遅い"]],
                   "note": "新しい枝が育つ前に、秋が来ます"}, "bamboo_stake_with_date_tag"),
 62: ("compare", {"kicker": "渡す肥料を間違えない", "title": "いま作る仕事が違います",
                  "left": {"label": "実を太らせる肥料", "mark": "x", "verdict": "遠回りになる"},
                  "right": {"label": "葉を茂らせる肥料", "mark": "o", "verdict": "いま要るのはこちら"}},
      "fertilizer_granules_in_palm"),
 65: ("process", {"kicker": "水のやり方", "title": "土に指を挿してから",
                  "steps": [{"label": "第一関節まで挿す", "sub": "株元から少し離して"},
                            {"label": "湿っていたらやらない", "sub": "根が息をできません"},
                            {"label": "白く乾いたらたっぷり", "sub": "それだけです", "hot": True}]},
      "finger_pressed_into_dry_soil"),
 77: ("flow", {"kicker": "届かない理由", "head": "土にはある。吸う側が古い",
               "pins": [[1300, 235, "肥料は土の中"], [1300, 350, "根が硬くなる"],
                        [1300, 465, "だから届かない"]],
               "arrows": [[1260, 300, 980, 390, 0.18]]}, "old_thick_eggplant_root"),
 80: ("stat", {"kicker": "スコップを差す位置", "big": "30", "unit": "センチ",
               "sub": "株元から離して、ぐるりと何か所か",
               "note": "近すぎると、支えの根まで切れて倒れます"}, "spade_blade_in_soil_beside_plant"),
 84: ("stat", {"kicker": "切ったあとに起きること", "big": "2", "unit": "週間",
               "sub": "髪の毛ほどの白い根が何十本も",
               "note": "この白い根が、いちばんよく吸います"}, "fine_white_roots_in_soil"),
 92: ("compare", {"kicker": "上と下は別の仕事", "title": "片方だけでは効きません",
                  "left": {"label": "枝を切る", "mark": "o", "verdict": "上の仕事を減らす"},
                  "right": {"label": "根を切る", "mark": "o", "verdict": "下を作り直す"}},
      "shears_and_spade_side_by_side"),
 95: ("timeline", {"kicker": "切った日からのカレンダー", "title": "40日先に印をつける",
                   "marks": [["半月", "白い根が出る"], ["40日", "花と実"],
                             ["10月", "採り終わり"]],
                   "note": "8月の頭に切れば、9月半ばから採れます"}, "calendar_with_red_circle"),
 100: ("title", {"title": "棒",
                 "sub": "切って半月、上では何も起きません。それが順調な証拠です"},
       "bare_cut_eggplant_stump"),
 107: ("compare", {"kicker": "なぜ売り場に無いのか", "title": "売れる話と、売れない話",
                   "left": {"label": "苗と肥料", "mark": "x", "verdict": "また買ってもらえる"},
                   "right": {"label": "鋏とスコップ", "mark": "o", "verdict": "家にあるもの"}},
       "garden_shears_and_spade_leaning"),
 112: ("source", {"kicker": "出典", "org": "農業全書", "asof": "元禄10年・1697年",
                  "number": "40年",
                  "quote": "宮崎安貞が全国を回り、年寄りの百姓から聞き取って11巻にまとめた"},
       "old_japanese_book_on_wood"),
 117: ("source", {"kicker": "出典", "org": "毛吹草", "asof": "寛永15年・1638年",
                  "number": "400年",
                  "quote": "「秋茄子は嫁に食わすな」の古い実例が、この本に載っている"},
       "old_proverb_book_page"),
 119: ("compare", {"kicker": "秋茄子は嫁に食わすな", "title": "同じ一言が、逆に読めます",
                   "left": {"label": "憎らしい嫁に", "mark": "x", "verdict": "いじわる"},
                   "right": {"label": "体を冷やすから", "mark": "o", "verdict": "気づかい"},
                   "note": "逆の読み方は、1783年ごろの安斎随筆にあります"},
       "autumn_eggplants_in_basket"),
}

# ══ SHOT LIST — mot phong su, khong phai anh minh hoa roi ════════════════════
# NEO: "my row" (coc tre, dat nau do) · "next row" · "straw hat" · "shears" · "spade"
ROW = ("a row of staked eggplant plants in a small home vegetable garden, bamboo stakes, "
       "dark reddish-brown soil, a low concrete block wall behind")

SUBJ = {
 # ── HOI I · cuoi thang 7 ──────────────────────────────────────────────────
 # 🔴 entry 0 = ANH CHU THE (media-library §2.0 + §2.10⑦) va nam trong MACRO_LINES
 #    => TUYET DOI khong ghep {ROW} vao day: STYLE_MACRO da noi "NO wall, NO sky",
 #    ghep vao thanh prompt tu mau thuan (da dinh o ban dau: "...wall behind blurred behind")
 0:  "a small dull eggplant fruit hanging on its stem, skin gone matte and rough with dry ridges",
 2:  f"{ROW}, late July morning haze, the plants visibly tired and sparse",
 3:  "a single eggplant flower seen face on, pale purple petals, held gently between two fingertips",
 4:  "extreme close up into the centre of an eggplant flower, a ring of yellow anthers around one thin pale style",
 5:  "a fallen eggplant flower lying on dry soil, petals already browning",
 6:  "a pair of green-handled pruning shears held open beside a thick eggplant stem",
 7:  "an eggplant plant cut back to bare stubs, cut ends pale, soil below littered with leaves",
 8:  "a garden spade standing upright in soil, blade half buried, evening light",
 9:  f"{ROW} at dusk, wide and quiet, nobody present",
 12: "an empty planting hole in the soil where a plant was pulled out, roots torn, bamboo stake fallen beside it",
 13: "several fallen eggplant flowers scattered on soil, no fruit anywhere on the plant above",
 14: "two neighbouring garden rows side by side, the left one untouched and tired, the right one already cut back",
 15: "a straw hat seen from behind and above, a gloved hand raised to wipe the brow, blurred garden row beyond",
 16: "gloved hands closing pruning shears on a branch that still carries a purple eggplant",
 17: "a cut branch with a purple eggplant still attached, lying on the soil where it fell",
 18: f"a row of eggplant plants cut back to bare sticks, {ROW}, harsh midday light",
 19: "several glossy deep purple eggplants hanging heavy on a leafy plant, late September light, rich and abundant",
 20: "an empty planting hole with a fallen bamboo stake, weeds starting, no plant at all",
 21: "a hand-written date tag tied to a bamboo stake in a garden",
 22: "pruning shears lying closed on bare soil, unused",
 # ── HOI II · quay lai thang 7, lan nay lam dung ───────────────────────────
 24: "a wooden garden board with a calendar pinned to it, hanging on a shed wall",
 25: "fingertips lifting a single eggplant leaf to look underneath",
 27: "the thick woody base of an eggplant stem, bark split and grey with the season",
 28: "a small hard eggplant held in a palm, surface dull and dry",
 29: "three small eggplants of different quality lined up on soil",
 30: "one eggplant flower isolated against dark foliage, sharply lit",
 31: "extreme macro of eggplant flower anthers, yellow pollen grains visible",
 32: "an eggplant flower with a long style clearly protruding past the yellow anthers",
 34: "a flower dropping from the stem, caught mid-fall against dark leaves",
 35: "a hand holding two eggplant leaves side by side, one pale, one dark",
 36: "a whole eggplant plant with pale yellow-green leaves, nitrogen starved look",
 38: "a healthy dark green eggplant leaf, macro, veins sharp",
 39: "fingertips pinching the soft growing tip of an eggplant shoot",
 40: "the thin weak tip of an eggplant branch, leaves no bigger than a fingernail",
 41: "a gardener's gloved hand hesitating, shears held but not closed",
 42: "pruning shears resting on an upturned bucket beside the row",
 43: "green-handled pruning shears opened wide, ready, close up",
 44: "shears cutting cleanly through a thick eggplant main stem, sap visible",
 46: "an eggplant plant reduced to three bare stubs standing in soil",
 47: "a branch bearing one purple eggplant being cut away, the fruit still glossy",
 48: "a cut purple eggplant lying on the ground beside the plant",
 49: "a purple eggplant on the plant with the branch behind it thin and drained",
 51: "a tiny new bud swelling on a bare cut stem, macro",
 52: "a cut stem end with one small leaf and a bud left just below the cut",
 53: "a slanted cut on a thick stem, rainwater beading and running off",
 54: "small harvested eggplants collected in a shallow bamboo basket",
 56: "a red circle drawn around a week on a paper wall calendar",
 57: "bare cut stems standing in dry soil, nothing added yet",
 59: "a scoop of granular fertiliser being poured from a bag",
 60: "fertiliser granules scattered in a ring on soil around a cut plant",
 61: "two fertiliser bags standing side by side on a shed floor",
 63: "a watering can tilted over dry soil, first water darkening the surface",
 64: "waterlogged dark soil with standing water at the base of a plant",
 66: "bare soil baking in strong summer sun, surface cracked and pale",
 67: "cut grass and old newspaper spread as mulch around a plant base",
 68: "a gardening book open on a wooden bench outdoors",
 69: "two cut-back plants side by side, one sprouting and one still bare, a straw hat resting on the stake of the sprouting one",
 70: "a gloved hand scattering a second round of fertiliser, doubtful",
 71: "an unchanged bare stump after weeks, no buds at all",
 72: "fertiliser granules sitting undissolved on the soil surface",
 73: "a garden spade carried over a shoulder, silhouette against sky",
 74: "an old garden spade leaning inside a dim wooden shed",
 75: "soil dug open to reveal thick woody eggplant roots",
 76: "a thick old root, bark-like and hard, held in a hand",
 78: "a spade blade poised vertically above soil, about to be driven in",
 79: "dark rain clouds gathering over a vegetable garden",
 81: "a spade driven vertically into soil, boot pressing on the step",
 82: "a cleanly severed root end in freshly cut soil",
 83: "soil pulled back showing pale root ends in the dark earth",
 85: "many fine white new roots branching out through soil, macro",
 86: "the base of a plant with the spade held a measured distance away",
 87: "several spade slits made around a plant with gaps between them",
 88: "a thermometer in the garden reading high, midday heat",
 89: "early morning garden, long shadows, cool light",
 90: "wind bending young shoots before a storm",
 91: "an eggplant leaf covered in dark spots, diseased",
 93: "a full watering can emptied at the base of a cut plant",
 94: "a paper calendar page for September on a shed wall",
 96: "a small new shoot with two leaves on a formerly bare stump",
 97: "a hand marking a date on a wall calendar with a pencil",
 98: "one glossy purple eggplant hanging on a regrown plant, early autumn",
 99: "a bare stump photographed the same way for many days, unchanged",
 101: "a hand gripping a bare stump as if about to pull it out, hesitating",
 102: "soil cut away in cross section showing new white roots below a bare stump",
 103: "green peppers and shishito plants growing beside eggplants",
 # ── HOI III · lich chay den thang 10 · cua hang · sach co · tuc ngu ───────
 104: "a home centre garden aisle, shelves of seedling trays and fertiliser bags",
 105: "rows of autumn seedling pots lined up for sale",
 106: "a shelf of fertiliser bags stacked high, no labels readable",
 108: "an empty patch of shelf where nothing is displayed",
 109: "a spade blade standing in soil beside a thriving regrown plant",
 110: "a gloved hand pressing a spade into soil at the base of a plant",
 111: "an old wooden farmhouse toolshed interior, hand tools hanging",
 113: "an old hand-written farming notebook, ink faded, pages worn",
 114: "a straw hat resting on a bamboo stake at the end of a garden row",
 115: "an old book closed on a wooden table, evening lamp light",
 116: "several deep purple autumn eggplants in a bamboo basket",
 117: "a very old Japanese book with a worn cover on dark wood",
 118: "two identical autumn eggplants placed apart on a table",
 120: "a single autumn eggplant on a plain plate, cut in half showing few seeds",
 121: "two eggplants side by side, one lit warmly, one lit coldly",
 122: "an old book left open, pages turning in a breeze",
 123: "a heap of glossy autumn eggplants, abundant and deep purple",
 124: "pruning shears lying beside a full basket of autumn eggplants",
 125: "an old proverb card and a pair of shears placed side by side",
 126: "a pair of worn shears alone on bare soil, evening light",
 127: "a plant that stayed bare, weeds around it, honest failure",
 128: "an empty planting hole beside a thriving regrown plant, direct comparison",
 129: "a bare hand closing pruning shears on a branch with fruit still on it",
 130: "a straw hat hanging on a bamboo stake, garden row behind, golden evening light",
 131: "a straw hat hanging alone on a bamboo stake at the end of a garden row, low golden evening light, the row behind it heavy with dark purple fruit",
 132: "one eggplant flower held up to the light, style clearly visible",
 133: "kitchen scraps and fallen leaves gathered in a corner of the garden",
 134: f"{ROW} at dusk in October, quiet and finished, one lantern glow beyond the wall",
}

# Anh cua THE VOX — bat buoc lay tu day (bay 2026-08-12: the vox rot vao dflt)
VOXSUBJ = {
 "wall_calendar_late_july": "a paper calendar page for late July pinned flat, one week area empty and plain, no characters legible",
 "eggplant_flower_face_on": "an eggplant flower seen straight on, yellow anther ring and central style filling the frame",
 "eggplant_leaf_two_tones": "two eggplant leaves held together, one pale yellow-green and one deep green",
 "three_tools_on_soil": "pruning shears, a folded cloth garden glove and a small fertiliser scoop laid in a row on bare dark soil, NO spade in view",
 "worn_eggplant_stem_base": "the woody base of an old eggplant stem, bark grey and split",
 "pruning_shears_on_thick_stem": "green-handled pruning shears closing on a thick eggplant main stem",
 "single_dull_eggplant_hanging": "one dull purple eggplant hanging from a thin drained branch",
 "bamboo_stake_with_date_tag": "a bamboo garden stake with a small blank paper tag tied to it, no characters written anywhere",
 "fertilizer_granules_in_palm": "granular fertiliser held in an open gloved palm, macro",
 "finger_pressed_into_dry_soil": "a bare finger pushed into dry garden soil up to the first knuckle",
 "old_thick_eggplant_root": "a thick woody old eggplant root pulled from soil, hard and bark-like",
 "spade_blade_in_soil_beside_plant": "a spade blade driven vertically into soil a measured distance from a plant base",
 "fine_white_roots_in_soil": "dozens of fine hair-thin white roots branching through dark soil, macro",
 "shears_and_spade_side_by_side": "pruning shears and a spade blade laid parallel on dark soil",
 "calendar_with_red_circle": "a paper calendar with one date circled in red pencil, no other marks",
 "bare_cut_eggplant_stump": "a single bare cut eggplant stump standing alone in soil",
 "garden_shears_and_spade_leaning": "the worn wooden grips of pruning shears and a spade lying side by side, polished by years of use, macro",
 "old_japanese_book_on_wood": "a very old thread-bound Japanese book lying closed on dark wood, no characters visible",
 "autumn_eggplants_in_basket": "glossy deep purple autumn eggplants piled in a bamboo basket, macro",
 "old_proverb_book_page": "an old thread-bound Japanese book opened to a worn page, paper fibres visible, no readable characters",
}

DEF = [(23, "a tired eggplant plant in a small home garden"),
       (43, "an eggplant flower and leaves, close up"),
       (59, "pruning shears and cut eggplant branches"),
       (73, "fertiliser, water and mulch at a plant base"),
       (94, "a garden spade and soil opened at a plant base"),
       (104, "a regrown eggplant plant with new purple fruit"),
       (115, "an old toolshed and a straw hat"),
       (999, "autumn eggplants and a pair of worn shears")]


def dflt(i):
    for lim, s in DEF:
        if i < lim:
            return s
    return DEF[-1][1]


# 🔴 BAI HOC 2026-08-16 — TACH TONG KHOI BOI CANH.
#   Ban dau tao nhet ca menh de continuity ("bamboo stakes, reddish-brown soil, concrete block
#   wall behind") vao STYLE goc => 39/54 prompt deu mang no. Tong rat dong nhat (tot) NHUNG
#   BOI CANH bi khoa cung (xau): slot nao can THOAT khoi vuon — loi di cua hang, ke hang, ban
#   go — model van keo ve vuon. Do dung bay `media-library.md` §2.11 (STYLE LOCK khoa framing),
#   chi doi chieu: video 19 dinh "phong dep + vat nho", day dinh "luong rau + vat nho".
#   15 slot MACRO khong dinh, vi STYLE_MACRO co cau "NO room, NO wall, NO sky" — do la co che.
#
#   ⇒ TONG (anh sang/palette/mood) va BOI CANH (vuon co coc tre) la HAI thu, phai tach:
#     STYLE_TONE  : chi tong. Dung cho moi slot KHONG phai canh vuon.
#     STYLE_SCENE : TONE + continuity. CHI dung cho slot that su la canh vuon rong.
STYLE_TONE = ("Photorealistic cinematic documentary still, soft natural daylight, warm neutral "
              "palette, muted colors, shallow depth of field, fine detail, calm quiet mood, "
              "16:9 horizontal, no text, no letters, no logos, no brand labels, no human faces, "
              "no watermark")

STYLE = (STYLE_TONE.replace("documentary still, ",
         "documentary still from a single continuous story set in one small Japanese home "
         "vegetable garden in late summer: bamboo stakes, dark reddish-brown soil, a low "
         "concrete block wall behind, "))

# Slot phai DUNG NGOAI khu vuon => dung STYLE_TONE, khong keo continuity vao.
# (bat dau tu ca hong slide_55: xin "loi di cua hang lam vuon" ma ra nguoi cuoc giua vuon)
OFF_GARDEN = {104, 105, 106, 108, 111, 113, 115, 117, 118, 122}

STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO wall, NO sky, NO tools in view unless named. Hard directional light, "
               "high micro-detail, muted warm palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

# Slot BUOC macro: chu the LA co che (hoa, re, vet cat, hat phan bon)
MACRO_LINES = {0, 3, 4, 5, 17, 27, 28, 30, 31, 32, 34, 38, 39, 40, 44, 47, 51, 52, 53,
               59, 60, 63, 66, 72, 75, 76, 82, 83, 85, 91, 96, 102, 120, 132}
MACRO_VOX = set(VOXSUBJ)

# ── chon cue: don >=58 ky/slide => ~4,0 doi hinh/phut (bang mat do video 19) ─
# 🔴 SKIP {17, 130}: HAI DONG GIONG HET NHAU ("いま切らんと、秋に困るとよ。") — day la
#    cau thoai lap lai CO CHU Y (mo o phut 2, dong o phut 19), nen KHONG the sua chu de
#    phan biet. Khong substring nao tach duoc hai dong y het nhau => cue dong LIEN TRUOC
#    (16 va 129) va de hinh GIU NGUYEN khi cau thoai vang len. Cat truoc cau thoai, khong
#    cat DUNG luc no vang — nghe cung hay hon.
# 58 = dong CTA canonical (~180 ky ≈ 35s). Khong ep cue o day thi hinh cua dong 57
# giu LIEN 41 GIAY. Ep cue => CTA co khung rieng, va chinh no la cho lop overlay CTA
# (cta_inject.py, cta-midvideo.md §5) chay hoat hoa => man hinh khong dung yen.
FORCE, SKIP = {16, 58, 129}, {17, 130}
CUE, acc = [], 0
for i, l in enumerate(L):
    if i in SKIP:
        acc += len(l)
        continue
    if i == 0 or i in VOX or i in FORCE or acc >= 58:
        CUE.append(i)
        acc = 0
    acc += len(l)


# 🔴 SAN 6 GIAY/ENTRY (audience-45plus.md §2 muc 2) — hau xu ly BAT BUOC.
#    Bay da dinh that: dong 25 「一つ目。読む。」 chi 6 ky, dung ngay truoc dong 26 la
#    the VOX bi ep cue => hai khung cach nhau 1 GIAY. Luat cue theo "don du 58 ky"
#    KHONG bat duoc ca nay vi cue VOX la cue ep, khong qua bo dem.
#    Xu: cue nao cach cue KE TIEP < 6s thi BO — uu tien giu cue VOX.
TOT = sum(len(x) for x in L)
CPS = TOT / DUR                      # ky/giay thuc te cua bai nay
MIN_CH = int(6 * CPS) + 1            # 6 giay quy ra ky tu

_pos, _a = {}, 0
for i, l in enumerate(L):
    _pos[i] = _a
    _a += len(l)

_keep = []
for k, i in enumerate(CUE):
    if k + 1 < len(CUE) and _pos[CUE[k + 1]] - _pos[i] < MIN_CH:
        # 🔴 i == 0 KHONG BAO GIO bi bo: entry 0 phai la ANH CHU THE
        #    (media-library §2.0 + §2.10⑦). Da dinh that 2026-08-16: bo cue 0 xong
        #    khung mo dau thanh THE CHU 10日 — che anh di la khong biet video noi gi.
        if i not in VOX and i != 0:
            continue
        # ca hai deu la VOX thi giu cai dau, bo cai sau o vong lap sau
    _keep.append(i)
CUE = _keep


def uniq_key(i):
    """16 ky dau phai DUY NHAT trong toan bo L. Dong 17 va 130 giong het nhau
    (「いま切らんと、秋に困るとよ。」) => phai noi dai hoac lay dong ke."""
    for n in (16, 24, 34, 48):
        m = L[i][:n]
        if sum(1 for x in L if m in x) == 1:
            return m
    return None


out, flow, names, bad = [], [], [], []
for i in CUE:
    m = uniq_key(i)
    if m is None:
        bad.append((i, L[i][:20]))
        continue
    if i in VOX:
        kind, spec, sub = VOX[i]
        v = {"kind": kind}
        v.update(spec)
        v["bg"] = "photo"
        v["photo"] = P(sub)
        v["photo_style"] = "darken"
        flow.append(f"{STYLE_MACRO}. {VOXSUBJ[sub]}")
        names.append(f"ai_clean/{sub}.jpeg")
        out.append({"match": m, "photo": False, "video": True, "vox": v})
    else:
        # 🔴 PHAI la CHI SO ENTRY, khong phai so thu tu anh.
        #    video_render.py va remotion-vox/tools/import_pipeline.py deu tim
        #    `slide_{i:02d}` voi i = chi so ENTRY (giong `clip_{i:02d}.mp4`).
        #    Dat theo so anh (0..53) => 16 entry cuoi khong tim thay file, importer
        #    bao "KHONG co anh/clip" (dinh that 2026-08-16). gen_slides19.py lam dung.
        idx = len(out)
        st = (STYLE_MACRO if i in MACRO_LINES
              else STYLE_TONE if i in OFF_GARDEN else STYLE)
        flow.append(f"{st}. {SUBJ.get(i) or dflt(i)}")
        names.append(f"slides_img/slide_{idx:02d}.jpg")
        out.append({"match": m, "photo": True})

S = PROJ / "03_SCRIPTS"
(S / f"{SLUG}_SLIDES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(S / f"{SLUG}_IMG_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S / f"{SLUG}_IMG_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

nv = [x["vox"]["kind"] for x in out if isinstance(x.get("vox"), dict)]
npho = sum(1 for x in out if x.get("photo") is True)
print(f"entry {len(out)} | anh thuong {npho} | vox {len(nv)} (100% co anh nen)")
print(f"doi hinh/phut {len(out)/(DUR/60):.1f}  (tran 6) | giay/entry {DUR/len(out):.1f} (san 6)")
print(f"prompt {len(flow)} dong | match TRUNG/THIEU: {bad if bad else '0 — tat ca duy nhat'}")
print("kinds:", ", ".join(sorted(set(nv))))
