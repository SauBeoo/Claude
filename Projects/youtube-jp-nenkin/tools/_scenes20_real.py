# -*- coding: utf-8 -*-
r"""_scenes20_real.py — OVERRIDE cho ban NGUOI THAT (photoreal) cua video 20.

User chot 2026-09-03 (dao lai sau ban anime): *"the cu de nguoi that di"*.

🔴 VI SAO PHAI CO FILE NAY, khong chi doi mot cau STYLE:
   **25/83 shot cua ban anime la SIEU THUC.** Voi anime do la ngon ngu dung
   (nha 2 tang phat sang, tang mot bien mat, hang bong giay xep hang, thanh
   bieu do tu ve). Voi NGUOI THAT thi no thanh quai di — vat the bay lo lung,
   nha tu tat den — dung cai lam video AI trong "sai sai".
   58 shot con lai von da TA THUC (mo phong bi, ngoi ban bep, quay sieu thi,
   quay 年金事務所) nen dung lai duoc; file nay chi ghi de 25 cai.
   ⓘ Cung bai hoc `_motion19_real.py` — chi lan nay nang hon 3x vi bai 20
   day AN DU HINH HOC (nha hai tang, thu tu, moc 20 nam).

📐 NGUYEN TAC CHUYEN: giu **NGHIA cua cau loi** va giu **HANG NANG LUONG**,
   doi cach thi hanh tu "phep la" sang "VAT THAT + may quay + dien xuat":
     nha 2 tang phat sang      -> **MO HINH KIEN TRUC go that** tren ban 研究員,
                                  co den LED trong tung tang, tang tren THAO ROI
     tang mot BIEN MAT         -> nhac khoi tang mot RA KHOI BAN, con lai vet bui
     hang bong giay xep hang   -> **standee bia cat tay** dung tren ban
     thanh bieu do tu ve       -> 研究員 **cam but ve len bang trang** treo sau ban
     cau thang so do tren troi -> cau thang **be tong that** o khu nha o
   Peak van la peak: cai manh nam o **hanh dong dut khoat + may day**, khong
   o phep la.

🔴 MOT LOI LOGIC DA SUA LUON, khong lien quan style (`sousai`):
   Ban anime dung **can hai dia**: bo them 2 xu ben trai VA nhac 2 xu ben phai
   => thuc te can se **do manh sang trai**, trong khi cau loi la 「合計は、
   変わりません」. An du SAI VE VAT LY. Thay bang **can dien tu mot khay**:
   chuyen xu tu chong nay sang chong kia tren cung mot khay, **so tren can
   khong doi**. Vua dung vat ly vua CHUNG MINH duoc cau loi — va chu SO tren
   can thi AI gen on dinh (`media-library.md` §2.9: chi kanji moi nat net).

⚠️ COMPLIANCE (`youtube-compliance.md` §2.1): canh AI **realistic** trong video
   => phai TICK "altered/synthetic content" luc upload. Day la cai GIA cua viec
   quay lai nguoi that — ban anime khong phai tick. Nhan vat phai HU CAU; cam
   mat nguoi that cu the, cam dan dung su kien/dia diem co that.
"""

