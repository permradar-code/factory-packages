#!/usr/bin/env python3
"""Short 10-15 s vertical Shorts from existing clips (owner, 9 Oct: action/insult in the very first frame, no 30 s).
Native 9:16 clips are used full screen; 16:9 clips are cropped to 9:16 on the speaker.
Big captions, hook line on top, "FULL MOVIE - LINK BELOW" pill, 2 s end card (from western_stagecoach_bride/shorts_vertical.py).
Usage: python3 shorts_quick.py [name ...]
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "western_stagecoach_bride"))
import shorts_vertical as sv  # noqa: E402

F2 = "/mnt/user-data/uploads/stagecoach_bride"
F3 = "/mnt/user-data/uploads/stagecoach_bride/film3_barn_storm/src"
OUT = "/home/claude/shorts_quick"
W, HH = sv.W, sv.HH
GRADE3 = "eq=contrast=1.05:saturation=1.15:gamma=1.13:brightness=0.03"
END_S = 2.0

# clip = (file, in, out, crop centre (None = native 9:16), caption line or "", extra filter)
SHORTS = {
    "f3_we_called_them_mothers": {
        "hook": "THEY MOCKED THE WIDOW…",
        "music": (f"{F3}/audio/music/M04.mp3", 0.20),
        "clips": [
            (f"{F3}/visuals/video/C32.mp4", 0.5, 7.7, 0.62,
             "A widow, sleeping under a widower's roof. In my day we had a word for women like that.", GRADE3),
            (f"{F3}/visuals/video/H02.mp4", 0.0, 2.5, None, "We called them mothers.", ""),
            (f"{F3}/visuals/video/C36.mp4", 0.0, 2.7, 0.63, "Mama… he does bite.", GRADE3),
        ],
    },
    "f2_wrong_bride": {
        "hook": "HE GRABBED\nTHE WRONG BRIDE.",
        "music": (f"{F2}/audio/music/M13.mp3", 0.20),
        "clips": [
            (f"{F2}/visuals/video/H02.mp4", 0.0, 4.03, None, "", ""),
            (f"{F2}/shorts1/V09.mp4", 0.4, 3.0, None, "Let her go, Crane.", ""),
            (f"{F2}/shorts1/V13.mp4", 1.0, 3.7, None, "Not one word, Agatha.", ""),
        ],
    },
}


def captions(line, L):
    if not line:
        return []
    parts = sv.chunks(line)
    a, b = 0.1, max(0.6, L - 0.25)
    tot = sum(len(p) for p in parts)
    out, t = [], a
    for p in parts:
        dt = (b - a) * len(p) / tot
        out.append((t, t + dt, p)); t += dt
    return out


def vf(crop, extra):
    if crop is None:
        v = f"scale={W}:{HH}:flags=lanczos,eq=contrast=1.04:saturation=1.08"
    else:
        cw = 405
        x = int(min(max(crop * 1280 - cw / 2, 0), 1280 - cw))
        v = f"crop={cw}:720:{x}:0,scale={W}:{HH}:flags=lanczos,unsharp=5:5:0.6"
    if extra:
        v += "," + extra
    return v + ",fps=24,setsar=1"


def build(name, spec):
    tmp = f"{OUT}/{name}_tmp"
    os.makedirs(tmp, exist_ok=True)
    hook, parts = spec["hook"], []
    for k, (f, a, b, crop, line, extra) in enumerate(spec["clips"]):
        L = b - a
        caps = captions(line, L)
        events = sorted({0.0, L, *[c0 for c0, _, _ in caps], *[min(L, c1) for _, c1, _ in caps]})
        inputs = ["-ss", f"{a:.3f}", "-t", f"{L:.3f}", "-i", f]
        fc, prev, j = [f"[0:v]{vf(crop, extra)}[v0]"], "[v0]", 0
        for i in range(len(events) - 1):
            t0, t1 = events[i], events[i + 1]
            if t1 - t0 < 0.02:
                continue
            mid = (t0 + t1) / 2
            txt = next((c for c0, c1, c in caps if c0 <= mid < c1), "")
            img = f"{tmp}/c{k:02d}_{j:02d}.png"
            sv.png(img, hook, txt, False)
            inputs += ["-i", img]
            fc.append(f"{prev}[{j + 1}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})'[o{j}]")
            prev, j = f"[o{j}]", j + 1
        out = f"{tmp}/p{k:02d}.mp4"
        af = f"loudnorm=I=-16:TP=-2,afade=t=in:d=0.03,afade=t=out:st={max(0, L - 0.08):.3f}:d=0.08"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", prev,
                        "-map", "0:a", "-af", af, "-t", f"{L:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                        out], check=True)
        parts.append(out)
    endpng, endmp4 = f"{tmp}/end.png", f"{tmp}/end.mp4"
    sv.png(endpng, hook, "", True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", parts[-1], "-frames:v", "1",
                    f"{tmp}/last.png"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{END_S}", "-i", f"{tmp}/last.png", "-i", endpng,
                    "-f", "lavfi", "-t", f"{END_S}", "-i", "anullsrc=r=48000:cl=stereo",
                    "-filter_complex", "[0:v]fps=24,format=yuv420p[a];[a][1:v]overlay=0:0[o]", "-map", "[o]",
                    "-map", "2:a", "-t", f"{END_S}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", endmp4],
                   check=True)
    parts.append(endmp4)
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in parts)
    joined = f"{tmp}/joined.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-c", "copy", joined], check=True)
    T = sv.dur(joined)
    mfile, vol = spec["music"]
    out = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-i", mfile, "-filter_complex",
                    f"[1:a]volume={vol},afade=t=out:st={T - 1.5:.2f}:d=1.5,atrim=0:{T:.2f}[m];"
                    f"[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-2[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    print(out, round(sv.dur(out), 1), "s")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or SHORTS):
        build(n, SHORTS[n])
