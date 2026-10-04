@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\01_danshari-kokoro_TTS.md --channel yawa --slides-only --reuse --skip-preflight > 06_VIDEO\01_danshari-kokoro\slides_only.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> 06_VIDEO\01_danshari-kokoro\slides_only.log
