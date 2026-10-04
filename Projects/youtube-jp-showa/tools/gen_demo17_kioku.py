# -*- coding: utf-8 -*-
"""DEMO video 17 — 昭和の会社がくれたもの5選. 9 canh dai dien, khuon `camera-language.md` (2026-09-21).

⛔ KHONG chep hang so: STYLE / AVOID / MOTION / CAM / SIZE / ANGLE / HEIGHT / LAND / OPTICS /
   EXPR_BANK / LEVEL / EXTRA_LOCK / PROP_TAIL deu IMPORT tu `gen_demo16_kioku` (ban thi hanh
   cua rule — camera-language.md §10). File nay chi khai phan BIEN THIEN cua video 17:
   SC (boi canh) · CA (dan dien) · PROPS (vat mau ruc) · MOVES (nuoc may) · SHOTS.

VI SAO CHI 9 CANH: user chot 2026-09-21 — demo truoc, dat roi moi nhan len 163 o cua SLIDES.
   Cung duong video 16 da di (gen_demo16_kioku = 8 clip demo), va dung luat "render demo truoc".

⭐ 9 canh phu HET cac loai shot se dung o ban day, de demo tra loi duoc cau "khuon nay co
   chay khong" chu khong chi "mot canh nay co dep khong":
   2 canh dam dong (keijiban) · 2 canh van phong · 1 POV · 1 nha · 1 khu tap the · 1 le ve huu
   · 1 canh THOI NAY (ima_ie).

🔴 BON BAY CUA RIENG BAI NAY — da dong vao prompt, dung go ra:
 a. ⛔ To giay tren bang thong bao / bang luong / so tiet kiem: **KHONG BAO GIO doc duoc chu**.
    Moi canh co giay deu quay goc nghieng hoac bi tay che. So lieu de Remotion ve
    (`feedback_so_tren_hinh_phai_do_font_ve`). Khoi NO-letters cua khuon da o dau prompt.
 b. ⛔ KHONG lich treo tuong, KHONG nhiet ke, KHONG bang bieu co truc (`ai-video-regen.md` §3:
    vat mang san mot thang so thi model dien so len bat ke cau cam).
 c. ⛔ Van phong Showa KHONG co man hinh may tinh. Chi may tinh co quay tay, dien thoai quay so.
 d. 🔴 KHONG dung nuoc may len/xuong truc dung: `camera-language.md` §7.5 do duoc PEDESTAL /
    CRANE DOWN = **0,995-1,009 scale, khong di, 3/3 ca**. Can ha may thi viet DOLLY IN
    "forward and dropping as it goes" — da lam vay o `dolly_safe`.
"""
import io
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import gen_demo16_kioku as K   # ban thi hanh cua rule — nguon cua moi hang so bat bien

OUT  = Path(__file__).resolve().parents[1] / "06_VIDEO" / "17_kaisha-ga-kureta"
VER  = "v1"
VIDEO_ID = "17"
FLOW = f"videogen_DEMO17_{VER}_FLOW.txt"
TENF = f"videogen_DEMO17_{VER}_TENFILE.txt"

