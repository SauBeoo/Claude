# -*- coding: utf-8 -*-
"""Video 15 — 昭和の母のお金 (5 muc). Cong thuc duy nhat v2.

⛔ KHONG chep hang so. STYLE / MOTION / AVOID / FRAMING / EXTRAS deu lay tu videogen_lib.

HAI THU KHAC VIDEO 14:
 1. ⭐ **MOT doi mat duy nhat: A_HAHA** (nguoi me). Video 14 la A_OJI (nam, cong so);
    bai nay ca kich ban la "ban tay do lam gi voi tien" nen POV qua chinh nguoi me la
    cach re nhat de giu "nhan vat dong nhat": chi phai giu MOT than nguoi (tay ao
    kappougi trang, nguc ao) xuyen ~150 clip, thay vi 5-6 dien vien phai khop nhau.
 2. ⭐ **HIEN VAT XUYEN BAI: cuon so 家計簿.** Kich ban v2 dung no lam xuong song
    (`03_SCRIPTS/15_haha-no-okane.md` §7.2) => lop hinh phai co mot MOTIF LAT SO
    tro lai o moi khoi. Preset `ima_ie` = tay nguoi chung nhan (A_IMA, 70 tuoi) dang
    lat chinh cuon so do o thoi NAY — no la cai neo giua 5 muc.

🔴 BA RUI RO — biet truoc, khong phat hien lai:
 a. POV la loai shot t2v hong nhieu nhat (`hands only` an 14/21 clip o video 10).
    => MOI shot POV deu phai co THAN trong khung: pov / pov_sit / pov_stand;
       chi dung pov_hand khi that su chi can hai ban tay tren mot mat ban.
 b. Thieu khoa `<cast>_pov*` trong C thi build() am tham roi ve mo ta NHIN TU NGOAI.
    A_HAHA va A_IMA da co du bien the.
 c. ⛔ **CAM can canh trang so co SO TIEN doc duoc** (`15_haha-no-okane.md` §7.3):
    vua la bia hien vat, vua dinh `feedback_so_tren_hinh_phai_do_font_ve`.
    So luon quay o goc nghieng / dang bi tay lat, chu khong doc ra.

📌 Thu tu chay: make_voice_15.py -> build_slides_15.py -> file nay (so canh = so clip
   cua SLIDES, doc o `06_VIDEO/15_haha-no-okane/clips/_MAP.txt`).
"""
import sys
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from videogen_lib import build, gate, write_outputs, autochain, linkage, act_report

# =====================================================================================
# P — BOI CANH. Ten khoa trung khoa EXTRAS cua videogen_lib de an dung lop nguoi nen.
# =====================================================================================
P = {
 "chanoma":    'the living room of a Showa house in the evening, a low round wooden dinner table in the middle of the tatami with flat floor cushions round it, a fluorescent ceiling light with a small glass shade and a long pull cord, a black rotary dial telephone on its own low stand, a wooden tea cabinet with sliding glass doors, a boxy wooden television standing on legs with wooden doors over the screen, a small household shrine shelf high on one wall, a blank unmarked calendar hanging on the pillar, sliding paper screens along one side',
 "chabudai":   'the top of a low round wooden dinner table in a Showa living room under a pull-cord fluorescent lamp, the grain worn pale in the middle, a lacquered tea tray with a squat teapot and small handleless cups pushed to one side',
 "daidokoro":  'the kitchen of a Showa house at night, a tiled worktop and a deep concrete sink, a two-ring gas burner with a blackened kettle on it, open shelves of enamel bowls and tin canisters, a wooden rice bin standing in the corner, a strip of sticky flypaper hanging from the ceiling, one bare bulb over the worktop and the rest of the room in shadow',
 "genkansaki": 'the doorway of a Showa house seen from just inside, a sunken concrete entrance floor with wooden sandals and lace-up shoes set out on it, a wooden shoe cabinet against the wall, a frosted glass sliding door half open onto the lane, the wooden corridor going back into the house',
 "shotengai":  'a Showa shopping street in the early evening, cloth awnings out over the pavement, a fishmonger weighing fish on a hanging balance and wrapping them in newspaper, a greengrocer with goods in wooden crates, plain unmarked split curtains hanging in the shop doorways, women carrying woven bamboo shopping baskets, bare bulbs strung over the street',
 "zashiki":    'a tatami room of a Showa house in the daytime, a low tea cabinet with sliding wooden doors against the wall, a square cloth wrapper folded on top of it, a dark wooden household altar in the corner, a shallow alcove with a plain hanging scroll, paper screens letting flat daylight in',
 "engawa":     'the wooden veranda of a Showa house in the late afternoon, the paper screens pushed back onto the garden, a flat cushion set down on the boards, a bamboo laundry pole and a stone water basin in the garden, the low hedge and the neighbouring tiled roofs beyond',
 "ginkou":     'a street outside a Showa branch bank, a tiled frontage with a heavy glass door, a rack of black bicycles with wooden crates on the back, low shopfronts along the pavement',
 "michi":      'a narrow Showa residential lane in the evening, wooden fences and low gates on both sides, a telegraph pole with a fire bell box on it, a round red postbox at the corner, the lit windows of the houses going away down the lane',
 "ima_ie":     'a present-day Japanese living room, a low sofa and a plain table, a flat window with a plain curtain, everyday daylight, nothing on the table but one old notebook',
}

# =====================================================================================
# C — DAN DIEN. A_HAHA la doi mat chinh; A_IMA la nguoi chung nhan o thoi NAY.
# =====================================================================================
C = {
 # ⭐ nguoi me — POV chinh cua ca video
 "haha":          "a woman in her forties in a white long-sleeved cook's smock tied in a bow at the back, worn over a plain blouse and a dark knee-length skirt, her hair cut short in a soft perm",
 "haha_pov":      "their own forearms in the pushed-back white sleeves of a cook's smock and the white smock front on their own chest",
 "haha_pov_sit":  "their own forearms in the pushed-back white sleeves of a cook's smock, the white smock front on their own chest, and their own knees and the dark skirt across the bottom of the picture",
 "haha_pov_stand":"their own forearms in the pushed-back white sleeves of a cook's smock and the white smock front on their own chest",
 "haha_pov_hand": 'their own forearms in pushed-back white smock sleeves and the backs of their own hands',
 "haha_pov_walk": 'only their own hand or hands where the work needs them, a white smock sleeve at the edge',
 # nguoi me NHIN THAY
 "chichi":  'a man in his forties in a white short-sleeved dress shirt with a plain narrow tie pulled loose, dark wide-legged trousers and a leather belt, his short hair combed flat',
 # thoi NAY — nguoi chung nhan cam cuon so
 "ima":          'a man in his seventies in a plain knitted cardigan over a checked shirt',
 "ima_pov":      'their own forearms and a knitted cardigan sleeve at the edge',
 "ima_pov_sit":  'their own forearms and a knitted cardigan on their own chest, and their own knees and lap across the bottom of the picture',
 "ima_pov_hand": 'their own forearms and the backs of their own hands, knitted cardigan cuffs at the edge',
}

# =====================================================================================
# CROWD — lop nguoi nen. Nha rieng thi 'solo'/'few' la NOI DUNG, khong phai thieu nguoi.
# =====================================================================================
CROWD = {
 "shotengai":  "full",
 "michi":      "few",
 "ginkou":     "few",
 "genkansaki": "few",
 "chanoma":    ("few", "trong nha — ca gia dinh, khong the dong hon"),
 "chabudai":   ("few", "can canh mat ban — VAN phai thay tay/chen cua nguoi nha o ria"),
 "daidokoro":  ("solo", "bep DEM — mot minh la NOI DUNG cua muc 3"),
 # 🔴 zashiki PHAI la 'solo' — KHONG phai vi muon canh vang, ma vi lop EXTRAS cua
 # videogen_lib cho key nay duoc viet cho canh NGU: "two more small figures lying on the
 # same bedding under the same net". Bat len 'few' thi moi canh me don giay to ban ngay
 # bi chen them nguoi NAM NGU DUOI MAN — lac hoan toan. Nguoi nha o day da co bang menh
 # de `as ... in the room beyond the screen` viet tay trong tung canh.
 "zashiki":    ("solo", "EXTRAS cua key nay ta canh NGU — xem ghi chu tren"),
 "engawa":     ("solo", "hien nha — khoang lang cuoi bai"),
 "ima_ie":     ("solo", "thoi NAY — mot nguoi, mot cuon so, do la LUAN DIEM"),
}


