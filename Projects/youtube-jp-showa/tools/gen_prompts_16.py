# -*- coding: utf-8 -*-
"""Video 16 — 昭和の結婚の常識5選 (198 clip). Cong thuc duy nhat v2.

⛔ KHONG chep hang so. STYLE / MOTION / AVOID / FRAMING / EXTRAS deu lay tu videogen_lib.

BA THU KHAC VIDEO 15:
 1. ⭐ **Doi mat chinh doi nguoi: A_MUSUME** (co gai 23 tuoi, nguoi BI quyet dinh).
    Video 15 POV qua nguoi me vi bai do la "ban tay lam gi voi tien". Bai nay cau chot la
    「いちばん大きく人生が変わる側は、いちばん小さな声で返事をしていました」 => phai nhin
    bang mat cua chinh nguoi do, khong phai cua nguoi bay anh ra chieu.
 2. ⭐ **HIEN VAT XUYEN BAI: tam 見合い写真 + CAI HOP.** Kich ban v2 dung no lam xuong song
    (`16_omiai-kekkon.md` §2): mat sau co HAI dong but chi, va o muc 3 thi "anh cam hoa tien
    viec" nam cung mot hop voi no. Preset `ima_ie` = A_IMA (con gai, 70 tuoi) o thoi NAY mo
    chinh cai hop do — no la cai neo giua 5 muc.
 3. ⭐ **Ba boi canh moi so voi 15: `shashinkan` (hieu anh) · `office`/`soubetsu`/`office_rouka`
    (cong so, lay EXTRAS co san cua thu vien) · `yakusho` (cua so hanh chinh).**

🔴 BON RUI RO — biet truoc, khong phat hien lai:
 a. **TRANG PHUC DOI THEO BOI CANH la ke thu cua "nhan vat dong nhat".** Co gai mac 着物 luc
    xem mat va blouse+cardigan luc o nha/cong so. => **POV CHI dung o bo blouse+cardigan**;
    moi canh 着物 deu la shot NHIN TU NGOAI. Nhu vay than nguoi trong POV chi co MOT bo.
 b. POV la loai shot t2v hong nhieu nhat (`hands only` an 14/21 clip o video 10).
    => moi shot POV deu phai co THAN: pov / pov_sit / pov_stand; `pov_hand` chi khi that su
    chi con hai ban tay tren mot mat ban.
 c. ⛔ **CAM lich treo tuong va moi vat mang san mot thang so** (`ai-video-regen.md` §3:
    nhiet ke -> 75, luoi lich -> 1人/Mon Tue). Muc 4 noi ve TUOI nen rat de bi keo ve phia
    ve mot cuon lich — tuyet doi khong.
 d. ⛔ **CAM can canh doc duoc chu tren 釣書 / 就業規則 / 通帳.** Vua la bia hien vat, vua dinh
    `feedback_so_tren_hinh_phai_do_font_ve`. Giay to luon quay goc nghieng hoac dang bi tay lat.

📌 Thu tu chay: make_voice_16.py -> build_slides_16.py -> file nay.
   So canh = so clip cua SLIDES (220, TRAN 7,0s), doc o `06_VIDEO/16_omiai-kekkon/clips/_MAP.txt`.
   Khoi: HOOK 16 · INTRO 3 · M1 37 · M2 32 · M3 37 · CTA 6 · M4 29 · BRIDGE 4 · M5 39 · KET 10 · OUTRO 7
"""
import sys
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from videogen_lib import build, gate, write_outputs, autochain, linkage, act_report
import videogen_lib as _V

# =====================================================================================
# P — BOI CANH. Ten khoa trung khoa EXTRAS cua videogen_lib de an dung lop nguoi nen.
# =====================================================================================
P = {
 "chanoma":    'the living room of a Showa house in the evening, a low round wooden dinner table in the middle of the tatami with flat floor cushions round it, a fluorescent ceiling light with a small glass shade and a long pull cord, a black rotary dial telephone on its own low stand, a wooden tea cabinet with sliding glass doors, a boxy wooden television standing on legs with wooden doors over the screen, a small household shrine shelf high on one wall, sliding paper screens along one side',
 "chabudai":   'the top of a low round wooden dinner table in a Showa living room under a pull-cord fluorescent lamp, the grain worn pale in the middle, a lacquered tea tray with a squat teapot and small handleless cups pushed to one side',
 "zashiki":    'the formal tatami room of a Showa house in the daytime, a shallow alcove with a plain hanging scroll and a single flower in a heavy vase, a dark wooden household altar in the corner, a low tea cabinet against the wall, paper screens pushed back onto the garden letting flat daylight in',
 "daidokoro":  'the kitchen of a Showa house at night, a tiled worktop and a deep concrete sink, a two-ring gas burner with a blackened kettle on it, open shelves of enamel bowls and tin canisters, a wooden rice bin standing in the corner, one bare bulb over the worktop and the rest of the room in shadow',
 "genkansaki": 'the doorway of a Showa house seen from just inside, a sunken concrete entrance floor with wooden sandals and lace-up shoes set out on it, a wooden shoe cabinet against the wall, a frosted glass sliding door half open onto the lane, the wooden corridor going back into the house',
 "michi":      'a narrow Showa residential lane in the evening, wooden fences and low gates on both sides, a telegraph pole with a fire bell box on it, a round red postbox at the corner, the lit windows of the houses going away down the lane',
 "shotengai":  'a Showa shopping street in the early evening, cloth awnings out over the pavement, a greengrocer with goods in wooden crates, plain unmarked split curtains hanging in the shop doorways, women carrying woven bamboo shopping baskets, bare bulbs strung over the street',
 "engawa":     'the wooden veranda of a Showa house in the late afternoon, the paper screens pushed back onto the garden, a flat cushion set down on the boards, a bamboo laundry pole and a stone water basin in the garden, the low hedge and the neighbouring tiled roofs beyond',
 # ⭐ moi so voi video 15
 "shashinkan": 'the inside of a small Showa portrait studio, a plain pale cloth backdrop hung down the far wall, a heavy plate camera on a wooden tripod facing it, two tall lamps on stands with their shades turned in, a single carved chair set in the middle of the bare floor, a dark curtain drawn across the doorway at the side',
 "office":     'the open floor of a Showa company office in the daytime, grey steel desks pushed together face to face in long rows, a mechanical calculator and a black rotary dial telephone on each row, stacked paper trays and a glass ashtray, a low partition down the middle of the floor, tall metal cabinets along the wall and wide windows with venetian blinds',
 "office_rouka":'the corridor of a Showa office building, a worn linoleum floor and painted plaster walls, frosted glass doors along one side, a metal window frame at the far end letting flat daylight down the length of it',
 "soubetsu":   'a cleared corner of a Showa office floor in the late afternoon, the desks pushed back to make a space, a low table with cups and a plate set out on it, the venetian blinds half down at the windows behind',
 "yakusho":    'the public counter of a Showa town hall, a long wooden counter running the width of the room with low partitions along it, rows of steel desks and shelves of bound files behind the staff side, hard chairs against the wall on the public side, high windows letting flat daylight in',
 "ima_ie":     'a present-day Japanese living room, a low sofa and a plain table, a flat window with a plain curtain, everyday daylight, nothing on the table but one old photograph and a flat lidded box',
}

