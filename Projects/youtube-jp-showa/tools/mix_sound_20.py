# -*- coding: utf-8 -*-
"""mix_sound_20.py — lop AM THANH GOC cho video 20 (khuon mix_sound_19.py).

Tron vao ban SACH 20_sumai-okane_nosfx.mp4 -> 20_sumai-okane.mp4 (-c:v copy):
  ① tieng goc clip AI (ban goc Flow) + clip quay that — chi o native_20.json 'use' (mod 2-8Hz < 0,35)
  ② nen moi truong (効果音ラボ, khong can credit) -34 dBFS: khu nha yen tinh o hook · khong khi 銭湯 dong 35-39
  ③ <=3 diem nhan dung loi ke: ngan keo 茶だんす (1) · guoc からんころん (34) · bep ga ぼっ (73)
Gain = MUC TIEU - mean DO DUOC cua file. Lan dau: doi ten ban render thanh _nosfx (chi 1 lan).
    python tools/probe_native_20.py && python tools/mix_sound_20.py
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:/Claude/Projects/youtube-jp-showa/06_VIDEO/20_sumai-okane")
REN, SRC, SFX = VD / "20_sumai-okane.mp4", VD / "20_sumai-okane_nosfx.mp4", VD / "sfx"
BED, AMB = -34.0, -34.0
# mean do bang volumedetect 2026-09-27
MEAN = {"quiet-residential-area2": -43.0, "bath1": -32.0, "walk-geta1": -28.8, "key-in1": -30.0,
        "stove-burner-ignition1": -38.3, "drawer-open1": -34.8}
TL = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]


def at(line_sub, word=None):
    """moc giay cua dong chua line_sub; word -> uoc vi tri chu trong dong theo ti le ky tu."""
    ln = next(x for x in TL if line_sub in x["text"])
    if not word:
        return ln["start"]
    k = ln["text"].index(word) / max(1, len(ln["text"]))
    return ln["start"] + k * (ln["end"] - ln["start"])


def span(a, b):
    return at(b) - at(a)


# (file, bat dau, dai, offset trong file, muc tieu dB, fade)
EV = [
    ("quiet-residential-area2", 0.0, at("こんばんは。昭和くらし図鑑"), 0.0, BED, 1.5),          # hook: nha me, yen
    ("drawer-open1", at("茶だんすを片づけていたら", "片づけ"), 0.62, 0.0, -22.0, 0.05),   # ③ hook: keo ngan keo go (thay key-in1 — user: 30s dau thieu tieng that)
    ("walk-geta1", at("下駄の音が", "下駄"), 3.2, 0.0, -24.0, 0.3),                             # ③ からん、ころん
    ("bath1", at("のれんをくぐると、番台"), span("のれんをくぐると、番台", "では、なぜ、家にお風呂が"), 0.0, AMB, 1.5),
    ("stove-burner-ignition1", at("ぼっ、という音"), 2.0, 0.0, -20.0, 0.1),                     # ③ ぼっ
]
assert sum(1 for e in EV if e[4] > -30) <= 3, "qua 3 tieng nhan"

nat = json.loads((VD / "native_20.json").read_text(encoding="utf-8"))
if not SRC.exists():
    assert REN.exists(), "chua co ban render"
    REN.rename(SRC)
inputs, chains, k = ["-i", str(SRC)], [], 1


def add(path, ss, t0, dur, gain, fade):
    global k
    inputs.extend(["-ss", "%.2f" % ss, "-t", "%.2f" % dur, "-i", str(path)])
    fo = max(0.0, dur - fade)
    chains.append("[%d:a]aresample=48000,aformat=channel_layouts=mono,volume=%.1fdB,afade=t=in:d=%.2f,"
                  "afade=t=out:st=%.2f:d=%.2f,adelay=%d:all=1[s%d]" % (k, gain, fade, fo, fade, int(t0 * 1000), k))
    k += 1


for f, t0, dur, off, tgt, fade in EV:
    add(SFX / (f + ".mp3"), off, t0, dur, tgt - MEAN[f], fade)
    print("SFX  %-18s @%7.2fs  %.1fs  gain %+.1f dB" % (f, t0, dur, tgt - MEAN[f]))
for i, v in nat.items():
    if not v["use"]:
        continue
    g = min(AMB - v["mean"], 18.0)
    add(VD / v["src"], v["ss"], v["t"], v["dur"], g, 0.6)
    print("GOC  clip_%-3s %-24s @%7.2fs  %.1fs  gain %+.1f dB" % (i, v["code"], v["t"], v["dur"], g))
n = k - 1
fc = ";".join(chains) + ";[0:a]aresample=48000[v];[v]" + "".join("[s%d]" % j for j in range(1, n + 1)) + \
     "amix=inputs=%d:duration=first:normalize=0,alimiter=limit=0.708:level=disabled[a]" % (n + 1)
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                                                  "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(REN)]
subprocess.run(cmd, check=True)
print("OK", n, "lop am thanh ->", REN.name)
