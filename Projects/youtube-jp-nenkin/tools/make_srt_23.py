# -*- coding: utf-8 -*-
r"""make_srt_23.py — xuat `subs.srt` cho video 23 tu `timeline.json`.

VI SAO CAN TOOL NAY: duong REMOTION burn phu de vao khung nhung **khong xuat file
srt** — trong khi `youtube-upload-seo.md` §1.2 bat buoc upload `subs.srt` bang tay
(cam auto-caption). Duong `video_render.py` cu thi tu sinh; doi engine la mat.
(Dung ho bai hoc "doi engine dung hinh thi phai ra lai tung thu engine cu lam ho",
`nenkin/CLAUDE.md` §②.)

Che khoi theo dung ham `split_caption` cua `build_remotion_23.py` (tran 78 ky,
cat SAU dau cau) => file srt khop tung khoi voi phu de chay tren man hinh.

CHAY:  python tools/make_srt_23.py
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJ, "tools"))
VD = os.path.join(PROJ, "06_VIDEO", "23_nenkin-seikyusho-todokanai")

from build_remotion_23 import split_caption  # noqa: E402


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))
    out, n, nsplit = [], 0, 0
    for ln in tl["lines"]:
        parts = split_caption(ln["text"])
        if len(parts) > 1:
            nsplit += 1
        tot = sum(len(p) for p in parts)
        t = ln["start"]
        dur = ln["end"] - ln["start"]
        for p in parts:
            d = dur * len(p) / tot
            n += 1
            out.append(f"{n}\n{ts(t)} --> {ts(t + d)}\n{p}\n")
            t += d
    dst = os.path.join(VD, "subs.srt")
    io.open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    longest = max(len(l["text"]) for l in tl["lines"])
    print(f"→ {dst}")
    print(f"   {len(tl['lines'])} dong timeline -> {n} khoi srt "
          f"({nsplit} dong phai che) · dai nhat {longest} ky")
    print(f"   tong {tl['total']:.1f}s — phai khop duration mp4")
    bad = [o for o in out if len(o.split("\n")[2]) > 78]
    print("   " + ("✅ moi khoi <=78 ky" if not bad else f"🔴 {len(bad)} khoi >78 ky"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
