# -*- coding: utf-8 -*-
r"""
build_remotion_22full.py — DUNG **TOAN BO** video 22 (未支給年金 36万円): 828,4s · 91 scene.

Khac ban demo `build_remotion_22i2v.py` o ba diem ban chat:
  1. **Khong con cua so scene**: chay het 0->90 (demo chi 0->18).
  2. **SHOTS SUY TU `plan22`, khong go tay**. Demo liet ke 12 khe bang tay; o day 62 khe la
     ket qua cua chinh phep chia clip cua `plan22` (gom scene `art` LIEN KE thanh KHOI roi
     chia deu) => builder va plan khong the lech nhau. Ten khe = `c22_<scene>[_<k>]`, dung
     ten ma `flow22_full` dat cho prompt va `ingest_c22` dat cho file.
     🔴 Day la ly do khong go tay: mot bang SHOTS viet tay se lech im lang moi lan
        `_TTS.md`/`_scenes22` doi (`feedback_gate_va_builder_phai_cung_ten`).
  3. **Du 4 the 原典 + 11 khoi gfx + 14 bang stat** (demo chi co 1 the 原典, 3 khoi gfx).

11 SCENE `gfx` — Remotion VE 100% bang font, KHONG gen bang Veo (`_scenes22` da ghi ly do:
Veo khong viet duoc tieng Nhat nen no tra ve hop mau + chu gia). Loi trong `GFX` duoi day
lay **verbatim tu chinh loi doc cua scene do** — YMYL: khong them mot so hay mot che do nao.
⏳ VIEC CON MO: cac scene nay dang la BANG CHU (`papercut-stat`), chua phai SO DO thuc su.
   remotion-vox chua co component INFOG/GAUGE (`grep preset` src/schema: chi co text/fx).
   Muon dung so do that thi phai viet component moi — ghi ra day de khong ai tuong da xong.

fps = 24 (clip Veo la 24fps, ep 30 thi 27% frame lap => judder).
Khe dai hon 8,000s => ha `speed = 8,0/khe`, **chi duoc lam CHAM** (CLAUDE.md §②).
"""
import io
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _scenes22 import SCENES, GENTEN as GT                          # noqa: E402
from plan22 import build                                            # noqa: E402

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-22full"
FPS, W, H = 24, 1920, 1080
VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
TL = os.path.join(VD, "timeline.json")
ASSETS = os.path.join(ROOT, "public", "projects", NAME, "assets")

SRC_SEC = 8.000
MASCOT_FRAMES = 192
FADE = 7
GRADE = {"brightness": 1.04, "contrast": 1.0, "saturate": 1.08}

f = lambda s: max(0, int(round(s * FPS)))

# ── 原典: moi khoa mot CHUOI TIET LO (doi CHO KHOANH, khong zoom) ────────────
# Moc lay o **ranh gioi CAU** cua chinh scene do (doc tu timeline), khong chia deu mu:
# the chua khoanh chay het cau "day la trang cua ...", the khoanh vao dung luc loi doc
# noi den noi dung duoc khoanh. Bang duoi la ti le trong scene (0..1) => builder tu doi
# ra giay, nen `_TTS.md` doi do dai thi moc tu chay theo.
GENTEN_STAGES = {
    13: [(0.00, "genten_shiharai.png"),          # 「こちらが、日本年金機構のページです」
         (0.145, "genten_shiharai_all.png"),     # 「赤で囲んだところを、ご覧ください」
         (0.431, "genten_shiharai_col.png"),     # 「年六回…偶数月の十五日に」
         (0.715, "genten_shiharai_row.png")],    # 「前月までの二か月分が…」
    32: [(0.00, "genten_gessuu.png"), (0.42, "genten_gessuu_box.png")],
    43: [(0.00, "genten_mynumber.png"), (0.40, "genten_mynumber_box.png")],
    79: [(0.00, "genten_ichiji.png"), (0.40, "genten_ichiji_box.png")],
}

