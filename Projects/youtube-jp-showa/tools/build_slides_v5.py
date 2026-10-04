# -*- coding: utf-8 -*-
"""Gian nhip 4s -> ~7s/anh (user chot 6-8s, 2026-08-07 khuya).
Chon loc tu bo 289 khung hien co: moi dong thoai giu m = round(dur/7) khung,
rai deu, uu tien giu khung CLIP. Khong gen lai anh nao.
"""
import json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
VID = os.path.join(ROOT, "06_VIDEO", "01_kyushoku")
IMG = os.path.join(VID, "slides_img")
CLIPS = os.path.join(VID, "clips")
V2 = os.path.join(ROOT, "06_VIDEO", "01_kyushoku_v2")
TARGET = 7.0

d = json.load(open(os.path.join(VID, "timeline.json"), encoding="utf-8"))
tl, total = d["lines"], d["total"]
E = json.load(open(os.path.join(ROOT, "03_SCRIPTS", "01_kyushoku_SLIDES.json"), encoding="utf-8"))
assert len(E) == 289, len(E)

def line_idx(match):
    for i, l in enumerate(tl):
        if match in l["text"]:
            return i
    raise SystemExit("match fail: " + match)

# group entries (giu thu tu index cu) theo dong
groups = []  # (line_idx, [old_slide_indices...])
for i, e in enumerate(E):
    li = line_idx(e["match"])
    if groups and groups[-1][0] == li:
        groups[-1][1].append(i)
    else:
        groups.append((li, [i]))

new_entries = []  # (old_idx, entry_dict)
for li, olds in groups:
    st = tl[li]["start"]
    en = tl[li + 1]["start"] if li + 1 < len(tl) else total
    dur = en - st
    m = max(1, min(len(olds), round(dur / TARGET)))
    # chon m chi so rai deu trong olds; neu co clip, dam bao no duoc giu
    picks = [olds[round(j * len(olds) / m)] if round(j * len(olds) / m) < len(olds) else olds[-1]
             for j in range(m)]
    picks = sorted(set(picks))
    clip_olds = [o for o in olds if E[o].get("video")]
    for co in clip_olds:
        if co not in picks:
            # thay pick gan nhat bang clip
            nearest = min(picks, key=lambda p: abs(p - co))
            picks[picks.index(nearest)] = co
            picks = sorted(set(picks))
    m = len(picks)
    for j, o in enumerate(picks):
        ent = {"match": E[o]["match"]}
        off = j * dur / m
        if off > 0.01:
            ent["offset"] = round(off, 2)
        if E[o].get("video"):
            ent["video"] = True
        else:
            ent["photo"] = True
        new_entries.append((o, ent))

print("khung moi:", len(new_entries), "| trung binh", round(total / len(new_entries), 2), "s/khung")

# xuat bo anh moi
NEW_IMG = IMG + "_v5"
NEW_CLIPS = CLIPS + "_v5"
os.makedirs(NEW_IMG, exist_ok=True)
os.makedirs(NEW_CLIPS, exist_ok=True)
out = []
for ni, (o, ent) in enumerate(new_entries):
    if ent.get("video"):
        shutil.copyfile(os.path.join(CLIPS, f"clip_{o:02d}.mp4"), os.path.join(NEW_CLIPS, f"clip_{ni:02d}.mp4"))
        # anh fallback
        src_img = os.path.join(IMG, f"slide_{o:02d}.jpg")
        if os.path.exists(src_img):
            shutil.copyfile(src_img, os.path.join(NEW_IMG, f"slide_{ni:02d}.jpg"))
    else:
        shutil.copyfile(os.path.join(IMG, f"slide_{o:02d}.jpg"), os.path.join(NEW_IMG, f"slide_{ni:02d}.jpg"))
    out.append(ent)

# swap
BK289 = os.path.join(V2, "_slides_289_backup")
if not os.path.exists(BK289):
    shutil.move(IMG, BK289)
    shutil.move(CLIPS, os.path.join(V2, "_clips_289_backup"))
else:
    shutil.rmtree(IMG); shutil.rmtree(CLIPS)
shutil.move(NEW_IMG, IMG)
shutil.move(NEW_CLIPS, CLIPS)
json.dump(out, open(os.path.join(ROOT, "03_SCRIPTS", "01_kyushoku_SLIDES.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
n_clip = sum(1 for e in out if e.get("video"))
print(f"SLIDES v5: {len(out)} entry ({n_clip} clip) · anh -> slides_img · bo 289 backup o _slides_289_backup")
PYEOF_MARKER = None
if __name__ == "__main__":
    pass
