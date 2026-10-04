# -*- coding: utf-8 -*-
"""sheet_08.py — contact sheet duyet mat lop hinh video 08: slides_img/slide_NN.jpg + frame@3s cua clips/clip_NN.mp4, ghi ten + kind."""
import io, sys, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\08_okane-joushiki")
slides = json.loads((VD.parent.parent / "03_SCRIPTS" / "08_okane-joushiki_SLIDES.json").read_text(encoding="utf-8"))
names = [l.split()[0] for l in (VD / "scene_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
W, H, COLS = 384, 216, 5
tiles = []
for i, e in enumerate(slides):
    if e.get("video"):
        fr = VD / "_sheet_tmp" / f"c{i:03d}.jpg"; fr.parent.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", str(VD / "clips" / f"clip_{i:02d}.mp4"), "-frames:v", "1", "-vf", f"scale={W}:-2", str(fr)], capture_output=True)
        im = Image.open(fr).convert("RGB") if fr.exists() else Image.new("RGB", (W, H), "red"); tag = "VID"
    elif e.get("kind") == "ai":
        im = Image.new("RGB", (W, H), (60, 60, 20)); tag = "AI"
    else:
        p = VD / "slides_img" / f"slide_{i:02d}.jpg"
        im = Image.open(p).convert("RGB") if p.exists() else Image.new("RGB", (W, H), "red"); tag = e.get("kind", "?")
    im.thumbnail((W, H)); tiles.append((i, im, tag, names[i] if i < len(names) else ""))
for part in range(0, len(tiles), 40):
    chunk = tiles[part:part + 40]; rows = (len(chunk) + COLS - 1) // COLS
    sh = Image.new("RGB", (W * COLS, (H + 26) * rows), "black"); d = ImageDraw.Draw(sh)
    for j, (i, im, tag, nm) in enumerate(chunk):
        x, y = (j % COLS) * W, (j // COLS) * (H + 26); sh.paste(im, (x, y))
        d.rectangle((x, y + H, x + W, y + H + 26), fill="black")
        d.text((x + 3, y + H + 1), f"{i:03d} {tag}", fill="yellow"); d.text((x + 3, y + H + 13), nm[10:70], fill="white")
    out = VD / f"_sheet_slides_{part//40:02d}.jpg"; sh.save(out, quality=82); print(out)
