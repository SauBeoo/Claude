# -*- coding: utf-8 -*-
"""kb_cells.py — dung moi o ANH (photo, khong phai card chu) thanh clip zoom/truot cham
theo khuon showa (still_kb.py, user 2026-10-01: "chuyen dong giong showa").

  python tools/kb_cells.py <stem> [--force]

- Nguon: 06_VIDEO/<stem>/slides_img/slide_NN.* (da xoa ✦, 1920x1080) -> clips/clip_NN.mp4
- Card chu (khoa "card") GIU DUNG YEN (pan cat chu). O video san co khong dung toi.
- Ghi lai SLIDES: entry duoc dung clip -> "video": true, "kb": mode, bo "static".
  Ban goc backup 1 lan: 03_SCRIPTS/<stem>_SLIDES_static.json
- Resume: clip moi hon anh nguon thi bo qua (render-background.md §2.5).
"""
import json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-yawa")
KB = Path(r"E:\Claude\Projects\_media_library\still_kb.py")
stem = sys.argv[1]
force = "--force" in sys.argv
VD = ROOT / "06_VIDEO" / stem
IMG, CL = VD / "slides_img", VD / "clips"
SL = ROOT / "03_SCRIPTS" / f"{stem}_SLIDES.json"
BK = ROOT / "03_SCRIPTS" / f"{stem}_SLIDES_static.json"
if not BK.exists():
    shutil.copy(SL, BK)
slides = json.loads(BK.read_text(encoding="utf-8"))      # luon dung tu ban goc
CL.mkdir(exist_ok=True)

MODES = ["zin", "pl", "zout", "pr", "tu", "zin", "td", "pl", "zout", "pr"]
jobs, k = [], 0
for i, s in enumerate(slides):
    if s.get("video") or s.get("card") or not s.get("photo"):
        continue
    src = next((p for e in (".jpg", ".jpeg", ".png") if (p := IMG / f"slide_{i:02d}{e}").exists()), None)
    if src is None:
        print("THIEU anh", i); continue
    dur = s["_dur"] + 1.0                         # du cho dissolve + lech timeline
    amt = min(0.06, max(0.03, 0.011 * dur))       # cung toc do showa 18 (user: "hoi nhanh" -> 60%)
    mode = MODES[k % len(MODES)]; k += 1
    s.pop("static", None); s["video"] = True; s["kb"] = mode
    jobs.append((i, src, dur, mode, amt))


def run(j):
    i, src, dur, mode, amt = j
    dst = CL / f"clip_{i:02d}.mp4"
    if not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return i, mode, "skip"
    p = subprocess.run([sys.executable, str(KB), str(src), str(dst), "--dur", "%.2f" % dur, "--mode", mode,
                        "--amount", "%.3f" % amt, "--fps", "30"], capture_output=True, text=True)
    return i, mode, "ok" if p.returncode == 0 else "LOI " + p.stderr[-200:]


with ThreadPoolExecutor(2) as ex:
    res = list(ex.map(run, jobs))
bad = [x for x in res if not x[2] in ("ok", "skip")]
for x in res:
    print(" clip_%02d %s %s" % x)
SL.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
print("KET QUA:", "SACH %d o anh" % len(res) if not bad else "LOI %d" % len(bad))
sys.exit(1 if bad else 0)
