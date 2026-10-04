# -*- coding: utf-8 -*-
"""3 prompt thumbnail cho video 38 — 鉛筆の名簿.

CHEP CAU TRUC tu ban da chay duoc cua kenh: 07_UPLOADED/37_nanaketa-no-kioku
(§ThumbNail) — giu nguyen thu tu khoi, chi doi PHONG CACH.

🔴 KHAC 37 MOT DIEM DUY NHAT, co chu y: 37 la `Photorealistic`, bai nay la
   **MANGA MAU**. Ly do: ca video 38 dung bang 289 anh manga, ma `media-library.md`
   §2.0 doi thumbnail -> frame dau phai LIEN MACH. Thumbnail anh that + frame dau
   manga = mismatch ngay tai diem rot nang nhat.

BO CHU GIONG HET NHAU o ca T1/T2/T3 (ab-3title-3thumb §3 muc 6): bien thu la HINH.
Tran 4 dong chu cho anh AI (§3 muc 8).
"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"

# ── BO CHU (dung chung 3 ban) ────────────────────────────────────────────────
TEXT = """TEXT, exactly these 4 blocks and nothing else:
line 1, white: 台風の夜の避難所
line 2, cyan: 「鉛筆の方は黙って」
line 3, yellow: 173人はボールペン
line 4, red with heavy black outline and white halo, LARGEST, roughly twice the height of the others: 私だけ鉛筆"""

# 🔴 HEADER phai NGAN: khoi TEXT bat buoc nam trong 15% DAU prompt (§3.1 Buoc 3).
#    Ban dau nhet ca doan ta phong cach len dau -> T2 lot ra 16%. Phong cach day
#    xuong CUOI, dau prompt chi giu MOT cau du de khoa the loai.
HEAD = ("Full-colour Japanese seinen drama manga panel, bold Japanese text burned "
        "into the image.")
# 🔴 PLATE dung HEAD RIENG: HEAD thuong co cau "bold Japanese text burned into the
#    image" — dat ngay truoc "NO TEXT ANYWHERE" la prompt TU CHOI NHAU (cung benh
#    "cau CAM chong lai MUC DICH" da dinh o cast plate va STYLE_MODERN).
HEAD_PLATE = "Full-colour Japanese seinen drama manga panel, no text of any kind."

STYLE = ("STYLE: hand-drawn manga, confident black ink linework with varied weight, flat "
         "cel colouring with hard-edged shadows, muted slate-blue and cold-grey palette "
         "with one warm accent, realistic adult proportions, dramatic composition.")

CAST = ("a composed Japanese woman of sixty-seven in a plain dark grey zip-up jacket, "
        "standing straight, calm and steady expression, holding nothing; beside her a "
        "Japanese woman in her fifties in a navy blue windbreaker with a yellow cloth "
        "armband on one sleeve, chin lifted, smug and dismissive expression, one hand "
        "pointing away out of frame")

PROP = ("an open ruled attendance ledger lying flat with a single wooden pencil laid "
        "across the page, and a ballpoint pen standing in a cup beside it")

TAIL = ("Keep the very top-right corner and the very bottom-right corner free of text and "
        "free of any important detail. "
        "Text must be perfectly formed Japanese characters, crisp and legible. "
        "No watermark, no logo, no signature, no additional text. --ar 16:9")

T1 = f"""{HEAD}

{TEXT}

LAYOUT: text block fills the LEFT 65-70% of frame, four lines stacked, line 4 clearly the tallest and boldest.
CENTER-RIGHT, occupying roughly 33% of frame width: {CAST}.
FOREGROUND, lower right of the text block: {PROP}.
BACKGROUND: the main hall of a Japanese primary school gymnasium at night during a typhoon used as an evacuation shelter, blue plastic sheets in rows on a varnished wooden floor, folded grey blankets, fluorescent strip lights in the high ceiling, rain running down tall windows near the roof, no legible text anywhere in the background.
{STYLE}
{TAIL}"""

T2 = f"""{HEAD}

{TEXT}

LAYOUT: text block fills the LEFT 65-70% of frame, four lines stacked, line 4 clearly the tallest and boldest.
CENTER-RIGHT, occupying roughly 33% of frame width: {CAST}.
FOREGROUND, lower right of the text block: {PROP}.
BACKGROUND: a close reception table just inside the gymnasium door, two long school tables pushed together, a cardboard box of folded blankets and a black corded telephone, one hard fluorescent tube directly overhead throwing sharp shadows, the hall behind falling away into darkness, no legible text anywhere in the background.
{STYLE}
{TAIL}"""

T3 = f"""{HEAD}

{TEXT}

