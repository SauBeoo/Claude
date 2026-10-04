@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set OUT=out\n19still
if not exist "%OUT%" mkdir "%OUT%"
for %%F in (300 1500 3200 5400 7900 9900 12400 15200 18600 21100 24800 27000) do (
  call npx remotion still VoxProject --props=projects/nenkin-19/project.json --frame=%%F "%OUT%\f%%F.png" >> "%OUT%\still.log" 2>&1
)
>> "%OUT%\still.log" echo EXITCODE=%ERRORLEVEL%
