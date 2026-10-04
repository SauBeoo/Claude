# -*- coding: utf-8 -*-
"""Khâu 1 video 15 — synth voice VOICEVOX 青山龍星 0.80 (VOICE ARM B), gọi qua .py để né bẫy non-ASCII trên command line."""
import subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
r = subprocess.run([sys.executable, str(PROJ / "tools" / "ambient_render.py"),
                    str(PROJ / "03_SCRIPTS" / "15_gifu-no-kashikinko_TTS.md"),
                    "--engine", "voicevox", "--speaker", "青山龍星",
                    "--speed", "0.80", "--intonation", "1.15", "--voice-only"],
                   cwd=str(PROJ))
sys.exit(r.returncode)
