# -*- coding: utf-8 -*-
"""Video 38 chouhen — 鉛筆の名簿 · 289 ANH TINH, phong cach MANGA MAU.

Ban ANH cua `gen_prompts_38.py` (ban VIDEO). Dung CHUNG du lieu canh (_s38_a/a2/b/c),
chung boi canh P, chung dan dien C, chung lop nguoi nen — chi doi BA thu:

  ① STYLE  : phim truyen hinh  ->  MANGA MAU (seinen drama, ink + cel shading)
  ② MOTION : "chuyen dong deu tu frame dau toi frame cuoi" -> MOT KHOANH KHAC DONG CUNG
  ③ ACT    : 3 beat noi bang ", then" -> MOT beat (xem `_s38_still.to_still`)

🔴 BA CAI BAY DA BIET TRUOC, da va san:

 (a) `AVOID` cua thu vien CAM THANG "anime style" — de nguyen thi prompt vua xin manga
     vua cam manga. Cung benh "cau CAM chong lai MUC DICH" da dinh o cast plate va o
     STYLE_MODERN. => AVOID_MANGA viet lai tu dau, KHONG ke thua.

 (b) Manga la moi truong co CHU: model rat thich them bong thoai, chu tuong thanh
     (オノマトペ), khung tranh, so trang. GUARD cu chi cam chu tren DO VAT. => GUARD moi
     cam ca bong thoai / chu tuong thanh / vien khung / trang truyen nhieu o.
     Vi tri guard giu nguyen DAU prompt (ai-video-regen.md §2: <=15%).

 (c) `--ar 16:9` DA DO DUOC LA BI BO QUA o tool gen ANH (media-library.md §2.10 ①:
     xin 16:10 / 5:4 / 16:9 -> 18/18 anh van ra 1376x768). Van de `--ar` vi vo hai,
     nhung thu THAT SU ganh ti le la CAU CHU trong STYLE => STYLE_MANGA noi ti le
     bang chu, hai lan.

⚖️ NHIP: 289 anh / 2.274 giay = 7,9 giay mot anh = 7,6 doi hinh/phut. Tren tran 6,0 cua
   `audience-45plus.md` §2 muc 1, nam trong NGOAI LE da do duoc cua ngach (co-dai 7,43-7,53).
   Anh TINH, KHONG pan/zoom (feedback_video_no_motion_mot_giong).
"""
import sys, os, re
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-chouhen\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import videogen_lib as V
from videogen_lib import build, write_outputs, autochain
from _s38_a import SA
from _s38_a2 import INS_A
from _s38_b import SB
from _s38_c import SC, P_EXTRA, CROWD_EXTRA
from _s38_still import to_still

# ════════════════════════════════════════════════════════════════════════════
# ① STYLE — MANGA MAU (user chot 2026-09-17: "truyen ke nhu phong cach manga,
#    phong cach mau manga")
# ════════════════════════════════════════════════════════════════════════════
# Mo ta MOT TRANG VE, khong mo ta mot cai may quay. Ba thu giu cho no ra "manga"
# chu khong ra "anime wallpaper": ① net muc co do day thay doi ② to phang 2-3 tong
# mot mat phang (cel), khong chuyen sac muot ③ nen ve tay co phoi canh kien truc.
STYLE_MANGA = (
 "a single full-colour panel from a modern Japanese seinen drama manga, drawn and "
 "painted by hand, "
 "confident black ink linework with varied line weight, heavier on the contours and "
 "finer inside, "
 "flat cel colouring in two or three tones on each surface with hard-edged shadows, "
 "no airbrushed gradients, "
 "a restrained muted palette of slate blue, cold grey, dull ochre and off-white with "
 "one quiet warm accent, "
 "screentone hatching kept only in the deepest shadows, "
 "the background drawn properly with ruled architectural perspective and a light "
 "watercolour wash, "
 "grown-up realistic adult proportions and plain ordinary Japanese faces, "
 "strong directional light coming from a source you can see inside the frame, "
 "dramatic composition with the subject placed off-centre and real empty space left "
 "around it, "
 "ONE single uninterrupted illustration that fills the whole picture edge to edge, "
 "horizontal landscape artwork in 16:9 aspect ratio, 1920x1080 widescreen, clearly "
 "wider than it is tall, not vertical and not square")

