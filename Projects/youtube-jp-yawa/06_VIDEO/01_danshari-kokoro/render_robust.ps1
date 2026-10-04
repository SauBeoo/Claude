# Render yawa 01 full: cho may RANH (khong co 'remotion render' cua phien khac) roi moi chay,
# khoi nho 1500 frame, khoi chet thi chay lai (render_chunks.py tu resume khoi da du frame).
$log = "E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\remotion_full.log"
$vd  = "E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro"
function Others { @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -match 'remotion-cli\.js" render' -and $_.CommandLine -notmatch 'yawa-01-full' }).Count }
for ($try = 1; $try -le 20; $try++) {
  while ((Others) -gt 0) { Start-Sleep -Seconds 60 }
  Add-Content $log "ROBUST: lan $try bat dau $(Get-Date)"
  Push-Location "E:\Claude\Projects\remotion-vox"
  & python tools\render_chunks.py --project yawa-01-full --chunk 1500 --concurrency 2 --cache-mb 256 *>> $log
  $rc = $LASTEXITCODE
  Pop-Location
  Add-Content $log "ROBUST: lan $try exit=$rc $(Get-Date)"
  if ($rc -eq 0) { break }
  Start-Sleep -Seconds 30
}
if ($rc -ne 0) { Add-Content $log "RENDER_EXIT=$rc"; exit 1 }
Add-Content $log "RENDER_EXIT=0"
& ffmpeg -hide_banner -nostats -y -i "E:\Claude\Projects\remotion-vox\out\yawa-01-full.mp4" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 "$vd\01_danshari-kokoro_remotion.mp4" *>> $log
Add-Content $log "EXITCODE=$LASTEXITCODE"
