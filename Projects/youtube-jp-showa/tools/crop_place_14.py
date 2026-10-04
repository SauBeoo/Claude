# -*- coding: utf-8 -*-
"""Video 14: cat dai phim 5% moi mep cho 171 clip Flow -> scale 1920x1080 -> dat vao
clips/clip_NN.mp4 theo DUNG thu tu slot ma SLIDES doi.

Khuon lay tu crop_place_13.py. Ba thu giu nguyen vi da chung minh:
 · CAT CA LO: clip dinh dai phim bi zoom 5% con clip sach thi khong => ngoi canh nhau
   se thay CO NGUOI NHAY. Cat deu thi khong ai nhan ra, VA no chuan hoa luon lo 720p.
 · Resume hoi "file con DUNG khong" (so mtime), khong hoi "co chua" — `render-background.md` §2.5.
 · 🔴 Renderer tim clip bang `clips/clip_<index>.mp4` theo SO THU TU SLOT (video_render.py
   dong 516: f"clip_{i:02d}.mp4"), KHONG doc khoa `source`. Dat sai ten => renderer am tham
   fallback anh tinh va preflight VAN xanh (thieu clip chi vao `warns`).

Nguon: F:\\Youtube\\Du_an_moi_ljwzyvmw\\task_NNN_*.mp4  (NNN = dong videogen_FLOW.txt = slot NNN-1)
"""
import os, re, sys, json, glob, subprocess, ctypes
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
STEM = "14_showa-no-shokuba"
VD = ROOT / "06_VIDEO" / STEM
SRC = Path(r"F:\Youtube") / "Dự_án_mới_ljwzyvmw"
OUT = VD / "_flow_crop"
DST = VD / "clips"
SL = ROOT / "03_SCRIPTS" / (STEM + "_SLIDES.json")

# ha do uu tien de khong lam don may (render-background.md §1 muc 7)
try:
    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = ctypes.c_void_p   # thieu dong nay = fail im lang tren 64-bit
    k.SetPriorityClass(ctypes.c_void_p(k.GetCurrentProcess()), 0x00004000)
except Exception:
    pass


def _ok(p, need=1.0):
    """File mp4 co doc duoc va du dai khong (chong file cut dau duoi khi bi kill)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip()) >= need
    except Exception:
        return False


if not SL.exists():
    print("[CHAN] chua co", SL.name, "— chay build_slides_14.py truoc")
    sys.exit(1)
slides = json.loads(SL.read_text(encoding="utf-8"))
n_slot = len(slides)

# task_NNN -> file. Vai so co 2 ban (gen lai): lay ban MOI NHAT.
raw = {}
for f in glob.glob(str(SRC / "task_*.mp4")):
    n = int(re.search(r"task_(\d+)_", os.path.basename(f)).group(1))
    if n not in raw or os.path.getmtime(f) > os.path.getmtime(raw[n]):
        raw[n] = f

missing = [i for i in range(1, n_slot + 1) if i not in raw]
if missing:
    print("[CHAN] SLIDES doi %d slot nhung thieu clip cho slot: %s" % (n_slot, missing))
    print("       nguon co %d clip (task_001..task_%03d)" % (len(raw), max(raw) if raw else 0))
    sys.exit(1)
extra = len(raw) - n_slot
print("SLIDES %d slot | nguon %d clip | du%s"
      % (n_slot, len(raw), (" (%d clip thua, khong dung)" % extra) if extra > 0 else ""))

OUT.mkdir(parents=True, exist_ok=True)
DST.mkdir(parents=True, exist_ok=True)
done = skip = fail = 0
for i in range(n_slot):                      # slot i  <-  task_(i+1)
    src = Path(raw[i + 1])
    mid = OUT / ("c%03d.mp4" % i)
    if mid.exists() and mid.stat().st_mtime >= src.stat().st_mtime and _ok(mid):
        skip += 1
    else:
        r = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
             "-vf", "crop=iw*0.90:ih*0.90:iw*0.05:ih*0.05,scale=1920:1080:flags=lanczos",
             "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-an", str(mid)], check=False)
        if r.returncode == 0 and mid.exists() and _ok(mid):
            done += 1
        else:
            fail += 1
            print("LOI slot %03d  <- %s" % (i, src.name))
            continue
    dst = DST / ("clip_%02d.mp4" % i)
    if dst.exists():
        dst.unlink()
    try:
        os.link(mid, dst)                    # hardlink: 0 byte ton them (cung o E:)
    except OSError:
        import shutil; shutil.copy2(mid, dst)

print("crop: moi %d | bo qua (da co) %d | loi %d" % (done, skip, fail))
have = sorted(int(re.search(r"clip_(\d+)\.mp4", p.name).group(1)) for p in DST.glob("clip_*.mp4"))
thieu = [i for i in range(n_slot) if i not in have]
print("clips/clip_NN.mp4 co:", len(have), "| thieu slot:", thieu or "khong")
sys.exit(1 if (fail or thieu) else 0)
