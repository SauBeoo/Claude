# -*- coding: utf-8 -*-
"""fetch_vlogfx_assets.py — one-off asset fetch for the vlogfx-demo project.
Reuses auto_collage.pexels_fetch (UA header) + skill cutout script.
3 city/street photos (full-bleed footage) + 1 traffic light -> rembg cutout.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from auto_collage import cutout, pexels_fetch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "public" / "projects" / "vlogfx-demo" / "assets"
RAW = ROOT / "projects" / "vlogfx-demo" / "_raw"
ASSETS.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

PHOTOS = [
    ("city street crosswalk people motion tokyo", "scene_a.jpg"),
    ("hong kong tram street neon evening", "scene_b.jpg"),
    ("desert highway road sign blue sky", "scene_c.jpg"),
]
CUTOUT = ("traffic light isolated blue sky", "raw_light.jpg", "el_light.png")

ok = 0
for q, name in PHOTOS:
    dest = ASSETS / name
    if dest.exists() or pexels_fetch(q, dest):
        ok += 1
        print(f"OK {name}")

raw = RAW / CUTOUT[1]
cut = ASSETS / CUTOUT[2]
if not cut.exists():
    if pexels_fetch(CUTOUT[0], raw) and cutout(raw, cut):
        print(f"OK {CUTOUT[2]}")
else:
    print(f"OK {CUTOUT[2]} (san co)")

print(f"xong: {ok}/3 photo + cutout {'co' if cut.exists() else 'THIEU'}")
