# -*- coding: utf-8 -*-
r"""thumb_prompts_29.py - 3 prompt thumbnail A/B video 29 (khuon TELOP nenkin).

QUY TRINH `ab-3title-3thumb.md` §3.1 - 4 BUOC, khong dao.

B1. KHUON LAY TU ANH DA LEN SONG/DA DUYET, khong tu tai lieu:
    v27 `07_UPLOADED/27_.../\_upload/thumbnail.jpg` (dang chay tren kenh)
    v28 `07_UPLOADED/28_.../\_upload/thumbnail.png` (da duyet, len song 22/9)
B2. DO BANG MAY (1376x768):
      BANNER navy : v27 **19,1%** chieu cao - v28 **19,8%** => khuon ON DINH, chay HET be ngang
      HERO vang   : v27 rong **83,7%** - v28 rong **90,8%** - deu co ELIP DO khoanh
      RIBBON do   : v27 y 72%-90% - v28 y 66%-80%, cheo nhe, chu trang
      ANH NGUOI   : tu ~x=62% sang phai, cao TRON khung
    * Thu mua duoc legibility la **BE NGANG** cua hero, khong phai chieu cao.
B3. Khoi TEXT trong **15% DAU** prompt (gate chinh).
B4. Xuat 4 FILE, moi file mot viec.

CHU - GIONG NHAU ca 3 ban (bien thu la HINH):
   banner  `年金暮らしの方へ、8月から`  (12) - AI + keyword `年金` 81,03 dung DAU + moc thang
   kicker  `一枚では`                (4)  - DIEU KIEN, phai nam NGAY TREN hero
   HERO    `使えない紙`              (5)  - HAU QUA, **<=6 ky** => qua gate 1 `audience-45plus` §1
   ribbon  `封筒を出して`            (6)  - PHAI LAM GI

🔴 VI SAO TACH `一枚では` RA KHOI HERO (phuong an "a", chot 2026-09-21):
Ban dau HERO la `一枚では使えない` = **8 ky, vuot tran 6 ky**. Nhung KHONG duoc rut thang thanh
`使えない紙` roi bo ve dieu kien - nhu the doc ra la *"to giay vo dung"*, tuc **misleading**
(`youtube-compliance.md` §4: moi tinh tiet phai CO THAT trong video). Video noi ro: no chi khong
dung duoc **MOT MINH**. => giu ca hai ve, chi doi CHO: dieu kien len dong kicker nho ngay tren
hero, hau qua o hero. Doc xuoi: 一枚では / 使えない紙.

TRAN 4 DONG cho anh AI (§3 muc 8). Dung dung 4 khoi.
CAM `blank`/`empty`/`text-free`. So thi KHONG xin (font cua tool ve) - o day khong co so nao.

CHAY:  python tools/thumb_prompts_29.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\29_shikaku-kakuninsho-8gatsu-85sai")

BANNER = "年金暮らしの方へ、8月から"
KICKER = "一枚では"
HERO = "使えない紙"
RIBBON = "封筒を出して"

# CAST co dinh cua thumbnail nenkin - GIU NGUYEN tu v28 (ao xanh da troi, user chot 2026-09-21).
# Toc ta bang HAI moc cu the chu khong noi "balding": tu chung chung thi moi ban ra mot kieu dau,
# ma cai mua duoc o thumbnail la NHAN DIEN LAP LAI.
CAST = ("a Japanese man in his mid seventies, THINNING HAIR ON TOP with a high receding "
        "hairline, short grey hair at the sides, in a LIGHT SKY BLUE collared shirt")

PAPER = "fine ruled grid lines and faint illegible marks, no readable character or digit"

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, with a "
           "thick black outline and a white halo around every glyph. No watermark, no logo and "
           "no extra text. Keep the very bottom-right corner free of text. --ar 16:9")

TEXT_BLOCK = (
    "TEXT, exactly these 4 blocks and nothing else:\n"
    "top banner, white on navy: " + BANNER + "\n"
    "kicker above the hero, black with 一枚 in red: " + KICKER + "\n"
    "HERO, LARGEST block by far, gold gradient with heavy black outline: " + HERO + "\n"
    "bottom ribbon, white on red: " + RIBBON + "\n")

LAYOUT_BASE = (
    "LAYOUT: the navy banner is a full-width bar across the very top, one fifth of the frame "
    "high. The kicker sits just under it on the LEFT. The HERO spans about TWO THIRDS OF "
    "THE FRAME WIDTH, far the tallest and widest block, looped by a hand-drawn red ellipse. The "
    "red ribbon crosses the lower left, tilted a few degrees, its top edge at seven tenths of "
    "the frame height, a curved red arrow rising from it to the hero.")

BG_BASE = ("BACKGROUND: pale cream graph paper, warm yellow glow spots, thin black speed "
           "lines radiating in from the edges, flat.")

HEAD = ("A bold Japanese YouTube thumbnail for a pension money channel, 16:9, bright and "
        "high-contrast, with large Japanese text burned into the image.\n\n")

PROMPTS = [
    # T1 BASELINE - khuon dang chay. Dao cu = HAI to giay, mot to moi tay (chinh la cu doi chieu
    # cua bai: mot to dung duoc mot minh, mot to thi khong).
    ("thumb_T1_shikaku-kakuninsho.png",
     "T1 baseline khuon TELOP/A-45 - ong gia cam HAI to giay, mot to moi tay",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", holding up one printed card-sized sheet in each "
     "hand at chest height, looking from one to the other, puzzled, cropped by the right edge, "
     "head near the top edge and body running the full height. Both sheets have " + PAPER + ".\n"
     "BOTTOM-LEFT: a pale yellow window envelope lying flat, one faint ruled line in its address "
     "window.\n\n" + BG_BASE + "\n" + QUALITY),

    # T2 doi DUNG 1 BIEN HINH - dao cu doi sang CANH QUAY (dung canh mo dau cua kich ban);
    # CHU + LAYOUT giu nguyen tuyet doi.
    ("thumb_T2_shikaku-kakuninsho.png",
     "T2 doi 1 bien HINH (chu + layout y nguyen): canh o quay, nhan vien gio tay chan",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + " at a hospital reception counter holding one "
     "printed card-sized sheet out across the counter, while a receptionist raises one open palm "
     "to stop him, cropped by the right edge, head near the top edge and body running the full "
     "height. The sheet has " + PAPER + ".\n"
     "BOTTOM-LEFT: a small counter card reader with a soft teal glow.\n\n"
     + BG_BASE + "\n" + QUALITY),

    # T3 doi LAYOUT - khuon kame-sensei, nen navy dam, hero chiem tron dai giua.
    # Day la khuon DUY NHAT trong so do workspace **VUOT** gate 2 (hero 38-40% chieu cao),
    # vi bo rang buoc chieu doc: ong gia xuong goc duoi-phai va chi cao ~1/3 khung.
    ("thumb_T3_shikaku-kakuninsho.png",
     "T3 doi LAYOUT: khuon kame-sensei - nen navy dam, hero tron dai giua, ong gia NHO goc duoi-phai",
     HEAD + TEXT_BLOCK + "\n"
     "LAYOUT: a yellow target chip across the top carries the banner line, one eighth of the "
     "frame high. The kicker sits just under it in white, small. The HERO fills the whole middle "
     "band and spans almost the entire width, the tallest and widest thing by far. A solid red "
     "band along the bottom edge carries the ribbon line in white.\n"
     "LOWER-RIGHT: a cut-out photograph of " + CAST + ", chest up, holding one printed card-sized "
     "sheet with a puzzled tilt of the head, only about one third of the frame high so he sits "
     "clearly BELOW the hero and never overlaps it, clean white die-cut border. The sheet has "
     + PAPER + ".\n"
     "BACKGROUND: one flat deep navy field with a subtle paper texture, thin gold radiating "
     "lines behind the hero, and two small flat icons at the lower left - a window envelope and "
     "a plastic card. Nothing else sits in the frame.\n\n" + QUALITY),
]

# PLATE de FILE RIENG - tron vao FLOW la extension bom ca file, ra 3 anh trang chu
# (da dinh o chouhen 21). Chi dung khi anh AI gen nat kanji.
PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + CAST + " holding up one printed card-sized sheet in each hand, "
     "cropped by the right edge, full height. A pale yellow window envelope lies flat at the "
     "bottom left. Keep the whole left two thirds a plain cream field with nothing placed on it. "
     "No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + CAST + " at a hospital reception counter holding one sheet out "
     "while a receptionist raises an open palm, cropped by the right edge, full height. A small "
     "counter card reader at the bottom left. Keep the whole left two thirds a plain cream field "
     "with nothing placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a solid "
     "red band along the bottom edge, and two small flat icons at the lower left - a window "
     "envelope and a plastic card. At the lower right, a cut-out photograph of " + CAST + ", "
     "chest up, only about one third of the frame height. Keep the middle band a plain navy "
     "field with nothing placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
]


def main() -> int:
    os.makedirs(VD, exist_ok=True)

    io.open(os.path.join(VD, "thumb_prompts_FLOW.txt"), "w", encoding="utf-8",
            newline="\n").write(
        "\n".join(p.replace("\n", " ") for _f, _d, p in PROMPTS) + "\n")

    io.open(os.path.join(VD, "thumb_prompts_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(
                "dong %d -> %s   [%s]" % (i + 1, f, d)
                for i, (f, d, _p) in enumerate(PROMPTS)) + "\n")

    io.open(os.path.join(VD, "thumb_prompts_PLATE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(p.replace("\n", " ") for _f, p in PLATE) + "\n")

    md = ["# thumbnail video 29 - 3 ban A/B (khuon TELOP/A-45 nenkin)", "",
          "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH; doi chu la hong phep do)", "",
          "| khoi | chu | ky | tra cau nao cua gate 7 |", "|---|---|---|---|",
          "| banner navy (full width) | `%s` | %d | AI + keyword `年金` 81,03 dung DAU + moc thang |"
          % (BANNER, len(BANNER)),
          "| kicker (`一枚` do) | `%s` | %d | DIEU KIEN - phai nam NGAY TREN hero |"
          % (KICKER, len(KICKER)),
          "| **HERO** vang + elip do | `%s` | %d | HAU QUA - **<=6 ky**, qua gate 1 |"
          % (HERO, len(HERO)),
          "| ribbon do | `%s` | %d | PHAI LAM GI |" % (RIBBON, len(RIBBON)), "",
          "## So do - do bang may tu 2 ban da duyet (1376x768)", "",
          "| khoi | v27 (dang chay) | v28 (len song 22/9) |", "|---|---|---|",
          "| banner navy | **19,1%** cao, full width | **19,8%** cao |",
          "| hero vang | rong **83,7%** | rong **90,8%** |",
          "| ribbon do | y 72%-90% | y 66%-80% |", "",
          "## 3 ban", ""]
    for i, (f, d, p) in enumerate(PROMPTS, 1):
        md += ["### %d. `%s`" % (i, f), "", d, "", "```", p, "```", ""]
    io.open(os.path.join(VD, "thumb_prompts_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md))

    print("%-34s%6s%8s" % ("file", "ky", "TEXT@"))
    bad = 0
    for f, _d, p in PROMPTS:
        one = p.replace("\n", " ")
        pos = one.find("TEXT, exactly") * 100 // len(one)
        ok = pos <= 15 and len(one) <= 1750
        bad += (not ok)
        print("%-34s%6d%7d%%  %s" % (f, len(one), pos, "OK" if ok else "GATE DO"))
    for f, _d, p in PROMPTS:
        for w in ("blank", "empty", "text-free"):
            if w in p.lower():
                bad += 1
                print("GATE DO %s: con tu cam '%s'" % (f, w))
    hero_ok = len(HERO) <= 6
    print("HERO %d ky (tran 6): %s" % (len(HERO), "OK" if hero_ok else "GATE DO"))
    bad += (not hero_ok)
    print("\n%s - 4 file -> %s" % ("SACH" if not bad else "GATE DO", VD))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
