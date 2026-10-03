import json, sys
d = json.load(open(r"C:\Users\permr\fl_work\wwp_brief\shotlist.json", encoding="utf-8"))
print("STYLE:", d["style"]); print("CLIP_STYLE:", d["clip_style"]); print("FORMAT:", d["format"], "| ESTIMATE:", d["estimate"]); print()
for sec in ("characters", "props", "locations"):
    print("=====", sec)
    for k, v in d[sec].items():
        print("--", k)
        for kk, vv in v.items():
            print("   ", kk, ":", vv)
