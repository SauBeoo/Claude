# -*- coding: utf-8 -*-
"""Render 7 giong demo 30s dau (yawa bai 1). Chay tuan tu, ghi render.log."""
import subprocess, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = Path(__file__).parent
TOOL = r"E:\Claude\Projects\youtube-jp-health\tools\tts_render.py"
V = [("01_aivis_morioki", "aivis", "morioki"),
     ("02_aivis_mao_ochitsuki", "aivis", "まお"),
     ("03_vv_No7_yomikikase", "voicevox", "No.7"),
     ("04_vv_meimei_himari", "voicevox", "冥鳴ひまり"),
     ("05_vv_tohoku_itako", "voicevox", "東北イタコ"),
     ("06_aivis_aida_shigeru_calm", "aivis", "阿井田 茂"),
     ("07_vv_kigashima_sorin", "voicevox", "麒ヶ島宗麟")]
bad = 0
for name, eng, spk in V:
    r = subprocess.run([sys.executable, TOOL, str(D / f"{name}_TTS.md"), "-o", str(D / f"{name}.wav"),
                        "--engine", eng, "--speaker", spk, "--speed", "0.9"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"== {name} EXIT={r.returncode}\n{r.stdout[-600:]}{r.stderr[-600:]}", flush=True)
    bad += r.returncode != 0
sys.exit(bad)
