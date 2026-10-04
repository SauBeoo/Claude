@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-kinishinai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python tools\render_voice_only.py 01_kuchiguse-hitonome > 06_VIDEO\01_kuchiguse-hitonome\voice.log 2>&1
>> 06_VIDEO\01_kuchiguse-hitonome\voice.log echo EXITCODE=%ERRORLEVEL%
