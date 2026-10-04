# -*- coding: utf-8 -*-
"""Doi ten clip Flow gen ra -> clips/clip_<index>.mp4 THEO DUNG THU TU FLOW.txt.

🔴 VI SAO PHAI CO TOOL NAY (CLAUDE.md §Visual): video_render.py tim clip bang
   `clips/clip_<index>.mp4` theo SO THU TU SLOT, KHONG doc khoa `source`. Dat ten mo ta
   => renderer coi nhu KHONG CO CLIP NAO va am tham fallback anh tinh, trong khi preflight
   van in "clip deu on" (thieu clip chi vao `warns`) => ra video rong voi EXITCODE=0.

Cach dung:
    1. Bom videogen_FLOW.txt vao Flow (extension), tai ve theo DUNG THU TU dong.
    2. Bo het file tai ve vao 06_VIDEO/12_natsu-atarimae/clips_named/ (ten tang dan theo thu tu).
    3. python tools/place_clips_12.py            -> kiem tra + in bang doi chieu
       python tools/place_clips_12.py --apply    -> tao hardlink sang clips/clip_NN.mp4
"""
import sys, os, json, re, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
SRC = VD / "clips_named"
DST = VD / "clips"
TEN = VD / "videogen_TENFILE.txt"
SL = ROOT / "03_SCRIPTS" / "12_natsu-atarimae_SLIDES.json"

names = []
for ln in TEN.read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*(\d+)\s+(\S+\.mp4)", ln)
    if m:
        names.append((int(m.group(1)), m.group(2)))
names.sort()
slides = json.loads(SL.read_text(encoding="utf-8"))

if len(names) != len(slides):
    print("[CHAN] TENFILE co %d dong nhung SLIDES co %d entry — KHONG khop"
          % (len(names), len(slides)))
    sys.exit(1)

SRC.mkdir(parents=True, exist_ok=True)
DST.mkdir(parents=True, exist_ok=True)
apply_it = "--apply" in sys.argv
missing, done = [], 0
for i, (n, nm) in enumerate(names):
    src = SRC / nm
    dst = DST / ("clip_%02d.mp4" % i)
    if not src.exists():
        missing.append((i, nm))
        continue
    if apply_it:
        if dst.exists():
            dst.unlink()
        try:
            os.link(src, dst)          # hardlink: 0 byte them, cung o E:
        except OSError:
            shutil.copyfile(src, dst)
        done += 1

print("SLIDES entry        : %d" % len(slides))
print("TENFILE dong        : %d" % len(names))
print("co trong clips_named: %d | THIEU: %d" % (len(names) - len(missing), len(missing)))
if missing:
    print("")
    print("THIEU (index -> ten file can co):")
    for i, nm in missing[:20]:
        print("  clip_%02d.mp4  <-  %s" % (i, nm))
    if len(missing) > 20:
        print("  ... con %d cai nua" % (len(missing) - 20))
if apply_it:
    print("")
    print("DA TAO %d link -> %s" % (done, DST))
else:
    print("")
    print("(chay lai voi --apply de tao link)")
print("")
print("⛔ DU 165/165 CLIP MOI DUOC RENDER VIDEO (render-background.md §1.5).")
sys.exit(1 if missing else 0)
