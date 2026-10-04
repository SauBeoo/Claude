# -*- coding: utf-8 -*-
"""Khâu 0+1 video 21 — prefetch cache TTS 4 luồng rồi synth voice.
VOICE ARM **A**: AivisSpeech morioki / speed 1.0 / 抑揚 1.0 (giọng NỮ).
Đổi từ arm B (青山龍星) ngày 2026-08-09: POV truyện là nữ「私」, và 4/4 video từng
được YouTube phân phối của kênh đều dùng morioki. Phép A/B giọng đã chạy đủ
3 video/nhánh nhưng cả 6 đều 0–1 view → không đọc được kết quả, xem AB_LOG.md.
Gọi qua .py để né bẫy non-ASCII trên command line Windows (CLAUDE.md §Handoff).
"""
import subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
TTS = PROJ / "03_SCRIPTS" / "21_hachinen-no-yachin_TTS.md"
VOICE = ["--engine", "aivis", "--speaker", "morioki",
         "--speed", "1.0", "--intonation", "1.0"]

print("=== KHAU 0: prefetch cache TTS (4 jobs) ===", flush=True)
rc = subprocess.run([sys.executable, str(PROJ / "tools" / "tts_prefetch.py"),
                     str(TTS), *VOICE, "--jobs", "4"], cwd=str(PROJ)).returncode
print(f"--- prefetch rc={rc}", flush=True)

print("=== KHAU 1: synth voice.wav + subs.srt ===", flush=True)
rc = subprocess.run([sys.executable, str(PROJ / "tools" / "ambient_render.py"),
                     str(TTS), *VOICE, "--voice-only"], cwd=str(PROJ)).returncode
print(f"--- voice rc={rc}", flush=True)
sys.exit(rc)
