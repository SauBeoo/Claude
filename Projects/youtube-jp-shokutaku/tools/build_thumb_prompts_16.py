# -*- coding: utf-8 -*-
r"""Xuat 4 file prompt thumbnail 3x3 cho video 16 (ab-3title-3thumb.md 3.1).

    python tools\build_thumb_prompts_16.py

Xuat vao 06_VIDEO/16_banana-yoru-toire/:
  thumb_prompts_FLOW.txt      3 prompt bake san CHU, moi prompt 1 DONG -> bom extension
  thumb_prompts_BLOCKS.md     ban nguoi doc: khung khoi + bang so do + bang chu
  thumb_prompts_TENFILE.txt   thu tu dong FLOW <-> thumb_T1/T2/T3_*.png
  thumb_prompts_PLATE.txt     3 plate KHONG chu (duong lui khi nat kanji) - FILE RIENG

Buoc 1 - khuon lay tu ANH DA LEN SONG:
  07_UPLOADED/15_shoga-tabekata/_upload/thumbnail.png (1920x1080)
  !! Tai lieu 15_shoga-tabekata.md muc 8 ghi "cot chu ben TRAI" nhung ANH THAT la
     cot chu ben PHAI, ba cu ben trai, badge do goc tren-trai, dai vang mep TRAI.
     Chỏi nhau thi TIN ANH (ab-3title-3thumb.md 3.1 Buoc 1).

Buoc 2 - DAO layout cho video 16 (luat Muc 15C: dao so voi video lien truoc):
  cot chu TRAI | nguoi + vat PHAI | dai vang mep PHAI | badge goc tren-PHAI
  mau: HAU QUA do -> VANG, DAP AN GIAU vang -> DO
  Hero thang bang BE NGANG (audience-45plus.md 6.10): ep co bang quan he voi MEP KHUNG,
  KHONG ta phan tram (media-library.md 2.10 muc 6: model nghe VI TRI, khong nghe TI LE).

Buoc 3 - khoi TEXT phai nam trong 15% DAU prompt (gate chinh) + <=1500 ky (gate phu).
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "16_banana-yoru-toire"

HEADER = ("YouTube thumbnail, Japanese senior-health cooking channel, photorealistic, "
          "bold Japanese text burned into the image. ")

# CHU: giong nhau ca 3 ban - bien thu la HINH (ab-3title-3thumb.md 3 muc 6)
TEXT = ("TEXT, exactly these three lines plus one badge, nothing else: "
        "line 1, cream-white with thick dark-brown outline: そのバナナ / "
        "line 2, THE LARGEST AND WIDEST, golden-yellow with thick dark-brown outline: 夜中に3回 / "
        "line 3, bright red with thick cream outline: 正解は時間 / "
        "badge, solid red circle in the top-right corner, two white characters: 食卓. ")

LAYOUT = ("LAYOUT: a band of gold leaf runs down the right edge. The three lines are stacked "
          "in the left half, each an unbroken row. Line 2 is the hero: it starts within a "
          "thumb's width of the left edge and reaches past the frame centre, and is clearly "
          "taller than lines 1 and 3. The red badge sits in the top-right corner, as wide as "
          "her head. ")

BG = ("BACKGROUND: a Japanese home kitchen at night, warm lamp light, wooden counter, "
      "blurred, soft even light, no harsh shadows. ")

BG_BRIGHT = ("BACKGROUND: a Japanese dining room in late afternoon, sun through lace "
             "curtains, wooden table, blurred, flat light, no dark masses. ")

WOMAN = ("RIGHT SIDE: a Japanese woman in her late sixties, short grey hair, beige apron over "
         "an indigo blouse, eyebrows raised in dismay. Her head nearly touches the top edge, "
         "her body cropped by the bottom edge. ")

FACE = ("RIGHT SIDE: an extreme close-up of a Japanese woman in her late sixties, short grey "
        "hair, beige apron over an indigo blouse, framed shoulders-up so her face fills the "
        "right third, eyes wide in dismay, one hand raised to her cheek. Hair cropped by the "
        "top edge, shoulders by the bottom edge. No food in the frame. ")

PROP = ("BOTTOM-RIGHT: she holds a white plate with one ripe banana; beside it a round "
        "twin-bell alarm clock, hands at two o'clock, both cropped by the bottom edge. "
        "Nothing written on the clock face. ")

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, no broken "
           "glyphs. Keep the very bottom-right corner free of text. No watermark, no logo, "
           "no additional text. --ar 16:9")

VARIANTS = [
    ("T1", "baseline khuon kenh, DAO ben so voi video 15 (chu TRAI, nguoi+vat PHAI)",
     BG, WOMAN + PROP),
    ("T2", "doi DUNG 1 bien hinh: nen TOI -> nen SANG (chu, layout, bieu cam giu nguyen)",
     BG_BRIGHT, WOMAN + PROP),
    ("T3", "doi LAYOUT: mat can tu vai len, bo han vat (chuoi + dong ho)",
     BG, FACE),
]


def one_line(s):
    return " ".join(s.split())


def main():
    VD.mkdir(parents=True, exist_ok=True)
    flow, blocks, tenfile = [], [], []
    names = {"T1": "thumb_T1_banana_base.png",
             "T2": "thumb_T2_banana_bright.png",
             "T3": "thumb_T3_banana_face.png"}

    for tag, hypo, bg, body in VARIANTS:
        p = one_line(HEADER + TEXT + LAYOUT + bg + body + QUALITY)
        flow.append(p)
        ti = p.find("TEXT, exactly")
        blocks.append(f"### {tag} - {hypo}\n\n"
                      f"- **{len(p)} ky** - khoi TEXT bat dau o **{ti * 100 // len(p)}%**\n\n"
                      f"```\n{p}\n```\n")
        tenfile.append(f"dong {len(flow)} -> {names[tag]}   ({hypo})")

    plates = [one_line(
        HEADER.replace(", bold Japanese text burned into the image", "")
        + LAYOUT.split("The three lines")[0] + bg + body
        + "Absolutely NO text, no letters, no numbers, no characters anywhere. "
          "No watermark, no logo. --ar 16:9")
        for _, _, bg, body in VARIANTS]

    (VD / "thumb_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_TENFILE.txt").write_text("\n".join(tenfile) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_PLATE.txt").write_text("\n".join(plates) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_BLOCKS.md").write_text(
        "# Video 16 - bo 3x3 thumbnail (prompt BAKE SAN CHU)\n\n"
        "> Khuon lay tu ANH DA LEN SONG `07_UPLOADED/15_shoga-tabekata/_upload/thumbnail.png`.\n"
        "> !! Tai lieu cua video 15 ghi \"cot chu ben TRAI\" nhung anh that la cot chu ben\n"
        ">    PHAI. Chỏi nhau thi TIN ANH. => video 16 DAO lai: **chu TRAI, nguoi+vat PHAI**,\n"
        ">    dai vang mep PHAI, badge goc tren-PHAI.\n"
        "> Hero thang bang BE NGANG, khong bang chieu cao (audience-45plus.md 6.10).\n"
        "> Prompt ep co bang quan he voi MEP KHUNG, khong ta phan tram.\n\n"
        "## Chu - GIONG NHAU ca 3 ban (bien thu la HINH)\n\n"
        "| dong | chu | ky | vai | mau |\n|---|---|---|---|---|\n"
        "| 1 | `そのバナナ` | 5 | HANH VI (ve cai gi) | cream + vien nau |\n"
        "| 2 | `夜中に3回` | 5 | HAU QUA - **to va rong nhat** | **VANG** + vien nau |\n"
        "| 3 | `正解は時間` | 5 | DAP AN GIAU (phai lam gi) | **DO** + vien cream |\n"
        "| badge | `食卓` | 2 | nhan dien kenh | trang tren tron DO, goc tren-PHAI |\n\n"
        + "\n".join(blocks)
        + "\n## PLATE (khong chu) - FILE RIENG `thumb_prompts_PLATE.txt`\n\n"
          "Duong lui khi kanji gen ra nat net: gen plate roi dot chu bang tool.\n"
          "Dung tron vao FLOW: extension bom ca file, plate ghi `No text` nen ra anh trang\n"
          "chu dung thiet ke -> tuong prompt chua sua (da dinh o chouhen 21).\n\n"
          "## Sau khi gen\n\n"
          "1. XOA WATERMARK ca lo (`tools/strip_wm_thumb.py`) - thumbnail phai VA, khong cat\n"
          "   duoc vi chu hero chay sat mep. Soi 1:1 CA 4 GOC, khong doc sheet thu nho.\n"
          "2. Duyet 3 cap: full-size / 168px / 120px. Ban nao roi gate 168px -> gen lai.\n"
          "3. Doi ten dung `thumb_T1_* / T2_* / T3_*` de `upload_pack.py` goi du bo 3x3.\n",
        encoding="utf-8")

    print("=== GATE (ab-3title-3thumb.md 3.1 Buoc 3) ===")
    ok = True
    for i, p in enumerate(flow):
        ti = p.find("TEXT, exactly") * 100 // len(p)
        g1, g2 = ti < 15, len(p) <= 1500
        ok &= g1 and g2
        print(f"  T{i+1}: {len(p):5d} ky {'OK ' if g2 else 'VUOT'} | TEXT @ {ti:2d}% "
              f"{'OK' if g1 else 'VUOT'}")
    print(f"\n  {'DAT CA HAI GATE' if ok else 'CON VUOT - siet cau chu, DUNG cat so do'}")
    for f in ("thumb_prompts_FLOW.txt", "thumb_prompts_BLOCKS.md",
              "thumb_prompts_TENFILE.txt", "thumb_prompts_PLATE.txt"):
        print(f"    -> {(VD / f).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
