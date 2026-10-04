#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""generate_sfx.py — synth 11 SFX one-shot cho video Vox-collage, chạy local bằng numpy.

Cách dùng:
    python generate_sfx.py <output_dir>          # vd: python generate_sfx.py public/sfx

Xuất 11 file wav (44.1kHz mono 16-bit), mỗi cái một vai — pairing gợi ý với
animation variant (xem references/animation-variants.md), coi là điểm xuất phát
chứ không phải luật:

    whoosh   — entrance lướt nhanh (rise, swipe-in), chuyển cảnh
    pop      — TitleTag chip hiện (frame ~6 của scene), support element pop-in
    coin     — con số/tiền/stat xuất hiện (punch phrase về số liệu)
    thud     — hero nặng rơi xuống (variant punch, wobble-drop chạm đất)
    boing    — variant boing/wobble-drop nảy, element bật vào tinh nghịch
    swipe    — variant flip/peel, element trượt ngang
    click    — chi tiết nhỏ hiện, tick list, magnifier zoom
    riser    — build-up trước reveal (đặt TRƯỚC beat 0.5-0.8s)
    drop     — reveal xấu/tụt dốc (chart đi xuống, sụp đổ)
    shatter  — variant shatter, khoảnh khắc đổ vỡ
    paper    — cutout dán vào nền (mọi entrance kiểu sticker), chuyển layer

