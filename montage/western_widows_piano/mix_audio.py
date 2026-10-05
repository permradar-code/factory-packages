#!/usr/bin/env python3
"""Mix narration, clip dialogue and music for The Widow's Piano; mux with video_only.mp4."""
import json, subprocess, numpy as np, os

SR = 48000
M = "/home/claude/montage"
PKG = "/home/claude/wwp_pkg"
EDL = json.load(open(f"{M}/edl.json"))
ev_all = EDL["events"]
for _i, _ev in enumerate(ev_all):
    _ev["seg"] = f"{M}/seg/{_i:03d}_{_ev['id']}.mp4"

def probe(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

def load(p, t=None):
    cmd = ["ffmpeg", "-v", "error", "-i", p]
    if t: cmd += ["-t", str(t)]
    raw = subprocess.run(cmd + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def active_rms(x):
    m = x.mean(1); hop = SR // 20; n = len(m) // hop
    if n == 0: return 1e-4
    r = np.sqrt((m[:n*hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    act = r[r > r.max() * 0.1]
    return float(np.sqrt((act ** 2).mean())) if len(act) else float(r.mean())

def db(v): return 10 ** (v / 20)

# real segment starts (frame-accurate) from the rendered segments
t = 0.0
for ev in ev_all:
    ev["rstart"] = t
    ev["rdur"] = probe(ev["seg"])
    if ev["kind"] == "narration":
        for im in ev["images"]:
            im["rstart"] = t + (im["start"] - ev["start"])
    t += ev["rdur"]
TOTAL = t
N = int(TOTAL * SR) + SR
voice = np.zeros((N, 2), np.float32)   # narration + dialogue
music = np.zeros((N, 2), np.float32)
vact = np.zeros(N, np.float32)          # voice activity mask (1 = someone speaks)
dialog_bed = np.zeros(N, np.float32)    # 1 during clips (ambient keeps music a bit lower)

def put(buf, x, start):
    s = int(start * SR); e = min(N, s + len(x))
    buf[s:e] += x[:e - s]

def fade(x, fi=0.03, fo=0.03):
    a = int(fi * SR); b = int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None]
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x

TARGET = db(-20)  # active speech RMS
for ev in ev_all:
    if ev["kind"] == "narration":
        x = load(ev["audio"]); x *= TARGET / active_rms(x)
        st = ev["rstart"] + 0.4
        put(voice, x, st); vact[int(st*SR):int(st*SR)+len(x)] = 1
    elif ev["kind"] == "image" and ev.get("line_audio"):
        x = load(ev["line_audio"]); x *= TARGET / active_rms(x)
        st = ev["rstart"] + 0.4
        put(voice, x, st); vact[int(st*SR):int(st*SR)+len(x)] = 1
    elif ev["kind"] == "clip":
        x = fade(load(ev["file"], ev["dur"]), 0.02, 0.12)
        if ev["dialogue"]:
            x *= TARGET / active_rms(x)
            s = int(ev["rstart"] * SR); vact[s:s+len(x)] = 1
        else:
            x *= db(-24) / max(active_rms(x), 1e-4)   # ambient-only clips
        put(voice, x, ev["rstart"])
        dialog_bed[int(ev["rstart"]*SR):int((ev["rstart"]+ev["rdur"])*SR)] = 1

# ---- music cues anchored to events
def ev_start(eid, img=None, offset=0.0):
    for ev in ev_all:
        if ev["id"] == eid:
            if img:
                return [im for im in ev["images"] if im["id"] == img][0]["rstart"] + offset
            return ev["rstart"] + offset
    raise KeyError(eid)

cues = [("M01", ev_start("C01")), ("M02", ev_start("T01")), ("M03", ev_start("N01", offset=38)),
        ("M04", ev_start("N02")), ("M05", ev_start("C11")), ("M06", ev_start("N03", img="I31")),
        ("M07", ev_start("N04")), ("M08", ev_start("C18")), ("M09", ev_start("N06")),
        ("M10", ev_start("N07a")), ("M11", ev_start("N07b", img="I54")), ("M12", ev_start("C34")),
        ("M13", ev_start("N09"))]
XF = 2.0
for k, (cid, st) in enumerate(cues):
    end = cues[k+1][1] + XF if k + 1 < len(cues) else TOTAL
    need = end - st
    x = load(f"{PKG}/audio/music/{cid}.mp3")
    x *= db(-18) / active_rms(x)          # cue base level when nobody talks
    if len(x) < need * SR:                # loop with a 2 s crossfade
        out = x.copy()
        while len(out) < need * SR:
            o = int(XF * SR); r = np.linspace(0, 1, o)[:, None]
            out = np.concatenate([out[:-o], out[-o:] * (1 - r) + x[:o] * r, x[o:]])
        x = out
    x = x[:int(need * SR)]
    fi = 0.05 if k == 0 else XF
    x = fade(x, fi, XF if k + 1 < len(cues) else 3.0)
    put(music, x, st)

# ---- ducking: music -15 dB under speech, -6 dB under clip ambience, 0 dB otherwise
hop = SR // 100
env = np.ones(N, np.float32)
env[dialog_bed > 0] = db(-6)
env[vact > 0] = db(-15)
# smooth: fast attack (0.15 s), slow release (0.6 s)
e = env[::hop].copy(); sm = np.empty_like(e); cur = e[0]
a_att, a_rel = np.exp(-1 / (0.15 * 100)), np.exp(-1 / (0.6 * 100))
for i, v in enumerate(e):
    cur = a_att * cur + (1 - a_att) * v if v < cur else a_rel * cur + (1 - a_rel) * v
    sm[i] = cur
env = np.repeat(sm, hop)[:N]
music *= env[:, None]

mix = voice + music
peak = np.abs(mix).max()
if peak > 0.98: mix *= 0.98 / peak
mix = mix[:int(TOTAL * SR)]
wav = f"{M}/mix.wav"
import wave
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())

# loudness normalize to -14 LUFS (two-pass loudnorm) and mux
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                       "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(meas[meas.rfind("{"):meas.rfind("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
      f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
out = os.environ.get("OUT", f"{M}/widows_piano_draft.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{M}/video_only.mp4", "-i", wav, "-af", ln, "-ar", "48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print("mixed", round(TOTAL, 2), "s ->", out)
