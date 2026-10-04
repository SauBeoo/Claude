# -*- coding: utf-8 -*-
"""gen_realism_20.py — o AI cua video 20 (sumai-okane), CONG THUC REALISM, khuon v08.

Video 20: 66% hinh THAT (tools/plan_20.py). AI chi lap: canh co NGUOI trong truyen (me, cha, con, ba 番台)
va VAT trung tam khong co ban that dung (bo hagaki buoc thun, mat sau hagaki trong).
Moi o = STILL (Flow Image, Nano Banana 2). 8 canh danh dau `clip=True` co them MOTION (⋮ Animate, Veo 3.1)
— trong tran 10 clip/video; khong gen clip thi build dung anh tinh, khong hong gi.

🔴 Chu tren hinh: KHONG giao AI. Mat sau hagaki (dong 120-126) va to 募集/貼り紙 de TRONG, chu ve bang FONT
   o make_cells (feedback_so_tren_hinh_phai_do_font_ve). Goc TREN-TRAI chua trong cho o +NUM.

Xuat 06_VIDEO/20_sumai-okane/:
    realism20_STILL_FLOW.txt   anh TINH (canh khong lam clip), 1 prompt / dong, extension bom thang
    realism20_VIDEO_STILL_FLOW.txt  anh DE TAO VIDEO (canh clip=True), cung thu tu MOTION_FLOW
    realism20_MOTION_FLOW.txt  chi cac canh clip=True, 1 prompt / dong
    realism20_TENFILE.txt      dong i -> ten file (cells_in_ai/ai_NN_<key>.png|.mp4) + cau TTS
    realism20_BLOCKS.md        ban nguoi doc
"""
import io, sys, json
from pathlib import Path
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
sys.path.insert(0, str(Path(__file__).parent))
import plan_20                      # tu boc stdout utf-8 — dung boc lan hai (dong luong cu)
from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "20_sumai-okane"

# ---- DAN DIEN video 20 — KHUON MAT co dinh + DO MAC doi theo boi canh. Moi, khong chep video 19.
FACE = {
 "haha": ("a Japanese woman of about twenty-four with a heart-shaped face, a slightly broad forehead, softly "
          "arched thick eyebrows, double-lidded almond eyes, a small straight nose, a full lower lip and a faint "
          "dimple in the right cheek, shoulder-length black hair tucked behind her ears"),
 "haha30": ("the same woman at about thirty — the same heart-shaped face, broad forehead, softly arched thick "
          "eyebrows, double-lidded almond eyes, small straight nose, full lower lip and faint right-cheek dimple — "
          "her black hair now in a short soft perm"),
 "chichi": ("a Japanese man of about twenty-seven with a long narrow face, hollow cheeks, straight heavy "
          "eyebrows, narrow thin-lidded eyes, a long nose with a slight bump, a small tight mouth and short "
          "side-parted black hair with a cowlick sticking up at the crown"),
 "chichi35": ("the same man at about thirty-five — the same long narrow face, hollow cheeks, straight heavy "
          "eyebrows, narrow thin-lidded eyes and long nose with a slight bump, the cowlick still at the crown, "
          "a first few grey hairs at the temples"),
 "chichi80": ("the same man past eighty — the same long narrow face and long nose with a slight bump, the heavy "
          "eyebrows gone white, cheeks sunken, deep lines from nose to mouth, thin white hair combed flat"),
 "bandai": ("a Japanese woman of about sixty with a wide flat face, round cheeks, small kind eyes behind round "
          "wire glasses, grey hair pulled into a tight bun, a knitted cardigan with white sleeve covers"),
 "baby":  "a baby girl of about six months, round-cheeked, with a wisp of black hair",
 "toddler": "a little girl of about eighteen months with a bowl of short black hair and chubby cheeks",
}
W67 = ("Setting: an ordinary Tokyo neighbourhood in the late nineteen-sixties, the real Showa era, classic and "
       "period-correct — wooden apartment houses, paper sliding screens, tatami, enamel basins, wooden geta — "
       "nothing modern and nothing futuristic.")
W70 = ("Setting: a brand-new public housing apartment block in the Tokyo suburbs in the early nineteen-seventies, "
       "the real Showa era — bare concrete, steel doors, a small dining kitchen with a formica table, "
       "period-correct and nothing modern.")
