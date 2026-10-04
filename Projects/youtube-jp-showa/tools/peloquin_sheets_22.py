# -*- coding: utf-8 -*-
"""peloquin_sheets_22.py — quet TOAN BO category anh Nhat 1971 cua wilford peloquin (CC BY 2.0)
thanh contact sheet 40 o/tam de chon canh CHO / TIEM / PHO / NHA cho video 19 bang MAT.
Thumb 320px, nhip cham (Commons 429 khi goi don). Ghi _p1971/index.json: so o -> title + url.
So den: bo qua file da co trong _cc/commons_used.txt (video 18 da dung).
"""
import io, sys, json, time
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / "22_kieta-shigoto"
OUT = VD / "_p1971"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
CAT = "Category:Files from wilford peloquin Flickr stream (Japan, 1971)"
USED = set(x.strip().replace("_", " ") for x in (VD / "_blacklist" / "commons_used.txt").read_text(encoding="utf-8").splitlines() if x.strip())

def api(p):
    for k in range(5):
        try:
            r = requests.get(API, params=dict(p, format="json"), headers=H, timeout=60)
            if r.status_code == 200: return r.json()
            print("http", r.status_code); time.sleep(5 + 5 * k)
        except Exception as e:
            print("err", e); time.sleep(5)
    return {}

titles, cont = [], {}
while True:
    j = api(dict({"action": "query", "list": "categorymembers", "cmtitle": CAT, "cmtype": "file", "cmlimit": 500}, **cont))
    titles += [m["title"] for m in j.get("query", {}).get("categorymembers", [])]
    if "continue" not in j: break
    cont = j["continue"]
titles = [t for t in sorted(titles) if t.replace("_", " ") not in USED]
print("files:", len(titles))

idx_p = OUT / "index.json"
idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {}
for i in range(0, len(titles), 40):
    j = api({"action": "query", "titles": "|".join(titles[i:i+40]), "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": 320})
    for p in j.get("query", {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [None])[0]
        if ii: idx.setdefault(p["title"], dict(url=ii["url"], thumb=ii.get("thumburl"), w=ii["width"], h=ii["height"]))
    time.sleep(1)
order = [t for t in titles if t in idx]
for n, t in enumerate(order):
    dst = OUT / f"{n:03d}.jpg"
    idx[t]["n"] = n
    if dst.exists(): continue
    try:
        r = requests.get(idx[t]["thumb"], headers=H, timeout=60)
        if r.status_code == 200 and len(r.content) > 2000: dst.write_bytes(r.content)
        else: print("dl", r.status_code, n); time.sleep(10)
    except Exception as e:
        print("dl err", n, e)
    time.sleep(0.6)
idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")

W, Hh, cols = 256, 170, 8
for s in range(0, len(order), 40):
    chunk = list(range(s, min(s + 40, len(order))))
    rows = (len(chunk) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 14) * rows), "black"); d = ImageDraw.Draw(sh)
    for k, n in enumerate(chunk):
        f = OUT / f"{n:03d}.jpg"
        if not f.exists(): continue
        im = Image.open(f).convert("RGB"); im.thumbnail((W, Hh))
        x, y = (k % cols) * W, (k // cols) * (Hh + 14); sh.paste(im, (x, y))
        d.text((x + 3, y + Hh + 1), f"{n:03d}", fill="yellow")
    sh.save(OUT / f"sheet_{s:03d}.jpg", quality=82)
print("OK", len(order), "->", OUT)
