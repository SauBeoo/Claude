@echo off
rem ASCII ONLY - render-background.md 2.6 trap 1
setlocal
cd /d E:\Claude\Projects\remotion-vox
set P=projects\nenkin-22i2v\project.json
set O=out\s22chk
if not exist "%O%" mkdir "%O%"
rem 'call' is REQUIRED before npx
for %%F in (1560 3132 288) do (
  >> "%O%\still.log" echo --- frame %%F
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\c_%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo EXITCODE=%ERRORLEVEL%
endlocal
