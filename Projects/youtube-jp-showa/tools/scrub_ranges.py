# -*- coding: utf-8 -*-
"""scrub_ranges.py — cat frame moi `step` giay trong CAC VUNG chi dinh -> 1 contact sheet / vung (ghi mm:ss).
python tools/scrub_ranges.py <video> <out_dir> <step> "label=mm:ss-mm:ss" ...
"""
import sys, io, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def mmss(s):
    m, x = s.split(":"); return int(m) * 60 + float(x)

vid, out, step = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
for spec in sys.argv[4:]:
    label, rng = spec.split("=", 1); a, b = rng.split("-"); t0, t1 = mmss(a), mmss(b)
    d = out / label; d.mkdir(exist_ok=True)
    for f in d.glob("f_*.jpg"): f.unlink()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", str(t1 - t0), "-i", str(vid),
                    "-vf", f"fps=1/{step},scale=320:-2", "-q:v", "5", str(d / "f_%04d.jpg")], check=True)
    frames = sorted(d.glob("f_*.jpg"))
    if not frames: print(label, "0 frame"); continue
    W = 320; H = Image.open(frames[0]).size[1]; COLS = 6; ROWS = (len(frames) + COLS - 1) // COLS
    sh = Image.new("RGB", (W * COLS, H * ROWS), "black"); dr = ImageDraw.Draw(sh)
    for i, f in enumerate(frames):
        im = Image.open(f).convert("RGB"); sh.paste(im, ((i % COLS) * W, (i // COLS) * H))
        t = t0 + i * step
        dr.rectangle(((i % COLS) * W, (i // COLS) * H, (i % COLS) * W + 62, (i // COLS) * H + 14), fill="black")
        dr.text(((i % COLS) * W + 3, (i // COLS) * H + 2), f"{int(t//60):02d}:{int(t%60):02d}", fill="yellow")
    sh.save(out / f"{label}.jpg", quality=80); print(label, len(frames), "frames ->", out / f"{label}.jpg")
