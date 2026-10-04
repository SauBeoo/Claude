@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-chouhen
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set V=06_VIDEO\22_tanin-no-hanko
set BG=--bg-only %V%\bg_list.txt

python -u tools\scene_render.py 22_tanin-no-hanko --stage segs  %BG% > %V%\stage_segs.log 2>&1
echo STAGE_segs_EXITCODE=%errorlevel% >> %V%\stage_segs.log

python -u tools\scene_render.py 22_tanin-no-hanko --stage parts %BG% > %V%\stage_parts.log 2>&1
echo STAGE_parts_EXITCODE=%errorlevel% >> %V%\stage_parts.log

python -u tools\scene_render.py 22_tanin-no-hanko --stage final %BG% > %V%\stage_final.log 2>&1
echo STAGE_final_EXITCODE=%errorlevel% >> %V%\stage_final.log
