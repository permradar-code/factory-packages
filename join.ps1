# Joins the film parts into one MP4 and checks the hash.
$ErrorActionPreference = "Stop"
cmd /c "copy /b The_Widows_Piano_1080p.mp4.part00+The_Widows_Piano_1080p.mp4.part01+The_Widows_Piano_1080p.mp4.part02+The_Widows_Piano_1080p.mp4.part03+The_Widows_Piano_1080p.mp4.part04 The_Widows_Piano_1080p.mp4"
$h = (Get-FileHash The_Widows_Piano_1080p.mp4 -Algorithm SHA256).Hash.ToLower()
if ($h -eq "4230b8b933a3660d36122427bdfa902ae26256d82b64849598abe877629fd13c") { Write-Host "OK: The_Widows_Piano_1080p.mp4" } else { Write-Host "HASH MISMATCH" }
