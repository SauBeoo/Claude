# -*- coding: utf-8 -*-
"""Mix SFX that (pocket-se.info) vao video 05 sau render — theo sfx_plan.md.
Moc THAT lay tu timeline.json (giong da synth) + vi tri clip tu SLIDES.json.
Khuon video 04 ban 6: -c:v copy · amix · alimiter · gain tinh -2.5dB · do peak/mean truoc-sau.
  python tools/mix_sfx_05.py            # mix -> 05_dagashiya-10en_sfx.mp4
  python tools/mix_sfx_05.py --dry      # chi in bang cue
"""
import io, sys, json, re, subprocess, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "05_dagashiya-10en"
SFX = VD / "sfx"
TL = json.load(open(VD / "timeline.json", encoding="utf-8"))["lines"]
SL = json.load(open(ROOT / "03_SCRIPTS" / "05_dagashiya-10en_SLIDES.json", encoding="utf-8"))
SRC = VD / "05_dagashiya-10en.mp4"
OUT = VD / "05_dagashiya-10en_sfx.mp4"

def t_of(phrase, nth=0):
    hits = [e for e in TL if phrase in e["text"]]
    if not hits:
        print(f"[CANH BAO] khong thay cau: {phrase}"); return None
    return hits[min(nth, len(hits) - 1)]["start"]

def slide_start(i):
    e = SL[i]; m = e["match"]
    line = next((x for x in TL if m in x["text"]), None)
    return None if line is None else line["start"] + float(e.get("offset", 0.0))

# --- diem nhan: (phrase, file, gain_dB, delay_s, repeat, gap_s) ---
CUES = [
    ("ガラスケースに、額をくっつけて", "garasto.mp3", 12, 0.0, 1, 0),
    ("カラン、カラン、カラン", "coinroll.mp3", 15, 0.3, 2, 1.5),
    ("手のひらの中には、十円玉が、十枚", "kozeni.mp3", 18, 0.2, 1, 0),
    ("レバー式の十円ゲーム機", "coingame.mp3", -5, 0.5, 1, 0),
    ("玉が穴に吸い込まれて", "coin2.mp3", 12, 0.8, 1, 0),
    ("ガコン、という音", "coin2.mp3", 12, 0.3, 1, 0),
    ("これも、違いました。残りは、七枚", "coin2.mp3", 12, 1.2, 1, 0),
    ("これで、五枚", "coin2.mp3", 12, 0.6, 1, 0),
    ("また、違いました。残るは、あと三枚", "coin2.mp3", 12, 1.2, 1, 0),
    ("店の外に出ると", "hikidopen.mp3", 10, 0.0, 1, 0),
    ("濡れた手のまま、店の中に戻ると", "hikidopen.mp3", 10, 0.3, 1, 0),
    ("数百円が、戻ってくる", "coinroll.mp3", 15, 0.5, 1, 0),
    ("気づけば、財布の中で、少しだけ増えていました", "coinroll.mp3", 15, 1.0, 1, 0),
    ("ガラスケースの前で、十円玉を、ぎゅっと握りしめていた", "five-melody.mp3", -7, 0.0, 1, 0),
]
# --- ambient duoi clip that: (ten clip chua chuoi, file, gain_dB) ---
AMBIENT = [
    ("jt_08", "sandougaya.mp3", -4), ("jt_09", "sandougaya.mp3", -4), ("jt_10", "sandougaya.mp3", -4),
    ("jt_11", "sandougaya.mp3", -4), ("jt_12", "sandougaya.mp3", -4), ("jt_13", "sandougaya.mp3", -4),
    ("jt_14", "sandougaya.mp3", -4), ("jt_15", "sandougaya.mp3", -4), ("jt_04", "sandougaya.mp3", -4),
    ("jt_03", "gaya.mp3", 7), ("jt_02", "gaya.mp3", 7), ("jt_07", "gaya.mp3", 7),
    ("jt_20", "gaya.mp3", 7), ("jt_06", "gaya.mp3", 7), ("jt_01", "gaya.mp3", 7),
    ("jt_22", "gaya.mp3", 7), ("jt_16", "maturibayasi2.mp3", -15),
]
# cua dong truoc cau chot cuoi
CLOSE = ("それでは、また、次のページで", "hikidoclose.mp3", 12, -1.0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry", action="store_true"); a = ap.parse_args()
    inst = []  # (file, start, gain, trim_dur or None, fade)
    for phrase, f, g, d, rep, gap in CUES:
        t = t_of(phrase)
        if t is None: continue
        for k in range(rep):
            inst.append((f, t + d + k * gap, g, None, 0.0))
    t = t_of(CLOSE[0])
    if t is not None: inst.append((CLOSE[1], max(0, t + CLOSE[3]), CLOSE[2], None, 0.0))
    for i, e in enumerate(SL):
        if not e.get("video"): continue
        name = e["source"]
        for key, f, g in AMBIENT:
            if key in name:
                st = slide_start(i); dur = float(e.get("dur", 6))
                if st is not None: inst.append((f, st, g, dur, 0.5))
    inst = sorted(set(inst), key=lambda x: x[1])  # dedupe (cua dong tung bi nhan doi)
    print(f"{len(inst)} instance SFX")
    for f, st, g, dur, fd in inst:
        print(f"  {st:7.2f}s  {f:18} {g:+d}dB" + (f"  dur={dur:.1f}s" if dur else ""))
    if a.dry: return
    inputs = ["-i", str(SRC)]; filt = []; labels = []
    for k, (f, st, g, dur, fd) in enumerate(inst):
        inputs += ["-i", str(SFX / f)]
        chain = f"[{k+1}:a]"
        if dur:  # ambient: loop du dai roi cat + fade
            chain += f"aloop=loop=-1:size=2e9,atrim=0:{dur:.2f},afade=t=in:d={fd},afade=t=out:st={max(0,dur-fd):.2f}:d={fd},"
        chain += f"volume={g}dB,adelay={int(st*1000)}|{int(st*1000)}[s{k}]"
        filt.append(chain); labels.append(f"[s{k}]")
    n = len(inst) + 1
    filt.append("[0:a]" + "".join(labels) + f"amix=inputs={n}:duration=first:normalize=0,alimiter=limit=0.97,volume=-1.0dB[aout]")
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt),
           "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUT)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print("FFMPEG LOI:", r.stderr[-800:]); sys.exit(1)
    for tag, p in (("GOC", SRC), ("SFX", OUT)):
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(p), "-af", "astats=measure_overall=Peak_level+RMS_level:measure_perchannel=none", "-f", "null", "-"], capture_output=True, text=True)
        pk = re.findall(r"Peak level dB: ([-\d.]+)", r.stderr); rms = re.findall(r"RMS level dB: ([-\d.]+)", r.stderr)
        print(f"  {tag}: peak {pk[-1] if pk else '?'} dB | RMS {rms[-1] if rms else '?'} dB")
    print("OK ->", OUT)

if __name__ == "__main__":
    main()
