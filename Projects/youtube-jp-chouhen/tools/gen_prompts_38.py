# -*- coding: utf-8 -*-
"""Video 38 chouhen — 鉛筆の名簿 · 284 CLIP. Dung CONG THUC v2 cua showa (videogen_lib).

NGAN SACH: bai dai 2.274s, clip 8s chay TRON => 284 clip = 7,5 doi hinh/phut.
  · 7,0s chan  -> 325 clip, nhung phai XEN moi clip 8s (mat 1s/clip, khong duoc gi)
  · 8,0s tron  -> 284 clip, 7,5 doi/phut  ⭐ CHON
  · tran rule audience-45plus §2 la 6,0/phut; 7,5 nam trong NGOAI LE da do duoc
    (co-dai, kenh thang ngach 2,35M view: 7,43-7,53 cat/phut).

⛔ KHONG chep hang so. STYLE / MOTION / AVOID / FRAMING / EXTRAS lay tu videogen_lib.
🔴 TOOL LA CUA SHOWA — STYLE mac dinh la 1970s. Bai nay HIEN DAI => phai truyen prof
   cho CA `build` LAN `gate`, neu khong ca 284 prompt ra phong the duc thap nien 1970
   (da dinh that, bat duoc bang `grep -c 1970s` tren file da xuat).

BA CACH GIU "NHAN VAT DONG NHAT":
 1. ⭐ POV cho A_CHIZURU — khong bao gio thay mat ba => khong bao gio lech.
 2. ⭐ Dung 3 nhan vat co ten (tran MAX_CAST_IN_VIDEO); A_SETSUKO / A_ICHINOSE
    uu tien behind/ots/high.
 3. ⭐ CAST PLATE: 3 anh tham chieu (tools/gen_plates_38.py) — ANH giu HINH DANG,
    CHU giu HANH DONG, nen act KHONG ta lai quan ao.
"""
import sys, os, re
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-showa\tools")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-chouhen\tools")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import videogen_lib as V
from videogen_lib import build, gate, write_outputs, autochain, linkage
from _s38_a import SA
from _s38_a2 import INS_A
from _s38_b import SB
from _s38_c import SC, P_EXTRA, CROWD_EXTRA

# ════════════════════════════════════════════════════════════════════════════
# ⭐ MAU PHIM (user chot): "nhu 1 bo phim drama chu khong phai canh thuong ngay"
# ════════════════════════════════════════════════════════════════════════════
# 🔴 STYLE_MODERN cua lib la ngon ngu PHIM TAI LIEU — "everyday digital video",
#    "candid unposed action filmed from a respectful distance", "deep focus".
#    Va AVOID_MODERN con CAM thang "no shallow blurred background, no cinematic
#    bokeh, no dramatic studio lighting" => chong lai chinh thu dang muon.
#    Cung benh voi ca CAST PLATE o luot truoc: cau CAM chong lai MUC DICH.
STYLE_FILM = (
 "a scene from a Japanese television drama, cinematic and composed, "
 "anamorphic lenses and a shallow depth of field so the subject stands clear of a "
 "softly falling-away background, "
 "a graded cinema image: cool desaturated shadows with a faint green cast from the "
 "fluorescent tubes, deep clean blacks, warm practical lights held in frame, "
 "a gentle fine grain over the picture, "
 "the light always coming from a source you can see, "
 "deliberate framing with the subject placed off-centre and room left in the frame, "
 "the image fills the entire frame edge to edge, "
 "horizontal landscape video in 16:9 aspect ratio, 1920x1080 widescreen, "
 "clearly wider than it is tall, not vertical and not square")

def _film_avoid(a):
    """Bo cac cau CHONG lai mau phim, GIU cac cau chong LOI."""
    for bad in ("no shallow blurred background, ", "no cinematic bokeh, ",
                "no dramatic studio lighting, ", "no shallow blurred background",
                "no cinematic bokeh", "no dramatic studio lighting",
                "not posed for the camera, ", "nobody looking at the camera, ",
                "no staged tableau, ", "not posed for the camera",
                "nobody looking at the camera", "no staged tableau"):
        a = a.replace(bad, "")
    import re as _re
    a = _re.sub(r"(,\s*)+,", ",", a)
    a = _re.sub(r",\s*,", ",", a)
    a = _re.sub(r"\s{2,}", " ", a).replace(", .", ".").strip().rstrip(",")
    return a + (", flat lifeless video lighting, daytime news footage look, "
                "harsh on-camera flash, washed-out greys, home-video look")

