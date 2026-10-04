# -*- coding: utf-8 -*-
"""review_slots_16.py — sheet nghiem thu 150 o cua video 16, CO NHAN LOP.

Contact sheet 1 frame/clip da tung CHO QUA 24/24 clip loi (CLAUDE.md §Visual), nen o day
lay 1 frame GIUA moi clip va chia sheet theo LOP + theo KHOI, de soi duoc hai thu ma sheet
tron khong thay:
  · chuyen lop co lam mat tong khong (phim 1946 <-> anh tinh <-> AI)
  · trong mot khoi co hai o lien tiep gan nhu CUNG MOT KHUNG khong

Chay: python tools/review_slots_16.py [--layer film|still|ai]
"""
import json, subprocess, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\16_omiai-kekkon")
only = None
for i, a in enumerate(sys.argv):
    if a == "--layer" and i + 1 < len(sys.argv): only = sys.argv[i + 1]

plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
rows = [r for r in plan if only is None or r["layer"] == only]
tmp = VD / "_slot_sheet"
if tmp.exists(): shutil.rmtree(tmp)
tmp.mkdir()

n = 0
for r in rows:
    src = VD / "clips" / ("clip_%02d.mp4" % r["idx"])
    if not src.exists(): print("thieu", src.name); continue
    n += 1
    # frame o GIUA clip: frame dau hay la frame chuyen canh cua phim goc
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(max(0.3, r["dur"] / 2)), "-i", str(src),
                    "-frames:v", "1", "-vf", "scale=300:-1", str(tmp / ("%03d.jpg" % n)), "-y"])
cols = 10
out = VD / ("sheet_slots_%s.jpg" % (only or "all"))
subprocess.run(["ffmpeg", "-v", "error", "-i", str(tmp / "%03d.jpg"),
                "-filter_complex", f"tile={cols}x{(n + cols - 1)//cols}:padding=4:color=white",
                "-frames:v", "1", str(out), "-y"])
print("%d o -> %s" % (n, out))
print("thu tu doc: trai->phai, tren->duoi; nhan lop/loi o clips/_MAP.txt")
