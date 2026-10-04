@echo off
rem ASCII-ONLY wrapper (render-background.md 2.6 case 1). Do NOT put non-ASCII here.
rem CALL is required for npx (2.6 case 6b); the python renderer spawns npx itself.
rem 4 chunks with resume + separate audio mux -- see render_chunks_21b.py docstring.
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-nenkin
set PYTHONIOENCODING=utf-8
python tools\render_chunks_21b.py --conc 1 > "06_VIDEO\21_fuyo-shinkokusho-205man\render21b.log" 2>&1
>> "06_VIDEO\21_fuyo-shinkokusho-205man\render21b.log" echo RENDER_EXIT=%ERRORLEVEL%
