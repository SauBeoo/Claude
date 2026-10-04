@echo off
chcp 65001 >nul
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set STEM=19_kaimono-joushiki
set VD=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\%STEM%
set ONLY=20,33,62,102,131,132,133,134,135,156
rem v19 era-fix: 10 cells changed (western stamps / 90s CRT / shutter). SLIDES already written and diffed.
cd /d E:\Claude\Projects\youtube-jp-showa
python tools\make_cells_19.py --jobs 2 --only %ONLY% > "%VD%\cells_era.log" 2>&1
set E2=%ERRORLEVEL%
>> "%VD%\cells_era.log" echo STEP_EXIT=%E2%
if not "%E2%"=="0" goto FAIL
for %%N in (20 33 62 102 131 132 133 134 135 156) do if exist "%VD%\clips_ungraded\clip_%%N.mp4" ren "%VD%\clips_ungraded\clip_%%N.mp4" clip_%%N_prevera.mp4
python tools\grade_cells.py %STEM% --jobs 2 --only %ONLY% > "%VD%\grade_era.log" 2>&1
set E3=%ERRORLEVEL%
>> "%VD%\grade_era.log" echo STEP_EXIT=%E3%
if not "%E3%"=="0" goto FAIL
if exist "%VD%\slides" rmdir /s /q "%VD%\slides"
if exist "%VD%\%STEM%_nosfx.mp4" ren "%VD%\%STEM%_nosfx.mp4" %STEM%_nosfx_prev%RANDOM%.mp4
cd /d E:\Claude\Projects\youtube-jp-health
python tools\video_render.py "E:\Claude\Projects\youtube-jp-showa\03_SCRIPTS\%STEM%_TTS.md" --channel showa-b --reuse --bgm "E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_bgm\Canon in D Major.mp3" --bgm-gain -34 > "%VD%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\render.log" echo EXITCODE=%RE%
if not "%RE%"=="0" exit /b %RE%
cd /d E:\Claude\Projects\youtube-jp-showa
python tools\probe_native_19.py > "%VD%\mix.log" 2>&1
python tools\mix_sound_19.py >> "%VD%\mix.log" 2>&1
set E5=%ERRORLEVEL%
>> "%VD%\mix.log" echo MIX_EXIT=%E5%
exit /b %E5%
:FAIL
>> "%VD%\render.log" echo PRE-STEP FAILED - SKIP RENDER
exit /b 1
