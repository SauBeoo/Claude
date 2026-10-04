@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
if not exist jobs mkdir jobs
py -3 tools\render_chunks.py --project 18_ringo-tabekata --chunk 5000 --concurrency 2 --cache-mb 512 > jobs\18-full.log 2>&1
set RC=%ERRORLEVEL%
>> jobs\18-full.log echo RENDER_EXIT=%RC%
if not "%RC%"=="0" (
  >> jobs\18-full.log echo RENDER GAY - BO QUA DELIVER
  exit /b 1
)
rem --mp4 BAT BUOC: deliver.py khong co co nay se TU RENDER LAI ca video (~70 phut nua).
rem render_chunks.py noi khoi ra out\<project>.mp4
py -3 tools\deliver.py --project 18_ringo-tabekata --channel shokutaku --stem 18_ringo-tabekata --mp4 out\18_ringo-tabekata.mp4 >> jobs\18-full.log 2>&1
>> jobs\18-full.log echo DELIVER_EXIT=%ERRORLEVEL%

rem CTA overlay giua video (card like/share/chuong + SFX). Renderer cu tu chay buoc nay
rem (cta-midvideo.md muc 5); duong remotion KHONG co, nen phai goi tay o day.
rem exit 2 = khong tim thay cau CTA trong srt -> bo qua em, khong phai loi.
set VD=E:\Claude\Projects\youtube-jp-shokutaku\06_VIDEO\18_ringo-tabekata
py -3 E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py "%VD%\18_ringo-tabekata.mp4" --srt "%VD%\subs.srt" --lang jp --in-place >> jobs\18-full.log 2>&1
>> jobs\18-full.log echo CTA_EXIT=%ERRORLEVEL%
