# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt MINH HOA AI cho video 19 (たんぱく質 x 一日三回しか開かないゲート).

    python tools\build_slides_19.py

Style theo khuon da chot tu video 18/20: minh hoa AI kawaii pastel nen TRANG, TINH,
phu de den o dai trang duoi day khung (sub_style "kuro").

⭐ AP THEM luat MOI hon video 20 (audience-45plus.md §2.0b, chot 2026-08-31, SAU khi
video 20 da dung): anh CHINH (hero) doi moi <=9,0s o scene ANH thuong (khong tinh scene
so lieu duoc mien) — mat do trong PLAN nay ~9,2s/canh (125 canh / 1151s), day hon han
video 20 (82 canh / ~18').

SOI CHI CUA BAI: an du trung tam DUY NHAT — co bap = ngoi nha duoc xay lai moi ngay,
protein = xe tai cho vat lieu, ba bua an = CONG CONG TRUONG chi mo 3 LAN/NGAY. Moi
canh nen bam vao mot trong ba vat: CONG / XE TAI / KHUNG NHA, giu tinh nhat quan hinh anh
xuyen suot bai (giong tube-with-crust cua video 20).

CHU TRONG HINH (media-library.md §2.9): chi nhan NGAN, uu tien chu so Latin
(5kg / 60g / 20g / 11g / 17g / 7g / 6g / 3つ / 30秒 / 5g / 4g / <5g / 1/4 / 20g×3) —
soi TUNG KY TU truoc khi nhan.

Xuat:
  04_SCRIPTS/19_tanpakushitsu-asa_SLIDES_photo.json
  06_VIDEO/19_tanpakushitsu-asa/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "19_tanpakushitsu-asa_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "19_tanpakushitsu-asa_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "19_tanpakushitsu-asa"

CPS, PER_LINE = 4.40, 0.25

STYLE = ("simple flat Japanese educational illustration, soft warm pastel colours, "
         "clean rounded shapes with thin warm-brown outlines, gentle flat shading, "
         "generous white space, plain pure-white background, kind reassuring mood, "
         "wide 16:9 composition, main subject centred in the upper two thirds, "
         "a clean empty white band left along the bottom edge")
NEG_BASE = ("no photorealism, no 3D render, no dark heavy colours, no watermark, "
            "no logo, no signature, no doctors, no white coats, no hospital beds, "
            "no blood, no gore, no extra people")
NEG_NOTEXT = NEG_BASE + ", no text, no letters, no numbers"

# An du trung tam — lap NGUYEN VAN moi canh co CONG/XE TAI/KHUNG NHA (style-lock)
GATE = ("a simple gantry-style wooden construction gate standing upright, two thick "
        "posts and a crossbar, drawn plainly and kindly")
TRUCK = ("a small round-bodied delivery truck loaded with a few bundled wooden planks, "
         "drawn in a friendly toy-like style")
HOUSE = ("a small wooden house frame under gentle construction, one pale new pillar "
         "being raised beside an older grey pillar")

# Nhan vat co dinh anecdote (style-lock — lap NGUYEN VAN o moi canh co nguoi)
KATSUMI = ("a lean Japanese man of seventy-two with neatly combed silver hair and a "
           "calm weathered face, wearing a beige cardigan over a light blue shirt")
AYAKO = ("a gentle Japanese woman of sixty-eight with short permed grey hair and round "
         "glasses, wearing a warm coral cardigan over a cream blouse")

# (line_idx, SCENE bo cuc, SUBJECT, TEXT nhan bake — None = khong chu)
PLAN = [
    # ═══ COLD OPEN — banh mi+ca phe, phep tinh soc 5kg/nam ═══
    (0, "a small breakfast plate sits alone at the centre, steam rising from a coffee cup beside it",
     "a single slice of toast on a plain white plate beside one cup of black coffee, nothing else "
     "on the table", None),
    (2, "the truck enters from the left edge toward the gate at the centre",
     TRUCK + " arriving at " + GATE + ", the truck carrying only a very small, half-empty load",
     None),
    (4, "a simple piggy bank sits at the centre with a crossed-out arrow above it",
     "a small ceramic piggy bank with a red crossed-out arrow drawn above its coin slot, showing "
     "nothing can be saved inside", None),
    (6, "a calendar page fills the frame, many identical small icons repeating across it",
     "a calendar page showing the same small empty breakfast plate icon repeated across every day "
     "of the month", "365"),
    (8, "a large sack sits at the centre, a small kitchen scale beside it",
     "a large burlap sack that looks heavy, standing beside a small kitchen scale, drawn plainly",
     "5kg"),
    (10, "a hand rests lightly on a stair handrail at the centre, one step below",
     "an elderly hand resting on a wooden stair handrail while descending one step, calm and gentle",
     None),
    (12, "a simple scale balances at the centre, both sides shown clearly",
     "a two-pan balance scale, one pan piled full and level, the other pan drawn with the same total "
     "weight but scattered and uneven", None),
    (14, "a small covered dish sits at the centre of an otherwise empty table",
     "a single small covered dish with a soft question mark drawn faintly above its lid, sitting "
     "alone on a plain table", None),
    (16, "a folded note sits at the centre with a soft ribbon around it",
     "a small folded paper note tied with a thin ribbon, resting on a plain table, waiting to be "
     "opened", None),

    # ═══ (1) YOU NO SHOKUTAKU — cong chi mo 3 lan, xe toi khong dung luc ═══
    (18, "the dinner table fills the frame, warm lamp light above it",
     "a simple Japanese dinner table at night with a grilled fish, a small piece of meat and a "
     "block of tofu, under a warm hanging lamp", None),
    (20, "the table fills the frame, many small dishes crowded together",
     "a generously filled Japanese dinner table seen from above, several small dishes close "
     "together, warm and abundant", None),
    (22, "the gate stands at the left, a stack of extra trucks waits at the right",
     GATE + " with several extra " + TRUCK.replace("a small round-bodied", "small round-bodied")
     + "s queued up on its right side, waiting", None),
    (24, "the house frame fills the centre, builders' tools resting quietly beside it",
     HOUSE + ", with small tools resting quietly on the ground beside it, calm evening light", None),
    (26, "one old grey pillar leaves at the left, one new pale pillar rises at the right",
     "a single grey weathered pillar being carried away at one side while a pale new wooden pillar "
     "is raised at the other side of a small house frame", None),
    (28, "the gate stands at the centre, three small clock faces line up above it",
     GATE + " with three small round clock faces lined up above the crossbar, each showing a "
     "different time of day", None),
    (30, "the truck approaches the gate from the left, the gate open at the centre",
     TRUCK + " approaching " + GATE + " with its doors open wide, delivering its load", None),
    (32, "the gate stands closed at the centre, the truck waits outside at the left",
     GATE + " shown closed, with " + TRUCK + " waiting just outside, unable to enter", None),
    (34, "many trucks are lined up at the right edge, the gate stands shut at the centre",
     "a long line of ten small identical " + TRUCK.replace("a small round-bodied delivery truck",
     "delivery trucks") + " queued outside a closed " + GATE, None),
    (36, "two identical piles sit side by side at the centre, each the same size",
     "two identical small piles of building blocks, exactly the same height, sitting side by side "
     "for comparison", None),
    (39, "two house frames stand side by side, one taller and one shorter",
     "two small house frames under construction standing side by side, one noticeably taller and "
     "more complete than the other", "25%"),
    (41, "two plates sit side by side at the centre, each holding the exact same food",
     "two identical dinner plates side by side holding exactly the same small portions of food, "
     "drawn to look perfectly equal", None),
    (44, "a quarter of a pie chart fades into empty white at the centre",
     "a simple round pie shape with one quarter drawn faded and empty, the other three quarters "
     "solid and warm coloured", "1/4"),

    # ═══ persona + xin dang ky ═══
    (46, "a simple welcome mat and a small doorway sit at the centre",
     "a small warm doorway with a round welcome mat in front of it and a gentle glow inside", None),
    (50, "a simple map of Japan sits at the centre, one soft pin marking a spot",
     "a soft rounded map of the Japanese islands with a single gentle pin mark hovering above it",
     None),
    (53, "a small bell icon floats above a folded envelope at the centre",
     "a small notification bell floating gently above a folded envelope on a bright tidy table",
     None),
    (54, "a folded note sits at the left, a small warning triangle at the right",
     "a plain folded note beside a small soft rounded warning triangle, calm and non-alarming",
     None),
    (56, "a kidney-shaped icon sits at the centre, a measuring spoon resting beside it",
     "a small soft rounded kidney-shaped icon beside a plain measuring spoon, drawn kindly without "
     "any medical setting", None),

    # ═══ nguon that + phep tinh 60÷3=20 ═══
    (58, "a small mirror stands at the centre reflecting a soft question mark",
     "a small round hand mirror standing upright on a table, reflecting a soft pale question mark",
     None),
    (59, "an official document card sits at the centre with a small round seal",
     "a plain official-looking document card with a small round red seal in one corner, drawn "
     "simply and respectfully", "厚生労働省"),
    (60, "two small figures stand side by side at the centre, each beside their own number",
     "a simple silhouette of a man and a woman standing side by side, each beside a small rounded "
     "number card", "60g"),
    (62, "one large truck sits at the left, three small trucks line up at the right",
     "one large loaded " + TRUCK.replace("a small round-bodied delivery truck", "delivery truck") +
     " beside three smaller identical trucks lined up, showing it split into three equal loads",
     "60g÷3"),
    (63, "one small truck sits alone at the centre, its number label glowing softly",
     TRUCK + ", its cargo label glowing softly warm", "20g"),
    (65, "the gate stands at the centre, opened only a small crack",
     GATE + " shown opened only a small narrow crack, not fully", None),

    # ═══ (指輪っかテスト) — phep do 30 giay ═══
    (68, "a round stopwatch sits at the centre, its hand sweeping gently",
     "a small round stopwatch with its hand sweeping a gentle arc, calm and unhurried", "30秒"),
    (70, "two hands meet at the centre, thumbs and index fingers forming a ring",
     "two elderly hands forming a gentle ring shape with thumbs and index fingers touching, seen "
     "close and warm, then lowering toward a calf just below", None),
    (73, "the ring of fingers sits loosely around the calf, a visible gap between them",
     "a gentle ring made of thumb and index finger placed loosely around a calf with a small clear "
     "gap left between the fingertips", None),
    (74, "the ring of fingers sits snugly around the calf, fingertips just touching",
     "a gentle ring made of thumb and index finger placed exactly around a calf with the fingertips "
     "just touching, neither gap nor overlap", None),
    (76, "the ring of fingers overlaps around the calf, extra space showing inside",
     "a gentle ring made of thumb and index finger placed around a calf with the fingers clearly "
     "overlapping, a soft gap of space left inside the ring", None),
    # ═══ (2) HIRU NO SHOKUTAKU — mot cong dong, hai cong dong ═══
    (78, "the lunch table fills the frame, midday light from the left",
     "a simple Japanese lunch table seen from the side under soft midday light, one bowl in the "
     "centre", None),
    (82, "three bowls line up across the middle of the frame",
     "a somen bowl, an udon bowl and a cold soba bowl lined up in a row, each holding only noodles "
     "and broth", None),
    (84, "a fan rests at the left, the same noodle bowl sits at the right",
     "a simple folding fan resting beside a bowl of cold noodles on a summer table, warm light",
     None),
    (86, "the gate stands at the centre, opened only slightly",
     GATE + " shown opened only slightly, a thin gap of light showing through", "5-9g"),
    (87, "one small truck sits at the left, the number twenty glows unreached at the right",
     TRUCK + " parked far from a faint glowing outline of the number twenty, unable to reach it",
     "20g"),
    (89, "two of the three gate sections are shaded closed, one remains open",
     "three simple gate sections in a row, two of them shaded dim and closed, only one still open "
     "and bright", None),
    (90, "a single small dish sits at the centre, an arrow pointing toward the noodle bowl",
     "a single small side dish with a gentle arrow pointing it toward a nearby noodle bowl", None),
    (92, "three small side dishes line up above the noodle bowl",
     "a small piece of chikuwa, one raised egg, and a small dish of cold tofu arranged neatly above "
     "a noodle bowl", None),
    (94, "the same noodle bowl sits at the centre, now fuller and richer looking",
     "the same bowl of noodles now topped generously with egg and a few extra pieces, richer and "
     "fuller than before", "2x"),
    (96, "one small dish sits beside the noodle bowl, not inside it",
     "a small extra side dish placed neatly beside a full bowl of noodles rather than replacing any "
     "of it", None),

    # ═══ anecdote 克己さん — Shizuoka, 72 tuoi ═══
    (99, "a single warm portrait fills the centre of the frame",
     KATSUMI + ", standing calmly in a quiet garden, a gentle kind expression", None),
    (101, "the figure waters small potted plants at the centre",
     KATSUMI + " watering a row of small potted plants on a morning veranda, early soft light",
     None),
    (102, "the dinner table fills the frame, the same figure seated at it",
     KATSUMI + " seated at a generously filled dinner table at night, chopsticks in hand", None),
    (104, "a small clipboard sits at the centre, a soft downward arrow beside one line",
     "a plain health checkup clipboard with a soft downward arrow drawn beside one line, calm and "
     "non-alarming", None),
    (105, "a speech bubble floats above the seated figure at the centre",
     KATSUMI + " sitting quietly at a table, a small speech bubble floating above him, puzzled "
     "expression", None),
    (107, "the same small breakfast plate sits alone on a long calendar strip",
     "a single slice of toast and a coffee cup repeated identically along a long calendar ribbon "
     "stretching into the distance", "30年"),
    (109, "the gate stands at the centre, only its night section lit and open",
     GATE + " with only the section marked for evening lit and open, the morning and noon sections "
     "dim", None),

    # ═══ CTA giua ═══
    (111, "a large comment bubble floats at the centre with one character inside",
     "a large friendly speech bubble floating on a plain table, one simple character drawn softly "
     "inside it", "に"),
    (112, "a heart mark and a small share icon float above a smartphone at the centre",
     "a smartphone lying on a table with a gentle heart mark and a small share arrow floating "
     "above it", None),
    (113, "a small mailbox sits at the centre, a few gentle notes floating above it",
     "a small friendly mailbox with a few gentle handwritten notes floating softly above it", None),
    # ═══ (3) ASA GA HONDAI — cong sang trong nhat ═══
    (115, "the gate stands at the centre, morning light streaming through it",
     GATE + " with soft warm morning light streaming directly through its open crossbar", None),
    (117, "three meal icons line up, the morning one glowing brighter than the rest",
     "three small simple meal icons in a row — breakfast, lunch and dinner — with the breakfast "
     "icon glowing noticeably brighter than the other two", None),
    (119, "a simple gauge sits at the centre, its needle resting below the halfway mark",
     "a small rounded gauge dial with its needle resting just below the halfway mark, drawn plainly",
     "<50%"),
    (121, "three gate sections line up, the morning one drawn wide open and empty",
     "three simple gate sections in a row, the morning section drawn wide open with nothing "
     "passing through it, looking noticeably empty", None),
    (123, "a crescent moon sits at the left, a sunrise glows at the right",
     "a small pale crescent moon on one side and a warm rising sun on the other, a long quiet gap "
     "of night stretching between them", None),
    (125, "a long empty road stretches from the left edge to the right edge",
     "a long empty road stretching from a small dinner table at one end to a small breakfast plate "
     "at the other, no trucks anywhere on it", "10時間"),
    (126, "the house frame fills the centre, its material shelf drawn completely bare",
     HOUSE + ", its small material shelf beside it drawn completely bare and empty at dawn", None),
    (128, "a single coffee cup sits alone at the centre, tools resting untouched behind it",
     "a single cup of coffee sitting alone on a table, small construction tools resting untouched "
     "and idle just behind it", None),

    # ═══ hoai niem — mam com xua ═══
    (133, "steam curls upward from a small grill at the centre",
     "a small grilled fish resting on a plate, gentle steam and aroma lines curling upward", None),
    (135, "three small dishes line up across a low breakfast table",
     "a rolled tamagoyaki, a bowl of miso soup and a small dish of natto arranged neatly on a low "
     "traditional breakfast table", None),
    (137, "the same low table now holds only two simple items",
     "the same low breakfast table now holding only a slice of toast and a cup of coffee, the "
     "warmth of before quietly gone", None),
    (139, "a single coffee cup sits alone at the centre of an empty table",
     "a single cup of black coffee sitting alone in the centre of an otherwise completely empty "
     "breakfast table", None),
    # ═══ 3 lot hom sang ═══
    (142, "three small numbered cards line up across the middle",
     "three small rounded numbered cards in a row, each showing a simple faded breakfast icon",
     "3つ"),
    (145, "a single slice of toast and a coffee cup sit at the centre",
     "one plain slice of toast beside a cup of black coffee, nothing else on the plate", "5g"),
    (148, "a piece of fruit and a small yogurt cup sit at the centre",
     "a piece of fruit beside a small cup of plain yogurt, nothing else on the table", None),
    (150, "a rice bowl and a miso soup bowl sit at the centre",
     "a plain bowl of rice beside a bowl of miso soup with little visible inside it", None),
    (153, "a small piece of tofu floats inside the miso soup bowl at the centre",
     "the same miso soup bowl now with a small piece of tofu visible inside it, a soft upward "
     "arrow beside the bowl", None),
    (154, "pickles sit beside the rice bowl at the centre",
     "a small dish of pickles beside a plain bowl of rice, nothing more added", "<5g"),
    (156, "the gate stands at the centre, opened just short of fully",
     GATE + " shown opened almost all the way, just short of fully wide", None),

    # ═══ thit nang / protein bot / com nhien lieu ═══
    (158, "a piece of meat sits at the left, an egg and a bowl of natto sit at the right",
     "a small piece of meat on one side and an egg with a small bowl of natto on the other side, "
     "shown as equal alternatives", None),
    (161, "three small coins sit at the centre beside a simple food item",
     "three small round coins resting beside a plain egg on a table, showing something inexpensive",
     "百円"),
    (162, "a small measuring scoop sits at the centre beside a glass of water",
     "a small measuring scoop resting beside a glass of water on a clean table, calm and practical",
     None),
    (163, "a rice bowl sits at the centre with a soft protective circle around it",
     "a plain bowl of rice with a soft warm protective circle drawn gently around it", None),
    (164, "a rice bowl sits at the centre, an arrow pointing firmly away from it",
     "a plain bowl of rice with a small arrow drawn firmly pointing away, showing it should not be "
     "reduced", None),
    (165, "a small gear and a rice bowl sit side by side at the centre",
     "a plain bowl of rice beside a small mechanical gear, connected by a soft dotted line", None),
    (167, "a small flame consumes part of a rice bowl at the centre",
     "a plain bowl of rice with a small gentle flame drawn touching part of it, showing fuel being "
     "used up", None),

    # ═══ TRA OPEN LOOP — trung ═══
    (169, "a folded note opens at the centre, revealing something inside",
     "a small folded note opening at its centre, a soft warm glow just beginning to show inside",
     None),
    (171, "a single egg sits alone at the centre of the frame, softly glowing",
     "a single brown egg resting alone in the centre of a plain white table, drawn large and clear, "
     "softly glowing with warm light", None),
    (173, "a slice of toast sits at the left, one egg sits at the right",
     "a slice of toast beside one whole egg on a plain plate", "11g"),
    (175, "two eggs sit side by side at the centre",
     "two whole eggs resting side by side on a plain white plate", "17g"),
    (177, "a small bowl of natto sits at the centre",
     "a small bowl of natto with chopsticks resting beside it, drawn plainly", "7g"),
    (179, "a glass of milk sits at the centre",
     "a plain glass filled with milk standing on a table", "6g"),
    (182, "a single egg sits at the centre, a small calendar strip stretches behind it",
     "a single egg resting in front of a long calendar ribbon stretching into the distance, "
     "simple and steady", None),
    (183, "a refrigerator door stands open at the centre, one egg visible inside",
     "a refrigerator door standing open with one egg clearly visible on a shelf inside, warm "
     "kitchen light", None),
    (185, "a small pot sits at the left, one egg cools on a plate at the right",
     "a small pot resting on a stove beside one boiled egg cooling on a plain small plate, quiet "
     "evening light", None),
    (186, "a single small smile-shaped line floats gently at the centre",
     "a plain small kitchen counter at night, calm and softly lit, nothing dramatic happening",
     None),

    # ═══ anecdote あや子さん — Niigata, 68 tuoi ═══
    (188, "a single warm portrait fills the centre of the frame",
     AYAKO + ", standing calmly in a quiet room, a gentle kind expression", None),
    (190, "a small stack of greeting cards sits at the centre, tied with a ribbon",
     "a small neat stack of New Year greeting cards tied with a thin ribbon, resting on a warm "
     "shelf", None),
    (191, "the same low breakfast table holds toast and coffee at the centre",
     AYAKO + " seated at a small breakfast table with only toast and coffee in front of her", None),
    (194, "the same table now holds one boiled egg beside the toast",
     AYAKO + " seated at the same breakfast table, now with one boiled egg added beside the toast "
     "and coffee", None),
    (196, "a small figure lifts a child gently at the centre",
     AYAKO + " gently lifting a small grandchild up in her arms, a warm relieved smile", None),
    (198, "two arms rest calmly at the centre, no numbers or charts anywhere",
     "a pair of calm relaxed arms resting on a table in soft warm light, nothing else in the frame",
     None),

    # ═══ recap ═══
    (202, "three small trucks line up beside the gate at the centre",
     "three identical small " + TRUCK.replace("a small round-bodied delivery truck", "delivery "
     "trucks") + " lined up beside " + GATE + ", each carrying the same small load", "20g×3"),
    (204, "a quarter of a pie chart fades into empty white at the centre",
     "a simple round pie shape with one quarter drawn faded and empty, the rest solid and warm "
     "coloured", "1/4"),
    (206, "the gate stands at the centre, its morning section drawn wide open and empty",
     GATE + " with its morning section drawn wide open and clearly the emptiest of the three",
     None),
    (208, "a single egg rests beside a small pot at the centre, evening light",
     "a single egg resting beside a small pot on a stovetop in warm evening light, ready for "
     "tomorrow", None),
    (210, "three small icons line up at the centre — egg, natto, milk",
     "a small egg, a small bowl of natto and a small glass of milk arranged in a row, each equally "
     "simple", None),
    (212, "a small notebook lies open at the centre, a pen resting on it",
     "a small open notebook with a pen resting across it on a bright table, warm and attentive",
     None),
    (213, "a single envelope travels from the left edge toward the right edge",
     "a small warm envelope travelling gently across the frame from one home toward another",
     None),
    (214, "a single egg sits at the left, a pair of legs rests calmly at the right",
     "a single egg on one side of the frame and a pair of calm resting legs on the other side, "
     "connected by a soft warm line", None),

    # ═══ disclaimer + ket ═══
    (215, "a folded note sits at the centre with a soft ribbon around it",
     "a small folded paper note tied with a thin ribbon, resting alone on a plain table", None),
    (217, "a plain information card sits at the centre, no medical setting shown",
     "a plain rounded information card standing on a table, calm and neutral, no hospital or "
     "clinic setting", None),
    (219, "a kidney-shaped icon sits at the centre, drawn gently once more",
     "a small soft rounded kidney-shaped icon resting alone on a plain table, calm and non-"
     "alarming", None),
    (220, "two speech bubbles face each other at the centre",
     "two soft speech bubbles facing each other on a plain table, warm and conversational", None),
    (221, "a single egg sits alone at the centre, glowing warmly one last time",
     "a single brown egg resting alone in the centre of a plain white table, drawn large and clear, "
     "warm golden light surrounding it", None),
    (223, "a warm evening kitchen table sits quietly at the centre, set for tomorrow",
     "a warm, quiet evening kitchen table with a single egg and a small pot set gently in place for "
     "the next morning, soft lamp light", None),
]


def body_lines():
    out = []
    for ln in TTS.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"\[[^\]]*\]", "", s).strip()
        if s:
            out.append(s)
    return out


