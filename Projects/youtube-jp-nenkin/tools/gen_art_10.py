# -*- coding: utf-8 -*-
"""gen_art_10.py — gen ảnh lớp sân khấu cho video 10 bằng Gemini image.

Đọc prompt TỪ `06_VIDEO/<slug>/art_prompts_FLOW.txt` + tên file TỪ `art_prompts_TENFILE.txt`
(nguồn sự thật duy nhất — đừng chép prompt vào đây, sẽ lệch với bản user bơm extension).

CHẠY:  python tools/gen_art_10.py                 # gen tất cả ảnh còn THIẾU
       python tools/gen_art_10.py 5 6 7 8         # chỉ gen dòng 5..8 của FLOW.txt
"""
import base64
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
SLUG = "10_shien-kyufukin-hagaki-9gatsu"
VD = PROJ / "06_VIDEO" / SLUG
KEY_FILE = Path(r"E:\Claude\Projects\youtube-jp-showa\tools\.gemini_key")
MODELS = ["gemini-3.1-flash-image", "gemini-3-pro-image", "gemini-2.5-flash-image"]


def load_jobs():
    """→ [(số dòng, tên file, prompt)] khớp thứ tự FLOW ↔ TENFILE."""
    prompts = [l.strip() for l in (VD / "art_prompts_FLOW.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    names = {}
    for l in (VD / "art_prompts_TENFILE.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+)\t([^\t]+)\t", l)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
    return [(i + 1, names[i + 1], p) for i, p in enumerate(prompts) if (i + 1) in names]


def gen(key, out: Path, prompt: str) -> bool:
    # `fill_*` là ô 4:3 (390×316), còn lại là khung 16:9 của thân bảng.
    ar = "4:3" if out.name.startswith("fill_") else "16:9"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"imageConfig": {"aspectRatio": ar}}}
    last = None
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        req = urllib.request.Request(url, json.dumps(body).encode("utf-8"),
                                     {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read().decode("utf-8"))
            for part in data["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    png = base64.b64decode(part["inlineData"]["data"])
                    out.write_bytes(png)
                    print(f"  ✓ {out.name}  {len(png)//1024} KB  ({model}, {ar})")
                    return True
            last = "response không có ảnh"
        except urllib.error.HTTPError as e:
            try:
                last = f"{e.code} {e.read().decode('utf-8')[:240]}"
            except Exception:  # noqa: BLE001
                last = str(e)[:200]
            continue
        except Exception as e:  # noqa: BLE001
            last = str(e)[:200]
            continue
    print(f"  ✗ {out.name}: {last}")
    return False


def main():
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    art = VD / "art"
    art.mkdir(parents=True, exist_ok=True)
    only = {int(a) for a in sys.argv[1:] if a.isdigit()}
    ok = bad = skip = 0
    for n, name, prompt in load_jobs():
        if only and n not in only:
            continue
        out = art / name
        if out.exists() and not only:
            skip += 1
            continue
        print(f"[{n:02d}] {name}")
        if gen(key, out, prompt):
            ok += 1
        else:
            bad += 1
    print(f"— gen {ok} ảnh, lỗi {bad}, bỏ qua (đã có) {skip} —")


if __name__ == "__main__":
    main()
