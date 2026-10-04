@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\19_kounenrei-koyou-keizoku-kyufu
set LOG=%VD%\fix.log
if exist "%LOG%" del "%LOG%"

rem Bang raw (out\nenkin-19.mp4) DA XAC MINH LA DUNG o 543/549/552s.
rem Dung lai _norm tu raw, roi thu cta_inject LAN 2 de xem loi co tai hien khong.
>> "%LOG%" echo === LOUDNORM LAI TU RAW ===
ffmpeg -y -i "out\nenkin-19.mp4" -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" "out\nenkin-19_nocta.mp4" >> "%LOG%" 2>&1
>> "%LOG%" echo LOUDNORM_EXIT=%ERRORLEVEL%

>> "%LOG%" echo === COPY DE THU CTA LAN 2 ===
copy /y "out\nenkin-19_nocta.mp4" "out\nenkin-19_ctatest.mp4" >> "%LOG%" 2>&1

>> "%LOG%" echo === CTA LAN 2 ===
python E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py "out\nenkin-19_ctatest.mp4" --srt "%VD%\subs.srt" --lang jp --in-place >> "%LOG%" 2>&1
>> "%LOG%" echo CTA2_EXIT=%ERRORLEVEL%
>> "%LOG%" echo EXITCODE=0
