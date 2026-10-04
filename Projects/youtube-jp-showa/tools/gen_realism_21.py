# -*- coding: utf-8 -*-
"""gen_realism_21.py — o AI cua video 21 (umaredoshi-okane), CONG THUC REALISM, khuon v08.

Video 21: ~50% hinh THAT (tools/plan_21.py). AI chi lap: canh co NGUOI trong truyen (me qua 3 thoi ky,
chi luc 6 tuoi / 18 tuoi / 74 tuoi, nguoi ke 68) va VAT hu cau trung tam (so tiet kiem, so chi tieu).
Moi o = STILL (Flow Image, Nano Banana 2). 10 canh `clip=True` co them MOTION (⋮ Animate, Veo 3.1) — dung tran 10.

🔴 Chu tren hinh: KHONG giao AI. Trang so tiet kiem / so chi / bang / to giay deu TRONG,
   chu 「でんわ」 va moi con so ve bang FONT o make_cells (feedback_so_tren_hinh_phai_do_font_ve).
🔴 Dong 34 (tho may Kyoto 1949 = nguoi THAT 林正治): chi quay LUNG, khong mat — cam mat nguoi that cu the.

Xuat 06_VIDEO/21_umaredoshi-okane/:
    realism21_STILL_FLOW.txt        anh TINH, 1 prompt / dong
    realism21_VIDEO_STILL_FLOW.txt  anh DE TAO VIDEO (clip=True), cung thu tu MOTION_FLOW
    realism21_MOTION_FLOW.txt       chi canh clip=True
    realism21_TENFILE.txt           dong i -> ten file (cells_in_ai/ai_NN_<key>.png|.mp4) + dong TTS
    realism21_BLOCKS.md             ban nguoi doc
"""
import io, sys
from pathlib import Path
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
sys.path.insert(0, str(Path(__file__).parent))
_argv = sys.argv; sys.argv = [sys.argv[0]]
import plan_21
sys.argv = _argv
from gen_prompts_21 import C
from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "21_umaredoshi-okane"

W59 = ("Setting: an ordinary Tokyo neighbourhood at the end of the nineteen-fifties, the real Showa era, classic and "
       "period-correct — a small wooden house, paper sliding screens, tatami, a low round chabudai table, a bare light "
       "bulb on a cord — nothing modern and nothing futuristic.")
W66 = ("Setting: the same small wooden Tokyo house in the mid-nineteen-sixties, the real Showa era — tatami, a tea "
       "cabinet, a wooden tube radio, lace doilies, a wooden-framed glass front door — period-correct, nothing modern.")
W71 = ("Setting: a provincial Japanese university town in the early nineteen-seventies, the real Showa era — wooden "
       "and plain concrete buildings, a women's student dormitory with tatami rooms — period-correct, nothing modern.")
W77 = ("Setting: Tokyo in the late nineteen-seventies, the real Showa era — a small neighbourhood post office with a "
       "wooden counter and frosted glass — period-correct, nothing modern.")
WNOW = ("Setting: the same old Japanese family home today, the night after a memorial service — a tatami room with a "
        "small household Buddhist altar, a low table, the Showa-era furniture still in use, quiet and cared for.")
NOTXT = "The upper-left quarter of the frame is calm and empty of important detail."
BLANK = "Every page, card and paper is completely blank, with no printing and no handwriting on it."
BOOK = ("an old Japanese post-office savings passbook lying open, small and pale green-grey, its pages ruled with "
        "faint empty lines and columns but carrying no characters and no numbers at all")

def P(key, line, still, act, where, height, light, world, cam="locked", alive="", clip=False):
    return dict(key=key, line=line, still=still, act=act, where=where, height=height, light=light,
                world=world, cam=cam, alive=alive, clip=clip)