# ══════════════════════════════════════════════════════════════════════════
# PROP moi / ghi de — deu la VAT CO THAT, cam duoc, quay duoc
# ══════════════════════════════════════════════════════════════════════════
PROP_OVERRIDE = {
    # ⭐ vat trung tam cua ca bai — thay cho "nha 2 tang ve kieu so do"
    "P_MODEL": ("the SAME model every time: a hand-built wooden architectural "
                "scale model of a two-storey Japanese house about 40cm tall "
                "standing on the study desk — a wide solid ground-floor block "
                "with small paper shoji windows, and a smaller upper-floor block "
                "with a grey tiled roof that is a SEPARATE removable piece; a "
                "warm LED is fitted inside each floor so either floor can be lit "
                "on its own"),
    "P_STANDEE": ("the SAME set every time: six small hand-cut card standees of "
                  "family figures on little wooden bases — warm cream card, "
                  "visibly cut by hand with scissors, each a slightly different "
                  "height — standing in a row on the pale desk"),
    "P_BOARD": ("the SAME board every time: a small white magnetic whiteboard on "
                "the study wall behind the desk with a thin black horizontal "
                "guide line already drawn across it, and a fat orange marker and "
                "a red marker resting in the tray beneath"),
    # ghi de: can hai dia -> can dien tu mot khay (xem docstring)
    "P_SCALE": ("the SAME scale every time: a small white digital kitchen scale "
                "with a flat square tray, its little display facing the camera "
                "and showing a clear three-digit number"),
    # 🔴 anh tho xuat hien o 3 shot (awaseta / hikitsugarenai / kekka_kawaru).
    #    Ban anime khong khoa mat ong chong o day => 3 shot ra 3 nguoi khac nhau,
    #    va shot `taishou` (hoi tuong) lai la nguoi thu tu. Ta mat ong ay NGAY
    #    TRONG prop, trung khop voi CAST M1 cua `_scenes20.py`.
    # ⚠️ Ta THANG bang tu trung tinh — dung de POLICY_SWAP phai doi ho, vi hai
    #    swap chong nhau da tung de lai "dark-wood dark-wood display shelf".
    # 🔴 KHONG ta nguoi trong khung anh. Khung dat NGHIENG so voi may nen chi
    #    thay canh khung va mot goc kinh loa sang — du hieu "anh cua ai do" ma
    #    khong bat model ve mot khuon mat. Doan ta mat M1 da bi go han khoi day.
    "P_BUTSU": ("the SAME quiet corner every time: a small dark-wood display "
                "shelf holding a plain wooden picture frame that stands turned "
                "well away from the camera, so only its back, its edge and a "
                "glancing highlight on the glass are visible, beside a single "
                "white flower in a slim vase"),
    # (a) ky vat — dung thay khung anh o nhung canh can noi "cua ong ay"
    "P_KATAMI": ("the SAME keepsakes every time: a man's folded reading glasses "
                 "with thin metal rims and a worn leather-strapped wristwatch, "
                 "lying together on a small cloth"),
    # phaperwork noi chung — ban photoreal KHONG duoc de giay trang tinh
    "P_TSUCHI": ("the SAME notice every time: a single pale-cream A4 official "
                 "letter folded once, carrying real printed structure — ruled "
                 "rows, boxed fields and column dividers — but photographed so "
                 "the wording is too small and too softly focused to read"),
    "P_FURI": ("the SAME notification every time: a wide pale-cream pension "
               "transfer slip with a ruled table of small printed figures and one "
               "pale blue column band down the left side, seen at an angle so the "
               "wording does not resolve"),
}

# ══════════════════════════════════════════════════════════════════════════
# DOC_FOCUS — shot ma TO GIAY LA CHU THE, hoac hanh dong chinh la DOC / CHI VAO.
# Bai hoc video 19 (user: *"nhin tay chi vao nhung cai text trang nhin no dieu
# qua"*): luat "chu mo khong doc duoc" cuu duoc anh NEN, nhung o nhung shot NAY
# thi nguoi xem thay ong ta chi vao **cho trong**.
# Cach phim tai lieu that giai: giu CAU TRUC + DAU DANH DAU, va cho **CHU SO
# A-rap doc duoc** (chu so AI gen on dinh, chi kanji moi nat net).
# ══════════════════════════════════════════════════════════════════════════
DOC_FOCUS = {
    "hiraku", "meutagau", "hazu", "naze", "furikomi", "jibun_kiso", "chigau_b",
    "kenkyu_b", "happyakugojuu", "mikomi", "kafu_kasan", "teikibin", "riyuu",
    "shirazu", "fuyo", "kaisei",
}

