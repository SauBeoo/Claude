# -*- coding: utf-8 -*-
"""kenburns.py — zoom/truot CHAM + MUOT cho o anh tinh (khuon video 08 showa, do 2026-09-24).

Do tren v08 (video thang cua kenh): moi anh mot huong, xoay vong — zoom vao ~5%/3s, zoom ra,
truot ngang/doc ~30–50 px/s (khung 1920). ⚠️ Memory cu "ghet Ken Burns" la vi RUNG: nguyen nhan
la zoompan/crop cua ffmpeg lam tron toa do ve SO NGUYEN -> o toc do cham moi frame nhay 0 hoac 1px.
Tool nay bien doi tung frame bang cv2.warpAffine (toa do le, INTER_CUBIC) + ease cosine -> khong giat.
  python kenburns.py <in.mp4> <out.mp4> --mode zin|zout|pl|pr|tu|td [--amount 0.07]
Doc clip da hoa dong cuc bo (animate_still) -> chong them chuyen dong khung. Khong co tieng.
"""
import argparse, json, math, subprocess, sys
import numpy as np, cv2
ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--mode", default="zin", choices=["zin", "zout", "pl", "pr", "tu", "td"])
ap.add_argument("--amount", type=float, default=0.07, help="zoom tong (0.07 = 7%) hoac quang truot theo ti le khung")
ap.add_argument("--crf", default="18")
a = ap.parse_args()

pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                                "stream=width,height,r_frame_rate,nb_read_packets", "-of", "json", a.inp],
                               capture_output=True, text=True).stdout)["streams"][0]
W, H = int(pr["width"]), int(pr["height"]); n = int(pr["nb_read_packets"])
num, den = map(int, pr["r_frame_rate"].split("/")); fps = num / den
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H),
                        "-r", "%.6f" % fps, "-i", "-", "-an", "-c:v", "libx264", "-crf", a.crf, "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
base = 1.0 + a.amount + 0.02          # phong to san de truot khong lo mep
for i in range(n):
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    p = i / max(1, n - 1); e = 0.5 - 0.5 * math.cos(math.pi * p)     # ease in-out
    s, dx, dy = base, 0.0, 0.0
    if a.mode == "zin":  s = 1.0 + 0.01 + a.amount * e
    if a.mode == "zout": s = 1.0 + 0.01 + a.amount * (1 - e)
    span = a.amount * W / 2
    if a.mode == "pl": dx = span * (1 - 2 * e)
    if a.mode == "pr": dx = -span * (1 - 2 * e)
    span_y = a.amount * H / 2
    if a.mode == "tu": dy = span_y * (1 - 2 * e)
    if a.mode == "td": dy = -span_y * (1 - 2 * e)
    M = np.float32([[s, 0, (1 - s) * W / 2 + dx], [0, s, (1 - s) * H / 2 + dy]])
    enc.stdin.write(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
sys.exit(enc.returncode)
