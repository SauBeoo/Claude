# -*- coding: utf-8 -*-
"""build_hoathinh.py — dựng phim hoạt hình 「Mèo Cam và Ngọn Đèn Bay Mất」
từ 12 ảnh gen (projects/hoathinh-demo/prompts_STORY.md là kịch bản gốc).

Usage: py -3 tools/build_hoathinh.py --images "C:\\...\\download (3)"
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from auto_collage import ensure_sfx  # noqa: E402

FPS = 30
OUT = "hoathinh-demo"

# (file gốc, giây, motion, wipe?, thoại, sfx tại đầu cảnh)
SCENES = [
    ("Riverside_village_at_golden_sunset", 8, "pan", None, "Ngôi làng bên sông, mùa đèn lồng.", None),
    ("Cat_gazing_at_red_lantern",          7, "pan", None, None, None),
    ("Cat_reaching_for_red_lantern",       6, "zoom-punch", None, "Á! Cơn gió!", "whoosh"),
    ("Orange_tabby_cat_leaping_rooftops",  5, "pan", None, None, "pop"),
    ("Cat_dashing_through_night_market",   5, "pan", None, None, "swipe"),
    ("Cat_looking_at_red_lantern",         7, "pan", "left", "Cao quá…", None),
    ("Cat_climbing_tree",                  6, "pan", None, None, "riser"),
    ("Tabby_cat_touching_red_lantern",     8, "pan", None, "…một chút nữa thôi.", None),
    ("Cat_falling_with_red_lantern",       4, "zoom-punch", None, None, "drop"),
    ("Cat_landing_in_golden_haystack",     6, "pan", None, None, "boing"),
    ("Cat_hanging_red_lantern",            7, "pan", None, "Về chỗ cũ nhé.", "coin"),
    ("Cat_sleeping_under_red_lantern",     9, "pan", None, "Hết.", None),
]
XFADE = 15  # dissolve nửa giây giữa các cảnh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True)
    args = ap.parse_args()
    src_dir = Path(args.images)

    assets = ROOT / "public" / "projects" / OUT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    ensure_sfx()

    # nhạc storybook
    music = assets / "music.wav"
    total_sec = sum(s[1] for s in SCENES)
    if not music.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "make_lullaby.py"),
                        str(music), "--seconds", str(total_sec)], check=True)

    footage, texts, sfxs = [], [], []
    markers = []
    TOTAL = round(total_sec * FPS)
    t = 0  # frame

    for i, (name, sec, motion, wipe, line, sfx) in enumerate(SCENES, 1):
        hits = list(src_dir.glob(f"{name}*.jpe*g")) + list(src_dir.glob(f"{name}*.png"))
        if not hits:
            raise SystemExit(f"[LOI] khong thay anh {name}* trong {src_dir}")
        dst = assets / f"scene_{i:02d}{hits[0].suffix.lower()}"
        if not dst.exists() or dst.stat().st_size != hits[0].stat().st_size:
            shutil.copy2(hits[0], dst)

        dur = round(sec * FPS)
        fade = XFADE if i > 1 else 0
        clip = {
            "id": f"sc{i:02d}", "kind": "video",
            "from": t - fade, "durationInFrames": dur + fade,
            "asset": f"assets/{dst.name}", "trimStartFrames": 0,
            "fit": "cover", "layout": {}, "motion": motion,
            "speed": 1, "mirror": False, "volume": 0,
            "fadeInFrames": fade if not wipe else 0,
            "wipeInFrames": 12 if wipe else 0, "wipeDir": wipe or "left",
            "filter": {},
        }
        footage.append(clip)
        markers.append({"id": f"m{i}", "atFrame": max(0, t), "label": f"c{i} {name[:18]}"})

        if line:
            is_title = i == 1
            texts.append({
                "id": f"line{i}", "kind": "text",
                "from": t + 20, "durationInFrames": dur - 30,
                "content": line, "preset": "plain",
                "color": "#FFF3D6",
                "animation": "pop", "animationParams": {"restDeg": 0},
                "layout": {"x": 120, "y": 900},
                "fontSize": 54,
            })
        if sfx:
            sfxs.append({"id": f"sfx{i}", "kind": "audio", "from": max(0, t - 5),
                         "durationInFrames": min(60, TOTAL - t + 5),
                         "asset": f"sfx/{sfx}.wav", "volume": 0.3,
                         "trimStartFrames": 0})
        t += dur

    # title card trên cảnh 1
    texts.insert(0, {
        "id": "title", "kind": "text", "from": 15, "durationInFrames": 165,
        "content": "Mèo Cam và Ngọn Đèn Bay Mất", "preset": "plain",
        "color": "#FFE9B0", "animation": "drop", "animationParams": {"restDeg": 0},
        "layout": {"x": 330, "y": 120}, "fontSize": 76,
    })

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "version": 1,
        "meta": {"name": OUT, "channel": None, "templateRef": None,
                 "fps": FPS, "width": 1920, "height": 1080,
                 "createdAt": now, "modifiedAt": now},
        "timeline": {"durationInFrames": TOTAL},
        "sceneMarkers": markers,
        "tracks": [
            {"id": "trk-film", "name": "Film", "type": "video",
             "muted": False, "hidden": False, "locked": False, "clips": footage},
            {"id": "trk-text", "name": "Thoại", "type": "text",
             "muted": False, "hidden": False, "locked": False, "clips": texts},
            {"id": "trk-music", "name": "Music", "type": "audio",
             "muted": False, "hidden": False, "locked": False,
             "clips": [{"id": "music-1", "kind": "audio", "from": 0,
                        "durationInFrames": TOTAL, "asset": "assets/music.wav",
                        "volume": 0.7, "trimStartFrames": 0}]},
            {"id": "trk-sfx", "name": "SFX", "type": "audio",
             "muted": False, "hidden": False, "locked": False, "clips": sfxs},
        ],
        "captions": {"source": "none", "style": "outline", "enabled": False,
                     "fontSize": 44, "lines": [], "words": []},
        "theme": {"palette": {"bgTop": "#1A1206", "bgBottom": "#1A1206",
                              "accent": "#FFE9B0"},
                  # Segoe UI phủ đủ dấu tiếng Việt
                  "fontFamily": '"Segoe UI", "Yu Gothic", sans-serif',
                  "canvasColor": "#0E0A05"},
    }
    out_dir = ROOT / "projects" / OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "project.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK projects/{OUT}/project.json — {len(SCENES)} canh / {total_sec}s / "
          f"{len(texts)} thoai / {len(sfxs)} sfx")


if __name__ == "__main__":
    main()
