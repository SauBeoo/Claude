# -*- coding: utf-8 -*-
r"""thumb_prompts_30.py - 3 prompt thumbnail A/B video 30 (10月15日 直前チェック) (khuon TELOP nenkin).

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
   banner  `10月15日の年金振込`  (10) - VE CAI GI + keyword `年金` (77,22 YT 30d, cao nhat ro) + moc ngay
   kicker  `8月より`             (4)  - SO VOI CAI GI, nam NGAY TREN hero
   HERO    `増える人も`          (5)  - CHUYEN GI XAY RA (chu も = co ca nguoi giam), **<=6 ky**
   ribbon  `7月の紙を見て`       (7)  - PHAI LAM GI
   (!) khong dat SO TIEN len hero: so tren anh AI hay rot chu so (feedback_so_tren_hinh_phai_do_font_ve).

VI SAO HERO KHONG PHAI SO TIEN: so tren anh AI hay rot chu so (~1/3 lan, 4 vong prompt khong chua).
Hero chu `増える人も` mang cu lat cua bai (加藤 +9.600) va chu も giu ca phia giam (中村) => khong misleading.
Banner co chu so `10月15日` - khuon da chay o v15/v29; SOI TUNG KY TU truoc khi nhan.

TRAN 4 DONG cho anh AI (§3 muc 8). Dung dung 4 khoi.
CAM `blank`/`empty`/`text-free`. So thi KHONG xin (font cua tool ve) - o day khong co so nao.

CHAY:  python tools/thumb_prompts_30.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\30_nenkin-furikomi-10gatsu-fueru-hito")

BANNER = "10月15日の年金振込"
KICKER = "8月より"
HERO = "増える人も"
RIBBON = "7月の紙を見て"

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
    "kicker above the hero, black with 8月 in red: " + KICKER + "\n"
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
    # cua bai: so ngan hang = 8月14日の行, to thong bao = 7月の紙).
    ("thumb_T1_nenkin-furikomi-10gatsu.png",
     "T1 baseline khuon TELOP/A-45 - ong gia cam SO NGAN HANG + to thong bao, ngac nhien vui",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", holding an open bank passbook in one hand and a "
     "folded notice in the other, PLEASANTLY SURPRISED with a small open-mouthed smile, cropped by "
     "the right edge, head near the top edge, body running the full height. Both have " + PAPER + ".\n"
     "BOTTOM-LEFT: a wall calendar page with one square circled in red marker.\n\n"
     + BG_BASE + "\n" + QUALITY),

    # T2 doi DUNG 1 BIEN HINH - dao cu doi sang CANH MAY IN SO (dung canh 10月15日の朝 cua bai);
    # CHU + LAYOUT giu nguyen tuyet doi.
    ("thumb_T2_nenkin-furikomi-10gatsu.png",
     "T2 doi 1 bien HINH (chu + layout y nguyen): canh truoc may in so ngan hang",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + " at a bank passbook-printing machine, pulling his "
     "printed passbook from the slot, PLEASANTLY SURPRISED, cropped by the right edge, head near "
     "the top edge, body running the full height. The page has " + PAPER + ".\n"
     "BOTTOM-LEFT: a folded notice lying flat.\n\n"
     + BG_BASE + "\n" + QUALITY),

    # T3 doi LAYOUT - khuon kame-sensei, nen navy dam, hero chiem tron dai giua.
    # Day la khuon DUY NHAT trong so do workspace **VUOT** gate 2 (hero 38-40% chieu cao),
    # vi bo rang buoc chieu doc: ong gia xuong goc duoi-phai va chi cao ~1/3 khung.
    ("thumb_T3_nenkin-furikomi-10gatsu.png",
     "T3 doi LAYOUT: khuon kame-sensei - nen navy dam, hero tron dai giua, ong gia NHO goc duoi-phai",
     HEAD + TEXT_BLOCK + "\n"
     "LAYOUT: a yellow target chip across the top carries the banner line, one eighth of the "
     "frame high. The kicker sits just under it in white, small. The HERO fills the whole middle "
     "band and spans almost the entire width, the tallest and widest thing by far. A solid red "
     "band along the bottom edge carries the ribbon line in white.\n"
     "LOWER-RIGHT: a cut-out photograph of " + CAST + ", chest up, holding an open bank "
     "passbook with a pleasantly surprised smile, only about one third of the frame high so he sits "
     "clearly BELOW the hero and never overlaps it, clean white die-cut border. The page has "
     + PAPER + ".\n"
     "BACKGROUND: one flat deep navy field with a subtle paper texture, thin gold radiating "
     "lines behind the hero, and two small flat icons at the lower left - a bank passbook and "
     "a wall calendar page. Nothing else sits in the frame.\n\n" + QUALITY),
]

# PLATE de FILE RIENG - tron vao FLOW la extension bom ca file, ra 3 anh trang chu
# (da dinh o chouhen 21). Chi dung khi anh AI gen nat kanji.
PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + CAST + " holding an open bank passbook and a folded notice, "
     "cropped by the right edge, full height. A wall calendar page lies at the "
     "bottom left. Keep the whole left two thirds a plain cream field with nothing placed on it. "
     "No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the right "
     "third, a photograph of " + CAST + " at a bank passbook-printing machine pulling out his "
     "passbook, cropped by the right edge, full height. A folded notice "
     "lies at the bottom left. Keep the whole left two thirds a plain cream field "
     "with nothing placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a solid "
     "red band along the bottom edge, and two small flat icons at the lower left - a bank "
     "passbook and a wall calendar page. At the lower right, a cut-out photograph of " + CAST + ", "
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

    md = ["# thumbnail video 30 - 3 ban A/B (khuon TELOP/A-45 nenkin)", "",
          "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH; doi chu la hong phep do)", "",
          "| khoi | chu | ky | tra cau nao cua gate 7 |", "|---|---|---|---|",
          "| banner navy (full width) | `%s` | %d | VE CAI GI + keyword `年金` (77,22) + moc ngay |"
          % (BANNER, len(BANNER)),
          "| kicker (`8月` do) | `%s` | %d | SO VOI CAI GI - NGAY TREN hero |"
          % (KICKER, len(KICKER)),
          "| **HERO** vang + elip do | `%s` | %d | CHUYEN GI XAY RA - **<=6 ky**, qua gate 1 |"
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
