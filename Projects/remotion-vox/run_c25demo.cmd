@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL required for npx (case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
call npx remotion render VoxProject --props=projects/co-dai-25/project.json --frames=0-3600 out/co-dai-25_demo.mp4 > "out\c25demo.log" 2>&1
>> "out\c25demo.log" echo EXITCODE=%ERRORLEVEL%
