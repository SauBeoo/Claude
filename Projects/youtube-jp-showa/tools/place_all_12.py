# -*- coding: utf-8 -*-
"""Dat CA LO 165 clip gen theo THU TU FLOW -> clips/clip_00..clip_164.mp4

Dung khi da bom videogen_FLOW.txt mot mach va tai ve theo dung thu tu dong:
    task_001 -> dong 1 -> clip_00.mp4 ... task_165 -> dong 165 -> clip_164.mp4
=> KHONG phai ghep bang mat nhu lo truoc.

Moi clip: cat 5% mep (bo dai phim) -> 1920x1080. Ban DOC 1080x1920 thi keo nguoc truoc.

    python tools/place_all_12.py <thu_muc>            -> kiem tra, khong dung file
    python tools/place_all_12.py <thu_muc> --apply    -> cat va dat vao clips/
"""
import sys, os, re, subprocess, ctypes
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
DST = VD / "clips"
N = 165

try:
    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetPriorityClass(ctypes.c_void_p(k.GetCurrentProcess()), 0x00004000)
except Exception:
    pass


def probe(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True).stdout.strip()
    try:
        w, h = (int(x) for x in o.split(",")[:2])
        return w, h
    except Exception:
        return None


def ok_file(p):
    """File con doc duoc va du dai khong — chong file bi cat cut luc tai/ghi.
    (Bay §2.5 render-background.md: hoi 'con DUNG khong', khong phai 'co chua'.)"""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip()) >= 1.0
    except Exception:
        return False


if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    print("Thieu thu muc nguon. Vd: python tools/place_all_12.py F:\\Youtube\\Du_an_xx")
    sys.exit(2)
SRC = Path(sys.argv[1])
apply_it = "--apply" in sys.argv

# gom theo so task, moi task lay ban NGANG (720p/1080p deu duoc; ngang hon doc)
best = {}
for p in SRC.glob("task_*.mp4"):
    m = re.match(r"task_(\d+)", p.name)
    if not m:
        continue
    wh = probe(p)
    if not wh:
        continue
    w, h = wh
    cand = (0 if w > h else 1, -w, p.name, p)
    n = int(m.group(1))
    if n not in best or cand < best[n]:
        best[n] = cand
nums = sorted(best)

print("tim thay        : %d task (%s..%s)" % (len(nums), nums[0] if nums else "-", nums[-1] if nums else "-"))
print("can             : %d" % N)
missing = [i for i in range(1, N + 1) if i not in best]
if missing:
    print("THIEU task      : %d -> %s%s" % (len(missing), missing[:15],
                                            " ..." if len(missing) > 15 else ""))
doc = [n for n in nums if best[n][0] == 1]
if doc:
    print("ban DOC (se keo nguoc): %d -> %s" % (len(doc), doc[:15]))

if not apply_it:
    print("")
    print("(chay lai voi --apply de cat 5%% mep va dat vao clips/)")
    sys.exit(0)

DST.mkdir(parents=True, exist_ok=True)
done = fail = 0
for n in nums:
    if n > N:
        continue
    slot = n - 1
    src = best[n][3]
    out = DST / ("clip_%02d.mp4" % slot)
    w, h = probe(src)
    pre = "" if w > h else "scale=1920:1080,"          # doc thi go nen ngang TRUOC
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-vf", pre + "crop=iw*0.90:ih*0.90:iw*0.05:ih*0.05,"
                "scale=1920:1080:flags=lanczos,setsar=1",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-an", str(out)], check=False)
    if r.returncode == 0 and out.exists() and ok_file(out):
        done += 1
    else:
        fail += 1
        print("  LOI task_%03d -> clip_%02d" % (n, slot))
    if n % 20 == 0:
        print("  ... %d/%d" % (n, len(nums)), flush=True)

con = [i for i in range(N) if not (DST / ("clip_%02d.mp4" % i)).exists()]
print("")
print("dat xong : %d | loi: %d" % (done, fail))
if con:
    print("⛔ CON THIEU %d/%d CLIP — CHUA DUOC RENDER (render-background.md §1.5)" % (len(con), N))
    print("   slot thieu: %s%s" % (con[:20], " ..." if len(con) > 20 else ""))
else:
    print("DU %d/%d clip. Buoc tiep: render nen bang 06_VIDEO/run_render12.cmd" % (N, N))
sys.exit(1 if (fail or con) else 0)