# =====================================================================================
# PROF — ⭐ STYLE RIENG CHO VIDEO 15 (user chot 2026-09-17: "mau phim hoai co hon")
#
# 🔴 Dung co che `prof=` cua videogen_lib, KHONG sua STYLE mac dinh — sua mac dinh la
#    doi luon lo 14 (171 clip da gen, dang cho dang) va moi video sau; hai lo khac cong
#    thuc thi sau nay so so do vo nghia. Cung ly do da ghi o §8.6 voi khoi `Avoid:`.
#
# ⚖️ PHAN CONG: mau do lop GRADE hau ky lo (tools/grade_showa.py) vi prompt khong dieu
#    khien duoc mau chinh xac. STYLE o day chi lam MOT viec: giu model khoi gen ra anh
#    QUA RUC / QUA NET — grade ha duoc bao hoa, nhung khong cuu duoc mau da chay.
# =====================================================================================
import videogen_lib as _V

# 🔴🔴 KET QUA PHEP THU ⓐ (lo 10 clip, 2026-09-17): GUARD O 70% PROMPT **KHONG AN**.
#   `AVOID` cua videogen_lib cam ro "any frame or border around the image" va cam chu —
#   nhung no nam o 65-75% prompt. Do tren 10 clip that:
#     · 5/10 clip co VIEN PHIM DEN + LO RANG + goc bo tron (H0,H1,H2,H3,H6)
#     · 1 clip (cho) day BIEN HIEU chu Nhat gia co doc duoc, chiem mang lon
#   => dung nguong da chot o §8.9 (>=4/10 thi chuyen ⓑ).
#   ⇒ Cach thi hanh ⓑ ma KHONG dung thu vien dung chung: nhet khoi CAM vao DAU STYLE.
#     STYLE la khoi dau tien cua prompt, nen guard roi vao ~2% dau — dung cho luat
#     `ai-video-regen.md` §2 doi. Lo 14 giu nguyen cong thuc cu, khong phai gen lai.
GUARD = ("The picture is a clean rectangle that runs right out to all four edges: "
         "no film border, no sprocket holes, no rounded corners, no black frame and no strip "
         "of any kind around the image. No printed lettering anywhere in the picture: no shop "
         "signs with writing, no banners, no printed labels, no printed text on any wall, box "
         "or packet. The one exception is the soft handwriting inside the notebook and the "
         "ledgers themselves, which is faint, uneven and far too small to read. ")

# 🔴 VONG SUA 2 CUA GUARD (2026-09-17) — ban dau no CAM CA CHU VIET TAY:
#   "...no writing on any paper, box or wall" — ma cuon 家計簿 la XUONG SONG ca bai (§7.2),
#   va so khong co chu thi la quyen vo trang, mat sach nghia. Guard nam o 1-3% prompt nen
#   no THANG cau ta canh o sau => model se ra so trang trang.
#   ⇒ Tach PRINTED (bien hieu, nhan, bang ron — thu that su hong) khoi HANDWRITING (chu
#     trong so). Khop dung §7.3: so quay goc nghieng, co chu nhung KHONG doc ra.
#   ⚠️ `AVOID` cua thu vien van cam "any letters... on any object" o cuoi prompt; hai cau
#     choi nhau, nhung cau o DAU thang — do la dinh luat da do (§8.12). Khong sua thu vien
#     dung chung chi vi mot video.

# ⚖️ VA BO CUM GAY RA CHINH CAI VIEN DO: "as if the print has sat in a box for fifty years"
#    mo ta mot VAT THE PHIM, nen model ve luon khung phim. Mau van giu bang cum ta MAU thuan.
PROF = {"HEAD": GUARD, "STYLE": _V.STYLE
    .replace("faded warm 1970s colour, low contrast, fine natural grain",
             "faded warm 1970s colour, muted and desaturated, no vivid and no electric colours "
             "anywhere, low contrast, fine natural grain")
    .replace("soft natural light",
             "soft natural light with a warm amber bloom around every window and lamp")
    .replace("deep focus so both the foreground and the background stay readable",
             "slightly soft focus rather than modern digital sharpness, deep enough that both "
             "the foreground and the background stay readable")}

S = []

