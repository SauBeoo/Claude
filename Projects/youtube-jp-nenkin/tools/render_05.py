# -*- coding: utf-8 -*-
"""Runner render video 04 — 年金生活者支援給付金.
Dùng: CHUNKS_ONLY=1 python tools/render_04.py   → step A (chunk, resume-safe)
      python tools/render_04.py --reuse           → finalize (step B) sau khi chunk xong
"""
import subprocess
import sys

NENKIN = r"E:\Claude\Projects\youtube-jp-nenkin"
HEALTH = r"E:\Claude\Projects\youtube-jp-health"
STEM = "05_60sai-teinen-taishoku-kiken"

args = [
    sys.executable, rf"{HEALTH}\tools\video_render.py",
    rf"{NENKIN}\03_SCRIPTS\{STEM}_TTS.md",
    "--speaker", "雀松朱司",
    "--speed", "0.9",
    "--sub-style", "glass",
    "--bgm", rf"{HEALTH}\06_VIDEO\bgm\Wholesome.mp3",
    "--bgm-gain", "-40",
    "--slides", rf"{NENKIN}\03_SCRIPTS\{STEM}_SLIDES.json",
    "--img-dir", rf"{NENKIN}\06_VIDEO\{STEM}\slides_img",
    "--clips-dir", rf"{NENKIN}\06_VIDEO\{STEM}\clips",
] + sys.argv[1:]

sys.exit(subprocess.call(args))
