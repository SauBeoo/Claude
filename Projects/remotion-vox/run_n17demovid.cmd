@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). CALL before npx (2.6 case 6b).
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set PYTHONIOENCODING=utf-8
set P=projects/nenkin-17/project.json
set O=out\n17demovid
if not exist "%O%" mkdir "%O%"

rem Clip 1 (55s): two hero scenes, 3 relay swaps each -- sticker size + swap on a photo.
call npx remotion render VoxProject --props=%P% --frames=9204-10845 "%O%\demo_hero.mp4" > "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo HERO_EXIT=%ERRORLEVEL%

rem Clip 2 (47s): the research-note table, 5 relay swaps in the dedicated right-hand lane.
call npx remotion render VoxProject --props=%P% --frames=21984-23386 "%O%\demo_note.mp4" >> "%O%\log.txt" 2>&1
>> "%O%\log.txt" echo NOTE_EXIT=%ERRORLEVEL%