# =====================================================================================
# HOOK 000-012 (13 clip / 37,9s = 2,7s moi canh) — user chot 2026-09-17:
#   "30s dau phai sinh dong len. Ngoi nhin may cai phong bi thi tu qua."
#
# ⭐ Ban truoc: 7 canh, 6/7 la CAN CANH TAY tren mat ban, khong mot khung rong nao,
#    khong mot khuon nguoi nao di chuyen. Nhip 5,4s/canh. Nhin ra la tu.
# ⭐ Ban nay doi CA HAI tang:
#    a. NHIP — tran rieng HOOK_MAX 3,4s trong build_slides_15.py => 13 canh thay vi 7.
#    b. LOAI CANH — 4 wide · 3 high · 2 medium · 1 ots · 2 pov_look · chi 2 can canh tay.
#       Ba cu soc (H6-H7-H8) la BA BOI CANH KHAC NHAU, deu co NGUOI, deu co khong gian.
#    c. Khoi mo bang nhip DEN NOI (nhan vat di toi tu cho khac), khong dung san.
# =====================================================================================
S += [
('H0','HOOK',"A_HAHA comes in from the corridor into the living room with a stack of small envelopes held against her apron, then she kneels down at the low table under the hanging lamp, then spreads the envelopes out across the table in front of her, while the hanging lamp sways over the table, as the family go on in the room behind",'chanoma','wide','Q',None,None),
('H1','HOOK',"A_HAHA reaches in over the row of small envelopes from the far side of the low table, then she squares the nearest one against the others, then draws her hand back out of the frame, while the hanging lamp sways over the table, as the father sits back at the far side of the table with a folded newspaper",'chanoma','low','Q',None,None),
('H2','HOOK',"A_HAHA: the row of small envelopes fills the bottom of the view across the table, then their own hand pushes the first three of them apart one after another, then rests flat past the end of the row, while the hanging lamp sways over the table, as the rest of the family go on with the evening in the room behind",'chanoma','pov_sit','Q',None,None),
('H3','HOOK',"A_HAHA, seen over her shoulder the whole time, reaches out over the spread envelopes, then she draws the thinnest one back out of the row towards herself, then sets it down apart from the others by her own knees, while the hanging lamp sways over the table, as the father sits back from the far side of the table",'chanoma','ots','Q',None,None),
('H4','HOOK',"A_IMA walks in across the bright modern room left to right across the frame carrying an old notebook in both hands, then he sits down at the plain table, then lays the notebook flat on it and opens the cover, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H5','HOOK',"A_IMA: the whole plain table lies below the view with the open notebook in the middle and a pair of hands resting on either side of it, then the hands turn the first page over, then flatten it down at both corners, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('H6','HOOK',"A_HAHA takes a wrapped parcel from the fishmonger in a rubber apron and a white cloth cap with a towel round his neck over the slab, then she turns away with it and walks on along the pavement left to right across the frame, then goes on past the next shopfront without stopping, while the bare bulbs sway over the street, as the crowd moves along the arcade on both sides",'shotengai','wide','Q',None,None),
('H7','HOOK',"A_HAHA sits alone at the kitchen worktop under the one bare bulb with the rest of the room in darkness, then she leans in over a cardboard box of small parts, then goes on working with only her hands moving, while the bare bulb sways overhead and her shadow moves on the wall",'daidokoro','wide','Q',None,None),
('H8','HOOK',"the collector, a man in his fifties in a grey work jacket, stands on the step at the half-open door seen from the chest up with a small ledger book open on one forearm, then he presses a red seal down onto the page, then lifts it away and turns the book round towards the house, while the shadow of the door frame moves across the floor, as a neighbour passes along the lane behind him",'genkansaki','medium','Q',None,None),
('H9','HOOK',"A_IMA: the open notebook fills the view on the modern table with its columns of handwriting, then the view moves along the page from the top of the column to the foot of it, then comes back up to the head of the page, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('H10','HOOK',"A_IMA: the notebook lies open in the bottom of the view, then their own hand turns a run of pages over towards the back of it, the hand staying in place, then stops flat on the last written page, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('H11','HOOK',"A_IMA: the whole table lies below the view with the notebook open at a blank page and a pair of hands resting on either side of it, then the hands smooth the empty paper flat, then draw back to the edge of the table and stay there, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('H12','HOOK',"A_HAHA kneels at the low table with the whole row of envelopes in front of her, then she gathers them up into one stack against her apron, then stays still holding them, while the hanging lamp sways over the table, as the father and the room go on behind her",'chanoma','wide','Q',None,None),
]

# =====================================================================================
# INTRO 013-015 (3 clip) — chao + hua "cung lat cuon so" + nhac lai LOOP
# =====================================================================================
S += [
('A0','INTRO',"A_IMA sits back from the plain table with the old notebook open in front of him, then he turns it round so the page faces across the table, then rests both hands on the edge of the table, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('A1','INTRO',"A_HAHA: the living room opens out ahead of the view from the corridor door, then the view carries in along the tatami left to right across the frame, then stops at the low table with the lamp hanging over it, while the hanging lamp sways over the table, as the family go on in the room",'chanoma','pov_look','Q',None,None),
('A2','INTRO',"A_HAHA: the low table fills the bottom of the view with a stack of small envelopes on it, then their own hand fans the stack out into a row again, then sets the last one straight and lifts away, while the hanging lamp sways over the table, as the father turns a page of his newspaper across the table",'chanoma','pov_hand','Q',None,None),
]

# =====================================================================================
# MUC 1 — 給料は封筒の現金で母の手に渡る (009-038, 30 clip)
# =====================================================================================
S += [
('B0','M1',"A_CHICHI comes in through the half-open frosted door and steps up onto the wooden floor, then he sets a cloth cap down on the step, then turns and pushes the door to behind him, while the shadow of the door frame moves across the floor, as a neighbour goes past along the lane outside",'genkansaki','medium','Q','C','A_CHICHI standing inside the doorway with his cap on the step'),
('B1','M1',"A_HAHA: the doorway fills the view with the father standing just inside it, then he takes a brown envelope out of the inside of his jacket and holds it out, then their own two hands come up and take it from him, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q','C',None),
('B2','M1',"A_HAHA: the brown envelope lies across their own two palms in the bottom of the view, then their own hands lift it once as if weighing it, then turn it over and hold it still, while the corridor light moves on the paper",'genkansaki','pov_hand','Q',None,None),
('B3','M1',"A_HAHA, seen from behind the whole time, carries the envelope the whole length of the corridor into the living room, then she kneels down at the low table, then lays the envelope on the table in front of her, while the hanging lamp sways over the table, as the family go on in the room behind",'chanoma','behind','Q',None,None),
('B4','M1',"A_HAHA: the low table fills the bottom of the view with the envelope on it, then their own thumb works the flap open along its edge without tearing it, then draws the folded notes halfway out and stops, while the hanging lamp sways over the table, as two of the family sit talking at the far end of the room",'chanoma','pov_sit','Q','D','A_HAHA seated with the notes half out of the envelope'),
('B5','M1',"A_HAHA: their own hands hold the notes in a fan over the table in the view, then the thumb counts them across from one side to the other, then stops halfway and goes back to the start, while the hanging lamp sways over the table, as the television murmurs to the family in the corner",'chanoma','pov_hand','Q','D','A_HAHA holding the fanned notes above the table'),
('B6','M1',"A_HAHA: the notes lie squared on the table in the bottom of the view, then their own finger goes up to their own mouth and comes back down, then counts the notes across a second time to the end, while the hanging lamp sways over the table, as the father sits back at the far side of the table with a folded newspaper",'chanoma','pov_sit','Q','D','A_HAHA with the counted notes squared on the table'),
('B7','M1',"A_CHICHI sets his teacup down on the low table and speaks a few words across it, then he sits back on his heels, then picks the cup up again and drinks, while the hanging lamp sways over the table, as the television murmurs in the corner",'chanoma','ots','Q','D','A_CHICHI sitting back with the teacup in his hand','warm'),
('B8','M1',"A_HAHA: the table fills the view with the father sitting back from it, then the view comes up from the notes to his face for a moment, then goes back down to the notes without stopping anywhere else, while the hanging lamp sways over the table, as the family go on in the room behind",'chanoma','pov_look','Q','D',None),
('B9','M1',"A_CHICHI sits back at the far side of the low table with a folded newspaper open in his hands, then he turns a page of it, then lowers it and looks across the table, while the hanging lamp sways over the table, as the parents go on talking above him",'chanoma','ots','Q',None,None,'warm'),
('B10','M1',"A_HAHA: the tea cabinet stands against the wall in the view, then their own hand slides the wooden door of it open, then lifts out a bundle of small envelopes held in a rubber band and brings them back towards the view, while the shadow of the screen frame moves across the wall, as the rest of the family go on with the evening in the room behind",'chanoma','pov_stand','Q',None,None),
('B11','M1',"A_HAHA: the small envelopes fill the bottom of the view on the table, then their own hands deal them out in a row one after another, then straighten the row square to the table edge, while the hanging lamp sways over the table, as a second teacup stands within reach at the far edge of the table",'chabudai','pov_hand','Q','E','the row of small envelopes squared on the table'),
('B12','M1',"A_HAHA: the row of envelopes fills the bottom of the view, then their own hand slides a folded set of notes into the first envelope, then presses the flap flat under the thumb and sets it back in the row, while the hanging lamp sways over the table, as another pair of hands rests on the far edge of the table",'chabudai','pov_hand','Q','E','the first small envelope filled and set back in the row'),
('B13','M1',"A_HAHA: the second envelope lies open under their own hand in the bottom of the view, then their own fingers feed a smaller set of notes down into it, then fold the flap over and smooth it shut, while the hanging lamp sways over the table, as a hand reaches in from the far side and lifts the teapot away",'chabudai','pov_hand','Q','E','the second small envelope folded shut on the table'),
('B14','M1',"A_HAHA: the envelope lies under their own hand in the bottom of the view, then the other hand takes up a pencil and writes a short word on the front of it, then lays the pencil down across the table, while the hanging lamp sways over the table, as a folded newspaper lies at the far edge of the table where someone set it down",'chabudai','pov_hand','Q','E','the pencil lying across the table beside the envelopes'),
('B15','M1',"A_HAHA: the worn corner of one envelope fills the bottom of the view, then their own finger and thumb rub the frayed edge of it once, then set it back down in the row with the others, while the hanging lamp sways over the table, as the shadow of someone sitting opposite falls across the far side of the table",'chabudai','pov_hand','Q','E','the worn envelope back in the row with the others'),
('B16','M1',"A_HAHA: the finished row of envelopes fills the bottom of the view, then their own two hands gather the row into one stack, then stand the stack on its end and square it against the table, while the hanging lamp sways over the table, as a second teacup stands within reach at the far edge of the table",'chabudai','pov_hand','Q','E',None),
('B17','M1',"A_CHICHI leans in over the low table from the far side and reaches towards the stack of envelopes, then he stops with his hand short of it, then sits back onto his heels again, while the hanging lamp sways over the table, as the television murmurs in the corner",'chanoma','ots','Q',None,None,'warm'),
('B18','M1',"A_HAHA, seen from behind the whole time, carries the last envelope from the living room into the kitchen, then she stops at the rice bin in the corner, then stands there holding it without opening the lid, while the bare bulb over the worktop sways and the shadows move with it",'daidokoro','behind','Q','F','A_HAHA standing at the rice bin with the envelope in her hand'),
('B19','M1',"A_HAHA: the wooden rice bin fills the view in the corner of the kitchen, then their own hand lifts the lid away and rests it against the wall, then goes down into the rice and pushes the folded notes under the surface, while the bare bulb over the worktop sways and the shadows move with it",'daidokoro','pov_stand','Q','F','A_HAHA with one hand still down in the rice'),
('B20','M1',"A_HAHA: the open rice bin fills the bottom of the view, then their own hand comes up out of the rice and brushes the grains off itself, then sets the wooden lid back down over the rim, while the bare bulb over the worktop sways and the shadows move with it",'daidokoro','pov_hand','Q','F',None),
('B21','M1',"A_HAHA: the kitchen opens out ahead of the view towards the lit living room door, then the view carries across the kitchen left to right, then stops in the doorway where the family are sitting round the table, while the bare bulb sways overhead and the shadows move with it, as the family go on talking at the table",'daidokoro','pov_look','Q',None,None),
('B22','M1',"A_HAHA and A_CHICHI sit on either side of the low table with the bowls set out between them, then they take up their bowls together, then begin to eat without hurrying, while the hanging lamp sways over the table, as the room goes on around them",'chanoma','wide','Q',None,None,'warm'),
('B23','M1',"A_HAHA: the empty brown envelope lies flat on the low table in the bottom of the view, then their own hand folds it once along the middle, then sets it down on the corner of the table and leaves it there, while the hanging lamp sways over the table, as the father turns a page of his newspaper across the table",'chanoma','pov_sit','Q',None,None),
('B24','M1',"A_CHICHI walks the length of the lane away from the house in the morning left to right across the frame, then he stops at the corner by the telegraph pole, then goes on out of sight round it, while the wind moves the fences along the lane, as a neighbour on a bicycle passes him",'michi','wide','Q',None,None),
('B25','M1',"A_HAHA: the bank front fills the view across the street with its heavy glass door, then the view holds on the people going in and out of it left to right across the frame, then turns away along the pavement to the low shops, while the awnings move in the wind, as passers-by cross in front of the frontage",'ginkou','pov_look','Q',None,None),
('B26','M1',"A_HAHA: the pavement outside the bank fills the view with a man coming out of the glass door with a small book in his hand, then he stops on the step and opens it, then closes it again and walks on left to right across the frame, while the awnings move in the wind, as other people come out behind him",'ginkou','pov_look','Q',None,None),
('B27','M1',"A_IMA: the open notebook fills the bottom of the view on the modern table, then their own finger runs down the first column to the bottom of the page, the hand staying in place, then stops there and lifts away, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('B28','M1',"A_HAHA: the low table fills the view cleared of everything but the one thin envelope, then the view holds on it, then turns away to the paper screen where the light is, while the hanging lamp sways over the table, as two of the family sit talking at the far end of the room",'chanoma','pov_look','Q',None,None),
('B29','M1',"A_HAHA, seen from behind the whole time, kneels at the low table and reaches up to the hanging lamp, then she pulls the cord once, then settles back with the room gone dim around her, while the lamp swings a little on its cord after the pull, as the television murmurs to the family in the corner",'chanoma','behind','Q',None,None),
]

# =====================================================================================
# MUC 2 — 買い物はその場で払わない（ツケ・通い帳・御用聞き）(039-066, 28 clip)
# =====================================================================================
S += [
('C0','M2',"A_HAHA: the shopping street opens out ahead of the view under the strung bulbs, then the view carries along the pavement left to right past the awnings, then stops where the fishmonger's slab comes into the frame, while the bare bulbs sway over the street, as shoppers move along the pavement on both sides",'shotengai','pov_look','Q',None,None),
('C1','M2',"A_HAHA, seen from behind the whole time, walks the length of the arcade with a cloth bag over one arm, then she slows at the greengrocer's boxes, then goes on past them towards the fish, the whole move running left to right across the frame, while the bare bulbs sway over the street, as other shoppers come the other way",'shotengai','behind','Q',None,None),
('C2','M2',"the fishmonger stands behind his slab of fish on ice and lifts a hand in greeting, then he says something across the slab, then turns back and takes up a sheet of paper to wrap with, while the bare bulbs sway over the street, as the queue behind moves up a step",'shotengai','ots','Q','G','the fishmonger behind the slab with the wrapping paper in his hands','warm'),
('C3','M2',"A_HAHA: the slab fills the view with the fish laid out on ice, then the shopkeeper lifts one clear of the ice and lays it on the paper, then folds the paper over it twice and holds the parcel out, while the bare bulbs sway over the street, as the shoppers behind wait their turn",'shotengai','pov','Q','G','the fishmonger holding the wrapped parcel out over the slab'),
('C4','M2',"A_HAHA: the parcel of fish comes into the bottom of the view in their own two hands, then their own hands turn it once and settle it into the cloth bag, then take hold of the handles and lift, while the bare bulbs sway over the street",'shotengai','pov_hand','Q','G',None),
('C5','M2',"the fishmonger takes a small ledger book off a nail on the post beside him, then he opens it flat on one forearm, then writes two short lines in it with a pencil, while the bare bulbs sway over the street, as the next customer steps up to the slab",'shotengai','ots','Q',None,None),
('C6','M2',"A_HAHA: the ledger on the shopkeeper's arm fills the view with the ruled lines of it, then he turns it a little so the page faces the view, then closes it and hangs it back on the nail, while the bare bulbs sway over the street",'shotengai','pov','Q',None,None),
('C7','M2',"A_HAHA: the pavement ahead fills the view with the cloth bag hanging from their own hand at the edge of it, then their own other hand stays flat against the apron front the whole time, then the view carries on along the pavement left to right, while the bare bulbs sway over the street, as shoppers pass on both sides",'shotengai','pov_walk','Q',None,None),
('C8','M2',"A_HAHA: the greengrocer's boxes fill the view with vegetables standing in them, then their own hand turns one of the boxes a little to see the back of it, then takes nothing and withdraws, while the awnings move over the pavement, as the shopkeeper serves someone at the far end",'shotengai','pov','Q',None,None),
('C9','M2',"A_HAHA, seen from behind the whole time, stops at the end of the arcade with the bag on her arm, then she looks back the whole length of the street, then turns and goes out of the arcade left to right across the frame, while the bare bulbs sway over the street, as the shops go on serving behind her",'shotengai','behind','Q',None,None),
('C10','M2',"A_HAHA: the lane fills the view ahead with the lit windows of the houses going away down it, then the view carries along the lane left to right, then stops at their own gate, while the wind moves the fences along the lane, as a neighbour comes the other way and passes",'michi','pov_walk','Q',None,None),
('C11','M2',"A_HAHA: the tea cabinet fills the view against the wall, then their own hand slides the door open and lifts out a small thin account book, then sets it down flat on the low table, while the shadow of the screen frame moves across the wall, as the father sits back at the far side of the table with a folded newspaper",'chanoma','pov_stand','Q',None,None),
('C12','M2',"A_HAHA: the thin account book lies open in the bottom of the view on the table, then their own hand turns two pages over together, then flattens the second one down with the side of the hand, while the hanging lamp sways over the table, as another pair of hands rests on the far edge of the table",'chabudai','pov_hand','Q','H','the account book open flat at the second page'),
('C13','M2',"A_HAHA: the open page fills the bottom of the view with its ruled columns, then their own finger goes down the column line by line to the foot of it, then stops and rests there, while the hanging lamp sways over the table, as a hand reaches in from the far side and lifts the teapot away",'chabudai','pov_hand','Q','H','A_HAHA with one finger resting at the foot of the column'),
('C14','M2',"A_HAHA: the account book lies open under the lamp in the bottom of the view, then their own hand takes up a pencil and adds a short line at the foot of the page, then lays the pencil down beside the book, while the hanging lamp sways over the table, as a folded newspaper lies at the far edge of the table where someone set it down",'chabudai','pov_hand','Q','H',None),
('C15','M2',"the delivery man in a work jacket and a peaked cap with canvas covers over his forearms stands at the half-open door with a wooden box held under one arm, then he lifts the lid of it and shows what is inside, then sets one item down on the step and straightens up again, while the shadow of the door frame moves across the floor, as a bicycle goes past in the lane behind him",'genkansaki','ots','Q','I','the delivery man at the door with the box open under his arm','warm'),
('C16','M2',"A_HAHA: the doorway fills the view with the delivery man standing on the step, then he says something and waits, then their own hand lifts once in answer without any money passing, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q','I','the delivery man standing on the step with the box still under one arm'),
('C17','M2',"the delivery man takes a pencil from behind his ear and writes in a small book against the door frame, then he puts the pencil back behind his ear, then picks the box up and goes off down the lane left to right across the frame, while the shadow of the door frame moves across the floor, as the lane goes on behind him",'genkansaki','medium','Q','I',None),
('C18','M2',"A_HAHA: the step inside the door fills the bottom of the view with the delivered item standing on it, then their own hand takes it up off the step, then carries it out of the top of the frame towards the kitchen, while the corridor light moves along the floor",'genkansaki','pov_hand','Q',None,None),
('C19','M2',"A_HAHA and A_CHICHI sit at the low table with the evening meal set out between them, then they begin to eat, then one of them holds a bowl up to be filled again, while the hanging lamp sways over the table, as the television murmurs in the corner",'chanoma','wide','Q',None,None,'warm'),
('C20','M2',"A_HAHA: the calendar on the wall fills the view with the month laid out on it, then their own hand turns the last few days over with one finger, then stops at the end of the month and withdraws, while the shadow of the screen frame moves across the wall, as the rest of the family go on with the evening in the room behind",'chanoma','pov_stand','Q',None,None),
('C21','M2',"A_HAHA: the low table fills the bottom of the view with the account book and one envelope side by side, then their own hands open the envelope and set the notes out beside the book, then square the notes against the edge of the page, while the hanging lamp sways over the table, as the shadow of someone sitting opposite falls across the far side of the table",'chabudai','pov_hand','Q',None,None),
('C22','M2',"A_HAHA, seen from behind the whole time, walks the length of the arcade with the notes held ready in one hand, then she stops at the fishmonger's post, then holds the money out across the slab to him, the whole move running left to right across the frame, while the bare bulbs sway over the street, as the shops go on serving on both sides",'shotengai','behind','Q','J','A_HAHA at the slab holding the money out to A_SAKANA'),
('C23','M2',"the fishmonger presses the money flat under the band of his apron, then he takes the ledger down off its nail, then draws one long line across the page and shows it, while the bare bulbs sway over the street, as the next customer waits behind",'shotengai','ots','Q','J','the fishmonger holding the ledger open with the line drawn across it','warm'),
('C24','M2',"A_HAHA: the ruled page of the ledger fills the view with the line drawn across it, then the shopkeeper closes the book on it, then hangs it back on the nail on the post, while the bare bulbs sway over the street",'shotengai','pov','Q','J',None),
('C25','M2',"A_HAHA: the far end of the street fills the view with a wide new shopfront standing among the low shops, then the view holds on people carrying baskets out of it left to right across the frame, then comes back along the pavement to the awnings, while the awnings move in the wind, as shoppers cross in both directions",'shotengai','pov_look','Q',None,None),
('C26','M2',"A_HAHA: a shelf inside the new shop fills the view with goods standing in rows on it, then their own hand takes one down and holds it, then sets it into a wire basket hanging from their own other arm, while the light moves along the shelf, as other shoppers pass behind with baskets",'shotengai','pov','Q',None,None),
('C27','M2',"A_IMA: the open notebook fills the bottom of the view on the modern table, then their own hand turns one page over to the next, then stops flat on a page where the columns are ruled closer together, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
]

# =====================================================================================
# MUC 3 — 夜の台所が工場になる（内職）(067-092, 26 clip)
# =====================================================================================
S += [
('D0','M3',"A_HAHA: the kitchen fills the view at night with one bare bulb over the worktop and the rest in shadow, then the view turns from the dark corner to the lit worktop, then settles on a cardboard box standing on it, while the bare bulb sways and the shadows move with it",'daidokoro','pov_look','Q',None,None),
('D1','M3',"A_HAHA: the cardboard box fills the bottom of the view on the worktop, then their own two hands pull the flaps of it apart, then fold them back against the sides and hold them down, while the bare bulb over the worktop sways and the shadows move with it",'daidokoro','pov_sit','Q','K','A_HAHA seated at the worktop with the box open in front of her'),
('D2','M3',"A_HAHA: the open box fills the bottom of the view with hundreds of small identical parts in it, then their own hand goes down into them and comes up with a handful, the hand staying in place, then lets them run back down into the box, while the bare bulb sways and the shadows move with it",'daidokoro','pov_sit','Q','K','A_HAHA with both hands resting on the open box'),
('D3','M3',"A_HAHA: the worktop fills the bottom of the view with two small parts lying on it, then their own two hands bring them together until they meet, then press them home and set the joined piece down to one side, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','K','the joined piece lying on the worktop to one side'),
('D4','M3',"A_HAHA: the finished pieces fill the bottom of the view in a growing row on the worktop, then their own hands add two more to the end of the row, then push the whole row a little further along to make space, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','K','the row of finished pieces pushed along the worktop'),
('D5','M3',"A_HAHA: the worktop fills the bottom of the view with a small pot of paste standing open on it, then their own finger takes a little of the paste out on its tip, then draws it along the edge of a folded paper flower, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','K','A_HAHA holding the pasted paper flower over the worktop'),
('D6','M3',"A_HAHA: their own two hands hold the paper flower in the bottom of the view, then they press the pasted edge closed between finger and thumb, then set the flower down with the others and let go, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','K',None),
('D7','M3',"A_HAHA: their own hands rest on the worktop in the bottom of the view, then they turn over so the fingertips come up into the light, then stay there while one thumb rubs across the ends of the fingers, while the bare bulb sways and the shadows move with it",'daidokoro','pov_sit','Q',None,None),
('D8','M3',"A_HAHA: the worktop fills the view with a small tin standing at the back of it, then their own hand takes out a strip of plaster and winds it round one fingertip, then presses the end of it down flat, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q',None,None),
('D9','M3',"A_HAHA: the doorway of the dark living room fills the view from the kitchen, then the view holds on a folded quilt laid out on the tatami, then comes back to the lit worktop, while the bare bulb sways and the shadows move with it",'daidokoro','pov_look','Q',None,None),
('D10','M3',"A_HAHA, seen from behind the whole time, sits alone at the worktop under the one bulb, then she leans in closer over the work, then straightens up and rolls her shoulders back once, while the bare bulb sways overhead and her shadow moves on the wall",'daidokoro','behind','Q',None,None),
('D11','M3',"A_HAHA: the kettle stands on the gas ring in the view, then their own hand turns the tap of the ring and the flame comes up under it, then withdraws and leaves it there, while the steam begins to lift off the kettle",'daidokoro','pov_stand','Q',None,None),
('D12','M3',"A_HAHA: the worktop fills the bottom of the view with a teacup set down beside the boxes, then their own two hands take the cup up and hold it, then set it down again without drinking, while the steam comes off the cup and bends away",'daidokoro','pov_sit','Q',None,None),
('D13','M3',"A_HAHA: the window over the sink fills the view black with the night outside, then the view holds on the dark glass with the room reflected in it, then comes down to the work on the worktop, while the reflection of the bulb moves in the glass",'daidokoro','pov_look','Q',None,None),
('D14','M3',"A_HAHA: the growing pile of finished pieces fills the bottom of the view, then their own two hands scoop a load of them up together, then tip them down into a second box at the side, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','L','the second box filling with finished pieces'),
('D15','M3',"A_HAHA: the second box fills the bottom of the view nearly full, then their own hands fold the flaps of it over one another, then press the last flap down under the others, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','L','the second box closed on the worktop'),
('D16','M3',"A_HAHA, seen from behind the whole time, carries the closed box the whole length of the kitchen to the door, then she crouches and sets it down on the step, then stands up and stays beside it, while the bare bulb sways overhead and her shadow moves on the wall",'daidokoro','behind','Q','L',None),
('D17','M3',"A_HAHA: the doorway fills the view with grey morning light coming through the frosted glass, then the view drops to the box standing waiting on the step, then holds there, while the shadow of the door frame moves across the floor",'genkansaki','pov_look','Q',None,None),
('D18','M3',"the delivery man crouches at the open door and takes hold of the box on the step, then he lifts it against his chest, then turns and carries it away down the lane left to right across the frame, while the shadow of the door frame moves across the floor, as the lane goes on behind him",'genkansaki','medium','Q',None,None),
('D19','M3',"A_HAHA: the empty step fills the bottom of the view where the box stood, then their own hand comes down and brushes the dust off it, then withdraws out of the frame, while the shadow of the door frame moves across the floor",'genkansaki','pov_hand','Q',None,None),
('D20','M3',"A_HAHA: the low table fills the bottom of the view with a few coins and small notes set out on it, then their own finger moves them one at a time into a line, then stops with the last one and rests beside it, while the shadow of the screen frame moves across the table, as a second teacup stands within reach at the far edge of the table",'chabudai','pov_hand','Q',None,None),
('D21','M3',"A_HAHA: the thin account book fills the bottom of the view open on the table, then their own hand writes one short line low down on the page, then closes the book over the pencil, while the shadow of the screen frame moves across the table, as another pair of hands rests on the far edge of the table",'chabudai','pov_hand','Q',None,None),
('D22','M3',"A_CHICHI comes along the corridor in the morning with his jacket over one arm, then he stops at the kitchen door and says something in, then goes on out towards the front door left to right across the frame, while the corridor light moves along the floor, as the house goes on waking behind him",'genkansaki','medium','Q',None,None,'warm'),
('D23','M3',"A_HAHA: the kitchen worktop fills the view in the morning wiped bare, then the view turns from the bare worktop to the stacked empty boxes in the corner, then holds on them, while the light moves across the worktop",'daidokoro','pov_look','Q',None,None),
('D24','M3',"A_CHICHI sits back on the tatami with a folded newspaper held up in front of him, then he lowers it onto his knees in place, then folds it over once and sets it down beside him, while the shadow of the screen frame moves across the floor, as the house goes on around him",'chanoma','ots','Q',None,None,'warm'),
('D25','M3',"A_IMA: the open notebook fills the bottom of the view on the modern table, then their own finger stops on a line of much smaller writing, then rests there without moving, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
]

# =====================================================================================
# CTA giua video (093-096, 4 clip) — canh trung tinh, khong day mach
# =====================================================================================
S += [
('E0','CTA',"A_IMA: the modern room opens out ahead of the view towards the window, then the view carries across to it left to right, then stops where the daylight comes in over the sill, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('E1','CTA',"A_HAHA: the veranda boards fill the view with the garden beyond the open screens, then the view turns along the boards to the cushion set down on them, then holds there, while the hedge moves in the wind beyond the boards",'engawa','pov_look','Q',None,None),
('E2','CTA',"A_HAHA, seen from behind the whole time, sits down on the cushion on the veranda boards, then she smooths her apron flat over her knees, then rests both hands on them and stays still, while the hedge moves in the wind beyond the boards",'engawa','behind','Q',None,None),
('E3','CTA',"A_IMA: the old notebook lies closed on the modern table in the bottom of the view, then their own hand rests flat on the cover of it, then lifts away and leaves it lying there, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
]

# =====================================================================================
# MUC 4 — 大きな買い物は月賦。足りない月は借りる (097-121, 25 clip)
# =====================================================================================
S += [
('F0','M4',"A_HAHA and A_CHICHI stand together in front of a shop window with a television standing in it, then they lean in towards the glass, then step back again and go on looking, while the awnings move over the pavement, as shoppers pass behind them",'shotengai','wide','Q',None,None,'warm'),
('F1','M4',"A_HAHA: the shop window fills the view with the television set standing behind the glass, then their own hand comes up and rests against the glass in front of it, then drops away to their side, while the awnings move in the wind behind",'shotengai','pov','Q',None,None),
('F2','M4',"the delivery man and another man carry a large wooden crate between them along the lane towards the house left to right across the frame, then they set it down at the gate, then take hold of it again lower down, while the wind moves the fences along the lane, as a neighbour stops to watch them",'michi','wide','Q',None,None),
('F3','M4',"A_HAHA: the doorway fills the view with the crate coming in through it, then the two men set it down inside on the wooden floor, then straighten up and stand back from it, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q',None,None),
('F4','M4',"A_HAHA and A_CHICHI kneel on either side of the television standing on its new stand in the corner, then one of them reaches out and turns the dial on the front of it, then sits back beside her, while the light moves on their faces, as the room goes on around them",'chanoma','wide','Q',None,None,'warm'),
('F5','M4',"the collector stands in the half-open doorway and takes a small book out of his jacket, then he opens it flat against his forearm, then turns it round so the page faces into the house, while the shadow of the door frame moves across the floor, as a bicycle passes in the lane behind him",'genkansaki','ots','Q','M','the collector at the door with the payment book open on his forearm'),
('F6','M4',"A_HAHA: the doorway fills the view with the collector holding the open book out, then their own hand comes into the frame and sets a folded note down on the page, then withdraws to the apron front, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q','M','the folded note lying on the open page in his hands'),
('F7','M4',"the collector takes the note off the page and folds it into his pocket, then he presses a red seal down into one of the ruled squares, then lifts the seal away and blows once on the mark, while the shadow of the door frame moves across the floor",'genkansaki','ots','Q','M','the collector holding the stamped book open on one forearm'),
('F8','M4',"A_HAHA: the payment book fills the view held open towards them, then the collector turns it a little further round, then closes it and puts it away inside his jacket, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q','M',None),
('F9','M4',"the collector steps back down onto the lane and lifts a hand in parting, then he turns away from the door, then goes off along the lane left to right across the frame, while the shadow of the door frame moves across the floor, as the lane goes on behind him",'genkansaki','medium','Q',None,None,'warm'),
('F10','M4',"A_HAHA: the tatami room fills the view with the low tea cabinet against the wall, then their own two hands slide the wooden doors of it apart, then hold them open at the sides, while the shadow of the screen frame moves across the cabinet, as someone moves about in the next room beyond the paper screen",'zashiki','pov_stand','Q','N','A_HAHA with the cabinet doors slid open'),
('F11','M4',"A_HAHA: the inside of the cabinet fills the view with folded cloths and papers in it, then their own hand goes in and brings the small payment book out, then holds it in the light from the screen, while the shadow of the screen frame moves across the cabinet, as the family go on with the day in the room beyond the screen",'zashiki','pov_stand','Q','N','A_HAHA holding the payment book in the light from the screen'),
('F12','M4',"A_HAHA: the payment book lies open in their own hands in the bottom of the view, then their own finger counts down the ruled squares one by one, then stops on the first empty one and stays there, while the shadow of the screen frame moves across the page, as someone moves about in the next room beyond the paper screen",'zashiki','pov_sit','Q','N','A_HAHA with one finger on the first empty square'),
('F13','M4',"A_HAHA, seen from behind the whole time, kneels in front of the open cabinet with the book in her hands, then she puts it back in among the cloths, then slides the wooden doors closed over it, while the shadow of the screen frame moves across the wall, as the family go on with the day in the room beyond the screen",'zashiki','behind','Q','N',None),
('F14','M4',"A_HAHA: the low table fills the bottom of the view with the account book and the payment book lying side by side, then their own hands square the two of them against each other, then rest flat on both, while the hanging lamp sways over the table, as a hand reaches in from the far side and lifts the teapot away",'chabudai','pov_hand','Q',None,None),
('F15','M4',"A_HAHA: the lane outside fills the view in the evening with the lit windows going away down it, then a man in a dark jacket comes along it towards the view, then turns in at a gate further down, while the wind moves the fences along the lane, as another neighbour passes the other way",'michi','pov_look','Q',None,None),
('F16','M4',"A_HAHA: the neighbouring gate fills the view with the man standing at it, then the door there opens and a hand takes something from him, then the door closes again and he walks on left to right across the frame, while the wind moves the fences along the lane",'michi','pov_look','Q',None,None),
('F17','M4',"A_HAHA, seen from behind the whole time, stands at her own gate looking down the lane after him, then she takes hold of the gate and pulls it to, then turns back towards the house, while the wind moves the fences along the lane, as the lit windows go on down the lane",'michi','behind','Q',None,None),
('F18','M4',"A_HAHA: the low table fills the bottom of the view with the thin account book open on it, then their own hand adds a line at the very foot of the page, then draws a short stroke beside it and stops, while the hanging lamp sways over the table, as a folded newspaper lies at the far edge of the table where someone set it down",'chabudai','pov_hand','Q',None,None),
('F19','M4',"A_CHICHI sits at the low table with the payment book open in front of him, then he turns it round towards the other side of the table, then sits back and says nothing, while the hanging lamp sways over the table, as the television murmurs in the corner",'chanoma','ots','Q',None,None),
('F20','M4',"A_HAHA: the payment book fills the bottom of the view with the last empty square on the page, then their own hand sets a folded note down on the square, then presses it flat and leaves it there, while the hanging lamp sways over the table, as the shadow of someone sitting opposite falls across the far side of the table",'chabudai','pov_hand','Q',None,None),
('F21','M4',"the collector presses the red seal down into the last square of the page, then he lifts the seal clear, then turns the book round and holds it out flat with both hands, while the shadow of the door frame moves across the floor, as the lane goes on behind him",'genkansaki','ots','Q','O','the collector holding the finished book out with both hands','warm'),
('F22','M4',"A_HAHA: the finished page fills the view with the whole run of red seals across it, then their own two hands take the book from him, the hands staying in place, then hold it against the apron front, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q','O',None),
('F23','M4',"A_HAHA, seen from behind the whole time, stands alone inside the doorway with the finished book in both hands, then she lowers it slowly to her side, then goes back along the corridor into the house, while the shadow of the door frame moves across the floor",'genkansaki','behind','Q',None,None),
('F24','M4',"A_IMA: the open notebook fills the bottom of the view on the modern table, then their own hand turns over a page with faint red marks running down the margin, the hand staying in place, then flattens the next one down, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
]

# =====================================================================================
# MUC 5 — 母には自分の名前の年金がなかった (122-155, 34 clip) — DINH BAI, tra LOOP
# =====================================================================================
S += [
('G0','M5',"A_IMA: the old notebook fills the bottom of the view on the modern table, then their own two hands turn the last leaf of it over, then hold the blank page down flat at both corners, while the curtain at the window stirs",'ima_ie','pov_sit','Q','P','A_IMA holding the last blank page of the notebook flat'),
('G1','M5',"A_IMA: the blank last page fills the bottom of the view with nothing written on it, then their own finger moves down the empty paper from top to bottom, then lifts away at the foot of it, while the curtain at the window stirs",'ima_ie','pov_hand','Q','P','A_IMA with the blank page open flat on the table'),
('G2','M5',"A_IMA, seen from behind the whole time, sits at the table with the notebook open at the blank page, then he turns back two pages to the written ones, then goes forward to the blank one again, while the curtain at the wide window stirs",'ima_ie','behind','Q','P',None),
('G3','M5',"A_HAHA: the low table fills the bottom of the view with the row of small envelopes on it, then their own hand moves along the row touching each one in turn, then stops past the end of the row where there is nothing, while the hanging lamp sways over the table, as a second teacup stands within reach at the far edge of the table",'chabudai','pov_hand','Q',None,None),
('G4','M5',"A_HAHA, seen from behind the whole time, kneels at the low table with the account book open in front of her, then she writes one line in it, then sits back and looks at the page without writing anything more, while the hanging lamp sways over the table, as the father turns a page of his newspaper across the table",'chanoma','behind','Q',None,None),
('G5','M5',"A_HAHA: the account book fills the bottom of the view open on the table, then their own hand turns to a clean page at the back, then stops with the pencil held above it and does not write, while the hanging lamp sways over the table",'chabudai','pov_hand','Q',None,None),
('G6','M5',"A_HAHA: the tatami room fills the view with the tea cabinet standing closed, then their own hands slide the doors open and take out the whole bundle of books and papers, then set the bundle down on the mat, while the shadow of the screen frame moves across the floor, as someone moves about in the next room beyond the paper screen",'zashiki','pov_stand','Q','Q','A_HAHA with the bundle of books and papers set down on the mat'),
('G7','M5',"A_HAHA: the bundle lies on the mat in the bottom of the view, then their own two hands spread the books and papers out across it, then move them apart one by one into a row, while the shadow of the screen frame moves across the mat, as the family go on with the day in the room beyond the screen",'zashiki','pov_sit','Q','Q','the books and papers spread out in a row on the mat'),
('G8','M5',"A_HAHA: the spread-out papers fill the bottom of the view, then their own hand turns over each one in the row in turn, then comes to the end of the row and rests on the bare mat, while the shadow of the screen frame moves across the mat, as someone moves about in the next room beyond the paper screen",'zashiki','pov_sit','Q','Q','A_HAHA with one hand resting on the bare mat at the end of the row'),
('G9','M5',"A_HAHA, seen from behind the whole time, kneels among the spread papers with her hands in her lap, then she gathers them back together into the bundle, then puts the bundle away in the cabinet and closes the doors, while the shadow of the screen frame moves across the wall, as the family go on with the day in the room beyond the screen",'zashiki','behind','Q','Q',None),
('G10','M5',"A_CHICHI sits at the low table with an official envelope open in front of him, then he takes the paper out of it and reads, then folds it and puts it back in the envelope, while the hanging lamp sways over the table, as the television murmurs in the corner",'chanoma','ots','Q',None,None),
('G11','M5',"A_HAHA: the low table fills the view with the father and the official envelope on it, then their own hand comes into the frame and turns the envelope round to face them, then rests beside it without opening it, while the hanging lamp sways over the table, as two of the family sit talking at the far end of the room",'chanoma','pov_sit','Q',None,None),
('G12','M5',"A_HAHA: the official paper fills the bottom of the view unfolded on the table, then their own finger goes along one printed line to the end of it, then stops and lifts away, while the hanging lamp sways over the table, as another pair of hands rests on the far edge of the table",'chabudai','pov_hand','Q',None,None),
('G13','M5',"A_HAHA: the tea cabinet drawer fills the view pulled half open, then their own hand lays the official envelope down flat inside it, then pushes the drawer shut over it, while the shadow of the screen frame moves across the cabinet, as someone moves about in the next room beyond the paper screen",'zashiki','pov_stand','Q',None,None),
('G14','M5',"A_HAHA and A_CHICHI sit on either side of the low table in the evening with the bowls cleared away, then they both look towards the television in the corner, then go on sitting without speaking, while the hanging lamp sways over the table, as the room goes on around them",'chanoma','wide','Q',None,None),
('G15','M5',"A_HAHA: the rice bin fills the view in the corner of the kitchen, then their own hand lifts the lid and goes down into the rice, then comes up with the folded notes and holds them, while the bare bulb over the worktop sways and the shadows move with it",'daidokoro','pov_stand','Q','S','A_HAHA holding the folded notes up out of the rice bin'),
('G16','M5',"A_HAHA: the folded notes lie in their own palm in the bottom of the view, then their own other hand adds one more note to them, then folds the whole set over once together, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','S','the folded set of notes held together in one palm'),
('G17','M5',"A_HAHA: the open rice bin fills the bottom of the view, then their own hand lays the folded set down on the rice, then draws a cloth across the top of it, while the bare bulb sways and the shadows move with it",'daidokoro','pov_hand','Q','S','the surface of the rice smoothed flat over the notes'),
('G18','M5',"A_HAHA, seen from behind the whole time, stands at the rice bin with the lid in her hands, then she sets the lid back on it, then rests both hands on the lid and stays there, while the bare bulb sways overhead and her shadow moves on the wall",'daidokoro','behind','Q','S',None),
('G19','M5',"A_HAHA: the veranda opens out ahead of the view onto the garden, then the view carries along the boards left to right, then stops at the cushion with the low hedge beyond it, while the hedge moves in the wind beyond the boards",'engawa','pov_look','Q',None,None),
('G20','M5',"A_HAHA, seen from behind the whole time, sits on the veranda cushion facing the garden, then she draws her knees in a little, then folds both hands together in her lap, while the hedge moves in the wind beyond the boards",'engawa','behind','Q',None,None),
('G21','M5',"A_HAHA: the garden fills the view from the veranda boards, then the view turns from the hedge along to the corner of the house, then comes back to their own hands resting in their own lap, while the hedge moves in the wind beyond the boards",'engawa','pov_sit','Q',None,None),
('G22','M5',"A_IMA: the notebook fills the bottom of the view open at the last written page, then their own hand moves down to the final line on it, then stops on the last word and stays, while the curtain at the window stirs",'ima_ie','pov_hand','Q','T','A_IMA with a finger resting on the last written line'),
('G23','M5',"A_IMA, seen from behind the whole time, sits at the table with the notebook open at that page, then he takes his glasses off and sets them down beside it, then sits back from the table, while the curtain at the wide window stirs",'ima_ie','behind','Q','T','A_IMA sitting back with the glasses set down beside the notebook'),
('G24','M5',"A_IMA: the last written page fills the bottom of the view, then their own hand turns it over onto the blank one, then stays flat on the blank paper without moving, while the curtain at the window stirs",'ima_ie','pov_hand','Q','T',None),
('G25','M5',"A_HAHA: the low table fills the bottom of the view with the account book closed on it, then their own two hands rest on the cover, then lift away and leave it there, while the hanging lamp sways over the table, as a hand reaches in from the far side and lifts the teapot away",'chabudai','pov_hand','Q',None,None),
('G26','M5',"A_HAHA, seen from behind the whole time, stands in the middle of the living room with the lamp above her, then she reaches up and pulls the cord, then stands on in the dimmed room, while the lamp swings a little on its cord after the pull",'chanoma','behind','Q',None,None),
('G27','M5',"A_HAHA: the kitchen fills the view in the morning with the worktop wiped bare, then the view turns along the bare worktop to the rice bin in the corner, then holds on the closed lid of it, while the light moves across the worktop",'daidokoro','pov_look','Q',None,None),
('G28','M5',"A_HAHA: the shopping street opens out ahead of the view in the daytime, then the view carries along the pavement left to right past the shopfronts, then stops where a new wide frontage stands among them, while the awnings move in the wind, as shoppers cross in both directions",'shotengai','pov_look','Q',None,None),
('G29','M5',"A_IMA: the modern room fills the view with the notebook lying open on the table, then the view turns from it to the window and the daylight there, then comes back down to the open page, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('G30','M5',"A_IMA: the table fills the bottom of the view with the notebook and a pair of glasses on it, then their own hand takes up the glasses and folds them, then sets them down on the closed cover, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('G31','M5',"A_HAHA: the veranda boards fill the view with the afternoon light lying across them, then the view turns along the boards to the empty cushion, then holds on it, while the hedge moves in the wind beyond the boards",'engawa','pov_look','Q',None,None),
('G32','M5',"A_HAHA: the garden beyond the veranda fills the view with the low hedge and the neighbouring roofs, then the view holds on the roofs, then comes back down to the boards at their own feet, while the hedge moves in the wind beyond the boards",'engawa','pov_stand','Q',None,None),
('G33','M5',"A_HAHA: the rice bin fills the view in the corner of the kitchen, then their own hand rests flat on the wooden lid of it, then lifts away and leaves it closed, while the light moves across the worktop",'daidokoro','pov_stand','Q',None,None),
]

# =====================================================================================
# KET 156-168 (13 clip) — 認める -> 裏返す -> xin 体験談 -> chu ky kenh
# =====================================================================================
S += [
('L0','KET',"A_IMA: the modern room opens out ahead of the view past the sofa, then the view carries across it left to right towards the window, then stops where the daylight comes in over the sill, while the curtain at the wide window stirs",'ima_ie','pov_look','Q',None,None),
('L1','KET',"A_HAHA: the low table fills the bottom of the view with one small envelope lying alone on it, then their own hand comes down and rests on the envelope, then lifts away and leaves it lying there, while the hanging lamp sways over the table, as a folded newspaper lies at the far edge of the table where someone set it down",'chabudai','pov_hand','Q',None,None),
('L2','KET',"A_HAHA: the shopping street fills the view at evening with the bulbs lit over it, then the view turns the whole length of the street, then settles on the fishmonger's empty slab, while the bare bulbs sway over the street, as the last shoppers go along the pavement",'shotengai','pov_look','Q',None,None),
('L3','KET',"A_HAHA: the kitchen worktop fills the view at night with the bare bulb over it, then the view turns from the empty worktop to the dark corner, then comes back to the bulb, while the bare bulb sways and the shadows move with it",'daidokoro','pov_look','Q',None,None),
('L4','KET',"A_HAHA: the doorway fills the view with the lane beyond the frosted glass, then their own hand slides the door to along its runner, then turns the catch down and lets go, while the shadow of the door frame moves across the floor",'genkansaki','pov_stand','Q',None,None),
('L5','KET',"A_HAHA, seen from behind the whole time, kneels alone at the low table with both books in front of her, then she squares them one on top of the other, then rests both hands flat on the pile, while the hanging lamp sways over the table, as the television murmurs to the family in the corner",'chanoma','behind','Q',None,None),
('L6','KET',"A_HAHA: the tea cabinet fills the view against the wall, then their own hands slide the wooden doors closed across it, then rest against the closed doors, while the shadow of the screen frame moves across the cabinet, as the family go on with the day in the room beyond the screen",'zashiki','pov_stand','Q',None,None),
('L7','KET',"A_HAHA: the veranda boards fill the view with the cushion set down on them, then the view holds on the empty cushion, then turns out to the garden beyond, while the hedge moves in the wind beyond the boards",'engawa','pov_look','Q',None,None),
('L8','KET',"A_IMA: the notebook lies closed on the modern table in the bottom of the view, then their own two hands take it up off the table, then hold it against their own chest, while the curtain at the window stirs",'ima_ie','pov_sit','Q','U','A_IMA holding the closed notebook against his chest'),
('L9','KET',"A_IMA, seen from behind the whole time, sits at the table holding the closed notebook, then he sets it down again in the middle of the table, then draws his hands back to the edge, while the curtain at the wide window stirs",'ima_ie','behind','Q','U',None),
('L10','KET',"A_HAHA: the living room fills the view with the lamp hanging low over the empty table, then the view holds on the table, then turns away to the paper screen with the light behind it, while the hanging lamp sways over the table, as the father sits back at the far side of the table with a folded newspaper",'chanoma','pov_look','Q',None,None),
('L11','KET',"A_HAHA: the rice bin stands closed in the corner of the kitchen in the view, then the view moves in along the worktop towards it, then stops with the bin filling the frame, while the light moves across the worktop",'daidokoro','pov_look','Q',None,None),
('L12','KET',"A_IMA: the modern table fills the bottom of the view with the old notebook lying closed in the middle of it, then the view holds on the cover, then lifts away to the window and the daylight there, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
]

# CUT tu dong: mot chuoi PHAI giu nguyen goc may (gate). Cho nao doi framing ma van
# cung (khoi, preset) thi CAT chuoi tai do — day la luat, khong phai tuy chon.
CUT = set()
_prev = None
for _x in S:
    if _prev is not None and _prev[1] == _x[1] and _prev[3] == _x[3] and _prev[4] != _x[4]:
        CUT.add(_x[0])
    _prev = _x
S = autochain(S, cut=CUT)

rows = build(S, P, C, prof=PROF, crowd=CROWD)
n_red, n_warn = gate(rows, S, P, C,
                     interior={"chanoma", "chabudai", "daidokoro", "zashiki",
                               "genkansaki", "ima_ie"},
                     strict=True, crowd=CROWD, prof=PROF)
act_report(S, C)
safe, risky, pct = linkage(S)
print("\nNOI AN TOAN: %d/%d moi noi cung boi canh co it nhat mot canh CHAT (%.0f%%)"
      % (safe, risky, pct))

pov = sum(1 for x in S if str(x[4]).startswith("pov"))
print("POV: %d/%d = %.0f%%" % (pov, len(S), pov * 100 / len(S)))
print("SO CANH: %d  (SLIDES can dung 176)" % len(S))

OUTDIR = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\15_haha-no-okane"
import os
os.makedirs(OUTDIR, exist_ok=True)
if n_red == 0:
    write_outputs(rows, OUTDIR, prof=PROF)
    print("\nXUAT -> %s\\videogen_FLOW.txt | _TENFILE.txt | _BLOCKS.md" % OUTDIR)
else:
    print("\n[CHAN] %d loi do — KHONG xuat file. Sua roi chay lai." % n_red)
