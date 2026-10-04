# -*- coding: utf-8 -*-
"""Video 17 — 昭和の会社がくれたもの5選. 112 canh, khuon `camera-language.md` (2026-09-21).

⭐⭐ DAY LA MOT CAU CHUYEN CO DAU CO DUOI, khong phai 112 prompt roi ghep lai
   (user chot 2026-09-22: *"Nó là 1 câu chuyện có đầu có đuôi nhé chứ không phải ghép từng
   prompt vào 1"*). Xuong song: **MOT NGUOI, MOT CONG TY, 37 NAM** —
     1968 vao lam (25 tuoi) -> 1975 dinh cao tang luong (40) -> cuoi, con ra doi ->
     ky tuc -> 社宅 -> gui tiet kiem o ket cong ty -> 2005 ve huu (60) -> NAY (78).
   A_HONNIN / A_HONNIN_TEI / A_IMA la CUNG MOT NGUOI o ba tuoi: cau khuon mat chep Y NGUYEN,
   chi doi toc + nep nhan + do mac. Nguoi xem phai nhan ra do la mot doi nguoi, khong phai
   ba nguoi khac nhau.

🔗 NOI LIEN: canh nao co `out` thi canh NGAY SAU trong CUNG boi canh mo bang trang thai ket
   do ("Continuing from that same moment, ..."). Day la thu bien mot chuoi canh thanh mot
   doan phim. ⛔ Canh doi boi canh thi CAT (khong noi), neu khong t2v ve lai canh cu.

⛔ KHONG chep hang so: STYLE / AVOID / MOTION / CAM / SIZE / ANGLE / HEIGHT / LAND / OPTICS /
   EXPR_BANK / LEVEL / EXTRA_LOCK / PROP_TAIL deu IMPORT tu `gen_demo16_kioku`.

🔴 NAM BAY CUA RIENG BAI NAY — da dong vao prompt, dung go ra:
 a. ⛔ To giay tren bang thong bao / bang luong / so tiet kiem: KHONG BAO GIO doc duoc chu.
    Moi canh co giay deu quay goc nghieng hoac bi tay che. So de Remotion ve bang font.
 b. ⛔ KHONG lich treo tuong, nhiet ke, bang bieu co truc (`ai-video-regen.md` §3).
 c. ⛔ Van phong Showa KHONG co man hinh may tinh — chi may tinh co quay tay, dien thoai quay so.
 d. 🔴 KHONG nuoc may truc dung (`camera-language.md` §7.5: PEDESTAL/CRANE = 0,995-1,009 scale,
    khong di, 3/3 ca). Can ha may thi DOLLY IN "forward and dropping as it goes".
 e. ⛔ KHONG not ruoi tren mat (user chot 2026-09-22: *"nhieu nhan vat co cai not ruoi to qua"*).

📐 112 o = 7,7 doi hinh/phut, tran o 12,0s. Clip Flow ra 8s => o >8s phai GIAN bang setpts
   (he so toi da 1,50x, trong vung "1,2-1,7x khong nhan ra"). Bang o: clips/_MAP.txt
"""
import io
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import gen_demo16_kioku as K

OUT  = Path(__file__).resolve().parents[1] / "06_VIDEO" / "17_kaisha-ga-kureta"
VER  = "v1"
VIDEO_ID = "17"
FLOW = f"videogen17_{VER}_FLOW.txt"
TENF = f"videogen17_{VER}_TENFILE.txt"
BLOCKS_MD = f"videogen17_{VER}_BLOCKS.md"

# =====================================================================================
# MOVES — §4.1 LUAT HAI MOC: moc dau -> duong di -> luong -> moc ket.
# =====================================================================================
def _m(name, phys, start, path, amount, end):
    return dict(name=name, phys=phys, start=start, path=path, amount=amount, end=end)

MOVES = {
 "in_board": _m("DOLLY IN, straight forward through the crowd",
   "the whole camera rolls forward down the corridor on a track, so the shoulders and backs of the men really pass it on both sides; a physical move through space, not a zoom and not a still frame",
   "far back down the corridor, the crowd only a dark mass of shoulders with the lit notice board glowing beyond them",
   "straight forward towards the board, the men on both sides sweeping out through the edges of the frame, staying level at their own standing eye height",
   "it closes about two thirds of the distance to the board",
   "close behind the two men at the front, the back of one head filling the near corner and the pinned sheet beyond them at a steep angle, never square to the camera"),
 "out_board": _m("DOLLY OUT, straight back down the corridor",
   "the whole camera rolls backwards along the corridor on a track, so the men and the wall really pass it; a physical move, not a zoom out",
   "close on the faces of the two men at the front of the crowd",
   "straight back away from the board, the crowd closing together in front of it as the camera leaves, the corridor walls sliding in from both sides",
   "it pulls back about the length of the corridor",
   "the whole corridor in frame with the crowd small at the far end under the board"),
 "track_desks": _m("TRACKING, sideways left to right along the desks",
   "the whole camera slides sideways across the office floor on a dolly, parallel to the row, so the desks really pass across the frame; a physical move, not a pan",
   "on the near end of the row, a hand-cranked calculator and a black dial telephone large in the foreground",
   "sideways along the row at tabletop height, each desk and each seated man sliding out through the left of the frame as the next comes in from the right",
   "it travels the length of about four desks",
   "on him at the far end of the row, looking up as the camera settles"),
 "track_desks_back": _m("TRACKING, sideways right to left along the desks",
   "the whole camera slides sideways back across the office floor on a dolly, parallel to the row; a physical move, not a pan",
   "close on his hands at his own desk",
   "sideways back along the row at tabletop height, paper trays and telephones sliding through the frame one after another",
   "it travels the length of about three desks",
   "on the window end of the room, the venetian blinds half open onto the town"),
 "in_desk": _m("DOLLY IN, straight forward to the desk",
   "the whole camera rolls forward between the desks on a track, so the row ends really pass it on both sides; a physical move, not a zoom",
   "at the end of the aisle with the whole office floor open in front of it",
   "straight forward down the aisle, the desk corners sweeping out through both edges of the frame, holding tabletop height",
   "it closes about three quarters of the distance to him",
   "close on him and the papers under his hands"),
 "in_safe": _m("DOLLY IN, forward and dropping as it goes",
   "the whole camera rolls forward on a track and sinks lower along the way, so the room really opens over the top of the counter; a physical move through space, not a crane shot on a post",
   "standing height in the doorway of the general affairs corner, the counter a bar across the bottom of the frame",
   "straight forward towards the safe, dropping steadily until it is level with the counter top, the ledger and the stamp pad passing out through the bottom of the frame",
   "it closes about half the distance and drops about the height of a standing man's chest",
   "level with the counter, the dial of the safe filling the middle of the frame with his hands coming into it"),
 "arc_shoulder": _m("ARC, the camera orbiting slowly round his shoulder",
   "the camera swings round him along a curve while holding the same distance, so the wall behind slides across; a physical move round him, not a zoom",
   "behind his shoulder, the back of his head filling the near corner and what he is holding soft and out of focus beyond it",
   "round that shoulder from his left towards his front, keeping the shoulder in the near corner and holding its own height",
   "it travels about a quarter of the way round him",
   "on his face clear, with the thing in his hands sharp in front of him"),
 "track_walk": _m("TRACKING, sideways along the open walkway",
   "the whole camera slides sideways along the outdoor walkway on a dolly, parallel to the doors, so the railing runs steadily through the bottom of the frame",
   "at one end of the walkway, washing hanging close in the near foreground",
   "sideways past one identical steel door after another, each with its small frosted window, the yard and the climbing frame below sliding past beyond the railing",
   "it travels past about five doors",
   "on her at the far end with the block behind her"),
 "in_yard": _m("DOLLY IN, straight forward across the yard",
   "the whole camera rolls forward across the concrete yard on a track, so the bicycles and the climbing frame really pass it; a physical move, not a zoom",
   "at the gate of the housing block, the whole four storey building and its balconies of washing in frame",
   "straight forward towards the stairwell, the parked bicycles sweeping out through the left of the frame and the climbing frame through the right",
   "it closes about half the distance to the stairwell",
   "at the foot of the stairs, the open walkways going up out of the top of the frame"),
 "in_rows": _m("DOLLY IN, straight forward down the two rows",
   "the whole camera rolls forward between two rows of standing colleagues on a track, so they really pass it on both sides; a physical move, not a zoom",
   "at the near end of the cleared corridor, the two rows receding away and him small between them",
   "straight forward between the rows, the nearest shoulders sweeping out through both edges of the frame, holding standing height",
   "it closes about three quarters of the distance to him",
   "close on him from the chest up as the bouquet comes into his hands"),
 "out_room": _m("DOLLY OUT, straight back across the room",
   "the whole camera rolls backwards through the room on a track, so the table edge and a chair back really pass it; a physical move, not a zoom out",
   "close on his hands and what lies flat on the table under them",
   "straight back away from the table at the same height, the table edge and then a chair back passing out through the bottom of the frame",
   "it pulls back about the length of the room",
   "the whole room in frame with him small at the table and the window bright beyond him"),
 "in_table": _m("DOLLY IN, straight forward to the low table",
   "the whole camera rolls forward across the tatami on a track, so the edge of the table really passes it; a physical move at floor height, not a zoom",
   "in the doorway of the living room, the low table small in the middle of the tatami with the two of them at it",
   "straight forward towards the table, the near cushion and then the table edge passing out through the bottom of the frame, staying down at their own seated height",
   "it closes about two thirds of the distance to them",
   "close on the two of them across the table, the teapot between them"),
 "in_kitchen": _m("DOLLY IN, straight forward past the rice bin",
   "the whole camera rolls forward across the kitchen floor on a track, so the corner of the worktop really passes it; a physical move, not a zoom",
   "in the kitchen doorway, the wooden rice bin large and dark in the near foreground",
   "straight forward past the rice bin, the bin sweeping out through the left of the frame, staying level with the worktop",
   "it closes about half the distance to her",
   "close on her hands at the worktop and her face above them"),
 "in_lane": _m("DOLLY IN, forward along the lane",
   "the whole camera rolls forward along the narrow lane on a track, so the fences and gates really pass it on both sides; a physical move, not a zoom",
   "at the mouth of the lane with the men walking away from the camera towards the main road",
   "forward along the lane behind them at their own walking pace, the wooden fences sliding out through both edges of the frame",
   "it closes about half the distance to the last of them",
   "close behind him as he turns in at a gate"),
 "creep_still": _m("CREEP IN, almost imperceptibly forward",
   "the camera creeps forward on a track so slowly that only the edges of the frame show it, while the steam, the curtain and the dust in the light carry all the movement; a physical move, not a still frame",
   "on the whole quiet room with the one lit thing small in the middle of it",
   "forward towards that one thing, the near furniture edging out of the bottom corners of the frame",
   "it closes about a third of the distance",
   "on that one thing alone, the room soft and dark around it"),
}


