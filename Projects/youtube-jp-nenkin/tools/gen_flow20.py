# -*- coding: utf-8 -*-
r"""gen_flow20.py — bo prompt cho video 20 遺族年金・四分の三の誤解.

User chot 2026-09-03: *"Dung cho toi slides cho kich ban 20... viet prompt de
toi gen anh va dua vao kich ban de viet prompt render video cho tung anh.
Chu y no phai khop voi text nhe"*.

⭐ STYLE: **NGUOI THAT / photoreal** (mac dinh) — user chot lai
   2026-09-03 sau khi thu ban anime: *"the cu de nguoi that di"*.
   Ban anime van chay duoc: `python tools/gen_flow20.py --style anime`
   (xuat ra `flow20anime_*`, khong de len ban that).
   🔴 Doi style KHONG chi la doi mot cau STYLE: 25/83 shot cua ban anime
   la SIEU THUC va phai dung lai canh bang VAT THAT — xem
   `tools/_scenes20_real.py`.

⭐⭐ XUAT (ban `real`, 2026-09-03 vong 4 — user: *"gop thanh 1 file prompt
   thoi, text chuyen thanh video cho tao do phai tao ra 2 prompt"*):
  flow20_T2V.txt      83 prompt TEXT->VIDEO, MOT prompt / MOT shot (8s), 1 dong/prompt
  flow20_BLOCKS.md    ban NGUOI DOC: tung scene, LOI DOC tieng Nhat that + prompt
  flow20_TENFILE.txt  dong N <-> ten clip <-> giay <-> loi doc
  (ban anime `--style anime` van xuat 2 buoc IMAGE + VIDEO nhu cu)

═══ THU TU TRONG MOT PROMPT T2V ═══
  CANH (co nguoi o tu the bat dau) -> VIEC nguoi do lam tron 8 giay -> may quay
  -> chat anh -> khoa nhan vat / vat -> bo cuc -> nhip. Canh + viec dung DAU vi
  model bam khoi dau; style/khoa la phan phu. Noi dung viec: `_scenes20_human.py`.

═══ BON TANG LIEN MACH (thu duy nhat lam 83 shot thanh MOT video) ═══
 (1) CAST LOCK — 7 nhan vat lap lai. Gen 83 prompt doc lap => 83 ba cu KHAC
     NHAU. Nang nhat la callback L27 「冒頭で…目を疑った女性。あれが、佐藤さんです」:
     nguoi o day PHAI dung la nguoi o L1/L2, khong thi callback mat nghia.
     Shot DAU TIEN cua moi nhan vat duoc danh dau **MASTER REFERENCE** — gen
     shot do truoc, roi dua chinh no lam anh tham chieu cho cac shot sau.
 (2) PROP LOCK — 16 vat/boi canh lap lai (thong bao, phong bi, bep, nha 2
     tang, ban tho, quay 年金事務所...). Cung mot vat o 5 shot phai cung hinh.
 (3) MOTION CHAIN — shot mo scene ghi OPEN, giua ghi mid, cuoi ghi CLOSE, de
     cat sang scene sau khong giat.
 (4) NANG LUONG peak / mid / calm — motion viet theo NGHIA cua dung cau loi
     tai dung giay do (`_scenes20.py`), khong phai "calm restrained" cho tat ca.

═══ ⭐ STYLE: ANIME (khac video 17/18/19) ═══
 · `youtube-compliance.md` §2.1 chi bat tick altered/synthetic voi canh AI
   **REALISTIC**. Anime khong realistic => **KHONG phai tick**. Loi mien phi.
 · Anime giu CAST LOCK tot hon photoreal nhieu (mat ve co dinh, khong bi
   "uncanny drift" nhu mat nguoi that).
 · ⛔ Nhung i2v tren anime co benh RIENG, prompt VIDEO phai chan:
   - **ve lai mat** giua chung (mat anime bien dang rat de thay);
   - **nhep mieng** — day la video co GIONG DAN rieng, nhan vat KHONG noi;
   - **troi ve 3D / CGI muot** — mat chat anime;
   - **doi net ve va bang mau** giua clip.

═══ 🔴 GIAY TO: CO CHU NHUNG KHONG DOC DUOC ═══
Kanji AI gen la nat net (`media-library.md` §2.9) va bai nay day giay to lam
chu the. Anime giai chuyen nay DE HON photoreal: trong anime, giay to ve bang
"dong ke + net nguech ngoac" la quy uoc BINH THUONG, khong doc ra "gia" nhu
anh that. => moi prompt bat: giay co dong ke/o/con dau, nhung chu la net
nguech ngoac, KHONG ky tu nao doc duoc.
ⓘ Khoi 原典 KHONG dinh luat nay — no la screenshot THAT, phai doc duoc.

═══ 🔴 BAI HOC I2V DO DUOC O VIDEO 19 (dung lap lai) ═══
 · Chi **4–5s DAU** cua clip 8s la dung duoc — nua sau AI het da, chi tiet tut
   trung binh 15,1%. => prompt VIDEO ep **don het chuyen dong vao 4 giay dau**.
 · ⛔ KHONG ep `speed > 1` luc dung — no day nguoi xem toi phan loang nhanh hon.
   Tha cat duoi.
 · Mo/dong shot bang mot khung TINH de con dissolve 0,6–0,8s vao/ra cho sach.

CHAY:  python tools/gen_flow20.py
"""
import collections
import io
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from _scenes20 import CAST, HANDS, PROP, SCENES  # noqa: E402
from _policy20 import GOOGLE_BLOCK, GOOGLE_SWAP  # noqa: E402
from _scenes20_human import HUMAN  # noqa: E402
from _scenes20_real import (CAST_OVERRIDE, DOC_FOCUS,  # noqa: E402
                            POLICY_SWAP, PROP_OVERRIDE, SHOT_OVERRIDE,
                            SHOT_OVERRIDE_MINORS)

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "20_izoku-nenkin-yonbunno-san"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
TL = os.path.join(VD, "timeline.json")