# =====================================================================================
# MOVES — §4.1 LUAT HAI MOC: nuoc may phai la DUONG DI (moc dau -> duong di -> moc ket),
#         khong phai cai NHAN. Viet kieu nhan thi model chon cach re nhat: gan nhu khong di.
# =====================================================================================
MOVES = {
 "dolly_board": dict(
   name="DOLLY IN, straight forward through the crowd",
   phys="the whole camera rolls forward down the corridor on a track, so the shoulders and backs "
        "of the men really pass it on both sides; this is a physical move through space, not a "
        "zoom, not a crop and not a still frame",
   start="far back down the corridor, the crowd only a dark mass of shoulders with the lit notice "
         "board glowing beyond them",
   path="straight forward towards the board, the men on both sides sweeping out through the edges "
        "of the frame as it passes them, staying level at their own standing eye height",
   amount="it closes about two thirds of the distance to the board",
   end="close behind the two men at the front, the back of one head filling the near corner and "
       "the pinned sheet beyond them at a steep angle, never square to the camera"),

 "track_desks": dict(
   name="TRACKING, sideways, left to right along the desks",
   phys="the whole camera slides sideways across the office floor on a dolly, parallel to the row, "
        "so the desks really pass across the frame; this is a physical move, not a pan and not a "
        "still frame",
   start="on the near end of the row, a mechanical calculator and a black dial telephone large in "
         "the foreground",
   path="sideways along the row at tabletop height, each desk and each seated man sliding out "
        "through the left of the frame as the next one comes in from the right",
   amount="it travels the length of about four desks",
   end="on the two of them at the far end of the row, the nearer one turning his head as the "
       "camera settles"),

 "arc_counter": dict(
   name="ARC, the camera orbiting slowly round his shoulder",
   phys="the camera swings round him along a curve while holding the same distance, so the safe "
        "and the cabinets slide across behind him; this is a physical move round him, not a zoom",
   start="behind his shoulder, the back of his head filling the near corner and the counter soft "
         "and out of focus beyond it",
   path="round that shoulder from his left towards his front, keeping the shoulder in the near "
        "corner and holding its own height",
   amount="it travels about a quarter of the way round him",
   end="on his face clear and the heavy safe standing sharp behind him"),

 "dolly_safe": dict(
   name="DOLLY IN, forward and dropping as it goes",
   phys="the whole camera rolls forward on a track and sinks lower along the way, so the room "
        "really opens over the top of the counter; this is a physical move through space, not a "
        "zoom and not a crane shot on a post",
   start="standing height at the doorway of the general affairs corner, the counter a bar across "
         "the bottom of the frame",
   path="straight forward towards the safe, dropping steadily as it goes until it is level with "
        "the counter top, the ledger and the stamp pad passing out through the bottom of the frame",
   amount="it closes about half the distance and drops about the height of a standing man's chest",
   end="level with the counter, the dial of the safe filling the middle of the frame with his "
       "hands coming into it"),

 "track_walkway": dict(
   name="TRACKING, sideways along the open walkway",
   phys="the whole camera slides sideways along the outdoor walkway on a dolly, parallel to the "
        "doors, so the railing runs steadily through the bottom of the frame",
   start="at one end of the walkway, washing hanging close in the near foreground",
   path="sideways past one identical steel door after another, each with its small frosted window, "
        "the railing running through the bottom of the frame the whole way, the yard and the "
        "climbing frame below sliding past beyond it",
   amount="it travels past about five doors",
   end="on her at the far end, pegging a shirt over the railing with the block behind her"),

 "dolly_flowers": dict(
   name="DOLLY IN, straight forward down the two rows",
   phys="the whole camera rolls forward between the two rows of colleagues on a track, so they "
        "really pass it on both sides; this is a physical move through space, not a zoom",
   start="at the near end of the cleared corridor, the two rows of colleagues receding away and "
         "him small between them",
   path="straight forward between the rows, the nearest shoulders sweeping out through both edges "
        "of the frame, holding its own standing height",
   amount="it closes about three quarters of the distance to him",
   end="close on him from the chest up as the bouquet is put into his hands"),

 "dolly_out_room": dict(
   name="DOLLY OUT, straight back",
   phys="the whole camera rolls backwards through the room on a track, so the doorway and the "
        "furniture really pass it; this is a physical move, not a zoom out",
   start="close on his hands and the single old sheet lying flat on the table",
   path="straight back away from the table at the same height, the edge of the table and then the "
        "back of a chair passing out through the bottom of the frame",
   amount="it pulls back about the length of the room",
   end="the whole room in frame with him small at the table and the window bright beyond him"),

 "dolly_kitchen": dict(
   name="DOLLY IN, straight forward past the rice bin",
   phys="the whole camera rolls forward across the kitchen floor on a track, so the corner of the "
        "worktop really passes it; this is a physical move through space, not a zoom",
   start="in the kitchen doorway, the wooden rice bin large and dark in the near foreground",
   path="straight forward past the rice bin, the bin sweeping out through the left of the frame, "
        "staying level at the height of the worktop",
   amount="it closes about half the distance to her",
   end="close on her hands at the worktop and her face above them"),
}