def move_block(k):
    m = MOVES[k]
    return ("CAMERA MOVE, one move only, running for the whole eight seconds: " + m["name"] + ". "
            + m["phys"] + ". It starts " + m["start"] + ". It travels " + m["path"] + ". "
            + m["amount"] + ". It ends " + m["end"] + ". "
            "It never pauses, never holds still and never reverses.")

# =====================================================================================
# SC — BOI CANH
# =====================================================================================
SC = {
 "keijiban": 'the end wall of a Showa office corridor where a large cork notice board hangs, a few loose sheets pinned to it, a worn linoleum floor and painted plaster walls, a tall metal window frame at the far end letting flat daylight down the corridor',
 "office":   'the open floor of a Showa company office in the daytime, grey steel desks pushed together face to face in long rows, a hand-cranked mechanical calculator and a black rotary dial telephone on the rows, stacked paper trays and a glass ashtray, tall metal cabinets along the wall and wide windows with venetian blinds, and no screens of any kind',
 "rouka":    'the corridor of a Showa office building, a worn linoleum floor and painted plaster walls, frosted glass doors along one side and a tall metal window frame at the far end',
 "soumu":    'the general affairs corner of a Showa office, a tall grey steel safe with a heavy dial standing against the wall, a wooden counter in front of it, a long ledger and a stamp pad on the counter, filing cabinets and a single bare pendant lamp above',
 "soubetsu": 'a cleared corridor on a Showa office floor in the late afternoon, the desks pushed back at one end, colleagues standing in two loose rows along the walls, the venetian blinds half down at the windows behind them',
 "ryou":     'the corridor of a Showa company dormitory at night, a worn wooden floor, identical thin doors along one side, a single shaded bulb at each end, a low shoe rack and a shared telephone on a small table against the wall',
 "ryoushitsu":'a three-mat room in a Showa company dormitory, a thin futon folded in one corner, a small desk under the window with a gooseneck lamp, a wooden locker, a single shelf and a window onto the next block',
 "shataku":  'the open outdoor walkway of a Showa company housing block in the late afternoon, concrete underfoot and a painted steel railing along the open side, identical steel doors in a row each with a small frosted window, and above the railing a long bamboo drying pole resting in a pair of iron brackets fixed to the wall, shirts and towels already hanging from it on wooden clothes pegs, more poles of washing along the balconies beyond',
 "shataku_niwa":'the concrete yard of a Showa company housing block, a four storey block with open walkways above, every balcony carrying a long bamboo drying pole in iron brackets with washing pegged along it, a row of bicycles leaning against the wall and a single steel climbing frame',
 "chanoma":  'the living room of a Showa house in the evening, a low round wooden dinner table in the middle of the tatami with flat floor cushions round it, a fluorescent ceiling light with a long pull cord, a wooden tea cabinet with sliding glass doors and sliding paper screens along one side',
 "daidokoro":'the kitchen of a Showa house at night, a tiled worktop and a deep concrete sink, a two-ring gas burner with a blackened kettle, open shelves of enamel bowls and tin canisters, a wooden rice bin standing in the corner and one bare bulb over the worktop',
 "genkan":   'the doorway of a Showa house seen from just inside, a sunken concrete entrance floor with lace-up shoes set out on it, a wooden shoe cabinet against the wall and a frosted glass sliding door half open onto the lane',
 "michi":    'a narrow Showa residential lane in the early morning, wooden fences and low gates on both sides, a telegraph pole, a round red postbox at the corner and men in work jackets walking the same way towards the main road',
 "ima_ie":   'a present-day Japanese living room, a low sofa and a plain table, a wide window with a plain curtain and everyday daylight, nothing on the table but one flat lidded box',
}

# =====================================================================================
# CA — DAN DIEN. MAT (khong doi ca video) + DO (doi theo boi canh). ⛔ khong not ruoi.
# =====================================================================================
CA = {
 "honnin":  'a man of about forty, wide square face, low flat forehead with a straight hairline, short thick eyebrows set far apart, single-lidded eyes slanting up very slightly at the outer corners, broad flat nose, a deep vertical crease between the brows, hair parted low on one side, in a plain white short-sleeved shirt with the collar open',
 "honnin_tei":'a man of about sixty, wide square face, low flat forehead with a straight hairline, short thick eyebrows set far apart, single-lidded eyes slanting up very slightly at the outer corners, broad flat nose, a deep vertical crease between the brows, hair now iron grey and thin at the temples with deep lines across the forehead, in a plain dark grey suit',
 "ima":     'a man of about seventy-eight, wide square face, low flat forehead with a straight hairline, short thick eyebrows set far apart, single-lidded eyes slanting up very slightly at the outer corners, broad flat nose, a deep vertical crease between the brows, hair now white and sparse, cheeks fallen in, in a plain beige cardigan',
 "tsuma":   'a woman of about thirty-five, long oval face, high rounded forehead, thin curved eyebrows set high, wide double-lidded eyes slightly sunken, low cheekbones, small round chin with a dimple in the right cheek, hair tied back low at the neck, in a plain blouse with a plain apron over it',
 "kachou":  'a man of about fifty-five, short blunt rectangular face, heavy square jaw, hairline receded deeply at both temples, thick grey eyebrows over heavy hooded eyelids, large nose with a pronounced bridge, a thin trimmed moustache, in a white shirt with a dark tie and sleeve garters',
 "douryou": 'a young man of about twenty-eight, long narrow face, prominent cheekbones, pointed chin, straight dark eyebrows low over large double-lidded eyes, narrow straight nose, thick hair parted in the middle, in a pale short-sleeved shirt with a thin dark tie pulled loose',
}
ARCH = {"honnin": "m40", "douryou": "m40", "honnin_tei": "m50", "ima": "m50", "kachou": "m50",
        "tsuma": "w40"}

