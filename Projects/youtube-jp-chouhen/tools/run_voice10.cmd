@echo off
cd /d E:\Claude\Projects\youtube-jp-chouhen
python tools\ambient_render.py 03_SCRIPTS\10_haha-no-gamaguchi_TTS.md --engine aivis --speaker morioki --speed 1.0 --voice-only > 06_VIDEO\voice10.log 2>&1
echo DONE >> 06_VIDEO\voice10.log