W76 = ("Setting: the outer Tokyo suburbs in the mid-nineteen-seventies, the real Showa era — new small wooden "
       "two-storey houses among vegetable fields, period-correct and nothing modern.")
WNOW = ("Setting: the same old Japanese family home today, fifty years later — the furniture from the Showa era "
        "still in use, worn and cared for, soft and quiet.")
NOTXT = "The upper-left quarter of the frame is calm and empty of important detail."
ONEFRAME = ("One single continuous photograph from one camera position — not a collage, not split into panels, "
            "no inset pictures, no picture-in-picture, no borders dividing the frame. ")
BLANK = "Every card and paper is completely blank, with no printing and no handwriting on it."

def P(key, line, still, act, where, height, light, world, cam="locked", alive="", clip=False):
    return dict(key=key, line=line, still=still, act=act, where=where, height=height, light=light,
                world=world, cam=cam, alive=alive, clip=clip)

TATAMI = "someone kneeling on the tatami across the room"
S = [
 P("hagaki_bundle", 2, "Close on an old wooden tea cabinet drawer pulled open: at the back of the drawer lies a small "
   "bundle of six old Japanese postcards, yellowed at the edges and held together with a single brown rubber band, "
   "resting on folded paper beside a spool of thread and a thimble. " + BLANK + " " + NOTXT,
   "a woman's hand in a grey cardigan sleeve reaches into the drawer and slowly lifts the bundle of postcards out "
   "into the light. " + HOLD_CLAUSE, "a daughter kneeling in front of the cabinet", "kneeling eye height",
   "interior", WNOW, clip=True),
 P("hagaki_turn", 8, "Close on a woman's hand in a grey cardigan sleeve turning over the top card of a small bundle of "
   "old yellowed Japanese postcards held over a tatami floor, the bundle still in its brown rubber band. " + BLANK +
   " " + NOTXT, "the hand turns the top card over slowly and holds it still. " + HOLD_CLAUSE,
   "a daughter kneeling in front of the tea cabinet", "just above her hands", "interior", WNOW),
 P("drawer_empty", 6, "Looking down into the same open tea cabinet drawer, now almost empty: only folded paper, a "
   "spool of thread and a thimble, and a pale rectangle on the paper where something lay for many years. " + NOTXT,
   "the light from the window moves very slightly across the paper.", "a daughter kneeling in front of the cabinet",
   "just above the drawer, looking down", "interior", WNOW),
 P("father_print", 14, "Inside a small town letterpress print shop, cases of metal type on sloping wooden racks along "
   "the wall and a black hand-fed press. The young father — " + FACE["chichi"] + ", in a grey work apron over a "
   "white shirt with the sleeves rolled up, ink on his fingers — stands at the press, eyes down on a sheet of "
   "blank paper. " + BLANK + " " + NOTXT, "the father lowers the lever of the press slowly and lifts it again.",
   "a fellow printer standing by the type racks", "standing eye height", "interior", W67),
 P("fudousan_door", 16, "The sliding glass front door of a small neighbourhood estate agent's office beside a "
   "station, its glass covered from top to bottom with rows of plain white sheets of paper taped up edge to edge. "
   + BLANK + " A young couple is reflected faintly in the glass. The upper-left part of the door is one clean area "
   "of plain white paper.", "the reflections shift a little as the couple leans closer.",
   "a passer-by stopping on the pavement", "standing eye height", "day", W67),
 P("apart_corridor", 17, "The upstairs corridor of an old two-storey wooden apartment house: worn dark floorboards, a "
   "row of plain wooden doors on one side, and at the far end a shared stone sink with one brass tap and a small "
   "shared toilet door. The young mother — " + FACE["haha"] + ", in a plain beige coat — walks away along the "
   "corridor behind a stooped landlady.", "the young mother walks slowly along the corridor towards the sink.",
   "someone standing at the top of the stairs", "standing eye height", "interior", W67),
 P("window_monohoshi", 18, ONEFRAME + "Inside a small six-mat tatami room with bare walls, the young mother — " + FACE["haha"] +
   ", in a beige coat — has just slid open the wooden window; a hand's reach away outside, on the next house, a "
   "bamboo drying pole hangs with white shirts and a striped futon cover moving in the breeze. " + NOTXT,
   "the washing outside sways gently while she rests one hand on the window frame and looks out.",
   "someone standing in the doorway of the empty room", "standing eye height", "day", W67),
 P("father_nod", 20, ONEFRAME + "In the same bare six-mat tatami room, the young father — " + FACE["chichi"] + ", in a dark "
   "suit jacket too big at the shoulders — stands by the window in three-quarter view, hands in his pockets, "
   "looking at the floor; beside him the young mother, seen from behind, turns towards him. " + NOTXT,
   "the father gives one small nod, then a second one to himself after she has already looked away.",
   TATAMI, "standing eye height", "day", W67),
 P("two_envelopes", 21, "On a low wooden table in a landlord's front room, two plain white paper envelopes lie side "
   "by side, a little apart, beside a cup of green tea and a pair of reading glasses. " + BLANK + " " + NOTXT,
   "a man's hand in a dark suit sleeve slides the two envelopes a little further across the table. " + HOLD_CLAUSE,
   "the landlord kneeling on the other side of the table", "seated height on the tatami", "interior", W67),
 P("shared_toilet", 29, "The narrow end of an old wooden apartment corridor: a small wooden door to a shared toilet, "
   "a pair of plastic toilet slippers set neatly in front of it, a bare bulb hanging from the ceiling, a "
   "mop propped in the corner. " + NOTXT, "the bare bulb sways very slightly on its cord.",
   "a tenant stepping out of his room", "standing eye height", "dawn", W67),
 P("toilet_line", 30, "Early morning in the same wooden apartment corridor: three tenants wait in a line outside the "
   "small shared toilet door — a middle-aged man in a striped cotton sleeping kimono, a young woman with a towel "
   "over her shoulder, and at the back the young father — " + FACE["chichi"] + ", in a crumpled undershirt, "
   "yawning.", "the young father rubs the back of his neck and shifts his weight from one foot to the other while "
   "the others stand still.", "a tenant standing in the doorway of his room", "standing eye height", "dawn", W67),
 P("senmenki_prep", 33, "On the tatami by the door of the small room: a yellow plastic washbasin holding a bar of "
   "white soap in a plastic case, a folded thin cotton towel and a small bottle, and beside it a pair of wooden "
   "geta on the concrete step. The young mother's hands — " + FACE["haha"] + " is seen only from the shoulders "
   "down, kneeling — tuck the towel into the basin.", "she lifts the basin onto her hip and rises slowly. "
   + HOLD_CLAUSE, "someone kneeling inside the room", "seated height on the tatami", "night", W67),
 P("night_walk_geta", 34, "A narrow residential lane at night between wooden fences and houses, a single street "
   "lamp, and in the distance the tall brick chimney of a public bathhouse against the dark sky. The young mother "
   "— " + FACE["haha"] + ", in a cardigan, the yellow washbasin under her arm — walks away from us in wooden geta, "
   "beside the young father.", "the couple walk slowly away along the lane towards the chimney.",
   "someone walking a few steps behind them", "standing eye height", "night", W67, cam="drift"),
 P("mother_baby_sento", 36, "In the changing room of an old public bathhouse, tall wooden lockers and wicker baskets "
   "on the floor, the young mother — " + FACE["haha"] + ", in a cotton yukata, her hair wet — kneels on the wooden "
   "floor drying " + FACE["baby"] + " wrapped in a white towel on her lap. Other women in the background are "
   "fully dressed and out of focus. Everyone is decently covered.", "the mother rubs the towel gently over the "
   "baby's head and bends to look at her face.", "a woman sitting on the bench beside the lockers",
   "seated eye height", "interior", W67, clip=True),
 P("mother_dress_baby", 36, "Close on the young mother's hands buttoning a small knitted baby cardigan on "
   + FACE["baby"] + " lying on a towel on a wicker basket lid in a bathhouse changing room; the mother, "
   + FACE["haha"] + ", in a cotton yukata, is seen in three-quarter view, her own hair still dripping. "
   "Everyone is decently covered.", "the mother fastens the last button and lifts the baby to her shoulder.",
   "a woman sitting on the bench beside the lockers", "seated eye height", "interior", W67),
 P("sento_noren_night", 37, "Late on a winter night outside an old wooden public bathhouse: the short dark-blue noren "
   "curtain hangs over the sliding door, warm light behind it, the street empty and dark. The young mother — "
   + FACE["haha"] + ", in a padded winter coat, " + FACE["baby"] + " tied on her back in a carrying sling, the "
   "yellow washbasin under her arm — ducks under the noren. The curtain is plain, with no lettering.",
   "the mother bends her head and slips under the curtain, one hand holding it aside.",
   "someone standing across the dark street", "standing eye height", "night", W67),
 P("mother_tub_baby", 39, "Late at night in an almost empty old public bathhouse, a large tiled bath with a big "
   "painted mountain mural on the far wall, steam thin and fading. The young mother — " + FACE["haha"] + " — sits "
   "in the water up to her shoulders holding " + FACE["baby"] + " against her chest, only their heads and her "
   "shoulders above the water. Wooden buckets stacked at the edge.", "the mother lowers the baby gently a little "
   "deeper into the water, her chin tightening, her eyes kept on the far wall.",
   "someone sitting on the edge of the bath at the far end", "seated eye height", "night", W67, clip=True),
 P("bandai_lady", 48, "At the entrance of an old public bathhouse: the raised wooden attendant's booth, and in it "
   + FACE["bandai"] + ", sitting and looking down at a small tray of coins, a round wall clock and a calendar with "
   "blank pages behind her. " + NOTXT, "the attendant slides the coin tray a little to one side and looks up "
   "towards the door with a half smile.", "a customer standing at the entrance", "standing eye height",
   "interior", W67),
 P("after_bath_walk", 50, "A narrow lane at night after the bath: the young mother — " + FACE["haha"] + ", in a "
   "cardigan, her hair damp and loose — carries " + FACE["baby"] + " wrapped in a blanket, her breath faintly "
   "visible in the cold air, a street lamp behind her, wooden houses with lit paper windows.",
   "she walks slowly towards us and pulls the blanket closer around the baby's head.",
   "a neighbour standing by his gate", "standing eye height", "night", W67),
 P("father_flyer", 52, "The genkan of the small wooden apartment at night: the young father — " + FACE["chichi"] +
   ", in a work jacket, just home — holds up one folded sheet of plain paper; behind him the young mother, "
   + FACE["haha"] + ", with the baby on her back in a carrying sling, turns from the tiny stove. " + BLANK,
   "the father slowly unfolds the sheet and holds it out towards her without a word.",
   "someone standing inside the room by the low table", "standing eye height", "night", W67, clip=True),
 P("flyer_table", 54, "A low round wooden table in the small tatami room at night, lit by one lamp: a single sheet of "
   "paper laid flat in front of an empty teacup, a pair of men's hands just drawing back from it. " + BLANK + " "
   + NOTXT, "the man's hands draw back slowly and rest on his knees.", "the wife kneeling at the table",
   "seated height on the tatami", "night", W67),
 P("mother_reads_flyer", 55, "The young mother — " + FACE["haha"] + ", in a cardigan — kneels at the low round "
   "table holding the plain sheet of paper in both hands, seen in three-quarter view, the baby asleep on a small "
   "futon behind her. " + BLANK, "her eyes go first and crease, the cheeks pushing up, and she lowers the paper "
   "into her lap.", "the husband kneeling across the table", "seated height on the tatami", "night", W67),
 P("hagaki_single", 57, "One plain old Japanese postcard lying alone on a dark wooden tea cabinet shelf, lit from one "
   "side by a window. " + BLANK + " The upper-left part of the frame is plain dark wood.",
   "the window light moves very slightly across the card.", "a woman standing at the cabinet",
   "standing eye height, looking down", "interior", W67),
 P("hagaki_six_table", 59, "Six plain old Japanese postcards laid out in a neat row on a low wooden tea table, a cup "
   "of tea and an ashtray beside them. " + BLANK + " " + NOTXT, "the steam from the tea rises slowly.",
   "someone kneeling at the table", "seated height on the tatami, looking down", "interior", W67),
 P("father_smoke_out", 60, "Outside the wooden apartment house at dusk, the young father — " + FACE["chichi"] + ", "
   "in a white shirt — stands alone at the foot of the outside iron staircase, a thin trail of smoke rising from "
   "his hand, looking down the lane. Laundry hangs on the balconies above.", "the father tips his head back and "
   "lets out one long breath of smoke, then looks down at his feet.", "a neighbour standing at the corner",
   "standing eye height", "dusk", W67),
 P("mother_drawer", 61, "In the small tatami room, the young mother — " + FACE["haha"] + ", in a cardigan — kneels in "
   "front of a small wooden tea cabinet, sliding one plain postcard into an open drawer on top of others. "
   + BLANK, "she lays the card down and slowly pushes the drawer closed with both hands. " + HOLD_CLAUSE,
   TATAMI, "seated height on the tatami", "interior", W67),
 P("hagaki_seventh", 70, "Morning light on the wooden step inside a front door: one plain postcard lying on the "
   "floor just inside the mail slot, the young mother's slippered feet stepping towards it. " + BLANK + " " + NOTXT,
   "the mother bends down slowly and picks up the card. " + HOLD_CLAUSE, "someone standing in the room behind her",
   "standing eye height, looking down", "day", W67),
 P("danchi_boxes", 72, "A brand-new empty public housing apartment: bare concrete walls painted cream, a small "
   "dining kitchen with a formica table, cardboard boxes tied with string piled on the floor, and through a "
   "doorway a small bathroom with a square tub and a gas bath heater on the wall. The young mother — "
   + FACE["haha"] + " — steps over the boxes towards the bathroom. " + NOTXT,
   "the mother walks slowly past the boxes towards the bathroom door.", "the husband standing at the front door",
   "standing eye height", "day", W70),
 P("danchi_bath_mother", 74, "A small square tiled bathtub in a new public housing apartment, a gas bath heater on "
   "the wall beside it, a frosted window. The young mother — " + FACE["haha"] + " — sits in the water holding "
   + FACE["toddler"] + " on her lap, only heads and shoulders above the water, steam rising softly. Everyone is "
   "decently covered by the water.", "the little girl slaps the water once and the mother laughs, her eyes "
   "creasing into two slits and her head tilting towards the child.", "someone standing at the bathroom door",
   "standing eye height", "interior", W70, clip=True),
 P("father_beer", 76, "Night in the new public housing apartment: the young father — " + FACE["chichi"] + ", in a "
   "white undershirt — sits cross-legged on the tatami beside a small futon where " + FACE["toddler"] + " sleeps, "
   "an unopened plain silver drink can in his hand, one lamp on. " + NOTXT,
   "the father opens the can with a small click and holds it without drinking, watching the child sleep.",
   "the wife standing in the kitchen doorway", "seated height on the tatami", "night", W70, clip=True),
 P("futon_room", 82, "A small two-room public housing apartment at night, the floor of both rooms covered edge to "
   "edge with futons: the parents, the little girl and a new baby boy asleep, one lamp in the kitchen beyond. "
   "The mother — " + FACE["haha30"] + " — sits up at the edge of the futons, looking over them.",
   "the mother pulls a blanket up over the baby boy's shoulder and stays sitting.",
   "someone standing in the kitchen doorway", "standing eye height", "night", W70),
 P("coat_pocket", 83, "Close on a man's dark wool winter coat hanging on a hook in a small entrance hall, the "
   "mother's hand — " + FACE["haha30"] + " is seen in three-quarter view — holding the empty pocket open.",
   "the mother slowly pulls her hand out of the empty pocket and looks at it.",
   "someone standing in the hall", "standing eye height", "interior", W70),
 P("passbook_small", 86, "On a formica dining table in a small public housing kitchen, a small plain bank passbook "
   "with a plain cover lies closed next to a personal seal in a little case and a cup of tea. " + BLANK + " "
   + NOTXT, "the father's hand lays a folded plain envelope on top of the passbook. " + HOLD_CLAUSE,
   "the wife sitting across the table", "seated eye height", "interior", W70),
 P("house_frame", 89, "A small wooden house frame going up on a building plot among vegetable fields: fresh pale "
   "timber posts and beams against the sky, two carpenters in headbands on the frame, a lorry of timber below. "
   + NOTXT, "one carpenter slowly raises a wooden mallet on the beam.", "the owner standing by the road",
   "standing eye height", "day", W76),
 P("hanko_form", 94, "Sunday in a small public housing dining kitchen: at a formica table the father — "
   + FACE["chichi35"] + ", in a cardigan — holds a small personal seal over a plain sheet of paper, the mother "
   + FACE["haha30"] + " beside him watching. " + BLANK, "the father presses the seal down slowly and lifts it, "
   "and the mother lets her breath all the way out.", "a child sitting on the other side of the table",
   "seated eye height", "day", W70, clip=True),
 P("house_pillar", 96, "Inside a newly framed small wooden house, sunlight through bare timber posts, sawdust on the "
   "floorboards, one fresh square pillar in the centre with a carpenter's pencil mark. The father — "
   + FACE["chichi35"] + " — stands with one palm on the pillar.", "the father slowly runs his palm down the pillar.",
   "a carpenter standing by the doorway", "standing eye height", "day", W76),
 P("mother_worried", 103, "In the public housing dining kitchen at night the mother — " + FACE["haha30"] + ", in an "
   "apron — sits at the formica table looking at the father across it, her hands folded tight on the table.",
   "her hand goes out towards his, stops short, and comes back to her lap.", "the husband sitting across the table",
   "seated eye height", "night", W70),
 P("nameplate_nail", 110, "Autumn at the front of a small new two-storey wooden house among vegetable fields: the "
   "father — " + FACE["chichi35"] + ", in a cardigan — holds a plain unmarked wooden nameplate against the entrance "
   "post and raises a small hammer. " + BLANK, "the father taps the nail twice and steps back to look.",
   "the wife standing at the gate", "standing eye height", "day", W76),
 P("new_bath_window", 111, "A new wooden house bathroom in autumn: a deep square wooden-rimmed tub full of steaming "
   "water under a wide open window, green fields outside. " + NOTXT, "the steam rises slowly past the window.",
   "someone standing at the bathroom door", "standing eye height", "day", W76),
 P("father_old_porch", 114, "Evening on the wooden veranda of the small house, now old: the father — "
   + FACE["chichi80"] + ", in a grey cardigan — sits alone looking out at the garden and the houses where the fields "
   "used to be.", "the old man lets his breath all the way out and his shoulders drop, and he keeps looking at the "
   "same spot.", "someone sitting on the veranda beside him", "seated height", "dusk", WNOW),
 P("chadansu_open", 117, "An old wooden tea cabinet in a quiet tatami room, its middle drawer pulled half open, a "
   "folded cardigan on the tatami in front of it and afternoon light through a paper screen. " + NOTXT,
   "the light through the paper screen shifts very slightly.", TATAMI, "seated height on the tatami",
   "interior", WNOW),
 P("hands_rubber_band", 118, "Close on a woman's hands in a grey cardigan sleeve slipping a brown rubber band off a "
   "small bundle of old yellowed postcards held over a tatami floor. " + BLANK,
   "the hands slide the rubber band off slowly and turn the top card over. " + HOLD_CLAUSE,
   "the woman's own place kneeling on the tatami", "just above her hands", "interior", WNOW),
]
for n, (lt, ang) in enumerate([("interior", "lying flat on tatami in soft window light"),
                               ("interior", "held in a woman's left hand against a grey cardigan"),
                               ("night", "lying on a low wooden table under a lamp"),
                               ("interior", "resting on the open lid of a wooden sewing box"),
                               ("day", "lying on a sunlit paper-screen sill"),
                               ("interior", "held in both of a woman's hands over her lap"),
                               ("night", "lying face up on a dark wooden tea cabinet shelf")]):
    line = 119 + n if n < 6 else 126
    S.append(P("hagaki_back_%d" % n, line, "The back of one old yellowed Japanese postcard, " + ang + ", the card "
               "filling the middle of the frame. The back of the card is completely blank and clean, with no "
               "printing and no handwriting at all. " + NOTXT,
               "the light moves very slightly across the card.", "a daughter kneeling on the tatami",
               "seated height, looking down", lt, WNOW))