V.STYLE          = STYLE_FILM
V.STYLE_MODERN   = STYLE_FILM
V.AVOID          = _film_avoid(V.AVOID_MODERN)
V.AVOID_MODERN   = V.AVOID
V.AVOID_POV      = _film_avoid(V.AVOID_MODERN_POV)
V.AVOID_MODERN_POV = V.AVOID_POV
PROF = {"STYLE": STYLE_FILM, "AVOID": V.AVOID}

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
 # ══════════════════════ VAI CHINH — co CAST PLATE (anh tham chieu) ══════════════════════
 # 3 nguoi nay xuat hien nhieu nhat va PHAI giong nhau tuyet doi => khoa bang ANH.
 "chizuru":          "an older woman in a plain dark grey zip-up jacket and dark trousers, a small cloth shoulder bag",
 "chizuru_pov":      "their own forearms in plain dark grey jacket sleeves and the dark grey jacket on their own chest",
 "chizuru_pov_sit":  "their own forearms in plain dark grey jacket sleeves, and their own knees and the edge of a blue plastic sheet across the bottom of the picture",
 "chizuru_pov_stand":"their own forearms in plain dark grey jacket sleeves and the dark grey jacket on their own chest",
 "chizuru_pov_hand": "their own forearms in plain dark grey jacket sleeves and the backs of their own hands",
 "chizuru_pov_walk": "only their own hand or hands where the work needs them, plain dark grey jacket cuffs at the edge",
 "setsuko":          "a woman in a navy blue windbreaker with a yellow armband on one sleeve and a small handmade name card on a cord round her neck",
 "ichinose":         "a very old man in a brown knitted cardigan with a blanket over his knees, a thin clear tube running to his face",

 # ══════════════════════ VAI PHU — khoa bang MO TA CO DINH (khong anh) ══════════════════════
 # Truoc buoc nay ho la "a young man" / "a teacher" / "a young woman" => moi clip mot nguoi
 # khac nhau, va do la thu lam video KHONG giong mot bo phim. Khoa bang MAU AO + VAT DEO,
 # lap nguyen van o moi clip. ⛔ Khong ta mat/tuoi/toc (model tu che, cang ta cang lech).
 # Yeu hon anh, nhung du de mat nhan ra "van nguoi do".
 "mago":      "a young man in a dark grey hooded sweatshirt with the hood down",            # chau cu — 26 clip
 "gyosha":    "a man in a dark blue waterproof work jacket with a towel round his neck",     # tho bom nuoc — 9
 "kaicho":    "a heavy-set man in a soaked beige zip jacket",                                # chong Setsuko — 8
 "shokuin":   "a man in an olive green city waterproof jacket carrying a clipboard",         # can bo dem — 7
 "shitsucho": "a man in a charcoal suit and a plain dark tie",                               # nguoi vest sang — 4
 "shonin":    "a young woman in a pale grey hooded fleece",                                  # nguoi lam chung — 7
 "kyoto":     "a middle-aged man in a dark school tracksuit top with a lanyard round his neck",  # thay hieu pho — 3
 "haha":      "a young woman in a dusty pink long-sleeved top",                              # nguoi me tre — 4
}

# 🔴 Tran cua tool la 3 nhan vat CO TEN / video — dat ra vi "1 anh / 1 lan gen", tuc moi
#    clip chi khoa duoc MOT nguoi bang anh. Tran do dung cho vai CO ANH. Vai phu khoa bang
#    CHU thi khong dung rang buoc do => noi tran VIDEO len 11, GIU nguyen tran SCENE = 2.
V.MAX_CAST_IN_VIDEO = 11

CROWD = {
 "taiikukan": "full", "uketsuke": "full", "asa": "full",
 "sumi": "few", "rouka": ("solo", "hanh lang — cho bi day ra, VANG chinh la noi dung"),
 "souko": ("solo", "cua kho khoa — khong ai o day, do la y"),
 "shokuin": ("solo", "phong giao vien ban dem"),
 "soto": "few", "supa": "few", "haru": "few",
}
CROWD.update(CROWD_EXTRA)

# ── ghep S: chen INS_A vao dung cho trong SA, roi noi SB, SC ──
S = list(SA)
for after_id, scene in INS_A:
    idx = next(i for i, r in enumerate(S) if r[0] == after_id)
    S.insert(idx + 1, scene)
S += SB
S += SC

