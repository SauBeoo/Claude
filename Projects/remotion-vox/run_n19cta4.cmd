@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\19_kounenrei-koyou-keizoku-kyufu
set CH=out\n19parts
set LOG=%VD%\cta4.log
if exist "%LOG%" del "%LOG%"

rem Gia thuyet: cta_inject hong vi file DA QUA concat -c copy.
rem Phep thu: chay no len DUNG khuc p4 (ban render mot-mach, cung cau truc voi video 18).
rem p4 = frame 13920..17399 = 464.00s..579.97s ; CTA tuyet doi 541.49s -> 77.49s trong p4.
>> "%LOG%" echo === CTA LEN CHUNK p4 ===
copy /y "%CH%\p4.mp4" "%CH%\p4_cta.mp4" >> "%LOG%" 2>&1
python E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py "%CH%\p4_cta.mp4" --srt "%CH%\p4.srt" --lang jp --in-place >> "%LOG%" 2>&1
>> "%LOG%" echo CTA4_EXIT=%ERRORLEVEL%
