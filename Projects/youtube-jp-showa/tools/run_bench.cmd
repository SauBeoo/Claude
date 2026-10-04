@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set OUTDIR=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_niche_scan
python tools\bench_channels.py UCYZa9C1bXs-mKIMAim9VOmQ UC7e-Sbi0tV4KXkMmjXB21wA UCvkyjgcOm4n5pj0ahT8JxpA UC5_MtTXJKSjHIDDv0WQGNIw UC4SmNbFH-buA6ShPOJ2G0yQ UCYJpCZrVno6lhctC8-e1RLw UCyNCYZih1CwKKsg2R4NTLCQ UCv3M7_UqcNhgYMDFfYFToUQ --n 20 > "%OUTDIR%\bench_kenh.log" 2>&1
echo EXITCODE=%ERRORLEVEL% >> "%OUTDIR%\bench_kenh.log"
