#!/bin/bash
# usage: tools/gem_save.sh <name> <dest.png>  -> saves the newest Gemini download as 1280x720 PNG at dest (relative to repo) and keeps the original under _variants/gemini2
cd /c/Users/permr/fl_work/wwp
powershell -NoProfile -File tools/grab_gem.ps1 -Name "$1" -Sub "_variants\gemini2" || exit 1
mkdir -p "$(dirname "$2")"
ffmpeg -v error -y -i "_variants/gemini2/$1.png" -vf scale=1280:720 "$2" && echo "installed $2"
