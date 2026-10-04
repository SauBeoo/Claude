# -*- coding: utf-8 -*-
r"""gen_flow19_real.py — bo prompt NGUOI THAT (photoreal) cho video 19.

User chot 2026-09-03: *"Toi muon lam dang nguoi that di, cho toi prompt gen anh
va video dang nguoi that."*

  flow19real_IMAGE.txt   74 prompt ANH   (text-to-image)
  flow19real_VIDEO.txt   74 prompt VIDEO (image-to-video)
  flow19real_BLOCKS.md   ban nguoi doc
  flow19real_TENFILE.txt dong N <-> ten anh <-> ten clip

GIU NGUYEN tu ban collage (3 tang lien mach van la thu quan trong nhat):
  · SCENE tung shot (canh vat khong doi, chi doi cach the hien)
  · CAST LOCK 5 nhan vat · PROP LOCK 18 vat  -> nhung ta theo kieu NGUOI THAT
  · MOTION CHAIN OPEN/mid/CLOSE · 3 hang nang luong peak/mid/calm

DOI:
  ① STYLE: paper collage -> **anh tai lieu photoreal**, ong kinh 50mm, anh sang
     cua so, mau tram am, grain phim nhe.
  ② 9 MOTION SIEU THUC -> ta thuc (`_motion19_real.py`).
  ③ FRAME RULES: khong con "dai giay xe" o dinh — thay bang yeu cau chua **vung
     tren ~1/5 IT CHI TIET** (tuong tron / troi / khoang trong) de dot chu Noto
     sau, va day 1/5 thoang cho phu de.
  ④ CAST LOCK ta **ky hon han** — mat nguoi that lech nhau la nhin ra ngay,
     trong khi cut-out giay thi de tha thu hon.

🔴 BAI HOC TU BAN COLLAGE (do duoc 2026-09-03, dung lap lai):
  · **Chi 4-5s DAU cua clip 8s la dung duoc** — nua sau AI het da, chi tiet hinh
    tut trung binh **15,1%** (nang nhat `84man` **41,3%**), chu the tan dan.
    Prompt VIDEO nay vi vay ghi ro: **don het chuyen dong vao 4 giay dau**.
  · ⛔ **KHONG ep `speed > 1`** luc dung — no day nguoi xem toi phan loang nhanh
    hon. Tha cat duoi.

🔴 DOC_FOCUS — 19 shot lay TO GIAY lam chu the thi con phai di xa hon: cho **chu so
   doc duoc** + **dau danh dau** o dung cho tay chi/khoanh, neu khong nguoi xem thay
   "chi vao cho trong" (user: *"nhin tay chi vao nhung cai text trang nhin no dieu
   qua"*). Xem dict `DOC_FOCUS`.

🔴 GIAY TO PHAI TRONG NHU THAT (user bat 2026-09-03: *"prompt giay toan text mau
   trang the"*): luat "moi giay to deu BLANK" be tu ban collage sang la SAI o
   photoreal - to A4 trang tinh trong gia ngay, ma nua so shot cua bai lay giay to
   lam chu the. Ly do goc cua luat do la **kanji AI gen bi nat net**; cach phim tai
   lieu that giai la: CO chu, nhung **ngoai net lay / qua nho / goc lia** nen khong
   doc duoc chu nao. Prompt VIDEO con phai chan "chu net len khi may day vao".
   ⓘ Khoi 原典 khong dinh luat nay - no la screenshot THAT, phai doc duoc.

⭐ MUOT / DIEN ANH (user chot 2026-09-03: *"video phai muot, hieu ung muot ma chuyen
   canh nhu dien anh"*): prompt VIDEO ep **ease-in/ease-out**, may truot dolly khong
   giat, motion blur deu, va **mo/dong shot bang mot khung TINH** de con dissolve vao
   ra sach. Khi DUNG thi doi lai: dissolve **0,6-0,8s** (ban collage chi 0,3-0,4s) va
   tuyet doi khong `speed != 1`.

⚠️ COMPLIANCE: canh AI realistic trong video => **TICK "altered/synthetic
   content"** luc upload (`youtube-compliance.md` §2.1, user chot 2026-08-09
   "tick cung oke"). Nhan vat HU CAU; cam mat nguoi that cu the.

CHAY:  python tools/gen_flow19_real.py
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from _motion19 import M as MOT_BASE          # noqa: E402
from _motion19_real import OVERRIDE          # noqa: E402
from gen_flow19 import (CAST_OF, HANDS_OF, PROP_OF, BEATS, VD)  # noqa: E402

MOT = dict(MOT_BASE)
MOT.update(OVERRIDE)

# 🔴 SCENE_OVERRIDE — i2v chi animate duoc thu **DA CO TRONG ANH**. Doi motion
# ma khong doi SCENE thi vat trong ACTION la vat *khong ton tai* => model tu bia
# ra giua chung => dung cai user bat 2026-09-03: *"tu dung la thu o dau ra do.
# Hanh dong hoac su vat su viec no phai logic voi nhau chu"*.
# Moi lan sua motion co nhac VAT MOI, phai them vat do vao day cung luot.
SCENE_OVERRIDE = {
    # motion real cho may lui ra lo BANG THONG BAO -> anh phai co san bang do
    "hataraku": ("a Japanese man in his early sixties in a work uniform checking "
                 "inventory on a shelf in a small warehouse, a clipboard under his arm, "
                 "daytime; on the wall behind him hangs a plain company notice board "
                 "with one sun-faded sheet of paper pinned to it, curling at the "
                 "corners; he looks focused and unhurried"),
}

# 🔴 DOC_FOCUS — shot ma TO GIAY LA CHU THE, hoac hanh dong chinh la DOC/CHI VAO
# (user bat 2026-09-03: *"nhin lich vs nhin tay chi vao nhung cai text trang nhin
# no dieu qua"*). Luat "chu mo khong doc duoc" o §FRAME cuu duoc anh nen, nhung o
# nhung shot NAY thi no lo lieu: nguoi xem thay ong ta chi vao cho trong.
#
# Cach phim tai lieu that giai — giu **CAU TRUC + DAU DANH DAU**, va cho **CHU SO
# doc duoc**: chu so A-rap AI gen ON DINH (`media-library.md` §2.9 — chi kanji moi
# nat net). Lich co so ngay 1..31 la thu vua that vua gen duoc.
DOC_FOCUS = {
    "kyuryo_meisai", "kyuryo_meisai_b", "kenkyu_b", "hondai", "hondai_b",
    "28000_b", "tanjoubi", "tanjoubi_b", "tanjoubi_c", "tanjoubi_d",
    "meisai_check", "meisai_check_b", "4kagetsu", "4kagetsu_b", "4kagetsu_c",
    "futatsu_mado", "futatsu_mado_b", "yokoku", "yokoku_b",
}
IMG_DOC = (
    "DOCUMENT IN FOCUS - this shot is ABOUT the paperwork, so it must not look empty "
    "or fake: give the sheet real structure the eye can follow - printed rule lines, "
    "column dividers, boxes, a faint official stamp - and a row of ARABIC NUMERALS that "
    "IS sharp and legible (digits only, e.g. dates or figures). Any Japanese wording "
    "stays small and softly out of focus so no kanji can be read. Where a hand points, "
    "circles or traces, put a clear visual marker at that exact spot - a red pen circle, "
    "a pencil tick or a highlighted row - so the gesture obviously lands on something."
)
VID_DOC = (
    "The marker and the digits the hand is working with stay sharp and stay exactly "
    "where they are; the Japanese wording around them stays soft and never resolves "
    "into readable characters."
)


# ══ CAST — ta theo kieu NGUOI THAT, ky hon ban collage ══════════════════════
CAST = {
    "M1": {"who": "松本さん 60 — case chinh, duoc nhan 2man8sen", "lock": (
        "a slim Japanese man of 60, about 168cm, narrow face with high cheekbones and a "
        "square jaw, short salt-and-pepper hair receding at the temples, deep lines "
        "either side of the mouth, tired but steady eyes, no glasses, clean-shaven, "
        "wearing a faded navy work jacket over a grey polo shirt")},
    "M2": {"who": "同僚のかた 60 — luong 40man, khong duoc mot dong", "lock": (
        "a heavier Japanese man of 60, round full face with soft jowls, thick hair still "
        "mostly black combed to one side with grey at the temples, black rectangular "
        "glasses, clean-shaven, wearing a short-sleeved white dress shirt with a pen in "
        "the breast pocket")},
    "M3": {"who": "研究員 — nguoi dan 案内役", "lock": (
        "a composed Japanese man in his late 60s, neat full white hair combed back, "
        "thin silver-rimmed reading glasses, calm unhurried expression, wearing a soft "
        "charcoal cardigan over a pale blue shirt")},
    "W1": {"who": "佐藤さん 66 — 次回予告, qua phu o Sendai", "lock": (
        "a Japanese woman of 66, soft white hair pinned back in a low bun, gentle round "
        "face with fine laugh lines, small stud earrings, wearing a muted grey-blue "
        "knitted cardigan over a cream blouse")},
    "C1": {"who": "vo chong gia — khoi CTA", "lock": (
        "an elderly Japanese couple in their 70s: the husband bald on top with white "
        "hair at the sides in a beige cardigan, the wife with short permed white hair "
        "in a soft lilac blouse, both relaxed and comfortable together")},
}
HANDS = {
    "M1": ("the same slim 60-year-old man's hands - lean with prominent knuckles and "
           "short clean nails, no ring, faded navy jacket cuff"),
    "M2": ("the same heavier 60-year-old man's hands - broad palms and thick fingers, "
           "a plain gold wedding band, short white shirt sleeve"),
    "M3": "the same elderly man's hands, thin and steady, charcoal cardigan cuff",
    "W1": "the same elderly woman's hands, slim with a thin gold ring, knitted cuff",
    "C1": "the same elderly couple's hands, one broader male pair and one slimmer female pair",
}
PROP = {
    "P_ENV": ("the SAME envelope every time: a plain kraft-brown Japanese pay envelope, "
              "no window, one horizontal fold crease across the middle, slightly worn corners"),
    "P_SLIP": ("the SAME payslip every time: one pale-cream A4 payslip with faint ruled "
               "rows and small printed figures filling the boxes - real-looking, but "
               "too small and too softly focused for any figure to be read"),
    "P_CAL": ("the SAME calendar every time: an ordinary cream wall-calendar page with a "
              "seven-column grid and small printed date numbers, thin navy border, seen "
              "at enough of an angle that the numbers do not read clearly"),
    "P_COIN": ("the SAME props every time: a stack of plain brass-coloured coins and one "
               "flat pale wooden ruler"),
    "P_DESK": ("the SAME desk every time: pale linen desk cloth, brass-handled magnifying "
               "glass, a small stack of printed government leaflets (dense small type, "
               "not legible), dark fountain pen, small brass desk clock"),
    "P_MONEY": ("the SAME notes every time: folded JAPANESE ten-thousand-yen notes - warm "
                "pale brown and soft violet paper, held folded so no printing shows. "
                "NOT green, NOT US dollars"),
    "P_HOUR": "the SAME hourglass every time: a small brass-framed hourglass with pale sand",
    "P_CUT": ("the SAME props every time: one cream A4 sheet and a pair of steel scissors "
              "with dark handles"),
    "P_GATE": ("the SAME gate every time: one waist-high steel turnstile with three barred "
               "arms in a pale-walled corridor"),
    "P_COUNTER": ("the SAME public office every time: pale wood-veneer counter, blank white "
                  "sign boards above, one grey moulded chair, pale institutional walls"),
    "P_BOOK": ("the SAME passbook every time: a small navy-covered Japanese bank passbook "
               "opened flat, ruled entry lines carrying a few rows of small printed "
               "figures, softly out of focus so nothing reads"),
    "P_NOTE": ("the SAME notice every time: one crisp official-looking A4 sheet with a "
               "ruled table of small printed entries, held at an angle so the text is "
               "clearly present but not legible"),
    "P_WARE": ("the SAME workplace every time: a small Japanese warehouse, pale metal "
               "shelving, plain cardboard boxes, one high window"),
    "P_BREAK": ("the SAME break room every time: pale formica table, grey vending machine "
                "against a cream wall, one strip light"),
    "P_PIN": ("the SAME props every time: a shallow wooden desk drawer with a plain brass "
              "handle and one small round company lapel pin with plain navy enamel inside; "
              "the same table lamp behind"),
    "P_CORR": ("the SAME corridor every time: a plain company corridor, pale grey walls, "
               "pale linoleum floor, one closed door at the far end"),
    "P_LIVING": ("the SAME living room every time: low beige fabric sofa, small dark wood "
                 "low table, pale ceramic teapot with two cups, a plain tablet"),
    "P_ROOM": ("the SAME room every time: a quiet tatami room at dusk, low dark wood table, "
               "one standing floor lamp with a warm cream shade"),
}

# ══ FILE 1 — PROMPT ANH (photoreal) ════════════════════════════════════════
IMG_STYLE = (
    "Photorealistic documentary photograph, shot on a full-frame camera with a 50mm lens "
    "at f/2.8, natural window light, muted warm colour grade, gentle film grain, shallow "
    "depth of field with a softly blurred background. Contemporary JAPAN, ordinary "
    "middle-class settings that look genuinely lived in - worn edges, honest textures, a "
    "little everyday clutter. Calm, respectful, unposed - like a frame from a quiet "
    "documentary, NOT a stock photo, NOT an advertisement. "
    "NOT illustration, NOT collage, NOT a 3D render, NOT anime, no stylisation."
)
IMG_FRAME = (
    "FRAME RULES (obey these before anything else): one clear subject, LARGE in frame. "
    "Keep the TOP fifth of the frame visually SIMPLE and uncluttered - a plain wall, a "
    "window, ceiling or open space - with nothing important in it, so a caption can be "
    "placed there later. Keep the BOTTOM fifth free of faces and important detail, and "
    "keep the very bottom-right corner clear. PAPERWORK MUST LOOK REAL, NEVER BLANK: "
    "documents, forms, payslips, calendars and leaflets carry normal printed matter - "
    "faint ruled rows, small dense body text, boxes and stamps - but it is never legible: "
    "it sits OUT OF FOCUS, or is too small, or falls at a grazing angle, so no individual "
    "character can be read. A sheet of pure blank white paper reads as fake - do not show "
    "one. No large or foreground text, no headline a viewer could read, no signage, no "
    "logos, no brand marks, no watermark. Aspect ratio 16:9."
)
IMG_TAIL = ("Reminder: printed matter looks natural but stays unreadable (out of focus or "
            "too small) - never a blank white sheet, and no text big enough to read. The "
            "top fifth stays visually simple.")
IMG_JP = ("Everyone in the frame is JAPANESE and elderly (60s-70s), in modest everyday "
          "Japanese clothing - not Western, not American styling.")

# ══ FILE 2 — PROMPT VIDEO (i2v, photoreal) ═════════════════════════════════
VID_HEAD = ("Animate this photograph into a short live-action shot - real people, real "
            "physics, documentary camera. Keep it photoreal; do not stylise.")
VID_TAIL = (
    "AESTHETIC: keep the grade, grain, lighting and depth of field exactly as in the "
    "photo; the background stays softly out of focus. Printed matter on documents stays "
    "exactly as unreadable as it is in the photo - it must NOT sharpen into legible "
    "characters as the camera moves, and no new text appears anywhere. The top fifth "
    "stays visually simple and uncluttered. "
    "CONSTRAINTS: real anatomy and real weight - hands keep five fingers, faces do not "
    "drift or change identity, objects do not appear, vanish, melt or pass through each "
    "other. ONE continuous action that does not loop or reset. "
    "⭐ PUT ALL THE MOVEMENT IN THE FIRST FOUR SECONDS and let the last part simply "
    "settle - do not invent extra action to fill the time. "
    "⭐ MOTION QUALITY - this matters as much as the action itself: everything moves "
    "SMOOTHLY and CINEMATICALLY. Every move eases in and eases out, never starts or "
    "stops abruptly. The camera glides on a dolly - no jitter, no stutter, no snapping, "
    "no frame-to-frame flicker. People move at a natural unhurried pace with real "
    "follow-through. Motion blur is gentle and consistent. Think of a slow, composed "
    "documentary shot on a cine camera, not a phone clip. "
    "⭐ Begin and end the shot on a COMPOSED, STEADY frame so it can be dissolved "
    "into and out of cleanly. "
    "No dialogue, no voice, no music, no sound effects."
)
CAM = {
    "static": "CAMERA: locked off on a tripod - no pan, no zoom, no shake.",
    "parallax": ("CAMERA: locked off, but a very slight handheld breathing gives the shot "
                 "depth - no pan, no zoom."),
    "push": "CAMERA: a slow steady dolly push-in of about five percent, easing at the end.",
    "push_hard": ("CAMERA: a decisive dolly push-in of about ten percent that arrives on "
                  "the beat - no shake."),
    "pull_out": ("CAMERA: a slow steady dolly pull-back that gradually reveals more of the "
                 "room - no pan, no shake."),
    "whip": "CAMERA: one quick whip-pan that snaps onto the subject and settles.",
}
AMP = {
    "peak": ("PERFORMANCE: this is the payoff beat - the action must be decisive and "
             "unmistakable at a glance, done with real weight and follow-through."),
    "mid": ("PERFORMANCE: clear, purposeful movement - the subject genuinely does "
            "something; nothing should read as a frozen photo."),
    "calm": ("PERFORMANCE: quiet and restrained - this is a resting beat, let it breathe."),
}
V_OPEN = ("CONTINUITY: this shot OPENS a section - start from exactly the pose in the "
          "photograph, do not re-stage it.")
V_MID = ("CONTINUITY: this shot CONTINUES the previous one in the same place - carry the "
         "same direction of movement onward; never reverse it.")
V_CLOSE = ("CONTINUITY: this shot CLOSES the section - the action comes to a natural rest "
           "and holds, so the cut to the next section does not jump.")


def locks(name, first_of):
    key, hkey = CAST_OF.get(name), HANDS_OF.get(name)
    bits, tags = [], []
    ids = [c for c in (key or hkey or "").split("+") if c]
    for cid in ids:
        tags.append(cid)
        if key:
            role = ("on the LEFT, calm" if cid == "M1" else "on the RIGHT, uneasy") \
                if len(ids) > 1 else ""
            lead = f"RECURRING CHARACTER {cid}" + (f" ({role})" if role else "")
            if first_of.get(cid) == name:
                bits.append(f"CAST LOCK - {lead}; THIS IMAGE IS THE MASTER REFERENCE for "
                            f"his/her face, use it for every other shot: {CAST[cid]['lock']}")
            else:
                bits.append(f"CAST LOCK - {lead}; the SAME PERSON as the reference image - "
                            f"identical face, same age, same hair: {CAST[cid]['lock']}")
        else:
            bits.append(f"CAST LOCK - the hands belong to RECURRING CHARACTER {cid}: "
                        f"{HANDS[cid]}")
    props = PROP_OF.get(name, [])
    for j, p in enumerate(props):
        txt = PROP[p]
        bits.append(("and " + re.sub(r"^the SAME [^:]+: ", "", txt)) if j
                    else f"PROP LOCK - {txt}")
    return " ".join(b if b.endswith(".") else b + "." for b in bits), tags, props


def main():
    doc = json.load(io.open(BEATS, encoding="utf-8"))
    beats = doc["beats"]
    first_of, seen, order = {}, set(), []
    for b in beats:
        for s in b.get("shots", []):
            nm = s.get("src_card", "").replace("card_19_", "")
            order.append(nm)
            for cid in (CAST_OF.get(nm) or "").split("+"):
                if cid and cid not in seen:
                    seen.add(cid)
                    first_of[cid] = nm

    img, vid, rows, blocks, lvs = [], [], [], [], []
    n = 0
    for b in beats:
        shots = b.get("shots", [])
        for k, shot in enumerate(shots):
            n += 1
            nm = shot.get("src_card", "").replace("card_19_", "")
            scene = SCENE_OVERRIDE.get(nm) or re.split(
                r"\s*Any person shown is JAPANESE", shot["scene"])[0].strip()
            scene = re.sub("[　-鿿]+", " study ", scene)
            scene = re.sub(r"\s{2,}", " ", scene).strip()
            cont, tags, props = locks(nm, first_of)
            has_person = bool(CAST_OF.get(nm) or HANDS_OF.get(nm))

            parts = [IMG_STYLE, IMG_FRAME, f"SCENE: {scene}."]
            if nm in DOC_FOCUS:
                parts.append(IMG_DOC)
            if cont:
                parts.append(cont)
            if has_person:
                parts.append(IMG_JP)
            parts.append(IMG_TAIL)
            img.append(re.sub(r"\s+", " ", " ".join(parts)).strip())

            mv = MOT[nm]
            chain = V_OPEN if (k == 0 or len(shots) == 1) else (
                V_CLOSE if k == len(shots) - 1 else V_MID)
            vparts = [VID_HEAD, f"ACTION: {mv['m']}.", CAM[mv["cam"]], AMP[mv["lv"]]]
            if nm in DOC_FOCUS:
                vparts.append(VID_DOC)
            vparts += [chain, VID_TAIL]
            vid.append(re.sub(r"\s+", " ", " ".join(vparts)).strip())
            lvs.append(mv["lv"])

            anchor = [c for c in tags if first_of.get(c) == nm]
            ref = [c for c in tags if first_of.get(c) != nm]
            note = ("ANCHOR " + "+".join(anchor)) if anchor else ""
            if ref:
                note = (note + " | khop " + "+".join(
                    f"{c}->#{order.index(first_of[c]) + 1}" for c in ref)).strip(" |")
            rows.append((n, b["id"], b.get("title_cn", ""), nm,
                         shot.get("shot_size", ""), mv["lv"].upper(), note or "-",
                         "+".join(props) if props else "-",
                         "OPEN" if chain is V_OPEN else
                         ("CLOSE" if chain is V_CLOSE else "mid"),
                         "REAL" if nm in OVERRIDE else ""))
            blocks.append((n, b["id"], b.get("title_cn", ""), nm, img[-1], vid[-1]))

    io.open(VD + "/flow19real_IMAGE.txt", "w", encoding="utf-8",
            newline="\n").write("\n".join(img) + "\n")
    io.open(VD + "/flow19real_VIDEO.txt", "w", encoding="utf-8",
            newline="\n").write("\n".join(vid) + "\n")
    ten = ["# dong N  ->  ten anh  ->  ten clip   (thu tu = THOI GIAN trong video)", ""]
    for r in rows:
        ten.append(f"{r[0]:>3}  real19_{r[3]}.png".ljust(42) +
                   f"-> rclip19_{r[3]}.mp4".ljust(34) + f"[beat {r[1]}]")
    io.open(VD + "/flow19real_TENFILE.txt", "w", encoding="utf-8",
            newline="\n").write("\n".join(ten) + "\n")

    md = ["# video 19 — 74 prompt ANH + 74 prompt VIDEO, ban **NGUOI THAT**\n"]
    md.append(
        "> User chot 2026-09-03: *\"Toi muon lam dang nguoi that di\"*.\n>\n"
        "> **Quy trinh 2 buoc:** `flow19real_IMAGE.txt` -> gen 74 anh -> DUYET MAT ->\n"
        "> `flow19real_VIDEO.txt` -> nap anh so N + prompt dong N -> clip N.\n>\n"
        "> ⚠️ **TICK 'altered/synthetic content' luc upload** — canh AI realistic bat buoc\n"
        "> khai bao (`youtube-compliance.md` §2.1). Nhan vat HU CAU, cam mat nguoi that.\n")
    md.append("\n## Khac gi ban collage\n")
    md.append(
        "| | collage | NGUOI THAT |\n|---|---|---|\n"
        "| style | giay cat dan, halftone | anh tai lieu 50mm f/2.8, anh sang cua so |\n"
        "| dinh khung | dai giay xe de dot chu | **vung tren 1/5 IT CHI TIET** (tuong/troi) |\n"
        "| 9 motion sieu thuc | giay bay, san tach doi | **ta thuc** — may lui/day, dien xuat |\n"
        "| CAST LOCK | ta vua | **ta ky** (cao, khuon mat, toc, ao) — mat that lech la thay ngay |\n"
        "| chuyen dong | deu ca 8s | **don vao 4 GIAY DAU** (xem duoi) |\n")
    md.append("\n## 🔴 Bai hoc do duoc tu ban collage — da dua vao prompt nay\n")
    md.append(
        "Do 8 clip cua ban collage: **nua sau clip tut trung binh 15,1% chi tiet hinh**\n"
        "(nang nhat `84man` **−41,3%**), chu the tan dan — do la thu gay cam giac\n"
        "\"suong\". Nen prompt VIDEO nay ghi thang: **don het chuyen dong vao 4 giay dau**,\n"
        "phan cuoi chi lang xuong.\n\n"
        "⛔ Va luc dung: **khong ep `speed > 1`** — ban truoc dat toi 1,25x o 7 scene, tuc\n"
        "day nguoi xem toi phan loang nhanh hon 25%. Tha cat duoi clip.\n")
    md.append("\n## Bang CAST (5) — gen ANCHOR truoc, dung lam reference cho phan con lai\n")
    md.append("| id | la ai | ANCHOR | mo ta chot cung |\n|---|---|---|---|")
    for cid, v in CAST.items():
        a = first_of.get(cid, "-")
        md.append(f"| **{cid}** | {v['who']} | #{order.index(a)+1} `{a}` | {v['lock']} |")
    md.append("\n🔴 Voi nguoi that, **reference image la BAT BUOC**, khong phai tuy chon —\n"
              "cau chu mo ta mat chi giu duoc ~50%. Gen 5 anh ANCHOR truoc, duyet ky,\n"
              "roi moi gen 69 anh con lai va nap anh anchor tuong ung.\n")
    md.append("\n## Bang 74 shot\n")
    md.append("| # | beat | headline | shot | co | NANG LUONG | cast | prop | chain | |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append("| " + " | ".join(str(x) for x in r) + " |")
    md.append("\n---\n\n## 74 cap prompt\n")
    for (i, bid, title, nm, a, v) in blocks:
        md.append(f"\n### {i}. `{nm}`  — beat {bid} {title}\n")
        md.append(f"**ANH** *({len(a)} ky)*\n\n```\n{a}\n```\n")
        md.append(f"**VIDEO** *({len(v)} ky)*\n\n```\n{v}\n```\n")
    io.open(VD + "/flow19real_BLOCKS.md", "w", encoding="utf-8",
            newline="\n").write("\n".join(md) + "\n")

    import collections
    print(f"OK {n} shot")
    print(f"   ANH   : flow19real_IMAGE.txt  {min(map(len,img))}-{max(map(len,img))} ky")
    print(f"   VIDEO : flow19real_VIDEO.txt  {min(map(len,vid))}-{max(map(len,vid))} ky")
    print("   MOTION: " + " · ".join(f"{k} {v}" for k, v in
          sorted(collections.Counter(lvs).items(), key=lambda x: -x[1])) +
          f"  | viet lai cho photoreal: {len(OVERRIDE)}")
    print(f"   doc   : flow19real_BLOCKS.md | map: flow19real_TENFILE.txt")
    assert n == 74, n
    for x in img:
        sc = x[x.index("SCENE:"):]
        assert "collage" not in sc and "paper cut-out" not in sc, "con sot chu collage"


if __name__ == "__main__":
    main()
