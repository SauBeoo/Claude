# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt MINH HOA AI cho video 20 (脳梗塞 × 前の晩).

    python tools\build_slides_20.py

Style theo khuon da chot tu video 18: minh hoa AI kawaii pastel nen TRANG, TINH,
~3-4 doi hinh/phut, phu de den o dai trang duoi day khung (sub_style "kuro").

SOI CHI CUA BAI: 前の晩 -> 朝. Anh phai ke duoc mot cau chuyen, khong phai
minh hoa roi tung cau: buoi sang cua 和夫さん -> co che かさぶた -> buoi toi
quyet dinh buoi sang -> hai nhan vat, hai ket cuc.

CHU TRONG HINH (media-library.md §2.9): chi nhan NGAN, uu tien chu so Latin
(30秒 / 2日後 / 2時間 / 7.5g / 半分 / 2.7倍 / 3つ) — soi TUNG KY TU truoc khi nhan.

Xuat:
  04_SCRIPTS/20_nokosoku-kasabuta_SLIDES_photo.json
  06_VIDEO/20_nokosoku-kasabuta/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "20_nokosoku-kasabuta_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "20_nokosoku-kasabuta_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "20_nokosoku-kasabuta"

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

# Nhan vat co dinh (style-lock — lap NGUYEN VAN o moi canh co nguoi)
KAZUO = ("a sturdy Japanese man of seventy-four with short white hair and a kind "
         "weathered face, wearing a grey zip-up work jacket over a navy polo shirt")
WIFE = ("a small Japanese woman of seventy with grey hair in a low bun, wearing a "
        "soft green apron over a beige blouse")
FUMIE = ("a slender Japanese woman of sixty-nine with softly waved grey hair, "
         "wearing a lavender knit cardigan over a cream blouse")

