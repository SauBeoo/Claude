@echo off
chcp 65001 >nul
cd /d "E:/Claude/Projects/youtube-jp-retrofuture/06_VIDEO/01_tou-no-fumoto/_render"

rem duong dan dung DAU GACH XUOI: \06 va \01 bi Python hieu la escape OCTAL khi sinh file
rem bang heredoc (render-background.md 2.6 muc 6). Moi thu muc cua kenh deu danh so
rem nen bay nay chac chan lap lai neu sinh .cmd bang heredoc.

rem step 1 - noi 40 clip, cat cung, copy stream (cung codec h264 1280x720 24fps)
ffmpeg -y -f concat -safe 0 -i list.txt -c copy full_hardcut.mp4 > build.log 2>&1
set E1=%ERRORLEVEL%
>> build.log echo STEP1_EXIT=%E1%
if not "%E1%"=="0" ( >> build.log echo STOP - concat that bai & exit /b 1 )

rem step 2 - ban re-encode deu fps, de doc nhip that
ffmpeg -y -f concat -safe 0 -i list.txt -vf "fps=24,format=yuv420p" -c:v libx264 -preset veryfast -crf 20 full_recode.mp4 >> build.log 2>&1
set E2=%ERRORLEVEL%
>> build.log echo STEP2_EXIT=%E2%

>> build.log echo EXITCODE=%E2%