# Bat TU LAP LIEN NHAU ("dark-wood dark-wood") — sinh ra khi hai phep
# doi chu chong len nhau. Dat thanh BIEN o day, khong viet regex inline:
# 3 lan trong phien 2026-09-03 regex bi hong vi escape (\b -> backspace)
# va gate van bao XANH. Bien thi kiem duoc bang mot dong test.
DUP_RE = re.compile(r"\b([a-z][\w-]{2,})\s+\1\b", re.I)
assert DUP_RE.search("the dark-wood dark-wood shelf"), "DUP_RE hong"

# ══════════════════════════════════════════════════════════════════════════
# ⭐ STYLE = "real" (MAC DINH, user chot 2026-09-03: *"the cu de nguoi that di"*)
# Ban "anime" giu lai o duoi, goi bang `--style anime`.
# ══════════════════════════════════════════════════════════════════════════
# 🔴 RUT GON vong 2 (2026-09-03) — xem `tools/_policy20.py`:
#    ① bo loc Google doc TU KHOA, khong doc PHU DINH => cam viet "not a real
#       person", "no watermark"... vi no NHAC den chinh dieu cam.
#    ② mat do "MUST / NEVER / obey these first" cung la tin hieu => ta canh
#       thuan tuy, ngan gon. 3.900 ky -> ~1.500 ky.
R_IMG_STYLE = (
    "Photorealistic documentary photograph, 50mm lens at f/2.8, natural window "
    "light, muted warm colour grade, gentle film grain, shallow depth of field "
    "with a softly blurred background. Contemporary Japan, an ordinary "
    "middle-class setting that looks genuinely lived in — worn edges, honest "
    "textures, a little everyday clutter. Calm, respectful and unposed, like a "
    "frame from a quiet documentary."
)
R_IMG_JP = (
    "Everyone shown is Japanese, of the age described, in modest everyday "
    "Japanese clothing. Older faces carry their real age — lines, real skin "
    "texture, thinning or white hair."
)
R_IMG_FRAME = (
    "Composition: one clear subject, large in frame. Keep the top fifth of the "
    "frame simple and open — plain wall, window or sky — and keep the bottom "
    "fifth clear of faces. Printing on paper is fine, small and softly out of "
    "focus so the wording stays indistinct; keep lettering out of the picture "
    "otherwise. Horizontal 16:9."
)
R_IMG_TAIL = "Quiet, natural, unstaged."
R_IMG_DOC = (
    "The sheet is the subject of this shot, so give it fine printed rule lines, "
    "column dividers and boxes, with one row of crisp numerals; put a red pen "
    "circle or a pencil tick exactly where the hand points, so the gesture "
    "lands on something."
)
# 🔴 Vong 3 (user, 2026-09-03): *"toi muon no nhu hoat dong binh thuong cua con
#    nguoi"* — prompt video la MOT NGUOI LAM MOT VIEC tron 8 giay, viet nhu dong
#    kich ban quay tai lieu. Bo `PERFORMANCE:`/`CONTINUITY:`/"first four
#    seconds" — nguoi that khong dien theo nhan. Noi dung: `_scenes20_human.py`.
R_VID_HEAD = (
    "An eight-second live-action documentary shot that continues from this "
    "photograph, with the same people, the same room and the same light."
)
R_VID_DOC = (
    "The pen mark and the numerals stay crisp and stay where they are; the "
    "wording around them stays soft."
)
R_VID_TAIL = (
    "People move at the unhurried pace of real life, the way they actually "
    "handle paper, cups and small objects at home — nothing rushed, "
    "nothing theatrical, and the action reaches its natural end within the "
    "eight seconds and rests there. The photographic look stays the same "
    "throughout: same grade, grain, lighting and depth of field, background "
    "softly out of focus, printing on paper as indistinct as in the still. "
    "Faces and clothes stay the same; hands and objects behave with real "
    "weight. Nobody talks. The shot begins and ends on a steady frame. Silent."
)
R_CAM = {
    # viet nhu loi nguoi quay noi voi nhau, khong phai danh sach cam
    "static":   "The camera sits still on a tripod for the whole shot.",
    "parallax": ("The camera is handheld but held very still, so the frame "
                 "breathes only slightly."),
    "push":     ("The camera creeps in a little on a dolly over the eight "
                 "seconds and comes to rest."),
    "push_hard": ("The camera moves in a clear, steady dolly push toward the "
                  "subject and stops as the action lands."),
    "pull_out": ("The camera draws slowly back on a dolly, gradually taking in "
                 "more of the room, and comes to rest."),
}

