# -*- coding: utf-8 -*-
"""
Tải ảnh mood Pexels cho SCENES (khi chưa có budget gen AI).

    python tools/fetch_scene_photos.py <SCENES json> <folder scenes>

- Query = "q" (fallback "q2") của từng entry; skip ảnh đã có.
- Chống trùng ảnh giữa các cảnh (1 pexels id / 1 cảnh) — log MANIFEST.json.
- Pexels license: thương mại OK, không cần credit; KHÔNG dùng mặt người thật
  cho cảnh phản diện (chọn query đồ vật/bóng dáng từ đầu).
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
KEY_FILE = Path(__file__).resolve().parents[2] / "youtube-jp-health/tools/.pexels_key"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def search(query, key):
    url = ("https://api.pexels.com/v1/search?" +
           urllib.parse.urlencode({"query": query, "per_page": 6,
                                   "orientation": "landscape", "size": "large"}))
    req = urllib.request.Request(url, headers={**UA, "Authorization": key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("photos", [])


def download(link, dest):
    req = urllib.request.Request(link, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    key = KEY_FILE.read_text().strip()
    mf_path = out_dir / "MANIFEST.json"
    manifest = json.loads(mf_path.read_text(encoding="utf-8")) if mf_path.exists() else {}
    used = {m["pexels_id"] for m in manifest.values() if m}

    for spec in cfg:
        dest = out_dir / spec["img"]
        if dest.exists() and dest.stat().st_size > 50_000:
            print(f"[{spec['img']}] đã có, skip")
            continue
        got = None
        for q in (spec.get("q"), spec.get("q2")):
            if not q:
                continue
            try:
                photos = search(q, key)
            except Exception as e:
                print(f"[{spec['img']}] '{q}' lỗi: {e}")
                continue
            for ph in photos:
                if ph["id"] in used:
                    continue
                got = (q, ph)
                break
            if got:
                break
        if not got:
            print(f"[{spec['img']}] KHÔNG tìm được — cảnh này sẽ chỉ ambient")
            manifest[spec["img"]] = None
            continue
        q, ph = got
        download(ph["src"]["large2x"], dest)
        used.add(ph["id"])
        manifest[spec["img"]] = {"pexels_id": ph["id"], "url": ph["url"], "query": q}
        print(f"[{spec['img']}] '{q}' -> id={ph['id']}")
        mf_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    print("XONG.")


if __name__ == "__main__":
    main()
