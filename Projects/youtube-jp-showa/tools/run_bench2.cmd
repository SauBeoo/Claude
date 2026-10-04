@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-health
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set OUTDIR=E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_niche_scan
python tools\bench_channels.py UCD4uKCu-8GS8DUiI4xWy4gQ UCvhkvwhIsDx7ZSMD4eGdduA UColQysaUqsbkrrloI7LkoRQ UCTOmkzpqRoNJecKp0pV68Kw UChUfZ8t2AaPII7Z0zR6iz3A > "%OUTDIR%\bench_kenh2.log" 2>&1
echo EXITCODE=%ERRORLEVEL% >> "%OUTDIR%\bench_kenh2.log"
