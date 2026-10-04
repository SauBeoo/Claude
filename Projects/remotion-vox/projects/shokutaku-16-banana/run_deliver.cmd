@echo off
chcp 65001 >nul
rem ASCII-ONLY file (render-background.md 2.6 muc 1)
rem Log goes OUTSIDE the video folder: deliver.py writes into 06_VIDEO/<stem>/,
rem and upload-schedule.md warns a log living inside a folder the tool touches
rem can break the move/copy step.
cd /d E:\Claude\Projects\remotion-vox
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set LOG=E:\Claude\Projects\remotion-vox\out\deliver_16.log
python tools\deliver.py --project shokutaku-16-banana --channel shokutaku --stem 16_banana-yoru-toire > "%LOG%" 2>&1
>> "%LOG%" echo EXITCODE=%ERRORLEVEL%
