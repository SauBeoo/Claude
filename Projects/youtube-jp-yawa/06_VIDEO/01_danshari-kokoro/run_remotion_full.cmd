@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set VD=E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro
python tools\kb_cells.py 01_danshari-kokoro > "%VD%\remotion_full.log" 2>&1
python tools\build_remotion_demo.py 01_danshari-kokoro --t0 0 --t1 1153.1 --name yawa-01-full >> "%VD%\remotion_full.log" 2>&1
set BE=%ERRORLEVEL%
>> "%VD%\remotion_full.log" echo BUILD_EXIT=%BE%
if not "%BE%"=="0" exit /b 1
cd /d E:\Claude\Projects\remotion-vox
python tools\render_chunks.py --project yawa-01-full --chunk 4000 --concurrency 2 --cache-mb 256 >> "%VD%\remotion_full.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\remotion_full.log" echo RENDER_EXIT=%RE%
if not "%RE%"=="0" exit /b 1
ffmpeg -hide_banner -nostats -y -i out\yawa-01-full.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 "%VD%\01_danshari-kokoro_remotion.mp4" >> "%VD%\remotion_full.log" 2>&1
>> "%VD%\remotion_full.log" echo EXITCODE=%ERRORLEVEL%
