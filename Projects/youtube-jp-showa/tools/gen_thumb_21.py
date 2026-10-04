# -*- coding: utf-8 -*-
"""gen_thumb_21.py — 3 thumbnail A/B video 21 (ab-3title-3thumb.md §3 · 03_THUMBNAIL_FORMULA.md §1.5 + §7).

Khuon = KHUON DANG CHAY cua kenh (chep tu gen_thumb_20.py + anh da len song 18/19/20, user 2026-10-03:
"khong giong cac prompt cu"): chip navy moc tren-trai · burst do 「5選」 tren-phai · dong TRANG = vat cua
cold open · dong DO to nhat = keyword. Ban "tuong chu" khung nam sinh: tools/gen_thumb_21_textwall.py.bak.
Chu GIONG NHAU ca 3 ban:
  (1) 昭和25〜34年生まれ  moc      (Trends YT 30 ngay 2026-10-03: 昭和生まれ 36,7 — cao nhat ro)
  (2) 5選                so luong
  (3) 母の通帳の秘密       ② chuyen gi — so tiet kiem cua me o giay 0-30 cua video
  (4) 昭和のお金           ① ve cai gi — cum お金 = cum thang cua kenh (v08 「昭和のお金」 · v18)
T1 collage 3 o · T2 K-PHOTO canh cold open (chi gai 74 lat so) · T3 K-PHOTO doi CANH (me tre 1966, dien thoai moi).
Xuat 06_VIDEO/21_umaredoshi-okane/thumb_prompts_{FLOW.txt,TENFILE.txt,PLATE.txt,BLOCKS.md}
"""
import io, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\21_umaredoshi-okane")

HEAD = ("YouTube thumbnail, 16:9, {style}, bold Japanese text burned into the image.")
TEXT = ("TEXT: the picture contains exactly four pieces of Japanese text and nothing else. No English word, "
        "no Latin letter and no label of any kind may appear anywhere in the image. "
        "(1) in the very top-left corner, cream-white characters on a small dark navy rounded box, reading: 昭和25〜34年生まれ "
        "(2) in the top-right corner, cream-white characters on a bright red starburst badge, reading: 5選 "
        "(3) a line of thick white characters with a heavy black outline, reading: 母の通帳の秘密 "
        "(4) directly below it, the LARGEST element in the whole image, bright red characters with a thick white "
        "outline and a heavy black outline over it, reading: 昭和のお金")
TAIL = ("All Japanese text must be perfectly formed characters, crisp and legible, correct stroke counts, no garbled "
        "glyphs; the red line (4) is the most important text and must be perfect. Keep the very bottom-right corner "
        "completely free of text and objects. No watermark, no logo, no signature, no additional text. "
        "There is no newspaper, no printed paper, no magazine, no calendar and no printed surface of any kind "
        "anywhere; the bankbook pages show only faint empty ruled lines with no characters, every postcard is plain "
        "and blank, and every coin is too small for any marking to be read. Avoid: English words, Latin letters, any "
        "label or instruction word rendered as text, Buddhist altar, incense, funeral, mourning clothes, derelict or "
        "abandoned building, ruins, horror mood, flat grey lighting, modern objects, anime style, garbled lettering, "
        "vertical lettering.")
BOOK = ("an old small Japanese bankbook with a plain dark-blue cover, held open, its pages showing only faint empty "
        "ruled lines")
PHONE = "a glossy black rotary dial telephone resting on a white lace doily"

