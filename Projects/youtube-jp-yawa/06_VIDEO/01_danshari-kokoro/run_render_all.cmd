@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\01_danshari-kokoro_TTS.md --channel yawa --reuse > 06_VIDEO\01_danshari-kokoro\render.log 2>&1
set RE=%ERRORLEVEL%
echo EXITCODE=%RE% >> 06_VIDEO\01_danshari-kokoro\render.log
if not "%RE%"=="0" exit /b 1
python tools\overlay_narrator.py 06_VIDEO\01_danshari-kokoro\01_danshari-kokoro.mp4 06_VIDEO\01_danshari-kokoro\01_danshari-kokoro_final.mp4 > 06_VIDEO\01_danshari-kokoro\overlay.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> 06_VIDEO\01_danshari-kokoro\overlay.log
