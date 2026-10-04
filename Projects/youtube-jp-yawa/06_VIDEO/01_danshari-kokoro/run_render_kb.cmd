@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set VD=06_VIDEO\01_danshari-kokoro
python tools\kb_cells.py 01_danshari-kokoro > "%VD%\kb.log" 2>&1
set KE=%ERRORLEVEL%
>> "%VD%\kb.log" echo KB_EXIT=%KE%
if not "%KE%"=="0" ( >> "%VD%\render_kb.log" echo KB GAY - BO QUA RENDER & exit /b 1 )
if exist "%VD%\01_danshari-kokoro.mp4" move /y "%VD%\01_danshari-kokoro.mp4" "%VD%\01_danshari-kokoro_v1_narrator.mp4"
if exist "%VD%\slides" move /y "%VD%\slides" "%VD%\_slides_v1_static"
python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\01_danshari-kokoro_TTS.md --channel yawa --reuse > "%VD%\render_kb.log" 2>&1
>> "%VD%\render_kb.log" echo EXITCODE=%ERRORLEVEL%
