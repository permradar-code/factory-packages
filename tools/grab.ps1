param([string]$Dest)
$f=$null
for($i=0;$i -lt 45;$i++){
  $f = Get-ChildItem "$env:USERPROFILE\Downloads" -File | Where-Object { $_.Extension -in '.jpg','.png','.jpeg','.webp','.jfif' } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if($f -and ((Get-Date) - $f.LastWriteTime) -lt [TimeSpan]::FromMinutes(3)){ break } else { $f=$null; Start-Sleep 2 }
}
if(-not $f){ "NO FRESH DOWNLOAD"; exit 1 }
Start-Sleep 1
New-Item -ItemType Directory -Force (Split-Path $Dest) | Out-Null
ffmpeg -v error -y -i $f.FullName $Dest
$dim = ffprobe -v error -show_entries stream=width,height -of csv=p=0 $Dest
Remove-Item $f.FullName -Force
"saved $Dest (src $($f.Name), $([math]::Round((Get-Item $Dest).Length/1KB)) KB) $dim"
