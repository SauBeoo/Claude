@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL before npx (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo6
if not exist "%O%" mkdir "%O%"

rem Verify the dedicated sticker lane for table/formula scenes (x=1242, y=250/620).
rem Three table shapes: stat only, stat+formula, and the 5-row research note.
call npx remotion still VoxProject --props=%P% --frame=11100 "%O%\n_tbl_9110.png"     > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=14300 "%O%\o_tbl_reiwa7.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=15100 "%O%\p_tbl_formula.png"  >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=15600 "%O%\q_tbl_yomikata.png" >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=22700 "%O%\r_tbl_note.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=23200 "%O%\s_tbl_note_late.png" >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo EXITCODE=%ERRORLEVEL%
