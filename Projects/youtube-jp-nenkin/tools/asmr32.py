# -*- coding: utf-8 -*-
r"""asmr32.py — lớp tiếng ASMR "bàn làm việc" + tầng âm thanh cuối cho video 32 (chép asmr31).

user 2026-09-27: *"Thêm các tiếng asmr vào cho nó thỏa mãn người nghe"*.
⚠️ Đè `audience-45plus.md` §2 gate 4 (SFX ≤1 chùm/5 phút) theo lệnh user — nghe demo xong
mới áp cả bài, kết quả phải ghi lại vào luật.

TIẾNG NEO VÀO CHÍNH MỐC HÌNH (cùng hàm `build28.sync_times` mà telop dùng — không có hai bộ mốc):
  ① dòng chữ chính vào      → bút chì viết カキカキ (lát 0,45s, mỗi lần một đoạn khác của file)
  ② thẻ phụ vào             → đặt thẻ ピッ
  ③ vòng khoanh đỏ vẽ dần   → bút lông khoanh (0,5s từ cung đầu)
  ④ đổi ô (dissolve)        → lật trang / mở giấy, xen kẽ
  ⑤ vật trong ẢNH của ô     → xu rơi · đóng dấu · bỏ thư · đặt chén · ngăn kéo · báo — chỉ khi
                               vật ĐỔI so với ô trước (không gõ lặp một tiếng qua nhiều ô liền)
Nguồn: 効果音ラボ (soundeffect-lab.info) — free thương mại, KHÔNG cần credit. File ở assets/sfx_lab/.
Gain = MỨC ĐÍCH − mean ĐO ĐƯỢC của file (memory feedback_sfx_gain_tinh_tu_so_do); mức đích tính
TƯƠNG ĐỐI với giọng (mean giọng thô −23,0 dB).

TẦNG ÂM CUỐI (thay `loudnorm` 1 lượt của build28 — đo được: ra −18 LUFS vì giọng thô có
đỉnh cao hơn trung bình 19,5 dB, không thể lên −14 mà giữ đỉnh ≤−4 nếu không nén):
  giọng + SFX → xoay pha (2 × 4 allpass 120/240/480/960 Hz) → gain → limiter trần 0,60
  → LẶP gain tới khi ebur128 trên FILE ĐÃ XUẤT (AAC) cho I −14 ±0,3 và true peak ≤ −3 dBTP.
  Đo 2026-09-27 trên 100s demo — vì sao chuỗi này:
    · giọng VOICEVOX thô −23,2 LUFS / đỉnh −3,7 (PLR 19,5): 3,2% khung vượt −8 dBFS, 13,9% vượt −10
      ⇒ đỉnh nằm ở DẠNG SÓNG, không phải đường bao ⇒ acompressor (rms lẫn peak, 4 mức) KHÔNG giúp gì:
      mọi mức kẹt ở −15 LUFS / TP −2,4. ⇒ ⛔ đừng thêm compressor vào lại.
    · allpass hạ crest KHÔNG làm méo (không bỏ âm nào): PLR 19,5 → 18,3.
    · trần 0,56 → −14,6 / −3,8 · **0,60 → −14,2 / −3,1** · 0,63 → −13,8 / −2,8 (lọt trần).
  ⚠️ memory project_loudness_14_lufs ghi alimiter "hại" — ca đó gắn limiter SAU loudnorm rồi
  KHÔNG bù gain. Ở đây gain lặp theo số đo file xuất. Limiter ép ~5 dB đỉnh ⇒ NGHE demo trước.

CHẠY:  python tools/asmr32.py                 → cả bài: _build/_v.mp4 → <stem>.mp4 (bản cũ giữ _nosfx)
       python tools/asmr32.py --demo 10       → 10 ô đầu: _build_demo/_v.mp4 → demo32_asmr.mp4
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import build32  # noqa: E402,F401
import build28 as b  # noqa: E402

SR = 48000
LAB = PROJ / "assets" / "sfx_lab"
VOICE_MEAN = -23.0
# file: (mean đo được dB, mức đích TƯƠNG ĐỐI giọng dB, lát dài s hoặc None = cả file)
SFX = {
    "mechanical-pencil-write1": (-30.9, -16, 0.45),
    "card-put1": (-32.4, -15, None),
    "magic-cap-write1": (-30.6, -16, 0.50),
    "page1": (-30.9, -17, None),
    "paper-take1": (-31.9, -17, None),
    "money-drop1": (-33.9, -12, None),
    "peta1": (-29.7, -12, None),
    "post1": (-25.0, -13, None),
    "cup-put1": (-30.5, -12, None),
    "drawer-open1": (-34.8, -12, None),
    "newspaper-turn-over1": (-35.2, -13, None),
}
# vật trong ảnh (từ SUBJECT prompt) → tiếng; thứ tự = ưu tiên
SCENE = [("coin", "money-drop1"), ("seal", "peta1"), ("stamp", "peta1"),
         ("postbox", "post1"), ("mailbox", "post1"), ("posting", "post1"),
         ("teacup", "cup-put1"), ("tea ", "cup-put1"), ("drawer", "drawer-open1"),
         ("newspaper", "newspaper-turn-over1")]
FADE_OUT = 0.08
LIMITS = (0.60, 0.56)  # trần limiter — thử 0,60 trước (đo: −14,2 / −3,1)


def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(LAB / f"{name}.mp3"), "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def scene_of(k, flow_subj, shot2flow):
    d = shot2flow.get(k)
    if d is None:
        return None
    s = flow_subj[d - 1].lower()
    for kw, snd in SCENE:
        if kw in s:
            return snd
    return None


def events(n_shots=None):
    plan = json.loads((b.VD / b.PLAN_NAME).read_text(encoding="utf-8"))
    tl = json.loads((b.VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    shots = plan["shots"][:n_shots] if n_shots else plan["shots"]
    flow = [l.rstrip("\n") for l in open(b.VD / "img32_FLOW.txt", encoding="utf-8")]
    subj = [l.split("SUBJECT:", 1)[1] if "SUBJECT:" in l else "" for l in flow]
    shot2flow = {}
    for l in open(b.VD / "img32_TENFILE.txt", encoding="utf-8"):
        m = re.match(r"dong (\d+) -> shot_(\d+)\.png", l)
        if m:
            shot2flow[int(m.group(2))] = int(m.group(1))
    ev, prev_scene, pencil_i, marker_i = [], None, 0, 0
    allshots = plan["shots"]
    for k, s in enumerate(shots):
        nxt = allshots[k + 1]["t0"] if k + 1 < len(allshots) else s["t1"]
        dur = nxt - s["t0"]
        sh = dict(b.TELOP[k]); sh.setdefault("sub", [])
        live = [i for i, ln in enumerate(tl) if ln["start"] < nxt - 1e-3 and ln["end"] > s["t0"] + 1e-3]
        tb, ts, _rows = b.sync_times(sh, live, tl, s["t0"], dur)
        T0 = s["t0"]
        if k:
            ev.append((T0, "page1" if k % 2 else "paper-take1", 0.0, "đổi ô"))
        for i, (line, t) in enumerate(zip(sh["big"], tb)):
            ev.append((T0 + t, "mechanical-pencil-write1", (pencil_i * 1.37) % 6.6, f"chữ: {line}"))
            pencil_i += 1
            want = (sh.get("circle") and any(c.isdigit() for c in line)) or sh.get("circle_line") == i
            if want:
                ev.append((T0 + t + 0.30, "magic-cap-write1", (marker_i * 2.11) % 9.3, f"khoanh: {line}"))
                marker_i += 1
        for sub, t in zip(sh["sub"], ts):
            ev.append((T0 + t, "card-put1", 0.0, f"thẻ: {sub}"))
        sc = scene_of(k, subj, shot2flow)
        if sc and sc != prev_scene:
            ev.append((T0 + 0.9, sc, 0.0, "vật trong ảnh"))
        prev_scene = sc
    t_end = shots[-1]["t1"]
    return sorted(ev), t_end


def render_sfx(ev, t_end):
    buf = np.zeros(int((t_end + 2) * SR), np.float32)
    cache = {}
    for t, name, off, _why in ev:
        if name not in cache:
            cache[name] = load(name)
        mean, rel, sl = SFX[name]
        x = cache[name]
        a = int(off * SR)
        x = x[a:a + int(sl * SR)] if sl else x[a:]
        x = x.copy()
        nf = int(FADE_OUT * SR)
        if len(x) > nf:
            x[-nf:] *= np.linspace(1, 0, nf)
        x *= 10 ** ((VOICE_MEAN + rel - mean) / 20)
        p = int(t * SR)
        buf[p:p + len(x)] += x[:max(0, len(buf) - p)]
    return buf


def ebur(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace").stderr
    tail = r[r.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    pk = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1))
    return i, pk


def main():
    demo = "--demo" in sys.argv
    n = int(sys.argv[sys.argv.index("--demo") + 1]) if demo else None
    bdir = b.VD / ("_build_demo" if demo else "_build")
    vid = bdir / "_v.mp4"
    out = b.VD / ("demo32_asmr.mp4" if demo else f"{b.STEM}.mp4")
    if not vid.exists():
        print(f"🔴 thiếu {vid} — dựng hình trước"); return 1
    ev, t_end = events(n)
    mins = t_end / 60
    kinds = {}
    for _t, name, _o, _w in ev:
        kinds[name] = kinds.get(name, 0) + 1
    print(f"sự kiện ASMR: {len(ev)} · {len(ev) / mins:.1f}/phút · " +
          " · ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])))
    (bdir / "asmr_events.txt").write_text("\n".join(f"{t:8.2f}  {nm:<24s} {w}" for t, nm, _o, w in ev),
                                          encoding="utf-8")
    sfx = render_sfx(ev, t_end)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(b.VD / "voice_full.wav"), "-t",
                          f"{t_end:.3f}", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    voice = np.frombuffer(raw, np.float32)
    mix = sfx[:len(voice)].copy()
    mix[:len(voice)] += voice
    mixw = bdir / "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    str(mixw)], input=mix.astype(np.float32).tobytes(), check=True)
    tmp = bdir / "_final_try.mp4"
    ap = ",".join(f"allpass=f={f}:width_type=q:w=0.707" for f in (120, 240, 480, 960))
    for lim in LIMITS:
        g, ok = 14.0, False
        for _it in range(8):  # limiter ăn bớt I ⇒ đo lại FILE XUẤT rồi bù
            af = f"{ap},{ap},volume={g:.2f}dB,alimiter=limit={lim}:attack=0.5:release=50:level=disabled"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(mixw), "-map", "0:v",
                            "-map", "1:a", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k",
                            "-ar", "48000", "-t", f"{t_end:.3f}", str(tmp)], check=True)
            I, P = ebur(tmp)
            if abs(I + 14) <= 0.3:
                ok = P <= -3.0
                break
            g += -14.0 - I
        print(f"  trần {lim} · gain {g:+.1f} dB  →  I {I:.1f} LUFS · peak {P:.1f} dBFS  {'✅' if ok else '—'}")
        if ok:
            break
    else:
        print("🔴 không trần nào đạt −14 LUFS ±0,3 + peak ≤−3 — KHÔNG ghi đè bản render")
        return 1
    if not demo and out.exists():
        keep = b.VD / f"{b.STEM}_nosfx.mp4"
        if not keep.exists():
            shutil.copy(out, keep)
    shutil.move(str(tmp), str(out))
    print(f"→ {out}  (trần {lim}, gain {g:+.1f} dB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
