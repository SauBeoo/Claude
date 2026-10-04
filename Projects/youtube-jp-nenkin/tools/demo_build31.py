# -*- coding: utf-8 -*-
r"""demo_build31.py — dựng HÌNH N ô đầu video 31 (telop neo lời) vào _build_demo/, không đè bản đầy đủ.

Rồi `python tools/asmr31.py --demo N` trộn lớp ASMR + tầng âm cuối → demo31_asmr.mp4 cho user nghe.
CHẠY:  python tools/demo_build31.py 10
"""
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import build31  # noqa: E402,F401
import build28 as b  # noqa: E402

b.OUT = b.VD / "_build_demo"
b.STEM = "demo31_video_only"      # fin của build28 = VD/<STEM>.mp4 ⇒ không đè bản thật

if __name__ == "__main__":
    sys.exit(b.main())
