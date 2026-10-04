# -*- coding: utf-8 -*-
"""still_kb.py — dung o anh tinh = ANH SACH + zoom/truot cham (khuon video 08), KHONG meo cuc bo.

User 2026-09-24: "video no cu luon song nhe nhe… bo cai do di" -> lop hoa dong cuc bo cua
animate_still.py (meo hoi nuoc/khoi/khong khi nong) bi BO cho showa. Chuyen dong con lai duy nhat:
Ken Burns do tren v08 (zoom ~5%/3s hoac truot cham), bien doi tu ANH GOC do phan giai cao
bang cv2.warpAffine toa do le -> 1 lan lay mau, khong giat, net hon.
  python still_kb.py <anh> <out.mp4> --dur 8.5 --mode zin|zout|pl|pr|tu|td [--amount 0.07] [--wm 0.905]
--wm: cat phai tai ti le nay (bo ✦ anh AI) roi trim 16:9 chia doi tren/duoi (media-library §2.10).
"""
import argparse, math, subprocess, sys
import numpy as np, cv2
ap = argparse.ArgumentParser()
ap.add_argument("img"); ap.add_argument("out")
ap.add_argument("--dur", type=float, required=True)
ap.add_argument("--mode", default="zin", choices=["zin", "zout", "pl", "pr", "tu", "td"])
ap.add_argument("--amount", type=float, default=0.07)
ap.add_argument("--wm", type=float, default=0.0)
ap.add_argument("--fps", type=int, default=24)
ap.add_argument("--crf", default="18")
a = ap.parse_args()
W, H = 1920, 1080
im = cv2.imdecode(np.fromfile(a.img, np.uint8), cv2.IMREAD_COLOR)
if im is None:
    sys.exit("khong doc duoc anh " + a.img)
h0, w0 = im.shape[:2]
if a.wm:
    im = im[:, :int(w0 * a.wm)]
    h0, w0 = im.shape[:2]
# cover-crop ve 16:9 (giu giua)
if w0 / h0 > W / H:
    nw = int(h0 * W / H); x0 = (w0 - nw) // 2; im = im[:, x0:x0 + nw]
else:
    nh = int(w0 * H / W); y0 = (h0 - nh) // 2; im = im[y0:y0 + nh]
h0, w0 = im.shape[:2]
if w0 < W:                                  # anh nho: phong truoc bang Lanczos cho net
    im = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4); h0, w0 = H, W
k = w0 / W                                  # ti le anh goc / khung ra
n = int(round(a.dur * a.fps))
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H),
                        "-r", str(a.fps), "-i", "-", "-an", "-c:v", "libx264", "-crf", a.crf, "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
for i in range(n):
    p = i / max(1, n - 1); e = 0.5 - 0.5 * math.cos(math.pi * p)
    z, dx, dy = 1.0 + a.amount + 0.01, 0.0, 0.0
    if a.mode == "zin":  z = 1.01 + a.amount * e
    if a.mode == "zout": z = 1.01 + a.amount * (1 - e)
    if a.mode == "pl": dx = (a.amount * W / 2) * (1 - 2 * e)
    if a.mode == "pr": dx = -(a.amount * W / 2) * (1 - 2 * e)
    if a.mode == "tu": dy = (a.amount * H / 2) * (1 - 2 * e)
    if a.mode == "td": dy = -(a.amount * H / 2) * (1 - 2 * e)
    s = z / k                                # anh goc -> khung ra
    M = np.float32([[s, 0, W / 2 - s * w0 / 2 + dx], [0, s, H / 2 - s * h0 / 2 + dy]])
    fr = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC,
                        borderMode=cv2.BORDER_REFLECT)
    enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait()
sys.exit(enc.returncode)
