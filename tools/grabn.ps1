param([string[]]$Names, [string]$Sub = "visuals\refs")
$w = "C:\Users\permr\fl_work\wwp"
New-Item -ItemType Directory -Force "$w\$Sub" | Out-Null
$n = $Names.Count
$files = Get-ChildItem "$env:USERPROFILE\Downloads" -File | Where-Object { $_.Extension -in '.jpg', '.png', '.jpeg', '.webp' } | Sort-Object LastWriteTime -Descending | Select-Object -First $n | Sort-Object LastWriteTime
if ($files.Count -ne $n) { "expected $n files, found $($files.Count)"; exit 1 }
for ($i = 0; $i -lt $n; $i++) {
  $out = "$w\$Sub\$($Names[$i]).png"
  ffmpeg -v error -y -i $files[$i].FullName $out
  $dim = ffprobe -v error -show_entries stream=width,height -of csv=p=0 $out
  "$($Names[$i])  <-  $($files[$i].Name)  $($files[$i].LastWriteTime.ToString('HH:mm:ss'))  $dim"
}
