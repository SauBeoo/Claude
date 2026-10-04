# -*- coding: utf-8 -*-
"""Sinh bo prompt CHUYEN DONG (image-to-video) cho 74 anh photocard cua video 19.

Xuat 3 file vao 06_VIDEO/19_kounenrei-koyou-keizoku-kyufu/:
  motion_prompts_19_FLOW.txt      1 prompt / 1 DONG  (import thang vao extension)
  motion_prompts_19_BLOCKS.md     ban nguoi doc: theo scene, thay duoc chuoi lien mach
  motion_prompts_19_TENFILE.txt   dong FLOW <-> anh nguon <-> ten clip output

LUAT AP:
  - Thu tu dong = thu tu THOI GIAN trong video (theo _scenes19.py), KHONG theo
    thu tu file art_prompts goc. Vi "lien mach" chi doc duoc khi xep theo timeline.
  - MOTION dat trong ~15% DAU prompt (bai hoc ab-3title-3thumb.md 3.1 Buoc 3:
    model bam khoi den truoc; de motion o cuoi thi no bam ta canh roi bo qua).
  - CAMERA LOCKED mac dinh (user ghet Ken Burns/rung —
    memory feedback_video_no_motion_mot_giong). Chi 3 scene PEAK duoc micro
    push-in 3%: 84man / futari-callback / modoranai.
  - Chuyen dong = NOI TAI canh + anh sang + giay, khong phai pan anh tinh.
"""
import io, os, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")

# ── khoi duoi CO DINH: giu chat giay + chan moi thu model hay tu them ─────────
TAIL = ("PAPER LOCK: every element stays a flat printed paper cut-out — torn and "
        "scissor-cut edges, halftone print dots, newsprint grain and slight ink "
        "misregistration all stay visible and breathe subtly frame to frame; soft "
        "paper drop-shadows shift only with the motion above. Handmade stop-motion "
        "feel with a slight stagger on figures, NOT smooth CGI, NOT 3D. Motion "
        "strength LOW. DO NOT re-render faces, add depth or perspective, morph "
        "shapes, change the palette, introduce new objects, or add any text, "
        "letters, numbers, logos or watermark anywhere. Calm editorial pacing, "
        "seamless 4-6 second loop.")

CAM_LOCK = "CAMERA — locked off: no pan, no zoom, no shake, no parallax drift."
CAM_PEAK = ("CAMERA — locked off except a barely perceptible push-in of about 3% "
            "over the whole clip; no pan, no shake.")

