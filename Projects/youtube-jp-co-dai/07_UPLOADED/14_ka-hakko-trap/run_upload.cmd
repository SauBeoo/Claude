@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python E:\Claude\Projects\youtube-jp-chouhen\tools\upload_api.py 14_ka-hakko-trap --channel co-dai --slot "2026-07-31 11:00" > 06_VIDEO\14_ka-hakko-trap\upload.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> 06_VIDEO\14_ka-hakko-trap\upload.log
