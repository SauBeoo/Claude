# move_pagefile_to_c.ps1 — dời pagefile E: (SSD SATA, cùng ổ workspace render) sang C: (NVMe)
# Chạy bằng PowerShell ADMIN. Sau khi chạy PHẢI RESTART máy mới có tác dụng.
# Vì sao: pagefile 17GB đang nằm đúng ổ E: nơi ffmpeg ghi file render → khi RAM căng,
# page I/O và render I/O đánh nhau trên cùng con SSD rẻ (Colorful SL300, không DRAM).
# Peak usage đo được chỉ 2.4GB → 8GB cố định trên C: là dư dả (C: còn ~21GB, sau còn ~13GB).

$ErrorActionPreference = "Stop"

# 1. Tắt chế độ tự quản
$cs = Get-CimInstance Win32_ComputerSystem
if ($cs.AutomaticManagedPagefile) {
    Set-CimInstance -InputObject $cs -Property @{AutomaticManagedPagefile = $false}
    Write-Host "Da tat AutomaticManagedPagefile"
}

# 2. Xoa moi pagefile setting cu (E: hoac cho khac)
Get-CimInstance Win32_PageFileSetting | ForEach-Object {
    Write-Host "Xoa pagefile cu: $($_.Name)"
    Remove-CimInstance -InputObject $_
}

# 3. Tao pagefile C: 8192MB co dinh
New-CimInstance -ClassName Win32_PageFileSetting -Property @{
    Name = "C:\pagefile.sys"; InitialSize = [uint32]8192; MaximumSize = [uint32]8192
} | Out-Null
Write-Host "Da tao pagefile C:\pagefile.sys 8192MB co dinh"
Write-Host ""
Write-Host ">>> RESTART MAY de ap dung. Sau restart, file E:\pagefile.sys se tu bien mat."