# 🔴 BAN — chu ky doi mot DAO CU ma cast/canh khong co thi no choi voi hanh dong.
BAN = {
 "honnin_tei": ["m50_glasses", "m50_pen", "m50_chair"],
 # ima ngoi ban nhung co canh cam to giay dung len => cam ca ghe/trang giay/dung day
 "ima":        ["m50_glasses", "m50_pen", "m50_chair", "m50_half", "m50_stand"],
 # kachou co canh dung o cua so · di doc day ban · dong ket => cam MOI bien the doi dao cu
 "kachou":     ["m50_glasses", "m50_pen", "m50_chair", "m50_half", "m50_stand"],
 "honnin":     [],
 "douryou":    [],
 "tsuma":      ["w40_apron"],
}

# =====================================================================================
# PROPS — §5.1 mau ruc den tu VAT, 1-3 vat/canh, vat ruc KHONG mang chu/so.
# =====================================================================================
PROPS = {
 "keijiban": [
  "a red fire-bell box on the wall by the window and a bundle of red cord hung on a nail beside it",
  "a scarlet cloth bundle set down on the window ledge and a yellow plastic bucket by the skirting",
  "an orange enamel jug on the ledge and a strip of red-and-white tape left over a doorway further down",
  "a dark red cushion left on a chair pushed against the wall and a green glass bottle on the ledge"],
 "office": [
  "a bottle of blue ink catching the light on the near desk and a yellow plastic desk mat under the papers",
  "a dark red ledger cover standing on end in a tray and a green shaded lamp on the far desk",
  "an orange enamel teacup beside the telephone and a bundle of red cord round the papers in the tray",
  "a flower-patterned vacuum flask standing on the cabinet and a yellow pencil case open on the desk"],
 "rouka": [
  "a red fire bucket on a bracket by the window",
  "a scarlet cloth bundle carried under one arm and a green mop standing in the corner",
  "an orange enamel jug left on the floor by the wall"],
 "soumu": [
  "a vermilion stamp-pad case sitting open on the counter",
  "a bolt of red cord binding the older files on the shelf behind and a green ink bottle on the counter",
  "a dark red ledger cover on the shelf and an orange enamel cup beside the lamp",
  "a yellow paper tag tied to the safe handle and a scarlet cloth folded on the counter end"],
 "soubetsu": [
  "the bouquet itself bright with red carnations and yellow chrysanthemums, and a red-and-white ribbon tied round the paper",
  "a red-and-white ribbon still tied round the paper of the bouquet and an orange enamel cup left on the low table"],
 "ryou": [
  "a red plastic washbasin on the shoe rack",
  "a yellow towel over one shoulder and a green kettle on the shared table"],
 "ryoushitsu": [
  "a yellow plastic desk mat, a red-and-blue pencil lying on it and a scarlet cloth wrapper folded on the locker"],
 "shataku": [
  "a scarlet plastic pail by one of the doors and a flower-patterned cloth wrapper folded over the railing",
  "a red child's tricycle in the yard below and an orange towel pegged on the railing",
  "a green watering can outside one door and a yellow plastic basin upturned beside it",
  "a dark red quilt airing over the railing and a blue enamel bowl on the concrete"],
 "shataku_niwa": [
  "a red tricycle on the concrete and scarlet geraniums in pots along the wall",
  "a flower-patterned quilt airing over one balcony and a yellow ball left under the climbing frame",
  "a green bicycle with a wicker basket at the end of the row and an orange bucket by the wall"],
 "chanoma": [
  "a flower-patterned vacuum flask on the tea cabinet and flower-patterned teacups on the tray",
  "a folded scarlet cloth wrapper at the edge of the tatami and a red-lacquered tray by the table",
  "a deep red cushion set at one side of the table and an orange persimmon on a small dish",
  "a ball of red wool with needles through it beside the cabinet and a green glass ashtray on the table"],
 "daidokoro": [
  "a red-lacquered pail under the worktop and a flower-patterned enamel bowl on the shelf",
  "a scarlet cloth on its hook by the sink and a yellow plastic colander on the worktop",
  "an orange enamel kettle on the burner and a green glass bottle on the shelf"],
 "genkan": [
  "a red-lacquered pail by the step and scarlet geraniums in the pots along the wall",
  "a yellow umbrella standing in the corner and an orange cloth bundle on the shoe cabinet"],
 "michi": [
  "a bright red postbox at the corner and a red fire bucket on a post",
  "a flower-patterned cloth bundle in one woman's hand and a green bicycle leaning at a gate",
  "an orange plastic crate stacked by a gate and a yellow hedge of winter flowers along one fence"],
 "ima_ie": [
  "a single red carnation in a small glass on the table",
  "a folded scarlet cloth wrapper beside the box and an orange cushion at the end of the sofa"],
}
PROP_ROT = {}   # boi canh -> so lan da dung, de XOAY VONG bo vat

# =====================================================================================
# STAND — §1.1 MAY DUNG O CHO CUA AI.
# =====================================================================================
STAND = {
 "crowd_back":  "one of the other men standing at the back of the same crowd",
 "crowd_front": "one of the men standing shoulder to shoulder with him at the front",
 "desk_side":   "a colleague standing at the end of that same desk",
 "desk_across": "the man sitting at the desk facing his across the row",
 "corridor":    "one of the others standing further along the same corridor",
 "counter_next":"the next person waiting at that counter",
 "walkway":     "a neighbour standing further along the same walkway",
 "yard":        "a neighbour crossing the same yard",
 "table4th":    "the fourth person sitting at that table",
 "kitchen_door":"someone standing in the kitchen doorway",
 "row_line":    "one of the colleagues standing in the row beside him",
 "sofa_side":   "someone sitting on the sofa across from him",
 "genkan_in":   "someone standing inside the house at the step",
 "lane":        "someone walking down the lane with them",
 "ryou_door":   "someone standing in the doorway of the next room",
}

# =====================================================================================
# SHOTS — (name, scene, size, angle, height, stand, move, land, expr, action, extras, out, why)
#   `out` = trang thai KET. Canh ngay sau, CUNG boi canh, se mo bang no => thanh mot doan phim.
# =====================================================================================
SHOTS = [
# ---------------------------------------------------------------- HOOK (0-9) : 1975年4月
 ("c000", "keijiban", "ms", "behind", "eye_st", "crowd_back", "in_board", "daylight", [],
  "{douryou} reaches up and presses a drawing pin into the top corner of a fresh sheet on the notice board; he smooths it flat with the side of his hand, then steps back one pace while the loose corner lifts and settles in the draught",
  True, "the sheet is pinned up and he is standing a pace back from the board",
  "MO BAI — to giay duoc dan len. Hien vat xuyen bai."),
 ("c001", "keijiban", "ms", "behind", "eye_st", "crowd_back", "in_board", "daylight", [],
  "men in white shirts come along the corridor from both ends and gather in front of the board; those at the front lean in until their heads almost touch the sheet, then the ones behind rise onto their toes to see over the shoulders in front of them",
  True, "a crowd is packed in front of the board, the front row leaning in",
  "dam dong keo den"),
 ("c002", "keijiban", "mcu", "eye", "eye_st", "crowd_front", "in_board", "daylight",
  [("honnin", "full")],
  "{honnin} works his way to the front of the crowd; his eyebrows go up before the rest of him catches on and his hand stops half way to the paper, then he turns his head to the man beside him, {EX:honnin}, and then he looks back and is still",
  True, "he is standing at the front of the crowd, still looking at the board",
  "NHAN VAT CHINH xuat hien — dinh cam xuc cold open"),
 ("c003", "keijiban", "ms", "ots", "eye_st", "crowd_front", "out_board", "daylight", [],
  "the man beside him says something short over his shoulder; the men behind lean in all together, then the whole group shifts one pace closer to the board and nobody steps away",
  True, None, "dam dong siet lai — dong khoi"),
 ("c004", "ima_ie", "ms", "eye", "table", "sofa_side", "creep_still", "daylight",
  [("ima", "trace")],
  "{ima} lifts a single old sheet of paper out of a flat lidded box with both hands; he turns it over once, then lays it flat and rests his palm on it, {EX:ima}, while the curtain moves at the window behind him",
  False, "the old sheet lies flat on the table under his palm",
  "⭐ NHAY VE THOI NAY — cung mot nguoi, 78 tuoi, cung to giay. Day la neo cua ca bai."),
 ("c005", "ima_ie", "mcu", "eye", "table", "sofa_side", "creep_still", "daylight", [],
  "his hand stays on the old sheet a moment longer, then slides it a little further away from him across the table, and he goes on looking at the same spot without touching it again",
  False, None, "giu lang — chuyen tiep ve qua khu"),
 ("c006", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening",
  [("tsuma", "full")],
  "{tsuma} lifts a wet shirt out of the pail and shakes it out once, threads the bamboo drying pole through both sleeves and pegs the shoulders down with two wooden clothes pegs, then straightens up and looks along the row of identical doors, {EX:tsuma}, while the washing already out moves in the wind",
  True, None, "cu soc 2 — nha o cong ty cap"),
 ("c007", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "full")],
  "{kachou} sets a long ledger down on the counter and opens it flat with both hands, turns it to face the other way, then rests one finger on the open page without looking down, {EX:kachou}; the page is always seen at a steep angle and nothing on it can be read",
  False, None, "cu soc 3 — tien duoc cong ty giu ho"),
 ("c008", "michi", "ms", "behind", "eye_st", "lane", "in_lane", "evening", [],
  "men in work jackets walk along the narrow lane in the early morning all the same way; one of them turns in at a gate, then the rest go on towards the main road and out of the frame",
  True, None, "dan nhan 「これが、昭和の会社です」 — mot the he di lam"),
 ("c009", "keijiban", "ms", "behind", "eye_st", "corridor", "out_board", "daylight", [],
  "{honnin} stands alone in front of the emptied board with his hands at his sides; he looks up at the single sheet left on it, then lowers his head and does not move",
  False, None, "chao + hua — mot nguoi, mot tam giay"),

