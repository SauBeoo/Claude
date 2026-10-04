@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\remotion-vox
if not exist jobs mkdir jobs
py -3 tools\render_chunks.py --project 19_tanpakushitsu-asa --chunk 5000 --concurrency 2 --cache-mb 512 > jobs\19-full.log 2>&1
set RC=%ERRORLEVEL%
>> jobs\19-full.log echo RENDER_EXIT=%RC%
if not "%RC%"=="0" (
  >> jobs\19-full.log echo RENDER GAY - BO QUA DELIVER
  exit /b 1
)
rem --mp4 BAT BUOC: deliver.py khong co co nay se TU RENDER LAI ca video.
py -3 tools\deliver.py --project 19_tanpakushitsu-asa --channel shokutaku --stem 19_tanpakushitsu-asa --mp4 out\19_tanpakushitsu-asa.mp4 >> jobs\19-full.log 2>&1
>> jobs\19-full.log echo DELIVER_EXIT=%ERRORLEVEL%

rem cta_inject DA BO khoi duong remotion (chot 2026-08-25, video 20):
rem no XOA PHU DE trong ca doan re-encode ma van tra exit 0.
rem Do that video 20: log bao CTA @579.51s / re-encode [566.83..591.83] / CTA_EXIT=0,
rem nhung frame 570-586 mat sach phu de trong khi subs.srt co 6 cue o dung vung do,
rem con ban remotion-vox\out\*.mp4 truoc inject thi CO phu de.
rem Cau CTA VAN DUOC DOC vi no nam trong _TTS.md (cta-midvideo.md muc 1) - chi mat lop hinh card.
rem Muon bat lai thi phai SUA cta_inject cho duong remotion, khong phai chinh toa do card.