# ══════════════════════════════════════════════════════════════════════════
# SHOT_OVERRIDE — 25 shot dung lai canh cho photoreal.
# Khoa nao khong ghi thi giu nguyen tu `_scenes20.py`.
# ══════════════════════════════════════════════════════════════════════════
SHOT_OVERRIDE = {

# ── an du NHA HAI TANG -> MO HINH KIEN TRUC tren ban 研究員 ─────────────────
"nanno": dict(props=["P_MODEL", "P_DESK"], cam="push", lv="mid",
    # L10 この四分の三は、いったい、何の四分の三なのでしょうか。
    sc="an overhead shot of the study desk: the wooden model house stands in the "
       "middle with both floors unlit, and two identical plain kraft envelopes "
       "have been laid on the desk beside it — one level with the ground floor, "
       "one level with the upper floor; an elderly man's hand hovers above them, "
       "not yet choosing",
    mo="the hovering hand moves slowly over the envelope by the upper floor, "
       "hesitates without touching it, drifts across to the one by the ground "
       "floor and stops there, still not touching either"),

"nikaidate": dict(props=["P_MODEL", "P_DESK"], cam="pull_out", lv="mid",
    # L14 日本の年金は、二階建てだと言われます。
    sc="the wooden two-storey model house standing alone in the middle of the "
       "study desk under the window, both of its interior LEDs glowing warm, the "
       "rest of the desk cleared and the wall behind it plain, soft daylight",
    mo="the camera eases back to take in the whole desk and settles; the warm "
       "glow inside both floors of the model comes up evenly and holds; a thin "
       "curl of dust turns slowly in the window light"),

"ikkai": dict(props=["P_MODEL", "P_COIN", "P_DESK"], cam="static", lv="mid",
    # L15 一階が、老齢基礎年金。二十歳から六十歳まで納めた期間で決まる部分です。
    sc="a close shot of the model house on the desk with only the GROUND floor's "
       "LED lit, the upper floor dark, and a long even line of brass coins laid "
       "out one by one along the desk in front of it like a paid-in record",
    mo="a hand sets three more coins onto the end of the line one after another, "
       "each with a small definite tap, then withdraws; the ground floor stays "
       "lit and the upper floor stays dark"),

"nikai": dict(props=["P_MODEL", "P_COIN", "P_DESK"], cam="static", lv="mid",
    # L16 二階が、老齢厚生年金。給料に応じて上乗せされる部分。
    sc="a close shot of the same model with only the UPPER floor's LED lit and "
       "the ground floor dark, and a small stack of brass coins resting on the "
       "narrow balcony ledge of the upper floor",
    mo="two more coins are placed gently on top of the balcony stack and the "
       "stack settles under them; the upper floor stays lit and the ground floor "
       "stays dark"),

"awaseta": dict(cast=None, hands="M3", props=["P_MODEL", "P_KATAMI", "P_DESK"],
    cam="parallax", lv="calm",
    # L17 ご主人が受け取っていた年金は、この一階と二階を足したものでした。
    # (ban anime cho M1 DUNG TRUOC nha — o photoreal la sai ti le; doi sang
    #  anh tho dat canh mo hinh, van giu duoc "day la cua ong ay")
    sc="the model house on the study desk with BOTH floors lit warm, and lying "
       "on the desk beside it a man's folded reading glasses and a worn "
       "leather-strapped wristwatch resting together on a small cloth, an "
       "elderly man's hands just withdrawing from them, soft afternoon light",
    mo="He switches both floors on so the whole house glows, then sets the "
       "folded glasses and the wristwatch down side by side on the cloth beside "
       "it, squares them with a fingertip, and draws his hands back to rest on "
       "the desk."),

"dochira": dict(hands="W1", props=["P_MODEL", "P_DESK"], cam="push", lv="mid",
    # L18 遺族厚生年金として四分の三になるのは、どちらでしょうか。
    sc="a close shot of the model house on the desk with both LEDs now off, and "
       "an elderly woman's hand entering from the side and hovering uncertainly "
       "in the gap between the ground-floor block and the upper-floor block, not "
       "touching either",
    mo="the hovering hand drifts up level with the upper floor, hesitates, drifts "
       "back down level with the ground floor and stops in between, still not "
       "touching; the model stays dark"),

"nikai_dake": dict(hands="M3", props=["P_MODEL", "P_DESK"], cam="push_hard", lv="peak",
    # L21 報酬比例部分。つまり、二階だけです。
    sc="the upper-floor block of the model has been LIFTED clear off the house "
       "and is held steadily in an elderly man's hands a short way above it, its "
       "LED still lit and its trailing wire visible; the ground-floor block left "
       "below on the desk is dark",
    mo="the hands raise the lit upper block a few more centimetres clear of the "
       "house in one smooth movement and hold it there absolutely steady; the "
       "dark ground-floor block below does not move at all"),

"ikkai_hairanai": dict(props=["P_MODEL", "P_DESK"], cam="static", lv="mid",
    # L22 一階の老齢基礎年金は、この計算に、入っていません。
    sc="the lit upper-floor block now set down on its own at the top of the desk, "
       "and the dark ground-floor block left where the house stood with a plain "
       "grey card laid flat across its roof line, closing it off",
    mo="a hand lays the grey card down across the dark ground-floor block, "
       "squares it with two fingertips and withdraws; the lit upper block at the "
       "top of the desk is untouched"),

"gokai_shin": dict(cast="M3", props=["P_MODEL", "P_DESK"], cam="static", lv="mid",
    # L23 ご主人の一階部分は、四分の三になるのではありません。
    sc="the researcher in the charcoal cardigan seated at his desk beside the "
       "separated model, one hand open and level toward the dark ground-floor "
       "block, his expression serious and unhurried as he explains",
    mo="his open hand travels slowly down through the air to indicate the dark "
       "ground-floor block and comes to rest flat on the desk beside it; he gives "
       "one small nod; the model does not move"),

"zero": dict(hands="M3", props=["P_MODEL", "P_DESK"], cam="push_hard", lv="peak",
    # L24 ゼロになります。
    sc="the ground-floor block is GONE from the desk entirely — the lit upper "
       "block sits alone on the bare wooden desktop, and where the lower block "
       "stood there is nothing but a clean rectangle of undisturbed desk marked "
       "out by a fine ring of dust, hard cold light from the side",
    mo="a pair of hands carries the ground-floor block steadily out of frame and "
       "does not come back; the upper block is left standing alone and the empty "
       "dust-marked rectangle beside it stays bare; nothing else moves"),

"izoku_kiso": dict(props=["P_MODEL", "P_STANDEE", "P_DESK"], cam="push", lv="mid",
    # L43 お子さんがいらっしゃる配偶者か、お子さんご本人だけが対象になります。
    sc="the ground-floor block is back on the desk on its own with its LED lit "
       "warm again, the upper block absent, and two of the small hand-cut child "
       "standees have been stood in its doorway",
    mo="a hand sets the second small child standee down beside the first in the "
       "lit doorway and steadies it with a fingertip until it stops rocking, then "
       "withdraws; the empty space above the block stays bare"),

"izoku_kiso_b": dict(hands="K1", props=["P_STANDEE", "P_COIN", "P_DESK"],
    cam="static", lv="mid",
    # L43後半 令和八年度で、年に八十四万七千三百円。
    sc="a close shot on the pale desk of a young mother's hands setting one neat "
       "stack of brass coins down in front of the two small hand-cut child "
       "standees, the cut edges of the card catching the light",
    mo="the hands lower the coin stack the last centimetre onto the desk in front "
       "of the two standees and release it; the stack settles square and the two "
       "card figures rock once on their bases and go still"),

# ── an du THU TU -> standee bia cat tay ────────────────────────────────────
"junban": dict(props=["P_STANDEE", "P_DESK"], cam="pull_out", lv="mid",
    # L50 お子さんのいる配偶者が最初。次に、お子さん。…父母、孫、祖父母
    sc="a low shot along the pale desk: all six hand-cut card standees stand in a "
       "single-file row from front to back, the nearest a taller adult figure "
       "holding a small child figure's hand, the ones behind steadily smaller, "
       "each on its own little wooden base",
    mo="the camera eases back along the row so the whole queue comes into frame; "
       "the standees stay exactly where they are and only the light along the "
       "desk shifts, picking out one base after another"),

"junban_b": dict(props=["P_STANDEE", "P_DESK"], cam="push", lv="mid",
    # L50後半 お子さんのいる配偶者が最初。次に、お子さん。
    sc="a close shot of the front of the same row: the parent-and-child standee "
       "stands on a small pencilled cross marked on the desk, brightly side-lit, "
       "with the lone child standee waiting one base-length behind it and the "
       "rest of the row falling away out of focus",
    mo="a fingertip nudges the parent-and-child standee the last centimetre onto "
       "the pencilled cross and lifts away; the standee rocks once and settles "
       "square on the mark"),

"saki_no_juni": dict(props=["P_STANDEE", "P_ENV", "P_DESK"], cam="static", lv="mid",
    # L51 先の順位のかたがいらっしゃると、あとの順位のかたには回りません。
    sc="the same row of six standees on the desk with one plain white envelope "
       "leaning against the front figure's base, and nothing at all in front of "
       "any of the five behind it; the front of the row is lit and the rest falls "
       "into shadow",
    mo="a hand slides the envelope firmly up against the front standee's base and "
       "lets go, then withdraws past the five figures behind without leaving "
       "anything; none of them move"),

# ── an du BIEU DO -> 研究員 ve len bang trang ──────────────────────────────
"yonjuu_rokujuugo": dict(cast="M3", props=["P_BOARD"], cam="static", lv="mid",
    # L59 四十歳以上六十五歳未満で、お子さんがいらっしゃらないかた
    sc="the researcher standing at the small whiteboard on his study wall drawing "
       "a thick orange bar along the black guide line, starting at one short "
       "vertical tick mark and heading toward a second tick further along, his "
       "back three-quarters to the camera",
    mo="he draws the orange bar steadily from the first tick along the guide line "
       "and stops the marker cleanly at the second tick, then lifts it away and "
       "lowers his arm"),

"keikateki": dict(cast="M3", props=["P_BOARD"], cam="static", lv="calm",
    # L63 経過的寡婦加算という形で一部が続くこともありますが、額は下がります。
    sc="a closer view of the same whiteboard: the thick orange bar ends at the "
       "second tick, and the researcher is holding the marker on its thin edge "
       "just past that tick, about to continue with a much narrower line",
    mo="he draws a thin narrow line onward from the tick with the edge of the "
       "marker, carries it a short way and stops; the thick bar before the tick "
       "is not touched"),

"nijuunen": dict(cast="M3", props=["P_BOARD"], cam="push_hard", lv="peak",
    # L65–L66 加入期間が二十年以上あったかどうかで／二十年に足りないと、つきません。
    sc="the whiteboard now carries a single bold RED vertical line, and two "
       "orange bars have been drawn one above the other running toward it — the "
       "upper bar already crosses past the red line, the lower one stops well "
       "short of it; the researcher's hand rests at the end of the lower bar",
    mo="he draws the lower orange bar the last stretch and stops the marker "
       "abruptly a clear hand's width short of the red line, then takes the "
       "marker away and leaves the gap open; the red line is untouched"),

"eikyou_nashi": dict(cast="M3", props=["P_BOARD"], cam="pull_out", lv="mid",
    # L88 いま受け取っていらっしゃるかたは、影響を受けません。
    sc="the researcher at the whiteboard where a row of three simple figures has "
       "been drawn in black on a solid horizontal base line, and he is completing "
       "a wide calm orange arc drawn over the top of them like a roof",
    mo="he carries the orange marker through the last of the wide arc above the "
       "figures and closes it onto the base line, then lowers the marker and "
       "steps half a pace back from the board"),

"korekara": dict(cast="M3", props=["P_BOARD"], cam="static", lv="mid",
    # L89 六十歳を過ぎて権利が発生するかたも、これまでどおりです。…変わりません。
    sc="the same whiteboard: under the finished orange arc the researcher is "
       "adding two more simple black figures onto the same base line beside the "
       "first three, so that all five now stand under one roof",
    mo="he draws the second added figure with two short strokes, caps the marker "
       "with one hand and rests it in the tray; the arc above is not redrawn"),

"mikomi": dict(hands="W1", props=["P_DESK"], cam="static", lv="mid",
    # L49 八百五十万円を超えていても、数年のうちに下回る見込みがあるかたは、対象になる場合があります。
    sc="a close overhead desk shot: a printed income sheet with ruled rows lies "
       "flat, a pale wooden ruler is laid straight across it as a threshold, and "
       "a pencil has already dotted a descending stepped line down the page from "
       "the upper left toward the ruler",
    mo="the pencil adds two more dots continuing the descending line and places "
       "the last one clearly BELOW the ruler's edge near the right of the page, "
       "then lifts away; the ruler is not moved"),

# ── an du CAU THANG -> cau thang be tong that ─────────────────────────────
"dansa": dict(cast="W1", props=["P_STAIR"], cam="pull_out", lv="mid",
    # L53 もうひとつの話をします。六十五歳の段差です。
    sc="a real outdoor concrete staircase between two levels of a Japanese "
       "housing estate, pale rendered walls either side and open sky above: the "
       "flight climbs steadily and ends on a small landing which then has ONE "
       "step DOWN onto a lower terrace; the 66-year-old woman stands on the "
       "landing at the edge of that step, looking down at it",
    mo="the camera eases back to take in the whole climb and the one step down; "
       "she shifts her weight back half a pace from the edge and holds; the hem "
       "of her cardigan lifts once in the open air"),

"dansa_b": dict(cast="W1", props=["P_STAIR"], cam="push", lv="mid",
    # L54 佐藤さんは、六十五歳になった年に、年金が減りました。
    sc="the same staircase from below: the woman is now standing on the lower "
       "terrace one level down, turned back to look up at the landing she came "
       "from, the long flight of steps rising away behind it into the pale sky",
    mo="she looks back and up at the landing and her hand comes halfway toward "
       "the wall beside her, then lowers again without touching it; her shoulders "
       "settle"),

"kekka_kawaru": dict(props=["P_KATAMI", "P_COIN", "P_DESK"], cam="static", lv="mid",
    # L66後半 同じように四十代で夫を亡くされても、勤め先での年数で、結果が変わってしまう。
    sc="two identical sets of keepsakes laid out side by side on the desk — each "
       "a pair of folded reading glasses and a worn wristwatch on its own small "
       "cloth — with a full stack of brass coins in front of the left set and "
       "nothing at all in front of the right one, one even light across both",
    mo="the light travels slowly across both sets and steadies; the coin stack "
       "in front of the left set stays exactly as it is and nothing is placed "
       "in front of the right one"),

# ── 🔴 SUA LOI VAT LY: can hai dia -> can dien tu mot khay ────────────────
"sousai": dict(hands="W1", props=["P_SCALE", "P_COIN"], cam="push", lv="peak",
    # L82 働いて増やしたはずの分が、そっくり相殺される。
    sc="a close shot of a small white digital kitchen scale on a pale table, its "
       "display facing the camera and showing a clear number, with two separate "
       "stacks of brass coins standing side by side on its single flat tray — the "
       "left stack short, the right stack tall",
    mo="a hand lifts two coins off the tall right-hand stack and sets them on top "
       "of the short left-hand one, so the left grows and the right shrinks — and "
       "the number on the scale's display does not change by a single digit "
       "through the whole move"),
}


