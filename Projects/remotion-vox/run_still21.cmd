@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d E:\Claude\Projects\remotion-vox
set OD=out\n21still
if not exist "%OD%" mkdir "%OD%"
> "%OD%\still.log" echo START
for %%F in (150 1200 3300 5000 8200 8700 10800 12600 14000 18800 22400 25000) do (
  call npx remotion still VoxProject --props=projects/nenkin-21/project.json --frame=%%F "%OD%\f%%F.png" >> "%OD%\still.log" 2>&1
  >> "%OD%\still.log" echo FRAME %%F EXIT=!ERRORLEVEL!
)
>> "%OD%\still.log" echo STILL_DONE