# ══════════════════════════════════════════════════════════════════════════
# ⭐⭐ MOT PROMPT / MOT SHOT — TEXT-TO-VIDEO (user chot 2026-09-03: *"gop thanh
#    1 file prompt thoi, text chuyen thanh video cho tao do phai tao ra 2
#    prompt"*). Ban `real` xuat DUY NHAT `flow20_T2V.txt`.
#    Thu tu trong prompt: CANH (co nguoi o tu the bat dau) -> VIEC nguoi do lam
#    -> may quay -> chat anh -> khoa nhan vat/vat -> bo cuc -> nhip. Canh va
#    viec dung DAU vi model bam khoi dau; style/khoa la phan phu.
# ══════════════════════════════════════════════════════════════════════════
T2V_STYLE = (
    "Photorealistic live-action footage shot on a cine camera with a 50mm lens "
    "at f/2.8, natural window light, muted warm colour grade, gentle film "
    "grain, shallow depth of field with a softly blurred background. "
    "Contemporary Japan, an ordinary middle-class setting that looks genuinely "
    "lived in — worn edges, honest textures, a little everyday clutter. Calm, "
    "respectful and unposed, like a quiet documentary."
)
T2V_FRAME = (
    "Composition: one clear subject, large in frame. Keep the top fifth of the "
    "frame simple and open — plain wall, window or sky — and the bottom fifth "
    "clear of faces. Any printing on paper is small and softly out of focus so "
    "the wording stays indistinct; keep lettering out of the picture "
    "otherwise. Horizontal 16:9, eight seconds."
)
T2V_DOC = R_IMG_DOC + " The pen mark and the numerals stay crisp throughout."
T2V_TAIL = (
    "People move at the unhurried pace of real life, the way they actually "
    "handle paper, cups and small objects at home — nothing rushed, nothing "
    "theatrical — and the action reaches its natural end within the eight "
    "seconds and rests there. Faces and clothes stay consistent throughout; "
    "hands and objects have real weight. Nobody talks. The shot begins and "
    "ends on a steady frame. Silent."
)

# ══ FILE 1 — PROMPT ANH (anime, text-to-image) ═════════════════════════════
IMG_STYLE = (
    "Japanese anime illustration in a warm slice-of-life TV-anime style — the look "
    "of a quiet contemporary drama anime, not fantasy and not moe. Clean confident "
    "lineart with a soft dark-brown ink line, flat cel shading with gentle "
    "watercolour-like gradients, a muted warm palette of cream, soft ochre, dusty "
    "blue and warm grey, soft rim light, a faint paper grain over the whole image. "
    "Backgrounds are painted in the careful detailed style of a Japanese anime "
    "background artist — real ordinary Japanese interiors, honestly observed and "
    "lived in. Calm, respectful, unhurried, wholesome. "
    "NOT photorealistic, NOT 3D, NOT CGI, NOT a photograph, NOT chibi, NOT manga "
    "screentone, no heavy black outlines, no neon colours."
)
IMG_JP = (
    "Everyone in frame is JAPANESE, drawn with realistic adult anime proportions "
    "and honest age — not stylised youthfulness. Elderly characters have real "
    "wrinkles, softened jawlines and thinning or white hair. Clothing is modest "
    "everyday contemporary Japanese wear, never Western or American styling."
)
IMG_FRAME = (
    "FRAME RULES (obey these before anything else): one clear subject, LARGE in "
    "frame. Keep the TOP fifth of the frame visually SIMPLE and uncluttered — plain "
    "wall, sky, ceiling or open space — with nothing important in it, because a "
    "caption will be burned in there later. Keep the BOTTOM fifth free of faces and "
    "of anything important, and keep the very bottom-right corner clear. "
    "PAPERWORK RULE: documents, forms, notices, calendars and leaflets DO carry "
    "printed matter — faint ruled rows, boxes, column dividers, a pale stamp — but "
    "every character on them is an unreadable squiggle of ink; NO kanji, kana, "
    "digit or letter anywhere is legible. Do not draw a sheet of pure blank white "
    "paper either. No headline, no signage, no logo, no brand mark, no watermark, "
    "no subtitle, no caption. Aspect ratio 16:9, horizontal."
)
IMG_TAIL = (
    "Reminder: printed matter is present but every character is an unreadable "
    "squiggle; nothing anywhere in the image is legible text. The top fifth stays "
    "visually simple. Anime illustration, not a photograph."
)

