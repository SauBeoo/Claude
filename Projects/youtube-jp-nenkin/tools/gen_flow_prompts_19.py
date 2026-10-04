# -*- coding: utf-8 -*-
r"""gen_flow_prompts_19.py — prompt HOAN CHINH (hinh + chuyen dong trong CUNG mot
prompt) cho Google Flow / Veo, video 19. User tu render, khong can anh dau vao.

VI SAO CO BO THU BA (user chot 2026-09-02: *"cho tao prompt hoan chinh de tao dung
google flow render ay khong can may render"*):

  art_prompts_photocard19*_FLOW.txt   -> chi HINH        (gen anh tinh)
  out/nenkin-19/motion.txt            -> chi CHUYEN DONG (doi anh dau vao i2v)
  flow_prompts_19_*.txt  ⭐ FILE NAY  -> HINH + CHUYEN DONG, tu du

⭐ BA CAI DUOC khi di duong text-to-video cua Flow, khong phai i2v tu 74 anh cu:
 ① **16:9 NGAY TU LUC GEN** => het chuyen crop 3:2 -> 16:9 mat 16% chieu cao.
    Day chinh la cai gia ③ cua `CLAUDE.md:178` ("anh phai gen rieng cho full-bleed"),
    bay gio duoc tra bang chinh buoc gen video, khong phai gen lai 74 anh roi moi i2v.
 ② **CHUA SAN BANNER TRONG** o dinh khung ~18% + chua day ~15% cho phu de. Lo anh
    khuon card khong co bang nao => dot banner len la che mat nhan vat.
 ③ Anh macro/tinh-vat-nho khong ganh duoc full-bleed (do duoc 2026-09-02: phai loai
    `tanjoubi_b` va `tanjoubi_d` khoi demo chuong 3) — prompt o day ep
    "subject FILLS the frame" ngay tu dau.

⚠️ VAN GIU dung huong user da chon: **KHONG bake chu vao video**. Prompt bat Flow
   de banner TRONG; chu Noto Sans JP dot len sau bang `make_fb19ch3.py::headline`
   (kanji AI nat net — `media-library.md` §2.9). Cai duy nhat doi la nen banner gio
   do Flow gen (co chuyen dong giay that) thay vi PIL ve.

⚠️ Veo GEN CA AUDIO => prompt phai ghi "no dialogue, no voice, no music", vi giong
   da co san (VOICEVOX 雀松朱司) va BGM co luat rieng (-40dB).

CHAY:  python tools/gen_flow_prompts_19.py
  -> 06_VIDEO/19_.../flow_prompts_19_FLOW.txt    74 dong, ca video
  -> 06_VIDEO/19_.../flow_prompts_19_CH3.txt      9 dong, CHUONG 3 de thu truoc
  -> 06_VIDEO/19_.../flow_prompts_19_BLOCKS.md   ban nguoi doc
  -> 06_VIDEO/19_.../flow_prompts_19_TENFILE.txt dong <-> ten clip
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")
BEATS = r"E:\vox-director\out\nenkin-19\beats.json"

# CHUONG 3 (八十四万円) = beat 12..15 cua beats.json — 9 shot.
# 📌 Loc theo BEAT, khong theo ten anh: demo `_fb19ch3/` phai loai `tanjoubi_b` va
#    `tanjoubi_d` vi **anh CU** (3:2, gen cho khuon card) crop ra khung trong —
#    khong phai vi canh do sai. Prompt o day co `MUST: FILLS the frame with one
#    clear LARGE subject` nen Flow gen moi se lap khung => ly do loai het hieu luc.
#    Va Flow khong co "crop", nen 9 canh RIENG tot hon 12 crop tu 7 anh (het lap hinh).
CH3_BEATS = {12, 13, 14, 15}

# 🔴 THU TU KHOI = GATE, khong phai tham my (`ab-3title-3thumb.md` §3.1 Buoc 3):
#    model bam khoi den TRUOC. Ban dau prompt dai 2.300 ky va de "no text anywhere"
#    + "nguoi Nhat cao tuoi" o CUOI => hai rang buoc quyet dinh nhat bi nuot.
#    Nay: STYLE ngan -> SCENE -> MOTION -> CAMERA -> BANNER+NOTEXT (khoi quyet dinh,
#    nam trong ~60% dau) -> con lai. Da rut 2.300 -> ~1.500 ky.
STYLE = (
    "Vintage newsprint editorial PAPER COLLAGE brought to life as stop-motion, "
    "mid-century JAPANESE front-page news feature. Hand-cut paper cut-outs with torn "
    "and scissor-cut edges, tape corners, soft paper drop shadows, heavy halftone "
    "dots and slight ink misregistration, on a bold flat {bg} paper ground with "
    "scattered paper accents (triangles, circles, zigzags, washi tape). Palette: "
    "cream, deep navy ink, deep red, mustard, charcoal. Every figure is a PRINTED "
    "illustrated cut-out with a thick white die-cut outline — NOT CGI, NOT 3D, NOT "
    "photoreal."
)

# ── khoi QUYET DINH: banner trong + no-text + nguoi Nhat. Dat NGAY sau CAMERA ──
#    (bit cai gia ③ cua CLAUDE.md:178 — anh khuon card khong co bang nao chua san)
KEY = (
    "MUST: the collage FILLS the frame with one clear LARGE subject. Across the top "
    "leave a torn-paper banner strip about one fifth of the height that is COMPLETELY "
    "BLANK — empty paper, nothing written, nothing important behind it. Keep the "
    "bottom fifth free of any important detail or face. Every paper surface, document "
    "and sign is BLANK: no text, letters, numbers, caption, signage, logo or "
    "watermark anywhere. Any person is JAPANESE and elderly (60s-70s) in modest "
    "everyday Japanese clothing — no Western or 1950s Americana styling."
)

GUARD = (
    "Stay flat 2D, camera parallel to the collage. One continuous move that does not "
    "loop or reset. Rigid paper — no morph, no melt. Calm restrained amplitude. No "
    "dialogue, no voice, no music, no sound effects. 16:9."
)

CAM = {
    "static": "CAMERA: locked off, completely static — no pan, no zoom, no shake.",
    "parallax": ("CAMERA: locked off, but the layered paper planes drift at slightly "
                 "different speeds for depth — no pan, no zoom of the camera itself."),
}
CAM_PEAK = ("CAMERA: locked off except a barely perceptible push-in of about three "
            "percent across the whole shot — no pan, no shake.")


def bg_phrase(bg):
    """`bg` cua beats.json -> cum mo ta nen giay."""
    return {
        "aged cream newsprint": "aged cream newsprint",
        "charcoal ink navy": "deep charcoal-navy ink",
        "deep red": "deep red",
        "mustard yellow": "mustard yellow",
    }.get(bg, bg)


def build():
    doc = json.load(io.open(BEATS, encoding="utf-8"))
    flow, ch3, ten, md = [], [], [], []
    md.append("# Flow prompts — video 19 `kounenrei-koyou-keizoku-kyufu`\n")
    md.append(
        "> **Prompt HOAN CHINH cho Google Flow / Veo** — hinh + chuyen dong trong cung\n"
        "> mot prompt, khong can anh dau vao. Moi dong `_FLOW.txt` = mot clip.\n>\n"
        "> ⚠️ **Chu van KHONG bake vao video.** Prompt bat Flow de mot dai banner giay xe\n"
        "> TRONG o dinh khung (~1/5 chieu cao); chu Noto Sans JP dot len sau bang\n"
        "> `tools/make_fb19ch3.py::headline` — kanji AI gen ra nat net.\n>\n"
        "> ⚠️ **Veo gen ca AUDIO** — prompt da ghi `no dialogue, no voice, no music`,\n"
        "> nhung nen tat audio trong Flow luon cho chac. Giong da co (VOICEVOX 雀松朱司).\n>\n"
        "> 📌 `flow_prompts_19_CH3.txt` = **9 shot cua chuong 3 (八十四万円)** = beat 12..15.\n"
        "> Thu 9 clip nay truoc khi dot ca 74. Demo tinh o `06_VIDEO/_fb19ch3/` la 12 shot\n"
        "> vi no CROP 12 lan tu 7 anh cu; Flow gen canh rieng nen 9 la du va het lap hinh.\n")
    n = 0
    for beat in doc["beats"]:
        md.append(f"\n## Beat {beat['id']} — {beat.get('title_cn','')} · "
                  f"{beat.get('title_en','')}\n")
        for shot in beat.get("shots", []):
            n += 1
            src = shot.get("src_card", "")
            cm = shot.get("camera_move", "static")
            cam = CAM_PEAK if "push-in" in cm else CAM.get(cm, CAM["static"])
            # `scene` trong beats.json da co JP_GUARD dinh duoi -> cat ra, vi GUARD
            # o day day du hon va dat o cuoi prompt
            scene = re.split(r"\s*Any person shown is JAPANESE", shot["scene"])[0].strip()
            p = " ".join([
                STYLE.format(bg=bg_phrase(beat.get("bg", "aged cream newsprint"))),
                f"SCENE: {scene}.",
                f"MOTION: {shot.get('element_motion','')}.",
                cam, KEY, GUARD,
            ])
            p = re.sub(r"\s+", " ", p).strip()
            flow.append(p)
            clip = f"flow_19_{src.replace('card_19_','')}.mp4"
            in3 = beat["id"] in CH3_BEATS
            ten.append(f"{clip:<34}<- dong {n} FLOW"
                       + ("   ⭐CH3" if in3 else ""))
            if in3:
                ch3.append(p)
            md.append(f"### `{clip}`  ← `{src}`  "
                      f"({shot.get('shot_size','')}, {shot.get('dur',6)}s)"
                      + ("  ⭐CH3" if in3 else "") + "\n")
            md.append(f"```\n{p}\n```\n*({len(p)} ky tu)*\n")

    for name, rows in [("flow_prompts_19_FLOW.txt", flow),
                       ("flow_prompts_19_CH3.txt", ch3),
                       ("flow_prompts_19_TENFILE.txt", ten)]:
        io.open(os.path.join(VD, name), "w", encoding="utf-8",
                newline="\n").write("\n".join(rows) + "\n")
    io.open(os.path.join(VD, "flow_prompts_19_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md) + "\n")
    ln = [len(x) for x in flow]
    print(f"OK {n} prompt hoan chinh | {min(ln)}-{max(ln)} ky (tb {sum(ln)//len(ln)})")
    print(f"   ca video : flow_prompts_19_FLOW.txt   ({len(flow)} dong)")
    print(f"   chuong 3 : flow_prompts_19_CH3.txt    ({len(ch3)} dong)")
    print(f"   -> {VD}")
    return n, len(ch3)


if __name__ == "__main__":
    a, b = build()
    assert a == 74, f"phai 74 prompt, dang co {a}"
