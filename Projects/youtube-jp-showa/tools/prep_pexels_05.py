# -*- coding: utf-8 -*-
"""Tai ban 1920 cua 3 clip Pexels TRUNG TINH (khong lo nguoi/thoi dai) da duyet mat 2026-08-26,
grade cung filter voi cut_archival (tong 8mm/Kodachrome), mute -> footage_raw/px_*.mp4.
Pexels License: free commercial, khong bat buoc credit (van ghi vao ATTRIBUTIONS cho sach).
"""
import io, sys, json, subprocess, urllib.request
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
KEY = Path(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\05_dagashiya-10en\footage_raw")
TMP = OUT / "_px_src"; TMP.mkdir(parents=True, exist_ok=True)
# (id, name, ss, dur) — dur cat ngan de khong keo qua dai
CANDS = [(7269978, "px_spinning_top", 2, 14), (856219, "px_coin_spinning", 0, 12), (7118320, "px_coins_hand_jar", 0, 12)]
GRADE = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=gamma=1.15:contrast=1.03:saturation=0.82,colorbalance=rs=0.05:gs=0.015:bs=-0.06,noise=alls=6:allf=t+u"
for pid, name, ss, dur in CANDS:
    req = urllib.request.Request(f"https://api.pexels.com/videos/videos/{pid}", headers={**UA, "Authorization": KEY})
    v = json.load(urllib.request.urlopen(req, timeout=30))
    fs = [f for f in v["video_files"] if f.get("file_type") == "video/mp4" and f.get("width")]
    fs.sort(key=lambda f: (abs(f["width"] - 1920), -f["width"]))
    src = TMP / f"{name}_{pid}.mp4"
    if not src.exists():
        with urllib.request.urlopen(urllib.request.Request(fs[0]["link"], headers=UA), timeout=300) as r, open(src, "wb") as f:
            while True:
                c = r.read(1 << 20)
                if not c: break
                f.write(c)
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(dur), "-i", str(src), "-an", "-vf", GRADE, "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(out)], check=True)
    print("ok", name, dur, "s", fs[0]["width"], "x", fs[0]["height"], v["url"])