# ---------------------------------------------------------------- M1 (10-32) : 春闘
 ("c010", "office", "ms", "eye", "table", "desk_side", "track_desks", "daylight",
  [],
  "{honnin} walks between the rows of steel desks with a folded work jacket over one arm, stops at his own desk and hangs it over the chair back, then sits down while the men already seated go on working behind him",
  True, "he is seated at his own desk with the jacket over the chair",
  "M1 vao bai — nhip lam viec thuong ngay"),
 ("c011", "office", "mcu", "eye", "table", "desk_across", "in_desk", "daylight", [],
  "he draws a stack of paper towards himself and squares it with both hands, then works the handle of the hand-cranked calculator twice and stops with his hand still on it",
  False, None, "khong khi thang hai"),
 ("c012", "keijiban", "ms", "eye", "eye_st", "corridor", "in_board", "daylight",
  [("douryou", "full")],
  "{douryou} pins a second sheet up beside the first, runs his thumb down the edge to flatten it and steps back, {EX:douryou}, while the draught lifts both loose corners together",
  True, "two sheets are pinned side by side on the board",
  "to giay yeu cau"),
 ("c013", "rouka", "ms", "behind", "eye_st", "corridor", "track_desks_back", "daylight", [],
  "three men in suits walk away down the corridor in the early morning with flat cloth folders under their arms; they pass the frosted glass doors and go out through the door at the far end",
  True, None, "dai bieu cong doan di dam phan tu sang"),
 ("c014", "rouka", "ms", "eye", "eye_st", "corridor", "in_board", None, [],
  "the same three men come back in through the far door late at night, walking towards the camera without speaking, and pass out of frame on both sides",
  True, None, "ho ve luc dem"),
 ("c015", "keijiban", "ms", "behind", "eye_st", "crowd_back", "in_board", "daylight", [],
  "the corridor fills again in the morning; the men at the front stand with their hands behind their backs and lean in, and the ones behind press closer together",
  True, "the crowd is packed tight in front of the board",
  "sang cong bo"),
 ("c016", "keijiban", "mcu", "eye", "eye_st", "crowd_front", "in_board", "daylight",
  [("honnin", "full"), ("douryou", "held")],
  "{honnin} reads the sheet and lets his breath out all at once; {douryou} beside him says something short, {EX:douryou}, and {honnin} answers in his own way, {EX:honnin}, without taking his eyes off the board",
  True, None, "HAI nguoi phan ung KHAC nhau trong mot khung (§6.7 gate)"),
 ("c017", "keijiban", "mcu", "ots", "eye_st", "crowd_front", "in_board", "daylight", [],
  "he rubs the side of his thumb against his fingertips and looks down at them, wipes his hand on the side of his trousers and looks back up, the sheet beyond him always at a steep angle",
  False, None, "muc roneo dinh tay — ngu quan"),
 ("c018", "keijiban", "ms", "eye", "eye_st", "crowd_back", "out_board", "daylight", [],
  "the men in front of the board stand completely still without speaking; one of them turns and walks away down the corridor, then the others break apart and follow in ones and twos",
  True, None, "nam nao thap thi im lang"),
 ("c019", "office", "ms", "eye", "eye_st", "desk_side", "track_desks", "daylight",
  [("kachou", "trace")],
  "{kachou} stands at the window with one slat of the blind held aside on his finger, lets it fall back and turns towards the room, {EX:kachou}, while the men at the desks behind him go on working",
  True, None, "「では、なぜ」— chuyen sang co che"),
 ("c020", "michi", "ms", "behind", "eye_st", "lane", "in_lane", "daylight", [],
  "a long line of men in work jackets comes up the lane towards the main road in the morning; more join from the side gates as it passes, and the line keeps coming without a gap",
  True, None, "thieu nguoi — ai cung dang tuyen"),
 ("c021", "office", "ms", "eye", "table", "desk_across", "track_desks", "daylight", [],
  "two men stand close together at the end of the row with their heads bent towards each other; one glances at the corridor door, then they move apart and go back to their own desks",
  True, None, "春闘 dinh hinh"),
 ("c022", "keijiban", "mcu", "eye", "eye_st", "crowd_front", "in_board", "daylight", [],
  "a hand smooths the pinned sheet flat against the cork, then holds one corner down while the draught pulls at it; the sheet is seen edge on and nothing on it can be made out",
  False, None, "so lieu 1 — de Remotion ve"),
 ("c023", "keijiban", "ms", "behind", "eye_st", "crowd_back", "in_board", "daylight", [],
  "the crowd in front of the board grows until it fills the corridor; those at the back cannot see and lean out sideways one after another to find a gap",
  True, None, "so lieu 2"),
 ("c024", "keijiban", "mcu", "eye", "eye_st", "crowd_front", "in_board", "daylight",
  [("honnin", "full")],
  "{honnin} reads it twice, his mouth opening a little on the second time; he turns to look back along the corridor as if for someone to tell, {EX:honnin}, then faces the board again",
  True, None, "⭐ 1974 32,9% — dinh so lieu cua M1"),
 ("c025", "office", "ms", "eye", "table", "desk_side", "in_desk", "daylight", [],
  "men at the desks put their heads up one after another along the row, and one of them says something that makes the next three look round; then they all go back down to their work",
  True, None, "ky luc chua bi pha"),
 ("c026", "shataku_niwa", "ms", "eye", "eye_st", "yard", "in_yard", "evening",
  [],
  "{tsuma} crosses the yard with a shopping basket, stops at the foot of the stairs to shift it to the other hand, then goes on up out of the frame",
  True, None, "vat gia len — doi song"),
 ("c027", "daidokoro", "mcu", "eye", "table", "kitchen_door", "in_kitchen", None,
  [("tsuma", "held")],
  "{tsuma} lifts the lid of the rice bin and scoops one measure out, levels it off with her finger and tips it into the pot, then puts the lid back and rests her hand on it, {EX:tsuma}",
  False, None, "ha canh M1 bat dau — cai gia cua mot nam"),
 ("c028", "office", "ms", "eye", "table", "desk_across", "track_desks_back", "daylight", [],
  "the office floor in a later year, half the desks empty and the paper trays stacked higher; one man works alone at the near end of the row with his jacket still on",
  True, None, "平成7年 duoi 3% — khong khi doi"),
 ("c029", "keijiban", "ms", "eye", "eye_st", "corridor", "in_board", "daylight", [],
  "a single small sheet is pinned in the middle of the wide empty board; two men glance at it as they pass along the corridor and neither of them stops",
  True, None, "平成15年 1,63% — khong ai dung lai nua"),
 ("c030", "rouka", "ms", "behind", "eye_st", "corridor", "track_desks_back", "daylight", [],
  "men walk away from the board down the corridor in a loose group with their heads down; one stops and looks back at it, then goes on after the others",
  True, None, "so hom nay con xa"),
 ("c031", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None,
  [("honnin", "held"), ("tsuma", "full")],
  "{honnin} sits back from the low table with a teacup in both hands while {tsuma} kneels opposite and pours; he says something short, she stops pouring and looks up, {EX:tsuma}, and he answers in his own way, {EX:honnin}",
  False, "the two of them are at the low table with the teapot between them",
  "ha canh M1 — ve nha"),
 ("c032", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "neither of them speaks; the steam off the cup tilts sideways under the hanging light and she sets the teapot down without a sound",
  False, None, "「疑わなくてよかった」"),

