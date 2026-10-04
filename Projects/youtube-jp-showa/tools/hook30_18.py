# -*- coding: utf-8 -*-
"""hook30_18.py — 30s dau video 18: thay 7 o AI (o1-7) bang PHIM/ANH THAT (user 2026-09-25:
"doan dau lam anh AI qua, tao muon 30s dau hau nhu la anh that va video that").

o1 bua com gia dinh (11059)  · o2 buu dien 1960 (Commons CC BY 4.0) · o3 san ga dong nguoi (11069)
o4 dan ong mang tay nai (11069, khop cau 父)   · o5 to 百円札 板垣退助 that (Commons PD) · o6 phu nu lao dong (11022)
o7 ba lao nong o ruong (11050). o8 (hop banh, 33.7s) giu anh AI — vat cua chuyen ke.
Ban AI cu backup o clips_ungraded_hookai/. Sau: grade_cells --only 1-7 -> render -> mix_sound_18.
"""
import json, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "18_hataraku-okane"
PD = ROOT / "06_VIDEO" / "_footage_pd"
CL, UG, BK = VD / "clips", VD / "clips_ungraded", VD / "clips_ungraded_hookai"
KB = Path(r"E:\Claude\Projects\_media_library\still_kb.py")
BK.mkdir(exist_ok=True)

FILM = {1: ("usaf11059_kyoto_home_1946_hd.mov", 841.0, "bua com gia dinh"),
        3: ("usaf11069_transport_1946_hd.mov", 2.0, "san ga dong nguoi mang tay nai"),
        4: ("usaf11069_transport_1946_hd.mov", 15.0, "dan ong mang tay nai roi lang (cau 父)"),
        6: ("usaf11022_industrial_life_1946_hd.mov", 1088.0, "phu nu khan trum dau lao dong"),
        7: ("usaf11050_agri_1946_hd.mov", 102.0, "ba lao nong ganh thung o ruong")}
PHOTO = {2: ("real_photos/hook18/02.jpg", "zin"), 5: ("real_photos/hook18/05.jpg", "pr")}

plan = json.loads((CL / "_PLAN.json").read_text(encoding="utf-8"))
byi = {r["idx"]: r for r in plan}
for i in list(FILM) + list(PHOTO):
    f = UG / ("clip_%02d.mp4" % i)
    if f.exists() and not (BK / f.name).exists():
        shutil.copy(f, BK / f.name)

cuts = []
for i, (src, ss, note) in FILM.items():
    r = byi[i]; r["layer"] = "film"; r["src"] = src; r["ss"] = ss
    cuts.append({"id": "clip_%02d" % i, "src": str(PD / src), "ss": ss, "dur": round(r["dur"] + 0.6, 2),
                 "ybias": 0.45, "grade": 0, "note": "o%d hook30 · %s" % (i, note)})
for i, (src, mode) in PHOTO.items():
    r = byi[i]; r["layer"] = "photo"; r["src"] = src; r.pop("ss", None)
(CL / "_PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")

fs = json.loads((VD / "film_spec.json").read_text(encoding="utf-8"))
ids = {c["id"] for c in cuts}
fs["cuts"] = [c for c in fs["cuts"] if c["id"] not in ids] + cuts
(VD / "film_spec.json").write_text(json.dumps(fs, ensure_ascii=False, indent=1), encoding="utf-8")
tmp = VD / "film_spec_hook30.json"
tmp.write_text(json.dumps({"cuts": cuts}, ensure_ascii=False, indent=1), encoding="utf-8")

p = subprocess.run([sys.executable, str(ROOT / "tools" / "cut_archival.py"), "--spec", str(tmp),
                    "--outdir", str(UG), "--record", "18_hataraku-okane"])
if p.returncode:
    print("CAT PHIM LOI", p.returncode); sys.exit(p.returncode)

bad = 0
for i, (src, mode) in PHOTO.items():
    dur = byi[i]["dur"] + 0.5
    amt = min(0.06, max(0.03, 0.011 * dur))
    q = subprocess.run([sys.executable, str(KB), str(VD / src), str(UG / ("clip_%02d.mp4" % i)), "--dur", "%.2f" % dur,
                        "--mode", mode, "--amount", "%.3f" % amt, "--wm", "0"], capture_output=True, text=True)
    print(" clip_%02d photo %s" % (i, "ok" if q.returncode == 0 else "LOI " + q.stderr[-200:]))
    bad += q.returncode != 0
print("KET QUA:", "SACH" if not bad else "LOI")
sys.exit(1 if bad else 0)