LAYOUT: line 1 and line 2 stacked at the very TOP of frame; line 3 and line 4 stacked at the very BOTTOM of frame, line 4 clearly the tallest and boldest; the CENTER band of the frame is fully open for the scene.
CENTER, filling the open middle band: {CAST}, the two of them face to face and close together, shown from the chest up so both faces read clearly.
LOWER LEFT, small: {PROP}.
BACKGROUND: the gymnasium shelter at night seen close behind them, blue plastic sheets and folded blankets out of focus, fluorescent light overhead, no legible text anywhere in the background.
{STYLE}
{TAIL}"""

PLATES = [
 (HEAD_PLATE + "\n\nNO TEXT ANYWHERE IN THIS IMAGE: no letters, no numbers, no Japanese "
  "characters, no signage, no labels — a clean plate for text to be added later.\n\n"
  "LAYOUT: leave the LEFT 65-70% of frame as clean uncluttered background with no "
  "important detail, for text to be placed over later.\n"
  f"CENTER-RIGHT, occupying roughly 33% of frame width: {CAST}.\n"
  "BACKGROUND: the main hall of a Japanese primary school gymnasium at night during a "
  "typhoon used as an evacuation shelter, blue plastic sheets in rows, folded grey "
  "blankets, fluorescent strip lights, rain on the high windows.\n"
  + STYLE + "\n"
  "Keep the very top-right and bottom-right corners clear. No watermark, no logo, "
  "no signature. --ar 16:9"),
 (HEAD_PLATE + "\n\nNO TEXT ANYWHERE IN THIS IMAGE: no letters, no numbers, no Japanese "
  "characters, no signage, no labels — a clean plate for text to be added later.\n\n"
  "LAYOUT: leave the LEFT 65-70% of frame as clean uncluttered background with no "
  "important detail.\n"
  f"CENTER-RIGHT, occupying roughly 33% of frame width: {CAST}.\n"
  "BACKGROUND: a close reception table just inside the gymnasium door under one hard "
  "fluorescent tube, the hall behind falling away into darkness.\n"
  + STYLE + "\n"
  "Keep the very top-right and bottom-right corners clear. No watermark, no logo, "
  "no signature. --ar 16:9"),
 (HEAD_PLATE + "\n\nNO TEXT ANYWHERE IN THIS IMAGE: no letters, no numbers, no Japanese "
  "characters, no signage, no labels — a clean plate for text to be added later.\n\n"
  "LAYOUT: leave a clear empty band across the TOP and across the BOTTOM of the frame; "
  "keep the CENTER band for the scene.\n"
  f"CENTER: {CAST}, face to face and close together, shown from the chest up.\n"
  "BACKGROUND: the gymnasium shelter at night close behind them, out of focus.\n"
  + STYLE + "\n"
  "Keep the very top-right and bottom-right corners clear. No watermark, no logo, "
  "no signature. --ar 16:9"),
]

NAMES = ["thumb_T1_hinan-taikukan.png", "thumb_T2_uketsuke-keikou.png",
         "thumb_T3_taimen-close.png"]

def one_line(p):
    return " ".join(p.split())

flow = [one_line(x) for x in (T1, T2, T3)]
plate = [one_line(x) for x in PLATES]

os.makedirs(VD, exist_ok=True)
io.open(os.path.join(VD, "thumb_prompts_FLOW.txt"), "w", encoding="utf-8").write(
    "\n".join(flow) + "\n")
io.open(os.path.join(VD, "thumb_prompts_PLATE.txt"), "w", encoding="utf-8").write(
    "\n".join(plate) + "\n")
io.open(os.path.join(VD, "thumb_prompts_TENFILE.txt"), "w", encoding="utf-8").write(
    "# dong FLOW.txt  ->  ten file (thu tu PHAI khop)\n"
    + "\n".join("%3d  %s" % (i, n) for i, n in enumerate(NAMES, 1)) + "\n")
with io.open(os.path.join(VD, "thumb_prompts_BLOCKS.md"), "w", encoding="utf-8") as f:
    f.write("# Thumbnail 38 — 鉛筆の名簿 · bản người đọc\n\n"
            "Bộ chữ **giống hệt nhau** ở T1/T2/T3 — biến thử là HÌNH "
            "(`ab-3title-3thumb.md` §3 mục 6).\n\n"
            "| | biến thử | khuôn |\n|---|---|---|\n"
            "| **T1** | baseline | K1 text-wall, nền sảnh thể dục rộng |\n"
            "| **T2** | đổi **1 biến hình**: nền → cận bàn tiếp nhận dưới đèn huỳnh quang | K1, chữ y hệt |\n"
            "| **T3** | đổi **layout**: chữ dồn trên+dưới, giữa mở, 2 mặt cận | K2 |\n\n")
    for n, p in zip(("T1", "T2", "T3"), (T1, T2, T3)):
        f.write("## %s\n\n```\n%s\n```\n\n" % (n, p))

# ── GATE ─────────────────────────────────────────────────────────────────────
print("GATE:")
for i, p in enumerate(flow, 1):
    pos = p.find("TEXT, exactly") * 100 // len(p)
    ok = "OK " if pos <= 15 else "🔴 "
    print("  %s T%d: %4d ky | khoi TEXT @ %d%% (luat <=15%%)" % (ok, i, len(p), pos))
for must, lab in ((("私だけ鉛筆",), "hero"), (("no watermark", "No watermark"), "watermark"),
                  (("bottom-right",), "goc timestamp"),
                  (("crisp and legible",), "cau chot chu")):
    bad = [i for i, p in enumerate(flow, 1) if not any(m in p for m in must)]
    print("  %s %-14s thieu o: %s" % ("OK " if not bad else "🔴 ", lab, bad or "khong"))
NG = ("殺", "血", "死ね", "自殺", "レイプ", "虐待")
hit = [(i, w) for i, p in enumerate(flow, 1) for w in NG if w in p]
print("  %s tu cam o thumbnail: %s" % ("OK " if not hit else "🔴 ", hit or "khong"))
print("\n-> thumb_prompts_FLOW.txt / _BLOCKS.md / _TENFILE.txt / _PLATE.txt")
