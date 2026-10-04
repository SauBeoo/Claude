# -*- coding: utf-8 -*-
"""Sinh bo prompt IMAGE-TO-VIDEO cho video 19 + script bat co video:true.

Chi lam clip o nhung cue ma CHUYEN DONG CHINH LA THONG TIN (chat long chay,
hoi nuoc, lang xuong, tay lam viec). Con lai giu anh tinh — user ghet Ken Burns
(feedback_video_no_motion_mot_giong) va audience-45plus.md §2 doi nhip cham.
"""
import json
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "19_haisuiko-naze-tsumaru"

LOCK = ("Animate the provided still image into a photorealistic video clip. LOCKED CAMERA: "
        "absolutely no camera movement, no pan, no zoom, no dolly, no shake, no cuts, no scene "
        "change. One single continuous take. Keep the original framing, colours and lighting of "
        "the image unchanged. Only the element described below moves, and it moves slowly and "
        "evenly. Calm documentary mood, muted warm palette, 16:9, about 8 seconds. "
        "No text, no letters, no logos, no human faces, no watermark.")

# idx entry SLIDES -> (nhom, mo ta chuyen dong)
CLIPS = {
 # ── A · chuyen dong LA co che (mat di la mat thong tin)
 39: ("A", "Inside the pipe, the pale solid grease slowly softens and turns glossy at its "
           "surface, beginning to slump downward, but it does not detach."),
 41: ("A", "A slow tongue of melted grease creeps further along the inside of the pipe, away "
           "from the camera, and stops."),
 23: ("A", "The white flour in the water slowly swells and thickens into a glossy paste; the "
           "swirling motion gradually stops as it becomes too thick to move."),
 52: ("A", "The coffee grounds swirl slowly in the water, then settle downward and come to rest "
           "as a dense layer at the bottom."),
 55: ("A", "Steam drifts over the hot water while the coffee grounds sit completely unchanged, "
           "not dissolving, not softening."),
 37: ("A", "A steady stream of very hot water pours straight down into the drain, steam curling "
           "upward from the sink surface."),
 20: ("A", "Elderly hands hold the strainer steady while golden oil runs slowly through the mesh "
           "into the can below."),
 9:  ("A", "A thin film of oil spreads slowly outward across the surface of the water in a "
           "widening ring."),
 42: ("A", "Water drains freely down the opening in a smooth steady spiral."),
 69: ("A", "Cloudy rice washing water pours slowly from a wooden pail onto the soil at the base "
           "of a tree and soaks in."),
 72: ("A", "Clear water runs steadily from the faucet into the sink, unbroken."),
 2:  ("A", "Steam rises and curls slowly from the kettle spout."),
 # ── B · hoi tho nen, mo section (rat nhe)
 0:  ("B", "Almost still: a single drop of water gathers at the rim of the drain and falls."),
 6:  ("B", "Almost still: fine dust drifts in the shaft of window light; a curtain edge lifts "
           "very slightly."),
 51: ("B", "Almost still: morning light strengthens a little across the counter."),
 66: ("B", "Almost still: a thin trickle of water seeps across the old stone surface."),
 82: ("B", "Almost still: warm light shifts slowly across the room."),
 87: ("B", "Almost still: a last drop falls into the dark sink, one small ripple."),
}

flow, names, table = [], [], []
for idx in sorted(CLIPS):
    grp, motion = CLIPS[idx]
    flow.append(f"{LOCK} {motion}")
    names.append(f"clips/clip_{idx:02d}.mp4")
    table.append((idx, grp, motion))

S = PROJ / "03_SCRIPTS"
(S / f"{SLUG}_VID_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S / f"{SLUG}_VID_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

# ── script bat co video:true — CHI cho clip da ton tai (tu chua duoc)
ENABLE = '''# -*- coding: utf-8 -*-
"""Bat "video": true cho entry SLIDES 19 CHI KHI clips/clip_NN.mp4 da ton tai.

Vi sao phai co script: preflight cua video_render (dong 121-126) BAO LOI neu entry
khai video:true ma thieu clip => bat truoc khi gen clip la tu chan chinh minh.
Chay lai bao nhieu lan cung duoc; clip nao chua co thi de nguyen anh tinh.
"""
import json
from pathlib import Path

P = Path(r"E:\\Claude\\Projects\\youtube-jp-co-dai")
SL = P / "03_SCRIPTS" / "19_haisuiko-naze-tsumaru_SLIDES.json"
CL = P / "06_VIDEO" / "19_haisuiko-naze-tsumaru" / "clips"
IDX = %s

d = json.loads(SL.read_text(encoding="utf-8"))
on, off = [], []
for i in IDX:
    if not (CL / f"clip_{i:02d}.mp4").exists():
        off.append(i)
        d[i].pop("video", None)
        continue
    d[i]["video"] = True
    on.append(i)
SL.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"BAT {len(on)} clip: {on}")
print(f"chua co clip, giu anh tinh: {off}")
''' % sorted(CLIPS)
(PROJ / "tools" / "enable_clips19.py").write_text(ENABLE, encoding="utf-8")

print(f"{len(flow)} prompt video  ·  A={sum(1 for _,g,_ in table if g=='A')} co che"
      f"  B={sum(1 for _,g,_ in table if g=='B')} hoi tho nen")
print("entry:", ", ".join(f"{i:02d}{g}" for i, g, _ in table))
