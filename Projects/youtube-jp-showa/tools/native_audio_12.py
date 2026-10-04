# -*- coding: utf-8 -*-
"""Tron TIENG GOC cua vai clip vao ban da render, o muc NEN.

Vi sao chi vai doan: tieng nguoi do Veo sinh ra la tieng Nhat GIA, de len loi dan la hong.
Chi lay doan co nguon am that ro (gau gieng, xe da, voi nuoc, te nuoc, phao bong) va CHI
nhung clip do duoc la "tieng nen" (mod 2-8 Hz thap) tren chinh DOAN SE PHAT, khong phai
tren ca clip 8 giay — vi doan khong phat khong lien quan.

Muc: mean -34 dBFS (duoi loi dan). Gain = target - mean do duoc cua chinh doan do.
alimiter chan dinh. Xuat: -c:v copy (khong dung lai video).

    python tools/native_audio_12.py           -> chi DO va in bang, khong ghi gi
    python tools/native_audio_12.py --apply   -> tron that
"""
import sys, json, subprocess, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "12_natsu-atarimae"
SRC = Path(r"F:\Youtube\Dự_án_mới_25_mofw5vg1")
MP4 = VD / "12_natsu-atarimae.mp4"
OUT = VD / "12_natsu-atarimae_amb.mp4"
TARGET = -34.0          # dBFS mean — muc nen, duoi loi dan
FADE = 0.6              # giay, vao/ra cho khoi "bat dien"
MOD_MAX = 0.35          # tren nguong nay = nghi co tieng nguoi -> loai

# slot -> mo ta. Clip nguon = task_{slot+1}. Doan phat = [offset, offset+dur) cua clip do.
PICKS = [
    # 30 GIAY DAU (user yeu cau 2026-09-12): slot 0 la ngo dem dong nguoi nhung mod=0.513
    #   -> gan nhu chac co tieng noi, LOAI. Slot 2 do -44 dB, keo len -34 la keo ca nhieu nen.
    #   Con lai slot 1 va slot 4 la hai cho vua som vua sach.
    (1,   "trong man, sang som — tieng phong + vo canh"),
    (4,   "ngo som, ngoai nha"),
    (44,  "tha gau xuong gieng — tieng rong reo + go go"),
    (56,  "xe da keo tren duong soi"),
    (90,  "voi nuoc san truong chay"),
    (102, "te nuoc ra dat kho (uchimizu)"),
    (113, "do not thung nuoc"),
    (134, "phao bong dem"),
]
# slot 72 duoc nap voi -ss 0.6 (cat khung trong dau clip); cac slot khac offset 0
SS = {72: 0.6}


def src_of(slot):
    g = list(SRC.glob("task_%03d*.mp4" % (slot + 1)))
    if not g:
        return None
    return sorted(g, key=lambda p: (0 if "720p" in p.name else 1))[0]


def mean_db(p, ss, dur):
    # ⚠️ volumedetect in ket qua o muc INFO — de "-v error" thi khong co gi de doc,
    #   ham tra None va ca 6 doan bao "KHONG DO DUOC" (dinh 2026-09-12).
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", "%.3f" % ss,
                        "-t", "%.3f" % dur, "-i", str(p), "-af", "volumedetect",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None


def mod_2_8(p, ss, dur):
    """Nhip am tiet ~4 Hz -> tieng noi. Do tren DUNG doan se phat."""
    import numpy as np
    sr = 8000
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % ss, "-t", "%.3f" % dur,
                        "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                       capture_output=True)
    x = np.frombuffer(r.stdout, dtype=np.float32)
    if x.size < sr:
        return None
    hop = sr // 100
    n = x.size // hop
    if n < 32:
        return None
    env = np.sqrt(np.mean((x[:n * hop].reshape(n, hop).astype(np.float64)) ** 2, axis=1) + 1e-12)
    env -= env.mean()
    sp = np.abs(np.fft.rfft(env)) ** 2
    fr = np.fft.rfftfreq(n, d=1.0 / 100)
    tot = sp[(fr > 0.3) & (fr < 30)].sum() + 1e-12
    return float(sp[(fr >= 2) & (fr <= 8)].sum() / tot)


cue = json.loads((VD / "_cue.json").read_text(encoding="utf-8"))
rows = []
print("%-5s %-7s %-6s %-8s %-7s %-6s %s" % ("slot", "t", "dur", "mean_dB", "mod2-8", "gain", "mo ta"))
for slot, desc in PICKS:
    p = src_of(slot)
    if p is None:
        print("%-5d THIEU FILE NGUON" % slot)
        continue
    ss = SS.get(slot, 0.0)
    dur = cue[slot]["dur"]
    md = mean_db(p, ss, dur)
    mo = mod_2_8(p, ss, dur)
    if md is None or mo is None:
        print("%-5d KHONG DO DUOC" % slot)
        continue
    gain = TARGET - md
    ok = mo < MOD_MAX
    print("%-5d %-7.1f %-6.2f %-8.1f %-7.3f %-6.1f %s%s"
          % (slot, cue[slot]["t"], dur, md, mo, gain, desc, "" if ok else "   ⛔ NGHI TIENG NGUOI -> LOAI"))
    if ok:
        rows.append({"slot": slot, "src": str(p), "ss": ss, "t": cue[slot]["t"],
                     "dur": dur, "gain": gain, "desc": desc})

print("\nlay %d/%d doan" % (len(rows), len(PICKS)))
(VD / "_native_pick.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
if "--apply" not in sys.argv:
    print("(chay lai voi --apply de tron that)")
    sys.exit(0)
if not rows:
    print("khong co doan nao dat — khong tron")
    sys.exit(1)

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(MP4)]
for r in rows:
    cmd += ["-ss", "%.3f" % r["ss"], "-t", "%.3f" % r["dur"], "-i", r["src"]]
parts, labels = [], []
for i, r in enumerate(rows, start=1):
    lab = "n%d" % i
    parts.append("[%d:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
                 "volume=%.2fdB,afade=t=in:st=0:d=%.2f,afade=t=out:st=%.3f:d=%.2f,"
                 "adelay=%d|%d[%s]"
                 % (i, r["gain"], FADE, max(r["dur"] - FADE, 0.1), FADE,
                    int(r["t"] * 1000), int(r["t"] * 1000), lab))
    labels.append("[%s]" % lab)
parts.append("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono[base]")
# normalize=0 : amix mac dinh CHIA cho so input -> loi dan bi tut 7 dB. Phai tat.
parts.append("[base]%samix=inputs=%d:normalize=0:duration=first:dropout_transition=0,"
             # limit=0.891 ~ -1.0 dBTP: de nguyen mac dinh thi dinh len -0.1 dBFS, sat tran.
             "alimiter=limit=0.891:level=disabled[a]" % ("".join(labels), len(rows) + 1))
cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUT)]
print("\ndang tron…")
r = subprocess.run(cmd)
print("xong" if r.returncode == 0 else "LOI ffmpeg")
sys.exit(r.returncode)
