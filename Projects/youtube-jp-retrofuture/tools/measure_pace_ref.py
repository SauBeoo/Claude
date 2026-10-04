# -*- coding: utf-8 -*-
"""Do TOC DO DI CHUYEN CUA MAY trong video mau — DUNG DON VI (theo SHOT, khong theo cua so).

Chay:  python tools/measure_pace_ref.py <video mau> [--step 2]

🔴 HAI BAY DA DINH, ca hai ghi lai o day:
  ① DON VI: lan truoc do "117px median" tren CUA SO 8 GIAY BAT KY. Cua so nao chua CAT CANH
     thi dich khung khong lo => median bi day len. Clip cua minh la MOT shot 8s khong cat
     => phai so voi SHOT cua mau. (Cung ho camera-language.md §8: MAD ca bai vs MAD trong shot.)
  ② RAM: ban dau giu TAT CA frame grayscale trong list => 14.400 frame x 921KB = 13GB, an 7,4GB
     roi treo. Ban nay STREAMING: chi giu frame DAU SHOT + frame TRUOC.
"""
import sys, math, argparse, statistics as st
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--step", type=int, default=2, help="lay mau moi N frame (2 = nhanh gap doi)")
ap.add_argument("--min-shot", type=float, default=3.0)
a = ap.parse_args()

cap = cv2.VideoCapture(a.video)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
ok, fr = cap.read()
if not ok:
    sys.exit("khong doc duoc")
H, W = fr.shape[:2]
han = cv2.createHanningWindow((W, H), cv2.CV_32F)

g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
shot_first, prev = g.copy(), g          # ⭐ chi hai frame nam trong RAM
shot_t0, t = 0.0, 0.0
CUT = 26.0                              # MAD tiny32 vuot nguong = cat canh
shots, steps, idx = [], [], 0

while True:
    for _ in range(a.step):
        ok, fr = cap.read()
        idx += 1
        if not ok:
            break
    if not ok:
        break
    t = idx / fps
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    mad = float(np.mean(cv2.absdiff(cv2.resize(g, (32, 18)), cv2.resize(prev, (32, 18)))))
    if mad > CUT:                       # dong shot cu
        dur = t - shot_t0
        if dur >= a.min_shot and steps:
            (tx, ty), _ = cv2.phaseCorrelate(np.float32(shot_first), np.float32(prev), han)
            d = math.hypot(tx, ty)
            med = st.median(steps)
            shots.append((dur, d, d / dur * 8.0, med,
                          st.median([abs(s - med) for s in steps])))
        shot_first, shot_t0, steps = g.copy(), t, []
    else:
        (sx, sy), _ = cv2.phaseCorrelate(np.float32(prev), np.float32(g), han)
        steps.append(math.hypot(sx, sy) / a.step)     # quy ve MOI FRAME
    prev = g
cap.release()

dur = t - shot_t0
if dur >= a.min_shot and steps:
    (tx, ty), _ = cv2.phaseCorrelate(np.float32(shot_first), np.float32(prev), han)
    d = math.hypot(tx, ty); med = st.median(steps)
    shots.append((dur, d, d / dur * 8.0, med, st.median([abs(s - med) for s in steps])))

print(f"file : {a.video.split('/')[-1]}")
print(f"khung: {W}x{H} | fps {fps:.1f} | {t:.0f}s | lay mau moi {a.step} frame")
print(f"shot >={a.min_shot}s: {len(shots)}\n")
shots.sort(key=lambda r: r[2])
print(f"{'shot':>7}{'dich':>9}{'/8giay':>9}{'buoc/fr':>9}{'jitter':>8}")
for d_, dd, p8, med, jit in shots:
    print(f"{d_:>6.1f}s{dd:>8.1f}p{p8:>8.1f}p{med:>9.3f}{jit:>8.3f}")

p8 = [r[2] for r in shots]
if p8:
    j = [r[4] for r in shots]
    print(f"\n*** DICH KHUNG QUY VE 8 GIAY — n={len(p8)} shot ***")
    print(f"  min {min(p8):.1f}  p25 {np.percentile(p8,25):.1f}  MEDIAN {st.median(p8):.1f}"
          f"  p75 {np.percentile(p8,75):.1f}  max {max(p8):.1f}")
    for lim in (10, 20, 40, 80):
        n = sum(1 for x in p8 if x < lim)
        print(f"  shot < {lim:>3}p/8s : {n:>3}/{len(p8)} = {100*n/len(p8):.0f}%")
    print(f"  jitter median {st.median(j):.3f} | dai {min(j):.3f}-{max(j):.3f}")