S += [
 P("drawer_hagaki_stack", 127, "Six old postcards fanned out in a curve on a folded cardigan in front of the open "
   "tea cabinet drawer, afternoon light through a paper screen. " + BLANK + " " + NOTXT,
   "the light shifts very slightly across the cards.", TATAMI, "seated height, looking down", "interior", WNOW),
 P("mother_young_letter", 128, "In the small tatami room of the wooden apartment, the young mother — " + FACE["haha"]
   + ", in a cardigan — sits alone by the window holding one plain postcard turned over in her hand, seen in "
   "three-quarter view. " + BLANK, "she presses her lips together to hold it in, and it escapes as a small smile; "
   "she looks down at the card.", TATAMI, "seated height on the tatami", "interior", W67),
 P("old_father_wallet", 130, "In the quiet tatami room today, the father — " + FACE["chichi80"] + ", in a grey "
   "cardigan — sits at the low table holding a very old worn brown leather wallet open in both hands; beside him "
   "his daughter in her fifties, seen from behind and out of focus.", "the old man slowly slides two fingers into "
   "the back of the wallet. " + HOLD_CLAUSE, "the daughter kneeling beside him", "seated height on the tatami",
   "interior", WNOW, clip=True),
 P("worn_hagaki", 131, "Close on an old man's wrinkled hands holding one old postcard, soft at the edges, its corners "
   "rounded and worn white, above an open worn leather wallet. " + BLANK, "the hands turn the card slowly towards "
   "the window light. " + HOLD_CLAUSE, "the daughter kneeling beside him", "just above his hands", "interior",
   WNOW),
 P("bandai_lady_old", 137, "The same old public bathhouse at closing time, the attendant — " + FACE["bandai"] + " — "
   "seen from the side in her raised wooden booth, holding the long noren curtain aside with one hand and looking "
   "out into the dark street, the lamp over the door still on.", "she holds the curtain aside and waits, looking "
   "down the street.", "a late customer coming along the street", "standing eye height", "night", W67),
]

