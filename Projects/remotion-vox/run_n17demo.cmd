@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem NOTE the CALL below: npx is npx.CMD. Invoking another .cmd/.bat from inside a .cmd
rem WITHOUT `call` transfers control away for good, so every line after it is skipped --
rem that is why the first run of this wrapper produced a correct mp4 but NO EXITCODE line.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
call npx remotion render VoxProject --props=projects/nenkin-17-demo/project.json out/nenkin-17-demo.mp4 > "out\n17demo.log" 2>&1
>> "out\n17demo.log" echo EXITCODE=%ERRORLEVEL%
