# -*- coding: utf-8 -*-
"""bench_visual.py — mo LOP HINH video mau (kenh thang ngach) de chep khuon do hoa.

Do (may) — tai dung cach do da kiem chung trong workspace:
- nhip cat: MAD frame ke nhau 2 khung/s tren 160x90, BO 22% day (dai phu de), cat = MAD > 8 (nhu check_motion.py).
  ⛔ khong dung ffmpeg scdet: dem phu de doi thanh cat canh (lech 4x, showa/CHANNEL_BENCHMARK_stills_2026-09-08.md).
- giu hinh trung vi / dai nhat · do sang TB · do bao hoa TB · 5 mau chu dao (k-means tren anh thu nho)
Xuat (soi MAT phan dinh tinh): <id>_sheet.jpg (1 khung/10s, co nhan giay) + <id>_open.jpg (30s dau, 1 khung/2,5s).
Chay: python tools/bench_visual.py 01_SOURCES/_bench/*.mp4
"""
import sys, io, glob, json
from pathlib import Path
import numpy as np
import cv2

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def sheet(cap, fps, times, out, cols=6, w=320):
    h = w * 9 // 16
    rows = (len(times) + cols - 1) // cols
    s = np.full((rows * h, cols * w, 3), 255, np.uint8)
    for k, t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
        if not ok:
            continue
        f = cv2.resize(f, (w, h))
        cv2.rectangle(f, (0, 0), (58, 16), (0, 0, 0), -1)
        cv2.putText(f, f"{int(t // 60)}:{int(t % 60):02d}", (3, 12), 0, 0.42, (0, 255, 255), 1)
        y, x = (k // cols) * h, (k % cols) * w
        s[y:y + h, x:x + w] = f
    cv2.imwrite(str(out), s, [cv2.IMWRITE_JPEG_QUALITY, 85])


def analyze(path):
    p = Path(path)
    cap = cv2.VideoCapture(str(p)); fps = cap.get(5); n = int(cap.get(7)); dur = n / fps
    step = max(1, int(round(fps / 2)))
    prev, mads, bright, sat, pix = None, [], [], [], []
    for i in range(0, n, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
        if not ok:
            break
        sm = cv2.resize(f, (160, 90))
        top = sm[: int(90 * 0.78)]
        g = cv2.cvtColor(top, cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            mads.append(np.abs(g - prev).mean())
        prev = g
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        bright.append(hsv[..., 2].mean()); sat.append(hsv[..., 1].mean())
        if len(pix) < 400:
            pix.append(cv2.resize(sm, (32, 18)).reshape(-1, 3))
    mads = np.array(mads)
    cuts = np.where(mads > 8)[0]
    holds = np.diff(np.r_[0, cuts, len(mads)]) / 2.0
    holds = holds[holds > 0]
    data = np.vstack(pix).astype(np.float32)
    _, lab, cen = cv2.kmeans(data, 5, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 3,
                             cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab.ravel(), minlength=5)
    pal = [("#%02X%02X%02X" % tuple(int(v) for v in cen[k][::-1]), round(cnt[k] / cnt.sum() * 100)) for k in np.argsort(-cnt)]
    sheet(cap, fps, list(np.arange(5, dur - 2, 10.0)), p.with_name(p.stem + "_sheet.jpg"))
    sheet(cap, fps, list(np.arange(0.5, min(30, dur), 2.5)), p.with_name(p.stem + "_open.jpg"))
    r = {"video": p.stem, "dur_s": round(dur, 1), "cuts_per_min": round(len(cuts) / (dur / 60), 2),
         "hold_median_s": round(float(np.median(holds)), 1) if len(holds) else None,
         "hold_max_s": round(float(holds.max()), 1) if len(holds) else None,
         "MAD_mean": round(float(mads.mean()), 2), "bright": round(float(np.mean(bright))),
         "sat": round(float(np.mean(sat))), "palette": pal}
    print(json.dumps(r, ensure_ascii=False))
    return r


if __name__ == "__main__":
    out = [analyze(f) for a in sys.argv[1:] for f in sorted(glob.glob(a))]
    if out:
        Path(sys.argv[1]).parent.joinpath("_bench_visual.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                                         encoding="utf-8")
