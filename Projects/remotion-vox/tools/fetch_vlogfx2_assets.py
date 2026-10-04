# -*- coding: utf-8 -*-
"""fetch_vlogfx2_assets.py — assets for vlogfx2-demo (9:16, real video):
- 3 Pexels VIDEO clips (free API, same key): HK tram street / traffic light /
  crosswalk crowd
- duck photo -> rembg cutout (sticker con vịt như reel)
- doodle mặt mèo vẽ bằng PIL (marker style, nền trong suốt)
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from auto_collage import PEXELS_KEY_FILE, cutout, pexels_fetch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "public" / "projects" / "vlogfx2-demo" / "assets"
RAW = ROOT / "projects" / "vlogfx2-demo" / "_raw"
ASSETS.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

KEY = os.environ.get("PEXELS_API_KEY") or PEXELS_KEY_FILE.read_text().strip()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def pexels_video(query: str, dest: Path, portrait=True) -> bool:
    if dest.exists():
        print(f"OK {dest.name} (san co)")
        return True
    url = (f"https://api.pexels.com/videos/search?query={urllib.request.quote(query)}"
           f"&per_page=5&orientation={'portrait' if portrait else 'landscape'}")
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        vids = data.get("videos", [])
        if not vids:
            print(f"⚠ 0 video: '{query}'")
            return False
        v = vids[0]
        # file nhỏ nhất mà vẫn >=720 chiều ngắn
        files = sorted(
            [f for f in v["video_files"] if f.get("file_type") == "video/mp4"],
            key=lambda f: (f.get("width") or 0) * (f.get("height") or 0))
        pick = next((f for f in files if min(f.get("width") or 0, f.get("height") or 0) >= 700),
                    files[-1] if files else None)
        if not pick:
            return False
        req2 = urllib.request.Request(pick["link"], headers={"User-Agent": UA})
        dest.write_bytes(urllib.request.urlopen(req2, timeout=180).read())
        with open(ASSETS / "ATTRIBUTIONS.txt", "a", encoding="utf-8") as f:
            f.write(f"{dest.name}: {v['url']} (Pexels video, {v['user']['name']})\n")
        print(f"OK {dest.name} {pick.get('width')}x{pick.get('height')} "
              f"{dest.stat().st_size // 1024}KB dur={v.get('duration')}s")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"⚠ video loi '{query}': {e}")
        return False


def draw_cat_doodle(dest: Path):
    """Mặt mèo doodle kiểu bút dạ — nền trong suốt."""
    from PIL import Image, ImageDraw
    S = 400
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = (255, 240, 235, 255)
    W = 14  # net but
    # dau
    d.ellipse([60, 90, 340, 350], outline=ink, width=W)
    # tai
    d.line([100, 130, 70, 40], fill=ink, width=W)
    d.line([70, 40, 165, 95], fill=ink, width=W)
    d.line([300, 130, 330, 40], fill=ink, width=W)
    d.line([330, 40, 235, 95], fill=ink, width=W)
    # mat
    d.ellipse([135, 180, 175, 220], fill=ink)
    d.ellipse([225, 180, 265, 220], fill=ink)
    # mui + mieng
    d.ellipse([190, 235, 210, 255], fill=ink)
    d.arc([160, 240, 200, 290], 0, 180, fill=ink, width=10)
    d.arc([200, 240, 240, 290], 0, 180, fill=ink, width=10)
    # ria
    for y1, y2 in [(215, 205), (240, 240), (265, 275)]:
        d.line([40, y1, 115, y2], fill=ink, width=8)
        d.line([285, y2, 360, y1], fill=ink, width=8)
    im.save(dest)
    print(f"OK {dest.name} (PIL doodle)")


ok = 0
ok += pexels_video("hong kong tram street city", ASSETS / "clip_tram.mp4")
ok += pexels_video("traffic light city sky", ASSETS / "clip_light.mp4")
ok += pexels_video("people crossing street city crowd", ASSETS / "clip_cross.mp4")

duck_raw = RAW / "raw_duck.jpg"
duck = ASSETS / "el_duck.png"
if not duck.exists():
    if pexels_fetch("white duck standing isolated", duck_raw) and cutout(duck_raw, duck):
        print("OK el_duck.png")
else:
    print("OK el_duck.png (san co)")

draw_cat_doodle(ASSETS / "doodle_cat.png")
print(f"xong: {ok}/3 video")
