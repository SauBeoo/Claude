# -*- coding: utf-8 -*-
"""sync_channel_templates.py — generate templates/<channel>.json from channels.py.

channels.py stays the single source of truth for channel identity (workspace
rule: renderer profiles live there). This tool derives editor templates —
rerun it whenever channels.py changes; a content hash makes reruns cheap.

Usage: py -3 tools/sync_channel_templates.py
"""

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHANNELS_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")


def rgb_hex(t):
    return "#{:02X}{:02X}{:02X}".format(*t)


def main():
    sys.path.insert(0, str(CHANNELS_TOOLS))
    import channels as CH  # noqa: E402

    src_hash = hashlib.sha1(
        (CHANNELS_TOOLS / "channels.py").read_bytes()).hexdigest()[:12]
    out_dir = ROOT / "templates"
    out_dir.mkdir(exist_ok=True)

    stamp = out_dir / ".source_hash"
    if stamp.exists() and stamp.read_text().strip() == src_hash:
        print(f"templates da khop channels.py ({src_hash}) — khong lam gi")
        return

    count = 0
    for key in CH.CHANNELS:
        prof = CH.get(key)
        pal = CH.palette(key)
        tpl = {
            "name": key,
            "displayName": prof.get("name", key),
            "sourceHash": src_hash,
            "theme": {
                "palette": {"bgTop": rgb_hex(pal["bg_top"]),
                            "bgBottom": rgb_hex(pal["bg_bottom"]),
                            "accent": rgb_hex(pal["accent"])},
                "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                "canvasColor": rgb_hex(pal["bg_top"]),
            },
            "captions": {
                "style": prof.get("sub_style", "outline"),
                "fontSize": (prof.get("sub_size") or 22) * 2,
            },
            "voice": {
                "engine": prof.get("engine", "voicevox"),
                "speaker": prof.get("speaker"),
                "style": prof.get("style"),
                "speed": prof.get("speed"),
                "intonation": prof.get("intonation"),
            },
            "video": {
                "transition": prof.get("transition", "dissolve"),
                "transitionDur": prof.get("transition_dur", 0.4),
                "bgmGain": prof.get("bgm_gain", -40),
                "watermark": prof.get("watermark"),
                "finalCrf": prof.get("final_crf", 20),
            },
            "entranceRotation": ["rise", "grow", "flip", "punch", "wobble",
                                  "peel", "zoom-through"],
        }
        (out_dir / f"{key}.json").write_text(
            json.dumps(tpl, ensure_ascii=False, indent=2), encoding="utf-8")
        count += 1

    stamp.write_text(src_hash)
    print(f"OK {count} template → templates/ (hash {src_hash})")


if __name__ == "__main__":
    main()