# ════════════════════════════════════════════════════════════════════════════
# ⭐ TI LE POV = 30% (user chot: "it goc POV thoi, chu yeu goc nhin thu 3")
# ════════════════════════════════════════════════════════════════════════════
# POV la cach re nhat de giu "nhan vat dong nhat" (khong thay mat = khong lech),
# nhung 61% ca video nhin qua MOT cai dau thi met. Ha ve 30%:
#   · GIU POV o beat CHU QUAN that: tay lam viec ("their own hand"), va may DI
#     CHUYEN theo dau nguoi ("the view carries/turns").
#   · CHUYEN sang ngoi 3 cac canh QUAN SAT TINH — chung von khong co Chizuru
#     lam gi trong khung, chi la "cai ba ay dang nhin". Bo tien to POV la thanh
#     canh khach quan, khong mat gi.
# ⚖️ Gia phai tra: Chizuru se xuat hien o ngoi 3 => co the lech mat. Bu lai bang
#    cast plate cua ba + uu tien behind/ots cho canh co ba trong khung.
_POV_MOVE = re.compile(r"the view (carries|turns|moves|comes down|holds|dips|rises|follows)"
                       r"|the whole view", re.I)
_POV_OWN  = re.compile(r"their own", re.I)
def _to_third(act, cam):
    a = re.sub(r"^A_[A-Z]+:\s*", "", act)
    a = (a.replace("fills the bottom of the view", "fills the foreground of the frame")
           .replace("fills the top of the view", "fills the top of the frame")
           .replace("fills the middle of the view", "fills the middle of the frame")
           .replace("fills the view", "fills the frame")
           .replace("in the bottom of the view", "in the foreground")
           .replace("in the middle of the view", "in the middle of the frame")
           .replace("ahead of the view", "ahead")
           .replace("at the far end of the view", "at the far end of the frame")
           .replace("towards the camera side", "towards the camera")
           .replace("the camera side", "the near side"))
    return a
_HAS_PERSON = re.compile(r"A_[A-Z]+|man|woman|figure|people|famil|grandson|"
                         r"teacher|officer|neighbour|shopper|queue|mother", re.I)
_TARGET_POV = 0.30
_pov_idx = [i for i, r in enumerate(S) if str(r[4]).startswith("pov")]
_keep = {i for i in _pov_idx if _POV_OWN.search(S[i][2]) or _POV_MOVE.search(S[i][2])}
_n_keep = round(len(S) * _TARGET_POV)
# neu nhom GIU van nhieu hon chi tieu thi tha them may-di-chuyen ve ngoi 3
if len(_keep) > _n_keep:
    _mv = [i for i in sorted(_keep) if not _POV_OWN.search(S[i][2])]
    for i in _mv[: len(_keep) - _n_keep]:
        _keep.discard(i)
