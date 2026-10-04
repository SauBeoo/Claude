# -*- coding: utf-8 -*-
"""gen_thumb_20.py — 3 thumbnail A/B video 20 (ab-3title-3thumb.md §3 · 03_THUMBNAIL_FORMULA.md §1.5 + §7).

Khuon lay tu ANH DA LEN SONG video 18 (07_UPLOADED/18_hataraku-okane/_upload/thumbnail*.jpg):
chip navy moc nam tren-trai · burst do 「5選」 tren-phai · dong TRANG = vat cua cold open · dong DO to nhat = keyword.
Chu GIONG NHAU ca 3 ban:
  (1) 昭和42年〜51年     moc      (cau chuyen 昭和42 → 51)
  (2) 5選               so luong
  (3) 6枚の落選はがき     ② chuyen gi — vat hien o giay 4-14 cua video
  (4) 昭和の団地          ① ve cai gi — 団地 = keyword do cao nhat dung intent (YT 30 ngay 47,3 · 2026-09-27)
T1 collage 3 o · T2 K-PHOTO canh cold open (con gai mo ngan keo) · T3 K-PHOTO doi CANH (me tre nhan hagaki 1969).
Xuat 06_VIDEO/20_sumai-okane/thumb_prompts_{FLOW.txt,TENFILE.txt,PLATE.txt,BLOCKS.md}
"""
import io, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\20_sumai-okane")

HEAD = ("YouTube thumbnail, 16:9, {style}, bold Japanese text burned into the image.")
TEXT = ("TEXT: the picture contains exactly four pieces of Japanese text and nothing else. No English word, "
        "no Latin letter and no label of any kind may appear anywhere in the image. "
        "(1) in the very top-left corner, cream-white characters on a small dark navy rounded box, reading: 昭和42年〜51年 "
        "(2) in the top-right corner, cream-white characters on a bright red starburst badge, reading: 5選 "
        "(3) a line of thick white characters with a heavy black outline, reading: 6枚の落選はがき "
        "(4) directly below it, the LARGEST element in the whole image, bright red characters with a thick white "
        "outline and a heavy black outline over it, reading: 昭和の団地")
TAIL = ("All Japanese text must be perfectly formed characters, crisp and legible, correct stroke counts, no garbled "
        "glyphs; the red line (4) is the most important text and must be perfect. Keep the very bottom-right corner "
        "completely free of text and objects. No watermark, no logo, no signature, no additional text. "
        "There is no newspaper, no printed paper, no book, no magazine and no printed surface of any kind anywhere; "
        "every postcard is plain, blank and unprinted. Avoid: English words, Latin letters, any label or instruction "
        "word rendered as text, derelict or abandoned building, ruins, horror mood, flat grey lighting, modern "
        "objects, anime style, garbled lettering, vertical lettering.")
CARDS = ("a small bundle of six old yellowed Japanese postcards held together with one brown rubber band, the cards "
         "plain and blank")