def move_block(k):
    m = MOVES[k]
    return ("CAMERA MOVE, one move only, running for the whole eight seconds: " + m["name"] + ". "
            + m["phys"] + ". It starts " + m["start"] + ". It travels " + m["path"] + ". "
            + m["amount"] + ". It ends " + m["end"] + ". "
            "It never pauses, never holds still and never reverses.")


# =====================================================================================
# SC — BOI CANH cua video 17
# =====================================================================================
SC = {
 "keijiban": 'the end wall of a Showa office corridor where a large cork notice board hangs, a few '
             'loose sheets pinned to it, a worn linoleum floor and painted plaster walls, a tall '
             'metal window frame at the far end letting flat daylight down the corridor',
 "office":   'the open floor of a Showa company office in the daytime, grey steel desks pushed '
             'together face to face in long rows, a mechanical hand-cranked calculator and a black '
             'rotary dial telephone on the rows, stacked paper trays and a glass ashtray, tall metal '
             'cabinets along the wall and wide windows with venetian blinds, and no screens of any kind',
 "soumu":    'the general affairs corner of a Showa office, a tall grey steel safe with a heavy dial '
             'standing against the wall, a wooden counter in front of it, a long ledger and a stamp '
             'pad on the counter, filing cabinets and a single bare pendant lamp above',
 "shataku":  'the open outdoor walkway of a Showa company housing block in the late afternoon, '
             'concrete underfoot and a painted steel railing along the open side, identical steel '
             'doors in a row each with a small frosted window, washing hung out along the balconies '
             'and a concrete yard with a steel climbing frame below',
 "chanoma":  'the living room of a Showa house in the evening, a low round wooden dinner table in '
             'the middle of the tatami with flat floor cushions round it, a fluorescent ceiling '
             'light with a long pull cord, a wooden tea cabinet with sliding glass doors and sliding '
             'paper screens along one side',
 "daidokoro":'the kitchen of a Showa house at night, a tiled worktop and a deep concrete sink, a '
             'two-ring gas burner with a blackened kettle, open shelves of enamel bowls and tin '
             'canisters, a wooden rice bin standing in the corner and one bare bulb over the worktop',
 "soubetsu": 'a cleared corridor on a Showa office floor in the late afternoon, the desks pushed '
             'back at one end, colleagues standing in two loose rows along the walls, the venetian '
             'blinds half down at the windows behind them',
 "ima_ie":   'a present-day Japanese living room, a low sofa and a plain table, a wide window with '
             'a plain curtain and everyday daylight, nothing on the table but one flat lidded box',
}

