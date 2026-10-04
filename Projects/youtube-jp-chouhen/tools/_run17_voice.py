# -*- coding: utf-8 -*-
"""One-off wrapper for video 17 v3 render — avoids cmd.exe mangling the Japanese
speaker name (bài học ghi ở run_voiceab.py / CLAUDE.md Handoff). Chạy 2 bước:
tts_prefetch (song song 4 job) rồi ambient_render --voice-only.
"""
import subprocess
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SLUG = "17_sakura-no-kigata"
SPEAKER = "青山龍星"
SCRIPT = PROJ / "07_UPLOADED" / SLUG / "_scripts" / f"{SLUG}_TTS.md"

common = ["--engine", "voicevox", "--speaker", SPEAKER, "--speed", "0.80", "--intonation", "1.15"]

print("==== PREFETCH ====", flush=True)
r1 = subprocess.run(
    [sys.executable, str(PROJ / "tools" / "tts_prefetch.py"), str(SCRIPT), *common, "--jobs", "4"],
    cwd=str(PROJ),
)
print(f"PREFETCH_EXIT={r1.returncode}", flush=True)

print("==== VOICE ONLY ====", flush=True)
r2 = subprocess.run(
    [sys.executable, str(PROJ / "tools" / "ambient_render.py"), str(SCRIPT), *common, "--voice-only"],
    cwd=str(PROJ),
)
print(f"VOICE_EXIT={r2.returncode}", flush=True)

sys.exit(r2.returncode)
