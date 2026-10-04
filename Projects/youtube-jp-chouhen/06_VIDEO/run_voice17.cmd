@echo off
chcp 65001 >nul
rem ASCII ONLY - see render-background.md 2.6 (1)
set SLUG=17_sakura-no-kigata
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
if not exist "%VD%" mkdir "%VD%"
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\voice.log" echo ==== STEP 1 VOICEVOX ENGINE ====
curl -s -m 3 http://127.0.0.1:50021/version >nul 2>&1
if errorlevel 1 (
  >> "%VD%\voice.log" echo starting VOICEVOX engine
  start "" /b /d "E:\VOICEVOX\vv-engine" run.exe
) else (
  >> "%VD%\voice.log" echo engine already up
)

set /a N=0
:WAITENG
curl -s -m 3 http://127.0.0.1:50021/version >nul 2>&1
if not errorlevel 1 goto ENGREADY
set /a N+=1
if %N% GEQ 60 (
  >> "%VD%\voice.log" echo VOICEVOX TIMEOUT after 180s
  >> "%VD%\voice.log" echo VOICE_EXIT=91
  exit /b 91
)
%SystemRoot%\System32\ping.exe -n 4 127.0.0.1 >nul
goto WAITENG
:ENGREADY
>> "%VD%\voice.log" echo engine READY

>> "%VD%\voice.log" echo ==== STEP 2+3 PREFETCH THEN VOICE (via py wrapper, avoids cmd.exe mangling JP speaker name) ====
python tools\_run17_voice.py >> "%VD%\voice.log" 2>&1
set VE=%ERRORLEVEL%
>> "%VD%\voice.log" echo VOICE_EXIT=%VE%
