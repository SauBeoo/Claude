# -*- coding: utf-8 -*-
"""make_17v3.py — lap clips cho video 17 ban REAL-FIRST (sau build_slides_v3 + plan_17v3).

Doc clips/_PLAN.json + _ASSIGN_17v3.json:
  film PD   -> 06_VIDEO/17_kaisha-ga-kureta/film_spec.json (cho cut_archival.py --record)
  film stock-> cat thang bang ffmpeg (Pexels, 1920x1080, 24fps, keo cham neu nguon ngan)
  photo     -> cells_in/NN.jpg (anh that)                        -> make_cells_v3 --wm 0
  aistill   -> cells_in/NN.png = frame 1,0s cua clip AI cu cung dong (clips_v17ai, DA sach ✦ + vien)
  ai        -> cells_in/NN.mp4 = clip AI cu cung dong / PICK_FINAL (canh thoi nay)
Chay:  python tools/make_17v3.py [--dry]
Sau do: cut_archival.py --spec <VD>/film_spec.json --outdir <VD>/clips --record 17_kaisha-ga-kureta
        make_cells_v3.py 17_kaisha-ga-kureta --wm 0 --jobs 2
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "17_kaisha-ga-kureta"
FP = ROOT / "06_VIDEO" / "_footage_pd"
CL, IN, OLD = VD / "clips", VD / "cells_in", VD / "clips_v17ai"
FINAL = VD / "clips_real_ima_ie" / "PICK_FINAL"
dry = "--dry" in sys.argv
plan = json.loads((CL / "_PLAN.json").read_text(encoding="utf-8"))
TL = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
STARTS = [x["start"] for x in TL]
def owner(t):
    # ⚠️ _PLAN.json lam tron t0 ve 0,01s -> o bat dau 62,03 ma dong bat dau 62,034 bi gan cho dong TRUOC
    return max(k for k, s0 in enumerate(STARTS) if s0 <= t + 0.02)
assign = {int(k): v for k, v in json.loads((VD / "_ASSIGN_17v3.json").read_text(encoding="utf-8")).items()}
# grade chung cho nguon KHONG co PRE rieng trong cut_archival (NARA 1950s toi: do 26-50/255 -> can nang)
GRADE = {"japan_today_1959.mp4": 0.7, "you_in_japan_512kb.mp4": 0.5, "we_the_japanese_512kb.mp4": 0.5,
         "steel_1960.mp4": 0.5, "japan_1960_nsc.mp4": 0.5,
         "color_story_japan_1957_r1_sq.mp4": 0.6, "color_story_japan_1957_r2_sq.mp4": 0.6}

# clip AI cu theo dong: _MAP.txt cu (idx  t0  dur  khoi  L<dong>  loi)
OLDS = []   # (idx, t0, t1) — chon clip cu PHU THOI DIEM o moi (nhan L<dong> cua _MAP cu cung lech do lam tron)
for ln in (OLD / "_MAP.txt").read_text(encoding="utf-8").splitlines()[1:]:
    m = re.match(r"\s*(\d+)\s+([\d.]+)s\s+([\d.]+)s", ln)
    if m:
        OLDS.append((int(m.group(1)), float(m.group(2)), float(m.group(2)) + float(m.group(3))))
def old_at(t0, t1):
    best = max(OLDS, key=lambda o: min(t1, o[2]) - max(t0, o[1]))
    return best[0]


def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


IN.mkdir(exist_ok=True)
for f in list(IN.glob("*")):
    if not dry: f.unlink()
cuts, log, kth = [], [], {}
for r in plan:
    i, lay = r["idx"], r["layer"]; li = owner(r["t"])
    k = kth.get(li, 0); kth[li] = k + 1
    a = assign[li]
    if lay == "film":
        src = r["src"]
        if src.startswith("stock/"):
            s = VD / src; need = r["dur"] + 0.6; d = probe_dur(s); ss = float(r["ss"])
            if ss + need > d:
                ss = max(0.0, d - need)
            fac = max(1.0, need / max(0.1, d - ss))
            vf = ("setpts=%.4f*PTS," % fac if fac > 1.001 else "") + \
                 "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=24"
            if not dry:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % ss, "-i", str(s), "-t", "%.2f" % need,
                                "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                                "-pix_fmt", "yuv420p", str(CL / ("clip_%02d.mp4" % i))], check=True)
            log.append((i, "stock", src, round(ss, 1), "x%.2f" % fac if fac > 1.001 else ""))
        else:
            cuts.append({"id": "clip_%02d" % i, "src": str(FP / src), "ss": r["ss"], "dur": round(r["dur"] + 0.6, 2),
                         "ybias": 0.45, "grade": GRADE.get(src, 0), "note": "o%d L%d %s" % (i, li, r["text"][:20])})
            log.append((i, "film", src, r["ss"], ""))
    elif lay == "photo":
        p = VD / a[1]
        if not dry: shutil.copy(p, IN / ("%02d%s" % (i, p.suffix)))
        log.append((i, "photo", a[1], "", ""))
    else:
        if a[0] == "I":
            src = FINAL / ("clip_%02d.mp4" % a[1]); tag = "ima %d" % a[1]
        else:
            o = old_at(r["t"], r["t"] + r["dur"])
            src = OLD / ("clip_%02d.mp4" % o); tag = "old %d" % o
        if lay == "ai":
            if not dry: shutil.copy(src, IN / ("%02d.mp4" % i))
        else:   # aistill: frame giua clip (khung on dinh nhat)
            t = min(2.0, probe_dur(src) * 0.35)
            if not dry:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % t, "-i", str(src), "-frames:v", "1",
                                str(IN / ("%02d.png" % i))], check=True)
        log.append((i, lay, tag, "", ""))

(VD / "film_spec.json").write_text(json.dumps({"_note": "sinh boi make_17v3.py", "cuts": cuts}, ensure_ascii=False,
                                              indent=1), encoding="utf-8")
from collections import Counter
print("o:", dict(Counter(x[1] for x in log)), "| film PD cut:", len(cuts))
(CL / "_MAKE_17v3.log").write_text("\n".join("\t".join(map(str, x)) for x in log), encoding="utf-8")
