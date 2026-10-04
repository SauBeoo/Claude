# -*- coding: utf-8 -*-
r"""gen_demo16_kioku v8 — 8 prompt DEMO video 16. Ap `.claude/rules/camera-language.md` §4.1 + §4.2.

LICH SUA — moi ban sua mot loi DO DUOC hoac user bat duoc:
  v1 : "respectful distance" + "at chest height" + 1 nguoi/canh + POV lo tay
  v2 : may SAT, dung tam cao nguoi trong canh, >=2 nguoi TRAO DOI, POV KHONG lo tay
  v3 : bo `35mm` (8/8 clip v2 ra dai phim + so in o mep) · dua nuoc may len 15% dau
  v4 : ⬇ user: "chua the hien ro goc quay cam, lia cam" + "canh vat phong canh phai mau sac vao"
       + "nhin ra ngoai cua so thi cam phai dua tu trong ra ngoai va nhin canh vat ben ngoai
          chuyen dong kieu the"

  🔴 v4-a  LUAT HAI MOC (rule §4.1). v3 viet nuoc may thanh CAI NHAN
      (`a slow steady dolly push straight in towards them`). Model khong biet DI TU DAU TOI DAU
      nen chon cach re nhat: gan nhu khong di (7/8 clip v2-v3 MAD duoi nguong, D8 51,6% dung yen).
      => Moi nuoc may phai khai BA thu: MOC DAU (khung frame 1) -> DUONG DI (di qua cai gi)
         -> MOC KET (khung frame cuoi). Va voi ngoai canh, MOC THU TU: the gioi phai CHAY
         trong khung (`sliding steadily past across the frame the whole time`).
      📌 Cung dinh luat da do 2 lan: model nghe VI TRI, khong nghe TEN GOI hay TI LE.

  🔴 v4-b  MAU PHONG CANH phai xin RIENG (rule §4.2). Khoi STYLE chung noi `full rich natural
      colour` cho CA khung; canh noi that toi chiem phan lon khung thi model don "mau" vao chu
      the va de phong canh xam. => canh nao co phong canh trong khung thi goi TEN MAU cua
      chinh phong canh do (khoi LAND). Van giu tran `no oversaturated colour` — xin DAM, khong
      xin RUC.

NGHIEM THU (camera-language.md §8.1): MAD blur trong shot >= 8,2 · %khung dung yen <= 10%
  ⛔ KHONG do `vien/tam` va `G` o muc mot clip — chung la thong ke CA BAI.
"""
import io
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(__file__).resolve().parents[1] / "06_VIDEO" / "16_omiai-kekkon"

# 🔴 GHI RA FILE CO VERSION, KHONG GHI DE BAN TRUOC.
#    Ban v1->v5 deu ghi vao cung `videogen_DEMO16_FLOW.txt` => 8 clip user da gen (tu v2)
#    khong con prompt goc de doi chieu. Do la loi cua flow, khong phai cua prompt.
VER = "v8"
VIDEO_ID = "16"
FLOW = f"videogen_DEMO16_{VER}_FLOW.txt"
TENF = f"videogen_DEMO16_{VER}_TENFILE.txt"

HEAD = "Camera move, the only one in this shot: "

