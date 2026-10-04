# -*- coding: utf-8 -*-
r"""gen_flow19.py — CA BO video 19: prompt ANH + prompt ANIMATION, co LIEN MACH.

User chot 2026-09-02: *"render them video nay theo dang E:\vox-director. Hay viet
prompt de toi tao anh va prompt video toi tao animation. Chu y Video phai lien
mach voi nhau nhe"*.

Mo rong `gen_flow_ch3.py` (9 shot demo) ra **ca 74 shot / 29 beat**, va them lop
LIEN MACH — thu duy nhat ban demo chua co.

  flow19_IMAGE.txt    74 prompt ANH   (text-to-image)  -> gen 74 poster tinh
  flow19_VIDEO.txt    74 prompt VIDEO (image-to-video) -> animate dung 74 anh do
  flow19_BLOCKS.md    ban nguoi doc: bang CAST/PROP + thu tu gen + tung cap prompt
  flow19_TENFILE.txt  dong N <-> ten file anh <-> ten file clip

VI SAO TACH 2 BUOC (README vox-director): *"The look is born in the IMAGE step.
   All the collage DNA lives in that image — if the poster isn't a rich collage,
   nothing downstream saves it."* Gen anh sai thi re; gen video sai la dot ca luot.

BA TANG LIEN MACH (phan them moi so voi ban ch3):

  (1) CAST LOCK — 6 nhan vat lap lai xuyen 74 shot. Gen 74 prompt doc lap thi ra
      74 ong gia KHAC NHAU. Nang nhat la beat 18 `futari` = CALLBACK cold open
      ("冒頭の、ふたりの男性。あれが、このおふたりです") — hai ong o day PHAI dung
      la 松本 (beat 1/9/11) va 同僚 (beat 16/17), khong thi callback mat nghia.
  (2) PROP LOCK — 14 vat/bo canh lap lai (phong bi nau, phieu luong, lich tuong,
      chong xu + thuoc ke, ban 研究...). Cung mot vat o 3 shot phai cung hinh dang.
  (3) MOTION CHAIN — tool giu DUNG THU TU timeline va danh dau OPEN/mid/CLOSE de
      cat sang beat sau khong giat.

  (4) ⭐ MOTION VIET THEO LOI DOC + 3 HANG NANG LUONG — `tools/_motion19.py`.
      Them 2026-09-02 sau khi user bat: *"mày có dựa theo script để tạo animation
      không thế. Sao tao thấy animation sinh ra tù thế"*. Ban truoc lay nguyen
      `element_motion` cua beats.json (motion_style=calm, constraints=strict,
      camera 56/74 static, 60/74 dong tu yeu) roi con chong them "Calm restrained
      amplitude" o MOI shot => tu. Nay 25 peak / 30 mid / 19 calm, moi motion viet
      theo NGHIA cua cau loi tai dung giay do. Chi tiet: docstring `_motion19.py`.

HAI THU PHAI CO O CA HAI FILE (di nguyen tu ban ch3, dung bo khi sua):
   (a) banner TRONG o dinh khung ~1/5 — cho de dot chu Noto Sans JP sau (kanji
       AI gen la nat net). File VIDEO cung phai nhac, vi i2v hay tu ve chu vao dai trong.
   (b) no text anywhere — moi mat giay/giay to phai blank.

CHAY:  python tools/gen_flow19.py
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from _motion19 import M as MOT  # noqa: E402  (motion viet theo loi doc)

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "19_kounenrei-koyou-keizoku-kyufu")
BEATS = os.path.join("E:" + os.sep, "vox-director", "out", "nenkin-19", "beats.json")

BG = {"aged cream newsprint": "aged cream newsprint",
      "charcoal ink navy": "deep charcoal-navy ink",
      "deep red": "deep red", "mustard yellow": "mustard yellow"}

# == TANG (1) — CAST LOCK ==================================================
# Moi cast = mot cau MO TA CHOT CUNG, dan y NGUYEN VAN vao moi prompt anh co
# nhan vat do. Doi mo ta thi phai gen lai TAT CA shot cua cast do.
CAST = {
    "M1": {
        "who": "松本さん 60 — case chinh, duoc nhan 2man8sen",
        "lock": ("a slight Japanese man of sixty, thin build, short cropped hair "
                 "grey at the temples with a receding front, long narrow face, "
                 "deep smile lines, clean-shaven, no glasses"),
    },
    "M2": {
        "who": "同僚のかた 60 — luong 40man, khong duoc mot dong",
        "lock": ("a heavier-set Japanese man of sixty, round face, fuller cheeks, "
                 "thick hair still mostly black with grey at the sides, "
                 "black-framed rectangular glasses, clean-shaven"),
    },
    "M3": {
        "who": "研究員 — nguoi dan 案内役 cua kenh",
        "lock": ("a calm Japanese man in his late sixties, neat white hair combed "
                 "back, narrow silver-rimmed reading glasses, a soft charcoal "
                 "cardigan over a pale shirt"),
    },
    "W1": {
        "who": "佐藤さん 66 — 次回予告, qua phu o Sendai",
        "lock": ("a Japanese woman of sixty-six, soft white hair pinned back in a "
                 "low bun, gentle rounded face, a muted grey-blue knitted cardigan"),
    },
    "C1": {
        "who": "vo chong gia — khoi CTA",
        "lock": ("an elderly Japanese couple in their seventies: the husband bald "
                 "on top with white hair at the sides in a beige cardigan, the wife "
                 "with short permed white hair in a soft lilac blouse"),
    },
}
# hands = shot chi thay BAN TAY cua cast do (khong thay mat) -> lock nhe hon
HANDS = {
    "M1": ("the same slight sixty-year-old man's hands - lean, prominent knuckles, "
           "no ring, plain shirt cuff"),
    "M2": ("the same heavier sixty-year-old man's hands - broad palms, thick "
           "fingers, a plain wedding band, short-sleeve white shirt cuff"),
    "M3": "the same elderly man's hands with a charcoal cardigan cuff",
    "W1": "the same elderly woman's hands, slim, a thin gold ring, knitted cuff",
    "C1": ("the same elderly couple's hands, one broader male pair and one slimmer "
           "female pair"),
}

# == TANG (2) — PROP LOCK ==================================================
PROP = {
    "P_ENV": ("the SAME envelope design every time: a plain unprinted kraft-brown "
              "window-less envelope, portrait format, one horizontal fold crease "
              "across the middle"),
    "P_SLIP": ("the SAME payslip every time: a single pale-cream sheet with three "
               "printed rule lines and an empty box grid, no characters at all"),
    "P_CAL": ("the SAME calendar every time: one pale cream wall-calendar page, a "
              "seven-column grid of empty squares, a thin navy border, no numbers"),
    "P_COIN": ("the SAME props every time: a stack of plain unmarked brass-coloured "
               "coins and one flat pale wooden ruler with faint tick marks"),
    "P_DESK": ("the SAME desk every time: pale linen desk cloth, a brass-handled "
               "magnifying glass, a small stack of pale grey leaflets, a dark "
               "fountain pen, a small brass desk clock"),
    # 🔴 SUA 2026-09-03 sau khi soi clip da gen: ban cu ghi "pale-GREEN banknotes"
    # => model ve thang **do la My** (chan dung Franklin, so 100) o 4 clip, nang
    # nhat la cold open va callback `futari`. Kenh Nhat noi ve 円 —
    # `feedback_jp_script_yen_only`. Chua bang cach BO tu "green" va ta giay tien
    # NHAT (nau-vang am), + cam tuong minh USD.
    "P_MONEY": ("the SAME banknotes every time: JAPANESE banknotes - warm pale "
                "gold and soft brown paper, slightly longer and narrower than a "
                "US bill, faces completely blank with no portrait and no numerals. "
                "NOT green, NOT American dollars, no US currency of any kind"),
    "P_HOUR": ("the SAME hourglass every time: a small brass-framed hourglass with "
               "pale cream sand"),
    "P_CUT": ("the SAME props every time: one cream rectangular sheet and a pair of "
              "steel scissors with dark handles"),
    "P_GATE": ("the SAME gate every time: a single waist-high steel one-way "
               "turnstile with three barred arms, pale corridor walls"),
    "P_COUNTER": ("the SAME public office every time: a pale wood-veneer counter, "
                  "blank white sign boards above it, one grey moulded chair, "
                  "pale institutional walls"),
    "P_BOOK": ("the SAME passbook every time: a small navy-covered bank passbook "
               "opened flat, ruled entry lines, all entries empty"),
    "P_NOTE": ("the SAME notice every time: one crisp official-looking A4 sheet, a "
               "ruled table printed on it, every cell empty"),
    "P_WARE": ("the SAME workplace every time: a small warehouse with pale metal "
               "shelving, plain cardboard boxes, one high window casting daylight"),
    "P_BREAK": ("the SAME break room every time: a pale formica table, a grey "
                "vending machine against a cream wall, one strip light"),
    "P_PIN": ("the SAME props every time: a shallow wooden desk drawer with a plain "
              "brass handle, and inside it one small round company lapel pin with a "
              "plain unmarked navy enamel face; the same table lamp behind"),
    "P_CORR": ("the SAME corridor every time: a plain company corridor, pale grey "
               "walls, a pale linoleum floor, one closed door at the far end"),
    "P_LIVING": ("the SAME living room every time: a low beige fabric sofa, a small "
                 "dark wood low table, a pale ceramic teapot with two cups, a plain "
                 "tablet with a blank pale screen"),
    "P_ROOM": ("the SAME room every time: a quiet tatami room at dusk, a low dark "
               "wood table, one standing floor lamp with a warm cream shade"),
}

# == MAP 74 shot -> cast / hands / prop ====================================
# key = ten shot (bo tien to card_19_)
CAST_OF = {
    "hataraku": "M1", "hatena": "M1", "hatena_c": "M1", "matsumoto": "M1",
    "matsumoto_c": "M1", "28000": "M1", "madoguchi2": "M1", "futatsu_mado": "M1",
    "douryou": "M2", "douryou_c": "M2",
    "tadashi": "M3", "tadashi_c": "M3",
    "yokoku": "W1", "yokoku_b": "W1", "yokoku_d": "W1",
    "cta": "C1", "cta_d": "C1",
    "futari": "M1+M2", "futari_c": "M1+M2",
}
HANDS_OF = {
    "hataraku_b": "M1", "hataraku_c": "M1", "kyuryo_meisai": "M1",
    "koyou_hoken": "M1", "koyou_hoken_b": "M1", "matsumoto_b": "M1",
    "28000_b": "M1", "tanjoubi": "M1", "jougen_d": "M1", "modoranai": "M1",
    "modoranai_b": "M1", "meisai_check": "M1", "meisai_check_b": "M1",
    "4kagetsu_c": "M1", "futatsu_mado_b": "M1",
    "douryou_b": "M2", "zero": "M2",
    "tadashi_b": "M3",
    "cta_b": "C1", "cta_c": "C1",
    "futari_b": "M1+M2",
}
PROP_OF = {
    "hataraku": ["P_WARE"], "hataraku_b": ["P_WARE"], "hataraku_c": ["P_WARE"],
    "kyuryo_meisai": ["P_SLIP"], "kyuryo_meisai_b": ["P_SLIP"],
    "hatena": ["P_ENV"], "hatena_b": ["P_ENV"], "hatena_c": ["P_ENV"],
    "kenkyu": ["P_DESK"], "kenkyu_b": ["P_DESK"],
    "koyou_hoken": ["P_MONEY"], "koyou_hoken_b": ["P_MONEY"],
    "75percent": ["P_COIN"], "75percent_b": ["P_COIN"],
    "jougen": ["P_COIN"], "jougen_b": ["P_COIN"], "jougen_c": ["P_COIN"],
    "jougen_d": ["P_COIN"],
    "28000": ["P_BOOK"], "28000_b": ["P_BOOK"], "28000_c": ["P_BOOK"],
    "hondai": ["P_DESK"], "hondai_b": ["P_DESK"],
    "84man": ["P_MONEY"], "84man_b": ["P_MONEY"],
    "tanjoubi": ["P_CAL"], "tanjoubi_b": ["P_CAL"], "tanjoubi_c": ["P_CAL"],
    "tanjoubi_d": ["P_CAL"],
    "wariai": ["P_SLIP", "P_COIN"],
    "douryou": ["P_SLIP", "P_BREAK"], "douryou_b": ["P_SLIP", "P_BREAK"],
    "douryou_c": ["P_ENV", "P_BREAK"],
    "zero": ["P_ENV"], "zero_b": ["P_ENV"],
    "futari": ["P_ENV", "P_CORR"], "futari_b": ["P_ENV", "P_CORR"],
    "futari_c": ["P_CORR"],
    "madoguchi2": ["P_COUNTER"], "madoguchi2_b": ["P_COUNTER"],
    "kuriage": ["P_HOUR"], "kuriage_b": ["P_HOUR"], "kuriage_c": ["P_HOUR"],
    "nijuu": ["P_CUT"], "nijuu_b": ["P_CUT"], "nijuu_c": ["P_CUT"],
    "modoranai": ["P_GATE"], "modoranai_b": ["P_GATE"], "modoranai_c": ["P_GATE"],
    "meisai_check": ["P_SLIP"], "meisai_check_b": ["P_SLIP"],
    "4kagetsu": ["P_CAL"], "4kagetsu_b": ["P_CAL"], "4kagetsu_c": ["P_CAL"],
    "futatsu_mado": ["P_SLIP"], "futatsu_mado_b": ["P_SLIP"],
    "chuui": ["P_COUNTER"], "chuui_b": ["P_COUNTER"], "chuui_c": ["P_COUNTER"],
    "yokoku": ["P_NOTE", "P_ROOM"], "yokoku_b": ["P_NOTE"],
    "yokoku_c": ["P_NOTE", "P_ROOM"], "yokoku_d": ["P_ROOM"],
    "matsumoto": ["P_PIN"], "matsumoto_b": ["P_PIN"], "matsumoto_c": ["P_PIN"],
    "tadashi": ["P_DESK"], "tadashi_b": ["P_DESK"], "tadashi_c": ["P_DESK"],
    "cta": ["P_LIVING"], "cta_b": ["P_LIVING"], "cta_c": ["P_LIVING"],
    "cta_d": ["P_LIVING"],
}

# == FILE 1 — PROMPT ANH ===================================================
IMG_STYLE = (
    "Vintage newsprint editorial PAPER COLLAGE, mid-century JAPANESE front-page news "
    "feature: bold cut-out photographs and illustrations laid over an aged broadsheet "
    "page, heavy halftone print dots, aged newsprint texture, slight ink "
    "misregistration - reads like a newspaper feature spread, not an advertisement. "
    "Clearly layered hand-cut paper cut-outs with visible torn and scissor-cut edges, "
    "tape corners and soft real paper drop shadows, on a bold flat {bg} paper "
    "background, with scattered geometric paper accents (triangles, circles, zigzags, "
    "washi tape). Palette: cream white, deep navy ink, deep red, mustard yellow, "
    "charcoal black. Every figure is a PRINTED, illustrated cut-out with a thick white "
    "die-cut outline - NOT CGI, NOT a 3D render, NOT photoreal; keep print grain and "
    "paper imperfections. High-contrast, tactile, hand-assembled."
)
IMG_FRAME = (
    "FRAME RULES (obey these before anything else): the collage FILLS the frame edge to "
    "edge with ONE clear LARGE subject cropped by the bottom edge. Across the TOP leave a "
    "torn-paper banner strip about one fifth of the height that is COMPLETELY BLANK - "
    "clean empty paper, nothing written on it, nothing important behind it. Keep the "
    "bottom fifth free of any important detail or face and the very bottom-right corner "
    "clear. EVERY paper surface, document, sign and screen in the image is BLANK and "
    "unprinted: no text, letters, numbers, headline, caption, signage, logo or watermark "
    "anywhere in the frame. Aspect ratio 16:9."
)
IMG_TAIL = (
    "Reminder: the top banner strip stays completely blank and nothing anywhere in the "
    "image is written, printed or lettered."
)
IMG_JP = ("Any person shown is JAPANESE and elderly (60s-70s) in modest everyday "
          "Japanese clothing - not Western, no 1950s Americana styling.")

# == FILE 2 — PROMPT VIDEO (i2v: anh da co, chi noi CHUYEN DONG) ===========
VID_HEAD = ("Animate this still paper-collage poster as a stop-motion MOTION GRAPHIC - "
            "printed paper cut-outs, not photoreal.")
VID_TAIL = (
    "AESTHETIC: keep the torn-paper, tape, halftone, newsprint and paper-stencil "
    "textures and the bold flat background exactly as they are; grain and halftone "
    "dots may breathe subtly frame to frame. KEEP the blank torn-paper banner strip "
    "across the top EMPTY - do not draw any text, letters or numbers on it or anywhere "
    "else in the frame. CONSTRAINTS: stay flat 2D - no 3D rotation, no perspective "
    "change, camera parallel to the poster. ONE continuous move that does not loop, "
    "retract or reset. Rigid paper - no morph, no melt, no re-rendering of faces. "
    "Animate the motion only; don't re-render the picture. "
    "No dialogue, no voice, no music, no sound effects."
)
# == BIEN DO theo HANG NANG LUONG (thay cho "Calm restrained" o MOI shot) ==
# Truoc: 74/74 shot deu "Calm, restrained amplitude" => animation "tu".
# `audience-45plus.md` §2 bat nhip CAT cham, KHONG bat bien do TRONG mot shot.
AMP = {
    "peak": ("AMPLITUDE: BOLD and large - this is a payoff beat, the motion must be "
             "unmistakable at a glance. Paper pieces are allowed to travel right across "
             "the frame and leave it. Push the movement to the top of what the image can "
             "take without tearing the collage look."),
    "mid": ("AMPLITUDE: moderate but clearly visible - several elements genuinely move, "
            "far more than a shimmer. Nothing should read as a still frame."),
    "calm": ("AMPLITUDE: calm and restrained - this is a resting beat between the loud "
             "ones, so keep it quiet and let it breathe."),
}
CAM = {
    "static": "CAMERA: locked off, completely static - no pan, no zoom, no shake.",
    "parallax": ("CAMERA: locked off, but the layered paper planes drift at clearly "
                 "different speeds for real depth - the camera itself does not move."),
    "push": ("CAMERA: a steady push-in of about five percent across the shot, easing at "
             "the end - no pan, no shake."),
    "push_hard": ("CAMERA: a decisive push-in of about ten percent across the shot, "
                  "arriving hard on the beat - no pan, no roll, no shake."),
    "whip": ("CAMERA: one fast whip-pan of a few degrees that snaps onto the subject and "
             "settles - nothing else."),
}
# lop lien mach tang (3) — noi vao prompt VIDEO
V_OPEN = ("CONTINUITY: this shot OPENS a new section - begin from the pose already in "
          "the image, do not re-stage it.")
V_MID = ("CONTINUITY: this shot CONTINUES the previous one in the same place - carry "
         "the same movement direction onward; never reverse it.")
V_CLOSE = ("CONTINUITY: this shot CLOSES the section - the motion must come to a full "
           "REST before the clip ends and hold still, so the cut to the next section "
           "does not jump.")


def cast_block(name, first_of):
    """Khoi CONTINUITY cho prompt ANH + nhan cast/prop de ghi bang."""
    key = CAST_OF.get(name)
    hkey = HANDS_OF.get(name)
    bits, tags = [], []
    ids = [c for c in (key or hkey or "").split("+") if c]
    for cid in ids:
        tags.append(cid)
        if key:  # thay mat
            desc = CAST[cid]["lock"]
            role = ("LEFT, calm" if cid == "M1" else "RIGHT, uneasy") if len(ids) > 1 else ""
            lead = f"the SAME RECURRING CHARACTER {cid}" + (f" ({role})" if role else "")
            if first_of.get(cid) == name:
                bits.append(f"CAST LOCK - {lead}, this image is the master reference "
                            f"for him/her: {desc}")
            else:
                bits.append(f"CAST LOCK - {lead}, exactly the same person as in the "
                            f"reference image, same face and hair: {desc}")
        else:  # chi ban tay
            bits.append(f"CAST LOCK - hands belong to RECURRING CHARACTER {cid}: "
                        f"{HANDS[cid]}")
    props = PROP_OF.get(name, [])
    for j, p in enumerate(props):
        txt = PROP[p]
        if j:  # prop thu 2 tro di: bo cum "the SAME ... every time:" cho gon
            txt = re.sub(r"^the SAME [^:]+: ", "", txt)
            bits.append(f"and {txt}")
        else:
            bits.append(f"PROP LOCK - {txt}")
    # dau cau giua cac khoi LOCK — thieu thi model doc thanh mot cau chay dai
    return " ".join(b if b.endswith(".") else b + "." for b in bits), tags, props


def build():
    doc = json.load(io.open(BEATS, encoding="utf-8"))
    beats = doc["beats"]

    # shot dau tien cua tung cast (theo timeline) = ANCHOR
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
        bg = BG.get(b.get("bg", ""), b.get("bg", ""))
        for k, shot in enumerate(shots):
            n += 1
            nm = shot.get("src_card", "").replace("card_19_", "")
            scene = re.split(r"\s*Any person shown is JAPANESE", shot["scene"])[0].strip()
            # beats.json co cho lot chu CJK vao scene tieng Anh ("a tidy研究 desk").
            # De nguyen thi model gen ANH co the VE chu do len anh => pha luat "no text".
            scene = re.sub("[　-鿿]+", " study ", scene)
            scene = re.sub(r"\s{2,}", " ", scene).strip()
            cont, tags, props = cast_block(nm, first_of)
            has_person = bool(CAST_OF.get(nm) or HANDS_OF.get(nm))

            parts = [IMG_STYLE.format(bg=bg), IMG_FRAME,
                     f"SCENE (as layered paper cut-outs): {scene}."]
            if cont:
                parts.append(cont)
            if has_person:
                parts.append(IMG_JP)
            parts.append(IMG_TAIL)
            img.append(re.sub(r"\s+", " ", " ".join(parts)).strip())

            # MOTION lay tu _motion19.py (viet theo LOI DOC tai dung giay do),
            # KHONG lay `element_motion` cua beats.json nua - xem docstring _motion19.
            mv = MOT.get(nm)
            assert mv, f"thieu motion cho shot {nm} trong tools/_motion19.py"
            chain = V_OPEN if (k == 0 or len(shots) == 1) else (
                V_CLOSE if k == len(shots) - 1 else V_MID)
            vid.append(re.sub(r"\s+", " ", " ".join(
                [VID_HEAD, f"MOTION: {mv['m']}.", CAM[mv["cam"]], AMP[mv["lv"]],
                 chain, VID_TAIL])).strip())
            lvs.append(mv["lv"])

            anchor = [c for c in tags if first_of.get(c) == nm]
            ref = [c for c in tags if first_of.get(c) != nm]
            note = ("ANCHOR " + "+".join(anchor)) if anchor else ""
            if ref:
                note = (note + " | khop " + "+".join(
                    f"{c}->#{order.index(first_of[c]) + 1}" for c in ref)).strip(" |")
            rows.append((n, b["id"], b.get("title_cn", ""), nm,
                         shot.get("shot_size", ""), mv["lv"].upper(),
                         note or "-", "+".join(props) if props else "-",
                         "OPEN" if chain is V_OPEN else
                         ("CLOSE" if chain is V_CLOSE else "mid")))
            blocks.append((n, b["id"], b.get("title_cn", ""), nm, img[-1], vid[-1]))

    # -- xuat file ---------------------------------------------------------
    io.open(os.path.join(VD, "flow19_IMAGE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(img) + "\n")
    io.open(os.path.join(VD, "flow19_VIDEO.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(vid) + "\n")

    ten = ["# dong N  ->  ten anh  ->  ten clip     (thu tu = THOI GIAN trong video)", ""]
    for r in rows:
        ten.append(f"{r[0]:>3}  card19_{r[3]}.png".ljust(42) +
                   f"-> clip19_{r[3]}.mp4".ljust(34) + f"[beat {r[1]}]")
    io.open(os.path.join(VD, "flow19_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(ten) + "\n")

    md = ["# video 19 - 74 prompt ANH + 74 prompt ANIMATION (khuon vox-director)\n"]
    md.append(
        "> Thu tu = **THOI GIAN trong video** (`beats.json` cua "
        "`E:\\vox-director\\out\\nenkin-19`), khong theo thu tu file goc - vi\n"
        "> **lien mach chi doc duoc khi xep theo timeline**.\n>\n"
        "> **Quy trinh 2 buoc:**\n"
        "> 1. `flow19_IMAGE.txt` (74 dong) -> gen 74 poster tinh -> **DUYET MAT**\n"
        ">    (banner dinh khung co that TRONG? chu the co lap khung? co chu rac lot vao?)\n"
        "> 2. `flow19_VIDEO.txt` (74 dong) -> nap **anh so N** + **prompt dong N** -> clip N\n>\n"
        "> Ca hai file deu nhac **banner TRONG** va **no text anywhere** - file VIDEO\n"
        "> cung phai nhac, vi i2v rat hay tu ve chu vao mot dai giay trong.\n>\n"
        "> Chu Noto Sans JP dot len banner SAU (`tools/build_remotion_19.py`), khong de\n"
        "> AI gen kanji - kanji AI gen la nat net.\n")

    md.append("\n## 74 SHOT NAY PHU DUOC BAO NHIEU CUA VIDEO (do bang timeline THAT)\n")
    md.append(
        "Video 19 dai **899,1s = 15,0 phut** (`timeline.json`). `tools/_scenes19.py` chia\n"
        "**46 scene**, va chung KHONG cung loai:\n\n"
        "| loai scene | so scene | tong giay | can anh AI? |\n|---|---|---|---|\n"
        "| co ANH (`heroes=[...]`) | **33** | **604s** | co - 74 shot nay |\n"
        "| co BANG SO LIEU (`hero=None, stat=...`) | 13 | 296s (33%) | **khong** |\n\n"
        "**604s / 74 shot = 8,2s moi clip** -> vua dung sàn *doi anh chinh <=9,0s* cua\n"
        "`audience-45plus.md` §2.0b, va 8,2 doi/phut van duoi tran khi tinh ca doan bang.\n"
        "=> **Bo 74 nay DU cho phan co anh, khong can gen them anh nao.**\n\n"
        "⚠️ Con so `dur: 6` trong `beats.json` la **mac dinh truu tuong**, khong phai giay\n"
        "that (74x6 = 444s = chi nua video). Dung `_scenes19.py` + `timeline.json` de\n"
        "chia giay, dung tin `dur`.\n\n"
        "⚠️ Clip AI thuong ra 4-8s < 8,2s can dung => builder phai **giu frame cuoi** cho\n"
        "du giay (prompt da yeu cau motion `CLOSE` ve DUNG YEN truoc khi clip het, nen\n"
        "hold frame cuoi khong loi mat).\n\n"
        "🔴 **13 scene bang so lieu VAN NEN de Remotion ve chu** (`papercut-stat` /\n"
        "`papercut-formula`), dung gen anh AI: `media-library.md` §2.9 + `CLAUDE.md` §② -\n"
        "**so va kanji AI gen la nat net**, va so lieu la thu dat nhat cua kenh YMYL nay.\n"
        "Muon phu ca 899s bang anh thi can **~123 shot** (them ~49 anh) VA mat bang so.\n")

    md.append("\n## BO NAO LA BAN DUNG (folder co 3 bo prompt cu)\n")
    md.append(
        "| bo | la gi | dung khong |\n|---|---|---|\n"
        "| **`flow19_IMAGE.txt` + `flow19_VIDEO.txt`** | 74 anh + 74 animation, "
        "**co CAST/PROP LOCK** | **BAN DUNG** |\n"
        "| `flow_ch3_IMAGE/VIDEO.txt` | demo 9 shot chuong 3, chua co lop lien mach "
        "| da bi bo nay phu |\n"
        "| `flow_prompts_19_FLOW.txt` | 74 prompt **text-to-video 1 buoc** (khong qua "
        "anh) | duong lui neu khong muon gen anh |\n"
        "| `motion_prompts_19_FLOW.txt` | 74 prompt i2v cho **anh photocard da co** "
        "trong `photocard/` | dung khi animate lo anh CU |\n")

    md.append("\n## THU TU GEN - 5 ANCHOR TRUOC, roi moi den 69 shot con lai\n")
    md.append(
        "```\n" + "\n".join(
            f"#{order.index(first_of[c]) + 1:<3} {first_of[c]:<16} = ANCHOR {c}"
            f"   ({CAST[c]['who']})" for c in CAST) + "\n```\n\n"
        "Gen 5 dong nay TRUOC, duyet ky mat/toc/ao, **luu lai 5 anh do**, roi moi gen\n"
        "tiep - moi shot con lai cua cast nao thi nap anh anchor cua cast do lam\n"
        "reference.\n")

    md.append("\n## MOTION - viet theo LOI DOC, 3 hang nang luong\n")
    md.append(
        "Ban dau (2026-09-02 sang) motion lay nguyen tu `beats.json` va **khong he doc\n"
        "script** - user bat ngay: *\"mày có dựa theo script để tạo animation không thế.\n"
        "Sao tao thấy animation sinh ra tù thế\"*. So do cua ban do:\n\n"
        "| | ban cu | ban nay |\n|---|---|---|\n"
        "| nguon motion | `beats.json` (khong doc loi) | **`tools/_motion19.py`** - viet theo cau loi tai dung giay do |\n"
        "| `motion_style` | `calm` cho ca 74 shot | **25 peak · 30 mid · 19 calm** |\n"
        "| camera | 56/74 static | static / parallax / push 5% / push 10% theo hang |\n"
        "| bien do trong khuon | `Calm, restrained amplitude` o MOI shot | `AMPLITUDE:` theo hang, peak duoc **bay ra khoi khung** |\n"
        "| dong tu | 60/74 yeu (slides/settles/drifts) | peak dung TORN AWAY / SLAMS / SPLITS / TEARS |\n\n"
        "Vi du 3 scene dat nhat, dat canh loi:\n\n"
        "| loi | motion cu | motion moi |\n|---|---|---|\n"
        "| 「五年間で、およそ**八十四万円**」 | \"settles one notch, drifts a pixel or two\" | ca mang tien bi **XE RUT** bay ra khoi khung, chong con lai thap han |\n"
        "| 「**一円も、出ません**」 | \"palm closes halfway and opens again\" | ban tay ngua ra **CHO** va khong co gi den, phong bi rong truot khoi ban |\n"
        "| 「**戻りません**」 | \"pushed a few degrees, catches\" | day cua quay di qua duoc, keo NGUOC lai thi **dap vao khoa, khong nhuc nhich** |\n\n"
        "🔴 **Vi sao ban cu bao thu - de khong ai 'sua lai cho an toan':** `audience-45plus.md`\n"
        "§2 bat nhip dung cham cho tep 45+, nhung no noi ve **NHIP CAT** (<=6 doi hinh/phut),\n"
        "KHONG noi ve **BIEN DO CHUYEN DONG TRONG MOT SHOT**. Dung cai loi ma §2.0 cua chinh\n"
        "rule do da ghi: *gate co TRAN ma khong co SAN*. Mot shot co the dong manh ma van\n"
        "khong cat nhanh. Va `E:\\vox-director\\SKILL.md` noi thang: *element_motion la cho\n"
        "**NANG LUONG SONG**, make it RICH, be bold*; camera bold la *available, NOT banned*.\n\n"
        "⚖️ **19 shot `calm` la CO Y, dung nang chung len:** gioi thieu 松本 + 社章 · khoi\n"
        "dinh chinh 「ここは正確に」 · CTA · disclaimer · 次回予告. Nhan het thi khong con gi\n"
        "de nhan - va tep 45+ can cho nghi giua cac cu don.\n")

    md.append("\n## LIEN MACH - doc truoc khi gen anh\n")
    md.append(
        "Gen 74 prompt doc lap thi ra **74 ong gia khac nhau**. Ba tang chong viec do:\n\n"
        "**(1) CAST LOCK - 6 nhan vat lap lai.** Moi prompt anh co nguoi da mang san mot\n"
        "cau mo ta CHOT CUNG. Shot dau tien cua moi cast la **ANCHOR** - gen no TRUOC,\n"
        "duyet ky, roi moi gen cac shot con lai cua cast do va **nap anh ANCHOR lam\n"
        "reference** (Flow: *Ingredients*; Nano Banana: dan anh vao khung chat). Khong\n"
        "nap reference thi cau chu chi giup ~70%, mat van troi.\n\n"
        "**Cho quan trong nhat la beat 18 `futari`** - do la CALLBACK cold open\n"
        "(\u300c\u5192\u982d\u306e\u3001\u3075\u305f\u308a\u306e\u7537\u6027\u3002"
        "\u3042\u308c\u304c\u3001\u3053\u306e\u304a\u3075\u305f\u308a\u3067\u3059\u300d).\n"
        "Hai ong o day PHAI dung la **M1 \u677e\u672c** (beat 1/9/11, ben TRAI, binh than)\n"
        "va **M2 \u540c\u50da** (beat 16/17, ben PHAI, kho tam). Neu hai ong nay khong\n"
        "giong hai ong da xuat hien truoc do thi cu callback - diem cao trao cua bai -\n"
        "**mat sach nghia**.\n\n"
        "**(2) PROP LOCK - 14 vat/bo canh lap lai** (phong bi nau, phieu luong, lich\n"
        "tuong, chong xu + thuoc ke, ban \u7814\u7a76, kho hang, phong nghi...). Cung mot\n"
        "vat o 3 shot khac nhau phai cung hinh dang, neu khong nguoi xem doc thanh 3 vat\n"
        "khac nhau.\n\n"
        "**(3) MOTION CHAIN - trong file VIDEO.** Moi beat co 1-4 shot ke tiep nhau;\n"
        "prompt da danh dau `OPEN` / `mid` / `CLOSE`:\n"
        "- `OPEN` - bat dau tu dung the trong anh, khong dan lai canh.\n"
        "- `mid` - **giu nguyen huong chuyen dong** cua shot truoc, cam dao chieu.\n"
        "- `CLOSE` - chuyen dong phai **ve DUNG YEN** truoc khi clip het, de cat sang\n"
        "  beat sau khong giat.\n\n"
        "**Neu tool cua may co 'last frame -> first frame'** (Flow co) thi dung cho cac\n"
        "cap `mid`/`CLOSE` trong cung beat: lay frame cuoi clip truoc lam frame dau clip\n"
        "sau => lien mach tuyet doi, khong con phu thuoc cau chu.\n")

    md.append("\n## Bang CAST (5 nhan vat/nhom)\n")
    md.append("| id | la ai | ANCHOR | mo ta chot cung |")
    md.append("|---|---|---|---|")
    for cid, v in CAST.items():
        a = first_of.get(cid, "-")
        ai = order.index(a) + 1 if a in order else "-"
        md.append(f"| **{cid}** | {v['who']} | #{ai} `{a}` | {v['lock']} |")
    md.append("\n`M1+M2` = shot co CA HAI ong (beat 18) - nap CA HAI anh anchor lam reference.\n")

    md.append("\n## Bang 74 shot (thu tu gen = thu tu nay)\n")
    md.append("| # | beat | headline beat | ten shot | co | NANG LUONG | cast | prop | chain |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | `{r[3]}` | {r[4]} | {r[5]} | "
                  f"{r[6]} | {r[7]} | {r[8]} |")

    md.append("\n---\n\n## 74 cap prompt\n")
    for (i, bid, title, nm, a, v) in blocks:
        md.append(f"\n### {i}. `{nm}`  - beat {bid} {title}\n")
        md.append(f"**ANH** *({len(a)} ky)*\n\n```\n{a}\n```\n")
        md.append(f"**VIDEO** *({len(v)} ky)*\n\n```\n{v}\n```\n")

    io.open(os.path.join(VD, "flow19_BLOCKS.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(md) + "\n")

    print(f"OK {n} shot / {len(beats)} beat")
    print(f"   ANH   : flow19_IMAGE.txt   {min(map(len, img))}-{max(map(len, img))} ky")
    print(f"   VIDEO : flow19_VIDEO.txt   {min(map(len, vid))}-{max(map(len, vid))} ky")
    print(f"   doc   : flow19_BLOCKS.md   |  map: flow19_TENFILE.txt")
    print(f"   -> {VD}")

    # gate: moi shot co nguoi phai co CAST LOCK, moi cast phai co anchor
    miss = [nm for i, nm in enumerate(order)
            if (CAST_OF.get(nm) or HANDS_OF.get(nm)) and "CAST LOCK" not in img[i]]
    assert not miss, f"thieu CAST LOCK: {miss}"
    for cid in CAST:
        assert cid in first_of, f"cast {cid} khong co anchor"
    naked = [nm for i, nm in enumerate(order)
             if "CAST LOCK" not in img[i] and "PROP LOCK" not in img[i]]
    if naked:
        print("   CHU Y: shot khong co lop LOCK nao (canh chi xuat hien 1 lan, "
              f"khong can khop): {', '.join(naked)}")
    import collections as _c
    print("   MOTION: " + " · ".join(f"{k} {v}" for k, v in
          sorted(_c.Counter(lvs).items(), key=lambda x: -x[1])) +
          "  (truoc: calm 74/74)")
    npers = sum(1 for nm in order if CAST_OF.get(nm) or HANDS_OF.get(nm))
    nprop = sum(1 for nm in order if PROP_OF.get(nm))
    print(f"   GATE  : cast anchor {len(first_of)}/{len(CAST)} OK | "
          f"{npers}/74 shot co nguoi | {nprop}/74 shot co prop lock")
    return n


if __name__ == "__main__":
    got = build()
    assert got == 74, f"phai 74 shot, dang co {got}"
