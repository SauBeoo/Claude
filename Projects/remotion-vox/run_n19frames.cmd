@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set OUT=out\n19frames
if not exist "%OUT%" mkdir "%OUT%"
rem 115.9 / 231.9 / 347.9 / 463.9 / 579.9 / 695.9 / 811.9 = dung MOI CHO NOI chunk
rem cong 3 moc noi dung: 25s (co the) . 541s (CTA) . 905s (ket bai)
for %%T in (25 115.9 231.9 347.9 463.9 541.6 579.9 695.9 811.9 905) do (
  ffmpeg -y -ss %%T -i out\nenkin-19_norm.mp4 -frames:v 1 -q:v 2 "%OUT%\t%%T.jpg" >> "%OUT%\f.log" 2>&1
)
>> "%OUT%\f.log" echo EXITCODE=%ERRORLEVEL%
