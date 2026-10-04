@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set P=projects/co-dai-28/project.json
set O=out\c28d
if not exist "%O%" mkdir "%O%"
for %%F in (8700 20700 5100) do (
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\i%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo STILL_EXIT=%ERRORLEVEL%
exit /b %ERRORLEVEL%
