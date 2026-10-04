@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-teinengo\06_VIDEO\01_teinengo-kurashi-7chigai\demo
set LOG=%VD%\render.log
call npx remotion render VoxProject --public-dir=public_tei out\teinengo\demo_sono1_raw.mp4 --props=projects/teinengo-01-demo/project.json --concurrency=2 --offthreadvideo-cache-size-in-bytes=268435456 --media-cache-size-in-bytes=268435456 > "%LOG%" 2>&1
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done
ffmpeg -hide_banner -nostats -y -i out\teinengo\demo_sono1_raw.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy -c:a aac -b:a 192k "%VD%\demo_sono1.mp4" >> "%LOG%" 2>&1
set RC=%ERRORLEVEL%
:done
>> "%LOG%" echo EXITCODE=%RC%
