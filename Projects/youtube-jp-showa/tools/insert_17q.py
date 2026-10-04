# -*- coding: utf-8 -*-
"""insert_17q.py — chen 2 o moi vao video 17 (cau hoi treo o hook + cau tra loi gan cuoi).

Renderer dinh danh clip bang clips/clip_<index>.mp4 theo THU TU slot trong SLIDES, nen chen o
giua bai = phai doi ten moi clip phia sau. Tool nay lam trong 1 luot, co backup:
  - SLIDES: chen entry sau slot 8 (cau hoi) va sau slot 123 cu (cau tra loi)
  - clips/clip_NN.mp4 + cells_in/NN.* : doi ten tu CAO xuong THAP (khong de de len nhau)
  - clips/_PLAN.json : doi idx + them 2 hang layer photo
  - film_spec.json : doi id cho khop (so sach)
Chay 1 LAN. Chay lai se bao loi (da co entry 'では、会社が用意').
"""
import json, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "17_kaisha-ga-kureta"
SL = ROOT / "03_SCRIPTS" / "17_kaisha-ga-kureta_SLIDES.json"
CL, IN = VD / "clips", VD / "cells_in"
Q_AFTER, A_AFTER = 8, 123          # chi so CU
TL = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
def line(prefix):
    return next(x for x in TL if x["text"].startswith(prefix))
q, a1 = line("では、会社が用意"), line("冒頭の答えです")
nxt = line("正直に言えば")

slides = json.loads(SL.read_text(encoding="utf-8"))
assert not any(e.get("match", "").startswith("では、会社が用意") for e in slides), "da chen roi"
assert len(slides) == 138
for p in (SL, CL / "_PLAN.json", VD / "film_spec.json"):
    b = p.with_name(p.name + ".bak_q")
    if not b.exists():
        shutil.copy(p, b)

def new_idx(i):
    return i if i <= Q_AFTER else (i + 1 if i <= A_AFTER else i + 2)

# 1) doi ten file, tu cao xuong thap
for i in range(137, Q_AFTER, -1):
    j = new_idx(i)
    src = CL / ("clip_%02d.mp4" % i)
    if src.exists():
        src.rename(CL / ("clip_%02d.mp4" % j))
    for f in list(IN.glob("%02d.*" % i)):
        f.rename(IN / ("%02d%s" % (j, f.suffix)))

# 2) SLIDES
out = []
for i, e in enumerate(slides):
    e = dict(e); e["source"] = "clips/clip_%02d.mp4" % new_idx(i); out.append(e)
    if i == Q_AFTER:
        out.append({"match": "では、会社が用意", "video": True, "source": "clips/clip_%02d.mp4" % (Q_AFTER + 1),
                    "offset": 0.0, "dur": round(q["end"] - q["start"], 2)})
    if i == A_AFTER:
        out.append({"match": "冒頭の答えです", "video": True, "source": "clips/clip_%02d.mp4" % (A_AFTER + 2),
                    "offset": 0.0, "dur": round(nxt["start"] - a1["start"], 2)})
assert all(e["source"] == "clips/clip_%02d.mp4" % k for k, e in enumerate(out)) and len(out) == 140
SL.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# 3) _PLAN
plan = json.loads((CL / "_PLAN.json").read_text(encoding="utf-8"))
for r in plan:
    r["idx"] = new_idx(r["idx"])
plan.append({"idx": Q_AFTER + 1, "t": q["start"], "dur": round(q["end"] - q["start"] + 0.6, 2), "layer": "photo",
             "line": TL.index(q), "preset": "flat", "text": q["text"], "src": "p1971/P064.jpg"})
plan.append({"idx": A_AFTER + 2, "t": a1["start"], "dur": round(nxt["start"] - a1["start"], 2), "layer": "photo",
             "line": TL.index(a1), "preset": "flat", "text": a1["text"], "src": "danchi_yaenosato_2026.jpg"})
plan.sort(key=lambda r: r["idx"])
assert [r["idx"] for r in plan] == list(range(140))
(CL / "_PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")

# 4) film_spec ids
fs = json.loads((VD / "film_spec.json").read_text(encoding="utf-8"))
for c in fs["cuts"]:
    c["id"] = "clip_%02d" % new_idx(int(c["id"][5:]))
(VD / "film_spec.json").write_text(json.dumps(fs, ensure_ascii=False, indent=1), encoding="utf-8")

shutil.copy(VD / "real_photos/p1971/P064.jpg", IN / ("%02d.jpg" % (Q_AFTER + 1)))
shutil.copy(VD / "real_photos/danchi_yaenosato_2026.jpg", IN / ("%02d.jpg" % (A_AFTER + 2)))
print("OK 140 slot | o moi:", Q_AFTER + 1, A_AFTER + 2, "| q dur", round(q["end"] - q["start"], 2),
      "| a dur", round(nxt["start"] - a1["start"], 2))
