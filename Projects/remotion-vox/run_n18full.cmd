@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem 3 steps, each gated on the previous exit code (render-background.md 1.6):
rem   1. remotion render        -> out\nenkin-18.mp4
rem   2. loudnorm -14 LUFS      -> out\nenkin-18_norm.mp4  (same chain as video_render.py VOICE_AF)
rem   3. cta_inject in-place    -> overlay at "kokode hitotsu dake onegai"
rem NOTE the CALL before npx (npx is npx.CMD -- 2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set LOG=out\n18full.log
set SRT=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\18_nenkin-60sai-kuriage-tsuki4man3sen\subs.srt

call npx remotion render VoxProject --props=projects/nenkin-18/project.json out/nenkin-18.mp4 > "%LOG%" 2>&1
set RE=%ERRORLEVEL%
>> "%LOG%" echo RENDER_EXIT=%RE%
if not "%RE%"=="0" (
  >> "%LOG%" echo RENDER FAILED - skip loudnorm and cta
  >> "%LOG%" echo EXITCODE=%RE%
  exit /b %RE%
)

ffmpeg -y -i out\nenkin-18.mp4 -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" -c:a aac -b:a 192k out\nenkin-18_norm.mp4 >> "%LOG%" 2>&1
set LE=%ERRORLEVEL%
>> "%LOG%" echo LOUDNORM_EXIT=%LE%
if not "%LE%"=="0" (
  >> "%LOG%" echo LOUDNORM FAILED - skip cta
  >> "%LOG%" echo EXITCODE=%LE%
  exit /b %LE%
)

python E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py out\nenkin-18_norm.mp4 --srt "%SRT%" --lang jp --in-place >> "%LOG%" 2>&1
set CE=%ERRORLEVEL%
>> "%LOG%" echo CTA_EXIT=%CE%
>> "%LOG%" echo EXITCODE=%CE%
exit /b %CE%
