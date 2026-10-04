# -*- coding: utf-8 -*-
"""mix_sound_22.py — lop AM THANH GOC cho video 22 (khuon mix_sound_21.py).

Tron vao ban SACH 22_kieta-shigoto_nosfx.mp4 -> 22_kieta-shigoto.mp4 (-c:v copy):
  ① tieng goc clip AI (ban goc Flow) + clip quay that — chi o native_22.json 'use' (mod 2-8Hz < 0,35)
  ② nen moi truong (効果音ラボ, khong can credit) -34 dBFS: chim se buoi sang o hook
  ③ <=3 diem nhan dung loi ke: xu じゃらじゃら (14) · 十円玉 vao 公衆電話 (85) · ngan keo cua ong (116)
  (踏切 カンカン: 効果音ラボ khong co ban thu -> de cam, CLAUDE.md §SFX)
Gain = MUC TIEU - mean DO DUOC cua file. Lan dau: doi ten ban render thanh _nosfx (chi 1 lan).
    python tools/probe_native_22.py && python tools/mix_sound_22.py
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:/Claude/Projects/youtube-jp-showa/06_VIDEO/22_kieta-shigoto")
REN, SRC, SFX = VD / "22_kieta-shigoto.mp4", VD / "22_kieta-shigoto_nosfx.mp4", VD / "sfx"
BED, AMB = -34.0, -34.0
# mean do bang volumedetect 2026-10-04
MEAN = {"sparrow-morning1": -34.1, "money1": -31.1, "publictelephone-money1": -31.9, "drawer-open1": -34.8}
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
    ("sparrow-morning1", 0.0, at("こんばんは。昭和くらし図鑑"), 0.0, BED, 1.5),                      # hook: sang som 昭和39, chim se
    ("money1", at("じゃらじゃらと鳴る", "じゃらじゃら"), 1.5, 0.0, -24.0, 0.1),                         # ① tui tien xu cua chau
    ("publictelephone-money1", at("十円玉を何枚も積み上げて"), 1.3, 0.0, -22.0, 0.05),              # ④ xu roi vao dien thoai cong cong
    ("drawer-open1", at("机の引き出しの鍵を開けました", "開け"), 0.6, 0.0, -22.0, 0.03),            # dinh: ong mo ngan keo
]
assert sum(1 for e in EV if e[4] > -30) <= 3, "qua 3 tieng nhan"

nat = json.loads((VD / "native_22.json").read_text(encoding="utf-8"))
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
