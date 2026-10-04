# -*- coding: utf-8 -*-
"""Video 13: cat dai phim 5% moi mep cho 162 clip Flow -> scale 1920x1080 -> dat vao
clips/clip_NN.mp4 theo DUNG thu tu slot ma SLIDES doi.

Vi sao cat CA LO (theo crop_clips_12.py): clip dinh dai phim bi zoom 5% con clip sach thi
khong => ngoi canh nhau se thay CO NGUOI NHAY. Do o video 13: soi mat 4 mau thi 4/4 canh
Showa deu co dai phim (so + lo rang cua), 15 canh `ima_*` thi sach. Cat deu thi khong ai
nhan ra, VA no chuan hoa luon lo clip dang lan 720p/1080p.

🔴 video_render.py tim clip bang `clips/clip_<index>.mp4` theo SO THU TU SLOT, khong doc
   khoa `source`. Dat sai ten => renderer am tham fallback anh tinh, preflight van xanh.

Nguon: F:\\Youtube\\showa_13_uyfd62mb\\task_NNN_*.mp4  (NNN = dong videogen_FLOW.txt = slot NNN-1)
"""
import os, re, sys, json, glob, subprocess, ctypes
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "13_kosodate-joushiki"
SRC = Path(r"F:\Youtube\showa_13_uyfd62mb")
OUT = VD / "_flow_crop"
DST = VD / "clips"
SL = ROOT / "03_SCRIPTS" / "13_kosodate-joushiki_SLIDES.json"

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


slides = json.loads(SL.read_text(encoding="utf-8"))
n_slot = len(slides)

# 🔴 3 slot dung ANH TU LIEU THAT (hoa dong bang animate_still.py), KHONG phai clip AI.
#    Bo qua o day, neu khong buoc cat se ghi de mat. Dat bang tools/place_photos_13.py.
PHOTO_SLOTS = {154}

# task_NNN -> file. Vai so co 2 ban (gen lai): lay ban MOI NHAT.
raw = {}
for f in glob.glob(str(SRC / "task_*.mp4")):
    n = int(re.search(r"task_(\d+)_", os.path.basename(f)).group(1))
    if n not in raw or os.path.getmtime(f) > os.path.getmtime(raw[n]):
        raw[n] = f

missing = [i for i in range(1, n_slot + 1) if i not in raw]
if missing:
    print("[CHAN] thieu clip cho slot:", missing)
    sys.exit(1)
print("SLIDES %d slot | nguon %d clip | du" % (n_slot, len(raw)))

OUT.mkdir(parents=True, exist_ok=True)
DST.mkdir(parents=True, exist_ok=True)
done = skip = fail = 0
for i in range(n_slot):                      # slot i  <-  task_(i+1)
    if i in PHOTO_SLOTS:
        continue
    src = Path(raw[i + 1])
    mid = OUT / ("c%03d.mp4" % i)
    # §2.5 render-background: hoi "file con DUNG khong", khong phai "co chua"
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
thieu = [i for i in range(n_slot) if i not in have and i not in PHOTO_SLOTS]
print("clips/clip_NN.mp4 co:", len(have), "| thieu slot (tru anh that):", thieu or "khong")
print("slot dung ANH THAT (dat rieng):", sorted(PHOTO_SLOTS))
sys.exit(1 if fail else 0)
