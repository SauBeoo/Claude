# -*- coding: utf-8 -*-
"""mix_sound_19.py — lop AM THANH GOC cho video 19 (khuon mix_sound_18.py).

Tron vao ban SACH 19_kaimono-joushiki_nosfx.mp4 -> 19_kaimono-joushiki.mp4 (-c:v copy):
  ① tieng goc clip AI (ban goc Flow) + clip quay that — chi o native_19.json 'use' (mod 2-8Hz < 0,35)
  ② nen moi truong (効果音ラボ, khong can credit) -34 dBFS: gio dem dong o hook, qua chieu o 商店街
  ③ <=3 diem nhan dung loi ke: cua keo 玄関 · mo がま口 · dong 1円 roi
Gain = MUC TIEU - mean DO DUOC cua file. Lan dau: doi ten ban render thanh _nosfx (chi 1 lan).
    python tools/probe_native_19.py && python tools/mix_sound_19.py
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\19_kaimono-joushiki")
REN, SRC, SFX = VD / "19_kaimono-joushiki.mp4", VD / "19_kaimono-joushiki_nosfx.mp4", VD / "sfx"
BED, AMB = -34.0, -34.0
MEAN = {"wind4": -22.8, "evening-crow1": -28.2, "slidingdoor-open2": -30.0, "wallet-open1": -36.1, "money-drop1": -33.9}
TL = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]


def at(line_sub, word=None):
    """moc giay cua dong chua line_sub; word -> uoc vi tri chu trong dong theo ti le ky tu."""
    ln = next(x for x in TL if line_sub in x["text"])
    if not word:
        return ln["start"]
    k = ln["text"].index(word) / max(1, len(ln["text"]))
    return ln["start"] + k * (ln["end"] - ln["start"])


# (file, bat dau, dai, offset trong file, muc tieu dB, fade)
EV = [
    ("wind4", 0.0, 26.0, 0.0, BED, 1.5),                                        # 昭和四十五年の冬 (hook dem dong)
    ("slidingdoor-open2", 0.6, 2.0, 0.0, -24.0, 0.1),                           # ③ 玄関で… cua keo
    ("wallet-open1", at("がま口を開きながら", "開き"), 0.45, 0.0, -20.0, 0.05),     # ③ 母のがま口を開きながら
    ("evening-crow1", at("夕方六時。商店街は"), 22.0, 2.0, -36.0, 1.5),          # 夕方六時の商店街
    ("money-drop1", at("指で数えておけば", "一円玉"), 1.26, 0.0, -24.0, 0.1),      # ③ 一円玉は、
]
assert sum(1 for e in EV if e[4] > -30) <= 3, "qua 3 tieng nhan"

nat = json.loads((VD / "native_19.json").read_text(encoding="utf-8"))
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
     "amix=inputs=%d:duration=first:normalize=0,alimiter=limit=0.79:level=disabled[a]" % (n + 1)
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                                                  "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(REN)]
subprocess.run(cmd, check=True)
print("OK", n, "lop am thanh ->", REN.name)
