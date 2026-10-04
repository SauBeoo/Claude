@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set D=E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\14_ka-hakko-trap
python E:\Claude\Projects\youtube-jp-health\tools\video_render.py ^
  03_SCRIPTS\14_ka-hakko-trap_TTS.md ^
  --channel co-dai ^
  --slides E:\Claude\Projects\youtube-jp-co-dai\03_SCRIPTS\14_ka-hakko-trap_SLIDES.json ^
  --img-dir %D%\slides_img ^
  --clips-dir %D%\clips ^
  --bgm-gain -40 --reuse ^
  > "%D%\render.log" 2>&1
echo EXITCODE=%ERRORLEVEL% >> "%D%\render.log"
