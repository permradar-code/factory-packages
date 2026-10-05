#!/usr/bin/env python3
"""Build English SRT subtitles for The Widow's Piano (timed to the rendered 1080p segments)."""
import json, subprocess, re, numpy as np

M = "/home/claude/montage"
PKG = "/home/claude/wwp_pkg"
EDL = json.load(open(f"{M}/edl.json"))
SHOT = {s["id"]: s for s in json.load(open("/home/claude/tm/briefs/western_widows_piano/shotlist.json"))["timeline"]}

def probe(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

def speech_span(path, limit):
    sr = 16000
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", str(limit), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = sr // 50; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n*hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    idx = np.where(db > max(db.max() - 20, -42))[0]
    return (idx[0] * 0.02, (idx[-1] + 1) * 0.02) if len(idx) else (0.0, limit)

t = 0.0
for i, ev in enumerate(EDL["events"]):
    ev["rstart"] = t
    t += probe(f"{M}/seg/{i:03d}_{ev['id']}.mp4")

cues = []  # (start, end, text)

def wrap(text, width=42):
    if len(text) <= width:
        return text
    best = None
    for i, c in enumerate(text):
        if c == " ":
            m = max(i, len(text) - i - 1)
            if best is None or m < best[0]:
                best = (m, i)
    i = best[1]
    return text[:i] + "\n" + text[i+1:]

# narration from ElevenLabs alignment
for ev in EDL["events"]:
    if ev["kind"] != "narration":
        continue
    al = json.load(open(f"{PKG}/audio/narration/{ev['id']}.alignment.json"))["alignment"]
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, ws = [], "", None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur: words.append((cur, ws, we)); cur = ""
            continue
        if not cur: ws = a
        cur += c; we = b
    if cur: words.append((cur, ws, we))
    base = ev["rstart"] + 0.4
    group = []
    def flush():
        if group:
            txt = " ".join(w for w, _, _ in group)
            cues.append([base + group[0][1], base + group[-1][2] + 0.15, txt])
            group.clear()
    for w in words:
        if group and len(" ".join(x for x, _, _ in group) + " " + w[0]) > 78:
            cut = max([k for k, g in enumerate(group) if re.search(r"[.!?,;:—]['\"”’]?$", g[0]) and k >= 2] or [len(group) - 1])
            keep = group[cut + 1:]
            del group[cut + 1:]
            flush(); group.extend(keep)
        group.append(w)
        txt = " ".join(x for x, _, _ in group)
        dur = group[-1][2] - group[0][1]
        end_punct = re.search(r"[.!?…]['\"”’]?$", w[0]) is not None
        soft = re.search(r"[,;:—]['\"”’]?$", w[0]) is not None
        if (end_punct and len(txt) >= 10) or (soft and len(txt) >= 45) or len(txt) >= 78 or dur >= 6.0:
            flush()
    flush()

# dialogue from clips (one speaker per clip) and Pike's line on the C19a still
for ev in EDL["events"]:
    lines = None
    if ev["kind"] == "clip" and ev.get("dialogue"):
        lines = SHOT[ev["id"]]["dialogue"]
        s0, s1 = speech_span(ev["file"], ev["dur"])
        start, end = ev["rstart"] + max(s0 - 0.05, 0), ev["rstart"] + min(s1 + 0.25, ev["dur"])
    elif ev["kind"] == "image" and ev.get("line_audio"):
        lines = SHOT[ev["id"]]["dialogue"]
        start = ev["rstart"] + 0.4; end = start + probe(ev["line_audio"]) + 0.2
    if not lines:
        continue
    txt = " ".join(d["line"] for d in lines)
    if end - start < 1.0: end = start + 1.0
    # long lines: split at sentence boundary into two cues
    parts = re.split(r"(?<=[.!?])\s+", txt) if len(txt) > 84 else [txt]
    merged = []
    for p_ in parts:
        if merged and (len(merged[-1]) < 24 or len(p_) < 12) and len(merged[-1]) + len(p_) < 90:
            merged[-1] += " " + p_
        else:
            merged.append(p_)
    parts = merged
    if len(parts) > 1:
        total = sum(len(p) for p in parts); t0 = start
        for p in parts:
            d = (end - start) * len(p) / total
            cues.append([t0, t0 + d, p]); t0 += d
    else:
        cues.append([start, end, txt])

cues.sort(key=lambda c: c[0])
for a, b in zip(cues, cues[1:]):          # no overlaps, small gap
    if a[1] > b[0] - 0.04: a[1] = max(a[0] + 0.5, b[0] - 0.04)

def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

with open(f"{M}/The_Widows_Piano.en.srt", "w", encoding="utf-8") as f:
    for i, (a, b, txt) in enumerate(cues, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{wrap(txt)}\n\n")
print(len(cues), "cues; last ends", ts(cues[-1][1]), "film", ts(t))
