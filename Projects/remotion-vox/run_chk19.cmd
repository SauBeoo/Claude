@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set OUT=out\n19chk
if not exist "%OUT%" mkdir "%OUT%"
for %%F in (700 4000 6100 11600 15900 24500) do (
  call npx remotion still VoxProject --props=projects/nenkin-19/project.json --frame=%%F "%OUT%\f%%F.png" >> "%OUT%\s.log" 2>&1
)
>> "%OUT%\s.log" echo EXITCODE=%ERRORLEVEL%