# ══════════════════════════════════════════════════════════════════════════
# 🔴 LOP CHONG VI PHAM CHINH SACH (user bao 2026-09-03: *"Dang thay vi pham
#    chinh sach do"* — sau khi doi tu anime sang NGUOI THAT).
#
# Quet 83 prompt ra 4 nhom rui ro, KHONG phai mot:
#   A. TRE EM photoreal      — 11 shot. Anime ve tre em thi khong sao; anh THAT
#      thi hau het generator chan cung. **Day la nhom moi sinh ra do doi style.**
#   B. GIAY TO CHINH THUC    — 49 shot (official 47x · government 30x · stamp
#      22x). Bo loc chong LAM GIA GIAY TO/CON DAU. Nhom to nhat.
#   C. NHAN DANG / SAME FACE — 45 shot ("identical face", "the SAME PERSON as
#      the reference image"). Doc ra nhu doi **nhan ban khuon mat mot nguoi**.
#   D. TANG LE               — 3 shot (memorial / altar / late husband).
#
# ⚖️ Sua C con LAM DUNG THEM luat cua minh: `youtube-compliance.md` §2.1 doi
#    nhan vat phai HU CAU. Ban cu chi noi "same person", khong he noi "fictional"
#    — tuc la vua rui ro filter, vua khong chung minh duoc tuan thu.
# ══════════════════════════════════════════════════════════════════════════

