@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\demo_voice
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
python run_demo.py > render.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> render.log
