# -*- coding: utf-8 -*-
"""apply_17B.py — muc B cho video 17: thay 49 o phim 1946 (sai thoi dai / lac de / lap / slate).

Danh gia 2026-09-24: 66 o phim PD, giu 18, bo 48 (+ o1 co slate). Thay bang:
  photo -> anh that 1971 (wilford peloquin, CC BY 2.0) + danchi 1960 (CC BY 4.0)
  film  -> phim do CHINH PHU MY lam: Japan Today 1959 HD (USIA) + You in Japan 1957 (US Army) — ⛔ KHONG steel_1960/japan_1960_nsc (phim tu nhan)
  ai    -> clip AI cu cung moc (clips_v17ai, da sach ✦ + vien) khi khong co hinh that khop loi
Chay:  python tools/apply_17B.py            (sua _PLAN.json + cells_in + ghi film_spec_B.json)
Sau:   cut_archival.py --spec <VD>/film_spec_B.json --outdir <VD>/clips --record 17_kaisha-ga-kureta
       make_cells_v3.py 17_kaisha-ga-kureta --only <photo+ai> --wm 0 --jobs 2
"""
import json, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "17_kaisha-ga-kureta"
FP = ROOT / "06_VIDEO" / "_footage_pd"
CL, IN, OLD = VD / "clips", VD / "cells_in", VD / "clips_v17ai"
PH = VD / "real_photos"

PHOTO = {1: "p1971/P039.jpg", 5: "p1971/P057.jpg", 6: "danchi_nishinomiya_1960.jpg", 9: "p1971/P132.jpg",
         10: "p1971/P148.jpg", 11: "p1971/P149.jpg", 12: "p1971/P135.jpg", 13: "p1971/P100.jpg",
         23: "p1971/P106.jpg", 30: "p1971/P133.jpg", 33: "p1971/P097.jpg", 41: "p1971/P056.jpg",
         100: "p1971/P147.jpg", 101: "p1971/P040.jpg", 108: "p1971/P099.jpg", 125: "p1971/P096.jpg",
         126: "p1971/P124.jpg", 127: "p1971/P028.jpg", 129: "p1971/P065.jpg",
         # 2026-09-24: 7 o nay luc dau dung steel_1960/japan_1960_nsc -> phim TU NHAN (Iwanami/ABC), CLAUDE.md cam
         18: "p1971/P101.jpg", 25: "p1971/P041.jpg", 29: "p1971/P052.jpg", 31: "p1971/P050.jpg",
         109: "p1971/P026.jpg", 110: "p1971/P029.jpg", 121: "p1971/P071.jpg",
         # 2026-09-24 lan 2: Japan Today 1959 bi NARA gan "Restricted - Possibly (copyright)" giong het 2 phim tu nhan -> thay 7 o
         7: "p1971/P105.jpg", 8: "p1971/P107.jpg", 42: "p1971/P005.jpg", 61: "p1971/P070.jpg",
         82: "p1971/P146.jpg", 133: "p1971/P122.jpg"}
YIJ = "you_in_japan_512kb.mp4"   # US Army Big Picture 1957 — NARA KHONG gan co ban quyen. ⛔ Japan Today 1959: NARA "Restricted - Possibly"
FILM = {45: (YIJ, 1249.0),
        48: (YIJ, 1243.8), 49: (YIJ, 1259.3), 53: (YIJ, 1231.2), 54: (YIJ, 1237.2)}
GRADE = {YIJ: 0.5}
AI = {17: 14, 47: 37, 50: 39, 51: 40, 52: 41, 55: 43, 70: 58, 80: 67, 81: 66, 83: 69, 90: 75, 94: 78,
      120: 101, 135: 109, 136: 111}

planp = CL / "_PLAN.json"
for p in (planp, VD / "film_spec.json"):
    b = p.with_name(p.name + ".bak_B")
    if not b.exists():
        shutil.copy(p, b)
plan = json.loads(planp.read_text(encoding="utf-8"))
byi = {r["idx"]: r for r in plan}
assert not (set(PHOTO) & set(FILM) | set(PHOTO) & set(AI) | set(FILM) & set(AI))
miss, cuts = [], []
for i, f in PHOTO.items():
    r = byi[i]; r["layer"] = "photo"; r["src"] = f; r.pop("ss", None)
    src = PH / f
    for old in IN.glob("%02d.*" % i):
        old.unlink()
    if src.exists() and src.stat().st_size > 1000:
        shutil.copy(src, IN / ("%02d.jpg" % i))
    else:
        miss.append(f)
for i, n in AI.items():
    r = byi[i]; r["layer"] = "ai"; r["src"] = "clips_v17ai/clip_%02d.mp4" % n; r.pop("ss", None)
    for old in IN.glob("%02d.*" % i):
        old.unlink()
    shutil.copy(OLD / ("clip_%02d.mp4" % n), IN / ("%02d.mp4" % i))
for i, (src, ss) in FILM.items():
    r = byi[i]; r["layer"] = "film"; r["src"] = src; r["ss"] = ss
    cuts.append({"id": "clip_%02d" % i, "src": str(FP / src), "ss": ss, "dur": round(r["dur"] + 0.6, 2),
                 "ybias": 0.45, "grade": GRADE[src], "note": "B o%d %s" % (i, r["text"][:20])})
planp.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
(VD / "film_spec_B.json").write_text(json.dumps({"_note": "sinh boi apply_17B.py", "cuts": cuts},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
# film_spec.json chinh: bo cut cu cua o da thay, them cut moi -> so nhat quan voi video
fs = json.loads((VD / "film_spec.json").read_text(encoding="utf-8"))
gone = {"clip_%02d" % i for i in list(PHOTO) + list(AI) + list(FILM)}
fs["cuts"] = [c for c in fs["cuts"] if c["id"] not in gone] + cuts
(VD / "film_spec.json").write_text(json.dumps(fs, ensure_ascii=False, indent=1), encoding="utf-8")
print("photo", len(PHOTO), "ai", len(AI), "film", len(FILM), "| thieu anh:", miss or "0")
print("--only", ",".join(str(i) for i in sorted(list(PHOTO) + list(AI))))
