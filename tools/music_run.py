"""Sequential music run with a usage counter logged after every cue. Stops if credits left < LIMIT.
Run from the package folder: python tools/music_run.py   (needs music_elevenlabs.py + music_cues.json next to it)"""
import json, os, subprocess, sys, time, urllib.request
LIMIT = 3000
CUES = ["M01"] + ["M%02d" % i for i in range(3, 14)]
LOG = os.path.join("audio", "music", "music_log.json")
def sub():
    r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]})
    s = json.load(urllib.request.urlopen(r, timeout=60)); return s["character_count"], s["character_limit"]
def stable():
    prev = None
    for _ in range(8):
        cur = sub()[0]
        if cur == prev: return cur
        prev = cur; time.sleep(6)
    return prev
log = json.load(open(LOG, encoding="utf-8"))
if "M02" in log and "counter_after" not in log["M02"]:
    log["M02"]["counter_after"] = 4815; log["M02"]["credits_spent"] = 275; log["M02"]["note"] = "credits inferred from counter delta"
before = stable()
for c in CUES:
    if os.path.exists(os.path.join("audio", "music", c + ".mp3")):
        print("skip", c); continue
    left = sub()[1] - before
    if left < LIMIT:
        print(f"STOP before {c}: left {left} < {LIMIT}"); break
    t = time.strftime("%H:%M:%S")
    p = subprocess.run([sys.executable, "music_elevenlabs.py", "--only", c], capture_output=True, text=True)
    print(c, p.stdout.strip(), p.stderr.strip()[:300], flush=True)
    if p.returncode != 0: print("FAILED, stopping"); break
    after = stable()
    log = json.load(open(LOG, encoding="utf-8"))
    log[c].update({"counter_before": before, "counter_after": after, "credits_spent": after - before, "time": t})
    json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  {c}: spent {after-before}, used {after}, left {sub()[1]-after}", flush=True)
    before = after
