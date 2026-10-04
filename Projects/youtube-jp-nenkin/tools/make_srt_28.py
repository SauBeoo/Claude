# -*- coding: utf-8 -*-
r"""make_srt_28.py - xuat `subs.srt` cho video 28 tu `timeline.json`.

VI SAO CAN TOOL NAY: duong `build28.py` (ffmpeg thuan) burn phu de vao khung nhung
**khong xuat file srt** - trong khi `youtube-upload-seo.md` §1.2 bat buoc upload
`subs.srt` bang tay (cam auto-caption). `upload_pack.py` bao "srt: THIEU".
Dung ho bai hoc "doi engine dung hinh thi phai ra lai tung thu engine cu lam ho"
(`nenkin/CLAUDE.md` §2) - `video_render.py` cu tu sinh srt, hai engine sau thi khong.

KHOP VOI PHU DE CHAY TREN MAN HINH: `caption_layers()` cua build28 lay **MOI DONG
timeline = MOT khoi phu de, nguyen van** (ham `wrap_cap` chi chia 2 dong DE HIEN,
khong doi loi). => srt cung 1 cue / 1 dong timeline, khong che khoi, khong gop.

CHAY:  python tools/make_srt_28.py
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "28_kouki-75sai-tanjyotsuki-hokenryo")


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def main():
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))
    out, n, prev_end = [], 0, -1.0
    for ln in tl["lines"]:
        txt = (ln.get("text") or "").strip()
        if not txt:
            continue
        st, en = float(ln["start"]), float(ln["end"])
        if en <= st:
            print("SKIP cue rong/nguoc: %.3f -> %.3f" % (st, en))
            continue
        if st < prev_end - 1e-6:
            print("CHONG CUE tai %.3f (cue truoc ket %.3f)" % (st, prev_end))
        prev_end = en
        n += 1
        out.append("%d\n%s --> %s\n%s\n" % (n, ts(st), ts(en), txt))
    dst = os.path.join(VD, "subs.srt")
    io.open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")

    longest = max(len(o.split("\n")[2]) for o in out)
    print("-> %s" % dst)
    print("   %d dong timeline -> %d cue - dai nhat %d ky" % (len(tl["lines"]), n, longest))
    print("   tong timeline %.1fs - PHAI khop duration mp4" % tl["total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
