# -*- coding: utf-8 -*-
r"""
build_remotion_23.py — dung TOAN BO video 23 (年金請求書が届かない): 953,5s · 118 scene.

Khuon = `build_remotion_22full.py` (telop + hoa-la-canh + 3 overlay), doi BA diem:

  1. **Lop hinh la VOX PAPER-COLLAGE**, khong con footage AI nguoi that (CLAUDE.md §②,
     user chot 2026-09-12). Khong doi gi trong builder — chi la clip nguon khac.
  2. **KHO CLIP LA NGUON SU THAT, khong phai `plan23.nshot`** (user chot khi ingest lo nay).
     `plan23` cap 85 clip theo do dai scene; lo da gen la **92 clip**, va bang phan bo cua no
     nam trong `vox23_TENFILE.txt`. Builder doc THANG file do.
     🔴 Vi sao an toan: `shot_runs` rai clip deu tren **KHOI** scene `art` lien ke, ma thanh
        vien cua khoi CHI phu thuoc `kind` — khong phu thuoc `nshot`. Da do: khe dai nhat
        8,70s => speed **0,92** = dung san, khong khe nao phai lam cham qua muc.
     ⚠️ Ke tu day `plan23.nshot` chi con la GOI Y. Muon quay ve dung plan thi phai gen bu
        ~10 khe moi (57a·63a·66a·69a·71a·99a·100a/b·61b/c·74b·89b) va bo 7 clip — xem README
        cua lo trong `06_VIDEO/23_.../`.
  3. **Scene `formula`** dung preset `papercut-formula` (video 22 khong co scene nay).

🔴 LECH MOT DONG DA SUA TRUOC KHI DUNG (2026-09-13): scene 20 (`stat 権利の時効`) phai om
   HAI dong timeline vi the ghi ca 国民年金法第百二条 lan 厚生年金保険法第九十二条; bang scene
   cu khai scene 21 bat dau o dong 21 => scene 21..102 tut mot dong, telop di TRUOC loi doc
   suot tu phut 3 den phut 13. Da lui +1 (`_scenes23.py`, backup `.bak_lnshift`).
   ⚠️ `plan23` GATE 1 KHONG bat duoc: no chi kiem SO DONG (124), khong kiem dong nao thuoc
   scene nao — dung cai bay chinh docstring cua no canh bao.

fps = 24 (clip nguon 24fps, ep 30 thi 27% frame lap => judder).
"""
import io
import json
import os
import re
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flow23_full                                                  # noqa: E402,F401
from _scenes23 import SCENES, GENTEN                                # noqa: E402
from plan23 import build                                            # noqa: E402

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-23"
FPS, W, H = 24, 1920, 1080
VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\23_nenkin-seikyusho-todokanai")
TL = os.path.join(VD, "timeline.json")
TENFILE = os.path.join(VD, "vox23_TENFILE.txt")
ASSETS = os.path.join(ROOT, "public", "projects", NAME, "assets")

SRC_SEC = 8.000
MASCOT_FRAMES = 192
FADE = 7
GRADE = {"brightness": 1.04, "contrast": 1.0, "saturate": 1.08}

f = lambda s: max(0, int(round(s * FPS)))

