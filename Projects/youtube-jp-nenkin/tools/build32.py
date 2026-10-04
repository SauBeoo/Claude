# -*- coding: utf-8 -*-
r"""build32.py — dung video 32. Vo mong cua `build28.py`: doi STEM + plan + telop, giu nguyen
co khi (ffmpeg thuan, anh TINH, cu dong, chip chuong, phu de tung dong).

Sua co khi => sua `build28.py` roi port sang, dung fork.
"""
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))

import build28 as b            # noqa: E402
import telop32                 # noqa: E402

STEM = "32_ginko-honnin-kakunin-2027"
b.STEM = STEM
b.VD = PROJ / "06_VIDEO" / STEM
b.ART, b.OUT = b.VD / "art_final", b.VD / "_build"
b.PLAN_NAME = "plan32.json"
b.TELOP = telop32.TELOP
# user 2026-09-27: "nói đến đâu hiển thị 1 câu đến đó" ⇒ telop neo vào lời đọc (build28.sync_times).
# Soi phép khớp trước khi build: `python tools/sync_report32.py` → telop_sync.txt
b.SYNC_TELOP = True

if __name__ == "__main__":
    sys.exit(b.main())
