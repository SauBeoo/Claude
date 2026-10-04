@echo off
cd /d E:\Claude\Projects\remotion-vox
if not exist out\k01yawa mkdir out\k01yawa
set LOG=out\k01yawa\still.log
> %LOG% echo START
for %%F in (240 420 870 1200 3240 3690) do (
  call npx remotion still VoxProject --public-dir=public_k01yawa --props=projects/kinishinai-01yawa/project.json --frame=%%F out\k01yawa\still_%%F.png >> %LOG% 2>&1
)
>> %LOG% echo EXITCODE=%ERRORLEVEL%
