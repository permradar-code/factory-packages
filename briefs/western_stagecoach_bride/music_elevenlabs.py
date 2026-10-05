#!/usr/bin/env python3
"""Music for "The Widow's Piano" via the ElevenLabs Music API (POST /v1/music).

Key from the environment: ELEVENLABS_API_KEY (never hard-code it).
  python music_elevenlabs.py --check                 # credits left on the account
  python music_elevenlabs.py --only M02              # test the main theme first
  python music_elevenlabs.py                         # all cues from music_cues.json (skips existing files)
  python music_elevenlabs.py --only M06 --force --seed 7   # regenerate one cue with another seed

Output: audio/music/M01.mp3 ... and audio/music/music_log.json (model, seed, length, prompt per cue).
"""
import argparse, json, os, sys, urllib.request, urllib.error

API = "https://api.elevenlabs.io/v1"
OUT = os.path.join("audio", "music")
HERE = os.path.dirname(os.path.abspath(__file__))

def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ELEVENLABS_API_KEY is not set")
    return k

def get_json(path):
    r = urllib.request.Request(API + path, headers={"xi-api-key": key()})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())

def check():
    sub = get_json("/user/subscription")
    used, limit = sub.get("character_count", 0), sub.get("character_limit", 0)
    print(f"Plan: {sub.get('tier')}  used {used} / {limit}  ->  left {limit - used} credits")

def compose(cue, model, seed):
    body = {"prompt": cue["prompt"], "music_length_ms": int(cue["target_s"] * 1000),
            "model_id": model, "force_instrumental": bool(cue["instrumental"])}
    if seed is not None:
        body["seed"] = seed
    r = urllib.request.Request(API + "/music?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                               method="POST", headers={"xi-api-key": key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=900) as resp:
            return resp.read(), resp.headers.get("song-id"), body
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} for {cue['id']}: {e.read().decode()[:500]}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--model", default="music_v2_5", help="music_v1 | music_v2 | music_v2_5")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    cues = json.load(open(os.path.join(HERE, "music_cues.json"), encoding="utf-8"))["cues"]
    os.makedirs(OUT, exist_ok=True)
    log_path = os.path.join(OUT, "music_log.json")
    log = json.load(open(log_path, encoding="utf-8")) if os.path.exists(log_path) else {}
    for cue in cues:
        if a.only and cue["id"] not in a.only:
            continue
        if cue.get("reuse_from"):
            print("skip", cue["id"], "(reused from", cue["reuse_from"] + ")"); continue
        mp3 = os.path.join(OUT, cue["id"] + ".mp3")
        if os.path.exists(mp3) and not a.force:
            print("skip", cue["id"], "(exists)"); continue
        audio, song_id, body = compose(cue, a.model, a.seed)
        open(mp3, "wb").write(audio)
        log[cue["id"]] = {"file": mp3.replace(os.sep, "/"), "song_id": song_id, "model": a.model, "seed": a.seed,
                          "length_ms": body["music_length_ms"], "instrumental": body["force_instrumental"],
                          "covers": cue["covers"], "prompt": cue["prompt"]}
        json.dump(log, open(log_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"{cue['id']}: {len(audio)//1024} KB, target {cue['target_s']} s")

if __name__ == "__main__":
    main()
