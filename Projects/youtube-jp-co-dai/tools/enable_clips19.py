# -*- coding: utf-8 -*-
"""Bat "video": true cho entry SLIDES 19 CHI KHI clips/clip_NN.mp4 da ton tai.

Vi sao phai co script: preflight cua video_render (dong 121-126) BAO LOI neu entry
khai video:true ma thieu clip => bat truoc khi gen clip la tu chan chinh minh.
Chay lai bao nhieu lan cung duoc; clip nao chua co thi de nguyen anh tinh.
"""
import json
from pathlib import Path

P = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SL = P / "03_SCRIPTS" / "19_haisuiko-naze-tsumaru_SLIDES.json"
CL = P / "06_VIDEO" / "19_haisuiko-naze-tsumaru" / "clips"
IDX = [0, 2, 6, 9, 20, 23, 37, 39, 41, 42, 51, 52, 55, 66, 69, 72, 82, 87]

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
