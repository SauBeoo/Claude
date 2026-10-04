# -*- coding: utf-8 -*-
"""scrub_sheets.py — contact sheet CO MOC GIAY de soi phim PD bang mat (RANGES_VERIFIED.md quy trinh §1).

Moi sheet = 4x4 o, moi o 480x(270|360) = 1 frame moi STEP giay (mac dinh 5s) => 80s phim / sheet.
Nhan vang tren o = giay trong phim (so nguyen) — ghi thang vao bang vung.
Mot lan ffmpeg / sheet (fps=1/STEP tren doan do), khong seek tung frame.

  python tools/scrub_sheets.py <phim> <thu_muc_ra> [--step 5] [--from 0] [--to END] [--w 480]
In ra danh sach sheet. ⛔ O < 450px bo sot chu tren bien hieu (quy trinh §1: >=620px khi nghi ngo -> --w 640).
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--step", type=float, default=5.0)
ap.add_argument("--from", dest="t0", type=float, default=0.0)
ap.add_argument("--to", dest="t1", type=float, default=None)
ap.add_argument("--w", type=int, default=480)
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("--rows", type=int, default=4)
a = ap.parse_args()

src = Path(a.src); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(src)],
                   capture_output=True, text=True)
dur = float(json.loads(r.stdout)["format"]["duration"])
t1 = min(a.t1 or dur, dur)
per = a.cols * a.rows
span = per * a.step
import cv2, numpy as np, tempfile, shutil
k = 0
t = a.t0
tmp = Path(tempfile.mkdtemp(prefix="scrub_"))
while t < t1 - 0.5:
    k += 1
    seg = min(span, t1 - t)
    dst = out / ("s_%03d_%05d.jpg" % (k, int(t)))
    for f in tmp.glob("*.png"): f.unlink()
    # frame dau doan lay o t + step/2 (giua o), nhan = giay tuyet doi cua frame do
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % t, "-t", "%.2f" % seg, "-i", str(src),
                    "-vf", "fps=1/%g:start_time=0,scale=%d:-2" % (a.step, a.w), str(tmp / "f_%03d.png")], check=False)
    fr = sorted(tmp.glob("f_*.png"))
    tiles = []
    for j, f in enumerate(fr[:per]):
        im = cv2.imread(str(f))
        if im is None: continue
        lab = "%ds" % int(t + j * a.step)
        cv2.rectangle(im, (0, 0), (8 + 17 * len(lab), 32), (0, 0, 0), -1)
        cv2.putText(im, lab, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        tiles.append(im)
    if tiles:
        h, w = tiles[0].shape[:2]
        sheet = np.full((a.rows * (h + 4), a.cols * (w + 4), 3), 90, np.uint8)
        for j, im in enumerate(tiles):
            rr, cc = divmod(j, a.cols)
            im = cv2.resize(im, (w, h))
            sheet[rr*(h+4):rr*(h+4)+h, cc*(w+4):cc*(w+4)+w] = im
        cv2.imwrite(str(dst), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
        print(dst.name, "%d-%ds" % (int(t), int(t + seg)))
    t += span
shutil.rmtree(tmp, ignore_errors=True)
print("XONG %d sheet, %.0fs phim, step %gs" % (k, t1 - a.t0, a.step))
