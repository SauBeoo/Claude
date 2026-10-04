# -*- coding: utf-8 -*-
"""Gen thử ảnh minh họa ANIME cho kênh nenkin (style D) — dùng Gemini image như stickman."""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY_FILE = Path(r"E:\Claude\Projects\youtube-stickman\tools\.gemini_key")
MODELS = ["gemini-3.1-flash-image", "gemini-3-pro-image", "gemini-2.5-flash-image"]
OUT = Path(__file__).parent.parent / "06_VIDEO" / "_demo_motion" / "anime"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = ("Japanese anime illustration, slice-of-life style, clean lineart, soft warm "
         "watercolor shading, gentle pastel colors, wholesome mood, high quality anime key visual, "
         "16:9 wide composition, NO text, no letters, no watermark.")

PROMPTS = {
    "cast_sato": ("A cheerful Japanese woman in her mid 60s, gray hair in a neat bun, rosy cheeks, "
                  "wearing a supermarket staff apron, smiling warmly, standing in a bright supermarket aisle, "
                  "half-body portrait, character centered LEFT side, RIGHT side simple and uncluttered for text overlay. " + STYLE),
    "scene_couple": ("A Japanese couple in their late 60s sitting at a cozy kitchen table in the evening, "
                     "looking together at a bank passbook, expressions relieved and happy, warm lamp light, "
                     "teapot on table, characters on RIGHT side, LEFT side dimmer and simple for text overlay. " + STYLE),
    "mascot_lab": ("A friendly Japanese researcher man in his 30s wearing a white lab coat and round glasses, "
                   "holding a clipboard, standing beside a whiteboard with simple charts, bright clean room, "
                   "warm reassuring smile, character on LEFT side, RIGHT side simple for text overlay. " + STYLE),
}


def gen(key, name, prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"imageConfig": {"aspectRatio": "16:9"}}}
    last = None
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        req = urllib.request.Request(url, json.dumps(body).encode("utf-8"),
                                     {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode("utf-8"))
            for part in data["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    png = base64.b64decode(part["inlineData"]["data"])
                    out = OUT / f"{name}.png"
                    out.write_bytes(png)
                    print(f"  ✓ {out.name} ({len(png)//1024} KB, {model})")
                    return
            last = "response không có ảnh"
        except urllib.error.HTTPError as e:
            try:
                last = f"{e.code}: {e.read().decode('utf-8')[:300]}"
            except Exception:  # noqa: BLE001
                last = str(e)[:200]
            continue
        except Exception as e:  # noqa: BLE001
            last = str(e)[:200]
            continue
    print(f"  ✗ {name}: {last}")


def main():
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    for name, prompt in PROMPTS.items():
        gen(key, name, prompt)


if __name__ == "__main__":
    main()
