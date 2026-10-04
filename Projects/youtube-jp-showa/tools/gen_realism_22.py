# -*- coding: utf-8 -*-
"""gen_realism_22.py — o AI video 22 (kieta-shigoto), CONG THUC REALISM, khuon v08. ~69% hinh THAT (plan_22.py);
AI chi lap canh co NGUOI trong truyen + VAT hu cau (給料袋 chua boc). Chu/so KHONG giao AI (font o make_cells). Tran 10 clip.
"""
import io, sys
from pathlib import Path
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
sys.path.insert(0, str(Path(__file__).parent))
_argv = sys.argv; sys.argv = [sys.argv[0]]
import plan_22
sys.argv = _argv
from gen_prompts_22 import C
from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
OUT = ROOT / "06_VIDEO" / "22_kieta-shigoto"

W64 = ("Setting: a Japanese provincial town in the mid-nineteen-sixties, the real Showa era — a small round-nosed bonnet bus "
       "in cream and red, wooden shop fronts, unpaved side streets, electric poles — period-correct, nothing modern and "
       "nothing futuristic.")
W60H = ("Setting: a Japanese National Railways level crossing beside farmland in the early nineteen-sixties, the real Showa "
        "era — a tiny wooden keeper's hut the size of one tatami mat, a hand-cranked striped barrier, a small bell on a post, "
        "a coal stove inside — period-correct, nothing modern.")
W60M = ("Setting: a coal-mining town in Kyushu in the early nineteen-sixties, the real Showa era — long wooden row houses "
        "for miners, a steel headframe tower on the hill, a black slag heap, dirt lanes — period-correct, nothing modern.")
W69 = ("Setting: a Japanese telephone office in the late nineteen-sixties, the real Showa era — long manual switchboards "
       "with rows of small jacks and lamps, women operators on tall wooden chairs, fluorescent ceiling lights — "
       "period-correct, nothing modern.")
W79 = ("Setting: a small Japanese company office at the end of the nineteen-seventies, the real Showa era — steel desks, "
       "a large Japanese typewriter with a flat tray of metal type, filing cabinets, a wall clock — period-correct, "
       "nothing modern.")
W72 = ("Setting: the same level crossing in the spring of the early nineteen-seventies, the real Showa era, at night — the "
       "keeper's wooden hut, the barrier now fitted with an electric motor box, a red warning lamp — period-correct.")
WNOW = ("Setting: a quiet Japanese town today — an ordinary modern route bus with no conductor, soft seats, a red stop "
        "button on the pole — calm and ordinary, no screens with readable text.")
WTOKYO = ("Setting: a Tokyo street at night in the late nineteen-sixties, the real Showa era, a public telephone on a shop "
          "front, period-correct, nothing modern.")
WAPT = ("Setting: a small Tokyo apartment at night at the end of the nineteen-seventies, the real Showa era, tatami and a "
        "paper lamp, period-correct.")
NOTXT = "The upper-left quarter of the frame is calm and empty of important detail."
BLANK = "Every envelope, paper, card and sign is completely blank, with no printing, no handwriting and no numbers on it."
ENV = "an old brown paper pay envelope, small and slightly yellowed, still sealed, with no printing and no writing on it"


def P(key, line, still, act, where, height, light, world, cam="locked", alive="", clip=False):
    return dict(key=key, line=line, still=still, act=act, where=where, height=height, light=light,
                world=world, cam=cam, alive=alive, clip=clip)


H15, H19, H20, H23, H30, H77 = C["haha15"], C["haha19"], C["haha20"], C["haha23"], C["haha30"], C["haha77"]
SOFU, CHICHI = C["sofu"], C["chichi"]
BOY = ("a Japanese boy of fifteen with a square face, a wide flat-bridged nose, thick eyebrows that almost meet, deep-set "
       "eyes, short black hair cut very close at the sides, in a grey work shirt and a cloth cap")
