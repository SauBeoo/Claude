@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set OUTDIR=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_niche_scan
if not exist "%OUTDIR%" mkdir "%OUTDIR%"
python tools\scan_niche_now.py --days 90 --per 45 ^
  --queries E:\Claude\Projects\youtube-jp-showa\tools\queries_showa.json ^
  --out "%OUTDIR%" --tag scan_showa_90d > "%OUTDIR%\scan_90d.log" 2>&1
echo EXITCODE=%ERRORLEVEL% >> "%OUTDIR%\scan_90d.log"
