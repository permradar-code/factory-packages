#!/usr/bin/env python3
"""Hand edit of film 2 "The Stagecoach Bride": EDL -> video segments -> audio mix -> SRT.

Usage:  python3 build.py edl|render|mix|srt|all
Env:    SRC  v1 package (clips, images, narration, music)     default /mnt/user-data/uploads/stagecoach_bride
        FIX  fix1 package (C61R, C102R, B01..B46)              default /home/claude/wsb_fix1
        WORK work dir                                           default /home/claude/wsb_edit
        W,H  output size (1920x1080), PRESET x264 preset (veryfast), OUT final mp4
Missing clips are replaced by a labelled grey placeholder so the edit can be checked before generation ends.
"""
import json, os, re, subprocess, sys, wave
from concurrent.futures import ThreadPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plan import PLAN, MUSIC, BADGE_AT  # noqa: E402

SRC = os.environ.get("SRC", "/mnt/user-data/uploads/stagecoach_bride")
FIX = os.environ.get("FIX", "/home/claude/wsb_fix1")
WORK = os.environ.get("WORK", "/home/claude/wsb_edit")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SHOT = json.load(open(os.path.join(REPO, "briefs/western_stagecoach_bride/shotlist.json"), encoding="utf-8"))
FIXSHOT = json.load(open(os.path.join(REPO, "briefs/western_stagecoach_bride/fix1/shotlist.json"), encoding="utf-8"))
LINES = {s["id"]: s.get("dialogue") or [] for s in SHOT["timeline"] + FIXSHOT["timeline"]}
# factory cut points (whisper word timings + 0.8 s tail). Not trusted where whisper heard only part of the line.
try:
    FACTORY_CUT = {e["id"]: (e["source_in"], e["source_out"])
                   for e in json.load(open(f"{SRC}/timeline/long_film_edl.json"))["events"] if e.get("kind") == "clip"}
except OSError:
    FACTORY_CUT = {}
PARTIAL = {"C11", "C42", "C62", "C66", "C73", "C87", "C105", "C61", "C102"}
FONT = os.path.join(REPO, "montage/fonts/Rye-Regular.ttf")
W, H, FPS = int(os.environ.get("W", 1920)), int(os.environ.get("H", 1080)), 24
X = 0.45          # crossfade between visuals inside a narration block
VOFF, VTAIL = 0.5, 0.9   # narrator starts 0.5 s into the block; 0.9 s of air after the last word
SR = 48000
os.makedirs(f"{WORK}/seg", exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", os.environ.get("PRESET", "veryfast"), "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-2000:])
        raise SystemExit("failed: " + " ".join(cmd[:10]))
    return r


def probe(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def has_audio(p):
    return "audio" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", p],
                                     capture_output=True, text=True).stdout


def clip_path(cid):
    for base in (FIX, SRC):
        p = f"{base}/visuals/video/{cid}.mp4"
        if os.path.exists(p):
            return p
    return None


