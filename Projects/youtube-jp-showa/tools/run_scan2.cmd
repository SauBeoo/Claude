@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set OUTDIR=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_niche_scan
python tools\scan_niche_now.py --days 90 --per 45 ^
  --queries E:\Claude\Projects\youtube-jp-showa\tools\queries_showa2.json ^
  --out "%OUTDIR%" --tag scan_showa2_90d > "%OUTDIR%\scan2_90d.log" 2>&1
echo EXITCODE=%ERRORLEVEL% >> "%OUTDIR%\scan2_90d.log"
