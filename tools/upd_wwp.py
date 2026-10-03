import json, glob, os
w = r"C:\Users\permr\fl_work\wwp"
m = json.load(open(w + r"\manifest.json", encoding="utf-8-sig"))
refs = {}
for p in sorted(glob.glob(w + r"\visuals\refs\*.png")):
    n = os.path.basename(p)
    key = n.rsplit("_", 1)[0]
    refs.setdefault(key, []).append("visuals/refs/" + n)
m["refs"] = refs
m["phase"] = "refs"
m["flow_credits_spent"] = 0
m["flow_project_id"] = "7a937194-22cf-4e10-a8ea-406b0d82a514"
json.dump(m, open(w + r"\manifest.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(w + r"\README.md", "w", encoding="utf-8").write(
"""# western_widows_piano_v1 (The Widow's Piano, western, 16:9)

Work in progress. Source of truth: briefs/western_widows_piano/shotlist.json (branch tools/montage).

## Status: Phase 1 (references), waiting for STOP 1
- Characters: 8 of 8 done, 3 angles each (front, 3/4, full body) in visuals/refs/ (CHAR_*_front/_34/_full.png, 1376x768).
  The 3/4 and full-body images were made with the chosen front image as the face reference.
- Props and locations: PROP_PIANO generated, not yet downloaded; PROP_HORSE and LOC_* (8) are pending because Flow returned
  "usage limit reached" (no credits were charged). They will be retried.
- Flow credits spent so far: 0 (all images are free). Flow project: 7a937194-22cf-4e10-a8ea-406b0d82a514.

## Notes
- Model: Nano Banana Pro, 16:9. Prompt = look + style from shotlist.json plus a plain-background / even-light instruction.
- Rejected variants (not pushed) stay in the Flow project.
- Clara reads a little older than 28 (tired look); the face is consistent across the three angles.
""")
print(len(refs), "ref groups,", sum(len(v) for v in refs.values()), "files")
