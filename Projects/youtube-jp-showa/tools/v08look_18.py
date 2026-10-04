# -*- coding: utf-8 -*-
"""v08look_18.py — dua video 18 ve KHUON video 08 (user 2026-09-24: "tao muon giong video tao gui… v8").

1) Thay 25 o phim 1946 mo bang ANH THAT net dung thoi dai (real_photos/b18/NN.jpg, MANIFEST co license).
2) MOI o anh tinh (anh that + anh AI) dung lai bang still_kb.py: anh SACH + zoom/truot cham xoay vong,
   BO lop meo cuc bo cua animate_still ("luon song nhe" — user bat 2026-09-24).
3) Ghi ket qua vao clips_ungraded/ (nguon cho grade_cells.py). Ban animate cu backup o clips_ungraded_anim/.
Sau: grade_cells.py 18_hataraku-okane --sharpen <cac o phim con lai>  ->  render  ->  mix_sound_18.py
"""
import json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "18_hataraku-okane"
CL, IN, UG, BKA = VD / "clips", VD / "cells_in", VD / "clips_ungraded", VD / "clips_ungraded_anim"
KB = Path(r"E:\Claude\Projects\_media_library\still_kb.py")
B18 = VD / "real_photos" / "b18"
BKA.mkdir(exist_ok=True)

man = json.loads((B18 / "MANIFEST.json").read_text(encoding="utf-8"))
NEW = {int(k): v for k, v in man.items()}
plan = json.loads((CL / "_PLAN.json").read_text(encoding="utf-8"))
byi = {r["idx"]: r for r in plan}
for i, v in NEW.items():
    r = byi[i]; r["layer"] = "photo"; r["src"] = "real_photos/b18/%02d.jpg" % i; r.pop("ss", None)
(CL / "_PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
fs = json.loads((VD / "film_spec.json").read_text(encoding="utf-8"))
gone = {"clip_%02d" % i for i in NEW}
fs["cuts"] = [c for c in fs["cuts"] if c["id"] not in gone]
(VD / "film_spec.json").write_text(json.dumps(fs, ensure_ascii=False, indent=1), encoding="utf-8")
L = ROOT / "06_VIDEO" / "_footage_test" / "FOOTAGE_USED.json"
u = json.loads(L.read_text(encoding="utf-8"))
u["used"] = [x for x in u["used"] if not (str(x.get("video", "")).startswith("18") and x.get("id") in gone)]
L.write_text(json.dumps(u, ensure_ascii=False, indent=1), encoding="utf-8")

MODES = ["zin", "pl", "zout", "pr", "tu", "zin", "td", "pl", "zout", "pr"]
jobs, k = [], 0
for r in plan:
    if r["layer"] not in ("photo", "aistill"):
        continue
    i = r["idx"]
    if r["layer"] == "photo":
        img, wm = B18 / ("%02d.jpg" % i), 0.0
    else:
        c = [f for f in IN.glob("%02d.*" % i) if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
        if not c:
            print("THIEU anh", i); continue
        img, wm = c[0], 0.905                 # anh AI co ✦ goc duoi-phai
    dur = r["dur"] + 0.5
    amt = min(0.06, max(0.03, 0.011 * dur))      # user 2026-09-24: "toc do hoi nhanh" -> ~60% ban dau
    jobs.append((i, img, wm, dur, MODES[k % len(MODES)], amt)); k += 1


def run(j):
    i, img, wm, dur, mode, amt = j
    dst = UG / ("clip_%02d.mp4" % i)
    if dst.exists() and not (BKA / dst.name).exists():
        shutil.copy(dst, BKA / dst.name)
    p = subprocess.run([sys.executable, str(KB), str(img), str(dst), "--dur", "%.2f" % dur, "--mode", mode,
                        "--amount", "%.3f" % amt, "--wm", str(wm)], capture_output=True, text=True)
    return i, mode, "ok" if p.returncode == 0 else "LOI " + p.stderr[-200:]


with ThreadPoolExecutor(2) as ex:
    res = list(ex.map(run, jobs))
bad = [x for x in res if x[2] != "ok"]
for x in res:
    print(" clip_%02d %s %s" % x)
film = sorted(r["idx"] for r in plan if r["layer"] == "film")
print("KET QUA:", "SACH %d o anh" % len(res) if not bad else "LOI %d" % len(bad))
print("o phim con lai (--sharpen):", ",".join(map(str, film)))
sys.exit(1 if bad else 0)
