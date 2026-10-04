@echo off
rem ASCII ONLY - render-background.md 2.6 trap (1)
setlocal
cd /d E:\Claude\Projects\remotion-vox
set P=projects\nenkin-22full\project.json
set O=out\s22full
if not exist "%O%" mkdir "%O%"
rem 'call' is REQUIRED before npx
for %%F in (60 300 1920 2610 3540 5760 7080 8500 10200 12000 14400 16200 18000 19800) do (
  >> "%O%\still.log" echo --- frame %%F
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\f_%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo EXITCODE=%ERRORLEVEL%
endlocal
