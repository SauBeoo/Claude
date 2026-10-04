# -*- coding: utf-8 -*-
"""Khâu 1 video 17 — synth voice VOICEVOX 青山龍星 0.80 (VOICE ARM B).
Gọi qua .py để né bẫy non-ASCII trên command line Windows (CLAUDE.md §Handoff).
Tham số 1 (tuỳ chọn): stem của file TTS, mặc định 17_sakura-no-kigata_TTS.md
"""
import subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
stem = sys.argv[1] if len(sys.argv) > 1 else "17_sakura-no-kigata_TTS"
cmd = [sys.executable, str(PROJ / "tools" / "ambient_render.py"),
       str(PROJ / "03_SCRIPTS" / f"{stem}.md"),
       "--engine", "voicevox", "--speaker", "青山龍星",
       "--speed", "0.80", "--intonation", "1.15", "--voice-only"]
if len(sys.argv) > 2:
    cmd += ["--out-dir", sys.argv[2]]
sys.exit(subprocess.run(cmd, cwd=str(PROJ)).returncode)
