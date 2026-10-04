# -*- coding: utf-8 -*-
"""gen_thumb_20b.py — bo thumbnail A/B THU HAI cho video 20 (CTR 3,8% sau 3 ngay, 2026-10-04).

Vi sao lam lai (doi chieu 3 anh dang chay 07_UPLOADED/20_sumai-okane/_upload/thumbnail*.jpg):
  - Chu GIONG NHAU ca 3 ban -> Test & compare chi thu HINH, chu thi chua ai thu.
  - (3) 「6枚の落選はがき」 = vat rieng cua cau chuyen, nguoi xem chua xem video khong biet 落選はがき la gi
    (落選 con goi bau cu) -> gap khong co stake.
  - (4) 「昭和の団地」 = DANH TU nhan, vi pham luat ① cua 03_THUMBNAIL_FORMULA.md (hero phai la menh de co gap).
  - Chip 「昭和42年〜51年」 khong chua so 51,4倍 (so cua 昭和41 — FACT #10).
  - Anh toi/nau (T2 nua trai gan den) — lan vao bien sepia cua ca ngach.
Bo moi: chu cho CU SOC CO THAT TRONG VIDEO + keyword 団地 (YT30 46,8 — top rổ dung intent):
  (1) 昭和40年代        moc   (bao duoc FACT #4 S43 · #5 S43 · #10 S41)
  (2) 5選              so luong
  (3) 風呂なし六畳一間    ② chuyen gi — muc ① 00:57 + muc ② 03:19 (Tokyo co 浴室 42,2% S43)
  (4) 団地は51倍         ① ve cai gi + con so — muc ③ 05:43 (6.564 戸 / 337.613 人 = 51,4倍)
T1 K-PHOTO MAU sang (canh 六畳一間) · T2 = T1 doi DUNG 1 bien: tong SEPIA · T3 doi LAYOUT: mat to + dam dong 団地.
Xuat 07_UPLOADED/20_sumai-okane/_thumb_v2/thumb_prompts_{FLOW.txt,TENFILE.txt,PLATE.txt,BLOCKS.md}
"""
import io, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\07_UPLOADED\20_sumai-okane\_thumb_v2")
OUT.mkdir(exist_ok=True)

HEAD = "YouTube thumbnail, 16:9, {style}, bold Japanese text burned into the image."
TEXT = ("TEXT: the picture contains exactly four pieces of Japanese text and nothing else. No English word, "
        "no Latin letter and no label of any kind may appear anywhere in the image. "
        "(1) in the very top-left corner, cream-white characters on a small dark navy rounded box, reading: 昭和40年代 "
        "(2) in the top-right corner, cream-white characters on a bright red starburst badge, reading: 5選 "
        "(3) a line of thick white characters with a heavy black outline, reading: 風呂なし六畳一間 "
        "(4) directly below it, the LARGEST element in the whole image, bright red characters with a thick white "
        "outline and a heavy black outline over it, reading: 団地は51倍")
TAIL = ("All Japanese text must be perfectly formed characters, crisp and legible, correct stroke counts, no garbled "
        "glyphs; the red line (4) is the most important text and must be perfect, the number 51 written once with "
        "exactly two digits. Keep the very bottom-right corner completely free of text. "
        "No watermark, no logo, no signature, no additional text. There is no newspaper, no calendar, no poster, "
        "no sign, no book and no printed surface of any kind anywhere; every postcard, towel and basin is plain and "
        "unmarked. Avoid: English words, Latin letters, any label or instruction word rendered as text, derelict or "
        "abandoned building, ruins, horror mood, flat grey lighting, modern objects, anime style, garbled lettering, "
        "vertical lettering.")

# Mot can phong -- dung chung T1/T2 de T2 chi doi DUNG mot bien (tong mau).
ROOM = ("a cramped six-tatami room of a small wooden apartment around 1970: folded futons stacked high against the "
        "wall, a low round chabudai table, a red zabuton cushion, a flower-patterned thermos flask, and in the "
        "foreground a plain yellow plastic washbasin holding a folded towel and a bar of soap, ready for the walk "
        "to the public bathhouse")
MOTHER = ("a Japanese mother of about twenty-eight with short permed black hair and an apron over a beige cardigan, "
          "a baby on her back in a carrying sling, two small children squeezed in beside her at the table")
FACE_T1 = ("her eyebrows shoot up and her mouth opens in a SURPRISED half-laugh, the look of someone who cannot "
           "believe how they used to live, her face clearly readable even at small size")