# Doi CHU, giu NGHIA. Cum DAI phai dung TRUOC cum ngan (thu tu co y nghia).
POLICY_SWAP = [
    # ── B. giay to / con dau / co quan ────────────────────────────────────
    (r"a faint official stamp",            "a faint printed reference mark"),
    (r"boxed fields and stamps",           "boxed fields and reference marks"),
    (r"plain government leaflets",         "plain printed information booklets"),
    (r"government leaflets",               "printed information booklets"),
    (r"a plain government leaflet",        "a plain printed information booklet"),
    (r"plain bound booklet of statutes",   "plain bound reference booklet"),
    (r"official declaration form",         "printed form"),
    (r"official-looking",                  "formal-looking"),
    (r"official web page",                 "reference web page"),
    (r"pension transfer notification",     "payment statement slip"),
    (r"pension transfer slip",             "payment statement slip"),
    (r"pension statement leaflet",         "printed statement leaflet"),
    (r"pension office",                    "public service office"),
    (r"official notice",                   "printed notice letter"),
    # 🔴 bien the phai dung TRUOC `\bofficial\b`, neu khong se ra
    #    "a plain white PLAIN window envelope" (tinh tu chong tinh tu).
    (r"white official window envelope",    "white window envelope"),
    (r"official window envelope",          "window envelope"),
    (r"official envelope",                 "window envelope"),
    (r"\bofficial\b",                      "plain"),      # con lai: bo tinh tu
    (r"\bgovernment\b",                    "public-information"),
    (r"a single plain government leaflet",  "a single plain printed booklet"),
    (r"dark-wood memorial shelf",           "dark-wood remembrance shelf"),
    (r"after the graduation",               "after the ceremony"),
    (r"a small child figure's hand",        "a smaller figure's hand"),
    # ── D. tang le ────────────────────────────────────────────────────────
    (r"memorial corner",                   "quiet remembrance corner"),
    (r"family altar shelf",                "dark-wood display shelf"),
    (r"altar shelf",                       "display shelf"),
    (r"the late husband",                  "her husband"),
    (r"\bmemorial\b",                      "remembrance"),
]