def main():
    lines = body_lines()
    starts, acc = [], 0.0
    for l in lines:
        starts.append(acc)
        acc += len(l) / CPS + PER_LINE
    total = acc

    errs, slides, flow, tenfile, blocks = [], [], [], [], []
    seen, prev = set(), -999.0
    for n, (idx, scene, subj, text) in enumerate(PLAN):
        if idx >= len(lines):
            errs.append(f"entry {n}: line_idx {idx} vuot so dong ({len(lines)})")
            continue
        if idx in seen:
            errs.append(f"entry {n}: line_idx {idx} bi dung hai lan")
        seen.add(idx)
        if starts[idx] - prev < 6.0:
            errs.append(f"entry {n} (line {idx}): cach entry truoc {starts[idx]-prev:.1f}s "
                        f"(<6s, audience-45plus §2)")
        prev = starts[idx]
        line = lines[idx]
        m = line.rstrip("。？」")
        if sum(1 for l in lines if m in l) > 1:
            errs.append(f"entry {n}: match '{m[:18]}' khop NHIEU dong")
        for bad in ("%", "two-thirds of the frame", "half of the frame width", "percent"):
            if bad in scene:
                errs.append(f"entry {n}: SCENE ta ti le ('{bad}') — ta bang MEP KHUNG")
        mm, ss = int(starts[idx]) // 60, int(starts[idx]) % 60

        fn = f"slide_{n:02d}.jpg"
        slides.append({"match": m, "photo": True})
        if text:
            p = (f"SCENE: {scene}. SUBJECT: {subj}. "
                 f"TEXT, exactly this one label and nothing else, bold rounded Japanese "
                 f"font in soft blue with a thin white halo, placed large near the centre: "
                 f"{text}. STYLE: {STYLE}. NEG: {NEG_BASE}.")
        else:
            p = (f"SCENE: {scene}. SUBJECT: {subj}. "
                 f"STYLE: {STYLE}. NEG: {NEG_NOTEXT}.")
        flow.append(p)
        tenfile.append(f"{fn}\t{mm:02d}:{ss:02d}\t{'TEXT:' + text if text else '-':10}\t{line}")
        blocks.append(
            f"### {fn} — {mm:02d}:{ss:02d}" + (f" — TEXT `{text}`" if text else "") + "\n"
            f"- cue: `{line}`\n\n```\nSCENE  : {scene}\nSUBJECT: {subj}"
            + (f"\nTEXT   : {text}" if text else "") + "\n```\n")

    if errs:
        print("[LOI] khong xuat file:")
        for e in errs:
            print("   ", e)
        return 1

    VD.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (VD / "slide_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "slide_prompts_TENFILE.txt").write_text(
        "ten file\tmoc\tnhan chu\tcau cue trong _TTS.md\n" + "\n".join(tenfile) + "\n",
        encoding="utf-8")
    ntext = sum(1 for *_x, t in PLAN if t)
    (VD / "slide_prompts_BLOCKS.md").write_text(
        f"# Video 19 — {len(slides)} minh hoa AI (たんぱく質 x 一日三回しか開かないゲート)\n\n"
        "> Slide TINH tren canvas trang, phu de den o dai trang duoi (sub_style `kuro`).\n"
        "> Ingest: `python tools\\ingest_slides_19.py <folder> --cut-x <do bang mat> --apply`\n\n"
        f"An du trung tam: CONG cong truong (mo 3 lan/ngay) · XE TAI (vat lieu protein) · "
        "KHUNG NHA (co bap dang xay lai).\n\n"
        f"🔴 {ntext} canh co CHU BAKE (5kg / 365 / 25% / 1/4 / 60g / 60g÷3 / 20g / 30秒 / 5-9g / "
        "20g / 3つ / 5g / <5g / 百円 / 11g / 17g / 7g / 6g / <50% / 10時間 / 20g×3)\n"
        "— uu tien chu so Latin cho de gen dung; van phai SOI TUNG KY TU truoc khi nhan.\n\n"
        "🔴 Nhan vat lap NGUYEN VAN mo ta (style-lock):\n"
        f"- 克己さん: `{KATSUMI}`\n- あや子さん: `{AYAKO}`\n\n"
        "🔴 An du lap NGUYEN VAN (style-lock):\n"
        f"- CONG: `{GATE}`\n- XE TAI: `{TRUCK}`\n- KHUNG NHA: `{HOUSE}`\n\n"
        "⚖️ NEG cam bac si/ao blouse/giuong benh/mau — de tai la an uong nhung anh phai\n"
        "GIU TONG AM (persona みのり + `youtube-compliance.md` §5).\n\n"
        f"**STYLE:** `{STYLE}`\n\n**NEG:** `{NEG_NOTEXT}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    idxs = [it[0] for it in PLAN]
    gaps = [starts[idxs[i]] - starts[idxs[i - 1]] for i in range(1, len(idxs))]
    print(f"OK  {n} minh hoa | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/canh | {n/(total/60):.2f} doi hinh/phut (tran 6 cu, "
          f"san moi <=9s/canh audience-45plus §2.0b)")
    print(f"    gap nho nhat {min(gaps):.1f}s | lon nhat {max(gaps):.1f}s | {ntext} canh co chu")
    over9 = sum(1 for g in gaps if g > 9.0)
    print(f"    {over9}/{len(gaps)} khe > 9,0s (san moi — chap nhan duoc o cho loi ngan lien tuc)")
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
