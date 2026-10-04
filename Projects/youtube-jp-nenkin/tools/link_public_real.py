# -*- coding: utf-8 -*-
r"""link_public_real.py — hardlink assets cua nenkin-19real sang public_n19r.

🔴 VI SAO CAN THU MUC PUBLIC RIENG: Remotion **copy ca thu muc public** moi lan
   render. `public/` chua 25 project = **3,7 GB** => moi lenh render/still mat
   3-4 phut chi de copy, va `remotion still` phai copy lai cho TUNG frame (da mat
   mot luot 15 phut vi chuyen do). Tro `--public-dir` vao mot thu muc chi chua
   dung project nay (~700 MB) la xong.

🔴 VI SAO HARDLINK: cung o E: nen hardlink ton **0 byte** them. `cp -r` thi
   nhan doi 700 MB moi lan.

⚠️ THU TU QUAN TRONG: phai chay SAU khi ingest + make_bgblur xong, neu khong
   public_n19r thieu file va render ra video **KHONG CO TIENG / THIEU HINH ma
   EXITCODE van 0** (da suyt dinh o ban vox: public_n19 tao truoc khi builder
   copy voice.mp3 vao).

CHAY:  python tools/link_public_real.py
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RV = os.path.join("E:" + os.sep, "Claude", "Projects", "remotion-vox")
SRC = os.path.join(RV, "public", "projects", "nenkin-19real", "assets")
DST = os.path.join(RV, "public_n19r", "projects", "nenkin-19real", "assets")


def main():
    os.makedirs(DST, exist_ok=True)
    n = link = copy = 0
    for fn in sorted(os.listdir(SRC)):
        a, b = os.path.join(SRC, fn), os.path.join(DST, fn)
        n += 1
        if os.path.exists(b) and os.path.getmtime(b) >= os.path.getmtime(a):
            continue
        if os.path.exists(b):
            os.remove(b)
        try:
            os.link(a, b)
            link += 1
        except OSError:
            shutil.copy(a, b)
            copy += 1
    have = len(os.listdir(DST))
    print(f"OK  {have}/{n} file o public_n19r (hardlink {link} · copy {copy})")
    must = ["voice.mp3", "bgm.mp3", "paper.jpg"]
    miss = [m for m in must if not os.path.exists(os.path.join(DST, m))]
    if miss:
        print(f"🔴 THIEU asset song con: {miss} — render se ra video hong ma exit 0")
        sys.exit(1)
    nclip = sum(1 for f in os.listdir(DST) if f.startswith("rclip19_"))
    nblur = sum(1 for f in os.listdir(DST) if f.startswith("bgblur_"))
    ngen = sum(1 for f in os.listdir(DST) if f.startswith("card_genten"))
    print(f"   clip real {nclip} · nen mo {nblur} · the 原典 {ngen}")
    if nclip != 74:
        print(f"🔴 phai co 74 clip real, dang co {nclip}")
        sys.exit(1)


if __name__ == "__main__":
    main()
