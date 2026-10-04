# -*- coding: utf-8 -*-
"""Runner render video 02 — tránh vỡ encoding tên giọng Nhật trên command line.
Dùng: python tools/render_02.py            → render đầy đủ
      CHUNKS_ONLY=1 python tools/render_02.py   → chỉ step A (chunk, resume-safe)
      python tools/render_02.py --reuse    → finalize (step B) sau khi chunk xong
"""
import subprocess
import sys

NENKIN = r"E:\Claude\Projects\youtube-jp-nenkin"
HEALTH = r"E:\Claude\Projects\youtube-jp-health"
STEM = "02_kurisage-jukyu-70sai-bunkiten"

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
