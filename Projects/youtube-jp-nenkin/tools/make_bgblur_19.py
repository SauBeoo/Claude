# -*- coding: utf-8 -*-
r"""make_bgblur_19.py — dung san 13 clip NEN MO cho scene bang so cua video 19.

🔴 VI SAO PHAI CO TOOL NAY: ban dau nen mo lam bang **CSS filter** cua Remotion
   (`"filter": {"blur": 24, ...}` tren `OffthreadVideo` full-screen). Render chet o
   **frame 2765 (giay 92)** — dung clip `bgv-8` — voi:
       Timed out evaluating page function ... / Error: kill EPERM
   `blur(24px)` tren mot the video 1920x1080 la phep loc cuc dat trong browser;
   Chrome treo qua `delayRender()` timeout, roi Remotion kill tien trinh con va
   dinh EPERM. `EXITCODE=1`, KHONG co file, sau 10% cua mot luot 1h45.

⇒ Chuyen phep mo sang **ffmpeg** (dung san thanh file), Remotion chi con phat
   video thuong. Bonus: blur o 480px roi phong len 1920 => rat nhanh va con mo
   hon, dung y do "chi con la mang mau chuyen dong".

Quy doi CSS -> ffmpeg (KHONG cung thang do, dung bê nguyen so):
   CSS brightness 1.18  ->  eq brightness  +0.07   (ffmpeg: -1..1, 0 = goc)
   CSS saturate   0.30  ->  eq saturation   0.30   (cung thang)
   CSS contrast   0.55  ->  eq contrast     0.55   (cung thang)
   CSS blur(24px)@1920  ->  scale 480 + gblur sigma 6 + scale 1920

CHAY:  python tools/make_bgblur_19.py
"""
import io
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RV = os.path.join("E:" + os.sep, "Claude", "Projects", "remotion-vox")
PROJ_JSON = os.path.join(RV, "projects", "nenkin-19vox", "project.json")
ASSETS = [os.path.join(RV, "public", "projects", "nenkin-19vox", "assets"),
          os.path.join(RV, "public_n19", "projects", "nenkin-19vox", "assets")]

VF = ("scale=420:-2,gblur=sigma=10,eq=brightness=0.07:saturation=0.30:contrast=0.55,"
      "scale=1920:1080:flags=lanczos")


def main():
    doc = json.load(io.open(PROJ_JSON, encoding="utf-8"))
    vid = [c for t in doc["tracks"] if t["id"] == "trk-video" for c in t["clips"]]
    # project.json (sau khi builder doi) da tro toi `bgblur_...` — bo tien to de
    # lay lai TEN NGUON. Khong bo thi tool di tim file no sap tao ra.
    want = sorted({c["asset"].split("/")[-1].replace("bgblur_", "", 1)
                   for c in vid if c["id"].startswith("bgv-")})
    print(f"can dung {len(want)} clip nen mo")
    src_dir = ASSETS[0]
    done = 0
    for fn in want:
        src = os.path.join(src_dir, fn)
        out_name = "bgblur_" + fn
        dst = os.path.join(src_dir, out_name)
        if not os.path.exists(src):
            print(f"  🔴 thieu nguon {fn}")
            sys.exit(1)
        # resume theo mtime (render-background.md §2.5), khong chi exists
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            print(f"  skip {out_name} (moi hon nguon)")
            continue
        print(f"  {fn} -> {out_name}", flush=True)
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", VF, "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
             "-pix_fmt", "yuv420p", dst],
            capture_output=True, text=True, errors="replace")
        if r.returncode:
            print("    LOI:", (r.stderr or "")[:300])
            sys.exit(1)
        done += 1
    # hardlink sang public_n19 (thu muc render doc)
    for fn in want:
        a = os.path.join(ASSETS[0], "bgblur_" + fn)
        b = os.path.join(ASSETS[1], "bgblur_" + fn)
        if os.path.exists(a) and not os.path.exists(b):
            try:
                os.link(a, b)
            except OSError:
                import shutil
                shutil.copy(a, b)
    print(f"OK dung {done} clip mo · {len(want)} file co mat o ca 2 public")


if __name__ == "__main__":
    main()