# ── BANG MOTION theo SCENE (thu tu = timeline). peak=True -> CAM_PEAK ────────
# moi tuple: (ten_anh, motion)
SCENES = [
 ("L=0  0:00  hataraku / con di lam", False, [
  ("card_19_hataraku",
   "MOTION — the man's hand slides slowly along the row of boxes on the shelf and "
   "stops; his head tilts a few degrees to follow it; the clipboard under his arm "
   "settles by a millimetre; daylight from the high window pulses very softly."),
  ("card_19_hataraku_b",
   "MOTION — continuing the same rightward push: the cardboard box is eased a few "
   "centimetres further onto the shelf and stops; the gloved fingertips tighten "
   "their grip; a faint dust shimmer drifts through the window light."),
 ]),
 ("L=2  0:12  kyuryo_meisai / phieu luong", False, [
  ("card_19_kyuryo_meisai",
   "MOTION — the hands adjust the payslip sheet by a few millimetres; the paper's "
   "free edge flutters faintly; warm morning light shifts slowly across the table "
   "as if a curtain moved, catching the halftone dots."),
  ("card_19_kyuryo_meisai_b",
   "MOTION — same morning light keeps creeping in the same direction, now sliding "
   "across the coffee ring stain; the loose corner of the payslip lifts a little "
   "and settles; the folded glasses stay perfectly still."),
 ]),
 ("L=6  0:39  hataraku_c + hatena / doi tuong la ai", False, [
  ("card_19_hataraku_c",
   "MOTION — the hand pushes the blank time card fully into the wall clock slot "
   "and holds; the machine gives one small mechanical jolt; the card stops flush."),
  ("card_19_hatena",
   "MOTION — the seated man's gaze travels from the left envelope to the right one "
   "and stops in the middle; his fingertip taps his cheek twice, slowly; the desk "
   "lamp's pool of light wavers once."),
 ]),
 ("L=7  0:46  hatena / ba cau hoi", False, [
  ("card_19_hatena_b",
   "MOTION — the three fanned envelopes shift a millimetre apart; their top edges "
   "flutter faintly; the lamp light nudges sideways so the paper shadows rotate "
   "very slowly beneath them."),
  ("card_19_hatena_c",
   "MOTION — the envelope is turned over one beat in his hands to show its back; "
   "he blinks once and his frown deepens slightly; the side lamp light stays fixed."),
 ]),
 ("L=9  1:04  kenkyu / luong huu cung dung", False, [
  ("card_19_kenkyu",
   "MOTION — the small brass clock's second hand ticks forward in single steps; the "
   "top leaflet's corner lifts and settles; the fountain pen and magnifier stay "
   "absolutely still; even flat light."),
 ]),
 ("L=11 1:18  kenkyu_b / phong nghien cuu", False, [
  ("card_19_kenkyu_b",
   "MOTION — the magnifying glass rocks by one or two pixels so the paper grain "
   "seen through the lens slides with it; the bright halo on the lens edge creeps "
   "across; the linen underneath does not move."),
 ]),
 ("L=12 1:26  koyou_hoken / bu phan bi giam", False, [
  ("card_19_koyou_hoken",
   "MOTION — the uniformed hand lowers the last two banknotes onto the stack, "
   "releases them and withdraws out of frame; the stack settles by a hair; the "
   "older palm underneath stays open and steady."),
  ("card_19_koyou_hoken_b",
   "MOTION — same 'placing down' action seen closer, as if the cut had zoomed in "
   "mid-gesture: the top note touches down and stops, the small stack compresses "
   "slightly, the fingers beneath curl in a fraction."),
 ]),
 ("L=18 2:03  75percent / duoi bay lam phan tram", False, [
  ("card_19_75percent",
   "MOTION — the taut red thread vibrates like a plucked string and slowly damps "
   "to stillness; the coin stack and the measuring stick do not move at all."),
  ("card_19_75percent_b",
   "MOTION — the same vibration finishes damping out on the thread in sharp focus, "
   "while the blurred stick markings behind it sway gently in the bokeh."),
 ]),
 ("L=21 2:46  matsumoto / mo ngan keo", False, [
  ("card_19_matsumoto",
   "MOTION — the drawer slides open a few more centimetres and stops; his eyes "
   "lower to the lapel pin inside; his shoulders drop one small notch."),
  ("card_19_matsumoto_b",
   "MOTION — the open palm tilts a few degrees so the warm lamp light sweeps across "
   "the plain enamel face of the pin; the fingers close in very slightly around it."),
  ("card_19_matsumoto_c",
   "MOTION — closing the sequence: the drawer is pushed shut in one slow, quiet "
   "motion until it seats; he keeps looking down; the table lamp behind him is "
   "steady."),
 ]),
 ("L=26 3:21  jougen / cai tran chan lai", False, [
  ("card_19_jougen",
   "MOTION — the wooden ruler presses down one notch onto the tall coin stack; the "
   "stack compresses; a single coin at the rim trembles and holds."),
  ("card_19_jougen_b",
   "MOTION — continuing the same downward press, seen extremely close: the ruler "
   "bites further into the top coin, the coins under it shift a fraction, the wood "
   "grain digs in."),
  ("card_19_jougen_c",
   "MOTION — the consequence: the last loose coin rolls slowly across the desk and "
   "topples flat; the capped stack behind it stays motionless in the bokeh."),
  ("card_19_jougen_d",
   "MOTION — the hand lowers the single coin until it meets the ruler, stops dead "
   "and stays there, unable to place it; the fingers hold the coin suspended; "
   "nothing else moves."),
 ]),
 ("L=33 4:29  28000 / hai man tam", False, [
  ("card_19_28000",
   "MOTION — he raises the passbook slightly closer to his eyes; the corner of his "
   "mouth lifts a little further into relief; steam drifts up from the tea cup."),
  ("card_19_28000_b",
   "MOTION — the fingertip glides to the right along the blank ruled entry line and "
   "stops at its end; the warm window light grows fractionally brighter on the page."),
  ("card_19_28000_c",
   "MOTION — seen from above, the tea steam curls upward and folds over; the warm "
   "afternoon light creeps slowly across the wooden table; passbook and glasses "
   "stay still."),
 ]),
 ("L=36 4:59  hondai / vao van de chinh", False, [
  ("card_19_hondai",
   "MOTION — the turned-up corner of the leaflet lifts and settles back; the desk "
   "lamp sways a hair so the pen's shadow sweeps across the page; the dark room "
   "stays dark."),
  ("card_19_hondai_b",
   "MOTION — the same corner keeps creeping upward while the narrow beam of lamp "
   "light contracts, letting the rest of the page sink deeper into shadow."),
 ]),
 ("L=42 5:47  84man / TAM MUOI BON MAN — PEAK", True, [
  ("card_19_84man",
   "MOTION — the ragged torn edge of the banknote stack bristles with loose paper "
   "fibres; the whole stack settles one notch as if the tearing has only just "
   "stopped; the hard single-source light does not move."),
  ("card_19_84man_b",
   "MOTION — the torn-away portion lying apart flutters faintly and drifts a "
   "further pixel or two away, so the empty gap between the two pieces reads wider; "
   "the remaining stack is dead still."),
 ]),
 ("L=44 6:07  tanjoubi / ranh gioi la ngay sinh", False, [
  ("card_19_tanjoubi",
   "MOTION — the red circle is completed on its last stroke and the marker tip "
   "lifts clear of the paper; the calendar page flutters once against the wall."),
  ("card_19_tanjoubi_b",
   "MOTION — extremely close: the red ink reads as still wet and bleeds a hair "
   "further into the paper fibres; the surrounding blank squares do not move."),
  ("card_19_tanjoubi_c",
   "MOTION — the unmarked right-hand page lifts its edge as if waiting to be marked "
   "too, then settles; the circled left page stays flat and still."),
  ("card_19_tanjoubi_d",
   "MOTION — closing the beat: the uncapped red marker rolls two or three pixels "
   "and stops against the calendar; the cap resting apart never moves; quiet "
   "aftermath stillness."),
 ]),
 ("L=52 7:18  wariai / ti le kho hon", False, [
  ("card_19_wariai",
   "MOTION — the two pans of the brass balance swing slowly and damp down into "
   "their tilted resting position; the pointer settles off-centre and stops."),
 ]),
 ("L=53 7:26  douryou / nguoi dong nghiep", False, [
  ("card_19_douryou",
   "MOTION — he lowers the payslip a little; the wry smile tightens further; the "
   "vending machine behind him pulses once in the blur."),
  ("card_19_douryou_b",
   "MOTION — the gripping fingers squeeze harder and the crease across the payslip "
   "spreads; the blurred break-room background stays still."),
  ("card_19_douryou_c",
   "MOTION — closing the beat: the folded sheet slides back into the brown envelope "
   "until it disappears; his shoulders drop; he keeps looking down."),
 ]),
 ("L=58 8:03  zero / khong mot yen", False, [
  ("card_19_zero",
   "MOTION — the open palm closes halfway and opens again — one empty beat — then "
   "holds; the empty envelope beside it does not move; the cold flat light is "
   "constant."),
  ("card_19_zero_b",
   "MOTION — the envelope's open flap lifts and falls back, showing nothing inside; "
   "the bare desk stays empty; the cold overhead light never changes."),
 ]),
 ("L=60 8:20  futari / HAI NGUOI O DAU BAI — PEAK CALLBACK", True, [
  ("card_19_futari",
   "MOTION — the uneasy man slowly turns his head toward the calm one; the calm man "
   "does not move at all; both keep holding their envelopes; the corridor is still."),
  ("card_19_futari_b",
   "MOTION — the tightly gripping pair of hands squeezes harder until the envelope "
   "creases; the other pair holds its envelope perfectly level and unchanged."),
  ("card_19_futari_c",
   "MOTION — the man ahead keeps walking away toward the door and blurs further out; "
   "the man who stopped to read stands completely still, so the gap between them "
   "opens wider."),
  ("card_19_futari_d",
   "MOTION — closing the callback: the folded work jacket sways almost "
   "imperceptibly between the two closed lockers; the fluorescent light flickers "
   "once; both doors stay shut."),
 ]),
 ("L=70 9:01  cta / loi moi giua video", False, [
  ("card_19_cta",
   "MOTION — the couple lean their heads a little toward each other and their smiles "
   "widen slightly; the warm living-room light is steady."),
  ("card_19_cta_b",
   "MOTION — a fingertip taps the blank pale tablet screen once and withdraws; the "
   "screen brightens very faintly — still completely blank, no icons and no text "
   "ever appear."),
  ("card_19_cta_c",
   "MOTION — green tea pours from the spout into the second cup in a steady thin "
   "stream and steam rises and curls; the low table stays still."),
  ("card_19_cta_d",
   "MOTION — the two keep looking at each other with knowing smiles; one of them "
   "blinks once; the face-down tablet and the warm lamp are motionless."),
 ]),
 ("L=71 9:29  madoguchi2 / cua so thu hai", False, [
  ("card_19_madoguchi2",
   "MOTION — the man standing between the counters turns his head from the left "
   "counter to the right one and settles facing straight ahead again; the two blank "
   "signs above do not move."),
  ("card_19_madoguchi2_b",
   "MOTION — almost entirely still: only the daylight creeps very slowly across the "
   "counter surface; the empty chair stays empty; the emptiness is the content."),
 ]),
 ("L=78 10:30 tadashi / cho o day phai chinh xac", False, [
  ("card_19_tadashi",
   "MOTION — the raised palm lifts a fraction higher into the 'wait a moment' "
   "gesture and holds there; his head tilts slightly; his expression stays calm."),
  ("card_19_tadashi_b",
   "MOTION — the same held gesture seen close: the fingers spread a little and stop; "
   "the palm's soft shadow on the pale background shifts with them."),
  ("card_19_tadashi_c",
   "MOTION — closing the beat: he pushes his reading glasses up the bridge of his "
   "nose with one hand and his eyes drop to the document; unhurried."),
 ]),
 ("L=81 11:00 kuriage / nhan som", False, [
  ("card_19_kuriage",
   "MOTION — the last few grains trickle out of the toppled hourglass's neck onto "
   "the desk and then stop; the spilled pile stays where it is; muted light."),
  ("card_19_kuriage_b",
   "MOTION — a few stray grains slide away from the small spilled pile and come to "
   "rest; the blurred hourglass base behind is motionless."),
  ("card_19_kuriage_c",
   "MOTION — the hourglass stands upright again and the sand runs steadily down "
   "through the neck, the upper level visibly dropping; the loose sand still on the "
   "desk never moves."),
 ]),
 ("L=85 11:36 nijuu / bi cat hai lan", False, [
  ("card_19_nijuu",
   "MOTION — one of the cut paper strips flutters and drifts a little further away "
   "from the sheet it came from; the scissors lie dead still."),
  ("card_19_nijuu_b",
   "MOTION — the open scissor blades close one beat and open again; the freshly cut "
   "strip beside them trembles from the movement of air."),
  ("card_19_nijuu_c",
   "MOTION — both parallel strips lift together and settle back, so the gap between "
   "them and the remaining sheet reads wider; even overhead light unchanged."),
 ]),
 ("L=90 12:05 modoranai / khong quay lai duoc — PEAK", True, [
  ("card_19_modoranai",
   "MOTION — the barred arm of the turnstile is pushed a few degrees, catches hard "
   "against its lock and refuses to give; the hand stays resting on it; nothing "
   "else moves."),
  ("card_19_modoranai_b",
   "MOTION — extremely close on the locking mechanism: it shifts a fraction and "
   "bites shut again; the cold metal is otherwise absolutely still."),
  ("card_19_modoranai_c",
   "MOTION — almost entirely still: the cold light down the far corridor pulses "
   "once; the out-of-focus gate in the foreground does not move; the corridor stays "
   "empty."),
 ]),
 ("L=95 12:50 meisai_check / xem phieu luong", False, [
  ("card_19_meisai_check",
   "MOTION — the fingertip traces slowly down the blank ruled column and stops; the "
   "magnifying glass is held steady above it, so the paper grain seen through the "
   "lens slides under the finger."),
  ("card_19_meisai_check_b",
   "MOTION — the hand withdraws fully out of frame and the magnifier stays put where "
   "it was set down; the warm kitchen light creeps a little across the payslip."),
 ]),
 ("L=97 13:04 4kagetsu / trong bon thang", False, [
  ("card_19_4kagetsu",
   "MOTION — the curling corner of the last calendar page lifts a little further and "
   "settles; the red marker resting on top does not move."),
  ("card_19_4kagetsu_b",
   "MOTION — the same corner keeps peeling slowly upward, just revealing the blank "
   "page beneath it; shallow focus holds."),
  ("card_19_4kagetsu_c",
   "MOTION — the hand tears the page further off the calendar and the half-detached "
   "sheet twists downward; the remaining pages stay flat against the wall."),
 ]),
 ("L=100 13:35 futatsu_mado / hai cua so", False, [
  ("card_19_futatsu_mado",
   "MOTION — his eyes move from the left document to the right one and back, then "
   "settle; both hands stay resting where they are; even daylight unchanged."),
  ("card_19_futatsu_mado_b",
   "MOTION — seen from above, both hands press down one beat — the right one half a "
   "beat later than the left — flattening the two sheets; then both hold still."),
 ]),
 ("L=112 14:20 chuui / luu y", False, [
  ("card_19_chuui",
   "MOTION — one blank leaflet on the counter-top stand flutters and settles; the "
   "counter, the chair and everything else stay completely still; nobody appears."),
  ("card_19_chuui_b",
   "MOTION — the outermost leaflet in the stand lifts and falls back; the rest of "
   "the pale blank leaflets do not move; soft neutral daylight is constant."),
  ("card_19_chuui_c",
   "MOTION — almost entirely still: only the soft daylight creeps slowly across the "
   "counter top; the single empty chair stays empty."),
 ]),
 ("L=113 14:28 yokoku / bao truoc so sau", False, [
  ("card_19_yokoku",
   "MOTION — her eyes travel down the notice sheet; her fingers adjust the paper a "
   "few millimetres; the evening lamp light is steady."),
  ("card_19_yokoku_b",
   "MOTION — the held notice sheet trembles faintly in both hands; the warm low lamp "
   "light does not change."),
  ("card_19_yokoku_c",
   "MOTION — steam drifts up from the teacup and thins out; the reading glasses and "
   "the folded notice stay exactly where they were set down; otherwise still."),
  ("card_19_yokoku_d",
   "MOTION — closing the video: her silhouette rises and falls with one slow breath; "
   "the floor lamp's warm pool of light wavers almost imperceptibly; dusk holds."),
 ]),
]

