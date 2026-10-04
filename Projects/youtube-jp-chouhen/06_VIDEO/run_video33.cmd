@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
rem Re-render with --frame radio (missed on first pass, user caught it).
set SLUG=33_bunke-no-asa
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\render2.log" echo ==== STEP 1 SEGS (frame radio) ====
python tools\scene_render.py %SLUG% --stage segs --bg-only "%VD%\bg_list.txt" --frame radio >> "%VD%\render2.log" 2>&1
set SE=%ERRORLEVEL%
>> "%VD%\render2.log" echo SEGS_EXIT=%SE%
if not "%SE%"=="0" (
  >> "%VD%\render2.log" echo SEGS FAILED - SKIP PARTS AND FINAL
  >> "%VD%\render2.log" echo EXITCODE=%SE%
  exit /b %SE%
)

>> "%VD%\render2.log" echo ==== STEP 2 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\render2.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\render2.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\render2.log" echo PARTS FAILED - SKIP FINAL
  >> "%VD%\render2.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\render2.log" echo ==== STEP 3 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\render2.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\render2.log" echo FINAL_EXIT=%FE%
>> "%VD%\render2.log" echo EXITCODE=%FE%