# ── 11 KHOI gfx — loi VERBATIM tu narration cua chinh scene do ───────────────
# ⚖️ YMYL: khong mot con so / che do nao khong co trong loi doc.
# 📐 Nham >=3 dong (LUAT BA KHOI, `stage-zu-layout.md` §2) khi scene du dai; scene <5s
#    thi 2 dong cho khoi khong bi nen. `*` o dau dong = dong CHOT (preset to hon).
GFX = {
    9:  ["受け取っていい|お金", "返さなければ|ならないお金", "*見分けが|つかない"],
    10: ["日本年金機構|原典", "国税庁|原典", "*画面で|確かめます"],
    18: ["相続財産|ではない", "請求するのは|ご家族自身", "*ご自身の|権利として"],
    26: ["亡くなったのは|三月五日", "受け取れるのは|亡くなった月の分まで", "*だから|二月分も三月分も"],
    42: ["ここに|救いがひとつ", "*このあと|原典で確かめます"],
    50: ["順位だけでは|足りない", "*もうひとつ|条件がある"],
    72: ["数えはじめは|亡くなった日ではない", "*では|いつからか"],
    75: ["五年と二年|混同しやすい", "*ここだけ|覚えておく"],
    81: ["ほかに一時的な|収入があった年", "*合わせて|計算されます"],
    83: ["最後に|三つだけ", "*確かめて|みてください"],
    85: ["この内容|令和八年八月時点", "手続きと添付書類|記録によって変わります",
         "*ご判断の前に|年金事務所かねんきんダイヤル"],
}

# ── fx "hoa la canh": THUA + moi variant <=2 lan, gian it nhat 4 scene ──────
# 🔴 Bai hoc video 22d2/22i2v: dung `sparkle` 3/6 lan la nhin ra ngay. O day 12 fx tren
#    91 scene = 0,87/phut — no la DIEM NHAN, khong phai nhip.
# ⚖️ Chon cho theo NGHIA cua beat, khong rai deu mu:
FX = {
    2:  ("coins",    18, None),        # 「36万円が入った」 — tien vao so
    6:  ("vignette", 10, "full"),      # 「線はどこに」 — bat an, an o RIA nen khong che ai
    10: ("sparkle",  16, None),        # scene gfx 13,1s, nen kem phang thi te
    18: ("stampx",    1, "gfxleft"),   # 「相続財産ではない」 — ✗ dung nghia PHU DINH
    26: ("glow",     22, None),        # 「亡くなった月まで」 — dinh nghia dap xuong
    30: ("coins",    16, None),        # stat 「受け取れる金額」 — payoff 36万
    33: ("stampx",    1, "gfxleft"),   # stat 「こちらは受け取れない」 — PHU DINH thu hai
    42: ("rays",     14, None),        # 「救いがひとつ」 — tia sang dung nghia
    47: ("vignette", 10, "full"),      # 「請求しないと渡らない」 — canh bao
    50: ("sparkle",  14, None),        # gfx 「もうひとつ条件」
    74: ("confetti", 16, None),        # 「まだ間に合うかも」 — beat TIN VUI duy nhat
    83: ("rays",     12, None),        # gfx 「三つだけ確かめる」 — chot bai
}
FX_COLOR = {"stampx": "#1C2A4A"}       # ✗ navy, KHONG do (CLAUDE.md §②)
FX_AREA = {"gfxleft": {"x": 6, "y": 26, "w": 24, "h": 30},
           "full":    {"x": 0, "y": 0, "w": 100, "h": 100}}

# ── SCENE DUNG IT CLIP HON `plan22` cap — khai TUONG MINH, kem ly do ────────
# 🔴 Vi sao co co che nay: scene 31 「同じ36万円だが」 duoc cap 2 clip, va sau BA vong gen
#    khong lan nao ca HAI clip cung dung. Bang chung tung vong o khe `c22_31_1`:
#      v1 `36,0000` · v2 `360000` (dung gia tri, thieu dau phay) + cast KHONG phai nguoi Nhat
#      · v3 `36,000 360,000` (cast dung, nhung mot con so SAI GIA TRI)
#    Trong khi `c22_31_2` ra **hoan hao** ngay v2: `360,000 · 4/15 · 360,000`.
# ⇒ Thay vi nhan mot khiem khuyet, scene 31 dung **DUNG MOT clip** cho ca 9,7s. Doi lai la
#    `speed 0,825` — va do duoc la vo hai o clip nay: **MAD 1,08** (gan nhu tinh tuyet doi),
#    xem gate SPEED dong-hoa duoi day.
# ⚖️ Gia: nhip doi anh 62 -> 61 khe (4,49 -> 4,42/phut, van duoi tran 6). Doi lay **0 con so
#    sai tren man hinh** — YMYL thang luat nhip.
SHOT_OVERRIDE = {
    31: ["c22_31_2"],
}

