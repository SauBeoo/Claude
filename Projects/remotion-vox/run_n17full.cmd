@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem NOTE the CALL: npx is npx.CMD -- invoking another .cmd without `call` transfers
rem control away for good and the EXITCODE line below never runs (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
call npx remotion render VoxProject --props=projects/nenkin-17/project.json out/nenkin-17.mp4 > "out\n17full.log" 2>&1
>> "out\n17full.log" echo EXITCODE=%ERRORLEVEL%