# =====================================================================================
# §4.1 NUOC MAY = DUONG DI. Moi cai: MOC DAU -> DUONG DI -> MOC KET (+ nen troi neu ngoai canh)
#      Dat trong 15% DAU prompt.
# =====================================================================================
# =====================================================================================
# 4.1 NUOC MAY = MOT BAN SPEC CO NHAN, khong phai van xuoi.
#
#   v7 sua loi user bat: "goc di chuyen cam khong ro rang lam".
#   v4-v6 BO HET TEN KY THUAT, chi con van xuoi ta duong di => OVER-CORRECT: bang cua user
#   toan TEN (Dolly / Pan / Tracking / Pedestal / Zoom). Ten la mot token manh va khong the
#   hieu lech; duong di la hinh hoc. PHAI CO CA HAI.
#
#   DO TREN 7 CLIP v5 (ECC affine, frame dau vs frame cuoi) - day la co so cua v7:
#     dolly tien/lui/ngang  -> CHAY: scale +13% / +21% / +47% / -21%, MAD 10,0-15,0
#     "sink down" (pedestal)-> KHONG CHAY: D4 scale 0,999 · D6 scale 0,995, dich 5-10px
#     "travel backward in through the screens" -> KHONG CHAY: D5 scale 1,021
#   => KET LUAN: t2v lam duoc DOLLY (truc truoc-sau) va TRACK (truc ngang);
#      KHONG lam duoc PEDESTAL/CRANE (truc doc) khi do la nuoc chinh.
#   => D4/D6 doi sang DOLLY IN co HA DAN theo duong di - dung dong tu da chung minh chay,
#      thay vi mot ky thuat da chung minh khong chay. D5 doi "backward in" -> "forward in".
#
#   Moi nuoc khai 6 o: TEN . VAT LY (+ "khong phai zoom") . BAT DAU . DUONG DI (truc/chieu/
#   cao do) . LUONG (di bao xa) . KET. Cong cau chot "khong dung, khong nguoc".
#   Cau "khong phai zoom" la BAT BUOC: 7.3 do duoc t2v tron zoom voi dolly.
# =====================================================================================
MOVES = {
 "dolly_row": dict(
   name="DOLLY IN, straight forward",
   phys="the whole camera rolls forward through the room on a track, so the desks really pass it "
        "on both sides; this is a physical move through space, not a zoom, not a crop and not a "
        "still frame",
   start="tight and low on the mechanical calculator and the black telephone on the near desk",
   path="straight forward along the row of desks, staying level at tabletop height the whole way, "
        "the desk edge and the paper trays sweeping out through both sides of the frame",
   amount="it closes about half the distance to them",
   end="close on the two of them at the far desk, their faces filling most of the frame"),

 "arc_shoulder": dict(
   name="ARC, the camera orbiting slowly round her shoulder",
   phys="the camera swings round her along a curve while holding the same distance from her, so "
        "the background slides across behind her; this is a physical move round her, not a zoom "
        "and not a still frame",
   start="behind her shoulder, the back of her head filling the near corner and the open ledger "
         "soft and out of focus beyond it",
   path="round that shoulder from her left towards her front, keeping her shoulder in the near "
        "corner and holding its own height",
   amount="it travels about a quarter of the way round her",
   end="on the ledger page sharp and the other woman's face clear above it"),

 "track_corridor": dict(
   name="TRACKING, sideways, left to right",
   phys="the whole camera slides sideways along the corridor on a dolly, parallel to the wall, so "
        "each door passes it in turn; this is a sideways move through space, not a pan from one "
        "fixed spot and not a zoom",
   start="on the frosted glass doors at the near end of the corridor",
   path="sideways from left to right, holding the same distance from the wall and the same height, "
        "each frosted door and each plaster pier sweeping through the front of the frame",
   amount="it covers about three doorways of corridor",
   end="on the two of them with the bouquet, the tall window at the far end blazing behind them"),

 # D4 - DA DOI: "PEDESTAL DOWN" do duoc la KHONG CHAY (scale 0,999). Dung DOLLY IN lam
 #      dong tu chinh (da chung minh chay), cho viec ha thap vao DUONG DI.
 "dolly_counter": dict(
   name="DOLLY IN, forward and dropping as it goes",
   phys="the whole camera rolls forward over the counter and sinks as it travels, so the counter "
        "edge really rises through the bottom of the frame; the forward travel is the main move "
        "and it is a physical move through space, not a zoom and not a tilt from one fixed spot",
   start="above the wooden counter looking down on the closed ledger and the folded paper",
   path="forward across the counter and downward at the same time, from above their heads to their "
        "own eye level, the counter edge rising through the bottom of the frame as it comes level",
   amount="it crosses the width of the counter and drops the height of a standing person",
   end="level with the two of them facing each other across the open page"),

 # D5 - DA SUA: "travel backward in through the screens" do duoc KHONG CHAY (scale 1,021).
 #      Huong vao nha la FORWARD, khong phai backward - cau cu tu mau thuan.
 "dolly_garden": dict(
   name="DOLLY IN, from the garden into the house",
   phys="the whole camera rolls forward out of the garden and in through the open paper screens, "
        "so the screen frames really pass it on both sides; this is a physical move into the room, "
        "not a zoom and not a cut",
   start="outside in the evening garden, the leaves and the stone lantern filling the frame with "
         "the lamplit room glowing beyond them",
   path="straight forward in through the open paper screens and on over the tatami, dropping as it "
        "goes from standing height down to the height of the tabletop",
   amount="it crosses the whole veranda and comes right up to the table",
   end="down low at the level of the tabletop with the two of them either side of it, the garden "
       "still stirring in the dark behind them"),

 # D6 - DA DOI: cu "sink down past the flower" do duoc la te nhat ca lo (dich 5px, scale 0,995).
 "dolly_alcove": dict(
   name="DOLLY IN, forward past a foreground flower and dropping as it goes",
   phys="the whole camera rolls forward past the alcove and sinks as it travels, so the flower "
        "really passes it and drifts up out through the top of the frame; the forward travel is "
        "the main move and it is a physical move through space, not a zoom and not a tilt",
   start="high on the hanging scroll and the single flower standing in the alcove",
   path="forward past that flower and downward at the same time, the stem and the petals drifting "
        "up out through the top of the frame as the camera passes them",
   amount="it crosses the width of the room and drops from above the scroll to just above their heads",
   end="looking down on the photograph lying on the stand with the three heads gathered round it"),

 "dolly_window": dict(
   name="DOLLY IN, towards the window and out through it",
   phys="the whole camera rolls forward down the carriage towards the open window, so the seat "
        "backs pass it on both sides; this is a physical move through the carriage, not a zoom and "
        "not a pan from one fixed seat",
   start="inside the dim carriage, tight on the worn blue plush of a seat back and the chrome grab rail",
   path="straight forward towards the half-open window, holding seated height, the window frame and "
        "the short curtain opening out past the edges of the frame",
   amount="it crosses two rows of seats and comes right up to the glass",
   end="looking straight out of that window at the open country"),

 "dolly_out_path": dict(
   name="DOLLY OUT, straight backward",
   phys="the whole camera rolls backward down the path away from the house, so the hedges really "
        "pass it on both sides; this is a physical move away through space, not a zoom out",
   start="close on the two of them standing together in the open doorway",
   path="straight backward down the front path, staying level at standing height, the garden hedge "
        "sliding past through both sides of the frame",
   amount="it retreats the whole length of the front path",
   end="wide, the little house small between the hedges with the green fields opening out behind it"),
}


def move_block(k):
    m = MOVES[k]
    return ("CAMERA MOVE, one move only, running for the whole eight seconds: " + m["name"] + ". "
            + m["phys"] + ". It starts " + m["start"] + ". It travels " + m["path"] + ". "
            + m["amount"] + ". It ends " + m["end"] + ". "
            "It never pauses, never holds still and never reverses.")


