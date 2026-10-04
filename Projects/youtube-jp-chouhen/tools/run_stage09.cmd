@echo off
cd /d E:\Claude\Projects\youtube-jp-chouhen
python -u tools\scene_render.py 09_aikagi-mudan-doukyo --stage %1 > 06_VIDEO\stage09_%1.log 2>&1
echo STAGE_%1_DONE_EXIT=%errorlevel% >> 06_VIDEO\stage09_%1.log