elif len(_keep) < _n_keep:
    # thieu thi giu them canh quan-sat-tinh, RAI DEU ca bai (khong dồn mot khoi)
    _rest = [i for i in _pov_idx if i not in _keep]
    _need = _n_keep - len(_keep)
    if _rest and _need > 0:
        step = max(1, len(_rest) // _need)
        for i in _rest[::step][:_need]:
            _keep.add(i)
_cycle = ["medium", "ots", "low", "behind", "medium", "high", "ots", "medium"]
_k = 0
for i in _pov_idx:
    if i in _keep:
        continue
    r = list(S[i])
    r[2] = _to_third(r[2], r[4])
    if _POV_MOVE.search(S[i][2]):
        r[4] = "pan"                      # may di chuyen -> pan, khong phai canh tinh
    else:
        cand = [c for c in _cycle if c not in ("ots", "behind")] if not _HAS_PERSON.search(r[2]) else _cycle
        r[4] = cand[_k % len(cand)]; _k += 1
    S[i] = tuple(r)
print("POV sau khi ha: %d/%d = %.0f%%" % (len(_keep), len(S), len(_keep) * 100 / len(S)))

CUT = set()
S = autochain(S, cut=CUT)

# ── VA TU DONG 2 loi may moc, lap den khi sach ──
# (a) "thieu out" trong chuoi AUTO  -> CAT chuoi do (khong bia trang thai ket)
# (b) hai canh RONG lien tiep cung preset -> doi framing canh SAU sang CHAT
#     canh co nguoi -> 'ots' ; canh tinh vat -> 'low'
WIDE  = {"wide", "behind", "pan", "high", "still"}
def _has_person(act):
    return bool(re.search(r"A_[A-Z]+|man|woman|figure|people|famil|grandson|"
                          r"teacher|officer|neighbour|shopper|children|queue", act, re.I))
for _ in range(40):
    changed = False
    # (a)
    for i, r in enumerate(S):
        ch = r[6] if len(r) > 6 else None
        out = r[7] if len(r) > 7 else None
        if ch and str(ch).startswith("auto_") and not out:
            nxt = S[i + 1] if i + 1 < len(S) else None
            if nxt and (nxt[6] if len(nxt) > 6 else None) == ch:
                CUT.add(nxt[0]); changed = True
    if changed:
        S = autochain([tuple(list(r[:6]) + [None, None]) if str(r[6] if len(r)>6 else "").startswith("auto_")
                       else r for r in S], cut=CUT)
        continue
    # (c) chuoi dung >1 preset, HOAC bi chen canh khac vao giua -> BO chain
    #     (canh "di toi noi" bang qua 2 boi canh thi khong the cung chuoi;
    #      noi lien van con o LOGIC, chi bo rang buoc cu may)
    from collections import defaultdict
    pos = defaultdict(list)
    for i, r in enumerate(S):
        ch = r[6] if len(r) > 6 else None
        if ch: pos[ch].append(i)
    bad = set()
    for ch, idxs in pos.items():
        presets = {S[i][3] for i in idxs}
        contiguous = (max(idxs) - min(idxs) + 1) == len(idxs)
        if len(presets) > 1 or not contiguous: bad.add(ch)
    if bad:
        for i, r in enumerate(S):
            if (r[6] if len(r) > 6 else None) in bad:
                lr = list(r); lr[6] = None; lr[7] = None; S[i] = tuple(lr)
        changed = True
        continue
    # (b)
    for i in range(1, len(S)):
        a, b = S[i - 1], S[i]
        if a[3] == b[3] and a[4] in WIDE and b[4] in WIDE:
            lb = list(b); lb[4] = "ots" if _has_person(b[2]) else "low"
            S[i] = tuple(lb); changed = True
    if not changed:
        break

# ⭐ CAST PLATE: co ANH thi KHONG duoc ta lai quan ao trong prompt
#    (dua ca anh lan mo ta dai = hai nguon mau thuan, model tron lai).
#    `plates` bat build() dung expand_with_plate() -> "matching the reference image exactly".
PLATES = {"chizuru": "cast_chizuru.png",
          "setsuko": "cast_setsuko.png",
          "ichinose": "cast_ichinose.png"}
rows = build(S, P, C, prof=PROF, plates=PLATES, crowd=CROWD)
n_red, n_warn = gate(rows, S, P, C, prof=PROF,
                     interior={"taiikukan", "uketsuke", "rouka", "sumi", "souko",
                               "shokuin", "asa", "haru", "genkan"},
                     strict=True, crowd=CROWD)
# ══════════════════════════════════════════════════════════════════════════
# 🔴 GUARD CHU PHAI NAM O 15% DAU PROMPT (ai-video-regen.md §2)
# ══════════════════════════════════════════════════════════════════════════
# Do duoc o nenkin 25: guard so dat o 55% => 4/6 clip "cam so" VAN co so;
# dua len 2% => sach. Bai nay AVOID nam o ~77% prompt, tuc dang vi pham —
# va no nguy hiem vi bai co 50 clip so ke dong + 52 clip kep ho so + 14 clip
# so tay: toan VAT MOI GOI model dien chu Nhat gia (§3 "vat moi goi thang cau cam").
# ⇒ Chen mot khoi cam NGAN ngay DAU moi prompt. AVOID cuoi giu nguyen.
GUARD = ("NO WRITING ANYWHERE IN THIS SHOT: every page, form, card, label, sign and screen "
         "is blank — ruled lines and empty boxes only, no letters, no numbers, no handwriting, "
         "no printed text, in any language. ")
rows = [(r[0], r[1], r[2], r[3], r[4], GUARD + r[5]) if len(r) > 5 else r for r in rows]
_gp = [x[5].find("NO WRITING") * 100 // len(x[5]) for x in rows if len(x) > 5]
print("guard chu @ %d%%–%d%% prompt (luat: <=15%%)" % (min(_gp), max(_gp)))

safe, risky, pct = linkage(S)
print("\nNOI AN TOAN: %d/%d moi noi cung boi canh co it nhat mot canh CHAT (%.0f%%)" % (safe, risky, pct))
pov = sum(1 for x in S if str(x[4]).startswith("pov"))
print("POV: %d/%d = %.0f%%" % (pov, len(S), pov * 100 / len(S)))
print("SO CLIP: %d  ->  %d giay = %.1f phut  |  %.1f doi hinh/phut"
      % (len(S), len(S) * 8, len(S) * 8 / 60, len(S) / (2274 / 60)))
from collections import Counter
print("theo khoi:", dict(Counter(x[1] for x in S)))

OUTDIR = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"
os.makedirs(OUTDIR, exist_ok=True)
if n_red == 0:
    write_outputs(rows, OUTDIR, prefix="videogen", prof=PROF)
    print("\nXUAT -> %s\\videogen_FLOW.txt | _TENFILE.txt | _BLOCKS.md" % OUTDIR)
else:
    print("\n[CHAN] %d loi do — KHONG xuat file. Sua roi chay lai." % n_red)
