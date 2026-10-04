# -*- coding: utf-8 -*-
r"""thumb_prompts_28.py - 3 prompt thumbnail A/B video 28 (khuon TELOP nenkin).

QUY TRINH `ab-3title-3thumb.md` §3.1 - 4 BUOC, khong dao.

B1. KHUON LAY TU ANH DA LEN SONG, khong tu tai lieu:
    `07_UPLOADED/27_nenkin-tsuchisho-nai-okane-5tsu/_upload/thumbnail.jpg`
B2. DO BANG MAY ban do (1376x768, do 2026-09-21):
      BANNER navy : y 0-147   = **19,1% chieu cao**, chay HET be ngang
      HERO vang   : x 55-1207 = **83,7% BE NGANG** - y 253-465 = 27,6% cao - co ELIP DO
      RIBBON do   : y 550-688 = **72%-90% chieu cao**, cheo nhe, chu trang, mui ten do cong
      ANH NGUOI   : tu ~x=62% sang phai, cao TRON khung (khong lo lung)
      Nen kem sang: RGB (201,181,118) o mep trai
    * Ban 27 rong **83,7%** (hero 8 ky) - xac nhan lai bai hoc: thu mua duoc legibility
      la **BE NGANG**, khong phai chieu cao (ban 27 chi cao 27,6% van doc ro o 120px).
      Hero cua 28 chi 5 ky => phai ghi ro "spans about two thirds of the frame width",
      neu khong model se ve nho lai.
B3. Khoi TEXT trong **15% DAU** prompt (gate chinh).
B4. Xuat 4 FILE, moi file mot viec.

CHU - GIONG NHAU ca 3 ban (bien thu la HINH), qua gate 7 `audience-45plus.md` §1:
   (1) AI          -> banner  nen-kin ... `年金を受け取る75歳の方へ`  (keyword 年金 = 82,53 dung DAU)
   (2) VE CAI GI   -> line2   `誕生月から変わります`   (lap cum hook cua Title CHOT)
   (3) CHUYEN GI   -> HERO    `2年で3倍`               (5 ky, duoi tran 6)
   (4) LAM GI      -> ribbon  `7月の紙を探して`
   `後期高齢者医療保険料` do duoc **0,03** tren YT search => KHONG len thumbnail, chi vao tag.
   Title di bang `年金`, thumbnail cung di bang `年金` - mot duong, khong tach.

TRAN 4 DONG cho anh AI (§3 muc 8). Dung dung 4 khoi. Them khoi thu 5 = meo kanji.
CAM moi tu `blank` / `empty` / `text-free` (CLAUDE.md §2) - chung keo model ve phia ve
   mang trong. Ta CAI CO MAT: "fine ruled grid and faint illegible texture marks".
   SO tren giay VAN CAM (`feedback_so_tren_hinh_phai_do_font_ve`).

CHAY:  python tools/thumb_prompts_28.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\28_kouki-75sai-tanjyotsuki-hokenryo")

BANNER = "年金を受け取る75歳の方へ"
LINE2 = "誕生月から変わります"
HERO = "2年で3倍"
RIBBON = "7月の紙を探して"

# CAST co dinh cua thumbnail nenkin - ta MOT LAN, dung CHUNG ca 3 ban. Toc ta bang HAI
# moc cu the (thua tren dinh + tran cao) chu khong noi "balding": tu chung chung thi moi
# ban ra mot kieu dau, ma cai mua duoc o thumbnail la NHAN DIEN LAP LAI.
# 🔵 AO XANH DA TROI (user chot 2026-09-21). BO gilet len - hai lop ao thi mau xanh chi
#    con o co + tay, o 120px gan nhu khong doc ra duoc; mot lop ao xanh = MOT MANG mau
#    lien, doc duoc ca o ban T3 nen navy (da co vien cat-nen trang tach ra).
CAST = ("a Japanese man in his mid seventies, THINNING HAIR ON TOP with a high receding "
        "hairline, short grey hair at the sides, in a LIGHT SKY BLUE collared shirt")

PAPER = "fine ruled grid lines and faint illegible texture marks, no readable character or digit on it"

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, with a "
           "thick black outline and a white halo around every glyph. No watermark, no logo and "
           "no extra text. Keep the very bottom-right corner free of text. --ar 16:9")

TEXT_BLOCK = (
    "TEXT, exactly these 4 blocks and nothing else:\n"
    "top banner, white on navy: " + BANNER + "\n"
    "line 2, black with the three characters 誕生月 in red: " + LINE2 + "\n"
    "HERO, LARGEST block by far, gold gradient with heavy black outline: " + HERO + "\n"
    "bottom ribbon, white on red: " + RIBBON + "\n")

LAYOUT_BASE = (
    "LAYOUT: the navy banner is a full-width bar across the very top, one fifth of the frame "
    "high. Line 2 sits under it on the LEFT. The HERO spans about TWO THIRDS OF THE FRAME "
    "WIDTH, far the tallest and widest block, looped by a hand-drawn red ellipse. The red ribbon crosses the lower left, tilted a few degrees, its top "
    "edge at seven tenths of the frame height, a curved red arrow rising from it to the hero.")

BG_BASE = ("BACKGROUND: pale cream graph paper, warm yellow glow spots, thin black speed "
           "lines radiating in from the edges, flat.")

HEAD = ("A bold Japanese YouTube thumbnail for a pension money channel, 16:9, bright and "
        "high-contrast, with large Japanese text burned into the image.\n\n")

PROMPTS = [
    # T1 BASELINE - khuon dang chay, dao cu = to 保険料額決定通知書 + phong bi
    ("thumb_T1_75sai_kintouwari.png",
     "T1 baseline khuon TELOP/A-45 - y het ban 27 dang chay, chi doi dao cu sang 決定通知書",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", holding up one printed municipal notice "
     "sheet with both hands, worried frown, cropped by the right edge, "
     "head almost touching the top edge and body running the full height. The sheet has "
     + PAPER + ".\n"
     "BOTTOM-LEFT: a cream window envelope lying flat, one faint ruled line in its address "
     "window.\n\n" + BG_BASE + "\n" + QUALITY),

    # T2 doi DUNG 1 BIEN HINH - dao cu doi sang so ngan hang, CHU + LAYOUT giu nguyen
    ("thumb_T2_75sai_kintouwari.png",
     "T2 doi 1 bien HINH (chu + layout y nguyen): dao cu = so ngan hang mo ra, tay chi vao dong",
     HEAD + TEXT_BLOCK + "\n" + LAYOUT_BASE + "\n"
     "RIGHT THIRD: a photograph of " + CAST + ", holding an open bank passbook on his palm "
     "and pointing one finger at a line in it, eyebrows drawn together, cropped by the right "
     "edge, head almost touching the top edge and body running the full height. The passbook "
     "pages have " + PAPER + ".\n"
     "BOTTOM-LEFT: reading glasses resting on a folded cream sheet.\n\n"
     + BG_BASE + "\n" + QUALITY),

    # T3 doi LAYOUT - khuon kame-sensei, nen navy dam, hero chiem tron dai giua.
    # Day la khuon DUY NHAT trong so do workspace **VUOT** gate 2 (hero 38-40% chieu cao),
    # vi bo rang buoc chieu doc: ong gia xuong goc duoi-phai va chi cao ~1/3 khung.
    # De ong chay tron chieu cao o day thi T3 mat dung cai no dang thu nghiem.
    ("thumb_T3_75sai_kintouwari.png",
     "T3 doi LAYOUT: khuon kame-sensei - nen navy dam, hero chiem tron dai giua, ong gia NHO goc duoi-phai",
     HEAD + TEXT_BLOCK + "\n"
     "LAYOUT: a yellow target chip across the top carries the banner line, one eighth of the "
     "frame high. Line 2 sits just under it in white. The HERO fills the whole middle band "
     "and spans almost the entire width, the tallest and widest thing by far. A solid red "
     "band along the bottom edge carries the ribbon line in white.\n"
     "LOWER-RIGHT: a cut-out photograph of " + CAST + ", chest up, holding one printed notice "
     "sheet with a puzzled tilt of the head, only about one third of the frame high so he "
     "sits clearly BELOW the hero and never overlaps it, clean white die-cut border. The "
     "sheet has " + PAPER + ".\n"
     "BACKGROUND: one flat deep navy field with a subtle paper texture, thin gold radiating "
     "lines behind the hero, and two small flat icons at the lower left - a calendar page "
     "and a stack of coins. Nothing else sits in the frame.\n\n"
     + QUALITY),
]

# PLATE de FILE RIENG - tron vao FLOW la extension bom ca file, ra 3 anh trang chu
# (da dinh o chouhen 21). Chi dung khi anh AI gen nat kanji.
PLATE = [
    ("plate_T1.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the "
     "right third, a photograph of " + CAST + " holding up one printed notice sheet with "
     "fine ruled grid lines on it, cropped by the right edge, full height. A cream window "
     "envelope lies flat at the bottom left. Keep the whole left two thirds a plain cream "
     "field with nothing placed on it. No text, no letters, no numbers, no watermark. --ar 16:9"),
    ("plate_T2.png", "A bold Japanese YouTube thumbnail background plate, 16:9, pale cream "
     "graph paper with warm glow spots and thin black speed lines from the edges. On the "
     "right third, a photograph of " + CAST + " holding an open bank passbook on his palm "
     "and pointing at a line in it, cropped by the right edge, full height. Reading glasses "
     "on a folded cream sheet at the bottom left. Keep the whole left two thirds a plain "
     "cream field with nothing placed on it. No text, no letters, no numbers, no watermark. "
     "--ar 16:9"),
    ("plate_T3.png", "A bold Japanese YouTube thumbnail background plate, 16:9, one flat deep "
     "navy field with subtle paper texture, thin gold radiating lines across the middle, a "
     "solid red band along the bottom edge, and two small flat illustrated icons at the lower "
     "left - a simple calendar page and a stack of coins. At the lower right, a cut-out "
     "photograph of " + CAST + ", chest up, only about one third of the frame height. Keep "
     "the middle band a plain navy field with nothing placed on it. No text, no letters, no "
     "numbers, no watermark. --ar 16:9"),
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

    md = ["# thumbnail video 28 - 3 ban A/B (khuon TELOP/A-45 nenkin)", "",
          "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH; doi chu la hong phep do)", "",
          "| khoi | chu | ky | tra cau nao cua gate 7 |", "|---|---|---|---|",
          "| banner navy (full width) | `%s` | %d | AI - keyword `年金` 82,53 dung DAU |"
          % (BANNER, len(BANNER)),
          "| line 2 (`誕生月` do) | `%s` | %d | VE CAI GI - lap cum hook cua Title CHOT |"
          % (LINE2, len(LINE2)),
          "| **HERO** vang + elip do | `%s` | %d | CHUYEN GI - duoi tran 6 ky |"
          % (HERO, len(HERO)),
          "| ribbon do | `%s` | %d | PHAI LAM GI |" % (RIBBON, len(RIBBON)), "",
          "## So do - do bang may tu ban DANG CHAY (video 27, 1376x768, 2026-09-21)", "",
          "| khoi | so do |", "|---|---|",
          "| banner navy | y 0-147 = **19,1% chieu cao**, full width |",
          "| hero vang | x 55-1207 = **83,7% be ngang** - y 253-465 = 27,6% cao - elip do |",
          "| ribbon do | y 550-688 = **72%-90% chieu cao**, cheo nhe + mui ten do cong |",
          "| anh nguoi | tu ~**x=62%** sang phai, cao TRON khung |",
          "| nen kem | RGB (201,181,118) o mep trai |", "",
          "## 3 ban", ""]
    for i, (f, d, p) in enumerate(PROMPTS, 1):
        md += ["### %d. `%s`" % (i, f), "", d, "", "```", p, "```", ""]
    md += ["## Plate khong chu (duong lui, file rieng)", "",
           "Chi dung khi anh AI gen nat kanji -> render chu bang `tools/make_thumb_45.py`.", ""]
    io.open(os.path.join(VD, "thumb_prompts_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md))

    # GATE: khoi TEXT trong 15% DAU + do dai <= 1750 ky + khong con tu cam
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
    print("\n%s - 4 file -> %s" % ("SACH" if not bad else "GATE DO", VD))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
