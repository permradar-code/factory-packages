#!/usr/bin/env python3
"""Narration for "The Widow's Piano" via ElevenLabs.

Usage (key is read from the environment, never hard-code it):
  set ELEVENLABS_API_KEY=...            (Windows)   /   export ELEVENLABS_API_KEY=...  (macOS/Linux)
  python tts_elevenlabs.py --check                  # credits left + how many characters the job needs
  python tts_elevenlabs.py --voices                 # list voices on the account (pick the narrator)
  python tts_elevenlabs.py --voice VOICE_ID --only N01      # test one block first
  python tts_elevenlabs.py --voice VOICE_ID                 # all blocks (skips ones already done)

Output: audio/narration/N01.mp3 + N01.alignment.json (per-character timings, used for editing and subtitles).
"""
import argparse, base64, glob, json, os, sys, urllib.request, urllib.error

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.55, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True}
OUT = os.path.join("audio", "narration")

def req(method, path, body=None):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method,
                               headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {path}: {e.read().decode()[:500]}")

def blocks():
    files = sorted(glob.glob(os.path.join("narration", "N*.txt")))
    return [(os.path.splitext(os.path.basename(f))[0], open(f, encoding="utf-8").read().strip()) for f in files]

def check():
    sub = req("GET", "/user/subscription")
    used, limit = sub.get("character_count", 0), sub.get("character_limit", 0)
    need = sum(len(t) for _, t in blocks())
    print(f"Plan: {sub.get('tier')}  used {used} / {limit}  ->  left {limit - used}")
    print(f"This job needs about {need} characters (one take). Test block N01 = {len(blocks()[0][1])} characters.")
    if sub.get("next_character_count_reset_unix"):
        import datetime
        print("Resets:", datetime.datetime.fromtimestamp(sub["next_character_count_reset_unix"]).isoformat())

def voices():
    for v in req("GET", "/voices").get("voices", []):
        labels = ", ".join(f"{k}={val}" for k, val in (v.get("labels") or {}).items())
        print(f"{v['voice_id']}  {v['name']}  [{labels}]")

def synth(voice, only=None, force=False):
    os.makedirs(OUT, exist_ok=True)
    bl = blocks()
    for i, (bid, text) in enumerate(bl):
        if only and bid not in only:
            continue
        mp3 = os.path.join(OUT, bid + ".mp3")
        if os.path.exists(mp3) and not force:
            print("skip", bid, "(exists)"); continue
        body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS,
                "previous_text": bl[i - 1][1][-400:] if i > 0 else None,
                "next_text": bl[i + 1][1][:400] if i + 1 < len(bl) else None}
        res = req("POST", f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128", body)
        open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
        json.dump({"text": text, "voice_id": voice, "model_id": MODEL, "settings": SETTINGS,
                   "alignment": res.get("alignment"), "normalized_alignment": res.get("normalized_alignment")},
                  open(os.path.join(OUT, bid + ".alignment.json"), "w", encoding="utf-8"))
        ends = (res.get("alignment") or {}).get("character_end_times_seconds") or [0]
        print(f"{bid}: {len(text)} chars -> {ends[-1]:.1f} s")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--voices", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--force", action="store_true", help="regenerate even if the mp3 exists")
    a = ap.parse_args()
    if a.check: check()
    elif a.voices: voices()
    elif a.voice: synth(a.voice, a.only, a.force)
    else: ap.print_help()
