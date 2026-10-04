@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-kinishinai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\01_demo_TTS.md --channel kinishinai --reuse > 06_VIDEO\01_demo\render.log 2>&1
>> 06_VIDEO\01_demo\render.log echo EXITCODE=%ERRORLEVEL%