# ── 原典: khoa GENTEN cua `_scenes23` -> the da dung san trong `genten/` ─────
# Mot the = mot anh 1920x1080 dung san (`make_genten_23.py`), `motion: "none"` — pan la
# CAT MAT BANG CHUNG (luat ④ cua make_genten_23).
GT_ASSET = {
    "nenkin_soufu":    "genten_soufu.png",
    "kikou_10nen":     "genten_kikou10.png",
    "nenkin_saisoufu": "genten_saisoufu.png",
    "nenkin_tokubetsu": "genten_tokubetsu.png",
    "nenkin_horyu":    "genten_horyu.png",
    "nenkin_zenjitsu": "genten_zenjitsu.png",
    "nenkin_shiharai": "genten_shiharai.png",
}
# Scene 原典 DAI hon 9,0s thi mot tam dung yen la "frame dung yen" that
# (`audience-45plus.md` §2.0i — trk-genten VAN bi tinh o gate ②). Su kien hinh phai den tu
# **doi cho khoanh**, khong tu pan (make_genten_23 luat ④).
# ⇒ Chang 1 = ban CHUA KHOANH (`_plain`, cung vung cat tuyet doi), chang 2 = ban da khoanh.
#   Khop dung nhip loi doc: 「機構のページです」 (trang) → 「…と書かれています」 (khoanh vao cau).
#   Chon `_plain` thay vi mot CHO KHOANH khac vi cho khoanh khac se lo noi dung cua scene
#   con chua toi (vd 3 loi thay the o scene 57-60) — di truoc loi doc, dung cai vua sua.
GT_PLAIN = {38: 0.42, 54: 0.45, 72: 0.40}   # scene -> ti le doi sang ban DA KHOANH

# ── 8 KHOI gfx — loi VERBATIM tu narration cua CHINH scene do ───────────────
# ⚖️ YMYL: khong mot con so / che do nao khong co trong loi doc cua scene ay.
# 📐 Nham >=3 dong (LUAT BA KHOI) khi scene du dai; scene <3s thi 1-2 dong cho khoi
#    khong bi nen. `*` dau dong = dong CHOT.
GFX = {
    6:   ["一|いつ届くのか", "二|届かないのはどなたか", "*三|出し忘れると何が起きるか"],
    7:   ["*まず|事実から"],
    29:  ["二つ目|届かないかた", "*理由は|ひとつではない"],
    56:  ["*道は|三つ"],
    83:  ["はがきの期限|あります", "*期限|誕生月の末日"],
    92:  ["いつから出せる|誕生日の前日以降", "*前に出すと|受け付けられない"],
    109: ["*最後に|三つだけ確かめる"],
    111: ["時点|令和八年九月", "手続き・添付書類|記録によって変わる",
          "*ご判断の前に|年金事務所かねんきんダイヤル"],
}

# ── fx "hoa la canh": THUA + moi variant <=2 lan, gian it nhat 4 scene ──────
# 12 fx tren 118 scene = 0,76/phut — DIEM NHAN, khong phai nhip.
FX = {
    2:   ("coins",    18, None),      # 「百五十六万円です」 — tien vao mot cuc
    6:   ("sparkle",  16, None),      # gfx mo bai 11,8s, nen phang thi te
    16:  ("stampx",    1, "gfxleft"),  # 「出さなければ、一円も動きません」 — PHU DINH
    24:  ("glow",     22, None),      # 「四年分、百五十六万円」 — dinh nghia dap xuong
    33:  ("rays",     14, None),      # 「そこが、逆なんです」 — loi thoat hien ra
    42:  ("vignette", 10, "full"),    # 「その二回とも逃す」 — canh bao
    55:  ("stampx",    1, "gfxleft"),  # 「再送付できない」 — PHU DINH thu hai
    56:  ("sparkle",  14, None),      # gfx 「道は三つ」
    61:  ("confetti", 16, None),      # 「間に合った」 — beat TIN VUI
    87:  ("vignette", 10, "full"),    # 「年金の支払いが止まる」 — canh bao nang nhat
    104: ("coins",    16, None),      # 「生活費の空白」 — tien lai la nhan vat
    109: ("rays",     12, None),      # gfx 「三つだけ確かめる」 — chot bai
}
FX_COLOR = {"stampx": "#1C2A4A"}      # ✗ navy, KHONG do (CLAUDE.md §②)
FX_AREA = {"gfxleft": {"x": 6, "y": 26, "w": 24, "h": 30},
           "full":    {"x": 0, "y": 0, "w": 100, "h": 100}}

POSE = ["owl_idle"]
PRESET = ["telop", "telop-gold", "telop"]

