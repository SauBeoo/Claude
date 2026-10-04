@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-shokutaku
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
if not exist "06_VIDEO\21_mochimugi-choukatsu" mkdir "06_VIDEO\21_mochimugi-choukatsu"
python tools\make_timeline.py 21_mochimugi-choukatsu > "06_VIDEO\21_mochimugi-choukatsu\voice.log" 2>&1
echo VOICE_EXIT=%ERRORLEVEL% >> "06_VIDEO\21_mochimugi-choukatsu\voice.log"
