@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
rem v2: 5 cue phu de bi wrap 4 dong (CTA de len card) - da tach dong trong _TTS.md
set SLUG=34_shinsatsu-no-kouden
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\fix.log" echo ==== STEP 1 AIVIS ENGINE ====
curl -s -m 3 http://127.0.0.1:10101/version >nul 2>&1
if errorlevel 1 (
  >> "%VD%\fix.log" echo starting AivisSpeech engine
  start "" /b /d "E:\AivisSpeech\AivisSpeech-Engine" run.exe
) else (
  >> "%VD%\fix.log" echo engine already up
)
set /a N=0
:WAITENG
curl -s -m 3 http://127.0.0.1:10101/version >nul 2>&1
if not errorlevel 1 goto ENGREADY
set /a N+=1
if %N% GEQ 60 (
  >> "%VD%\fix.log" echo AIVIS TIMEOUT
  >> "%VD%\fix.log" echo EXITCODE=91
  exit /b 91
)
%SystemRoot%\System32\ping.exe -n 4 127.0.0.1 >nul
goto WAITENG
:ENGREADY

>> "%VD%\fix.log" echo ==== STEP 2 PREFETCH (cache am, chi 8 dong moi) ====
python tools\tts_prefetch.py 03_SCRIPTS\%SLUG%_TTS.md --engine aivis --speaker morioki --speed 1.0 --jobs 4 >> "%VD%\fix.log" 2>&1
>> "%VD%\fix.log" echo PREFETCH_EXIT=%ERRORLEVEL%

>> "%VD%\fix.log" echo ==== STEP 3 VOICE ONLY ====
python tools\ambient_render.py 03_SCRIPTS\%SLUG%_TTS.md --engine aivis --speaker morioki --speed 1.0 --voice-only >> "%VD%\fix.log" 2>&1
set VE=%ERRORLEVEL%
>> "%VD%\fix.log" echo VOICE_EXIT=%VE%
if not "%VE%"=="0" (
  >> "%VD%\fix.log" echo VOICE GAY - BO QUA RENDER
  >> "%VD%\fix.log" echo EXITCODE=%VE%
  exit /b %VE%
)

>> "%VD%\fix.log" echo ==== STEP 4 SEGS (frame radio) ====
python tools\scene_render.py %SLUG% --stage segs --bg-only "%VD%\bg_list.txt" --frame radio >> "%VD%\fix.log" 2>&1
set SE=%ERRORLEVEL%
>> "%VD%\fix.log" echo SEGS_EXIT=%SE%
if not "%SE%"=="0" (
  >> "%VD%\fix.log" echo SEGS GAY - BO QUA PARTS
  >> "%VD%\fix.log" echo EXITCODE=%SE%
  exit /b %SE%
)

>> "%VD%\fix.log" echo ==== STEP 5 VERIFY MIN-GAP 4 ====
python tools\pick_bg20.py --slug %SLUG% --verify --min-gap 4 >> "%VD%\fix.log" 2>&1
>> "%VD%\fix.log" echo VERIFY_EXIT=%ERRORLEVEL%

>> "%VD%\fix.log" echo ==== STEP 6 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\fix.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\fix.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\fix.log" echo PARTS GAY - BO QUA FINAL
  >> "%VD%\fix.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\fix.log" echo ==== STEP 7 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\fix.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\fix.log" echo FINAL_EXIT=%FE%
>> "%VD%\fix.log" echo EXITCODE=%FE%
