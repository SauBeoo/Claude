@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

rem ASCII-ONLY file (render-background.md 2.6 item 1)
rem redirect placed BEFORE echo (render-background.md 2.6 item 3)

set V21=06_VIDEO\21_furo-no-kabi-modoru
set V22=06_VIDEO\22_furaipan-kuttsuku
if not exist "%V21%" mkdir "%V21%"
if not exist "%V22%" mkdir "%V22%"

python tools\voice_only.py 03_SCRIPTS\21_furo-no-kabi-modoru_TTS.md --channel co-dai > "%V21%\voice.log" 2>&1
set E21=%ERRORLEVEL%
>> "%V21%\voice.log" echo VOICE_EXIT=%E21%

python tools\voice_only.py 03_SCRIPTS\22_furaipan-kuttsuku_TTS.md --channel co-dai > "%V22%\voice.log" 2>&1
set E22=%ERRORLEVEL%
>> "%V22%\voice.log" echo VOICE_EXIT=%E22%

>> "%V21%\voice.log" echo ALL_DONE 21=%E21% 22=%E22%
exit /b 0
