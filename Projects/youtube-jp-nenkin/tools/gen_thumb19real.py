# -*- coding: utf-8 -*-
r"""gen_thumb19real.py — 3 prompt thumbnail A/B cho video 19 (khuon dang chay).

User chot 2026-09-03: *"cho tao prompt gen anh thumbnail luon nhe"*.

📐 KHUON LAY TU **ANH DA LEN SONG**, khong tu tai lieu (`ab-3title-3thumb.md`
   §3.1 Buoc 1 — tai lieu co the ta mot quy trinh da chet). Anh mau:
   `07_UPLOADED/24_shien-kyufukin-midori-futo-9gatsu/_upload/thumbnail.jpg`
   Do bang may (Buoc 2), khung 2752x1536:
     · banner navy tren  : **22,4% chieu cao**
     · HERO vang-cam     : cao **19,9%** · **rong 71,1%**  <- BE NGANG moi la thu
       mua duoc kha nang doc o 120px, khong phai chieu cao
     · dai do day        : ~14%
     · nguoi ben phai    : cao tron khung, rong ~1/3, cat nen vien trang
     · nen               : giay ke o kem
     · trang tri         : vong khoanh do quanh hero + mui tui do cong

🔴 GATE CHINH (§3.1 Buoc 3): khoi **TEXT phai nam trong 15% DAU prompt**. Dat
   cuoi thi model bam ta canh va **nuot chu** (da dinh that o chouhen 21). Hai
   ban bake chu Nhat THANH CONG (co-dai 17 · nenkin 09) deu de TEXT o dau.
🔴 Tran **4 DONG chu** cho anh AI; 5 dong gan nhu chac meo kanji.
🔴 Xuat **4 FILE, moi file mot viec** — dac biet PLATE (ban khong chu) phai o
   file RIENG: tron vao FLOW thi extension bom ca file, plate ghi "no text" nen
   ra anh trang chu, tuong prompt chua sua (da dinh o chouhen 21).

🔴 DUNG DAT TEN VAI TRONG KHOI TEXT: ban dau ghi "HERO line, LARGEST by far..."
   => model **ve nguyen chu "HERO"** vao anh (task_003 phai bo). Trong khoi TEXT,
   model coi MOI THU la chu can bake. Dung "first/second/third/fourth line" +
   ta mau, con vai (hero/banner/ribbon) thi noi o khoi LAYOUT.

🔴 CHAN CHU RAC: model van ve kanji VO NGHIA vao bien hieu va giay to du prompt
   ghi "no extra text" o cuoi (anh T2: 「試業試務出口」・「耽証券」). Phai ghi
   `no characters written anywhere` NGAY TRONG khoi dao cu/nen — da them.

CHAY:  python tools/gen_thumb19real.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")

# ── chu: 3 khoi + badge (spec da chot trong script 19) ────────────────────
BANNER = "60歳から働く人へ"        # ① VE CAI GI      — chip doi tuong
SUB    = "15％が10％に"             # (dong phu, den + DO o so)
HERO   = "5年で84万円"              # ② CHUYEN GI XAY RA — to nhat
FOOT   = "一日違いで変わります"      # ③ MOC / PHAI LAM GI

# 🔴 KHONG dat ten vai (HERO/banner/ribbon) trong khoi nay — model coi MOI THU
# trong khoi TEXT la chu can bake, va da ve nguyen chu "HERO" vao anh task_003.
# Chi danh so dong + ta mau; vai thi noi o khoi LAYOUT.
TEXT_BLOCK = (
    'TEXT, bake exactly these 4 lines into the image and nothing else, '
    'as perfectly formed Japanese characters:\n'
    f'line 1, white: {BANNER}\n'
    f'line 2, black with the numbers in red: {SUB}\n'
    f'line 3, LARGEST by far, warm yellow-to-orange gradient: {HERO}\n'
    f'line 4, white: {FOOT}'
)

LAYOUT = (
    "LAYOUT: line 1 sits in a deep navy strip across the very top taking about ONE FIFTH "
    "of the height, its white text filling it. Line 2 sits just below on the cream paper. "
    "Line 3 is the main headline - it must be BOTH the tallest AND by far the widest "
    "element, spanning about SEVEN TENTHS of the frame width, in thick rounded gothic "
    "with a heavy black outline and a white halo behind it, a hand-drawn red ellipse "
    "looping around it and one curved red arrow pointing up into it. Line 4 sits on a "
    "deep red ribbon band across the lower left, tilted very slightly."
)
BG = ("BACKGROUND: pale cream paper with a faint printed grid, flat and evenly lit, "
      "no shadows, no gradient.")
QUALITY = ("Text must be perfectly formed Japanese characters, crisp, high-contrast and "
           "legible even at thumbnail size. No watermark, no logo, no signature, no "
           "extra text anywhere. Keep the very bottom-right corner completely free of "
           "text. 16:9.")

# ── 3 bien the: doi DUNG MOT BIEN moi ban ────────────────────────────────
VARIANTS = {
    "T1": dict(
        note="baseline khuon kenh — ong 60 tuoi cam giay luong, tuong kem",
        right=("RIGHT THIRD: a photoreal Japanese man of 60, slim, short salt-and-pepper "
               "hair receding at the temples, faded navy work jacket over a grey polo, "
               "looking DOWN at a payslip he holds in both hands with a worried frown, "
               "cut out with a thick white sticker outline, standing full height from the "
               "banner down to the bottom edge. Nothing he holds has any characters "
               "written on it."),
        corner=("BOTTOM-LEFT: a payslip and a brown pay envelope lying flat, with no "
                "characters written anywhere on them."),
    ),
    "T2": dict(
        note="doi 1 BIEN HINH: nen -> quay Hello Work (chu GIU NGUYEN)",
        right=("RIGHT THIRD: the same photoreal Japanese man of 60, slim, short "
               "salt-and-pepper hair receding at the temples, faded navy work jacket over "
               "a grey polo, looking DOWN at a payslip in both hands with a worried frown, "
               "cut out with a thick white sticker outline, standing full height; behind "
               "him a softly blurred public employment office counter with NO signage and NO "
               "characters written anywhere on it."),
        corner=("BOTTOM-LEFT: a numbered queue ticket and a brown pay envelope lying flat, "
                "with absolutely no characters written anywhere on them."),
    ),
    "T3": dict(
        note="doi LAYOUT: bo mat nguoi, minh chi tiet + but do khoanh lam hero ~3/4 khung",
        right=("RIGHT SIDE: no person at all. Instead a large photoreal close-up of a "
               "Japanese payslip lying at a slight angle, its ruled rows carrying small "
               "printed figures too small to read, with ONE row circled in red ballpoint "
               "and a red pen resting across the sheet; it fills the right two thirds "
               "behind the text, brightly and evenly lit."),
        corner=("BOTTOM-LEFT: an older hand entering the frame holding the red pen, no "
                "face visible, no characters written anywhere."),
    ),
}

HEAD = ("Bold YouTube thumbnail for a Japanese pension channel, 16:9, flat graphic poster "
        "style with photoreal cut-out subjects and BOLD JAPANESE TEXT BURNED INTO THE "
        "IMAGE.")


def build():
    flow, plate, ten, md = [], [], [], []
    md.append("# THUMBNAIL video 19 — 3 ban A/B (khuon do tu anh da len song)\n")
    md.append(
        "> Khuon lay tu `07_UPLOADED/24_.../thumbnail.jpg` (anh DANG CHAY), do bang may:\n"
        "> banner navy **22,4%** chieu cao · HERO cao **19,9%** nhung **rong 71,1%** ·\n"
        "> dai do day ~14% · nguoi ben phai cao tron khung rong ~1/3 · nen giay ke o kem.\n>\n"
        "> ⭐ **BE NGANG moi mua duoc kha nang doc o 120px, khong phai chieu cao** —\n"
        "> day la ly do HERO phai rong ~7/10 khung (`ab-3title-3thumb.md` §3.1 Buoc 2).\n>\n"
        "> 🔴 Khoi TEXT nam trong **15% dau** moi prompt (gate chinh §3.1 Buoc 3).\n"
        "> 🔴 Dung **PLATE** o file rieng — tron vao FLOW la ra 3 anh trang chu.\n")
    md.append("\n## Chu (giong nhau ca 3 ban — bien thu la HINH)\n")
    md.append("| khoi | chu | vai |\n|---|---|---|")
    md.append(f"| banner navy | `{BANNER}` | ① VE CAI GI (chip doi tuong) |")
    md.append(f"| dong phu | `{SUB}` | so DO — cu lat cua bai |")
    md.append(f"| **HERO** vang-cam | `{HERO}` | ② CHUYEN GI XAY RA |")
    md.append(f"| dai do day | `{FOOT}` | ③ MOC thoi gian |")
    md.append("\n## 3 ban\n")
    md.append("| ban | doi bien gi |\n|---|---|")

    for key, v in VARIANTS.items():
        p = " ".join([HEAD, TEXT_BLOCK.replace("\n", " "), LAYOUT, BG,
                      v["right"], v["corner"], QUALITY])
        p = " ".join(p.split())
        flow.append(p)
        # PLATE: cung layout, KHONG chu — duong lui neu kanji nat
        pl = " ".join([HEAD.replace(" and BOLD JAPANESE TEXT BURNED INTO THE IMAGE", ""),
                       LAYOUT.replace("its white text filling it", "left completely EMPTY")
                       .replace("with the bottom line on it", "left completely EMPTY"),
                       BG, v["right"], v["corner"],
                       "Absolutely NO text, NO letters, NO numbers anywhere in the image - "
                       "leave the banner, the hero area and the ribbon as clean empty "
                       "shapes for text to be added later. No watermark. 16:9."])
        pl = " ".join(pl.split())
        # bo khoi TEXT khoi plate
        for s in (TEXT_BLOCK.replace("\n", " "), BANNER, SUB, HERO, FOOT):
            pl = pl.replace(s, "")
        plate.append(" ".join(pl.split()))
        ten.append(f"{key}  -> thumb_{key}_84man.png".ljust(38) + f"({v['note']})")
        md.append(f"| **{key}** | {v['note']} |")

    md.append("\n---\n")
    for key, p, pl in zip(VARIANTS, flow, plate):
        md.append(f"\n## {key} — {VARIANTS[key]['note']}\n")
        pos = p.find("TEXT, bake") / len(p) * 100
        md.append(f"*({len(p)} ky · khoi TEXT o {pos:.0f}% dau)*\n\n```\n{p}\n```\n")
        md.append(f"**PLATE (khong chu, duong lui)** *({len(pl)} ky)*\n\n```\n{pl}\n```\n")

    io.open(os.path.join(VD, "thumb19real_FLOW.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(flow) + "\n")
    io.open(os.path.join(VD, "thumb19real_PLATE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(plate) + "\n")
    io.open(os.path.join(VD, "thumb19real_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(ten) + "\n")
    io.open(os.path.join(VD, "thumb19real_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md) + "\n")

    print("OK 3 prompt thumbnail")
    for key, p in zip(VARIANTS, flow):
        pos = p.find("TEXT, bake") / len(p) * 100
        star = "OK " if pos <= 15 else "🔴 "
        print(f"   {key}: {len(p)} ky · TEXT o {pos:.0f}% dau  {star}")
    print(f"   FLOW  : thumb19real_FLOW.txt   (3 dong, bake chu)")
    print(f"   PLATE : thumb19real_PLATE.txt  (3 dong, KHONG chu — duong lui)")
    print(f"   doc   : thumb19real_BLOCKS.md  | map: thumb19real_TENFILE.txt")
    for p in flow:
        assert p.find("TEXT, bake") / len(p) <= 0.15, "khoi TEXT phai o 15% dau"
        assert len(p) <= 2000, f"prompt qua dai: {len(p)}"
    for pl in plate:
        assert BANNER not in pl and HERO not in pl, "PLATE con chu"


if __name__ == "__main__":
    build()
