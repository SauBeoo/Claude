# -*- coding: utf-8 -*-
"""make_lullaby.py — synth nhạc nền storybook mềm (pad hợp âm + pluck ngũ cung),
pure numpy, license sạch. Cho phim hoạt hình/kể chuyện — khác hẳn make_beat.py.

Usage: py -3 tools/make_lullaby.py <out.wav> [--seconds 80]
"""

import argparse
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
SR = 44100

# C dur pentatonic-ish, tần số nốt (Hz)
N = {
    "C3": 130.81, "F3": 174.61, "G3": 196.0, "A3": 220.0, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0,
    "A4": 440.0, "C5": 523.25, "D5": 587.33, "E5": 659.26, "G5": 783.99,
}
CHORDS = [
    ("C4", "E4", "G4"), ("A3", "C4", "E4"),
    ("F3", "A3", "C4"), ("G3", "B3", "D4"),
]
MELODY_POOL = ["C5", "D5", "E5", "G5", "A4", "G4", "E4"]


def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for f in freqs:
        x += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    # attack 1s / release 1s
    env = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.0)
    return x * env * 0.16


def pluck(freq, dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    x = (np.sin(2 * np.pi * freq * t)
         + 0.4 * np.sin(2 * np.pi * 2 * freq * t)
         + 0.15 * np.sin(2 * np.pi * 3 * freq * t))
    return x * np.exp(-t * 2.8) * 0.22


def soften(x):
    k = np.ones(9) / 9.0  # moving average = lowpass nhẹ
    return np.convolve(x, k, mode="same")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=80.0)
    args = ap.parse_args()

    total = int(args.seconds * SR)
    buf = np.zeros(total + SR * 3)
    rng = np.random.default_rng(7)

    # pad hợp âm: mỗi hợp âm 4s, xoay vòng
    t = 0.0
    ci = 0
    while t < args.seconds:
        freqs = [N[n] for n in CHORDS[ci % len(CHORDS)]]
        seg = pad(freqs, 4.4)
        at = int(t * SR)
        buf[at:at + len(seg)] += seg[:len(buf) - at]
        t += 4.0
        ci += 1

    # melody pluck: mỗi 2s một nốt, thỉnh thoảng nghỉ
    t = 2.0
    while t < args.seconds - 3:
        if rng.random() > 0.25:
            note = MELODY_POOL[int(rng.integers(len(MELODY_POOL)))]
            seg = pluck(N[note])
            at = int(t * SR)
            buf[at:at + len(seg)] += seg[:len(buf) - at]
        t += 2.0

    buf = soften(buf[:total])
    # fade out 3s cuối
    fade = np.minimum(1, (total - np.arange(total)) / (3 * SR))
    buf *= fade
    buf = buf / max(1e-9, np.max(np.abs(buf))) * 0.5  # ~-6dBFS
    pcm = (buf * 32767).astype(np.int16)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"OK {out} — {args.seconds:.0f}s nhac storybook")


if __name__ == "__main__":
    main()
