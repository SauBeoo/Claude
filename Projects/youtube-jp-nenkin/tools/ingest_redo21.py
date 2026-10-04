# -*- coding: utf-8 -*-
r"""ingest_redo21.py — nhan LO GEN LAI cua video 21 (danh so theo THU TU BOM).

🔴 VI SAO KHONG DUNG `ingest_clips_21.py`: tool do map `task_<DONG_GOC>` (001,
   006, 007, 023...), con extension danh so lo gen lai theo **thu tu bom**
   (001..007). Map nham thi 7 clip vao SAI 7 cho — va **khong gate nao bat duoc**
   vi file van du, ten van dung, render van exit 0.
   => Doc bang doi chieu tu `flow21_REDO_TENFILE.txt` (cot thu_tu_bom).

Lam 3 viec giong `ingest_clips_21.py`: cat watermark "Veo" (do lai lo nay:
**x 1860-1895, y 1040-1060**, trung lo truoc) · bo audio · doi ten theo shot.

CHAY:  python tools/ingest_redo21.py <thu_muc>
       python tools/ingest_redo21.py <thu_muc> --check
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "21_fuyo-shinkokusho-205man")
OUT = os.path.join(VD, "clips")
VF = "crop=1840:1035:0:0,scale=1920:1080:flags=lanczos"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.split("CHAY:")[1]); return 1
    src = args[0]
    rows = []
    for ln in io.open(os.path.join(VD, "flow21_REDO_TENFILE.txt"),
                      encoding="utf-8").read().split("\n")[1:]:
        c = ln.split("\t")
        if len(c) >= 4 and c[0].strip().isdigit():
            rows.append((int(c[0]), int(c[1]), c[2].strip(), c[3].strip()))
    print(f"{len(rows)} cho can lap")
    todo = []
    for bom, goc, fn, key in rows:
        p = os.path.join(src, f"task_{bom:03d}_1_1080p.mp4")
        if not os.path.exists(p):
            print(f"🔴 THIEU {p}"); return 1
        todo.append((p, os.path.join(OUT, fn), bom, goc, key))
    for p, d, bom, goc, key in todo:
        print(f"   bom {bom:03d}  ->  {os.path.basename(d):32s} (dong goc {goc:03d})")
    if "--check" in sys.argv:
        return 0
    for i, (p, d, bom, goc, key) in enumerate(todo, 1):
        rc = subprocess.call(["ffmpeg", "-v", "error", "-y", "-i", p,
                              "-vf", VF, "-an", "-c:v", "libx264",
                              "-preset", "veryfast", "-crf", "17",
                              "-pix_fmt", "yuv420p", "-r", "24", d])
        print(f"[{i}/{len(todo)}] {os.path.basename(d)}  "
              f"{'OK' if rc == 0 else 'LOI rc=' + str(rc)}", flush=True)
        if rc:
            return 2
    print("XONG:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