# =====================================================================================
# §4.2 MAU PHONG CANH — chi dan cho canh CO phong canh trong khung
# =====================================================================================
LAND = {
 "summer": "the landscape in full saturated colour: vivid green rice fields, dark green wooded "
           "hills and a deep blue summer sky with white cloud, bright and clear, never washed out "
           "and never hazy",
 "evening":"the garden in full saturated colour: deep green leaves, wet grey stone and moss, the "
           "last warm light on them, rich and clear, never washed out and never hazy",
 "daylight":"the daylight coming in the far window bright and clean with real colour in everything "
           "it falls on, never washed out and never hazy",
}

# =====================================================================================
# §3 CO CANH · §2 GOC · §1 CHIEU CAO — ba thanh phan rieng
# =====================================================================================
SIZE = {"mcu":  "a close shot, the two of them filling most of the frame from the chest up",
        "mcu3": "a close shot, the three of them filling most of the frame from the chest up",
        "ms":   "a medium shot, the figures from the knees up in frame"}
ANGLE = {"eye":     "their faces seen in three-quarter profile, clearly visible but never turned "
                    "towards the camera",
         "ots":     "seen over the shoulder of the nearer one, the back of her head and one shoulder "
                    "filling the near corner of the frame",
         "high_sl": "a slightly high angle, looking down over their shoulders at what lies between them",
         "behind":  "seen from directly behind them"}
HEIGHT = {"table":  "the camera down at the level of the tabletop itself, close enough to reach the dishes",
          "seated": "the camera down at their own seated height on the floor, low and near",
          "eye_st": "the camera at their own standing eye height"}
OPTICS = ("shallow depth of field with the background melting softly out of focus, and one "
          "out-of-focus object at the very edge of the near foreground")

POV_OUT  = ("a first-person shot: the camera is the viewer's own eyes and the whole picture is only "
            "ever what lies out in front of them")
POV_WAVE = ("a first-person shot: the camera is the viewer's own eyes, and the only part of them "
            "ever in the picture is their own one raised hand entering at the very edge of the frame "
            "as they wave, everything else being what lies out in front of them")

AVOID = (
    # ⚠️ Khong lap lai "NO letters / no film strip" o day — dong guard NGAN dau prompt da noi,
    #    lap lai chi ton ~200 ky/prompt. Chi giu phan KHONG co o dong ngan:
    "no picture of film stock and no border of any kind around the picture; "
    "no modern object of any kind, no smartphone, no LED lighting, no plastic bottle, no air "
    "conditioner, no modern clothing, no sneakers with logos; "
    "nobody looks at the camera, nobody is posed for the camera, no staged tableau; "
    "no face filling the whole frame; "
    "the camera never stops moving and never holds still, it never pauses and it never reverses "
    "its direction part way through; "
    "no dark vignette and no shading at the corners, no sepia or brown-washed colour, no faded "
    "washed-out look, no HDR look, no oversaturated colour, no studio lighting; "
    "no camera shake, no handheld wobble, no jerky or stuttering motion, no speed ramping, no slow "
    "motion, no skipped or repeated frames; "
    "no rubbery bending limbs, no feet sliding across the ground, no floating or gliding movement, "
    "no disembodied hands, no extra fingers, no morphing objects"
)
AVOID_SUBJ = ("; no part of the viewer's own body is ever in the picture, no hands, no arms, no "
              "legs, no feet, no lap and no shoulders in the frame, and the viewer is never seen "
              "from outside")

STYLE = (
    "1970s Japan, the Showa era filmed as if it were happening right now on a modern cinema camera, "
    "crisp and sharp with fine clean detail, "
    "full rich natural colour with warm sunlit skin, true deep greens and clear blues, "
    "fine photographic film grain evenly over the whole picture, "
    "evenly exposed right into all four corners with no darkening or shading at the edges, "
    "the picture fills the whole frame right out to all four edges, "
    "horizontal landscape video in 16:9 aspect ratio, 1920x1080 widescreen, clearly wider than it "
    "is tall, not vertical and not square"
)
CAM = ("The camera carries out that one move, and only that move, steadily from the first frame to "
       "the last without ever coming to rest: smooth and mechanical as if on a dolly, never "
       "handheld and never shaky, never speeding up or slowing down, and the background stays solid "
       "and does not warp as it passes.")
MOTION = ("Slow deliberate natural human motion at one even speed from first frame to last, the "
          "weight shifting through the body before each movement, every action carried through once "
          "in a single unbroken arc and never undone, continuous single take, no cuts, no reversing.")