# =====================================================================================
# C — DAN DIEN.
#  ⭐ A_MUSUME la doi mat chinh. Xem RUI RO (a): POV CHI o bo blouse+cardigan.
# =====================================================================================
C = {
 # =====================================================================================
 # ⭐ MOI CAST = KHUON MAT (khong doi ca video) + DO MAC (doi theo boi canh).
 #
 # 🔴 VI SAO PHAI TA MAT (user bat 2026-09-18: "mat cac nhan vat gan giong cac video cu"):
 #    Ban dau cua file nay — va CA video 13/14/15 — chi ta QUAN AO. Do bang may:
 #    32/32 cast khong mot chu nao ve khuon mat (`tools/check_cast_unique.py`).
 #    Model khong duoc cho mat nao thi no dung MAT MAC DINH cua phong cach => video 13 va 14
 #    quan ao khac hoan toan ma mat van giong nhau. **Doi quan ao khong chua duoc benh nay.**
 #
 # 🔴 Va `haha`/`chichi` ban cu con CHEP NGUYEN VAN tu video 15 (tung ky tu) — nen o day
 #    doi CA DO, khong chi them mat.
 #
 # ⚖️ Gioi han biet truoc: t2v KHONG khoa duoc mat. Ta mat chi keo phan bo ve mot vung khac
 #    giua cac video va giu mot video khoi troi; thu khoa duoc danh tinh that su van la
 #    giau mat / canh xa / quay lung / POV.
 # =====================================================================================

 # ⭐ co gai — POV chinh. Xem RUI RO (a): POV CHI o bo blouse+cardigan.
 "musume":          'a young woman of about twenty-three with a long narrow face, a small pointed chin, thin straight eyebrows set low over quiet deep-set eyes and pale skin, her hair set in a short neat wave, wearing a plain white round-collared blouse under a soft pale cardigan and a dark knee-length skirt',
 "musume_pov":      "their own forearms in the pushed-back sleeves of a pale cardigan and the white blouse front on their own chest",
 "musume_pov_sit":  "their own forearms in the pushed-back sleeves of a pale cardigan, the white blouse front on their own chest, and their own knees and the dark skirt across the bottom of the picture",
 "musume_pov_stand":"their own forearms in the pushed-back sleeves of a pale cardigan and the white blouse front on their own chest",
 "musume_pov_hand": 'their own smooth young forearms in pale cardigan cuffs and the backs of their own hands, the nails short and unpainted',
 "musume_pov_walk": 'only their own hand or hands where the work needs them, a pale cardigan cuff at the edge',
 # ⚠️ ban 着物 — CUNG MOT KHUON MAT, chi doi do. KHONG bao gio dung cho POV (RUI RO a)
 "musume_kimono":   'the same young woman of about twenty-three with a long narrow face, a small pointed chin, thin straight eyebrows set low over quiet deep-set eyes and pale skin, her hair pinned up, wearing a formal patterned kimono with a wide stiff sash, sitting very straight',
 # gia dinh
 "haha":    'a woman in her forties with a broad square face, high flat cheekbones, thick straight eyebrows and narrow eyes with deep smile lines at the corners, a short blunt nose, her greying hair pulled back into a low knot, wearing a plain grey wrap-around apron over a long-sleeved blouse with the sleeves held back by a cord',
 "chichi":  'a man in his forties with a lean angular face, hollow cheeks and a heavy jaw, bushy eyebrows and a high forehead with a receding hairline, wearing an open-necked shirt with the collar worn outside a dark knitted vest and loose dark trousers',
 # cap vo chong lam mai — bai nay ho KHONG co ten, va do la NOI DUNG (§muc 2)
 "nakoudo_f": 'a woman in her fifties with a round full face, soft heavy jowls, thin high-arched eyebrows over small narrow eyes and a flat wide nose, her hair pinned back tight, wearing a subdued formal kimono with a dark haori jacket over it',
 "nakoudo_m": 'a man in his fifties with a wide heavy face, a thick neck and a broad flat nose, bushy eyebrows and deep lines running from the nose to the corners of the mouth, his hair oiled flat, wearing a dark double-breasted suit with wide lapels and a plain tie',
 # ben nha trai
 "muko":    'a young man of about twenty-six with a soft round face, full cheeks and a weak chin, low thick eyebrows over wide-set eyes and a small mouth, his hair cut short and combed to one side, wearing a dark suit that sits slightly loose on him and a plain tie',
 # cong so
 "joushi":  'a man in his fifties with a long bony face, a heavy jaw and hollow temples, sparse eyebrows over heavy eyelids and grey stubble on the chin, wearing a white shirt with the sleeves rolled and a loosened tie, reading glasses pushed up on his forehead',
 "douryou": 'a young woman of about twenty-five with a small heart-shaped face, a pointed chin, high round eyebrows over large round eyes and freckles across the nose, her hair tied back with a plain band, wearing a plain blouse and a dark pinafore work apron over it',
 # thoi NAY — nguoi chung nhan cam tam anh
 "ima":          'a woman in her seventies with a small thin face, deep vertical lines round the mouth, sparse grey eyebrows over heavy-lidded eyes and thin white hair combed back, wearing a plain knitted cardigan over a soft collared blouse',
 "ima_pov":      'their own thin freckled forearms with raised veins and loose papery skin, and a knitted cardigan sleeve at the edge',
 "ima_pov_sit":  'their own thin freckled forearms with raised veins and loose papery skin, a knitted cardigan on their own chest, and their own knees and lap across the bottom of the picture',
 "ima_pov_hand": 'their own thin freckled forearms and the backs of their own hands, the skin loose and papery over raised veins, the nails short and unpainted, knitted cardigan cuffs at the edge',

}

# =====================================================================================
# CROWD — lop nguoi nen.
# =====================================================================================
CROWD = {
 "shotengai":   "full",
 "michi":       "few",
 "genkansaki":  "few",
 "office":      ("full", "cong so gio lam — dong la NOI DUNG cua muc 3"),
 "office_rouka":("full", "hanh lang tien viec — ⭐ canh dat nhat muc 3, phai DONG"),
 "soubetsu":    ("full", "ca tang vay quanh — day la 'me man' cua tu 寿退社"),
 "yakusho":     ("few",  "quay hanh chinh — vai nguoi cho, khong the vang"),
 "chanoma":     ("few",  "trong nha — ca gia dinh"),
 "chabudai":    ("few",  "can canh mat ban — VAN phai thay tay/chen cua nguoi nha o ria"),
 "daidokoro":   ("solo", "bep DEM — mot minh la NOI DUNG"),
 # 🔴 zashiki PHAI 'solo' — KHONG phai vi muon canh vang, ma vi EXTRAS cua key nay duoc viet
 # cho canh NGU ("lying on the same bedding under the same net"). Bat len 'few' thi canh
 # 結納 ban ngay bi chen them nguoi nam ngu duoi man. Da dinh that o video 15.
 # Nguoi trong phong o day viet TAY trong tung canh.
 "zashiki":     ("solo", "EXTRAS cua key nay ta canh NGU — xem ghi chu"),
 "shashinkan":  ("solo", "hieu anh — khong co EXTRAS; nguoi viet tay trong act"),
 "engawa":      ("solo", "hien nha — khoang lang cuoi bai"),
 "ima_ie":      ("solo", "thoi NAY — mot nguoi, mot tam anh, do la LUAN DIEM"),
}

