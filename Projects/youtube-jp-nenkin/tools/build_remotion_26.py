# -*- coding: utf-8 -*-
r"""
build_remotion_26.py — dung TOAN BO video 26 (年金の天引きと手取り): 988,6s · 117 scene.

Khuon = `build_remotion_23.py` (vox paper-collage toan khung + telop + 3 overlay dan cung).
BON diem khac video 23:

  1. **Kho clip = 67**, va lan nay `plan26.nshot` **KHOP** voi kho (23 phai doc TENFILE vi
     lo gen lech plan). Van doc TENFILE lam nguon su that — re va khong the lech.
  2. **23 scene `gfx`** (23 co 8). Moi khoi chu duoi day la loi VERBATIM cua CHINH scene do.
  3. **5 scene `genten` / 11 the** — mot khoa co 2-3 CHO KHOANH khac nhau, chia chang deu
     nhau trong scene. `motion: "none"` (the dung san 1920x1080, pan la cat mat bang chung).
  4. **7 scene `formula`** (23 co 4).

fps = 24 (clip nguon 24fps, ep 30 thi 27% frame lap => judder).

CHAY:  python tools/build_remotion_26.py
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

from _scenes26 import SCENES                                        # noqa: E402
from plan26 import build                                            # noqa: E402

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-26"
FPS, W, H = 24, 1920, 1080
VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai")
TL = os.path.join(VD, "timeline.json")
TENFILE = os.path.join(VD, "vox26_TENFILE.txt")
ASSETS = os.path.join(ROOT, "public", "projects", NAME, "assets")

SRC_SEC = 8.000
MASCOT_FRAMES = 192
FADE = 7
GRADE = {"brightness": 1.04, "contrast": 1.0, "saturate": 1.08}

f = lambda s: max(0, int(round(s * FPS)))

# ── CAU HINH RIENG cua video 26 (GT_STAGES · GFX · FX) o file rieng ────────
# 🔴 Tach ra de builder giu nguyen phan CO KHI da chay duoc cua ban 25 — chi doi
#    DU LIEU. Sua noi dung video thi sua `tools/_cfg26.py`, khong sua file nay.
from _cfg26 import GT_STAGES, GFX, FX                              # noqa: E402

FX_COLOR = {"stampx": "#1C2A4A"}      # ✗ navy, KHONG do (CLAUDE.md §②)
FX_AREA = {"gfxleft": {"x": 6, "y": 26, "w": 24, "h": 30},
           "full":    {"x": 0, "y": 0, "w": 100, "h": 100}}

POSE = ["owl_idle"]
PRESET = ["telop", "telop-gold", "telop"]

# ── HOP KHOI CHU + PHEP TU CO CO (audience-45plus.md §2.0f) ────────────────
# Hop phai tranh CU (x>=1642) va nut SUBSCRIBE (x<=260).
BLK_BOX = (300, 1326)              # x, w — mep phai 1626
BLK_BOX_FX = (606, 1020)           # scene co stampx: chua cot trai cho dau ✗
BLK_CAP = {1: 92, 2: 84, 3: 76, 4: 66}
BLK_SAFE = 1.06                    # bien an toan do duoc cua preset (§2.0f)


def read_inventory():
    """scene -> [ten khe] LAY TU LO DA GEN (`vox26_TENFILE.txt`)."""
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


# ── PHEP TU CO CO cho `papercut-formula` ───────────────────────────────────
# 🔴 BAT O STILL FRAME 3504 (scene 18): `fontSize: 62` co dinh (bê tu builder 23) lam
#    「八十四万七千三百円」 GAY DONG thanh 「八十四万七千三百 / 円」 va 「納めた月数」 thanh
#    「納めた月 / 数」. Dung benh `audience-45plus.md` §2.0f: preset la flex NOWRAP co
#    maxWidth, vuot tran thi o bi NEN va chu wrap BEN TRONG o — khong tran ra ngoai khung
#    nen khong gate nao thay, **chi MAT thay tren still**. Cong thuc cua video 23 ngan hon
#    nen no khong dinh; bê hang so sang video khac la lo.
# 📐 Hinh hoc doc tu `TextClip.tsx` (don vi `size`):
#      o thuong = w_em + 0,32 (padding 0,16 moi ben) · o DAP AN (sau `=`) = 1,16·w_em + 0,32
#      toan tu = 0,92 · gap giua cac o 0,22 · hang dap an thut vao 0,90
FM_MAX, FM_MIN = 62, 40
FM_OPS = set("÷×−+＋-=≒→")


def fm_size(line: str, w_avail: int):
    """(co chu, hang chat nhat) cho mot dong `papercut-formula`."""
    parts = line.split()
    eq = next((k for k, p in enumerate(parts) if p in ("=", "≒")), -1)
    rows = [parts[:eq + 1], parts[eq + 1:]] if eq >= 0 else [parts]
    worst, who = 0.0, ""
    for r, row in enumerate(rows):
        if not row:
            continue
        u = 0.90 if r > 0 else 0.0
        for k, p in enumerate(row):
            i = k if r == 0 else eq + 1 + k
            if len(p) == 1 and p in FM_OPS:
                u += 0.92          # toan tu: glyph ve full-width trong font JP, khong 0,55
            else:
                u += (1.16 if (eq >= 0 and i > eq) else 1.0) * _w_em(p) + 0.32
        u += 0.22 * (len(row) - 1)
        if u > worst:
            worst, who = u, " ".join(row)
    fs = int((w_avail / BLK_SAFE) / worst) if worst else FM_MAX
    return min(FM_MAX, fs), who


def mad_of(asset: str) -> float:
    """Chuyen dong frame-to-frame cua clip (MAD tren ban 320x180, 1 frame/2)."""
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
    """Loi VAO cua khe hinh thu `k` — xoay 3 HO, trong moi ho xoay huong/do dai.

    🔴 Chi so phai dem theo SO LAN HO DO da dung (`n_fam`), khong theo chi so vong lap
       ngoai — `k % 4` khi k chi nhan gia tri le thi chi phu 2/4 huong (CLAUDE.md §② muc 9).
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