# ② MOTION -> KHOANH KHAC DONG CUNG. Thay MOI hang so MOTION_* cua thu vien, vi
#    build() chon mot trong nhieu ban theo framing.
STILL = (
 "one single frozen instant held completely motionless, everything in the picture is "
 "stopped exactly where it is, "
 "no before and no after and no sequence, the whole of the story is in this one held "
 "moment, "
 "a still drawing, not a film and not a sequence of pictures")

# ③ AVOID — VIET LAI TU DAU (khong ke thua ban video: ban do cam "anime style").
AVOID_MANGA = (
 "Avoid: any letters, words, numbers, kanji, kana or logos anywhere in the picture, "
 "speech balloons, speech bubbles, dialogue text, captions, subtitles, "
 "sound-effect lettering, onomatopoeia, "
 "panel borders, frames, gutters, a multi-panel comic page, page numbers, signature, "
 "watermark, "
 "chibi or super-deformed proportions, moe or idol character design, huge glossy eyes "
 "with heavy highlights, "
 "3D CG render, photorealism, a photograph, oil painting, rough sketch, unfinished "
 "line art, "
 "western faces, oversaturated neon colours, HDR look, extreme close-up of a face, "
 "extra fingers, floating limbs, disembodied hands, melted or duplicated faces, "
 "motion blur, speed lines, a strip of several images")
AVOID_MANGA_POV = (AVOID_MANGA +
 ", no third-person shot, no view from outside the person whose eyes this is, their "
 "own face and their own back are never visible, no mirror, no reflection showing "
 "their face")

V.STYLE = V.STYLE_MODERN = STYLE_MANGA
V.AVOID = V.AVOID_MODERN = AVOID_MANGA
V.AVOID_POV = V.AVOID_MODERN_POV = AVOID_MANGA_POV
for _m in ("MOTION", "MOTION_EXIT", "MOTION_MOVE", "MOTION_POV", "MOTION_POV_STEP",
           "MOTION_POV_WALK", "MOTION_POV_LOOK", "MOTION_POV_LOOK_WALK", "MOTION_POV_BIKE"):
    setattr(V, _m, STILL)
PROF = {"STYLE": STYLE_MANGA, "AVOID": AVOID_MANGA}

# 🔴 FRAMINGS cua thu vien mo ta MAY QUAY dang chay — voi anh tinh thi cac cum
#    "one single continuous move", "the view carrying forward and turning left and
#    right" tu no chong lai khoi STILL. Sua tai cho, KHONG viet lai ca bang.
_FIX_FRAMING = [
 (r"static ", ""),
 (r"slow horizontal camera pan at chest height, one single continuous move, "
  r"the whole figure in frame by the end of the move",
  "a wide view at chest height, the whole figure in frame"),
 (r"slow camera tilt at chest height, one single continuous move, "
  r"the whole figure in frame by the end of the move",
  "a view at chest height looking slightly up, the whole figure in frame"),
 (r", the view carrying forward and turning left and right the way their head turns", ""),
 (r"first-person walking point of view", "first-person point of view mid-stride"),
 (r"\bshot\b", "view"),
 (r"\bfilmed\b", "drawn"),
]
for _k, _v in list(V.FRAMINGS.items()):
    for _a, _b in _FIX_FRAMING:
        _v = re.sub(_a, _b, _v)
    V.FRAMINGS[_k] = _v.strip().strip(",")
V.POV_BODY["pov_look"] = (
 "nothing of their own body appears in the picture at all, not a hand, not an arm, not "
 "a shoulder, not a knee and not a foot, so the frame holds only what is in front of "
 "their eyes")

