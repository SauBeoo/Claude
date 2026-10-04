# -*- coding: utf-8 -*-
"""Synth 2 lop am hoai niem (license sach 100% - tu tao):
1. school_chime.wav — chuong truong Westminster (キーンコーンカーンコーン)
2. film_bed.wav — nen phim cu: hum may chieu + crackle vinyl, 40s loop duoc
"""
import numpy as np, wave, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

def bell(freq, dur, vol=0.5):
    t = np.linspace(0, dur, int(SR*dur), False)
    tone = (np.sin(2*np.pi*freq*t) * 1.0
            + np.sin(2*np.pi*freq*2.76*t) * 0.35
            + np.sin(2*np.pi*freq*5.40*t) * 0.12)
    env = np.exp(-t*1.7)
    return tone * env * vol

# Westminster: E4 C4 D4 G3 / G3 D4 E4 C4
E4, C4, D4, G3 = 329.63, 261.63, 293.66, 196.00
seq = [E4, C4, D4, G3, None, G3, D4, E4, C4]
gap = 0.62
total = gap*len(seq) + 3.5
chime = np.zeros(int(SR*total))
for i, f in enumerate(seq):
    if f is None: continue
    s = bell(f, 3.2, 0.42)
    st = int(SR*gap*i)
    chime[st:st+len(s)] += s[:len(chime)-st]
chime = np.tanh(chime)  # soft clip
w = wave.open(os.path.join(OUT, "school_chime.wav"), "wb")
w.setparams((1, 2, SR, 0, 'NONE', ''))
w.writeframes((chime*32767*0.8).astype(np.int16).tobytes()); w.close()
print("school_chime.wav", round(total,1), "s")

# film bed: pink-ish noise (hum) + random pops (crackle)
dur = 40.0
rng = np.random.default_rng(1963)
n = int(SR*dur)
white = rng.normal(0, 1, n)
# lowpass thô (moving average) -> hum am
kernel = np.ones(220)/220
hum = np.convolve(white, kernel, 'same') * 2.2
# crackle: pop ngau nhien
crackle = np.zeros(n)
for _ in range(int(dur*9)):
    p = rng.integers(0, n-80)
    amp = rng.uniform(0.12, 0.5) * rng.choice([1,-1])
    L = rng.integers(15, 70)
    crackle[p:p+L] += amp * np.exp(-np.linspace(0, 6, L))
# flutter cua may chieu: bien do dao dong 24Hz nhe
t = np.arange(n)/SR
flutter = 1 + 0.15*np.sin(2*np.pi*24*t)
bed = (hum*0.5 + crackle) * flutter * 0.5
bed = np.tanh(bed)
# fade 2 dau de loop em
f = int(SR*0.8)
bed[:f] *= np.linspace(0,1,f); bed[-f:] *= np.linspace(1,0,f)
w = wave.open(os.path.join(OUT, "film_bed.wav"), "wb")
w.setparams((1, 2, SR, 0, 'NONE', ''))
w.writeframes((bed*32767*0.8).astype(np.int16).tobytes()); w.close()
print("film_bed.wav", dur, "s")
