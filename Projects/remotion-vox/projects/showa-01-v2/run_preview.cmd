@echo off
rem ASCII ONLY (render-background.md 2.6 mucA). Preview of the rebuilt v2:
rem new voice (gap 0.35) + 26 archival inserts + 4 nostalgia sounds.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=projects\showa-01-v2
set LOG=%VD%\preview.log
if exist "%LOG%" del "%LOG%"

rem opening: kids singing + entry-0 footage + train kids
call :seg 1 0 500
if errorlevel 1 goto fail
rem lunch chime (end of 4th period)
call :seg 2 3698 4065
if errorlevel 1 goto fail
rem PA chime (school lunch broadcast)
call :seg 3 14406 14611
if errorlevel 1 goto fail
rem rice planting - gohan no kyushoku, showa 51
call :seg 4 18873 19207
if errorlevel 1 goto fail
rem tableware shop - sakiware spoon
call :seg 5 25226 25509
if errorlevel 1 goto fail
rem distant chime at the end
call :seg 6 31315 31686
if errorlevel 1 goto fail

>> "%LOG%" echo == CONCAT ==
> out\_v2_list.txt echo file 'showa01v2_p1.mp4'
>> out\_v2_list.txt echo file 'showa01v2_p2.mp4'
>> out\_v2_list.txt echo file 'showa01v2_p3.mp4'
>> out\_v2_list.txt echo file 'showa01v2_p4.mp4'
>> out\_v2_list.txt echo file 'showa01v2_p5.mp4'
>> out\_v2_list.txt echo file 'showa01v2_p6.mp4'
ffmpeg -v error -y -f concat -safe 0 -i out\_v2_list.txt -c copy out\showa01v2_PREVIEW.mp4 >> "%LOG%" 2>&1
>> "%LOG%" echo EXITCODE=%ERRORLEVEL%
exit /b 0

:seg
>> "%LOG%" echo == SEG %1 frames %2-%3 ==
call npx remotion render VoxProject --props=projects/showa-01-v2/project.json --frames=%2-%3 out/showa01v2_p%1.mp4 >> "%LOG%" 2>&1
set RC=%ERRORLEVEL%
>> "%LOG%" echo SEG%1_EXIT=%RC%
exit /b %RC%

:fail
>> "%LOG%" echo RENDER FAILED
>> "%LOG%" echo EXITCODE=1
exit /b 1