# ── boi canh + dan dien: GIU Y NGUYEN ban video ────────────────────────────────
P = {
 "taiikukan": "the main hall of a Japanese primary school gymnasium at night in a typhoon, used as an evacuation shelter, a varnished wooden floor covered with blue plastic sheets laid in rows, folded grey blankets and cardboard boxes of supplies, families sitting and lying on the sheets, fluorescent strip lights in the high ceiling, tall windows up near the roof with rain running down them, wall bars along one side",
 "uketsuke": "a reception table set up just inside the door of the gymnasium shelter, two long school tables pushed together, a cardboard box of folded blankets, a black corded telephone, a folding chair, a clipboard and an open ruled ledger lying flat, fluorescent light overhead",
 "rouka":    "the covered walkway joining the gymnasium to the school building at night, a double door with a gap under it, a narrow strip of blue plastic sheet on the boards against the wall, rain blowing past outside, a single fluorescent tube overhead",
 "sumi":     "the far corner of the gymnasium shelter, quieter and dimmer than the middle, an elderly place made up with folded blankets, a small wheeled oxygen cylinder and a squat oxygen concentrator beside it, a plug socket low on the wall",
 "souko":    "the door of the gymnasium equipment store at night, a heavy sliding steel door with a padlock through the hasp, vaulting horses and rolled mats visible through the gap, a distribution board on the wall beside it",
 "shokuin":  "a Japanese primary school staff room at night, rows of desks with papers stacked on them, a laptop and a projector on a trolley, a wall of lockers, one fluorescent tube left on",
 "soto":     "the concrete apron outside the gymnasium doors at night in heavy rain, a light over the door, a small truck parked with its tailgate down, puddles moving in the wind",
 "asa":      "the main hall of the gymnasium in the early morning after the storm, the same blue plastic sheets and blankets on the floor, both front doors standing wide open, low morning sun coming straight in across the boards, people sitting up and folding bedding",
 "supa":     "the car park of a suburban Japanese supermarket on a grey winter afternoon, parked cars, a line of trolleys, a low shopfront with plain awnings",
 "haru":     "the same gymnasium in spring in daylight, doors open on a green schoolyard, trestle tables set out for a disaster drill, folded blankets stacked in boxes, no storm and no bedding on the floor",
}
P.update(P_EXTRA)

C = {
 "chizuru":          "an older woman in a plain dark grey zip-up jacket and dark trousers, a small cloth shoulder bag",
 "chizuru_pov":      "their own forearms in plain dark grey jacket sleeves and the dark grey jacket on their own chest",
 "chizuru_pov_sit":  "their own forearms in plain dark grey jacket sleeves, and their own knees and the edge of a blue plastic sheet across the bottom of the picture",
 "chizuru_pov_stand":"their own forearms in plain dark grey jacket sleeves and the dark grey jacket on their own chest",
 "chizuru_pov_hand": "their own forearms in plain dark grey jacket sleeves and the backs of their own hands",
 "chizuru_pov_walk": "only their own hand or hands where the work needs them, plain dark grey jacket cuffs at the edge",
 "setsuko":          "a woman in a navy blue windbreaker with a yellow armband on one sleeve and a small handmade name card on a cord round her neck",
 "ichinose":         "a very old man in a brown knitted cardigan with a blanket over his knees, a thin clear tube running to his face",
 "mago":      "a young man in a dark grey hooded sweatshirt with the hood down",
 "gyosha":    "a man in a dark blue waterproof work jacket with a towel round his neck",
 "kaicho":    "a heavy-set man in a soaked beige zip jacket",
 "shokuin":   "a man in an olive green city waterproof jacket carrying a clipboard",
 "shitsucho": "a man in a charcoal suit and a plain dark tie",
 "shonin":    "a young woman in a pale grey hooded fleece",
 "kyoto":     "a middle-aged man in a dark school tracksuit top with a lanyard round his neck",
 "haha":      "a young woman in a dusty pink long-sleeved top",
}
V.MAX_CAST_IN_VIDEO = 11

CROWD = {
 "taiikukan": "full", "uketsuke": "full", "asa": "full",
 "sumi": "few", "rouka": ("solo", "hanh lang — cho bi day ra, VANG chinh la noi dung"),
 "souko": ("solo", "cua kho khoa — khong ai o day, do la y"),
 "shokuin": ("solo", "phong giao vien ban dem"),
 "soto": "few", "supa": "few", "haru": "few",
}
CROWD.update(CROWD_EXTRA)

# ── ghep S ────────────────────────────────────────────────────────────────────
S = list(SA)
for after_id, scene in INS_A:
    idx = next(i for i, r in enumerate(S) if r[0] == after_id)
    S.insert(idx + 1, scene)
S += SB
S += SC