# =====================================================================================
# CA — DAN DIEN. Moi cast = KHUON MAT (khong doi ca video) + DO MAC.
#  🔴 Khuon mat phai KHAC moi cast cua video 13/14/15/16 — kiem bang check_cast_unique.py 17
#  ⭐ honnin / honnin_tei / ima la CUNG MOT NGUOI o ba tuoi: cau khuon mat CHEP Y NGUYEN,
#     chi them toc bac + nep nhan. Dung sua le mot ban.
# =====================================================================================
CA = {
 "honnin":    'a man of about forty, wide square face, low flat forehead with a straight hairline, '
              'short thick eyebrows set far apart, single-lidded eyes slanting up very slightly at '
              'the outer corners, broad flat nose, a deep vertical crease between the brows, hair parted '
              'low on one side, in a plain white short-sleeved shirt with the collar open',
 "honnin_tei":'a man of about sixty, wide square face, low flat forehead with a straight hairline, '
              'short thick eyebrows set far apart, single-lidded eyes slanting up very slightly at '
              'the outer corners, broad flat nose, a deep vertical crease between the brows, hair now '
              'iron grey and thin at the temples with deep lines across the forehead, in a plain '
              'dark grey suit',
 "ima":       'a man of about seventy-eight, wide square face, low flat forehead with a straight '
              'hairline, short thick eyebrows set far apart, single-lidded eyes slanting up very '
              'slightly at the outer corners, broad flat nose, a deep vertical crease between the brows, '
              'hair now white and sparse, cheeks fallen in, brown age spots at the temples, in a '
              'plain beige cardigan',
 "tsuma":     'a woman of about thirty-five, long oval face, high rounded forehead, thin curved '
              'eyebrows set high, wide double-lidded eyes slightly sunken, low cheekbones, small '
              'round chin with a dimple in the right cheek, hair tied back low at the neck, in a '
              'plain blouse with a plain apron over it',
 "kachou":    'a man of about fifty-five, short blunt rectangular face, heavy square jaw, hairline '
              'receded deeply at both temples, thick grey eyebrows over heavy hooded eyelids, large '
              'nose with a pronounced bridge, a thin trimmed moustache, in a white shirt with a dark '
              'tie and sleeve garters',
}
ARCH = {"honnin": "m40", "honnin_tei": "m50", "ima": "m50", "kachou": "m50", "tsuma": "w40"}

# 🔴 BAN — chu ky doi mot DAO CU ma cast/canh khong co thi no choi voi hanh dong.
#   Bat duoc o luot demo dau: `honnin_tei` bi rut `m50_glasses` ("bo kinh xuong") trong khi
#   nhan vat khong deo kinh VA o canh d8 hai tay dang om bo hoa. Gate cu khong thay, vi no
#   chi kiem TRUNG chu ky, khong kiem chu ky co DUNG voi nguoi/canh khong.
#   ⇒ Khai thang dao cu tung cast KHONG co. Bang nay di theo CAST, khong theo canh: mot cast
#     giu mot chu ky suot ca video (§6.7), nen no phai hop voi MOI canh cua cast do.
BAN = {
 "honnin_tei": ["m50_glasses",              # khong deo kinh
                "m50_pen", "m50_chair"],    # canh le ve huu: dung, hai tay om hoa
 "ima":        ["m50_glasses", "m50_pen"],  # khong deo kinh; tren ban khong co but
 "kachou":     ["m50_glasses"],             # khong deo kinh
 "honnin":     [],
 "tsuma":      ["w40_apron"],               # chu ky nay trung dong tac voi viec dang lam (tap de)
}

# =====================================================================================
# PROPS — §5.1 mau ruc phai den tu VAT, 1-3 vat moi canh, va vat ruc KHONG mang chu/so.
# =====================================================================================
PROPS = {
 "keijiban": "a vermilion stamp-pad case left on the window ledge, a red-and-blue pencil tucked "
             "behind one man's ear and a red fire-bell box on the wall by the window",
 "office":   "a vermilion stamp-pad case open beside the ledger, a red-and-blue pencil lying across "
             "the papers and a bottle of blue ink catching the light on the next desk",
 "soumu":    "a vermilion stamp-pad case sitting open on the counter, a red pencil in the tray "
             "beside it and a bolt of red cord binding the older files on the shelf behind",
 "shataku":  "a scarlet plastic pail by one of the doors, a red child's tricycle in the yard below "
             "and a flower-patterned cloth wrapper folded over the railing",
 "chanoma":  "a flower-patterned vacuum flask standing on the tea cabinet, flower-patterned teacups "
             "on the tray and a folded scarlet cloth wrapper at the edge of the tatami",
 "daidokoro":"a red-lacquered pail under the worktop, a scarlet cloth hanging on its hook and a "
             "flower-patterned enamel bowl on the shelf",
 "soubetsu": "the bouquet itself bright with red carnations and yellow chrysanthemums, and a "
             "red-and-white ribbon tied round the paper",
 "ima_ie":   "a single red carnation in a small glass on the table and a folded scarlet cloth "
             "wrapper beside the box",
}

