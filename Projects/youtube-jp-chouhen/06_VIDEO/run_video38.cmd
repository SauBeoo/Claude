@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
set SLUG=38_enpitsu-no-meibo
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\render.log" echo ==== STEP 1 SEGS (photo inorder, frame radio) ====
python tools\scene_render.py %SLUG% --stage segs --frame radio --motion photo --photo-dir "%VD%\img_seq" --photo-inorder >> "%VD%\render.log" 2>&1
set SE=%ERRORLEVEL%
>> "%VD%\render.log" echo SEGS_EXIT=%SE%
if not "%SE%"=="0" (
  >> "%VD%\render.log" echo SEGS FAILED - SKIP PARTS AND FINAL
  >> "%VD%\render.log" echo EXITCODE=%SE%
  exit /b %SE%
)

>> "%VD%\render.log" echo ==== STEP 2 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\render.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\render.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\render.log" echo PARTS FAILED - SKIP FINAL
  >> "%VD%\render.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\render.log" echo ==== STEP 3 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\render.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\render.log" echo FINAL_EXIT=%FE%
>> "%VD%\render.log" echo EXITCODE=%FE%
