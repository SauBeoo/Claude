@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
if not exist out mkdir out
if not exist jobs mkdir jobs
npx remotion render VoxProject --props=projects/18_ringo-tabekata/project.json out/18-probe.mp4 --frames=3980-4100 --overwrite > jobs\18-probe.log 2>&1
>> jobs\18-probe.log echo EXITCODE=%ERRORLEVEL%