Mỗi video nên RẢI đều bộ này qua các scene — video nào scene nào cũng cùng 2-3
tiếng thì flat y như video dùng 1 animation cho mọi scene. Thiếu tiếng nào hợp
nội dung thì THÊM hàm synth mới vào đây thay vì đi tìm sample library ngoài.
Volume khi wire vào Remotion giữ 0.3-0.55 (texture dưới narration, không cạnh tranh).
"""
import os
import sys
import wave

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

SR = 44100


def _write(path, sig):
    """Normalize peak -3dB rồi ghi wav 16-bit mono."""
    peak = np.max(np.abs(sig)) or 1.0
    sig = sig / peak * 0.7079  # -3 dBFS
    data = (sig * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"  {os.path.basename(path):12s} {len(sig)/SR:.2f}s")


def _t(dur):
    return np.linspace(0, dur, int(SR * dur), endpoint=False)


def _env(n, attack=0.01, release=0.3):
    """Envelope attack-release đơn giản theo tỉ lệ độ dài."""
    e = np.ones(n)
    a = max(1, int(n * attack))
    r = max(1, int(n * release))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    return e


def _noise(dur, seed):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(int(SR * dur))


def _onepole_lp(x, cutoff):
    """Lowpass 1 cực, cutoff Hz (scalar hoặc mảng cùng độ dài — cho sweep)."""
    if np.isscalar(cutoff):
        cutoff = np.full(len(x), float(cutoff))
    alpha = 1 - np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def _sine_sweep(dur, f0, f1, curve=1.0):
    t = _t(dur)
    f = f0 + (f1 - f0) * (t / dur) ** curve
    phase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(phase)


def whoosh():
    dur = 0.55
    n = _noise(dur, 1)
    t = _t(dur)
    # bandpass sweep giả lập: lowpass sweep lên rồi xuống + highpass bằng diff
    cutoff = 300 + 2800 * np.sin(np.pi * t / dur)
    x = _onepole_lp(n, cutoff)
    x = np.diff(x, prepend=0)  # bỏ ù trầm
    return x * _env(len(x), attack=0.35, release=0.4)


def pop():
    dur = 0.14
    body = _sine_sweep(dur, 420, 150, curve=0.6)
    click = _noise(0.006, 2) * 0.6
    sig = body * _env(len(body), attack=0.005, release=0.7)
    sig[: len(click)] += click
    return sig


def coin():
    dur = 0.5
    t = _t(dur)
    decay = np.exp(-t * 7)
    sig = 0.6 * np.sin(2 * np.pi * 988 * t) + 0.5 * np.sin(2 * np.pi * 1319 * t)
    # nốt 2 vào sau 60ms (kiểu coin game cổ điển)
    d = int(0.06 * SR)
    sig[d:] += 0.5 * np.sin(2 * np.pi * 1319 * t[:-d])
    return sig * decay


def thud():
    dur = 0.35
    body = _sine_sweep(dur, 120, 45, curve=0.5)
    t = _t(dur)
    sig = body * np.exp(-t * 14)
    punch = _onepole_lp(_noise(0.02, 3), 900) * 1.5
    sig[: len(punch)] += punch * np.linspace(1, 0, len(punch))
    return sig


def boing():
    dur = 0.6
    t = _t(dur)
    vib = 220 * np.exp(-t * 3.5) * np.sin(2 * np.pi * 11 * t)
    f = 180 + vib
    phase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(phase) * np.exp(-t * 4)


def swipe():
    dur = 0.22
    n = _noise(dur, 4)
    t = _t(dur)
    cutoff = 4500 - 3800 * (t / dur)
    x = _onepole_lp(n, cutoff)
    x = np.diff(x, prepend=0)
    return x * _env(len(x), attack=0.1, release=0.5)


def click():
    dur = 0.03
    n = _noise(dur, 5)
    x = np.diff(np.diff(n, prepend=0), prepend=0)  # highpass gắt
    return x * _env(len(x), attack=0.05, release=0.8)


def riser():
    dur = 0.85
    t = _t(dur)
    tone = _sine_sweep(dur, 200, 1150, curve=1.4)
    n = _onepole_lp(_noise(dur, 6), 200 + 3000 * (t / dur) ** 2) * 0.5
    grow = (t / dur) ** 1.6
    return (tone * 0.6 + n) * grow * _env(len(t), attack=0.02, release=0.06)


def drop():
    dur = 0.55
    t = _t(dur)
    sig = _sine_sweep(dur, 620, 55, curve=0.7)
    return sig * np.exp(-t * 3.2) * _env(len(t), attack=0.01, release=0.25)


def shatter():
    dur = 0.65
    rng = np.random.default_rng(7)
    t = _t(dur)
    sig = np.diff(_onepole_lp(_noise(dur, 8), 6000), prepend=0) * np.exp(-t * 6)
    # sparkle: 14 hạt sine cao tần rơi rải rác
    for _ in range(14):
        f = rng.uniform(1800, 6500)
        start = rng.uniform(0, 0.3)
        d = rng.uniform(0.08, 0.25)
        i0 = int(start * SR)
        seg = _t(d)
        piece = np.sin(2 * np.pi * f * seg) * np.exp(-seg * 22) * rng.uniform(0.15, 0.4)
        end = min(len(sig), i0 + len(piece))
        sig[i0:end] += piece[: end - i0]
    return sig


def paper():
    dur = 0.4
    rng = np.random.default_rng(9)
    n = _noise(dur, 10)
    # crinkle: biên độ nhấp nhô ngẫu nhiên tần số thấp
    mod = _onepole_lp(rng.standard_normal(len(n)), 30)
    mod = 0.4 + 0.6 * (mod - mod.min()) / (np.ptp(mod) or 1)
    x = np.diff(_onepole_lp(n * mod, 5500), prepend=0)
    return x * _env(len(x), attack=0.08, release=0.35)


SOUNDS = {
    "whoosh": whoosh, "pop": pop, "coin": coin, "thud": thud, "boing": boing,
    "swipe": swipe, "click": click, "riser": riser, "drop": drop,
    "shatter": shatter, "paper": paper,
}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    print(f"Synth {len(SOUNDS)} SFX -> {out}")
    for name, fn in SOUNDS.items():
        _write(os.path.join(out, f"{name}.wav"), fn())
    print("XONG.")


if __name__ == "__main__":
    main()
