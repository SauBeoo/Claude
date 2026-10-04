@echo off
chcp 65001 >nul
rem ASCII ONLY - see render-background.md 2.6 (1)
set SLUG=37_nanaketa-no-kioku
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
if not exist "%VD%" mkdir "%VD%"
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\voice.log" echo ==== STEP 1 AIVIS ENGINE ====
curl -s -m 3 http://127.0.0.1:10101/version >nul 2>&1
if errorlevel 1 (
  >> "%VD%\voice.log" echo starting AivisSpeech engine
  start "" /b /d "E:\AivisSpeech\AivisSpeech-Engine" run.exe
) else (
  >> "%VD%\voice.log" echo engine already up
)

set /a N=0
:WAITENG
curl -s -m 3 http://127.0.0.1:10101/version >nul 2>&1
if not errorlevel 1 goto ENGREADY
set /a N+=1
if %N% GEQ 60 (
  >> "%VD%\voice.log" echo AIVIS TIMEOUT after 180s
  >> "%VD%\voice.log" echo VOICE_EXIT=91
  exit /b 91
)
%SystemRoot%\System32\ping.exe -n 4 127.0.0.1 >nul
goto WAITENG
:ENGREADY
>> "%VD%\voice.log" echo engine READY

>> "%VD%\voice.log" echo ==== STEP 2 TTS PREFETCH 4 JOBS ====
python tools\tts_prefetch.py 03_SCRIPTS\%SLUG%_TTS.md --engine aivis --speaker morioki --speed 1.0 --jobs 4 >> "%VD%\voice.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\voice.log" echo PREFETCH_EXIT=%PE%

>> "%VD%\voice.log" echo ==== STEP 3 VOICE ONLY ====
python tools\ambient_render.py 03_SCRIPTS\%SLUG%_TTS.md --engine aivis --speaker morioki --speed 1.0 --voice-only >> "%VD%\voice.log" 2>&1
set VE=%ERRORLEVEL%
>> "%VD%\voice.log" echo VOICE_EXIT=%VE%