def mono(path, start=0.0, dur=None, sr=16000):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", path]
    if dur:
        cmd += ["-t", str(dur)]
    raw = subprocess.run(cmd + ["-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def speech_span(path):
    """(first, last) second with speech energy, 20 ms frames, voice band only."""
    sr = 16000
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", "highpass=f=150,lowpass=f=4000",
                          "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = sr // 50
    n = len(x) // hop
    if n == 0:
        return None
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    thr = max(db.max() - 22, -45)
    idx = np.where(db > thr)[0]
    return (idx[0] * 0.02, (idx[-1] + 1) * 0.02) if len(idx) else None


def parse_vis(spec):
    w = None
    if "|" in spec:
        spec, w = spec.split("|"); w = float(w)
    if spec.startswith("img:"):
        iid = spec[4:]
        return {"type": "still", "id": iid, "file": f"{SRC}/visuals/images/{iid}.png", "w": w or 4.5}
    if spec.startswith("frame:"):
        cid, t = spec[6:].split("@")
        return {"type": "frame", "id": cid, "file": clip_path(cid), "t": float(t), "w": w or 4.5}
    rng = None
    if "@" in spec:
        spec, r = spec.split("@"); a, b = r.split("-"); rng = (float(a), float(b))
    f = clip_path(spec)
    d = probe(f) if f else 6.0
    a, b = rng or (0.0, d)
    return {"type": "video", "id": spec, "file": f, "in": a, "out": min(b, d), "w": w or (min(b, d) - a)}


# ------------------------------------------------------------------ EDL
def build_edl():
    events, t = [], 0.0
    for kind, eid, extra in PLAN:
        ev = {"kind": kind, "id": eid, "start": round(t, 3)}
        if kind == "clip":
            f = clip_path(eid)
            ev["file"] = f
            d = probe(f) if f else 5.0
            lines = LINES.get(eid) or []
            ev["dialogue"] = lines
            if extra:
                a, b = map(float, extra.split("-"))
            elif lines and eid in FACTORY_CUT and eid not in PARTIAL:
                # the factory's whisper cut is reliable when the transcript was complete; give it a little more air
                fa, fb = FACTORY_CUT[eid]
                a, b = fa, min(d, fb + 0.25)
                if b - a < 2.4:
                    b = min(d, a + 2.4)
                sp = speech_span(f)
                ev["speech"] = (max(fa, sp[0]) if sp else fa, min(fb, sp[1]) if sp else fb)
            elif lines and f:
                sp = speech_span(f)
                a, b = 0.0, d
                if sp:
                    a = 0.0 if sp[0] < 1.0 else max(0.0, sp[0] - 0.45)
                    b = min(d, sp[1] + 0.85)
                    if b - a < 2.4:
                        b = min(d, a + 2.4)
                ev["speech"] = sp
            else:
                a, b = 0.0, d
            ev["in"], ev["out"] = round(a, 3), round(min(b, d), 3)
            ev["dur"] = round(ev["out"] - ev["in"], 3)
            ev["audio"] = bool(f and has_audio(f))
        elif kind == "title":
            ev["text"], ev["dur"] = extra
        elif kind == "end":
            ev["dur"] = extra
        elif kind == "narr":
            spec = extra if isinstance(extra, dict) else {"vis": extra}
            src_id = spec.get("src", eid)
            audio = f"{SRC}/audio/narration/{src_id}.mp3"
            ev["audio"], ev["src"] = audio, src_id
            ev["a_from"] = float(spec.get("from", 0.0))
            ev["a_to"] = float(spec.get("to", probe(audio)))
            ev["voice_dur"] = round(ev["a_to"] - ev["a_from"], 3)
            extra = spec["vis"]
            ev["dur"] = round(VOFF + ev["voice_dur"] + VTAIL, 3)
            vis = [parse_vis(s) for s in extra]
            total_w = sum(v["w"] for v in vis)
            # visual lengths include the crossfade overlap: sum(len) - X*(n-1) = block length
            need = ev["dur"] + X * (len(vis) - 1)
            for v in vis:
                v["len"] = round(need * v["w"] / total_w, 3)
            ev["visuals"] = vis
        events.append(ev)
        t += ev["dur"]
    edl = {"total": round(t, 3), "events": events}
    json.dump(edl, open(f"{WORK}/edl.json", "w"), indent=1)
    print(f"EDL: {t/60:.2f} min, {len(events)} events")
    for ev in events:
        if ev["kind"] == "narr":
            desc = " ".join(f"{v['id']}:{v['len']:.1f}" + ("" if v["type"] != "video" or v["len"] <= v["out"] - v["in"] + 0.05 else "*") for v in ev["visuals"])
            print(f"{ev['start']:7.1f} {ev['id']:5s} {ev['dur']:5.1f}  {desc}")
        elif ev["kind"] == "clip":
            miss = "" if ev["file"] else "  MISSING"
            print(f"{ev['start']:7.1f} {ev['id']:5s} {ev['dur']:5.2f}  [{ev['in']}-{ev['out']}]{miss}")
        else:
            print(f"{ev['start']:7.1f} {ev['id']:5s} {ev['dur']:5.1f}  {ev.get('text', '')}")
    return edl


# ------------------------------------------------------------------ VIDEO
SCALE = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"


def kb(frames, k):
    """slow Ken Burns: alternate push in / drift."""
    n = max(frames - 1, 1)
    p = f"(on/{n})"
    if k % 2 == 0:
        z, x, y = f"1.0+0.08*{p}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    else:
        z, x, y = "1.08", f"(iw-iw/zoom)*{p}", "ih/2-(ih/zoom/2)"
    return (f"scale={int(W*1.5)//2*2}:{int(H*1.5)//2*2}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={int(W*1.5)//2*2}:{int(H*1.5)//2*2},zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1")


def placeholder(label, dur, out):
    txt = label.replace(":", "\\:")
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x404040:s={W}x{H}:r={FPS}:d={dur}",
         "-vf", f"drawtext=fontfile={FONT}:text='{txt}':fontsize=90:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
         *ENC, out])