# ── ti le POV 30% (giu nguyen lap luan cua ban video) ─────────────────────────
_POV_MOVE = re.compile(r"the view (carries|turns|moves|comes down|holds|dips|rises|follows)"
                       r"|the whole view", re.I)
_POV_OWN  = re.compile(r"their own", re.I)
def _to_third(act):
    a = re.sub(r"^A_[A-Z]+:\s*", "", act)
    return (a.replace("fills the bottom of the view", "fills the foreground of the frame")
             .replace("fills the top of the view", "fills the top of the frame")
             .replace("fills the middle of the view", "fills the middle of the frame")
             .replace("fills the view", "fills the frame")
             .replace("in the bottom of the view", "in the foreground")
             .replace("in the middle of the view", "in the middle of the frame")
             .replace("ahead of the view", "ahead")
             .replace("at the far end of the view", "at the far end of the frame")
             .replace("towards the camera side", "towards the camera")
             .replace("the camera side", "the near side"))
_HAS_PERSON = re.compile(r"A_[A-Z]+|man|woman|figure|people|famil|grandson|"
                         r"teacher|officer|neighbour|shopper|queue|mother", re.I)
_pov_idx = [i for i, r in enumerate(S) if str(r[4]).startswith("pov")]
_keep = {i for i in _pov_idx if _POV_OWN.search(S[i][2]) or _POV_MOVE.search(S[i][2])}
_n_keep = round(len(S) * 0.30)
if len(_keep) > _n_keep:
    _mv = [i for i in sorted(_keep) if not _POV_OWN.search(S[i][2])]
    for i in _mv[: len(_keep) - _n_keep]:
        _keep.discard(i)