def shot_runs(rows, inv):
    """(khe hinh) -> [(t0, t1, stem, scene_chu)] — chia deu theo **KHOI**, khong theo scene.

    KHOI = day scene `art` LIEN KE. Chia deu trong khoi giu speed khong tut xuong slow-motion
    o nhung scene dai (bai hoc video 22 muc 14).
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
    used, slow, slow_mad, blk_fs, drift, fm_fs = [], [], [], [], [], []

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
            if key not in GT_STAGES:
                errs.append(f"scene {i}: khoa genten «{key}» khong co the trong GT_STAGES")
                continue
            st = GT_STAGES[key]
            for k, asset in enumerate(st):
                at = s0 + dur * k / len(st)
                end = s0 + dur * (k + 1) / len(st)
                if end - at > 9.05:
                    errs.append(f"scene {i}: chang 原典 {k} dai {end-at:.1f}s > 9,0s "
                                f"(gate ② check_frame_pace) — them mot CHO KHOANH khac")
                trk_g.append({
                    "id": f"g{i}_{k}", "kind": "video", "from": f(at),
                    "durationInFrames": f(end - at), "asset": f"assets/{asset}",
                    "fit": "cover", "motion": "none", "speed": 1.0, "volume": 0,
                    "fadeInFrames": FADE if k == 0 else 0,
                })
        elif is_fm:
            # 🔴 CHUAN HOA `＝` (full-width) -> `=`. Lop toan tu cua `TextClip.tsx` la
            #    [÷×−+＋-=≒→] — co `＋` nhung KHONG co `＝`, nen `＝` bi coi la mot HANG va
            #    duoc dong khung giay y nhu mot con so; va `eq` khong tim thay nen khong
            #    tach duoc hang dap an. Doi mot ky tu duoc ca hai: toan tu de TRAN, dap an
            #    xuong hang duoi to hon 1,16x va to nen nhan. Dinh o scene 33 va 80.
            lines = [ln.replace("＝", "=") for ln in SCENES[i][3]]
            fms, fmw = min((fm_size(ln, BLK_BOX[1]) for ln in lines), key=lambda x: x[0])
            if fms < FM_MIN:
                errs.append(f"scene {i}: cong thuc phai co ve {fms}px moi lot hop "
                            f"{BLK_BOX[1]}px — qua nho cho tep 45+. Hang chat nhat: «{fmw}».")
            fm_fs.append((i, fms, fmw))
            trk_fm.append({
                "id": f"fm{i}", "kind": "text", "from": f(s0) + 8,
                "durationInFrames": max(12, f(dur) - 12),
                "content": "\n".join(lines), "preset": "papercut-formula",
                "color": "#1C2A4A", "animation": "none",
                "layout": {"x": BLK_BOX[0], "y": 470, "w": BLK_BOX[1]}, "fontSize": fms,
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
              f"cua no):")
        for st, sc, a2_, t0_, dl in drift:
            print(f"     {st:<12} chieu luc {a2_:>6.1f}s · scene {sc} bat dau {t0_:>6.1f}s "
                  f"(lech {dl:+.1f}s)")
    fshr = [r for r in fm_fs if r[1] < FM_MAX]
    print(f"   cong thuc: {len(fm_fs)} khoi · {len(fshr)} khoi phai CO CO (tran {FM_MAX}px)")
    for i2, fs2, wo in fshr:
        print(f"     scene {i2:>3}: {FM_MAX} -> {fs2}px | hang chat nhat «{wo[:46]}»")
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
