@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa\01_SOURCES\_hot_2026-09-29
set PYTHONIOENCODING=utf-8
python -m yt_dlp --js-runtimes node --skip-download --write-auto-subs --write-subs --sub-langs ja --sub-format vtt -o "%%(id)s.%%(ext)s" J2WiiKe2VY4 AQcPSZ8Em_4 nqMXJcCF_4I PO5fcKbaHTc vnQNrPhgadQ 4jENiPcvG4w > dl.log 2>&1
python -m yt_dlp --js-runtimes node -f "bv*[height<=360]+ba/b[height<=360]" --merge-output-format mp4 -o "%%(id)s.%%(ext)s" J2WiiKe2VY4 PO5fcKbaHTc vnQNrPhgadQ >> dl.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> dl.log
