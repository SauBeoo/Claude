# -*- coding: utf-8 -*-
"""gen_thumb_19b.py — bo thumbnail A/B THU HAI cho video 19 昭和の買い物 (2026-10-04, cung chan doan video 20).

Bo v1 dang chay (07_UPLOADED/19_kaimono-joushiki/_upload/thumbnail*.jpg):
  - chu GIONG NHAU ca 3 ban: 「がま口の質札」 (vat rieng cua cau chuyen) + 「昭和の買い物」 (DANH TU nhan, vi pham luat ①).
  - keyword do cao nhat ro (消費税 YT30 38,4, related 「食料品 消費税 ゼロ」) khong co tren thumbnail.
  - anh toi/nau, T1 collage 3 o.
Bo moi — moi cu soc co trong video:
  (1) 昭和30〜60年代   moc (質屋 S33 · 割賦法 S36 · TV S45 · 大店法 S49 · 昭和64)
  (2) 5選
  (3) テレビは月賦      muc ① 00:55 (割賦販売法 S36, 普及率 S45 26,3%)
  (4) 消費税0%         muc ⑤ 09:59 (消費税法 ap dung 平成元.4.1 => ca 昭和 khong co 消費税; video tra them: 物品税 an trong gia)
T1 K-PHOTO MAU sang (ca nha quanh TV mau moi, bo cam vi) · T2 = T1 doi tong SEPIA · T3 layout: mat to tai tiem dien.
"""
import io, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\07_UPLOADED\19_kaimono-joushiki\_thumb_v2")
OUT.mkdir(exist_ok=True)

HEAD = "YouTube thumbnail, 16:9, {style}, bold Japanese text burned into the image."
TEXT = ("TEXT: the picture contains exactly four pieces of Japanese text and nothing else. No English word, "
        "no Latin letter and no label of any kind may appear anywhere in the image. "
        "(1) in the very top-left corner, cream-white characters on a small dark navy rounded box, reading: 昭和30〜60年代 "
        "(2) in the top-right corner, cream-white characters on a bright red starburst badge, reading: 5選 "
        "(3) a line of thick white characters with a heavy black outline, reading: テレビは月賦 "
        "(4) directly below it, the LARGEST element in the whole image, bright red characters with a thick white "
        "outline and a heavy black outline over it, reading: 消費税0%")
TAIL = ("All Japanese text must be perfectly formed characters, crisp and legible, correct stroke counts, no garbled "
        "glyphs; the red line (4) is the most important text and must be perfect, the line (4) ends with one zero and one percent sign, written once. Keep the very bottom-right corner completely free of text. "
        "No watermark, no logo, no signature, no additional text. There is no newspaper, no calendar, no poster, "
        "no sign, no book and no printed surface of any kind anywhere; every wallet, bundle, cup and cabinet is plain and unmarked, and every "
        "television screen shows only a soft blank glow with no picture and no writing. Avoid: English words, Latin letters, any label or instruction word rendered as text, derelict or "
        "abandoned building, ruins, horror mood, flat grey lighting, modern objects, anime style, garbled lettering, "
        "vertical lettering.")

# Mot canh -- dung chung T1/T2 de T2 chi doi DUNG mot bien (tong mau).
# Hoan canh bai: TV mau mua bang 月賦, thang thieu tien gop -> phai mang do di 質屋. KHAC KHO, khong vui ve.
ROOM = ("a cramped, worn but tidy six-tatami room of a small rented house on a winter evening around 1970, lit by one "
        "bare light bulb hanging from the ceiling: the tatami frayed, a low "
        "chabudai with one chipped teacup, and in the back of the room a brand-new colour television in a wooden "
        "cabinet on four short legs, its screen softly glowing, the only new and shiny thing in the house, two small "
        "children in hand-knitted sweaters sitting in front of it, their backs to us")
MAN = ("a thin, tired Japanese father of about forty with short black hair going grey at the temples and stubble on "
       "his cheeks, a faded work shirt under an old grey cardigan with a darned elbow, holding a thin, worn brown "
       "leather wallet open in one hand and looking down at three or four small coins in his other palm")
FACE_T1 = ("his brow deeply furrowed, his lips pressed tight, his eyes heavy and WORRIED, the face of a man who does not "
           "know how he will make this month's payment, his face clearly readable even at small size")
LAYOUT_PHOTO = ("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right "
                "corner; the white line (3) sits in the lower half, aligned to the left; the red line (4) sits "
                "directly below it, about one third of the frame height and about four fifths of the frame width, "
                "starting near the very left edge, taller and wider than everything else; the left third of the "
                "picture falls into deep shade from the sliding door so the text stands out.")

