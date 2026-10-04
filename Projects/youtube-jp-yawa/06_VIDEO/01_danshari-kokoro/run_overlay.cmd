@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa
set PYTHONIOENCODING=utf-8
python tools\overlay_narrator.py 06_VIDEO\01_danshari-kokoro\01_danshari-kokoro.mp4 06_VIDEO\01_danshari-kokoro\01_danshari-kokoro_final.mp4 > 06_VIDEO\01_danshari-kokoro\overlay.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> 06_VIDEO\01_danshari-kokoro\overlay.log