# ── A. TRE EM — 2 shot phai BO HAN nguoi duoi 18 khoi khung ───────────────
# ⚠️ Khong "lam mo mat tre" hay "quay tu xa" — van la depict minor. Cach duy
#    nhat sach: ke su co mat cua chung bang DO DAC, khong cho chung vao khung.
#    Cai nay KHONG lam yeu canh — bat com trong, doi giay nho o cua, buc tranh
#    sap mau tren tuong ke duoc dung cau chuyen do ma con dat hon.
SHOT_OVERRIDE_MINORS = {

"kodomo": dict(cast="K1", props=[], cam="parallax", lv="calm",
    # L41 お子さんが小さいうちに、ご主人を亡くされたかた。/ L42 遺族基礎年金です。
    sc="a Japanese mother in her late thirties sitting alone at a low table in a "
       "modest living room in the evening, three places set but only hers used — "
       "two small empty rice bowls and two pairs of short chopsticks wait across "
       "from her; crayon drawings are taped to the wall behind and a man's "
       "folded reading glasses rest on the shelf beside a small clock; warm lamp "
       "light, NOBODY ELSE IS IN THE FRAME",
    mo="she reaches across and straightens the two small bowls so they sit square, "
       "then draws her hands back into her lap and looks at the empty places; the "
       "lamp light is steady"),

"sotsugyou": dict(cast="K1", props=[], cam="parallax", lv="calm",
    # L46 お子さんが高校を卒業される年の春に、この一階部分は終わります。家計が変わる。
    sc="a spring morning outside a Japanese school gate under cherry blossom, the "
       "ceremony over and the gateway empty; the mother in her late thirties "
       "stands alone just inside the gate holding a rolled certificate tube "
       "against her chest, looking off down the road, proud and a little "
       "uncertain, petals in the air, NOBODY ELSE IS IN THE FRAME",
    mo="she lowers the certificate tube from her chest and holds it in both hands "
       "in front of her, then lifts her eyes to follow something down the road; "
       "cherry petals drift slowly across the frame"),
}

