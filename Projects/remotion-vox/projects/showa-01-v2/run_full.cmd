@echo off
rem ASCII ONLY (render-background.md 2.6 mucA).
rem Full render of showa-01-v2, split into 8 chunks so a killed process only
rem costs one chunk (workspace rule: long ffmpeg/python runs get killed).
rem Re-running skips chunks that already exist -> resume for free.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=projects\showa-01-v2
set LOG=%VD%\full.log
set OD=out\full_v2

if not exist "%OD%" mkdir "%OD%"

call :seg 1 0 4155
if errorlevel 1 goto fail
call :seg 2 4156 8311
if errorlevel 1 goto fail
call :seg 3 8312 12467
if errorlevel 1 goto fail
call :seg 4 12468 16623
if errorlevel 1 goto fail
call :seg 5 16624 20779
if errorlevel 1 goto fail
call :seg 6 20780 24935
if errorlevel 1 goto fail
call :seg 7 24936 29091
if errorlevel 1 goto fail
call :seg 8 29092 33245
if errorlevel 1 goto fail

>> "%LOG%" echo == CONCAT ==
> "%OD%\list.txt" echo file 'v2_p1.mp4'
>> "%OD%\list.txt" echo file 'v2_p2.mp4'
>> "%OD%\list.txt" echo file 'v2_p3.mp4'
>> "%OD%\list.txt" echo file 'v2_p4.mp4'
>> "%OD%\list.txt" echo file 'v2_p5.mp4'
>> "%OD%\list.txt" echo file 'v2_p6.mp4'
>> "%OD%\list.txt" echo file 'v2_p7.mp4'
>> "%OD%\list.txt" echo file 'v2_p8.mp4'
ffmpeg -v error -y -f concat -safe 0 -i "%OD%\list.txt" -c copy "%OD%\_joined.mp4" >> "%LOG%" 2>&1
if errorlevel 1 goto fail

>> "%LOG%" echo == LOUDNORM -14 LUFS ==
ffmpeg -v error -y -i "%OD%\_joined.mp4" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=9 -c:a aac -b:a 192k "%OD%\01_kyushoku_v2.mp4" >> "%LOG%" 2>&1
if errorlevel 1 goto fail

>> "%LOG%" echo ALL DONE
>> "%LOG%" echo EXITCODE=0
exit /b 0

:seg
if exist "%OD%\v2_p%1.mp4" (
  >> "%LOG%" echo == SEG %1 da co, bo qua ==
  exit /b 0
)
>> "%LOG%" echo == SEG %1 frames %2-%3 ==
call npx remotion render VoxProject --props=projects/showa-01-v2/project.json --frames=%2-%3 "%OD%/v2_p%1.mp4" >> "%LOG%" 2>&1
set RC=%ERRORLEVEL%
>> "%LOG%" echo SEG%1_EXIT=%RC%
exit /b %RC%

:fail
>> "%LOG%" echo RENDER FAILED
>> "%LOG%" echo EXITCODE=1
exit /b 1
