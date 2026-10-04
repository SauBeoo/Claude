# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt MINH HOA AI cho video 21 (もち麦 × もう一つの台所).

    python tools\build_slides_21.py

Style theo khuon da chot tu video 18/20: minh hoa AI kawaii pastel nen TRANG, TINH,
~3 doi hinh/phut, phu de den o dai trang duoi day khung (khung san khau lam o
buoc ingest_slides_21.py, o day chi lo minh hoa + prompt).

SOI CHI CUA BAI: an du trung tam la 「もう一つの台所」(mot cai bep thu hai, vo hinh,
trong bung) — dai trang la hanh lang bep, vi khuan duong ruot la nhung dau bep tí hon
doi mu trang, もち麦 la nguyen lieu duoc mang toi. Anh phai ke MOT mach chuyen duy nhat
(cua bep dong -> mo -> vi khuan lam viec -> もち麦 la nguyen lieu -> ket cua bep sang den),
khong phai minh hoa roi tung cau don le.

CHU TRONG HINH (media-library.md §2.9): chi nhan NGAN, uu tien chu so Latin
(3種類 / もち麦 / 12g / 3:1 / 大さじ1 / 2週間 / 1 / 一週目 / 秋田県 / 富山県 / 12月) —
soi TUNG KY TU truoc khi nhan.

Xuat:
  04_SCRIPTS/21_mochimugi-choukatsu_SLIDES_photo.json
  06_VIDEO/21_mochimugi-choukatsu/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "21_mochimugi-choukatsu_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "21_mochimugi-choukatsu_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "21_mochimugi-choukatsu"

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

# Nhan vat co dinh (style-lock — lap NGUYEN VAN o moi canh co nguoi). Day la nhan vat
# CUA RIENG anecdote (KHONG phai cast minori/kikite — cast do dan o buoc ingest).
KEIKO = ("a Japanese woman in her mid sixties with short ash-brown hair, wearing a "
         "pale pink apron over a cream blouse, a gentle warm expression")
MASAO = ("a sturdy Japanese man in his early seventies with short grey hair, wearing "
         "a warm brown work jacket over a checked shirt, a calm weathered face")

