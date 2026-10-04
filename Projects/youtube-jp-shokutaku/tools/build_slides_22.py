# -*- coding: utf-8 -*-
r"""Dung SLIDES + prompt MINH HOA AI cho video 22 (ラーメン x 水道管、血管を守る).

    python tools\build_slides_22.py

Style theo khuon da chot tu video 18/20/21: minh hoa AI kawaii pastel nen TRANG,
TINH, khung san khau + cast lam o buoc ingest_slides_22.py (o day chi lo minh
hoa nen + prompt).

SOI CHI CUA BAI (MOT AN DU DUY NHAT, khong roi rac):
血管 = mot duong ong nuoc chay khap nha (mot cai cutaway ong nuoc chay xuyen
tu trai sang phai khung, xuat hien tu slide_06 va CHAY LAI moi khi quay ve chu
de chinh). Ba canh bao la BA CACH ong nay hong: muoi lam ong CUNG (slide 08-09),
mo lam ong TAC (slide 20-24 — an du ong thoat nuoc bep), duong huyet tang vot
lam ong RI SET (slide 35-36). Ket bai la ong SACH, chay deu (slide 50).
KHONG duoc minh hoa 3 canh bao bang 3 vat the khong lien quan — moi slide canh
bao deu phai con NHIN RA duong ong o dau do trong khung (chi tiet nen, khong
can to).

NHIP HINH (audience-45plus.md §2.0 + feedback_nhip_hinh_san_7s):
  ① TRAN doi HERO <=6/phut — 53 slide / ~16'15 = 3.3/phut, RAT DUOI tran.
  ② SAN su kien <=7s — LOP NAY o day KHONG lo, se lam o buoc
     `remotion-vox/tools/build_overlays_22.py` (lop sticker/tag rieng, dung
     picto co san `ex_hatena/ex_hirameki/ex_hiyari/ex_mukumi/ex_furatsuki`).
     Slide hero o day chi lo phan TRAN (cat canh chinh), KHONG chua bang cach
     nhoi them slide cho day 7s — dung sai tang (`render-background.md` triet
     ly "mot viec mot tang").

CHU TRONG HINH (media-library.md §2.9): chi nhan NGAN, uu tien chu so Latin
(3つ / 6g / 7.5g / 6.5g / 5g / 6-8g / 半分 / 週1 / 三重県 / 山形県) — soi TUNG
KY TU truoc khi nhan.

Xuat:
  04_SCRIPTS/22_ramen-kekkan_SLIDES_photo.json
  06_VIDEO/22_ramen-kekkan/slide_prompts_FLOW.txt / _TENFILE.txt / _BLOCKS.md
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TTS = ROOT / "04_SCRIPTS" / "22_ramen-kekkan_TTS.md"
OUT_JSON = ROOT / "04_SCRIPTS" / "22_ramen-kekkan_SLIDES_photo.json"
VD = ROOT / "06_VIDEO" / "22_ramen-kekkan"

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

# An du trung tam — nhac lai NGUYEN VAN moi lan dung, de anh AI giu dung mach.
PIPE = ("a single friendly cutaway water pipe running horizontally across the "
        "lower third of the frame, drawn as a simple soft-grey rounded tube "
        "embedded in a pale kitchen wall")

# Nhan vat co dinh cho 2 anecdote (style-lock, RIENG — khac cast minori/kikite
# dan o buoc ingest).
SHOJI = ("a sturdy Japanese man in his late sixties with short grey hair, "
         "wearing a faded blue work jacket over a plain shirt, a calm "
         "weathered face")
SACHIKO = ("a Japanese woman in her early seventies with short silver hair, "
           "wearing a soft lavender cardigan over a cream blouse, a gentle "
           "warm expression")

# (line_idx, SCENE bo cuc, SUBJECT, TEXT nhan bake hoac None)
PLAN = [
    # === COLD OPEN — bat kinh vao to ramen, tu ngo den canh bao ===
    (0, "a large steaming ramen bowl fills most of the frame, gentle steam curls "
        "rising from it",
     "a large ceramic ramen bowl full of noodles and rich broth, soft steam "
     "curling upward, warm and inviting", None),
    (1, "a hand tips the bowl up toward the frame, about to drink the broth",
     "a hand tipping a ramen bowl upward, about to drink the last of the broth, "
     "warm kitchen light", None),
    (3, "a hand rests at the centre wearing a slightly tight ring, a small "
        "worried sparkle mark beside it",
     "a hand wearing a plain gold ring that looks a little tight on the finger, "
     "a small soft worried sparkle mark beside it", None),
    (4, "a blood pressure cuff wraps an arm at the centre, a small round dial "
        "beside it",
     "a simple home blood pressure cuff wrapped around an upper arm, a small "
     "round dial gauge beside it, calm colours", None),
    (5, "a small bowl of pale thin miso soup sits at the centre, looking a "
        "little plain",
     "a small bowl of very pale thin miso soup, looking plain and a little "
     "unsatisfying, drawn kindly", None),
    (8, PIPE + ", faint and just becoming visible behind a small kitchen scene",
     PIPE + ", faint and just becoming visible, with a small cosy kitchen "
     "corner drawn in front of it", None),

    # === ITEM1 — chinh thuc gioi thieu duong ong + muoi lam CUNG ===
    (11, PIPE + ", now clearly drawn and centred",
     PIPE + ", clearly drawn, plain and calm, introduced as the main subject "
     "of the scene", None),
    (15, "the same pipe now shown soft and flexible, gently curving",
     "the same friendly water pipe drawn soft, flexible and slightly curved, "
     "young and healthy looking", None),
    (17, "the same pipe now shown stiffer, with small hard cracked patches "
         "along its surface",
     "the same water pipe now drawn stiffer, with small rough hard patches "
     "along its surface, aging but not alarming", None),
    (20, "a small clean official chart card sits at the centre with two soft "
         "bars",
     "a small clean paper chart with two simple soft bars side by side, "
     "trustworthy and calm colours", "7.5g / 6.5g"),
    (21, "a single stricter bar chart sits at the centre, slightly shorter",
     "a small clean paper chart with one single shorter soft bar, drawn "
     "plainly, trustworthy", "6g"),
    (22, "one more chart card sits at the centre, the shortest bar yet",
     "a small clean paper chart with one very short soft bar, the strictest "
     "of the three, drawn plainly", "5g"),
    (23, "a ramen bowl sits at the centre with a small rising gauge beside it",
     "a ramen bowl of broth beside a small simple rising gauge dial, showing "
     "a high reading, calm colours", "6-8g"),
    (24, "a small kitchen scale tips fully to one side at the centre",
     "a small kitchen scale with its dial tipped all the way to one side, "
     "drawn plainly, a little surprising but not alarming", "1日分"),
    (27, "a hand pushes a half-full ramen bowl gently aside at the centre",
     "a hand gently pushing a ramen bowl aside with the broth level now at "
     "half, calm and simple", "半分"),
    (28, "a small bowl of rice tips toward a leftover soup bowl at the centre, "
         "a soft caution mark above it",
     "a small bowl of plain rice tipping toward a bowl of leftover ramen "
     "broth, a small soft caution mark above it, not alarming", None),
    (30, "a ramen bowl sits calmly at the centre with the broth at half level",
     "a ramen bowl sitting calmly with its broth at exactly half level, warm "
     "and reassuring, drawn plainly", None),
    (32, "two small bowls sit side by side at the centre, one with noodles and "
         "one with dipping broth",
     "two small bowls side by side, one holding plain noodles and one holding "
     "a separate dipping broth, tsukemen style, drawn plainly", None),
    (36, "a warm kitchen counter fills the frame, a teapot and two cups sit at "
         "the centre",
     "a bright tidy Japanese kitchen counter with a teapot, two cups and a "
     "small vase of pale flowers", None),

    # === persona break — canh bao thuoc ===
    (47, "a small pill bottle sits at the left, a plain ramen bowl sits at the "
         "right",
     "a small plain pill bottle beside a simple ramen bowl on a kitchen "
     "counter, calm and not alarming", None),

    # === ITEM2 — mo lam TAC (an du ong thoat nuoc bep) ===
    (48, PIPE + ", the camera has moved further along its length",
     PIPE + ", shown further along its length, plain and calm", None),
    (50, "a bowl of broth sits at the centre with a thin oily sheen on the "
         "surface",
     "a bowl of ramen broth with a thin glistening oily sheen visible on the "
     "surface, drawn plainly", None),
    (53, "a section of kitchen drain pipe sits at the centre, a little grease "
         "clinging to its inner wall",
     "a simple cutaway of a kitchen drain pipe with a little soft yellow "
     "grease clinging gently to its inner wall, not alarming", None),
    (55, "the same water pipe from earlier now shows a narrower inner channel, "
         "clogged along one side",
     "the same friendly water pipe now drawn with its inner channel visibly "
     "narrower and clogged along one side with the same soft yellow grease", None),
    (57, "three small ramen bowls sit in a row at the centre, each a slightly "
         "different shade",
     "three small ramen bowls in a row, one light golden broth, one pale "
     "clear broth, one rich creamy broth, shown as a simple comparison", None),
    (59, "a spoon skims a thin layer off the top of a bowl at the centre",
     "a Chinese soup spoon gently skimming a thin oily layer off the top of a "
     "ramen bowl, calm and simple", None),
    (62, "a small wall calendar hangs at the centre with one day circled softly",
     "a small wall calendar with just one day gently circled in soft colour, "
     "calm and unhurried", "週1"),
    (64, "a cup noodle container sits at the left, a small soup packet sits "
         "half emptied at the right",
     "a cup noodle container beside a small foil soup packet shown half "
     "emptied into it, drawn plainly", None),

    # === anecdote 1 — 正治さん (三重県) ===
    (67, "a small rounded map card sits at the centre",
     "a small warm rounded card showing a map pin over a stylised region "
     "shape, calm and inviting", "三重県"),
    (69, SHOJI + ", standing at the centre in front of a small auto parts "
         "factory gate",
     SHOJI + ", standing calmly in front of a small plain factory gate at "
         "dusk, a lunch bag in hand", None),
    (71, SHOJI + ", sitting at a ramen shop counter with a tonkotsu bowl in "
         "front of him",
     SHOJI + ", sitting at a small ramen shop counter, a steaming tonkotsu "
         "bowl in front of him, relaxed", None),
    (72, "an empty ramen bowl sits at the centre, a small extra noodle bowl "
         "beside it",
     "an empty ramen bowl with only broth left, a small extra noodle serving "
         "bowl beside it, drawn plainly", None),
    (74, SHOJI + ", with a small speech bubble above him and a slightly "
         "surprised expression",
     SHOJI + ", with a small rounded speech bubble above his head and a "
         "slightly surprised expression, looking at a paper", None),
    (77, SHOJI + ", pushing a half-full bowl aside calmly, a small content "
         "expression",
     SHOJI + ", pushing a ramen bowl aside with the broth at half level, a "
         "small calm contented expression", None),

    # === CTA giua ===
    (79, "a smartphone lies at the centre, a soft heart and speech bubble "
         "above it",
     "a smartphone lying on a table with a gentle heart mark and a small "
     "speech bubble floating above", None),

    # === ITEM3 — duong huyet lam RI SET ===
    (82, PIPE + ", the camera has moved to a third section further along",
     PIPE + ", shown at a third section further along its length, plain and "
     "calm", None),
    (84, "chopsticks lift noodles quickly at the centre, small motion lines "
         "around them",
     "a pair of chopsticks lifting noodles quickly out of a bowl, small soft "
     "motion lines showing speed, drawn plainly", None),
    (87, "the same water pipe now shows small reddish-brown rust patches "
         "forming along its inner wall",
     "the same friendly water pipe now drawn with a few small reddish-brown "
     "rust patches forming gently along its inner wall, not alarming", None),
    (89, "a small pile of wheat grains sits at the centre beside a few "
         "noodle strands",
     "a small pile of wheat grains beside a few plain noodle strands, drawn "
     "simply and calmly", None),
    (92, "a small side dish of bean sprouts and green onion sits at the "
         "centre, chopsticks reaching for it first",
     "a small side dish of bean sprouts and chopped green onion, a pair of "
     "chopsticks reaching toward it first, before the noodles", None),
    (96, "a person eats slowly and calmly at the centre, a gentle unhurried "
         "mood",
     "a bowl of ramen being eaten slowly and calmly, one chopstick pause "
     "mid-air, unhurried warm mood", None),

    # === checkpoint recap truoc khi tra loop ===
    (98, "three small round icons line up across the centre: a stiff pipe "
         "segment, a clogged pipe segment, and a rusty pipe segment",
     "three small round icon cards in a row: one showing a stiff cracked "
     "pipe segment, one showing a clogged greasy pipe segment, one showing a "
     "rusty pipe segment, calm and simple", "3つ"),

    # === TRA OPEN LOOP ===
    (101, "a small rounded speech bubble floats empty at the centre, waiting "
          "to be filled",
     "a small soft rounded speech bubble floating above a ramen shop "
     "counter, empty and waiting, calm and inviting", None),
    (104, "a small speech bubble sits above a ramen shop counter at the "
          "centre",
     "a small rounded speech bubble above a ramen shop counter, with a "
     "gentle simple mark inside it, warm and calm", "半分"),
    (109, "a woman stands at a ramen shop counter at the centre, speaking "
          "gently to a small counter figure",
     "a Japanese woman in her sixties standing at a ramen shop counter, "
     "speaking gently, a small friendly shopkeeper figure listening", None),

    # === anecdote 2 — 幸子さん (山形県) ===
    (112, "a small rounded map card sits at the centre",
     "a small warm rounded card showing a map pin over a stylised snowy "
     "region shape, calm and inviting", "山形県"),
    (116, SACHIKO + ", sitting at a small ramen shop counter with a miso "
          "ramen bowl in front of her",
     SACHIKO + ", sitting at a small ramen shop counter, a steaming miso "
          "ramen bowl in front of her, relaxed", None),
    (118, SACHIKO + ", pushing a half-full bowl aside calmly",
     SACHIKO + ", pushing a ramen bowl aside with the broth at half level, "
          "calm and unhurried", None),
    (121, SACHIKO + ", with a small warm smile, a little shy",
     SACHIKO + ", with a small warm shy smile, steam rising gently around "
          "her", None),

    # === recap + ket 4 lop ===
    (123, PIPE + ", now shown clean, flexible and flowing smoothly, healthy "
          "and calm",
     PIPE + ", now drawn clean, flexible and glowing softly, healthy and "
          "flowing smoothly, a satisfying resolution", None),
    (130, "a bowl of ramen sits at the centre tonight, calm and inviting, no "
          "worry in the scene",
     "a warm bowl of ramen at a home dinner table this evening, calm and "
          "inviting, gentle steam rising", None),
    (132, "three small icons line up at the centre: a bowl with less broth, "
          "a spoon skimming oil, and vegetables first",
     "three small round icon cards in a row: a bowl with less broth, a spoon "
          "skimming oil, and a small dish of vegetables, calm and simple", None),
    (134, "a smartphone lies at the centre, a small heart and share icon "
          "above it",
     "a smartphone lying on a table with a small heart mark and a share icon "
          "floating gently above, warm and inviting", None),
    (137, "a small clean leaflet sits at the centre",
     "a small clean health leaflet and a pen resting on a plain table, calm "
          "and trustworthy", None),
    (143, "a warm dinner table fills the frame, a ramen bowl steams gently at "
          "the centre under soft evening light",
     "a simple warm Japanese dinner table at night with a bowl of ramen "
          "steaming gently under a soft lamp, calm and peaceful", None),
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
        f"# Video 22 — {len(slides)} minh hoa AI (ラーメン x 水道管)\n\n"
        "> Slide TINH tren canvas trang, khung san khau + cast lam o buoc\n"
        "> `ingest_slides_22.py` (buoc sau, khi da co anh). Lop su kien 7s (sticker/tag)\n"
        "> lam o `remotion-vox/tools/build_overlays_22.py`, KHONG o day.\n\n"
        f"🔴 {ntext} canh co CHU BAKE — uu tien chu so Latin, soi TUNG KY TU truoc khi nhan.\n\n"
        "🔴 Nhan vat lap NGUYEN VAN mo ta (style-lock, RIENG cua anecdote — khac cast "
        "minori dan o buoc ingest):\n"
        f"- 正治さん: `{SHOJI}`\n- 幸子さん: `{SACHIKO}`\n\n"
        "⭐ AN DU XUYEN SUOT — DUY NHAT MOT CAI, khong duoc doi giua chung: "
        f"`{PIPE}`\n"
        "Xuat hien tu slide_05 (mo dau, con mo), slide_06 (gioi thieu ro), roi CHAY LAI "
        "moi lan quay ve chu de chinh: slide_16 (cung vi muoi), slide_28 (tac vi mo), "
        "slide_35 (ri set vi duong huyet), slide_50 (sach, ket bai). Kiem tra mach nay "
        "LIEN TUC khi soi anh — dung chi soi tung anh don le.\n\n"
        f"**STYLE:** `{STYLE}`\n\n**NEG:** `{NEG_NOTEXT}`\n\n---\n\n"
        + "\n".join(blocks), encoding="utf-8")

    n = len(slides)
    idxs = [it[0] for it in PLAN]
    gaps = [starts[idxs[i]] - starts[idxs[i - 1]] for i in range(1, len(idxs))]
    print(f"OK  {n} minh hoa | video ~{int(total)//60}'{int(total)%60:02d}")
    print(f"    {total/n:.1f} giay/canh | {n/(total/60):.2f} doi hinh/phut (tran 6, "
          f"dung DE cho lop overlay lam san 7s)")
    print(f"    gap nho nhat {min(gaps):.1f}s | lon nhat {max(gaps):.1f}s | {ntext} canh co chu")
    for f in (OUT_JSON, VD / "slide_prompts_FLOW.txt",
              VD / "slide_prompts_TENFILE.txt", VD / "slide_prompts_BLOCKS.md"):
        print(f"    -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
