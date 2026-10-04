# -*- coding: utf-8 -*-
"""make_beat.py — synth a simple 120bpm beat track (kick + hat), pure numpy.
For beat-synced demo edits; license-clean like generate_sfx.py.

Usage: py -3 tools/make_beat.py <out.wav> [--seconds 12] [--bpm 120]
"""

import argparse
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
SR = 44100


def kick(t):
    f = 95 * np.exp(-t * 22) + 42
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def hat(t, seed):
    rng = np.random.default_rng(seed)
    n = rng.standard_normal(len(t))
    # crude highpass: diff
    n = np.diff(n, prepend=0)
    return n * np.exp(-t * 55) * 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=12.0)
    ap.add_argument("--bpm", type=float, default=120.0)
    args = ap.parse_args()

    total = int(args.seconds * SR)
    buf = np.zeros(total)
    beat = 60.0 / args.bpm  # seconds per beat

    i = 0
    t_hit = np.arange(int(0.35 * SR)) / SR
    while i * beat < args.seconds:
        at = int(i * beat * SR)
        seg = min(len(t_hit), total - at)
        if seg <= 0:
            break
        buf[at:at + seg] += kick(t_hit[:seg]) * (1.0 if i % 4 == 0 else 0.8)
        # hats on the off-beat
        off = at + int(beat / 2 * SR)
        if off + seg < total:
            buf[off:off + seg] += hat(t_hit[:seg], seed=i) * 0.6
        i += 1

    buf = buf / max(1e-9, np.max(np.abs(buf))) * 0.7  # ~-3dBFS
    pcm = (buf * 32767).astype(np.int16)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"OK {out} — {args.seconds}s @ {args.bpm}bpm ({i} beat)")


if __name__ == "__main__":
    main()