# ── HOP KHOI CHU + PHEP TU CO CO (audience-45plus.md §2.0f) ────────────────
# Hop phai tranh CU (x>=1642) va nut SUBSCRIBE (x<=260) — xem build_remotion_22full §4b.
BLK_BOX = (300, 1326)              # x, w — mep phai 1626
BLK_BOX_FX = (606, 1020)           # scene co stampx: chua cot trai cho dau ✗
BLK_CAP = {1: 92, 2: 84, 3: 76, 4: 66}
BLK_SAFE = 1.06                    # bien an toan do duoc cua preset (§2.0f)


def read_inventory():
    """scene -> [ten khe] LAY TU LO DA GEN (`vox23_TENFILE.txt`), khong tu plan23.

    Day la diem khac ban chat so voi builder 22 — xem docstring dau file.
    """
    inv = {}
    rx = re.compile(r"^dong\s+\d+\s*->\s*clips/(clip_(\d+)[a-z])\.mp4")
    for ln in io.open(TENFILE, encoding="utf-8"):
        m = rx.match(ln.strip())
        if m:
            inv.setdefault(int(m.group(2)), []).append(m.group(1))
    return inv


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


def _w_em(t: str) -> float:
    """Be rong uoc theo 'em': full-width JP ~1,0 · ASCII ~0,55 (§2.0f)."""
    return sum(0.55 if ord(c) < 0x3000 else 1.0 for c in t)


def blk_size(lines, w_avail: int, nl: int):
    """(co chu, dong chat nhat) — co lon nhat ma MOI dong lot `w_avail`.

    Hinh hoc `papercut-stat` doc tu `TextClip.tsx`:
        row = [label 0,82s] + gap 0,34s + [o gia tri s, padding 0,18s moi ben, minW 4,6s]
    """
    worst, who = 0.0, ""
    for ln in lines:
        b = ln.strip().lstrip("*")
        lab, _, val = b.partition("|")
        need = 0.82 * _w_em(lab.strip())
        if val.strip():
            need += 0.34 + max(4.6, _w_em(val.strip()) + 0.36)
        if need > worst:
            worst, who = need, b
    fit = int((w_avail / BLK_SAFE) / worst) if worst else 99
    return min(BLK_CAP.get(nl, 60), fit), who


def mad_of(asset: str) -> float:
    """Chuyen dong frame-to-frame cua clip (MAD tren ban 320x180, 1 frame/2).

    Dung de **san speed thanh dong-hoa**: 'lam cham' chi lo khi trong khung co chuyen
    dong that.
    """
    cap = cv2.VideoCapture(os.path.join(ASSETS, asset))
    prev, ds, i = None, [], 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % 2 == 0:
            g = cv2.cvtColor(cv2.resize(fr, (320, 180)),
                             cv2.COLOR_BGR2GRAY).astype(np.float32)
            if prev is not None:
                ds.append(float(np.abs(g - prev).mean()))
            prev = g
        i += 1
    cap.release()
    return float(np.mean(ds)) if ds else 99.0


SPEED_FLOOR, SPEED_FLOOR_STATIC, MAD_STATIC = 0.92, 0.80, 2.5


def enter_of(k: int, n_fam: dict) -> dict:
    """Loi VAO cua khe hinh thu `k` — xoay 3 HO, trong moi ho xoay huong/do dai."""
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


