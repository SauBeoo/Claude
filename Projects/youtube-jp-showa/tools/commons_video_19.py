# -*- coding: utf-8 -*-
"""commons_video_19.py — CLIP QUAY THAT tren Wikimedia Commons cho video 19 (webm/ogv, license mo).
Hai nguon: (1) search `filetype:video` + tu khoa · (2) file video trong category bao tang/pho Showa (+1 tang con).
Loc: PD/CC0/CC BY/BY-SA · cao >=720 · 4-120s · so den. Xuat _cv/<key>__NN.jpg (poster) + sheet + cv_info.json.
"""
import io, sys, json, time, re
from pathlib import Path
import requests
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa"); VD = ROOT / "06_VIDEO" / "19_kaimono-joushiki"
OUT = VD / "_cv"; OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
H = {"User-Agent": "ShowaKurashiZukanBot/1.0 (https://www.youtube.com/@showa-kurashi-zukan; educational video research) python-requests"}
OK_LIC = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d?(\.\d)?( .*)?|attribution)", re.I)
BAD_LIC = re.compile(r"(nc|nd|non-?commercial|no derivatives)", re.I)
USED = set(x.strip().replace("_", " ") for x in (VD / "_cc" / "commons_used.txt").read_text(encoding="utf-8").splitlines() if x.strip())

SEARCH = {
 "v_showa_retro": ["filetype:video 昭和レトロ", "filetype:video Showa retro", "filetype:video 昭和 商店街"],
 "v_shotengai":   ["filetype:video 商店街", "filetype:video shotengai", "filetype:video shopping street Japan"],
 "v_market":      ["filetype:video 魚屋", "filetype:video fish market Japan", "filetype:video 八百屋", "filetype:video Tsukiji"],
 "v_tofu":        ["filetype:video 豆腐", "filetype:video tofu making"],
 "v_kimono":      ["filetype:video kimono", "filetype:video 着物"],
 "v_house":       ["filetype:video 民家 Japan", "filetype:video tatami room", "filetype:video Japanese old house interior"],
 "v_tv_old":      ["filetype:video television set vintage", "filetype:video ブラウン管"],
 "v_abacus_shop": ["filetype:video soroban", "filetype:video 駄菓子屋"],
 "v_alley":       ["filetype:video 路地 Japan", "filetype:video Japanese alley"],
}
CATS = {
 "c_showamuse":  ["The Showa Era Lifestyle Museum"],
 "c_edotokyo":   ["Edo-Tokyo Open Air Architectural Museum"],
 "c_bungo":      ["Bungotakada Showa no Machi"],
 "c_shitamachi": ["Shitamachi Museum"],
 "c_ameyoko":    ["Ameyoko"],
 "c_tsukiji":    ["Tsukiji fish market"],
 "c_yanaka":     ["Yanaka Ginza"],
}

def api(p):
    for k in range(5):
        try:
            r = requests.get(API, params=dict(p, format="json"), headers=H, timeout=60)
            if r.status_code == 200 and r.text.startswith("{"): return r.json()
            print("   http", r.status_code); time.sleep(6 + 6 * k)
        except Exception as e:
            print("   err", e); time.sleep(6)
    return {}

def search(q, n=30):
    j = api({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": n})
    return [x["title"] for x in j.get("query", {}).get("search", [])]

def members(cat, typ):
    j = api({"action": "query", "list": "categorymembers", "cmtitle": "Category:" + cat, "cmtype": typ, "cmlimit": 300})
    return [m["title"] for m in j.get("query", {}).get("categorymembers", [])]

def info(titles):
    out = {}
    for i in range(0, len(titles), 20):
        j = api({"action": "query", "titles": "|".join(titles[i:i+20]), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime|mediatype", "iiurlwidth": 640})
        for p in j.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [None])[0]
            if not ii or not ii.get("mime", "").startswith(("video/", "application/ogg")): continue
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "") or em.get("License", {}).get("value", "")
            out[p["title"]] = dict(url=ii["url"], thumb=ii.get("thumburl"), w=ii.get("width", 0), h=ii.get("height", 0),
                                   dur=float(ii.get("duration") or 0), license=lic,
                                   artist=re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:80],
                                   date=em.get("DateTimeOriginal", {}).get("value", "")[:20])
        time.sleep(0.5)
    return out

def keep(t, m):
    return (OK_LIC.search(m["license"]) and not BAD_LIC.search(m["license"]) and m["h"] >= 720
            and (m["dur"] == 0 or 4 <= m["dur"] <= 180) and t.replace("_", " ") not in USED)

allinfo = {}
jobs = [(k, "s", v) for k, v in SEARCH.items()] + [(k, "c", v) for k, v in CATS.items()]
for key, mode, src in jobs:
    titles = []
    for s in src:
        if mode == "s": titles += search(s)
        else:
            titles += members(s, "file")
            for sub in members(s, "subcat")[:15]:
                titles += members(sub.replace("Category:", ""), "file"); time.sleep(0.3)
        time.sleep(0.5)
    titles = [t for t in dict.fromkeys(titles) if re.search(r"\.(webm|ogv|ogg|mpg|mpeg)$", t, re.I)]
    meta = info(titles)
    cands = [(t, m) for t, m in meta.items() if keep(t, m)][:16]
    ims = []
    for i, (t, m) in enumerate(cands):
        dst = OUT / f"{key}__{i:02d}.jpg"
        if not dst.exists() and m["thumb"]:
            try:
                r = requests.get(m["thumb"], headers=H, timeout=60)
                if r.status_code == 200 and len(r.content) > 2000: dst.write_bytes(r.content)
            except Exception as e: print("   dl err", e)
            time.sleep(0.5)
        if dst.exists():
            ims.append((i, t, m, dst)); allinfo[f"{key}__{i:02d}"] = dict(title=t, **m)
    print(f"{key:14} {len(ims)} clip / {len(titles)} file video")
    if not ims: continue
    W, Hh, cols = 320, 180, 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (W * cols, (Hh + 30) * rows), "black"); d = ImageDraw.Draw(sh)
    for i, t, m, dst in ims:
        try: im = Image.open(dst).convert("RGB")
        except Exception: continue
        im.thumbnail((W, Hh)); x, y = (i % cols) * W, (i // cols) * (Hh + 30); sh.paste(im, (x, y))
        d.text((x + 3, y + Hh + 2), f"{i:02d} {m['license'][:12]} {m['w']}x{m['h']} {m['dur']:.0f}s", fill="yellow")
        d.text((x + 3, y + Hh + 15), t.replace("File:", "")[:50].encode("ascii", "replace").decode(), fill="white")
    sh.save(OUT / f"sheet_{key}.jpg", quality=85)
    (OUT / "cv_info.json").write_text(json.dumps(allinfo, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", OUT)