POSE = ["owl_idle"]
PRESET = ["telop", "telop-gold", "telop"]


def quiet_side(asset: str) -> str:
    """Ben nao cua khung IT BAN hon — DO tren frame giua cua chinh clip dang chieu."""
    cap = cv2.VideoCapture(os.path.join(ASSETS, asset))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    cap.set(cv2.CAP_PROP_POS_FRAMES, n // 2)
    ok, fr = cap.read()
    cap.release()
    if not ok:
        return "right"
    g = cv2.cvtColor(cv2.resize(fr, (480, 270)), cv2.COLOR_BGR2GRAY)
    e = cv2.Laplacian(g, cv2.CV_64F)
    third = 480 // 3
    return ("left" if float(np.abs(e[20:250, 6:third]).sum())
            < float(np.abs(e[20:250, 480 - third:474]).sum()) else "right")


# ── HOP KHOI CHU + PHEP TU CO CO (audience-45plus.md §2.0f) ────────────────
# 🔴 BAT DUOC KHI DUYET MAT BAN RENDER CUOI (t=700s va t=780s) — khong gate nao thay:
#   ① hop cu `x=606 w=1100` co mep phai **1706**, ma CU chiem **x 1642-1905** => cu de len
#      ~64px cuoi cua moi o gia tri; dong nao chay sat mep la mat ky tu cuoi.
#   ② `papercut-stat` la `display:flex` co `maxWidth`: dong rong hon hop thi o bi **NEN va
#      chu WRAP BEN TRONG o** — 「…受け取れる」/「分」, 「記録によって変わ」/「ります」. Khong
#      tran ra ngoai khung nen khong lo, chi MAT THAY (dung §2.0f).
# ⇒ Vá o tang BUILDER (dung de engine nen):
#   · hop moi `x=300 w=1326` => mep phai **1626**, cach cot cu 16px; x=300 cung qua khoi
#     x-range cua SUBSCRIBE (20-260).
#   · **tu co co chu** cho toi khi dong dai nhat lot hop, roi lay min voi tran theo so dong.
# ⚠️ Scene co `stampx` (dau ✗ dap vao o `gfxleft` = frame x 115-576) phai chua cot TRAI
#    => dung hop hep hon, khong keo sang 300 duoc.
BLK_BOX = (300, 1326)              # x, w — mep phai 1626
BLK_BOX_FX = (606, 1020)           # scene co stampx: chua cot trai cho dau ✗
BLK_CAP = {2: 84, 3: 76, 4: 66}    # tran co chu theo so dong (§2.0c), con lai 60
BLK_SAFE = 1.06                    # bien an toan do duoc cua preset (§2.0f)


def _w_em(t: str) -> float:
    """Be rong uoc theo 'em': full-width JP ~1,0 · ASCII ~0,55 (§2.0f)."""
    return sum(0.55 if ord(c) < 0x3000 else 1.0 for c in t)


def blk_size(lines, w_avail: int, nl: int):
    """(co chu, dong chat nhat) — co lon nhat ma MOI dong lot `w_avail`.

    Hinh hoc cua `papercut-stat` doc TU `TextClip.tsx`, khong doan:
        row = [label fontSize 0,82s] + gap 0,34s
              + [o gia tri fontSize s, padding ngang 0,18s moi ben, minWidth 4,6s]
    => can  0,82*Wlabel + 0,34 + max(4,6, Wval + 0,36) <= w_avail / s
    """
    worst, who = 0.0, ""
    for ln in lines:
        b = ln.strip()
        if b.startswith("*"):
            b = b[1:]
        lab, _, val = b.partition("|")
        need = 0.82 * _w_em(lab.strip())
        if val.strip():
            need += 0.34 + max(4.6, _w_em(val.strip()) + 0.36)
        if need > worst:
            worst, who = need, b
    fit = int((w_avail / BLK_SAFE) / worst) if worst else 99
    return min(BLK_CAP.get(nl, 60), fit), who


def mad_of(asset: str) -> float:
    """Chuyen dong frame-to-frame cua clip (MAD tren ban 320x180, lay 1 frame/2).

    Dung de **san speed thanh dong-hoa**: mot cu 'lam cham' chi lo khi trong khung co
    chuyen dong that. Clip locked-off, nguoi ngoi yen nhin man hinh (MAD ~1) thi
    `speed 0,82` mat khong thay; clip co nguoi vung tay (MAD >3) thi thay ngay.
    📌 Cung thuoc do dung o `animate_still.py`/showa, nen khong dat ra don vi moi.
    """
    cap = cv2.VideoCapture(os.path.join(ASSETS, asset))
    prev, ds, i = None, [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % 2 == 0:
            g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
            if prev is not None:
                ds.append(float(np.abs(g - prev).mean()))
            prev = g
        i += 1
    cap.release()
    return float(np.mean(ds)) if ds else 99.0


# san speed: 0,92 cho canh CO chuyen dong; 0,80 cho canh gan nhu tinh (MAD < 2,5)
SPEED_FLOOR, SPEED_FLOOR_STATIC, MAD_STATIC = 0.92, 0.80, 2.5


def enter_of(k: int, n_fam: dict) -> dict:
    """Loi VAO cua khe footage thu `k` — xoay 3 HO, trong moi ho xoay huong/do dai.

    Chi so dem theo **so lan HO DO da dung**, khong theo chi so vong lap ngoai:
    `x % N` chi phu het N gia tri khi `x` chay LIEN TUC (bug da sua o ban 22i2v).
    """
    if k == 0:
        return {}
    fam = ["fade", "curl", "wipe"][(k - 1) % 3]
    j = n_fam[fam]
    n_fam[fam] += 1
    if fam == "curl":
        return {"curlInFrames": [13, 15, 11, 14][j % 4],
                "curlDir": ["br", "tr", "bl", "tl"][j % 4]}
    if fam == "wipe":
        return {"wipeInFrames": [10, 12, 9, 11][j % 4],
                "wipeDir": ["left", "up", "right", "down"][j % 4]}
    return {"fadeInFrames": [7, 10, 5, 8][j % 4]}


def split_caption(text: str, maxlen: int = 78):
    """Che khoi phu de <=78 ky, cat SAU dau cau (Remotion khong che ho)."""
    if len(text) <= maxlen:
        return [text]
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。、」）" and len(cur) >= maxlen * 0.55:
            out.append(cur)
            cur = ""
        elif len(cur) >= maxlen:
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out


def shot_runs(rows):
    """(khe footage) -> [(t0, t1, stem, scene_chu)] — chia deu theo **KHOI**, khong theo scene.

    KHOI = day scene `art` LIEN KE (chen mot the stat/genten vao giua la cat khoi — luc do
    footage that su bi ngat tren man hinh). Ten khe van la ten `plan22`/`flow22_full` dat
    (`c22_<scene>[_<k>]`), chi CHO DAT tren truc thoi gian la chia deu trong khoi.

    🔴 VI SAO KHONG NEO TUNG KHE VAO SCENE CHU CUA NO (ban dau da lam vay va phai bo):
       `plan22` cap clip cho TUNG scene bang lam tron, nen trong cung mot khoi co scene
       11,7s duoc 1 clip trong khi scene 7,8s duoc 2 clip. Neo theo scene thi khe dai nhat
       thanh **11,7s** => `speed = 8,0/11,7 = 0,685`, tuc slow-motion nhin ra ngay (san la
       0,92 — CLAUDE.md §②). Va scene DAU cua mot khoi co the nhan `nshot=0` (scene 19·51·61)
       => neo theo scene thi ba scene do **khong co hinh nao**, gate "vung giua" bao do.
       Chia deu trong khoi chua ca hai: khe dai nhat **8,61s => speed 0,929** (dat san), va
       khoi luon duoc phu tu t0.
    ⚖️ Gia phai tra, do duoc: clip len song som hon scene chu toi da **3,9s**. Nhung
       **0/62 clip roi ra ngoai scene chu qua nua** (gate `ALIGN` duoi day chan cung), va
       trong mot khoi thi cac scene lien ke cung mot beat nen hinh khong lech noi dung.
    """
    idxs = sorted(rows)
    blocks, cur = [], []
    for i in idxs:
        if rows[i]["kind"] == "art":
            cur.append(rows[i])
        else:
            if cur:
                blocks.append(cur)
                cur = []
    if cur:
        blocks.append(cur)

    runs = []
    for blk in blocks:
        owners = []
        for r in blk:
            if r["i"] in SHOT_OVERRIDE:                 # scene khai tuong minh so clip
                for stem in SHOT_OVERRIDE[r["i"]]:
                    owners.append((stem, r))
                continue
            for k in range(r["nshot"]):
                suf = f"_{k+1}" if r["nshot"] > 1 else ""
                owners.append((f"c22_{r['i']:02d}{suf}", r))
        if not owners:
            continue
        t0, t1 = blk[0]["t0"], blk[-1]["t1"]
        step = (t1 - t0) / len(owners)
        for k, (stem, r) in enumerate(owners):
            runs.append((t0 + k * step, t0 + (k + 1) * step, stem, r["i"]))
    return runs


def main() -> int:
    rows = {r["i"]: r for r in build()}
    idxs = sorted(rows)
    total = rows[idxs[-1]]["t1"]
    errs = []

    runs = shot_runs(rows)
    # scene -> khe dang chieu GIUA scene do (de do `quiet_side`, de gate "vung giua").
    # Tra theo THOI GIAN, khong theo scene-chu: mot khe co the trai qua 2 scene.
    on_air = {}
    for i in idxs:
        mid = (rows[i]["t0"] + rows[i]["t1"]) / 2
        for a, b, stem, _sc in runs:
            if a <= mid < b:
                on_air[i] = stem
                break

    trk_v, trk_g, trk_blk, trk_fx, trk_t, markers, poses = [], [], [], [], [], [], []
    n_fam = {"fade": 0, "curl": 0, "wipe": 0}
    n_side = {"left": 0, "right": 0}
    used, slow, slow_mad, blk_fs = [], [], [], []

    # ── track footage: mot clip / khe ────────────────────────────────────────
    for k, (a, b, stem, sc) in enumerate(runs):
        khe = b - a
        speed = round(min(1.0, SRC_SEC / khe), 4)
        # GATE SPEED dong-hoa: san 0,92; clip gan nhu TINH thi ha san ve 0,80 —
        # va phai DO, khong duoc mien bang phan doan (xem `mad_of`).
        if speed < SPEED_FLOOR:
            m = mad_of(f"{stem}.mp4")
            floor = SPEED_FLOOR_STATIC if m < MAD_STATIC else SPEED_FLOOR
            slow_mad.append((stem, speed, round(m, 2), floor))
            if speed < floor:
                errs.append(f"khe {stem} (scene {sc}) dai {khe:.1f}s can speed {speed} < "
                            f"{floor} (MAD {m:.2f}) => slow-motion nhin ra duoc. "
                            f"Cap them clip cho khoi nay.")
        # GATE ALIGN: khe phai nam trong scene chu >= 50% (xem docstring shot_runs)
        r_own = rows[sc]
        ov = max(0.0, min(b, r_own["t1"]) - max(a, r_own["t0"]))
        if ov < 0.5 * min(khe, r_own["dur"]) - 1e-6:
            errs.append(f"khe {stem} ({a:.1f}-{b:.1f}) chi phu {ov:.1f}s cua scene {sc} "
                        f"({r_own['t0']:.1f}-{r_own['t1']:.1f}) — hinh lech loi")
        if speed < 1.0:
            slow.append((stem, speed))
        head = SRC_SEC / speed - khe
        ext = FADE if head >= FADE / FPS and k < len(runs) - 1 else 0
        trk_v.append({
            "id": f"v{k}", "kind": "video", "from": f(a),
            "durationInFrames": f(khe) + ext,
            "asset": f"assets/{stem}.mp4", "fit": "cover", "motion": "none",
            "speed": speed, "volume": 0, "filter": GRADE,
            **enter_of(k, n_fam),
        })
        used.append(stem)

    # ── moi scene: telop + (stat|gfx|genten) + fx ───────────────────────────
    for n, i in enumerate(idxs):
        r = rows[i]
        s0, dur = r["t0"], r["dur"]
        markers.append({"id": f"m{i}", "atFrame": f(s0),
                        "label": r["telop"].replace("\n", " ")})
        poses.append({"atSec": s0, "asset": f"assets/{POSE[n % len(POSE)]}/f_%04d.png"})

        is_blk = r["kind"] in ("stat", "gfx")
        is_gt = r["kind"] == "genten"
        has_v = i in on_air

        # GATE 1: dung MOT thu o vung giua
        if sum([has_v, is_blk, is_gt]) != 1:
            errs.append(f"scene {i} ({r['kind']}): {sum([has_v, is_blk, is_gt])} lop o vung "
                        f"giua (footage={has_v} block={is_blk} genten={is_gt})")
            continue

        if is_gt:
            if i not in GENTEN_STAGES:
                errs.append(f"scene {i}: genten khong co trong GENTEN_STAGES")
                continue
            st = GENTEN_STAGES[i]
            for k, (frac, asset) in enumerate(st):
                at = s0 + frac * dur
                end = s0 + st[k + 1][0] * dur if k + 1 < len(st) else r["t1"]
                if end - at > 9.05:
                    errs.append(f"scene {i}: chang 原典 {k} dai {end-at:.1f}s > 9,0s "
                                f"(gate ② check_frame_pace) — them mot chang")
                trk_g.append({
                    "id": f"g{i}_{k}", "kind": "video", "from": f(at),
                    "durationInFrames": f(end - at), "asset": f"assets/{asset}",
                    # 🔴 motion "none" cho MOI chang: the 原典 duoc dung SAN o dung
                    #    1920x1080 (make_genten_22b), nen `pan` la keo mot anh vua khung
                    #    => **cat mat bang chung** o mep trai/phai. Bat duoc tren still
                    #    frame 5760 (the 機構はこう書く bi mat chu dau moi dong).
                    #    Ban demo khong lo vi bang chi rong 1350 dat o x275, con lai le;
                    #    ban nay rong 1600 o x40 nen pan la cat ngay.
                    #    Su kien hinh cua scene 原典 den tu DOI CHO KHOANH, khong tu pan.
                    "fit": "cover", "motion": "none",
                    "speed": 1.0, "volume": 0, "fadeInFrames": FADE if k == 0 else 0,
                })
        elif is_blk:
            lines = GFX[i] if r["kind"] == "gfx" else SCENES[i][3]
            if r["kind"] == "gfx" and i not in GFX:
                errs.append(f"scene {i}: gfx khong co khoi chu trong GFX")
                continue
            nl = len(lines)
            bx, bw = BLK_BOX_FX if (i in FX and FX[i][2] == "gfxleft") else BLK_BOX
            fs, worst = blk_size(lines, bw, nl)
            if fs < 40:
                errs.append(f"scene {i}: khoi chu phai co ve {fs}px moi lot hop "
                            f"{bw}px — qua nho cho tep 45+. Dong chat nhat: "
                            f"«{worst}». Rut ngan loi.")
            blk_fs.append((i, nl, fs, BLK_CAP.get(nl, 60), worst))
            top = int((250 + 860) / 2 - nl * fs * 1.55 / 2)
            trk_blk.append({
                "id": f"b{i}", "kind": "text", "from": f(s0) + 8,
                "durationInFrames": max(12, f(dur) - 12),
                "content": "\n".join(lines), "preset": "papercut-stat",
                "color": "#1C2A4A", "animation": "none",
                "layout": {"x": bx, "y": top, "w": bw}, "fontSize": fs,
            })

        trk_t.append({
            "id": f"t{i}", "kind": "text", "from": f(s0) + 3,
            "durationInFrames": max(8, f(dur) - 5),
            "content": r["telop"],
            "preset": "telop-band" if (is_blk or is_gt) else PRESET[n % 3],
            "color": "#FFD34E", "animation": "pop", "layout": {}, "fontSize": None,
        })

        if i in FX:
            variant, dens, area_kind = FX[i]
            if has_v:
                side = quiet_side(on_air[i] + ".mp4")
            else:
                # scene khoi chu/原典: khoi nam o x 606+ nen cot TRAI trong
                side = "left" if n_side["left"] <= n_side["right"] else "right"
            trk_fx.append({
                "id": f"fx{i}", "kind": "fx", "from": f(s0) + 6,
                "durationInFrames": max(12, f(dur) - 12),
                "variant": variant, "density": dens,
                "color": FX_COLOR.get(variant, "#FFC83A"), "seed": 100 + i * 7,
                # 🔴 Goc PHAI-DUOI la cho cua MASCOT (y~594-894) => cot phai chi dung NUA TREN.
                "area": (FX_AREA[area_kind] if area_kind else
                         ([{"x": 2, "y": 8, "w": 32, "h": 84},
                           {"x": 4, "y": 4, "w": 30, "h": 44},
                           {"x": 6, "y": 40, "w": 28, "h": 48}][n_side["left"] % 3]
                          if side == "left" else
                          [{"x": 66, "y": 6, "w": 30, "h": 40},
                           {"x": 64, "y": 34, "w": 32, "h": 52},
                           {"x": 68, "y": 14, "w": 26, "h": 62}][n_side["right"] % 3])),
                "opacity": 1, "fadeInFrames": 8, "fadeOutFrames": 10, "dir": "upright",
            })
            if not area_kind:
                n_side[side] += 1

    # ── GATE 2: MOI scene phai co telop (khuon video 22 = telop ~100%) ───────
    if len(trk_t) != len(idxs):
        errs.append(f"chi {len(trk_t)}/{len(idxs)} scene co telop — thieu: "
                    f"{sorted(set(idxs) - {int(c['id'][1:]) for c in trk_t})}")

    # ── GATE 3: khong dung lai clip trong cung video ─────────────────────────
    dup = sorted({c for c in used if used.count(c) > 1})
    if dup:
        errs.append(f"clip dung lai trong cung video: {dup}")

    # ── GATE 4: asset phai CO THAT (render-background §1.5) ─────────────────
    for c in trk_v + trk_g:
        if not os.path.exists(os.path.join(ROOT, "public", "projects", NAME, c["asset"])):
            errs.append(f"thieu asset {c['asset']}")

    # ── GATE 4b: hop khoi chu khong duoc lan CU (x>=1642) hay SUBSCRIBE (x<=260) ──
    for c in trk_blk:
        x0, w0 = c["layout"]["x"], c["layout"]["w"]
        if x0 + w0 > 1626:
            errs.append(f"{c['id']}: hop chu {x0}-{x0+w0} lan cot MASCOT (x>=1642)")
        if x0 < 280:
            errs.append(f"{c['id']}: hop chu bat dau {x0} < 280, lan nut SUBSCRIBE")

    # ── GATE 5: khoi gfx/genten phai phu du 4 khoa + 11 scene gfx ───────────
    gfx_sc = sorted(i for i in idxs if rows[i]["kind"] == "gfx")
    if sorted(GFX) != gfx_sc:
        errs.append(f"GFX khai {sorted(GFX)} nhung scene gfx that la {gfx_sc}")
    gt_sc = sorted(i for i in idxs if rows[i]["kind"] == "genten")
    if sorted(GENTEN_STAGES) != gt_sc:
        errs.append(f"GENTEN_STAGES khai {sorted(GENTEN_STAGES)} nhung scene genten "
                    f"that la {gt_sc}")

    # ── phu de: ca bai, goc 0 ────────────────────────────────────────────────
    lines = json.load(io.open(TL, encoding="utf-8"))["lines"]
    cap = []
    for ln in lines:
        parts = split_caption(ln["text"])
        span = (ln["end"] - ln["start"]) / max(1, sum(len(p) for p in parts))
        t = ln["start"]
        for p in parts:
            d = span * len(p)
            cap.append({"text": p, "startMs": round(t * 1000),
                        "endMs": round((t + d) * 1000)})
            t += d
    bad = [c for c in cap if len(c["text"]) > 78]
    if bad:
        errs.append(f"{len(bad)} khoi phu de > 78 ky")

    if errs:
        print("\nGATE DO:")
        for e in errs[:30]:
            print("  ", e)
        return 1

    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": None,
                 "fps": FPS, "width": W, "height": H, "createdAt": "", "modifiedAt": ""},
        "timeline": {"durationInFrames": f(total)},
        "sceneMarkers": markers,
        "tracks": [
            {"id": "trk-video", "name": "footage t2v", "type": "video", "clips": trk_v},
            {"id": "trk-genten", "name": "genten", "type": "video", "clips": trk_g},
            {"id": "trk-fx", "name": "hoa la canh", "type": "fx", "clips": trk_fx},
            {"id": "trk-stat", "name": "khoi chu font", "type": "text", "clips": trk_blk},
            {"id": "trk-telop", "name": "telop", "type": "text", "clips": trk_t},
            {"id": "trk-audio", "name": "voice", "type": "audio", "clips": [
                {"id": "a0", "kind": "audio", "from": 0, "durationInFrames": f(total),
                 "asset": "assets/voice.wav", "volume": 1, "trimStartFrames": 0}]},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44, "lines": cap, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236", "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F3EAD8"},
        "brand": {
            "logo": "assets/brand_logo.png", "mascot": None, "mascotPoses": poses,
            "mascotVideo": poses[0]["asset"], "mascotVideoFrames": MASCOT_FRAMES,
            "mascotH": 300, "logoH": 110, "subscribe": True,
            # Con so DO tren ban render demo, khong doan — xem build_remotion_22i2v.py:
            #   phu de 2 dong: y 908-1013 (va rong toi x 1765)
            #   cu cao 300 + bob ±6 => day toi da = 908 - 8 le - 6 bob = 894 => offset 186
            "bottomOffset": 186,
            #   con tro chuot nam 18px DUOI nut + no x1,12 => day = 1080 - offset + 20
            #   muon day <= 900 thi offset >= 200
            "subscribeBottom": 200,
        },
    }
    out = os.path.join(ROOT, "projects", NAME, "project.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(json.dumps(proj, ensure_ascii=False, indent=1))

    print(f"\nOK {out}")
    print(f"   {len(idxs)} scene · {total:.1f}s = {total/60:.2f}' @ {FPS}fps")
    print(f"   footage {len(trk_v)} khe · genten {len(trk_g)} chang · khoi chu "
          f"{len(trk_blk)} ({len(GFX)} gfx + {len(trk_blk)-len(GFX)} stat) · "
          f"fx {len(trk_fx)} · telop {len(trk_t)} · phu de {len(cap)} khoi")
    print(f"   nhip doi anh chinh: {len(trk_v)/(total/60):.2f}/phut (tran 6) "
          f"— genten tinh track rieng")
    print(f"   khe phai lam cham: {len(slow)} khe, cham nhat "
          f"{min([s for _, s in slow], default=1.0)}")
    for st, sp, m, fl in slow_mad:
        print(f"     duoi san 0,92: {st} speed {sp} · MAD {m} · san ap dung {fl}")
    shrunk = [r for r in blk_fs if r[2] < r[3]]
    print(f"   khoi chu: {len(blk_fs)} khoi · {len(shrunk)} khoi phai CO CO de lot hop")
    for i2, nl2, fs2, cap2, wo in shrunk:
        print(f"     scene {i2:>2} ({nl2} dong): {cap2} -> {fs2}px | chat nhat «{wo[:40]}»")
    if SHOT_OVERRIDE:
        print(f"   SHOT_OVERRIDE: {SHOT_OVERRIDE} (scene dung it clip hon plan22 cap)")
    print(f"   clip dung: {len(set(used))} khac nhau, khong lap")
    import collections
    vc = collections.Counter(v for v, _, _ in FX.values())
    print(f"   fx: {dict(vc)} — moi variant <= {max(vc.values())} lan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
