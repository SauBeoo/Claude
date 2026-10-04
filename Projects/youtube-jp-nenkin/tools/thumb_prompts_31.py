# -*- coding: utf-8 -*-
r"""thumb_prompts_31.py - 3 prompt thumbnail A/B video 31 (扶養親族等申告書 -> 非課税世帯 domino).

KHUON: chep y nguyen thumb_prompts_30.py (TELOP/A-45 nenkin; so do B2 cua v27/v28 ghi o do).
CHU chot trong script 31 muc "Thumbnail - bo 3 A/B" - GIONG NHAU ca 3 ban (bien thu la HINH):
   chip    `年金暮らしのご夫婦へ`         (10) - CHO AI + keyword `年金` (76,47 YT 30d)
   banner  `扶養親族等申告書を出さないと` (13) - VE CAI GI (chu the hang 2, 0,75)
   HERO    `課税に変わる`                 (6)  - CHUYEN GI XAY RA, dung tran 6 ky
   ribbon  `介護保険料も給付金も`         (10) - DO THEO CAI GI (domino)
   (!) khong dat so tien / 148万 len anh (feedback_so_tren_hinh_phai_do_font_ve).
   (!) 扶養親族等申告書 = 8 kanji ram lien nhau -> gen T1 truoc, soi TUNG KY TU; nat thi lui PLATE.
Cast: ong = CAST co dinh thumbnail nenkin (v28, ao xanh da troi) + ba (cardigan teal, trong palette).
Dao cu: phong bi (chu the) + bo bao cu buoc day ket phong bi (mo-tip xuyen bai) + domino (T2).
CHAY:  python tools/thumb_prompts_31.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\31_fuyo-shinkokusho-hikazei-domino")

CHIP = "年金暮らしのご夫婦へ"
BANNER = "扶養親族等申告書を出さないと"
HERO = "課税に変わる"
RIBBON = "介護保険料も給付金も"

CAST = ("a Japanese man in his mid seventies, THINNING HAIR ON TOP with a high receding "
        "hairline, short grey hair at the sides, in a LIGHT SKY BLUE collared shirt")
WIFE = ("a Japanese woman in her early seventies, grey hair tied in a low bun, in a TEAL "
        "cardigan")

PAPER = "fine ruled grid lines and faint illegible marks, no readable character or digit"
ENV = "a white window envelope showing only faint illegible lines"
BUNDLE = ("old newspapers tied with white string, an envelope edge peeking out under the "
          "string")
DOMINO = ("a row of plain navy blocks toppling one after another like dominoes, no dots, "
          "no markings")

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

COUPLE = ("RIGHT THIRD: a photograph of " + CAST + ", holding up " + ENV + ", WORRIED, "
          "brows drawn together; behind his shoulder " + WIFE + ", also worried. Cropped by the "
          "right edge, his head near the top edge, full height.\n")

CORNER = "BOTTOM-LEFT: " + BUNDLE + ", no characters written anywhere.\n\n"

PROMPTS = [
    # T1 BASELINE - khuon TELOP/A-45: ong cam phong bi, ba phia sau, net LO; goc = bo bao cu.
    ("thumb_T1_fuyo-hikazei-domino.png",
     "T1 baseline TELOP/A-45 - ong cam phong bi, ba phia sau, lo; goc duoi-trai bo bao cu",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n" + COUPLE + CORNER + BG_BASE + "\n" + QUALITY),

    # T2 doi DUNG 1 BIEN HINH: nen sau lung = hang domino dang do. Chu + layout + nguoi y nguyen.
    ("thumb_T2_fuyo-hikazei-domino.png",
     "T2 doi 1 bien HINH (chu + layout y nguyen): hang domino dang do sau lung hai ong ba",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n" + COUPLE + CORNER
     + "BACKGROUND: pale cream graph paper, flat; behind the couple " + DOMINO + ".\n"
     + QUALITY),

    # T3 doi LAYOUT - khuon kame-sensei (nen navy, hero tron dai giua, nguoi nho goc duoi-phai).
    ("thumb_T3_fuyo-hikazei-domino.png",
     "T3 doi LAYOUT: kame-sensei - nen navy, hero tron dai giua, hai ong ba NHO goc duoi-phai",
     HEAD + TEXT_BLOCK + "\n"
     "LAYOUT: the small yellow chip sits in the top left corner. The banner line runs just under "
     "it in white on a thin navy strip, one eighth of the frame high. The HERO fills the whole "
     "middle band and spans almost the entire width, the tallest and widest thing by far, looped "
     "by a red ellipse. A solid red band along the bottom edge carries the ribbon line in white.\n"
     "LOWER-RIGHT: a cut-out photograph of " + CAST + ", chest up, holding " + ENV + ", worried, "
     "with " + WIFE + " beside him, the two only one third of the frame high, clearly BELOW the "
     "hero, white die-cut border.\n"
     "BACKGROUND: flat deep navy with subtle paper texture, thin gold rays behind the hero, a "
     "small flat icon of " + BUNDLE + " at the lower left. Nothing else.\n\n" + QUALITY),
]

# PLATE de FILE RIENG - tron vao FLOW la extension bom ca file, ra anh trang chu.
PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + CAST + " holding " + ENV + ", worried, with " + WIFE + " behind "
     "his shoulder, cropped by the right edge, full height. At the bottom left, " + BUNDLE + ". "
     "Keep the whole left two thirds a plain cream field with nothing placed on it. "
     "No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper. On the right third, a photograph of " + CAST + " holding " + ENV + ", worried, "
     "with " + WIFE + " behind his shoulder, cropped by the right edge, full height, and behind "
     "them " + DOMINO + ". At the bottom left, " + BUNDLE + ". Keep the whole left two thirds a "
     "plain cream field with nothing placed on it. No text, no letters, no numbers, no "
     "watermark. --ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a solid "
     "red band along the bottom edge, and a small flat icon of " + BUNDLE + " at the lower left. "
     "At the lower right, a cut-out photograph of " + CAST + " and " + WIFE + ", chest up, only "
     "about one third of the frame height. Keep the middle band a plain navy field with nothing "
     "placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
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

    md = ["# thumbnail video 31 - 3 ban A/B (khuon TELOP/A-45 nenkin)", "",
          "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH; doi chu la hong phep do)", "",
          "| khoi | chu | ky | tra cau nao cua gate 7 |", "|---|---|---|---|",
          "| chip vang (tren-trai) | `%s` | %d | CHO AI + keyword `年金` (76,47) |"
          % (CHIP, len(CHIP)),
          "| banner navy (full width) | `%s` | %d | VE CAI GI - chu the hang 2 (0,75) |"
          % (BANNER, len(BANNER)),
          "| **HERO** vang + elip do | `%s` | %d | CHUYEN GI XAY RA - **<=6 ky** |"
          % (HERO, len(HERO)),
          "| ribbon do | `%s` | %d | DO THEO CAI GI (domino) |" % (RIBBON, len(RIBBON)), "",
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
