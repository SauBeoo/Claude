# -*- coding: utf-8 -*-
"""probe_native_22.py — do TIENG GOC cua moi o video (clip AI + clip quay that) cho video 22.

Moi o: lay dung doan SE PHAT (khuc giua nhu make_cells_22, do dai = o) -> do
  mean dBFS · mod = nang luong bao 2-8 Hz / tong (nhip am tiet) — mod >= 0,35 => nghi TIENG NGUOI, LOAI
(render-background §2.8: day la phep DOAN -> dung file audition cho user nghe truoc khi chot).
Ghi 06_VIDEO/22_kieta-shigoto/native_22.json
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\22_kieta-shigoto")
plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
SR = 16000
# clip AI da lam sach (cells_in_ai) mat tieng -> tieng lay tu ban goc Flow = bang MAP cua ingest_ai_22 (mot nguon su that)
sys.path.insert(0, str(Path(__file__).parent))
import ingest_ai_22 as IG
FLOW = {k: v[1] for k, v in IG.MAP.items() if v[1]}


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
    src = IG.IN / FLOW[r["code"][3:]] if r["layer"] == "ai" else VD / r["src"]
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
(VD / "native_22.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nnhan %d / co tieng %d" % (sum(v["use"] for v in out.values()), len(out)))
