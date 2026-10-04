# -*- coding: utf-8 -*-
"""swap_real.py — doi ung vien anh THAT cho vai o (sau khi soi khop loi), khong chay lai ca pick_real.

  python tools/swap_real.py <stem> 18:2 27:2 ...
- tai ban goc ung vien _cand/cand.json -> cover 1920x1080 -> slides_img/slide_NN.jpg
- anh cu backup sang _plan/audit/replaced/ (khong xoa)
- cap nhat "real" trong <stem>_SLIDES.json VA _SLIDES_static.json (kb_cells doc ban static)
- ghi so den _media_library
"""
import sys, io, json, shutil
from pathlib import Path
# stdout utf-8: pick_real tu boc lai
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
from pick_real import dl, cover, ML
stem = sys.argv[1]
vd = PROJ / "06_VIDEO" / stem
cand = json.load(open(vd / "_cand" / "cand.json", encoding="utf-8"))
bk = vd / "_plan" / "audit" / "replaced"; bk.mkdir(parents=True, exist_ok=True)
paths = [PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json", PROJ / "03_SCRIPTS" / f"{stem}_SLIDES_static.json"]
sls = [json.load(open(p, encoding="utf-8")) for p in paths]
idx = ML.load_index()
for arg in sys.argv[2:]:
    i, k = map(int, arg.split(":"))
    it = cand[str(i)]["items"][k]
    assert it["kind"] == "photo", f"slide {i}: chi doi anh"
    src = vd / "_real_raw" / f"{i:02d}_pexels_{it['id']}.jpg"
    if not src.exists():
        dl(it["orig"], src)
    for old in vd.glob(f"slides_img/slide_{i:02d}.*"):
        shutil.move(str(old), str(bk / old.name))
    cover(src, vd / "slides_img" / f"slide_{i:02d}.jpg")
    for sl in sls:
        sl[i]["real"] = {"src": "pexels", "id": it["id"], "url": it["url"]}
    ML.add_file(src, "photo", source="pexels", source_id=str(it["id"]), url=it["url"],
                query=cand[str(i)]["q"], used_by=f"yawa/{stem}", idx=idx, autosave=False)
    print(f"slide {i:3d} <- pexels {it['id']}")
ML.save_index(idx)
for p, sl in zip(paths, sls):
    json.dump(sl, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