T = {
 "T1": dict(
   style="a collage of three vintage photo panels separated by clean white gutters, the whole image framed by a thin white border",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the upper middle of the frame, crossing the gutter; the red line (4) crosses the "
           "centre of the frame just below it, starting near the very left edge and running about three quarters of "
           "the way across, about one third of the frame height, taller and wider than everything else, overlapping "
           "the panel edges."),
   body=("PANELS: the tall left panel, rich warm sepia, a row of four-storey concrete public housing apartment blocks "
         "of the nineteen-sixties with laundry on the balconies and a young mother walking in front with a baby on her "
         "back; the top-right panel in saturated warm colour, close on an old wooden tea cabinet drawer pulled open "
         "with " + CARDS + " lying on folded paper beside a spool of red thread; the bottom-right panel, sepia, the "
         "entrance of an old wooden public bathhouse at night with a plain dark-blue noren curtain and a yellow "
         "washbasin on the step, the curtain plain with no lettering. COLOUR: rich warm sepia and umber for the "
         "archival panels, one panel in saturated colour, deep near-black shadows, cream highlights, very high "
         "contrast, crisp focus, photorealistic.")),
 "T2": dict(
   style="one full-bleed warm sepia photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly below it, "
           "about one third of the frame height and about four fifths of the frame width, starting near the very "
           "left edge, taller and wider than everything else; the whole left half of the picture is in deep shadow "
           "so the text stands out."),
   body=("PHOTO: the right half of the frame is a Japanese woman in her fifties with a grey cardigan, her head almost "
         "touching the top edge and cropped by the bottom edge at the chest, kneeling in front of an old wooden tea "
         "cabinet with its drawer pulled open, holding " + CARDS + " up in both hands and looking at it with wide "
         "SURPRISED eyes and parted lips, her face clearly readable, lit from one window on the right; behind her a "
         "quiet tatami room. COLOUR: warm sepia with deep near-black shadows and cream highlights, very high "
         "contrast, crisp focus, photorealistic.")),
 "T3": dict(
   style="one full-bleed warm nostalgic colour photograph, slightly faded like a well-kept 1970s photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right corner; "
           "the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly below it, "
           "about one third of the frame height and about four fifths of the frame width, starting near the very "
           "left edge, taller and wider than everything else; a dark wooden sliding door casts deep shadow over the "
           "left third so the text stands out."),
   body=("PHOTO: the right half of the frame is a young Japanese woman of about twenty-four with shoulder-length black "
         "hair and a beige cardigan, a baby asleep on her back in a carrying sling, standing in the doorway of a small "
         "wooden apartment, her head near the top edge and cropped by the bottom edge at the waist, holding one plain "
         "blank postcard in both hands and looking down at it with a DISAPPOINTED, holding-back-tears expression, "
         "her face clearly readable; behind her through the open door, blurred, a row of new concrete public housing "
         "apartment blocks far away. COLOUR: warm, gently faded 1970s colour, deep shadows, very high contrast, "
         "crisp focus, photorealistic.")),
}
PLATE_TAIL = ("There is no text of any kind anywhere in the image, no letters, no numbers, no badge and no label. "
              "Keep the upper-left area and the lower-left area dark and calm for text to be added later. "
              "No watermark, no logo, no signature.")


def one(k):
    t = T[k]
    return " ".join([HEAD.format(style=t["style"]), TEXT, t["layout"], t["body"], TAIL, "--ar 16:9"])


def main():
    bad, lines, plates, md = 0, [], [], ["# thumb_prompts_BLOCKS — video 20 (ban nguoi doc)\n",
        "Chu 4 khoi GIONG NHAU ca 3 ban: `昭和42年〜51年` · `5選` · `6枚の落選はがき` · **`昭和の団地`** (hero, 団地 YT30=47,3 — cao nhat dung intent).\n",
        "Khuon lay tu anh da len song video 18 (chip navy · burst do · trang = vat cold open · do = keyword).\n"]
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
    W("thumb_prompts_TENFILE.txt", "# dong i cua thumb_prompts_FLOW.txt -> ten file trong 06_VIDEO/20_sumai-okane/\n"
      "01\tthumb_T1_collage.png\tbaseline K-COLLAGE 3 o (danchi sepia · ngan keo hagaki MAU · 銭湯 sepia)\n"
      "02\tthumb_T2_photo_daughter.png\tK-PHOTO = canh cold open (con gai mo ngan keo, ngac nhien)\n"
      "03\tthumb_T3_photo_mother.png\tK-PHOTO doi CANH (me tre 1969 cam hagaki, that vong)\n"
      "# PLATE (khong chu) o thumb_prompts_PLATE.txt — duong lui, KHONG tron vao FLOW\n")
    W("thumb_prompts_BLOCKS.md", "\n".join(md))
    print("gate do:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
