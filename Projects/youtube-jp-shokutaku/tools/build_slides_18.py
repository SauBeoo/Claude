# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt MINH HOA AI cho video 18 — style theo video mau sA59aiPJYLA.

    python tools\build_slides_18.py

⭐ DOI STYLE KENH (user chot 2026-08-21, dua video mau YTSave_..._sA59aiPJYLA_002_720p.mp4):
  - Do bang may tu video mau: minh hoa AI kawaii pastel nen TRANG, TINH TUYET DOI
    (diff giua 2 frame cach 2s: than hinh 0,5 / vung sub 10,8 — chi phu de doi),
    ~3-6 doi hinh/phut, phu de DEN tran to o DAI TRANG duoi day khung.
  - Thay cho style photorealistic + make_shot cua video 17. KHONG shot/fx/label layer
    — slide tinh thuan, transition dissolve 0.45s (channels.py giu nguyen).
  - Phu de: sub_style "kuro" (den vien trang, day khung — them vao video_render.py
    cung ngay). Ingest pad anh len canvas 1920x1080 TRANG, chua dai ~190px duoi.
  - Loi cho compliance: minh hoa cartoon KHONG realistic -> KHONG phai tick
    "altered/synthetic content" (youtube-compliance.md §2 chi bat noi dung realistic).

CHU TRONG HINH (media-library.md §2.9): chi nhan NGAN o 6 canh (1万回 ×2 200g 2 3)
— chu so Latin + kanji don gian; anh ve phai SOI TUNG KY TU truoc khi nhan.

Xuat:
  04_SCRIPTS/18_ringo-tabekata_SLIDES_photo.json   (entry {"match","photo":true} thuan)
  06_VIDEO/18_ringo-tabekata/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "18_ringo-tabekata_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "18_ringo-tabekata_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "18_ringo-tabekata"

CPS, PER_LINE = 4.40, 0.25

# STYLE LOCK — moi prompt cung mot chuoi nay de ca video mot tong (nhu video mau).
STYLE = ("simple flat Japanese educational illustration, soft warm pastel colours, "
         "clean rounded shapes with thin warm-brown outlines, gentle flat shading, "
         "generous white space, plain pure-white background, kind reassuring mood, "
         "wide 16:9 composition, main subject centred in the upper two thirds, "
         "a clean empty white band left along the bottom edge")
NEG_BASE = ("no photorealism, no 3D render, no dark heavy colours, no watermark, "
            "no logo, no signature, no doctors, no white coats, no extra people")
NEG_NOTEXT = NEG_BASE + ", no text, no letters, no numbers"

# Nhan vat co dinh (style-lock — lap nguyen van o moi canh co nguoi)
OJI = ("a gentle Japanese man in his late sixties with neat grey hair and round "
       "glasses, wearing a beige striped shirt and a dark olive apron")
MICHIKO = ("a kind Japanese woman of sixty-seven with short grey hair, wearing a "
           "mustard-yellow cardigan over a white blouse")
DRIVER = ("a sturdy cheerful Japanese man of seventy-two with short white hair and "
          "a warm weathered face, wearing a red-and-navy plaid flannel shirt")