# CAST K1 phai bo hai dua tre khoi phan mo ta — neu khong thi moi prompt co K1
# van keo tre em vao khung qua duong CAST LOCK.
CAST_OVERRIDE = {
    "K1": {"who": "遺族基礎年金 doan — nguoi me (con cai KHONG vao khung)", "lock": (
        "a Japanese mother in her late thirties with shoulder-length dark hair, "
        "tired gentle eyes and a plain knitted jumper over a cotton blouse")},
}

# ── A phu: doi chu o may shot con lai co dinh tu tre em nhung KHONG co nguoi
#    that (standee bia, hinh ve tren bang trang, ao treo mac ao) ────────────
POLICY_SWAP += [
    (r"child-sized paper silhouette figures", "small card cut-out figures"),
    (r"small hand-cut child standees",   "small hand-cut card standees"),
    # ⚠️ KHONG viet "small card standee" — nguon da co "the second small child
    #    standee" => se ra "small small card standee" (gate TU LAP bat duoc).
    (r"child standee",                   "card standee"),
    (r"the lone child standee",          "the lone small standee"),
    (r"a parent holding a child's hand", "a taller figure holding a smaller one's hand"),
    (r"the parent-and-child standee",    "the paired standee"),
    (r"a young parent with two small children",
                                         "a small family group"),
    (r"an older woman, an older man, a parent with two small children",
                                         "an older woman, an older man and a small family group"),
    (r"navy Japanese high-school blazer", "navy school-style blazer"),
    (r"a navy Japanese high-school blazer on a hanger",
                                         "a navy school-style blazer on a hanger"),
    (r"her son's certificate tube",      "a rolled certificate tube"),
    (r"the now grown son",               "a young adult"),
]