# ---------------------------------------------------------------- M2 (33-50) : 家族手当
 ("c033", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("honnin", "held")],
  "{honnin} lays a folded paper on the general affairs counter and pushes it across with two fingers; the clerk on the other side turns it round and stamps it once, and {honnin} bows slightly, {EX:honnin}; the paper is always seen at a steep angle",
  True, "the stamped paper lies on the counter between them",
  "M2 mo — nop ban sao dang ky ket hon"),
 ("c034", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "the clerk closes the ledger over the paper and slides it to one side of the counter; a vermilion stamp-pad case sits open beside his hand and he caps it without looking",
  False, None, "thang sau, bang luong them mot dong"),
 ("c035", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None,
  [("tsuma", "trace")],
  "{honnin} holds a thick envelope out low across the table and {tsuma} takes it in both hands; she weighs it on her palm without opening it, {EX:tsuma}, then sets it down and pushes it a little back towards him",
  False, "the envelope lies on the table between them",
  "phong bi day hon mot chut"),
 ("c036", "daidokoro", "mcu", "eye", "table", "kitchen_door", "in_kitchen", None,
  [("tsuma", "held")],
  "{tsuma} takes the lid off a small tin at the end of the worktop and puts something into it without looking down, presses the lid back with the heel of her hand and pushes the tin in behind the rice bin, {EX:tsuma}",
  False, None, "⭐ cai lon canh hu gao — hien vat cua M2"),
 ("c037", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "a folded quilt airs over the paper screen and a small pair of shoes stands by the tatami edge; the room is otherwise empty and the light moves slowly across the floor",
  False, None, "canh tho — con ra doi, khong can noi"),
 ("c038", "office", "ms", "eye", "table", "desk_side", "track_desks", "daylight", [],
  "the office floor with every desk occupied; the men work without looking up and the paper trays are stacked level along the whole row",
  True, None, "co che — bat dau giai thich"),
 ("c039", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "full")],
  "{kachou} runs his finger down a column in the long ledger and stops, taps the counter twice with the side of his thumb and says something to the clerk, {EX:kachou}; the page is never square to the camera",
  True, None, "電産型 — luong tinh theo tuoi va so mieng an"),
 ("c040", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "his hand closes the ledger and rests flat on the cover; the stamp-pad case is capped beside it and the safe stands dark behind his shoulder",
  False, None, "十二月協定 1946"),
 ("c041", "office", "mcu", "eye", "table", "desk_across", "in_desk", "daylight",
  [("honnin", "trace")],
  "{honnin} works the calculator handle in a steady rhythm, stops, winds it back and starts again; he lets his breath all the way out and his shoulders drop an inch, {EX:honnin}, and keeps his eyes on the same spot",
  False, None, "44,3% tuoi + 18,9% gia dinh"),
 ("c042", "office", "ms", "eye", "table", "desk_side", "track_desks_back", "daylight", [],
  "the row of desks seen along its length, every man at the same posture and the same distance apart, the light from the blinds falling in bars across all of them",
  True, None, "24,4% nang luc — phan nho nhat"),
 ("c043", "chanoma", "ms", "eye", "seated", "table4th", "in_table", None, [],
  "three sets of chopsticks are laid out round the low table and a small cushion is set at one side; a hand comes in and straightens the smallest pair, then withdraws",
  False, None, "生活給 — luong nuoi ca nha"),
 ("c044", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None, [],
  "a present-day hand slides a thin folder across the same counter in a plain modern office; the counter is bare except for a single pen and the safe is gone from the wall behind",
  False, None, "so lieu nay 1"),
 ("c045", "office", "ms", "eye", "table", "desk_side", "track_desks", "daylight", [],
  "the office floor with several desks cleared and their chairs pushed in; the remaining men sit further apart and nobody speaks across the gap",
  True, None, "so lieu nay 2 — 69,1% -> 55,1%"),
 ("c046", "daidokoro", "mcu", "eye", "table", "kitchen_door", "in_kitchen", None,
  [("tsuma", "trace")],
  "{tsuma} opens the small tin again, looks into it for a moment longer than before and presses the lid back, {EX:tsuma}, then leaves her hand resting on it",
  False, None, "103万円の壁"),
 ("c047", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "the ledger is lifted off the counter and carried away out of frame; the counter is left bare with only the stamp-pad case on it, still open",
  False, None, "令和4年6月 閣議決定"),
 ("c048", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None, [],
  "{honnin} and {tsuma} sit on either side of the low table with the envelope between them; he pushes it across, she pushes it half back without a word, and he lets it stay where it is",
  False, None, "「家族が増えると、給料が増える」"),
 ("c049", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "the envelope lies alone on the table under the hanging light; the pull cord swings very slightly and the steam from the cup beside it leans the same way",
  False, None, "ha canh M2 — mot cai hieu tu cong ty"),
 ("c050", "genkan", "ms", "eye", "eye_st", "genkan_in", "in_lane", "evening",
  [("tsuma", "trace")],
  "{tsuma} slides the frosted door open as he steps up out of the sunken floor; she takes the jacket from him and both of them go back into the house, {EX:tsuma}, the door left half open behind them",
  False, None, "chuyen sang M3 — cai nha"),
]

# ---------------------------------------------------------------- M3 (51-68) : 社宅・寮
SHOTS += [
 ("c051", "ryou", "ms", "eye", "eye_st", "ryou_door", "track_walk", None,
  [("douryou", "held")],
  "{douryou} walks down the dormitory corridor at night with a towel over one shoulder and a red washbasin under his arm; he stops at a door, shifts the basin to the other hand and slides the door open, {EX:douryou}",
  True, "he is standing in the open doorway of his room",
  "M3 mo — chia khoa ky tuc, nguoi moi vao lam"),
 ("c052", "ryoushitsu", "ms", "eye", "seated", "ryou_door", "creep_still", None, [],
  "a three-mat room with a folded futon in the corner and a small desk under the window; a gooseneck lamp is the only light and the window shows the wall of the next block a few feet away",
  False, None, "3 chieu — ca can phong"),
 ("c053", "ryou", "ms", "behind", "eye_st", "ryou_door", "track_walk", None, [],
  "steam drifts along the dormitory corridor from the far end where the bath is; two men pass each other with basins under their arms and neither of them says anything",
  True, None, "nha tam chung — mui xa phong, hoi nuoc"),
 ("c054", "shataku_niwa", "ms", "eye", "eye_st", "yard", "in_yard", "evening",
  [("honnin", "held"), ("tsuma", "full")],
  "{honnin} carries a wooden crate across the yard while {tsuma} walks beside him with a bundle; at the foot of the stairs she looks up at the walkways above them, {EX:tsuma}, and he sets the crate down to change hands, {EX:honnin}",
  True, "the two of them are standing at the foot of the stairs with the crate between them",
  "⭐ cuoi xong chuyen vao 社宅 — buoc ngoat cua nhan vat"),
 ("c055", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening", [],
  "identical steel doors go past one after another along the open walkway, each with the same small frosted window and the same pair of shoes outside it, the railing running the whole length below",
  True, None, "day cua giong het nhau"),
 ("c056", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening",
  [],
  "{tsuma} lifts a quilt up onto the bamboo drying pole, squares it so it hangs evenly on both sides, and beats it twice with the flat of her hand; a neighbour further along does the same a moment later, and {tsuma} glances that way without stopping",
  True, None, "phoi do — ai cung lam mot viec"),
 ("c057", "shataku_niwa", "ms", "high_sl", "eye_st", "yard", "in_yard", "evening", [],
  "children run round the steel climbing frame in the concrete yard while bicycles stand in a row against the wall; a woman comes out onto a walkway above and calls down, and two of them stop",
  True, None, "tre con trong khu — ai cung biet ai"),
 ("c058", "shataku", "mcu", "eye", "eye_st", "walkway", "track_walk", None, [],
  "a thin wall seen from the walkway with the frosted window lit from inside; the shadow of someone moving crosses it once, and the sound of it carries along the concrete",
  False, None, "tuong mong — nghe duoc dong ho nha ben"),
 ("c059", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening", [],
  "steam rises from a kitchen window and drifts along the walkway past three doors; at the far end another window is open and the same steam comes out of it",
  True, None, "mui mon ham tu moi cau thang"),
 ("c060", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "held")],
  "{kachou} opens a thin folder on the counter, runs his finger along one line and taps it twice, {EX:kachou}; he turns the folder so it faces the other way and pushes it across, always at a steep angle",
  True, None, "「では、なぜ、そんなに安く貸せたのか」"),
 ("c061", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "a hand lays a rubber stamp down beside the folder and turns it upright; the vermilion pad sits open beside it and the safe stands dark behind the shoulder in the near corner",
  False, None, "国税庁 No.2597 — quy dinh thue"),
 ("c062", "shataku_niwa", "ms", "eye", "eye_st", "yard", "in_yard", "evening", [],
  "the whole four storey block seen from the gate, a drying pole of washing on every balcony and lights coming on in the windows one floor at a time as the sky goes over",
  True, None, "hop phap va re — ca khu"),
 ("c063", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening", [],
  "a row of identical doors again, but three of them now have no shoes outside and one has an empty drying pole with nothing pegged to it",
  True, None, "so lieu 1 — 5,0%"),
 ("c064", "shataku_niwa", "ms", "high_sl", "eye_st", "yard", "in_yard", None, [],
  "the same yard with the climbing frame gone and two cars parked where the bicycles stood; only one balcony still has a drying pole with washing on it",
  True, None, "so lieu 2 — 2,3%, hai muoi can con mot"),
 ("c065", "shataku", "mcu", "eye", "eye_st", "walkway", "track_walk", None, [],
  "one door with the paint gone matt and a single pot plant beside it; the frosted window is dark and the railing in front of it holds nothing",
  False, None, "家賃 37.993円 — van re"),
 ("c066", "shataku", "ms", "eye", "eye_st", "walkway", "track_walk", "evening",
  [("honnin", "trace")],
  "{honnin} comes out of a door with his jacket over one arm and stops at the railing to look down at the yard; he lets his breath out and his shoulders drop an inch, {EX:honnin}, then goes on towards the stairs",
  True, None, "ha canh M3 — song trong dat cua cong ty"),
 ("c067", "shataku_niwa", "ms", "behind", "eye_st", "yard", "in_yard", "evening", [],
  "he crosses the yard away from the camera towards the gate; a neighbour comes the other way and they pass each other with a small nod that neither of them breaks stride for",
  True, None, "khong thoai mai, nhung khong lo tien nha"),
 ("c068", "rouka", "ms", "eye", "eye_st", "corridor", "track_desks_back", "daylight", [],
  "the office corridor in the late afternoon with the light coming level down its whole length; nobody is in it and the frosted doors are all closed",
  False, None, "dan vao CTA — canh tho"),

