@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set VD=E:\Claude\Projects\youtube-jp-shokutaku\06_VIDEO\21_mochimugi-choukatsu

python tools\render_chunks.py --project 21_mochimugi-choukatsu --chunk 5000 --concurrency 2 --cache-mb 512 > "%VD%\render.log" 2>&1
set RC=%ERRORLEVEL%
echo RENDER_EXIT=%RC% >> "%VD%\render.log"
if not "%RC%"=="0" (
  echo RENDER GAY - BO QUA DELIVER >> "%VD%\render.log"
  exit /b 1
)

python tools\deliver.py --project 21_mochimugi-choukatsu --channel shokutaku --stem 21_mochimugi-choukatsu --mp4 out\21_mochimugi-choukatsu.mp4 >> "%VD%\render.log" 2>&1
echo DELIVER_EXIT=%ERRORLEVEL% >> "%VD%\render.log"
