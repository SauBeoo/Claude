@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
if not exist out mkdir out
if not exist jobs mkdir jobs
npx remotion render VoxProject --props=projects/18-demo/project.json out/18-demo.mp4 --overwrite > jobs\18-demo.log 2>&1
>> jobs\18-demo.log echo EXITCODE=%ERRORLEVEL%
