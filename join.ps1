# Joins the film parts into one MP4 and checks the hash.
$ErrorActionPreference = "Stop"
cmd /c "copy /b The_Widows_Piano_1080p.mp4.part00+The_Widows_Piano_1080p.mp4.part01+The_Widows_Piano_1080p.mp4.part02+The_Widows_Piano_1080p.mp4.part03+The_Widows_Piano_1080p.mp4.part04 The_Widows_Piano_1080p.mp4"
$h = (Get-FileHash The_Widows_Piano_1080p.mp4 -Algorithm SHA256).Hash.ToLower()
if ($h -eq "6bff623f470502cc499619b556e9069e3891029a67fe3aa764cb908ac0fcb4e1") { Write-Host "OK: The_Widows_Piano_1080p.mp4" } else { Write-Host "HASH MISMATCH" }
