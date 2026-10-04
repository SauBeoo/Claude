# -*- coding: utf-8 -*-
"""Cat nen magenta clip nguoi ke (yawa) -> webm VP9 alpha, lap ping-pong.
Chay: python tools/cut_narrator.py <in.mp4> <out.webm> [--crop x0,y0,x1,y1]
Luat: media-library.md 2.10 (9): co mask ~3px, giu blob lon nhat, do vet tim sau cat."""
import sys, io, argparse, subprocess, cv2, numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--crop", default="110,135,840,720"); ap.add_argument("--erode", type=int, default=3)
ap.add_argument("--key", default="182,102,239", help="BGR nen, do tu chinh clip")
ap.add_argument("--fade", type=int, default=60, help="px mo o mep tren; 0 = tat (clip thay tron nguoi)")
a = ap.parse_args(); x0, y0, x1, y1 = map(int, a.crop.split(","))
cap = cv2.VideoCapture(a.src); fps = cap.get(5); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f[y0:y1, x0:x1])
H, W = frames[0].shape[:2]
KEY = np.array(list(map(float, a.key.split(","))), np.float32)
FADE = np.clip(np.arange(H, dtype=np.float32) / a.fade, 0, 1)[:, None] if a.fade else np.ones((H, 1), np.float32)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.erode + 1, 2 * a.erode + 1))
out = []; purple = []
for f in frames:
    dist = np.linalg.norm(f.astype(np.float32) - KEY, axis=2)
    m = (dist > 70).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == big).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))  # lap lo nho trong nguoi
    m = cv2.erode(m, k)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m[(hsv[..., 0] >= 140) & (hsv[..., 0] <= 172) & (hsv[..., 1] > 80)] = 0   # xoa khe magenta CLOSE lap nham; loc theo TONG mau (da/ao kem khong dinh)
    alpha = cv2.GaussianBlur(m.astype(np.float32), (5, 5), 0)
    alpha *= FADE                                          # mep tren mo dan, khong cat phang
    f = f.copy(); fb, fg_, fr = [f[..., i].astype(np.int32) for i in range(3)]
    sp = (fr - fg_ > 40) & (fb - fg_ > 40)                 # despill: pixel am magenta o vien -> keo R,B ve G
    f[..., 2][sp] = np.minimum(fr, fg_ + 30)[sp].astype(np.uint8); f[..., 0][sp] = np.minimum(fb, fg_ + 30)[sp].astype(np.uint8)
    b, g, r = [f[..., i].astype(int) for i in range(3)]
    purple.append(int(((alpha > 0.05) & (r - g > 40) & (b - g > 40)).sum()))
    out.append(np.dstack([f, (alpha * 255).astype(np.uint8)]))
seq = out + out[-2:0:-1]                                   # ping-pong -> lap muot
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-auto-alt-ref", "0", a.dst], stdin=subprocess.PIPE)
for x in seq: p.stdin.write(x.tobytes())
p.stdin.close(); p.wait()
cv2.imwrite(a.dst.replace(".webm", "_frame.png"), out[len(out) // 2])
print(f"{a.dst}: {W}x{H} {len(seq)} frame ({len(seq)/fps:.1f}s) | vet tim max {max(purple)} px | exit {p.returncode}")
