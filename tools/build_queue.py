"""Builds the work queues for Gemini from shotlist.json: upload copies of refs (jpg 1024w) + prompts.
usage: python tools/build_queue.py  -> _variants/up/<ID>_<n>.jpg, _variants/queue_images.json, _variants/queue_frames.json"""
import json, os, subprocess, re
W = r"C:\Users\permr\fl_work\wwp"
SL = json.load(open(os.path.join(W, "_variants", "brief", "shotlist.json"), encoding="utf-8"))
REFS = os.path.join(W, "visuals", "refs"); UP = os.path.join(W, "_variants", "up"); os.makedirs(UP, exist_ok=True)
NAMES = {k: v["name"] for k, v in {**SL["characters"], **SL["props"], **SL["locations"]}.items()}
def small(src, dst):
    if not os.path.exists(dst):
        subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf","scale=1024:-1","-q:v","4",dst], check=True)
def refs_for(item_id, ids):
    files, labels = [], []
    for rid in ids or []:
        if rid.startswith("CHAR_"):
            for ang, lab in (("front","face"),("full","full body")):
                src = os.path.join(REFS, f"{rid}_{ang}.png")
                if os.path.exists(src): files.append(src); labels.append(f"{NAMES[rid]} ({lab})")
        else:
            src = os.path.join(REFS, f"{rid}.png")
            if os.path.exists(src): files.append(src); labels.append(NAMES[rid])
    out = []
    for i, src in enumerate(files, 1):
        dst = os.path.join(UP, f"{item_id}_{i}.jpg"); small(src, dst); out.append(dst)
    return out, labels
def build(step, key):
    ids = step.get("refs") or []
    files, labels = refs_for(step["id"], ids)
    prefix = ""
    if labels:
        prefix = "Use the attached reference images, in this order: " + "; ".join(f"{i}) {l}" for i, l in enumerate(labels, 1)) + ". Keep every person's face, hair and clothing and every place and prop exactly as in the references. "
    text = prefix + step[key]
    if "CHAR_MARSHAL" in ids: text += " The marshal's star badge is a plain five-pointed silver star badge, no lettering, no engraving."
    if "PROP_PIANO" in ids: text += " The piano has no nameplate and no lettering anywhere."
    text += " All signs, papers and books show no readable writing."
    return {"id": step["id"], "n": len(files), "prompt": text, "files": [os.path.basename(f) for f in files], "flashback": step.get("flashback", False)}
imgs = [build(s, "full_prompt") for s in SL["timeline"] if s.get("type") == "image"]
frames = [dict(build(s, "start_frame_full_prompt"), priority=s.get("priority"), duration=s.get("duration_s"), video_prompt=s.get("video_prompt"), end=s.get("end_frame_prompt")) for s in SL["timeline"] if s.get("type") == "clip"]
json.dump(imgs, open(os.path.join(W, "_variants", "queue_images.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(frames, open(os.path.join(W, "_variants", "queue_frames.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(imgs), "images;", len(frames), "clips")
for x in imgs[:6]: print(x["id"], x["n"], x["flashback"], len(x["prompt"]))
