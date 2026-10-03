param([string]$Name, [string]$Sub = "_variants\gemini")
# Saves the newest Gemini_Generated_Image* from Downloads (< 3 min old) as a real PNG named <Name>.png.
# Waits up to 25 s for a download whose content differs from every PNG already in the target folder (avoids saving the previous image twice).
$w = "C:\Users\permr\fl_work\wwp"
New-Item -ItemType Directory -Force "$w\$Sub" | Out-Null
$out = "$w\$Sub\$Name.png"
for ($i = 0; $i -lt 13; $i++) {
  $f = Get-ChildItem "$env:USERPROFILE\Downloads" -File | Where-Object { $_.Name -like "Gemini_Generated_Image*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($f -and ((Get-Date) - $f.LastWriteTime -lt [TimeSpan]::FromMinutes(3))) {
    $tmp = "$env:TEMP\gem_tmp.png"; ffmpeg -v error -y -i $f.FullName $tmp
    $h = (Get-FileHash $tmp).Hash
    $dup = Get-ChildItem "$w\$Sub" -Filter *.png -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "$Name.png" -and (Get-FileHash $_.FullName).Hash -eq $h }
    if (-not $dup) { Copy-Item $tmp $out -Force; $dim = ffprobe -v error -show_entries stream=width,height -of csv=p=0 $out; "saved $out (src $($f.Name) $([math]::Round($f.Length/1KB)) KB) $dim"; exit 0 }
  }
  Start-Sleep 2
}
"NO NEW DOWNLOAD"; exit 1
