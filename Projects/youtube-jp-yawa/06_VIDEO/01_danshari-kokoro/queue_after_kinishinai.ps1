$log = "E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\remotion_full.log"
Add-Content $log "QUEUE: cho PID 21912 (kinishinai render) ket thuc - $(Get-Date)"
while (Get-Process -Id 21912 -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 60 }
Add-Content $log "QUEUE: bat dau render yawa - $(Get-Date)"
cmd.exe /c "E:\Claude\Projects\youtube-jp-yawa\06_VIDEO\01_danshari-kokoro\run_remotion_full.cmd"
