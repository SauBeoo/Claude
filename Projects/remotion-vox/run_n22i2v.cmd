@echo off
rem ASCII ONLY - render-background.md 2.6 trap 1 (cmd.exe reads OEM codepage first)
rem 'call' is REQUIRED before npx - npx is a .CMD; without call the rest of the file is skipped
setlocal
cd /d E:\Claude\Projects\remotion-vox
set O=out\n22i2v
if not exist "%O%" mkdir "%O%"
>> "%O%\render.log" echo === START %DATE% %TIME%
call npx remotion render VoxProject --props=projects\nenkin-22i2v\project.json --concurrency=4 "%O%\demo.mp4" >> "%O%\render.log" 2>&1
set RC=%ERRORLEVEL%
>> "%O%\render.log" echo EXITCODE=%RC%
endlocal
