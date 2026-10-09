#!/usr/bin/env python3
"""Film 3 promo Short (1080x1920): the cold-open dialogue in vertical, ending on the Texas Ranger reveal.
Native 9:16 hooks (H01, H03) + 16:9 film clips cropped to 9:16 on the speaker's face, big captions,
hook line on top, "FULL MOVIE - LINK BELOW" pill and the end card from the film 2 Shorts.
Usage: python3 short_fire.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "western_stagecoach_bride"))
import shorts_vertical as sv  # noqa: E402

SRC = "/mnt/user-data/uploads/stagecoach_bride/film3_barn_storm"
OUT = "/home/claude/wbs_edit/shorts"
W, HH = sv.W, sv.HH
GRADE = "eq=contrast=1.05:saturation=1.15:gamma=1.13:brightness=0.03"
NAME = "short_barn_ranger"
HOOK = "THEY CAME FOR HER BABY…\nWRONG RANCH."

# (id, file, in, out, crop centre as fraction of width or None for native 9:16, caption line, extra post filter)
SEQ = [
    ("H01", "flow/H01.mp4", 2.3, 4.9, None, "May we sleep in your barn, mister?", ""),
    ("C02", "src/visuals/video/C02.mp4", 0.0, 2.4, 0.60, "No, ma'am.", ""),
    ("C04", "src/visuals/video/C04.mp4", 0.0, 2.1, 0.52, "You'll sleep in the house.", ""),
    ("C05", "src/visuals/video/C05.mp4", 0.0, 2.4, 0.38, "Does he bite, Mama?", ""),
    ("C06", "flow/C06.mp4", 0.97, 3.37, 0.50, "Only on Sundays.", ""),
    ("C07", "flow/C07.mp4", 4.2, 8.0, 0.50, "Five hundred dollars for the boy.",
     "eq=brightness=-0.13:saturation=0.75:gamma=0.85,colorbalance=bs=0.10:bm=0.05:rs=-0.05"),
    ("C09", "src/visuals/video/C09.mp4", 0.0, 2.4, 0.47, "The woman doesn't matter.", ""),
    ("H03", "src/visuals/video/H03.mp4", 0.0, 5.75, None, "Captain Harlan. Company D. Texas Rangers.", ""),
]
MUSIC = f"{SRC}/src/audio/music/M01.mp3"


def captions(line, L):
    parts = sv.chunks(line)
    a, b = 0.15, max(0.6, L - 0.35)
    tot = sum(len(p) for p in parts)
    out, t = [], a
    for p in parts:
        dt = (b - a) * len(p) / tot
        out.append((t, t + dt, p)); t += dt
    return out


def vf(crop, post):
    if crop is None:
        v = f"scale={W}:{HH}:flags=lanczos,eq=contrast=1.04:saturation=1.08"
    else:
        cw = 405
        x = int(min(max(crop * 1280 - cw / 2, 0), 1280 - cw))
        v = f"crop={cw}:720:{x}:0,scale={W}:{HH}:flags=lanczos,unsharp=5:5:0.6,{GRADE}"
    if post:
        v += "," + post
    return v + ",fps=24,setsar=1"


def build():
    tmp = f"{OUT}/{NAME}_tmp"
    os.makedirs(tmp, exist_ok=True)
    parts = []
    for k, (cid, f, a, b, crop, line, post) in enumerate(SEQ):
        L = b - a
        caps = captions(line, L)
        events = sorted({0.0, L, *[c0 for c0, _, _ in caps], *[min(L, c1) for _, c1, _ in caps]})
        inputs = ["-ss", f"{a:.3f}", "-t", f"{L:.3f}", "-i", f"{SRC}/{f}"]
        fc, prev, j = [f"[0:v]{vf(crop, post)}[v0]"], "[v0]", 0
        for i in range(len(events) - 1):
            t0, t1 = events[i], events[i + 1]
            if t1 - t0 < 0.02:
                continue
            mid = (t0 + t1) / 2
            txt = next((c for c0, c1, c in caps if c0 <= mid < c1), "")
            img = f"{tmp}/c{k:02d}_{j:02d}.png"
            sv.png(img, HOOK, txt, False)
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
    # end card on the frozen last frame
    endpng, endmp4 = f"{tmp}/end.png", f"{tmp}/end.mp4"
    sv.png(endpng, HOOK, "", True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", parts[-1], "-frames:v", "1",
                    f"{tmp}/last.png"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", "3", "-i", f"{tmp}/last.png", "-i", endpng,
                    "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=48000:cl=stereo",
                    "-filter_complex", "[0:v]fps=24,format=yuv420p[a];[a][1:v]overlay=0:0[o]", "-map", "[o]",
                    "-map", "2:a", "-t", "3", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", endmp4],
                   check=True)
    parts.append(endmp4)
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in parts)
    joined = f"{tmp}/joined.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-c", "copy", joined], check=True)
    T = sv.dur(joined)
    out = f"{OUT}/{NAME}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-i", MUSIC, "-filter_complex",
                    f"[1:a]volume=0.22,afade=t=out:st={T - 2:.2f}:d=2,atrim=0:{T:.2f}[m];"
                    f"[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-2[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", out], check=True)
    print(out, round(sv.dur(out), 1), "s")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build()
