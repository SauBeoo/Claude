# -*- coding: utf-8 -*-
"""gen_realism_17 — 112 canh cua video 17 theo CONG THUC REALISM (user chot 2026-09-22).

Chep khuon `gen_realism_16.py`. GIU cua video 17: boi canh 昭和 that (SC) · dan cast co KHUON MAT (CA)
· vat mau XOAY VONG (PROPS, list) · chu ky bieu cam (EXPR_BANK + so EXPR_REGISTRY) · cho may dung (STAND)
· MACH TRUYEN 112 canh (SHOTS) — tat ca import tu `gen_prompts_17`, KHONG chep.

DOI so voi ban truoc (`gen_prompts_17.py` = khuon `camera-language` §4, nay het ap cho clip AI showa):
  ⛔ 15 nuoc may dolly/tracking + "never comes to rest"  ->  ✅ may KHOA 2/3 · TROI mot buoc 1/3
  ⛔ prompt t2v 4.700 ky mot manh                        ->  ✅ cap STILL (Nano Banana) -> Animate -> MOTION
  ⛔ "fine film grain over the whole picture" tu do      ->  ✅ khoi chung realism_blocks.py
  Bang chung: lo 109 clip showa 16 theo khuon cu do duoc MAD 9,4 · 87% khung dang dong · 37 px/s;
  mau 異世界さんぽ (32K/11 ngay, cung Veo) = 1,5 · 10% · 14 px/s. (CLAUDE.md §Visual)

⚠️ Day la lop L3 (AI) — L1 phim that / L2 anh that cua REAL-FIRST v2 khong doi.
   Video 17 la bai VAN PHONG nen kho phim PD khong voi toi (xem build_slides_17.py) => L3 ganh ca bai.

Chay:  python tools/gen_realism_17.py
Xuat:  06_VIDEO/17_kaisha-ga-kureta/realism17_STILL_FLOW.txt · _MOTION_FLOW.txt · _T2V_FLOW.txt · _TENFILE.txt
"""
import io, json, re, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "_media_library"))

from realism_blocks import build_pair, gate_prompt, gate_action, HOLD_CLAUSE, LIMIT_SHOWA
import gen_prompts_17 as G      # SC · CA · PROPS · STAND · SHOTS · ARCH · BAN · pick_expr17

OUT = G.OUT
VIDEO_ID = G.VIDEO_ID

# ---------------------------------------------------------------- anh sang theo BOI CANH
# 🔴 Chon theo NGUON SANG THAT cua canh do, khong chon theo "cho dep".
LIGHT_OF = {
 "keijiban": "interior", "office": "interior", "rouka": "interior", "soumu": "interior",
 "soubetsu": "interior", "ryou": "night", "ryoushitsu": "night",
 "shataku": "day", "shataku_niwa": "day", "michi": "dawn", "genkan": "day",
 "chanoma": "night", "daidokoro": "night", "ima_ie": "interior",
}
HEIGHT_OF = {"table": "the height of the tabletop, seated",
             "seated": "seated eye height on the floor",
             "eye_st": "standing eye height"}

# ---------------------------------------------------------------- may TROI (1/3) hay KHOA (2/3)
# Mau do duoc: 32% shot co di, va di chi la TROI 8–10 px/s = mot buoc chan trong 8 giay.
# ⇒ TROI danh cho canh CHUYEN CHO / CANH THO / canh mo mot khoi; canh CAM XUC thi KHOA
#   (khoa lam nguoi xem nhin mat, khong nhin khung).
DRIFT_SCENES = {"michi", "shataku_niwa", "rouka"}          # canh di lai / canh tho
DRIFT_IDS = {"c000", "c010", "c051", "c054", "c070", "c086", "c087", "c103", "c111"}  # mo/dong tung khoi
LOCK_IDS  = {"c002", "c016", "c024", "c087", "c090", "c101", "c108"}                  # canh cam xuc: KHOA


