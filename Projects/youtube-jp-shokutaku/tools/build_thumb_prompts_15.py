# -*- coding: utf-8 -*-
r"""Xuat 4 file prompt thumbnail 3x3 cho video 15 (ab-3title-3thumb.md 3.1).

    python tools\build_thumb_prompts_15.py

Xuat vao 06_VIDEO/15_shoga-tabekata/:
  thumb_prompts_FLOW.txt      3 prompt bake san CHU, moi prompt 1 DONG -> bom extension
  thumb_prompts_BLOCKS.md     ban nguoi doc: khung khoi + bang so do + bang chu
  thumb_prompts_TENFILE.txt   thu tu dong FLOW <-> thumb_T1/T2/T3_*.png
  thumb_prompts_PLATE.txt     3 plate KHONG chu (duong lui khi nat kanji) - FILE RIENG

Buoc 1 — khuon lay tu ANH DA LEN SONG, khong lay tu tai lieu:
  07_UPLOADED/14_kabocha-tabekata/_upload/thumbnail.jpg
Buoc 2 — so do bang may (1920x1080):
  vien vang 21px = 2% khung | badge do goc tren-trai d = 18% be ngang
  HERO do: cao 19.0% khung NHUNG rong 51.1% be ngang (x 858-1839, y 418-623)
  khoi chu: cot phai, 58% be ngang
=> Hero thang bang BE NGANG, khong bang chieu cao. Ep co bang quan he voi MEP KHUNG,
   dung ta phan tram (media-library.md 2.10-f: model nghe VI TRI, khong nghe TI LE).
Buoc 3 — khoi TEXT phai nam trong 15% DAU prompt (gate chinh) + ~1500 ky (gate phu).
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "15_shoga-tabekata"

HEADER = ("YouTube thumbnail, Japanese senior-health cooking channel, photorealistic, "
          "bold Japanese text burned into the image. ")

# CHU: giong nhau ca 3 ban — bien thu la HINH (ab-3title-3thumb.md 3 muc 6)
TEXT = ("TEXT, exactly these three lines plus one badge, nothing else: "
        "line 1, cream-white with thick dark-brown outline: 生姜は後入れ / "
        "line 2, THE LARGEST AND WIDEST, bright red with thick cream outline: 夏に食が細る / "
        "line 3, golden-yellow with thick dark outline: 入れ方4つ / "
        "badge, solid red circle in the top-left corner, two white characters: 食卓. ")

LAYOUT = ("LAYOUT: a thin bright-yellow border frames the image, a finger thick. The three "
          "lines are stacked in the right half, each one unbroken row. Line 2 is the hero: "
          "it starts at the frame centre and reaches to within a thumb's width of the right "
          "edge, and is clearly taller than lines 1 and 3. The red badge sits in the "
          "top-left corner, about as wide as her head. ")

BG = ("BACKGROUND: a bright Japanese home kitchen in soft daylight, wooden counter, pale "
      "tiled wall, blurred, flat even light, no dark masses. ")

WOMAN = ("LEFT SIDE: a Japanese woman in her late sixties, short grey hair, beige apron over "
         "an indigo blouse, mouth open in shock, looking down at what she "
         "holds. Her head nearly touches the top edge; her body is cropped by the bottom "
         "edge. ")

FACE = ("LEFT SIDE: an extreme close-up of a Japanese woman in her late sixties, short grey "
        "hair, beige apron over an indigo blouse, framed shoulders-up so her face fills the "
        "left third, mouth open in shock, one hand raised to her cheek. Hair cropped by the "
        "top edge, shoulders by the bottom edge. No food in the frame. ")

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and legible, no broken "
           "or invented glyphs. Keep the very bottom-right corner free of text. No "
           "watermark, no logo, no additional text. --ar 16:9")

TOFU = ("BOTTOM-LEFT: she holds a white plate of chilled tofu heaped with freshly grated raw "
        "ginger, the plate large and cropped by the bottom edge. No characters written "
        "anywhere. ")
RICE = ("BOTTOM-LEFT: she holds a rice bowl with exactly half the rice left uneaten, "
        "chopsticks laid across the rim, the bowl large and cropped by the bottom edge. No "
        "characters written anywhere. ")

VARIANTS = [
    ("T1", "baseline khuon kenh (nguyen khuon video 14: ba cu + vat chu de duoi-trai)",
     WOMAN + TOFU),
    ("T2", "doi DUNG 1 bien hinh: vat trong tay = HAU QUA (bat com con nua) thay THU PHAM",
     WOMAN + RICE),
    ("T3", "doi LAYOUT: mat can tu vai len, bo han vat do an", FACE),
]

PLATES = [("T1", WOMAN + TOFU), ("T2", WOMAN + RICE), ("T3", FACE)]


def one_line(s):
    return " ".join(s.split())


def main():
    VD.mkdir(parents=True, exist_ok=True)
    flow, blocks, tenfile = [], [], []

    for tag, hypo, body in VARIANTS:
        p = one_line(HEADER + TEXT + LAYOUT + BG + body + QUALITY)
        flow.append(p)
        ti = p.find("TEXT, exactly")
        blocks.append(f"### {tag} — {hypo}\n\n"
                      f"- **{len(p)} ky** · khoi TEXT bat dau o **{ti * 100 // len(p)}%**\n\n"
                      f"```\n{p}\n```\n")
        tenfile.append(f"dong {len(flow)} -> thumb_{tag}_shoga.png   ({hypo})")

    plates = [one_line(HEADER.replace(", bold Japanese text burned into the image", "")
                       + LAYOUT.split("The three")[0] + BG + body
                       + "Absolutely NO text, no letters, no numbers, no characters anywhere. "
                         "No watermark, no logo. --ar 16:9")
              for _, body in PLATES]

    (VD / "thumb_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_TENFILE.txt").write_text("\n".join(tenfile) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_PLATE.txt").write_text("\n".join(plates) + "\n", encoding="utf-8")
    (VD / "thumb_prompts_BLOCKS.md").write_text(
        "# Video 15 — bo 3x3 thumbnail (prompt BAKE SAN CHU)\n\n"
        "> Khuon lay tu ANH DA LEN SONG `07_UPLOADED/14_kabocha-tabekata/_upload/thumbnail.jpg`.\n"
        "> So do bang may (1920x1080): vien vang 21px = 2% · badge do d = 18% be ngang ·\n"
        "> **HERO cao 19,0% NHUNG rong 51,1% be ngang** · khoi chu cot phai 58% ngang.\n"
        "> => hero thang bang BE NGANG. Prompt ep co bang quan he voi MEP KHUNG.\n\n"
        "## Chu — GIONG NHAU ca 3 ban (bien thu la HINH)\n\n"
        "| dong | chu | ky | vai | mau |\n|---|---|---|---|---|\n"
        "| 1 | `生姜は後入れ` | 6 | HANH VI (ve cai gi) | cream + vien nau |\n"
        "| 2 | `夏に食が細る` | 6 | HAU QUA — **to va rong nhat** | **DO** + vien cream |\n"
        "| 3 | `入れ方4つ` | 5 | DAP AN GIAU (phai lam gi) | vang + vien den |\n"
        "| badge | `食卓` | 2 | nhan dien kenh | trang tren tron DO |\n\n"
        + "\n".join(blocks)
        + "\n## PLATE (khong chu) — FILE RIENG `thumb_prompts_PLATE.txt`\n\n"
          "Duong lui khi kanji gen ra nat net: gen plate roi dot chu bang tool.\n"
          "Dung tron vao FLOW: extension bom ca file, plate ghi `No text` nen ra anh trang\n"
          "chu dung thiet ke -> tuong prompt chua sua (da dinh o chouhen 21).\n",
        encoding="utf-8")

    print("=== GATE (ab-3title-3thumb.md 3.1 Buoc 3) ===")
    ok = True
    for i, p in enumerate(flow):
        ti = p.find("TEXT, exactly") * 100 // len(p)
        g1, g2 = ti < 15, len(p) <= 1500
        ok &= g1 and g2
        print(f"  T{i+1}: {len(p):5d} ky {'OK ' if g2 else 'VUOT'} | TEXT @ {ti:2d}% "
              f"{'OK' if g1 else 'VUOT'}")
    print(f"\n  {'DAT CA HAI GATE' if ok else 'CON VUOT — siet cau chu, DUNG cat so do'}")
    for f in ("thumb_prompts_FLOW.txt", "thumb_prompts_BLOCKS.md",
              "thumb_prompts_TENFILE.txt", "thumb_prompts_PLATE.txt"):
        print(f"    -> {(VD / f).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
