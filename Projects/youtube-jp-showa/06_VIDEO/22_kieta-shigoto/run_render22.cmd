@echo off
chcp 65001 >nul
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set STEM=22_kieta-shigoto
set VD=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\%STEM%
rem v22: cells -> grade -> render (voice reused). Sound mix runs after, separately.
cd /d E:\Claude\Projects\youtube-jp-showa
python tools\make_cells_22.py --jobs 2 > "%VD%\cells.log" 2>&1
set E2=%ERRORLEVEL%
>> "%VD%\cells.log" echo STEP_EXIT=%E2%
if not "%E2%"=="0" goto FAIL
python tools\grade_cells.py %STEM% --jobs 2 > "%VD%\grade.log" 2>&1
set E3=%ERRORLEVEL%
>> "%VD%\grade.log" echo STEP_EXIT=%E3%
if not "%E3%"=="0" goto FAIL
if exist "%VD%\slides" rmdir /s /q "%VD%\slides"
cd /d E:\Claude\Projects\youtube-jp-health
python tools\video_render.py "E:\Claude\Projects\youtube-jp-showa\03_SCRIPTS\%STEM%_TTS.md" --channel showa-b --reuse --bgm "E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_bgm\At Rest.mp3" --bgm-gain -34 > "%VD%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\render.log" echo EXITCODE=%RE%
exit /b %RE%
:FAIL
>> "%VD%\render.log" echo PRE-STEP FAILED - SKIP RENDER
exit /b 1
