# -*- coding: utf-8 -*-
"""gen_film_spec_v3.py — sinh spec cho cut_archival.py tu clips/_PLAN.json (khuon REAL-FIRST v3).

Moi o lop 'film' co san src + ss (build_slides_v3 tinh tu film_lines cua visual_plan.json).
id = "clip_NN" => cut_archival ghi THANG clips/clip_NN.mp4, dung ten renderer doc.
dur = do dai o + 0,6s (renderer thieu do dai thi LAP clip — CLAUDE.md §Visual).

  python tools/gen_film_spec_v3.py <stem>  ->  06_VIDEO/<stem>/film_spec.json
  python tools/cut_archival.py --spec 06_VIDEO/<stem>/film_spec.json --outdir 06_VIDEO/<stem>/clips [--record <stem>]
⚠️ Chi --record khi SLIDES da CHOT tren timeline.json THAT (o doi thi ss doi).
"""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
FP = ROOT / "06_VIDEO" / "_footage_pd"
stem = sys.argv[1]
VD = ROOT / "06_VIDEO" / stem
plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
notes = {}
vp = VD / "visual_plan.json"
if vp.exists():
    for fl in json.loads(vp.read_text(encoding="utf-8")).get("film_lines", []):
        notes[(fl[1], float(fl[2]))] = fl[3] if len(fl) > 3 else ""
cuts = []
for r in plan:
    if r["layer"] != "film":
        continue
    if not r.get("src"):
        print("🔴 o %02d la film nhung KHONG co src — khai film_lines cho dong nay" % r["idx"]); sys.exit(1)
    cuts.append({"id": "clip_%02d" % r["idx"], "src": str(FP / r["src"]), "ss": r["ss"],
                 "dur": round(r["dur"] + 0.6, 2), "ybias": 0.45, "grade": 0,
                 "note": "o%d · %s" % (r["idx"], r["text"][:24])})
out = VD / "film_spec.json"
out.write_text(json.dumps({"_note": "sinh tu _PLAN.json boi gen_film_spec_v3.py", "cuts": cuts},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print("%d o film -> %s" % (len(cuts), out))