CA = {
 # ⚠️ Giu nguyen phan KHUON MAT (luat kenh: `check_cast_unique.py` doi phai ta mat),
 #    RUT GON phan do mac — v5 them khoi STAND + dien xuat nen phai mua lai do dai.
 "musume": 'a woman of about twenty-three, long narrow face, small pointed chin, thin straight '
           'eyebrows low over quiet deep-set eyes, pale skin, hair in a short neat wave, in a white '
           'collared blouse and pale cardigan',
 "haha":   'a woman in her forties, broad square face, high flat cheekbones, thick straight eyebrows, '
           'narrow eyes with deep smile lines, short blunt nose, greying hair in a low knot, in a grey '
           'wrap-around apron',
 "chichi": 'a man in his forties, lean angular face, hollow cheeks, heavy jaw, bushy eyebrows, high '
           'forehead, in a plain open-necked shirt',
 "joushi": 'a man in his fifties, long bony face, heavy jaw, hollow temples, sparse eyebrows over heavy '
           'eyelids, grey stubble, in a white shirt with rolled sleeves and a loosened tie',
 "douryou":'a woman of about twenty-five, small heart-shaped face, pointed chin, high round eyebrows '
           'over large round eyes, freckles across the nose, hair tied back, in a dark pinafore apron',
 "nakoudo":'a woman in her fifties, round full face, soft heavy jowls, thin high-arched eyebrows over '
           'small narrow eyes, flat wide nose, hair pinned back tight, in a subdued formal kimono',
}
# =====================================================================================
# §1.1 MAY DUNG O CHO CUA AI — cau lam "goc nhin that hon" (user chot 2026-09-21).
#   Chieu cao la mot SO DO; cau nay tra loi "toi dang dung o dau". Thieu no thi t2v chon
#   cho KHONG AI DUNG DUOC (giua mat ban, lo lung trong tuong) => khung doc ra la "may bay".
# =====================================================================================
STAND = {
 "desk_side":  "a colleague standing at the end of that same desk",
 "bench_next": "the person sitting on the same bench on her other side",
 "corridor":   "one of the others standing further along the corridor",
 "counter":    "the next person waiting in the queue at that counter",
 "table4th":   "the fourth person sitting at that table",
 "tatami3rd":  "the fourth person kneeling at that stand",
 "seat_next":  "the passenger sitting on the seat beside them",
 "path":       "someone walking out down the path with them",
}

SC = {
 "office": 'the open floor of a Showa company office in the daytime, grey steel desks pushed '
           'together face to face in long rows, stacked paper trays and a glass ashtray, tall metal '
           'cabinets along the wall and wide windows with venetian blinds onto the town',
 "rouka":  'the corridor of a Showa office building, a worn linoleum floor and painted plaster '
           'walls, frosted glass doors along one side and a tall metal window frame at the far end',
 "yakusho":'the public counter of a Showa town hall, a long wooden counter with low partitions along '
           'it, rows of steel desks and shelves of bound files behind the staff side, high windows',
 "chanoma":'the living room of a Showa house in the evening, a low round wooden dinner table in the '
           'middle of the tatami with flat floor cushions round it, a fluorescent ceiling light with '
           'a small glass shade and a long pull cord, a wooden tea cabinet, a boxy wooden television '
           'on legs, and sliding paper screens standing open onto the garden',
 "zashiki":'the formal room of a Showa house, a tokonoma alcove with a hanging scroll and a single '
           'flower, fresh tatami, sliding paper screens open onto a small garden, flat silk floor '
           'cushions in a row and a low lacquered stand to one side',
 "densha": 'an old two-car country train in the daytime, worn blue plush bench seats facing each '
           'other, chrome grab rails, wide windows pushed half open, and open farmland outside',
 "genkan": 'the entrance of an old wooden house seen from the front path, the sliding door pushed '
           'open, a stone step and wooden sandals below it, potted plants along the wall, a clipped '
           'garden hedge on both sides of the path and rice fields beyond',
}
EXTRA_LOCK = ("the others in the room have plain ordinary faces, are seen from behind or in profile, "
              "and none of them appears anywhere else in the story")


# =====================================================================================
# §6.7 CHU KY BIEU CAM THEO NHAN VAT — chong "dieu cuoi cong nghiep"
#   user 2026-09-21: "dieu cuoi hoi cong nghiep va trong giong nhau"
#   🔴 Day la loi CAU TRUC cua v5, khong phai loi thi hanh: v5 dua MOT cau cuoi chuan roi moi
#      nhan vat dung bien the cua no. Kho cau DUNG CHUNG thi BAT BUOC sinh ra bieu cam giong
#      nhau (cung benh `feedback_prompt_khoi_chung_huy_mo_ta` + bai hoc sticker xoay vong).
#   => Bieu cam la CHU KY CUA NHAN VAT, khai cung luc voi khuon mat. Mot nguoi mot kieu suot
#      ca video; hai nguoi trong CUNG mot khung thi KHONG duoc cung kieu (gate may).
#   Truc bien thien doc tu mau (t=96/131/163/221/450): TUOI + VI THE, khong phai ngau nhien.
# =====================================================================================
LEVEL = {"full":  "",
         "held":  " but this time he or she keeps most of it back",
         "trace": " and this time only the very start of it shows before it is gone"}


# =====================================================================================
# 5.1 VAT MAU RUC — mau phai den tu VAT, khong den tu grade.
#   user 2026-09-21: "Video co nhung vat trang tri hoac quan ao co mau sac ruc ro di.
#                     Co the cac phu kien, van phong pham de lam video sinh dong hon"
#   Doc lai bang boi canh cu: grey steel desks / worn linoleum / plain white blouse /
#   grey apron / worn blue plush / plaster walls -> KHONG MOT VAT RUC NAO. Khoi STYLE noi
#   "full rich natural colour" cung vo nghia neu trong khung khong co gi co mau.
#   LUAT: moi canh 1-3 vat ruc, dat vao DUONG DI cua may hoac ngay canh viec dang lam,
#         va vat ruc KHONG duoc mang chu/so (model hay in chu Nhat gia len khay/phich/hop).
# =====================================================================================
PROPS = {
 "office":  "a vermilion stamp-pad case open beside the ledger, a red-and-blue pencil lying across "
            "the papers and a bottle of blue ink catching the light on the next desk",
 "rouka":   "the bouquet itself bright with red carnations and yellow chrysanthemums, and a "
            "red-and-white ribbon still tied round the paper",
 "yakusho": "a vermilion stamp-pad case sitting open on the counter, a red pencil in the tray "
            "beside it and a bolt of red cord binding the older files on the shelf behind",
 "chanoma": "a flower-patterned vacuum flask standing on the tea cabinet, flower-patterned teacups "
            "on the tray and a folded scarlet cloth wrapper at the edge of the tatami",
 "zashiki": "one deep red carnation in the alcove vase, a scarlet silk cloth under the low stand "
            "and a persimmon-orange fruit on a small dish to one side",
 "densha":  "a scarlet cloth bundle and a yellow-banded straw hat left on the seat opposite",
 "genkan":  "a red-lacquered pail by the step, scarlet geraniums in the pots along the wall and a "
            "flower-patterned cloth bundle in her free hand",
}
PROP_TAIL = " with no writing or marking of any kind on any of them"


