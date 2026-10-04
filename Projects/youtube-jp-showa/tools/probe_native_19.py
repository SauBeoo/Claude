# -*- coding: utf-8 -*-
"""probe_native_19.py — do TIENG GOC cua moi o video (clip AI + clip quay that) cho video 19.

Moi o: lay dung doan SE PHAT (khuc giua nhu make_cells_19, do dai = o) -> do
  mean dBFS · mod = nang luong bao 2-8 Hz / tong (nhip am tiet) — mod >= 0,35 => nghi TIENG NGUOI, LOAI
(render-background §2.8: day la phep DOAN -> dung file audition cho user nghe truoc khi chot).
Ghi 06_VIDEO/19_kaimono-joushiki/native_19.json
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\19_kaimono-joushiki")
plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
SR = 16000
# clip AI da lam sach (cells_in_ai) mat tieng -> tieng lay tu ban goc Flow (bang REVIEW_AI_19.md)
FLOW = {"denkiya_bow": "C_People_exchanging_bows_and_gestures.mp4",
        "kids_tv": "A_Children_laughing_in_tatami_room_20260925200453.mp4",
        "hands_shichifuda": "A_Mother_receiving_ticket_at_pawnshop_20260925200453.mp4",
        "mother_cosme_window": "A_Mother_leans_near_window_street_20260925200453.mp4",
        "lipstick_hand": "A_People_gesturing_in_shop_20260925200453.mp4",
        "yaoya_103yen": "A_Daughter_turning_toward_mother_20260925200453.mp4",
        "mother_two_piles": "A_Mother_sliding_booklet_towards_h__20260925200453.mp4",
        "daughter_bride": "B_Daughter_turning_toward_mother_20260925200859.mp4",
        "mother_smile": "B_Woman_smiling_and_looking_away_20260925200858.mp4"}


def dur_of(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def has_audio(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return bool(r.stdout.strip())


out = {}
for r in plan:
    if r["layer"] not in ("video", "ai"):
        continue
    src = VD / "_src_flow" / FLOW[r["code"][3:]] if r["layer"] == "ai" else VD / r["src"]
    if not has_audio(src):
        print("clip_%02d  %-26s  (khong co tieng)" % (r["idx"], r["code"])); continue
    d = dur_of(src); need = r["dur"] + 0.5
    ss = 0.0 if r["layer"] == "ai" else (max(0.0, (d - need) / 2) if d > need + 1 else 0.0)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % ss, "-t", "%.2f" % r["dur"], "-i", str(src),
                          "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if len(x) < SR:
        continue
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    mean_db = 20 * np.log10(rms)
    env = np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, mode="same"))[::160]      # bao 100 Hz
    env = env - env.mean()
    spec = np.abs(np.fft.rfft(env)) ** 2; f = np.fft.rfftfreq(len(env), 1 / 100)
    mod = float(spec[(f >= 2) & (f <= 8)].sum() / (spec[(f > 0.5) & (f < 50)].sum() + 1e-12))
    ok = mean_db > -60 and mod < 0.35
    out[str(r["idx"])] = {"code": r["code"], "t": r["t"], "dur": r["dur"], "ss": round(ss, 2),
                          "src": str(src.relative_to(VD)), "mean": round(float(mean_db), 1), "mod": round(mod, 2), "use": bool(ok)}
    print("clip_%02d  %-26s  mean %6.1f dB  mod %.2f  %s" % (r["idx"], r["code"], mean_db, mod,
                                                          "NHAN" if ok else ("LOAI tieng nguoi?" if mod >= 0.35 else "LOAI qua nho")))
(VD / "native_19.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nnhan %d / co tieng %d" % (sum(v["use"] for v in out.values()), len(out)))
