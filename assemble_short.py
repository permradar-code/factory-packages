#!/usr/bin/env python3
"""Assemble a vertical Short from a factory package: clips + voice + music + word-synced captions.

usage: assemble_short.py <package_dir> <out.mp4> [--config cfg.json]
cfg: {"replace": {"Elblong": "Elbląg"}, "labels": [{"text": "...", "start": 5.0, "end": 7.5}],
      "music_db": -17, "sfx": [{"kind": "whoosh"|"splash", "at": 2.1}], "tail": 0.4}
"""
import json
import re
import subprocess
import sys
from pathlib import Path

W, H, FPS = 1080, 1920, 30
FONT = "Inter Display Black"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(map(str, cmd))[:400]}\n{r.stderr[-2000:]}")
    return r.stdout


def probe_duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_escape(text):
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


_FONT_OBJ = None


def text_width(text):
    """Conservative on-screen width (px) of caption text in the Cap style."""
    global _FONT_OBJ
    if _FONT_OBJ is None:
        from PIL import ImageFont
        _FONT_OBJ = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 100)
    # libass renders Fontsize 100 at ~0.8 of a PIL 100px em (calibrated on rendered frames)
    return _FONT_OBJ.getlength(text.upper()) * 0.8 * 1.08 + 30  # highlight scale + outline


CAP_MAX_W = 940  # px of 1080 frame, ~70 px side margins


def caption_groups(words, max_words=3, max_chars=16):
    groups, cur = [], []
    for w in words:
        if cur and text_width(" ".join(x["text"] for x in cur + [w])) > CAP_MAX_W:
            groups.append(cur); cur = []
        cur.append(w)
        text = " ".join(x["text"] for x in cur)
        ends_sentence = re.search(r"[.!?,;:]$", w["raw"])
        if len(cur) >= max_words or len(text) >= max_chars or ends_sentence:
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    return groups