A, AC, A18 = C["ane_now"], C["ane_child"], C["ane_18"]
H30, H38, H49 = C["haha30"], C["haha38"], C["haha49"]
ME, OBA, RYOBO = C["watashi_now"], C["tabako_oba"], C["ryobo"]
TABLE = "someone kneeling at the low table"
S = [
 # ---------------- HOOK (hien tai) ----------------
 P("siblings_tsucho", 1, "Two elderly siblings kneel side by side at a low wooden table in a tatami room at night, "
   "seen in three-quarter view: " + A + ", and beside her " + ME + ", his back half to the camera. Between them on "
   "the table lies " + BOOK + ". A small Buddhist altar glows softly behind them. " + BLANK + " " + NOTXT,
   "the man slowly turns one page of the passbook with his fingertip. " + HOLD_CLAUSE, TABLE, "seated height on the tatami",
   "night", WNOW),
 P("tsucho_pencil", 2, "Close on " + BOOK + ", lying on a dark wooden table under a warm lamp, a short worn pencil "
   "resting across the lower corner of the page. The ruled lines are empty. " + BLANK + " " + NOTXT,
   "the lamplight trembles very slightly across the page.", TABLE, "just above the table, looking down", "night", WNOW),
 P("ane_silent", 3, A + " kneels at a low table at night, looking down at an open passbook under her hands, seen from "
   "the side at her own seated height. Her face is still; her lips press together. " + BLANK + " " + NOTXT,
   "her fingertips stop on the page and stay there; she does not look up, and her shoulders drop a little as she "
   "breathes out. " + HOLD_CLAUSE, "her brother kneeling beside her", "seated height on the tatami", "night", WNOW, clip=True),
 P("ane_confess", 4, "A close shot of " + A + " at night, her face and shoulders filling most of the frame, eyes lowered "
   "to the table, one hand resting flat on an open passbook. Soft lamp light from one side. " + BLANK + " " + NOTXT,
   "her chin tightens once, she swallows, and her eyes lift slowly to the side towards her brother and then fall back "
   "to the page. " + HOLD_CLAUSE, "her brother kneeling beside her", "seated height, close", "night", WNOW, clip=True),
 P("ane_window", 6, A + " sits alone by a paper-screen window at night, seen in profile, her hands folded in her lap, "
   "looking at nothing. " + NOTXT, "she sits still; only her breathing moves.", "someone at the far side of the room",
   "seated height on the tatami", "night", WNOW),
 P("haha_iei", 7, "A small framed black-and-white portrait photograph standing on a household Buddhist altar between two "
   "small candles and a bowl of white chrysanthemums: the photo shows an old Japanese woman of about eighty with a round "
   "face, thick straight white eyebrows, wide-set eyes and a wide gentle mouth. The frame and altar carry no writing. " + NOTXT,
   "the candle flames flicker very slightly.", "someone kneeling before the altar", "kneeling eye height", "night", WNOW),
 P("tsucho_close", 8, "Close on " + BOOK + ", now half closed, lying on a tatami mat beside a folded mourning handkerchief. "
   + BLANK + " " + NOTXT, "the light moves very slightly across the pages.", TABLE, "just above the tatami, looking down",
   "night", WNOW),
 # ---------------- 1 百円玉 (1959) ----------------
 P("coin_palm", 15, "Inside a small Tokyo house in spring, " + H30 + " kneels on the tatami facing " + AC + ", who holds "
   "out one small open hand; the mother is about to place a single shining silver coin in it. The coin is small and bright, "
   "its design turned away from the camera. " + NOTXT,
   "the mother lays the coin in the girl's palm and gently folds the small fingers closed over it with both hands; the girl "
   "looks down at her own fist. " + HOLD_CLAUSE, "someone kneeling at the side of the room", "seated height on the tatami",
   "interior", W59, clip=True),
 P("coin_phoenix_macro", 16, "An extreme close shot of a little girl's fingertips turning a single shining silver coin under "
   "the warm light of a bare bulb, the coin tilted so that its face catches the light as a bright blur. " + NOTXT,
   "the fingertips turn the coin slowly once.", "the girl herself sitting on her futon", "just above her hands", "night", W59),
 P("haha_young_speak", 17, H30 + " kneels on the tatami in soft daylight, seen in three-quarter view, one hand still resting "
   "over her daughter's small closed fist, smiling a little with her eyes. " + NOTXT,
   "she gives one small nod and lets go of the girl's hand.", "the daughter standing before her", "a child's eye height",
   "interior", W59),
 P("ane_futon_coin", 18, AC + " lies in a futon at night under a bare light bulb on a cord, holding a small silver coin up "
   "between two fingers towards the bulb, the coin catching the light. " + NOTXT,
   "she turns the coin slowly in the light and smiles to herself.", "someone sitting beside the futon",
   "the camera almost on the tatami beside her pillow", "night", W59),
 P("far_banknote", 25, "A late nineteen-fifties Japanese shop counter seen from a small child's eye height: an adult's hand in "
   "a dark coat sleeve lays one large folded banknote on the wooden counter, the note far away and soft, seen only as a pale "
   "rectangle with no readable design, no portrait and no numbers. " + NOTXT,
   "the adult hand slides the note forward slowly across the counter.", "a small child standing at the counter",
   "a child's eye height", "interior", W59),
 P("haha_young_smile", 26, H30 + " stands at a small wooden kitchen with a paper-screen door behind her, a cloth over one "
   "shoulder, glancing back over her shoulder with a small closed-mouth smile. " + NOTXT,
   "she wipes her hands slowly on the cloth.", "someone at the kitchen doorway", "standing eye height", "interior", W59),
 # ---------------- 2 年賀はがき ----------------
 P("haha_brush", 31, H30 + " kneels at a low round chabudai table at night, writing on a plain postcard with a small "
   "calligraphy brush, an inkstone beside her, a small stack of blank postcards at her elbow. " + BLANK + " " + NOTXT,
   "she draws one slow stroke with the brush and lifts it away from the card. " + HOLD_CLAUSE,
   "someone kneeling across the table", "seated height on the tatami", "night", W59),
 P("tailor_kyoto", 34, "A small tailor's workroom in Kyoto at the end of the nineteen-forties: a man in a white shirt and "
   "waistcoat is seen strictly from behind, bent over a black treadle sewing machine by a window, bolts of grey wool on a "
   "shelf; his face is never visible. " + NOTXT, "the man's shoulders move slightly as he guides the cloth.",
   "someone standing at the door behind him", "standing eye height", "interior",
   "Setting: Kyoto at the end of the nineteen-forties, just after the war, a real period-correct Japanese town workshop."),
 P("kids_lottery", 42, AC + " and her small brother, a boy of about four with a round face and a cowlick, kneel on the "
   "tatami in winter daylight with New Year postcards laid out in rows in front of them, both bending over the cards. "
   + BLANK + " " + NOTXT, "the girl points at one card and the boy leans closer to look.", "someone kneeling at the edge of "
   "the tatami", "seated height on the tatami", "day", W59),
 P("haha_genkan_wait", 44, H38 + " stands in the small earthen entrance of a wooden house, looking out through the "
   "wooden-framed glass of the front door towards a small tin letterbox, her hands folded under her apron. " + NOTXT,
   "she leans very slightly towards the glass and then stays still.", "someone in the hallway behind her",
   "standing eye height", "day", W66),
 # ---------------- 3 ラジオ ----------------
 P("radio_wood", 46, "A wooden tabletop tube radio of the nineteen-fifties on top of a dark tea cabinet in a tatami room, "
   "a woven cloth grille, two round bakelite knobs and a plain glass dial window with no numbers and no letters on it. " + NOTXT,
   "the room stays still.", "someone kneeling in front of the cabinet", "seated height on the tatami", "night", W66),
 P("radio_night", 47, "A tatami living room at night: " + H38 + " reaches up and turns the knob of a wooden tube radio on "
   "top of the tea cabinet while " + AC.replace("about six", "about twelve") + " sits at a low table with a school notebook. "
   + BLANK + " " + NOTXT, "the mother turns the knob and steps back one pace; the girl puts down her pencil and turns her "
   "head towards the radio. " + HOLD_CLAUSE, "someone kneeling at the low table", "seated height on the tatami", "night", W66,
   clip=True),
 P("radio_back_glow", 49, "The back of an old wooden tube radio in a dark room, a warm orange glow coming through the gaps "
   "of its perforated back board, the shapes of the glowing tubes faintly visible inside. " + NOTXT,
   "the orange glow brightens very slowly.", "someone kneeling behind the cabinet", "seated height", "night", W66),
 P("family_listen", 50, "A tatami living room at night lit by one low lamp: " + H38 + " kneels by the kitchen doorway with a "
   "dish cloth in her hands, and a girl of twelve sits at the low table with her pencil down, both turned towards a "
   "wooden radio on the tea cabinet. " + BLANK + " " + NOTXT, "they both stay still, listening.",
   "someone kneeling in the corner of the room", "seated height on the tatami", "night", W66),
 P("radio_dial_close", 54, "Close on the plain glass dial window and one round knob of an old wooden radio, glowing warm "
   "amber from inside, the dial window carrying no numbers and no letters. " + NOTXT,
   "the amber glow flickers very slightly.", "someone kneeling in front of the radio", "at the height of the dial", "night", W66),
 P("tv_color_1968", 56, "A late nineteen-sixties Japanese living room: a wooden-cabinet colour television on four thin legs "
   "with a lace cover on top, its screen glowing with soft abstract colour and showing no text and no faces. " + NOTXT,
   "the colours on the screen shift slowly.", "someone kneeling across the room", "seated height on the tatami", "night", W66),
 P("haha_radio_quiet", 57, H38 + " kneels alone beside the wooden radio at night, seen in profile, one hand resting on the "
   "top of the cabinet, looking at the dial. " + NOTXT, "her eyes stay on the radio; she breathes out slowly.",
   "someone at the far side of the room", "seated height on the tatami", "night", W66),
 P("kakeibo_pencil", 59, "Close on an open household account book lying on a low table under a lamp, its ruled columns empty, "
   "a short pencil beside it and a few coins in a small dish. " + BLANK + " " + NOTXT,
   "the lamplight trembles very slightly.", TABLE, "just above the table, looking down", "night", W66),
 # ---------------- 4 電話 ----------------
 P("tabakoya_call", 64, OBA + " leans out of the small window of a tiny wooden tobacco shop in the mid-nineteen-sixties, one "
   "hand beside a red public telephone on the counter, turning her head down the lane. " + NOTXT,
   "she raises one hand and beckons twice down the lane.", "someone standing in the lane", "standing eye height", "day", W66),
 P("haha_run_sandal", 65, H38 + " hurries along a narrow lane between wooden houses in wooden sandals, wiping her hands on "
   "her apron as she goes, heading towards a small tobacco shop with a red telephone at its window. " + NOTXT,
   "she walks quickly along the lane away from the camera towards the shop, still wiping her hands.",
   "someone standing in the lane behind her", "standing eye height", "day", W66, clip=True),
 P("haha_decide", 69, H38 + " kneels at the low table in the evening, seen from the front at her own seated height, both "
   "hands flat on a small cloth bundle of savings, looking up with a set, calm face. " + NOTXT,
   "she presses her hands once on the bundle and gives one firm small nod.", "someone kneeling across the table",
   "seated height on the tatami", "interior", W66),
 P("haha_count_savings", 79, "Close on a woman's hands untying a small cloth bundle on a tatami mat to show a thin stack of "
   "folded paper money and a small savings passbook, the notes turned face down so no design shows. " + BLANK + " " + NOTXT,
   "the hands smooth the stack flat once. " + HOLD_CLAUSE, "the woman kneeling on the tatami", "just above her hands",
   "interior", W66),
 P("kurodenwa_lace", 80, "A heavy black rotary telephone of the nineteen-sixties sitting on a white lace doily on top of a "
   "polished wooden tea cabinet in a tatami living room, its dial with plain white finger holes and no printed letters. "
   + NOTXT, "the room stays still; the light moves slightly.", "someone kneeling in front of the cabinet",
   "seated height on the tatami", "interior", W66),
 P("haha_first_call", 83, H38 + " kneels beside the black telephone at night, holding the heavy receiver to her ear with both "
   "hands, seen in three-quarter view, her eyes bright. " + NOTXT,
   "her mouth opens in a small surprised laugh and she presses the receiver closer with both hands. " + HOLD_CLAUSE,
   "her daughter kneeling nearby", "seated height on the tatami", "night", W66, clip=True),
 P("tsucho_interest", 85, "Close on " + BOOK + ", open on a low table in soft daylight, a pencil resting in the fold. "
   + BLANK + " " + NOTXT, "the light moves very slightly across the page.", TABLE, "just above the table, looking down",
   "interior", W66),
 P("haha_tsucho_drawer", 88, H38 + " slides a small savings passbook into the back of a wooden tea-cabinet drawer, under a "
   "folded cloth, seen from the side. " + BLANK + " " + NOTXT,
   "she pushes the drawer closed slowly with both hands. " + HOLD_CLAUSE, "someone kneeling beside the cabinet",
   "seated height on the tatami", "interior", W66),
 # ---------------- 5 授業料 (1971 / 1977) ----------------
 P("ane_goukaku", 92, A18 + " stands among a small crowd of students in coats in front of a long wooden board of pinned blank "
   "white sheets outside a plain university building in early spring, one hand over her mouth, eyes shining. " + BLANK
   + " " + NOTXT, "her hand stays over her mouth; her eyes fill and she closes them for a moment. The crowd stands still.",
   "someone standing at the edge of the crowd", "standing eye height", "day", W71, clip=True),
 P("ryo_room", 94, "A small women's dormitory room of four and a half tatami mats in the early nineteen-seventies: two low "
   "desks against opposite walls, a small kerosene heater in the middle, socks drying on a string by the window. " + NOTXT,
   "the heater's warm air makes the socks sway very slightly.", "someone kneeling by the door", "seated height on the tatami",
   "dusk", W71),
 P("ryo_phone", 96, A18 + " stands in the entrance hall of a women's dormitory holding the receiver of a pink public "
   "telephone to her ear with one hand, the other hand pressed flat on the wall, smiling with her eyes closed. "
   + RYOBO + " walks away down the corridor behind her. " + NOTXT,
   "she turns her face towards the wall and laughs silently into the receiver. " + HOLD_CLAUSE,
   "someone standing at the far end of the hall", "standing eye height", "night", W71),
 P("univ_notice", 101, "A plain concrete university corridor in the early nineteen-seventies with a wooden notice board "
   "covered in pinned blank white sheets, a few students in coats walking past in the far background. " + BLANK + " " + NOTXT,
   "the students in the background stand still.", "someone standing in the corridor", "standing eye height", "day", W71),
 P("lecture_hall", 106, "A tiered university lecture hall of the early nineteen-seventies seen from the back row: wooden "
   "benches, students in dark coats and sweaters seen from behind, a large blank blackboard at the front. " + BLANK + " "
   + NOTXT, "the students sit still, one turns a page.", "a student sitting in the back row", "seated eye height", "day", W71),
 P("table_bg", 107, "Soft plain background of an old sheet of cream Japanese paper with a faint fibre texture, lit evenly, "
   "completely empty. " + BLANK, "nothing moves.", "someone looking at the paper", "straight on", "interior", ""),
 P("table_bg_b", 110, "Soft plain background of an old sheet of pale grey-blue Japanese paper with a faint fibre texture, "
   "lit evenly, completely empty. " + BLANK, "nothing moves.", "someone looking at the paper", "straight on", "interior", ""),
 P("table_bg_c", 93, "Soft plain background of an old sheet of pale cream Japanese paper with a faint fibre texture, lit "
   "evenly, completely empty. " + BLANK, "nothing moves.", "someone looking at the paper", "straight on", "interior", ""),
 P("yubin_window", 113, H49 + " stands at the wooden counter of a small neighbourhood post office, counting a stack of "
   "banknotes twice with her fingers, the notes turned so no design shows, a blank paying-in slip and a small red ink pad "
   "on the counter. " + BLANK + " " + NOTXT,
   "she finishes counting, lays the notes down and presses a small seal onto the blank slip once. " + HOLD_CLAUSE,
   "the clerk behind the counter", "standing eye height", "interior", W77, clip=True),
 P("ane_young_photo", 115, "An old small colour photograph of the early nineteen-seventies lying on a tatami mat, slightly "
   "faded, showing " + A18 + " standing in front of a plain university gate in spring; the gate carries no readable sign. "
   + NOTXT, "the light moves slightly across the photograph.", "someone kneeling on the tatami", "looking down",
   "interior", WNOW),
 P("private_univ", 116, "A grand old private university building in Tokyo in the mid-nineteen-seventies, red brick and ivy, "
   "students walking far in the background, no readable signs. " + NOTXT, "the students in the far background stand still.",
   "someone standing across the street", "standing eye height", "day", W77),
 # ---------------- KET (hien tai) ----------------
 P("siblings_night2", 119, ME + " and " + A + " kneel at the low table at night, both looking down at an open passbook "
   "between them, seen from across the table. " + BLANK + " " + NOTXT, "the man turns back one page slowly. " + HOLD_CLAUSE,
   "someone kneeling across the table", "seated height on the tatami", "night", WNOW),
 P("tsucho_pages", 120, "Close on two hands turning back the pages of " + BOOK + " to the very first page, on a dark table "
   "under a lamp. " + BLANK + " " + NOTXT, "the hands turn one page. " + HOLD_CLAUSE, TABLE, "just above the table",
   "night", WNOW),
 P("tsucho_rows", 121, "Close on " + BOOK + ", open flat, a man's fingertip running down the empty ruled column. " + BLANK
   + " " + NOTXT, "the fingertip moves slowly down the column and stops. " + HOLD_CLAUSE, TABLE, "just above the page",
   "night", WNOW),
 P("tsucho_out1", 122, "Close on " + BOOK + ", a woman's fingertip with a short silver bob just in frame resting on one "
   "empty ruled line near the top of the page. " + BLANK + " " + NOTXT, "the fingertip stays still on the line.",
   TABLE, "just above the page", "night", WNOW),
 P("tsucho_out2", 123, "Close on " + BOOK + ", a man's fingertip resting on one empty ruled line lower down the page. "
   + BLANK + " " + NOTXT, "the fingertip taps the line once and stays.", TABLE, "just above the page", "night", WNOW),
 P("haha_bond_kept", 125, H38 + " kneels at the tea cabinet in the evening holding a folded plain paper certificate in both "
   "hands, looking at it, then setting it carefully back into a drawer. " + BLANK + " " + NOTXT,
   "she lays the paper into the drawer and rests her hand on it for a moment. " + HOLD_CLAUSE,
   "someone kneeling behind her", "seated height on the tatami", "dusk", W66),
 P("haha_phone_old", 126, H49 + " sits beside the black telephone on its lace doily in the evening, the receiver in her lap, "
   "looking at it with a small tired smile. " + NOTXT, "she lifts the receiver slowly back onto its cradle. " + HOLD_CLAUSE,
   "someone at the far side of the room", "seated height on the tatami", "dusk", W77),
 P("tsucho_first", 128, "Close on " + BOOK + ", open at its first page under a lamp, beside it a small old black-and-white "
   "photograph of a mother and two young children, face down. " + BLANK + " " + NOTXT,
   "the lamplight trembles very slightly.", TABLE, "just above the table, looking down", "night", WNOW),
 P("ane_handbag", 130, A + " kneels at the low table at night and takes a tiny folded paper packet out of an old black "
   "handbag on her lap, seen in three-quarter view. " + NOTXT,
   "she lifts the paper packet out with two fingers and holds it in her palm. " + HOLD_CLAUSE,
   "her brother kneeling across the table", "seated height on the tatami", "night", WNOW),
 P("coin_unwrap", 131, "Close on the palms of " + A.split(",")[0] + " unfolding a tiny square of old white paper at night; "
   "inside lies one small shining silver coin, its design turned away from the camera. " + NOTXT,
   "she opens the last fold of the paper and the silver coin catches the lamplight. " + HOLD_CLAUSE,
   "her brother kneeling across the table", "just above her hands", "night", WNOW, clip=True),
 P("ane_tears", 132, "A close shot of " + A + " at night, looking down at something in her hand, her eyes wet and bright, "
   "her mouth trying to smile. " + NOTXT, "she lets out one breath through her nose and blinks slowly twice.",
   "her brother kneeling beside her", "seated height, close", "night", WNOW),
 P("coin_on_tsucho", 133, "Close on " + BOOK + ", open on the low table at night, and the hand of an old woman with a "
   "pearl ring holding one small silver coin just above the page. " + BLANK + " " + NOTXT,
   "her fingers lower the coin slowly onto the open page and rest there, trembling a little. " + HOLD_CLAUSE,
   "her brother kneeling across the table", "just above the table", "night", WNOW, clip=True),
 P("tsucho_coin_light", 134, "Close on one small shining silver coin lying alone on the open pages of " + BOOK + " under a "
   "warm lamp, its design turned away from the camera. " + BLANK + " " + NOTXT,
   "the lamplight moves very slightly across the coin.", TABLE, "just above the table, looking down", "night", WNOW),
 P("ane_smile", 137, A + " sits at the low table at night, seen in three-quarter view, looking across at her brother with a "
   "small, wet-eyed smile. " + NOTXT, "one corner of her mouth goes up and she gives one small nod.",
   "her brother kneeling across the table", "seated height on the tatami", "night", WNOW),
 P("siblings_back", 142, "Two elderly siblings seen from behind at night, " + A.split(",")[0] + " and " + ME.split(",")[0]
   + ", kneeling side by side in front of a small glowing household Buddhist altar. " + NOTXT,
   "they both bow their heads slowly.", "someone kneeling at the back of the room", "seated height on the tatami",
   "night", WNOW),
]