LAYOUT_PHOTO = ("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right "
                "corner; the white line (3) sits in the lower half, aligned to the left; the red line (4) sits "
                "directly below it, about one third of the frame height and about four fifths of the frame width, "
                "starting near the very left edge, taller and wider than everything else; the left third of the "
                "picture falls into soft shade from the sliding door so the text stands out.")

T = {
 "T1": dict(
   style="one full-bleed bright warm colour photograph, like a well-kept 1970s family snapshot",
   layout=LAYOUT_PHOTO,
   body=("PHOTO: " + ROOM + ". The right half of the frame is " + MOTHER + "; she kneels on the tatami, her head "
         "almost touching the top edge and cropped by the bottom edge at the waist, turned towards the viewer, "
         + FACE_T1 + ". Warm afternoon sunlight from one window on the right. COLOUR: bright, warm and clean "
         "1970s colour, cream walls, the red cushion and the yellow basin vivid, high contrast, crisp focus, "
         "photorealistic.")),
 "T2": dict(
   style="one full-bleed warm sepia photograph",
   layout=LAYOUT_PHOTO,
   body=("PHOTO: " + ROOM + ". The right half of the frame is " + MOTHER + "; she kneels on the tatami, her head "
         "almost touching the top edge and cropped by the bottom edge at the waist, turned towards the viewer, "
         + FACE_T1 + ". Warm afternoon sunlight from one window on the right. COLOUR: the whole picture in rich "
         "warm sepia and umber, deep shadows, cream highlights, very high contrast, crisp focus, photorealistic.")),
 "T3": dict(
   style="one full-bleed bright warm colour photograph, like a well-kept 1970s photograph",
   layout=("LAYOUT: the navy box (1) sits in the very top-left corner; the red badge (2) sits in the top-right "
           "corner; the white line (3) sits in the lower half, aligned to the left; the red line (4) sits directly "
           "below it, about one third of the frame height and about three fifths of the frame width, starting near "
           "the very left edge, taller and wider than everything else on the left side; the woman's face is the "
           "largest thing on the right side."),
   body=("PHOTO: a CLOSE shot. The right side of the frame, more than half of it, is the face and shoulders of a "
         "Japanese woman of about twenty-eight with short permed black hair and a beige cardigan, her head touching "
         "the top edge, cropped by the bottom edge at the chest, holding one plain blank postcard up beside her "
         "cheek, her eyes wide open and her mouth open in SHOCK, her face very clearly readable even at small size. "
         "Behind her, softly out of focus, a brand-new white five-storey concrete public housing block of the "
         "nineteen-sixties and in front of it a huge crowd of hundreds of people standing still, filling the whole "
         "width of the background, the building plain with no lettering. Bright clear daylight. COLOUR: bright, "
         "warm, clean 1970s colour, blue sky, the background slightly darker on the left so the text stands out, "
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
    md = ["# thumb_prompts_BLOCKS — video 20 bo THU HAI (2026-10-04, CTR bo 1 = 3,8%)\n",
          "Chu 4 khoi GIONG NHAU ca 3 ban: `昭和40年代` · `5選` · `風呂なし六畳一間` · **`団地は51倍`**.\n",
          "Moi cu soc tren chu deu co trong video: 六畳一間 00:57 · 銭湯 03:19 · 抽選 51,4倍 05:43 (FACT #10, S41).\n",
          "| | bien | mo ta |\n|---|---|---|\n",
          "| T1 | baseline | K-PHOTO MAU sang, canh 六畳一間 + thau 銭湯, me ngac nhien-bat cuoi |\n",
          "| T2 | 1 bien hinh = TONG MAU | y het T1 nhung SEPIA (thu: mau sang co thang bien sepia cua ngach?) |\n",
          "| T3 | layout | mat TO chiem >1/2 khung, cam hagaki, dam dong truoc 団地 moi (= 51倍 bang hinh) |\n"]
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
      "01\tthumb_T1_rokujo_color.png\tbaseline K-PHOTO mau sang (六畳一間 + thau 銭湯)\n"
      "02\tthumb_T2_rokujo_sepia.png\tT1 doi tong -> sepia\n"
      "03\tthumb_T3_danchi_face.png\tlayout mat to + dam dong 団地\n"
      "# PLATE (khong chu) o thumb_prompts_PLATE.txt — duong lui, KHONG tron vao FLOW\n")
    W("thumb_prompts_BLOCKS.md", "\n".join(md))
    print("gate do:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
