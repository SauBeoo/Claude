@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health\tools
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set S=E:\Claude\Projects\youtube-jp-co-dai\03_SCRIPTS\14_ka-hakko-trap_SLIDES.json
set D=E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\14_ka-hakko-trap
echo ===== FETCH PHOTOS ===== > "%D%\fetch.log"
python fetch_photos.py "%S%" "%D%\slides_img" >> "%D%\fetch.log" 2>&1
echo PHOTOS_EXIT=%ERRORLEVEL% >> "%D%\fetch.log"
echo ===== FETCH CLIPS ===== >> "%D%\fetch.log"
python fetch_clips.py "%S%" "%D%\clips" >> "%D%\fetch.log" 2>&1
echo CLIPS_EXIT=%ERRORLEVEL% >> "%D%\fetch.log"
echo EXITCODE=0 >> "%D%\fetch.log"