# =====================================================================================
# 6.8 CHU KY CUOI XOAY GIUA CAC VIDEO — so dang ky, khong phai thien chi.
#   user 2026-09-21: "Dung video nao cung lap lai dong tac cuoi nhu the.
#                     Moi video co 1 dieu cuoi khac nhau di"
#   6.7 chi giai MOT TANG: trong mot video moi nguoi mot kieu. Nhung bo chu ky la HANG SO
#   cua tool => video sau lai dung dung bo do. Sau 3 video ca kenh chi co 6 dieu cuoi.
#   Kenh da giai dung bai nay o KHUON MAT (CAST_REGISTRY.json + check_cast_unique.py) —
#   ap y nguyen co che: moi nguyen mau co KHO >=4 bien the, moi video RUT mot bien the
#   CHUA DUNG, ghi vao so. Kho can thi viet bien the moi, KHONG quay lai dung cai cu.
# =====================================================================================
EXPR_BANK = {
 "w40": {   # phu nu 40s (haha) — me, dang lam viec nha
  "w40_hands":  "it happens while her hands are still working and her eyes stay down on what she is "
                "holding, never lifting to be seen, and only the cheeks and the lines at her eyes move",
  "w40_turn":   "she turns her face away towards the wall before it shows at all, and all that is "
                "left facing forward is one shoulder shaking twice and going still",
  "w40_sleeve": "she catches it in the back of her wrist with her sleeve half over her mouth, and "
                "then she has to put the whole thing down before she can carry on",
  "w40_sigh":   "it comes out as one short breath through the nose and nothing more, and she shakes "
                "her head slowly at the same time as if telling herself off",
  "w40_apron":  "she wipes both hands down the front of her apron first, as if that were what she "
                "had turned round for, and only then does her face give way",
  "w40_scold":  "it comes out mixed with a word of scolding, so the mouth is telling them off while "
                "everything round the eyes is doing the opposite",
 },
 "w50": {   # phu nu 50s (nakoudo) — vi the cao hon, kiem che
  "w50_eyes":   "her eyes go first and crease into two slits, the cheeks pushing up, the mouth "
                "barely opening at all, and her head tilts a little towards whoever she is looking at",
  "w50_fan":    "she brings one hand up flat in front of her mouth and keeps it there, and the only "
                "thing left to read is how far her eyes have narrowed",
  "w50_rock":   "she rocks back on her heels once with her hands still folded in her lap, and lets "
                "it out through closed teeth in three short pushes",
  "w50_nodown": "she nods down at the floor twice, slowly, before she looks up again, and by then "
                "it has already gone",
  "w50_sleeve": "she draws one sleeve up across the lower half of her face and holds it there, and "
                "lets only the eyes finish it",
  "w50_tea":    "she reaches for her tea in the middle of it and drinks, which stops it dead, and "
                "sets the cup down with her face already level again",
 },
 "wy": {    # phu nu tre 20s (musume, douryou) — ne nep thoi do
  "wy_nose":    "she holds it in behind closed lips and it escapes through her nose instead, one "
                "hand going up towards her mouth and stopping half way, and she looks down and to the side",
  "wy_loud":    "her mouth goes first, short and quick and out loud, then she clamps it shut herself "
                "and glances round to see who heard, her shoulders still going",
  "wy_bite":    "she bites the inside of her lip to stop it, the corners of her mouth going anyway, "
                "and she looks hard at her own hands until it passes",
  "wy_double":  "it comes out twice, a small one and then a bigger one she was not expecting, and "
                "she covers the second one with both hands",
  "wy_shoulder":"nothing happens on her face at all for a moment and then both shoulders drop and "
                "come up once, and only after that does the smile arrive",
  "wy_away":    "she turns her head right away to the window and laughs at the window instead, and "
                "comes back with her face already composed",
  "wy_apron":   "she presses the back of one wrist against her mouth, still holding whatever is in "
                "the other hand, and her eyes go very wide above it",
  "wy_late":    "she does not react at all at first, then it arrives a beat too late and all at "
                "once, and she apologises with a small bow while it is still going",
  "wy_silent":  "no sound comes out of her at all, only the shoulders going and the eyes shutting, "
                "and one hand flat on the table to steady herself",
 },
 "m40": {   # dan ong 40s (chichi)
  "m40_eyesonly": "nothing of it reaches his mouth at all, he keeps his hand up and quite still, and "
                  "the only thing that changes is around his eyes",
  "m40_snort":    "it comes out of him as one snort through the nose, and he rubs the side of his "
                  "face afterwards as if that would put it back",
  "m40_look":     "he looks off to the side and away from everyone, and his jaw moves once before "
                  "he brings his face back straight",
  "m40_back":     "his shoulders go before anything else does, and he turns half away so that only "
                  "his back is doing the laughing",
  "m40_cough":    "he covers it with a cough into his fist that fools nobody, and looks for "
                  "something on the floor that is not there",
  "m40_slap":     "he slaps his own knee once, hard, and that is the whole of it, and then he is "
                  "quiet again",
 },
 "m50": {   # dan ong 50s (joushi) — cap tren, cong so
  "m50_half":     "only one side of his mouth goes, he clears his throat over the top of it, and he "
                  "looks back down at the page without letting it finish",
  "m50_glasses":  "he takes the glasses off his forehead and puts them down slowly, which is the "
                  "only thing that shows, and then he says nothing at all",
  "m50_chair":    "he leans back once so the chair takes it instead of his face, and comes forward "
                  "again with his mouth already straight",
  "m50_pen":      "he taps the pen twice on the desk in place of laughing, and his eyes stay on the "
                  "same line of the page the whole time",
  "m50_brow":     "one eyebrow goes up and stays up, and nothing else on him moves at all until he "
                  "lets it back down",
  # ⭐ THEM 2026-09-23: kho m50 co 5/6 bien the DOI DAO CU (but · kinh · ghe · trang giay · dang
 # ngoi), ma ba cast cung dung kho nay => canh dung/di bo khong co bien the nao hop.
 # Rule §6.8: kho can thi VIET BIEN THE MOI, dung quay lai cai cu. Hai cai duoi khong can gi ca.
 "m50_chin":   ("his chin comes down towards his chest once and stays there a moment with the rest of "
                "the face not moving at all, and only then does he lift it again"),
 "m50_breath": ("he lets one long breath out through the nose and his shoulders come down with it, and "
                "nothing else about him changes"),
 "m50_stand":    "he stands up in the middle of it as though he had meant to all along, and takes "
                  "it with him across the room",
 },
}
ARCH = {"haha": "w40", "nakoudo": "w50", "musume": "wy", "douryou": "wy",
        "chichi": "m40", "joushi": "m50"}