T = {
 "T1": dict(
   style="one full-bleed warm colour photograph, like a real 1970s family photograph",
   layout=LAYOUT_PHOTO,
   body=("PHOTO: " + ROOM + ". The right half of the frame is " + MAN + "; he sits cross-legged on the tatami in "
         "the foreground, his head almost touching the top edge and cropped by the bottom edge at the waist, his "
         "body turned three-quarters towards the viewer, " + FACE_T1 + ". COLOUR: warm amber light from the single "
         "bulb on his face, deep shadows in the corners, muted worn colours, the "
         "television glow the brightest colour, high contrast, crisp focus, photorealistic.")),
 "T2": dict(
   style="one full-bleed warm sepia photograph",
   layout=LAYOUT_PHOTO,
   body=("PHOTO: " + ROOM + ". The right half of the frame is " + MAN + "; he sits cross-legged on the tatami in "
         "the foreground, his head almost touching the top edge and cropped by the bottom edge at the waist, his "
         "body turned three-quarters towards the viewer, " + FACE_T1 + ". COLOUR: the whole picture in rich warm "
         "sepia and umber, deep shadows, cream highlights on his face, very high contrast, crisp focus, "
         "photorealistic.")),
 "T3": dict(
   style="one full-bleed warm colour photograph, like a real 1970s photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right "
           "corner; the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly "
           "below it, about one third of the frame height and about three fifths of the frame width, starting near "
           "the very left edge, taller and wider than everything else on the left side; the man's face is the "
           "largest thing on the right side."),
   body=("PHOTO: a CLOSE shot at the dim wooden entrance of a small rented house on a winter evening around 1970. "
         "The right side of the frame, more than half of it, is the face and shoulders of a thin, tired Japanese "
         "man of about forty with short black hair going grey at the temples and stubble on his cheeks, an old "
         "grey cardigan over a faded work shirt, his head touching the top edge, cropped by the bottom edge at the "
         "chest, clutching a cloth bundle wrapped in a plain dark furoshiki against his chest with both arms, "
         "about to carry it to the pawnshop, his brow furrowed, his jaw clenched and his eyes glistening, holding "
         "back his feelings, his face very clearly readable even at small size. Behind him, softly out of focus, "
         "inside the dim room, a brand-new colour television in a wooden cabinet glowing, and two small children "
         "watching it. One bare bulb, cold blue dusk through the door glass. COLOUR: warm amber on his face against "
         "cold blue evening shadow, muted worn colours, the background darker on the left so the text stands out, "
         "high contrast, crisp focus, photorealistic.")),
}
PLATE_TAIL = ("There is no text of any kind anywhere in the image, no letters, no numbers, no badge and no label. "
              "Keep the upper-left area and the lower-left area calm and slightly shaded for text to be added later. "
              "No watermark, no logo, no signature.")


def one(k):
    t = T[k]
    return " ".join([HEAD.format(style=t["style"]), TEXT, t["layout"], t["body"], TAIL, "--ar 16:9"])


def main():
    bad, lines, plates = 0, [], []
    md = ["# thumb_prompts_BLOCKS — video 19 bo THU HAI (2026-10-04)\n",
          "Chu 4 khoi GIONG NHAU ca 3 ban: `昭和30〜60年代` · `5選` · `テレビは月賦` · **`消費税0%`**.\n",
          "Moi cu soc tren chu deu co trong video: 月賦 00:55 · 消費税/物品税 09:59 (FACT #1).\n",
          "| | bien | mo ta |\n|---|---|---|\n",
          "| T1 | baseline | K-PHOTO MAU sang, ca nha quanh TV mau moi, bo cam vi ngac nhien-bat cuoi |\n",
          "| T2 | 1 bien hinh = TONG MAU | y het T1 nhung SEPIA (thu: mau sang co thang bien sepia cua ngach?) |\n",
          "| T3 | layout | mat TO chiem >1/2 khung, om goi furoshiki di 質屋 |\n"]
    for k in ("T1", "T2", "T3"):
        p = one(k)
        pos = p.find("TEXT:") * 100 // len(p)
        ok = pos <= 15 and len(p) <= 3500 and "HERO" not in p
        bad += not ok
        print("%s  %d ky | TEXT @ %d%%  %s" % (k, len(p), pos, "OK" if ok else "DO"))
        lines.append(p)
        t = T[k]
        plates.append(" ".join([HEAD.format(style=t["style"]).replace(", bold Japanese text burned into the image", ""),
                                t["body"], PLATE_TAIL, "--ar 16:9"]))
        md += ["\n## %s\n" % k, "**style**: " + t["style"] + "\n", t["layout"] + "\n", t["body"] + "\n",
               "(%d ky, TEXT @ %d%%)\n" % (len(p), pos)]
    W = lambda n, s: io.open(OUT / n, "w", encoding="utf-8", newline="\n").write(s)
    W("thumb_prompts_FLOW.txt", "\n".join(lines) + "\n")
    W("thumb_prompts_PLATE.txt", "\n".join(plates) + "\n")
    W("thumb_prompts_TENFILE.txt", "# dong i cua thumb_prompts_FLOW.txt -> ten file trong _thumb_v2/\n"
      "01\tthumb_T1_tv_color.png\tbaseline K-PHOTO mau am: bo kiet suc dem vai dong xu, TV mau moi (月賦) sau lung\n"
      "02\tthumb_T2_tv_sepia.png\tT1 doi tong -> sepia\n"
      "03\tthumb_T3_furoshiki_face.png\tlayout mat to: bo om goi furoshiki di 質屋, TV sau lung\n"
      "# PLATE (khong chu) o thumb_prompts_PLATE.txt — duong lui, KHONG tron vao FLOW\n")
    W("thumb_prompts_BLOCKS.md", "\n".join(md))
    print("gate do:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
