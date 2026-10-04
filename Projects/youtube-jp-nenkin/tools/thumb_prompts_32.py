# -*- coding: utf-8 -*-
r"""thumb_prompts_32.py - 3 prompt thumbnail A/B video 32 (ginko honnin kakunin 2027 / 2 PIN bang lai).

KHUON: chep y nguyen thumb_prompts_31.py (TELOP/A-45 nenkin).
CHU chot trong script 32 muc "Thumbnail - bo 3 A/B" - GIONG NHAU ca 3 ban (bien thu la HINH):
   chip    `ゆうちょ・農協・信金の方へ`   (12) - CHO AI + keyword `ゆうちょ` (6,26 YT 30d, #1 rieng de)
   banner  `口座は止まりません`           (9)  - CHUYEN GI - lat tin don (`銀行 口座` 4,48 = #2)
   HERO    `暗証番号`                     (4)  - CAI GI DOI
   ribbon  `免許証の番号、言えますか`     (12) - PHAI LAM GI - cau tu kiem
   (!) khong dat 2027 / 2つ / so len anh (feedback_so_tren_hinh_phai_do_font_ve).
   (!) may doc the + ban phim = VAT MOI GOI SO -> phim tron, khong ky tu; soi tung phim.
   (!) khong ve logo / mau nhan dien buu dien / JA.
Cast: 佐藤 (66, 仙台) - token SATO cua img32_prompts.py (cardigan DO 2 tui) -> dong nhat voi video.
CHAY:  python tools/thumb_prompts_32.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\32_ginko-honnin-kakunin-2027")

CHIP = "ゆうちょ・農協・信金の方へ"
BANNER = "口座は止まりません"
HERO = "暗証番号"
RIBBON = "免許証の番号、言えますか"

SATO = ("an elderly Japanese woman in her mid sixties with short grey permed hair, in a RED "
        "cardigan with two front pockets over a white blouse")

READER = ("a small grey card-reader terminal on a counter with a keypad of plain round buttons, "
          "no digit or symbol on any key, a dark unlit screen")
CARD = ("a plain pale green plastic ID card with a gold IC chip and no photo"
        "")
BANK = ("a softly blurred bank counter and a row of grey waiting chairs, no signs or logos"
        "")

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, with a "
           "thick black outline and a white halo around every glyph. No watermark, no logo and "
           "no extra text. Keep the very bottom-right corner free of text. --ar 16:9")

TEXT_BLOCK = (
    "TEXT, exactly these 4 blocks and nothing else:\n"
    "small target chip at the top left, black on yellow: " + CHIP + "\n"
    "banner, white on navy: " + BANNER + "\n"
    "HERO, LARGEST block by far, gold gradient with heavy black outline: " + HERO + "\n"
    "bottom ribbon, white on red: " + RIBBON + "\n")

LAYOUT_BASE = (
    "LAYOUT: yellow chip in the top left corner; navy banner a full-width bar under it, one "
    "fifth of the frame high; HERO spans TWO THIRDS OF THE FRAME WIDTH, the tallest and widest "
    "block, looped by a red ellipse; red ribbon across the lower left, tilted slightly, top edge "
    "at seven tenths of the frame height, a red arrow from the hero down to it.")

BG_BASE = "BACKGROUND: pale cream graph paper, warm glow spots, thin speed lines, flat."

HEAD = ("A bold Japanese YouTube thumbnail for a pension money channel, 16:9, bright and "
        "high-contrast, with large Japanese text burned into the image.\n\n")

PERSON = ("RIGHT THIRD: a photograph of " + SATO + ", one finger stopped in mid-air just above "
          + READER + ", HESITANT AND PUZZLED, brows drawn together, lips pressed, eyes on the "
          "keypad. Cropped by the right edge, her head near the top edge, full height.\n")

CORNER = "BOTTOM-LEFT: " + CARD + ", no characters written anywhere.\n\n"

PROMPTS = [
    # T1 BASELINE - khuon TELOP/A-45: 佐藤 ngon tay dung tren ban phim may doc the, ngap ngung.
    ("thumb_T1_ginko-honnin-2027.png",
     "T1 baseline TELOP/A-45 - 佐藤 (cardigan do) ngon tay dung tren may doc the; goc duoi-trai bang lai tron",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n" + PERSON + CORNER + BG_BASE + "\n" + QUALITY),

    # T2 doi DUNG 1 BIEN HINH: nen = quay ngan hang mo + hang ghe cho. Chu + layout + nguoi y nguyen.
    ("thumb_T2_ginko-honnin-2027.png",
     "T2 doi 1 bien HINH (chu + layout y nguyen): nen = quay ngan hang mo + hang ghe cho",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n" + PERSON + CORNER
     + "BACKGROUND: behind the whole frame " + BANK + ", bright and low contrast, flat.\n"
     + QUALITY),

    # T3 doi LAYOUT - khuon kame-sensei (nen navy, hero tron dai giua, nguoi nho goc duoi-phai).
    ("thumb_T3_ginko-honnin-2027.png",
     "T3 doi LAYOUT: kame-sensei - nen navy, hero tron dai giua, 佐藤 NHO goc duoi-phai",
     HEAD + TEXT_BLOCK + "\n"
     "LAYOUT: the small yellow chip sits in the top left corner. The banner line runs just under "
     "it in white on a thin navy strip, one eighth of the frame high. The HERO fills the middle "
     "band from the left edge to three quarters of the frame width, the tallest and widest thing "
     "by far, looped by a red ellipse, and nothing overlaps any of its four characters. A solid "
     "red band along the bottom edge carries the ribbon line in white.\n"
     "RIGHT QUARTER, LOWER HALF: a cut-out photograph of " + SATO + ", chest up, CROPPED BY THE "
     "BOTTOM EDGE, the top of her head lower than the bottom of the hero, hesitant and puzzled, "
     "white die-cut border.\n"
     "BACKGROUND: flat deep navy with subtle paper texture, thin gold rays behind the hero, a "
     "small flat icon of " + CARD + ", no characters on it, at the lower left. Nothing else.\n\n" + QUALITY),
]

# PLATE de FILE RIENG - tron vao FLOW la extension bom ca file, ra anh trang chu.
PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + SATO + ", one finger stopped above " + READER + ", hesitant "
     "and puzzled, cropped by the right edge, full height. At the bottom left, " + CARD + ". "
     "Keep the whole left two thirds a plain cream field with nothing placed on it. "
     "No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, " + BANK + ", "
     "bright and low contrast. On the right third, a photograph of " + SATO + ", one finger "
     "stopped above " + READER + ", hesitant and puzzled, cropped by the right edge, full "
     "height. At the bottom left, " + CARD + ". Keep the whole left two thirds soft and plain "
     "with nothing placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a solid "
     "red band along the bottom edge, and a small flat icon of " + CARD + ", no characters on it, at the lower left. "
     "At the lower right, a cut-out photograph of " + SATO + ", chest up, hesitant, only about "
     "one third of the frame height. Keep the middle band a plain navy field with nothing placed "
     "on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
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

    md = ["# thumbnail video 32 - 3 ban A/B (khuon TELOP/A-45 nenkin)", "",
          "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH; doi chu la hong phep do)", "",
          "| khoi | chu | ky | tra cau nao cua gate 7 |", "|---|---|---|---|",
          "| chip vang (tren-trai) | `%s` | %d | CHO AI + keyword `ゆうちょ` (6,26 YT30d) |"
          % (CHIP, len(CHIP)),
          "| banner navy (full width) | `%s` | %d | CHUYEN GI - lat tin don (`銀行 口座` 4,48) |"
          % (BANNER, len(BANNER)),
          "| **HERO** vang + elip do | `%s` | %d | CAI GI DOI - **<=6 ky** |"
          % (HERO, len(HERO)),
          "| ribbon do | `%s` | %d | PHAI LAM GI - cau tu kiem |" % (RIBBON, len(RIBBON)), "",
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
