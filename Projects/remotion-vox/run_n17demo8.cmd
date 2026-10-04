@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL before npx (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo8
if not exist "%O%" mkdir "%O%"

rem Stickers moved OUTSIDE the photocard (two upper corners, above the cast heads).
rem Stills first (cheap), then re-render the same hero clip the user reviewed.
call npx remotion still VoxProject --props=%P% --frame=9400  "%O%\a_one_right.png"  > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=9700  "%O%\b_two_both.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=9950  "%O%\c_swap_right.png" >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=12500 "%O%\d_long_tag.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=17600 "%O%\e_mail_sms.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=22400 "%O%\f_note_lane.png"  >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo STILL_EXIT=%ERRORLEVEL%

call npx remotion render VoxProject --props=%P% --frames=9204-10845 "%O%\demo_hero2.mp4" >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo HERO_EXIT=%ERRORLEVEL%