def render_visual(v, out, k):
    L = v["len"]
    frames = int(round(L * FPS))
    if v["type"] in ("still", "frame"):
        if not v["file"] or not os.path.exists(v["file"]):
            return placeholder(v["id"], L, out)
        if v["type"] == "frame":
            png = f"{WORK}/seg/frame_{v['id']}.png"
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(v["t"]), "-i", v["file"], "-frames:v", "1", png])
            src = png
        else:
            src = v["file"]
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src, "-vf", kb(frames, k), "-frames:v", str(frames), *ENC, out])
        return
    if not v["file"]:
        return placeholder(v["id"], L, out)
    avail = v["out"] - v["in"]
    vf = SCALE + f",fps={FPS}"
    if L > avail + 0.04:          # stretch up to 1.25x, then hold the last frame
        f = min(L / avail, 1.25)
        vf = f"setpts={f:.4f}*PTS," + vf
        if avail * f < L:
            vf += f",tpad=stop_mode=clone:stop_duration={L - avail * f + 0.1:.3f}"
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(v["in"]), "-i", v["file"], "-vf", vf, "-t", f"{L:.3f}", "-an", *ENC, out])


def render_event(i, ev):
    out = f"{WORK}/seg/{i:03d}_{ev['id']}.mp4"
    if os.path.exists(out) and os.environ.get("FORCE") != "1":
        return out
    if ev["kind"] == "clip":
        if not ev["file"]:
            placeholder(ev["id"], ev["dur"], out)
        else:
            badge = next((off for n, off in BADGE_AT if n == ev["id"]), None)
            if badge is None:
                run(["ffmpeg", "-y", "-v", "error", "-ss", str(ev["in"]), "-i", ev["file"], "-t", f"{ev['dur']:.3f}",
                     "-vf", SCALE + f",fps={FPS}", "-an", *ENC, out])
            else:
                run(["ffmpeg", "-y", "-v", "error", "-ss", str(ev["in"]), "-i", ev["file"], "-itsoffset", str(badge),
                     "-i", f"{WORK}/badge.mov", "-filter_complex",
                     f"[0:v]{SCALE},fps={FPS}[b];[b][1:v]overlay=0:0:eof_action=pass[o]", "-map", "[o]",
                     "-t", f"{ev['dur']:.3f}", "-an", *ENC, out])
    elif ev["kind"] in ("title", "end"):
        d = ev["dur"]
        if ev["kind"] == "title":
            txt = ev["text"].replace("'", "’").replace(":", "\\:")
            big = ev["id"] == "T01"
            vf = (f"drawtext=fontfile={FONT}:text='{txt}':fontsize={int(H*(0.11 if big else 0.075))}:fontcolor=0xE8D9B5:"
                  f"x=(w-text_w)/2:y=(h-text_h)/2:alpha='if(lt(t,0.6),t/0.6,if(gt(t,{d-0.6}),({d}-t)/0.6,1))'")
            if big:
                vf += (f",drawtext=fontfile={FONT}:text='A TALE OF CEDAR BLUFF':fontsize={int(H*0.035)}:fontcolor=0xB89A6A:"
                       f"x=(w-text_w)/2:y=(h/2)+{int(H*0.1)}:alpha='if(lt(t,1.2),max(t-0.4,0)/0.8,if(gt(t,{d-0.6}),({d}-t)/0.6,1))'")
            run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x0b0806:s={W}x{H}:r={FPS}:d={d}", "-vf", vf, *ENC, out])
        else:   # end screen: the aspen wedding (bright, warm), series name on top, room for YouTube end-screen cards
            src = clip_path("B43") or clip_path("C101")
            frames = int(round(d * FPS))
            png = f"{WORK}/seg/end_bg.png"
            run(["ffmpeg", "-y", "-v", "error", "-ss", "4", "-i", src, "-frames:v", "1", png])
            vf = (kb(frames, 0) + ",eq=brightness=-0.06:saturation=0.95,"
                  f"drawtext=fontfile={FONT}:text='TALES OF CEDAR BLUFF':fontsize={int(H*0.06)}:fontcolor=0xE8D9B5:x=(w-text_w)/2:y=h*0.08:"
                  f"alpha='if(lt(t,1),t,1)',"
                  f"drawtext=fontfile={FONT}:text='Keep a light in the window':fontsize={int(H*0.035)}:fontcolor=0xB89A6A:x=(w-text_w)/2:y=h*0.08+{int(H*0.08)}:"
                  f"alpha='if(lt(t,1.6),max(t-0.6,0),1)'")
            run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", png, "-vf", vf, "-frames:v", str(frames), *ENC, out])
    elif ev["kind"] == "narr":
        parts = []
        for k, v in enumerate(ev["visuals"]):
            p = f"{WORK}/seg/{i:03d}_{ev['id']}_v{k:02d}.mp4"
            render_visual(v, p, k)
            parts.append((p, v["len"]))
        badge = next((off for n, off in BADGE_AT if n == ev["id"]), None)
        if len(parts) == 1 and badge is None:
            os.replace(parts[0][0], out)
            return out
        inputs, fc, prev, olen = [], [], "[0:v]", parts[0][1]
        for p, _ in parts:
            inputs += ["-i", p]
        for k in range(1, len(parts)):
            off = olen - X
            fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[x{k}]")
            prev, olen = f"[x{k}]", off + parts[k][1]
        if badge is not None:
            bmov = f"{WORK}/badge.mov"
            inputs += ["-itsoffset", str(badge), "-i", bmov]
            fc.append(f"{prev}[{len(parts)}:v]overlay=0:0:eof_action=pass[bo]")
            prev = "[bo]"
        if not fc:
            fc = ["[0:v]null[o]"]; prev = "[o]"
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", prev,
             "-t", f"{ev['dur']:.3f}", *ENC, out])
        for p, _ in parts:
            os.remove(p)
    return out


