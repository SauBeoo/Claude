# -*- coding: utf-8 -*-
"""8 clip FIX8 bi gen ra 1080x1920 (DOC) -> keo nguoc ve 16:9 + cat 5% mep + dat vao clips/.

🔴 CHAN DOAN (do 2026-09-12): file la 1080x1920, NHUNG noi dung ben trong la canh 16:9
   bi NEN NGANG, khong phai bo cuc doc. Bang chung: resize ve 1920x1080 thi nguoi co ti le
   binh thuong; de nguyen thi nguoi cao leu ngheu; cat giua ve 16:9 thi mat dau.
   => Keo nguoc lai la TRA VE dung hinh, khong mat mot chut khung nao.

⚠️ Cai gia: chieu ngang chi co 1080 mau that, keo len 1920 nen hoi mem. Chap nhan duoc,
   va van hon gen lai (gen lai chua chac ra dung khung neu setting tool chua sua).

Thu tu filter co y:
   scale 1920x1080   -> go nen ngang TRUOC
   crop 90% + scale  -> bo dai phim / lo rang cua (giong ca lo 168 clip kia)
"""
import sys, os, subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# thu muc nguon truyen qua dong lenh; mac dinh la lo dau tien
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else Path(r"F:\Youtube") / "Dự_án_mới_27_1mlztx0p"
ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
DST = VD / "clips"
CHK = VD / "_sheet"

# thu tu dong trong videogen_FIX8_FLOW.txt -> slot  (xem videogen_FIX8_TENFILE.txt)
ORDER = [78, 81, 84, 118, 157, 162, 163, 164]

DST.mkdir(parents=True, exist_ok=True)
CHK.mkdir(parents=True, exist_ok=True)
def probe(p):
    import subprocess as sp
    o = sp.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height", "-of", "csv=p=0", str(p)],
               capture_output=True, text=True).stdout.strip()
    w, h = (int(x) for x in o.split(",")[:2])
    return w, h

# Mot task co the co NHIEU ban xuat (720p / 1080p). Uu tien ban NGANG san (w>h):
# no la 16:9 nguyen goc, hon han ban doc phai keo gian (1080 mau ngang -> 1920).
best = {}
for p in SRC.glob("task_*.mp4"):
    n = p.name.split("_")[1]              # task_00N_...
    w, h = probe(p)
    cand = (0 if w > h else 1, -w, p)     # ngang truoc; trong cung nhom lay ban to hon
    if n not in best or cand < best[n]:
        best[n] = cand
files = [best[k][2] for k in sorted(best)]
print("tim thay %d task (chon 1 ban xuat moi task)" % len(files))
if len(files) != len(ORDER):
    print("[CHAN] co %d task nhung can %d" % (len(files), len(ORDER)))
    sys.exit(1)

ok = 0
for f, slot in zip(files, ORDER):
    out = DST / ("clip_%02d.mp4" % slot)
    w, h = probe(f)
    pre = "" if w > h else "scale=1920:1080,"      # doc thi go nen ngang TRUOC
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(f),
         "-vf", pre + "crop=iw*0.90:ih*0.90:iw*0.05:ih*0.05,"
                "scale=1920:1080:flags=lanczos,setsar=1",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-an", str(out)],
        check=False)
    if r.returncode == 0 and out.exists():
        ok += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3.5", "-i", str(out),
                        "-frames:v", "1", "-vf", "scale=320:-2",
                        str(CHK / ("fix8_%03d.jpg" % slot))], check=False)
        print("  %-26s %-9s -> clip_%02d.mp4" % (f.name, "ngang" if w > h else "DOC->keo", slot))
    else:
        print("  LOI: %s" % f.name)

print("")
print("xong %d/%d" % (ok, len(ORDER)))
sys.exit(0 if ok == len(ORDER) else 1)
