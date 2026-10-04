# -*- coding: utf-8 -*-
r"""build29.py — dung video 29. Vo mong cua `build28.py`: doi STEM + plan + telop, giu nguyen
co khi (ffmpeg thuan, anh TINH, cu dong, chip chuong, phu de tung dong).

Sua co khi => sua `build28.py` roi port sang, dung fork.
"""
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))

import build28 as b            # noqa: E402
import telop29                 # noqa: E402

STEM = "29_shikaku-kakuninsho-8gatsu-85sai"
b.STEM = STEM
b.VD = PROJ / "06_VIDEO" / STEM
b.ART, b.OUT = b.VD / "art_final", b.VD / "_build"
b.PLAN_NAME = "plan29.json"
b.TELOP = telop29.TELOP

if __name__ == "__main__":
    sys.exit(b.main())
