# -*- coding: utf-8 -*-
r"""Sinh SLIDES cho video 29 (FULL AI, 112 clip) + dat clip_XX.mp4 dung index.

video_render.py doi `clips/clip_{i:02d}.mp4` theo INDEX cua entry SLIDES, KHONG theo
ten mo ta. Tool nay lam ca hai viec:
  1. sinh SLIDES, moi entry `match` = MOT DONG CO THAT trong _TTS.md
  2. --place: copy clip (ten mo ta) sang clip_XX.mp4 dung index

🔴 BA BAY DA DINH THAT (2026-09-04), doc truoc khi sua:

 (1) SO CLIP != THU TU THOI GIAN. TENFILE2 danh so 42-112 nhung lo 2 duoc viet de
     "lap cho lo 1 con thua" -> clip 42-45 thuoc COLD OPEN. Sap theo so clip thi
     clip 45 bi day xuong cuoi bai (do duoc: lech 1.091 giay).
     => Tinh moc thoi gian cho TUNG clip roi SORT TOAN BO theo thoi gian; index
        SLIDES di theo thu tu do.
 (2) Neo THUAN theo dong TTS -> nhip vo (72 entry <6s, 17 entry >20s, trung vi 0,0s).
     Chia deu thoi gian THUAN -> 53 clip lech >45s khoi doan no minh hoa.
     => Giu ANCHOR lam moc cung, giua hai anchor noi suy theo THOI GIAN.
 (3) `used` set + ep tang dan se DON CUC neu thu tu vao sai -> sort TRUOC, gan dong SAU.

    python tools\gen_slides29.py              # sinh SLIDES + gate
    python tools\gen_slides29.py --place      # + dat clip_XX.mp4
"""
import argparse
import json
import re
import shutil
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
VD = P / "06_VIDEO" / "29_hocho-togi-mennaoshi"
TTS = P / "03_SCRIPTS" / "29_hocho-togi-mennaoshi_TTS.md"
OUT = P / "03_SCRIPTS" / "29_hocho-togi-mennaoshi_SLIDES.json"


def tts_lines():
    out = []
    for raw in TTS.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith("<!--"):
            continue
        out.append(re.sub(r"\[[^\]]*\]", "", s).strip())
    return out


def load_map():
    m = []
    for f in ("video_prompts_TENFILE.txt", "video_prompts_TENFILE2.txt"):
        p = VD / f
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            g = re.match(r"^\s*(\d+)\s*->\s*(\S+\.mp4)\s*\|\s*(.*)$", line)
            if g:
                m.append((int(g.group(1)), g.group(2), g.group(3).strip()))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--place", action="store_true")
    a = ap.parse_args()

    lines = tts_lines()
    mp = load_map()
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
    T, starts = tl["total"], [float(x["start"]) for x in tl["lines"]]
    print(f"── {len(lines)} dong TTS · {len(mp)} clip · voice {T:.0f}s")

    # 1) ANCHOR cho clip co cau thoai Nhat that
    anc = {}
    for no, fn, cue in mp:
        if not cue or not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", cue):
            continue
        key = cue.split("（")[0].strip()[:14]
        hit = [i for i, L in enumerate(lines) if L.startswith(key)]
        if len(hit) == 1:
            anc[no] = starts[hit[0]]
    print(f"   anchor khop: {len(anc)}/{len(mp)}")

    # 2) MOC THOI GIAN cho MOI clip — noi suy TRONG TUNG LO (moi lo don dieu rieng)
    lots = {}
    for no, fn, cue in mp:
        lots.setdefault(1 if no <= 41 else 2, []).append(no)
    want = {}
    for lot, nos in lots.items():
        nos = sorted(nos)
        ks = [n for n in nos if n in anc]
        for n in nos:
            if n in anc:
                want[n] = anc[n]
                continue
            lo = max([k for k in ks if k < n], default=None)
            hi = min([k for k in ks if k > n], default=None)
            if lo is not None and hi is not None:
                want[n] = anc[lo] + (anc[hi] - anc[lo]) * (n - lo) / (hi - lo)
            elif hi is not None:
                want[n] = anc[hi] * (n - nos[0] + 1) / max(hi - nos[0] + 1, 1)
            elif lo is not None:
                want[n] = anc[lo] + (T - anc[lo]) * (n - lo) / max(nos[-1] - lo + 1, 1)
            else:
                want[n] = (n - nos[0]) / len(nos) * T

    # 3) 🔴 SORT TOAN BO theo thoi gian TRUOC, roi moi gan dong TTS
    order = sorted(mp, key=lambda x: (want[x[0]], x[0]))

    # rang buoc NHIP: moi entry cach entry truoc >= MIN_GAP giay
    # (audience-45plus.md §2 muc 2: khong entry nao <6 giay)
    MIN_GAP = 6.0
    used, slides, last_t = set(), [], -MIN_GAP
    for no, fn, cue in order:
        cand = [i for i in range(len(starts))
                if i not in used and starts[i] >= last_t + MIN_GAP]
        if not cand:                       # het cho -> lay dong ke tiep con trong
            cand = [i for i in range(len(starts)) if i not in used]
        c = min(cand, key=lambda i: (abs(starts[i] - want[no]), i))
        used.add(c); last_t = starts[c]
        slides.append({"match": lines[c], "video": True, "_clip": fn, "_no": no, "_line": c})
    slides.sort(key=lambda s: s["_line"])
    prev = -1
    for s in slides:
        if s["_line"] <= prev:
            s["_line"] = min(prev + 1, len(lines) - 1)
            s["match"] = lines[s["_line"]]
        prev = s["_line"]

    OUT.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── GATE
    bad = [s for s in slides if sum(1 for L in lines if L == s["match"]) != 1]
    secs = [starts[s["_line"]] for s in slides]
    g = [secs[i + 1] - secs[i] for i in range(len(secs) - 1)]
    lech = [(s["_no"], s["_clip"], round(abs(anc[s["_no"]] - starts[s["_line"]])))
            for s in slides if s["_no"] in anc and abs(anc[s["_no"]] - starts[s["_line"]]) > 45]
    print(f"\n── SLIDES: {len(slides)} entry -> {OUT.name}")
    print(f"   khoang cach GIAY: min {min(g):.1f} · trung vi {statistics.median(g):.1f} · max {max(g):.1f}")
    print(f"   entry <6s: {sum(1 for x in g if x < 6)} · >20s: {sum(1 for x in g if x > 20)}"
          f" · nhip {len(slides)/(T/60):.2f} doi hinh/phut")
    print("   ✅ moi `match` khop dung 1 dong" if not bad else f"   🔴 {len(bad)} match hong")
    if lech:
        print(f"   ⚠️ {len(lech)} clip lech >45s khoi doan no minh hoa:")
        for no, fn, d in lech[:5]:
            print(f"      clip {no:3d} {fn:34s} lech {d}s")
    else:
        print("   ✅ khong clip nao lech >45s khoi doan no minh hoa")

    if a.place:
        cl = VD / "clips"
        n, miss = 0, []
        for i, s in enumerate(slides):
            src, dst = cl / s["_clip"], cl / f"clip_{i:02d}.mp4"
            if not src.exists():
                miss.append(s["_no"])
                continue
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dst)
                n += 1
        print(f"\n✅ dat {n} clip_XX.mp4")
        if miss:
            print(f"🔴 THIEU {len(miss)} clip (so {min(miss)}-{max(miss)}) "
                  f"-> KHONG render (render-background.md §1.5)")
            return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