def shot_runs(rows, inv):
    """(khe hinh) -> [(t0, t1, stem, scene_chu)] — chia deu theo **KHOI**, khong theo scene.

    KHOI = day scene `art` LIEN KE. Ten khe lay tu KHO (`vox23_TENFILE.txt`), cho dat tren
    truc thoi gian la chia deu trong khoi — xem docstring dau file ve ly do khong dung
    `plan23.nshot`.
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
        owners = [(stem, r) for r in blk for stem in inv.get(r["i"], [])]
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

    inv = read_inventory()
    n_inv = sum(len(v) for v in inv.values())
    runs = shot_runs(rows, inv)
    if len(runs) != n_inv:
        errs.append(f"kho co {n_inv} clip nhung chi xep duoc {len(runs)} khe — "
                    f"co scene trong kho khong phai scene `art`")

    # scene -> khe dang chieu GIUA scene do. Tra theo THOI GIAN, khong theo scene-chu.
    on_air = {}
    for i in idxs:
        mid = (rows[i]["t0"] + rows[i]["t1"]) / 2
        for a, b, stem, _sc in runs:
            if a <= mid < b:
                on_air[i] = stem
                break

    trk_v, trk_g, trk_blk, trk_fm, trk_fx, trk_t = [], [], [], [], [], []
    markers, poses = [], []
    n_fam = {"fade": 0, "curl": 0, "wipe": 0}
    n_side = {"left": 0, "right": 0}
    used, slow, slow_mad, blk_fs, drift = [], [], [], [], []

    # ── track hinh: mot clip / khe ──────────────────────────────────────────
    for k, (a, b, stem, sc) in enumerate(runs):
        khe = b - a
        speed = round(min(1.0, SRC_SEC / khe), 4)
        if speed < SPEED_FLOOR - 1e-3:
            m = mad_of(f"{stem}.mp4")
            floor = SPEED_FLOOR_STATIC if m < MAD_STATIC else SPEED_FLOOR
            slow_mad.append((stem, speed, round(m, 2), floor))
            if speed < floor - 1e-3:
                errs.append(f"khe {stem} (scene {sc}) dai {khe:.1f}s can speed {speed} < "
                            f"{floor} (MAD {m:.2f}) => slow-motion nhin ra duoc.")
        # ── GATE ALIGN: **bao cao**, khong chan cung — va day la mot DANH DOI CO Y ────
        # Kho clip (92) duoc cap phat theo bang scene CU (truoc khi sua lech mot dong), nen
        # trong vai KHOI, scene nao do co it clip hon muc do dai da sua doi hoi. Chia deu
        # trong khoi van giu speed >= 0,92 va khong bao gio cho clip ra ngoai KHOI cua no,
        # nhung mot so clip len song som/muon hon scene-chu vai giay.
        # ⇒ Neo tung clip vao dung scene cua no thi phai gen them **26 clip** (do duoc), va
        #   ha speed xuong toi 0,29 o scene 61 (28,0s / 1 clip) ⇒ slow-motion nhin ra ngay.
        #   Chia deu la phuong an re nhat khong sinh slow-motion. Danh sach lech in o cuoi.
        r_own = rows[sc]
        ov = max(0.0, min(b, r_own["t1"]) - max(a, r_own["t0"]))
        if ov < 0.5 * min(khe, r_own["dur"]) - 1e-6:
            drift.append((stem, sc, round(a, 1), round(r_own["t0"], 1),
                          round(r_own["t0"] - a, 1)))
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

    # ── moi scene: telop + (stat|gfx|formula|genten) + fx ───────────────────
    for n, i in enumerate(idxs):
        r = rows[i]
        s0, dur = r["t0"], r["dur"]
        markers.append({"id": f"m{i}", "atFrame": f(s0),
                        "label": r["telop"].replace("\n", " ")})
        poses.append({"atSec": s0, "asset": f"assets/{POSE[n % len(POSE)]}/f_%04d.png"})

        is_blk = r["kind"] in ("stat", "gfx")
        is_fm = r["kind"] == "formula"
        is_gt = r["kind"] == "genten"
        has_v = i in on_air

        # GATE 1: vung giua chi chor DUNG MOT thu
        if sum([has_v, is_blk, is_fm, is_gt]) != 1:
            errs.append(f"scene {i} ({r['kind']}): {sum([has_v, is_blk, is_fm, is_gt])} lop "
                        f"o vung giua (footage={has_v} block={is_blk} formula={is_fm} "
                        f"genten={is_gt})")
            continue

        if is_gt:
            key = SCENES[i][3]
            if key not in GT_ASSET:
                errs.append(f"scene {i}: khoa genten «{key}» khong co the trong GT_ASSET")
                continue
            if i in GT_PLAIN:
                stages = [(0.0, GT_ASSET[key].replace(".png", "_plain.png")),
                          (GT_PLAIN[i], GT_ASSET[key])]
            else:
                stages = [(0.0, GT_ASSET[key])]
            for k, (frac, asset) in enumerate(stages):
                at = s0 + frac * dur
                end = (s0 + stages[k + 1][0] * dur) if k + 1 < len(stages) else r["t1"]
                if end - at > 9.05:
                    errs.append(f"scene {i}: chang 原典 {k} dai {end-at:.1f}s > 9,0s "
                                f"(gate ② check_frame_pace) — them mot CHO KHOANH khac")
                trk_g.append({
                    "id": f"g{i}_{k}", "kind": "video", "from": f(at),
                    "durationInFrames": f(end - at), "asset": f"assets/{asset}",
                    # motion "none": the dung san dung 1920x1080, pan la CAT MAT BANG CHUNG
                    "fit": "cover", "motion": "none", "speed": 1.0, "volume": 0,
                    "fadeInFrames": FADE if k == 0 else 0,
                })
        elif is_fm:
            lines = SCENES[i][3]
            trk_fm.append({
                "id": f"fm{i}", "kind": "text", "from": f(s0) + 8,
                "durationInFrames": max(12, f(dur) - 12),
                "content": "\n".join(lines), "preset": "papercut-formula",
                "color": "#1C2A4A", "animation": "none",
                "layout": {"x": BLK_BOX[0], "y": 470, "w": BLK_BOX[1]}, "fontSize": 62,
            })
        elif is_blk:
            if r["kind"] == "gfx" and i not in GFX:
                errs.append(f"scene {i}: gfx khong co khoi chu trong GFX")
                continue
            lines = GFX[i] if r["kind"] == "gfx" else SCENES[i][3]
            nl = len(lines)
            bx, bw = BLK_BOX_FX if (i in FX and FX[i][2] == "gfxleft") else BLK_BOX
            fs, worst = blk_size(lines, bw, nl)
            if fs < 40:
                errs.append(f"scene {i}: khoi chu phai co ve {fs}px moi lot hop {bw}px — "
                            f"qua nho cho tep 45+. Dong chat nhat: «{worst}».")
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
            "preset": "telop-band" if (is_blk or is_gt or is_fm) else PRESET[n % 3],
            "color": "#FFD34E", "animation": "pop", "layout": {}, "fontSize": None,
        })

        if i in FX:
            variant, dens, area_kind = FX[i]
            if has_v:
                side = quiet_side(on_air[i] + ".mp4")
            else:
                side = "left" if n_side["left"] <= n_side["right"] else "right"
            trk_fx.append({
                "id": f"fx{i}", "kind": "fx", "from": f(s0) + 6,
                "durationInFrames": max(12, f(dur) - 12),
                "variant": variant, "density": dens,
                "color": FX_COLOR.get(variant, "#FFC83A"), "seed": 100 + i * 7,
                # Goc PHAI-DUOI la cho cua MASCOT (y~594-894) => cot phai chi dung NUA TREN.
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

    # ── GATE 2: MOI scene phai co telop ─────────────────────────────────────
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
    for c in trk_blk + trk_fm:
        x0, w0 = c["layout"]["x"], c["layout"]["w"]
        if x0 + w0 > 1626:
            errs.append(f"{c['id']}: hop chu {x0}-{x0+w0} lan cot MASCOT (x>=1642)")
        if x0 < 280:
            errs.append(f"{c['id']}: hop chu bat dau {x0} < 280, lan nut SUBSCRIBE")

    # ── GATE 5: GFX/GT phai phu du scene gfx/genten ──────────────────────────
    gfx_sc = sorted(i for i in idxs if rows[i]["kind"] == "gfx")
    if sorted(GFX) != gfx_sc:
        errs.append(f"GFX khai {sorted(GFX)} nhung scene gfx that la {gfx_sc}")
    gt_sc = sorted(i for i in idxs if rows[i]["kind"] == "genten")
    if len({int(c["id"][1:].split('_')[0]) for c in trk_g}) != len(gt_sc):
        errs.append(f"the 原典 phu {len(trk_g)} chang nhung co {len(gt_sc)} scene genten")

    # ── GATE 6: kho clip phai dung het, khong thua ──────────────────────────
    have = {s for v in inv.values() for s in v}
    if set(used) != have:
        errs.append(f"kho va ban dung lech: thua {sorted(have - set(used))[:6]} · "
                    f"thieu {sorted(set(used) - have)[:6]}")

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
            {"id": "trk-video", "name": "collage t2v", "type": "video", "clips": trk_v},
            {"id": "trk-genten", "name": "genten", "type": "video", "clips": trk_g},
            {"id": "trk-fx", "name": "hoa la canh", "type": "fx", "clips": trk_fx},
            {"id": "trk-stat", "name": "khoi chu font", "type": "text", "clips": trk_blk},
            {"id": "trk-formula", "name": "cong thuc", "type": "text", "clips": trk_fm},
            {"id": "trk-telop", "name": "telop", "type": "text", "clips": trk_t},
            {"id": "trk-audio", "name": "voice", "type": "audio", "clips": [
                {"id": "a0", "kind": "audio", "from": 0, "durationInFrames": f(total),
                 "asset": "assets/voice.wav", "volume": 1, "trimStartFrames": 0}]},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44, "lines": cap, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F3EAD8"},
        "brand": {
            "logo": "assets/brand_logo.png", "mascot": None, "mascotPoses": poses,
            "mascotVideo": poses[0]["asset"], "mascotVideoFrames": MASCOT_FRAMES,
            "mascotH": 300, "logoH": 110, "subscribe": True,
            "bottomOffset": 186, "subscribeBottom": 200,
        },
    }
    out = os.path.join(ROOT, "projects", NAME, "project.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(
        json.dumps(proj, ensure_ascii=False, indent=1))

    print(f"\nOK {out}")
    print(f"   {len(idxs)} scene · {total:.1f}s = {total/60:.2f}' @ {FPS}fps")
    print(f"   hinh {len(trk_v)} khe (kho {n_inv} clip) · genten {len(trk_g)} chang · "
          f"khoi chu {len(trk_blk)} ({len(GFX)} gfx + {len(trk_blk)-len(GFX)} stat) · "
          f"cong thuc {len(trk_fm)} · fx {len(trk_fx)} · telop {len(trk_t)} · "
          f"phu de {len(cap)} khoi")
    print(f"   nhip doi anh chinh: {len(trk_v)/(total/60):.2f}/phut (tran 6) "
          f"— genten tinh track rieng")
    print(f"   khe phai lam cham: {len(slow)} khe, cham nhat "
          f"{min([s for _, s in slow], default=1.0)}")
    for st, sp, m, fl in slow_mad:
        print(f"     duoi san 0,92: {st} speed {sp} · MAD {m} · san ap dung {fl}")
    if drift:
        print(f"   ⚠️ {len(drift)}/{len(trk_v)} clip len song lech scene-chu (van trong KHOI "
              f"cua no — xem GATE ALIGN trong code):")
        for st, sc, a2_, t0_, dl in drift:
            print(f"     {st:<12} chieu luc {a2_:>6.1f}s · scene {sc} bat dau {t0_:>6.1f}s "
                  f"(lech {dl:+.1f}s)")
    shrunk = [r for r in blk_fs if r[2] < r[3]]
    print(f"   khoi chu: {len(blk_fs)} khoi · {len(shrunk)} khoi phai CO CO de lot hop")
    for i2, nl2, fs2, cap2, wo in shrunk:
        print(f"     scene {i2:>3} ({nl2} dong): {cap2} -> {fs2}px | chat nhat «{wo[:40]}»")
    import collections
    vc = collections.Counter(v for v, _, _ in FX.values())
    print(f"   fx: {dict(vc)} — moi variant <= {max(vc.values())} lan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
