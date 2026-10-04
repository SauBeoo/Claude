# -*- coding: utf-8 -*-
r"""check_bars_20.py — tim VIEN DEN THAT o mep clip (letterbox do Veo gen ra).

🔴 PHEP DO DAU TIEN CUA TAO SAI, ghi lai de khong lap:
   Ban dau tao dem "cot co do sang trung binh < 25" => ra **30/83 clip dinh**.
   Nhung canh TOI THAT (tuong toi, khung cua, hanh lang) cung thoa dieu kien do.
   Kiem lai 6 clip: `junban` `izoku_kiso` `todoku` `mata` **khong he co vien**,
   do la noi dung. Chi `cta_d` va `dansa_b` co vien that.
   ⇒ Gate hoi sai cau: "cot co toi khong" thay vi "cot co phai VIEN khong".

📐 PHAN BIET: vien letterbox thi cot vua **RAT TOI** (mean < 12) vua **GAN NHU
   KHONG DOI** doc theo chieu cao (std < 6). Canh toi that luon co bien thien
   (chi tiet, do doc anh sang) nen std lon.

CHAY:  python tools/check_bars_20.py
"""
import glob
import io as _io
import os
import subprocess
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "20_izoku-nenkin-yonbunno-san")


def frame(f, t):
    o = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f,
                        "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True)
    if not o.stdout:
        return None
    return np.array(Image.open(_io.BytesIO(o.stdout)).convert("L")).astype(float)


def run_edge(a, axis, rev):
    """dem so hang/cot lien tiep tu mep vao thoa 'rat toi + gan nhu khong doi'."""
    n = a.shape[1] if axis == 1 else a.shape[0]
    idx = range(n - 1, n - 1 - 200, -1) if rev else range(200)
    out = 0
    for i in idx:
        line = a[:, i] if axis == 1 else a[i, :]
        if line.mean() < 12 and line.std() < 6:
            out += 1
        else:
            break
    return out


def main():
    fs = sorted(glob.glob(os.path.join(VD, "clips", "*.mp4")))
    bad = []
    for f in fs:
        # do o 2 moc: vien that co o CA HAI, canh toi thi thuong doi
        res = []
        for t in (2, 6):
            a = frame(f, t)
            if a is None:
                continue
            res.append((run_edge(a, 1, False), run_edge(a, 1, True),
                        run_edge(a, 0, False), run_edge(a, 0, True)))
        if not res:
            continue
        L, R, T, B = (min(r[k] for r in res) for k in range(4))
        if max(L, R, T, B) >= 6:
            bad.append((os.path.basename(f), L, R, T, B))
    print(f"{len(fs)} clip | co VIEN DEN THAT >=6px: {len(bad)}")
    for b in bad:
        print(f"   {b[0]:34s} trai {b[1]:3d}  phai {b[2]:3d}  tren {b[3]:3d}  duoi {b[4]:3d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
