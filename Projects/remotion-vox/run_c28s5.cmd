@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set P=projects/co-dai-28/project.json
set O=out\c28e
if not exist "%O%" mkdir "%O%"
for %%F in (2600 5100 9200 11700 17800 20700 25500 8700 16500 30500) do (
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\j%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo STILL_EXIT=%ERRORLEVEL%
exit /b %ERRORLEVEL%
