@echo off
cd /d E:\Claude\Projects\remotion-vox
if not exist out\k01demo mkdir out\k01demo
set LOG=out\k01demo\render.log
> %LOG% echo START
call npx remotion render VoxProject --public-dir=public_k01demo --props=projects/kinishinai-01demo/project.json out\k01demo\demo.mp4 --concurrency=2 --offthreadvideo-cache-size-in-bytes=268435456 --media-cache-size-in-bytes=268435456 >> %LOG% 2>&1
>> %LOG% echo EXITCODE=%ERRORLEVEL%
