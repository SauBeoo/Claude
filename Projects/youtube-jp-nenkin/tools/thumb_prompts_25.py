# -*- coding: utf-8 -*-
r"""thumb_prompts_25.py — 3 prompt thumbnail A/B cua video 25 (天引きと手取り).

QUY TRINH theo `.claude/rules/ab-3title-3thumb.md` §3.1 — **lay khuon tu ANH DA LEN SONG,
khong tu tai lieu**:

  Buoc 1  mo `07_UPLOADED/24_shien-kyufukin-midori-futo-9gatsu/_upload/thumbnail.jpg`
  Buoc 2  DO bang may (khong ta bang cam giac):
            banner navy tren cung  22,4% chieu cao, full width
            HERO cam-vang          cao 21,4% · **rong 68% khung** (x 4% -> 72%)
            dai do day nghieng     15,6% chieu cao
            nguoi cat-nen          bat dau o **72% be ngang**, cao tron khung
          ⭐ Hero thang bang BE NGANG, khong bang chieu cao — ghi ti le RONG vao prompt,
            neu khong model ve chu vua phai roi rot legibility 120px.
  Buoc 3  chep cau truc tu `06_VIDEO/23_.../thumb_prompts_v2_FLOW.txt` (2.252 ky, TEXT @ 5%,
          ban T2 cua no da len song, kanji sach). Khoi TEXT phai nam trong **15% dau**.
  Buoc 4  xuat 4 FILE, moi file mot viec (dung gop — PLATE tron vao FLOW = 3 anh trang chu)
  Buoc 5  chu qua gate 7 + bang do keyword:
            ① ve cai gi   -> 国民年金 / 年金        (年金 = top-1 do duoc, 81,97)
            ② chuyen gi   -> 天引き 3万3千円
            ③ phai lam gi -> もらえるのは7万3千円

🔴 CHU GIONG NHAU CA 3 BAN — bien thu cua T1/T2/T3 la HINH, doi chu theo la hong phep do
   (`ab-3title-3thumb.md` §3 muc 6). T3 doi BO CUC, khong doi chu.

CHAY:  python tools/thumb_prompts_25.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\25_nenkin-tenbiki-tetori-6man2sen")

HEAD = ("A 16:9 bright Japanese YouTube thumbnail in broadcast news telop style, "
        "with bold Japanese text burned into the image.")

# ⭐ KHOI TEXT — GIONG HET o ca 3 ban, va dat NGAY CAU 2 (gate chinh: <=15% do dai prompt)
TEXT = ("TEXT, exactly these 4 blocks and nothing else: "
        "top banner, white on deep navy: 国民年金だけの方へ, "
        "second line, black with the word 天引き in red: 年金から天引き, "
        "HERO, largest and widest, golden-yellow with a thick black outline and a white "
        "halo: 3万3千円, "
        "tilted red ribbon, white characters: もらえるのは7万3千円.")

QUAL = ("Text must be perfectly formed Japanese characters, crisp and legible. "
        "Do not add any badge, stamp, sticker, seal or extra label anywhere; the top banner "
        "must be one unbroken strip of text. Keep the very bottom-right corner free of text. "
        "No watermark, no logo, no signature, no additional text. --ar 16:9")

# ── T1 — BASELINE khuon TELOP dang khoa cua kenh ───────────────────────────
T1 = " ".join([
    HEAD, TEXT,
    "LAYOUT: A deep navy banner runs across the full width of the top, a little over one "
    "fifth of the frame tall; the black second line sits just beneath it on the left; below "
    "that the golden-yellow hero line, by far the tallest and widest text in the frame, "
    "spanning about two thirds of the frame width, with one thick hand-drawn red ellipse "
    "looping right round it and a bold curved red arrow sweeping up into it from below; a "
    "large red ribbon tilted a few degrees lies across the lower left, well clear of the "
    "hero.",
    "BACKGROUND: Warm cream graph paper with a faint blue grid and softly aged warm edges, "
    "bright and evenly lit, flat with no shadows, and fine black speed lines radiating in "
    "from all four corners.",
    "ACCENTS: a warm golden glow blooming behind the hero and a few small golden bokeh "
    "sparkles scattered across the upper half.",
    "RIGHT THIRD: a pair of elderly Japanese hands entering from the right edge, the "
    "forearms in a pale blue knitted sleeve, holding open a large printed pension payment "
    "notice covered in fine ruled rows and empty boxes, tilted slightly toward the camera; "
    "no face and no head anywhere in the frame, the hands cropped by the right and bottom "
    "edges.",
    "BOTTOM-LEFT PROP: a bank passbook lying open with ruled empty columns, a plain window "
    "envelope leaning at its foot, no characters written anywhere on either.",
    QUAL])

# ── T2 — doi DUNG MOT bien hinh: NEN + dao cu (chu + bo cuc giu nguyen) ────
T2 = " ".join([
    HEAD, TEXT,
    "LAYOUT: A deep navy banner runs across the full width of the top, a little over one "
    "fifth of the frame tall; the black second line sits just beneath it on the left; below "
    "that the golden-yellow hero line, by far the tallest and widest text in the frame, "
    "spanning about two thirds of the frame width, with one thick hand-drawn red ellipse "
    "looping right round it and a bold curved red arrow sweeping up into it from below; a "
    "large red ribbon tilted a few degrees lies across the lower left, well clear of the "
    "hero.",
    "BACKGROUND: A warm wooden kitchen table shot from straight above in soft morning light "
    "through a window, honey-toned grain, bright and evenly lit with gentle shadows.",
    "ACCENTS: a warm golden glow blooming behind the hero and a few small golden bokeh "
    "sparkles scattered across the upper half.",
    "RIGHT THIRD: a pair of elderly Japanese hands entering from the right edge, the "
    "forearms in a pale blue knitted sleeve, holding open a large printed pension payment "
    "notice covered in fine ruled rows and empty boxes, tilted slightly toward the camera; "
    "no face and no head anywhere in the frame, the hands cropped by the right and bottom "
    "edges.",
    "BOTTOM-LEFT PROP: a bank passbook lying open on the table with ruled empty columns, a "
    "teacup and a plain window envelope beside it, no characters written anywhere.",
    QUAL])

# ── T3 — doi BO CUC (khuon カメ先生): bo nguoi, nen navy, hero 2 dong ~40% ──
# ⚖️ Day la phep thu dang chay tu video 21: bo cast/dong phu thi hero len 38-40% chieu cao
#    (`audience-45plus.md` §6.10 ca 19-20 — hai ca DAU TIEN dat gate 2 cua ca workspace).
#    Chu VAN GIU NGUYEN 4 khoi; thu doi la BO CUC, khong phai chu.
T3 = " ".join([
    HEAD, TEXT,
    "LAYOUT: No people anywhere in the frame. A small rounded golden-yellow pill sits "
    "centred at the very top carrying the banner text in deep navy, only about one tenth of "
    "the frame tall. Beneath it the second line and the hero line are stacked as TWO very "
    "large lines of almost equal weight filling the whole middle of the frame, together "
    "about two fifths of the frame height and spanning nearly the full width, the hero the "
    "brighter and heavier of the two, with one thick hand-drawn red ellipse looping round "
    "the hero and short red radiating burst lines fanning out behind it. A red ribbon lies "
    "flat across the bottom of the frame carrying the last block in white.",
    "BACKGROUND: A deep navy ground with a subtle darker radial vignette and fine pale "
    "speed lines radiating in from the corners, flat and evenly lit.",
    "ACCENTS: a warm golden glow blooming behind the stacked lines, four round golden yen "
    "coins floating at different sizes near the upper left, upper right and lower left, and "
    "small golden bokeh sparkles across the frame.",
    "BOTTOM-LEFT PROP: a bank passbook lying open with ruled empty columns and a plain "
    "window envelope leaning at its foot, small and low in the corner, no characters written "
    "anywhere on either.",
    QUAL])

# ── PLATE — duong lui: 3 nen KHONG CHU, de tool dot chu neu kanji gen nat ──
# 🔴 PHAI o FILE RIENG. Tron vao FLOW thi extension bom ca file va tra ve 3 anh trang chu,
#    roi nguoi doc tuong prompt chua sua (da dinh that o chouhen 21).
PLATE = [
    ("plate_T1", "A 16:9 bright Japanese YouTube thumbnail background plate. Warm cream "
     "graph paper with a faint blue grid and softly aged warm edges, bright and evenly lit, "
     "fine black speed lines radiating in from all four corners, a warm golden glow blooming "
     "in the left half. On the right third, a pair of elderly Japanese hands in pale blue "
     "knitted sleeves enter from the right edge holding open a large printed pension payment "
     "notice of fine ruled rows and empty boxes, no face and no head in frame. Bottom-left: "
     "an open bank passbook with ruled empty columns and a plain window envelope. Leave the "
     "top fifth and the whole left two thirds clear and uncluttered for text to be added "
     "later. Absolutely NO text, NO letters, NO numbers, NO characters anywhere in the "
     "image. No watermark, no logo. --ar 16:9"),
    ("plate_T2", "A 16:9 bright Japanese YouTube thumbnail background plate. A warm wooden "
     "kitchen table shot from straight above in soft morning window light, honey-toned "
     "grain, bright and evenly lit, a warm golden glow blooming in the left half. On the "
     "right third, a pair of elderly Japanese hands in pale blue knitted sleeves enter from "
     "the right edge holding open a large printed pension payment notice of fine ruled rows "
     "and empty boxes, no face and no head in frame. Bottom-left: an open bank passbook, a "
     "teacup and a plain window envelope. Leave the top fifth and the whole left two thirds "
     "clear and uncluttered for text to be added later. Absolutely NO text, NO letters, NO "
     "numbers, NO characters anywhere in the image. No watermark, no logo. --ar 16:9"),
    ("plate_T3", "A 16:9 Japanese YouTube thumbnail background plate. A deep navy ground "
     "with a subtle darker radial vignette and fine pale speed lines radiating in from the "
     "corners, flat and evenly lit, a warm golden glow blooming across the middle. Four "
     "round golden yen coins float at different sizes near the upper left, upper right and "
     "lower left, with small golden bokeh sparkles across the frame. Bottom-left: a small "
     "open bank passbook with ruled empty columns and a plain window envelope. No people "
     "anywhere. Leave the whole middle of the frame clear and uncluttered for large text to "
     "be added later. Absolutely NO text, NO letters, NO numbers, NO characters anywhere in "
     "the image. No watermark, no logo. --ar 16:9"),
]

ROWS = [("thumb_T1_tenbiki-3man3sen.png", "baseline khuon TELOP — nen giay ke o kem", T1),
        ("thumb_T2_tenbiki-3man3sen.png", "doi 1 bien HINH — nen ban bep go, tong am", T2),
        ("thumb_T3_tenbiki-3man3sen.png", "doi BO CUC — khuon カメ先生, 0 nguoi, hero 2 dong", T3)]


def main() -> int:
    os.makedirs(VD, exist_ok=True)
    w = lambda n, s: io.open(os.path.join(VD, n), "w", encoding="utf-8",
                             newline="\n").write(s)

    w("thumb_prompts_FLOW.txt", "\n".join(" ".join(p.split()) for _f, _v, p in ROWS) + "\n")
    w("thumb_prompts_TENFILE.txt", "\n".join(
        f"dong {i} -> {f}   | {v}" for i, (f, v, _p) in enumerate(ROWS, 1)) + "\n")
    w("thumb_prompts_PLATE.txt", "\n".join(" ".join(p.split()) for _n, p in PLATE) + "\n")

    md = ["# thumb 25 — 3 prompt A/B (khuon TELOP nenkin)", "",
          "Chu **giong het** o ca 3 ban; bien thu la HINH/BO CUC.", "",
          "| khoi | chu | vai |", "|---|---|---|",
          "| banner navy | `国民年金だけの方へ` | chip 対象 — tep tu loc trong 0,3 giay |",
          "| dong 2 | `年金から天引き` | keyword `年金` do duoc 81,97 (top-1) |",
          "| **HERO** | `3万3千円` | so hero, rong ~2/3 khung |",
          "| dai do day | `もらえるのは7万3千円` | dan them — mat roi duoc |", ""]
    for i, (f, v, p) in enumerate(ROWS, 1):
        pos = p.find("TEXT, exactly") * 100 // len(p)
        md += [f"### T{i} — {v}", "", f"`{f}` · {len(' '.join(p.split()))} ky · "
               f"TEXT @ {pos}%", "", "```", p, "```", ""]
    w("thumb_prompts_BLOCKS.md", "\n".join(md))

    print(f"OK -> {VD}")
    for i, (f, v, p) in enumerate(ROWS, 1):
        one = " ".join(p.split())
        pos = one.find("TEXT, exactly") * 100 // len(one)
        flag = "✅" if pos <= 15 else "🔴"
        print(f"  {flag} T{i}  {len(one):>5} ky · TEXT @ {pos:>2}%  -> {f}")
    print("     thumb_prompts_FLOW.txt · _BLOCKS.md · _TENFILE.txt · _PLATE.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
