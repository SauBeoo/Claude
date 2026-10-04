# -*- coding: utf-8 -*-
"""Runner render video 01 — tránh vỡ encoding tên giọng Nhật trên command line."""
import subprocess
import sys

NENKIN = r"E:\Claude\Projects\youtube-jp-nenkin"
HEALTH = r"E:\Claude\Projects\youtube-jp-health"
STEM = "01_zaishoku-rorei-nenkin-kaisei-2026"

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
] + sys.argv[1:]

sys.exit(subprocess.call(args))
