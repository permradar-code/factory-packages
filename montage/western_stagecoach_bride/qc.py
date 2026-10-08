#!/usr/bin/env python3
"""QC of the finished film: duration, black frames, silences, loudness, frozen frames, contact sheets.
Usage: python3 qc.py [film.mp4]   (default /home/claude/wsb_edit/stagecoach_bride.mp4)
"""
import json, os, re, subprocess, sys

F = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wsb_edit/stagecoach_bride.mp4"
OUT = os.path.join(os.path.dirname(F), "qc")
os.makedirs(OUT, exist_ok=True)


def ff(args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True).stderr


dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", F],
                           capture_output=True, text=True).stdout)
print(f"duration {dur/60:.2f} min ({dur:.1f} s)")

log = ff(["-i", F, "-vf", "blackdetect=d=0.4:pix_th=0.10", "-an", "-f", "null", "-"])
blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
print("black >0.4s:", [(round(float(a), 1), round(float(b) - float(a), 1)) for a, b in blacks] or "none")

log = ff(["-i", F, "-af", "silencedetect=n=-45dB:d=1.5", "-vn", "-f", "null", "-"])
sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", log)
print("silence >1.5s:", [(round(float(a), 1), round(float(b) - float(a), 1)) for a, b in sil] or "none")

log = ff(["-i", F, "-vf", "freezedetect=n=0.003:d=2.5", "-an", "-f", "null", "-"])
fr = re.findall(r"freeze_start: ([\d.]+)[\s\S]*?freeze_duration: ([\d.]+)", log)
print("frozen >2.5s:", [(round(float(a), 1), round(float(b), 1)) for a, b in fr] or "none")

log = ff(["-i", F, "-af", "loudnorm=I=-14:TP=-1.5:print_format=json", "-vn", "-f", "null", "-"])
j = json.loads(log[log.rfind("{"):log.rfind("}") + 1])
print(f"loudness {j['input_i']} LUFS, true peak {j['input_tp']} dBTP")

# contact sheets: first 60 s every 2 s, then the whole film every 10 s
ff(["-y", "-i", F, "-t", "60", "-vf", "fps=0.5,scale=320:-1,tile=6x5", "-frames:v", "1", f"{OUT}/first60.jpg"])
ff(["-y", "-i", F, "-vf", "fps=0.1,scale=240:-1,tile=10x9", "-frames:v", "1", f"{OUT}/whole.jpg"])
print("sheets:", f"{OUT}/first60.jpg", f"{OUT}/whole.jpg")
