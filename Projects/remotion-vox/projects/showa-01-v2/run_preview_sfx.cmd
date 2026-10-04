@echo off
rem ASCII ONLY (render-background.md 2.6 mucA). Preview of the 4 SFX moments:
rem kids song (opening) / lunch chime / PA chime / distant chime at the end.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=projects\showa-01-v2
set LOG=%VD%\preview_sfx.log
if exist "%LOG%" del "%LOG%"

call :seg 1 0 465
if errorlevel 1 goto fail
call :seg 2 3880 4257
if errorlevel 1 goto fail
call :seg 3 15127 15342
if errorlevel 1 goto fail
call :seg 4 32750 33131
if errorlevel 1 goto fail

>> "%LOG%" echo == CONCAT ==
> out\_sfx_list.txt echo file 'sfx_p1.mp4'
>> out\_sfx_list.txt echo file 'sfx_p2.mp4'
>> out\_sfx_list.txt echo file 'sfx_p3.mp4'
>> out\_sfx_list.txt echo file 'sfx_p4.mp4'
ffmpeg -v error -y -f concat -safe 0 -i out\_sfx_list.txt -c copy out\showa01v2_SFX_PREVIEW.mp4 >> "%LOG%" 2>&1
>> "%LOG%" echo EXITCODE=%ERRORLEVEL%
exit /b 0

:seg
>> "%LOG%" echo == SEG %1 frames %2-%3 ==
call npx remotion render VoxProject --props=projects/showa-01-v2/project.json --frames=%2-%3 out/sfx_p%1.mp4 >> "%LOG%" 2>&1
set RC=%ERRORLEVEL%
>> "%LOG%" echo SEG%1_EXIT=%RC%
exit /b %RC%

:fail
>> "%LOG%" echo RENDER FAILED
>> "%LOG%" echo EXITCODE=1
exit /b 1