_NOCAST_N = [0]


def cam_of(sid, scene, has_cast=True):
    if sid in LOCK_IDS:
        return "locked"
    if sid in DRIFT_IDS or scene in DRIFT_SCENES:
        return "drift"
    if not has_cast:                       # canh THO: cu 3 canh lay 1 canh troi
        _NOCAST_N[0] += 1
        return "drift" if _NOCAST_N[0] % 3 == 0 else "locked"
    return "locked"


# ---------------------------------------------------------------- [VA 2026-09-22] bon lop sua
# Do duoc tren lo gen dau (3/3 clip hong): 93/112 canh khong khai huong than/mat · 5/112 dung
# dong tu tu the mo ho · boi canh nam cuoi prompt STILL. Xem docstring dau file.

ORIENT = {
 "behind":  "Everyone is seen from behind with their backs to the camera for the whole shot, and nobody turns round.",
 "ots":     "The shot is over the near person's shoulder, the back of that head and shoulder held in the near corner of the frame, and nobody turns towards the camera.",
 "ots_":    "",
 "eye":     "Everyone is seen in three-quarter view from the side, faces angled away from the lens, and nobody turns towards the camera or walks towards it.",
 "high_sl": "Everyone is seen from slightly above and to one side, faces angled down at what they are doing, and nobody turns towards the camera.",
}

# 🔴 Dong tu tu the MO HO -> dong tac DUT KHOAT. Ca goc c001: "lean in until their heads almost
#    touch the sheet" + "rise onto their toes" => model cho ca nhom CUI GAP NGUOI nhu dang chao.
VAGUE = [
 # [VA 8, 22/09 toi] 5 kieu loi do tren 14 clip — xem realism_blocks.gate_action
 ("men in white shirts come along the corridor from both ends and gather in front of the board",
  "men in white shirts already stand in a loose group in front of the board, nobody arriving and nobody leaving"),
 ("men in work jackets walk along the narrow lane in the early morning all the same way",
  "men in work jackets walk away down the narrow lane in the early morning, all the same way"),
 ("the man beside him says something short over his shoulder", "the man beside him glances at him over his shoulder"),
 ("says something short", "glances at him and gives one small nod"),
 ("reaches up and presses a drawing pin into the top corner of a fresh sheet on the notice board",
  "reaches up and presses a fresh sheet flat against the notice board with the whole palm of one hand, the sheet staying on the board"),
 ("pins a second sheet up beside the first", "holds a second sheet flat against the board beside the first with one hand"),
 ("runs his thumb down the edge to flatten it", "smooths it down with the flat of his other hand"),
 ("works his way to the front of the crowd", "stands at the front of the crowd"),
 ("the crowd in front of the board grows until it fills the corridor; those at the back look sideways one after another to find a gap between the heads",
  "the crowd in front of the board stands still, filling the corridor; one man at the back turns his head to look between the heads in front of him"),
 ("men at the desks put their heads up one after another along the row, and one of them says something that makes the next three look round; then they all go back down to their work",
  "the men at the desks work with their heads down; one of them looks up and turns to the man beside him, and the two beyond look round; then they go back to their work"),
 ("and says something to the clerk", "and looks at the clerk"),
 ("lean in until their heads almost touch the sheet",
  "stand close to the board with their faces a hand's width from it"),
 ("the ones behind rise onto their toes to see over the shoulders in front of them",
  "the ones behind look over the shoulders in front of them without moving their feet"),
 ("then the ones behind press closer together",
  "and the ones behind stand shoulder to shoulder without moving their feet"),
 ("then the whole group shifts one pace closer to the board and nobody steps away",
  "and nobody steps away from the board"),
 ("the whole crowd shifts forward one pace", "the whole crowd stays where it is"),
 ("then the whole group shifts a pace closer to the board", "and nobody moves their feet"),
 ("those at the front lean in until their heads almost touch the sheet",
  "those at the front stand close to the board with their faces near it"),
 ("the men at the front stand with their hands behind their backs and lean in",
  "the men at the front stand with their hands behind their backs, close to the board"),
 ("and the ones behind press closer together",
  "and the ones behind stand shoulder to shoulder"),
 ("those at the back cannot see and lean out sideways one after another to find a gap",
  "those at the back look sideways one after another to find a gap between the heads"),
 ("the front row leans in", "the front row stands close to the board"),
 # [VA 8] ba ca con lai sau gate: dam dong "grows" · "answers"/"says" = hanh dong noi
 ("the crowd in front of the board grows until it fills the corridor", "the crowd in front of the board stands still, filling the corridor"),
 ("he says something short, she stops pouring and looks up", "he glances up at her, she stops pouring and looks up"),
 ("answers in his own way", "reacts in his own way"),
 ("the men behind lean in all together", "the men behind hold still where they are"),
]


