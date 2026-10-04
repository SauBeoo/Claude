@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python tools\render_chunks28.py > "E:\Claude\Projects\remotion-vox\out\c28chunks.log" 2>&1
>> "E:\Claude\Projects\remotion-vox\out\c28chunks.log" echo EXITCODE=%ERRORLEVEL%
