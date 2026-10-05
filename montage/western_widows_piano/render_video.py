#!/usr/bin/env python3
"""Render video segments for The Widow's Piano from edl.json (video only; audio is mixed separately)."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

EDL = json.load(open("/home/claude/montage/edl.json"))
SEG = "/home/claude/montage/seg"
os.makedirs(SEG, exist_ok=True)
W, H = int(os.environ.get("W", 1280)), int(os.environ.get("H", 720))
FPS = 24
SC = float(os.environ.get("SCALE", 2))
SW, SH = int(W*SC)//2*2, int(H*SC)//2*2
X = 0.7  # crossfade between stills inside a narration block
ENC = ["-c:v", "libx264", "-preset", os.environ.get("PRESET", "veryfast"), "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]
FONT = "/home/claude/fonts/Rye-Regular.ttf"

def zoom_filter(motion, frames, flashback):
    # source is pre-scaled to 2W x 2H; output W x H
    n = max(frames - 1, 1)
    p = f"(on/{n})"
    m = motion.lower()
    if "pull out" in m:
        z, x, y = f"1.12-0.12*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif "very slow push" in m:
        z, x, y = f"1.0+0.05*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif "pan left" in m:
        z, x, y = "1.12", f"(iw-iw/zoom)*(1-{p})", "ih/2-(ih/zoom/2)"
    elif "pan" in m or "tracking" in m:
        z, x, y = "1.12", f"(iw-iw/zoom)*{p}", "ih/2-(ih/zoom/2)"
    elif "crane down" in m:
        z, x, y = "1.12", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*{p}"
    else:  # push in / aerial drift forward
        z, x, y = f"1.0+0.10*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    f = (f"scale={SW}:{SH}:force_original_aspect_ratio=increase:flags=lanczos,crop={SW}:{SH},"
         f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1")
    if flashback:
        f += ",eq=saturation=0.55:contrast=1.03,vignette=PI/4.5"
    return f

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-1500:]); raise SystemExit(f"failed: {' '.join(cmd[:8])}")

def still(img, dur, motion, flashback, out):
    frames = int(round(dur * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", img, "-vf", zoom_filter(motion, frames, flashback),
         "-frames:v", str(frames), *ENC, out])

def block(ev, out):
    ims = ev["images"]
    if not ims:
        return
    tmp = []
    for k, im in enumerate(ims):
        L = im["dur"] + (X if k < len(ims) - 1 else 0)
        p = f"{SEG}/{ev['id']}_{k:02d}.mp4"
        still(im["file"], L, im["motion"], im["flashback"], p)
        tmp.append((p, L))
    if len(tmp) == 1:
        os.replace(tmp[0][0], out); return
    inputs, fc, prev, out_len = [], [], "[0:v]", tmp[0][1]
    for p, _ in tmp:
        inputs += ["-i", p]
    for k in range(1, len(tmp)):
        off = out_len - X
        lab = f"[v{k}]"
        fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={X}:offset={off:.3f}{lab}")
        prev, out_len = lab, off + tmp[k][1]
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", prev, *ENC, out])
    for p, _ in tmp:
        os.remove(p)

def clip(ev, out):
    vf = f"scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    run(["ffmpeg", "-y", "-v", "error", "-i", ev["file"], "-t", str(ev["dur"]), "-vf", vf, "-an", *ENC, out])

def title(ev, out):
    d = ev["dur"]
    if ev["text"]:
        txt = ev["text"].replace("'", "’").replace(":", "\\:")
        vf = (f"drawtext=fontfile={FONT}:text='{txt}':fontsize={int(H*0.11)}:fontcolor=0xE8D9B5:"
              f"x=(w-text_w)/2:y=(h-text_h)/2:alpha='if(lt(t,1),t,if(gt(t,{d-1}),{d}-t,1))',"
              f"drawtext=fontfile={FONT}:text='A TALE OF CEDAR BLUFF':fontsize={int(H*0.035)}:fontcolor=0xB89A6A:"
              f"x=(w-text_w)/2:y=(h/2)+{int(H*0.11)}:alpha='if(lt(t,1.5),max(t-0.5,0),if(gt(t,{d-1}),{d}-t,1))'")
    else:
        vf = "null"
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x0b0806:s={W}x{H}:r={FPS}:d={d}", "-vf", vf, *ENC, out])

jobs = []
for idx, ev in enumerate(EDL["events"]):
    out = f"{SEG}/{idx:03d}_{ev['id']}.mp4"
    ev["seg"] = out
    if os.path.exists(out) and os.environ.get("FORCE") != "1":
        continue
    if ev["kind"] == "narration":
        jobs.append((block, ev, out))
    elif ev["kind"] == "clip":
        jobs.append((clip, ev, out))
    elif ev["kind"] == "image":
        jobs.append((lambda e, o: still(e["file"], e["dur"], e["motion"], e["flashback"], o), ev, out))
    else:
        jobs.append((title, ev, out))

with ThreadPoolExecutor(2) as ex:
    for f in [ex.submit(fn, ev, out) for fn, ev, out in jobs]:
        f.result()

with open(f"{SEG}/list.txt", "w") as fh:
    for ev in EDL["events"]:
        fh.write(f"file '{ev['seg']}'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{SEG}/list.txt", "-c", "copy",
     "/home/claude/montage/video_only.mp4"])
print("video done")
