@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
set SLUG=17_sakura-no-kigata
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

if not exist "%VD%\voice.wav" (
  >> "%VD%\render.log" echo NO voice.wav - run_voice17.cmd chua xong hoac loi
  >> "%VD%\render.log" echo EXITCODE=90
  exit /b 90
)

>> "%VD%\render.log" echo ==== STEP 1 PICK BG20 ====
python tools\pick_bg20.py --slug %SLUG% -n 20 --per-theme 2 >> "%VD%\render.log" 2>&1
set BE=%ERRORLEVEL%
>> "%VD%\render.log" echo PICKBG_EXIT=%BE%
if not "%BE%"=="0" (
  >> "%VD%\render.log" echo PICKBG FAILED - STOP
  >> "%VD%\render.log" echo EXITCODE=%BE%
  exit /b %BE%
)

>> "%VD%\render.log" echo ==== STEP 2 CHECK BG LUM ====
python tools\check_bg_lum.py %SLUG% --bg-only "%VD%\bg_list.txt" >> "%VD%\render.log" 2>&1
set LE=%ERRORLEVEL%
>> "%VD%\render.log" echo LUM_EXIT=%LE%

>> "%VD%\render.log" echo ==== STEP 3 SEGS (frame radio) ====
python tools\scene_render.py %SLUG% --stage segs --frame radio --bg-only "%VD%\bg_list.txt" >> "%VD%\render.log" 2>&1
set SE=%ERRORLEVEL%
>> "%VD%\render.log" echo SEGS_EXIT=%SE%
if not "%SE%"=="0" (
  >> "%VD%\render.log" echo SEGS FAILED - SKIP PARTS AND FINAL
  >> "%VD%\render.log" echo EXITCODE=%SE%
  exit /b %SE%
)

>> "%VD%\render.log" echo ==== STEP 4 VERIFY BG GAP ====
python tools\pick_bg20.py --slug %SLUG% --verify --min-gap 4 >> "%VD%\render.log" 2>&1
set VFE=%ERRORLEVEL%
>> "%VD%\render.log" echo VERIFY_EXIT=%VFE%

>> "%VD%\render.log" echo ==== STEP 5 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\render.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\render.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\render.log" echo PARTS FAILED - SKIP FINAL
  >> "%VD%\render.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\render.log" echo ==== STEP 6 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\render.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\render.log" echo FINAL_EXIT=%FE%
>> "%VD%\render.log" echo EXITCODE=%FE%
