# -*- coding: utf-8 -*-
"""build_remotion_01.py — lop CHU Remotion (chip chuong · o chu tu khoa · 出典 · the so) tren NEN = ban render final.

Nen = 06_VIDEO/<stem>/01_kuchiguse-hitonome.mp4 (anh still_kb + nguoi dan + phu de chay san) — khong dung lai anh.
Noi dung: 06_VIDEO/<stem>/_plan/remo_spec.py. Moc hien chu = dau cau + (vi tri tu khoa / do dai cau) x thoi luong cau
(port toi gian `sync_times`, youtube-jp-nenkin/tools/build28.py:218).
Preset: remotion-vox/src/components/KinText.tsx (kin-chip / kin-callout / kin-source / kin-stat) — chi fade.
Gate (chan cung): asset ton tai · moi lop y < 790 (phu de 2 dong bat dau y~796) · o chu khong roi vao slide nguoi dan
· khong 2 o chu cung luc · chu khong roi vao the chu (card/reveal) tru the so.
Chay: python tools/build_remotion_01.py 01_kuchiguse-hitonome --demo 100-215   (bo --demo = ca bai)
"""
import sys, io, json, argparse, subprocess, importlib.util, shutil
from pathlib import Path
import numpy as np
import cv2

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
RV = Path(r"E:\Claude\Projects\remotion-vox")
FPS = 30
SUB_TOP = 790
HOLD = 4.5
MIN_HOLD = 3.5      # nguoi 60+ doc kip: o chu dung >= 3,5s, hien som hon tu khoa neu tu khoa sat cuoi slide


FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def frame_at(mp4, t):
    cap = cv2.VideoCapture(str(mp4)); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    return f if ok else None


def box_size(text, size=64):
    lines = text.split("\n")
    w = max(len(l) for l in lines) * size + int(size * 1.5) + 10
    return w, int(len(lines) * size * 1.35 + size * 0.94)