REG = Path(__file__).resolve().parent / "EXPR_REGISTRY.json"


def pick_expr(video_id):
    """Rut mot bien the CHUA DUNG cho tung cast. Ghi so => video sau khong lay lai."""
    reg = {}
    if REG.exists():
        reg = json.loads(REG.read_text(encoding="utf-8"))
    taken = {v for vid, d in reg.items() if vid != video_id for v in d.values()}
    mine, used_now = {}, set()
    for cast in sorted(ARCH, key=lambda c: (ARCH[c], c)):
        bank = EXPR_BANK[ARCH[cast]]
        free = [k for k in bank if k not in taken and k not in used_now]
        if not free:
            raise SystemExit("KHO CAN cho nguyen mau %s — viet bien the moi, dung quay lai cai cu"
                             % ARCH[cast])
        mine[cast] = free[0]
        used_now.add(free[0])
    return mine, reg


def expr_text(cast, pick):
    return EXPR_BANK[ARCH[cast]][pick[cast]]

# =====================================================================================
# (file, scene, size, angle, height, stand, move, land, expr[(cast,level)], action, extras, why)
# =====================================================================================
SHOTS = [
 ("s1_office_cha", "office", "mcu", "eye", "table", "desk_side", "dolly_row", "daylight",
  [("musume", "full"), ("joushi", "full")],
  "{musume} leans in and sets a small teacup down at {joushi}'s elbow with both hands; he keeps "
  "reading a moment longer, then lifts his eyes to her and says something short; at that she reacts, "
  "{EX:musume} and then it settles and she gives one small nod; he reacts in his own way, "
  "{EX:joushi}, while the steam off the cup tilts sideways in the draught from the blinds",
  True, "co gai NEN (ra mui) vs ong chu MOT BEN mieng + hang giong"),

 ("s2_office_futari", "office", "mcu", "ots", "seated", "bench_next", "arc_shoulder", "daylight",
  [("douryou", "full"), ("musume", "held")],
  "{douryou} leans over and puts one finger on a line of the open ledger; {musume} follows the "
  "finger; {douryou} goes off first, {EX:douryou}; {musume} is slower and quieter about it, "
  "{EX:musume}, while the loose top sheet of the ledger lifts and falls under the fan",
  True, "HAI co gai cung tuoi nhung KHAC chu ky: mot bung ra, mot nen lai"),

 ("s3_soubetsu", "rouka", "mcu", "eye", "eye_st", "corridor", "track_corridor", "daylight",
  [("musume", "trace"), ("douryou", "held")],
  "{douryou} holds a wrapped bouquet out with both arms; {musume} takes it against her chest, "
  "swallows once, her chin tightens and she keeps her eyes wide and dry on purpose, then she bows "
  "her head down over the flowers and holds it there a beat too long; when she comes up, "
  "{EX:musume}; {douryou} puts one hand on her shoulder and leaves it there, {EX:douryou}; one of "
  "the others further down the corridor is already clapping and another is looking at the floor, "
  "while the paper round the bouquet crackles open and one petal comes loose and drops",
  True, "NEN xuc dong; cuoi chi HE ra mot chut o cuoi (level trace)"),

 ("s4_yakusho", "yakusho", "mcu", "high_sl", "eye_st", "counter", "dolly_counter", None,
  [],
  "{musume} slides a folded paper across the counter; {joushi} opens a heavy bound ledger flat "
  "between them and turns it round to face her; her hand goes out towards the page, stops short of "
  "it, comes back to the edge of the counter, and only then goes out again to follow where his "
  "finger is moving; he lets his breath all the way out and his shoulders drop an inch when she "
  "finds the line, while the loose pages of the ledger lift and settle in the draught",
  True, "KHONG co cuoi — do du ta bang TAY. Canh khong cuoi thi dung nhet chu ky vao"),

 ("s5_chanoma", "chanoma", "mcu", "eye", "table", "table4th", "dolly_garden", "evening",
  [("haha", "trace")],
  "{haha} tips the squat teapot and fills a small cup, then pushes it across the worn tabletop; "
  "{musume} has both hands in her lap and does not reach for it at first, then takes it up in both "
  "hands and holds it without drinking; {haha} watches the cup and not her daughter, lets her "
  "breath all the way out and her shoulders drop an inch, and {EX:haha}, while the steam off the "
  "cup climbs and bends between the two of them and the lamp cord swings slightly",
  False, "me: bieu cam DI QUA hanh dong, mat o cai chen — muc trace"),

 ("s6_omiai", "zashiki", "mcu3", "high_sl", "seated", "tatami3rd", "dolly_alcove", "evening",
  [("nakoudo", "full"), ("haha", "full"), ("musume", "trace")],
  "{nakoudo} lays a single photograph face up on the low stand between them and sits back with her "
  "hands folded, watching the two of them and not the picture, and {EX:nakoudo}; {haha} leans right "
  "in over it at once, her eyebrows going up before the rest of her catches on, and {EX:haha}; "
  "{musume} leans in more slowly from the other side, looks at it, looks at her own hands and rubs "
  "one thumb along the other, glances up only once, and {EX:musume}; then {haha} turns the "
  "photograph a little towards her daughter and takes her own hand away from it, while the single "
  "flower in the alcove nods in the air from the garden",
  False, "BA nguoi BA chu ky khac nhau trong CUNG mot khung — day la ca kho nhat"),

 ("s7_subj_densha", "densha", None, None, None, "seat_next", "dolly_window", "summer",
  [],
  "Nobody else is in the picture at all; the short curtain above the window lifts and falls in the "
  "moving air for the whole shot, and once the shadow of a passing pole sweeps across the frame and "
  "is gone",
  False, "canh tho, 0 nguoi"),

 ("s8_subj_wave", "genkan", None, None, None, "path", "dolly_out_path", "summer",
  [("haha", "full"), ("chichi", "full")],
  "{haha} and {chichi} stand in the open doorway; {chichi} raises one hand flat and holds it up "
  "without moving it, and {EX:chichi}; {haha} waves hers quickly and keeps waving after he has "
  "stopped, and {EX:haha}; the viewer's own one hand comes up at the edge of the frame and waves "
  "back once, and at that {haha} waves harder, while the potted plants along the wall stir and one "
  "long shoot swings across the doorway",
  False, "vo chong KHAC han nhau: ong khong cuoi (chi quanh mat), ba cuoi qua hanh dong vay"),
]
POV_SHOTS = {"s7_subj_densha": POV_OUT, "s8_subj_wave": POV_WAVE}


