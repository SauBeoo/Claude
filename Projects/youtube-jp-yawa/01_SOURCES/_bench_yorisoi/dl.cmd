@echo off
cd /d E:\Claude\Projects\youtube-jp-yawa\01_SOURCES\_bench_yorisoi
set PYTHONIOENCODING=utf-8
python -m yt_dlp --js-runtimes node -f "bv*[height<=480]+ba/b[height<=480]" --merge-output-format mp4 --write-auto-subs --write-subs --sub-langs ja --sub-format vtt -o "%%(id)s.%%(ext)s" X5HvXr3ICG4 jOv7SmTSPLU bmvyQKYdxUg > dl.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> dl.log
