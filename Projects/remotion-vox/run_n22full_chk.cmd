@echo off
rem ASCII ONLY
setlocal
cd /d E:\Claude\Projects\remotion-vox
set TEMP=E:\Claude\_tmp
set TMP=E:\Claude\_tmp
set P=projects\nenkin-22full\project.json
set O=out\s22chk2
if not exist "%O%" mkdir "%O%"
for %%F in (16800 18720 9600) do (
  >> "%O%\still.log" echo --- frame %%F
  call npx remotion still VoxProject --props=%P% --frame=%%F --concurrency=1 "%O%\f_%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo EXITCODE=%ERRORLEVEL%
endlocal
