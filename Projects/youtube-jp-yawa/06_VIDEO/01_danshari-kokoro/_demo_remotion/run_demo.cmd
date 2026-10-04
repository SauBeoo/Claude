@echo off
cd /d E:\Claude\Projects\remotion-vox
set OUT=E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\_demo_remotion
call npx remotion render VoxProject out\yawa-01-demo_raw.mp4 --props=projects/yawa-01-demo/project.json --concurrency=2 --offthreadvideo-cache-size-in-bytes=268435456 --media-cache-size-in-bytes=268435456 --log=error > "%OUT%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%OUT%\render.log" echo RENDER_EXIT=%RE%
if not "%RE%"=="0" exit /b 1
ffmpeg -hide_banner -nostats -y -i out\yawa-01-demo_raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 "%OUT%\demo_remotion_FULL.mp4" >> "%OUT%\render.log" 2>&1
>> "%OUT%\render.log" echo NORM_EXIT=%ERRORLEVEL%
ffmpeg -hide_banner -nostats -y -ss 468.98 -i E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\01_danshari-kokoro.mp4 -t 124.27 -c:v libx264 -crf 18 -preset veryfast -c:a aac -b:a 192k "%OUT%\demo_current.mp4" >> "%OUT%\render.log" 2>&1
>> "%OUT%\render.log" echo EXITCODE=%ERRORLEVEL%
