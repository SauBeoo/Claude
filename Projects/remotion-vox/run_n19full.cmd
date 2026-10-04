@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\19_kounenrei-koyou-keizoku-kyufu
set OUT=out\nenkin-19.mp4
set NORM=out\nenkin-19_norm.mp4

rem ---- 1/3 RENDER (call npx: npx la .CMD, thieu call thi cac dong sau bi bo) ----
>> "%VD%\render.log" echo === STAGE 1 RENDER ===
call npx remotion render VoxProject --props=projects/nenkin-19/project.json "%OUT%" >> "%VD%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\render.log" echo RENDER_EXIT=%RE%
if not "%RE%"=="0" ( >> "%VD%\render.log" echo RENDER GAY - BO QUA 2 KHAU SAU & exit /b 1 )

rem ---- 2/3 LOUDNORM -14 LUFS (chuoi VOICE_AF chep tu video_render.py) ----
>> "%VD%\render.log" echo === STAGE 2 LOUDNORM ===
ffmpeg -y -i "%OUT%" -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" "%NORM%" >> "%VD%\render.log" 2>&1
set LE=%ERRORLEVEL%
>> "%VD%\render.log" echo LOUDNORM_EXIT=%LE%
if not "%LE%"=="0" ( >> "%VD%\render.log" echo LOUDNORM GAY & exit /b 2 )

rem ---- 3/3 CTA overlay (mau cau nenkin da co san trong cta_inject.py) ----
>> "%VD%\render.log" echo === STAGE 3 CTA ===
python E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py "%NORM%" --srt "%VD%\subs.srt" --lang jp --in-place >> "%VD%\render.log" 2>&1
>> "%VD%\render.log" echo CTA_EXIT=%ERRORLEVEL%

>> "%VD%\render.log" echo EXITCODE=0
