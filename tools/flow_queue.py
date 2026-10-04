"""Builds _variants/queue_flow.json for the Flow image/video pipeline from shotlist.json.
Each clip: refs (names of uploaded jpgs in attach order), prompt (frame prompt with ref prefix), video_prompt, duration.
usage: python tools/flow_queue.py  (optional override: ORDER = {'C11': [...]})"""
import json, os
W = r"C:\Users\permr\fl_work\wwp"
SL = json.load(open(os.path.join(W, "_variants", "brief", "shotlist.json"), encoding="utf-8-sig"))
NAMES = {k: v["name"] for k, v in {**SL["characters"], **SL["props"], **SL["locations"]}.items()}
ORDER = {"C11": ["LOC_RANCH", "CHAR_CLARA_front", "CHAR_CLARA_full"]}
def label(n):
    if n.endswith("_front"): return NAMES[n[:-6]] + " (face)"
    if n.endswith("_full"): return NAMES[n[:-5]] + " (full body)"
    return NAMES[n]
out = []
for s in SL["timeline"]:
    if s.get("type") != "clip": continue
    ids = s.get("refs") or []
    names = []
    for rid in ids:
        if rid.startswith("CHAR_"): names += [rid + "_front", rid + "_full"]
        else: names.append(rid)
    names = ORDER.get(s["id"], names)
    prefix = ""
    if names:
        prefix = "Use the attached reference images, in this order: " + "; ".join(f"{i}) {label(n)}" for i, n in enumerate(names, 1)) + ". Keep every person's face, hair and clothing and every place and prop exactly as in the references. "
    t = prefix + s["start_frame_full_prompt"]
    if "CHAR_MARSHAL" in ids: t += " The marshal's star badge is a plain five-pointed silver star badge, no lettering, no engraving."
    if "PROP_PIANO" in ids: t += " The piano has no nameplate and no lettering anywhere."
    t += " All signs, papers and books show no readable writing."
    out.append({"id": s["id"], "refs": [n + ".jpg" for n in names], "prompt": t, "video_prompt": s["video_prompt"], "duration": s["duration_s"], "priority": s.get("priority"), "flashback": s.get("flashback", False), "credits": s.get("credits")})
json.dump(out, open(os.path.join(W, "_variants", "queue_flow.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), "clips")
