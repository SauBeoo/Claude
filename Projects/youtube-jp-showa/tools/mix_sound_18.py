# -*- coding: utf-8 -*-
"""mix_sound_18.py — lop AM THANH GOC cho video 18 (user 2026-09-24: "khong co may am thanh goc do").

Tron vao ban SACH 18_hataraku-okane_nosfx.mp4 -> 18_hataraku-okane.mp4 (-c:v copy):
  ① tieng goc 7 clip AI (cells_in/NN.mp4) — da do: khong co tieng nguoi (mod 2-8Hz 0,18-0,30 < 0,35)
  ② nen moi truong (効果音ラボ, khong can credit) o canh co khong khi rieng — muc -34 dBFS
  ③ 3 diem nhan dung loi ke — muc -20…-28
Gain = MUC TIEU - mean DO DUOC cua file (render-background §2.8 / feedback_sfx_gain_tinh_tu_so_do).
Chay lai bao nhieu lan cung duoc: luon doc ban _nosfx.
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\18_hataraku-okane")
SRC, OUT, SFX = VD / "18_hataraku-okane_nosfx.mp4", VD / "18_hataraku-okane.mp4", VD / "sfx"
BED, AMB = -34.0, -34.0

MEAN = {"train-bell1": -22.7, "train-start1": -22.6, "train-driving1": -28.2, "wind1": -28.7, "wind2": -23.4,
        "wind3": -24.8, "station-square1": -24.7, "industrialzone1": -23.1, "slidingdoor-open1": -23.8}
# (file, bat dau trong video, dai, offset trong file, muc tieu dB, fade)
EV = [
    ("wind1", 84.4, 5.8, 3.0, BED, 0.6),             # 荷台の上は、風が冷たい
    ("station-square1", 224.4, 7.0, 10.0, BED, 0.6),  # 駅のホーム
    ("train-bell1", 231.6, 2.58, 0.0, -22.0, 0.1),    # ③ 発車のベルが鳴ると
    ("train-driving1", 240.2, 9.2, 5.0, BED, 0.8),    # 列車は、夜通し走ります
    ("industrialzone1", 338.5, 7.0, 0.0, -36.0, 0.6), # 寮 -> 工場
    ("industrialzone1", 352.6, 5.8, 7.5, -36.0, 0.6), # 切れた糸を…
    ("industrialzone1", 514.9, 8.3, 4.0, -36.0, 0.6), # 旋盤
    ("train-start1", 635.5, 4.5, 2.0, -28.0, 0.8),    # ③ 夜行で上野へ
    ("wind2", 638.6, 6.5, 12.0, BED, 0.8),            # 雪
    ("wind3", 659.2, 7.6, 2.0, BED, 0.8),             # 屋根の雪下ろし
    ("wind3", 681.3, 5.0, 10.0, BED, 0.8),            # 田んぼは、雪の下
    ("slidingdoor-open1", 749.8, 1.3, 0.0, -20.0, 0.05),  # ③ 玄関の戸が開く音
]
PLAN = {r["idx"]: r for r in json.loads((VD / "clips/_PLAN.json").read_text(encoding="utf-8"))}
NATIVE_MEAN = {18: -46.8, 31: -45.4, 43: -40.5, 66: -49.3, 71: -41.7, 84: -47.3, 85: -52.2}

inputs, chains = ["-i", str(SRC)], []
k = 1
def add(path, ss, t0, dur, gain, fade):
    global k
    inputs.extend(["-ss", "%.2f" % ss, "-t", "%.2f" % dur, "-i", str(path)])
    fo = max(0.0, dur - fade)
    chains.append("[%d:a]aresample=48000,aformat=channel_layouts=mono,volume=%.1fdB,afade=t=in:d=%.2f,"
                  "afade=t=out:st=%.2f:d=%.2f,adelay=%d:all=1[s%d]" % (k, gain, fade, fo, fade, int(t0 * 1000), k))
    k += 1
for f, t0, dur, off, tgt, fade in EV:
    add(SFX / (f + ".mp3"), off, t0, dur, tgt - MEAN[f], fade)
for i, m in NATIVE_MEAN.items():
    r = PLAN[i]
    add(VD / "cells_in" / ("%02d.mp4" % i), 0.0, r["t"], r["dur"], min(AMB - m, 18.0), 0.6)
n = k - 1
fc = ";".join(chains) + ";[0:a]aresample=48000[v];[v]" + "".join("[s%d]" % j for j in range(1, n + 1)) + \
     "amix=inputs=%d:duration=first:normalize=0,alimiter=limit=0.84:level=disabled[a]" % (n + 1)
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                                                  "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUT)]
assert SRC.exists(), "thieu ban sach _nosfx"
subprocess.run(cmd, check=True)
print("OK", n, "lop am thanh ->", OUT.name)
