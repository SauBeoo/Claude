@echo off
rem ASCII ONLY - see render-background.md 2.6 trap 1 (cmd.exe reads OEM codepage first)
setlocal
cd /d E:\Claude\Projects\remotion-vox
set P=projects\nenkin-22i2v\project.json
set O=out\s22i
if not exist "%O%" mkdir "%O%"
rem 'call' is REQUIRED before npx - npx is a .CMD, without call the rest of this file is skipped
for %%F in (288 881 1351 1560 2052 2340 2486 2962 3134) do (
  >> "%O%\still.log" echo --- frame %%F
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\f_%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo EXITCODE=%ERRORLEVEL%
endlocal
