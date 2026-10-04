@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set OUT=out\n19chk2
if not exist "%OUT%" mkdir "%OUT%"
for %%F in (15900 18200 24500) do (
  call npx remotion still VoxProject --props=projects/nenkin-19/project.json --frame=%%F "%OUT%\f%%F.png" >> "%OUT%\s.log" 2>&1
)
>> "%OUT%\s.log" echo EXITCODE=%ERRORLEVEL%
