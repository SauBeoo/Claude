@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\24_shien-kyufukin-midori-futo-9gatsu
set OUT=out\nenkin-24.mp4
set NORM=out\nenkin-24_norm.mp4

rem ---- 1/2 RENDER (call npx: npx la .CMD, thieu call thi cac dong sau bi bo) ----
>> "%VD%\render.log" echo === STAGE 1 RENDER ===
call npx remotion render VoxProject --props=projects/nenkin-24/project.json "%OUT%" >> "%VD%\render.log" 2>&1
set RE=%ERRORLEVEL%
>> "%VD%\render.log" echo RENDER_EXIT=%RE%
if not "%RE%"=="0" ( >> "%VD%\render.log" echo RENDER GAY - BO QUA KHAU SAU & exit /b 1 )

rem ---- 2/2 LOUDNORM -14 LUFS (chuoi VOICE_AF chep tu video_render.py) ----
>> "%VD%\render.log" echo === STAGE 2 LOUDNORM ===
ffmpeg -y -i "%OUT%" -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" "%NORM%" >> "%VD%\render.log" 2>&1
set LE=%ERRORLEVEL%
>> "%VD%\render.log" echo LOUDNORM_EXIT=%LE%
if not "%LE%"=="0" ( >> "%VD%\render.log" echo LOUDNORM GAY & exit /b 2 )

>> "%VD%\render.log" echo EXITCODE=0
