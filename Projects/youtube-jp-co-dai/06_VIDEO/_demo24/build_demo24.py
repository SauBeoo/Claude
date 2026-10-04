# -*- coding: utf-8 -*-
r"""Dung DEMO cho video 24 (pipeline muc 7.3) — NHIEU CUA SO, moi cua so 1 file.

Vi sao co file nay: soi frame tinh KHONG bat duoc 2 loi da dinh that o #21 —
avatar vao muon 12 giay, va hai khung inset lap nhau. Ca hai chi hien khi
build-on dang chay + voice that + phu de that.

🔴 VI SAO PHAI CO NHIEU CUA SO (them 2026-08-26): sau khi callout24.py bo het
vong khoanh va thay bang stamp/tag, ban demo cu (chi 0-95s) KHONG con phu du
cac kieu callout — trong 95s dau chi co stamp ngan va 1 tag ngan. Tag DAI
(「薄い匂い＝集合」) va stamp 5 ky (「虫の休憩所」) nam o phut 11-12. Demo mot
cua so = duyet mot phan ba so kieu, roi phat hien loi o ban day du.

Chay:
    python 06_VIDEO\_demo24\build_demo24.py                    # 2 cua so mac dinh
    python 06_VIDEO\_demo24\build_demo24.py --win 660,765      # chi 1 cua so
(hoac qua run_demo24.cmd de co log + EXITCODE theo render-background.md)
"""
import argparse, io, json, re, shutil, subprocess, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
ML = Path(r"E:\Claude\Projects\_media_library")
SLUG = "24_kamemushi-3mm-sukima"
VD = PROJ / "06_VIDEO" / SLUG
OUT = PROJ / "06_VIDEO" / "_demo24"
CLIPS = OUT / "clips"
SLIDES = PROJ / "03_SCRIPTS" / f"{SLUG}_SLIDES.json"

# cua so mac dinh — moi cua so phu mot NHOM callout khac nhau:
#   A 0-95s     : tag ngan 「開ける」 · inset e3 + stamp 「3秒」 · stamp 「2匹」 · avatar
#   B 655-765s  : stamp 5 ky 「虫の休憩所」 · stamp 「日暮れ前」 (khung vua bo inset)
#                 · tag DAI 「薄い匂い＝集合」 · the vox giua doan
WINDOWS = [(0.0, 95.0), (655.0, 765.0)]


def run(cmd):
    print(">", " ".join(str(x) for x in cmd))
    r = subprocess.run([str(x) for x in cmd], cwd=str(PROJ))
    if r.returncode:
        raise SystemExit(f"[LOI] exit {r.returncode}: {cmd[1]}")


