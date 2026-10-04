@echo off
rem ASCII ONLY - see 09_VIDEO_PIPELINE.md section 6
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set OD=06_VIDEO\_demo24
> "%OD%\demo.log" echo START demo24
python "%OD%\build_demo24.py" >> "%OD%\demo.log" 2>&1
set DE=%ERRORLEVEL%
>> "%OD%\demo.log" echo EXITCODE=%DE%
exit /b %DE%