# ---------------------------------------------------------------- CTA (69)
 ("c069", "rouka", "ms", "eye", "eye_st", "corridor", "creep_still", "daylight", [],
  "dust turns slowly in the shaft of light at the far end of the empty corridor; a door further down stands very slightly open and does not move",
  False, None, "CTA giua video — canh trung tinh, khong nhan vat"),

# ---------------------------------------------------------------- M4 (70-86) : 社内預金
 ("c070", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "full")],
  "{kachou} turns the heavy dial of the safe with one hand while holding a closed ledger under his other arm; he stops and listens with his head tilted, turns it back the other way, then pulls the handle down and the door gives, {EX:kachou}",
  False, "the safe door is open with the ledger still under his arm",
  "M4 mo — ket sat tong vu"),
 ("c071", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "he slides the long ledger into the open safe and squares it against the ones already there; the shelf inside is full of identical spines and he closes the door on all of them",
  False, None, "so ghi ten tung nguoi"),
 ("c072", "soumu", "ms", "eye", "eye_st", "counter_next", "in_safe", None, [],
  "the counter with nothing on it but the stamp-pad case; behind it the safe stands closed and the pendant lamp above turns very slightly on its flex",
  False, None, "khong ai co so rieng"),
 ("c073", "office", "ms", "eye", "table", "desk_side", "track_desks", "daylight", [],
  "a small slip is put down on each desk along the row in turn, the same way on every one; the men glance at them and go back to work without picking them up",
  True, None, "moi nam mot to giay"),
 ("c074", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None,
  [],
  "{honnin} slides open the drawer of the tea cabinet, puts a folded slip inside and closes it again with two fingers; he sits back on his heels and looks at the closed drawer",
  False, None, "cat trong ngan keo — hien vat M4"),
 ("c075", "office", "ms", "eye", "table", "desk_across", "in_desk", "daylight",
  [("kachou", "held")],
  "{kachou} walks the length of the row with his hands behind his back, stops at the far end and looks out over the whole floor, {EX:kachou}, while every man below him goes on working",
  True, None, "co che — cong ty can von"),
 ("c076", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "a hand lifts a bound bundle out of the safe, sets it on the counter and unties the red cord round it; the cord is laid aside still curled and nothing inside the bundle is ever shown",
  False, None, "lai cao hon ngan hang"),
 ("c077", "soumu", "ms", "eye", "eye_st", "counter_next", "in_safe", None, [],
  "the safe door stands half open with the shelves inside in shadow; the pendant lamp swings a little and the light moves across the closed dial",
  False, None, "diem yeu — cong ty pha san la mat"),
 ("c078", "rouka", "ms", "behind", "eye_st", "corridor", "track_desks_back", "daylight", [],
  "two men in suits walk down the corridor carrying a flat box between them and go out through the door at the far end without stopping",
  True, None, "財形法 昭和46年"),
 ("c079", "soumu", "mcu", "ots", "eye_st", "counter_next", "in_safe", None, [],
  "a new folder is set down on the counter and squared against its edge; a hand smooths the cover flat once and leaves it there, the cover kept at a steep angle throughout",
  False, None, "法律第九十二号"),
 ("c080", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "trace")],
  "{kachou} closes the safe and turns the dial twice with the flat of his hand, then rests his palm on the door for a moment, {EX:kachou}, before he steps away",
  False, None, "賃確法 昭和51年 — bao toan"),
 ("c081", "soumu", "ms", "eye", "eye_st", "counter_next", "arc_shoulder", None, [],
  "the closed safe fills most of the frame with the counter bare in front of it; the filing cabinets stand in line beside it and nothing in the corner moves but the lamp",
  False, None, "法律第三十四号"),
 ("c082", "keijiban", "ms", "eye", "eye_st", "corridor", "in_board", "daylight", [],
  "a single small sheet is pinned low on the corner of the notice board; a man passing slows, looks at it, and goes on down the corridor",
  True, None, "lai suat ha — dan len bang truoc"),
 ("c083", "office", "mcu", "eye", "table", "desk_across", "in_desk", "daylight",
  [("honnin", "trace")],
  "{honnin} looks at a slip on his desk without picking it up, turns it a quarter round with one finger and leaves it face down, {EX:honnin}, then goes back to the calculator",
  False, None, "roi moi den con so tren bang luong"),
 ("c084", "soumu", "ms", "eye", "eye_st", "counter_next", "in_safe", None, [],
  "the general affairs corner in a later year: the safe gone and a plain low cabinet in its place, the wooden counter replaced by a bare desk with one telephone on it",
  False, None, "che do gan nhu bien mat"),
 ("c085", "chanoma", "mcu", "eye", "seated", "table4th", "creep_still", None, [],
  "the tea cabinet drawer stands open with nothing in it but one old folded slip; the room is dark except for the light from the doorway falling across the tatami",
  False, None, "ha canh M4 — cam giac gui tien cho cong ty"),
 ("c086", "soubetsu", "ms", "eye", "eye_st", "row_line", "in_rows", "daylight", [],
  "the desks at one end of the office floor are pushed back against the wall and the blinds are half down; colleagues begin to come out and stand along both walls without being told where",
  True, "two loose rows of colleagues are standing along the walls of the cleared corridor",
  "M5 mo — chuan bi le ve huu"),

