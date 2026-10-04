# -*- coding: utf-8 -*-
"""Do tieng GOC cua 165 clip Flow -> doan clip nao CO NGUOI NOI, clip nao chi la tieng nen.

Vi sao can: user muon "thinh thoang co tieng video goc" nhung CHI o clip khong co nguoi noi.
Tieng nguoi do Veo sinh ra thuong la tieng Nhat gia / lam nham => de len tren loi dan la hong.

Hai so do:
  mean_dB  : to nho (ffmpeg volumedetect). Rat nho = gan nhu cam, khong dang lay.
  mod_2_8  : nang luong bao dao dong o dai 2-8 Hz / tong nang luong bao.
             TIENG NOI co nhip am tiet ~4 Hz => mod cao.
             Tieng nen (gio, nuoc, ve, buoc chan deu) on dinh hon => mod thap.

⚠️ Day la PHEP DOAN, khong phai nhan dang tieng noi. Nguong duoi la de CHIA NHOM cho nguoi
   nghe kiem, khong phai de tu dong tron. Nghe roi moi chot.
"""
import sys, os, json, subprocess
import numpy as np
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
RAW = VD / "_flow_raw"
SR = 8000

try:
    import ctypes
    k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetPriorityClass(ctypes.c_void_p(k.GetCurrentProcess()), 0x00004000)
except Exception:
    pass


def decode(p):
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1",
         "-ar", str(SR), "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None
    return np.frombuffer(r.stdout, dtype=np.float32)


def stats(x):
    if x is None or x.size < SR:
        return None
    rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-12)
    mean_db = 20 * np.log10(rms)
    # bao (envelope) o 100 Hz
    hop = SR // 100
    n = x.size // hop
    env = np.sqrt(np.mean((x[:n * hop].reshape(n, hop).astype(np.float64)) ** 2, axis=1) + 1e-12)
    env = env - env.mean()
    if n < 32 or np.allclose(env, 0):
        return mean_db, 0.0
    sp = np.abs(np.fft.rfft(env)) ** 2
    fr = np.fft.rfftfreq(n, d=1.0 / 100)
    tot = sp[(fr > 0.3) & (fr < 30)].sum() + 1e-12
    mod = sp[(fr >= 2) & (fr <= 8)].sum() / tot
    return mean_db, float(mod)


files = sorted(RAW.glob("*.mp4"))
out = []
for i, p in enumerate(files):
    s = stats(decode(p))
    if s is None:
        out.append({"idx": i, "name": p.name, "mean_db": None, "mod": None})
        continue
    out.append({"idx": i, "name": p.name, "mean_db": round(s[0], 1), "mod": round(s[1], 3)})
    if (i + 1) % 30 == 0:
        print("  ... %d/%d" % (i + 1, len(files)), flush=True)

(VD / "_audio_scan.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
ok = [o for o in out if o["mean_db"] is not None]
cam = [o for o in ok if o["mean_db"] < -50]
noi = [o for o in ok if o["mean_db"] >= -50 and o["mod"] >= 0.35]
nen = [o for o in ok if o["mean_db"] >= -50 and o["mod"] < 0.35]
print("")
print("tong clip do duoc : %d / %d" % (len(ok), len(files)))
print("gan nhu CAM (<-50dB): %d  -> khong co gi de lay" % len(cam))
print("nghi CO NGUOI NOI   : %d  (mod 2-8Hz >= 0.35)" % len(noi))
print("nghi chi TIENG NEN  : %d" % len(nen))
print("")
print("-> %s" % (VD / "_audio_scan.json"))
