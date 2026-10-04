@echo off
rem start remotion-vox editor: API server (7788) + Vite editor (5599)
cd /d E:\Claude\Projects\remotion-vox
start "remotion-vox-server" /min cmd /c "node server\index.mjs"
start "remotion-vox-editor" /min cmd /c "npx.cmd vite --config apps\editor\vite.config.mts"
%SystemRoot%\System32\ping.exe -n 4 127.0.0.1 >nul
start http://localhost:5599/