S += [
 # --- v3 hook B+ (2026-09-27): dem to thiep thu 6 — me lan dau cai lai cha (user: "tranh luan / dong cam")
 # 🔴 lan 1 bi Flow chan "vi pham chinh sach" (2026-09-27): me "angry" + nguoi dan ong quay lung + EM BE trong khung
 #    + "sharp breath" + "genuinely dark" = doc thanh xung dot gia dinh. Ban 2: BUON LANG, khong em be, anh sang am.
 P("mother_argue", 4, "Late winter afternoon in a small six-mat tatami room of an old wooden apartment, low warm "
   "sun coming through the one window. A young married couple sit on the tatami on either side of a low round wooden table "
   "with two cups of tea. The young mother — " + FACE["haha"] + ", in a faded cardigan over a plain skirt — sits "
   "upright with her hands folded in her lap, looking down at one plain postcard lying on the table, her face "
   "quiet, tired and sad, seen in three-quarter view. Across the table the young father — " + FACE["chichi"] + ", "
   "in a work jacket — sits with his head lowered, looking at the same postcard. " + BLANK,
   "she slowly slides the postcard across the table towards him with two fingers and then turns her face to the "
   "window; he looks at the card and lowers his head a little further. " + HOLD_CLAUSE,
   "a relative sitting at the side of the small room", "seated height on the tatami", "interior", W67),   # clip=False: Animate bi chan "vi pham chinh sach" 3 lan (2026-09-27)
 P("father_goes_out", 5, "The narrow wooden entrance of the old apartment at night: the young father — "
   + FACE["chichi"] + ", in a work jacket — seen from behind and a little to the side, is sliding open the rattling "
   "glass-and-wood front door onto the cold dark lane, one hand on the door, the other holding a plain postcard. "
   "Behind him, out of focus in the lit room, the young mother kneels with her head bowed. " + BLANK,
   "the father slides the door open slowly and steps out into the dark without looking back.",
   "the wife kneeling inside the room", "seated height on the tatami", "night", W67),
]

