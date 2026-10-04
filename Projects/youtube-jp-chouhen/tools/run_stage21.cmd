@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-chouhen
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python -u tools\scene_render.py 21_hachinen-no-yachin --stage %1 %2 %3 %4 %5 > 06_VIDEO\21_hachinen-no-yachin\stage_%1.log 2>&1
echo STAGE_%1_EXITCODE=%errorlevel% >> 06_VIDEO\21_hachinen-no-yachin\stage_%1.log