def build(sh):
    (name, scene, size, angle, height, stand, move, land, expr, action, extras, _why) = sh
    for cast, lv in expr:                       # 6.7 chu ky rieng + 6.8 xoay giua video
        action = action.replace("{EX:%s}" % cast, expr_text(cast, PICK) + LEVEL[lv])
    for k, v in CA.items():
        action = action.replace("{%s}" % k, v)
    is_pov = name in POV_SHOTS
    stand_s = (f"The camera is placed exactly where {STAND[stand]} would be, at that person's own eye "
               f"level, and the whole shot is seen from that one place.")
    if is_pov:
        frame_block, opener = POV_SHOTS[name], "A first-person shot filmed in 1970s Japan."
    else:
        frame_block = ", ".join([SIZE[size], ANGLE[angle], HEIGHT[height], OPTICS])
        opener = f"{SIZE[size].split(',')[0]}, filmed in 1970s Japan."
    parts = [opener,
             "NO letters, NO words, NO numbers and NO logos anywhere in the picture, and no film "
             "strip, no sprocket holes and no frame line along its edges.",
             move_block(move),
             stand_s,
             AVOID + (AVOID_SUBJ if is_pov else "") + ".",
             action + ".",
             frame_block + ".",
             SC[scene].rstrip(",") + ".",
             "Bright colour in the props: " + PROPS[scene] + PROP_TAIL + "."]
    if land:
        parts.append(LAND[land] + ".")
    if extras:
        parts.append(EXTRA_LOCK + ".")
    parts += [STYLE + ".", CAM, MOTION,
              "Remember: the camera must move the whole way through as described; each person's "
              "reaction is their own and no two of them react the same way; the feeling must build "
              "and then settle, never held as a pose; no text and no film-strip edge anywhere; "
              "nobody looking at the camera."]
    return " ".join(" ".join(p.split()) for p in parts)


BAD = ("respectful distance", "holds one position", "slight vignette", "deep focus so both",
       "35mm", "16mm", "8mm", "hands only", "feet only", "the subject remains in frame",
       "at chest height")
FLAT = ("they laugh", "she smiles", "he smiles", "they smile politely", "looks surprised",
        "looks shy", "she hesitates", "she is moved", "looks content", "they both laugh")


PICK = {}