# ══ FILE 2 — PROMPT VIDEO (i2v tren anh anime) ═════════════════════════════
VID_HEAD = (
    "Animate this anime illustration into a short hand-drawn anime shot. Keep it "
    "2D anime: the exact same lineart, the exact same flat cel shading and the "
    "exact same palette as the still. Do NOT convert it to 3D, CGI, photoreal or "
    "any other style, and do not re-render or repaint anything."
)
VID_TAIL = (
    "AESTHETIC LOCK: the drawing style, line weight, colours, lighting and paper "
    "grain stay identical to the still frame for the whole clip. Printed matter on "
    "documents stays exactly as unreadable as it is in the still — it must NOT "
    "sharpen into legible characters as the camera moves, and no new text, number "
    "or logo appears anywhere. The top fifth stays visually simple. "
    "CHARACTER LOCK: faces are NOT redrawn — the same face, same age, same hair, "
    "same eye shape throughout; hands keep five fingers; nobody grows or shrinks. "
    "⛔ NOBODY SPEAKS: mouths stay closed or move only in a tiny natural breath — "
    "no talking, no lip-sync, no mouth flapping. This video is narrated by a "
    "separate voice. "
    "PHYSICS: objects do not appear, vanish, melt, morph or pass through each "
    "other; nothing floats that should not float. ONE continuous action that does "
    "not loop or reset. "
    "⭐ PUT ALL THE MOVEMENT IN THE FIRST FOUR SECONDS and let the rest simply "
    "settle and hold — do not invent extra action to fill the time. "
    "⭐ MOTION QUALITY: smooth and cinematic anime movement. Every move eases in "
    "and eases out and never starts or stops abruptly; the camera glides with no "
    "jitter, no stutter, no snapping, no frame-to-frame flicker or boiling lines. "
    "People move at a natural unhurried pace with real follow-through. "
    "⭐ Begin and end on a COMPOSED, STEADY frame so the clip can be dissolved "
    "into and out of cleanly. "
    "No dialogue, no voice, no music, no sound effects, no on-screen text."
)
CAM = {
    "static":   "CAMERA: locked off — no pan, no zoom, no shake.",
    "parallax": ("CAMERA: locked off, but the painted background layers drift a "
                 "hair against each other for depth — no pan, no zoom."),
    "push":     ("CAMERA: a slow steady push-in of about five percent, easing to a "
                 "stop at the end."),
    "push_hard": ("CAMERA: a decisive push-in of about ten percent that arrives "
                  "exactly on the beat and stops — no shake."),
    "pull_out": ("CAMERA: a slow steady pull-back that gradually reveals more of "
                 "the scene — no pan, no shake."),
}
AMP = {
    "peak": ("PERFORMANCE: this is the payoff beat — the action must be decisive "
             "and unmistakable at a glance, with real weight and follow-through."),
    "mid":  ("PERFORMANCE: clear purposeful movement — the subject genuinely does "
             "something; nothing may read as a frozen still."),
    "calm": ("PERFORMANCE: quiet and restrained — this is a resting beat, let it "
             "breathe."),
}
V_OPEN = ("CONTINUITY: this shot OPENS a section — start from exactly the pose in "
          "the still, do not re-stage it.")
V_MID = ("CONTINUITY: this shot CONTINUES the previous one in the same place — "
         "carry the same direction of movement onward, never reverse it.")
V_CLOSE = ("CONTINUITY: this shot CLOSES the section — the action comes to a "
           "natural rest and holds, so the cut to the next section does not jump.")


def _tl():
    d = json.load(io.open(TL, encoding="utf-8"))
    return d["lines"]


def merged_cast(style):
    """CAST cua ban anime; ban `real` bo hai dua tre khoi mo ta K1 (nhom A)."""
    d = {k: dict(v) for k, v in CAST.items()}
    if style == "real":
        d.update(CAST_OVERRIDE)
    return d


