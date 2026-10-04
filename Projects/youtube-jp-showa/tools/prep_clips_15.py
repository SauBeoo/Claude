# -*- coding: utf-8 -*-
r"""prep_clips_15 — clips_raw/<ten mo ta>.mp4  ->  clips/clip_<index>.mp4 (da GRADE mau).

🔴 VI SAO PHAI DOI TEN THEO INDEX: `video_render.py` dinh danh clip bang **SO THU TU SLOT**
   (`clips/clip_<i>.mp4`), KHONG doc khoa `source` mo ta. Dat ten mo ta vao `clips/` thi
   renderer coi nhu KHONG CO CLIP NAO va am tham fallback anh tinh, `EXITCODE=0`, khong
   mot dong canh bao (CLAUDE.md §Visual). Ten mo ta giu o `clips_raw/` + bang tra `_MAP.txt`.

🎞️ GRADE: preset `showa70` cua tools/grade_showa.py.
   ⛔ Canh THOI NAY (`ima_ie`) KHONG grade — videogen_lib cho chung STYLE_MODERN rieng
   (sach, net); phu mau phim 1970 len la XOA MAT doi lap xua/nay, thu chinh la co che
   cua bai nay (cuon so cu trong tay nguoi thoi nay).

  py tools/prep_clips_15.py [--preset showa70|showa70_soft|showa70_deep] [--no-grade]
"""
import argparse, io, os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\15_haha-no-okane"
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

_src = open(os.path.join(TOOLS, "grade_showa.py"), encoding="utf-8").read()
_g = {}
exec(_src[_src.index("PRESETS = {"):_src.index("def run(")], _g)   # chi lay dict PRESETS
PRESETS = _g["PRESETS"]

ap = argparse.ArgumentParser()
ap.add_argument("--preset", default="showa70", choices=sorted(PRESETS))
ap.add_argument("--no-grade", action="store_true")
a = ap.parse_args()

# ⭐ CROP VIEN PHIM + UPSCALE 1080p (do 2026-09-17)
# Lo clip van con VIEN DEN quanh khung du guard da nam o 1-3% prompt — mong hon lo truoc
# (khong con lo rang) nhung van thay bang mat. Do do day tren 4 clip dai dien:
#   tren 0-11px · duoi 0-11px · trai 16-37px · phai 16-32px  (khung 1280x720)
# => cat 44px moi ben ngang + 25px moi ben doc, giu dung 16:9, roi scale len 1920x1080
#    (clip Flow ra 720p ma renderer xuat 1080p, nen dang nao cung phai upscale).
# ⚖️ Re hon gen lai 60 clip, va KHONG dung toi noi dung: vien nam ngoai vung co vat the.
CROP = "crop=1192:670:44:25,scale=1920:1080:flags=lanczos"

ten = [l.split()[1] for l in io.open(os.path.join(VD, "videogen_TENFILE.txt"), encoding="utf-8")
       if l.strip() and not l.startswith("#")]
raw, out = os.path.join(VD, "clips_raw"), os.path.join(VD, "clips")
os.makedirs(out, exist_ok=True)

ok = skip = miss = 0
for i, name in enumerate(ten):
    src = os.path.join(raw, name)
    dst = os.path.join(out, "clip_%02d.mp4" % i)   # 🔴 %02d — SLIDES ghi clips/clip_00.mp4
    if not os.path.exists(src):
        print("  !! THIEU %s (index %d)" % (name, i)); miss += 1; continue
    # resume dung luat §2.5: so MTIME, khong hoi "da co file chua"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        skip += 1; ok += 1; continue
    # canh THOI NAY: KHONG grade mau phim cu (giu doi lap xua/nay) — nhung VAN crop vien
    vf = CROP if (a.no_grade or "ima_ie" in name) else CROP + "," + PRESETS[a.preset]
    if True:
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src,
                            "-filter_complex", vf,
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-an", dst], capture_output=True)
        if r.returncode:
            sys.stderr.write(r.stderr.decode("utf-8", "replace")[-400:] + "\n")
            print("  !! grade fail: %s" % name); continue
    ok += 1
    if ok % 25 == 0:
        print("  [%3d/%d] %s" % (ok, len(ten), name))

io.open(os.path.join(out, "_MAP.txt"), "w", encoding="utf-8").write(
    "index -> ten mo ta (ban goc o clips_raw/)\n" +
    "\n".join("clip_%-4d %s" % (i, n) for i, n in enumerate(ten)) + "\n")

n_modern = sum(1 for n in ten if "ima_ie" in n)
print("\nxong: %d/%d clip -> %s" % (ok, len(ten), out))
print("  grade '%s': %d clip | GIU NGUYEN (thoi nay): %d | bo qua vi da moi: %d | thieu: %d"
      % (a.preset, ok - n_modern - skip if not a.no_grade else 0, n_modern, skip, miss))
sys.exit(1 if miss else 0)
