@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem CALL is mandatory before npx: npx is npx.CMD and control never returns without it
rem (2.6 case 6b) -- the EXITCODE line at the bottom would silently never run.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo3
if not exist "%O%" mkdir "%O%"

rem --- 7 stills, one per scene whose hero image was replaced (lot CARD3) ---
call npx remotion still VoxProject --props=%P% --frame=920   "%O%\s02_shikyuteishi.png"  > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=2850  "%O%\s05_hitonokoe.png"    >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=6690  "%O%\s12_genten.png"       >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=8820  "%O%\s15_keisatsu.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=17540 "%O%\s29_mail_sms.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=18010 "%O%\s30_hitokoto.png"     >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=24700 "%O%\s38_jikai.png"        >> "%O%\log.txt" 2>&1

rem --- 33s clip: two replaced scenes back to back (checks stagger + transition) ---
call npx remotion render VoxProject --props=%P% --frames=17159-18155 "%O%\demo3.mp4" >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo EXITCODE=%ERRORLEVEL%
