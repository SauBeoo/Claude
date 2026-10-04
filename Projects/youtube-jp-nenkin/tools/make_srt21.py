# -*- coding: utf-8 -*-
r"""make_srt21.py  [<stem> <ten_project_remotion>] — xuat `subs.srt` tu project.json cua Remotion.

🔴 VI SAO CAN: `youtube-upload-seo.md` §1.2 bat buoc **tu upload subs.srt**, cam
   auto-caption (kem chinh xac + mat mot tin hieu SEO la van ban chuan). Duong
   `video_render.py` cu tu sinh srt; **doi sang Remotion la mat buoc do** —
   video 20 da len song KHONG co srt. Day dung la bai hoc "doi engine dung hinh
   thi phai ra lai tung thu engine cu lam ho" (`CLAUDE.md` §②).

Nguon: `captions.lines` trong project.json — chinh la cac khoi da CHE theo tran
78 ky (`split_caption`), nen srt khop tung khoi voi phu de chay tren video.

CHAY:  python tools/make_srt21.py
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = sys.argv[1] if len(sys.argv) > 1 else "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
PJ = os.path.join(os.path.dirname(PROJ), "remotion-vox", "projects",
                  (sys.argv[2] if len(sys.argv) > 2 else "nenkin-21"), "project.json")


def ts(ms):
    ms = max(0, int(round(ms)))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    doc = json.load(io.open(PJ, encoding="utf-8"))
    lines = doc["captions"]["lines"]
    out, prev_end = [], -1
    for i, c in enumerate(lines, 1):
        a, b = c["startMs"], c["endMs"]
        # 🔴 chong CHONG LAN: khoi sau bat dau truoc khi khoi truoc ket thuc thi
        #    player nao cung hien hai khoi cung luc. Ep a >= prev_end + 1ms.
        if a <= prev_end:
            a = prev_end + 1
        if b <= a:
            b = a + 300
        prev_end = b
        out.append(f"{i}\n{ts(a)} --> {ts(b)}\n{c['text']}\n")
    p = os.path.join(VD, "subs.srt")
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    dur = lines[-1]["endMs"] / 1000
    over = sum(1 for c in lines if len(c["text"]) > 78)
    print(f"→ {p}")
    print(f"   {len(out)} khoi · cuoi {dur:.1f}s")
    print(f"   GATE khoi >78 ky : {'✅ 0' if not over else '🔴 ' + str(over)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