def srt_window(src: Path, dst: Path, t0: float, t1: float):
    """Cat srt ve [t0,t1) va DICH moc ve 0. Khong dung -itsoffset (khong dich srt)."""
    def to_s(s):
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

    def to_ts(v):
        v = max(v, 0.0)
        h = int(v // 3600); m = int(v % 3600 // 60); s = int(v % 60)
        return f"{h:02d}:{m:02d}:{s:02d},{round((v - int(v)) * 1000):03d}"

    blocks = re.split(r"\n\s*\n", src.read_text(encoding="utf-8").strip())
    keep, n = [], 0
    for b in blocks:
        L = b.splitlines()
        if len(L) < 3 or "-->" not in L[1]:
            continue
        a, z = [to_s(x.strip()) for x in L[1].split("-->")]
        if z <= t0 or a >= t1:
            continue
        n += 1
        keep.append(f"{n}\n{to_ts(a - t0)} --> {to_ts(min(z, t1) - t0)}\n"
                    + "\n".join(L[2:]))
    dst.write_text("\n\n".join(keep) + "\n", encoding="utf-8")
    return n


ap = argparse.ArgumentParser()
ap.add_argument("--win", action="append", default=None,
                help="cua so 'start,end' (giay) — lap lai duoc; bo trong = 2 cua so mac dinh")
a = ap.parse_args()
wins = ([tuple(float(x) for x in w.split(",")) for w in a.win] if a.win else WINDOWS)

CLIPS.mkdir(parents=True, exist_ok=True)
sl = json.loads(SLIDES.read_text(encoding="utf-8"))
tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
TOTAL = max(L["end"] for L in tl)


def start_of(entry):
    for L in tl:
        if entry["match"] in L["text"]:
            return L["start"]
    return None


# ── chon entry cho TUNG cua so ───────────────────────────────────────────────
starts = []
for i, e in enumerate(sl):
    st = start_of(e)
    if st is None:
        raise SystemExit(f"[LOI] e{i} match khong co trong timeline: {e['match']!r} — "
                         "sua loi thoai thi phai quet lai `match` (pipeline muc 0)")
    starts.append((i, st))
starts.sort(key=lambda x: x[1])

plan = []
for (t0, t1) in wins:
    sel = []
    for k, (i, st) in enumerate(starts):
        nxt = starts[k + 1][1] if k + 1 < len(starts) else TOTAL
        if nxt <= t0 or st >= t1:
            continue
        sel.append((i, max(st, t0), min(nxt, t1)))   # cat 2 dau theo cua so
    plan.append(((t0, t1), sel))
    print(f"cua so {t0:.0f}-{t1:.0f}s -> entry {[i for i, _, _ in sel]}")

# ── dung clip: gom CA HAI cua so vao MOT lan goi make_* (tranh 2 build song song)
need = sorted({i for _, sel in plan for i, _, _ in sel})
vox = [str(i) for i in need if isinstance(sl[i].get("vox"), dict)]
shot = [str(i) for i in need if isinstance(sl[i].get("shot"), dict)]
print(f"vox {len(vox)}: {vox}\nshot {len(shot)}: {shot}")
if vox:
    run([sys.executable, ML / "make_vox.py", SLIDES, CLIPS, "--channel", "co-dai",
         "--img-dir", VD, "--only", *vox])
if shot:
    run([sys.executable, ML / "make_shot.py", "slides", SLIDES, CLIPS,
         "--img-dir", VD, "--only", *shot])

# ── ghep tung cua so ─────────────────────────────────────────────────────────
outs = []
for w, ((t0, t1), sel) in enumerate(plan):
    tag = f"{int(t0)}-{int(t1)}"
    parts = []
    for n, (i, s, e) in enumerate(sel):
        dur = round(e - s, 3)
        if dur <= 0.05:
            continue
        p = CLIPS / f"clip_{i:02d}.mp4"
        if not p.exists():
            raise SystemExit(f"[LOI] thieu clip {p} — make_* da chay chua?")
        q = OUT / f"_w{w}_s{n:02d}.mp4"
        # entry bi cat dau (khung dau cua so B) -> bo qua phan build-on da chay xong
        ss = ["-ss", str(round(s - start_of(sl[i]), 3))] if s > start_of(sl[i]) + 0.05 else []
        run(["ffmpeg", "-y", "-v", "error", *ss, "-i", p, "-t", dur,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", q])
        parts.append(q)

    lst = OUT / f"_concat{w}.txt"
    lst.write_text("".join(f"file '{q.as_posix()}'\n" for q in parts), encoding="utf-8")
    silent = OUT / f"_silent{w}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", silent])

    va = OUT / f"_voice{w}.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(t0), "-i", VD / "voice.wav",
         "-t", str(t1 - t0), "-c:a", "aac", "-b:a", "160k", va])

    sub = OUT / f"subs_w{w}.srt"
    ncue = srt_window(VD / "subs.srt", sub, t0, t1)
    print(f"  srt cua so {tag}: {ncue} cue (da dich moc ve 0)")

    final = OUT / f"demo24_{tag}.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(va),
                        "-vf", f"subtitles={sub.name}:force_style='FontName=Noto Sans JP,"
                               "FontSize=26,Outline=3,Shadow=0'",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", str(final)],
                       cwd=str(OUT))
    if r.returncode:
        raise SystemExit(f"[LOI] burn phu de cua so {tag} exit {r.returncode}")
    for q in parts:
        q.unlink(missing_ok=True)
    silent.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)
    va.unlink(missing_ok=True)
    outs.append(final)

for f in outs:
    print("XONG ->", f)
