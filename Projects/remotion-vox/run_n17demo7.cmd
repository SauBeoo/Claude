@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL before npx (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo7
if not exist "%O%" mkdir "%O%"

rem RELAY (one sticker at a time) + SW 280 -> 360. Sample each of the 3 slots
rem (right / centre / left) plus the widened table lane.
call npx remotion still VoxProject --props=%P% --frame=900   "%O%\a_slot0_right.png"  > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=9600  "%O%\b_slot1_centre.png" >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=10000 "%O%\c_slot2_left.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=8900  "%O%\d_keisatsu.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=22400 "%O%\e_note_a.png"       >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=23100 "%O%\f_note_b.png"       >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=14300 "%O%\g_tbl_reiwa7.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=18500 "%O%\h_quiz.png"         >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo EXITCODE=%ERRORLEVEL%
