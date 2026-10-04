@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set P=projects/co-dai-28/project.json
set O=out\c28
if not exist "%O%" mkdir "%O%"
for %%F in (120 900 2400 4200 6000 9000 12000 15000 18000 21000 24000 27000 30000 33000) do (
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\f%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo STILL_EXIT=%ERRORLEVEL%
exit /b %ERRORLEVEL%
