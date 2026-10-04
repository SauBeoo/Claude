@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem CALL is mandatory before npx (2.6 case 6b) or the EXITCODE line never runs.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demo4
if not exist "%O%" mkdir "%O%"

rem SW 150 -> 280: check every sup-slot count (1, 2 and 3 stickers per scene)
call npx remotion still VoxProject --props=%P% --frame=920   "%O%\a_1sup_shikyuteishi.png" > "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=2850  "%O%\b_2sup_hitonokoe.png"   >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=8820  "%O%\c_3sup_keisatsu.png"    >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=9800  "%O%\d_3sup_komyou.png"      >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=17540 "%O%\e_3sup_mail_sms.png"    >> "%O%\log.txt" 2>&1
call npx remotion still VoxProject --props=%P% --frame=24700 "%O%\f_3sup_jikai.png"       >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo EXITCODE=%ERRORLEVEL%