S += [
 # clip user gen tu prompt NGAN (ban REALISM bi Flow chan): vo chong ngoi ban tra ban ngay, me day tam thiep sang cha
 P("couple_table", 55, "A warm, quiet photograph of a small Japanese tatami room in the late nineteen-sixties, late winter afternoon, "
   "soft sunlight through a wooden window. A young Japanese woman in a beige cardigan and a young Japanese man in a "
   "work jacket sit on the tatami on either side of a low round wooden table with two cups of green tea. One plain "
   "blank postcard lies on the table between them.",
   "the woman slowly slides the postcard across the table towards the man, then gently turns her head towards the window.",
   "a relative sitting at the side of the room", "seated height on the tatami", "interior", W67, clip=True),
]

DROPPED = {"drawer_empty", "hagaki_turn"}   # co prompt, anh da gen, nhung da thay bang anh THAT (hook 30s, user 2026-09-27)
EXTRA_OK = {"mother_tub_still", "danchi_bath_b", "hanko_form_b", "hagaki_drawer_b"}   # anh du cua user (ingest_ai_20.EXTRA), khong co prompt rieng

def main():
    stills, vstills, motions, rows, vrows, si, md, bad = [], [], [], [], [], 0, ["# realism20 — o AI video 20 (ban nguoi doc)\n"], 0
    keys = [s["key"] for s in S]
    assert len(keys) == len(set(keys)), "trung key"
    need = sorted({c[3:].replace("+NUM", "") for _, cs in plan_20.PLAN_T for c in cs if c.startswith("AI:")})
    miss = sorted(set(need) - set(keys) - EXTRA_OK); extra = sorted(set(keys) - set(need) - DROPPED)
    if miss or extra: print("🔴 lech plan_20 — thieu:", miss, "| thua:", extra); bad += 1
    mi = 0
    for i, sc in enumerate(S, 1):
        sc = dict(sc, still=sc["still"])
        st, mo, _ = build_pair(sc, sc["world"])
        for kind, p in (("still", st),) + ((("motion", mo),) if sc["clip"] else ()):
            pr = gate_prompt(kind, p, LIMIT_SHOWA)
            if pr: bad += 1; print(f"  🔴 {i:02d} {sc['key']} {kind}: {pr}")
        for k, m in gate_action(sc["act"]):
            if k != "③": bad += 1
            print(f"  {'⚠' if k == '③' else '🔴'} {i:02d} {sc['key']} action {k}: {m}")
        fn = "ai_%02d_%s" % (i, sc["key"])
        if sc["clip"]:
            # anh DE TAO VIDEO: file rieng, cung thu tu voi MOTION_FLOW (dong k anh -> dong k motion)
            vstills.append(st); motions.append(mo); mi += 1
            vrows.append(f"{mi:02d}\t{fn}.png -> Animate -> {fn}.mp4\tTTS dong {sc['line']}\t{sc['key']}")
        else:
            stills.append(st); si += 1
            rows.append(f"{si:02d}\t{fn}.png\tTTS dong {sc['line']}\t{len(st)} ky")
        md += [f"## {i:02d} · {sc['key']} (TTS dong {sc['line']}){' · CLIP' if sc['clip'] else ''}\n",
               f"**STILL** ({len(st)} ky)\n\n{st}\n"] + ([f"**MOTION** ({len(mo)} ky)\n\n{mo}\n"] if sc["clip"] else [])
    W = lambda name, txt: io.open(OUT / name, "w", encoding="utf-8", newline="\n").write(txt)
    REDO = ("window_monohoshi", "father_nod")        # lo 1: Nano Banana ra anh GHEP O (2/54) — gen lai
    rs = [build_pair(dict(x), x["world"])[0] for x in S if x["key"] in REDO]
    NL, TAB = chr(10), chr(9)
    W("realism20_REDO1_STILL_FLOW.txt", NL.join(rs) + NL)
    W("realism20_REDO1_TENFILE.txt", "# gen lai lo 1 - ly do: anh ra GHEP NHIEU O (panel collage), cat 1 o chi con 300-880px" + NL
      + NL.join("%02d" % (k + 1) + TAB + "ai_%02d_%s.png" % ([y["key"] for y in S].index(key) + 1, key) + TAB + "(thay the ban ghep o)"
                for k, key in enumerate(REDO)) + NL)
    W("realism20_STILL_FLOW.txt", "\n".join(stills) + "\n")
    W("realism20_VIDEO_STILL_FLOW.txt", "\n".join(vstills) + "\n")
    W("realism20_MOTION_FLOW.txt", "\n".join(motions) + "\n")
    W("realism20_TENFILE.txt",
      "# ===== A. ANH TINH — realism20_STILL_FLOW.txt (dong i -> ten file) =====\n"
      "# bo vao 06_VIDEO/20_sumai-okane/cells_in_ai/\n" + "\n".join(rows) + "\n\n"
      "# ===== B. ANH DE TAO VIDEO — realism20_VIDEO_STILL_FLOW.txt dong k + realism20_MOTION_FLOW.txt dong k =====\n"
      "# gen anh (Image) -> chon anh -> ⋮ Animate -> dan MOTION cung so dong -> tai .mp4\n"
      "# bo CA .png lan .mp4 vao cells_in_ai/ (khong gen duoc clip thi .png van dung lam anh tinh)\n"
      + "\n".join(vrows) + "\n")
    io.open(OUT / "realism20_BLOCKS.md", "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(f"{si} anh tinh · {mi} anh+motion de tao video -> {OUT}\\realism20_*  | gate do: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
