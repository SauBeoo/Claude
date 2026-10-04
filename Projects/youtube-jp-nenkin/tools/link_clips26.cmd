@echo off
setlocal
set SRC=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\26_kaigo-hokenryo-dankai-setai\clips
set DST=E:\Claude\Projects\remotion-vox\public\projects\nenkin-26\assets
for %%F in ("%SRC%\clip_*.mp4") do (
  if not exist "%DST%\%%~nxF" mklink /H "%DST%\%%~nxF" "%%~fF" >nul
)
echo LINKED
