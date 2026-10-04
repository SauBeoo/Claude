# -*- coding: utf-8 -*-
"""Do tieng GOC cua 165 file NGUON lo moi (F:\...\Du_an_moi_25_mofw5vg1).

Vi sao phai do lai: _audio_cand.json cu do tren lo _flow_raw ngay 11/9 — lo do da BO,
user gen lai toan bo. Lay tieng theo file cu = tron nham tieng cua clip khong con trong video.

Hai so do (nhu ban cu):
  mean_dB : to nho. Rat nho = gan nhu cam, khong dang lay.
  mod_2_8 : nang luong bao dao dong 2-8 Hz / tong. TIENG NOI co nhip am tiet ~4 Hz => cao.
            Tieng nen (nuoc, gio, ve, banh xe) on dinh hon => thap.
⚠️ Day la PHEP DOAN de CHIA NHOM cho nguoi nghe, khong phai nhan dang tieng noi.
"""
import sys, json, subprocess, re
import numpy as np
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"F:\Youtube\Dự_án_mới_25_mofw5vg1")
OUT = Path(__file__).resolve().parent.parent / "06_VIDEO" / "12_natsu-atarimae" / "_audio_scan_new.json"
SR = 8000

try:
    import ctypes
    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetPriorityClass(ctypes.c_void_p(k.GetCurrentProcess()), 0x00004000)
except Exception:
    pass


def decode(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32) if r.returncode == 0 and r.stdout else None


def stats(x):
    if x is None or x.size < SR:
        return None
    rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-12)
    mean_db = 20 * np.log10(rms)
    hop = SR // 100
    n = x.size // hop
    if n < 32:
        return mean_db, 0.0
    env = np.sqrt(np.mean((x[:n * hop].reshape(n, hop).astype(np.float64)) ** 2, axis=1) + 1e-12)
    env = env - env.mean()
    if np.allclose(env, 0):
        return mean_db, 0.0
    sp = np.abs(np.fft.rfft(env)) ** 2
    fr = np.fft.rfftfreq(n, d=1.0 / 100)
    tot = sp[(fr > 0.3) & (fr < 30)].sum() + 1e-12
    return mean_db, float(sp[(fr >= 2) & (fr <= 8)].sum() / tot)


files = {}
for p in SRC.glob("task_*.mp4"):
    m = re.match(r"task_(\d+)", p.name)
    if m:
        files[int(m.group(1))] = p

out = []
for n in sorted(files):
    s = stats(decode(files[n]))
    slot = n - 1
    out.append({"slot": slot, "task": n, "name": files[n].name,
                "mean_db": round(s[0], 1) if s else None,
                "mod": round(s[1], 3) if s else None})
    if n % 30 == 0:
        print("  ... %d/%d" % (n, len(files)), flush=True)

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
ok = [o for o in out if o["mean_db"] is not None]
cam = [o for o in ok if o["mean_db"] < -50]
noi = [o for o in ok if o["mean_db"] >= -50 and o["mod"] >= 0.35]
nen = [o for o in ok if o["mean_db"] >= -50 and o["mod"] < 0.35]
print("\ndo duoc            : %d/%d" % (len(ok), len(files)))
print("gan nhu CAM (<-50) : %d" % len(cam))
print("nghi CO NGUOI NOI  : %d  -> LOAI" % len(noi))
print("nghi chi TIENG NEN : %d  -> dung duoc" % len(nen))
print("-> %s" % OUT)
