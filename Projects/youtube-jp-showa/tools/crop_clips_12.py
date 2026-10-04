# -*- coding: utf-8 -*-
"""Cat 5% moi mep cua 170 clip Flow -> bo dai phim / lo rang cua, roi scale ve 1920x1080.

Vi sao cat CA LO chu khong chi clip dinh (user chot 2026-09-12): clip dinh bi zoom 5%
con clip sach thi khong => ngoi canh nhau trong cung mot doan se thay CO NGUOI NHAY.
Cat deu thi khong ai nhan ra.

Muc 5% do bang MAT tren _sheet/crop_test.jpg (goc / 5% / 8%): 5% da sach o moi clip nang
nhat, 8% chi mat them khung. ⛔ Detector do bang may da BAO OAN (tieu chi "dem chuyen
sang-toi" bat ca hang rao/dam dong/tan la) — xem 04_VIDEOGEN_PROMPTS.md §2.1.

⛔ LOAI 2 clip khoi lo:
   #010 Characters_entering_preschool  -> clip rac (nhan vat hoat hinh), khong thuoc video 12
   #158 Woman_walking_in_residential   -> CO DIEU HOA gan tuong, giet luan diem "nha khong may lanh"
"""
import os, sys, subprocess, ctypes
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(__file__).resolve().parent.parent / "06_VIDEO" / "12_natsu-atarimae"
RAW = VD / "_flow_raw"
OUT = VD / "_flow_crop"
BAD = {10, 158}          # theo chi so #NNN cua contact sheet (= thu tu sorted cua _flow_raw)

# ha do uu tien de khong lam don may (render-background.md §1 muc 7)
try:
    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = ctypes.c_void_p      # thieu dong nay = fail im lang tren 64-bit
    k.SetPriorityClass(ctypes.c_void_p(k.GetCurrentProcess()), 0x00004000)
except Exception:
    pass

def _ok(p):
    """File mp4 co doc duoc va du dai khong (chong file cut dau duoi)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip()) >= 1.0
    except Exception:
        return False


OUT.mkdir(parents=True, exist_ok=True)
files = sorted(os.listdir(RAW))
done = skipped = failed = 0
for i, f in enumerate(files):
    if i in BAD:
        print("BO QUA #%03d  %s" % (i, f))
        skipped += 1
        continue
    dst = OUT / ("c%03d.mp4" % i)
    # 🔴 2026-09-12: dieu kien cu chi hoi "co file chua + moi hon nguon chua".
    #   File bi CAT CUT luc tien trinh bi kill thoa CA HAI => bi bo qua, va chi lo ra
    #   luc render ("moov atom not found", chunk 40/42 chet). Dung bay §2.5 cua
    #   render-background.md: phai hoi "file con DUNG khong", khong phai "co chua".
    if dst.exists() and dst.stat().st_mtime >= (RAW / f).stat().st_mtime and _ok(dst):
        done += 1
        continue
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(RAW / f),
         "-vf", "crop=iw*0.90:ih*0.90:iw*0.05:ih*0.05,scale=1920:1080:flags=lanczos",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-an", str(dst)],
        check=False)
    if r.returncode == 0 and dst.exists():
        done += 1
    else:
        failed += 1
        print("LOI #%03d %s" % (i, f))
    if (i + 1) % 20 == 0:
        print("  ... %d/%d" % (i + 1, len(files)), flush=True)

print("")
print("cat xong : %d" % done)
print("bo qua   : %d  (#010 rac, #158 dieu hoa)" % skipped)
print("loi      : %d" % failed)
print("-> %s" % OUT)
sys.exit(1 if failed else 0)