# (line_idx, SCENE bo cuc, SUBJECT, TEXT nhan bake — None = khong chu)
PLAN = [
    # ── COLD OPEN ───────────────────────────────────────────────────────────
    (0, "the apple sits on a small plate at the centre, one clean bite taken out",
     "a shiny red apple on a small white plate on a breakfast table, morning mood",
     None),
    (4, "the calendar block stands at the left, the apple at the right, both large",
     "a very thick page-a-day paper calendar block with many thin pages beside one red apple",
     None),
    (6, "one long winding road climbs from the bottom left corner to the top right corner",
     "a long winding hill road dotted with many tiny red apples climbing upward into soft clouds",
     "1万回"),
    (9, "the eye at the left, the kidney at the right, both softly rounded",
     "a softly drawn human eye and a bean-shaped kidney with a few faint winding vessel lines "
     "around them, calm and gentle, nothing graphic",
     None),
    (10, f"he sits alone at a table filling the right half, a blank wall clock at the top left",
     f"{OJI}, sitting alone at an empty table in mid-afternoon, quietly biting an apple",
     None),
    (11, "he fills the right half holding a paper, a single sweat drop by his cheek",
     f"{OJI}, looking worried at a health check-up sheet with faint blank rows and one red "
     "pen circle, the print unreadable",
     None),
    (13, "he fills the centre, a small soft grey cloud floating above his head",
     f"{OJI}, resting his cheek on one hand, eyes tired, a fuzzy little grey cloud over his head",
     None),
    (15, "the apple at the centre, a hand lifting the tiny armour plate away toward the top edge",
     "a red apple wearing a tiny silver knight's breastplate, a hand gently lifting the "
     "breastplate off",
     None),
    # ── ITEM1 · AO GIAP THU NHAT: VO TAO ────────────────────────────────────
    (17, "the peel spirals down from the hands at the top into the sink at the bottom",
     "hands peeling a red apple, one long red spiral of peel falling into a kitchen sink",
     None),
    (19, "the apple fills the centre, large, with small sparkle marks on its skin",
     "an extreme close view of a glossy red apple with a bright natural shine and tiny sparkles",
     None),
    (21, "the apple stands proudly at the centre, small sparkles around the armour",
     "a red apple wearing a tiny shining silver knight's breastplate like proud armour",
     None),
    (23, "the pale apple at the centre, its spiral peel lying beside it, one small blue drop",
     "a peeled pale apple looking bare and cold, its removed red spiral peel lying on the "
     "table beside it, one small cold sweat drop",
     None),
    (25, "two apples side by side, under each a short stack of soft green blocks, the right "
     "stack twice as tall",
     "a peeled pale apple and an unpeeled red apple side by side, beneath each a small stack "
     "of soft green fibre blocks, the stack under the red apple twice as tall",
     "×2"),
    (27, "the hands and apple fill the centre under a simple tap, small circular arrows",
     "fingertips rubbing a red apple in gentle circles under running water, a few small "
     "circular motion arrows and water sparkles",
     None),
    (29, "the salt dish small at the left, the apple large at the right",
     "a tiny dish of white salt with a pinch being taken, beside a red apple",
     None),
    (32, "the bowl at the left, the small pot at the right, steam curling up",
     "a bowl of softly grated apple and a small pot of gently simmered apple slices with "
     "thin steam curls",
     None),
    (33, "neat rows of apples run across the middle of the frame",
     "tidy rows of red apples on a simple shop shelf, each apple with a gentle soft shine",
     None),
    (35, f"he stands at the sink filling the right half, holding the apple under the tap",
     f"{OJI}, smiling softly while washing a red apple under running water at a kitchen sink",
     None),
    (37, "the small armoured apple at the left, a larger empty suit of armour at the right "
     "under soft light",
     "a red apple in its tiny breastplate looking at a second, larger empty suit of silver "
     "armour standing on a simple stand, softly glowing",
     None),
    # ── PERSONA + KY UC ─────────────────────────────────────────────────────
    (39, "the kitchen runs the full width, an apron on a hook at the left, a kettle on the stove",
     "a tidy warm Japanese home kitchen with a hanging apron and a small kettle, nobody present",
     None),
    (40, "the hands and apple fill the centre, the peel curling down",
     "close view of hands peeling a red apple in one long unbroken spiral",
     None),
    (43, "one big soft round memory bubble fills the upper frame",
     "inside a soft round sepia-toned memory bubble, a Japanese mother peeling an apple at a "
     "low kitchen table while a small child watches, warm nostalgic colours",
     None),
    (45, "the smartphone stands at the centre, small bubbles floating around it",
     "a smartphone showing a simple soft map of Japan, small pastel comment bubbles and "
     "hearts floating around it",
     None),
    # ── LUONG + KALI + HUYET AP ─────────────────────────────────────────────
    (46, "one apple on a plate at the left, two apples on a plate at the right, a soft "
     "question mark floating between",
     "one red apple on a small plate and two red apples on another plate, a gentle rounded "
     "question mark floating between them",
     None),
    (48, "the balance scale fills the centre, the apple on the left pan",
     "a simple kitchen balance scale with one red apple on the left pan",
     "200g"),
    (50, "four apples piled on one small plate at the centre, one small worried drop above",
     "four red apples piled high on one small plate, a single small worried sweat drop "
     "floating above the pile",
     None),
    (52, "the kidney character at the left with one hand raised, the apple at the right, a "
     "small orange warning triangle above",
     "a soft bean-shaped kidney character politely raising one small hand as if saying wait, "
     "facing a red apple, a small rounded orange warning triangle floating above",
     None),
    (53, "the telephone at the left, the small clinic building at the right",
     "a simple home telephone and a small friendly clinic building with a soft cross-free "
     "sign, side by side",
     None),
    (54, "the apple at the centre sweeping toward an open door at the right edge",
     "a red apple pushing a small broom, sweeping little white salt cubes out through an "
     "open door",
     None),
    (56, "the monitor at the left with a blank screen, the apple at the right",
     "a home blood-pressure arm monitor with a completely blank screen, beside a red apple",
     None),
    (58, "the meal tray fills the lower half, the armoured apple resting on its rim",
     "a complete Japanese meal tray with rice and soup, a red apple in its tiny silver "
     "breastplate resting on the tray's rim",
     None),
    # ── MICHIKO (STAKE NHAN VAT 1) ──────────────────────────────────────────
    (61, "she fills the right half, a window at the left showing soft green tea fields",
     f"{MICHIKO}, standing in her bright kitchen, a window behind her showing soft green "
     "tea fields of Shizuoka",
     None),
    (63, "her hands at the top, the plate of thin fanned slices at the bottom centre",
     f"{MICHIKO}, peeling an apple and arranging thin pale slices in a neat fan on a small plate",
     None),
    (64, "she stands at the centre, eyes closed, soft scent swirls rising around her",
     f"{MICHIKO}, smiling with her eyes closed while soft pale scent swirls rise gently "
     "through the kitchen air",
     None),
    (65, "she fills the right half holding the sheet, one sweat drop by her cheek",
     f"{MICHIKO}, looking at a health check-up sheet with blank rows and one red pen circle, "
     "slightly worried, the print unreadable",
     None),
    (67, "she fills the centre, holding one apple slice with the red peel still on, head "
     "tilted slightly",
     f"{MICHIKO}, hesitantly holding up one apple slice with the red peel left on, tilting "
     "her head",
     None),
    (69, "she fills the centre biting a slice, small sparkles around her cheeks",
     f"{MICHIKO}, happily biting an apple slice with the peel on, small sparkles of "
     "enjoyment around her",
     None),
    (70, "the boy fills the centre biting a slice, a small music note floating above",
     "a small cheerful Japanese boy of about six happily biting an apple slice with the "
     "peel on, one small music note floating above his head",
     None),
    (72, "she sits small at the centre of a row of waiting chairs, calm soft light",
     f"{MICHIKO}, sitting quietly alone on a row of simple waiting-room chairs, hands in "
     "her lap, a calm content face",
     None),
    (73, "she fills the centre, both hands resting over her chest, a soft warm glow",
     f"{MICHIKO}, both hands gently over her chest, eyes soft, a warm pale glow around her",
     None),
    # ── CHECKPOINT + CTA ────────────────────────────────────────────────────
    (75, "the number stands huge at the centre, small apples around it",
     "one large friendly rounded number drawn in soft blue with a thin outline, small red "
     "apples floating around it",
     "2"),
    (76, "three rounded buttons in a row across the centre",
     "three soft rounded pastel buttons in a row: a thumbs-up, a small paper plane and a "
     "little bell, gentle sparkles",
     None),
    # ── AO GIAP THU HAI (TRA LOOP) ──────────────────────────────────────────
    (78, "the armoured apple at the left, the covered stand at the right",
     "a red apple in its tiny breastplate beside a display stand covered by a soft cloth, "
     "something hidden underneath",
     None),
    (79, "the winding apple road again climbs from the bottom left to the top right",
     "the same long winding hill road dotted with many tiny red apples climbing upward",
     "1万回"),
    (82, "the large armour stands at the centre, the cloth half lifted, soft light rays",
     "the larger empty suit of silver armour with its cloth cover half lifted, gentle "
     "light rays behind it",
     None),
    # dinh bai o line 83 nhung match cua 83 trung nguyen van voi line 134 (recap) →
    # cue dat o line 84 (duy nhat), hinh van la canh "khong mot minh" cua dinh bai
    (84, "the apple sits at the centre of a close warm circle of friends, soft glow around "
     "the whole group",
     "a red apple sitting closely together with a small white yogurt cup, a wedge of pale "
     "cheese and three almonds, a soft warm glow surrounding the group",
     None),
    (86, "the dark room fills the frame, a crescent moon in the window, the hand reaching "
     "from the right edge",
     "a dim bedroom at night with a crescent moon in the window, a hand quietly reaching "
     "for one apple slice on a bedside plate, a toothbrush in a cup nearby",
     None),
    (88, "the steep slope rises from the lower left to the upper right, the apple small, "
     "alone and struggling near the bottom, its tiny breastplate lying far behind",
     "a bare pale apple without its armour struggling alone up a steep grey-green slope, "
     "small sweat drops flying, the tiny silver breastplate left lying at the very bottom",
     None),
    (89, "the finished tray fills the lower half, the small dessert dish resting on its rim",
     "a finished Japanese meal tray with empty rice bowl, a small dish of red apple slices "
     "placed on the tray's rim as dessert, a spoon of white yogurt beside it",
     None),
    (90, "the friends form a ring around the apple at the centre, a faint shield glow",
     "a white yogurt cup, a wedge of cheese, a boiled egg and three almonds standing in a "
     "protective ring around a red apple, a faint round shield-like glow",
     None),
    (92, "the steep slope at the left melts into a long gentle slope toward the right edge",
     "a steep hill on the left smoothly flattening into a long gentle green slope on the "
     "right, a red apple rolling gently along the easy part, calm pastel sky",
     None),
    # ── MINORI TU THU ───────────────────────────────────────────────────────
    (93, "the hand enters from the bottom right holding one slice, the counter bare, cool "
     "morning tones",
     "a first-person view of a hand holding a single apple slice above an empty kitchen "
     "counter, early pale morning light",
     None),
    (95, "the teacup and empty plate at the centre, a soft grey wavy haze floating above",
     "a teacup and a small empty plate on a table, a soft grey wavy haze drawn hovering "
     "above them, heavy sleepy mood",
     None),
    (96, "the slice and yogurt bowl sit close together at the centre, bright and clear",
     "one apple slice beside a small bowl of white yogurt, bright cheerful morning colours, "
     "tiny sparkles",
     None),
    (99, "two small vignettes side by side: the left grey and hazy, the right sunny",
     "two small round vignettes: on the left an apple slice alone under a grey haze, on "
     "the right the same slice beside a yogurt bowl under a little sun",
     None),
    # ── JUICE + YAKI-RINGO ──────────────────────────────────────────────────
    (100, "the blender at the left, the full glass at the right",
     "a simple kitchen blender and a tall glass of pale apple juice side by side",
     None),
    (103, "the strainer at the top centre, juice pouring through, shreds staying behind",
     "a mesh strainer holding back soft pale fibre shreds while clear apple juice pours "
     "through into a glass below",
     None),
    (105, "the dish fills the centre, two baked halves, thin steam curling up",
     "two golden baked apple halves in a small dish, thin steam curls rising, cosy warm "
     "colours",
     None),
    (107, "the baked apple at the left, the yogurt dollop close beside it",
     "a golden baked apple half with a soft dollop of white yogurt right beside it on the "
     "same plate",
     None),
    (108, "the doorway at the right edge, the figure hurrying out biting an apple, a blank "
     "clock at the top left",
     f"{OJI}, hurrying out through a front door while biting an apple, a small bag on his "
     "shoulder, a blank wall clock above",
     None),
    (110, "the open fridge fills the frame, one shelf spot clearly empty",
     "an open home refrigerator, neat shelves, one spot where the yogurt should be clearly "
     "empty with a faint dotted outline",
     None),
    (111, "the egg and rice bowl stand close beside the apple, all three at the centre",
     "a boiled egg and a small bowl of white rice standing right beside a red apple like "
     "two steady friends",
     None),
    (112, "the tray moves along a gentle path from the left toward a small doorway at the "
     "right edge",
     "a small wooden tray carrying a red apple, a boiled egg and a yogurt cup together "
     "along a gentle path toward a little doorway",
     None),
    (113, "the armoured apple at the left, the friends-ring apple at the right, sparkles "
     "over both",
     "on the left a red apple wearing its tiny breastplate, on the right a red apple "
     "surrounded by a ring of yogurt, cheese and egg, gentle sparkles above both",
     None),
    (115, "the number stands huge at the centre, small apples around it",
     "one large friendly rounded number drawn in soft blue with a thin outline, small red "
     "apples floating around it",
     "3"),
    # ── DRIVER (STAKE NHAN VAT 2) ───────────────────────────────────────────
    (117, "he fills the right half, the truck cab behind him at the left, night sky with "
     "small stars",
     f"{DRIVER}, standing proudly beside his parked truck at night, a few small stars in "
     "a soft navy sky",
     None),
    (119, "the cab interior fills the frame, the window open at the left, breeze lines "
     "coming in",
     f"{DRIVER}, sitting in his truck cab at night biting an apple, the side window "
     "cracked open with soft breeze lines, a little radio glowing warmly on the dash",
     None),
    (122, "he sits on the bed edge at the centre, a warm bedside lamp at the right",
     f"{DRIVER}, in simple pyjamas sitting on the edge of his bed at night, biting an "
     "apple, a warm little bedside lamp glowing",
     None),
    (124, "he fills the centre laughing, one hand behind his head",
     f"{DRIVER}, laughing heartily with one hand behind his head, relaxed and carefree",
     None),
    (126, "the table fills the lower half, his finished tray with the apple dish on its "
     "rim, his wife across the table",
     f"{DRIVER}, sitting at the dinner table with a finished meal tray, a small dish of "
     "apple slices on the tray's rim, a gentle grey-haired wife smiling across the table, "
     "warm lamp light",
     None),
    (127, "he lies in bed at the centre staring up, the bedside table completely bare",
     f"{DRIVER}, lying awake in bed staring at the ceiling, the bedside table empty, a "
     "small moon in the window",
     None),
    (128, "she points gently at his face at the left, he looks surprised at the right, "
     "morning light",
     "a gentle grey-haired Japanese wife pointing softly at her husband's face with a "
     "happy surprised smile, the sturdy white-haired husband blinking, bright morning "
     "light through a window",
     None),
    (130, "he fills the centre scratching the back of his head, small warm sparkles",
     f"{DRIVER}, scratching the back of his head with a shy warm smile, small sparkles",
     None),
    # ── RECAP + KET ─────────────────────────────────────────────────────────
    (132, "two display stands side by side fill the centre",
     "two small wooden display stands: the left one holding a red apple wearing its "
     "red-peel breastplate, the right one holding a ring of yogurt, cheese and egg around "
     "an apple-shaped glowing space",
     None),
    (134, "the tray fills the lower half, the apple among its friends on top",
     "a meal tray carrying a red apple surrounded closely by a yogurt cup, a cheese wedge "
     "and a boiled egg, warm and complete",
     None),
    (136, "one long gentle slope runs across the whole frame, the couple small at the "
     "middle walking up",
     "a long gentle green slope under a warm pastel evening sky, an elderly Japanese "
     "couple walking easily up the path together carrying a small basket of red apples",
     None),
    (137, "the evening tray fills the centre under a warm lamp glow from above",
     "a Japanese dinner tray in warm evening lamp light with a small dish of red apple "
     "slices as dessert on its rim",
     None),
    (139, "the smartphone at the centre, the apple beside it, bubbles floating up",
     "a smartphone with soft pastel comment bubbles floating up from its screen, a red "
     "apple resting beside it",
     None),
    (140, "the hand enters from the top placing the whole apple onto the tray at the centre",
     "a hand gently placing one whole unpeeled red apple onto an evening meal tray",
     None),
    (142, "the bowl of apples sits at the centre of the table, the table fills the lower "
     "half, warm and wide",
     "a family dining table with a bowl of shiny red apples at its centre, teacups around, "
     "warm inviting colours",
     None),
    (143, "the booklet, glasses and teacup arranged calmly across the centre",
     "a closed plain booklet, a pair of reading glasses and a cup of green tea arranged "
     "quietly on a table",
     None),
    (144, "the table fills the lower half, the lamp glow from above, dusk colours",
     "a warm Japanese dining table at dusk with a bowl of red apples at the centre, two "
     "cushions set out, a soft lamp glow from above, peaceful closing mood",
     None),
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
        f"# Video 18 — {len(slides)} minh hoa AI (style theo video mau sA59aiPJYLA)\n\n"
        "> Slide TINH tren canvas trang, phu de den o dai trang duoi (sub_style `kuro`).\n"
        "> Ingest: `python tools\\ingest_slides_18.py <folder> --cut-x <do bang mat> --apply`\n"
        "> — tool CAT watermark ben phai roi PAD len 1920x1080 trang (dai sub 190px).\n\n"
        f"🔴 {ntext} canh co CHU BAKE (1万回 ×2 200g 2 3) — anh ve phai SOI TUNG KY TU,\n"
        "sai mot net la gen lai (media-library.md §2.9). Cac canh khac NEG cam chu.\n\n"
        "🔴 Nhan vat lap lai NGUYEN VAN mo ta (style-lock): ong cu ao soc + tap de olive ·\n"
        "道子さん cardigan vang mu tat · bac tai xe ao flannel ke do-navy.\n\n"
        f"**STYLE:** `{STYLE}`\n\n**NEG:** `{NEG_NOTEXT}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    idxs = [it[0] for it in PLAN]
    gaps = [starts[idxs[i]] - starts[idxs[i - 1]] for i in range(1, len(idxs))]
    print(f"OK  {n} minh hoa | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/canh | {n/(total/60):.2f} doi hinh/phut (tran 6, mau ~3-6)")
    print(f"    gap nho nhat {min(gaps):.1f}s | lon nhat {max(gaps):.1f}s | {ntext} canh co chu")
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
