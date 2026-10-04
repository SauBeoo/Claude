@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem CALL is required: npx is npx.CMD (2.6 case 6b) -- without call EXITCODE never runs.
rem concurrency 2 -> 4: ban v3 la 100%% footage + 7 scene speed 0.18 nen decode nang
rem hon han, uoc 1h09 va da bi kill o frame 11180/33537. May 6 nhan, 4 worker con
rem chua o 1 nhan cho he thong.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
call npx remotion render VoxProject --props=projects/co-dai-28/project.json out/co-dai-28.mp4 --concurrency=4 > "out\c28full.log" 2>&1
>> "out\c28full.log" echo EXITCODE=%ERRORLEVEL%
