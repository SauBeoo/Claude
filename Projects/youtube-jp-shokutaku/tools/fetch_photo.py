# -*- coding: utf-8 -*-
"""Tải ảnh stock THẬT từ Pexels Photo API cho thumbnail/slide kênh shokutaku.
Ảnh thật free-thương-mại (Pexels License, không cần attribution) → khỏi tick AI-disclosure.
Chạy: python tools/fetch_photo.py "<query>" [<query2> ...] [--out <dir>] [--n 4]
Ảnh landscape, ưu tiên đủ lớn cho khung 1920x1080. In kèm nguồn để ghi credit nếu muốn.
"""
import sys, json, argparse, urllib.request, urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KEY = (Path(__file__).resolve().parents[2] / "youtube-jp-health/tools/.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0"}


def search(query, per=12):
    u = "https://api.pexels.com/v1/search?orientation=landscape&size=large&per_page=%d&query=%s" % (
        per, urllib.parse.quote(query))
    req = urllib.request.Request(u, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--n", type=int, default=4, help="số ảnh tải mỗi query")
    args = ap.parse_args()
    out_dir = Path(args.out) if args.out else Path(__file__).resolve().parents[1] / "06_VIDEO/_photo_candidates"
    out_dir.mkdir(parents=True, exist_ok=True)

    for q in args.queries:
        print(f"\n=== search: {q} ===")
        try:
            data = search(q)
        except Exception as e:
            print("  lỗi:", e)
            continue
        got = 0
        for p in data.get("photos", []):
            if got >= args.n:
                break
            w, h = p.get("width", 0), p.get("height", 0)
            if w < 1920 or h < 1080:
                continue
            link = p["src"].get("large2x") or p["src"].get("original")
            slug = "".join(c if c.isalnum() else "_" for c in q)[:24]
            dest = out_dir / f"{slug}_{p['id']}.jpg"
            try:
                req = urllib.request.Request(link, headers=UA)
                with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as fo:
                    fo.write(r.read())
            except Exception as e:
                print("  tải lỗi:", e)
                continue
            got += 1
            print(f"  ĐÃ LƯU: {dest.name} ({w}x{h}) — Pexels {p['id']} by {p.get('photographer','')} (free, no attribution)")
    print("\nXong. Ảnh ở:", out_dir)


if __name__ == "__main__":
    main()
