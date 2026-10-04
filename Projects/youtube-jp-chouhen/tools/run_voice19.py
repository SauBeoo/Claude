# -*- coding: utf-8 -*-
"""Khâu 0+1 video 19 — prefetch cache TTS 4 luồng rồi synth voice.
VOICE ARM B: VOICEVOX 青山龍星 / ノーマル / 速0.80 / 抑揚1.15.
Gọi qua .py để né bẫy non-ASCII trên command line Windows (CLAUDE.md §Handoff).
"""
import subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
TTS = PROJ / "03_SCRIPTS" / "19_daiku-no-enpitsu_TTS.md"
VOICE = ["--engine", "voicevox", "--speaker", "青山龍星",
         "--speed", "0.80", "--intonation", "1.15"]

print("=== KHAU 0: prefetch cache TTS (4 jobs) ===", flush=True)
rc = subprocess.run([sys.executable, str(PROJ / "tools" / "tts_prefetch.py"),
                     str(TTS), *VOICE, "--jobs", "4"], cwd=str(PROJ)).returncode
print(f"--- prefetch rc={rc}", flush=True)

print("=== KHAU 1: synth voice.wav + subs.srt ===", flush=True)
rc = subprocess.run([sys.executable, str(PROJ / "tools" / "ambient_render.py"),
                     str(TTS), *VOICE, "--voice-only"], cwd=str(PROJ)).returncode
print(f"--- voice rc={rc}", flush=True)
sys.exit(rc)
