# -*- coding: utf-8 -*-
r"""thumb_prompts_26.py — 3 prompt thumbnail A/B cua video 26 (khuon TELOP nenkin).

QUY TRINH theo `ab-3title-3thumb.md` §3.1 — 4 BUOC, khong duoc dao:
 B1. LAY KHUON TU ANH DA LEN SONG, khong tu tai lieu.
     -> mo `07_UPLOADED/25_.../\_upload/thumbnail.png` (ban dang chay tren kenh) va NHIN.
 B2. DO ANH DO BANG MAY. So do that (1280x720), 2026-09-17:
       BANNER navy  : y 27-137 = **15,4% chieu cao khung**, chay HET be ngang
       HERO vang    : x 93-799 = **55,2% BE NGANG** (ke ca quang sang), co ELIP DO khoanh
       RIBBON do    : y 431-592 = **60%-82% chieu cao**, cheo nhe, chu trang
       ANH NGUOI    : tu **x=60%** sang phai, cao TRON khung (khong lo lung)
       Goc duoi-phai: mau co 40,2% muc (tay + phong bi) => DAO CU o day DUOC,
                      chi CHU la khong duoc (o timestamp cua YouTube).
     ⭐ Bai hoc da ghi: thu mua duoc legibility la **BE NGANG** cua hero, khong phai
       chieu cao — ban 09 chi cao ~18% ma van doc duoc o 120px vi rong ~2/3 khung.
 B3. VIET THEO KHUNG KHOI, khoi TEXT trong **15% DAU** prompt (gate chinh).
 B4. XUAT 4 FILE, moi file mot viec (xem cuoi ham main).

CHU — qua gate 7 (`audience-45plus.md` §1) + bang do keyword (`youtube-upload-seo.md` §0.5):
   (1) ve CAI GI  -> 介護保険料      (thuc the chinh cua bai)
   (2) chuyen GI  -> 年3万7千円      (con so dat nhat, 6 ky = dat tran hero)
   (3) LAM GI/moc -> 同居した        (nguyen nhan, la cai bai ban)
⚖️ 介護保険料 do duoc 0,12 tren YT search (gan 0) nhung VAN len thumbnail: bai nay song
   bang suggested tu hang xom フクロウ, khong song bang search — da chot o script §Do keyword.
   Tu do cao nhat (年金 81,97) da di dau TITLE, dung hai duong khac nhau.

⚠️ TRAN 4 DONG CHU cho anh AI (§3 muc 8): dung 4 khoi (banner · dong2 · hero · ribbon).
   Them dong thu 5 la gan nhu chac meo kanji.

CHAY:  python tools/thumb_prompts_26.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai")

BANNER = "65歳以上の介護保険料"
LINE2 = "世帯で決まる"
HERO = "年3万7千円"
RIBBON = "同居した、それだけで"

# ── khoi dung chung ────────────────────────────────────────────────────────
# ── CAST CO DINH cua thumbnail (user chot 2026-09-17: "phai co hinh nguoi ong gia,
#    dau hoi hoi") — ta MOT LAN, dung CHUNG ca 3 ban de mat nhan ra day la mot kenh.
# 🔴 Ta TOC bang HAI moc cu the (thua tren dinh + tran cao) chu khong noi "balding":
#    mot tu chung chung thi moi ban gen ra mot kieu dau khac nhau, va cai mua duoc o
#    thumbnail la NHAN DIEN LAP LAI, khong phai mot khuon mat dep.
CAST = ("a Japanese man in his early seventies with THINNING HAIR ON TOP and a high "
        "receding hairline, short grey hair at the sides, clean-shaven, wearing a knitted "
        "vest over a collared shirt")

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, with a "
           "thick black outline and a white halo around every glyph. No watermark, no logo and "
           "no extra text. Keep the very bottom-right corner free of text. --ar 16:9")

TEXT_BLOCK = (
    f"TEXT, exactly these 4 blocks and nothing else:\n"
    f"top banner, white on navy: {BANNER}\n"
    f"line 2, black with the two characters 世帯 in red: {LINE2}\n"
    f"HERO, LARGEST block by far, gold gradient with heavy black outline: {HERO}\n"
    f"bottom ribbon, white on red: {RIBBON}\n")

LAYOUT_BASE = (
    "LAYOUT: the navy banner is a full-width bar across the very top, height about one "
    "sixth of the frame. Line 2 sits under it on the LEFT. The HERO spans about TWO "
    "THIRDS OF THE FRAME WIDTH with a hand-drawn red ellipse looping around it. The red "
    "ribbon crosses the lower left, tilted a few degrees, its top edge at about three "
    "fifths of the frame height, a curved red arrow rising from it to the right.")

BG_BASE = ("BACKGROUND: pale cream graph paper, warm yellow glow spots, thin black speed "
           "lines radiating in from the edges. Flat, no depth of field.")

PROMPTS = [
    # ── T1: BASELINE — khuon kenh, doi tuong duy nhat la 通知書 tren tay ─────
    ("thumb_T1_kaigo-tsuchisho.png",
     "T1 baseline khuon TELOP — y het khuon dang chay, chi doi anh sang 決定通知書",
     "A bold Japanese YouTube thumbnail for a pension money channel, 16:9, "
     "bright and high-contrast, with large Japanese text burned into the image.\n\n"
     + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", holding up one printed municipal notice "
     "sheet toward the camera and looking at it with a worried frown, cropped by the right "
     "edge, head almost touching the top of the picture and body running the full height. "
     "The sheet's ruled boxes are blank, no characters on it.\n"
     "BOTTOM-LEFT: a cream envelope lying flat, address window empty, no characters.\n\n"
     + BG_BASE + "\n" + QUALITY),

    # ── T2: doi DUNG 1 BIEN HINH — anh phai doi tu 通知書 sang canh 同居 ────
    ("thumb_T2_kaigo-doukyo.png",
     "T2 doi 1 bien HINH (giu nguyen chu + layout): anh phai = canh con gai don ve o chung",
     "A bold Japanese YouTube thumbnail for a pension money channel, 16:9, "
     "bright and high-contrast, with large Japanese text burned into the image.\n\n"
     + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", standing inside the open front door of a "
     "home looking uneasy, a woman in her forties in office clothes carrying a box in behind "
     "him. He is cropped by the right edge, head almost touching the top and body running "
     "the full height. Warm daylight, no signage and no characters anywhere.\n"
     "BOTTOM-LEFT: house slippers on the step.\n\n" + BG_BASE + "\n" + QUALITY),

    # ── T3: doi LAYOUT — khuon カメ先生, 0 NGUOI, nen navy dam ───────────────
    # ⭐ Day la khuon DUY NHAT trong 22 ca do duoc cua workspace **VUOT** gate 2
    #    (hero 38,7-39,8% chieu cao) — vi bo cast di la bo dung rang buoc chieu doc.
    # ⚖️ T3 VAN la bien "doi LAYOUT", nhung ong gia bay gio dung o goc duoi-phai va CHI
    #    cao ~1/3 khung, khong chay tron chieu cao nhu T1/T2. Ly do do duoc: 21/22 ca
    #    trong so workspace co cast chay het chieu cao deu ket hero o 20-31%; ban BO cast
    #    la ban duy nhat len 38-40%. De ong to het khung o day thi T3 mat dung cai no
    #    dang thu nghiem. Nho lai = van co mat nguoi ma hero giu duoc dai giua.
    ("thumb_T3_kaigo-kame.png",
     "T3 doi LAYOUT: khuon カメ先生 — nen navy dam, hero chiem tron dai giua, ong gia NHO o goc",
     "A bold Japanese YouTube thumbnail for a pension money channel, 16:9, high-contrast, "
     "with large Japanese text burned into the image.\n\n"
     + TEXT_BLOCK + "\n"
     "LAYOUT: a yellow target chip sits at the top carrying the banner line, about one "
     "eighth of the frame height. Line 2 sits just under it in white. The HERO fills the "
     "whole middle band of the frame and spans almost the entire width, the tallest and "
     "widest thing by far. A solid red band runs along the bottom edge carrying the ribbon "
     "line in white.\n"
     "LOWER-RIGHT: a cut-out photograph of " + CAST + ", shown from the chest up with a "
     "puzzled tilt of the head, standing only about one third of the frame height so he sits "
     "clearly BELOW the hero and never overlaps it, with a clean white die-cut border.\n"
     "BACKGROUND: one flat deep navy field with a subtle paper texture, a few thin gold "
     "radiating lines behind the hero, and two small flat illustrated icons at the lower "
     "left — a simple house outline and a stack of coins. Nothing else in the frame.\n\n"
     + QUALITY),
]

PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the "
     "right third, a photograph of " + CAST + " holding up a blank printed notice sheet, "
     "cropped by the right edge, full height. A cream envelope lies flat at the bottom "
     "left. Leave the whole left "
     "two thirds empty and uncluttered. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the "
     "right third, a photograph of " + CAST + " standing inside an open front door with a "
     "younger woman carrying a box in behind him, cropped by the right edge, full height. "
     "House slippers on the step at the bottom left. Leave the whole left "
     "two thirds empty and uncluttered. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a "
     "solid red band along the bottom edge, and two small flat illustrated icons at the lower "
     "left — a simple house outline and a stack of coins. At the lower right, a cut-out "
     "photograph of " + CAST + ", chest up, only about one third of the frame height. Leave "
     "the middle band completely empty. No text, no letters, no numbers, no watermark. --ar 16:9"),
]


def main() -> int:
    os.makedirs(VD, exist_ok=True)
    flow = os.path.join(VD, "thumb_prompts_FLOW.txt")
    io.open(flow, "w", encoding="utf-8", newline="\n").write(
        "\n".join(p.replace("\n", " ") for _f, _d, p in PROMPTS) + "\n")

    io.open(os.path.join(VD, "thumb_prompts_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(
                f"dong {i+1} -> {f}   [{d}]" for i, (f, d, _p) in enumerate(PROMPTS)) + "\n")

    io.open(os.path.join(VD, "thumb_prompts_PLATE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(p.replace("\n", " ") for _f, p in PLATE) + "\n")

    md = ["# thumbnail video 26 — 3 ban A/B (khuon TELOP nenkin)", "",
          "## Chu (GIONG NHAU ca 3 ban — bien thu la HINH, doi chu la hong phep do)", "",
          "| khoi | chu | ky |", "|---|---|---|",
          f"| banner navy | `{BANNER}` | {len(BANNER)} |",
          f"| dong 2 (世帯 do) | `{LINE2}` | {len(LINE2)} |",
          f"| **HERO** | `{HERO}` | {len(HERO)} |",
          f"| ribbon do | `{RIBBON}` | {len(RIBBON)} |", "",
          "## So do lay tu ban DANG CHAY (video 25, 1280x720)", "",
          "| khoi | so do |", "|---|---|",
          "| banner navy | y 27-137 = **15,4% chieu cao**, full width |",
          "| hero vang | x 93-799 = **55,2% be ngang**, co elip do khoanh |",
          "| ribbon do | y 431-592 = **60%-82% chieu cao**, cheo nhe |",
          "| anh nguoi | tu **x=60%** sang phai, cao TRON khung |", "",
          "## 3 ban", ""]
    for i, (f, d, p) in enumerate(PROMPTS, 1):
        md += [f"### {i}. `{f}`", "", d, "", "```", p, "```", ""]
    io.open(os.path.join(VD, "thumb_prompts_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md))

    # ── GATE: khoi TEXT phai nam trong 15% DAU (gate chinh cua §3.1 Buoc 3) ──
    print(f"{'file':<28}{'ky':>6}{'TEXT @':>8}")
    bad = 0
    for f, _d, p in PROMPTS:
        one = p.replace("\n", " ")
        pos = one.find("TEXT, exactly") * 100 // len(one)
        ok = pos <= 15 and len(one) <= 1750
        bad += not ok
        print(f"{f:<28}{len(one):>6}{pos:>7}%  {'OK' if ok else '🔴'}")
    print(f"\n{'SACH' if not bad else 'GATE DO'} · 4 file -> {VD}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
