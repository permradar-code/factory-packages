import json
w = r"C:\Users\permr\fl_work\wwp"
d = json.load(open(r"C:\Users\permr\fl_work\wwp_brief\shotlist.json", encoding="utf-8"))
m = {
    "schema": "moiastro.montage.package.v2",
    "project_id": "western_widows_piano_v1",
    "title": d.get("working_title_youtube") or d.get("title"),
    "language": "en",
    "aspect_ratio": "16:9",
    "fps": 24,
    "source": "Google Flow (Omni 1.1 Flash 720p clips; Nano Banana Pro images); narration ElevenLabs",
    "flow_credits_spent": 0,
    "flow_credits_left": None,
    "phase": "refs",
    "narration": {"voice_id": None, "files": []},
    "refs": {},
    "scenes": [],
    "montage_ready": False,
}
json.dump(m, open(w + r"\manifest.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(w + r"\README.md", "w", encoding="utf-8").write(
    "# western_widows_piano_v1 (The Widow's Piano, western, 16:9)\n\n"
    "Work in progress. Phase 1 (references) is running. Source of truth: briefs/western_widows_piano/shotlist.json "
    "(branch tools/montage).\n\nStatus: phase = refs.\n")
open(w + r"\.gitignore", "w", encoding="utf-8").write("_variants/\n*.key\n.env\n")
print("ok", m["title"])
