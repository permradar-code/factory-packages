# Joins the parts into The_Stagecoach_Bride.mp4 (same folder) and checks the file
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$out = Join-Path $dir "The_Stagecoach_Bride.mp4"
$parts = Get-ChildItem (Join-Path $dir "The_Stagecoach_Bride_part*.bin") | Sort-Object Name
$fs = [System.IO.File]::Create($out)
foreach ($p in $parts) { $b = [System.IO.File]::ReadAllBytes($p.FullName); $fs.Write($b, 0, $b.Length) }
$fs.Close()
$md5 = (Get-FileHash $out -Algorithm MD5).Hash.ToLower()
$want = (Get-Content (Join-Path $dir "md5.txt")).Trim()
if ($md5 -eq $want) { Write-Host "OK: The_Stagecoach_Bride.mp4 is ready." -ForegroundColor Green; Remove-Item $parts.FullName }
else { Write-Host "ERROR: checksum mismatch, parts kept." -ForegroundColor Red }
Read-Host "Press Enter"