def build_ass(words, labels, total, path):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,5,60,60,0
Style: Label,{FONT},72,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4000000,-1,0,0,0,100,100,2,0,3,18,0,8,60,60,210
Style: Stat,{FONT},150,&H0000F2FF,&H0000F2FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,9,4,8,60,60,330
Style: End,{FONT},92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1,0,1,7,4,5,60,60,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    groups = caption_groups(words)
    y = int(H * 0.66)
    for gi, group in enumerate(groups):
        g_start = group[0]["start"]
        g_end = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else min(total, group[-1]["end"] + 0.6)
        width = text_width(" ".join(x["text"] for x in group))
        sc = min(100, int(100 * CAP_MAX_W / width)) if width > 0 else 100
        for wi, w in enumerate(group):
            s = w["start"] if wi else g_start
            e = group[wi + 1]["start"] if wi + 1 < len(group) else g_end
            if e <= s:
                continue
            parts = []
            for k, x in enumerate(group):
                word = ass_escape(x["text"].upper())
                if k == wi:
                    hi = int(sc * 1.08)
                    parts.append(f"{{\\c&H00F2FF&\\fscx{hi}\\fscy{hi}}}" + word + f"{{\\c&HFFFFFF&\\fscx{sc}\\fscy{sc}}}")
                else:
                    parts.append(word)
            pop = (f"{{\\t(0,80,\\fscx{int(sc*1.04)}\\fscy{int(sc*1.04)})\\t(80,160,\\fscx{sc}\\fscy{sc})}}" if wi == 0 else "")
            lines.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{{\\an5\\pos({W//2},{y})\\fscx{sc}\\fscy{sc}}}{pop}{' '.join(parts)}")
    for lab in labels:
        style = lab.get("style", "Label")
        fx = "{\\fad(100,150)\\fscx70\\fscy70\\t(0,180,\\fscx100\\fscy100)}" if style == "Stat" else "{\\fad(120,120)}"
        if style == "End":
            fx = "{\\fad(250,400)}"
        if float(lab["start"]) <= 0.01:
            fx = "{\\fad(0,150)}"  # visible on the very first frame (feed preview)
        text = ass_escape(lab["text"]).replace("\n", "\\N")
        lines.append(f"Dialogue: 2,{ass_time(lab['start'])},{ass_time(lab['end'])},{style},,0,0,0,,{fx}{text}")
    Path(path).write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def sfx(kind, out):
    if kind == "whoosh":
        flt = "highpass=f=600,lowpass=f=5000,afade=t=in:d=0.18,afade=t=out:st=0.18:d=0.22,volume=0.55"
        dur = 0.4
    else:  # splash
        flt = "lowpass=f=2500,highpass=f=120,afade=t=in:d=0.02,afade=t=out:st=0.08:d=0.9,volume=0.9"
        dur = 1.0
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"anoisesrc=d={dur}:c=pink:r=48000:a=0.8",
         "-af", flt, "-ac", "2", str(out)])


def main():
    pkg = Path(sys.argv[1]); out = Path(sys.argv[2])
    cfg = {}
    if "--config" in sys.argv:
        cfg = json.loads(Path(sys.argv[sys.argv.index("--config") + 1]).read_text(encoding="utf-8"))
    work = out.parent / (out.stem + "_work"); work.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
    raw_words = json.loads((pkg / "timings/words.json").read_text(encoding="utf-8"))
    voice = pkg / manifest["voice"]
    voice_len = probe_duration(voice)
    tail = float(cfg.get("tail", 0.35))
    total = voice_len + tail

    scenes = sorted(manifest["scenes"], key=lambda s: s["index"])
    # Cut points: scene i spans from its start to next scene start; first starts at 0; last ends at total.
    bounds = []
    for i, sc in enumerate(scenes):
        start = 0.0 if i == 0 else float(sc["start"])
        end = float(scenes[i + 1]["start"]) if i + 1 < len(scenes) else total
        bounds.append((start, end))

    clips = []
    for i, (sc, (s, e)) in enumerate(zip(scenes, bounds)):
        dur = max(0.3, e - s)
        src = pkg / (sc.get("video") or sc["image"])
        clip = work / f"clip_{i:02d}.mp4"
        zoom = "scale=1188:2112:flags=lanczos,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2"
        ov = cfg.get("scene_overrides", {}).get(sc["shot_id"], {})
        if sc.get("video"):
            src_start = float(ov.get("src_start", 0.0))
            src_end = ov.get("src_end")
            src_len = (float(src_end) if src_end is not None else probe_duration(src)) - src_start
            speed = min(1.0, src_len / dur) if src_len < dur else 1.0
            if ov.get("push"):
                frames = max(1, int(dur * FPS))
                amount = float(ov.get("push"))
                zoom = (f"scale=1080:1920:flags=lanczos,zoompan=z='1.04+{amount}*on/{frames}':d=1:"
                        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}")
            vf = (f"setpts=PTS/{speed},fps={FPS},{zoom},"
                  f"tpad=stop_mode=clone:stop_duration={dur},trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p")
            trim_in = ["-ss", str(src_start)] + (["-to", str(src_end)] if src_end is not None else [])
            run(["ffmpeg", "-y", "-v", "error", *trim_in, "-i", str(src), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", str(clip)])
        else:
            frames = max(2, int(round(dur * FPS)))
            mode = ov.get("move") or ["in", "pan_up", "out", "pan_down"][i % 4]
            zmax = float(ov.get("zoom", 0.14))
            p = f"(on/{frames - 1})"
            if mode == "in":
                z, x, y = f"1+{zmax}*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
            elif mode == "out":
                z, x, y = f"1+{zmax}-{zmax}*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
            elif mode == "pan_up":
                z, x, y = f"{1 + zmax}", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(1-{p})"
            else:  # pan_down
                z, x, y = f"{1 + zmax}", "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*{p}"
            vf = (f"scale=2160:3840:flags=lanczos,setsar=1,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
            run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-crf", "17", "-preset", "medium", str(clip)])
        clips.append(clip)

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
    video = work / "video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(video)])

    # Captions
    replace = cfg.get("replace", {})
    words = []
    script = ""
    if (pkg / "input.json").is_file():
        script = json.loads((pkg / "input.json").read_text(encoding="utf-8")).get("script", "")
    tokens = script.split()
    norm = lambda x: re.sub(r"[^\w]", "", x.lower())
    j = 0
    punct_for = []
    for w in raw_words:
        target, found = norm(str(w["word"])), None
        for k in range(j, min(j + 6, len(tokens))):
            if norm(tokens[k]) == target:
                found = k; break
        if found is not None:
            j = found + 1
            m = re.search(r"[.,;:!?]+$", tokens[found])
            punct_for.append(m.group(0) if m else "")
        else:
            punct_for.append("")
    for w, punct in zip(raw_words, punct_for):
        raw = str(w["word"]).strip() + punct
        text = raw
        for k, v in replace.items():
            text = re.sub(re.escape(k), v, text, flags=re.I)
        text = re.sub(r"[.,;:?]+$", "", text)
        if text:
            words.append({"text": text, "raw": raw, "start": float(w["start"]), "end": float(w["end"])})
    for a, b, joined in cfg.get("merge", []):
        merged, k = [], 0
        while k < len(words):
            if k + 1 < len(words) and words[k]["text"].lower() == a.lower() and words[k + 1]["text"].lower() == b.lower():
                merged.append({**words[k + 1], "text": joined, "start": words[k]["start"]}); k += 2
            else:
                merged.append(words[k]); k += 1
        words = merged
    ass = work / "captions.ass"
    build_ass(words, cfg.get("labels", []), total, ass)

    # Audio: voice + ducked music + sfx
    inputs = ["-i", str(video), "-i", str(voice)]
    filters = ["[1:a]aresample=48000,apad=whole_dur=%f,volume=1.15,asplit=2[v][vsc]" % total]
    mix = ["[v]"]
    idx = 2
    music = manifest.get("music")
    if music and (pkg / music).is_file():
        inputs += ["-stream_loop", "-1", "-i", str(pkg / music)]
        db = float(cfg.get("music_db", -17))
        filters.append(f"[{idx}:a]aresample=48000,atrim=0:{total},volume={db}dB,afade=t=out:st={total-0.6}:d=0.6[m]")
        filters.append("[m][vsc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[md]")
        mix.append("[md]"); idx += 1
    else:
        filters.append("[vsc]anullsink")
    for k, fx in enumerate(cfg.get("sfx", [])):
        path = work / f"sfx_{k}.wav"; sfx(fx["kind"], path)
        inputs += ["-i", str(path)]
        ms = int(float(fx["at"]) * 1000)
        filters.append(f"[{idx}:a]adelay={ms}|{ms}[s{k}]"); mix.append(f"[s{k}]"); idx += 1
    filters.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,atrim=0:{total}[a]")
    ass_path = str(ass).replace(":", "\\:")
    filters.append(f"[0:v]ass='{ass_path}'[vo]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
         "-map", "[vo]", "-map", "[a]", "-t", f"{total}", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    print(json.dumps({"out": str(out), "duration": round(total, 2), "scenes": [round(e - s, 2) for s, e in bounds]}))


if __name__ == "__main__":
    main()
