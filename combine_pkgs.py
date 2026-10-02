#!/usr/bin/env python3
"""Merge a base package with a fix-pass package into one montage package.

usage: combine_pkgs.py <base_pkg> <fix_pkg> <out_pkg> --voice base|fix --images-as id,id --drop-video id,id
- visuals: fix package wins for every shot it contains; base for the rest
- voice/words: taken from --voice package; every shot start re-aligned on those words by its narration cue
- music: base package
"""
import json
import re
import shutil
import sys
from pathlib import Path


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def find_cue(words, cue, start_idx):
    target = [norm(x) for x in cue.split() if norm(x)]
    toks = [norm(w["word"]) for w in words]
    # whisper may split "C-130" into "C","130": compare on concatenated strings
    joined_target = "".join(target)
    for i in range(start_idx, len(words)):
        acc = ""
        for j in range(i, min(len(words), i + len(target) + 4)):
            acc += toks[j]
            if acc == joined_target:
                return i, j + 1
            if not joined_target.startswith(acc):
                break
    return None, start_idx


def main():
    base, fix, out = map(Path, sys.argv[1:4])
    args = sys.argv[4:]
    opt = {args[i]: args[i + 1] for i in range(0, len(args), 2)}
    voice_pkg = fix if opt.get("--voice") == "fix" else base
    as_images = set(filter(None, opt.get("--images-as", "").split(",")))
    drop_video = set(filter(None, opt.get("--drop-video", "").split(",")))

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    bm = json.loads((base / "manifest.json").read_text())
    fm = json.loads((fix / "manifest.json").read_text())
    fix_scenes = {s["shot_id"]: s for s in fm["scenes"]}
    words = json.loads((voice_pkg / "timings/words.json").read_text())
    base_input = json.loads((base / "input.json").read_text())
    cues = {s["id"]: s["narration_cue"] for s in base_input["shots"]}

    for rel in ("audio/narration.wav", "timings/words.json"):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(voice_pkg / rel, out / rel)
    if bm.get("music"):
        (out / bm["music"]).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(base / bm["music"], out / bm["music"])
    inp = dict(base_input)
    inp["script"] = json.loads((voice_pkg / "input.json").read_text())["script"]
    (out / "input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=1))

    scenes, idx, report = [], 0, []
    for sc in sorted(bm["scenes"], key=lambda s: s["index"]):
        sid = sc["shot_id"]
        src_pkg, src = (fix, fix_scenes[sid]) if sid in fix_scenes else (base, sc)
        new = {"index": sc["index"], "shot_id": sid, "image": None, "video": None}
        for kind in ("image", "video"):
            rel = src.get(kind)
            if not rel or (kind == "video" and (sid in drop_video or sid in as_images)):
                continue
            dest = f"visuals/{'images' if kind == 'image' else 'video'}/{sid}{Path(rel).suffix}"
            (out / dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_pkg / rel, out / dest)
            new[kind] = dest
        i, idx_next = find_cue(words, cues[sid], idx)
        if i is None:
            new["start"] = None
        else:
            new["start"] = 0.0 if sc["index"] == 1 else float(words[i]["start"])
            idx = idx_next
        new["source"] = "fix" if src_pkg == fix else "base"
        scenes.append(new)
        report.append((sid, new["source"], new["start"], "video" if new["video"] else "image"))
    # interpolate missing starts
    for k, s in enumerate(scenes):
        if s["start"] is None:
            prev = next((x["start"] for x in reversed(scenes[:k]) if x["start"] is not None), 0.0)
            nxt = next((x["start"] for x in scenes[k + 1:] if x["start"] is not None), prev + 2)
            s["start"] = (prev + nxt) / 2
    manifest = {"voice": "audio/narration.wav", "music": bm.get("music"), "scenes": scenes}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    for r in report:
        print(*r)


if __name__ == "__main__":
    main()
