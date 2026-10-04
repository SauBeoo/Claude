@echo off
cd /d E:\Claude\Projects\remotion-vox
if not exist out\k01demo mkdir out\k01demo
set LOG=out\k01demo\still.log
> %LOG% echo START
for %%F in (963 1170 2745 3000 3330) do (
  call npx remotion still VoxProject --public-dir=public_k01demo --props=projects/kinishinai-01demo/project.json --frame=%%F out\k01demo\still_%%F.png >> %LOG% 2>&1
)
>> %LOG% echo EXITCODE=%ERRORLEVEL%
