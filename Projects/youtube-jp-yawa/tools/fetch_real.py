# -*- coding: utf-8 -*-
"""fetch_real.py — tim ANH/VIDEO THAT (Pexels) cho tung o anh cua SLIDES yawa, truoc khi dung AI.

User 2026-09-30: "tim anh that va video truoc di. Khong co thi ghep AI thoi."
- Doc 03_SCRIPTS/<stem>_SLIDES.json (o anh = entry khong co card/reveal) + _plan/queries.py (key = _shot).
- Moi o: 1 request Pexels (photo, hoac video neu query la ("v", q)) -> giu 3 ung vien:
  ⛔ bo asset DA LEN SONG o video khac (so den _media_library, media-library.md §2)
  ⛔ khong trung id trong cung video.
- Tai ban NHO de duyet -> 06_VIDEO/<stem>/_cand/NN_cK.jpg + cand.json; dung contact sheet _cand/sheet_XX.png.
- Chua tai ban goc: sau khi chon moi tai (pick_real.py).
Chay: python tools/fetch_real.py 01_danshari-kokoro
"""
import sys, io, json, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
import media_lib as ML
KEY = Path(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def api(url):
    req = urllib.request.Request(url, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def dl(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())


def used_pexels_ids(idx):
    """So den: id Pexels da len song o video khac (INDEX co used_in khac rong)."""
    return {str(e.get("source_id")) for e in idx.values()
            if e.get("source") == "pexels" and e.get("used_in")}


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sys.path.insert(0, str(vd / "_plan"))
    from queries import Q
    sl = json.load(open(PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json", encoding="utf-8"))
    cd = vd / "_cand"; cd.mkdir(exist_ok=True)
    cj = cd / "cand.json"
    cand = json.load(open(cj, encoding="utf-8")) if cj.exists() else {}
    idx = ML.load_index()
    taken = {c["id"] for v in cand.values() for c in v.get("items", [])}
    black = used_pexels_ids(idx)
    print(f"so den Pexels: {len(black)} id")
    for i, e in enumerate(sl):
        if "card" in e or "reveal" in e or str(i) in cand:
            continue
        q = Q.get(e["_shot"])
        if q is None:
            raise SystemExit(f"[LOI] shot {e['_shot']} chua co query")
        if q == "AI":
            cand[str(i)] = {"q": "AI", "items": []}
            continue
        kind, qq = (q if isinstance(q, tuple) else ("p", q))
        if kind == "v":
            r = api("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
                {"query": qq, "per_page": 12, "orientation": "landscape", "size": "medium"}))
            pool = [dict(id=v["id"], kind="video", thumb=v["image"], url=v["url"], dur=v["duration"],
                         files=[f for f in v["video_files"] if f.get("width") and f["width"] >= 1280])
                    for v in r.get("videos", [])]
            pool = [p for p in pool if p["files"] and p["dur"] >= 6]
        else:
            r = api("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
                {"query": qq, "per_page": 12, "orientation": "landscape"}))
            pool = [dict(id=p["id"], kind="photo", thumb=p["src"]["medium"], url=p["url"],
                         orig=p["src"]["original"], alt=p.get("alt", "")) for p in r.get("photos", [])]
        items = []
        for p in pool:
            if len(items) == 3:
                break
            if p["id"] in taken or str(p["id"]) in black:
                continue
            k = len(items)
            try:
                dl(p["thumb"], cd / f"{i:02d}_c{k}.jpg")
            except Exception as ex:
                print("  tai loi", p["id"], ex); continue
            items.append(p); taken.add(p["id"])
        cand[str(i)] = {"q": qq, "kind": kind, "items": items}
        print(f"slide {i:3d} shot {e['_shot']:3d} [{kind}] {qq!r}: {len(items)} ung vien")
        json.dump(cand, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(0.4)
    json.dump(cand, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    make_sheets(stem, sl, cand, cd)


def make_sheets(stem, sl, cand, cd, per=8):
    f = ImageFont.truetype("C:/Windows/Fonts/YuGothB.ttc", 22)
    shots = {s["id"]: s for s in json.load(open(PROJ / "06_VIDEO" / stem / "_plan" / "shots.json", encoding="utf-8"))}
    keys = [k for k in sorted(cand, key=int) if cand[k]["items"]]
    TW, TH, LW = 360, 203, 520
    for n in range(0, len(keys), per):
        chunk = keys[n:n + per]
        im = Image.new("RGB", (LW + 3 * TW + 40, len(chunk) * (TH + 10) + 10), (30, 30, 30))
        d = ImageDraw.Draw(im)
        for r, k in enumerate(chunk):
            y = 10 + r * (TH + 10)
            line = shots[sl[int(k)]["_shot"]]["lines"][0]
            txt = f"#{k} [{cand[k]['kind']}] {cand[k]['q']}"
            d.text((10, y), txt, font=f, fill=(255, 220, 120))
            for j in range(0, len(line), 20):
                d.text((10, y + 30 + j // 20 * 28), line[j:j + 20], font=f, fill=(235, 235, 235))
            for c in range(len(cand[k]["items"])):
                t = Image.open(cd / f"{int(k):02d}_c{c}.jpg").convert("RGB")
                t.thumbnail((TW - 10, TH))
                im.paste(t, (LW + c * TW, y))
                d.text((LW + c * TW + 6, y + 4), f"c{c}", font=f, fill=(255, 80, 80))
        im.save(cd / f"sheet_{n // per:02d}.png")
    print(f"{len(keys)} o co ung vien -> {(len(keys) + per - 1) // per} sheet")


if __name__ == "__main__":
    main()