elif len(_keep) < _n_keep:
    _rest = [i for i in _pov_idx if i not in _keep]
    _need = _n_keep - len(_keep)
    if _rest and _need > 0:
        step = max(1, len(_rest) // _need)
        for i in _rest[::step][:_need]:
            _keep.add(i)
# 🔴 khac ban video: canh lia may KHONG duoc doi thanh 'pan' — anh tinh khong lia duoc.
_cycle = ["medium", "ots", "low", "behind", "medium", "high", "ots", "medium"]
_k = 0
for i in _pov_idx:
    if i in _keep:
        continue
    r = list(S[i])
    r[2] = _to_third(r[2])
    cand = _cycle if _HAS_PERSON.search(r[2]) else [c for c in _cycle if c not in ("ots", "behind")]
    r[4] = cand[_k % len(cand)]; _k += 1
    S[i] = tuple(r)
print("POV sau khi ha: %d/%d = %.0f%%" % (len(_keep), len(S), len(_keep) * 100 / len(S)))

CUT = set()
S = autochain(S, cut=CUT)

# ── ③ ACT: 3 beat -> MOT khoanh khac ──────────────────────────────────────────
n_b2 = 0
_S2 = []
for r in S:
    lr = list(r)
    lr[2], used = to_still(r[2])
    n_b2 += used
    _S2.append(tuple(lr))
S = _S2
print("act -> anh tinh: %d canh (trong do %d canh lia may lay diem DUNG lam khung)"
      % (len(S), n_b2))

# ⭐ CAST PLATE PHAI LA MANGA, KHONG DUNG LAI PLATE CUA BAN VIDEO.
#    Plate cu (`cast_chizuru.png`) la anh NGUOI THAT theo mau phim. Dua no lam anh tham
#    chieu cho mot prompt xin manga = hai nguon mau thuan, dung cai benh "cau CAM chong
#    lai MUC DICH" da dinh 3 lan trong project nay. => ten file RIENG, gen lai.
PLATES = {"chizuru": "cast_manga_chizuru.png",
          "setsuko": "cast_manga_setsuko.png",
          "ichinose": "cast_manga_ichinose.png"}
rows = build(S, P, C, prof=PROF, plates=PLATES, crowd=CROWD)

# ── GUARD CHU: dau prompt (<=15%), ban MANGA ──────────────────────────────────
GUARD = ("NO WRITING AND NO COMIC FURNITURE ANYWHERE IN THIS PICTURE: every page, form, "
         "card, label, sign and screen is blank — ruled lines and empty boxes only, no "
         "letters, no numbers, no handwriting, no printed text, in any language; and no "
         "speech balloons, no sound-effect lettering, no panel borders and no page "
         "layout — this is ONE single picture, not a comic page. ")
rows = [(r[0], r[1], r[2], r[3], r[4], GUARD + r[5]) for r in rows]

# ── GATE MAY ──────────────────────────────────────────────────────────────────
_g = [x[5].find("NO WRITING") * 100 // len(x[5]) for x in rows]
print("guard chu @ %d%%-%d%% prompt (luat ai-video-regen §2: <=15%%)" % (min(_g), max(_g)))

_BAD = re.compile(r"\banime style\b|\bfirst frame\b|\bfrom first frame to last\b|"
                  r"\bcontinuous single take\b|\bno cuts\b|\bone even speed\b|"
                  r"\bcontinuous move\b|\bfast cuts\b|\breversing motion\b|"
                  r"\bmorphing objects\b|\bthe camera holds one position\b|\b, then \b", re.I)
_hit = [(x[0], _BAD.search(x[5]).group(0)) for x in rows if _BAD.search(x[5])]
print("tan du ngon ngu VIDEO trong prompt: %d %s" % (len(_hit), _hit[:6]))

_NOMANGA = [x[0] for x in rows if "seinen drama manga" not in x[5]]
print("prompt THIEU khoi manga: %d %s" % (len(_NOMANGA), _NOMANGA[:6]))
print("do dai prompt: %d-%d ky (trung vi %d)"
      % (min(len(x[5]) for x in rows), max(len(x[5]) for x in rows),
         sorted(len(x[5]) for x in rows)[len(rows) // 2]))
print("SO ANH: %d  |  bai 2.274s  ->  %.1f giay / anh  =  %.1f doi hinh/phut"
      % (len(rows), 2274 / len(rows), len(rows) / (2274 / 60)))

OUTDIR = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"


def write_img_outputs(rows, outdir, prefix="imggen"):
    """Nhu write_outputs cua lib, nhung ten file la .png (khong phai .mp4)."""
    import io
    os.makedirs(outdir, exist_ok=True)
    with io.open(os.path.join(outdir, prefix + "_FLOW.txt"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(" ".join(r[5].split()) + "\n")
    with io.open(os.path.join(outdir, prefix + "_TENFILE.txt"), "w", encoding="utf-8") as f:
        f.write("# dong FLOW.txt  ->  ten file ANH  (thu tu PHAI khop)\n")
        for i, r in enumerate(rows, 1):
            f.write("%3d  img_%s_%s_%s.png   [%s]\n" % (i, r[0], r[1].lower(), r[2], r[3]))
    # 🔴 BLOCKS.md: ACT phai lay tu S, KHONG cat chuoi tu prompt. Cach cat cu
    #    (`r[5].split(", " + r[4])`) im lang tra ve CA prompt khi framing da bi sua
    #    -> file "nguoi doc" thanh ban sao FLOW, tuc mat luon cho de soi.
    acts = {r[0]: r[2] for r in S}
    with io.open(os.path.join(outdir, prefix + "_BLOCKS.md"), "w", encoding="utf-8") as f:
        f.write("# imggen 38 — ban nguoi doc (MANGA MAU · anh tinh)\n\n"
                "Ba khoi duoi day DAN NGUYEN VAN vao moi prompt; phan rieng cua tung "
                "anh chi la ACT + FRAMING + BOI CANH.\n\n")
        f.write("**STYLE:** " + STYLE_MANGA + "\n\n**STILL:** " + STILL +
                "\n\n**AVOID:** " + AVOID_MANGA + "\n\n---\n\n")
        for i, r in enumerate(rows, 1):
            f.write("## %d. %s [%s · %s · %s]\n\n- **ACT:** %s\n- **FRAMING:** %s\n\n"
                    % (i, r[0], r[1], r[2], r[3], acts.get(r[0], "?"), r[4]))
    print("da ghi %s_FLOW.txt (%d dong) · %s_TENFILE.txt · %s_BLOCKS.md"
          % (prefix, len(rows), prefix, prefix))


def write_manga_plates(outdir):
    """3 anh tham chieu nhan vat, VE THEO MANGA (khong phai anh chup)."""
    import io
    lines, names = [], []
    for tok, path in PLATES.items():
        p = ("full-body character reference sheet of " + C[tok] + ", drawn as a single "
             "full-colour manga character design, standing still and relaxed, "
             "three-quarter view turned slightly towards the viewer, arms at the sides, "
             "the whole figure from head to shoes inside the frame with a little space "
             "above the head, "
             "a plain flat pale grey background with nothing on it, no props, no "
             "furniture, no scenery, "
             "even flat light with no harsh shadows so every detail of the clothing reads, "
             + STYLE_MANGA + ". " + AVOID_MANGA + ", no turnaround sheet, no multiple "
             "views of the same character, no colour swatches, no annotations. --ar 16:9")
        lines.append(" ".join(p.split()))
        names.append("%3d  %s   (A_%s)" % (len(names) + 1, path, tok.upper()))
    io.open(os.path.join(outdir, "cast_plates_manga_FLOW.txt"), "w",
            encoding="utf-8").write("\n".join(lines) + "\n")
    io.open(os.path.join(outdir, "cast_plates_manga_TENFILE.txt"), "w",
            encoding="utf-8").write("# dong FLOW.txt -> ten file anh (thu tu PHAI khop)\n"
                                    + "\n".join(names) + "\n")
    print("da ghi cast_plates_manga_FLOW.txt (%d dong) · _TENFILE.txt" % len(lines))


# ── BAN GON: prompt 3.064 ky nam NGOAI vung da do (~1.700 ky, ab-3title-3thumb §3.1) ──
# ⛔ KHONG bop ban chinh: moi cau trong AVOID_MANGA deu bit mot loi cu the (bong thoai,
#    khung tranh, chibi, anh chup). Xuat them MOT ban gon de neu gen T1 ra nat thi co
#    cai doi chung ngay, thay vi doan xem dai co phai nguyen nhan khong.
LEAN_STYLE = (
 "a single full-colour panel from a modern Japanese seinen drama manga, hand-drawn, "
 "black ink linework with varied weight, flat cel colouring with hard-edged shadows, "
 "a muted slate blue and cold grey palette with one warm accent, "
 "background drawn in ruled architectural perspective, realistic adult proportions, "
 "strong directional light from a source inside the frame, subject off-centre, "
 "horizontal landscape artwork in 16:9, 1920x1080, clearly wider than tall")
LEAN_STILL = "one frozen instant, everything stopped exactly where it is, a still drawing"
LEAN_AVOID = ("Avoid: any letters, words, numbers or logos, speech balloons, sound-effect "
              "lettering, panel borders, a multi-panel comic page, watermark, chibi or moe "
              "character design, 3D CG render, photorealism, extra fingers, motion blur")


def lean(p):
    p = p.replace(STYLE_MANGA, LEAN_STYLE).replace(STILL, LEAN_STILL)
    i = p.find("Avoid:")
    tail = p[i:]
    extra = ""
    for cue in ("no third-person shot", "no lap, no knees", "no legs, no knees",
                "no hands, no arms"):
        j = tail.find(cue)
        if j > 0:
            extra = ", " + tail[j:].rstrip()
            break
    return p[:i] + LEAN_AVOID + (extra if extra else " --ar 16:9\n"[:0] + ". --ar 16:9")


if _hit or _NOMANGA:
    print("\n[CHAN] con loi — KHONG xuat file.")
else:
    import io as _io
    _lean = [" ".join(lean(r[5]).split()) for r in rows]
    _io.open(os.path.join(OUTDIR, "imggen_LEAN_FLOW.txt"), "w",
             encoding="utf-8").write("\n".join(_lean) + "\n")
    print("ban GON: %d-%d ky (trung vi %d) -> imggen_LEAN_FLOW.txt"
          % (min(len(x) for x in _lean), max(len(x) for x in _lean),
             sorted(len(x) for x in _lean)[len(_lean) // 2]))
    write_img_outputs(rows, OUTDIR)
    write_manga_plates(OUTDIR)
    print("\nXUAT -> %s" % OUTDIR)
    print("  THU TU GEN: cast_plates_manga_FLOW.txt (3 anh) TRUOC, roi imggen_FLOW.txt (289 anh)")