# ---------------------------------------------------------------- M5 (87-102) : 退職金
 ("c087", "soubetsu", "mcu", "eye", "eye_st", "row_line", "in_rows", None,
  [("honnin_tei", "full")],
  "{honnin_tei} walks between the two rows as a large bouquet of red carnations and yellow chrysanthemums is put into his hands; he takes it against his chest, his chin tightens and he keeps his eyes wide and dry on purpose, then bows his head over the flowers, {EX:honnin_tei}",
  True, "he is standing between the rows holding the bouquet against his chest",
  "⭐ DINH CAM XUC CA BAI — cung nguoi cua c002, 60 tuoi"),
 ("c088", "soubetsu", "ms", "eye", "eye_st", "row_line", "in_rows", None, [],
  "the two rows of colleagues clap without hurrying; one of them steps out to take a photograph, and everyone turns a little towards him at the same time",
  True, None, "chup anh"),
 ("c089", "office", "mcu", "eye", "table", "desk_across", "in_desk", "daylight",
  [("honnin_tei", "held")],
  "{honnin_tei} empties his desk drawer into a cardboard box; his hand stops on three old rubber stamps at the back of it, he turns one of them upright, {EX:honnin_tei}, then puts all three in together",
  False, None, "ba con dau — 37 nam"),
 ("c090", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None,
  [("honnin_tei", "trace"), ("tsuma", "held")],
  "{honnin_tei} and {tsuma} sit on either side of the low table looking down at a bankbook lying open between them; neither of them speaks, she lets her breath out first, {EX:tsuma}, and he only nods once to himself, {EX:honnin_tei}",
  False, "the bankbook lies open on the table between the two of them",
  "ve nha, hai vo chong nhin con so"),
 ("c091", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "the bankbook stays open on the table under the hanging light; the pull cord swings very slightly and neither pair of hands comes back into the frame",
  False, None, "「では、なぜ、会社は最後にまとめて払ったのか」"),
 ("c092", "office", "ms", "eye", "table", "desk_side", "track_desks", "daylight", [],
  "the office floor with every desk filled and the men all at the same posture; one empty chair stands pushed in at the end of the row and nobody has taken it",
  True, None, "giu nguoi — de khong ai bo di giua chung"),
 ("c093", "soumu", "ms", "ots", "eye_st", "counter_next", "in_safe", None,
  [("kachou", "held")],
  "{kachou} sets a thin folder on the counter and slides it across with two fingers, then taps the counter once beside it, {EX:kachou}; the folder is kept at a steep angle throughout",
  True, None, "中退共法 昭和34年 — cong ty nho cung co"),
 ("c094", "soumu", "mcu", "ots", "eye_st", "counter_next", "arc_shoulder", None, [],
  "a hand stamps the folder once, lifts the stamp straight up and sets it back on the vermilion pad; the red cord bundle on the shelf behind stays exactly where it was",
  False, None, "法律第百六十号"),
 ("c095", "soubetsu", "ms", "eye", "eye_st", "row_line", "in_rows", None, [],
  "the cleared corridor after everyone has gone: the desks still pushed back, one chair left out in the middle of the floor and the blinds still half down",
  True, None, "khoan tien nay la mot loi hua"),
 ("c096", "rouka", "mcu", "eye", "eye_st", "corridor", "creep_still", "daylight", [],
  "the empty corridor with the light level along it and one door standing very slightly open at the far end",
  False, None, "「では、いまは」— o ngan nhat bai"),
 ("c097", "office", "ms", "eye", "table", "desk_side", "track_desks_back", "daylight", [],
  "a present-day office floor in the same building: low partitions, plain chairs and two thirds of the desks empty, the windows the same but the blinds gone",
  True, None, "74,9% — bon cong ty mot khong con"),
 ("c098", "soumu", "ms", "eye", "eye_st", "counter_next", "in_safe", None, [],
  "the wall where the safe stood, now bare except for a pale rectangle on the paint and a single plain cabinet pushed against it",
  False, None, "80,5% -> 74,9%"),
 ("c099", "chanoma", "mcu", "eye", "seated", "table4th", "in_table", None, [],
  "the bankbook is closed on the table and pushed to one side; a teacup is set down beside it and the hand that put it there withdraws out of frame",
  False, None, "1.983万 -> 1.896万"),
 ("c100", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "the low table with only the closed bankbook and the cooling cup on it; steam still comes off the cup and leans in the draught from the screens",
  False, None, "giam 87万円"),
 ("c101", "genkan", "ms", "eye", "eye_st", "genkan_in", "in_lane", "evening",
  [("honnin_tei", "full")],
  "{honnin_tei} sets his shoes straight on the sunken floor with one hand and stands a moment looking at them; he lets his breath all the way out and his shoulders drop, {EX:honnin_tei}, then slides the frosted door closed",
  False, None, "ha canh M5 — moi thu duoc dung tren loi hua do"),
 ("c102", "ima_ie", "ms", "eye", "table", "sofa_side", "creep_still", "daylight", [],
  "the present-day room with the flat lidded box open on the table and the old sheet lying beside it; the curtain moves once at the window and settles",
  False, None, "chuyen sang KET — ve lai thoi nay"),

# ---------------------------------------------------------------- END (103-111)
 ("c103", "ima_ie", "mcu", "eye", "table", "sofa_side", "creep_still", "daylight",
  [("ima", "held")],
  "{ima} lays five things out on the table one after another and moves the last one a little straighter; he sits back and looks at the row of them, {EX:ima}, without touching any of them again",
  False, "the five things are laid out in a row on the table in front of him",
  "KET — nam thu bay ra"),
 ("c104", "ima_ie", "ms", "eye", "table", "sofa_side", "out_room", "daylight", [],
  "he pushes the row of things a little away from himself across the table, then folds his hands in his lap and goes on looking at them from further back",
  False, None, "「戻りたいとは思わない部分もあります」"),
 ("c105", "michi", "ms", "eye", "eye_st", "lane", "in_lane", "daylight", [],
  "a present-day street where the lane used to be: the fences replaced, the postbox gone and two people walking in opposite directions without passing anyone else",
  False, None, "tu do chon lai — nhung it nguoi hon"),
 ("c106", "chanoma", "ms", "eye", "seated", "table4th", "creep_still", None, [],
  "the old living room empty in the evening, the low table bare and the tea cabinet doors closed; the pull cord hangs still under the light",
  False, None, "bang luong co ten gia dinh, nha, so tiet kiem, tien ve huu"),
 ("c107", "shataku_niwa", "ms", "high_sl", "eye_st", "yard", "in_yard", "daylight", [],
  "the housing block yard in the present day with the block itself still standing, the balconies bare and the climbing frame replaced by a painted line of parking bays",
  True, None, "di lam la giao ca doi song cho cong ty"),
 ("c108", "ima_ie", "mcu", "eye", "table", "sofa_side", "creep_still", "daylight",
  [("ima", "full")],
  "{ima} picks the old sheet up by two corners and holds it a moment at the height of his chest; his eyes narrow and the cheeks push up without the mouth opening, {EX:ima}, and he lays it back down flat",
  False, None, "phan duoc giu ho, nay tra ve tay minh"),
 ("c109", "ima_ie", "ms", "eye", "table", "sofa_side", "out_room", "daylight", [],
  "he puts the lid back on the flat box and sets it square in the middle of the table, then leaves his hand resting on the lid",
  False, None, "「あなたの会社には、何がありましたか」"),
 ("c110", "keijiban", "ms", "eye", "eye_st", "corridor", "creep_still", "daylight", [],
  "the old notice board with nothing pinned on it at all, the cork marked all over with the holes of drawing pins and the light falling level across it",
  False, None, "⭐ dong vong — to giay cua c000, nay khong con"),
 ("c111", "ima_ie", "ms", "eye", "table", "sofa_side", "out_room", "daylight", [],
  "the present-day room seen from further back with him small at the table and the box in front of him, the window bright beyond and the curtain moving once",
  False, None, "dong bai"),
]

POV_SHOTS = {}


def pick_expr17():
    reg = {}
    if K.REG.exists():
        reg = json.loads(K.REG.read_text(encoding="utf-8"))
    taken = {v for vid, d in reg.items() if vid != VIDEO_ID for v in d.values()}
    mine, used_now = {}, set()
    for cast in sorted(ARCH, key=lambda c: (ARCH[c], c)):
        bank = K.EXPR_BANK[ARCH[cast]]
        free = [k for k in bank
                if k not in taken and k not in used_now and k not in BAN.get(cast, [])]
        if not free:
            raise SystemExit("KHO CAN cho nguyen mau %s — viet bien the moi" % ARCH[cast])
        mine[cast] = free[0]
        used_now.add(free[0])
    return mine, reg


PICK = {}
PREV = {}   # name -> (scene, out) cua canh TRUOC, de noi lien


