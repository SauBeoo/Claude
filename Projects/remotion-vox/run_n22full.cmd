@echo off
rem ASCII ONLY - render-background.md 2.6 trap (1): cmd.exe reads OEM codepage first
rem 'call' is REQUIRED before npx - npx is a .CMD; without it the rest of the file is skipped
setlocal
cd /d E:\Claude\Projects\remotion-vox
set P=projects\nenkin-22full\project.json
set O=out\n22full
if not exist "%O%" mkdir "%O%"
>> "%O%\render.log" echo === START %DATE% %TIME%
call npx remotion render VoxProject --props=%P% --concurrency=4 "%O%\raw.mp4" >> "%O%\render.log" 2>&1
set RC=%ERRORLEVEL%
>> "%O%\render.log" echo RENDER_EXIT=%RC%
if not "%RC%"=="0" goto END
rem -14 LUFS chuan kenh (project_loudness_14_lufs): nen truoc roi loudnorm
ffmpeg -y -v error -i "%O%\raw.mp4" -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" -c:a aac -b:a 192k "%O%\final.mp4" >> "%O%\render.log" 2>&1
set RC=%ERRORLEVEL%
>> "%O%\render.log" echo LOUDNORM_EXIT=%RC%
:END
>> "%O%\render.log" echo EXITCODE=%RC%
endlocal