DROPPED = {"tsucho_coin_light", "siblings_tsucho", "ane_silent", "ane_window", "haha_iei", "tsucho_close"}   # 09-29: 30s dau doi sang hinh THAT   # user khong gen duoc anh nay (2026-09-29) -> o truoc keo dai

def main():
    stills, vstills, motions, rows, vrows, si, md, bad = [], [], [], [], [], 0, ["# realism21 — o AI video 21 (ban nguoi doc)\n"], 0
    keys = [s["key"] for s in S]
    assert len(keys) == len(set(keys)), "trung key"
    need = sorted({c[3:].replace("+NUM", "") for _, cs in plan_21.PLAN_T for c in cs if c.startswith("AI:")})
    miss = sorted(set(need) - set(keys)); extra = sorted(set(keys) - set(need) - DROPPED)
    if miss or extra: print("🔴 lech plan_21 — thieu:", miss, "| thua:", extra); bad += 1
    nclip = sum(1 for s in S if s["clip"])
    if nclip > 10: print("🔴 %d clip AI > tran 10" % nclip); bad += 1
    mi = 0
    for i, sc in enumerate(S, 1):
        st, mo, _ = build_pair(dict(sc), sc["world"])
        for kind, p in (("still", st),) + ((("motion", mo),) if sc["clip"] else ()):
            pr = gate_prompt(kind, p, LIMIT_SHOWA)
            if pr: bad += 1; print(f"  🔴 {i:02d} {sc['key']} {kind}: {pr}")
        for k, m in gate_action(sc["act"]):
            if k != "③": bad += 1
            print(f"  {'⚠' if k == '③' else '🔴'} {i:02d} {sc['key']} action {k}: {m}")
        fn = "ai_%02d_%s" % (i, sc["key"])
        if sc["clip"]:
            vstills.append(st); motions.append(mo); mi += 1
            vrows.append(f"{mi:02d}\t{fn}.png -> Animate -> {fn}.mp4\tTTS dong {sc['line']}\t{sc['key']}")
        else:
            stills.append(st); si += 1
            rows.append(f"{si:02d}\t{fn}.png\tTTS dong {sc['line']}\t{len(st)} ky")
        md += [f"## {i:02d} · {sc['key']} (TTS dong {sc['line']}){' · CLIP' if sc['clip'] else ''}\n",
               f"**STILL** ({len(st)} ky)\n\n{st}\n"] + ([f"**MOTION** ({len(mo)} ky)\n\n{mo}\n"] if sc["clip"] else [])
    W = lambda name, txt: io.open(OUT / name, "w", encoding="utf-8", newline="\n").write(txt)
    W("realism21_STILL_FLOW.txt", "\n".join(stills) + "\n")
    W("realism21_VIDEO_STILL_FLOW.txt", "\n".join(vstills) + "\n")
    W("realism21_MOTION_FLOW.txt", "\n".join(motions) + "\n")
    W("realism21_TENFILE.txt",
      "# ===== A. ANH TINH — realism21_STILL_FLOW.txt (dong i -> ten file) =====\n"
      "# bo vao 06_VIDEO/21_umaredoshi-okane/cells_in_ai/\n" + "\n".join(rows) + "\n\n"
      "# ===== B. ANH DE TAO VIDEO — realism21_VIDEO_STILL_FLOW.txt dong k + realism21_MOTION_FLOW.txt dong k =====\n"
      "# gen anh (Image) -> chon anh -> ⋮ Animate -> dan MOTION cung so dong -> tai .mp4\n"
      "# bo CA .png lan .mp4 vao cells_in_ai/ (khong gen duoc clip thi .png van dung lam anh tinh)\n"
      + "\n".join(vrows) + "\n")
    io.open(OUT / "realism21_BLOCKS.md", "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(f"{si} anh tinh · {mi} anh+motion de tao video -> {OUT}\\realism21_*  | gate do: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