# (line_idx, SCENE bo cuc, SUBJECT, TEXT nhan bake — None = khong chu)
PLAN = [
    # ═══ COLD OPEN — canh buoi sang cua 和夫さん ═══
    (0, "the futon fills the lower half, the window light comes from the left",
     KAZUO + ", just awake and sitting up on a futon in a quiet tatami room, morning light",
     None),
    (5, "the calendar hangs at the left, an empty futon lies at the right",
     "a small wall calendar with two days circled in soft red, beside a neatly folded empty futon "
     "in the same quiet tatami room", "2日後"),
    (9, "one long tube crosses the frame from the left edge to the right edge",
     "a large cutaway of a smooth pale pink tube with a small brown crust stuck on its inner wall, "
     "drawn simply and kindly", None),
    (12, "the clock stands at the centre, a soft sunrise glow behind it",
     "a round wall clock with a gentle two-hour arc marked in warm orange, a soft sunrise behind it",
     "2時間"),
    (16, "the evening table fills the frame, one small lamp glows above it",
     "a simple Japanese dinner table at night seen from the side, a bowl of noodle soup and a small "
     "rice bowl under a warm hanging lamp", None),

    # ═══ (1) CAI VAY HINH THANH — muoi ═══
    (20, "the knee at the left, the same tube at the right, both large and clear",
     "a scraped knee with a small neat scab beside a cutaway tube with an identical small scab "
     "on its inner wall, shown as a friendly comparison", None),
    (24, "the tube runs across the frame, the passage narrowing toward the right edge",
     "a cutaway tube whose inner crust grows thicker step by step so the open channel becomes narrow, "
     "drawn in four gentle stages", None),
    (28, "the salt shaker at the left, a swelling water drop at the right",
     "a small ceramic salt shaker beside a round water droplet that is visibly swollen and heavy",
     None),
    (31, "the hose runs from the bottom left corner up to the top right corner",
     "a garden hose with strong water rushing through it, the inner wall shown worn and scuffed "
     "where the water presses hardest", None),
    (34, "two plates sit side by side at the centre, each with a small salt mound",
     "two simple white plates each holding a small mound of salt, one slightly larger than the other, "
     "with a thin measuring line under each", "7.5g"),
    (38, "three bowls line up across the middle of the frame",
     "a ramen bowl, a soba bowl and a hotpot bowl lined up in a row, each still holding soup", None),
    (41, "the bowl at the centre, a pair of chopsticks resting across it",
     KAZUO + " looking a little guilty at a noodle bowl he has just emptied, chopsticks resting on top",
     None),
    (45, "the bowl at the centre with the broth filled only to its middle",
     "a noodle bowl left with exactly half of its soup remaining, a soft arrow pointing to the "
     "remaining half", "半分"),

    # ═══ (1b) an nhanh ═══
    (48, "the table fills the frame, the chopsticks laid down at the right",
     "a pair of chopsticks laid neatly on a chopstick rest beside a half eaten meal, calm and unhurried",
     None),
    (51, "three small clocks in a row across the middle",
     "three small clocks in a row marking breakfast, lunch and dinner, each with a tiny rice bowl "
     "under it", None),
    (55, "hands at the centre, the chopsticks being placed down",
     WIFE + " gently setting her chopsticks down on the rest between bites at a bright table", None),

    # ═══ persona + canh bao ═══
    (59, "the kitchen counter fills the frame, warm and tidy",
     "a bright tidy Japanese kitchen counter with a teapot, two cups and a small vase of yellow flowers",
     None),
    (63, "a simple map of Japan sits at the centre",
     "a soft rounded map of the Japanese islands with several small warm dots scattered on it", None),
    (67, "the pill case at the left, the doctor's desk sign at the right",
     "a weekly pill organiser box beside a small clipboard and a pen on a clean desk", None),
    (70, "two figures at the centre, one listening to the other",
     WIFE + " talking calmly with a pharmacist figure drawn only from behind, over a counter", None),

    # ═══ (2) CAI VAY LON LEN — mo cu ═══
    (73, "the tube crosses the frame, a soft yellow lump swelling on its inner wall",
     "a cutaway tube with a pale yellow fatty lump swelling out from the crust on its inner wall",
     None),
    (76, "the frying pan at the left, an old oil bottle at the right",
     "a used frying pan with darkened oil beside a cloudy oil bottle, drawn plainly", None),
    (79, "the plastic tray at the centre, a small clock beside it",
     "a supermarket tray of fried food covered with film, a small clock beside it showing the next day",
     None),
    (84, "three small cards in a row across the middle",
     "three small rounded cards showing a shop bag, a piece of fried food with its coating half "
     "peeled off, and a crossed-out next-day calendar", "3つ"),
    (89, "three fish lie in a row on one long plate",
     "a mackerel, a sardine and a horse mackerel lying side by side on a long pale plate", None),
    (93, "the open can at the left, the grated radish at the right",
     "an opened mackerel can tipped onto a small plate with a mound of grated white radish beside it",
     None),
    (97, "four vegetables arranged in an arc across the middle",
     "a piece of pumpkin, a carrot, a bundle of spinach and a broccoli floret arranged in a gentle arc",
     None),
    (100, "one plate at the centre, everything on it the same brown tone",
     "a dinner plate holding only brown coloured food, drawn plainly so the lack of colour is obvious",
     None),
    (105, "one bowl at the centre with two small icons above it",
     "a ramen bowl with a tiny salt shaker icon and a tiny oil drop icon hovering above it side by side",
     None),
    (107, "a week strip runs across the frame",
     "a simple seven day strip with fried food drawn on one day only and light meals on the others",
     None),

    # ═══ anecdote 和夫さん ═══
    (112, "the taxi at the left, the small dish at the right",
     KAZUO + " standing beside a small pale taxi at dusk, a set of keys in his hand", None),
    (116, "the night table fills the frame, one cup noodle at the centre",
     KAZUO + " sitting alone at a small table at night with one instant noodle cup in front of him",
     None),
    (120, "a long ribbon of small nights runs from the left edge to the right edge",
     "a long ribbon made of many tiny repeated night scenes with one noodle cup in each, ending at a "
     "small sunrise", "30秒"),

    # ═══ CTA giua ═══
    (122, "the phone at the centre, a soft heart and speech bubble above it",
     "a smartphone lying on a table with a gentle heart mark and a small speech bubble floating above",
     None),

    # ═══ (3) CAI VAY BONG RA — 2 tieng buoi sang ═══
    (125, "the clock fills the centre, a warm arc drawn over its upper right",
     "a large round clock with a warm orange arc drawn over the two hours after waking, a small sun "
     "rising behind", "2時間"),
    (128, "the tube crosses the frame, one piece of the crust breaking free",
     "a cutaway tube where a piece of the inner crust has just broken loose and is drifting along "
     "the channel, drawn calmly", None),
    (132, "one line graph runs from the bottom left up to the top right",
     "a soft line that stays low through a sleeping moon then rises sharply at a rising sun", None),
    (135, "the clock face at the centre with a shaded band from eight to twelve",
     "a round clock face with the segment from eight to twelve shaded in warm orange", None),
    (137, "the sleeping figure at the left, small vapour marks rising at the right",
     KAZUO + " sleeping peacefully under a quilt with tiny soft vapour marks rising from him", None),
    (141, "two glasses side by side at the centre",
     "two glasses of the same size, one holding clear thin liquid and the other holding a thicker "
     "cloudier liquid, shown as a friendly comparison", None),

    # ═══ FAST ═══
    (145, "the figure at the centre, one arm hanging lower than the other",
     WIFE + " noticing that one of her arms will not lift as high as the other, a gentle worried face",
     None),
    (149, "the telephone at the centre, three large digits beside it",
     "a home telephone handset being lifted, with three clear digits beside it", "119"),
    (152, "the hourglass at the left, an ambulance drawn small at the right",
     "a small hourglass beside a simple pale ambulance drawn kindly and without alarm", None),

    # ═══ dem lanh ═══
    (157, "the corridor runs from the warm room at the left to the cold door at the right",
     "a warm lit tatami room on one side and a chilly bare corridor on the other, a soft temperature "
     "difference shown by colour", None),
    (161, "the changing room at the left, a small heater at the right",
     "a small bathroom changing area with a compact heater switched on and a folded towel", None),

    # ═══ CU LAT — 前の晩に決まる ═══
    (165, "the morning window at the left, a locked gate drawn faintly at the right",
     "a bright morning window beside a closed gate drawn in faint grey, showing that the morning "
     "cannot be changed", None),
    (170, "three small cards in a row across the middle of the frame",
     "three small rounded cards in a row showing a glass of water, a bowl with half its soup, and a "
     "pinch of green seaweed", "3つ"),
    (173, "the bedside table at the centre with one glass on it",
     "a glass of water standing on a small bedside table beside a folded futon at night", None),
    (177, "the dinner bowl at the centre, half of its soup gone",
     "a miso soup bowl at a night table with half of its soup remaining, a chopstick rest beside it",
     None),
    (181, "the dried seaweed at the left, the bowl at the right",
     "a small pinch of dried black wakame beside an empty lacquer bowl on a night table", None),
    (184, "the bowl fills the centre, green seaweed opening inside it",
     "a lacquer bowl of hot miso soup with green wakame slowly unfurling in the broth, gentle steam "
     "rising", None),
    (188, "the tube at the left, small salt grains leaving it at the right",
     "a cutaway tube with tiny salt grains being carried gently out and away along the channel", None),

    # ═══ 3 canh bao ═══
    (192, "three small cards in a row across the middle",
     "three small rounded warning cards drawn kindly, showing a kidney shape, a pill packet and a "
     "piece of kelp", None),
    (195, "the kelp at the centre, a small measuring spoon beside it",
     "a folded sheet of dried kelp beside a small measuring spoon, drawn plainly", None),
    (198, "the calendar strip runs across the frame",
     "a long calendar ribbon where the same small pinch of seaweed is drawn on every day, running "
     "into the distance", None),

    # ═══ anecdote ふみ江さん ═══
    (202, "the salon chair at the left, the mirror at the right",
     FUMIE + " standing beside a simple salon chair and a round mirror, a warm calm expression", None),
    (206, "the night table fills the frame, two glasses on it",
     FUMIE + " and her husband drawn from behind, sitting at a night table with two glasses of water "
     "and two small bowls", None),
    (211, "the path runs from the bottom left corner toward the top right corner",
     "two elderly figures drawn small from behind, walking together along a gentle tree lined path",
     None),

    # ═══ khep vong 和夫さん ═══
    (214, "two bowls side by side at the centre, one clearly smaller",
     WIFE + " placing a smaller bowl beside the old larger one on a night table", None),
    (218, "the tube at the left, the clock at the right, a small bowl below",
     "a cutaway tube, a round clock and a small bowl of seaweed soup arranged as three linked steps",
     None),
    (221, "three cards in a row above one moon",
     "a glass of water, a half filled soup bowl and a pinch of seaweed drawn in a row under a small "
     "calm moon", None),
    (224, "the bowl at the centre, one pinch of seaweed falling into it",
     "a hand dropping a small pinch of dried wakame into a lacquer bowl, drawn close and warm", None),
    (227, "the phone at the centre with three small icons above",
     "a smartphone on a table with a glass, a bowl and a seaweed pinch drawn as three small choices "
     "above it", None),
    (231, "the desk at the centre, a leaflet and a pen on it",
     "a clean desk with a simple health leaflet and a pen, drawn calm and trustworthy", None),
    (233, "two pairs of hands at the centre over one open notebook",
     "two pairs of hands, one older and one younger, resting together over an open notebook and a "
     "pen on a bright table, warm and reassuring", None),
    (236, "the bowl fills the centre, softly steaming",
     "a lacquer bowl of miso soup with green wakame, steam rising gently, warm evening light", None),
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
        f"# Video 20 — {len(slides)} minh hoa AI (脳梗塞 × 前の晩)\n\n"
        "> Slide TINH tren canvas trang, phu de den o dai trang duoi (sub_style `kuro`).\n"
        "> Ingest: `python tools\\ingest_slides_20.py <folder> --cut-x <do bang mat> --apply`\n\n"
        f"🔴 {ntext} canh co CHU BAKE (2日後 / 2時間 ×2 / 7.5g / 半分 / 3つ ×3 / 30秒 / 119)\n"
        "— uu tien chu so Latin cho de gen dung; van phai SOI TUNG KY TU truoc khi nhan.\n\n"
        "🔴 Nhan vat lap NGUYEN VAN mo ta (style-lock):\n"
        f"- 和夫さん: `{KAZUO}`\n- 奥さま: `{WIFE}`\n- ふみ江さん: `{FUMIE}`\n\n"
        "⚖️ NEG cam bac si/ao blouse/giuong benh/mau — de tai la benh cap cuu nhung anh phai\n"
        "GIU TONG AM, khong doa (persona みのり + `youtube-compliance.md` §5).\n\n"
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
