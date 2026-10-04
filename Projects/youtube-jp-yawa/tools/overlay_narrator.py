# -*- coding: utf-8 -*-
"""overlay_narrator.py — ghep nguoi ke (09_BRAND/narrator/narrator_B_full.webm, VP9 alpha, lap) vao
goc duoi-phai video yawa sau khi video_render.py xong. An o 20s cuoi (cho end screen YouTube).
Chay: python tools/overlay_narrator.py <in.mp4> <out.mp4> [--h 380] [--margin 30] [--hide-tail 20]"""
import sys, io, argparse, subprocess
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--h", type=int, default=380); ap.add_argument("--margin", type=int, default=30)
ap.add_argument("--hide-tail", type=float, default=20.0)
a = ap.parse_args()
nar = PROJ / "09_BRAND" / "narrator" / "narrator_B_full.webm"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.src]))
end = max(dur - a.hide_tail, 0)
fc = (f"[1:v]scale=-1:{a.h},format=yuva420p[n];"
      f"[0:v][n]overlay=W-w-{a.margin}:H-h:shortest=1:enable='lt(t,{end:.2f})'[v]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.src, "-stream_loop", "-1", "-c:v", "libvpx-vp9", "-i", str(nar),
       "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
       "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", a.dst]
r = subprocess.run(cmd)
print(f"overlay nguoi ke: 0..{end:.1f}s / {dur:.1f}s -> {a.dst} | exit {r.returncode}")
sys.exit(r.returncode)
