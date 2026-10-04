@echo off
chcp 65001 >nul
rem ASCII ONLY - render-background.md 2.6 (1)
set PROJ=E:\Claude\Projects\youtube-jp-chouhen
set VD=%PROJ%\06_VIDEO\25_shinya-no-genkan
if not exist "%VD%" mkdir "%VD%"
cd /d %PROJ%
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

>> "%VD%\fetch.log" echo ==== FETCH BG CLIPS for 25_shinya-no-genkan ====
python tools\fetch_bg.py --per-query 8 "japanese house entrance night" "shoes on doorstep" "shoe rack hallway" "door lock cylinder closeup" "locksmith working door" "gate lamp night" "doorbell intercom light" "hospital corridor night" "dried persimmon" "old tin box lid" "aged envelope letter" "official document stamp" "tatami room dim light" "shinkansen window scenery" "washing machine laundry night" "cutting radish kitchen" "handwriting notebook pen" "post office counter" "quiet residential street night japan" "kettle steam kitchen night" "wooden stairs indoor" "futon bedding room" "persimmon tree autumn" "elderly man hands sitting" "kitchen sink water night" "notice board neighborhood" >> "%VD%\fetch.log" 2>&1
set FE=%ERRORLEVEL%
>> "%VD%\fetch.log" echo FETCH_EXIT=%FE%