S = [
 # ---------------- HOOK ----------------
 P("conductor_young", 2, H15 + " stands at the open rear door of a small cream-and-red bonnet bus on a town street in "
   "the early morning, one hand on the door rail, seen in three-quarter view, her face young and serious. " + NOTXT,
   "she steps up onto the bus step and turns her head towards the street.", "someone waiting at the bus stop",
   "standing eye height", "day", W64),
 P("bag_coins", 3, "Close on a black leather conductor's coin bag hanging at the hip of a young girl in a navy uniform, "
   "heavy and bulging, its brass clasp half open, small silver and copper coins visible inside. " + NOTXT,
   "the bag sways a little as the bus moves.", "a passenger seated beside the door", "seated height", "interior", W64),
 P("envelope_father", 4, H15 + " kneels on the tatami of a small dim house at night and holds out " + ENV + " with both "
   "hands to her father, a thin Japanese man in his fifties seen only from behind, his shoulders and grey cropped head. "
   + BLANK + " " + NOTXT,
   "she holds the envelope out with both hands and bows her head; his hand reaches out and takes it. " + HOLD_CLAUSE,
   "someone kneeling at the side of the room", "seated height on the tatami", "night", W64, clip=True),
 P("haha77_bus", 6, H77 + " sits by the window of a modern quiet route bus, seen in profile, her hands resting on the "
   "handbag in her lap, looking out of the window. " + NOTXT,
   "her lips move very slightly as if saying two words to herself, and she keeps looking out of the window.",
   "her son sitting in the seat beside her", "seated height", "day", WNOW, clip=True),
 P("envelope_drawer", 8, "A small wooden desk drawer slightly open in a dark hut at night, and inside it, only half "
   "visible in the shadow, " + ENV + ". " + BLANK + " " + NOTXT,
   "the lamplight moves very slightly across the drawer.", "someone standing at the desk", "just above the desk",
   "night", W60H),
 # ---------------- 1 バスの車掌 ----------------
 P("depot_rollcall", 13, "A row of five young Japanese women bus conductors in navy uniforms and small caps stand in a "
   "line in front of a wooden bus depot at dawn, coin bags across their chests; in the middle stands " + H15 + ". "
   "A middle-aged male supervisor in a dark coat faces them, seen from behind. " + NOTXT,
   "the girls stand still and straighten their caps; the supervisor walks slowly along the line.",
   "someone standing at the depot gate", "standing eye height", "dusk", W64),
 P("conductor_lean", 16, H15 + " leans half out of the open rear door of a moving bonnet bus, one hand gripping the door "
   "rail, calling out towards the street with her mouth open, the wind in her short hair. " + NOTXT,
   "she leans out from the door and raises her free hand high as the bus pulls away from the stop. " + HOLD_CLAUSE,
   "a passenger standing inside the bus behind her", "standing eye height", "day", W64, clip=True),
 P("fingers_cracked", 18, "Close on the bare hands of a young girl in a navy uniform sleeve on a winter morning, the "
   "fingertips red and cracked from the cold, sorting small coins from an open coin bag in her palm. " + NOTXT,
   "her fingers pick out one coin and then stop, stiff with cold.", "a passenger seated across from her",
   "seated height", "interior", W64),
 P("count_sales", 19, H15 + " sits alone at a small wooden table in the bus depot office at night under one bare bulb, "
   "counting little stacks of coins and a few small banknotes laid out in rows, her small purse open beside them. "
   + BLANK + " " + NOTXT,
   "she counts one stack again with her fingertip, then opens her own small purse.", "someone at the office doorway",
   "seated height", "night", W64),
 P("conductor_last_day", 32, H19 + " stands alone at the rear door of the bonnet bus at dusk, holding her small navy cap "
   "in both hands, looking down at it. " + NOTXT,
   "she turns the cap slowly in her hands and does not put it on.", "someone on the pavement",
   "standing eye height", "dusk", W64),
 # ---------------- 2 踏切警手 ----------------
 P("sofu_keeper", 35, SOFU + " stands beside the tiny wooden keeper's hut at a rural level crossing, seen in three-quarter "
   "view, looking down the line. " + NOTXT,
   "he lifts his head and looks along the rails into the distance.", "someone standing across the road",
   "standing eye height", "day", W60H),
 P("sofu_handle", 37, SOFU + " turns the iron crank handle beside the keeper's hut with both hands, and the striped wooden "
   "barrier arm comes down across the dirt road. " + NOTXT,
   "he turns the crank steadily with both hands and the barrier arm lowers slowly to the ground. " + HOLD_CLAUSE,
   "someone waiting on the road", "standing eye height", "day", W60H, clip=True),
 P("girl_bento_hut", 44, "A Japanese girl of about ten in a hand-knitted cardigan, with a heart-shaped face and a dimple "
   "in her right cheek, walks along the side of the railway at dusk carrying an aluminium lunch box wrapped in a cloth "
   "towards a small lit keeper's hut. " + NOTXT,
   "she walks steadily towards the hut holding the wrapped lunch box against her chest.", "someone at the hut door",
   "a child's eye height", "dusk", W60H),
 P("flag_ignored", 48, SOFU + " stands in the middle of the dirt road at the level crossing holding a signal flag out "
   "sideways, while a man on a bicycle in a cap rides past him onto the rails without slowing. " + NOTXT,
   "the cyclist pedals past him; the keeper turns his head to follow him.", "someone waiting by the hut",
   "standing eye height", "day", W60H),
 # ---------------- 3 炭鉱 ----------------
 P("miners_walk", 55, "A line of Japanese coal miners in helmets with lamps and dark work clothes walk in silence along "
   "a dirt lane between long wooden row houses in the early morning, a steel headframe tower on the hill behind them. "
   + NOTXT, "the men keep walking in a slow line towards the mine; nobody turns.", "a child at a row-house doorway",
   "standing eye height", "dusk", W60M, clip=True),
 P("miner_black_face", 56, "A Japanese coal miner just up from the shaft stands outside the pithead, his face and neck "
   "black with coal dust except around the eyes, his helmet lamp still on, seen in three-quarter view. " + NOTXT,
   "he lets out a long breath and wipes his forehead with the back of his wrist.", "another miner beside him",
   "standing eye height", "day", W60M),
 P("boy_sentan", 58, BOY + ", stands at a long sloping wooden chute in a dusty coal-sorting shed, picking stones out of "
   "the black coal sliding past. " + NOTXT,
   "he picks one grey stone out of the coal with both hands and tosses it into a basket beside him.",
   "an older worker beside him at the chute", "standing eye height", "interior", W60M),
 P("father_bus_morning", 71, CHICHI + " stands at a town bus stop at dawn, a cloth lunch bundle in one hand, as a "
   "cream-and-red bonnet bus pulls up. " + NOTXT,
   "he steps towards the bus as its door opens.", "someone waiting at the bus stop", "standing eye height", "dusk", W64),
 P("coins_ready_palm", 72, "Close on the open palm of a young working man, rough and lined with coal dust in the creases, "
   "holding exactly two small coins ready, held out towards the rear door of a bus. " + NOTXT,
   "the young conductor's hand comes in and takes the two coins from his palm.", "the conductor at the bus door",
   "standing eye height, close", "day", W64),
 P("conductor_smile", 73, H19 + " stands at the rear door of the bus in the morning, turning her face away to the side "
   "with a small held-in smile, one hand pressed to the coin bag. " + NOTXT,
   "the corner of her mouth goes up and she looks down at her coin bag to hide it.", "a passenger at the door",
   "standing eye height", "day", W64),
 # ---------------- 4 電話交換手 ----------------
 P("haha_switchboard", 77, H20 + " sits on a tall wooden chair at a long manual switchboard, seen in three-quarter view "
   "from behind her shoulder, among a row of other women operators. " + BLANK + " " + NOTXT,
   "she lifts one cord with a plug from the shelf and reaches up towards the board. " + HOLD_CLAUSE,
   "the operator sitting next to her", "seated height", "interior", W69, clip=True),
 P("headset_on", 78, H20 + " at the switchboard settles a thin black headset with a small mouthpiece over her pinned "
   "hair, seen in profile. " + NOTXT, "she presses the earpiece gently against her ear with one finger.",
   "the operator sitting next to her", "seated height", "interior", W69),
 P("plug_in", 80, "Close on a section of a manual telephone switchboard: rows of small round jacks and tiny lamps, one "
   "lamp glowing amber, and the hand of a young woman operator in a grey cardigan sleeve guiding a corded plug towards "
   "it. " + BLANK + " " + NOTXT,
   "her hand pushes the plug into the jack beside the glowing lamp, and the lamp goes out. " + HOLD_CLAUSE,
   "the operator herself", "seated height, close", "interior", W69, clip=True),
 P("operators_row", 81, "A long row of young Japanese women operators seen from behind on tall wooden chairs at a "
   "manual switchboard stretching away down a long room, each wearing a thin headset. " + BLANK + " " + NOTXT,
   "their hands move slowly across the board, plugging and unplugging cords.", "a supervisor at the end of the room",
   "standing eye height", "interior", W69),
 P("dekasegi_phone", 85, "A young Japanese labourer in a work jacket stands at a public telephone at night in a Tokyo "
   "street, the receiver to his ear, a small stack of coins on the shelf in front of him, seen from the side. " + NOTXT,
   "he lowers his head and presses the receiver closer to his ear.", "someone waiting behind him",
   "standing eye height", "night", WTOKYO),
 P("haha_listen", 87, "A close shot of " + H20 + " at the switchboard at night, her eyes lowered, one hand resting on the "
   "earpiece of her headset, listening. " + NOTXT,
   "she stays very still; her eyes soften and she lowers them.", "the operator sitting next to her",
   "seated height, close", "night", W69),
 P("operators_reassigned", 94, "A small group of Japanese women operators in cardigans stand in a bare office corridor, "
   "holding their folded headsets in their hands, listening to a man in a suit seen from behind. " + BLANK + " " + NOTXT,
   "the women stand and listen; one of them looks down at the headset in her hands.", "someone at the corridor door",
   "standing eye height", "interior", W69),
 P("headset_stain", 96, "Close on a thin black operator's headset lying on a wooden switchboard shelf, its cushioned "
   "earpiece worn and darkened in a ring. " + NOTXT, "the light from the window moves very slightly across it.",
   "someone standing at the switchboard", "just above the shelf", "interior", W69),
 # ---------------- 5 タイピスト ----------------
 P("haha_typist", 99, H30 + " sits at a large Japanese typewriter on a steel desk in a small office, one hand on the "
   "lever, her eyes searching the flat tray of metal type in front of her. " + BLANK + " " + NOTXT,
   "her eyes move across the tray, find one place, and she presses the lever down. " + HOLD_CLAUSE,
   "a colleague at the next desk", "seated height", "interior", W79),
 P("haha_rub_arm", 103, H30 + " sits at the edge of a futon in a small dim room at night beside a sleeping small child, "
   "slowly rubbing her own right forearm and shoulder with her left hand. " + NOTXT,
   "she rubs her forearm slowly, rolls her shoulder once and winces.", "someone at the sliding door",
   "seated height on the tatami", "night", WAPT),
 P("wordpro_desk", 107, "A large beige office machine the size of a desk with a built-in screen and a wide keyboard "
   "stands alone in a bright corner of an office at the end of the nineteen-seventies, no logo, no name and no writing "
   "on it, the screen dark. " + NOTXT, "the light from the window moves very slightly across it.",
   "someone standing in the office", "standing eye height", "interior", W79),
 P("wordpro_price", 108, "An empty steel office desk at dusk with a closed Japanese typewriter under a grey dust cover, "
   "and beside it the edge of a large new beige office machine, no logo and no writing anywhere. " + NOTXT,
   "the dusk light fades very slightly.", "someone standing in the office", "standing eye height", "dusk", W79),
 P("haha_wordpro", 110, H30 + " sits at a beige keyboard in front of a small screen, seen from behind her shoulder, her "
   "fingers on the keys. The screen shows only soft light, no characters. " + NOTXT,
   "her fingers move slowly across the keys.", "a colleague standing behind her", "seated height", "interior", W79),
 # ---------------- KET ----------------
 P("envelope_drawer2", 112, "A small wooden desk inside a keeper's hut at night, its drawer closed with a small brass "
   "lock, a coal stove glowing beside it. " + NOTXT, "the stove glow flickers very slightly.",
   "someone standing at the desk", "standing eye height", "night", W72),
 P("electric_barrier", 114, "A level-crossing barrier at night, newly fitted with a grey electric motor box at its base "
   "and a red warning lamp, the keeper's small wooden hut lit behind it. " + BLANK + " " + NOTXT,
   "the red lamp blinks slowly.", "someone standing across the road", "standing eye height", "night", W72),
 P("haha_bento_night", 115, H23 + " walks along the railway at night carrying a lunch box wrapped in a cloth towards the "
   "small lit keeper's hut. " + NOTXT, "she walks steadily towards the lit hut.", "someone at the hut door",
   "standing eye height", "night", W72),
 P("envelope_reveal", 117, SOFU + " sits at the small desk in the keeper's hut at night and holds out " + ENV + " in both "
   "hands across the desk. " + BLANK + " " + NOTXT,
   "he lifts the envelope out of the open drawer with both hands and holds it out across the desk. " + HOLD_CLAUSE,
   "his daughter standing at the hut door", "seated height", "night", W72, clip=True),
 P("envelope_sealed", 118, "Close on " + ENV + ", lying in two weathered hands under the glow of a coal stove, its flap "
   "still glued shut. " + BLANK + " " + NOTXT, "the hands hold the envelope still; the glow flickers.",
   "the daughter standing at the desk", "just above the hands", "night", W72),
 P("sofu_hand_over", 119, "Inside the keeper's hut at night, " + SOFU + " puts " + ENV + " into the hands of " + H23 +
   ", seen from the side, both of them looking down at it. " + BLANK + " " + NOTXT,
   "he lays the envelope in her hands and closes her fingers over it with his own. " + HOLD_CLAUSE,
   "someone at the hut door", "standing eye height", "night", W72, clip=True),
 P("barrier_auto_night", 122, "The level crossing at night seen through the small window of the keeper's hut: the striped "
   "barrier arm lowering by itself, the red lamp blinking, no one at the crank. " + NOTXT,
   "the barrier arm comes down slowly by itself and the red lamp blinks.", "someone inside the hut at the window",
   "standing eye height", "night", W72),
 P("haha_cry_hut", 123, "A close shot of " + H23 + " inside the keeper's hut at night, the sealed envelope held against "
   "her chest, her face crumpling into tears, her father beside her seen only as a dark shoulder. " + NOTXT,
   "her chin trembles, her eyes close, and she bends her head down over the envelope and cries. " + HOLD_CLAUSE,
   "her father standing beside her", "standing eye height, close", "night", W72, clip=True),
 P("haha77_bus2", 126, H77 + " sits by the window of the quiet modern bus, seen from the seat beside her, smiling a "
   "little at the window. " + NOTXT, "she breathes out and smiles to herself.", "her son sitting beside her",
   "seated height", "day", WNOW),
 P("envelope_bag", 128, "Close on a small black handbag on the lap of an old woman in a dove-grey cardigan on a bus, its "
   "clasp open, and the corner of an old yellowed brown paper envelope showing inside. " + BLANK + " " + NOTXT,
   "her hand lifts the envelope a little out of the bag.", "her son sitting beside her", "seated height, close", "day", WNOW),
 P("haha77_smile", 129, "A close shot of " + H77 + " on the bus, turning her face towards her son with a bright, "
   "mischievous smile, the deep dimple showing in her right cheek. " + NOTXT,
   "her eyes crease and she gives one small nod.", "her son sitting beside her", "seated height, close", "day", WNOW),
 P("envelope_old_hands", 134, "Close on two old wrinkled hands holding an old yellowed brown paper pay envelope, still "
   "sealed, against a soft dove-grey cardigan, warm window light. " + BLANK + " " + NOTXT,
   "the hands hold the envelope still; the thumb moves once along its edge.", "her son sitting beside her",
   "seated height, close", "day", WNOW),
]

