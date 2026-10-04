# -*- coding: utf-8 -*-
"""Tai clip ung vien Pexels cho video 05 + cat frame giua de soi mat.
Chi de DUYET — chua phai asset chinh thuc. Ket qua: 06_VIDEO/05_dagashiya-10en/pexels_probe/
"""
import io, sys, json, subprocess, urllib.request, urllib.parse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

KEY = (Path(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key").read_text().strip())
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\05_dagashiya-10en\pexels_probe")
OUT.mkdir(parents=True, exist_ok=True)

# (pexels_id, tag)
CANDS = [
    (3942461, "item7_water_carnival_game"),
    (3031949, "item7_pop_balloon_prize"),
    (7269978, "item6_spinning_top"),
    (4841204, "item1_pinball_ball_close"),
    (4841207, "item1_pinball_hand"),
    (3842243, "item1_pinball_tilt"),
    (856219, "ending_coin_spinning"),
    (2876561, "item4_game_of_luck_machine"),
    (7118320, "item2_kid_coins_jar"),
    (34183483, "item10_japanese_shopfront"),
    (35406247, "cta_japanese_street_festival"),
    (33102609, "cta_traditional_festival"),
    (17431599, "item3_market_stalls"),
    (4750080, "item2_lottery_outlet"),
    (2982434, "item2_lottery_tickets_roller"),
]

def api(url):
    req = urllib.request.Request(url, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

rows = []
for pid, tag in CANDS:
    try:
        v = api(f"https://api.pexels.com/videos/videos/{pid}")
    except Exception as e:
        print(f"[skip] {pid} {tag}: {e}"); continue
    fs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width")]
    fs.sort(key=lambda f: (abs(f["width"] - 1280), -f["width"]))  # ban ~1280 de duyet nhanh
    if not fs:
        print(f"[skip] {pid} no mp4"); continue
    link = fs[0]["link"]
    dest = OUT / f"{tag}_{pid}.mp4"
    if not dest.exists():
        req = urllib.request.Request(link, headers=UA)
        with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as f:
            while True:
                c = r.read(1 << 20)
                if not c: break
                f.write(c)
    dur = v["duration"]
    # 3 frame: 15% / 50% / 85%
    for k, p in enumerate((0.15, 0.5, 0.85)):
        png = OUT / f"{tag}_{pid}_f{k}.jpg"
        if not png.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{dur*p:.2f}", "-i", str(dest),
                            "-frames:v", "1", "-vf", "scale=640:-2", "-q:v", "4", str(png)], check=False)
    rows.append((tag, pid, dur, fs[0]["width"], fs[0]["height"], v["url"]))
    print(f"ok {tag} {pid} {dur}s {fs[0]['width']}x{fs[0]['height']}")

# contact sheet: moi clip 1 hang 3 frame
frames = []
for tag, pid, dur, w, h, url in rows:
    for k in range(3):
        frames.append(str(OUT / f"{tag}_{pid}_f{k}.jpg"))
if frames:
    # dung ffmpeg tile
    n = len(rows)
    inputs = sum([["-i", f] for f in frames], [])
    filt = "".join(f"[{i}:v]scale=426:240,drawtext=text='{rows[i//3][0][:22]}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6[v{i}];" for i in range(len(frames)))
    filt += "".join(f"[v{i}]" for i in range(len(frames))) + f"xstack=inputs={len(frames)}:layout=" + "|".join(f"{(i%3)*426}_{(i//3)*240}" for i in range(len(frames))) + "[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", filt, "-map", "[out]", str(OUT / "_contact_sheet.jpg")], check=False)
    print("sheet ->", OUT / "_contact_sheet.jpg")
(OUT / "_rows.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
