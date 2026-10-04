# -*- coding: utf-8 -*-
"""Đo khách quan 4 wav demo: F0 trung bình (cao/thấp giọng), dải F0, tốc độ, độ to."""
import io, sys, wave, math
from pathlib import Path
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

D = Path(r"E:\Claude\Projects\youtube-jp-kaigo\00_VOICE_TEST")
NCHAR = 200  # số ký tự đoạn demo

def f0_track(x, sr, fmin=60, fmax=400, frame=0.04, hop=0.02):
    n = int(sr * frame); h = int(sr * hop)
    out = []
    for i in range(0, len(x) - n, h):
        w = x[i:i + n].astype(np.float64)
        if np.sqrt(np.mean(w * w)) < 0.01:      # bỏ khoảng lặng
            continue
        w = w - w.mean()
        ac = np.correlate(w, w, mode="full")[n - 1:]
        lo, hi = int(sr / fmax), int(sr / fmin)
        if hi >= len(ac):
            continue
        seg = ac[lo:hi]
        k = int(np.argmax(seg)) + lo
        if ac[0] <= 0 or seg.max() / ac[0] < 0.3:  # không đủ tuần hoàn → vô thanh
            continue
        out.append(sr / k)
    return np.array(out)

print(f"{'File':38} {'dài':>6} {'nói':>6} {'ký/phút':>8} {'F0 TB':>7} {'F0 dải':>13} {'RMS dB':>7}")
for p in sorted(D.glob("demo_*.wav")):
    with wave.open(str(p)) as r:
        sr, nf, sw, ch = r.getframerate(), r.getnframes(), r.getsampwidth(), r.getnchannels()
        raw = r.readframes(nf)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        x = x.reshape(-1, 2).mean(axis=1)
    dur = nf / sr
    # thời gian thực có tiếng (RMS theo khung 20ms)
    h = int(sr * 0.02)
    frames = np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)])
    voiced = float((frames > 0.01).sum()) * 0.02
    f0 = f0_track(x, sr)
    med = np.median(f0) if len(f0) else float("nan")
    p10, p90 = (np.percentile(f0, [10, 90]) if len(f0) else (float("nan"),) * 2)
    rms = 20 * math.log10(max(np.sqrt(np.mean(x ** 2)), 1e-9))
    print(f"{p.name:38} {dur:5.1f}s {voiced:5.1f}s {NCHAR/(voiced/60):8.0f} {med:6.0f}Hz {p10:5.0f}–{p90:<5.0f}Hz {rms:6.1f}")