def policy_clean(text, tally):
    """Lop cuoi: doi CHU, giu NGHIA. Tra ve text da sach + ghi so lan doi."""
    # GOOGLE_SWAP chay SAU POLICY_SWAP: no don not cac tu con sot + go
    # chinh may cau "phu dinh" ma vong 1 nhet vao (xem `_policy20.py` muc ①).
    for pat, sub in list(POLICY_SWAP) + list(GOOGLE_SWAP):
        new, k = re.subn(pat, sub, text)
        if k:
            tally[pat] += k
            text = new
    return re.sub(r"\s{2,}", " ", text)


def merged_prop(style):
    """PROP cua ban anime, ban `real` ghi de + them vat that (mo hinh, standee...)."""
    d = dict(PROP)
    if style == "real":
        d.update(PROP_OVERRIDE)
    return d


def apply_override(shot, style):
    """Ban `real`: 25 shot sieu thuc duoc dung lai canh bang VAT THAT."""
    if style != "real":
        return shot
    out = dict(shot)
    # SHOT_OVERRIDE_MINORS ap SAU => no thang, vi day la rang buoc chinh sach
    # chu khong phai lua chon tham my.
    # HUMAN ap CUOI: no viet lai `mo` (va `sc` khi phai them nguoi vao khung)
    # thanh MOT NGUOI LAM MOT VIEC tron 8 giay — xem `_scenes20_human.py`.
    for src in (SHOT_OVERRIDE, SHOT_OVERRIDE_MINORS, HUMAN):
        if shot["key"] in src:
            out.update(src[shot["key"]])
    return out


def locks(shot, first_of, PROP, CAST):
    """CAST LOCK + PROP LOCK cho mot shot."""
    bits = []
    cid = shot.get("cast")
    hid = shot.get("hands")
    if cid:
        if first_of.get(cid) == shot["key"]:
            bits.append(
                f"CHARACTER {cid} — a RECURRING FICTIONAL CHARACTER invented for "
                f"this series, not a real or identifiable person. This shot "
                f"establishes the character, so keep the description below "
                f"unchanged in every later shot: {CAST[cid]['lock']}")
        else:
            bits.append(
                f"CHARACTER {cid} — the same RECURRING FICTIONAL CHARACTER as "
                f"before, not a real or identifiable person; keep the same age, "
                f"hair, build and clothing so the series stays consistent: "
                f"{CAST[cid]['lock']}")
    if hid:
        bits.append(f"The hands belong to RECURRING FICTIONAL CHARACTER {hid}: "
                    f"{HANDS[hid]}")
    props = shot.get("props", [])
    if props:
        # gop het vao MOT cau: "PROP LOCK — A, and B, and C."
        # (ban cu noi bang dau cham roi "and ..." => cau cut dau, doc nhu loi go)
        parts = [PROP[props[0]]] + [re.sub(r"^the SAME [^:]+: ", "", PROP[q])
                                    for q in props[1:]]
        bits.append("PROP LOCK — " + ", and ".join(parts))
    return " ".join(b if b.endswith(".") else b + "." for b in bits)