# =====================================================================================
# PROF — STYLE rieng, giu nguyen co che cua video 15 (user chot 2026-09-17 "mau phim hoai co hon")
#
# 🔴 GUARD nam o ~2% dau prompt (`ai-video-regen.md` §2: cam cai gi thi phai cam o 15% DAU).
#    Phep thu 10 clip o video 15 da do duoc: guard o 70% prompt => 5/10 clip co vien phim.
#
# 🔴 VONG SUA CUA GUARD — hoc thang tu video 15: ban dau no cam CA CHU VIET TAY, ma o bai nay
#    HAI DONG BUT CHI o mat sau tam anh chinh la xuong song (§2). Tach PRINTED (bien hieu,
#    nhan, bang ron) khoi HANDWRITING (but chi mat sau anh, but long tren 釣書) — chu viet tay
#    duoc phep TON TAI nhung phai mo va khong doc ra.
# =====================================================================================
GUARD = ("The picture is a clean rectangle that runs right out to all four edges: "
         "no film border, no sprocket holes, no rounded corners, no black frame and no strip "
         "of any kind around the image. No printed lettering anywhere in the picture: no shop "
         "signs with writing, no banners, no printed labels, no printed text on any wall, box "
         "or packet, and no calendar and no clock face anywhere. The one exception is the soft "
         "handwriting on the back of the photograph and on the folded papers themselves, which "
         "is faint, uneven and far too small to read. ")

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
# HOOK 000-015 (16 clip / 47,7s = 3,0s moi canh)
#
# ⭐ Bai hoc thang tu video 15: cold open KHONG duoc toan can canh tay tren mat ban.
#    Phan bo o day: 6 wide · 3 medium · 2 high/low · 2 ots/behind · 3 pov.
#    Ba cu soc (H8-H9-H10 = 仲人 / 結納 / 送別) la BA BOI CANH KHAC NHAU, deu co NGUOI.
# =====================================================================================
S += [
('H0','HOOK',"A_NAKOUDO_F comes in from the corridor into the living room holding a flat paper envelope in both hands, then she kneels down at the low table where the family are sitting, then lays the envelope down in the middle of the table, while the hanging lamp sways over the table, as the family go on in the room behind",'chanoma','wide','Q',None,None),
('H1','HOOK',"A_HAHA draws a single photograph out of the flat envelope on the low table, then she turns it the right way round, then sets it down on the tatami in front of the others, while the hanging lamp sways over the table, as the father sits back at the far side of the table",'chanoma','medium','Q',None,None),
('H2','HOOK',"A_MUSUME: the photograph lies on the tatami below the view with the family's hands around the edge of it, then their own hand comes down and turns it a little straighter, then draws back to their own knee, while the hanging lamp sways over the table, as the rest of the family go on talking above",'chanoma','pov_sit','Q',None,None),
('H3','HOOK',"A_MUSUME sits back on her heels at the low table looking down at the photograph, seen over her shoulder the whole time, then she leans in a little towards it, then sits back again without picking it up, while the hanging lamp sways over the table, as her father sits across the table with his arms folded",'chanoma','ots','Q',None,None),
('H4','HOOK',"A_MUKO sits alone on the carved chair in front of the pale backdrop facing the camera on its tripod, then he squares his shoulders and puts his hands flat on his knees, then holds still, while the lamps on their stands glow steadily at both sides, as a studio assistant steps back out of the way beside the tripod",'shashinkan','wide','Q',None,None),
('H5','HOOK',"A_IMA walks in across the bright modern room left to right across the frame carrying a flat lidded box in both hands, then she sits down at the plain table, then sets the box down and lifts the lid off, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H6','HOOK',"A_IMA: the open box lies below the view on the plain table with old photographs stacked inside it, then a pair of hands lifts the top photograph out, then holds it flat above the box, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('H7','HOOK',"A_MUSUME kneels at the low table with the photograph in front of her, then she looks up across the table at her mother, then looks back down at it and says nothing, while the hanging lamp sways over the table, as the family go on around her",'chanoma','medium','Q',None,None),
('H8','HOOK',"A_NAKOUDO_M stands on the step at the half-open frosted door with his hat in one hand, then he bows in towards the house, then steps up onto the wooden floor, while the shadow of the door frame moves across the floor, as a neighbour goes past along the lane behind him",'genkansaki','wide','Q',None,None),
('H9','HOOK',"A_NAKOUDO_M carries a plain white wooden tray of wrapped gifts in both hands across the formal room, then he lowers it to the floor in front of the alcove, then draws back and kneels beside it, while the paper screens stir in the draught and the shadows shift across the tatami, as the two families kneel facing each other on either side of the room",'zashiki','wide','Q',None,None),
('H10','HOOK',"A_MUSUME walks left to right across the frame along the cleared corner of the office floor carrying a wrapped bunch of flowers in both arms, then she turns to face the room, then bows to the people standing round her, while the blinds move at the windows behind, as the whole floor stands gathered in a ring around her",'soubetsu','wide','Q',None,None),
('H11','HOOK',"A_IMA: the photograph lies face up in the bottom of the view on the plain table, then their own hand turns it over onto its back, then flattens it down with two fingers, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('H12','HOOK',"A_IMA: the back of the photograph fills the view with two faint pencil lines written across it, then the view moves down from the upper line to the lower one, then comes back up to the upper line again, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('H13','HOOK',"A_IMA sits back from the plain table with the photograph held in both hands, then she lowers it to the table, then rests both hands flat on either side of it, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H14','HOOK',"A_MUSUME: the low table fills the bottom of the view with the photograph lying on the tatami beyond it, then their own hands come together in their own lap, then stay folded there, while the hanging lamp sways over the table, as the family go on talking around the table",'chanoma','pov_sit','Q',None,None),
('H15','HOOK',"A_CHICHI sits at the far side of the low table with his arms folded looking down at the photograph, then he unfolds his arms and reaches out to it, then draws his hand back without touching it, while the hanging lamp sways over the table, as the mother and daughter sit on at the table",'chanoma','low','Q',None,None),
]

# =====================================================================================
# INTRO 016-018 (3 clip) — chao + hua "cung lat tam anh" + nhac lai LOOP
# =====================================================================================
S += [
('A0','INTRO',"A_IMA sits back from the plain table with the photograph lying face up in front of her, then she turns it round so it faces across the table, then rests both hands on the edge of the table, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('A1','INTRO',"A_MUSUME: the living room opens out ahead of the view from the corridor door, then the view carries in along the tatami left to right across the frame, then stops at the low table with the photograph lying on it, while the hanging lamp sways over the table, as the family go on in the room",'chanoma','pov_look','Q',None,None),
('A2','INTRO',"A_IMA: the plain table lies below the view with the photograph and the open box on it, then a pair of hands sets the photograph down beside the box, then squares it to the edge of the table, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
]

# =====================================================================================
# MUC 1 — 相手は、写真と紙で決まる (019-052, 34 clip)
#   nhip: 仲人 mang do den -> 釣書 -> hieu anh -> bay len chieu -> bo im lang -> cau tra loi nho
#         -> 家制度 da chet nam 1948 ma cam giac van song -> so lieu 59,8%
# =====================================================================================
S += [
('B0','M1',"A_NAKOUDO_F kneels at the low table and takes a flat paper envelope out of a cloth wrapper, then she slides a photograph and a folded paper out of it, then lays them side by side on the table, while the hanging lamp sways over the table, as the family sit round the table watching",'chanoma','medium','Q','B','A_NAKOUDO_F kneeling with the photograph and the folded paper laid out'),
('B1','M1',"A_MUSUME: the low table fills the bottom of the view with a photograph and a folded paper lying on it, then their own hand draws the photograph a little closer, then stops with one finger still resting on its edge, while the hanging lamp sways over the table, as the others go on talking above the table",'chanoma','pov_sit','Q','B',None),
('B2','M1',"A_HAHA unfolds the long folded paper out flat across the low table, then she smooths it down with the side of her hand, then turns it round towards her husband, while the hanging lamp sways over the table, as the daughter sits on the other side of the table",'chabudai','high','Q','C','A_HAHA with the long paper unfolded flat on the table'),
('B3','M1',"A_CHICHI takes the long unfolded paper up off the table in both hands, then he holds it out at arm's length to read it, then lowers it flat to the table again, while the hanging lamp sways over the table, as the mother kneels beside him at the table",'chabudai','medium','Q','C','A_CHICHI holding the long paper out in both hands'),
('B4','M1',"A_MUSUME: the unfolded paper fills the bottom of the view at a low angle with columns of brush writing running down it, then the view moves along it from one end to the other across the frame, then comes back and stops halfway, while the hanging lamp sways over the table",'chabudai','pov_look','Q',None,None),
('B5','M1',"A_MUKO walks in through the side curtain of the portrait studio left to right across the frame to the carved chair, then he sits down on it facing the camera, then straightens his tie, while the lamps glow steadily on their stands, as the studio assistant moves the tripod a little at the side",'shashinkan','wide','Q','D','A_MUKO seated on the carved chair facing the camera'),
('B6','M1',"the studio photographer, a man in his sixties in a waistcoat with his sleeves rolled, leans in behind the plate camera under a dark cloth, then he comes back out from under it, then raises one hand towards the chair, while the lamps glow steadily at both sides, as the young man sits waiting on the chair",'shashinkan','medium','Q','D','the photographer standing back from the camera with one hand raised'),
('B7','M1',"A_MUKO sits very straight on the carved chair in front of the pale backdrop, then he puts both hands flat on his knees, then holds completely still, while the lamps glow steadily at both sides, as the photographer's arm stays raised at the edge of the room",'shashinkan','wide','Q','D','A_MUKO holding still on the chair with his hands on his knees'),
('B8','M1',"A_MUSUME_KIMONO sits on the same carved chair in front of the pale backdrop with her hands folded in her lap, then she lifts her chin a little, then holds still, while the lamps glow steadily at both sides, as the photographer stands back beside the tripod",'shashinkan','low','Q',None,None),
('B9','M1',"A_MUSUME_KIMONO sits on the carved chair seen from the waist up, then she turns her face towards the camera, then looks straight ahead and holds it, while the lamps glow steadily at both sides, as the photographer's hand comes into the edge of the picture and goes out again",'shashinkan','medium','Q',None,None),
('B10','M1',"A_HAHA kneels on the tatami and lays out three photographs in a row on the mat in front of her, then she shifts the middle one forward out of the line, then sits back on her heels to look at them, while the hanging lamp sways over the table, as the rest of the family sit on around the low table",'chanoma','high','Q','E','A_HAHA kneeling with three photographs laid out on the mat'),
('B11','M1',"A_CHICHI sits back from the low table with his arms folded looking down at the row of photographs, then he leans forward over them, then folds his arms again without saying anything, while the hanging lamp sways over the table, as the mother kneels by the photographs",'chanoma','medium','Q','E','A_CHICHI sitting back with his arms folded over the row of photographs','cool'),
('B12','M1',"A_MUSUME: the three photographs lie in a row on the tatami below the view, then their own hand moves across above them from the first to the last, then comes back and stops over the middle one, while the hanging lamp sways over the table, as the parents go on talking above the view",'chanoma','pov_sit','Q','E',None),
('B12b','M1',"A_HAHA kneels over the row of photographs on the tatami and turns one of them face down, then she sets it aside from the others, then draws the remaining two closer together, while the hanging lamp sways over the table, as the father sits back at the far side of the table",'chanoma','high','Q',None,None),
('B12c','M1',"A_MUSUME: the two remaining photographs lie side by side on the tatami below the view, then their own hand moves from one to the other and back, then settles flat on the mat between them, while the hanging lamp sways over the table, as the parents go on talking above the view",'chanoma','pov_sit','Q',None,None),
('B13','M1',"A_MUSUME kneels at the end of the low table with the photographs in front of her, seen over her shoulder the whole time, then she lifts her head towards her parents, then lowers it again to the photographs, while the hanging lamp sways over the table, as her mother and father sit on at the table",'chanoma','ots','Q',None,None),
('B14','M1',"A_MUSUME sits very still on the tatami seen from the chest up, then she opens her mouth to say something, then closes it and looks down, while the hanging lamp sways over the table, as her parents sit on either side of the picture",'chanoma','medium','Q',None,None,'cool'),
('B15','M1',"A_HAHA gathers the three photographs up off the tatami one after another, then she squares them into a stack, then slides the stack back into the flat envelope, while the hanging lamp sways over the table, as the father gets up and goes out of the room behind her",'chanoma','medium','Q',None,None),
('B16','M1',"A_IMA: the old photograph lies flat in the bottom of the view on the modern table, then their own thumb runs along its worn corner, then turns it a little into the light, while the curtain at the window stirs",'ima_ie','pov_hand','Q','F','the old photograph turned into the light on the modern table'),
('B17','M1',"A_IMA sits at the plain table holding the old photograph up in both hands, then she tilts it towards the window, then lowers it to the table again, while the curtain at the wide window stirs",'ima_ie','medium','Q','F',None),
('B18','M1',"A_IMA: the face of the photograph fills the view with fine scratches across its surface, then the view moves slowly across it from one side to the other, then stops at the worn rounded corner, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('B19','M1',"A_NAKOUDO_F kneels at the low table talking across it with both hands resting on her knees, then she lifts one hand towards the photograph, then sets it back on her knee, while the hanging lamp sways over the table, as the parents kneel opposite her",'chanoma','ots','Q',None,None),
('B20','M1',"A_CHICHI stands in front of the household shrine shelf high on the living room wall, then he claps his hands twice in front of it, then bows his head, while the hanging lamp sways over the table behind him, as the family go on in the room behind him",'chanoma','low','Q',None,None),
('B21','M1',"A_MUSUME: the dark wooden altar stands in the corner of the formal room ahead of the view, then the view carries slowly towards it across the tatami, then stops in front of the row of small standing tablets, while the paper screens stir in the draught and the shadows shift across the floor",'zashiki','pov_look','Q',None,None),
('B22','M1',"A_HAHA kneels in front of the altar in the corner of the formal room, then she sets a small cup down on the ledge of it, then presses her hands together, while the paper screens stir in the draught and the shadows shift across the tatami, as the daughter kneels a little way back in the same room",'zashiki','medium','Q',None,None),
('B23','M1',"a clerk in a grey work jacket behind the town hall counter takes a bound ledger down from the shelf, then he opens it flat on the counter, then turns it round towards the public side, while the shadows of the window frames shift along the counter and the papers stir, as two or three people wait along the counter further down",'yakusho','medium','Q','G','the bound ledger lying open on the counter'),
('B24','M1',"A_CHICHI stands at the town hall counter with the open ledger in front of him, then he leans down over it, then straightens up and puts his hat back on, while the shadows of the window frames shift along the counter and the papers stir, as other people stand waiting further along the counter",'yakusho','wide','Q','G',None),
('B25','M1',"A_MUSUME: the long wooden counter runs across the bottom of the view with a bound ledger open on it, then their own hand comes down flat on the page in place, then draws back to the edge of the counter, while the shadows of the window frames shift along the counter and the papers stir, as somebody waits at the next partition along",'yakusho','pov_stand','Q',None,None),
('B26','M1',"a plain wooden nameplate is fixed beside the gatepost of a Showa house, then the shadow of the gate moves slowly across it, then a hand reaches in and straightens it, while the shadows shift along the fence and the dust stirs in the lane, as two neighbours talk at a gate further down the lane",'michi','medium','Q',None,None),
('B27','M1',"A_MUSUME walks down the narrow lane away from the view towards the lit windows at the far end, then she stops at a gate, then pushes it open and goes through, while the lit windows go on down the lane, as neighbours walk home along the street behind her",'michi','behind','Q',None,None),
('B28','M1',"A_HAHA kneels at the low table with the tea tray in front of her, then she pours from the squat teapot into two small cups, then sets the pot down and pushes one cup across the table, while the hanging lamp sways over the table, as the family go on around the table",'chabudai','high','Q',None,None,'warm'),
('B29','M1',"A_NAKOUDO_F takes the small cup up from the table in both hands, then she drinks from it, then sets it down and says a few words across the table, while the hanging lamp sways over the table, as the parents kneel across the table from her",'chabudai','medium','Q',None,None,'warm'),
('B30','M1',"A_MUSUME_KIMONO sits on her heels in the formal room facing the alcove, then she lowers her head, then raises it again very slowly, while the paper screens stir in the draught and the shadows shift across the tatami, as her mother kneels a little way behind her in the same room",'zashiki','wide','Q',None,None),
('B31','M1',"A_MUSUME: the photographs lie in a row on the tatami below the view again, then their own hand pushes one of them slightly forward out of the line, then rests flat on the mat beside it, while the hanging lamp sways over the table, as her parents go on above the view",'chanoma','pov_sit','Q',None,None),
('B32','M1',"A_HAHA kneels at the low table and slides the flat envelope back into the tea cabinet, then she pushes the wooden door of it shut, then turns back to the room, while the hanging lamp sways over the table, as the family go on with the evening behind her",'chanoma','medium','Q',None,None),
('B32b','M1',"A_MUSUME stands at the paper screen at the side of the living room, then she slides it half open onto the dark corridor, then stands looking out through the gap, while the hanging lamp sways over the table behind her, as the family go on in the room behind her",'chanoma','medium','Q',None,None,'cool'),
('B33','M1',"A_MUSUME sits alone at the end of the low table after the others have moved away, then she looks down at the empty tatami where the photographs were, then folds her hands in her lap, while the hanging lamp sways over the table, as one of the family moves about at the far end of the room",'chanoma','wide','Q',None,None,'cool'),
]

# =====================================================================================
# MUC 2 — 結婚には、仲人が要る (053-080, 28 clip)
#   nhip: 仲人 di lai giua hai nha -> quyet ngay -> 結納 (白木の台・するめ・昆布・末広) ->
#         床の間 -> chen tra khong ai cham -> "khong ai nho ten" -> vai tro dem
# =====================================================================================
S += [
('C0','M2',"A_NAKOUDO_M walks along the narrow lane towards the view with his hat in one hand and a cloth-wrapped bundle under the other arm, then he stops at a gate, then turns in through it, while the lit windows go on down the lane, as neighbours walk home along the street behind him",'michi','wide','Q',None,None),
('C1','M2',"A_NAKOUDO_F steps up from the sunken entrance floor onto the wooden corridor, then she turns and kneels to set her shoes straight behind her, then stands and goes on into the house, while the shadow of the door frame moves across the floor, as a neighbour passes along the lane outside",'genkansaki','medium','Q',None,None),
('C2','M2',"A_MUSUME: the doorway fills the view with the go-between couple standing just inside it, then they both bow towards the view, then straighten and step up onto the corridor, while the shadow of the door frame moves across the floor",'genkansaki','pov','Q',None,None),
('C3','M2',"A_NAKOUDO_M kneels at the low table opposite the parents and takes a small notebook out of his jacket, then he opens it flat on the table, then runs one finger down the open page, while the hanging lamp sways over the table, as the mother and father kneel across the table",'chabudai','high','Q','H','A_NAKOUDO_M with the small notebook open on the table'),
('C4','M2',"A_CHICHI leans in over the small open notebook on the low table, then he taps one place on the page with his finger, then sits back on his heels, while the hanging lamp sways over the table, as the go-between kneels across the table from him",'chabudai','medium','Q','H',None),
('C5','M2',"A_MUSUME: the low table lies below the view with the small notebook open on it, then a hand comes in from the far side and turns the page over, then withdraws, while the hanging lamp sways over the table, as the voices go on around the table",'chabudai','pov_sit','Q',None,None),
('C6','M2',"A_NAKOUDO_M carries the plain white wooden tray in both hands the whole length of the corridor, then he turns in through the screen door of the formal room, then lowers the tray to the tatami, while the paper screens stir in the draught and the shadows shift across the floor, as the family kneel waiting inside the room",'zashiki','behind','Q','I','A_NAKOUDO_M kneeling with the white tray set down on the tatami'),
('C7','M2',"A_NAKOUDO_M kneels behind the white wooden tray and lifts a wrapped dried package off it, then he sets it down on the mat in front of the alcove, then reaches back for the next one, while the paper screens stir in the draught and the shadows shift across the tatami, as both families kneel facing each other along the sides of the room",'zashiki','medium','Q','I','A_NAKOUDO_M kneeling behind the tray with one package set down in front of the alcove'),
('C8','M2',"A_NAKOUDO_M lifts a folded paper fan off the white tray, then he opens it halfway, then lays it down beside the wrapped packages in front of the alcove, while the paper screens stir in the draught and the shadows shift across the tatami, as the two families kneel on either side of the room",'zashiki','medium','Q','I','the opened fan lying beside the wrapped packages'),
('C9','M2',"A_MUSUME: the row of wrapped packages and the opened fan lie on the tatami below the view in front of the alcove, then the view moves slowly along them from one end to the other, then stops on the fan, while the paper screens stir in the draught and the shadows shift across the floor",'zashiki','pov_look','Q',None,None),
('C9b','M2',"A_NAKOUDO_F kneels beside the white wooden tray and straightens the wrapped packages in their row, then she draws back onto her heels, then folds her hands in her lap, while the paper screens stir in the draught and the shadows shift across the tatami, as both families kneel facing each other in the room",'zashiki','medium','Q',None,None),
('C9c','M2',"A_MUSUME_KIMONO kneels at the side of the formal room looking towards the tray of gifts, then she lowers her eyes to the tatami in front of her, then raises them again to the alcove, while the paper screens stir in the draught and the shadows shift across the floor, as the two families kneel along both sides of the room",'zashiki','medium','Q',None,None),
('C10','M2',"A_NAKOUDO_F kneels at the side of the formal room facing the alcove, then she bows low with both hands flat on the tatami, then straightens up again, while the paper screens stir in the draught and the shadows shift across the floor, as the families kneel in two lines on either side of the room",'zashiki','wide','Q',None,None),
('C11','M2',"A_CHICHI kneels facing the other family across the room, then he bows low with both hands on the mat, then sits up straight again, while the paper screens stir in the draught and the shadows shift across the tatami, as his wife and daughter kneel in line beside him",'zashiki','medium','Q',None,None),
('C12','M2',"A_MUSUME_KIMONO kneels at the end of the line with her hands folded in her lap, then she bows her head, then raises it again very slowly, while the paper screens stir in the draught and the shadows shift across the tatami, as the two families kneel facing each other in the room",'zashiki','wide','Q',None,None),
('C13','M2',"A_HAHA carries a lacquered tea tray of small cups into the formal room, then she kneels and sets it down at the edge of the group, then withdraws her hands into her lap, while the paper screens stir in the draught and the shadows shift across the tatami, as both families kneel in place round the room",'zashiki','medium','Q','J','A_HAHA kneeling with the tea tray set down beside her'),
('C14','M2',"A_MUSUME: the tea tray lies on the tatami below the view with the small cups full and untouched, then the view moves slowly across the row of cups, then stops without any hand coming into the picture, while the paper screens stir in the draught and the shadows shift across the floor",'zashiki','pov_look','Q','J',None),
('C15','M2',"the two families kneel facing each other in the formal room with the tea cups set out between them, then nobody moves for a long moment, then one of them shifts a little on their heels, while the paper screens stir in the draught and the shadows shift across the tatami, as everyone in the room stays kneeling in place",'zashiki','wide','Q',None,None),
('C16','M2',"A_NAKOUDO_M kneels between the two families and spreads both hands a little apart, then he turns his head from one side of the room to the other, then brings his hands back to his knees, while the paper screens stir in the draught and the shadows shift across the tatami, as both families kneel facing each other",'zashiki','medium','Q',None,None),
('C17','M2',"A_NAKOUDO_F stands at the half-open frosted door with her back to the house, then she bows in towards the corridor, then steps down into the sunken entrance, while the shadow of the door frame moves across the floor, as a neighbour stands out in the lane behind her",'genkansaki','behind','Q',None,None),
('C18','M2',"A_NAKOUDO_M walks away down the narrow lane with his hat back on his head, then he turns the corner by the round postbox, then goes on out of sight, while the lit windows go on down the lane, as neighbours walk home along the street",'michi','wide','Q',None,None),
('C19','M2',"A_IMA sits at the plain modern table with the old photograph in front of her, then she turns her palms up on the table, then lets them fall back flat, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('C19b','M2',"A_IMA sits at the plain table and turns the old photograph face down, then she looks at the pencil lines on the back of it, then turns it face up again, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('C20','M2',"A_IMA: the open box lies below the view with photographs stacked inside it, then a pair of hands goes through them one by one, then stops without lifting any of them out, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('C21','M2',"A_NAKOUDO_M and A_NAKOUDO_F kneel side by side at the edge of the wedding party, then they both bow towards the room, then sit back up with their hands on their knees, while the paper screens stir in the draught and the shadows shift across the tatami, as the families kneel in place around the room",'zashiki','wide','Q',None,None),
('C22','M2',"A_MUSUME: the formal room opens out ahead of the view with the two families kneeling along both sides, then the view carries slowly down the middle of the room, then stops facing the alcove, while the paper screens stir in the draught and the shadows shift across the floor",'zashiki','pov_look','Q',None,None),
('C23','M2',"A_HAHA kneels at the low table with a cloth wrapper spread open on it, then she folds the corners of it over a flat parcel, then knots them together on top, while the hanging lamp sways over the table, as the family go on in the room behind her",'chabudai','high','Q',None,None),
('C24','M2',"A_CHICHI stands in the doorway of the living room with his jacket over his arm, then he turns back towards the room, then goes out along the corridor, while the hanging lamp sways over the table, as the mother kneels at the table behind him",'chanoma','medium','Q',None,None),
('C25','M2',"A_MUSUME kneels alone at the low table in the empty living room, then she straightens the cloth wrapper on the table, then sits back with her hands in her lap, while the hanging lamp sways over the table, as somebody moves about at the far end of the room",'chanoma','wide','Q',None,None,'cool'),
('C25b','M2',"A_HAHA slides the paper screen shut across the living room doorway, then she rests one hand flat on the frame of it, then turns back into the room, while the hanging lamp sways over the table, as somebody moves about at the far end of the room",'chanoma','medium','Q',None,None),
('C26','M2',"A_MUSUME: the empty tatami lies ahead of the view across the living room, then the view carries slowly along it towards the paper screens, then stops in front of them, while the hanging lamp sways over the table",'chanoma','pov_look','Q',None,None),
('C27','M2',"A_IMA sits back from the plain table with both hands resting on the old photograph, then she lifts them away from it, then folds them together in her lap, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
]

# =====================================================================================
# MUC 3 — 結婚したら、女性は会社を辞める (081-112, 32 clip)  ⭐ MUC DAT NHAT BAI
#   nhip: cong so binh thuong -> thong bao -> hoa + thung carton -> HANH LANG XEP HANG TIEN
#         -> "toa an da noi vi hien nam 1966" -> ma 20 nam sau van vo tay
#         -> 均等法 昭和61年4月1日 -> hai tam anh cung mot hop
# =====================================================================================
S += [
('D0','M3',"A_MUSUME walks in between the long rows of steel desks left to right across the frame carrying a paper tray in both hands, then she sets it down on her own desk, then pulls the chair out and sits down, while the blinds move at the windows, as the whole floor works on at every desk around her",'office','wide','Q',None,None),
('D1','M3',"A_MUSUME sits at her steel desk working the handle of a mechanical calculator, then she stops and writes something down beside it, then goes back to the handle, while the blinds move at the windows, as colleagues work on at the desks on either side of her",'office','medium','Q',None,None),
('D2','M3',"A_MUSUME: her own desk fills the bottom of the view with a mechanical calculator and paper trays on it, then their own hand pulls the calculator handle down in place and lets it come back, then reaches for the paper beside it, while the blinds move at the windows, as somebody walks past behind the desk",'office','pov_sit','Q',None,None),
('D3','M3',"A_DOURYOU leans over the low partition from the next row with a paper in her hand, then she says something across it, then goes back to her own desk, while the blinds move at the windows, as the whole floor works on around them",'office','medium','Q',None,None,'warm'),
('D4','M3',"A_JOUSHI stands up at the head of the row of desks and raises one hand towards the floor, then he says a few words to the room, then sits back down, while the blinds move at the windows, as the whole floor stops and turns towards him",'office','wide','Q','K','A_JOUSHI sitting back down at the head of the row'),
('D5','M3',"A_MUSUME stands up beside her own desk facing the room, then she bows towards the floor, then straightens up and stays standing, while the blinds move at the windows, as the whole floor turns in their chairs towards her",'office','medium','Q','K',None),
('D5b','M3',"A_JOUSHI stands at the head of the row of desks clapping towards the room, then he lowers his hands, then sits back down at his own desk, while the blinds move at the windows, as the whole floor claps from the desks around him",'office','medium','Q',None,None),
('D5c','M3',"A_DOURYOU stands up at her own desk in the next row clapping, then she turns towards the far side of the floor, then goes on clapping, while the blinds move at the windows, as the whole floor claps at the desks around her",'office','medium','Q',None,None),
('D6','M3',"A_MUSUME: the whole office floor lies ahead of the view with faces turned towards it from every desk, then the view moves slowly along the rows, then stops at the far end of the floor, while the blinds move at the windows",'office','pov_stand','Q',None,None),
('D7','M3',"A_MUSUME stands at her own desk with a flat cardboard box open on the desktop beside her, then she sets the things from the desk into it one after another, then folds the flaps of the box over, while the blinds move at the windows, as colleagues work on at the desks around her",'office','high','Q','L','A_MUSUME kneeling with the packed cardboard box in front of her'),
('D8','M3',"A_MUSUME: the open cardboard box lies below the view on the desktop, then their own hands lay a last small thing down inside it in place, then press the flaps together over the top, while the blinds move at the windows, as somebody walks past behind the desk",'office','pov_sit','Q','L',None),
('D9','M3',"A_DOURYOU carries a wrapped bunch of flowers across the cleared corner of the office floor, then she holds it out with both hands, then steps back into the ring of people, while the blinds move at the windows behind, as the whole floor stands gathered round the cleared space",'soubetsu','medium','Q','M','A_DOURYOU standing back in the ring with her hands empty'),
('D10','M3',"A_MUSUME takes the wrapped flowers into both arms, then she bows over them to the room, then straightens up holding them against her, while the blinds move at the windows, as the whole floor stands gathered in a ring around her",'soubetsu','wide','Q','M',None),
('D11','M3',"A_MUSUME stands in the middle of the cleared corner holding the flowers seen from the chest up, then she looks round the ring of people, then lowers her eyes to the flowers, while the blinds move at the windows, as the people stand shoulder to shoulder around her",'soubetsu','medium','Q',None,None),
('D12','M3',"A_JOUSHI stands at the edge of the cleared space and raises both hands to clap, then he goes on clapping, then lowers his hands, while the blinds move at the windows, as the whole floor claps around him",'soubetsu','medium','Q',None,None),
('D13','M3',"A_MUSUME: the ring of people stands all round ahead of the view with their hands up clapping, then the view moves slowly along the faces from one side to the other, then comes back and stops, while the blinds move at the windows behind them",'soubetsu','pov_look','Q',None,None),
('D13b','M3',"A_MUSUME stands in the middle of the cleared corner with the flowers held against her, then she bows once more to the room, then turns towards the corridor door, while the blinds move at the windows, as the ring of people stands clapping around her",'soubetsu','wide','Q',None,None),
('D14','M3',"A_MUSUME walks the whole length of the office corridor away from the view with the flowers in one arm and the box under the other, then she reaches the metal window frame at the end, then turns the corner out of sight, while the shadows of the window frames shift along the corridor floor, as colleagues stand along both walls of the corridor clapping",'office_rouka','behind','Q',None,None),
('D15','M3',"A_MUSUME walks between the two lines of colleagues along the corridor into frame, then she bows to one side as she passes, then goes on walking, while the shadows of the window frames shift along the corridor floor, as the corridor stays lined with people on both sides clapping",'office_rouka','medium','Q',None,None),
('D16','M3',"A_MUSUME: the corridor runs away ahead of the view between two lines of clapping people, then the view carries slowly forward between them, then stops at the bright window frame at the end, while the shadows of the window frames shift along the corridor floor",'office_rouka','pov_walk','Q',None,None),
('D17','M3',"A_DOURYOU stands in the line along the corridor wall clapping, then she stops and lowers her hands, then turns back towards the office door beside her, while the shadows of the window frames shift along the corridor floor, as the rest of the line goes on clapping around her",'office_rouka','medium','Q',None,None),
('D18','M3',"A_MUSUME stands outside the office building door with the box under one arm and the flowers in the other, then she looks back up at the building, then turns and walks away left to right across the frame, while the shadows shift along the frontage and the dust stirs at the kerb, as people come and go along the pavement behind her",'michi','wide','Q',None,None,'cool'),
('D19','M3',"A_JOUSHI takes a thick bound book down from the metal cabinet at the wall, then he opens it flat on the top of the cabinet, then runs one finger down the open page, while the blinds move at the windows, as the floor works on at the desks behind him",'office','medium','Q','N','A_JOUSHI with the bound book open on the cabinet top'),
('D20','M3',"A_MUSUME: the thick book lies open at a low angle in the bottom of the view with columns of small print running down the page, then a hand comes into frame and turns two pages over, then flattens them down, while the blinds move at the windows, as somebody stands waiting beside the cabinet",'office','pov_look','Q','N',None),
('D21','M3',"a clerk in a grey work jacket sets a bound ledger down on the town hall counter, then he opens it flat, then turns it round towards the public side, while the shadows of the window frames shift along the counter and the papers stir, as people wait along the counter further down",'yakusho','medium','Q','O','the bound ledger open on the counter facing the public side'),
('D22','M3',"a man in a dark suit stands at the town hall counter with the open ledger in front of him, then he leans down over the page, then straightens and puts both hands on the counter, while the shadows of the window frames shift along the counter and the papers stir, as others wait along the counter behind him",'yakusho','wide','Q','O',None),
('D23','M3',"A_MUSUME: the counter runs across the bottom of the view with the open ledger on it, then the view moves down the page from the top to the foot of the column, then comes back up to the head of it, while the shadows of the window frames shift along the counter and the papers stir",'yakusho','pov_look','Q',None,None),
('D23b','M3',"A_JOUSHI closes the thick bound book on top of the metal cabinet, then he slides it back onto the shelf, then pushes the cabinet door to, while the blinds move at the windows, as the floor works on at the desks behind him",'office','medium','Q',None,None),
('D24','M3',"the office floor goes on working at every desk in the long rows, then one of them gets up and crosses the floor left to right across the frame, then sits down again at another desk, while the blinds move at the windows, as the whole floor works on around them",'office','wide','Q',None,None),
('D25','M3',"A_DOURYOU stands up beside her own desk facing the room with her hands at her sides, then she bows towards the floor, then stays standing, while the blinds move at the windows, as the whole floor turns towards her from the desks",'office','medium','Q',None,None),
('D26','M3',"the cleared corner of the office floor stands empty with the low table pushed to one side, then the blinds shift at the windows behind it, then the slats settle again in place, while the blinds stir at the windows and the shadows shift across the floor, as two people cross the floor at the far end",'soubetsu','wide','Q',None,None,'cool'),
('D27','M3',"A_IMA lifts a second photograph out of the open box, then she sets it down on the table beside the first one, then lays both hands flat on either side of them, while the curtain at the wide window stirs",'ima_ie','medium','Q','P','A_IMA with the two photographs lying side by side on the table'),
('D28','M3',"A_IMA: the two old photographs lie side by side in the bottom of the view on the modern table, then their own hand moves from one to the other, then stops resting between them, while the curtain at the window stirs",'ima_ie','pov_hand','Q','P',None),
('D29','M3',"A_IMA: the second photograph fills the view showing a young woman holding a wrapped bunch of flowers, then the view moves slowly across it, then stops on the flowers, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('D30','M3',"A_IMA slides both photographs back into the flat box, then she sets the lid back on it, then rests one hand on the lid, while the curtain at the wide window stirs",'ima_ie','high','Q',None,None),
('D30b','M3',"A_IMA: the closed box lies below the view on the modern table with one hand resting on the lid, then the hand slides the box a little way across the table in place, then lifts off it, while the curtain at the window stirs",'ima_ie','ots','Q',None,None),
('D31','M3',"A_IMA sits back from the plain table with the closed box in front of her, then she turns her head towards the window, then looks back down at the box, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None,'cool'),
]

# =====================================================================================
# CTA 113-118 (6 clip) — canh tinh, nhip cham, khong day them thong tin moi
# =====================================================================================
S += [
('E0','CTA',"A_IMA sits at the plain table with both hands resting on the closed box, then she lifts one hand away, then sets it back down on the lid, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('E1','CTA',"the wooden veranda runs away along the house with one flat cushion set down on the boards, then the paper screens move a little in the draught, then the shadows shift along the boards, while the garden hedge stirs in the breeze and the shadows shift along the boards, as somebody moves about inside the house beyond the screens",'engawa','wide','Q',None,None,'warm'),
('E2','CTA',"A_HAHA kneels on the veranda boards folding a cloth in her lap, then she smooths it flat across her knees, then sets it down beside her, while the garden hedge stirs in the breeze and the shadows shift along the boards, as the laundry pole stands out in the garden beyond",'engawa','medium','Q',None,None,'warm'),
('E3','CTA',"the low round table stands alone in the empty living room with the tea tray on it, then the hanging lamp sways a little over it in place, then the shadow of it lengthens across the tatami, while the hanging lamp goes on swaying, as somebody crosses the far end of the room",'chanoma','wide','Q',None,None),
('E4','CTA',"A_IMA: the closed box lies below the view on the modern table, then a pair of hands rests on the lid of it, then lifts away to the edge of the table, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('E5','CTA',"A_IMA lifts the lid off the box again, then she takes the first photograph out, then turns it face down on the table, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
]

# =====================================================================================
# MUC 4 — 結婚には、適齢期という期限がある (119-144, 26 clip)
#   ⛔ KHONG mot cuon lich nao trong ca khoi nay (RUI RO c).
#   nhip: ho hang tu tap hoi tuoi -> hang xom len nha -> giong doi khac di ->
#         doi tre tu chon nhau ngoai pho (恋愛が追い抜いた) -> nhung co gai van bi giuc
# =====================================================================================
S += [
('F0','M4',"a group of relatives kneel round the low table in the formal room with tea cups in front of them, then one of them turns towards the doorway, then goes on talking to the room, while the paper screens stir in the draught and the shadows shift across the tatami, as the whole group sits on around the table",'zashiki','wide','Q',None,None),
('F1','M4',"an aunt in a plain kimono kneels at the table and leans forward towards the doorway, then she says something across the room, then sits back on her heels laughing, while the paper screens stir in the draught and the shadows shift across the tatami, as the other relatives sit round the table",'zashiki','medium','Q',None,None),
('F2','M4',"A_MUSUME kneels in the doorway of the formal room with a tea tray in both hands, then she lowers it to the mat just inside the door, then stays kneeling behind it, while the paper screens stir in the draught and the shadows shift across the tatami, as the relatives sit round the table beyond her",'zashiki','wide','Q',None,None),
('F3','M4',"A_MUSUME: the room full of kneeling relatives lies ahead of the view from just inside the door, then several of the faces turn towards the view one after another, then stay turned that way, while the paper screens stir in the draught and the shadows shift across the floor",'zashiki','pov_sit','Q',None,None),
('F4','M4',"A_MUSUME kneels just inside the doorway seen from the chest up, then she lowers her head, then lifts it again with her eyes down, while the paper screens stir in the draught and the shadows shift across the tatami, as the relatives go on talking in the room behind her",'zashiki','medium','Q',None,None,'cool'),
('F4b','M4',"an uncle in a plain open-necked shirt kneels at the table and turns towards the doorway, then he says something across the room, then reaches for his cup, while the paper screens stir in the draught and the shadows shift across the tatami, as the relatives sit round the table laughing",'zashiki','medium','Q',None,None),
('F5','M4',"A_MUSUME backs out of the formal room on her knees with the empty tray, then she slides the screen door shut in front of her, then stands up in the corridor, while the shadows of the window frames shift along the corridor floor, as the voices go on behind the closed screen",'zashiki','wide','Q',None,None),
('F6','M4',"a neighbour in a plain apron stands up on the sunken entrance floor talking in through the doorway, then she steps up onto the wooden corridor uninvited, then goes on talking, while the shadow of the door frame moves across the floor, as another neighbour waits out in the lane",'genkansaki','medium','Q','R','the neighbour standing up on the corridor still talking'),
('F7','M4',"A_HAHA stands in the corridor facing the neighbour with a cloth in her hands, then she nods twice, then folds the cloth over her arm, while the shadow of the door frame moves across the floor, as the neighbour stands on the corridor beside her",'genkansaki','medium','Q','R',None),
('F8','M4',"A_MUSUME: the corridor runs towards the doorway ahead of the view with two women standing talking in it, then the view stays where it is as one of them turns to look back, then the other goes on talking, while the shadow of the door frame moves across the floor",'genkansaki','pov_stand','Q',None,None),
('F9','M4',"A_MUSUME stands halfway along the corridor with one hand on the wall, then she turns away from the doorway, then walks deeper into the house, while the dust stirs in the light from the doorway and the shadows shift along the floor, as the two women go on talking at the door behind her",'genkansaki','behind','Q',None,None),
('F10','M4',"A_HAHA kneels at the low table across from her daughter and sets a cup down in front of her, then she says a few words across the table, then looks down into her own cup, while the hanging lamp sways over the table, as the father sits at the far end of the room",'chabudai','medium','Q','S','A_HAHA looking down into her own cup across the table'),
('F11','M4',"A_MUSUME: the low table lies below the view with two cups on it, then their own hand turns the nearer cup slowly round where it stands, then lets go of it, while the hanging lamp sways over the table, as her mother sits across the table from the view",'chabudai','pov_sit','Q','S',None),
('F12','M4',"A_MUSUME kneels at the low table looking down at the cup in front of her, then she lifts her head towards her mother, then looks down again without speaking, while the hanging lamp sways over the table, as her mother kneels across the table",'chanoma','ots','Q',None,None,'cool'),
('F13','M4',"a young couple walk along the shopping street side by side without touching, then they stop together at a shopfront, then walk on left to right across the frame, while the bare bulbs sway over the street, as the whole street moves with shoppers around them",'shotengai','wide','Q',None,None,'warm'),
('F14','M4',"the young woman of the couple stands at the shopfront turning something over in her hands, then she holds it up towards the young man, then sets it back down on the crate, while the bare bulbs sway over the street, as shoppers pass behind them both ways",'shotengai','medium','Q',None,None,'warm'),
('F15','M4',"A_MUSUME walks left to right across the frame along the shopping street with a woven basket over one arm, then she passes the young couple going the other way, then walks on without turning her head, while the bare bulbs sway over the street, as the crowd moves along the arcade on both sides",'shotengai','wide','Q',None,None),
('F15b','M4',"A_MUSUME stops at a shopfront along the arcade with the basket over one arm, then she looks back down the street behind her, then turns and walks on left to right across the frame, while the bare bulbs sway over the street, as shoppers pass her both ways along the pavement",'shotengai','medium','Q',None,None),
('F16','M4',"A_MUSUME: the shopping street opens out ahead of the view under the strung bulbs, then the view carries slowly forward along the pavement, then stops where the awnings end, while the crowd moves along on both sides of the view",'shotengai','pov_walk','Q',None,None),
('F17','M4',"A_MUSUME sits at her steel desk in the office with her hands flat on the desktop, then she turns her head towards the window, then looks back down at the desk, while the blinds move at the windows, as the whole floor works on at the desks around her",'office','medium','Q',None,None),
('F18','M4',"A_DOURYOU crosses the office floor left to right across the frame carrying a paper tray, then she stops at the desk in the next row, then goes on past it to her own, while the blinds move at the windows, as the floor works on at every desk",'office','wide','Q',None,None),
('F19','M4',"A_MUSUME: her own desk fills the bottom of the view with her own hands resting on it, then their own hands come together in place, then draw back to the edge of the desk, while the blinds move at the windows, as somebody walks past behind the desk",'office','pov_sit','Q',None,None),
('F20','M4',"A_MUSUME walks home down the narrow lane away from the view in the evening, then she stops under the telegraph pole, then goes on towards the lit windows, while the lit windows go on down the lane, as neighbours walk home along the street behind her",'michi','behind','Q',None,None,'cool'),
('F21','M4',"A_HAHA kneels alone at the low table with the tea tray in front of her, then she pours one cup, then sets the pot down and does not drink, while the hanging lamp sways over the table, as somebody moves about at the far end of the room",'chanoma','wide','Q',None,None),
('F21b','M4',"A_MUSUME kneels down at the low table opposite her mother, then she takes up the cup that was poured for her, then sets it down again without drinking, while the hanging lamp sways over the table, as the father sits back at the far end of the room",'chabudai','medium','Q',None,None),
('F22','M4',"A_MUSUME kneels at the low table facing her mother across it, then she nods once, then lowers her head, while the hanging lamp sways over the table, as the father sits back at the far end of the room",'chanoma','medium','Q',None,None,'cool'),
('F23','M4',"A_IMA sits at the plain table with the face-down photograph in front of her, then she turns it face up again, then looks down at it, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('F24','M4',"A_IMA: the photograph lies face up in the bottom of the view, then their own finger rests on the edge of it, then draws slowly away across the table, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('F25','M4',"the empty formal room stands with the screens pushed back onto the garden, then the shadows lengthen across the tatami in place, then the screens shift a little in the draught, while the garden hedge stirs in the breeze and the shadows shift along the boards, as somebody crosses the corridor past the doorway",'zashiki','wide','Q',None,None,'cool'),
]

# =====================================================================================
# BRIDGE 145-148 (4 clip) — 「ここまでが、写真の表の話です」
# =====================================================================================
S += [
('G0','BRIDGE',"A_IMA holds the photograph up in both hands in front of her, then she turns it slowly over to its back, then lowers it flat to the table, while the curtain at the wide window stirs",'ima_ie','medium','Q','T','A_IMA with the photograph lying face down on the table'),
('G1','BRIDGE',"A_IMA: the back of the photograph lies in the bottom of the view with the two pencil lines on it, then their own hand rests beside it on the table, then draws back out of the picture, while the curtain at the window stirs",'ima_ie','pov_hand','Q','T',None),
('G2','BRIDGE',"A_IMA: the back of the photograph fills the view with the two faint pencil lines, then the view moves down to the lower line, then holds on it, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('G3','BRIDGE',"A_IMA sits very still at the plain table with the photograph face down in front of her, then she folds both hands together on the table, then looks down at them, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
]

# =====================================================================================
# MUC 5 — 妻の老後は、夫の年金の中にあった (149-183, 35 clip)
#   nhip: dong but chi thu hai -> nguoi vo trong bep/hien -> quay hanh chinh (任意加入) ->
#         cai "tien de" cua ca bai -> 昭和61年4月1日 -> hai luat mot ngay -> tra LOOP
# =====================================================================================
S += [
('H20','M5',"A_IMA: the back of the photograph lies in the bottom of the view, then their own finger moves along the lower pencil line from one end to the other, then lifts away, while the curtain at the window stirs",'ima_ie','pov_hand','Q',None,None),
('H21','M5',"A_IMA sits at the plain table holding the photograph face down in both hands, then she brings it closer to her eyes, then lowers it to the table again, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H22','M5',"A_HAHA stands at the kitchen worktop under the one bare bulb with the rest of the room dark, then she lifts the blackened kettle off the burner, then sets it down on the tiled worktop, while the bare bulb sways overhead and her shadow moves on the wall",'daidokoro','wide','Q',None,None),
('H23','M5',"A_HAHA: the worktop fills the bottom of the view under the bare bulb, then their own hands wipe along the tiles from one side to the other, then wring the cloth out over the sink, while the bare bulb sways overhead",'daidokoro','pov_stand','Q',None,None),
('H24','M5',"A_HAHA kneels at the low table alone in the living room with a small book open in front of her, then she writes one short line in it, then closes it and rests her hand on the cover, while the hanging lamp sways over the table, as somebody moves about at the far end of the room",'chanoma','medium','Q','U','A_HAHA with her hand resting on the closed small book'),
('H25','M5',"A_HAHA: the low table lies below the view with the small closed book on it, then their own hand slides it under the edge of the tea tray, then draws back to their own knee, while the hanging lamp sways over the table",'chanoma','pov_sit','Q','U',None),
('H26','M5',"a clerk in a grey work jacket stands behind the town hall counter turning the pages of a bound file, then he stops at one page, then turns the file round in place towards the public side, while the shadows of the window frames shift along the counter and the papers stir, as people wait along the counter further down",'yakusho','medium','Q','V','the bound file lying open on the counter facing outwards'),
('H27','M5',"A_HAHA stands at the town hall counter in front of the open file, then she leans down over it in place, then straightens up and puts both hands on the counter edge, while the shadows of the window frames shift along the counter and the papers stir, as others wait along the counter behind her",'yakusho','wide','Q','V',None),
('H28','M5',"A_HAHA: the counter runs across the bottom of the view with the open file on it, then their own hand comes down flat on the page in place, then draws back to the edge of the counter, while the shadows of the window frames shift along the counter and the papers stir, as somebody waits at the next partition",'yakusho','pov_stand','Q',None,None),
('H28b','M5',"A_HAHA stands at the town hall counter with both hands on the edge of it, then she turns her head in place towards the clerk, then looks back down at the open file, while the shadows of the window frames shift along the counter and the papers stir, as people wait along the counter behind her",'yakusho','medium','Q',None,None),
('H29','M5',"A_HAHA turns away from the town hall counter and walks down the length of the room into frame, then she stops by the chairs against the wall, then goes on past them, while the shadows of the window frames shift across the floor and the papers stir, as people sit waiting along the wall",'yakusho','wide','Q',None,None),
('H30','M5',"A_CHICHI sits at the low table with a brown envelope in one hand, then he sets it down on the table, then pushes it a little way across towards the other side, while the hanging lamp sways over the table, as the family go on in the room behind him",'chabudai','medium','Q','W','A_CHICHI with the brown envelope pushed across the table'),
('H31','M5',"A_HAHA: the low table fills the bottom of the view with the brown envelope lying on it, then their own two hands take it up, then hold it still above the table, while the hanging lamp sways over the table, as her husband sits across the table",'chabudai','pov_sit','Q','W',None),
('H32','M5',"A_HAHA kneels at the low table holding the brown envelope in both hands, then she looks across the table at her husband, then looks back down at the envelope, while the hanging lamp sways over the table, as the family go on around the table",'chanoma','medium','Q',None,None),
('H33','M5',"A_HAHA and A_CHICHI kneel on either side of the low table with the envelope between them, then neither of them moves for a moment, then she draws the envelope towards herself, while the hanging lamp sways over the table, as the rest of the family go on in the room",'chanoma','wide','Q',None,None),
('H34','M5',"A_HAHA sits on the veranda boards in the late afternoon with her hands in her lap, then she looks out into the garden, then lowers her eyes to her own hands, while the garden hedge stirs in the breeze and the shadows shift along the boards, as the laundry pole stands out in the garden beyond",'engawa','medium','Q',None,None,'cool'),
('H35','M5',"A_HAHA: the garden lies ahead of the view from the veranda boards, then the view moves slowly across the hedge and the stone basin, then stops on the neighbouring roofs, while the garden hedge stirs in the breeze and the shadows shift along the boards",'engawa','pov_sit','Q',None,None),
('H35b','M5',"A_HAHA sits on the veranda boards with her hands in her lap, then she turns her head back towards the house, then looks out into the garden again, while the garden hedge stirs in the breeze and the shadows shift along the boards, as somebody moves about inside beyond the screens",'engawa','medium','Q',None,None,'cool'),
('H36','M5',"the wooden veranda runs away along the house with one flat cushion on the boards, then the paper screens shift in the draught behind it, then the shadows move along the boards, while the garden hedge stirs in the breeze and the shadows shift along the boards, as somebody moves about inside beyond the screens",'engawa','wide','Q',None,None,'cool'),
('H37','M5',"a clerk behind the town hall counter stamps a red seal down onto an open page, then he lifts it away, then turns the page round towards the public side, while the shadows of the window frames shift along the counter and the papers stir, as people wait along the counter further down",'yakusho','medium','Q','X','the stamped page turned round towards the public side'),
('H38','M5',"A_HAHA stands at the counter as the clerk slides the stamped page across to her, then she takes it up in both hands, then holds it against her, while the shadows of the window frames shift along the counter and the papers stir, as others wait along the counter behind her",'yakusho','wide','Q','X',None),
('H39','M5',"A_HAHA: the counter lies across the bottom of the view with the stamped page on it, then their own two hands draw it towards the view, then lift it out of the picture, while the shadows of the window frames shift along the counter and the papers stir",'yakusho','pov_stand','Q',None,None),
('H40','M5',"A_HAHA walks out of the town hall doorway into the daylight, then she stops on the step, then goes on down it left to right across the frame, while the shadows shift along the frontage and the dust stirs at the kerb, as people come and go past the doorway",'michi','wide','Q',None,None),
('H41','M5',"A_HAHA kneels at the low table and lays the folded page flat on it, then she smooths it down with the side of her hand, then rests both hands on either side of it, while the hanging lamp sways over the table, as the family go on in the room behind her",'chabudai','high','Q','Y','A_HAHA with the folded page smoothed flat on the table'),
('H42','M5',"A_HAHA: the folded page lies in the bottom of the view on the low table, then their own finger rests on one corner of it, then draws slowly across to the other corner, while the hanging lamp sways over the table, as somebody sets a cup down at the far edge of the table",'chabudai','pov_hand','Q','Y',None),
('H43','M5',"A_HAHA slides the folded page into the tea cabinet and pushes the wooden door shut on it, then she rests her hand on the door, then turns back to the room, while the hanging lamp sways over the table, as the family go on with the evening behind her",'chanoma','medium','Q',None,None),
('H43b','M5',"A_HAHA kneels in front of the tea cabinet with one hand still on the closed wooden door, then she lets the hand fall to her lap, then stays kneeling there, while the hanging lamp sways over the table, as the family go on with the evening behind her",'chanoma','medium','Q',None,None,'cool'),
('H44','M5',"A_MUSUME kneels at the low table in the living room with her hands in her lap, then she looks across at her mother by the cabinet, then looks down again, while the hanging lamp sways over the table, as the family go on in the room",'chanoma','wide','Q',None,None),
('H45','M5',"A_IMA sits at the plain modern table with the photograph face down in front of her, then she lays one hand flat beside the pencil lines, then draws it back, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H46','M5',"A_IMA: the back of the photograph fills the view with the two pencil lines on it, then the view holds on the lower line without moving, then lifts slowly away from it, while the curtain at the window stirs",'ima_ie','pov_look','Q',None,None),
('H47','M5',"A_IMA turns the photograph face up again on the table, then she sets it down square in front of her, then folds both hands on the table behind it, while the curtain at the wide window stirs",'ima_ie','high','Q',None,None),
('H48','M5',"A_IMA sits back from the plain table looking down at the photograph, then she turns her head towards the window, then looks back at the photograph, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H49','M5',"the office floor goes on working in the long rows of steel desks, then two of them cross the floor left to right across the frame, then sit back down at their desks, while the blinds move at the windows, as the whole floor works on around them",'office','wide','Q',None,None),
('H50','M5',"A_DOURYOU sits at her steel desk with both hands on the desktop, then she looks up across the floor, then goes back to the paper in front of her, while the blinds move at the windows, as the whole floor works on around her",'office','medium','Q',None,None),
('H50b','M5',"A_MUSUME sits at her steel desk with a paper in front of her, then she looks up across the office floor, then goes back down to the paper, while the blinds move at the windows, as the whole floor works on at the desks around her",'office','medium','Q',None,None),
('H51','M5',"A_HAHA stands at the kitchen worktop in the daytime with the shutters open, then she lifts an enamel bowl down from the shelf, then sets it on the tiled worktop, while the cloth by the sink stirs and the shadows shift across the tiles, as somebody moves about in the room beyond the doorway",'daidokoro','wide','Q',None,None,'warm'),
('H52','M5',"A_HAHA kneels on the veranda in the late afternoon folding a cloth across her knees, then she sets it down on the boards, then looks out into the garden, while the garden hedge stirs in the breeze and the shadows shift along the boards, as the hedge and the roofs stand beyond the garden",'engawa','medium','Q',None,None,'warm'),
('H53','M5',"A_IMA holds the photograph up in both hands towards the window light, then she turns it a little in her hands, then lowers it slowly to the table, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('H54','M5',"A_IMA: the photograph lies face up in the bottom of the view on the modern table, then their own hands come to rest on either side of it, then stay there, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
]

# =====================================================================================
# KET 184-191 (8 clip) — tong luan 認める→裏返す
# =====================================================================================
S += [
('I0','KET',"A_MUSUME kneels at the low table with the photograph lying on the tatami in front of her, then she looks down at it, then folds her hands in her lap, while the hanging lamp sways over the table, as her parents sit on either side of the table",'chanoma','wide','Q',None,None,'cool'),
('I1','KET',"A_MUSUME sits very still at the low table seen from the chest up, then she opens her mouth to answer, then closes it and lowers her eyes, while the hanging lamp sways over the table, as her parents sit on both sides of the picture",'chanoma','medium','Q',None,None,'cool'),
('I2','KET',"A_MUSUME: the low table lies below the view with the photograph on the tatami beyond it and the family's hands round the edge, then their own hands fold together in their own lap, then stay folded there, while the hanging lamp sways over the table",'chanoma','pov_sit','Q',None,None),
('I3','KET',"the whole family kneel round the low table with the photograph in the middle of them, then one of them reaches out and turns it a little, then draws the hand back, while the hanging lamp sways over the table, as the family sit on together around the table",'chanoma','wide','Q',None,None),
('I3b','KET',"A_MUSUME kneels at the low table with the family round it, then she nods once towards her parents, then lowers her head, while the hanging lamp sways over the table, as the family sit on together around the table",'chanoma','medium','Q',None,None,'cool'),
('I3c','KET',"A_MUSUME: the family sit round the low table ahead of the view with the photograph between them, then several of the faces turn towards the view, then look back down at the photograph, while the hanging lamp sways over the table",'chanoma','pov_sit','Q',None,None),
('I4','KET',"A_IMA sits at the plain modern table with the photograph in front of her and the box beside it, then she looks down at both of them, then lifts her head towards the window, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('I5','KET',"A_IMA: the modern table lies below the view with the photograph and the open box on it, then a pair of hands sets the photograph down inside the box, then rests on the rim of it, while the curtain at the window stirs",'ima_ie','high','Q',None,None),
('I6','KET',"A_IMA sets the lid back on the flat box, then she presses it down at both corners, then leaves both hands resting on the lid, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None),
('I7','KET',"the empty living room stands with the low table under the hanging lamp and nothing on it, then the lamp sways a little over the table in place, then the shadow of it lengthens across the tatami, while the hanging lamp goes on swaying, as somebody crosses the far end of the room",'chanoma','wide','Q',None,None,'cool'),
]

# =====================================================================================
# OUTRO 192-197 (6 clip) — cau hoi cuoi + chu ky kenh
# =====================================================================================
S += [
('J0','OUTRO',"A_IMA sits back from the plain table with the closed box in front of her, then she rests one hand on the lid, then looks up towards the window, while the curtain at the wide window stirs",'ima_ie','medium','Q',None,None,'warm'),
('J1','OUTRO',"the wooden veranda runs away along the house in the late afternoon with the screens pushed back, then the light moves slowly along the boards, then the screens shift a little, while the garden hedge stirs in the breeze and the shadows shift along the boards, as somebody moves about inside the house",'engawa','wide','Q',None,None,'warm'),
('J2','OUTRO',"A_HAHA kneels on the veranda boards looking out into the garden, then she smooths her skirt over her knees, then folds her hands in her lap, while the garden hedge stirs in the breeze and the shadows shift along the boards, as the hedge and the roofs stand beyond the garden",'engawa','medium','Q',None,None,'warm'),
('J3','OUTRO',"the shopping street goes on under the strung bulbs in the early evening, then the awnings move in the draught, then the light shifts along the shopfronts, while the bulbs sway over the street, as the crowd moves along the arcade on both sides",'shotengai','wide','Q',None,None,'warm'),
('J4','OUTRO',"the narrow lane runs away between the fences with the lit windows going down it, then the light in one of the windows shifts, then the shadows move along the fence, while the shadows shift along the fences and the dust stirs in the lane, as two neighbours talk at a gate further down",'michi','wide','Q',None,None,'cool'),
('J4b','OUTRO',"the kitchen stands empty in the daytime with the shutters open over the worktop, then the daylight moves across the tiles, then a cloth hanging by the sink stirs, while the cloth by the sink stirs and the shadows shift across the tiles, as somebody moves about in the room beyond the doorway",'daidokoro','wide','Q',None,None,'warm'),
('J5','OUTRO',"A_IMA sits alone at the plain table with both hands resting on the closed box, then she lifts both hands off it, then folds them together in her lap, while the curtain at the wide window stirs",'ima_ie','wide','Q',None,None,'cool'),
]

# =====================================================================================
# CHAY
# =====================================================================================
# CUT tu dong: cat chuoi noi-lien tai moi cho DOI FRAMING trong cung mot (khoi, preset) —
# cung luat da dung o video 15.
CUT = set(); _prev = None
for _x in S:
    if _prev is not None and _prev[1] == _x[1] and _prev[3] == _x[3] and _prev[4] != _x[4]:
        CUT.add(_x[0])
    _prev = _x

# 🔴 LOP THU HAI cua CUT — canh KHONG khai `out` thi canh NGAY SAU no khong noi vao duoc.
#    autochain van se noi chung lai neu cung boi canh => gate bao "THIEU out" hang loat.
#    Sua o day (mot cho) thay vi di gan `out` le cho 13 canh: canh nao khong co trang thai
#    ket thi CAT chuoi tai canh sau no. Noi-lien la de GIU BOI CANH, khong phai nghia vu.
for _i in range(len(S) - 1):
    if len(S[_i]) < 8 or S[_i][7] is None:
        CUT.add(S[_i + 1][0])

S = autochain(S, cut=CUT)

rows = build(S, P, C, prof=PROF, crowd=CROWD)
n_red, n_warn = gate(rows, S, P, C,
                     interior={"chanoma", "chabudai", "daidokoro", "zashiki",
                               "genkansaki", "shashinkan", "office", "office_rouka",
                               "soubetsu", "yakusho", "engawa", "ima_ie"},
                     strict=True, crowd=CROWD, prof=PROF)
act_report(S, C)
safe, risky, pct = linkage(S)
print("\nNOI AN TOAN: %d/%d moi noi cung boi canh co it nhat mot canh CHAT (%.0f%%)"
      % (safe, risky, pct))

pov = sum(1 for x in S if str(x[4]).startswith("pov"))
print("POV: %d/%d = %.0f%%" % (pov, len(S), pov * 100 / len(S)))
print("SO CANH: %d  (SLIDES can dung 220 — TRAN 7,0s)" % len(S))

OUTDIR = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\16_omiai-kekkon"
import os
os.makedirs(OUTDIR, exist_ok=True)
if n_red == 0:
    write_outputs(rows, OUTDIR, prefix="videogen16", prof=PROF)
    print("\nXUAT -> %s\\videogen16_FLOW.txt | _TENFILE.txt | _BLOCKS.md" % OUTDIR)
else:
    print("\n[CHAN] %d loi do — KHONG xuat file. Sua roi chay lai." % n_red)
sys.exit(0 if n_red == 0 else 1)