T = {
 "T1": dict(
   style="a collage of three vintage photo panels separated by clean white gutters, the whole image framed by a thin white border",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the upper middle of the frame, crossing the gutter; the red line (4) crosses the "
           "centre of the frame just below it, starting near the very left edge and running about three quarters of "
           "the way across, about one third of the frame height, taller and wider than everything else, overlapping "
           "the panel edges."),
   body=("PANELS: the tall left panel, rich warm sepia, a small old Tokyo tobacco shop front of the nineteen-fifties "
         "with a red public telephone on the counter and a woman in an apron calling a neighbour to the phone, the "
         "shop front plain with no lettering; the top-right panel in saturated warm colour, close on " + BOOK + " lying "
         "on a wooden chabudai table beside " + PHONE + " and two old silver coins gleaming under lamplight; the "
         "bottom-right panel, sepia, a tall wooden valve radio glowing orange on a chest of drawers in a tatami room "
         "with a stack of plain blank New Year postcards beside it. COLOUR: rich warm sepia and umber for the "
         "archival panels, one panel in saturated colour, deep near-black shadows, cream highlights, very high "
         "contrast, crisp focus, photorealistic.")),
 "T2": dict(
   style="one full-bleed warm sepia photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly below it, "
           "about one third of the frame height and about four fifths of the frame width, starting near the very "
           "left edge, taller and wider than everything else; the whole left half of the picture is in deep shadow "
           "so the text stands out."),
   body=("PHOTO: the right half of the frame is a Japanese woman of about seventy-four with short permed grey hair "
         "and a soft beige cardigan, her head almost touching the top edge and cropped by the bottom edge at the "
         "chest, kneeling at a low wooden chabudai table at night under one warm pendant lamp, holding " + BOOK +
         " up in both hands and looking down at it with wide SURPRISED, glistening eyes and lips pressed together, "
         "holding back tears, her face clearly readable; on the table in front of her " + PHONE + "; behind her a "
         "quiet tatami room with a wooden tea cabinet, softly out of focus. COLOUR: warm sepia with deep near-black "
         "shadows and cream highlights, very high contrast, crisp focus, photorealistic.")),
 "T3": dict(
   style="one full-bleed warm nostalgic colour photograph, slightly faded like a well-kept 1970s photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly below it, "
           "about one third of the frame height and about four fifths of the frame width, starting near the very "
           "left edge, taller and wider than everything else; a dark wooden sliding door casts deep shadow over the "
           "left third so the text stands out."),
   body=("PHOTO: the right half of the frame is a Japanese mother of about forty with black hair tied back and a "
         "white kappogi apron over a plain kimono, kneeling at a low wooden chabudai table in a 1960s tatami room, her "
         "head near the top edge and cropped by the bottom edge at the waist, holding the receiver of a brand-new "
         + PHONE + " to her ear with one hand and " + BOOK + " pressed to her chest with the other, a JOYFUL, "
         "amazed smile with wide eyes, her face clearly readable; behind her, blurred, a young girl in a school "
         "uniform and a small boy peeking in from the doorway. COLOUR: warm, gently faded 1970s colour, deep "
         "shadows, very high contrast, crisp focus, photorealistic.")),
}
PLATE_TAIL = ("There is no text of any kind anywhere in the image, no letters, no numbers, no badge and no label. "
              "Keep the upper-left area and the lower-left area dark and calm for text to be added later. "
              "No watermark, no logo, no signature.")


def one(k):
    t = T[k]
    return " ".join([HEAD.format(style=t["style"]), TEXT, t["layout"], t["body"], TAIL, "--ar 16:9"])


def main():
    bad, lines, plates, md = 0, [], [], ["# thumb_prompts_BLOCKS — video 21 (ban nguoi doc)\n",
        "Chu 4 khoi GIONG NHAU ca 3 ban: `昭和25〜34年生まれ` · `5選` · `母の通帳の秘密` · **`昭和のお金`** (hero).\n",
        "Khuon = khuon dang chay (gen_thumb_20.py + anh len song 18/19/20). Trends YT 30 ngay 2026-10-03: "
        "昭和生まれ 36,7 · 昭和の常識 0,9 · お金の常識 0,3 · 昭和のお金 0.\n"]
    for k in ("T1", "T2", "T3"):
        p = one(k)
        pos = p.find("TEXT:") * 100 // len(p)
        ok = pos <= 15 and len(p) <= 3500 and "HERO" not in p
        bad += not ok
        print("%s  %d ky | TEXT @ %d%%  %s" % (k, len(p), pos, "OK" if ok else "🔴"))
        lines.append(p)
        t = T[k]
        plates.append(" ".join([HEAD.format(style=t["style"]).replace(", bold Japanese text burned into the image", ""),
                                t["body"], PLATE_TAIL, "--ar 16:9"]))
        md += ["## %s\n" % k, "**style**: " + t["style"] + "\n", t["layout"] + "\n", t["body"] + "\n",
               "(%d ky, TEXT @ %d%%)\n" % (len(p), pos)]
    W = lambda n, s: io.open(OUT / n, "w", encoding="utf-8", newline="\n").write(s)
    W("thumb_prompts_FLOW.txt", "\n".join(lines) + "\n")
    W("thumb_prompts_PLATE.txt", "\n".join(plates) + "\n")
    W("thumb_prompts_TENFILE.txt", "# dong i cua thumb_prompts_FLOW.txt -> ten file trong 06_VIDEO/21_umaredoshi-okane/\n"
      "01\tthumb_T1_collage.png\tbaseline K-COLLAGE 3 o (tiem thuoc la + dien thoai do sepia · so tiet kiem + 黒電話 MAU · radio sepia)\n"
      "02\tthumb_T2_photo_sister.png\tK-PHOTO = canh cold open (chi gai 74 lat so, xuc dong)\n"
      "03\tthumb_T3_photo_mother.png\tK-PHOTO doi CANH (me 1966 nghe dien thoai moi, om so)\n"
      "# PLATE (khong chu) o thumb_prompts_PLATE.txt — duong lui, KHONG tron vao FLOW\n")
    W("thumb_prompts_BLOCKS.md", "\n".join(md))
    print("gate do:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