# (line_idx, SCENE bo cuc, SUBJECT, TEXT nhan bake — None = khong chu)
PLAN = [
    # ═══ COLD OPEN — nghich ly can nang / bep bi khoa ═══
    (0, "a round bathroom scale sits at the left, a full rice bowl sits at the right, "
        "both plain and unchanged",
     "a simple round bathroom scale with a plain neutral dial face beside a full bowl "
     "of plain white rice, both ordinary and unchanged", None),
    (6, "a soft pale silhouette shape fills the frame, a small door glows at its centre",
     "a plain soft pale silhouette shape of a torso, with a small warm wooden door "
     "glowing gently at its centre, calm and a little mysterious", None),
    (10, "three small rounded cards line up across the middle of the frame",
     "three small rounded cards drawn kindly in a row, one showing a tired sleepy face, "
     "one showing a small sneeze, one showing a stomach with a soft question mark", None),
    (13, "a small empty basket sits at the left, a plump grain sack sits at the right",
     "a small empty wicker basket beside a plump cloth sack of grain waiting to be "
     "carried over, warm and inviting", None),

    # ═══ ITEM1 — mo cua: dai trang la hanh lang bep ═══
    (16, "a long soft tube runs across the frame from the left edge to the right edge, "
         "drawn like a cosy warm corridor",
     "a large friendly cutaway of the large intestine drawn as a warm cosy kitchen "
     "corridor with soft pastel pink walls", None),
    (19, "a few tiny characters stand together across the middle of the corridor",
     "a few tiny round pastel bacterium characters, each wearing a small white chef "
     "hat with simple friendly dot eyes, standing together in the corridor", None),
    (21, "two ceramic containers sit side by side at the centre",
     "a jar of miso paste and a small dish of natto beans sitting side by side on a "
     "plain counter, drawn warmly", None),
    (23, "three small bottles stand in a row across the middle",
     "three small rounded glass bottles standing in a row, each a slightly different "
     "soft pastel colour, drawn plainly", "3種類"),
    (25, "a section of corridor wall runs along the bottom edge, small warm patches "
         "glow along it",
     "a section of the cosy kitchen corridor wall with small warm glowing patches "
     "being gently repaired by tiny chef bacterium characters", None),

    # ═══ もち麦 hero + so lieu ═══
    (29, "a plump cloth grain sack glows warmly at the centre",
     "a plump cloth sack with grain spilling gently out of it, mochi mugi pearl barley "
     "glowing warmly, drawn as the hero of the scene", "もち麦"),
    (31, "two rice bowls sit side by side at the centre, one plain and one speckled",
     "two bowls of rice side by side, one of plain white rice and one speckled with "
     "mochi mugi grains mixed in, shown as a gentle comparison", None),
    (34, "a small official looking paper sits at the centre",
     "a small clean paper chart with two simple soft bars on it, drawn plainly and "
     "trustworthy, calm colours", "食物繊維の目標量"),
    (37, "a small bowl of grain sits at the left, a measuring line runs at the right",
     "a small bowl of mochi mugi grain beside a simple soft measuring scale line "
     "showing its fibre content", "12g"),
    (41, "three scoops of white rice sit at the left, one scoop of mochi mugi sits at "
         "the right",
     "three identical scoops of plain white rice lined up beside one scoop of mochi "
     "mugi grain, shown as a simple ratio comparison", "3:1"),
    (44, "a wooden measuring spoon holds grain at the centre, a rice cooker sits behind "
         "it",
     "a wooden tablespoon holding a small mound of mochi mugi grain, a rice cooker "
     "open and waiting behind it", "大さじ1"),

    # ═══ persona + confession ═══
    (47, "a warm kitchen counter fills the frame",
     "a bright tidy Japanese kitchen counter with a teapot, two cups and a small vase "
     "of pale flowers", None),
    (55, "a cluttered small bag and measuring tools sit scattered across the centre",
     "a small cloth bag, a measuring cup and a spoon scattered messily on a counter, "
     "looking like too much trouble", None),
    (58, "one wooden spoon rests calmly at the centre",
     "a single wooden tablespoon resting beside a rice cooker, simple and calm, the "
     "earlier clutter gone", None),

    # ═══ mien dich + duong huyet ═══
    (61, "a small warm shield glows over a section of corridor wall",
     "a small soft round shield shape glowing warmly over a section of the cosy "
     "kitchen corridor wall", None),
    (64, "many tiny soft dots gather along the corridor wall",
     "many tiny soft pastel dot shapes gathered densely along the inner wall of the "
     "kitchen corridor, drawn kindly", None),
    (67, "a soft gel-like film coats the inside of a bowl at the centre",
     "a bowl of rice with a soft translucent gel-like film gently coating the grains "
     "inside it", None),
    (72, "a hand pauses mid motion at the centre of a kitchen counter",
     "a hand pausing mid task on a kitchen counter in soft afternoon light, a gentle "
     "drowsy glow around it", None),

    # ═══ anecdote 恵子さん (富山県) ═══
    (76, "a small rounded map card sits at the centre",
     "a small warm rounded card showing a map pin over a stylised region shape, calm "
     "and inviting", "富山県"),
    (78, "a small shop counter fills the frame",
     KEIKO + ", standing behind a small lunch box shop counter lined with neat boxes, "
     "a warm gentle expression", None),
    (81, "a row of potted plants sits at the left, a small watering can rests at the "
         "right",
     KEIKO + ", watering a row of small potted plants in the evening light outside "
     "her shop, calm and unhurried", None),
    (84, "a small calendar hangs at the left, a bowl of rice sits at the right",
     "a small wall calendar with two weeks marked in soft colour, beside a bowl of "
     "rice with mochi mugi mixed in", "2週間"),
    (87, "a figure stands lightly at the centre, a soft glow around the torso",
     KEIKO + ", standing with a light relieved posture, a soft warm glow around her "
     "torso", None),

    # ═══ CTA giua ═══
    (90, "a smartphone lies at the centre, a soft heart and speech bubble above it",
     "a smartphone lying on a table with a gentle heart mark and a small speech "
     "bubble floating above", None),

    # ═══ canh bao than + NG habit ═══
    (94, "a small caution card sits alone at the centre",
     "a small rounded card drawn calmly and kindly, showing a simple soft caution "
     "mark, not alarming", None),
    (95, "a kidney-shaped icon sits at the centre, drawn gently",
     "a small kidney-shaped icon drawn plainly and kindly beside a tiny measuring "
     "spoon", None),
    (99, "a fallen cloth sack lies at the centre, a few grains spilled beside it",
     "a cloth sack of grain tipped over and left on a counter, a few grains spilled "
     "beside it, looking forgotten", None),
    (101, "a soft rounded stomach shape sits at the centre with a small swirl icon "
          "above it",
     "a soft rounded stomach shape with a small swirling discomfort icon above it, "
     "drawn kindly and not alarming", None),
    (105, "one small plain card sits alone at the centre",
     "a single small rounded card with a plain surface, waiting to be revealed, calm "
     "and simple", "1"),

    # ═══ TRA OPEN LOOP ═══
    (110, "a bowl overflows at the centre, tiny characters look startled at the sides",
     "a rice bowl overflowing with grain spilling over its edge, a few tiny chef "
     "bacterium characters looking startled beside it", None),
    (113, "a calendar strip runs across the frame, tiny characters settle along it",
     "a two-week calendar strip with the tiny chef bacterium characters gradually "
     "looking calmer and more settled along it", "2週間"),
    (116, "a small staircase rises from the bottom left corner toward the top right "
          "corner, one spoon rests on the first step",
     "a small gentle staircase with a single wooden spoon of grain resting on its "
     "first step", "一週目"),
    (118, "the staircase reaches its top step at the centre, a full bowl sits there",
     "the same gentle staircase now reaching its top step, where a bowl showing the "
     "three to one ratio sits proudly", "3:1"),

    # ═══ anecdote 正雄さん (秋田県) ═══
    (122, "a small rounded map card sits at the centre",
     "a small warm rounded card showing a map pin over a stylised snowy region shape, "
     "calm and inviting", "秋田県"),
    (124, "a snowplow sits at the left, a small figure stands beside it",
     MASAO + ", standing beside a small pale snowplow truck at dusk in winter, a calm "
     "weathered expression", None),
    (127, "a steaming teacup sits at the centre",
     MASAO + ", holding a warm teacup with gentle steam rising, sitting at a small "
     "shop counter", None),
    (129, "a wooden spoon of grain sits at the left, a snowy window glows at the "
          "right",
     "a wooden tablespoon of mochi mugi grain beside a small snowy window at night, "
     "warm indoor light", None),
    (131, "a calendar page sits at the left, a figure stands with a soft glow at the "
          "right",
     "a calendar page marked December beside " + MASAO + " standing with a light "
     "healthy glow, calm and well", "12月"),

    # ═══ recap + ket 4 lop ═══
    (135, "the kitchen door glows warmly at the centre, standing wide open now",
     "the same small wooden door from the opening scene, now standing open and "
     "glowing warmly, tiny chef characters visible working happily inside", None),
    (138, "a gentle winding path runs from the bottom left corner to the top right "
          "corner",
     "a small gentle winding path drawn calmly, easy and unhurried, leading toward a "
     "warm light", None),
    (141, "a speech bubble floats at the centre above a notebook",
     "a soft rounded speech bubble floating above a notebook and pen, inviting and "
     "warm", None),
    (143, "a thumbs-up icon sits at the left, a small bell icon sits at the right",
     "a simple rounded thumbs-up icon beside a small bell icon, both drawn kindly and "
     "softly", None),
    (146, "a small clean leaflet sits at the centre",
     "a small clean health leaflet and a pen resting on a plain table, calm and "
     "trustworthy", None),
    (150, "a warm dinner table fills the frame, a bowl steams at the centre",
     "a simple warm Japanese dinner table at night with a bowl of rice mixed with "
     "mochi mugi steaming gently under a soft lamp", None),
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
        f"# Video 21 — {len(slides)} minh hoa AI (もち麦 × もう一つの台所)\n\n"
        "> Slide TINH tren canvas trang, khung san khau + cast + phu de lam o buoc\n"
        "> `ingest_slides_21.py` (buoc sau, khi da co anh).\n\n"
        f"🔴 {ntext} canh co CHU BAKE (3種類 / もち麦 / 食物繊維の目標量 / 12g / 3:1 ×2 / "
        "大さじ1 / 富山県 / 2週間 ×2 / 一週目 / 1 / 秋田県 / 12月)\n"
        "— uu tien chu so Latin cho de gen dung; van phai SOI TUNG KY TU truoc khi nhan.\n\n"
        "🔴 Nhan vat lap NGUYEN VAN mo ta (style-lock, RIENG cua anecdote — khac cast "
        "minori/kikite dan o buoc ingest):\n"
        f"- 恵子さん: `{KEIKO}`\n- 正雄さん: `{MASAO}`\n\n"
        "⭐ AN DU XUYEN SUOT: dai trang duoi day + hanh lang bep hong nhat mo dau o slide_04, "
        "vi khuan dau bep tí hon xuat hien tu slide_05, cua bep 'mo lai' o slide cuoi cung "
        "(slide_44) — kiem tra mach chuyen nay LIEN TUC khi soi anh, dung chi soi tung anh don le.\n\n"
        f"**STYLE:** `{STYLE}`\n\n**NEG:** `{NEG_NOTEXT}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    idxs = [it[0] for it in PLAN]
    gaps = [starts[idxs[i]] - starts[idxs[i - 1]] for i in range(1, len(idxs))]
    print(f"OK  {n} minh hoa | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/canh | {n/(total/60):.2f} doi hinh/phut (tran 6, mau ~3-4)")
    print(f"    gap nho nhat {min(gaps):.1f}s | lon nhat {max(gaps):.1f}s | {ntext} canh co chu")
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