def main():
    style = "anime" if "--style" in sys.argv and "anime" in sys.argv else "real"
    PROPS = merged_prop(style)
    CASTS = merged_cast(style)
    tally = collections.Counter()
    if style == "real":
        S_STYLE, S_JP, S_FRAME, S_TAIL = (R_IMG_STYLE, R_IMG_JP, R_IMG_FRAME,
                                          R_IMG_TAIL)
        S_VHEAD, S_VTAIL, S_CAM = R_VID_HEAD, R_VID_TAIL, R_CAM
        pre = "flow20"
    else:
        S_STYLE, S_JP, S_FRAME, S_TAIL = IMG_STYLE, IMG_JP, IMG_FRAME, IMG_TAIL
        S_VHEAD, S_VTAIL, S_CAM = VID_HEAD, VID_TAIL, CAM
        pre = "flow20anime"

    lines = _tl()
    dur = lines[-1]["end"]
    os.makedirs(VD, exist_ok=True)

    # ── shot dau tien cua moi nhan vat = MASTER REFERENCE ──────────────────
    # 🔴 Tinh SAU khi ap override — lop HUMAN them nguoi vao shot som hon (todoku
    #    co W1 truoc hiraku); tinh tren SCENES goc thi "shot lap khuon" bi gan
    #    nham vao shot thu hai, con shot dau lai ghi "same as before".
    first_of, seen = {}, set()
    for s in SCENES:
        for sh0 in s.get("shots", []):
            sh = apply_override(sh0, style)
            c = sh.get("cast")
            if c and c not in seen:
                seen.add(c)
                first_of[c] = sh["key"]

    img_lines, vid_lines, ten_rows, blocks = [], [], [], []
    t2v_lines = []                     # ban real: MOT prompt / shot
    n = 0
    n_shot_total = sum(len(s["shots"]) for s in SCENES if s["kind"] == "art")

    blocks.append(
        f"# {pre} — video 20 遺族年金・四分の三の誤解 · STYLE: "
        f"{'NGUOI THAT (photoreal)' if style == 'real' else 'ANIME'}\n\n"
        f"- kich ban: `03_SCRIPTS/{STEM}_TTS.md` · **110 dong · {dur:.1f}s "
        f"({dur/60:.2f} phut)**\n"
        f"- **{len(SCENES)} scene** ({len(SCENES)/(dur/60):.2f} scene/phut) · "
        f"**{n_shot_total} anh AI** + **5 screenshot 原典**\n"
        f"- Thu tu duoi day = **thu tu THOI GIAN trong video**. Gen theo dung thu "
        f"tu nay thi lien mach doc ra duoc.\n"
        + (f"- ⚠️ Canh AI **realistic** => **PHAI TICK 'altered/synthetic "
           f"content'** luc upload (`youtube-compliance.md` §2.1).\n"
           f"- {len(SHOT_OVERRIDE)} shot da duoc **dung lai canh bang VAT THAT** "
           f"(mo hinh nha go · standee bia · bang trang · cau thang be tong) — "
           f"xem `tools/_scenes20_real.py`.\n"
           f"- {len(DOC_FOCUS)} shot **DOC_FOCUS**: giay to phai co CHU SO doc "
           f"duoc + dau danh dau o dung cho tay chi vao.\n"
           if style == "real" else
           "- ⚖️ Anime => **KHONG phai tick altered/synthetic** luc upload.\n"))

    # bang CAST / PROP
    blocks.append("\n## CAST LOCK — gen shot MASTER truoc, roi dung lam anh tham chieu\n")
    blocks.append("| id | vai | shot MASTER |\n|---|---|---|")
    for cid, c in CAST.items():
        blocks.append(f"| **{cid}** | {c['who']} | `{first_of.get(cid, '—')}` |")
    blocks.append("\n## PROP LOCK\n")
    blocks.append("| id | phai giong nhau o moi shot |\n|---|---|")
    for pid, t in PROP.items():
        blocks.append(f"| **{pid}** | {t[:150]}… |")
    blocks.append("")

    for si, s in enumerate(SCENES):
        a = lines[s["L"]]["start"]
        b = lines[SCENES[si + 1]["L"]]["start"] if si + 1 < len(SCENES) else dur
        span = b - a
        L0 = s["L"]
        L1 = SCENES[si + 1]["L"] if si + 1 < len(SCENES) else len(lines)
        jp = "  \n".join(f"`L{i}` {lines[i]['text']}" for i in range(L0, L1))

        # 🔴 mm:ss phai dung // (chia lay nguyen). `{a/60:.0f}` LAM TRON:
        #    119,2s ra "2:59.2" thay vi "1:59.2" — sai ca phut lan cam giac thu tu.
        head = (f"\n---\n\n## SCENE {si:02d} · {int(a)//60}:{a % 60:04.1f}–"
                f"{int(b)//60}:{b % 60:04.1f} ({span:.1f}s) · {s['tag']} · "
                f"`{s['kind']}`\n\n**LOI DOC:**  \n{jp}\n")
        blocks.append(head)

        if s["kind"] == "stat":
            blocks.append("\n**BANG SO** (khong co anh hero — vung giua cho duoc "
                          "mot thu):\n")
            for lab, val in s["stat"]:
                mark = " ⭐NHAN" if lab.startswith("*") else ""
                blocks.append(f"- `{lab.lstrip('*')}` → **{val}**{mark}")
            blocks.append("")
            continue
        if s["kind"] == "formula":
            blocks.append(f"\n**CONG THUC** (khong co anh hero): "
                          f"**`{s['formula']}`**"
                          f"{'  ⭐PEAK' if s.get('peak') else ''}\n")
            continue
        if s["kind"] == "genten":
            g = s["genten"]
            blocks.append(
                f"\n**原典 — SCREENSHOT THAT, ⛔ KHONG GEN AI** ({g['shots']} shot):\n"
                f"- URL (da verify 2026-09-03): {g['url']}\n"
                f"- cau phai thay: 「{g['quote']}」\n"
                f"- danh dau: {g['mark']}\n"
                f"- chup man hinh trang THAT, khoanh do dung cau tren, cat 16:9. "
                f"Khoi nay **PHAI doc duoc** — no la bang chung, KHONG duoc gen AI "
                f"va KHONG duoc lam mo chu.\n")
            continue

        # ── art ────────────────────────────────────────────────────────────
        k = len(s["shots"])
        for j, sh0 in enumerate(s["shots"]):
            sh = apply_override(sh0, style)
            n += 1
            t0 = a + span * j / k
            t1 = a + span * (j + 1) / k
            chain = V_OPEN if j == 0 else (V_CLOSE if j == k - 1 else V_MID)
            if k == 1:
                chain = V_OPEN + " " + V_CLOSE
            lk = locks(sh, first_of, PROPS, CASTS)
            # DOC_FOCUS chi co o ban `real` — o anime, giay to ve net nguech
            # ngoac la quy uoc binh thuong nen khong can khoi nay.
            doc_i = (" " + R_IMG_DOC) if (style == "real"
                                          and sh["key"] in DOC_FOCUS) else ""
            doc_v = (" " + R_VID_DOC) if (style == "real"
                                          and sh["key"] in DOC_FOCUS) else ""

            ip = (f"{sh['sc']}. {lk} {S_JP} {S_STYLE} {S_FRAME}{doc_i} {S_TAIL}")
            if style == "real":
                # mot doan van: dieu nguoi do lam -> may quay -> chat anh.
                # Khong nhan, khong "PERFORMANCE", khong "CONTINUITY".
                vp = f"{S_VHEAD} {sh['mo']} {S_CAM[sh['cam']]}{doc_v} {S_VTAIL}"
            else:
                vp = (f"{S_VHEAD} ACTION — {sh['mo']}. {S_CAM[sh['cam']]} "
                      f"{AMP[sh['lv']]} {chain}{doc_v} {S_VTAIL}")
            ip = re.sub(r"\s+", " ", ip).strip()
            vp = re.sub(r"\s+", " ", vp).strip()
            if style == "real":                       # lop chong chinh sach
                ip = policy_clean(ip, tally)
                vp = policy_clean(vp, tally)

            img_lines.append(ip)
            vid_lines.append(vp)
            fn = f"a20_{sh['key']}"
            master = (f" · ⭐KHUON {sh['cast']}"
                      if sh.get('cast') and first_of.get(sh['cast']) == sh['key']
                      else "")
            if style == "real":
                doc_t = (" " + T2V_DOC) if sh["key"] in DOC_FOCUS else ""
                tp = (f"{sh['sc']}. {sh['mo']} {S_CAM[sh['cam']]} {T2V_STYLE} "
                      f"{lk} {T2V_FRAME}{doc_t} {T2V_TAIL}")
                tp = policy_clean(re.sub(r"\s+", " ", tp).strip(), tally)
                t2v_lines.append(tp)
                ten_rows.append(
                    f"{n:03d}\t{fn}.mp4\t{t0:7.1f}-{t1:7.1f}s\t"
                    f"S{si:02d} {s['tag']}\t{lines[min(L0 + j, L1 - 1)]['text'][:38]}")
                blocks.append(
                    f"\n### {n:03d} · `{fn}.mp4` · {t0:.1f}–{t1:.1f}s "
                    f"({t1-t0:.1f}s) · cam `{sh['cam']}`{master}"
                    f"\n\n**PROMPT (text → video, 8s):**\n```\n{tp}\n```\n")
            else:
                ten_rows.append(
                    f"{n:03d}\t{fn}.png\t{fn}.mp4\t{t0:7.1f}-{t1:7.1f}s\t"
                    f"S{si:02d} {s['tag']}\t{lines[min(L0 + j, L1 - 1)]['text'][:38]}")
                blocks.append(
                    f"\n### {n:03d} · `{fn}` · {t0:.1f}–{t1:.1f}s ({t1-t0:.1f}s) · "
                    f"{sh['lv'].upper()} · cam `{sh['cam']}`{master}"
                    f"\n\n**ANH:**\n```\n{ip}\n```\n\n**VIDEO (i2v):**\n```\n{vp}\n```\n")

    def w(name, text):
        path = os.path.join(VD, name)
        io.open(path, "w", encoding="utf-8", newline="\n").write(text)
        return path

    # 🔴 PHAI di qua `pre` — neu hard-code "flow20_" thi lenh `--style anime`
    #    GHI DE len ban that, va no bao "da xuat flow20anime_*" nen khong ai
    #    nghi ngo (da dinh that 2026-09-03). Ten in ra man hinh va ten file ghi
    #    dia PHAI lay tu cung mot bien.
    if style == "real":
        w(f"{pre}_T2V.txt", "\n".join(t2v_lines) + "\n")
        w(f"{pre}_TENFILE.txt",
          "dong\tclip\tgiay\tscene\tloi doc\n" + "\n".join(ten_rows) + "\n")
        # don 2 file cua khuon cu de khong ai bom nham
        for old in (f"{pre}_IMAGE.txt", f"{pre}_VIDEO.txt"):
            q = os.path.join(VD, old)
            if os.path.exists(q):
                os.remove(q)
    else:
        w(f"{pre}_IMAGE.txt", "\n".join(img_lines) + "\n")
        w(f"{pre}_VIDEO.txt", "\n".join(vid_lines) + "\n")
        w(f"{pre}_TENFILE.txt",
          "dong\tanh\tclip\tgiay\tscene\tloi doc\n" + "\n".join(ten_rows) + "\n")
    w(f"{pre}_BLOCKS.md", "\n".join(blocks) + "\n")

    # ── GATE TU KHOA GOOGLE ────────────────────────────────────────────────
    # 🔴 Soi CHINH CHUOI DA XUAT. Bai hoc 2026-09-03: bao cao cua ham doi chu
    #    bao "da doi 75 cum" trong khi 6 mau regex im lang khong chay (loi
    #    escape). Bao cao cua mot lop KHONG chung minh duoc lop do da chay.
    gblock = collections.Counter()
    gshots = set()
    # 🔴 doi chu CHONG NHAU thi de lai tu lap ("dark-wood dark-wood display
    #    shelf") — mat khong thay khi luot 83 prompt, nen phai do bang may.
    dup_word = set()
    if style == "real":
        for idx, a in enumerate(t2v_lines):
            b = ""
            for pat in GOOGLE_BLOCK:
                k = len(re.findall(pat, a + " " + b, re.I))
                if k:
                    gblock[pat] += k
                    gshots.add(idx + 1)
            for m in DUP_RE.finditer(a + " " + b):
                dup_word.add((idx + 1, m.group(0)))

    # ── GATE ───────────────────────────────────────────────────────────────
    bad9 = []
    for si, s in enumerate(SCENES):
        if s["kind"] != "art":
            continue
        a = lines[s["L"]]["start"]
        b = lines[SCENES[si + 1]["L"]]["start"] if si + 1 < len(SCENES) else dur
        per = (b - a) / len(s["shots"])
        if per > 9.05:
            bad9.append((si, s["tag"], round(per, 1), math.ceil((b - a) / 9)))
    lens_i = [len(x) for x in img_lines]
    lens_v = [len(x) for x in vid_lines]

    print(f"→ {VD}")
    print(f"   STYLE = {style.upper()}")
    if style == "real":
        lens_t = [len(x) for x in t2v_lines]
        print(f"   {pre}_T2V.txt     {len(t2v_lines):3d} prompt text->video  "
              f"({min(lens_t)}–{max(lens_t)} ky)  ← MOT prompt / MOT shot")
    else:
        print(f"   {pre}_IMAGE.txt   {len(img_lines):3d} prompt  "
              f"({min(lens_i)}–{max(lens_i)} ky)")
        print(f"   {pre}_VIDEO.txt   {len(vid_lines):3d} prompt  "
              f"({min(lens_v)}–{max(lens_v)} ky)")
    print(f"   {pre}_BLOCKS.md   ban nguoi doc (loi doc JP + tung cap prompt)")
    print(f"   {pre}_TENFILE.txt dong <-> ten clip <-> giay <-> loi doc")
    print(f"\n   video {dur:.1f}s · {len(SCENES)} scene · {n} anh AI + 5 原典")
    print(f"   GATE san 9s: {'✅ SACH' if not bad9 else '🔴 ' + str(bad9)}")
    dup = [k for k in set(r.split('\t')[1] for r in ten_rows)
           if sum(1 for r in ten_rows if r.split('\t')[1] == k) > 1]
    print(f"   GATE trung ten anh: {'✅ khong trung' if not dup else '🔴 ' + str(dup)}")
    if style == "real" and tally:
        print(f"   LOP CHINH SACH: doi {sum(tally.values())} cum tu "
              f"({len(tally)} mau) — 4 nhom rui ro A/B/C/D")
        for pat, k in tally.most_common(8):
            print(f"      {k:4d}x  {pat}")
    if style == "real":
        if gblock:
            print(f"   🔴 GATE TU KHOA GOOGLE: {sum(gblock.values())} tu con sot "
                  f"o {len(gshots)} shot — CHUA DUOC GIAO")
            for pat, k in gblock.most_common(12):
                print(f"      {k:4d}x  {pat}")
        else:
            print(f"   GATE tu khoa Google: ✅ SACH "
                  f"({len(GOOGLE_BLOCK)} mau, 0 tu con sot)")
        if dup_word:
            print(f"   🔴 GATE TU LAP (doi chu chong nhau): {len(dup_word)} cho")
            for sh, w in sorted(dup_word)[:8]:
                print(f"      shot {sh}: {w!r}")
        else:
            print("   GATE tu lap: ✅ khong co")
    return 0 if not bad9 and not dup and not gblock and not dup_word else 1


if __name__ == "__main__":
    sys.exit(main())
