# -*- coding: utf-8 -*-
"""Video 18: plan doi so o (bo dokkoi) -> chuyen cells_in/NN.* theo (lop, dong loi, thu tu trong dong).
Cu: _src_flow/_PLAN_dokkoi.json + cells_in_prev/ (doi ten tu cells_in). Moi: clips/_PLAN.json -> cells_in/.
Khong xoa gi: file cu nam nguyen o cells_in_prev/."""
import sys, json, shutil
from pathlib import Path
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\18_hataraku-okane")
old = json.loads((VD / "_src_flow" / "_PLAN_dokkoi.json").read_text(encoding="utf-8"))
new = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
PREV, OUT = VD / "cells_in_prev", VD / "cells_in"
if not PREV.exists():
    (VD / "cells_in").rename(PREV)
OUT.mkdir(exist_ok=True)

def key(rows):
    seen, k = defaultdict(int), {}
    for r in rows:
        if r["layer"] == "film": continue
        kk = (r["layer"], r["text"]); k[r["idx"]] = kk + (seen[kk],); seen[kk] += 1
    return k

ko, kn = key(old), key(new)
inv = {v: i for i, v in ko.items()}
moved, need = [], []
for i, kk in sorted(kn.items()):
    j = inv.get(kk)
    src = None
    if j is not None:
        for e in (".png", ".jpg", ".jpeg", ".webp", ".mp4"):
            p = PREV / ("%02d%s" % (j, e))
            if p.exists(): src = p; break
    if src:
        shutil.copy2(src, OUT / ("%02d%s" % (i, src.suffix))); moved.append((j, i))
    else:
        need.append((i, kk[0], kk[1][:40]))
print("chuyen: %d | can anh MOI: %d" % (len(moved), len(need)))
for n in need: print("  %02d %-7s %s" % n)
(VD / "_src_flow" / "remap_dokkoi.json").write_text(json.dumps({"moved": moved, "need": need}, ensure_ascii=False, indent=1), encoding="utf-8")
