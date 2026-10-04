@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d E:\Claude\Projects\remotion-vox
set OD=out\n21still
> "%OD%\still2.log" echo START
for %%F in (18800 19000 5000 25000) do (
  call npx remotion still VoxProject --props=projects/nenkin-21/project.json --frame=%%F "%OD%\g%%F.png" >> "%OD%\still2.log" 2>&1
  >> "%OD%\still2.log" echo FRAME %%F EXIT=!ERRORLEVEL!
)
>> "%OD%\still2.log" echo STILL_DONE
