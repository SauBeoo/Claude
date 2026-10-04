@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python tools\fetch_photos.py ..\youtube-jp-shokutaku\04_SCRIPTS\05_kyabetsu-tabeawase_SLIDES_video.json ..\youtube-jp-shokutaku\06_VIDEO\05_kyabetsu-tabeawase\slides_img_photo_v2 > ..\youtube-jp-shokutaku\06_VIDEO\_logs\fetch05.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> ..\youtube-jp-shokutaku\06_VIDEO\_logs\fetch05.log
