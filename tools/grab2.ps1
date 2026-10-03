param([string]$Name, [string]$Sub = "visuals\refs", [string]$Ext = "png")
$w = "C:\Users\permr\fl_work\wwp"
New-Item -ItemType Directory -Force "$w\$Sub" | Out-Null
$f = Get-ChildItem "$env:USERPROFILE\Downloads" -File | Where-Object { $_.Extension -in '.jpg', '.png', '.mp4', '.jpeg', '.webp' } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ((Get-Date) - $f.LastWriteTime -gt [TimeSpan]::FromMinutes(3)) { Write-Output "NO FRESH DOWNLOAD (newest: $($f.Name) at $($f.LastWriteTime))"; exit 1 }
$out = "$w\$Sub\$Name.$Ext"
if ($Ext -eq "png") { ffmpeg -v error -y -i $f.FullName $out } else { Copy-Item $f.FullName $out -Force }
$dim = ffprobe -v error -show_entries stream=width,height -of csv=p=0 $out
"saved $out (src $($f.Name), $([math]::Round($f.Length/1KB)) KB) $dim"
