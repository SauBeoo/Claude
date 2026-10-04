@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-showa
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set VD=06_VIDEO\22_kieta-shigoto
python tools\make_voice_22.py > "%VD%\voice.log" 2>&1
>> "%VD%\voice.log" echo EXITCODE=%ERRORLEVEL%