HEAD = ("Animate this still vintage-newsprint paper-collage image into a short "
        "seamless loop, keeping it unmistakably a hand-assembled paper collage. ")


def build():
    flow, ten, blocks = [], [], []
    blocks.append("# MOTION PROMPTS — video 19 `kounenrei-koyou-keizoku-kyufu`\n")
    blocks.append("> 74 prompt image-to-video, MOT prompt cho MOT anh photocard.\n"
                  "> Thu tu = **THOI GIAN trong video** (theo `tools/_scenes19.py`), "
                  "khong theo thu tu file `art_prompts_*` goc — vi tinh **lien mach** "
                  "chi doc duoc khi xep theo timeline.\n>\n"
                  "> **Cach doc:** moi khoi `L=` ben duoi la MOT SCENE. Cac anh trong "
                  "cung scene la mot CHUOI ke tiep nhau (mo -> ngam -> dong / ep -> "
                  "truot -> khong dat duoc), nen huong chuyen dong da duoc noi lien; "
                  "dung doi thu tu trong scene.\n>\n"
                  "> **CAMERA LOCKED** o 68/74 anh. Chi 3 scene PEAK "
                  "(`84man` · `futari` callback · `modoranai`) duoc micro push-in 3%.\n")
    blocks.append(
        "\n## 🔴 8 THE 原典 — KHONG CO trong bo nay, va DUNG animate\n\n"
        "`photocard/` co **82** anh nhung bo motion nay chi **74**. Tam anh con lai "
        "la the trich nguon, dung bang `tools/make_genten_19.py` (PIL + font Noto), "
        "**khong phai anh AI**:\n\n"
        "```\ncard_genten19_01 / _01_b / _01_c     (Hello Work)\n"
        "card_genten19_02 / _02_b            (Kourou-shou)\n"
        "card_genten19_03 / _03_b / _03_c     (Nenkin Kikou)\n```\n\n"
        "⛔ **Dua the chu vao image-to-video la mat chu**: model se morph/nhoe kanji, "
        "va the 原典 mat gia tri ngay khi khong doc duoc — trong khi day dung la thu "
        "duy nhat chung minh so lieu cua bai. Muon cho chung dong thi lam o tang "
        "DUNG CLIP (build-on tung dong, zoom-punch cua Remotion), khong qua AI video.\n")
    n = 0
    for title, peak, items in SCENES:
        blocks.append(f"\n## {title}" + ("  ⭐PEAK" if peak else ""))
        for name, motion in items:
            n += 1
            cam = CAM_PEAK if peak else CAM_LOCK
            p = f"{HEAD}{motion} {cam} {TAIL}"
            p = re.sub(r"\s+", " ", p).strip()
            flow.append(p)
            ten.append(f"{name+'.png':<32}<- dong {n} FLOW  -> clip_19_{name.replace('card_19_','')}.mp4")
            blocks.append(f"\n**[{n:02d}] `{name}.png`**\n\n```\n{p}\n```\n")
            blocks.append(f"*({len(p)} ky tu)*\n")
    io.open(os.path.join(VD, "motion_prompts_19_FLOW.txt"), "w",
            encoding="utf-8", newline="\n").write("\n".join(flow) + "\n")
    io.open(os.path.join(VD, "motion_prompts_19_TENFILE.txt"), "w",
            encoding="utf-8", newline="\n").write("\n".join(ten) + "\n")
    io.open(os.path.join(VD, "motion_prompts_19_BLOCKS.md"), "w",
            encoding="utf-8", newline="\n").write("\n".join(blocks) + "\n")
    ln = [len(x) for x in flow]
    print(f"OK {n} prompt | do dai {min(ln)}-{max(ln)} ky (tb {sum(ln)//len(ln)})")
    print("  motion_prompts_19_FLOW.txt / _BLOCKS.md / _TENFILE.txt ->", VD)
    return n


if __name__ == "__main__":
    got = build()
    assert got == 74, f"phai la 74 anh, dang co {got}"