# =====================================================================================
# STAND — §1.1 MAY DUNG O CHO CUA AI. Thieu cau nay thi t2v chon cho khong ai dung duoc.
# =====================================================================================
STAND = {
 "crowd_back":  "one of the other men standing at the back of the same crowd",
 "desk_side":   "a colleague standing at the end of that same desk",
 "counter_next":"the next person waiting at that counter",
 "walkway":     "a neighbour standing further along the same walkway",
 "table4th":    "the fourth person sitting at that table",
 "kitchen_door":"someone standing in the kitchen doorway",
 "row_line":    "one of the colleagues standing in the row beside him",
 "sofa_side":   "someone sitting on the sofa across from him",
}

# =====================================================================================
# SHOTS — (file, scene, size, angle, height, stand, move, land, expr, action, extras, why)
# =====================================================================================
SHOTS = [
 ("d1_board_crowd", "keijiban", "ms", "behind", "eye_st", "crowd_back", "dolly_board", "daylight",
  [],
  "the men crowd in towards the notice board with their backs to the camera; those at the front "
  "lean in until their heads almost touch the sheet, then the ones behind rise onto their toes to "
  "see over the shoulders in front of them, then the whole group presses one pace closer; the "
  "pinned sheet is always seen at a steep angle and nothing written on it can be made out",
  True, "canh mo bai — dam dong, KHONG doc duoc chu tren giay"),

 ("d2_board_face", "keijiban", "mcu", "eye", "eye_st", "crowd_back", "dolly_board", "daylight",
  [("honnin", "full")],
  "{honnin} stands at the front of the crowd with his face close to the board; his eyebrows go up "
  "before the rest of him catches on and his hand stops half way to the paper, then he turns his "
  "head to the man beside him, {EX:honnin}, and then he looks back at the board and is still; the "
  "sheet stays at a steep angle and nothing on it can be read",
  True, "dinh cam xuc cold open — vong cung 3 nhip, chu ky cuoi rieng"),

 ("d3_office_row", "office", "mcu", "eye", "table", "desk_side", "track_desks", "daylight",
  [("honnin", "held"), ("kachou", "full")],
  "{honnin} works the handle of the hand-cranked calculator with one hand while steadying it with "
  "the other; {kachou} comes along the row and stops at the end of the desk and says something "
  "short, then {honnin} stops cranking and looks up at him, {EX:honnin}, and {kachou} answers in "
  "his own way, {EX:kachou}, while the blind slats sway a little in the draught behind them",
  True, "van phong — HAI nguoi phan ung KHAC nhau trong cung khung (§6.7 gate)"),

 ("d4_soumu_safe", "soumu", "ms", "ots", "eye_st", "counter_next", "dolly_safe", None,
  [("kachou", "full")],
  "{kachou} turns the heavy dial of the safe with one hand while holding the long ledger closed "
  "under his other arm; he stops and listens with his head tilted, then he turns the dial back the "
  "other way, then he pulls the handle down and the door gives; the ledger stays shut and no page "
  "of it is ever seen",
  False, "may HA XUONG bang DOLLY IN dropping (§7.5: truc dung t2v khong lam duoc)"),

 ("d5_shataku", "shataku", "ms", "eye", "eye_st", "walkway", "track_walkway", "evening",
  [("tsuma", "full")],
  "{tsuma} lifts a wet shirt out of the pail and shakes it out once, then she hangs it over the "
  "railing and pegs it down, then she straightens up and looks along the row of doors, {EX:tsuma}, "
  "while the washing already hung out along the balconies moves in the wind",
  True, "khu tap the — canh doi thuong, co phong canh nen dung LAND"),

 ("d6_kitchen_tin", "daidokoro", "mcu", "eye", "table", "kitchen_door", "dolly_kitchen", None,
  [("tsuma", "held")],
  "{tsuma} takes the lid off a small tin at the end of the worktop and puts something into it "
  "without looking down, then she presses the lid back on with the heel of her hand, then she "
  "pushes the tin in behind the rice bin, {EX:tsuma}, and goes straight back to the pot on the burner",
  False, "M2 — cai lon canh hu gao; dong tac di qua, khong giu pose"),

 ("d7_sofa_pov", "chanoma", "ms", "eye", "seated", "table4th", "dolly_kitchen", None,
  [("honnin", "full"), ("tsuma", "full")],
  "{honnin} sits back from the low table with a teacup in both hands while {tsuma} kneels opposite "
  "and pours; he says something short and she stops pouring and looks up, then she reacts, "
  "{EX:tsuma}, and he answers in his own way, {EX:honnin}, while the steam off the cup tilts "
  "sideways under the hanging light",
  False, "canh gia dinh — hai chu ky khac nhau, may o tam ngoi"),

 ("d8_flowers", "soubetsu", "mcu", "eye", "eye_st", "row_line", "dolly_flowers", None,
  [("honnin_tei", "full")],
  "{honnin_tei} stands between the two rows of colleagues as a large bouquet of red carnations and "
  "yellow chrysanthemums is put into his hands; he takes it and holds it against his chest, then "
  "his chin tightens and he keeps his eyes wide and dry on purpose, then he bows his head over the "
  "flowers, {EX:honnin_tei}, while the colleagues on both sides go on clapping",
  True, "M5 dinh bai — bo hoa la diem mau duy nhat"),

 ("d9_ima_paper", "ima_ie", "ms", "eye", "table", "sofa_side", "dolly_out_room", "daylight",
  [("ima", "trace")],
  "{ima} lifts a single old sheet of paper out of the flat box with both hands and lays it down "
  "on the table, then he turns it over once and rests his palm flat on it, then he lets his breath "
  "all the way out and his shoulders drop an inch, {EX:ima}, and he keeps looking at the same spot; "
  "the sheet is seen at an angle and nothing on it can be read",
  False, "canh THOI NAY — dong bai, chung nhan cua cold open da gia"),
]