def build(sh, prev):
    (name, scene, size, angle, height, stand, move, land, expr, action, extras, out, _why) = sh
    occ = PROP_ROT.get(scene, 0)
    PROP_ROT[scene] = occ + 1
    props = PROPS[scene][occ % len(PROPS[scene])]
    for cast, lv in expr:
        action = action.replace("{EX:%s}" % cast, K.EXPR_BANK[ARCH[cast]][PICK[cast]] + K.LEVEL[lv])
    for k, v in CA.items():
        action = action.replace("{%s}" % k, v)
    # 🔗 NOI LIEN: chi noi khi canh truoc CUNG BOI CANH va co trang thai ket
    lead = ""
    if prev and prev[0] == scene and prev[1]:
        lead = "Continuing straight on from the moment just before, %s. " % prev[1]
    stand_s = (f"The camera is placed exactly where {STAND[stand]} would be, at that person's own "
               f"eye level, and the whole shot is seen from that one place.")
    frame_block = ", ".join([K.SIZE[size], K.ANGLE[angle], K.HEIGHT[height], K.OPTICS])
    opener = f"{K.SIZE[size].split(',')[0]}, filmed in 1970s Japan."
    parts = [opener,
             "NO letters, NO words, NO numbers and NO logos anywhere in the picture, and no film "
             "strip, no sprocket holes and no frame line along its edges.",
             move_block(move),
             stand_s,
             K.AVOID + ".",
             lead + action + ".",
             frame_block + ".",
             SC[scene].rstrip(",") + ".",
             "Bright colour in the props: " + props + K.PROP_TAIL + "."]
    if land:
        parts.append(K.LAND[land] + ".")
    if extras:
        parts.append(K.EXTRA_LOCK + ".")
    parts += [K.STYLE + ".", K.CAM, K.MOTION,
              "Remember: the camera must move the whole way through as described; each person's "
              "reaction is their own and no two of them react the same way; the feeling must build "
              "and then settle, never held as a pose; no text and no film-strip edge anywhere; "
              "nobody looking at the camera."]
    return " ".join(" ".join(p.split()) for p in parts)


def main():
    global PICK
    PICK, reg = pick_expr17()
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((OUT / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
    slots = plan["slots"]
    red = 0

    # --- GATE 1: so canh PHAI khop so o cua SLIDES
    if len(SHOTS) != len(slots):
        print("[CHAN] %d canh nhung SLIDES co %d o" % (len(SHOTS), len(slots))); red += 1

    # --- GATE 2: hai cast trong CUNG khung khong duoc cung chu ky
    for sh in SHOTS:
        sig = [PICK[c] for c, _ in sh[8]]
        if len(set(sig)) != len(sig):
            print("[CHAN] %s: hai nguoi cung mot dieu cuoi" % sh[0]); red += 1

    # --- GATE 3: chu ky bi BAN
    for cast, sig in PICK.items():
        if sig in BAN.get(cast, []):
            print("[CHAN] %s bi rut chu ky %s nam trong BAN" % (cast, sig)); red += 1

    # --- GATE 4: tran lap chu ky ca video (§6.7 muc 4 — tran 3, tinh ca cuong do)
    cnt = Counter((c, lv) for sh in SHOTS for c, lv in sh[8])
    for (c, lv), n in cnt.items():
        if n > 3:
            print("[CHAN] chu ky %s/%s lap %d lan (tran 3)" % (c, lv, n)); red += 1

    flow, rows, prev = [], [], None
    for i, sh in enumerate(SHOTS):
        p = build(sh, prev)
        prev = (sh[1], sh[11])
        for b in K.BAD:
            if b in p:
                print("[CHAN] %s chua tu cam: %s" % (sh[0], b)); red += 1
        for f in K.FLAT:
            if f in p.lower():
                print("[CHAN] %s ta cam xuc bang TEN: %s" % (sh[0], f)); red += 1
        pos = p.find("NO letters")
        if pos * 100 // len(p) > 15:
            print("[CHAN] %s guard @ %d%%" % (sh[0], pos * 100 // len(p))); red += 1
        if p.count("CAMERA MOVE, one move only") != 1:
            print("[CHAN] %s khong phai dung 1 nuoc may" % sh[0]); red += 1
        # --- GATE 8: khong con placeholder chua thay (canh bo expr ma action con {EX:})
        if "{EX:" in p or "{honnin" in p or "{tsuma" in p or "{kachou" in p or "{ima" in p or "{douryou" in p:
            import re as _re
            print("[CHAN] %s con placeholder: %s" % (sh[0], _re.findall(r"\{[A-Za-z:_]+\}", p)[:4])); red += 1
        flow.append(p)
        s = slots[i] if i < len(slots) else {"dur": 0, "block": "?", "text": ""}
        rows.append((sh[0], s["block"], s["dur"], sh[6], sh[12], s["text"]))

    # --- GATE 5: o >8,0s phai GIAN clip (Flow chi ra 8s)
    need = [(r[0], r[2]) for r in rows if r[2] > 8.0]
    print("=== VIDEO 17 — %d canh ===" % len(SHOTS))
    print("chu ky da rut: %s" % PICK)
    print("o >8,0s can GIAN clip bang setpts: %d/%d (he so toi da %.2fx)"
          % (len(need), len(rows), max([r[2] for r in rows]) / 8.0))
    # --- GATE 6: moi boi canh phai xuat hien >=2 lan (canh le = mot cai anh lac)
    sc_cnt = Counter(sh[1] for sh in SHOTS)
    for k, n in sc_cnt.items():
        if n < 2: print("[warn] boi canh %s chi dung %d lan" % (k, n))
    # --- GATE 7: chuoi noi lien — dem so cap noi duoc
    link = sum(1 for i in range(1, len(SHOTS)) if SHOTS[i-1][1] == SHOTS[i][1] and SHOTS[i-1][11])
    print("noi lien: %d/%d cap canh lien nhau cung boi canh co trang thai ket" % (link, len(SHOTS) - 1))
    print("boi canh dung: %s" % dict(sc_cnt))

    # --- GATE 9: vat ruc khong duoc lap qua 8/112 prompt (ca goc: stamp-pad 53/112)
    import re as _re
    frag = Counter()
    for p in flow:
        seg = p.split("Bright colour in the props: ")[1].split(" with no writing")[0]
        for piece in _re.split(r" and |, ", seg):
            piece = piece.strip()
            if len(piece) > 12: frag[piece] += 1
    hot = [(k, n) for k, n in frag.items() if n > 8]
    for k, n in sorted(hot, key=lambda x: -x[1])[:6]:
        print("[CHAN] vat ruc lap %d/%d lan: %s" % (n, len(flow), k[:60])); red += 1
    if not hot:
        print("vat ruc: %d cum khac nhau, cum day nhat %d/%d lan"
              % (len(frag), max(frag.values()), len(flow)))

    if red:
        print("\n[CHAN] %d loi — KHONG xuat file." % red)
        sys.exit(1)

    io.open(OUT / FLOW, "w", encoding="utf-8", newline="\n").write("\n".join(flow) + "\n")
    io.open(OUT / TENF, "w", encoding="utf-8", newline="\n").write(
        "# video 17 — thu tu dong trong %s <-> ten file clip\n"
        "# clip_NN.mp4 la ten renderer DOC (theo so thu tu o), ten mo ta chi de tra\n\n" % FLOW
        + "\n".join("%3d  clip_%02d.mp4  %-6s %5.2fs  %-14s %s"
                    % (i, i, r[1], r[2], r[3], r[4]) for i, r in enumerate(rows))
        + "\n\n# chu ky bieu cam (so EXPR_REGISTRY.json): %s\n" % PICK)
    io.open(OUT / BLOCKS_MD, "w", encoding="utf-8", newline="\n").write(
        "# Video 17 — 112 canh, ban nguoi doc\n\n"
        "> Mot cau chuyen: mot nguoi, mot cong ty, 37 nam. 1968 vao lam -> 1975 dinh cao tang\n"
        "> luong -> cuoi, con ra doi -> ky tuc -> 社宅 -> gui tiet kiem o ket cong ty -> 2005\n"
        "> ve huu -> NAY. honnin / honnin_tei / ima la CUNG MOT NGUOI o ba tuoi.\n\n"
        "| # | khoi | dai | boi canh | nuoc may | y do | loi dang doc |\n|---|---|---:|---|---|---|---|\n"
        + "\n".join("| %d | %s | %.2fs | %s | %s | %s | %s |"
                    % (i, r[1], r[2], SHOTS[i][1], r[3], r[4], r[5]) for i, r in enumerate(rows))
        + "\n")
    reg[VIDEO_ID] = PICK
    K.REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n-> %s\n-> %s\n-> %s" % (OUT / FLOW, OUT / TENF, OUT / BLOCKS_MD))


if __name__ == "__main__":
    main()
