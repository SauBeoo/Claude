@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
rem Wait signal = voice.wav EXISTS and SIZE STABLE.
rem Do NOT grep voice.log for VOICE_EXIT=0: log is append-only, a marker from a
rem PREVIOUS run stays there forever (exit 94 on 2026-08-13). Same family as 2.5:
rem asking "does it exist" instead of "is it from THIS run".
set SLUG=25_shinya-no-genkan
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\%SLUG%
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\render.log" echo ==== STEP 0 WAIT FOR voice.wav STABLE ====
set /a W=0
:WAITVOICE
if not exist "%VD%\voice.wav" goto SLEEPW
if not exist "%VD%\subs.srt" goto SLEEPW
set S1=0
set S2=0
for %%A in ("%VD%\voice.wav") do set S1=%%~zA
%SystemRoot%\System32\ping.exe -n 8 127.0.0.1 >nul
for %%A in ("%VD%\voice.wav") do set S2=%%~zA
if "%S1%"=="%S2%" goto VOICEOK
>> "%VD%\render.log" echo still growing %S1% -^> %S2%
goto WAITVOICE
:SLEEPW
set /a W+=1
if %W% GEQ 420 (
  >> "%VD%\render.log" echo WAIT TIMEOUT 70min
  >> "%VD%\render.log" echo EXITCODE=93
  exit /b 93
)
%SystemRoot%\System32\ping.exe -n 11 127.0.0.1 >nul
goto WAITVOICE
:VOICEOK
>> "%VD%\render.log" echo voice.wav READY size=%S2%

>> "%VD%\render.log" echo ==== STEP 1 SEGS ====
python tools\scene_render.py %SLUG% --stage segs >> "%VD%\render.log" 2>&1
set SE=%ERRORLEVEL%
>> "%VD%\render.log" echo SEGS_EXIT=%SE%
if not "%SE%"=="0" (
  >> "%VD%\render.log" echo SEGS GAY - BO QUA PARTS VA FINAL
  >> "%VD%\render.log" echo EXITCODE=%SE%
  exit /b %SE%
)

>> "%VD%\render.log" echo ==== STEP 2 PARTS ====
python tools\scene_render.py %SLUG% --stage parts >> "%VD%\render.log" 2>&1
set PE=%ERRORLEVEL%
>> "%VD%\render.log" echo PARTS_EXIT=%PE%
if not "%PE%"=="0" (
  >> "%VD%\render.log" echo PARTS GAY - BO QUA FINAL
  >> "%VD%\render.log" echo EXITCODE=%PE%
  exit /b %PE%
)

>> "%VD%\render.log" echo ==== STEP 3 FINAL ====
python tools\scene_render.py %SLUG% --stage final >> "%VD%\render.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\render.log" echo FINAL_EXIT=%FE%
>> "%VD%\render.log" echo EXITCODE=%FE%
