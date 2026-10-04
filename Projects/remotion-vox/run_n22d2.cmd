@echo off
rem Render demo nenkin 22 ban 2 (anh LOT1 sau khi sua prompt + 2 khoi do hoa font).
rem ASCII ONLY - cmd.exe doc file theo codepage OEM truoc khi chcp kip tac dung.
rem "call" bat buoc truoc npx: npx la npx.CMD, thieu call thi moi dong sau bi bo qua.
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set OUT=out\n22d2
if not exist "%OUT%" mkdir "%OUT%"
> "%OUT%\render.log" echo START %DATE% %TIME%
call npx remotion render VoxProject --props=projects/nenkin-22d2/project.json --concurrency=3 "%OUT%\demo.mp4" >> "%OUT%\render.log" 2>&1
>> "%OUT%\render.log" echo EXITCODE=%ERRORLEVEL%