def render(edl):
    if not os.path.exists(f"{WORK}/badge.mov"):
        run([sys.executable, os.path.join(REPO, "montage/overlays/subscribe_badge.py"), "--out", f"{WORK}/badge.mov"])
    evs = edl["events"]
    with ThreadPoolExecutor(int(os.environ.get("JOBS", 2))) as ex:
        segs = list(ex.map(lambda a: render_event(*a), list(enumerate(evs))))
    with open(f"{WORK}/seg/list.txt", "w") as fh:
        for s in segs:
            fh.write(f"file '{s}'\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/seg/list.txt", "-c", "copy", f"{WORK}/video_only.mp4"])
    print("video:", round(probe(f"{WORK}/video_only.mp4"), 2), "s")


# ------------------------------------------------------------------ AUDIO
def load(p, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", p]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    raw = subprocess.run(cmd + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def active_rms(x):
    m = x.mean(1); hop = SR // 20; n = len(m) // hop
    if n == 0:
        return 1e-4
    r = np.sqrt((m[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    act = r[r > r.max() * 0.1]
    return max(float(np.sqrt((act ** 2).mean())) if len(act) else float(r.mean()), 1e-4)


def dbv(v):
    return 10 ** (v / 20)


def fade(x, fi=0.03, fo=0.05):
    a, b = int(fi * SR), int(fo * SR)
    if a and len(x) > a:
        x[:a] *= np.linspace(0, 1, a)[:, None]
    if b and len(x) > b:
        x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


def real_starts(edl):
    t = 0.0
    for i, ev in enumerate(edl["events"]):
        ev["rstart"] = t
        t += probe(f"{WORK}/seg/{i:03d}_{ev['id']}.mp4")
    return t


def mix(edl):
    total = real_starts(edl)
    N = int(total * SR) + SR
    speech = np.zeros((N, 2), np.float32)
    amb = np.zeros((N, 2), np.float32)
    music = np.zeros((N, 2), np.float32)
    vact = np.zeros(N, np.float32)
    clipbed = np.zeros(N, np.float32)

    def put(buf, x, st):
        s = int(st * SR); e = min(N, s + len(x))
        if e > s:
            buf[s:e] += x[:e - s]

    TARGET = dbv(-20)
    for ev in edl["events"]:
        if ev["kind"] == "narr":
            x = fade(load(ev["audio"], ev.get("a_from", 0.0), ev["voice_dur"]), 0.01, 0.12); x *= TARGET / active_rms(x)
            st = ev["rstart"] + VOFF
            put(speech, x, st); vact[int(st * SR):int(st * SR) + len(x)] = 1
            # quiet natural ambience of the b-roll under the narrator
            t = ev["rstart"]
            for k, v in enumerate(ev["visuals"]):
                if v["type"] == "video" and v["file"] and has_audio(v["file"]):
                    L = min(v["len"], v["out"] - v["in"])
                    y = fade(load(v["file"], v["in"], L), 0.3, 0.3)
                    y *= dbv(-34) / active_rms(y)
                    put(amb, y, t)
                t += v["len"] - X
        elif ev["kind"] == "clip" and ev["file"] and ev["audio"]:
            x = fade(load(ev["file"], ev["in"], ev["dur"]), 0.02, 0.15)
            if ev["dialogue"]:
                x *= TARGET / active_rms(x)
                put(speech, x, ev["rstart"])
                s = int(ev["rstart"] * SR); vact[s:s + len(x)] = 1
            else:
                x *= dbv(-23) / active_rms(x)
                put(amb, x, ev["rstart"])
            clipbed[int(ev["rstart"] * SR):int((ev["rstart"] + ev["dur"]) * SR)] = 1

    starts = {ev["id"]: ev["rstart"] for ev in edl["events"]}
    cues = [(c, starts[a] + o) for c, a, o in MUSIC]
    XF = 2.0
    for k, (cid, st) in enumerate(cues):
        end = cues[k + 1][1] + XF if k + 1 < len(cues) else total
        need = end - st
        x = load(f"{SRC}/audio/music/{cid}.mp3")
        x *= dbv(-18) / active_rms(x)
        while len(x) < need * SR:
            o = int(XF * SR); r = np.linspace(0, 1, o)[:, None]
            base = load(f"{SRC}/audio/music/{cid}.mp3"); base *= dbv(-18) / active_rms(base)
            x = np.concatenate([x[:-o], x[-o:] * (1 - r) + base[:o] * r, base[o:]])
        x = fade(x[:int(need * SR)].copy(), 0.05 if k == 0 else XF, XF if k + 1 < len(cues) else 4.0)
        put(music, x, st)
    for ev in edl["events"]:             # silence the score under the title cards' first beat? keep; louder on end screen
        if ev["kind"] == "end":
            s = int(ev["rstart"] * SR)
            music[s:] *= dbv(3)

    hop = SR // 100
    env = np.ones(N, np.float32)
    env[clipbed > 0] = dbv(-7)
    env[vact > 0] = dbv(-15)
    e = env[::hop].copy(); sm = np.empty_like(e); cur = e[0]
    a_att, a_rel = np.exp(-1 / (0.15 * 100)), np.exp(-1 / (0.6 * 100))
    for i, v in enumerate(e):
        cur = a_att * cur + (1 - a_att) * v if v < cur else a_rel * cur + (1 - a_rel) * v
        sm[i] = cur
    env = np.repeat(sm, hop)[:N]
    m = speech + amb + music * env[:, None]
    pk = np.abs(m).max()
    if pk > 0.98:
        m *= 0.98 / pk
    m = m[:int(total * SR)]
    wav = f"{WORK}/mix.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(m, -1, 1) * 32767).astype(np.int16).tobytes())
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                           "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(meas[meas.rfind("{"):meas.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    out = os.environ.get("OUT", f"{WORK}/stagecoach_bride.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", f"{WORK}/video_only.mp4", "-i", wav, "-af", ln, "-ar", "48000",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    json.dump(edl, open(f"{WORK}/edl_timed.json", "w"), indent=1)
    print("mixed", round(total, 2), "s ->", out)


# ------------------------------------------------------------------ SUBTITLES
def wrap(text, width=42):
    if len(text) <= width:
        return text
    best = min((max(i, len(text) - i - 1), i) for i, c in enumerate(text) if c == " ")
    return text[:best[1]] + "\n" + text[best[1] + 1:]


def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt(edl):
    if "rstart" not in edl["events"][0]:
        real_starts(edl)
    cues = []
    for ev in edl["events"]:
        if ev["kind"] == "narr":
            al = json.load(open(f"{SRC}/audio/narration/{ev.get('src', ev['id'])}.alignment.json"))["alignment"]
            words, cur, ws, we = [], "", None, None
            for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
                if c.isspace():
                    if cur:
                        words.append((cur, ws, we)); cur = ""
                    continue
                if not cur:
                    ws = a
                cur += c; we = b
            if cur:
                words.append((cur, ws, we))
            a0 = ev.get("a_from", 0.0)
            words = [(w, a - a0, b - a0) for w, a, b in words if a >= a0 - 0.05 and b <= ev.get("a_to", 1e9) + 0.05]
            base = ev["rstart"] + VOFF
            group = []
            for w in words:
                group.append(w)
                txt = " ".join(x for x, _, _ in group)
                end_p = re.search(r"[.!?…]['\"”’]?$", w[0]) is not None
                soft = re.search(r"[,;:—]['\"”’]?$", w[0]) is not None
                if (end_p and len(txt) >= 12) or (soft and len(txt) >= 45) or len(txt) >= 76:
                    cues.append([base + group[0][1], base + group[-1][2] + 0.2, txt]); group = []
            if group:
                cues.append([base + group[0][1], base + group[-1][2] + 0.2, " ".join(x for x, _, _ in group)])
        elif ev["kind"] == "clip" and ev["dialogue"]:
            sp = ev.get("speech") or (0.2, ev["dur"])
            a = ev["rstart"] + max(0.0, sp[0] - ev["in"])
            b = ev["rstart"] + min(ev["dur"], sp[1] - ev["in"] + 0.3)
            txt = " ".join(d["line"] for d in ev["dialogue"])
            cues.append([a, max(b, a + 1.2), txt])
    cues.sort()
    for k in range(len(cues) - 1):
        cues[k][1] = min(cues[k][1], cues[k + 1][0] - 0.04)
    out = os.environ.get("SRT", f"{WORK}/stagecoach_bride.en.srt")
    with open(out, "w", encoding="utf-8") as fh:
        for k, (a, b, t) in enumerate(cues, 1):
            fh.write(f"{k}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n\n")
    print("srt:", len(cues), "cues ->", out)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    edl = build_edl() if step in ("edl", "all") else json.load(open(f"{WORK}/edl.json"))
    if step in ("render", "all"):
        render(edl)
    if step in ("mix", "all"):
        mix(edl)
    if step in ("srt", "all"):
        srt(edl)
