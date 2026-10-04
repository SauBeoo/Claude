# -*- coding: utf-8 -*-
"""Demo 'khoang lang de nghe am hoai niem': 2 khoanh khac, ~40s.
Synth giong Itako -> ghep voice + gap, chime ngan dung cho lang."""
import io, os, sys, wave
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demo_voice_showa import synth_line, VOICEVOX

OUT = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\01_kyushoku\_demo_pause"
SFX = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\01_kyushoku\_sfx"
os.makedirs(OUT, exist_ok=True)
SR = 44100
ITAKO = 109

def load_wav(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
        if w.getframerate() != SR:
            raise SystemExit(f"SR khac: {path}")
        return a

def tts(text):
    b = synth_line(text, ITAKO, VOICEVOX)
    with wave.open(io.BytesIO(b)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
        sr = w.getframerate()
    if sr != SR:  # resample tho neu can (VOICEVOX 24k)
        idx = np.linspace(0, len(a) - 1, int(len(a) * SR / sr))
        a = np.interp(idx, np.arange(len(a)), a)
    return a

# timeline: (audio hoac 'gap:sec', sfx_at_gap hoac None)
chime = load_wav(os.path.join(SFX, "school_chime.wav")) * 0.5
pa = load_wav(os.path.join(SFX, "pa_chime.wav")) * 0.5
segs = [
    (tts("この揚げパン、覚えていますか。"), None),
    ("gap:3.4", chime),
    (tts("きなこの粉で、口のまわりを真っ白にして食べた、あの味です。"), None),
    ("gap:1.2", None),
    (tts("いただきますの声のあとには、お昼の放送が流れていました。"), None),
    ("gap:3.6", pa),
    (tts("放送委員の、少し緊張した声と、聞き慣れたレコードの音楽。"), None),
    ("gap:2.0", None),
]
parts, sfx_events, t = [], [], 0.0
for seg, sfx in segs:
    if isinstance(seg, str):
        dur = float(seg.split(":")[1])
        parts.append(np.zeros(int(SR * dur)))
        if sfx is not None:
            sfx_events.append((t + 0.25, sfx))
        t += dur
    else:
        parts.append(seg)
        t += len(seg) / SR
mix = np.concatenate(parts)
for at, s in sfx_events:
    st = int(SR * at)
    mix[st:st + len(s)] += s[:len(mix) - st]
# nen phim cu rat khe
bed = load_wav(os.path.join(SFX, "film_bed.wav"))
reps = int(np.ceil(len(mix) / len(bed)))
mix += np.tile(bed, reps)[:len(mix)] * 0.06
mix = np.tanh(mix)
w = wave.open(os.path.join(OUT, "demo_pause.wav"), "wb")
w.setparams((1, 2, SR, 0, "NONE", ""))
w.writeframes((mix * 32767 * 0.85).astype(np.int16).tobytes())
w.close()
print(f"demo_pause.wav {len(mix)/SR:.1f}s | sfx tai: {[round(a,1) for a,_ in sfx_events]}")