DROPPED = set()

def main():
    stills, vstills, motions, rows, vrows, si, md, bad = [], [], [], [], [], 0, ["# realism22 — o AI video 22 (ban nguoi doc)\n"], 0
    keys = [s["key"] for s in S]
    assert len(keys) == len(set(keys)), "trung key"
    need = sorted({c[3:].replace("+NUM", "") for _, cs in plan_22.PLAN_T for c in cs if c.startswith("AI:")})
    miss = sorted(set(need) - set(keys)); extra = sorted(set(keys) - set(need) - DROPPED)
    if miss or extra: print("🔴 lech plan_22 — thieu:", miss, "| thua:", extra); bad += 1
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
    W("realism22_STILL_FLOW.txt", "\n".join(stills) + "\n")
    W("realism22_VIDEO_STILL_FLOW.txt", "\n".join(vstills) + "\n")
    W("realism22_MOTION_FLOW.txt", "\n".join(motions) + "\n")
    W("realism22_TENFILE.txt",
      "# ===== A. ANH TINH — realism22_STILL_FLOW.txt (dong i -> ten file) =====\n"
      "# bo vao 06_VIDEO/22_kieta-shigoto/cells_in_ai/\n" + "\n".join(rows) + "\n\n"
      "# ===== B. ANH DE TAO VIDEO — realism22_VIDEO_STILL_FLOW.txt dong k + realism22_MOTION_FLOW.txt dong k =====\n"
      "# gen anh (Image) -> chon anh -> ⋮ Animate -> dan MOTION cung so dong -> tai .mp4\n"
      "# bo CA .png lan .mp4 vao cells_in_ai/ (khong gen duoc clip thi .png van dung lam anh tinh)\n"
      + "\n".join(vrows) + "\n")
    io.open(OUT / "realism22_BLOCKS.md", "w", encoding="utf-8", newline="\n").write("\n".join(md))
    print(f"{si} anh tinh · {mi} anh+motion de tao video -> {OUT}\\realism22_*  | gate do: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
