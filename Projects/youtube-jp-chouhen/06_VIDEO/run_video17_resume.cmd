@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
rem Resume-only: STEP1-4 (bg pick/lum/segs/verify) da xong, KHONG chay lai de tranh
rem lam _render_plan.json moi hon cac part da render (kich hoat "dung lai" oan).
set SLUG=17_sakura-no-kigata
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

if not exist "%VD%\_render_plan.json" (
  >> "%VD%\render.log" echo NO _render_plan.json - chua chay xong STEP1-4, dung file run_video17.cmd goc
  >> "%VD%\render.log" echo EXITCODE=90
  exit /b 90
)

>> "%VD%\render.log" echo ==== RESUME STEP 5 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\render.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\render.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\render.log" echo PARTS FAILED - SKIP FINAL
  >> "%VD%\render.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\render.log" echo ==== RESUME STEP 6 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\render.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\render.log" echo FINAL_EXIT=%FE%
>> "%VD%\render.log" echo EXITCODE=%FE%