def _rest_after(first, act):
    """Phan TIEP DIEN sau nhip 1 (xem [VA 5]). Khong tach duoc thi bao model HOAN TAT dong tac
    do that cham, chu KHONG lam lai tu dau — day la khac biet giua 'dien tiep' va 'dien lai'."""
    f = first.rstrip(".").strip()
    a = act.strip()
    if a.lower().startswith(f.lower()):
        rest = a[len(f):].lstrip(" ;,.").strip()
        if len(rest) >= 30:
            # ⚠️ KHONG them cau dan o day: `build_pair` da mo bang "Starting from exactly the
            #    framing of the first frame: ". Them nua thanh hai cau dan chong nhau.
            return rest[0].lower() + rest[1:]
    return ("the moment simply carries through to its end without starting over — "
            + a[0].lower() + a[1:])


def _tighten(act):
    """[VA 3] MOTION chi giu toi da HAI nhip. Khuon REALISM: mot dong tac trai het 8 giay;
    ba nhip cua §6.6 sinh ra khi may CON DI — may dung yen thi no thanh ba viec roi rac."""
    for a, b in VAGUE:
        act = act.replace(a, b)
    # 🔴 [VA 6, 22/09 tối] cắt trên BẢN CÒN PLACEHOLDER: {EX:x} là 1 token, sau khi bung nó thành
    #    một mệnh đề 3 nhịp nữa (c003: "turns his head… he looks off… jaw moves once… looks back") = 5 nhịp/8s.
    segs = re.split("; |, and then |, then ", act)
    if len(segs) > 2:
        ex = [x for x in segs[1:] if "{EX:" in x]
        keep = [segs[0]] + (ex[:1] if ex else [segs[1]])
        act = ", then ".join(keep)
    return act.rstrip(" ,.")


def world_of(scene, occ):
    """THE GIOI cua showa = boi canh that + vat mau (xoay vong theo lan xuat hien cua boi canh)."""
    props = G.PROPS[scene][occ % len(G.PROPS[scene])]
    if "present-day" in G.SC[scene]:
        # [VA 9, 23/09] 8/8 canh ima_ie gen ra PHONG THAP NIEN 70 (go nau, den tron, ban thap) => neo "thoi nay"
        #   cua ca bai vo hinh. Prompt chi noi "present-day" ma khong ke VAT hien dai nao => model lay palette
        #   chung cua lo. Phai goi ten vat (cung dinh luat mau ruc phai den tu VAT, camera-language §5.1).
        era = ("Present-day Japan, unmistakably TODAY and not the past: plain white walls, a flat LED ceiling panel, "
               "an aluminium-framed sliding window with a white roller blind, a light-grey fabric sofa, a pale wood "
               "table, a thin dark flat television switched off on a low stand; clean, bright, uncluttered, filmed "
               "like a documentary; nothing staged, and only the one old sheet of paper is from another time.")
    else:
        era = ("Real Japan of the early nineteen-seventies exactly as it was — a classical, ordinary, documentary "
               "world: no fantasy element, no futuristic or impossible architecture, no modern object anywhere.")
    return ("Setting: " + G.SC[scene].rstrip(",") + ". Bright colour only in the props: " + props
            + G.K.PROP_TAIL + ". " + era)


