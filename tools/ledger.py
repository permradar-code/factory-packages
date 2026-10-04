"""usage: python tools/ledger.py clip C11 credits=12 takes=1 audio=1 note="..." [frame_tries=3]
        python tools/ledger.py image I16 note="..."
Updates manifest.json scenes (replaces an entry with the same shot_id) and flow_credits_spent/left."""
import json, sys, os
W = r"C:\Users\permr\fl_work\wwp"; p = os.path.join(W, "manifest.json")
m = json.load(open(p, encoding="utf-8"))
kind, sid = sys.argv[1], sys.argv[2]
kv = dict(a.split("=", 1) for a in sys.argv[3:])
if kind == "clip":
    e = {"shot_id": sid, "type": "video", "video": f"visuals/video/{sid}.mp4", "duration": int(kv.get("dur", 0)) or None,
         "first_frame": f"visuals/images/{sid}_first.png", "has_audio": kv.get("audio", "1") == "1", "dialogue_ok": None,
         "takes": int(kv.get("takes", 1)), "credits": int(kv.get("credits", 0)), "frame_tries": int(kv.get("frame_tries", 1)), "note": kv.get("note", "")}
else:
    e = {"shot_id": sid, "type": "image", "image": f"visuals/images/{sid}.png", "note": kv.get("note", ""), "tool": "Gemini",
         "original": "2752x1536 (kept locally in _variants, not in git); delivered 1280x720"}
m["scenes"] = [s for s in m["scenes"] if s["shot_id"] != sid] + [e]
if "spent_extra" in kv:
    m["flow_credits_spent"] += int(kv["spent_extra"]); m["flow_credits_left"] -= int(kv["spent_extra"])
elif kind == "clip" and kv.get("count", "1") == "1":
    m["flow_credits_spent"] += e["credits"]; m["flow_credits_left"] -= e["credits"]
json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("spent", m["flow_credits_spent"], "left", m["flow_credits_left"])
