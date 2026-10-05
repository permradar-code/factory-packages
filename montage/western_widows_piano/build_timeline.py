#!/usr/bin/env python3
"""Build the edit decision list (EDL) for The Widow's Piano from the package + shotlist."""
import json, subprocess, os, numpy as np

PKG = "/home/claude/wwp_pkg"
SHOT = "/home/claude/tm/briefs/western_widows_piano/shotlist.json"
OUT = "/home/claude/montage/edl.json"

def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout.strip())

def audio_env(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    hop = sr // 20  # 50 ms
    n = len(x) // hop
    if n == 0:
        return np.array([]), 0.05
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms), 0.05

def speech_end(path):
    db, step = audio_env(path)
    if len(db) == 0:
        return None
    thr = max(db.max() - 22, -42)
    idx = np.where(db > thr)[0]
    return (idx[-1] + 1) * step if len(idx) else None

shot = json.load(open(SHOT))
man = json.load(open(f"{PKG}/manifest.json"))
skipped = {s["shot_id"] for s in man["scenes"] if s.get("type") == "skipped"}
tl = shot["timeline"]

# Epilogue (wedding) after C38, before the sign-off N10 — added after the first cut
EPILOGUE = [{"type": "narration", "id": "N09b"},
            {"type": "image", "id": "I70", "motion": "slow push in"},
            {"type": "image", "id": "I71", "motion": "slow tracking drift"},
            {"type": "image", "id": "I72", "motion": "very slow push in"}]
if os.path.exists(f"{PKG}/audio/narration/N09b.mp3") and "N09b" not in [s["id"] for s in tl]:
    k = [s["id"] for s in tl].index("C38") + 1
    tl = tl[:k] + EPILOGUE + tl[k:]

events = []   # visual events in order
i = 0
while i < len(tl):
    s = tl[i]
    t = s["type"]
    if t == "narration":
        block = {"kind": "narration", "id": s["id"], "audio": f"{PKG}/audio/narration/{s['id']}.mp3"}
        block["audio_dur"] = dur(block["audio"])
        imgs = []
        j = i + 1
        while j < len(tl) and tl[j]["type"] == "image":
            imgs.append(tl[j]); j += 1
        block["images"] = [{"id": im["id"], "file": f"{PKG}/visuals/images/{im['id']}.png", "motion": im["motion"],
                            "flashback": im.get("flashback", False)} for im in imgs]
        events.append(block)
        i = j
        continue
    if t == "image":   # image without narration ("music beat")
        events.append({"kind": "image", "id": s["id"], "file": f"{PKG}/visuals/images/{s['id']}.png",
                       "motion": s["motion"], "flashback": s.get("flashback", False), "dur": 4.0})
    elif t == "clip":
        if s["id"] in skipped:
            ev = {"kind": "image", "id": s["id"], "file": f"{PKG}/visuals/images/{s['id']}_first.png",
                  "motion": "slow push in", "flashback": False, "dur": 4.5, "skipped_clip": True,
                  "dialogue": s["dialogue"]}
            la = f"{PKG}/audio/dialogue/{s['id']}_pike_v1.mp3"
            if os.path.exists(la):
                ev["line_audio"] = la
                ev["dur"] = round(max(4.5, dur(la) + 1.3), 3)
            events.append(ev)
        else:
            f = f"{PKG}/visuals/video/{s['id']}.mp4"
            d = dur(f)
            keep = d
            if s["dialogue"]:
                e = speech_end(f)
                if e is not None:
                    keep = min(d, max(e + 0.6, 2.5))
            events.append({"kind": "clip", "id": s["id"], "file": f, "src_dur": round(d, 3), "dur": round(keep, 3),
                           "dialogue": bool(s["dialogue"]), "priority": s.get("priority")})
    elif t == "title_card":
        events.append({"kind": "title", "id": s["id"], "text": s["text"], "dur": float(s["duration_s"])})
    i += 1

# lay out times
PAD_AFTER_NARR = 0.6
MAXIMG, MINIMG = 11.0, 3.5
tcur = 0.0
for ev in events:
    ev["start"] = round(tcur, 3)
    if ev["kind"] == "narration":
        n = max(1, len(ev["images"]))
        total = ev["audio_dur"] + PAD_AFTER_NARR + 0.4   # narration starts 0.4 s into the block
        per = total / n
        if per < MINIMG:
            per = MINIMG
        t0 = tcur
        for im in ev["images"]:
            im["start"] = round(t0, 3); im["dur"] = round(per, 3); t0 += per
        ev["dur"] = round(t0 - tcur, 3)
        ev["voice_start"] = round(tcur + 0.4, 3)
    tcur += ev["dur"]

json.dump({"total": round(tcur, 2), "events": events}, open(OUT, "w"), indent=1)
nimg = sum(len(e["images"]) for e in events if e["kind"] == "narration") + sum(e["kind"] == "image" for e in events)
print(f"total {tcur/60:.1f} min, events {len(events)}, clips {sum(e['kind']=='clip' for e in events)}, images {nimg}")
for e in events:
    if e["kind"] == "narration":
        print(f"{e['start']:7.1f} N {e['id']:5s} voice {e['audio_dur']:6.1f}s  {len(e['images'])} img x {e['images'][0]['dur'] if e['images'] else 0:.1f}s")
    elif e["kind"] == "clip":
        print(f"{e['start']:7.1f} C {e['id']:5s} {e['dur']:5.2f}/{e['src_dur']:.2f}")
    else:
        print(f"{e['start']:7.1f} {e['kind'][0].upper()} {e['id']:5s} {e['dur']:.1f}")