def freeze(raw):
    """Khung dau (STILL) = NHIP 1 cua hanh dong.

    🔴🔴 PHAI CAT TREN BAN CON PLACEHOLDER `{honnin_tei}`, KHONG cat sau khi thay cast.
       Cast cua showa la mot cau ~250 ky CO DAU PHAY ben trong ("a man of about sixty, wide square
       face, low flat forehead, ..."). Cat theo do dai chuoi SAU khi thay thi dao cat roi vao GIUA
       mo ta khuon mat => c087 ra dung `A man of about sixty.` — mat ca mat lan bo hoa.
       Do la cat sai TANG: cai can cat ngan la HANH DONG, khong phai CAST.
       Cat tren ban placeholder thi `{honnin_tei}` chi la 1 token, moi dau phay con lai deu la
       ranh gioi cua menh de hanh dong that."""
    c = raw.split(";")[0].strip().rstrip(".,")
    for sep in (", then", ", and "):
        if len(c) <= 170:
            break
        c = c.split(sep)[0].strip().rstrip(".,")
    return c[0].upper() + c[1:] + "."


def _fill(txt, expr, pick):
    for cast, lv in expr:
        txt = txt.replace("{EX:%s}" % cast, G.K.EXPR_BANK[G.ARCH[cast]][pick[cast]] + G.K.LEVEL[lv])
    for k, v in G.CA.items():
        txt = txt.replace("{%s}" % k, v)
    return txt


_LAST_CAST = [None]


def convert(sh, occ, pick, W):
    (name, scene, size, angle, height, stand, move, land, expr, action, extras, out, _why) = sh
    # [VA 8] dai tu khong chu: "his hand stays…" o canh khong cast => model tu chon nguoi (c005 ra co gai).
    #   Muon cast cua canh TRUOC co cast (cung mach), khai ro o dau hanh dong.
    if expr:
        _LAST_CAST[0] = expr[0][0]
    carry = (_LAST_CAST[0] if (not expr and _LAST_CAST[0]
             and action.lstrip().lower().startswith(("he ", "she ", "his ", "her "))) else None)
    # 🔴🔴 [VA 5, 2026-09-22] ANH la NHIP 1; MOTION phai la phan TIEP DIEN, khong dien lai nhip 1.
    #   Ca goc (user: *"anh thi oke roi nhung hanh dong no dang khong khop"*): c001 — anh da co
    #   dam dong DUNG TRUOC BANG, ma MOTION van mo bang "nguoi di toi tu hai dau hanh lang va TU LAI"
    #   => model phai dung lai canh da co san trong anh, nguoi di lung tung.
    #   Cat theo BAN DA _tighten (khong phai ban goc), neu khong prefix khong con khop.
    act_t = _tighten(action)
    if carry:   # [VA 8 ②] them CHU SAU khi cat nhip, noi bang ":" (khong phai dau ngat) => khong an mat mot nhip
        act_t = "{%s} is the one in the shot: " % carry + act_t
    first_raw = freeze(act_t)
    rest_raw = _rest_after(first_raw, act_t)
    first = _fill(first_raw, expr, pick)           # cho STILL
    orient = ORIENT.get(angle, ORIENT["eye"])      # [VA 1] khoa HUONG than/mat so voi may
    # [VA 6] orient ghi MOT lan — o STILL (anh quyet dinh huong); motion tiep dien tu anh nen khong lap.
    action = _fill(rest_raw, expr, pick).rstrip(" .") + "."
    act_full = _fill(act_t, expr, pick).rstrip(" .") + "."     # t2v: hanh dong day du, mot lan
    # [VA 8 ③] vat nho tren tay (giay, but, con dau) — khong cam (bai van phong can chung), them cau GIU VAT
    if any(k == "③" for k, _ in gate_action(act_full)):
        action = action + " " + HOLD_CLAUSE
        act_full = act_full + " " + HOLD_CLAUSE
    return dict(
        id=name,
        light=LIGHT_OF[scene],
        cam=cam_of(name, scene, bool(expr)),
        where=G.STAND[stand],
        height=HEIGHT_OF.get(height, "standing eye height"),
        # 🔴 KHONG prefix SC o day: `build_pair` da ghep khoi `world` (= "Setting: " + SC + props)
        #    vao STILL roi => de SC o ca hai cho la LAP NGUYEN VAN boi canh trong cung mot prompt,
        #    ton ~200-400 ky va day 9/112 canh vuot tran 2.400 cua LIMIT_SHOWA. STILL chi can NHIP 1.
        # [VA 4] boi canh di TRUOC nguoi: "cai gi quan trong phai o 15% dau" (ai-video-regen §2).
        #   Ca goc c000: world nam o ~70% do dai => model tu bia noi chon (ra quan an nhin ra pho).
        still=W + " " + first + " " + orient,
        act=action,
        act_full=act_full,
        still_t2v=W + " " + orient,        # t2v: boi canh + huong, KHONG nhip 1 (nhip 1 da nam trong act_full)
        alive="",
    ), scene


