@echo off
rem Render DEMO khuon telop + hoa la canh cho nenkin video 22.
rem ASCII ONLY (render-background.md 2.6 muc 1).
rem 'call' bat buoc truoc npx (npx la .CMD) - thieu no thi dong EXITCODE khong chay.
cd /d E:\Claude\Projects\remotion-vox
if not exist "out\n22demo" mkdir "out\n22demo"
call npx remotion render VoxProject --props=projects/nenkin-22demo/project.json --concurrency=4 "out\n22demo\demo.mp4" > "out\n22demo\render.log" 2>&1
>> "out\n22demo\render.log" echo EXITCODE=%ERRORLEVEL%
