#!/bin/bash
# usage: tools/sheet.sh out.jpg id1 id2 ... (images in visuals/images)
cd /c/Users/permr/fl_work/wwp
out=$1; shift
args=(); fl=""; i=0
for id in "$@"; do args+=(-i "visuals/images/$id.png"); fl+="[$i:v]scale=480:-1,drawtext=text='$id':x=8:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[v$i];"; i=$((i+1)); done
row=""; for ((j=0;j<i;j++)); do row+="[v$j]"; done
cols=4; 
ffmpeg -v error -y "${args[@]}" -filter_complex "${fl}${row}xstack=inputs=$i:layout=$(python - <<P
n=$i; cols=4
print('|'.join(f"{(k%cols)*480}_{(k//cols)*270}" for k in range(n)))
P
)" -q:v 3 "$out" && echo ok
