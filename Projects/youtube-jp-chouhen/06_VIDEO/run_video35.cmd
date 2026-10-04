@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
set SLUG=35_taishonin-no-hizuke
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

rem STEP 0 - wait for voice.wav to exist AND stop growing (render-background.md 2.6 (5))
set /a W=0
:WAITVOICE
set /a W+=1
if %W% GEQ 400 (
  >> "%VD%\render.log" echo WAIT VOICE TIMEOUT
  >> "%VD%\render.log" echo EXITCODE=93
  exit /b 93
)
if not exist "%VD%\voice.wav" goto SLEEPW
if not exist "%VD%\subs.srt"  goto SLEEPW
for %%A in ("%VD%\voice.wav") do set S1=%%~zA
%SystemRoot%\System32\ping.exe -n 9 127.0.0.1 >nul
for %%A in ("%VD%\voice.wav") do set S2=%%~zA
if "%S1%"=="%S2%" goto VOICEOK
goto WAITVOICE
:SLEEPW
%SystemRoot%\System32\ping.exe -n 11 127.0.0.1 >nul
goto WAITVOICE
:VOICEOK
>> "%VD%\render.log" echo ==== VOICE READY size=%S2% ====

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
>> "%VD%\render.log" echo LUM_EXIT=%ERRORLEVEL%

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
>> "%VD%\render.log" echo VERIFY_EXIT=%ERRORLEVEL%

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