POV_SHOTS = {}     # ban demo nay khong co POV — POV se them o ban day (163 o)


def pick_expr17():
    """Rut mot bien the CHUA DUNG cho tung cast cua video 17. Dung chung so voi cac video khac."""
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
            raise SystemExit("KHO CAN cho nguyen mau %s — viet bien the moi, dung quay lai cai cu"
                             % ARCH[cast])
        mine[cast] = free[0]
        used_now.add(free[0])
    return mine, reg


PICK = {}


def build(sh):
    (name, scene, size, angle, height, stand, move, land, expr, action, extras, _why) = sh
    for cast, lv in expr:
        action = action.replace("{EX:%s}" % cast, K.EXPR_BANK[ARCH[cast]][PICK[cast]] + K.LEVEL[lv])
    for k, v in CA.items():
        action = action.replace("{%s}" % k, v)
    is_pov = name in POV_SHOTS
    stand_s = (f"The camera is placed exactly where {STAND[stand]} would be, at that person's own "
               f"eye level, and the whole shot is seen from that one place.")
    if is_pov:
        frame_block, opener = POV_SHOTS[name], "A first-person shot filmed in 1970s Japan."
    else:
        frame_block = ", ".join([K.SIZE[size], K.ANGLE[angle], K.HEIGHT[height], K.OPTICS])
        opener = f"{K.SIZE[size].split(',')[0]}, filmed in 1970s Japan."
    parts = [opener,
             "NO letters, NO words, NO numbers and NO logos anywhere in the picture, and no film "
             "strip, no sprocket holes and no frame line along its edges.",
             move_block(move),
             stand_s,
             K.AVOID + (K.AVOID_SUBJ if is_pov else "") + ".",
             action + ".",
             frame_block + ".",
             SC[scene].rstrip(",") + ".",
             "Bright colour in the props: " + PROPS[scene] + K.PROP_TAIL + "."]
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
    flow, rows, red = [], [], 0

    # --- GATE 1: hai cast trong CUNG mot khung khong duoc cung chu ky (§6.7 muc 2)
    for sh in SHOTS:
        casts = [c for c, _ in sh[8]]
        sigs = [PICK[c] for c in casts]
        if len(set(sigs)) != len(sigs):
            print("[CHAN] %s: hai nguoi cung mot dieu cuoi trong mot khung: %s" % (sh[0], sigs)); red += 1

    # --- GATE 1b: chu ky khong duoc nhac dao cu ma cast khong co (bat 2026-09-21)
    for cast, sig in PICK.items():
        if sig in BAN.get(cast, []):
            print("[CHAN] %s bi rut chu ky %s nam trong BAN" % (cast, sig)); red += 1

    # --- GATE 2: tran lap chu ky ca video (§6.7 muc 4)
    cnt = Counter(c for sh in SHOTS for c, _ in sh[8])
    for c, n in cnt.items():
        if n > 3:
            print("[CHAN] chu ky cua %s lap %d lan (tran 3)" % (c, n)); red += 1

    for sh in SHOTS:
        p = build(sh)
        # --- GATE 3: tu cam cua khuon
        for b in K.BAD:
            if b in p:
                print("[CHAN] %s chua tu cam: %s" % (sh[0], b)); red += 1
        # --- GATE 4: dien xuat khong duoc la TEN cam xuc (§6.6)
        for f in K.FLAT:
            if f in p.lower():
                print("[CHAN] %s ta cam xuc bang TEN: %s" % (sh[0], f)); red += 1
        # --- GATE 5: khoi cam phai nam trong 15% dau (ai-video-regen.md §2)
        pos = p.find("NO letters")
        if pos * 100 // len(p) > 15:
            print("[CHAN] %s: guard NO-letters @ %d%% (tran 15%%)" % (sh[0], pos * 100 // len(p))); red += 1
        # --- GATE 6: dung MOT nuoc may
        if p.count("CAMERA MOVE, one move only") != 1:
            print("[CHAN] %s: khong phai dung 1 nuoc may" % sh[0]); red += 1
        flow.append(p)
        rows.append("%-16s %-10s %-14s %s" % (sh[0], sh[1], sh[6], sh[11]))
        print("%-16s %5d ky | guard @%2d%% | %s" % (sh[0], len(p), pos * 100 // len(p), sh[6]))

    print("\nchu ky da rut cho video 17: %s" % PICK)
    if red:
        print("\n[CHAN] %d loi — KHONG xuat file." % red)
        sys.exit(1)

    io.open(OUT / FLOW, "w", encoding="utf-8", newline="\n").write("\n".join(flow) + "\n")
    io.open(OUT / TENF, "w", encoding="utf-8", newline="\n").write(
        "# DEMO video 17 — thu tu dong trong %s <-> ten file\n" % FLOW
        + "\n".join("%d  %s.mp4   %s" % (i + 1, r.split()[0], r) for i, r in enumerate(rows))
        + "\n\n# chu ky bieu cam da rut (so EXPR_REGISTRY.json): %s\n" % PICK)
    reg[VIDEO_ID] = PICK
    K.REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n-> %s" % (OUT / FLOW))
    print("-> %s" % (OUT / TENF))
    print("-> da ghi so EXPR_REGISTRY.json cho video 17")


if __name__ == "__main__":
    main()
