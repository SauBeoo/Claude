@echo off
chcp 65001 >nul
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set STEM=22_kieta-shigoto
set VD=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\%STEM%
set ONLY=82,83,108
rem v22 round 2: +conductor_smile, new operators_reassigned. Other 149 cells renamed, not rebuilt.
cd /d E:\Claude\Projects\youtube-jp-showa
python tools\make_cells_22.py --jobs 2 --only %ONLY% > "%VD%\cells_b.log" 2>&1
set E2=%ERRORLEVEL%
>> "%VD%\cells_b.log" echo STEP_EXIT=%E2%
if not "%E2%"=="0" goto FAIL
python tools\grade_cells.py %STEM% --jobs 2 --only %ONLY% > "%VD%\grade_b.log" 2>&1
set E3=%ERRORLEVEL%
>> "%VD%\grade_b.log" echo STEP_EXIT=%E3%
if not "%E3%"=="0" goto FAIL
if exist "%VD%\slides" rmdir /s /q "%VD%\slides"
cd /d E:\Claude\Projects\youtube-jp-health
python tools\video_render.py "E:\Claude\Projects\youtube-jp-showa\03_SCRIPTS\%STEM%_TTS.md" --channel showa-b --reuse --bgm "E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_bgm\At Rest.mp3" --bgm-gain -34 > "%VD%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\render.log" echo EXITCODE=%RE%
if not "%RE%"=="0" exit /b %RE%
cd /d E:\Claude\Projects\youtube-jp-showa
python tools\probe_native_22.py > "%VD%\mix.log" 2>&1
python tools\mix_sound_22.py >> "%VD%\mix.log" 2>&1
set E5=%ERRORLEVEL%
>> "%VD%\mix.log" echo MIX_EXIT=%E5%
exit /b %E5%
:FAIL
>> "%VD%\render.log" echo PRE-STEP FAILED - SKIP RENDER
exit /b 1
