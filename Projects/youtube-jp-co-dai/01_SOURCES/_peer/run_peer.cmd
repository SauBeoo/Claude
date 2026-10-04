@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\youtube-jp-co-dai
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set LOG=01_SOURCES\_peer\run_peer.log
set SRC=C:\Users\tuana\Downloads\codai
if exist "%LOG%" del "%LOG%"

>> "%LOG%" echo ==== HIT-ka 1-p4aqr-Naw
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_1-p4aqr-Naw_002_720p.mp4" --views 499000 --label HIT-ka --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== HIT-haisuiko sqB200m33fw
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_sqB200m33fw_002_720p.mp4" --views 559302 --label HIT-haisuiko --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== FLOP-mizumawari 3n9odfH-31E
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_3n9odfH-31E_002_720p.mp4" --views 826 --label FLOP-mizumawari --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== FLOP-wifi cQ4f6GzqTZM
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_cQ4f6GzqTZM_002_720p.mp4" --views 811 --label FLOP-wifi --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== HIT-chichu WeiR67KxbVI
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_WeiR67KxbVI_002_720p.mp4" --views 219782 --label HIT-chichu --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== HIT-tv mSLbPOk1_Yc
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_mSLbPOk1_Yc_002_720p.mp4" --views 73056 --label HIT-tv --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ==== HIT-nakaniwa kK9Zx7q2UNc
python tools\analyze_peer.py "%SRC%\YTSave_YouTube_Media_kK9Zx7q2UNc_002_720p.mp4" --views 67437 --label HIT-nakaniwa --model small >> "%LOG%" 2>&1
>> "%LOG%" echo STEP_EXIT=%ERRORLEVEL%

>> "%LOG%" echo ALLDONE
>> "%LOG%" echo EXITCODE=%ERRORLEVEL%
