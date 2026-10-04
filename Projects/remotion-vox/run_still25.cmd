@echo off
rem still sheet for nenkin-25 - 10 frames across every scene kind
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set P=projects\nenkin-25\project.json
set O=out\n25still
if not exist "%O%" mkdir "%O%"
> "%O%\still.log" echo START
for %%F in (3504 5928 6192 15840) do (
  >> "%O%\still.log" echo --- frame %%F
  call npx remotion still VoxProject --props=%P% --frame=%%F "%O%\f_%%F.png" >> "%O%\still.log" 2>&1
)
>> "%O%\still.log" echo EXITCODE=%ERRORLEVEL%
