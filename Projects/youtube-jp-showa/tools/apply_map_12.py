# -*- coding: utf-8 -*-
"""Ap bang ghep map_12.MAP -> clips/clip_<slot>.mp4 (ten theo SO THU TU SLOT).

🔴 Ten file la HOP DONG voi renderer: video_render.py tim `clips/clip_<index>.mp4` theo
   thu tu slot, KHONG doc khoa `source` (CLAUDE.md §Visual). Dat ten mo ta => renderer
   coi nhu khong co clip nao va am tham fallback anh tinh, preflight van in "clip deu on".

Nguon = _flow_crop/ (da cat 5% mep, bo dai phim), KHONG phai _flow_raw/.

    python tools/apply_map_12.py            -> bao cao, khong dung file
    python tools/apply_map_12.py --apply    -> tao clips/clip_NN.mp4
"""
import sys, os, json, shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import map_12 as M

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
CROP = VD / "_flow_crop"
DST = VD / "clips"
SL = ROOT / "03_SCRIPTS" / "12_natsu-atarimae_SLIDES.json"

slides = json.loads(SL.read_text(encoding="utf-8"))
N = len(slides)
apply_it = "--apply" in sys.argv

missing_src, ok = [], []
for slot, clip in sorted(M.MAP.items()):
    src = CROP / ("c%03d.mp4" % clip)
    if not src.exists():
        missing_src.append((slot, clip))
        continue
    ok.append((slot, clip, src))

print("slot tong        : %d" % N)
print("co trong bang    : %d" % len(M.MAP))
print("thieu clip han   : %d  -> %s" % (len(M.THIEU), sorted(M.THIEU)))
print("da cat, san sang : %d" % len(ok))
print("chua cat xong    : %d" % len(missing_src))

if apply_it:
    DST.mkdir(parents=True, exist_ok=True)
    n = 0
    for slot, clip, src in ok:
        dst = DST / ("clip_%02d.mp4" % slot)
        if dst.exists():
            dst.unlink()
        try:
            os.link(src, dst)
        except OSError:
            shutil.copyfile(src, dst)
        n += 1
    print("")
    print("DA DAT %d clip -> %s" % (n, DST))
    (DST / "_MAP_SLOT_CLIP.txt").write_text(
        "slot -> clip goc (#NNN tren contact sheet)\n"
        + "\n".join("clip_%02d.mp4  <-  #%03d" % (s, c) for s, c, _ in ok)
        + "\n\nTHIEU (chua gen):\n"
        + "\n".join("  slot %3d  %s" % (k, v) for k, v in sorted(M.THIEU.items()))
        + "\n", encoding="utf-8")
    con = N - n
    print("")
    if con:
        print("⛔ CON THIEU %d/%d CLIP — CHUA DUOC RENDER VIDEO (render-background.md §1.5)" % (con, N))
    else:
        print("DU %d/%d clip." % (n, N))
else:
    print("")
    print("(chay lai voi --apply de dat vao clips/)")
