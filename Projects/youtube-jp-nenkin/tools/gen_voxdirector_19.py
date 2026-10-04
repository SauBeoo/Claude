# -*- coding: utf-8 -*-
"""Sinh project VOX-DIRECTOR cho video 19 -> E:\\vox-director\\out\\nenkin-19\\beats.json

Vi sao co file nay: bo prompt cua nenkin dang o dang `art_prompts_*_FLOW.txt`
(1 dong = 1 prompt anh) + `motion_prompts_*` roi rac. Vox-director thi lay
`beats.json` lam NGUON SU THAT DUY NHAT: mot file chua ca prompt ANH
(`scene` -> compose_collage_prompt) va prompt VIDEO (`camera_move` +
`element_motion` -> collage_prompt), roi moi stage doc tu do.

Chay xong thi dung chinh script cua vox-director de xuat prompt (khong ton API):
    cd /e/vox-director
    python scripts/print_prompts.py out/nenkin-19     # -> PROMPTS.md + prompts.txt
    python scripts/print_motion_19.py out/nenkin-19   # -> MOTION.md + motion.txt

MAP: scene cua `tools/_scenes19.py`  ->  BEAT
     tung anh trong `heroes=[...]`   ->  SHOT (a/b/c/d)

BA CHO CO Y LECH KHOI MAC DINH CUA VOX-DIRECTOR — doc truoc khi sua:
 1. `camera_move` = "static" o 60/74 shot. Vox-director khuyen "varied, never
    repeat"; user thi chot ghet Ken Burns (memory feedback_video_no_motion_mot_giong).
    Giai bang `parallax` cho shot wide — no la "cac lop giay troi lech toc do,
    camera VAN dung yen", nen van varied ma khong pan/zoom. Chi 3 scene PEAK
    (84man / futari callback / modoranai) dung `push_in`.
 2. `title: false` o 74/74 shot. Anh cua nenkin KHONG co chu nao (luat "All paper
    surfaces BLANK"), nen phai tat text_lock — de mac dinh True thi prompt di kem
    cau "Keep the HEADLINE TEXT sharp" = moi model tu sinh chu.
 3. `motion_style: "calm"` (vox-director default "punchy"). Tep 45+ —
    audience-45plus.md §2: nhip dung phai cham hon 20–30%.
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.dirname(HERE)                                    # youtube-jp-nenkin
VD19 = os.path.join(PRJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")
OUT = r"E:\vox-director\out\nenkin-19"

# ── idiom JP: override `collage_style`. Giu nguyen van khoi da GEN DUOC 74 anh ──
#    (them "mid-century JAPANESE" + "deep navy ink" — theme newsprint-editorial
#     goc cua vox-director khong co ca hai)
COLLAGE_STYLE = (
    "Vintage newsprint editorial paper collage in the style of a mid-century "
    "JAPANESE front-page news feature: bold cut-out photographs and illustrations "
    "laid over an aged broadsheet newspaper page, heavy halftone print dots, aged "
    "newsprint texture with slight ink misregistration, tactile editorial calm — "
    "reads like a newspaper feature spread brought to life, not an advertisement."
)

# ── guard JP: 3 rang buoc cua nenkin KHONG co trong khuon vox-director. Chen vao
#    cuoi `scene` vi `compose_collage_prompt` nhet `scene` nguyen van. ─────────
JP_GUARD = (
    " Any person shown is JAPANESE and elderly (60s-70s), in modest everyday "
    "Japanese clothing — not Western, not American, not 1950s retro fashion, no "
    "Americana styling. All paper surfaces, documents and signs are BLANK and "
    "unprinted, and there is no text, letter, number, headline, caption, signage, "
    "logo or watermark anywhere in the image — any accent element must be a blank "
    "paper shape or a strip of tape, never lettering. Leave a narrow empty strip "
    "of flat paper along the right edge, about one tenth of the width"
)

# ⚠️ `camera_move` cua 3 scene PEAK: KHONG dung token "push_in". CAMERA_VOCAB cua
#    vox-director dich no thanh "...(uniform scale-up, Ken-Burns)" — dung chu ma
#    user chot ghet (memory feedback_video_no_motion_mot_giong). `clips.py` co
#    `CAMERA_VOCAB.get(camera, camera)` nen chuoi la se PASS THROUGH nguyen van
#    ⇒ ghi thang muc 3% vao day, vua giu y dinh vua bo chu Ken-Burns.
PEAK_CAM = ("a barely perceptible push-in of about three percent over the whole "
            "clip — no pan, no shake, no perspective change")

# ── BEAT: (id, tag_jp, title_en, bg, feel, [(anh, shot_size, camera_move, element_motion)]) ─
# element_motion = chi mo ta MANH GIAY chuyen dong. Camera tach ra `camera_move`.
BEATS = [
 (1, "働き続けるあなた", "STILL WORKING AT SIXTY", "aged cream newsprint",
  "quiet, close to home, faintly uneasy", [
  ("card_19_hataraku", "WIDE", "parallax",
   "the man's hand slides along the row of boxes and stops; his head tilts a few "
   "degrees to follow it; the clipboard under his arm settles a millimetre; the "
   "high-window daylight pulses softly and the halftone dots breathe with it"),
  ("card_19_hataraku_b", "CLOSE", "static",
   "continuing the same rightward push, the cardboard box eases a few centimetres "
   "further onto the shelf and stops; the gloved fingertips tighten their grip; a "
   "faint paper dust shimmer drifts through the light"),
 ]),
 (2, "もらわないまま", "THE MONEY NEVER CLAIMED", "aged cream newsprint",
  "domestic, ordinary, a slow dawning", [
  ("card_19_kyuryo_meisai", "MEDIUM", "static",
   "the hands adjust the payslip a few millimetres; the paper's free edge flutters "
   "faintly; the morning light shifts slowly across the table as if a curtain moved, "
   "catching the halftone dots"),
  ("card_19_kyuryo_meisai_b", "DETAIL", "static",
   "the same morning light keeps creeping in the same direction, now sliding across "
   "the coffee-ring stain; the loose corner of the payslip lifts and settles; the "
   "folded glasses stay perfectly still"),
 ]),
 (3, "対象は", "WHO IT IS FOR", "aged cream newsprint",
  "checklist-plain, slightly clinical", [
  ("card_19_hataraku_c", "DETAIL", "static",
   "the hand pushes the blank time card fully into the wall-clock slot and holds; "
   "the machine gives one small mechanical jolt; the card stops flush"),
  ("card_19_hatena", "WIDE", "parallax",
   "the seated man's gaze travels from the left envelope to the right one and stops "
   "in the middle; his fingertip taps his cheek twice, slowly; the lamp's pool of "
   "light wavers once across the paper"),
 ]),
 (4, "三つの問い", "THREE QUESTIONS", "charcoal ink navy",
  "hushed, a question hanging in the air", [
  ("card_19_hatena_b", "DETAIL", "static",
   "the three fanned envelopes shift a millimetre apart; their top edges flutter; "
   "the lamp light nudges sideways so the layered paper shadows rotate very slowly "
   "beneath them"),
  ("card_19_hatena_c", "CLOSE", "static",
   "the envelope is turned over one beat in his hands to show its blank back; he "
   "blinks once and his frown deepens slightly; the side light stays fixed"),
 ]),
 (5, "年金も止まる", "THE PENSION STOPS TOO", "aged cream newsprint",
  "study-quiet, methodical", [
  ("card_19_kenkyu", "WIDE", "static",
   "the small brass clock's second hand ticks forward in single steps; the top "
   "leaflet's corner lifts and settles; the fountain pen and magnifier stay "
   "absolutely still"),
 ]),
 (6, "研究室", "THE RESEARCH ROOM", "aged cream newsprint",
  "calm, precise, an editorial desk", [
  ("card_19_kenkyu_b", "DETAIL", "static",
   "the magnifying glass rocks a pixel or two so the paper grain seen through the "
   "lens slides with it; the bright halo on the lens edge creeps across; the linen "
   "underneath does not move"),
 ]),
 (7, "下がった分を補う", "TOPPING UP WHAT WAS LOST", "mustard yellow",
  "practical, mildly hopeful", [
  ("card_19_koyou_hoken", "MEDIUM", "static",
   "the uniformed hand lowers the last two banknotes onto the stack, releases them "
   "and withdraws out of frame; the stack settles by a hair; the older palm beneath "
   "stays open and steady"),
  ("card_19_koyou_hoken_b", "DETAIL", "static",
   "the same placing-down action, now seen close as if the cut had zoomed in "
   "mid-gesture: the top note touches down and stops, the small stack compresses "
   "slightly, the fingers beneath curl in a fraction"),
 ]),
 (8, "七十五パーセント未満", "UNDER SEVENTY-FIVE PERCENT", "deep red",
  "a threshold, taut", [
  ("card_19_75percent", "MEDIUM", "static",
   "the taut red thread vibrates like a plucked string and slowly damps to "
   "stillness; the coin stack and the measuring stick do not move at all"),
  ("card_19_75percent_b", "DETAIL", "static",
   "the vibration finishes damping out on the thread in sharp focus while the "
   "blurred stick markings behind it sway gently in the bokeh"),
 ]),
 (9, "松本さん", "ONE MAN'S PAYSLIP", "aged cream newsprint",
  "personal, a little wistful", [
  ("card_19_matsumoto", "WIDE", "parallax",
   "the drawer slides open a few more centimetres and stops; his eyes lower to the "
   "lapel pin inside; his shoulders drop one small notch"),
  ("card_19_matsumoto_b", "DETAIL", "static",
   "the open palm tilts a few degrees so the warm lamp light sweeps across the "
   "plain enamel face of the pin; the fingers close in very slightly around it"),
  ("card_19_matsumoto_c", "MEDIUM", "static",
   "closing the sequence: the drawer is pushed shut in one slow quiet motion until "
   "it seats; he keeps looking down; the lamp behind him is steady"),
 ]),
 (10, "落とし穴", "THE CEILING", "charcoal ink navy",
  "a trap closing, mechanical", [
  ("card_19_jougen", "MEDIUM", "static",
   "the wooden ruler presses down one notch onto the tall coin stack; the stack "
   "compresses; a single coin at the rim trembles and holds"),
  ("card_19_jougen_b", "DETAIL", "static",
   "continuing the same downward press, extremely close: the ruler bites further "
   "into the top coin, the coins under it shift a fraction, the wood grain digs in"),
  ("card_19_jougen_c", "CLOSE", "static",
   "the consequence: the last loose coin rolls slowly across the desk and topples "
   "flat; the capped stack behind it stays motionless in the bokeh"),
  ("card_19_jougen_d", "CLOSE", "static",
   "the hand lowers the single coin until it meets the ruler, stops dead and stays "
   "there unable to place it; the fingers hold the coin suspended; nothing else moves"),
 ]),
 (11, "二万八千円", "TWENTY-EIGHT THOUSAND YEN", "mustard yellow",
  "warm, a small relief", [
  ("card_19_28000", "MEDIUM", "static",
   "he raises the passbook slightly closer to his eyes; the corner of his mouth "
   "lifts a little further into relief; steam drifts up from the tea cup"),
  ("card_19_28000_b", "DETAIL", "static",
   "the fingertip glides right along the blank ruled entry line and stops at its "
   "end; the warm window light grows fractionally brighter on the page"),
  ("card_19_28000_c", "WIDE", "parallax",
   "seen from above, the tea steam curls upward and folds over; the warm afternoon "
   "light creeps slowly across the wooden table; passbook and glasses stay still"),
 ]),
 (12, "ここからが本題", "NOW THE REAL POINT", "charcoal ink navy",
  "a turn, the room darkening", [
  ("card_19_hondai", "MEDIUM", "static",
   "the turned-up corner of the leaflet lifts and settles back; the desk lamp sways "
   "a hair so the pen's shadow sweeps across the page; the dark room stays dark"),
  ("card_19_hondai_b", "DETAIL", "static",
   "the same corner keeps creeping upward while the narrow beam of lamp light "
   "contracts, letting the rest of the page sink deeper into shadow"),
 ]),
 (13, "八十四万円", "EIGHT HUNDRED FORTY THOUSAND", "deep red",
  "the loss made physical — the payoff of the film", [
  ("card_19_84man", "MEDIUM", "push_in",
   "the ragged torn edge of the banknote stack bristles with loose paper fibres; "
   "the whole stack settles one notch as if the tearing has only just stopped; the "
   "hard single-source light does not move"),
  ("card_19_84man_b", "CLOSE", "push_in",
   "the torn-away portion lying apart flutters faintly and drifts a further pixel "
   "or two away, so the empty gap between the two pieces reads wider; the remaining "
   "stack is dead still"),
 ]),
 (14, "分かれ目は誕生日", "THE LINE IS A BIRTHDAY", "deep red",
  "arbitrary, irreversible", [
  ("card_19_tanjoubi", "MEDIUM", "static",
   "the red circle is completed on its last stroke and the marker tip lifts clear "
   "of the paper; the calendar page flutters once against the wall"),
  ("card_19_tanjoubi_b", "DETAIL", "static",
   "extremely close: the red ink reads as still wet and bleeds a hair further into "
   "the paper fibres; the surrounding blank squares do not move"),
  ("card_19_tanjoubi_c", "CLOSE", "static",
   "the unmarked right-hand page lifts its edge as if waiting to be marked too, "
   "then settles; the circled left page stays flat and still"),
  ("card_19_tanjoubi_d", "CLOSE", "static",
   "closing the beat: the uncapped red marker rolls two or three pixels and stops "
   "against the calendar; the cap resting apart never moves"),
 ]),
 (15, "割合が厳しい", "THE RATIO IS UNFORGIVING", "mustard yellow",
  "weighing, judicial", [
  ("card_19_wariai", "MEDIUM", "static",
   "the two pans of the brass balance swing slowly and damp down into their tilted "
   "resting position; the pointer settles off-centre and stops"),
 ]),
 (16, "同僚のかた", "THE COLLEAGUE", "aged cream newsprint",
  "resigned, a wry human beat", [
  ("card_19_douryou", "WIDE", "parallax",
   "he lowers the payslip a little; the wry smile tightens further; the vending "
   "machine behind him pulses once in the blur"),
  ("card_19_douryou_b", "DETAIL", "static",
   "the gripping fingers squeeze harder and the crease across the payslip spreads; "
   "the blurred break-room background stays still"),
  ("card_19_douryou_c", "MEDIUM", "static",
   "closing the beat: the folded sheet slides back into the brown envelope until it "
   "disappears; his shoulders drop; he keeps looking down"),
 ]),
 (17, "一円も、出ません", "NOT ONE YEN", "charcoal ink navy",
  "cold, empty, final", [
  ("card_19_zero", "CLOSE", "static",
   "the open palm closes halfway and opens again — one empty beat — then holds; the "
   "empty envelope beside it does not move; the cold flat light is constant"),
  ("card_19_zero_b", "DETAIL", "static",
   "the envelope's open flap lifts and falls back showing nothing inside; the bare "
   "desk stays empty; the cold overhead light never changes"),
 ]),
 (18, "冒頭のふたり", "THE TWO MEN, AGAIN", "deep red",
  "the callback landing — two identical men, two different fates", [
  ("card_19_futari", "WIDE", "push_in",
   "the uneasy man slowly turns his head toward the calm one; the calm man does not "
   "move at all; both keep holding their envelopes; the corridor is still"),
  ("card_19_futari_b", "DETAIL", "push_in",
   "the tightly gripping pair of hands squeezes harder until the envelope creases; "
   "the other pair holds its envelope perfectly level and unchanged"),
  ("card_19_futari_c", "EST_WIDE", "push_in",
   "the man ahead keeps walking away toward the door and blurs further out while "
   "the man who stopped to read stands completely still, so the gap between them "
   "opens wider"),
  ("card_19_futari_d", "MEDIUM", "push_in",
   "closing the callback: the folded work jacket sways almost imperceptibly between "
   "the two closed lockers; the fluorescent light flickers once; both doors stay shut"),
 ]),
 (19, "お願いです", "ONE SMALL REQUEST", "mustard yellow",
  "warm, domestic, a hand on the shoulder", [
  ("card_19_cta", "WIDE", "parallax",
   "the couple lean their heads a little toward each other and their smiles widen "
   "slightly; the warm living-room light is steady"),
  ("card_19_cta_b", "DETAIL", "static",
   "a fingertip taps the blank pale tablet screen once and withdraws; the screen "
   "brightens very faintly and stays completely blank"),
  ("card_19_cta_c", "CLOSE", "static",
   "green tea pours from the spout into the second cup in a steady thin stream and "
   "the steam rises and curls; the low table stays still"),
  ("card_19_cta_d", "MEDIUM", "static",
   "the two keep looking at each other with knowing smiles; one of them blinks "
   "once; the face-down tablet and the warm lamp are motionless"),
 ]),
 (20, "二つ目の窓口", "THE SECOND COUNTER", "aged cream newsprint",
  "bureaucratic, slightly disorienting", [
  ("card_19_madoguchi2", "WIDE", "parallax",
   "the man standing between the counters turns his head from the left counter to "
   "the right one and settles facing straight ahead again; the two blank signs "
   "above do not move"),
  ("card_19_madoguchi2_b", "MEDIUM", "static",
   "almost entirely still: only the daylight creeps very slowly across the counter "
   "surface; the empty chair stays empty; the emptiness is the content"),
 ]),
 (21, "ここは正確に", "GET THIS PART EXACT", "aged cream newsprint",
  "steadying, careful", [
  ("card_19_tadashi", "MEDIUM", "static",
   "the raised palm lifts a fraction higher into the wait-a-moment gesture and "
   "holds there; his head tilts slightly; his expression stays calm"),
  ("card_19_tadashi_b", "DETAIL", "static",
   "the same held gesture seen close: the fingers spread a little and stop; the "
   "palm's soft shadow on the pale background shifts with them"),
  ("card_19_tadashi_c", "CLOSE", "static",
   "closing the beat: he pushes his reading glasses up the bridge of his nose with "
   "one hand and his eyes drop to the document; unhurried"),
 ]),
 (22, "繰上げ受給", "TAKING IT EARLY", "charcoal ink navy",
  "time running out early, muted", [
  ("card_19_kuriage", "MEDIUM", "static",
   "the last few grains trickle out of the toppled hourglass's neck onto the desk "
   "and then stop; the spilled pile stays where it is"),
  ("card_19_kuriage_b", "DETAIL", "static",
   "a few stray grains slide away from the small spilled pile and come to rest; the "
   "blurred hourglass base behind is motionless"),
  ("card_19_kuriage_c", "CLOSE", "static",
   "the hourglass stands upright again and the sand runs steadily down through the "
   "neck, the upper level visibly dropping; the loose sand on the desk never moves"),
 ]),
 (23, "二重に、削られます", "CUT TWICE", "deep red",
  "compounding, surgical", [
  ("card_19_nijuu", "MEDIUM", "static",
   "one of the cut paper strips flutters and drifts a little further away from the "
   "sheet it came from; the scissors lie dead still"),
  ("card_19_nijuu_b", "DETAIL", "static",
   "the open scissor blades close one beat and open again; the freshly cut strip "
   "beside them trembles from the movement of air"),
  ("card_19_nijuu_c", "CLOSE", "static",
   "both parallel strips lift together and settle back so the gap between them and "
   "the remaining sheet reads wider"),
 ]),
 (24, "戻りません", "NO WAY BACK", "charcoal ink navy",
  "one-way, locked, the hardest line in the film", [
  ("card_19_modoranai", "MEDIUM", "push_in",
   "the barred arm of the turnstile is pushed a few degrees, catches hard against "
   "its lock and refuses to give; the hand stays resting on it; nothing else moves"),
  ("card_19_modoranai_b", "DETAIL", "push_in",
   "extremely close on the locking mechanism: it shifts a fraction and bites shut "
   "again; the cold metal is otherwise absolutely still"),
  ("card_19_modoranai_c", "EST_WIDE", "push_in",
   "almost entirely still: the cold light down the far corridor pulses once; the "
   "out-of-focus gate in the foreground does not move; the corridor stays empty"),
 ]),
 (25, "給料明細を見る", "READ YOUR PAYSLIP", "mustard yellow",
  "instructional, hands-on", [
  ("card_19_meisai_check", "DETAIL", "static",
   "the fingertip traces slowly down the blank ruled column and stops; the "
   "magnifying glass is held steady above it so the paper grain seen through the "
   "lens slides under the finger"),
  ("card_19_meisai_check_b", "MEDIUM", "static",
   "the hand withdraws fully out of frame and the magnifier stays put where it was "
   "set down; the warm kitchen light creeps a little across the payslip"),
 ]),
 (26, "四か月以内", "WITHIN FOUR MONTHS", "deep red",
  "a deadline peeling away", [
  ("card_19_4kagetsu", "MEDIUM", "static",
   "the curling corner of the last calendar page lifts a little further and "
   "settles; the red marker resting on top does not move"),
  ("card_19_4kagetsu_b", "DETAIL", "static",
   "the same corner keeps peeling slowly upward, just revealing the blank page "
   "beneath it"),
  ("card_19_4kagetsu_c", "CLOSE", "static",
   "the hand tears the page further off the calendar and the half-detached sheet "
   "twists downward; the remaining pages stay flat against the wall"),
 ]),
 (27, "二つの窓口", "TWO WINDOWS", "aged cream newsprint",
  "side by side, comparative", [
  ("card_19_futatsu_mado", "MEDIUM", "static",
   "his eyes move from the left document to the right one and back, then settle; "
   "both hands stay resting where they are"),
  ("card_19_futatsu_mado_b", "DETAIL", "static",
   "seen from above, both hands press down one beat — the right one half a beat "
   "later than the left — flattening the two sheets, then both hold still"),
 ]),
 (28, "ご注意", "A WORD OF CAUTION", "aged cream newsprint",
  "empty, institutional, quiet", [
  ("card_19_chuui", "WIDE", "parallax",
   "one blank leaflet on the counter-top stand flutters and settles; the counter, "
   "the chair and everything else stay completely still; nobody appears"),
  ("card_19_chuui_b", "DETAIL", "static",
   "the outermost leaflet in the stand lifts and falls back; the rest of the pale "
   "blank leaflets do not move"),
  ("card_19_chuui_c", "MEDIUM", "static",
   "almost entirely still: only the soft daylight creeps slowly across the counter "
   "top; the single empty chair stays empty"),
 ]),
 (29, "次回予告", "NEXT TIME", "mustard yellow",
  "closing down for the night, warm and calm", [
  ("card_19_yokoku", "MEDIUM", "static",
   "her eyes travel down the notice sheet; her fingers adjust the paper a few "
   "millimetres; the evening lamp light is steady"),
  ("card_19_yokoku_b", "DETAIL", "static",
   "the held notice sheet trembles faintly in both hands; the warm low lamp light "
   "does not change"),
  ("card_19_yokoku_c", "CLOSE", "static",
   "steam drifts up from the teacup and thins out; the reading glasses and the "
   "folded notice stay exactly where they were set down"),
  ("card_19_yokoku_d", "EST_WIDE", "parallax",
   "closing the film: her silhouette rises and falls with one slow breath; the "
   "floor lamp's warm pool of light wavers almost imperceptibly; dusk holds"),
 ]),
]

DUR = 6          # vox-director SKILL.md: "shots run 3-6s; never exceed ~7s"


def load_scenes():
    """Doc field SCENE tu chinh 2 file art_prompts FLOW — dung hard-code lai,
    de prompt anh doi thi beats.json tu theo."""
    out = {}
    for flow, tenf in [("art_prompts_photocard19_FLOW.txt", "art_prompts_photocard19_TENFILE.txt"),
                       ("art_prompts_photocard19b_FLOW.txt", "art_prompts_photocard19b_TENFILE.txt")]:
        rows = [l for l in io.open(os.path.join(VD19, tenf), encoding="utf-8") if "<-" in l]
        names = [l.split("<-")[0].strip().replace(".png", "") for l in rows]
        lines = [l.rstrip("\n") for l in io.open(os.path.join(VD19, flow), encoding="utf-8") if l.strip()]
        for i, l in enumerate(lines):
            m = re.search(r"SCENE \(as layered paper cut-outs\):(.*?)(?:Any person shown|Composition:)", l, re.S)
            if m:
                out[names[i]] = m.group(1).strip().rstrip(".")
    return out


def build():
    scenes = load_scenes()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "keyframes"), exist_ok=True)
    beats, miss, n = [], [], 0
    for bid, tag, ten, bg, feel, shots in BEATS:
        sh = []
        for i, (name, size, cam, elem) in enumerate(shots):
            n += 1
            if name not in scenes:
                miss.append(name)
                continue
            kf = os.path.join(VD19, "photocard", name + ".png")
            sh.append({
                "id": "abcd"[i],
                "dur": DUR,
                "title": False,                     # 74/74 — anh khong co chu nao
                "shot_size": size,
                "camera_move": PEAK_CAM if cam == "push_in" else cam,
                "scene": scenes[name] + JP_GUARD,
                "element_motion": elem,
                "keyframe_path": kf if os.path.exists(kf) else None,
                "src_card": name,
            })
        beats.append({"id": bid, "title_cn": tag, "title_en": ten,
                      "bg": bg, "feel": feel, "shots": sh})
    doc = {
        "project": "nenkin-19",
        "topic": "高年齢雇用継続給付 — 60歳を過ぎて働き続ける人が受け取り損ねる給付金",
        "language": "ja",
        "aspect": "16:9",
        "style": "collage",                 # BAT BUOC — khong thi roi vao painterly_prompt
        "theme": "newsprint-editorial",     # lay palette / type_style / finish
        "collage_style": COLLAGE_STYLE,     # override idiom -> ban JP
        "motion_style": "calm",             # audience-45plus.md §2 (default cua tool la punchy)
        "constraints": "strict",            # bat defect guard: flat 2D / no morph / one move
        "video_model": "google/gemini-omni-flash/image-to-video",
        "note": ("Chi dung stage KEYFRAME + CLIPS. Voice/music/assemble cua "
                 "vox-director KHONG dung: giong da co (VOICEVOX 雀松朱司 + tag "
                 "nhan nha), phu de/CTA/watermark do Remotion cua nenkin lo."),
        "beats": beats,
    }
    p = os.path.join(OUT, "beats.json")
    io.open(p, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=2))
    print(f"beats.json -> {p}")
    print(f"  {len(beats)} beat · {sum(len(b['shots']) for b in beats)}/{n} shot")
    nokf = [s["src_card"] for b in beats for s in b["shots"] if not s["keyframe_path"]]
    print(f"  thieu keyframe tren dia: {nokf or '-- khong thieu --'}")
    print(f"  thieu scene trong art_prompts: {miss or '-- khong thieu --'}")
    cams = {}
    for b in beats:
        for s in b["shots"]:
            cams[s["camera_move"]] = cams.get(s["camera_move"], 0) + 1
    print("  camera_move:", cams)
    return doc


if __name__ == "__main__":
    d = build()
    tot = sum(len(b["shots"]) for b in d["beats"])
    assert tot == 74, f"phai 74 shot, dang co {tot}"
