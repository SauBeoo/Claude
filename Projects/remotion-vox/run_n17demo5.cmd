@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL before npx (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo5
if not exist "%O%" mkdir "%O%"

rem After dropping el_police_badge (blank ring) from 9 scenes at SW=280.
rem The 4 hero=None frames are the real risk: a 280px sticker could cover the stat table.
call npx remotion still VoxProject --props=%P% --frame=6100  "%O%\g_gozaimasen.png"   > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=8820  "%O%\h_keisatsu.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=11100 "%O%\i_tbl_9110.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=15600 "%O%\j_tbl_yomikata.png" >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=22700 "%O%\k_tbl_note.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=24700 "%O%\l_jikai.png"        >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=14300 "%O%\m_tbl_reiwa7.png"   >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo EXITCODE=%ERRORLEVEL%
