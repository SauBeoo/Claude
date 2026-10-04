@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem CALL is required: npx is npx.CMD (2.6 case 6b) -- without call EXITCODE never runs.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
call npx remotion render VoxProject --props=projects/co-dai-25/project.json out/co-dai-25.mp4 > "out\c25full.log" 2>&1
>> "out\c25full.log" echo EXITCODE=%ERRORLEVEL%