def main():
    from collections import Counter
    global PICK
    PICK, reg = pick_expr(VIDEO_ID)
    flow, rows = [], []
    used = Counter()
    for sh in SHOTS:
        p = build(sh)
        flow.append(p)
        rows.append((len(flow), f"demo16_{sh[0]}.mp4", sh[6], len(p),
                     "+".join(c for c, _ in sh[8]) or "-", sh[11]))
        for c, lv in sh[8]:
            used[(c, lv)] += 1

    bad = 0
    for i, p in enumerate(flow, 1):
        sh = SHOTS[i - 1]
        is_pov = sh[0] in POV_SHOTS
        gpos = p.find("NO letters") * 100 // len(p)
        mpos = p.find("CAMERA MOVE, one move only") * 100 // len(p)
        nmv = sum(1 for v in MOVES.values() if v['name'] in p)
        hit = [b for b in BAD if b in p]
        flat = [f for f in FLAT if f in p]
        ncast = sum(1 for v in CA.values() if v in p)
        # v7: ban spec 6 o — TEN + VAT LY(khong phai zoom) + BAT DAU + DUONG DI + LUONG + KET
        three = all(t in p for t in ("CAMERA MOVE, one move only", "It starts ", "It travels ",
                                     "It ends ", "not a zoom",
                                     "never pauses, never holds still and never reverses"))
        # ⭐ §6.7 muc 2: hai cast trong CUNG khung phai KHAC chu ky
        sigs = [PICK[c] for c, _ in sh[8]]
        uniq = len(set(sigs)) == len(sigs)
        left = [t for t in ("{EX:", "{musume}", "{haha}") if t in p]   # placeholder con sot
        g = [gpos <= 15, mpos <= 15, nmv == 1, not hit, three, not flat, uniq, not left,
             "The camera is placed exactly where" in p,
             "16:9 aspect ratio" in p, "no film strip" in p,
             "no darkening or shading at the edges" in p,
             "without ever coming to rest" in p, "crisp and sharp" in p,
             "no two of them react the same way" in p,
             ("no hands, no arms" in p) == is_pov,
             ncast >= 2 or sh[0] == "s7_subj_densha",
             (sh[7] is None) or ("full saturated colour" in p or "real colour in everything" in p)]
        bad += sum(not x for x in g)
        print("D%d %-24s%5d ky | g@%2d%% m@%2d%% | 3moc=%s chu-ky=%d/%s | %s" % (
            i, rows[i - 1][1], len(p), gpos, mpos, "Y" if three else "N",
            len(set(sigs)), len(sigs) if sigs else "-",
            "OK" if all(g) else "FAIL " + str([j for j, x in enumerate(g) if not x])))
    # ⭐ §6.7 muc 4: moi (chu ky, cuong do) <= 3 lan ca video
    over = {k: n for k, n in used.items() if n > 3}
    print("")
    print("CHU KY RUT CHO VIDEO " + VIDEO_ID + ": "
          + ", ".join(c + "=" + PICK[c] for c in sorted(PICK)))
    reg[VIDEO_ID] = PICK
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("da ghi so: " + str(REG))
    print("chu ky dung: " + ", ".join(f"{c}/{lv}x{n}" for (c, lv), n in sorted(used.items())))
    if over:
        bad += len(over)
        print("LAP QUA 3 LAN: " + str(over))
    print("")
    print(("SACH %d/%d" % (len(flow), len(flow))) if not bad else ("%d MUC ROT" % bad))

    OUT.mkdir(parents=True, exist_ok=True)
    with io.open(OUT / FLOW, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(flow) + "\n")
    with io.open(OUT / TENF, "w", encoding="utf-8", newline="\n") as f:
        f.write("# " + FLOW + " - camera-language.md 1.1 (cho dung cua may) + 6.6 + 6.7 (chu ky bieu cam)\n"
                "# v6 sua loi user bat: 'dieu cuoi hoi cong nghiep va trong giong nhau'\n"
                "#   v5 dua MOT cau cuoi chuan roi moi nhan vat dung bien the => bat buoc giong nhau.\n"
                "#   v6: moi CAST mot CHU KY rieng (khai cung luc voi khuon mat), doc tu mau theo\n"
                "#       truc TUOI + VI THE. Hai nguoi trong cung mot khung KHONG duoc cung chu ky.\n"
                "#   6 chu ky: ba-gia-dang-lam-viec / ba-gia-mat-truoc / co-gai-nen /\n"
                "#             co-gai-bung-roi-tu-khoa / ong-chu-mot-ben-mieng / ong-khong-cuoi\n"
                "#   3 cuong do: full / held / trace (dung khi phai lap lai mot chu ky)\n"
                "# NGHIEM THU: MAD blur trong shot >= 8,2 | %khung dung yen <= 10%\n"
                "#   KHONG do vien/tam va G o muc mot clip (thong ke ca bai)\n"
                "# SOI MAT: 1) hai nguoi trong mot khung co cuoi KHAC nhau khong\n"
                "#          2) bieu cam co DI QUA hanh dong khong, hay dung mot pose 8 giay\n"
                "#          3) may co dung o cho NGUOI dung duoc khong\n\n")
        f.write("%-5s%-26s%-19s%-7s%-18s%s\n" % ("dong", "file", "nuoc may", "ky", "chu ky", "y do"))
        for n, nm, mv, ln, ex, why in rows:
            f.write("%-5s%-26s%-19s%-7s%-18s%s\n" % (n, nm, mv, ln, ex, why))
    print('')
    print('-> ' + str(OUT / FLOW))
    print('-> ' + str(OUT / TENF))


if __name__ == "__main__":
    main()