PROFILE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
HOG = cv2.HOGDescriptor(); HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def people_boxes(frame):
    """Mat chinh dien + mat nghieng (2 chieu) + dang nguoi (HOG) — tra ve hop o toa do 1920x1080.
    Mat nghieng bi bo sot o ban dau (still 2:11: o chu de dau chang trai dang nghieng)."""
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out = [tuple(b) for b in FACE.detectMultiScale(g, 1.1, 5, minSize=(50, 50))]
    out += [tuple(b) for b in PROFILE.detectMultiScale(g, 1.1, 5, minSize=(50, 50))]
    W = g.shape[1]
    out += [(W - x - w, y, w, h) for (x, y, w, h) in PROFILE.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(50, 50))]
    faces = [(x - w // 3, y - h // 3, w * 5 // 3, h * 5 // 3) for (x, y, w, h) in out]   # noi rong: toc + tran
    sm = cv2.resize(frame, (960, 540))
    rects, _ = HOG.detectMultiScale(sm, winStride=(8, 8), padding=(8, 8), scale=1.05)
    bodies = [(x * 2, y * 2, w * 2, h * 2) for (x, y, w, h) in rects]
    return faces, bodies


def overlap(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1]); x1, y1 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    return max(0, x1 - x0) * max(0, y1 - y0) / float(a[2] * a[3])


def place(frame, text):
    """Chon cho TRONG NHAT cho o chu: 4 o ung vien.
    Diem = mat do canh (Canny) + 3 x phan dien tich de len MAT + 1 x phan de len NUA TREN dang nguoi."""
    bw, bh = box_size(text)
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); e = cv2.Canny(g, 60, 150)
    faces, bodies = people_boxes(frame)
    heads = [(x, y, w, h // 2) for (x, y, w, h) in bodies]
    cand = {"tl": (96, 130), "tr": (1920 - 96 - bw, 130), "ml": (96, 330), "mr": (1920 - 96 - bw, 330)}
    best = None
    for k, (x, y) in cand.items():
        y1 = min(y + bh, 780)
        if y1 - y < bh * 0.9:
            continue
        box = (x, y, bw, y1 - y)
        dens = e[y:y1, x:x + bw].mean() / 255
        sc = dens + 3.0 * sum(overlap(box, f) for f in faces) + 1.0 * sum(overlap(box, h) for h in heads)
        if best is None or sc < best[0]:
            best = (sc, k, x, y)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("--demo", help="giay a-b, vd 100-215")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    spec = importlib.util.spec_from_file_location("rs", vd / "_plan" / "remo_spec.py")
    S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
    sl = json.loads((PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json").read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8")); L, T = tl["lines"], tl["total"]
    t0, t1 = (float(x) for x in a.demo.split("-")) if a.demo else (0.0, T)
    name = f"kinishinai-{a.stem[:2]}" + ("demo" if a.demo else "")

    def line_of(prefix):
        hit = [n for n, ln in enumerate(L) if ln["text"].startswith(prefix) or prefix in ln["text"]]
        assert hit, f"khong thay cau 「{prefix}」"
        return hit[0]

    def at_kw(n, kw):
        ln = L[n]; i = ln["text"].find(kw)
        assert i >= 0, f"tu khoa 「{kw}」 khong co trong 「{ln['text']}」"
        return ln["start"] + (i / len(ln["text"])) * (ln["end"] - ln["start"])

    # khung slide: (t_dau, t_cuoi, loai)
    st = sorted((next(l for l in L if e["match"] in l["text"])["start"] + float(e.get("offset", 0.0)), i)
                for i, e in enumerate(sl))
    st[0] = (0.0, st[0][1])
    spans = []
    for k, (t, i) in enumerate(st):
        e = sl[i]; end = st[k + 1][0] if k + 1 < len(st) else T
        kind = "host" if e.get("_host") else ("card" if e.get("card") else ("reveal" if e.get("reveal") else "img"))
        spans.append((t, end, kind, i))
    slide_at = lambda t: next(s for s in spans if s[0] <= t < s[1])

    clips = {"chip": [], "callout": [], "source": [], "stat": []}
    # chip chuong: tu het the chuong toi the chuong ke tiep (an o slide nguoi dan — clip co o chu rieng)
    ch = [(line_of(p), lab, tit) for p, lab, tit in S.CHAPTERS]
    for k, (n, lab, tit) in enumerate(ch):
        card = slide_at(L[n]["start"])
        c0 = card[1]
        c1 = slide_at(L[ch[k + 1][0]]["start"])[0] if k + 1 < len(ch) else T
        # cat bo cac doan nguoi dan
        cur = c0
        for s in spans:
            if s[2] == "host" and c0 <= s[0] < c1:
                if s[0] - cur > 1.0:
                    clips["chip"].append((cur, s[0], f"{lab}\n{tit}"))
                cur = s[1]
        if c1 - cur > 1.0:
            clips["chip"].append((cur, c1, f"{lab}\n{tit}"))
    for p, kw, txt in S.CALLOUT:
        n = line_of(p); ta = at_kw(n, kw); s = slide_at(ta)
        assert s[2] == "img", f"o chu 「{txt}」 roi vao slide {s[2]} #{s[3]}"
        on = max(s[0] + 0.6, min(ta, s[1] - 0.3 - MIN_HOLD))
        clips["callout"].append((on, min(on + HOLD, s[1] - 0.3), txt))
    for p, txt in S.SOURCE:
        n = line_of(p); s = slide_at(L[n]["start"] + 0.01)
        clips["source"].append((L[n]["start"] + 0.3, s[1] - 0.2, txt))
    for p, txt, kws in S.STAT:
        n = line_of(p); s = slide_at(L[n]["start"] + 0.01)
        assert s[2] == "card", f"the so phai dat len the chu, gap {s[2]}"
        # "" = hien ngay khi vao the (0,3s) — tranh the trong tron cho toi luc doc toi tu khoa
        times = [0.3 if not k else round(at_kw(n, k) - s[0], 2) for k in kws]
        clips["stat"].append((s[0], s[1], txt, times))

    # gate: 2 o chu khong cung luc
    co = sorted(clips["callout"])
    for x, y in zip(co, co[1:]):
        assert y[0] >= x[1], f"2 o chu chong nhau: {x[2]!r} / {y[2]!r}"

    # cat theo cua so demo + doi ra frame
    def win(a0, a1):
        b0, b1 = max(a0, t0), min(a1, t1)
        return (round((b0 - t0) * FPS), round((b1 - b0) * FPS)) if b1 - b0 > 0.5 else None

    dur = round((t1 - t0) * FPS)
    rdir = RV / "projects" / name; adir = RV / "public" / "projects" / name / "assets"
    rdir.mkdir(parents=True, exist_ok=True); adir.mkdir(parents=True, exist_ok=True)
    base = vd / f"{a.stem}.mp4"
    assert base.exists(), f"thieu nen {base}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", str(base), "-t", f"{t1 - t0:.3f}",
                    "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-r", str(FPS), str(adir / "base.mp4")],
                   check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", str(base), "-t", f"{t1 - t0:.3f}",
                    "-vn", "-ac", "2", "-ar", "48000", str(adir / "audio.wav")], check=True)

    tr_text = []
    for kind, preset in (("chip", "kin-chip"), ("callout", "kin-callout"), ("source", "kin-source"), ("stat", "kin-stat")):
        for k, c in enumerate(clips[kind]):
            w = win(c[0], c[1])
            if not w:
                continue
            clip = {"id": f"{kind}{k}", "kind": "text", "from": w[0], "durationInFrames": w[1], "content": c[2],
                    "preset": preset, "animation": "none", "layout": {}}
            if kind == "callout":
                fr = frame_at(base, max(c[0], t0) + 0.8)
                sc, pos, x, y = place(fr, c[2])
                clip["layout"] = {"x": x, "y": y}; clip["_pos"] = f"{pos} {sc:.3f}"
            if kind == "stat":
                off = max(0.0, t0 - c[0])
                clip["animationParams"] = {"times": [max(0.0, x - off) for x in c[3]]}
            tr_text.append((preset, clip))
    stat = [c for p, c in tr_text if p == "kin-stat"]
    proj = {
        "version": 1,
        "meta": {"name": name, "channel": "kinishinai", "fps": FPS, "width": 1920, "height": 1080},
        "timeline": {"durationInFrames": dur},
        "tracks": [
            {"id": "trk-base", "name": "nen", "type": "video", "clips": [{"id": "base", "kind": "video", "from": 0,
             "durationInFrames": dur, "asset": "assets/base.mp4", "fit": "cover", "motion": "none", "volume": 0}]},
            {"id": "trk-stat", "name": "the so", "type": "text", "clips": stat},
            {"id": "trk-text", "name": "chu", "type": "text", "clips": [c for p, c in tr_text if p != "kin-stat"]},
            {"id": "trk-audio", "name": "tieng", "type": "audio", "clips": [{"id": "a0", "kind": "audio", "from": 0,
             "durationInFrames": dur, "asset": "assets/audio.wav", "volume": 1}]},
        ],
        "captions": {"enabled": False, "lines": []},
        "theme": {"fontFamily": '"Yu Gothic", "YuGothic", "Meiryo", sans-serif', "canvasColor": "#000000"},
    }
    (rdir / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{name}: {dur} frame ({t1 - t0:.1f}s)")
    for p, c in tr_text:
        print(f"  {p:11s} {c['from'] / FPS + t0:7.1f}s +{c['durationInFrames'] / FPS:4.1f}s  {c.get('_pos', ''):10s} {c['content'].replace(chr(10), ' / ')}")
    print("->", rdir / "project.json")


if __name__ == "__main__":
    main()
