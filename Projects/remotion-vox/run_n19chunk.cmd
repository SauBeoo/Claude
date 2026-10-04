@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
set VD=E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\19_kounenrei-koyou-keizoku-kyufu
set CH=out\n19parts
set LOG=%VD%\render.log
if not exist "%CH%" mkdir "%CH%"

rem ---- RENDER THEO CHUNK, CO RESUME -------------------------------------
rem  Ly do: lan truoc bi kill o frame 10154/27832 va MAT TRANG toan bo.
rem  Chunk 3480 frame (~116s) -> 8 khuc; bi kill thi chi mat 1 khuc.
rem  Khuc nao da co file thi BO QUA (resume). Xoa file khuc de bat render lai.
rem  ? KHONG dung "file da ton tai chua" lam dieu kien duy nhat khi doi ASSET ?
rem     doi anh thi phai xoa ca thu muc %CH% (render-background.md ?2.5).

>> "%LOG%" echo === CHUNKED RENDER ===
for %%C in (0 1 2 3 4 5 6 7) do call :one %%C
goto :concat

:one
set /a A=%1*3480
set /a B=%A%+3479
if %B% GTR 26973 set B=26973
if exist "%CH%\p%1.mp4" ( >> "%LOG%" echo SKIP chunk %1 [%A%-%B%] da co & exit /b 0 )
>> "%LOG%" echo --- chunk %1 [%A%-%B%] ---
call npx remotion render VoxProject --props=projects/nenkin-19/project.json --frames=%A%-%B% "%CH%\p%1.mp4" >> "%LOG%" 2>&1
>> "%LOG%" echo CHUNK%1_EXIT=%ERRORLEVEL%
exit /b 0

:concat
>> "%LOG%" echo === CONCAT ===
if exist "%CH%\list.txt" del "%CH%\list.txt"
for %%C in (0 1 2 3 4 5 6 7) do (
  if not exist "%CH%\p%%C.mp4" ( >> "%LOG%" echo THIEU chunk %%C - DUNG & exit /b 1 )
  >> "%CH%\list.txt" echo file 'p%%C.mp4'
)
ffmpeg -y -f concat -safe 0 -i "%CH%\list.txt" -c copy "out\nenkin-19.mp4" >> "%LOG%" 2>&1
set CE=%ERRORLEVEL%
>> "%LOG%" echo CONCAT_EXIT=%CE%
if not "%CE%"=="0" exit /b 2

>> "%LOG%" echo === LOUDNORM ===
ffmpeg -y -i "out\nenkin-19.mp4" -c:v copy -af "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" "out\nenkin-19_norm.mp4" >> "%LOG%" 2>&1
>> "%LOG%" echo LOUDNORM_EXIT=%ERRORLEVEL%

>> "%LOG%" echo === CTA: BO QUA (rule render-background muc 8) ===
>> "%LOG%" echo EXITCODE=0