def main():
    pick, reg = G.pick_expr17()
    plan = json.loads((OUT / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
    slots = plan["slots"]
    out = {"still": [], "motion": [], "t2v": []}
    rows, fails = [], 0
    occ = Counter()

    if len(G.SHOTS) != len(slots):
        print("🔴 %d canh nhung SLIDES co %d o" % (len(G.SHOTS), len(slots))); fails += 1

    for i, sh in enumerate(G.SHOTS):
        scene = sh[1]
        sc, scene = convert(sh, occ[scene], pick, world_of(scene, occ[scene]))
        occ[scene] += 1
        st, mo, tv = build_pair(sc, "")   # world da nam trong sc["still"], khong lap lai o cuoi
        for k, p in (("still", st), ("motion", mo), ("t2v", tv)):
            out[k].append(p)
            for e in gate_prompt(k, p, LIMIT_SHOWA):
                fails += 1
                print("  🔴 %s [%s]: %s" % (sc["id"], k, e))
        for kind, e in gate_action(sc.get("act_full", sc["act"]), has_cast=bool(sh[8]) or "{" in sh[9]):
            if kind == "③":
                continue                      # da xu ly trong convert (HOLD_CLAUSE)
            fails += 1
            print("  🔴 %s [act %s]: %s" % (sc["id"], kind, e))
        sigs = [pick[c] for c, _ in sh[8]]
        if len(set(sigs)) != len(sigs):
            fails += 1; print("  🔴 %s: hai cast cung mot chu ky" % sc["id"])
        s = slots[i] if i < len(slots) else {"dur": 0, "block": "?", "text": ""}
        rows.append((sc["id"], sc["cam"], sc["light"], scene, s["block"], s["dur"], sh[12], s["text"]))

    # --- GATE CHU KY <-> CANH (them 2026-09-23, user chi ca c019)
    #   Chu ky bieu cam gan theo CAST nen no di theo nguoi vao MOI canh — ke ca canh nguoi do
    #   khong o tu the/khong co dao cu ma chu ky doi. Ca goc c019: `kachou` mang m50_pen
    #   ("go but hai cai xuong ban, mat o dong trang giay") trong khi canh la DUNG O CUA SO he rem.
    #   ⚠️ Da va mot lan o tang CAST (bang BAN), lan nay la tang CANH — hai tang khac nhau.
    SIG_PROP = {"pen": ("desk", "table", "page", "papers", "ledger", "counter"),
                "chair": ("chair", "desk", "sits", "seated"),
                "glasses": ("glasses",),
                "sleeve": ("sleeve", "apron", "kimono"),
                "apron": ("apron",),
                "fan": ("fan",),
                "tea": ("tea", "cup", "pour")}
    for sh in G.SHOTS:
        act = sh[9].lower()
        for cast, _lv in sh[8]:
            sig = pick[cast]
            for key, need in SIG_PROP.items():
                if key in sig and not any(n in act for n in need):
                    fails += 1
                    print("  🔴 %s: chu ky %s doi '%s' ma canh khong co (%s)"
                          % (sh[0], sig, key, act[:52]))

    # --- GATE HA TANG (them 2026-09-23, user: *"treo quan ao khong co gia treo the"*)
    #   HANH DONG can mot VAT thi BOI CANH phai khai vat do. Thieu => model tu bia hoac bo:
    #   ca goc c006 "hangs it over the railing and pegs it down" trong khi SC chi co lan can thep
    #   => quan ao vat qua lan can / treo lo lung, khong co 物干し竿.
    #   Cung ho "vat moi goi thang cau cam" (ai-video-regen §3), nhung nguoc chieu: o day la
    #   VAT CAN MA KHONG CO. Gate re, chan duoc mot lop loi ma mat chi thay sau khi gen.
    # ⚠️ Tu khoa phai la CUM DAC TRUNG cua hanh dong do, khong phai mot dong tu chung.
    #   Ban dau dung "hangs" tran => bao oan 3/4: "hangs the jacket over the chair back" (c010),
    #   "the pull cord hangs still" (c106), "rubber stamps at the back of the drawer" (c089).
    #   Gate bao do hang loat ngay lan dau thi nghi chinh GATE truoc khi nghi du lieu.
    NEED = {
     ("drying pole", "clothes peg", "pegs the shoulders", "wet shirt out of the pail",
      "washing already out", "pegged"): "drying pole",
     ("drawing pin", "pinned up", "pinned low", "pins a second sheet"): "notice board",
     ("dial of the safe", "turns the heavy dial", "into the open safe", "closes the safe"): "safe",
     ("long ledger", "the ledger",): "ledger",
     ("calculator handle", "the hand-cranked calculator",): "calculator",
     ("lid of the rice bin", "behind the rice bin",): "rice bin",
     ("stamps it once", "stamp-pad case", "lays a rubber stamp down"): "stamp",
    }
    for sh in G.SHOTS:
        act, sc_txt = sh[9].lower(), G.SC[sh[1]].lower()
        for keys, need in NEED.items():
            if any(k in act for k in keys) and need not in sc_txt:
                fails += 1
                print("  🔴 %s [%s]: hanh dong can '%s' ma boi canh khong khai"
                      % (sh[0], sh[1], need))

    # --- gate tran lap chu ky (camera-language §6.7 muc 4)
    cnt = Counter((c, lv) for sh in G.SHOTS for c, lv in sh[8])
    for (c, lv), n in cnt.items():
        if n > 3:
            fails += 1; print("  🔴 chu ky %s/%s lap %d lan (tran 3)" % (c, lv, n))

    # --- gate vat ruc (giu tu ban truoc: ca goc but chi cai tai 16/112, stamp-pad 53/112)
    frag = Counter()
    for p in out["still"]:
        if "Bright colour only in the props: " in p:
            seg = p.split("Bright colour only in the props: ")[1].split(" with no writing")[0]
            for piece in seg.replace(", ", " and ").split(" and "):
                piece = piece.strip()
                if len(piece) > 12: frag[piece] += 1
    hot = [(k, n) for k, n in frag.items() if n > 8]
    for k, n in sorted(hot, key=lambda x: -x[1])[:5]:
        fails += 1; print("  🔴 vat ruc lap %d/%d: %s" % (n, len(rows), k[:60]))

    OUT.mkdir(parents=True, exist_ok=True)
    for k, fn in (("still", "realism17_STILL_FLOW.txt"), ("motion", "realism17_MOTION_FLOW.txt"),
                  ("t2v", "realism17_T2V_FLOW.txt")):
        io.open(OUT / fn, "w", encoding="utf-8", newline="\n").write("\n".join(out[k]) + "\n")

    # [VA 7, 22/09 toi] CAST PLATE — anh tham chieu khoa NHAN VAT cho Ingredients (04_VIDEOGEN_PROMPTS §8.6g).
    #   user: "no khong giong 1 cau chuyen" — t2v moi clip ve mot mat khac. Flow nay co nut Ingredients (thay 22/09).
    plates = []
    for cast in ("honnin", "honnin_tei", "ima", "tsuma", "kachou", "douryou"):
        plates.append("A single photorealistic reference photograph, wide 16:9, of one person standing still, full body, "
                      "turned three-quarters towards the camera, on a plain light-grey studio background with no props and no "
                      "setting, soft even light with no hard shadow, sharp and clear, Japan around the year nineteen seventy "
                      "in period clothing: " + G.CA[cast] + ". No writing, lettering or numbers anywhere.")
    with io.open(OUT / "realism17_CASTPLATE_FLOW.txt", "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(chr(10).join(plates) + chr(10))
    with io.open(OUT / "realism17_CASTPLATE_TENFILE.txt", "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write("# dong i cua CASTPLATE_FLOW -> anh plate cua cast (Image, Nano Banana 2; chon 1 anh mat ro, toan than)" + chr(10))
        for i2, c in enumerate(("honnin", "honnin_tei", "ima", "tsuma", "kachou", "douryou"), 1):
            fh.write(f"{i2}" + chr(9) + f"plate_{c}.png" + chr(10))
    with io.open(OUT / "realism17_TENFILE.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# video 17 — 112 canh AI theo CONG THUC REALISM (_media_library/realism_blocks.py)\n"
                 "# STILL -> Image (Nano Banana 2) -> chon anh -> ⋮ Animate -> MOTION (Veo 3.1). T2V = duong lui.\n"
                 "# Chon anh: dung boi canh 昭和? cast dung khuon mat? nguoi o NHIP 1? khong chu bia?\n"
                 "# clip_NN.mp4 = ten renderer DOC (theo so thu tu o trong SLIDES).\n"
                 "# CHU KY RUT: " + ", ".join(c + "=" + pick[c] for c in sorted(pick)) + "\n#\n"
                 "# idx  file            may     sang      boi canh        khoi   dai     y do\n")
        for i, r in enumerate(rows):
            fh.write("%3d\tclip_%02d.mp4\t%-6s\t%-8s\t%-13s\t%-5s\t%5.2fs\t%s\n"
                     % (i, i, r[1], r[2], r[3], r[4], r[5], r[6]))

    lock = sum(1 for r in rows if r[1] == "locked")
    print("video 17 REALISM — %d canh · may: KHOA %d (%.0f%%) / TROI %d (%.0f%%)"
          % (len(rows), lock, 100 * lock / len(rows), len(rows) - lock, 100 * (len(rows) - lock) / len(rows)))
    for k in ("still", "motion", "t2v"):
        L = [len(p) for p in out[k]]
        print("  %-6s: %d–%d ky, TB %d" % (k, min(L), max(L), sum(L) // len(L)))
    print("  vat ruc: %d cum, day nhat %d/%d" % (len(frag), max(frag.values()) if frag else 0, len(rows)))
    print("  anh sang: %s" % dict(Counter(r[2] for r in rows)))
    if not fails:
        reg[VIDEO_ID] = pick
        G.K.REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("GATE: " + ("✅ SACH" if not fails else "🔴 %d loi" % fails))
    print("-> %s/realism17_{STILL,MOTION,T2V}_FLOW.txt" % OUT)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
