# -*- coding: utf-8 -*-
r"""gen_flow_ch3.py — DEMO 1 DOAN: chuong 3 video 19, TACH LAM 2 FILE.

User chot 2026-09-02: *"tach cho tao lam 2 file. 1 file prompt anh, 1 file prompt
video. Demo 1 doan cho tao thoi"*.

  flow_ch3_IMAGE.txt   9 prompt ANH   (text-to-image) -> gen 9 poster tinh
  flow_ch3_VIDEO.txt   9 prompt VIDEO (image-to-video) -> animate dung 9 anh do

⭐ VI SAO TACH LA DUNG (khong phai chi de tien): `E:\vox-director\README.md` —
   *"The look is born in the image step. All the collage DNA lives in that image —
   if the poster isn't a rich collage, nothing downstream saves it."* Gen anh sai
   thi re de gen lai; gen video sai la dot ca luot. Bo text-to-video 1 buoc
   (`flow_prompts_19_*.txt`) van giu, nhung duyet anh truoc thi kiem soat hon.

PHAM VI: CHUONG 3 (八十四万円) = beat 12..15 cua beats.json = 9 shot. Day la
   chuong PEAK cua bai va la chuong duy nhat co **0 KHUON MAT** => banner dot len
   dinh khung khong che mat ai (cai gia ③ cua `CLAUDE.md:178`).

⚠️ HAI THU PHAI CO O CA HAI FILE, dung bo khi sua:
   ① **banner TRONG o dinh khung ~1/5** — cho de dot chu Noto sau (kanji AI nat net).
      File VIDEO cung phai nhac, vi i2v hay tu ve chu vao dai trong.
   ② **no text anywhere** — moi mat giay/giay to phai blank.

CHAY:  python tools/gen_flow_ch3.py
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")
BEATS = r"E:\vox-director\out\nenkin-19\beats.json"
CH3 = {12, 13, 14, 15}

BG = {"aged cream newsprint": "aged cream newsprint",
      "charcoal ink navy": "deep charcoal-navy ink",
      "deep red": "deep red", "mustard yellow": "mustard yellow"}

# ══ FILE 1 — PROMPT ANH ═══════════════════════════════════════════════════
IMG_STYLE = (
    "Vintage newsprint editorial PAPER COLLAGE, mid-century JAPANESE front-page news "
    "feature: bold cut-out photographs and illustrations laid over an aged broadsheet "
    "page, heavy halftone print dots, aged newsprint texture, slight ink "
    "misregistration — reads like a newspaper feature spread, not an advertisement. "
    "Clearly layered hand-cut paper cut-outs with visible torn and scissor-cut edges, "
    "tape corners and soft real paper drop shadows, on a bold flat {bg} paper "
    "background, with scattered geometric paper accents (triangles, circles, zigzags, "
    "washi tape). Palette: cream white, deep navy ink, deep red, mustard yellow, "
    "charcoal black. Every figure is a PRINTED, illustrated cut-out with a thick white "
    "die-cut outline — NOT CGI, NOT a 3D render, NOT photoreal; keep print grain and "
    "paper imperfections. High-contrast, tactile, hand-assembled."
)
IMG_MUST = (
    "MUST: the collage FILLS the frame edge to edge, the main subject LARGE and "
    "cropped by the bottom edge of the frame. Across the top of the frame leave a "
    "torn-paper banner strip about one fifth of the height that is COMPLETELY BLANK — "
    "clean empty paper, nothing written on it, nothing important behind it. Keep the "
    "bottom fifth free of any important detail or face, and keep the very bottom-right "
    "corner clear. Every paper surface, document and sign in the image is BLANK and "
    "unprinted: no text, letters, numbers, headline, caption, signage, logo or "
    "watermark anywhere. Any person shown is JAPANESE and elderly (60s-70s) in modest "
    "everyday Japanese clothing — not Western, no 1950s Americana styling. "
    "Aspect ratio 16:9."
)

# ══ FILE 2 — PROMPT VIDEO (i2v: anh da co, chi noi CHUYEN DONG) ═══════════
VID_HEAD = ("Animate this still paper-collage poster as a stop-motion MOTION GRAPHIC — "
            "printed paper cut-outs, not photoreal.")
VID_TAIL = (
    "AESTHETIC: keep the torn-paper, tape, halftone, newsprint and paper-stencil "
    "textures and the bold flat background exactly as they are; grain and halftone "
    "dots may breathe subtly frame to frame. KEEP the blank torn-paper banner strip "
    "across the top EMPTY — do not draw any text, letters or numbers on it or anywhere "
    "else in the frame. CONSTRAINTS: stay flat 2D — no 3D rotation, no perspective "
    "change, camera parallel to the poster. ONE continuous move that does not loop, "
    "retract or reset. Rigid paper — no morph, no melt, no re-rendering of faces. "
    "Animate the motion only; don't re-render the picture. Calm, restrained amplitude. "
    "No dialogue, no voice, no music, no sound effects."
)
CAM = {"static": "CAMERA: locked off, completely static — no pan, no zoom, no shake.",
       "parallax": ("CAMERA: locked off, but the layered paper planes drift at slightly "
                    "different speeds for depth — the camera itself does not move.")}
CAM_PEAK = ("CAMERA: locked off except a barely perceptible push-in of about three "
            "percent across the whole shot — no pan, no shake.")


def build():
    doc = json.load(io.open(BEATS, encoding="utf-8"))
    img, vid, md = [], [], []
    md.append("# DEMO chuong 3 — video 19 · prompt ANH + prompt VIDEO\n")
    md.append(
        "> **Chuong 3 (八十四万円)** = beat 12..15 = **9 shot**. Chuong PEAK cua bai, va\n"
        "> la chuong duy nhat co **0 khuon mat** => banner dot len dinh khung khong che ai.\n>\n"
        "> **Quy trinh 2 buoc:**\n"
        "> 1. `flow_ch3_IMAGE.txt` -> gen 9 poster tinh -> **DUYET MAT** (banner co that\n"
        ">    trong? chu the co lap khung? co chu rac nao lot vao?)\n"
        "> 2. `flow_ch3_VIDEO.txt` -> nap dung anh so N + prompt dong N -> ra clip\n>\n"
        "> ⚠️ Ca hai file deu nhac **banner TRONG** va **no text anywhere** — file VIDEO\n"
        "> cung phai nhac, vi i2v rat hay tu ve chu vao mot dai giay trong.\n>\n"
        "> ⚠️ Chu Noto Sans JP dot len banner SAU, bang `tools/make_fb19ch3.py::headline`.\n"
        "> Headline tung beat ghi o bang duoi.\n")
    md.append("\n| # | clip | headline se dot len banner | nen |\n|---|---|---|---|")
    rows, n = [], 0
    for beat in doc["beats"]:
        if beat["id"] not in CH3:
            continue
        bg = BG.get(beat.get("bg", ""), beat.get("bg", ""))
        for k, shot in enumerate(beat.get("shots", [])):
            n += 1
            src = shot.get("src_card", "")
            name = src.replace("card_19_", "")
            # headline chi o shot DAU cua beat (luat showcase: 1 headline/beat)
            head = beat.get("title_cn", "") if k == 0 else "— (cut-in, khong headline)"
            rows.append(f"| {n} | `{name}` | {head} | {bg} |")
            scene = re.split(r"\s*Any person shown is JAPANESE", shot["scene"])[0].strip()
            img.append(re.sub(r"\s+", " ", " ".join(
                [IMG_STYLE.format(bg=bg), f"SCENE (as layered paper cut-outs): {scene}.",
                 IMG_MUST])).strip())
            cm = shot.get("camera_move", "static")
            vid.append(re.sub(r"\s+", " ", " ".join(
                [VID_HEAD, f"MOTION: {shot.get('element_motion','')}.",
                 CAM_PEAK if "push-in" in cm else CAM.get(cm, CAM["static"]),
                 VID_TAIL])).strip())
    md += rows
    md.append("\n---\n")
    for i, (a, b) in enumerate(zip(img, vid), 1):
        md.append(f"\n## {i}. `{rows[i-1].split('`')[1]}`\n")
        md.append(f"**ANH** *({len(a)} ky)*\n\n```\n{a}\n```\n")
        md.append(f"**VIDEO** *({len(b)} ky)*\n\n```\n{b}\n```\n")

    io.open(os.path.join(VD, "flow_ch3_IMAGE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(img) + "\n")
    io.open(os.path.join(VD, "flow_ch3_VIDEO.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(vid) + "\n")
    io.open(os.path.join(VD, "flow_ch3_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md) + "\n")
    print(f"OK {n} shot (chuong 3)")
    print(f"   ANH  : flow_ch3_IMAGE.txt  {min(map(len,img))}-{max(map(len,img))} ky")
    print(f"   VIDEO: flow_ch3_VIDEO.txt  {min(map(len,vid))}-{max(map(len,vid))} ky")
    print(f"   doc  : flow_ch3_BLOCKS.md")
    print(f"   -> {VD}")
    return n


if __name__ == "__main__":
    got = build()
    assert got == 9, f"chuong 3 phai 9 shot, dang co {got}"
