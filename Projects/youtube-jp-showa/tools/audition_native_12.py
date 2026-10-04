# -*- coding: utf-8 -*-
"""Cat DUNG 6 doan da tron tieng goc ra mot file ngan de NGHE KIEM.

Vi sao can: may chi DOAN duoc dau la tieng nen dau la tieng nguoi (nhip 2-8 Hz).
Nguong do khong thay duoc tai nguoi. Phai nghe roi moi dam phat.
Moi doan lay them 1.5 s truoc/sau de nghe duoc luc no vao va ra.
"""
import sys, json, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(__file__).resolve().parent.parent / "06_VIDEO" / "12_natsu-atarimae"
MP4 = VD / "12_natsu-atarimae_amb.mp4"
OUT = VD / "_audition"
PAD = 1.5
rows = json.loads((VD / "_native_pick.json").read_text(encoding="utf-8"))
OUT.mkdir(exist_ok=True)
parts = []
for i, r in enumerate(rows, 1):
    dst = OUT / ("nat%02d.mp4" % i)
    ss = max(r["t"] - PAD, 0)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.3f" % ss,
                    "-t", "%.3f" % (r["dur"] + PAD * 2), "-i", str(MP4),
                    "-vf", "scale=960:-2", "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "160k", str(dst)], check=False)
    if dst.exists():
        parts.append(dst)
        print("%d. slot %-4d t=%-6.0f %s" % (i, r["slot"], r["t"], r["desc"]))
lst = OUT / "nat.txt"
lst.write_text("".join("file '%s'\n" % p.as_posix() for p in parts), encoding="utf-8")
final = OUT / "AUDITION_NATIVE.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", str(lst), "-c", "copy", str(final)], check=False)
print("\n-> %s" % final)
